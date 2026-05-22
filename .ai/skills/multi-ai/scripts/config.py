"""config.py — load and resolve .ai/config.yml for multi-ai build scripts."""
from pathlib import Path
import sys

_DEFAULTS = {
    "claude":  {"skills_folder_path": ".claude/skills",  "project_context_file_path": "CLAUDE.md"},
    "codex":   {"skills_folder_path": ".agents/skills",  "project_context_file_path": "AGENTS.md"},
    "cursor":  {"skills_folder_path": ".cursor/skills",  "project_context_file_path": ".cursorrules"},
    "copilot": {"skills_folder_path": ".github/skills",  "project_context_file_path": ".github/copilot-instructions.md"},
}


def load_config(repo_root: Path) -> dict:
    """Return resolved config for enabled harnesses only.

    Returns a dict keyed by harness name. Each value:
        {"skills_folder_path": str, "project_context_file_path": str}
    Path fields absent from the YAML fall back to _DEFAULTS.
    If config.yml is missing, all four harnesses are returned with defaults.
    """
    config_path = repo_root / ".ai" / "config.yml"
    if not config_path.exists():
        return dict(_DEFAULTS)

    try:
        import yaml
    except ImportError:
        print(
            "WARNING: PyYAML not installed — using defaults. Run: pip install pyyaml",
            file=sys.stderr,
        )
        return dict(_DEFAULTS)

    try:
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    except Exception as e:
        print(f"ERROR: Failed to parse {config_path}: {e}", file=sys.stderr)
        sys.exit(1)

    result = {}
    for name, block in (raw.get("harnesses") or {}).items():
        if name not in _DEFAULTS:
            print(f"WARNING: Unknown harness '{name}' in config — skipping", file=sys.stderr)
            continue
        block = block or {}
        if not block.get("enabled", True):
            continue
        cfg = dict(_DEFAULTS[name])
        if "skills_folder_path" in block:
            cfg["skills_folder_path"] = block["skills_folder_path"]
        if "project_context_file_path" in block:
            cfg["project_context_file_path"] = block["project_context_file_path"]
        result[name] = cfg

    return result
