# lnx-browser-automation — as of 2026-06-18

## Description

Browser automation skill using Playwright CLI. Resolves browser profiles from global and project config, merges them, and builds correct `playwright` commands for opening pages, taking screenshots, generating PDFs, and recording user actions with codegen.

## Activate me when...

- User wants to open a URL in a browser (headed or headless)
- User wants to take a screenshot of a web page
- User wants to generate a PDF from a web page
- User wants to record browser interactions with codegen
- User mentions Playwright, browser automation, or browser profiles
- User says "open in chrome", "screenshot this page", "browse to", "capture page"

## Do NOT activate me when...

- User wants to write Playwright test scripts (Python/JS test files)
- User wants to install or update Playwright browsers (`playwright install`)
- User wants to use Selenium, Puppeteer, or other browser automation tools
- User is editing browser-automation config files directly (just edit the YAML)

## Minimum Knowledge

### Script location

The helper script is at `<skill-dir>/scripts/browser-automation.py` where `<skill-dir>` is the directory containing this SKILL.md file.

### Config paths

- **Global**: `~/.ai/browser-automation/config.yml`
- **Project**: `<project-root>/.ai/browser-automation/config.yml`

Both are optional. Without any config the skill uses default settings (`--headless`, no persistent user data).

### Config structure

```yaml
ignore_home_config: true  # project-level only; skips global config entirely
default:
  browser: chrome       # unset by default (playwright defaults to chromium)
  headless: true        # true by default
  executable_path: "…"  # unset by default
profiles:
  my_profile:
    browser: firefox
    headless: false
    executable_path: "/path/to/browser"
    use_as_default: true              # use this profile when none is specified
    extension_token: "token_value"    # sets PLAYWRIGHT_MCP_EXTENSION_TOKEN env var
    overwrite_user_dir: "/custom/dir" # use this path as user-data-dir directly
    shared_user_dir_id: shared_id     # share user-data-dir with other profiles using same id
    user_dir_scope: "global"          # "global" (default) or "project"
    isolated: false                   # true = no persistent user data
```

Project-level config overrides global-level config (field by field, profile by profile). Set `ignore_home_config: true` in project config to discard global config entirely.

### Profile selection

1. If `--profile <name>` is passed → use that profile
2. Else find a profile with `use_as_default: true`
3. Else use virtual `__default` profile with `isolated: true` (ephemeral session)

Custom profiles default to `isolated: false`. The `__default` virtual profile defaults to `isolated: true`.

### User data directory

Each profile gets its own persistent browser data directory unless isolated:

- Normal profile: `~/.ai/browser-automation/data/<profile_name>/`
- `overwrite_user_dir`: use that path directly
- `shared_user_dir_id` + `user_dir_scope: "global"`: `~/.ai/browser-automation/data/shared__<id>/`
- `shared_user_dir_id` + `user_dir_scope: "project"`: `<project>/.ai/browser-automation/data/shared__<id>/`
- `isolated: true`: no `--user-data-dir` flag (ephemeral)

## Commands

### resolve-config

Show the resolved configuration for a profile:

```
python "<skill-dir>/scripts/browser-automation.py" resolve-config [--profile <name>]
```

Use this first to check available profiles and what settings will be applied.

### build-cmd

Build (and optionally execute) a playwright command:

```
python "<skill-dir>/scripts/browser-automation.py" build-cmd <command> [--profile <name>] [--exec] [-- extra-args...]
```

Where `<command>` is one of: `open`, `screenshot`, `pdf`, `codegen`.

Pass `--exec` to run the command immediately after printing it. Without `--exec`, only the command string is printed.

Extra arguments after `--` are passed through to playwright as-is.

## Workflow

1. User asks to perform a browser task
2. Run `resolve-config` to check available profiles and settings
3. Run `build-cmd` with the appropriate playwright command and `--exec`
4. For `screenshot`/`pdf`: report the output file path to the user

## Headless behavior

- `headless: true` adds `--headless` to the playwright command
- `codegen` always runs headed — if headless is configured, the script prints a warning and runs headed anyway
- `open` supports headless mode normally
- `screenshot` and `pdf` are inherently headless operations

## Anti-patterns

**Running playwright directly without the helper script** — always use `build-cmd` to ensure the correct browser, channel, user-data-dir, executable path, and extension token are resolved from config.

**Modifying config for a one-off command** — use `--profile <name>` or pass extra args after `--` instead. Config files represent persistent preferences.
