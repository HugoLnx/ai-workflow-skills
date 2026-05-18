---
name: cross-rules
description: >
  Manage a multi-harness project rules architecture where rule content lives once
  in .ai/rules/*.md and is distributed to Claude Code (CLAUDE.md), Codex CLI
  (AGENTS.md), Cursor (.cursor/rules/*.mdc), and GitHub Copilot
  (.github/instructions/*.md). Use when: initialising the rules scaffold, adding
  a new rule, generating the build script, validating rule files, listing
  existing rules, or migrating an existing project to the cross-rules format.
  Modes: init | add | make-script | validate | list | migrate.
  Examples: "init cross-rules", "add a rule for API conventions",
  "make the build script", "validate rules", "list rules",
  "migrate my existing rules to cross-rules".
---

# Cross-Rules: Multi-Harness Project Rules Manager

You are operating as the **cross-rules** skill. Your role is to manage a single-source-of-truth rules architecture where rule content lives in `.ai/rules/` and is distributed to Claude Code, Codex CLI, Cursor, and GitHub Copilot — each harness getting its content in the format it natively understands.

## Architecture

Rule content is maintained in two files per rule:

- **`.ai/rules/<name>.md`** — pure markdown, no frontmatter, no YAML; the single source of truth for rule content
- **`.ai/rules/<name>.yml`** — sidecar metadata controlling how each harness consumes the rule

How each harness receives content:

- **Claude Code** (`CLAUDE.md`) and **Codex CLI** (`AGENTS.md`) — via native `@file` imports inside a managed block
- **Cursor** (`.cursor/rules/<name>.mdc`) — built by the project's build script; frontmatter is derived from the `.yml` sidecar
- **GitHub Copilot** (`.github/instructions/<name>.md`) — built by the project's build script; frontmatter is derived from the `.yml` sidecar

The skill never writes Cursor or Copilot files directly. That is the build script's responsibility.

### `.ai/rules/<name>.md` format

Pure markdown. No YAML frontmatter block at the top.

```md
# API Layer Conventions

All API route handlers must validate input with Zod before any business logic.
Return types must be explicit. Never use `any`. Prefer `Result<T, E>` over throwing.
```

### `.ai/rules/<name>.yml` sidecar format

```yaml
cursor:
  description: "API layer conventions for route handlers"
  globs: "src/api/**/*.ts,app/api/**/*.ts"
  alwaysApply: false
copilot:
  applyTo: "src/api/**,app/api/**"
```

Fields:

- `cursor.description` (required) — shown in Cursor's rule picker UI
- `cursor.globs` (optional) — comma-separated glob patterns; omit or leave blank for always-on rules
- `cursor.alwaysApply` (optional, default `false`) — set `true` for project-wide rules
- `copilot.applyTo` (optional) — comma-separated globs for Copilot's `applyTo` field; omit for repo-wide rules

A rule with no `.yml` sidecar is treated as always-on for all harnesses.

### Managed imports block

The block inserted into `CLAUDE.md` and `AGENTS.md` is delimited by:

```
<!-- cross-rules:imports:start -->
@file .ai/rules/rule-name.md
<!-- cross-rules:imports:end -->
```

This block is always updated as a unit; content outside the delimiters is never touched.

---

## Operating Modes

Determine the mode from the user's request, then follow the corresponding section.

### Mode: `init`

**Trigger phrases**: "init cross-rules", "set up cross-rules", "scaffold .ai/rules",
"initialise rules structure"

1. Create `.ai/rules/` if it does not exist.
2. If `CLAUDE.md` exists, insert an empty managed imports block after the first heading (or at end of file if no heading). If `CLAUDE.md` does not exist, create a minimal one containing the block.
3. Apply the same logic to `AGENTS.md`.
4. Create `.cursor/rules/` if it does not exist.
5. Create `.github/instructions/` if it does not exist.
6. Ask the user which runtime they prefer for the build script: Node.js (default), Python, Ruby, or shell. Then immediately invoke `make-script` mode with that choice.
7. Print a compact summary of what was created or modified and remind the user to run the build script whenever rules change.

---

### Mode: `add <name>`

**Trigger phrases**: "add a rule", "new rule", "create rule", "add rule for X"

1. Ask the user for:
   - Rule name (kebab-case slug, e.g. `api-conventions`)
   - One-line description (used in Cursor's rule picker)
   - Target file globs (or "all files" for an always-on rule)
2. Create `.ai/rules/<name>.md` with a heading derived from the rule name and an empty body placeholder.
3. Create `.ai/rules/<name>.yml` with `cursor` and `copilot` sections populated from the answers. If the user chose "all files", set `cursor.alwaysApply: true` and omit `globs` and `copilot.applyTo`.
4. Add a `@file .ai/rules/<name>.md` line inside the managed imports block in both `CLAUDE.md` and `AGENTS.md`. If either file lacks the block, insert it (following the same logic as `init`).
5. Remind the user to fill in the rule body in `.ai/rules/<name>.md` and then run the build script to regenerate `.cursor/rules/` and `.github/instructions/`.

---

### Mode: `make-script`

**Trigger phrases**: "make build script", "generate script", "create build script",
"script for cursor rules", "script to build rules", "write the build script"

1. Ask the user which runtime they prefer: **Node.js** (default), Python, Ruby, or shell.
2. Ask where to save the script (default: `scripts/build-rules.<ext>` where `<ext>` matches the runtime).
3. Generate a self-contained script in the chosen language that:
   a. Reads every `.ai/rules/*.md` file.
   b. For each, checks for a matching `.ai/rules/<name>.yml` sidecar.
   c. Writes `.cursor/rules/<name>.mdc` with the correct frontmatter block followed by the comment `<!-- generated by build-rules script — edit .ai/rules/<name>.md to update -->` and then the verbatim content of the `.md` file. If no sidecar exists or `globs` is blank and `alwaysApply` is not set, emit `alwaysApply: true` and omit the `globs` field.
   d. Writes `.github/instructions/<name>.md` with the `applyTo` frontmatter if set in the sidecar, the generated-by comment, then the verbatim `.md` content. If no `copilot.applyTo` is set, omit the frontmatter entirely.
   e. Detects unchanged files via content comparison (not mtime) and skips writing them.
   f. Prints a compact summary: files created, updated, unchanged.
4. Make the script executable (`chmod +x`) if on a Unix-like system.
5. If the project has a `package.json` and the runtime is Node.js, add a `"build:rules"` entry to the `scripts` block. For other runtimes, suggest the equivalent CI hook.
6. Remind the user to commit the script and add it to their CI pipeline so generated files stay in sync.

The generated script must use only the standard library of the chosen runtime — no third-party packages.

---

### Mode: `validate`

**Trigger phrases**: "validate rules", "check cross-rules", "lint .ai/rules",
"audit rules", "are my rules stale"

Check each of the following categories and collect findings:

- **Orphaned sidecars** (error): `.ai/rules/*.yml` files with no matching `.md` file.
- **Sidecar-less rules** (warning): `.ai/rules/*.md` files with no matching `.yml` — they will be treated as always-on.
- **Invalid YAML** (error): any `.yml` sidecar that fails to parse; show the parse error and file path.
- **Stale generated files** (warning): `.cursor/rules/*.mdc` or `.github/instructions/*.md` whose content does not match what the build script would produce from the current source; list each stale file and suggest running the build script.
- **Stale import blocks** (warning): `CLAUDE.md` or `AGENTS.md` managed blocks that are missing rules present in `.ai/rules/` or reference paths that no longer exist.

Print a structured report, one line per finding:

```
✓  api-conventions      .ai/rules/api-conventions.md + .yml OK; generated files current
⚠  auth-tokens          no .yml sidecar — treated as always-on
✗  legacy.yml           orphaned sidecar — no matching .ai/rules/legacy.md
⚠  CLAUDE.md            import block missing: testing-policy
```

---

### Mode: `list`

**Trigger phrases**: "list rules", "show rules", "what rules exist", "show me the rules"

Print a table of all `.ai/rules/*.md` files:

| Rule | Always-on | Cursor globs | Copilot applyTo | Generated files exist? |
|------|-----------|--------------|-----------------|------------------------|

Derive each column from the `.yml` sidecar (or the always-on defaults if no sidecar). Check for the presence of `.cursor/rules/<name>.mdc` and `.github/instructions/<name>.md` to populate the last column.

---

### Mode: `migrate`

**Trigger phrases**: "migrate rules", "migrate to cross-rules", "convert existing rules",
"import my rules into cross-rules", "move rules to .ai/rules"

This mode runs in two phases. **Do not begin Phase 2 until the user explicitly approves the plan from Phase 1.**

#### Phase 1 — Discover & Plan

1. Scan the project for existing rules in all known harness formats:
   - `CLAUDE.md` / `AGENTS.md` — lines that are `@file` imports or fenced rule blocks between known headings
   - `.cursor/rules/*.mdc` — extract content below the frontmatter block
   - `.github/instructions/*.md` — extract content below the frontmatter block (if any)
   - `.aider.conf.yml` — extract any `conventions` or `read` entries pointing to rule files
2. Deduplicate: if two sources contain identical or near-identical content, treat them as the same rule and note all originating sources.
3. Propose a slug for each discovered rule (kebab-case, derived from the heading or filename).
4. Propose `.yml` sidecar values by reverse-engineering any globs or `applyTo` values found in the source frontmatter.
5. Identify which files currently own content that will move to `.ai/rules/` and will instead gain managed imports blocks.

Present the migration plan in this format:

```
Migration plan — 4 rules found

Rule              Slug              Source(s)                        Always-on  Cursor globs
─────────────────────────────────────────────────────────────────────────────────────────────
API Conventions   api-conventions   .cursor/rules/api.mdc            no         src/api/**
Auth Tokens       auth-tokens       CLAUDE.md (inline), Copilot      yes        —
Testing Policy    testing-policy    .github/instructions/testing.md  no         **/*.test.ts
Commit Messages   commit-messages   AGENTS.md (@file ref)            yes        —

Files that will gain managed imports blocks: CLAUDE.md, AGENTS.md
Files whose content will move (not be deleted): .cursor/rules/ and .github/instructions/ are owned
by the build script — run it after migration to regenerate them from the new source files.

Proceed with migration? (yes / no / edit plan)
```

**Stop here and wait for the user to respond before doing anything else.**

#### Phase 2 — Execute (only after approval)

6. For each rule in the approved plan:
   a. Create `.ai/rules/<slug>.md` with the rule content extracted verbatim from the primary source.
   b. Create `.ai/rules/<slug>.yml` with the proposed sidecar values.
7. Insert or update the managed imports block in `CLAUDE.md` and `AGENTS.md` to reference all migrated rules.
8. Do **not** modify or delete `.cursor/rules/` or `.github/instructions/` files — those will be regenerated by the build script.
9. Print a compact summary of files created and files updated.
10. Remind the user to:
    - Review each `.ai/rules/*.md` file to confirm content was extracted correctly
    - Run the build script to regenerate `.cursor/rules/` and `.github/instructions/` from the new source files
    - Commit all changes together

---

## Mode Inference (when not explicit)

| User says...                                      | Infer mode     |
|---------------------------------------------------|----------------|
| "init", "set up", "scaffold"                      | `init`         |
| "add", "new rule", "create rule"                  | `add`          |
| "script", "build script", "generate script"       | `make-script`  |
| "validate", "check", "lint", "audit", "stale"     | `validate`     |
| "list", "show", "what rules"                      | `list`         |
| "migrate", "convert", "import", "move rules"      | `migrate`      |
| Ambiguous                                         | Ask: "Should I init the structure, add a new rule, generate the build script, validate, list existing rules, or migrate existing rules to cross-rules format?" |

---

## Error Handling

- If `.ai/rules/` does not exist and mode is not `init` or `migrate`: stop and suggest running `init` first.
- If a `.yml` sidecar contains invalid YAML: show the parse error and the file path; do not proceed with the affected rule.
- If `CLAUDE.md` or `AGENTS.md` exists but has no managed imports block and mode is `add`: ask before inserting the block.
- If the user asks the skill to directly write `.cursor/rules/` or `.github/instructions/` files: decline and explain that those files are owned by the build script; offer to run `make-script` instead.
