# Module: Translator

**Invoked by**: `skill.md` when mode is `translate`

**Purpose**: Parse an existing ecosystem's config files into a UIR document, then
delegate to the generator module to produce output for the target ecosystem.
Annotates all fidelity losses with `_degraded` flags and `CROSS-SKILLS: DEGRADED`
comments in the output.

---

## Inputs

- **Source ecosystem**: One of `claude-code`, `cursor`, `codex`, `aider`
- **Source path**: Directory containing the source config files
- **Target ecosystem(s)**: One or more of `claude-code`, `cursor`, `codex`, `aider`
- **Output path**: Where to write generated target configs (default: `<source-path>/<target-ecosystem>/`)
- **Save UIR**: Whether to write the intermediate `uir.json` (default: yes, to `<source-path>/uir.json`)

If source ecosystem is not specified, auto-detect by checking for:
- `CLAUDE.md` or `.claude/` → `claude-code`
- `.cursor/rules/` directory with `.mdc` files → `cursor`
- `AGENTS.md` with OpenAI-style structure → `codex`
- `.aider.conf.yml` → `aider`
- `.github/skills/` directory → `copilot`

---

## Phase 1 — Source Parsing

### Parser: `claude-code`

Read files in this order:

**CLAUDE.md** (root and nested)
1. Parse H1 as `meta.name`
2. Parse `## Project Overview` / `## Overview` section → `context.project_summary`
3. Parse `## Tech Stack` table → `context.tech_stack[]`
4. Parse `## Directory Layout` table → `context.directory_layout`
5. Parse `## Build` / `## Commands` section → `context.build_commands`
6. Parse `## Environment Variables` table → `context.environment_variables[]`
7. Parse `## AI Behavior Rules` subsections → `rules[]`
   - Each `###` heading → `category`
   - Each bullet → `content`; extract italic sub-bullet as `rationale`
   - Fenced code blocks after bullets → `examples.good` or `examples.bad`
   - Assign scope: `global`, priority: `5` (default)
8. Parse `## File-Specific Rules` → rules with `scope: "file-glob"`, `scope_value: <heading text>`
9. Parse `@import path/to/file` directives → recurse into those files
10. Assign a sequential `id` based on category + index: `code-style-001`, etc.

**AGENTS.md** (if present)
- Parse each `## AgentName` section → one `agents[]` entry
- Extract `**Role**:` → `role`
- Extract `**Scope**:` → `scope`
- Extract `**Allowed tools**:` → `tools_allowed[]`
- Remaining body → `instructions`

**settings.json** (if present)
- `permissions.allow[]` → `permissions.allow[]`
- `permissions.deny[]` → `permissions.deny[]`
- `hooks[]` → extract and map to `hooks[]`
  - Claude Code hooks format: `{ "event": ..., "matcher": ..., "hooks": [{ "command": ... }] }`
  - Map to UIR hook: `{ "event": ..., "matcher": ..., "command": ... }`
- `env` → `context.environment_variables[]` (merge with existing, no overwrite)

**`.claude/skills/`** (if present — supports both layouts)

*Directory layout* (`.claude/skills/<id>/SKILL.md` + `content.md`):
- Parse `SKILL.md` frontmatter: `name` → `id` and `name`; `description` → `description`; `when_to_use` → stored separately
- Read `content.md` (follow symlink if it is one) → `instructions`
- Add to `skills[]`

*Flat layout* (`.claude/skills/<id>.md` or legacy `skills/<id>.md`):
- Parse frontmatter `name` → `id` and `name`
- Parse frontmatter `description` → `description`
- Parse body → `instructions`
- Add to `skills[]`

---

### Parser: `cursor`

Read all `.mdc` files in `.cursor/rules/`:

For each file:
1. Parse YAML frontmatter: `description`, `alwaysApply`, `globs`
2. Parse body as rules:
   - Each numbered/bulleted item → one rule `content`
   - `> **Why**: ...` blockquote → `rationale`
   - Fenced code blocks in context → `examples`
3. Map to UIR:
   - `alwaysApply: true`, no globs → `scope: "global"`
   - `alwaysApply: false`, with globs → `scope: "file-glob"`, `scope_value: globs[0]`
   - `alwaysApply: false`, no globs → `scope: "task-type"` (manual activation hint)
4. Set `priority`:
   - File named `00-*` or `critical` → priority 2
   - File named `01-*` or `conventions` → priority 5
   - File named `02-*` or `suggestions` → priority 8
   - Otherwise: priority 5
5. Set `category` from file name if parseable (e.g. `10-testing.mdc` → category `testing`)
6. Assign `id` as `<filename-without-ext>-<index>`

**Note**: Parse `index.mdc` last; use its content to populate `context` fields if not already filled.

Degradation notes to add to UIR:
- No permissions found → `_degraded: true`, `_degraded_reason: "Cursor has no native permissions; check if rules contained deny-style instructions"`
- No hooks found → `_degraded: true`, `_degraded_reason: "Cursor has no native hooks"`

---

### Parser: `codex`

Read `AGENTS.md` (OpenAI format):

1. Parse intro before first `##` → `context.project_summary`
2. Parse `## Context` section:
   - Tech stack list → `context.tech_stack[]`
   - Directory layout → `context.directory_layout`
   - Build commands → `context.build_commands`
3. Parse `## Instructions` section:
   - Each numbered item → one rule with `scope: "global"`, `priority: 5`
   - Note: all rules from Codex are global (scope lost) → add `_degraded: true`
4. Parse `## <AgentName>` sections (excluding Context and Instructions):
   - `**Role**:` → `role`
   - `**Instructions**:` → `instructions`
   - `**Tools**:` → `tools_allowed[]`
   - → one `agents[]` entry
5. Parse `## Available Tasks` section → `skills[]`
   - Each `### TaskName` → one skill with `name` from heading, `instructions` from body

Degradation notes:
- All rules will have `_degraded: true`, `_degraded_reason: "Codex AGENTS.md does not support file-glob scoping; original scope is unknown"`

---

### Parser: `aider`

Read `.aider.conf.yml`:
1. `model` → `extensions.aider.model`
2. `read[]` → `memory.always_load[]`
3. `auto-commits` → `extensions.aider.auto_commits`
4. `commit-prompt` → `rules[]` entry with `category: "git"`, `scope: "task-type"`, `scope_value: "commit-message"`

Read `CONVENTIONS.md`:
1. Extract `## <Category>` sections → map to rule categories
2. Each numbered item within a section → one rule
3. Italic sub-items → `rationale`
4. Assign `scope: "global"`, `priority: 5`

Read `.aiderignore`:
1. Non-comment, non-empty lines → `ignore_patterns[]`

Degradation notes:
- All rules are global (no scoping in Aider) → `_degraded: true` on rules that had scope annotations
- No permissions, hooks, or sub-agents extractable from Aider format

---

### Parser: `copilot`

Read all `.github/skills/*/SKILL.md` files:

For each file:
1. Parse YAML frontmatter: `name` → `id` and `name`; `description` → `description`
2. Look for `content.md` in the same directory (may be a symlink):
   - If it exists and is a symlink: resolve target path and read content → `instructions`
   - If it exists and is a regular file: read content → `instructions`
   - If absent: use empty `instructions`; note in gap summary
3. Add to `skills[]`

Note: Copilot SKILL.md files carry only `name` + `description`. Any richer metadata
(`when_to_use`, `allowed-tools`, scope, etc.) is absent. Mark all parsed skills as
`_degraded: true`, `_degraded_reason: "Copilot format carries only name+description; when_to_use and allowed-tools are unavailable"`.

Also check for `.github/copilot-instructions.md` (Copilot project-level instructions):
- If present, extract body → one `rules[]` entry with `scope: "global"`, `category: "agent-behavior"`, `priority: 5`
- Mark `_degraded: true`, `_degraded_reason: "Parsed from .github/copilot-instructions.md — structured rule categories unavailable"`

Degradation notes to add to UIR:
- No permissions found → `_degraded_reason: "Copilot has no native permissions"`
- No hooks found → `_degraded_reason: "Copilot has no lifecycle hooks"`
- No agents found → `_degraded_reason: "Copilot has no sub-agent definitions"`

---

## Phase 2 — UIR Normalization

After parsing:

1. **Deduplicate rules**: Remove exact duplicate `content` values; keep the one with more metadata.
2. **Assign missing IDs**: Any rule without an `id` gets `<category>-<padded-index>`.
3. **Set missing priorities**: Default to 5.
4. **Set missing categories**: Default to `agent-behavior`.
5. **Validate uniqueness**: Ensure `rules[].id`, `agents[].id`, `skills[].id` are unique within UIR.
6. **Merge ignore patterns**: Combine `ignore_patterns[]` and `memory.ignore[]` and deduplicate.
7. **Set meta**:
   - `meta.id`: new UUID v4
   - `meta.generated_at`: current timestamp
   - `meta.source.method`: `"translate"`
   - `meta.source.from_ecosystem`: source ecosystem id
   - `meta.version`: `"1.0.0"`

---

## Phase 3 — Delegation to Generator

After producing the normalized UIR:

1. Optionally save UIR to `<source-path>/uir.json` (or user-specified path).
2. Invoke the generator module instructions with:
   - UIR = the just-produced document
   - Target ecosystems = as specified by user
   - Output directory = as specified by user
3. The generator will handle all template rendering and degradation annotation.

---

## Translation Gap Summary

After generation completes, print a gap summary:

```
## Translation Summary: <source-ecosystem> → <target-ecosystem(s)>

### Transferred with full fidelity
- <N> global rules
- <N> agents
- Tech stack, directory layout, build commands

### Degraded (functionality reduced)
- <N> hooks → converted to rule text in Cursor / dropped in Codex,Aider
- <N> permission entries → converted to rule text (no enforcement)
- <N> file-glob scoped rules → flattened to global rules in Codex,Aider
- <N> sub-agent definitions → flattened to context in Cursor,Aider

### Dropped (no equivalent)
- <N> lifecycle hook commands (Codex, Aider)
- <N> environment variable definitions (Cursor, Codex)

See CROSS-SKILLS: DEGRADED and CROSS-SKILLS: NOT TRANSLATABLE comments in output files.
Consult schema/capability-matrix.json for the full capability matrix.
```
