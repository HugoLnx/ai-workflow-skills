#!/usr/bin/env python3
"""lnx-ai-global-skills — install, list, and remove AI skills from global harness folders."""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

# ── Harness config ────────────────────────────────────────────────────────────

GLOBAL_HARNESSES = {
    "claude":  Path.home() / ".claude"  / "skills",
    "codex":   Path.home() / ".agents"  / "skills",
    "cursor":  Path.home() / ".cursor"  / "skills",
    "copilot": Path.home() / ".copilot" / "skills",
}

GLOBAL_AI_FOLDER = Path.home() / ".ai" / "skills"

LOCAL_HARNESSES = {
    "claude":  ".claude/skills",
    "codex":   ".agents/skills",
    "cursor":  ".cursor/skills",
    "copilot": ".github/skills",
}

LOCAL_SOURCE = ".ai/skills"

HARNESS_ORDER = ("ai", "claude", "codex", "cursor", "copilot")

# ── ANSI colors ───────────────────────────────────────────────────────────────

_ANSI = {
    "ai":      "\033[35m",  # magenta
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
    """'name         | ai claude !codex cursor !copilot'"""
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
    if GLOBAL_AI_FOLDER.is_dir():
        names.update(p.name for p in GLOBAL_AI_FOLDER.iterdir() if p.is_dir() or p.is_symlink())

    if not names:
        print("No global skills found.")
        return

    for name in sorted(names):
        presence = {h: (folder / name).is_dir() for h, folder in GLOBAL_HARNESSES.items()}
        presence["ai"] = (GLOBAL_AI_FOLDER / name).exists()
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
        presence["ai"] = (source_dir / name).is_dir()
        print(render_skill_line(name, presence))


# ── link-as-global ────────────────────────────────────────────────────────────

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


def _link_one_skill(source: Path) -> bool:
    """Link a single skill source to all global harness folders and ~/.ai/skills/. Returns True on success."""
    if not (source / "content.md").exists():
        print(
            f"Error: {source} has no content.md — not a valid skill source.",
            file=sys.stderr,
        )
        return False

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

    # Symlink the whole source directory into ~/.ai/skills/
    GLOBAL_AI_FOLDER.mkdir(parents=True, exist_ok=True)
    ai_result = _make_symlink(source, GLOBAL_AI_FOLDER / name)
    if ai_result == "created":
        created += 1
    elif ai_result == "verified":
        verified += 1
    else:
        errors.append(f"  ~/.ai/skills/{name}: {ai_result}")

    print(f"Linked '{name}' globally.")
    print(f"  Symlinks created : {created}")
    print(f"  Symlinks verified: {verified}")
    for err in errors:
        print(err, file=sys.stderr)
    return not errors


def cmd_link_as_global(args):
    ok = True
    for path_str in args.paths:
        source = Path(path_str).resolve()
        if not _link_one_skill(source):
            ok = False
    if not ok:
        sys.exit(1)


# ── copy-from-global ──────────────────────────────────────────────────────────

def cmd_copy_from_global(args):
    cwd = Path.cwd()
    local_ai = cwd / LOCAL_SOURCE
    local_ai.mkdir(parents=True, exist_ok=True)

    for name in args.names:
        src_link = GLOBAL_AI_FOLDER / name
        if not src_link.exists():
            print(f"Error: '{name}' not found in {GLOBAL_AI_FOLDER}", file=sys.stderr)
            sys.exit(1)
        src = src_link.resolve()  # follow symlink to get real source path
        dst = (local_ai / name).resolve() if (local_ai / name).exists() else local_ai / name
        if src == dst:
            print(f"'{name}' is already in local .ai/skills/ (same physical path — skipping copy, rebuild only)")
            continue
        dst = local_ai / name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst, symlinks=False)
        print(f"Copied '{name}' to {dst}")

    build_script = cwd / ".ai/skills/lnx-multi-ai/scripts/build-skills.py"
    if build_script.exists():
        subprocess.run([sys.executable, str(build_script)], check=True)
    else:
        print("Warning: build-skills.py not found — skipping rebuild.", file=sys.stderr)


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
    link_args = argparse.Namespace(paths=[args.path])
    cmd_link_as_global(link_args)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="lnx-ai-global-skills",
        description="Install, list, and remove AI skills from global harness folders.",
    )
    sub = parser.add_subparsers(dest="command", required=False)

    p = sub.add_parser("link-as-global", help="Symlink one or more local skills to all global harness folders and ~/.ai/skills/")
    p.add_argument("paths", nargs="+", help="Path(s) to skill source directories (each must contain content.md)")
    p.set_defaults(func=cmd_link_as_global)

    p = sub.add_parser("copy-from-global", help="Copy one or more skills from ~/.ai/skills/ to local .ai/skills/ and rebuild")
    p.add_argument("names", nargs="+", help="Skill name(s) to copy from global ~/.ai/skills/")
    p.set_defaults(func=cmd_copy_from_global)

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

    if args.command is None:
        print("lnx-ai-global-skills — manage AI skills across global harness folders\n")
        print("Commands:")
        print("  link-as-global <path>...   Symlink skill(s) to all global harness folders and ~/.ai/skills/")
        print("  copy-from-global <name>... Copy skill(s) from ~/.ai/skills/ to local .ai/skills/ and rebuild")
        print("  list-global                List skills installed in global harness folders")
        print("  list-local                 List skills found in the current project")
        print("  remove <name>              Remove a globally installed skill")
        print("  replace <name> <path>      Replace a globally installed skill with a new source")
        print("\nRun 'lnx-ai-global-skills <command> --help' for command details.")
        return

    args.func(args)


if __name__ == "__main__":
    main()
