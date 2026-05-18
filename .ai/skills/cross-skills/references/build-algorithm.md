# Build Algorithm

Consult this file when producing a build script in any language. The algorithm is the same regardless of language; only the syntax differs.

---

## Algorithm (language-agnostic)

The script must be **idempotent** — running it multiple times produces identical results without duplicating or corrupting anything. It must **never write outside** the four harness skills folders.

```
For each subdirectory <name> in .ai/skills/:

  1. Read content.md
     → Fail loudly and skip this skill if content.md is missing

  2. For each harness in [claude, codex, cursor, copilot]:

     a. Determine target folder:
          claude  → .claude/skills/<name>/
          codex   → .agents/skills/<name>/
          cursor  → .cursor/skills/<name>/
          copilot → .github/skills/<name>/

     b. Create target folder if it does not exist

     c. Create or verify symlink:
          <target>/content.md → .ai/skills/<name>/content.md  (relative path)
        If symlink exists with correct target: verify (no-op)
        If symlink exists with wrong target: replace
        If a non-symlink file exists at that path: print error, skip

     d. For every other file or subfolder inside .ai/skills/<name>/
        (excluding .yaml files and content.md):
          Create or verify symlink at the same relative path inside <target>/

     e. Read <harness>.yaml
        → Fail loudly and skip this harness if the file is missing

     f. Build SKILL.md content:
          ---\n
          <contents of <harness>.yaml>
          ---\n
          \n
          @content.md\n

     g. Write <target>/SKILL.md only if content differs from existing file
        (compare strings before writing — skip unchanged files)

3. Print summary:
   - Skills processed
   - SKILL.md files written (skipped if unchanged)
   - Symlinks created
   - Symlinks verified (already correct)
   - Errors (exit non-zero if any)
```

---

## Language implementations

### Bash

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILLS_SRC="$SCRIPT_DIR/skills"

declare -A HARNESS_DIRS=(
  [claude]=".claude/skills"
  [codex]=".agents/skills"
  [cursor]=".cursor/skills"
  [copilot]=".github/skills"
)

for skill_dir in "$SKILLS_SRC"/*/; do
  skill_name="$(basename "$skill_dir")"
  content_src="$skill_dir/content.md"
  [ -f "$content_src" ] || { echo "ERROR: $content_src missing"; continue; }

  for harness in claude codex cursor copilot; do
    yaml_src="$skill_dir/${harness}.yaml"
    [ -f "$yaml_src" ] || { echo "ERROR: $yaml_src missing"; continue; }

    target_base="$REPO_ROOT/${HARNESS_DIRS[$harness]}/$skill_name"
    mkdir -p "$target_base"

    rel_content="$(realpath --relative-to="$target_base" "$content_src")"
    ln -sf "$rel_content" "$target_base/content.md"

    for item in "$skill_dir"/*; do
      item_name="$(basename "$item")"
      case "$item_name" in *.yaml|content.md) continue ;; esac
      ln -sf "$(realpath --relative-to="$target_base" "$item")" "$target_base/$item_name"
    done

    frontmatter="$(cat "$yaml_src")"
    printf -- "---\n%s---\n\n@content.md\n" "$frontmatter" > "$target_base/SKILL.md"
  done
done
```

### PowerShell

Key considerations:
- Use `New-Item -ItemType SymbolicLink` (requires Developer Mode or Admin)
- Compute relative paths with `[System.Uri]::MakeRelativeUri`
- Write files with `[System.IO.File]::WriteAllText` using UTF-8 without BOM
- Compare existing content before writing to implement idempotent skip

See `.ai/build-skills.ps1` for the complete implementation.

### Node.js

```js
import { readdirSync, statSync, symlinkSync, mkdirSync,
         readFileSync, writeFileSync, existsSync } from 'node:fs'
import { join, relative, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = join(fileURLToPath(import.meta.url), '..', '..')
const src  = join(root, '.ai', 'skills')
const harnesses = { claude: '.claude/skills', codex: '.agents/skills',
                    cursor: '.cursor/skills', copilot: '.github/skills' }

for (const name of readdirSync(src)) {
  const skillDir  = join(src, name)
  if (!statSync(skillDir).isDirectory()) continue
  const contentSrc = join(skillDir, 'content.md')
  if (!existsSync(contentSrc)) { console.error(`ERROR: ${contentSrc} missing`); continue }

  for (const [harness, dir] of Object.entries(harnesses)) {
    const yamlSrc = join(skillDir, `${harness}.yaml`)
    if (!existsSync(yamlSrc)) { console.error(`ERROR: ${yamlSrc} missing`); continue }

    const target = join(root, dir, name)
    mkdirSync(target, { recursive: true })

    const relContent = relative(target, contentSrc)
    symlinkSync(relContent, join(target, 'content.md'))

    for (const item of readdirSync(skillDir)) {
      if (item.endsWith('.yaml') || item === 'content.md') continue
      symlinkSync(relative(target, join(skillDir, item)), join(target, item))
    }

    const frontmatter = readFileSync(yamlSrc, 'utf8')
    const skillMd = `---\n${frontmatter}---\n\n@content.md\n`
    const dest = join(target, 'SKILL.md')
    if (!existsSync(dest) || readFileSync(dest, 'utf8') !== skillMd) {
      writeFileSync(dest, skillMd, 'utf8')
    }
  }
}
```

---

## .gitignore hint

Users may choose to ignore generated harness `SKILL.md` files and commit only `.ai/skills/`, since everything else can be rebuilt by running the script:

```gitignore
# Generated by build-skills script — rebuild with .ai/build-skills.ps1 or .ai/build-skills.sh
.claude/skills/*/SKILL.md
.agents/skills/*/SKILL.md
.cursor/skills/*/SKILL.md
.github/skills/*/SKILL.md
```

If the project uses symlinks for `content.md`, those may also be excluded since they are regenerated:

```gitignore
.claude/skills/*/content.md
.agents/skills/*/content.md
.cursor/skills/*/content.md
.github/skills/*/content.md
```
