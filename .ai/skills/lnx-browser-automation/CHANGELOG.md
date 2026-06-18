## [0.1.0] — 2026-06-18

- Initial release
- Multi-profile configuration system with global and project-level config
- Config merging with `ignore_home_config` support
- Profile resolution: explicit → `use_as_default` → virtual `__default`
- User data directory: normal, `overwrite_user_dir`, `shared_user_dir_id`, `isolated`
- Browser mapping: chrome, chromium, firefox, webkit with aliases
- `resolve-config` and `build-cmd` subcommands with `--exec` mode
- `check-prereqs` subcommand for verifying Playwright installation
- Extension token support via `--extension` flag and `PLAYWRIGHT_MCP_EXTENSION_TOKEN` env var
- Executable path support via browser-specific env vars
