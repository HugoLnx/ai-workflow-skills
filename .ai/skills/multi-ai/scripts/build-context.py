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
    print(f"ERROR: {CONTEXT_SRC} does not exist.", file=sys.stderr)
    sys.exit(1)

created = verified = errors = 0
for link in SYMLINKS:
    link.parent.mkdir(parents=True, exist_ok=True)
    rel = Path(os.path.relpath(CONTEXT_SRC, link.parent))
    if link.is_symlink():
        if link.resolve() == CONTEXT_SRC:
            verified += 1
        else:
            link.unlink()
            link.symlink_to(rel)
            created += 1
    elif link.exists():
        print(
            f"ERROR: {link.relative_to(REPO_ROOT)} is a regular file — remove it first",
            file=sys.stderr,
        )
        errors += 1
    else:
        link.symlink_to(rel)
        created += 1

print(f"build-context complete")
print(f"  Symlinks created : {created}")
print(f"  Symlinks verified: {verified}")
if errors:
    sys.exit(1)
