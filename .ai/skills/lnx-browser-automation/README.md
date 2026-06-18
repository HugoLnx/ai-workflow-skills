# lnx-browser-automation

Browser automation skill using [Playwright CLI](https://playwright.dev/). Resolves browser profiles from layered config files and builds correct `playwright` commands.

## Configuration

Config is loaded from two optional YAML files, merged together:

| Level | Path |
|---|---|
| Global | `~/.ai/browser-automation/config.yml` |
| Project | `<project-root>/.ai/browser-automation/config.yml` |

Project-level values override global-level values (field by field, profile by profile). If no config files exist, the skill uses sensible defaults: headless chromium with no persistent data.

### Full example

```yaml
# Only available in project-level config.
# When true, ignores all settings from the global config.
# When false (default), merges with global config (project wins on conflicts).
ignore_home_config: false

# Default settings applied to every profile unless overridden.
default:
  browser: chrome
  headless: true
  executable_path: "/usr/bin/google-chrome"

# Named profiles. Each profile inherits from `default` and can override any field.
profiles:
  chrome_windows:
    executable_path: "/c/programs/chrome.exe"
    use_as_default: true

  chrome_extension:
    extension_token: LapxmHFPFb

  firefox_headed:
    browser: firefox
    headless: false
    overwrite_user_dir: "/c/custom_user_dir/"

  firefox_isolated:
    browser: firefox
    isolated: true

  chrome_steam_1:
    shared_user_dir_id: c_steam
    user_dir_scope: "project"

  chrome_steam_2:
    shared_user_dir_id: c_steam
    user_dir_scope: "project"
```

## Config options reference

### Top-level

| Option | Type | Default | Scope | Description |
|---|---|---|---|---|
| `ignore_home_config` | bool | `false` | project only | When `true`, the global config file is ignored entirely. |
| `default` | map | `{}` | both | Default settings inherited by all profiles. |
| `profiles` | map | `{}` | both | Named profile definitions (see below). |

### `default` and profile options

These options can appear under `default` (applied to all profiles) or inside a specific profile (overrides `default` for that profile).

| Option | Type | Default | Description |
|---|---|---|---|
| `browser` | string | _(unset)_ | Browser engine. Accepted values: `chrome`, `chromium`, `cr`, `firefox`, `ff`, `webkit`, `wk`. When unset, Playwright defaults to chromium. `chrome` uses chromium with the Chrome channel. |
| `headless` | bool | `true` | Run the browser without a visible window. Note: `codegen` always runs headed regardless of this setting (a warning is printed). |
| `executable_path` | string | _(unset)_ | Path to a custom browser executable. Passed via environment variable (e.g. `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`). |
| `extension_token` | string | _(unset)_ | Value for the `PLAYWRIGHT_MCP_EXTENSION_TOKEN` environment variable. Also passed as `--extension <token>` to the CLI. |

### Profile-only options

These options only make sense inside a profile definition, not under `default`.

| Option | Type | Default | Description |
|---|---|---|---|
| `use_as_default` | bool | `false` | Use this profile when no `--profile` is specified. Only one profile should have this set. |
| `isolated` | bool | `false` | When `true`, the browser runs with no persistent user data directory (ephemeral session). Custom profiles default to `false`. If no profile is selected at all, the implicit `__default` profile uses `true`. |
| `overwrite_user_dir` | string | _(unset)_ | Use this exact path as the browser's user data directory instead of the auto-generated one. The directory is not created automatically — it must already exist. |
| `shared_user_dir_id` | string | _(unset)_ | Share a user data directory with other profiles that use the same id. The directory name becomes `shared__<id>`. |
| `user_dir_scope` | string | `"global"` | Where to place the shared user data directory. `"global"` → `~/.ai/browser-automation/data/shared__<id>/`. `"project"` → `<project-root>/.ai/browser-automation/data/shared__<id>/`. Only relevant when `shared_user_dir_id` is set. |

## User data directories

Each non-isolated profile gets a persistent browser data directory (cookies, local storage, etc.):

| Scenario | Path |
|---|---|
| Normal profile | `~/.ai/browser-automation/data/<profile_name>/` |
| `overwrite_user_dir` set | The exact path specified |
| `shared_user_dir_id` + scope `global` | `~/.ai/browser-automation/data/shared__<id>/` |
| `shared_user_dir_id` + scope `project` | `<project>/.ai/browser-automation/data/shared__<id>/` |
| `isolated: true` | No directory (ephemeral session) |

Directories are created automatically when needed, except for `overwrite_user_dir` paths.

## Profile selection

When no `--profile` is specified:

1. The first profile with `use_as_default: true` is used.
2. If no default profile exists, a virtual `__default` profile is used with `isolated: true` (ephemeral headless chromium session).

## Config merging

When both global and project configs exist:

1. `default` sections are merged — project values override global values for the same key.
2. `profiles` are merged per profile name — if a profile exists in both, the project's fields override the global's fields within that profile. Profiles that exist in only one file are kept as-is.
3. Set `ignore_home_config: true` in the project config to skip the global config entirely.
