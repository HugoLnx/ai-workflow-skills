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

def render_skill_line(name: str, presence: dict, manually_installed: bool = False) -> str:
    """'name         | ai claude !codex cursor !copilot'"""
    tags = []
    for h in HARNESS_ORDER:
        label = h if presence.get(h) else f"!{h}"
        tags.append(_color(h, label))
    line = f"{name:<20} | {' '.join(tags)}"
    if manually_installed:
        line += " | manually-installed"
    return line


# ── list-global ───────────────────────────────────────────────────────────────

def cmd_list_global(_args):
    names: set = set()
    for folder in GLOBAL_HARNESSES.values():
        if folder.is_dir():
            names.update(p.name for p in folder.iterdir() if p.is_dir() or p.is_symlink())
    if GLOBAL_AI_FOLDER.is_dir():
        names.update(p.name for p in GLOBAL_AI_FOLDER.iterdir() if p.is_dir() or p.is_symlink())

    if not names:
        print("No global skills found.")
        return

    for name in sorted(names):
        presence = {h: (folder / name).exists() for h, folder in GLOBAL_HARNESSES.items()}
        presence["ai"] = (GLOBAL_AI_FOLDER / name).exists()

        # Detect manually-installed: any existing folder that is not a symlink
        manually_installed = False
        ai_entry = GLOBAL_AI_FOLDER / name
        if ai_entry.exists() and not ai_entry.is_symlink():
            manually_installed = True
        if not manually_installed:
            for folder in GLOBAL_HARNESSES.values():
                entry = folder / name
                if entry.exists() and not entry.is_symlink():
                    manually_installed = True
                    break

        print(render_skill_line(name, presence, manually_installed))


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


# ── Symlink helper ────────────────────────────────────────────────────────────

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


# ── lib-link ──────────────────────────────────────────────────────────────────

def cmd_lib_link(args):
    ok = True
    for path_str in args.paths:
        source = Path(path_str).resolve()
        if not (source / "content.md").exists():
            print(f"Error: {source} has no content.md — not a valid skill source.", file=sys.stderr)
            ok = False
            continue

        name = source.name
        GLOBAL_AI_FOLDER.mkdir(parents=True, exist_ok=True)
        result = _make_symlink(source, GLOBAL_AI_FOLDER / f"gl-{name}")
        if result in ("created", "verified"):
            print(f"lib-link '{name}' → {GLOBAL_AI_FOLDER}/gl-{name}: {result}")
        else:
            print(result, file=sys.stderr)
            ok = False

    if not ok:
        sys.exit(1)


# ── harness-link ──────────────────────────────────────────────────────────────

def _parse_harnesses(harnesses_arg) -> list:
    if not harnesses_arg:
        return list(GLOBAL_HARNESSES.keys())
    selected = []
    for h in harnesses_arg.split(","):
        h = h.strip()
        if h not in GLOBAL_HARNESSES:
            print(f"Error: unknown harness '{h}'. Valid: {', '.join(GLOBAL_HARNESSES)}", file=sys.stderr)
            sys.exit(1)
        selected.append(h)
    return selected


def cmd_harness_link(args):
    cwd = Path.cwd()
    harnesses = _parse_harnesses(args.harnesses)
    ok = True

    for name in args.names:
        created = verified = 0
        errors = []

        for harness in harnesses:
            local_folder = cwd / LOCAL_HARNESSES[harness] / name
            if not local_folder.is_dir():
                errors.append(f"  {harness}: local {LOCAL_HARNESSES[harness]}/{name} not found — skipped")
                continue

            global_folder = GLOBAL_HARNESSES[harness]
            global_folder.mkdir(parents=True, exist_ok=True)
            dst = global_folder / f"gl-{name}"
            result = _make_symlink(local_folder.resolve(), dst)
            if result == "created":
                created += 1
            elif result == "verified":
                verified += 1
            else:
                errors.append(f"  {harness}: {result}")

        print(f"harness-link '{name}':")
        print(f"  Symlinks created : {created}")
        print(f"  Symlinks verified: {verified}")
        for err in errors:
            print(err, file=sys.stderr)
            ok = False

    if not ok:
        sys.exit(1)


# ── lib-pull ──────────────────────────────────────────────────────────────────

def cmd_lib_pull(args):
    cwd = Path.cwd()
    local_ai = cwd / LOCAL_SOURCE
    local_ai.mkdir(parents=True, exist_ok=True)

    for name in args.names:
        # Strip gl- prefix from user input if provided
        bare_name = name[3:] if name.startswith("gl-") else name
        src_link = GLOBAL_AI_FOLDER / f"gl-{bare_name}"
        if not src_link.exists():
            print(f"Error: 'gl-{bare_name}' not found in {GLOBAL_AI_FOLDER}", file=sys.stderr)
            sys.exit(1)
        src = src_link.resolve()
        dst = local_ai / bare_name
        if src == dst.resolve() if dst.exists() else False:
            print(f"'{bare_name}' is already in local .ai/skills/ (same physical path — skipping copy, rebuild only)")
            continue
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst, symlinks=False)
        print(f"Copied 'gl-{bare_name}' → {dst}")

    build_script = cwd / ".ai/skills/lnx-multi-ai/scripts/build-skills.py"
    if build_script.exists():
        subprocess.run([sys.executable, str(build_script)], check=True)
    else:
        print("Warning: build-skills.py not found — skipping rebuild.", file=sys.stderr)


# ── Unlink helpers ────────────────────────────────────────────────────────────

def _resolve_global_ai_entry(name: str) -> Path | None:
    """Return the first existing entry for name in GLOBAL_AI_FOLDER (gl-<name> first, then <name>)."""
    for candidate in (f"gl-{name}", name):
        entry = GLOBAL_AI_FOLDER / candidate
        if entry.exists() or entry.is_symlink():
            return entry
    return None


def _resolve_harness_entry(harness: str, name: str) -> Path | None:
    """Return the first existing harness folder entry for name (gl-<name> first, then <name>)."""
    folder = GLOBAL_HARNESSES[harness]
    for candidate in (f"gl-{name}", name):
        entry = folder / candidate
        if entry.exists() or entry.is_symlink():
            return entry
    return None


def _remove_path(path: Path):
    if path.is_symlink():
        path.unlink()
    else:
        shutil.rmtree(path)


# ── lib-unlink ────────────────────────────────────────────────────────────────

def cmd_lib_unlink(args):
    removed = []
    not_found = []
    for name in args.names:
        bare = name[3:] if name.startswith("gl-") else name
        entry = _resolve_global_ai_entry(bare)
        if entry:
            _remove_path(entry)
            removed.append(entry.name)
        else:
            not_found.append(bare)

    if removed:
        print(f"Removed from ~/.ai/skills/: {', '.join(removed)}")
    if not_found:
        print(f"Not found in ~/.ai/skills/: {', '.join(not_found)}")
    if not removed and not_found:
        sys.exit(1)


# ── harness-unlink ────────────────────────────────────────────────────────────

def cmd_harness_unlink(args):
    harnesses = _parse_harnesses(args.harnesses)
    any_removed = False

    for name in args.names:
        bare = name[3:] if name.startswith("gl-") else name
        removed = []
        not_found = []

        for harness in harnesses:
            entry = _resolve_harness_entry(harness, bare)
            if entry:
                _remove_path(entry)
                removed.append(f"{harness}/{entry.name}")
            else:
                not_found.append(harness)

        if removed:
            print(f"Removed '{bare}' from: {', '.join(removed)}")
            any_removed = True
        if not_found:
            print(f"Not found in   : {', '.join(not_found)}")

    if not any_removed:
        sys.exit(1)


# ── full-unlink ───────────────────────────────────────────────────────────────

def cmd_full_unlink(args):
    lib_args = argparse.Namespace(names=args.names)
    cmd_lib_unlink(lib_args)
    harness_args = argparse.Namespace(names=args.names, harnesses=None)
    cmd_harness_unlink(harness_args)


# ── replace ───────────────────────────────────────────────────────────────────

def cmd_replace(args):
    full_unlink_args = argparse.Namespace(names=[args.name])
    cmd_full_unlink(full_unlink_args)
    lib_link_args = argparse.Namespace(paths=[args.path])
    cmd_lib_link(lib_link_args)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="lnx-ai-global-skills",
        description="Install, list, and remove AI skills from global harness folders.",
    )
    sub = parser.add_subparsers(dest="command", required=False)

    p = sub.add_parser("lib-link", help="Symlink skill source(s) to ~/.ai/skills/ as gl-<name>")
    p.add_argument("paths", nargs="+", help="Path(s) to skill source directories (each must contain content.md)")
    p.set_defaults(func=cmd_lib_link)

    p = sub.add_parser("harness-link", help="Link local harness output(s) to global harness folders as gl-<name>")
    p.add_argument("names", nargs="+", help="Skill name(s) to link from local harness output folders")
    p.add_argument("--harnesses", default=None, help="Comma-separated harnesses to target (default: all)")
    p.set_defaults(func=cmd_harness_link)

    p = sub.add_parser("lib-pull", help="Copy skill(s) from ~/.ai/skills/gl-<name> to local .ai/skills/ and rebuild")
    p.add_argument("names", nargs="+", help="Skill name(s) to copy from global ~/.ai/skills/")
    p.set_defaults(func=cmd_lib_pull)

    p = sub.add_parser("list-global", help="List skills installed in global harness folders")
    p.set_defaults(func=cmd_list_global)

    p = sub.add_parser("list-local", help="List skills found in the current project")
    p.set_defaults(func=cmd_list_local)

    p = sub.add_parser("lib-unlink", help="Remove skill(s) from ~/.ai/skills/")
    p.add_argument("names", nargs="+", help="Skill name(s) to remove (with or without gl- prefix)")
    p.set_defaults(func=cmd_lib_unlink)

    p = sub.add_parser("harness-unlink", help="Remove skill(s) from global harness folders")
    p.add_argument("names", nargs="+", help="Skill name(s) to remove (with or without gl- prefix)")
    p.add_argument("--harnesses", default=None, help="Comma-separated harnesses to target (default: all)")
    p.set_defaults(func=cmd_harness_unlink)

    p = sub.add_parser("full-unlink", help="Remove skill(s) from all global locations")
    p.add_argument("names", nargs="+", help="Skill name(s) to remove (with or without gl- prefix)")
    p.set_defaults(func=cmd_full_unlink)

    p = sub.add_parser("replace", help="Replace a globally installed skill with a new source")
    p.add_argument("name", help="Skill name to replace")
    p.add_argument("path", help="New skill source path")
    p.set_defaults(func=cmd_replace)

    args = parser.parse_args()

    if args.command is None:
        print("lnx-ai-global-skills — manage AI skills across global harness folders\n")
        print("Commands:")
        print("  lib-link <path>...                      Symlink skill source(s) to ~/.ai/skills/ as gl-<name>")
        print("  harness-link <name>... [--harnesses h]  Link local harness output(s) to global harness folders as gl-<name>")
        print("  lib-pull <name>...                      Copy skill(s) from ~/.ai/skills/gl-<name> to local .ai/skills/ and rebuild")
        print("  list-global                             List skills installed in global harness folders")
        print("  list-local                              List skills found in the current project")
        print("  lib-unlink <name>...                    Remove skill(s) from ~/.ai/skills/")
        print("  harness-unlink <name>... [--harnesses h] Remove skill(s) from global harness folders")
        print("  full-unlink <name>...                   Remove skill(s) from all global locations")
        print("  replace <name> <path>                   Replace a globally installed skill with a new source")
        print("\nRun 'lnx-ai-global-skills <command> --help' for command details.")
        return

    args.func(args)


if __name__ == "__main__":
    main()
