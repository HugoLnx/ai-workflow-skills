#!/usr/bin/env python3
"""global-ai-skills — install, list, and remove AI skills from global harness folders."""

import argparse
import os
import shutil
import sys
from pathlib import Path

# ── Harness config ────────────────────────────────────────────────────────────

GLOBAL_HARNESSES = {
    "claude":  Path.home() / ".claude"  / "skills",
    "codex":   Path.home() / ".agents"  / "skills",
    "cursor":  Path.home() / ".cursor"  / "skills",
    "copilot": Path.home() / ".copilot" / "skills",
}

LOCAL_HARNESSES = {
    "claude":  ".claude/skills",
    "codex":   ".agents/skills",
    "cursor":  ".cursor/skills",
    "copilot": ".github/skills",
}

LOCAL_SOURCE = ".ai/skills"

HARNESS_ORDER = ("claude", "codex", "cursor", "copilot")

# ── ANSI colors ───────────────────────────────────────────────────────────────

_ANSI = {
    "claude":  "\033[31m",  # red
    "codex":   "\033[34m",  # blue
    "cursor":  "\033[32m",  # green
    "copilot": "\033[33m",  # yellow
}
_RESET = "\033[0m"
_USE_COLOR = sys.stdout.isatty() and "NO_COLOR" not in os.environ


def _color(harness: str, text: str) -> str:
    if not _USE_COLOR:
        return text
    return f"{_ANSI.get(harness, '')}{text}{_RESET}"


# ── Output rendering ──────────────────────────────────────────────────────────

def render_skill_line(name: str, presence: dict) -> str:
    """'name         | claude !codex cursor !copilot'"""
    tags = []
    for h in HARNESS_ORDER:
        label = h if presence.get(h) else f"!{h}"
        tags.append(_color(h, label))
    return f"{name:<20} | {' '.join(tags)}"


# ── list-global ───────────────────────────────────────────────────────────────

def cmd_list_global(_args):
    names: set = set()
    for folder in GLOBAL_HARNESSES.values():
        if folder.is_dir():
            names.update(p.name for p in folder.iterdir() if p.is_dir())

    if not names:
        print("No global skills found.")
        return

    for name in sorted(names):
        presence = {h: (folder / name).is_dir() for h, folder in GLOBAL_HARNESSES.items()}
        print(render_skill_line(name, presence))


# ── list-local ────────────────────────────────────────────────────────────────

def cmd_list_local(_args):
    cwd = Path.cwd()
    source_dir = cwd / LOCAL_SOURCE
    harness_dirs = {h: cwd / p for h, p in LOCAL_HARNESSES.items()}

    names: set = set()
    if source_dir.is_dir():
        names.update(p.name for p in source_dir.iterdir() if p.is_dir())
    for folder in harness_dirs.values():
        if folder.is_dir():
            names.update(p.name for p in folder.iterdir() if p.is_dir())

    if not names:
        print("No local skills found.")
        return

    for name in sorted(names):
        presence = {h: (d / name).is_dir() for h, d in harness_dirs.items()}
        print(render_skill_line(name, presence))


# ── install ───────────────────────────────────────────────────────────────────

def _make_symlink(src: Path, dst: Path) -> str:
    """Create symlink dst → src. Returns 'created', 'verified', or 'error: ...'."""
    if dst.is_symlink():
        if dst.resolve() == src.resolve():
            return "verified"
        dst.unlink()
    elif dst.exists():
        return f"error: {dst} exists and is not a symlink — remove it manually"

    try:
        rel = Path(os.path.relpath(src, dst.parent))
        dst.symlink_to(rel, target_is_directory=src.is_dir())
        return "created"
    except OSError as exc:
        if hasattr(exc, "winerror") and exc.winerror == 1314:
            return (
                "error: symlinks require Developer Mode on Windows "
                "(Settings → System → Developer Mode)"
            )
        return f"error: {exc}"


def cmd_install(args):
    source = Path(args.path).resolve()
    if not (source / "content.md").exists():
        print(
            f"Error: {source} has no content.md — not a valid skill source.",
            file=sys.stderr,
        )
        sys.exit(1)

    name = source.name
    created = verified = 0
    errors = []

    for harness, global_folder in GLOBAL_HARNESSES.items():
        skill_dir = global_folder / name
        skill_dir.mkdir(parents=True, exist_ok=True)

        # Build SKILL.md
        fm_file = source / "frontmatter" / f"{harness}.yaml"
        body = f"---\n{fm_file.read_text()}---\n\n@content.md\n" if fm_file.exists() else "@content.md\n"
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists() or skill_md.read_text() != body:
            skill_md.write_text(body)

        # Symlink content.md + optional directories
        for item_name in ("content.md", "references", "scripts"):
            src_item = source / item_name
            if not src_item.exists():
                continue
            result = _make_symlink(src_item, skill_dir / item_name)
            if result == "created":
                created += 1
            elif result == "verified":
                verified += 1
            else:
                errors.append(f"  {harness}/{item_name}: {result}")

    print(f"Installed '{name}' globally.")
    print(f"  Symlinks created : {created}")
    print(f"  Symlinks verified: {verified}")
    for err in errors:
        print(err, file=sys.stderr)
    if errors:
        sys.exit(1)


# ── remove ────────────────────────────────────────────────────────────────────

def cmd_remove(args):
    name = args.name
    removed = []
    not_found = []

    for harness, global_folder in GLOBAL_HARNESSES.items():
        skill_dir = global_folder / name
        if skill_dir.exists() or skill_dir.is_symlink():
            shutil.rmtree(skill_dir)
            removed.append(harness)
        else:
            not_found.append(harness)

    if removed:
        print(f"Removed '{name}' from: {', '.join(removed)}")
    if not_found:
        print(f"Not found in   : {', '.join(not_found)}")
    if not removed:
        sys.exit(1)


# ── replace ───────────────────────────────────────────────────────────────────

def cmd_replace(args):
    remove_args = argparse.Namespace(name=args.name)
    cmd_remove(remove_args)
    install_args = argparse.Namespace(path=args.path)
    cmd_install(install_args)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="global-ai-skills",
        description="Install, list, and remove AI skills from global harness folders.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("install", help="Install a skill globally from a source path")
    p.add_argument("path", help="Path to skill source directory (must contain content.md)")
    p.set_defaults(func=cmd_install)

    p = sub.add_parser("list-global", help="List skills installed in global harness folders")
    p.set_defaults(func=cmd_list_global)

    p = sub.add_parser("list-local", help="List skills found in the current project")
    p.set_defaults(func=cmd_list_local)

    p = sub.add_parser("remove", help="Remove a globally installed skill")
    p.add_argument("name", help="Skill name to remove")
    p.set_defaults(func=cmd_remove)

    p = sub.add_parser("replace", help="Replace a globally installed skill with a new source")
    p.add_argument("name", help="Skill name to replace")
    p.add_argument("path", help="New skill source path")
    p.set_defaults(func=cmd_replace)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
