# Mode: generate

**Triggers**: "generate a skill", "create a skill for X", "new skill", "add a skill"

**Goal**: create a complete new skill under `.ai/skills/<name>/`.

---

## Steps

1. **Gather information** — ask the user for (if not already provided):
   - Skill name (kebab-case slug, e.g. `api-conventions`)
   - What the skill does and when it should trigger (include examples of triggering phrases)
   - Which file globs it applies to, or "all files"
   - Which tools the skill needs (`Read`, `Write`, `Bash`, `WebSearch`, etc.)

2. **Create `content.md`** at `.ai/skills/<name>/content.md` — pure markdown, no frontmatter. Include:
   - One-sentence purpose statement
   - **When to use** (✅) and **when NOT to use** (❌) with specific trigger keywords and explicit exclusions
   - Step-by-step process or decision tree; use a Mermaid `flowchart` for decision trees
   - At least one anti-pattern in Novice / Expert format
   - A References section if the skill has sub-files (list them with "Consult When" descriptions)

3. **Create all four `.yaml` files** — consult `references/harness-frontmatter.md` for the exact fields and format per harness.

4. **Describe the build step** — explain how to run `.ai/build-skills.ps1` (Windows) or `.ai/build-skills.sh` (macOS/Linux) to propagate the new skill into all four harness folders. Offer to produce a build script if one does not exist yet (invoke `build-skill` mode).

5. **Print a summary** of all files created:
   ```
   Created .ai/skills/<name>/content.md
   Created .ai/skills/<name>/claude.yaml
   Created .ai/skills/<name>/codex.yaml
   Created .ai/skills/<name>/cursor.yaml
   Created .ai/skills/<name>/copilot.yaml

   Run .ai/build-skills.ps1 (Windows) or .ai/build-skills.sh (macOS/Linux)
   to propagate to harness folders.
   ```
