# Cross-Rules: Multi-Harness Project Rules Manager

You are operating as the **cross-rules** skill. Your role is to manage a single-source-of-truth rules architecture where rule content lives in `.ai/rules/` and is distributed to Claude Code, Codex CLI, Cursor, and GitHub Copilot — each harness getting its content in the format it natively understands.

## Hard Restriction

This skill writes **only** to `.ai/rules/` source files. It never touches built files.

**Never** write to `CLAUDE.md`, `AGENTS.md`, `.cursor/rules/`, `.github/instructions/`, or any other harness-managed file. All content changes flow exclusively through `.ai/rules/` source files. After any change to `.ai/rules/`, always run the build script to propagate changes to all harness outputs.

If the user asks to edit a built file directly, decline and redirect: identify the corresponding `.ai/rules/` source file and offer to edit that instead.

The build script is the sole writer of built files. This skill is the sole writer of `.ai/rules/` source files.

---

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

## Design Philosophy

### The master root markdown

`CLAUDE.md` and `AGENTS.md` are the master root — an entry-point map the agent reads on every session. They are **not** a knowledge dump. Keep them lean.

- **Absolute maximum**: 350 lines
- **Preferred target**: under 200 lines
- **Structure**: 7 sections (omit any that don't apply yet):

```markdown
# <Project Name>
<one-sentence description>

## Tech Stack
<languages, frameworks, key libs, package manager — one line each>

## Architecture
<high-level design; e.g. "monorepo: api/ + frontend/ + shared/">

## Project Structure
<key directories, one line each — no full file trees>

## Workflow Quick Overview
<3–5 bullets; link to skills for details>

## MCPs
<MCP name — what it provides; omit section if none>

## Core Skills
<@skill-name — one-line trigger; omit section if none>
```

### Rules vs Skills decision

| Content type | Where it goes |
|---|---|
| Always-loaded project context (description, stack, structure, MCPs) | `.ai/rules/root.md` (imported into master root) |
| Short always-applicable invariants too long for root.md | `.ai/rules/<name>.md` (separate file, justify it) |
| Detailed workflows, coding conventions, testing patterns | Skill — delegate to `cross-skills` |
| Tool configuration (lint, format, typecheck) | Config files — not rules, not skills |
| Context-specific knowledge (only certain tasks or files) | Glob-scoped skill — delegate to `cross-skills` |

### What NOT to put in rules

- **Complex code style** — let the agent read lint/prettier/eslint config files directly; duplicating them in prose causes drift and wastes context.
- **Context-specific knowledge** — if it only applies when working on certain files or certain tasks, it doesn't belong in an always-on rule; use a glob-scoped skill instead.
- **Procedural workflows** — multi-step processes belong in skills, not rules.

### Prefer a single rule file

- **Ideal**: one `.ai/rules/root.md` — the master root source; no other rule files.
- **Acceptable**: one additional rule file when content is genuinely separate and always-on.
- **Avoid**: multiple rule files. Every file loads on every session. Each additional file must be explicitly justified.

---

## Operating Modes

Determine the mode from the user's request, then follow the corresponding section.

### Mode: `init`

**Trigger phrases**: "init cross-rules", "set up cross-rules", "scaffold .ai/rules",
"initialise rules structure"

The agent writes **only** to `.ai/rules/`. The build script creates/updates `CLAUDE.md` and `AGENTS.md`.

1. Create `.ai/rules/` if it does not exist.
2. **Scaffold `.ai/rules/root.md`** — the master root source file:
   - Ask the user for each of the 7 sections in the Design Philosophy template (allow "skip / fill in later" for any).
   - Write `.ai/rules/root.md` with the populated content.
   - No `.yml` sidecar needed — `root.md` is always-on by default.
3. Create `.cursor/rules/` and `.github/instructions/` if they don't exist.
4. Ask the user which runtime they prefer for the build script: Python (default), Node.js, Ruby, or shell. Invoke `make-script` mode with that choice.
5. Run the build script. It will:
   - Create `CLAUDE.md` and `AGENTS.md` with a minimal header and managed imports block if they don't exist.
   - Insert `@file .ai/rules/root.md` into the managed block.
   - Generate `.cursor/rules/root.mdc` and `.github/instructions/root.md`.
6. Print a compact summary. Clarify that `CLAUDE.md` / `AGENTS.md` were written by the build script, not by this skill.

---

### Mode: `add <name>`

**Trigger phrases**: "add a rule", "new rule", "create rule", "add rule for X"

Apply the **Rules vs Skills gate** before writing anything. All writes go to `.ai/rules/` only; the build script handles harness outputs.

1. Ask: "What do you want to add and when should it apply?"
2. Classify and route:

   | Classification | Action |
   |---|---|
   | Always-on, short, declarative | Prefer appending to `.ai/rules/root.md` over creating a new file |
   | Detailed, procedural, multi-step | Decline; offer to delegate to `cross-skills` |
   | Code style / formatting rules | Decline; direct the user to lint/prettier config files instead |
   | Context-specific (certain files or tasks only) | Decline as a rule; offer a glob-scoped skill via `cross-skills` |
   | Genuinely needs a separate rule file | Ask for justification; proceed only if user confirms it can't go in `root.md` |

3. **If appending to `root.md`**: add the content to `.ai/rules/root.md` directly; no new file, no new `.yml`.
4. **If creating a new file**: create `.ai/rules/<name>.md` and `.ai/rules/<name>.yml` with cursor/copilot sections.
5. Run the build script. It updates the managed block in `CLAUDE.md` / `AGENTS.md` and regenerates `.cursor/rules/` and `.github/instructions/`. Do not touch those files directly.

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

Check all categories below and collect findings before printing the report. Do not stop at the first error.

| Severity | Check | Description |
|---|---|---|
| error | Orphaned sidecars | `.ai/rules/*.yml` with no matching `.md` |
| error | Invalid YAML | `.yml` sidecar that fails to parse; show path and error |
| error | Master root too long | `CLAUDE.md` or `AGENTS.md` exceeds 350 lines |
| warning | Master root approaching limit | `CLAUDE.md` or `AGENTS.md` exceeds 200 lines |
| warning | Multiple rule files | More than one `.ai/rules/*.md` — prefer consolidating into `root.md` or skills |
| warning | Sidecar-less rules | `.ai/rules/*.md` with no matching `.yml` — treated as always-on |
| warning | Stale generated files | `.cursor/rules/*.mdc` or `.github/instructions/*.md` out of sync with source — re-run build script |
| warning | Stale import blocks | Managed block missing rules present in `.ai/rules/` or referencing non-existent paths |
| warning | Code style in rules | Rule body contains `eslint`, `prettier`, `biome`, `ruff`, or style-guide prose — move to config files |
| warning | Conditional content | Rule body contains "if … then …" patterns — context-specific content belongs in a skill |
| warning | Hardcoded file paths | Rule body references specific paths (e.g. `src/api/`) — staleness risk; prefer capability descriptions |
| warning | Missing master root sections | `CLAUDE.md` / `AGENTS.md` missing one or more of the 7 recommended sections |

Print one line per finding, with line counts for `CLAUDE.md` / `AGENTS.md`:

```
✓  CLAUDE.md             152 lines — within budget
⚠  AGENTS.md             224 lines — approaching 200-line preference
✗  CLAUDE.md             378 lines — exceeds 350-line hard limit
⚠  (rules)               3 rule files — prefer consolidating
⚠  api-conventions       contains eslint prose — move to .eslintrc
✗  legacy.yml            orphaned sidecar — no matching .ai/rules/legacy.md
⚠  CLAUDE.md             import block missing: testing-policy
```

End with a summary: `Validation complete: N errors, N warnings — run build script to fix stale files`

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
   - `CLAUDE.md` / `AGENTS.md` — inline content and `@file` imports
   - `.cursor/rules/*.mdc` — extract content below the frontmatter block
   - `.github/instructions/*.md` — extract content below the frontmatter block (if any)
   - `.aider.conf.yml` — extract any `conventions` or `read` entries pointing to rule files
2. Deduplicate: if two sources contain identical or near-identical content, treat them as the same rule.
3. Propose a slug for each discovered rule (kebab-case).
4. **Apply the Rules vs Skills gate** to each discovered item — classify each as:
   - `root.md` — short, always-on, declarative context
   - `rule file` — always-on but genuinely separate concern
   - `→ skill` — procedural, multi-step, context-specific, or code style
5. Propose `.yml` sidecar values by reverse-engineering globs / `applyTo` from source frontmatter.

Present the migration plan in this format:

```
Migration plan — 4 items found

Rule              Slug              Source(s)                        Destination    Cursor globs
────────────────────────────────────────────────────────────────────────────────────────────────
Project Context   root              CLAUDE.md (inline)               root.md        —
Auth Tokens       auth-tokens       CLAUDE.md (inline), Copilot      root.md        —
Testing Policy    testing-policy    .github/instructions/testing.md  → skill        **/*.test.ts
API Conventions   api-conventions   .cursor/rules/api.mdc            rule file      src/api/**

Items marked "→ skill" will NOT be created as rules — offer to delegate those to cross-skills.

Proceed with migration? (yes / no / edit plan)
```

**Stop here and wait for the user to respond before doing anything else.**

#### Phase 2 — Execute (only after approval)

6. For each item classified as `root.md` or `rule file`:
   a. `root.md` items: consolidate content into `.ai/rules/root.md` (create if needed).
   b. `rule file` items: create `.ai/rules/<slug>.md` and `.ai/rules/<slug>.yml`.
7. For items classified as `→ skill`: do **not** create rule files — offer to delegate to `cross-skills` after migration completes.
8. Do **not** touch `CLAUDE.md`, `AGENTS.md`, `.cursor/rules/`, or `.github/instructions/` — the build script handles all of those.
9. Run the build script.
10. Print a compact summary of files created.
11. Remind the user to:
    - Review `.ai/rules/root.md` and any new rule files to confirm content was extracted correctly
    - Follow up with `cross-skills` for any items marked `→ skill`
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

## Anti-Patterns

### Anti-Pattern: Dumping code style into rules
**Novice**: "I'll add our ESLint and Prettier rules to the master root so the agent always follows our style."
**Expert**: Code style lives in config files (`.eslintrc`, `biome.json`, `ruff.toml`, etc.). Duplicating it in prose causes drift — the config is the authoritative source, and the agent can read it directly. Style rules in markdown also become stale the moment the config changes, and they bloat the always-loaded context with content only relevant when writing code.
**Timeline**: Pre-linter era: style guides in prose were the only option. Post-linter (2013+): config files are authoritative. LLMs can read config files directly — no need to re-encode them in markdown.
**LLM mistake**: Models optimize for "the agent should know X" and reach for the nearest writable file (the master root). They don't model the downstream cost: every token in the master root loads on every request regardless of relevance.
**Detection**: Rule body contains `eslint-disable`, `prettier`, `biome`, `ruff`, tab-size or quote-style directives, or multi-paragraph prose about naming conventions.

### Anti-Pattern: Context-specific knowledge in always-on rules
**Novice**: "I'll add our GraphQL resolver patterns to the master root so the agent knows them."
**Expert**: Always-on rules load on every session — including sessions that have nothing to do with GraphQL. Context-specific knowledge (file-type conventions, domain patterns, deployment procedures) belongs in a glob-scoped skill that the agent loads only when working in the relevant context. Loading it always wastes the instruction budget and can cause the agent to apply irrelevant constraints.
**Timeline**: Before agent skills existed: CLAUDE.md was the only place to put guidance. Post-skills: glob-scoped skills let you scope knowledge precisely to the context where it's needed.
**LLM mistake**: Models trained on monolithic config files default to "put everything in one place." They optimize for completeness at the point of writing and don't model the instruction-budget cost at inference time.
**Detection**: Rule body includes conditional language ("when working on the API…", "for TypeScript files…") or covers a domain that only applies to a subset of the codebase.

### Anti-Pattern: Rule proliferation (many small rule files)
**Novice**: "I'll create a separate rule for commits, one for testing, one for API conventions, one for error handling…"
**Expert**: Every `.ai/rules/*.md` file loads on every session. Ten small rule files cost ten times more context than one consolidated `root.md`. The threshold for a separate file is high: the content must be genuinely distinct, always-applicable, and too long to fit in `root.md`. In most cases, consolidating into `root.md` or moving procedural content to skills reduces the always-loaded footprint dramatically.
**Timeline**: Early harness configs had no include mechanism — many files were the only option. Once `@file` imports and skills arrived, a single well-structured root + on-demand skills became the better architecture.
**LLM mistake**: Models pattern-match on "one concern per file" from software engineering principles and apply it to agent config files without modelling the runtime cost. Separation of concerns is valuable in code; in always-loaded config it is an anti-pattern unless the concerns are truly independent and equally universal.
**Detection**: More than two `.ai/rules/*.md` files; `validate` mode reports "multiple rule files" warning.

---

## Error Handling

- If `.ai/rules/` does not exist and mode is not `init` or `migrate`: stop and suggest running `init` first.
- If a `.yml` sidecar contains invalid YAML: show the parse error and the file path; do not proceed with the affected rule.
- If the user asks the skill to directly write `CLAUDE.md`, `AGENTS.md`, `.cursor/rules/`, or `.github/instructions/`: decline, explain the Hard Restriction, identify the corresponding `.ai/rules/` source file, and offer to edit that instead.
