---
description: |
  Manage a multi-harness project rules architecture where rule content lives once
  in .ai/rules/*.md and is distributed to Claude Code (CLAUDE.md), Codex CLI
  (AGENTS.md), Cursor (.cursor/rules/*.mdc), and GitHub Copilot
  (.github/instructions/*.md). Use when: initialising the rules scaffold, adding
  a new rule, generating the build script, validating rule files, listing
  existing rules, or migrating an existing project to the cross-rules format.
  Modes: init | add | make-script | validate | list | migrate.
  NOT for: writing .cursor/rules/ or .github/instructions/ files directly —
  those are owned by the build script.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
argument-hint: "init | add | make-script | validate | list | migrate"
---

@content.md
