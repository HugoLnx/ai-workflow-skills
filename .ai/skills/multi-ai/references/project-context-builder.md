# Project-Context Builder

How to build and distribute `.ai/project-context.md` to all harnesses via symlinks.

---

## Config: `.ai/config.yml`

The build script reads `.ai/config.yml` to determine which harnesses to symlink and what target filepath to use per harness. If the file is absent, all four harnesses are symlinked at their default paths.

```yaml
harnesses:
  claude:
    enabled: true
    # project_context_file_path: CLAUDE.md   # uncomment to override
```

- `enabled: false` skips the harness entirely.
- `project_context_file_path` overrides the default symlink path for that harness.
- Requires `PyYAML` (`pip install pyyaml`).

---

## Distribution Model

`.ai/project-context.md` is distributed by creating symlinks from four harness-specific paths to the single source file. All symlinks use relative paths so the repository is portable.

| Symlink | Points to |
|---|---|
| `CLAUDE.md` | `.ai/project-context.md` |
| `AGENTS.md` | `.ai/project-context.md` |
| `.cursorrules` | `.ai/project-context.md` |
| `.github/copilot-instructions.md` | `.ai/project-context.md` |

No managed imports block, no frontmatter processing, no generated files — just symlinks.

---

## Running the Build Script

```bash
python .ai/skills/multi-ai/scripts/build-context.py
```

The script is idempotent — safe to run multiple times. It creates or verifies each symlink and prints a summary.

---

## Build Script Source

```python
#!/usr/bin/env python3
"""build-context.py — symlink harness files to .ai/project-context.md"""
from pathlib import Path
import os, sys

REPO_ROOT = Path(__file__).resolve().parents[4]
CONTEXT_SRC = REPO_ROOT / ".ai" / "project-context.md"
SYMLINKS = [
    REPO_ROOT / "CLAUDE.md",
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / ".cursorrules",
    REPO_ROOT / ".github" / "copilot-instructions.md",
]

if not CONTEXT_SRC.exists():
    print(f"ERROR: {CONTEXT_SRC} does not exist.", file=sys.stderr); sys.exit(1)

created = verified = errors = 0
for link in SYMLINKS:
    link.parent.mkdir(parents=True, exist_ok=True)
    rel = Path(os.path.relpath(CONTEXT_SRC, link.parent))
    if link.is_symlink():
        if link.resolve() == CONTEXT_SRC:
            verified += 1
        else:
            link.unlink(); link.symlink_to(rel); created += 1
    elif link.exists():
        print(f"ERROR: {link.relative_to(REPO_ROOT)} is a regular file — remove it first", file=sys.stderr)
        errors += 1
    else:
        link.symlink_to(rel); created += 1

print(f"build-context complete\n  Symlinks created : {created}\n  Symlinks verified: {verified}")
if errors: sys.exit(1)
```

---

## Validate Operation

Check that the distribution is correct:

1. `.ai/project-context.md` exists (error if missing)
2. All four symlinks exist and point to `.ai/project-context.md` (error if missing or pointing elsewhere)
3. None of the four paths is a regular file instead of a symlink (error if so)
4. `.ai/rules/`, `.cursor/rules/`, `.github/instructions/` do not exist (error if they do)

Consult `references/validator.md` for the full report format.

---

## Manually Creating Symlinks

### macOS / Linux

```sh
ln -sf .ai/project-context.md CLAUDE.md
ln -sf .ai/project-context.md AGENTS.md
ln -sf .ai/project-context.md .cursorrules
mkdir -p .github && ln -sf ../.ai/project-context.md .github/copilot-instructions.md
```

### Windows (Developer Mode or Administrator)

```powershell
New-Item -ItemType SymbolicLink -Path "CLAUDE.md" -Target ".ai\project-context.md"
New-Item -ItemType SymbolicLink -Path "AGENTS.md" -Target ".ai\project-context.md"
New-Item -ItemType SymbolicLink -Path ".cursorrules" -Target ".ai\project-context.md"
New-Item -ItemType SymbolicLink -Path ".github\copilot-instructions.md" -Target "..\ai\project-context.md"
```

If symlink creation fails: see Developer Mode requirement in `references/skill-builder.md`.

---

## Editing Project Context

Always edit `.ai/project-context.md` — never edit `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, or `.github/copilot-instructions.md` directly. Those are symlinks; edits to them would modify the source file anyway, but multi-ai-wall will intercept any direct write attempts and redirect here.
