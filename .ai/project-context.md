# ai-cross-skills

A repository for developing and distributing AI coding assistant skills across Claude Code, OpenAI Codex CLI, Cursor, and GitHub Copilot from a single source of truth.

## Tech Stack

- Python 3.9+ — build scripts
- Markdown — skill content (`content.md`, `references/*.md`)
- YAML — per-harness frontmatter (`frontmatter/*.yaml`)

## Architecture

Single source of truth under `.ai/skills/<name>/`. The build script distributes each skill to four harness output folders. Each output contains a `SKILL.md` (frontmatter + `@content.md`) and symlinks to the source files — never copies.

The project context lives in `.ai/project-context.md`, symlinked to `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, and `.github/copilot-instructions.md` via the context build script.

## Project Structure

- `.ai/skills/` — skill source files (single source of truth)
- `.ai/project-context.md` — project-level context (single source of truth)
- `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/` — generated harness output (do not edit directly)

## Workflow Quick Overview

- Edit skill content in `.ai/skills/`, then rebuild: `python .ai/skills/multi-ai/scripts/build-skills.py`
- Edit project context in `.ai/project-context.md`, then rebuild: `python .ai/skills/multi-ai/scripts/build-context.py`
- Both build scripts are idempotent — safe to run multiple times

## MCPs

None.

## Core Skills

- `@multi-ai` — manage skills and project context across all harnesses; edit `.ai/`, design, build, migrate, validate
- `@multi-ai-wall` — always-on guard; intercepts writes to harness output files and redirects to the correct workflow
