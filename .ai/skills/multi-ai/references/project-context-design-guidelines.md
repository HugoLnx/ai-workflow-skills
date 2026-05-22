# Project-Context Design Guidelines

Best practices, sections, anti-patterns, and philosophy for `.ai/project-context.md`.

---

## The Project Context File

`.ai/project-context.md` is the single source of truth for project-level context — the equivalent of `CLAUDE.md` and `AGENTS.md`. It is distributed to all harnesses via symlinks (not by copying or importing).

- **One file only**: `.ai/project-context.md` — nothing else
- **Absolute maximum**: 350 lines
- **Preferred target**: under 200 lines
- **Forbidden**: `.ai/rules/`, `.cursor/rules/`, `.github/instructions/` — these folders must not exist

---

## 7-Section Template

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

---

## What to Put in Project Context
Always-loaded project context
    - description
    - stack
    - structure
    - instructions redirecting to core specialized files, MCPs and skills with triggers

---

## What NOT to Put in Project Context

| Content type | Where it belongs instead |
|---|---|
| Detailed workflows, coding conventions, testing patterns | Skill — glob-scoped `.ai/skills/<name>/` |
| Tool configuration (lint, format, typecheck) | Config files — agent reads them directly |
| Context-specific knowledge (only certain files or tasks) | Glob-scoped skill |
| Code style (ESLint, Prettier, Biome, Ruff rules) | Config files only |
| Procedural multi-step processes | Skill |
| Conditional language ("when working on X…") | Glob-scoped skill |

---

## Anti-Patterns

### Anti-Pattern: Dumping code style into project context
**Novice**: "I'll add our ESLint and Prettier rules to the project context so the agent always follows our style."
**Expert**: Code style lives in config files (`.eslintrc`, `biome.json`, `ruff.toml`, etc.). Duplicating it in prose causes drift — the config is authoritative and the agent can read it directly. Style rules in markdown become stale the moment the config changes, and they bloat always-loaded context.
**Timeline**: Pre-linter era: style guides in prose were the only option. Post-linter (2013+): config files are authoritative. LLMs can read config files directly.
**LLM mistake**: Models optimize for "the agent should know X" and reach for the nearest writable file. They don't model that every token in the project context loads on every request.
**Detection**: Project context contains `eslint-disable`, `prettier`, `biome`, `ruff`, tab-size or quote-style directives, or multi-paragraph prose about naming conventions.

### Anti-Pattern: Context-specific knowledge in always-on project context
**Novice**: "I'll add our GraphQL resolver patterns to the project context so the agent knows them."
**Expert**: `.ai/project-context.md` loads on every session — including sessions that have nothing to do with GraphQL. Context-specific knowledge belongs in a glob-scoped skill that loads only when working in the relevant context.
**Timeline**: Before agent skills existed: CLAUDE.md was the only place to put guidance. Post-skills: glob-scoped skills scope knowledge precisely to the context where it's needed.
**LLM mistake**: Models trained on monolithic config files default to "put everything in one place." They optimize for completeness at write time and don't model the instruction-budget cost at inference time.
**Detection**: Project context includes conditional language ("when working on the API…", "for TypeScript files…") or covers a domain that only applies to a subset of the codebase.

### Anti-Pattern: Multiple project-context files
**Novice**: "I'll create `.ai/rules/api-conventions.md` and `.ai/rules/testing-policy.md` for better organization."
**Expert**: `.ai/project-context.md` is the only allowed context file. Every additional always-on file costs context on every session. There are no `.ai/rules/`, `.cursor/rules/`, or `.github/instructions/` folders in the multi-ai architecture. Procedural or context-specific content belongs in skills.
**Timeline**: 2023 (early harness designs): multiple rule files were the only option → multi-ai (2024+): single project-context file enforced; context-specific content uses glob-scoped skills.
**LLM mistake**: Models pattern-match on "one concern per file" from software engineering and apply it to agent config without modelling runtime cost. Separation of concerns is valuable in code; in always-loaded config it is an anti-pattern.
**Detection**: Any `.ai/rules/` directory, `.cursor/rules/` directory, or `.github/instructions/` directory — these must not exist.
