# Project-Context Migration Planner

Use this reference when migrating existing harness context files to `.ai/project-context.md`.

**Also read**: `references/planner.md` for the Project-Context vs Skills gate.

---

## Phase 1 — Discover

Scan the project for existing always-on context in all known harness locations:

- **`CLAUDE.md`** — inline content (if not already a symlink to `.ai/project-context.md`)
- **`AGENTS.md`** — inline content (if not already a symlink)
- **`.cursorrules`** — inline content (if not already a symlink)
- **`.github/copilot-instructions.md`** — inline content (if not already a symlink)
- **`.cursor/rules/*.mdc`** — extract content below the frontmatter block
- **`.github/instructions/*.md`** — extract content below the frontmatter block

For each discovered item:
1. Extract the content (strip any frontmatter blocks)
2. Deduplicate: if two sources contain identical or near-identical content, treat them as one
3. Apply the **Project-Context vs Skills gate** from `references/planner.md` — classify each as:
   - `project-context` — short, always-on, declarative project information
   - `→ skill` — procedural, multi-step, context-specific, or code style

---

## Phase 2 — Plan

Present the migration plan:

```
Migration plan — N items found

Content                    Source(s)                        Destination
──────────────────────────────────────────────────────────────────────────
Project Context            CLAUDE.md (inline)               project-context.md
Tech Stack                 CLAUDE.md (inline), AGENTS.md    project-context.md
Testing Policy             .github/instructions/testing.md  → skill
API Conventions            .cursor/rules/api.mdc            → skill

Items marked "→ skill" will NOT go into project-context — offer to create skills after.

Proceed with migration? (yes / no / edit plan)
```

**Stop here and wait for user approval before Phase 3.**

---

## Phase 3 — Execute (only after approval)

1. Consolidate all `project-context` items into `.ai/project-context.md` (create if needed)
   - Follow the 7-section template from `references/project-context-design-guidelines.md`
   - Keep it declarative, lean, under 200 lines

2. For items classified as `→ skill`: do **not** add to project-context — offer to create skills via `references/skill-builder.md` after migration completes

3. Run the build script to create/update symlinks:
   ```bash
   python .ai/skills/multi-ai/scripts/build-context.py
   ```

4. If the original `CLAUDE.md`, `AGENTS.md`, etc. were regular files (not symlinks): the build script will report an error. Remove the regular files first, then re-run.

5. Print a compact summary of what was done

6. Remind the user to:
   - Review `.ai/project-context.md` to confirm content was extracted correctly
   - Follow up for any items marked `→ skill`
   - Commit all changes together
   - Delete any `.cursor/rules/` or `.github/instructions/` folders that were scanned
