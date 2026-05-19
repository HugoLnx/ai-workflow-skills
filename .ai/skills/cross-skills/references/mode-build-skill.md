# Mode: build-skill

**Triggers**: "build a skill", "scaffold skill", "set up skill from description", "create skill files", "make skill", "scaffold a skill with a build script"

**Goal**: given a description of what a skill should do, produce all source files AND a ready-to-run build script.

---

## Steps

1. **Gather information** — ask the user for (if not already provided):
   - Skill name (kebab-case slug) and one-line purpose
   - Target file globs, or "all files"
   - Preferred build script language:
     - **PowerShell** (default when on Windows)
     - Bash (default on macOS/Linux)
     - Node.js, Python, or Ruby (if user prefers)
   - Where to save the build script (default: `.ai/build-skills.<ext>`)

2. **Create the full `.ai/skills/<name>/` folder**:
   - `content.md` — see `references/mode-generate.md` for structure requirements
   - All four `.yaml` files inside `frontmatter/` — consult `references/harness-frontmatter.md` for fields

3. **Generate the build script** implementing the algorithm from `references/build-algorithm.md`:
   - Enumerate `.ai/skills/` subdirectories
   - For each skill and each harness: create target folder, create/verify symlinks, read `.yaml`, write `SKILL.md`
   - Skip unchanged files (compare content before writing)
   - Handle Windows symlink failures with the standard error message
   - Print a summary on completion
   - Use only the standard library of the chosen runtime — no third-party packages
   - Make executable (`chmod +x`) if generating a shell script on a Unix-like system

4. **Optional CI integration**:
   - If the project has `package.json` and the runtime is Node.js, offer to add a `"build:skills"` entry to `scripts`.
   - For other runtimes, suggest the equivalent CI step.

5. **Print a summary** of all files created and the command to run:

   ```
   Created .ai/skills/<name>/content.md
   Created .ai/skills/<name>/frontmatter/claude.yaml
   Created .ai/skills/<name>/frontmatter/codex.yaml
   Created .ai/skills/<name>/frontmatter/cursor.yaml
   Created .ai/skills/<name>/frontmatter/copilot.yaml
   Created .ai/build-skills.ps1

   Run: powershell -ExecutionPolicy Bypass -File .ai/build-skills.ps1
   ```

   Remind the user to commit the build script and add it to their CI pipeline so generated files stay in sync.
