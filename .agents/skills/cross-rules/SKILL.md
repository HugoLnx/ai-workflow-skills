---
description: |
  Manage a multi-harness project rules architecture where rule content lives once
  in .ai/rules/*.md and is distributed to Claude Code (CLAUDE.md), Codex CLI
  (AGENTS.md), Cursor (.cursor/rules/*.mdc), and GitHub Copilot
  (.github/instructions/*.md). Modes: init | add | make-script | validate |
  list | migrate. NOT for: writing .cursor/rules/ or .github/instructions/ files
  directly — those are owned by the build script.
tools:
  - shell
  - read_file
  - write_file
tags:
  - config
  - dx
  - multi-agent
  - rules
---

@content.md
