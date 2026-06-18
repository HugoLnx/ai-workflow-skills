---
description: |
  Browser automation via Playwright CLI with multi-profile configuration.
  Resolves config from global (~/.ai/browser-automation/config.yml) and project
  (.ai/browser-automation/config.yml), merges profiles, and builds playwright commands.
  Use when the user wants to open a browser, take screenshots, generate PDFs, record
  interactions with codegen, or mentions browser profiles / playwright.
  NOT for: writing Playwright test scripts, installing browsers, Selenium/Puppeteer.
---

# lnx-browser-automation — as of 2026-06-18

## Description

Browser automation skill using Playwright CLI. Resolves browser profiles from layered config (global + project), merges them, and builds correct `playwright` commands for opening pages, taking screenshots, generating PDFs, and recording user actions.

## Activate me when...

- User wants to open, screenshot, PDF, or codegen a web page via a browser
- User mentions Playwright CLI, browser automation, or browser profiles
- User says "open in chrome", "screenshot this page", "browse to", "capture page"

## Do NOT activate me when...

- User wants to write Playwright test scripts (Python/JS test files — that's test authoring, not CLI automation)
- User wants to install or update Playwright browsers (`playwright install`)
- User wants to use Selenium, Puppeteer, or other non-Playwright tools

## References table

| File | Load when |
|---|---|
| `references/core-knowledge.md` | Always — config structure, commands, workflow, guardrails, output contracts |
| `references/anti-patterns.md` | Always — common mistakes when using this skill |

## Minimum Knowledge

- Helper script: `<skill-dir>/scripts/browser-automation.py` — never run `playwright` directly; always use the script to resolve profiles
- Before first use run `python "<skill-dir>/scripts/browser-automation.py" check-prereqs` to verify Playwright is installed
- Config: global `~/.ai/browser-automation/config.yml` + project `<project-root>/.ai/browser-automation/config.yml` (both optional; works with no config)
- Two subcommands: `resolve-config [--profile <name>]` to inspect settings; `build-cmd <open|screenshot|pdf|codegen> [--profile <name>] [--exec] [-- extra-args]` to build/run commands
- Profile selection: explicit `--profile` → profile with `use_as_default: true` → virtual `__default` (ephemeral, `isolated: true`)
- `codegen` always runs headed regardless of config; all other commands respect the `headless` setting
