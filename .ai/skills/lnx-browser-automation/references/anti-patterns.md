# Anti-Patterns

### Anti-Pattern: Running playwright-cli directly without the helper script

**Novice**: "I'll just run `playwright-cli open https://example.com` — it's simpler."
**Expert**: Running playwright-cli directly bypasses profile resolution entirely: no browser/channel mapping, no user-data-dir, no executable path env var, no extension token. The helper script exists specifically to translate config into the correct flags. Always use `build-cmd --exec` instead.
**Timeline**: 2026-06-18 (skill v0.1.0): helper script introduced as the sole entry point for all playwright-cli commands.
**LLM mistake**: Models default to the simplest invocation of a CLI tool and skip wrapper scripts unless explicitly instructed, because training data overwhelmingly shows direct CLI usage.
**Detection**: Any `playwright-cli open`, `playwright-cli screenshot`, `playwright-cli pdf`, or `playwright-cli codegen` command that does not originate from the helper script output.

### Anti-Pattern: Creating or modifying config.yml without explicit user request

**Novice**: "Let me update config.yml to change the browser for this request." / "I'll create a config.yml to set up a profile."
**Expert**: Config files represent persistent user preferences and must never be created or modified unless the user explicitly asks to create/update profiles or the config YAML. For one-off overrides, use CLI override flags (`--browser`, `--headless`, etc.) or `--profile <name>` to select a different existing profile. Creating or editing config without being asked creates drift and may surprise the user on subsequent runs.
**Timeline**: 2026-06-18 (skill v0.1.0): `build-cmd` supports CLI override flags and `-- extra-args` passthrough for one-off overrides.
**LLM mistake**: Models treat config files as mutable state they can freely create or edit to achieve a goal, without considering that config changes persist beyond the current task. They may also proactively create config files "to help" when none exist.
**Detection**: Any `Write` or `Edit` call targeting `config.yml` that was not explicitly requested by the user.

### Anti-Pattern: Assuming a default profile exists

**Novice**: "The user has profiles configured, so I can just run `build-cmd` without `--profile` and it will use their preferred browser."
**Expert**: If no profile has `use_as_default: true`, the script falls back to a virtual `__default` profile with `isolated: true` and default headless chromium. This means no persistent cookies, no custom browser, no user data. Always run `resolve-config` first to check which profile will actually be selected, and confirm with the user if the resolved profile is `__default`.
**Timeline**: 2026-06-18 (skill v0.1.0): virtual `__default` profile introduced as safe fallback with `isolated: true`.
**LLM mistake**: Models assume that the presence of a `profiles:` section in config implies one of them is the default. They skip the `resolve-config` verification step because they expect the "obvious" profile to be selected.
**Detection**: Running `build-cmd` without `--profile` and without a prior `resolve-config` call in the same session.
