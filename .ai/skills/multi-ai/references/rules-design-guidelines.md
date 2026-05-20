# Rules Design Guidelines

Best practices, sections, anti-patterns, and philosophy for `.ai/rules/` files.

---

## The Master Root

`CLAUDE.md` and `AGENTS.md` are the master root — an entry-point map the agent reads on every session. They are **not** a knowledge dump. Keep them lean.

- **Absolute maximum**: 350 lines
- **Preferred target**: under 200 lines
- **Structure** (omit any section that doesn't apply yet):

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

## Prefer a Single Rule File

- **Ideal**: one `.ai/rules/root.md` — the master root source; no other rule files.
- **Acceptable**: one additional rule file when content is genuinely separate and always-on.
- **Avoid**: multiple rule files. Every file loads on every session. Each additional file must be explicitly justified.

Threshold for a separate file: the content must be genuinely distinct, always-applicable, and too long to fit in `root.md`.

---

## What NOT to Put in Rules

| Content type | Where it belongs instead |
|---|---|
| Always-loaded project context (description, stack, structure, MCPs) | `.ai/rules/root.md` |
| Short always-applicable invariants | Append to `root.md` (prefer over new file) |
| Detailed workflows, coding conventions, testing patterns | Skill — use `multi-ai/skill-builder` |
| Tool configuration (lint, format, typecheck) | Config files — not rules, not skills |
| Context-specific knowledge (only certain tasks or files) | Glob-scoped skill |
| Code style (ESLint, Prettier, Biome, Ruff rules) | Keep in config files — agent can read them directly |
| Procedural multi-step processes | Skill |
| Conditional language ("when working on X…") | Glob-scoped skill |

---

## Anti-Patterns

### Anti-Pattern: Dumping code style into rules
**Novice**: "I'll add our ESLint and Prettier rules to the master root so the agent always follows our style."
**Expert**: Code style lives in config files (`.eslintrc`, `biome.json`, `ruff.toml`, etc.). Duplicating it in prose causes drift — the config is authoritative and the agent can read it directly. Style rules in markdown also become stale the moment the config changes, and they bloat always-loaded context.
**Timeline**: Pre-linter era: style guides in prose were the only option. Post-linter (2013+): config files are authoritative. LLMs can read config files directly — no need to re-encode them in markdown.
**LLM mistake**: Models optimize for "the agent should know X" and reach for the nearest writable file (the master root). They don't model the downstream cost: every token in the master root loads on every request.
**Detection**: Rule body contains `eslint-disable`, `prettier`, `biome`, `ruff`, tab-size or quote-style directives, or multi-paragraph prose about naming conventions.

### Anti-Pattern: Context-specific knowledge in always-on rules
**Novice**: "I'll add our GraphQL resolver patterns to the master root so the agent knows them."
**Expert**: Always-on rules load on every session — including sessions that have nothing to do with GraphQL. Context-specific knowledge belongs in a glob-scoped skill that loads only when working in the relevant context. Loading it always wastes the instruction budget and can cause the agent to apply irrelevant constraints.
**Timeline**: Before agent skills existed: CLAUDE.md was the only place to put guidance. Post-skills: glob-scoped skills let you scope knowledge precisely to the context where it's needed.
**LLM mistake**: Models trained on monolithic config files default to "put everything in one place." They optimize for completeness at write time and don't model the instruction-budget cost at inference time.
**Detection**: Rule body includes conditional language ("when working on the API…", "for TypeScript files…") or covers a domain that only applies to a subset of the codebase.

### Anti-Pattern: Rule proliferation (many small rule files)
**Novice**: "I'll create a separate rule for commits, one for testing, one for API conventions, one for error handling…"
**Expert**: Every `.ai/rules/*.md` file loads on every session. Ten small rule files cost ten times more context than one consolidated `root.md`. The threshold for a separate file is high: the content must be genuinely distinct, always-applicable, and too long to fit in `root.md`. In most cases, consolidating into `root.md` or moving procedural content to skills is the better architecture.
**Timeline**: Early harness configs had no include mechanism — many files were the only option. Once `@file` imports and skills arrived, a single well-structured root + on-demand skills became the better architecture.
**LLM mistake**: Models pattern-match on "one concern per file" from software engineering and apply it to agent config files without modelling the runtime cost. Separation of concerns is valuable in code; in always-loaded config it is an anti-pattern unless concerns are truly independent and equally universal.
**Detection**: More than two `.ai/rules/*.md` files; validate mode reports "multiple rule files" warning.
