# Skills Migration Planner

Use this reference when migrating existing harness skill configurations to the multi-ai `.ai/skills/` format.

**Also read**: `references/planner.md` for design decisions and the Rules vs Skills gate.

---

## Phase 1 — Discover

Scan all four harness skill folders for existing skills:

```
.claude/skills/*/SKILL.md
.agents/skills/*/SKILL.md
.cursor/skills/*/SKILL.md
.github/skills/*/SKILL.md
```

For each found `SKILL.md`:
1. Extract the frontmatter block (between `---` delimiters)
2. Note whether the body is inline content (already in multi-ai format) or `@content.md` directive (built with old system — regenerate by re-running `build-skills.py`)
3. If `content.md` exists as a symlink: it was created by the old build system — re-run `build-skills.py` to clean it up
4. If `content.md` is a regular file: it contains the skill body to migrate

Deduplicate: if the same skill slug exists in multiple harness folders with identical or near-identical content, treat them as one skill.

---

## Phase 2 — Plan

For each discovered skill, propose:

| Skill | Slug | Source harness(es) | Body location | Action |
|---|---|---|---|---|
| My Workflow | my-workflow | .claude/skills/ | inline SKILL.md | Extract body → content.md |
| API Guide | api-guide | .claude + .cursor | content.md (symlink) | Already split — verify target |
| Old Spec | old-spec | .github/skills/ | inline SKILL.md | Extract + apply Rules vs Skills gate |

For each skill where the body is inline or the source is unclear:
- Apply the **Rules vs Skills gate** from `references/planner.md`
- Classify: `keep as skill`, `move to rule`, or `split`

Present the full migration plan in tabular format. **Stop here and wait for user approval before Phase 3.**

---

## Phase 3 — Execute (only after approval)

For each skill to migrate:

1. Create `.ai/skills/<slug>/` directory
2. Write `.ai/skills/<slug>/content.md` — pure markdown, no frontmatter
3. Create `.ai/skills/<slug>/frontmatter/` with `claude.yaml`, `codex.yaml`, `cursor.yaml`, `copilot.yaml`
   - Extract the relevant frontmatter fields from each harness's existing `SKILL.md`
   - Consult `references/skill-frontmatter-expert.md` for valid fields per harness
   - Write only the fields recognized by that harness — strip unknowns
4. Do **not** delete or modify the existing harness skill folders yet
5. Run the build script to regenerate harness output from `.ai/skills/`
6. Verify the new harness output matches (or improves on) the original
7. Remove the old harness skill folders once verified

---

## Output Contract

```
Migration plan — N skills found

Skill             Slug            Source harness(es)      Action
──────────────────────────────────────────────────────────────────
My Workflow       my-workflow     .claude/skills/         Extract body → content.md
API Guide         api-guide       .claude + .cursor       Verify symlink target
Old Spec          old-spec        .github/skills/         → rule (apply gate)

Proceed with migration? (yes / no / edit plan)
```

Do not proceed until the user confirms.
