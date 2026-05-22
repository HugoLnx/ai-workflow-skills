# Skill Builder

How to build skills from `.ai/skills/` to harness output folders, generate build scripts, and validate harness output.

**Also read**: `references/skill-frontmatter-expert.md` when writing or validating frontmatter fields.

---

## Config: `.ai/config.yml`

The build script reads `.ai/config.yml` to determine which harnesses to build for and what output folder to use per harness. If the file is absent, all four harnesses are built with their default output folders.

```yaml
harnesses:
  claude:
    enabled: true
    # skills_folder_path: .claude/skills   # uncomment to override
```

- `enabled: false` skips the harness entirely.
- `skills_folder_path` overrides the default output folder for that harness.
- Requires `PyYAML` (`pip install pyyaml`).

---

## Running the Build Script

```bash
python .ai/skills/multi-ai/scripts/build-skills.py
```

The script is idempotent — safe to run multiple times. It prints a summary of SKILL.md files written and symlinks created/verified. A non-zero exit means at least one error.

---

## Build Algorithm

The script implements this algorithm (language-agnostic):

```
For each subdirectory <name> in .ai/skills/:

  1. Read content.md
     → Fail loudly and skip this skill if content.md is missing

  2. For each harness in [claude, codex, cursor, copilot]:

     a. Target folder:
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
        (excluding frontmatter/ and content.md):
          Create or verify symlink at the same relative path inside <target>/

     e. Read frontmatter/<harness>.yaml
        → Fail loudly and skip this harness if the file is missing

     f. Build SKILL.md content:
          ---\n<contents of <harness>.yaml>---\n\n@content.md\n

     g. Write <target>/SKILL.md only if content differs from existing file

  3. Print summary: skills processed, SKILL.md files written, symlinks created/verified, errors
```

---

## Symlink Strategy

All symlinks use **relative paths** so the repo is portable across machines.

### macOS / Linux

```sh
ln -s ../../../.ai/skills/<name>/content.md .claude/skills/<name>/content.md
ln -s ../../../.ai/skills/<name>/references  .claude/skills/<name>/references
```

| Harness | Target base |
|---|---|
| Claude Code | `.claude/skills/<name>/` |
| Codex CLI | `.agents/skills/<name>/` |
| Cursor | `.cursor/skills/<name>/` |
| Copilot | `.github/skills/<name>/` |

### Windows

Requires **Developer Mode** (Settings → System → Developer Mode) or Administrator privileges.

```powershell
New-Item -ItemType SymbolicLink `
  -Path ".claude\skills\<name>\content.md" `
  -Target "..\..\..\.ai\skills\<name>\content.md"
```

If symlink creation fails due to permissions, print:
> Symlinks require Developer Mode (Settings → System → Developer Mode) or Administrator privileges on Windows.

Offer to copy as a fallback, but warn the user: copies break the single-source guarantee and will not reflect future edits until the build script is re-run.

### Verifying symlinks

```sh
# macOS / Linux — list all symlinks in a harness skill folder
find .claude/skills/<name> -type l

# Windows PowerShell
Get-ChildItem ".claude\skills\<name>" -Force | Where-Object { $_.LinkType -eq 'SymbolicLink' }
```

---

## Generating a Build Script

When no build script exists yet, or the user asks for one in a specific language:

1. Ask which runtime: **Python** (default/cross-OS), Bash (macOS/Linux), Node.js
2. Ask where to save (default: `.ai/skills/multi-ai/scripts/build-skills.<ext>`)
3. Generate a self-contained script implementing the algorithm above
4. Use only the standard library — no third-party packages
5. Make executable (`chmod +x`) if generating a shell script on Unix
6. Offer to add a CI step (e.g., `"build:skills"` in `package.json` for Node.js)

### Python key implementation notes

- Resolve `REPO_ROOT` via `Path(__file__).resolve().parents[N]` (adjust N for script depth)
- Create symlinks with `Path.symlink_to(rel, target_is_directory=target.is_dir())`
- Compute relative paths with `os.path.relpath(target, link.parent)`
- Catch `OSError` with `winerror == 1314` on Windows and print the Developer Mode message
- Compare file contents with `path.read_text()` before writing to skip unchanged files

---

## Validate Operation

Audit harness skill output vs source. Consult `references/validator.md` for the full check list and report format.

Quick checks specific to skills:
- Harness `SKILL.md` size — should be tiny (frontmatter + `@content.md` only)
- All `content.md` files in harness folders are symlinks (`-type l`), not regular files
- No extra inline content in any `SKILL.md`

---

## .gitignore Hints

Users may choose to ignore generated harness files and commit only `.ai/skills/`:

```gitignore
# Generated by build-skills script
.claude/skills/*/SKILL.md
.agents/skills/*/SKILL.md
.cursor/skills/*/SKILL.md
.github/skills/*/SKILL.md

# Symlinks (regenerated by build script)
.claude/skills/*/content.md
.agents/skills/*/content.md
.cursor/skills/*/content.md
.github/skills/*/content.md
```
