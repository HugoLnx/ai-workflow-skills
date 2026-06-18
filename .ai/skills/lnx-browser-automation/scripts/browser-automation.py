#!/usr/bin/env python3
"""Browser automation helper — resolves Playwright CLI profiles and builds commands."""

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install it with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

GLOBAL_CONFIG_DIR = Path.home() / ".ai" / "browser-automation"
GLOBAL_CONFIG_PATH = GLOBAL_CONFIG_DIR / "config.yml"
GLOBAL_DATA_DIR = GLOBAL_CONFIG_DIR / "data"

PROJECT_CONFIG_REL = Path(".ai") / "browser-automation" / "config.yml"
PROJECT_DATA_REL = Path(".ai") / "browser-automation" / "data"

BROWSER_ALIASES = {
    "chrome": ("chromium", "chrome"),
    "chromium": ("chromium", None),
    "cr": ("chromium", None),
    "firefox": ("firefox", None),
    "ff": ("firefox", None),
    "webkit": ("webkit", None),
    "wk": ("webkit", None),
}

EXECUTABLE_ENV_VARS = {
    "chromium": "PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH",
    "firefox": "PLAYWRIGHT_FIREFOX_EXECUTABLE_PATH",
    "webkit": "PLAYWRIGHT_WEBKIT_EXECUTABLE_PATH",
}

META_KEYS = {"use_as_default", "user_dir_scope", "shared_user_dir_id", "overwrite_user_dir", "isolated", "extension_token"}


def find_project_root():
    cwd = Path.cwd()
    for d in [cwd, *cwd.parents]:
        if (d / ".git").exists() or (d / ".ai").exists():
            return d
    return cwd


def load_raw_config(path):
    if not path.exists():
        return {}
    with open(path) as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, dict) else {}


def load_and_merge_configs(project_root):
    global_cfg = load_raw_config(GLOBAL_CONFIG_PATH)
    project_cfg = load_raw_config(project_root / PROJECT_CONFIG_REL)

    if project_cfg.get("ignore_home_config", False):
        global_cfg = {}

    merged_default = {**global_cfg.get("default", {}), **project_cfg.get("default", {})}

    global_profiles = global_cfg.get("profiles", {}) or {}
    project_profiles = project_cfg.get("profiles", {}) or {}
    merged_profiles = {}
    all_names = set(global_profiles) | set(project_profiles)
    for name in all_names:
        g = global_profiles.get(name, {}) or {}
        p = project_profiles.get(name, {}) or {}
        merged_profiles[name] = {**g, **p}

    return {"default": merged_default, "profiles": merged_profiles}


def resolve_profile(merged, profile_name=None):
    defaults = dict(merged.get("default", {}) or {})
    profiles = merged.get("profiles", {}) or {}

    if profile_name:
        if profile_name not in profiles:
            available = ", ".join(sorted(profiles)) if profiles else "(none)"
            print(f"ERROR: Profile '{profile_name}' not found. Available: {available}", file=sys.stderr)
            sys.exit(1)
        resolved = {**defaults, **profiles[profile_name]}
        resolved.setdefault("isolated", False)
        return profile_name, resolved

    for name, cfg in profiles.items():
        if (cfg or {}).get("use_as_default", False):
            resolved = {**defaults, **(cfg or {})}
            resolved.setdefault("isolated", False)
            return name, resolved

    resolved = {**defaults, "isolated": True}
    return "__default", resolved


def resolve_user_data_dir(resolved, profile_name, project_root):
    if resolved.get("isolated", False):
        return None

    if resolved.get("overwrite_user_dir"):
        return str(resolved["overwrite_user_dir"])

    shared_id = resolved.get("shared_user_dir_id")
    if shared_id:
        scope = resolved.get("user_dir_scope", "global")
        dir_name = f"shared__{shared_id}"
        if scope == "project":
            return str(project_root / PROJECT_DATA_REL / dir_name)
        return str(GLOBAL_DATA_DIR / dir_name)

    return str(GLOBAL_DATA_DIR / profile_name)


def resolve_browser(resolved):
    browser_raw = resolved.get("browser")
    if not browser_raw:
        return None, None
    key = str(browser_raw).lower().strip()
    if key not in BROWSER_ALIASES:
        print(f"ERROR: Unknown browser '{browser_raw}'. Supported: {', '.join(sorted(BROWSER_ALIASES))}", file=sys.stderr)
        sys.exit(1)
    return BROWSER_ALIASES[key]


def build_playwright_command(command, resolved, profile_name, project_root, extra_args):
    env_vars = {}
    args = ["playwright-cli", command]

    browser, channel = resolve_browser(resolved)
    if browser:
        args.extend(["--browser", browser])
    if channel:
        args.extend(["--channel", channel])

    user_data_dir = resolve_user_data_dir(resolved, profile_name, project_root)
    if user_data_dir:
        if not resolved.get("overwrite_user_dir"):
            Path(user_data_dir).mkdir(parents=True, exist_ok=True)
        args.extend(["--user-data-dir", user_data_dir])

    headless = resolved.get("headless", True)
    if command == "codegen" and headless:
        print("WARNING: codegen requires headed mode. Ignoring headless config.", file=sys.stderr)
    elif headless:
        args.append("--headless")

    executable_path = resolved.get("executable_path")
    if executable_path:
        effective_browser = browser or "chromium"
        env_key = EXECUTABLE_ENV_VARS.get(effective_browser)
        if env_key:
            env_vars[env_key] = str(executable_path)

    extension_token = resolved.get("extension_token")
    if extension_token:
        env_vars["PLAYWRIGHT_MCP_EXTENSION_TOKEN"] = str(extension_token)
        args.extend(["--extension", str(extension_token)])

    args.extend(extra_args)

    env_prefix = " ".join(f'{k}="{v}"' for k, v in sorted(env_vars.items()))
    cmd_str = " ".join(args)
    if env_prefix:
        return f"{env_prefix} {cmd_str}"
    return cmd_str


def _add_override_args(parser):
    parser.add_argument("--browser", choices=sorted(BROWSER_ALIASES.keys()), help="Override browser from config")
    parser.add_argument("--headless", action=argparse.BooleanOptionalAction, default=None, help="Override headless mode")
    parser.add_argument("--executable-path", dest="executable_path", help="Override executable path")
    parser.add_argument("--extension-token", dest="extension_token", help="Override extension token")
    parser.add_argument("--user-data-dir", dest="user_data_dir", help="Override user data directory (exact path)")
    parser.add_argument("--isolated", action=argparse.BooleanOptionalAction, default=None, help="Override isolated mode")


def _apply_overrides(resolved, args):
    if args.browser is not None:
        resolved["browser"] = args.browser
    if args.headless is not None:
        resolved["headless"] = args.headless
    if args.executable_path is not None:
        resolved["executable_path"] = args.executable_path
    if args.extension_token is not None:
        resolved["extension_token"] = args.extension_token
    if args.user_data_dir is not None:
        resolved["overwrite_user_dir"] = args.user_data_dir
        if args.isolated is None:
            resolved["isolated"] = False
    if args.isolated is not None:
        resolved["isolated"] = args.isolated


def cmd_check_prereqs(args):
    pw = shutil.which("playwright-cli")
    if pw:
        result = subprocess.run(["playwright-cli", "--version"], capture_output=True, text=True)
        version = result.stdout.strip() or "unknown"
        print(f"OK: playwright-cli found at {pw} (version {version})")
    else:
        print("ERROR: playwright-cli not found on PATH.", file=sys.stderr)
        print("Install with: npm install -g @playwright/cli", file=sys.stderr)
        sys.exit(1)


def cmd_install_deps(args):
    cmd = ["npm", "install", "-g", "@playwright/cli"]
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


def cmd_resolve_config(args):
    project_root = find_project_root()
    merged = load_and_merge_configs(project_root)
    profile_name, resolved = resolve_profile(merged, args.profile)
    _apply_overrides(resolved, args)

    user_data_dir = resolve_user_data_dir(resolved, profile_name, project_root)
    browser, channel = resolve_browser(resolved)

    output = {"profile": profile_name}
    if browser:
        output["browser"] = browser
    if channel:
        output["channel"] = channel
    output["headless"] = resolved.get("headless", True)
    output["isolated"] = resolved.get("isolated", False)
    if user_data_dir:
        output["user_data_dir"] = user_data_dir
    if resolved.get("executable_path"):
        output["executable_path"] = resolved["executable_path"]
    if resolved.get("extension_token"):
        output["extension_token"] = resolved["extension_token"]

    profiles = merged.get("profiles", {})
    if profiles:
        output["available_profiles"] = sorted(profiles.keys())

    print(yaml.dump(output, default_flow_style=False, sort_keys=False).strip())


def cmd_build_cmd(args):
    project_root = find_project_root()
    merged = load_and_merge_configs(project_root)
    profile_name, resolved = resolve_profile(merged, args.profile)
    _apply_overrides(resolved, args)

    cmd_str = build_playwright_command(args.command, resolved, profile_name, project_root, args.extra_args)
    print(cmd_str)

    if args.exec:
        env = os.environ.copy()
        parts = cmd_str.split()
        i = 0
        while i < len(parts) and "=" in parts[i] and not parts[i].startswith("-"):
            key, val = parts[i].split("=", 1)
            env[key] = val.strip('"')
            i += 1
        actual_cmd = parts[i:]
        result = subprocess.run(actual_cmd, env=env)
        sys.exit(result.returncode)


def main():
    parser = argparse.ArgumentParser(description="Browser automation helper for Playwright CLI")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    subparsers.add_parser("check-prereqs", help="Verify playwright-cli is installed")
    subparsers.add_parser("install-deps", help="Install playwright-cli via npm")

    rc = subparsers.add_parser("resolve-config", help="Show resolved config for a profile")
    rc.add_argument("--profile", "-p", help="Profile name (default: auto-detect)")
    _add_override_args(rc)

    bc = subparsers.add_parser("build-cmd", help="Build a playwright CLI command")
    bc.add_argument("command", choices=["open", "screenshot", "pdf", "codegen"], help="Playwright command")
    bc.add_argument("--profile", "-p", help="Profile name (default: auto-detect)")
    bc.add_argument("--exec", action="store_true", help="Execute the command after printing it")
    _add_override_args(bc)
    bc.add_argument("extra_args", nargs="*", help="Extra arguments passed to playwright-cli")

    args = parser.parse_args()
    if args.subcommand == "check-prereqs":
        cmd_check_prereqs(args)
    elif args.subcommand == "install-deps":
        cmd_install_deps(args)
    elif args.subcommand == "resolve-config":
        cmd_resolve_config(args)
    elif args.subcommand == "build-cmd":
        cmd_build_cmd(args)


if __name__ == "__main__":
    main()
