# Skill Frontmatter Expert

Supported fields per harness for skill frontmatter. Each `frontmatter/<harness>.yaml` file must contain **only** the fields recognized by that harness — never mix fields across harnesses.

---

## Creation Rule

When creating a new skill, **always create all four frontmatter files**:

```
frontmatter/claude.yaml
frontmatter/codex.yaml
frontmatter/cursor.yaml
frontmatter/copilot.yaml
```

Whether a harness is `enabled: false` in `.ai/config.yml` is irrelevant at creation time — that flag only controls whether the build script writes output to that harness. The frontmatter files must always exist so the skill is ready to build for any harness at any time without requiring edits to the source.

---

## Claude Code (`claude.yaml`)

Written to: `.claude/skills/<name>/SKILL.md`

| Field | Required | Notes |
|---|---|---|
| `description` | yes | When Claude should invoke this skill. Follow `[What] [When] [Keywords]. NOT for [Exclusions]` pattern. |
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
  [What it does] [when to use it] [trigger keywords].
  NOT for: [specific exclusions].
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
argument-hint: "mode-a | mode-b | mode-c"
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
  [What it does] [when to use it] [trigger keywords].
tools:
  - shell
  - read_file
  - write_file
tags:
  - config
  - dx
```

---

## Cursor (`cursor.yaml`)

Written to: `.cursor/skills/<name>/SKILL.md`

| Field | Required | Notes |
|---|---|---|
| `description` | yes | When to apply this skill. |
| `globs` | no | File patterns that trigger automatic application. Empty list = on-request only. |
| `alwaysApply` | no | Inject into every request if `true`. Default `false`. Use sparingly. |

```yaml
description: |
  [What it does] [when to use it].
globs: []
alwaysApply: false
```

---

## GitHub Copilot (`copilot.yaml`)

Written to: `.github/skills/<name>/SKILL.md`

| Field | Required | Notes |
|---|---|---|
| `applyTo` | yes | Glob pattern for which files or contexts this skill applies to. Use `"**"` for global. |

```yaml
applyTo: "**"
```

---

## SKILL.md Format (all harnesses)

Each harness `SKILL.md` contains the frontmatter block followed by the full skill body. The body is embedded by `build-skills.py` from `.ai/skills/<name>/content.md` — do not write `@content.md` or paste content manually.

```markdown
---
description: |
  ...
allowed-tools:
  - Read
---

# <skill-name> — as of YYYY-MM-DD

## Description
...
```

Any `SKILL.md` containing only `@content.md` after the closing `---` was built with the old system — re-run `build-skills.py` to regenerate it with inline content.
