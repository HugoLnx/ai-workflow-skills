# Markdown Writer

Best practices for writing effective AI configuration markdown. Harness-agnostic — applies to both skills and project context.

---

## General Principles

| Do | Avoid |
|---|---|
| Concise headings that name the concept | Vague headings ("Notes", "Info", "Other") |
| Tables for multi-column comparisons | Prose lists where a table would be clearer |
| Mermaid `flowchart TD` for any branching logic | Prose descriptions of "if X then Y" flows |
| Bullet lists for enumerable items | Long prose paragraphs |
| Bold for terms being defined | Bold for emphasis throughout |
| Active imperative voice ("Run the build script") | Passive or hedged voice ("The script should be run") |

---

## Skill-Specific Practices

### Trigger Blocks

Every skill needs explicit ✅ / ❌ sections. These teach the agent when to engage and when to stay out:

```markdown
## When to use ✅
- User says "generate a skill", "create a skill for X", "new skill"
- User asks to validate harness skill folders

## When NOT to use ❌
- Editing CLAUDE.md, AGENTS.md, .cursorrules directly → redirect to lnx-multi-ai-wall
- General coding tasks unrelated to AI configuration
```

Trigger keywords must match words users actually type. NOT clauses must name specific excluded paths or scenarios.

### Description Formula

```
[What it does] [When to use it] [Trigger keywords]. NOT for [Specific exclusions].
```

Example:
> Manage AI assistant configuration across all harnesses from a single source of truth in `.ai/`. Use when editing `.ai/skills/` or `.ai/project-context.md`, designing or reviewing skills, or building harness output. NOT for writing CLAUDE.md, AGENTS.md, .cursorrules, or .github/copilot-instructions.md directly.

- 25–50 words ideal, 100 words maximum
- Semantically identical across all four harness yamls (adapted for length/field constraints)

### Anti-Pattern Block Format

```markdown
### Anti-Pattern: [Short Name]
**Novice**: "[Wrong assumption]"
**Expert**: [Why wrong + correct approach]
**Timeline**: [Date]: [old] → [Date]: [new]
**LLM mistake**: [Why models get this wrong]
**Detection**: [Concrete signal]
```

All 5 fields are required. Timelines use concrete dates or version anchors.

### Output Contract Format

```markdown
## Output: [Mode or Action Name]

**Result**: <summary of what was done>
**Files created**:
- `<path>`: <purpose>
**Next step**: <what the user should do next>
```

Document edge cases (missing input, already-exists, partial failure) after the main template.

---

## Project-Context Practices

### 7-Section Template

```markdown
# <Project Name>
<one-sentence description>

## Tech Stack
<languages, frameworks, key libs — one line each>

## Architecture
<high-level design>

## Project Structure
<key directories, one line each — no full file trees>

## Workflow Quick Overview
<3–5 bullets; link to skills for details>

## MCPs
<MCP name — what it provides; omit section if none>

## Core Skills
<@skill-name — one-line trigger; omit section if none>
```

### Line Budget Awareness

- Under 200 lines: preferred
- 200–350 lines: acceptable, monitor growth
- Over 350 lines: must trim — move content to skills

Every line in project context loads on every agent session. Write with that cost in mind.

### Declarative vs Procedural Language

Project context should be **declarative**: state what is true, what the invariants are.

```markdown
✅ Declarative: "All API routes validate input with Zod before business logic."
❌ Procedural: "When adding an API route, first import Zod, then define the schema, then..."
```

Procedural multi-step instructions belong in skills, not project context.
