# Init Planner

Use this reference when initializing a project in the multi-ai format from scratch, or when setting it up for the first time in a repo that may have existing agent configuration.

**Also read**:
- `references/planner.md` — always; provides the Rules vs Skills gate and plan generation
- `references/skills-migration-planner.md` — if existing harness skill configurations are found
- `references/rules-migration-planner.md` — if existing harness rule configurations are found

---

## Step 1 — Detect Existing Configuration

```mermaid
flowchart TD
  Start[Start init] --> ScanSkills{Harness skill folders\nexist and non-empty?}
  ScanSkills -->|Yes| MigrateSkills[Use skills-migration-planner\nto plan skill migration]
  ScanSkills -->|No| ScanRules{Harness rule files\nexist?}
  MigrateSkills --> ScanRules
  ScanRules -->|Yes| MigrateRules[Use rules-migration-planner\nto plan rules migration]
  ScanRules -->|No| FreshSetup[Fresh setup:\nscaffold root.md\nand first skill]
  MigrateRules --> Coordinate[Coordinate plan\nwith planner]
  FreshSetup --> Coordinate
```

### What to scan for

| Location | What it indicates |
|---|---|
| `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/` | Existing harness skills to migrate |
| `CLAUDE.md`, `AGENTS.md` | Master root content to migrate to `.ai/rules/root.md` |
| `.cursor/rules/*.mdc`, `.github/instructions/*.md` | Harness-specific rules to migrate |
| `.ai/skills/`, `.ai/rules/` | Already in multi-ai format — validate instead of init |

If `.ai/skills/` or `.ai/rules/` already exist: stop and suggest running the `validator` instead.

---

## Step 2 — Fresh Setup (no existing config)

If no existing harness configuration is found:

1. Ask the user for each of the 7 master root sections (allow "skip / fill later" for any):
   - Project name + one-sentence description
   - Tech Stack
   - Architecture
   - Project Structure
   - Workflow Quick Overview
   - MCPs (if any)
   - Core Skills (if any)

2. Create `.ai/rules/root.md` with the populated content

3. Ask which runtime they prefer for the rules build script: Python, Node.js, Ruby, or shell — then coordinate with `rules-builder` to generate it

4. Ask whether they want to create an initial skill now — if yes, coordinate with `planner` to design it and `skill-builder` to generate the build script

5. Run the build script(s)

6. Print a summary of all files created and next steps

---

## Step 3 — Coordinate the Full Plan

Whether fresh or migrating, produce a consolidated plan before executing:

```
Init plan for <project>

Phase 1 — Rules migration (N items)
  [table from rules-migration-planner if applicable]

Phase 2 — Skills migration (N skills)
  [table from skills-migration-planner if applicable]

Phase 3 — Fresh content
  Create .ai/rules/root.md with: <sections listed>
  Create .ai/skills/<name>/ for: <skill listed>

Proceed? (yes / no / edit plan)
```

Do not execute any phase until the user approves the full plan.
