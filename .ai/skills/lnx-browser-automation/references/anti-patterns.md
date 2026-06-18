# Anti-Patterns

### Anti-Pattern: Running playwright-cli directly without the helper script

**Novice**: "I'll just run `playwright-cli open https://example.com` — it's simpler."
**Expert**: Running playwright-cli directly bypasses profile resolution entirely: no browser/channel mapping, no user-data-dir, no executable path env var, no extension token. The helper script exists specifically to translate config into the correct flags. Always use `build-cmd --exec` instead.
**Timeline**: 2026-06-18 (skill v0.1.0): helper script introduced as the sole entry point for all playwright-cli commands.
**LLM mistake**: Models default to the simplest invocation of a CLI tool and skip wrapper scripts unless explicitly instructed, because training data overwhelmingly shows direct CLI usage.
**Detection**: Any `playwright-cli open`, `playwright-cli screenshot`, `playwright-cli pdf`, or `playwright-cli codegen` command that does not originate from the helper script output.

### Anti-Pattern: Modifying config for a one-off command

**Novice**: "Let me update config.yml to change the browser for this one request."
**Expert**: Config files represent persistent user preferences. For one-off overrides, use `--profile <name>` to select a different existing profile, or pass extra flags after `--` in `build-cmd`. Editing config for a single command creates drift and may surprise the user on subsequent runs.
**Timeline**: 2026-06-18 (skill v0.1.0): `build-cmd` supports `-- extra-args` passthrough for one-off flag overrides.
**LLM mistake**: Models treat config files as mutable state they can freely edit to achieve a goal, without considering that config changes persist beyond the current task.
**Detection**: Any `Write` or `Edit` call targeting `config.yml` in the same turn as a `build-cmd` invocation, where the edit is not explicitly requested by the user.

### Anti-Pattern: Assuming a default profile exists

**Novice**: "The user has profiles configured, so I can just run `build-cmd` without `--profile` and it will use their preferred browser."
**Expert**: If no profile has `use_as_default: true`, the script falls back to a virtual `__default` profile with `isolated: true` and default headless chromium. This means no persistent cookies, no custom browser, no user data. Always run `resolve-config` first to check which profile will actually be selected, and confirm with the user if the resolved profile is `__default`.
**Timeline**: 2026-06-18 (skill v0.1.0): virtual `__default` profile introduced as safe fallback with `isolated: true`.
**LLM mistake**: Models assume that the presence of a `profiles:` section in config implies one of them is the default. They skip the `resolve-config` verification step because they expect the "obvious" profile to be selected.
**Detection**: Running `build-cmd` without `--profile` and without a prior `resolve-config` call in the same session.
