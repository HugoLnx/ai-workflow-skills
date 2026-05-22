"""cleanup.py — delete harness output files for disabled harnesses and legacy folders."""

import shutil
from pathlib import Path

from config import _DEFAULTS, load_config

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parents[3]

LEGACY_FOLDERS = [".cursor/rules", ".github/integrations"]


def _collect_harness_items(repo_root: Path, disabled: dict) -> list:
    items = []
    for harness_name, cfg in disabled.items():
        skills_folder = repo_root / cfg["skills_folder_path"]
        context_file = repo_root / cfg["project_context_file_path"]
        if skills_folder.exists():
            items.append(("dir", skills_folder))
        if context_file.exists() or context_file.is_symlink():
            items.append(("file", context_file))
    return items


def _collect_legacy_items(repo_root: Path) -> list:
    items = []
    for folder_rel in LEGACY_FOLDERS:
        folder = repo_root / folder_rel
        if folder.exists():
            items.append(("legacy_dir", folder))
    return items


def _print_dir_item(repo_root: Path, path: Path, show_all_children: bool = False) -> None:
    rel = path.relative_to(repo_root)
    print(f"  [dir]  {rel}/")
    children = sorted(path.iterdir())
    if show_all_children:
        for child in children:
            kind = "dir" if child.is_dir() else "file"
            print(f"           └── [{kind}] {child.name}")
    else:
        for child in (c for c in children if c.is_dir()):
            print(f"           └── {child.name}/")


def main():
    enabled = load_config(REPO_ROOT)
    disabled_names = set(_DEFAULTS.keys()) - set(enabled.keys())
    disabled = {name: _DEFAULTS[name] for name in disabled_names}

    harness_items = _collect_harness_items(REPO_ROOT, disabled) if disabled_names else []
    legacy_items = _collect_legacy_items(REPO_ROOT)

    if not harness_items and not legacy_items:
        print("Nothing to clean up.")
        return

    if harness_items:
        if disabled_names:
            print(f"Disabled harnesses: {', '.join(sorted(disabled_names))}\n")
        print("Harness outputs to delete:")
        for kind, path in harness_items:
            if kind == "dir":
                _print_dir_item(REPO_ROOT, path, show_all_children=False)
            else:
                print(f"  [file] {path.relative_to(REPO_ROOT)}")

    if legacy_items:
        if harness_items:
            print()
        print("Legacy folders to delete:")
        for _kind, path in legacy_items:
            _print_dir_item(REPO_ROOT, path, show_all_children=True)

    answer = input("\nDelete all of the above? [y/N] ").strip().lower()
    if answer != "y":
        print("Aborted.")
        return

    for kind, path in harness_items:
        rel = path.relative_to(REPO_ROOT)
        shutil.rmtree(path) if kind == "dir" else path.unlink()
        print(f"  Deleted: {rel}")

    for _kind, path in legacy_items:
        rel = path.relative_to(REPO_ROOT)
        shutil.rmtree(path)
        print(f"  Deleted: {rel}/")

    total = len(harness_items) + len(legacy_items)
    print(f"\nDone. Removed {total} item(s).")


if __name__ == "__main__":
    main()
