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

## Phase 2 — Skill File Generation (Claude Code)

Populate `templates/claude-code/skill.md.tmpl` with:

```yaml
---
name: <skill-id>  # slugified from skill name
description: >
  <activation trigger — 2-3 sentences covering when to invoke this skill,
   key phrases, and primary use case. This text is shown in system-reminder
   and drives automatic triggering.>
---
```

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
- `## Cross-Ecosystem Notes` — how this skill translates to Cursor/Codex/Aider

Output path: `<output-path>/<skill-id>.md`

---

## Phase 3 — Cursor Translation

If `cursor` is in target ecosystems:

Generate `50-skill-<skill-id>.mdc`:

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
- Numbered steps (from skill Steps section, simplified for Cursor inline use)
- If the original has output format requirements: include as "Expected output:" section
- Note: `<!-- CROSS-SKILLS: Translated from Claude Code skill '<skill-id>'. Activation is manual: use @50-skill-<skill-id> in your prompt. -->`

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

Generate a task description section for `AGENTS.md`:

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

Files written:
- <output-path>/<skill-id>.md          (Claude Code)
- .cursor/rules/50-skill-<id>.mdc      (Cursor, if requested)
- CONVENTIONS.md (appended)            (Aider, if requested)
- AGENTS.md (task section appended)    (Codex, if requested)

To activate in Claude Code: invoke with the Skill tool or add to your harness.
To activate in Cursor: type @50-skill-<id> in a prompt.
To activate in Aider: /add CONVENTIONS.md, then reference the skill section.
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
