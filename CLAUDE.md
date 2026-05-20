# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build

After editing any skill source file, regenerate harness output:

```bash
python .ai/skills/cross-skills/scripts/build-skills.py
```

Requires Python 3.9+. Works on Linux, macOS, and Windows (symlinks on Windows require Developer Mode or Administrator privileges).

The build script is idempotent — safe to run multiple times. It prints a summary of SKILL.md files written and symlinks created/verified. A non-zero exit means at least one error (listed above the summary).

## Architecture

### Skills: single source of truth

All skill content lives under `.ai/skills/<skill-name>/`:

```
.ai/skills/<name>/
  content.md        # Skill body — pure markdown, no frontmatter
  frontmatter/
    claude.yaml     # Frontmatter for Claude Code
    codex.yaml      # Frontmatter for OpenAI Codex CLI
    cursor.yaml     # Frontmatter for Cursor
    copilot.yaml    # Frontmatter for GitHub Copilot
  references/       # Progressive-disclosure reference files (symlinked, not copied)
  scripts/          # Helper scripts (symlinked, not copied)
```

The build script creates one output folder per skill per harness:

| Harness | Output folder |
|---|---|
| Claude Code | `.claude/skills/<name>/` |
| OpenAI Codex CLI | `.agents/skills/<name>/` |
| Cursor | `.cursor/skills/<name>/` |
| GitHub Copilot | `.github/skills/<name>/` |

Each output `SKILL.md` contains only the YAML frontmatter (from `frontmatter/<harness>.yaml`) followed by `@content.md`. The `content.md` file and all files/folders other than `frontmatter/` are **symlinked** (never copied) to avoid drift.

### Harness frontmatter fields

Each `.yaml` file must contain only fields that harness recognizes — see `.ai/skills/cross-skills/references/harness-frontmatter.md` for the exact per-harness field list. Mixing fields across harnesses silently breaks things.

### cross-rules skill

`cross-rules/SKILL.md` is a standalone Claude Code skill (not using the `.ai/skills/` structure). It manages a parallel architecture for project-level *rules* (distributing content from `.ai/rules/` to `CLAUDE.md`, `AGENTS.md`, `.cursor/rules/`, `.github/instructions/`).

### .reference-skills/

External reference skill implementations organized by category (`agentsmd/`, `claudemd/`, `skill-quality/`). Used as examples when generating new skills — not part of the build output.

## Key constraints

- The build script writes **only** to the four harness skills folders. Never write to `CLAUDE.md`, `AGENTS.md`, `.cursor/rules/`, or `.github/instructions/` from within a skill.
- Non-`.yaml` files must be symlinked, not copied, to prevent silent drift.
- `SKILL.md` files should be tiny: frontmatter + one `@content.md` line. Any `SKILL.md` over ~10 lines is a copy-paste violation.
- Skill quality is governed by the 10-axis rubric in `.ai/skills/cross-skills/references/skill-quality-checklist.md`.

<!-- cross-rules:imports:start -->
@file .ai/rules/root.md
<!-- cross-rules:imports:end -->
