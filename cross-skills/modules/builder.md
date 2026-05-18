# Module: Builder

**Invoked by**: `skill.md` when mode is `build-skill`

**Purpose**: Generate a new reusable skill file in Claude Code format and optionally
translate it to Cursor manual-activation rules, Aider CONVENTIONS.md sections,
and Codex task descriptions.

Can generate from:
- A description the user provides
- An existing task workflow the user describes
- One of the pre-built skill templates in `skills/`
- A UIR `skills[]` entry

---

## Cross-Tool Skill Layout

The recommended layout for a cross-tool skill keeps instructions in one place and
lets each harness contribute only its own frontmatter:

```
.skills/<skill-name>/content.md               ← shared instructions, no frontmatter
.claude/skills/<skill-name>/SKILL.md          ← Claude Code frontmatter only
.claude/skills/<skill-name>/content.md        ← symlink → ../../../.skills/<skill-name>/content.md
.agents/skills/<skill-name>/SKILL.md          ← Codex CLI frontmatter only
.agents/skills/<skill-name>/content.md        ← symlink → ../../../.skills/<skill-name>/content.md
.cursor/skills/<skill-name>/SKILL.md          ← Cursor frontmatter only
.cursor/skills/<skill-name>/content.md        ← symlink → ../../../.skills/<skill-name>/content.md
.github/skills/<skill-name>/SKILL.md         ← GitHub Copilot frontmatter only
.github/skills/<skill-name>/content.md       ← symlink → ../../../.skills/<skill-name>/content.md
```

**Why file-level symlinks, not directory symlinks**: Claude Code and GitHub Copilot have
known bugs where symlinking the entire skill directory (e.g. `.claude/skills/my-skill` →
`.agents/skills/my-skill`) fails discovery validation. Symlinking only the `content.md`
file inside each harness directory avoids this entirely.

**`.agents/skills/` is the cross-tool open standard**: Cursor and Copilot also recognize
`.agents/skills/`, but the explicit per-tool folders listed above are preferred because
they allow harness-specific frontmatter customization.

### Symlink Setup

**Linux / macOS** (run inside each harness skill directory):
```sh
ln -s ../../../.skills/<skill-name>/content.md content.md
```

**Windows** (run inside each harness skill directory, Command Prompt):
```cmd
mklink content.md ..\..\..\skills\<skill-name>\content.md
```

> **Windows requirements**: Developer Mode must be enabled AND `git config core.symlinks true`
> must be set. Without Developer Mode, `mklink` fails with an access-denied error.
> Without `core.symlinks true`, Git checks out symlinks as plain text files containing
> the target path string — the strategy breaks silently. Git stores symlinks as mode
> `120000` blobs; verify with `git ls-files --stage`.

---

## Frontmatter Reference

Each harness reads different frontmatter fields from a `SKILL.md`. Use this table
when writing per-harness `SKILL.md` files:

| Field | Claude Code | Codex CLI | Cursor | GitHub Copilot |
|---|---|---|---|---|
| `name` | Optional | **Required** | — (uses filename) | **Required** |
| `description` | Optional (recommended) | **Required** | Optional (recommended) | **Required** |
| `when_to_use` | Optional | ❌ Ignored | ❌ Ignored | ❌ Not documented |
| `allowed-tools` | Optional | ❌ Ignored | ❌ N/A | ❌ N/A |
| `context` (fork/inline) | Optional | ❌ Ignored | ❌ N/A | ❌ N/A |
| `agent` | Optional | ❌ Ignored | ❌ N/A | ❌ N/A |
| `effort` | Optional | ❌ Ignored | ❌ N/A | ❌ N/A |
| `disable-model-invocation` | Optional | ❌ Ignored | ❌ N/A | ❌ N/A |
| `globs` | ❌ N/A | ❌ N/A | Optional | ❌ N/A |
| `alwaysApply` | ❌ N/A | ❌ N/A | Optional | ❌ N/A |
| `applyTo` | ❌ N/A | ❌ N/A | ❌ N/A | Optional¹ |
| Unknown fields | Silently ignored | **Causes errors** | Silently ignored | Silently ignored |

¹ `applyTo` is a field in the GitHub Copilot `.github/instructions/*.instructions.md`
format — a different format from `SKILL.md`. For SKILL.md specifically, Copilot only
uses `name` + `description`.

**Critical behaviors**:
- **Codex** rejects unknown frontmatter fields with an error. Only ever include `name`
  and `description` in `.agents/skills/*/SKILL.md` files.
- **Codex** decides whether to trigger a skill based on frontmatter alone; the body
  (`content.md`) loads only after trigger. Therefore the `description` must be
  self-contained — covering both what the skill does AND when to use it. On Claude Code,
  `when_to_use` separates these concerns; on Codex, everything must be in `description`.
- **Cursor** uses `globs` for file-pattern-based auto-attachment (skill attaches
  automatically when matching files are open), in addition to semantic description matching.
- **Claude Code** fields `context: fork`, `agent`, `allowed-tools`, `effort`, and
  `disable-model-invocation` are powerful but non-portable — they must only appear in
  `.claude/skills/` SKILL.md files, never in `.agents/skills/`.

**Minimal portable frontmatter** (safe for all four harnesses, use in `.agents/skills/`):
```yaml
---
name: my-skill
description: What it does and when to use it — self-contained, one dense sentence or two.
---
```

**Claude Code extended frontmatter** (`.claude/skills/` only):
```yaml
---
name: my-skill
description: What it does
when_to_use: "More detailed trigger guidance, separated from description"
allowed-tools: Read Grep Bash
context: fork
agent: Explore
effort: low
---
```

**Cursor extended frontmatter** (`.cursor/skills/` only):
```yaml
---
description: What it does and when to use it
globs: ['src/**/*.ts', 'tests/**/*.ts']
alwaysApply: false
---
```

---

## Inputs

- **Skill name or description**: What the skill does (required)
- **Target ecosystems**: Where to generate the skill (default: `claude-code` + all others)
- **Output path**: Where to write the skill file(s)
- **Source**: `new` (generate from scratch) or `library` (adapt from `skills/` library) or `uir` (from UIR skills[] entry)
- **Scope**: Optional file glob this skill applies to (e.g. `**/*.test.ts`)

---

## Phase 1 — Skill Design

If `source: "library"`: List available skills from `skills/` directory. Let the user
choose one to adapt. Load it as the starting point.

If `source: "uir"`: Load from UIR `skills[]` by id. Use its fields as the starting point.

If `source: "new"` (or unspecified): Gather information through these questions
(ask all at once to minimize back-and-forth):

1. **Purpose**: What does this skill do? What problem does it solve?
2. **Trigger**: When should this skill be activated? What phrases or contexts trigger it?
3. **Scope**: Does it apply to all files, or specific file types/directories?
4. **Steps**: What are the sequential steps to execute this skill?
5. **Output**: What does the skill produce? (diff, report, new file, inline comments, etc.)
6. **Constraints**: What should the skill never do? Any safety boundaries?
7. **Edge cases**: Known failure modes or unusual inputs to handle?

For each question: if the user provided it in the original request, use it directly.
Only ask for missing information.

---

## Phase 2 — Skill File Generation

### Step 2a — Shared instructions file

Write `.skills/<skill-id>/content.md` (no frontmatter — instructions only):

Body sections:
- `## Purpose` — 1 paragraph: what it does, when to use it, what it produces
- `## Activation Criteria` — bulleted list of trigger phrases and contexts
- `## Steps` — numbered sequential instructions
  - Each step: imperative verb, specific action, expected result
  - Include conditional branching: "If X, then Y; else Z"
  - Reference specific files/paths when relevant
- `## Output Format` — what the model must produce (file, diff, report, structured text)
- `## Scope` — file globs or directories, or "all files"
- `## Constraints` — what the skill must never do (numbered list)
- `## Edge Cases` — known failure modes and handling instructions (bullet list)
- `## Cross-Ecosystem Notes` — how this skill translates across harnesses

### Step 2b — Claude Code harness file

Create directory `.claude/skills/<skill-id>/`.

Write `.claude/skills/<skill-id>/SKILL.md` using `templates/claude-code/skill.md.tmpl`:

```yaml
---
name: <skill-id>
description: >
  <activation trigger — 2-3 sentences covering when to invoke this skill,
   key phrases, and primary use case.>
when_to_use: "<optional extended trigger guidance>"
# allowed-tools, context, agent, effort are optional — add only if needed
---
```

Create the symlink:
- Linux/Mac: `ln -s ../../../.skills/<skill-id>/content.md .claude/skills/<skill-id>/content.md`
- Windows: `mklink .claude\skills\<skill-id>\content.md ..\..\..\skills\<skill-id>\content.md`
  (requires Developer Mode + `git config core.symlinks true`)

### Step 2c — Agents (Codex) harness file

Create directory `.agents/skills/<skill-id>/`.

Write `.agents/skills/<skill-id>/SKILL.md` with **only** `name` and `description`
(Codex rejects unknown fields with an error). The description must be self-contained:

```yaml
---
name: <skill-id>
description: >
  <what it does AND when to use it — Codex reads only this field to decide trigger;
   do NOT add when_to_use or any other field here>
---
```

Create the symlink:
- Linux/Mac: `ln -s ../../../.skills/<skill-id>/content.md .agents/skills/<skill-id>/content.md`
- Windows: `mklink .agents\skills\<skill-id>\content.md ..\..\..\skills\<skill-id>\content.md`

---

## Phase 3 — Cursor Translation

If `cursor` is in target ecosystems:

### Option A — Cursor skills directory (recommended for cross-tool content.md layout)

Create directory `.cursor/skills/<skill-id>/`.

Write `.cursor/skills/<skill-id>/SKILL.md`:

```yaml
---
description: <skill description — self-contained: what it does and when to use it>
alwaysApply: false
globs: [<scope glob if set>]  # omit if no scope
---
```

Create the symlink:
- Linux/Mac: `ln -s ../../../.skills/<skill-id>/content.md .cursor/skills/<skill-id>/content.md`
- Windows: `mklink .cursor\skills\<skill-id>\content.md ..\..\..\skills\<skill-id>\content.md`

### Option B — Cursor rules directory (legacy / standalone use)

Generate `.cursor/rules/50-skill-<skill-id>.mdc`:

```yaml
---
description: <skill description — first sentence>
alwaysApply: false
globs: [<scope glob if set>]  # omit if no scope
---
```

Body:
- Heading: `# Skill: <skill-name>`
- Brief purpose statement
- Numbered steps (from content.md Steps section, simplified for Cursor inline use)
- If the original has output format requirements: include as "Expected output:" section
- Note: `<!-- CROSS-SKILLS: Translated from skill '<skill-id>'. Activation is manual: use @50-skill-<skill-id> in your prompt. -->`

---

## Phase 3.5 — GitHub Copilot Translation

If `copilot` is in target ecosystems:

Create directory `.github/skills/<skill-id>/`.

Write `.github/skills/<skill-id>/SKILL.md` with only `name` + `description`
(Copilot silently ignores all other fields, but keeping the file minimal avoids confusion):

```yaml
---
name: <skill-id>
description: >
  <what it does and when to use it — self-contained; Copilot reads only name+description>
---
```

Create the symlink:
- Linux/Mac: `ln -s ../../../.skills/<skill-id>/content.md .github/skills/<skill-id>/content.md`
- Windows: `mklink .copilot\skills\<skill-id>\content.md ..\..\..\skills\<skill-id>\content.md`

---

## Phase 4 — Aider Translation

If `aider` is in target ecosystems:

Generate a named section to append to `CONVENTIONS.md`:

```markdown
## Skill: <Skill Name>

<!-- CROSS-SKILLS: Translated from Claude Code skill '<skill-id>'. Use /add CONVENTIONS.md and reference this section in your prompt. -->

**Purpose**: <one-line purpose>

**Steps**:
<numbered steps>

**Output**: <output format>
```

If the user has an existing `CONVENTIONS.md`, append to it rather than overwriting.
If not, create a new one with this section.

---

## Phase 5 — Codex Translation

If `codex` is in target ecosystems:

The `.agents/skills/<skill-id>/` directory + SKILL.md + symlink are created in Phase 2c.

Optionally also append a task description to `AGENTS.md` for older Codex setups that
don't yet use the `.agents/skills/` directory:

```markdown
## Task: <Skill Name>

**Purpose**: <purpose>
**Steps**:
<numbered steps>
**Output**: <output format>
```

If the user has an existing `AGENTS.md`, add under `## Available Tasks`.

---

## Phase 6 — UIR Integration (optional)

If the user wants to persist the skill in their UIR:

Add a `skills[]` entry:
```json
{
  "id": "<skill-id>",
  "name": "<Skill Name>",
  "description": "<activation trigger>",
  "instructions": "<full markdown body>",
  "scope": "<glob or null>",
  "tags": []
}
```

Write the updated UIR back to `uir.json`.

---

## Output

After generation, confirm:

```
## Skill Generated: <Skill Name>

Shared source:
- .skills/<skill-id>/content.md                    (instructions, no frontmatter)

Harness files:
- .claude/skills/<skill-id>/SKILL.md               (Claude Code frontmatter)
- .claude/skills/<skill-id>/content.md             (symlink → shared source)
- .agents/skills/<skill-id>/SKILL.md               (Codex CLI frontmatter)
- .agents/skills/<skill-id>/content.md             (symlink → shared source)
- .cursor/skills/<skill-id>/SKILL.md               (Cursor frontmatter, if requested)
- .cursor/skills/<skill-id>/content.md             (symlink → shared source, if requested)
- .github/skills/<skill-id>/SKILL.md              (Copilot frontmatter, if requested)
- .github/skills/<skill-id>/content.md            (symlink → shared source, if requested)
- CONVENTIONS.md (appended)                        (Aider, if requested)
- AGENTS.md (task section appended)                (Codex legacy, if requested)

To activate in Claude Code: invoke with the Skill tool or add to your harness.
To activate in Cursor: open a file matching the skill's globs, or type the skill name.
To activate in Aider: /add CONVENTIONS.md, then reference the skill section.
To activate in Copilot: reference the skill by name in your prompt.

Windows note: if symlinks appear as plain text files containing a path string,
run: git config core.symlinks true  and re-checkout, or enable Developer Mode.
```

---

## Pre-Built Skill Library Reference

The `skills/` directory contains these ready-to-use skills:

| File | Purpose | Key trigger phrases |
|---|---|---|
| `code-review.md` | Review changed code for bugs, style, security | "review this", "review changes", "code review" |
| `arch-analysis.md` | Extract and document architectural patterns | "analyze architecture", "document structure" |
| `debugging.md` | Systematic bug investigation workflow | "debug this", "investigate error", "find the bug" |
| `test-gen.md` | Generate tests for untested code | "generate tests", "write tests for", "add test coverage" |
| `refactoring.md` | Safe structural improvement without behavior change | "refactor this", "clean up", "restructure" |
| `docs.md` | Generate or update documentation | "document this", "generate docs", "update README" |
| `devops.md` | CI/CD, Docker, infrastructure tasks | "generate pipeline", "create Dockerfile", "set up CI" |
| `unity.md` | Unity-specific C# patterns and conventions | "unity component", "monobehaviour", "coroutine" |
| `frontend.md` | Frontend component and UI development | "create component", "frontend pattern", "UI review" |
| `backend.md` | Backend API, data, and service development | "create endpoint", "API design", "service pattern" |
| `onboarding.md` | New developer onboarding and codebase tour | "onboard", "explain the codebase", "new developer guide" |

To adapt a pre-built skill: `build-skill source:library` and select from this list.
