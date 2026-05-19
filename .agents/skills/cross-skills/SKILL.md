---
description: |
  Generate, translate, validate, and maintain AI coding assistant skills across
  multiple agent frameworks (Claude Code, Cursor, Codex CLI, GitHub Copilot) from
  a single source of truth under .ai/skills/. Modes: analyze | generate |
  translate | validate | build-skill. NOT for project-level harness configs such
  as AGENTS.md, CLAUDE.md, .cursor/rules/, or .github/instructions/.
tools:
  - shell
  - read_file
  - write_file
tags:
  - config
  - dx
  - multi-agent
  - skills
---

@content.md
