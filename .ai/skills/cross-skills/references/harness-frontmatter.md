# Harness Frontmatter Reference

Consult this file when writing or validating frontmatter for any harness. Each harness `.yaml` file contains **only** the fields recognized by that harness — never mix fields across harnesses.

---

## Claude Code (`claude.yaml`)
Written to: `.claude/skills/<name>/SKILL.md`

| Field | Required | Notes |
|---|---|---|
| `description` | yes | When Claude should invoke this skill. Used for auto-triggering. Follow `[What] [When] [Keywords]. NOT for [Exclusions]` pattern. |
| `allowed-tools` | no | Tools Claude may call. List format. Examples: `Read`, `Write`, `Edit`, `Bash`, `Glob`, `Grep`, `WebSearch`. |
| `argument-hint` | no | Hint shown in slash-command autocomplete for expected arguments. |

**Invalid keys** (silently ignored or cause errors):

| Wrong key | Correct alternative |
|---|---|
| `tools:` | `allowed-tools:` |
| `triggers:` | Use `description` keywords instead |
| `globs:` | Not a Claude Code field |

```yaml
description: |
  Generate, translate, validate, and maintain AI coding assistant
  configurations across Claude Code, Cursor, Codex, and Copilot.
  Modes: analyze | generate | translate | validate | build-skill.
  NOT for: CLAUDE.md, AGENTS.md, .cursor/rules/, .github/instructions/.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
argument-hint: "analyze | generate | translate | validate | build-skill"
```

---

## OpenAI Codex CLI (`codex.yaml`)
Written to: `.agents/skills/<name>/SKILL.md`

| Field | Required | Notes |
|---|---|---|
| `description` | yes | When the agent should apply this skill. |
| `tools` | no | Allowed tools/builtins. Examples: `shell`, `read_file`, `write_file`. |
| `tags` | no | Categorization tags for discoverability. List format. |

```yaml
description: |
  Generate, translate, validate, and maintain AI coding assistant
  configurations across multiple agent frameworks.
  Modes: analyze | generate | translate | validate | build-skill.
tools:
  - shell
  - read_file
  - write_file
tags:
  - config
  - dx
  - multi-agent
  - skills
```

---

## Cursor (`cursor.yaml`)
Written to: `.cursor/skills/<name>/SKILL.md`

| Field | Required | Notes |
|---|---|---|
| `description` | yes | When to apply this skill. |
| `globs` | no | File patterns that trigger automatic application. Empty list = on-request only. |
| `alwaysApply` | no | Inject into every request if `true`. Default `false`. Use sparingly. |

**Note**: `.cursor/rules/` is a project-level location and is strictly out of scope. This skill writes only to `.cursor/skills/`.

```yaml
description: |
  Maintain and generate cross-agent skill configurations from a single
  source of truth under .ai/skills/.
globs: []
alwaysApply: false
```

---

## GitHub Copilot (`copilot.yaml`)
Written to: `.github/skills/<name>/SKILL.md`

| Field | Required | Notes |
|---|---|---|
| `applyTo` | yes | Glob pattern for which files or contexts this skill applies to. Use `"**"` for global application. |

**Note**: `.github/instructions/` is a project-level location and is strictly out of scope. This skill writes only to `.github/skills/`.

```yaml
applyTo: "**"
```

---

## SKILL.md Format (all harnesses)

Each harness `SKILL.md` contains **only** the frontmatter block followed by `@content.md`. It never duplicates the body of `content.md`.

```markdown
---
description: |
  ...
allowed-tools:
  - Read
---

@content.md
```

The `@content.md` line uses Claude Code's native file-inclusion syntax. For harnesses that do not support inline file inclusion, the build script may expand the reference at build time — but `content.md` in `.ai/skills/` remains the single canonical copy.
