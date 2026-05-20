# Rules Migration Planner

Use this reference when migrating existing harness rule configurations to the multi-ai `.ai/rules/` format.

**Also read**: `references/planner.md` for the Rules vs Skills gate.

---

## Phase 1 — Discover

Scan the project for existing rules in all known harness formats:

- **`CLAUDE.md` / `AGENTS.md`** — inline content and `@file` imports
- **`.cursor/rules/*.mdc`** — extract content below the frontmatter block
- **`.github/instructions/*.md`** — extract content below the frontmatter block (if any)

For each discovered item:
1. Note the source harness(es) and the content
2. Deduplicate: if two sources contain identical or near-identical content, treat them as one rule
3. Propose a kebab-case slug
4. Apply the **Rules vs Skills gate** from `references/planner.md` — classify each as:
   - `root.md` — short, always-on, declarative context
   - `rule file` — always-on but genuinely separate concern
   - `→ skill` — procedural, multi-step, context-specific, or code style
5. Reverse-engineer `.yml` sidecar values from source frontmatter (globs, applyTo)

---

## Phase 2 — Plan

Present the migration plan in this format:

```
Migration plan — N items found

Rule              Slug              Source(s)                        Destination    Cursor globs
────────────────────────────────────────────────────────────────────────────────────────────────
Project Context   root              CLAUDE.md (inline)               root.md        —
Auth Tokens       auth-tokens       CLAUDE.md (inline), Copilot      root.md        —
Testing Policy    testing-policy    .github/instructions/testing.md  → skill        **/*.test.ts
API Conventions   api-conventions   .cursor/rules/api.mdc            rule file      src/api/**

Items marked "→ skill" will NOT be created as rules — offer to delegate to skill-builder after.

Proceed with migration? (yes / no / edit plan)
```

**Stop here and wait for user approval before Phase 3.**

---

## Phase 3 — Execute (only after approval)

1. For each item classified as `root.md`:
   - Consolidate content into `.ai/rules/root.md` (create if needed)
   - No `.yml` sidecar needed — `root.md` is always-on by default

2. For each item classified as `rule file`:
   - Create `.ai/rules/<slug>.md` with the extracted content
   - Create `.ai/rules/<slug>.yml` with cursor/copilot sections derived from source frontmatter

3. For items classified as `→ skill`:
   - Do **not** create rule files
   - After migration completes, offer to create skills via `references/skill-builder.md`

4. Do **not** touch `CLAUDE.md`, `AGENTS.md`, `.cursor/rules/`, or `.github/instructions/` — the build script handles those

5. Run the build script

6. Print a compact summary of files created

7. Remind the user to:
   - Review `.ai/rules/root.md` and any new rule files to confirm content was extracted correctly
   - Follow up with skill-builder for any items marked `→ skill`
   - Commit all changes together
