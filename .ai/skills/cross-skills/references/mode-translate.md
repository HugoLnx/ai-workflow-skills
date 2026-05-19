# Mode: translate

**Triggers**: "translate skill", "convert this skill", "port this skill to Cursor", "migrate skill config"

**Goal**: given an existing skill file in one harness format, produce the equivalent configs for the other three harnesses.

---

## Steps

1. **Read the source file**. Identify which harness it came from by inspecting its frontmatter fields:

   | Field present | Harness |
   |---|---|
   | `allowed-tools` or `argument-hint` | Claude Code |
   | `tools` and/or `tags` | Codex CLI |
   | `globs` or `alwaysApply` | Cursor |
   | `applyTo` | GitHub Copilot |

2. **Extract from the source**:
   - Description text (preserve verbatim)
   - Skill body (everything after the frontmatter block)
   - Any harness-specific fields (globs, tools, etc.)

3. **Map fields to the other three harnesses** — consult `references/harness-frontmatter.md` for exact field names and format per harness. Preserve the description; adapt structure.

   Mapping guide:
   - `globs` (Cursor) → use as inspiration for `applyTo` (Copilot) and `allowed-tools` scope (Claude)
   - `alwaysApply: true` (Cursor) → implies global scope → `applyTo: "**"` (Copilot)
   - `tools` (Codex) → map to closest `allowed-tools` equivalents (Claude)

4. **Write the translated `.yaml` files** into `.ai/skills/<name>/frontmatter/` (ask the user for the name if not clear from context).

5. **Check for `content.md`**:
   - If `.ai/skills/<name>/content.md` already exists: leave it unchanged.
   - If it does not exist: extract the skill body from the source file and write it to `content.md` (no frontmatter).

6. **Print a summary** of files created or updated, and remind the user to run the build script to propagate changes.
