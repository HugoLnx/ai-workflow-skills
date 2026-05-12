---
name: arch-analysis
description: >
  Analyze and document a codebase's architectural patterns, layers, dependencies,
  and coupling. Produces an architecture document, dependency map, and ADR-style
  findings. Triggers: "analyze architecture", "document the architecture",
  "what is the structure", "explain how this is organized", "architecture review".
---

## Purpose

Survey a repository's architecture: identify layers, modules, dependency flows,
coupling points, and patterns. Produce a structured architecture document that
serves as onboarding material and a baseline for future architectural decisions.

## Activation Criteria

- User asks to analyze, describe, or document the architecture
- User asks "how is this organized?", "what are the main components?"
- User wants an architectural overview before starting a feature
- User wants to identify architectural problems or violations

## Steps

1. **Entry point scan**:
   - Read `package.json` / `Cargo.toml` / `pyproject.toml` for top-level deps
   - Read `src/index.*`, `main.*`, `app.*`, `server.*` as entry points
   - List top-level directories and infer their responsibility

2. **Layer identification**: Detect common architectural patterns:
   - **N-tier**: presentation / business logic / data access
   - **Hexagonal/Clean**: domain / application / infrastructure / adapters
   - **Feature-based**: feature modules with internal layers
   - **Micro/Modular**: independent services or packages
   - **Monolith**: single deployment unit with internal modules
   Note which pattern is dominant and where deviations exist.

3. **Dependency flow mapping**:
   - For each identified module/layer: list what it imports from other modules
   - Draw a dependency graph (as ASCII or described in text)
   - Identify: dependency direction violations (inner layers importing outer layers)
   - Identify: circular dependencies between modules
   - Identify: God modules (imported by everything, importing everything)

4. **Pattern detection**:
   - Repository/DAO pattern
   - Service layer pattern
   - Event-driven / pub-sub
   - CQRS or event sourcing
   - Factory / Builder / DI container
   - Middleware chains (Express, Django, etc.)
   Note where patterns are consistently applied vs. inconsistently applied.

5. **Coupling analysis**:
   - **Tight coupling**: direct class/function references across module boundaries
   - **Interface-based coupling**: abstraction used (good)
   - **Shared state**: global singletons, module-level state
   - **Data coupling**: shared database tables or shared data models

6. **Hotspots identification** (optional, if codebase is available):
   - Files with the most imports (high fan-in = potential God objects)
   - Files that import the most (high fan-out = potentially fragile)
   - Files changed most frequently in git history

7. **Produce architecture document**:
   ```markdown
   # Architecture: <Project Name>

   ## Overview
   <Type of architecture, primary pattern, deployment model>

   ## Layers / Modules
   | Module | Responsibility | Key files |
   |---|---|---|

   ## Dependency Flow
   <ASCII diagram or described flow>

   ## Patterns Used
   - <Pattern>: <where applied> — <consistency assessment>

   ## Coupling Issues Found
   - <Finding>: <files involved> — <recommended fix>

   ## Architectural Decisions (ADR format)
   ### Decision: <title>
   Status: <current state>
   Context: <why this decision was made>
   Consequence: <what this means for the codebase>
   ```

## Output Format

A markdown architecture document. Write to `docs/ARCHITECTURE.md` unless told otherwise.

## Scope

The entire repository. Read broadly rather than deeply.

## Constraints

- Do not refactor code — only document and analyze
- Do not propose major architectural changes without being asked
- Note uncertain findings as "appears to be" rather than stating them as facts
- Do not read every file — focus on module boundaries and entry points

## Edge Cases

- **Large monorepo**: Focus on the top-level package structure first; offer to
  dive into specific packages on request
- **No clear architecture**: Document what exists as-is; note the absence of
  a clear pattern as a finding
- **Mixed patterns**: Document each pattern and where it's used; note inconsistency

## Cross-Ecosystem Notes

- **Cursor**: Activate with `@50-skill-arch-analysis` to get contextual analysis
- **Aider**: Reference the Architecture Analysis section in CONVENTIONS.md
- **Codex**: Reference "Task: Architecture Analysis" in AGENTS.md
