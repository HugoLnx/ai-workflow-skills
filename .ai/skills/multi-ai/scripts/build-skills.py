#!/usr/bin/env python3
"""Build all harness SKILL.md files from .ai/skills/ source of truth.

Idempotent: safe to run multiple times.
Active harnesses and output paths are read from .ai/config.yml.
"""

import os
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[4]
SKILLS_SRC = REPO_ROOT / ".ai" / "skills"

sys.path.insert(0, str(SCRIPT_PATH.parent))
from config import load_config

_harness_config = load_config(REPO_ROOT)
HARNESSES = {name: cfg["skills_folder_path"] for name, cfg in _harness_config.items()}

skills_processed = 0
skill_mds_written = 0
symlinks_created = 0
symlinks_verified = 0
errors = 0


def make_symlink(link: Path, target: Path) -> None:
    global symlinks_created, symlinks_verified, errors
    rel = os.path.relpath(target, link.parent)
    if link.is_symlink():
        if os.readlink(link) == rel:
            symlinks_verified += 1
            return
        link.unlink()
    elif link.exists():
        print(f"ERROR: {link} exists but is not a symlink — skipping", file=sys.stderr)
        errors += 1
        return
    try:
        link.symlink_to(rel, target_is_directory=target.is_dir())
        symlinks_created += 1
    except OSError as e:
        if hasattr(e, "winerror") and e.winerror == 1314:
            print(
                "ERROR: symlink creation requires Developer Mode "
                "(Settings → System → Developer Mode) or Administrator privileges on Windows.",
                file=sys.stderr,
            )
        else:
            print(f"ERROR: could not create symlink {link} → {rel}: {e}", file=sys.stderr)
        errors += 1


def write_if_changed(path: Path, content: str) -> None:
    global skill_mds_written
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return
    path.write_text(content, encoding="utf-8")
    skill_mds_written += 1


def main() -> int:
    global skills_processed, errors

    if not SKILLS_SRC.is_dir():
        print(f"ERROR: {SKILLS_SRC} does not exist. Nothing to build.", file=sys.stderr)
        return 1

    for skill_dir in sorted(SKILLS_SRC.iterdir()):
        if not skill_dir.is_dir():
            continue

        skill_name = skill_dir.name
        content_src = skill_dir / "content.md"

        if not content_src.is_file():
            print(f"ERROR: {content_src} missing — skipping skill '{skill_name}'", file=sys.stderr)
            errors += 1
            continue

        for harness, harness_rel in HARNESSES.items():
            yaml_src = skill_dir / "frontmatter" / f"{harness}.yaml"
            if not yaml_src.is_file():
                print(
                    f"ERROR: {yaml_src} missing — skipping harness '{harness}' "
                    f"for skill '{skill_name}'",
                    file=sys.stderr,
                )
                errors += 1
                continue

            target_base = REPO_ROOT / harness_rel / skill_name
            target_base.mkdir(parents=True, exist_ok=True)

            # Symlink every child except frontmatter/
            for item in skill_dir.iterdir():
                if item.name == "frontmatter":
                    continue
                make_symlink(target_base / item.name, item)

            # Write SKILL.md
            frontmatter = yaml_src.read_text(encoding="utf-8")
            skill_md = f"---\n{frontmatter}---\n\n@content.md\n"
            write_if_changed(target_base / "SKILL.md", skill_md)

        skills_processed += 1

    print()
    print("build-skills complete")
    print(f"  Skills processed : {skills_processed}")
    print(f"  SKILL.md written : {skill_mds_written}")
    print(f"  Symlinks created : {symlinks_created}")
    print(f"  Symlinks verified: {symlinks_verified}")
    if errors:
        print(f"  Errors           : {errors} (see above)")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
