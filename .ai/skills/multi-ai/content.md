# multi-ai — as of 2026-05-20

You are the **multi-ai** skill. Your role is to manage AI assistant configuration across Claude Code, OpenAI Codex CLI, Cursor, and GitHub Copilot — all from a single source of truth under `.ai/`.

## When to Use ✅

- Editing or creating files under `.ai/skills/` or `.ai/project-context.md`
- Designing, reviewing, or planning skills or project context
- Building harness output from `.ai/` source files
- Migrating existing harness configurations to the multi-ai format
- Initializing a project for the first time in multi-ai format
- Validating that the project structure matches the multi-ai spec
- Redirected here by `multi-ai-wall`

## When NOT to Use ❌

- Writing directly to `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `.github/copilot-instructions.md`, `.cursor/skills/`, `.claude/skills/`, `.agents/skills/`, or `.github/skills/` — those are managed outputs; `multi-ai-wall` will intercept these
- Translating a skill from one harness format to another (harness-A → harness-B) — not in scope
- General coding tasks unrelated to AI configuration

---

## Explicit Load Rule

**Always load** `references/core.md` first. Load all other references explicitly based on the task table below. Do not pre-load references that are not needed for the current task.

References must be loaded explicitly — they are not auto-loaded. Each reference file declares its own transitive dependencies inline.

---

## Task → References Routing Table

| Task | References to load |
|---|---|
| Edit or write skill **content** | `core`, `markdown-writer` |
| Edit or write skill **frontmatter** | `core`, `skill-frontmatter-expert` |
| Edit **project context** | `core`, `project-context-builder` |
| **Design or review** a skill | `core`, `planner` → then `skill-design-guidelines` |
| **Design project context** content | `core`, `planner` → then `project-context-design-guidelines` |
| **Migrate** existing harness skill to `.ai/skills/` | `core`, `skills-migration-planner` → `planner` → `skill-design-guidelines` |
| **Migrate** existing context to `.ai/project-context.md` | `core`, `project-context-migration-planner` → `planner` → `project-context-design-guidelines` |
| **Initialize** project (no existing config) | `core`, `init-planner` → `planner` |
| **Initialize** project (existing config) | `core`, `init-planner` → `planner` + `skills-migration-planner` + `project-context-migration-planner` |
| **Build** skills to harness output | `core`, `skill-builder` → `skill-frontmatter-expert` |
| **Build** project-context symlinks | `core`, `project-context-builder` |
| **Validate** project structure | `core`, `validator` |

Arrows (`→`) indicate that the left reference will instruct you to also read the right reference when relevant. Load them in order.

---

## References

Read only the files relevant to the current task — do not pre-load all references.

| File | When to load |
|---|---|
| `references/core.md` | Always — folder structure and equivalences |
| `references/planner.md` | Designing or reviewing a skill or project context |
| `references/skill-design-guidelines.md` | Designing skills (load alongside planner) |
| `references/project-context-design-guidelines.md` | Designing project context (load alongside planner) |
| `references/markdown-writer.md` | Writing skill or project context content |
| `references/skill-frontmatter-expert.md` | Writing or validating skill frontmatter |
| `references/skill-builder.md` | Building skills to harness output |
| `references/project-context-builder.md` | Building project-context symlinks |
| `references/skills-migration-planner.md` | Migrating existing harness skill configs |
| `references/project-context-migration-planner.md` | Migrating existing harness context files |
| `references/init-planner.md` | Initializing a project in multi-ai format |
| `references/validator.md` | Validating project structure |
