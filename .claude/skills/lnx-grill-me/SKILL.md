---
description: |
  Interview the user one question at a time to build a Feature or Technical Architecture
  Specification. Writes session state to .ai/grills/. Accepts @specialist skills for
  domain-enriched critiques via parallel subagents. Use when invoked as /lnx-grill-me or
  user says "grill me", "interview me", or "help me spec out".
  NOT for: implementing specs, quick Q&A, or tasks with no spec artifact needed.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Agent
---

# lnx-grill-me — as of 2026-05-21

## Description

Structured interview skill that grills the user one question at a time to produce a complete Feature or Technical Architecture Specification. Maintains persistent session files, supports pluggable domain grillers, and accepts `@specialist` skills for parallel domain critiques.

## Activate me when...

- User invokes `/lnx-grill-me [topic]` or says "grill me on X", "interview me about X", "help me spec out X"
- User wants structured help thinking through all aspects of a plan before implementing
- User supplies `@skill1 @skill2` to bring specialist knowledge into the grilling

## Do NOT activate me when...

- Implementing a spec — use the plan skill instead
- Quick one-off questions with no spec artifact needed
- User already has a finalized spec and just needs review or implementation

## References table

| File | Load when |
|---|---|
| `references/process.md` | Always — full interview flow, question protocol, session files, specialist integration, output contract |
| `references/anti-patterns.md` | Always — 4 anti-patterns specific to this skill |
| `references/feature-griller.md` | User asks for a Feature spec or describes a user-facing business capability |
| `references/technical-griller.md` | User asks for a Technical Architecture spec or system design |
| `references/game-feature-griller.md` | User asks for a game feature spec or game mechanic |
| `references/unity3d-technical-griller.md` | User asks for a Unity 3D technical spec or Unity system design |

## Minimum Knowledge

- Ask **one question per turn** — never stack multiple questions in the same turn
- Do **not** show your recommended answer until the user explicitly asks ("what do you recommend?")
- After every accepted answer: write a critic block covering potential issues, missing info, and edge cases
- Griller type unknown → ask once: "Feature spec or Technical Architecture spec?" then load the matching reference
- Session folder: `.ai/grills/yyyy-mm-dd-HH-MM-<slug>/` with `todo.md`, `knowledge.md`, `history.md`
- Consult `@specialist` subagents in **parallel** — never sequentially
