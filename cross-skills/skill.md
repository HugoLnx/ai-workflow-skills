---
name: cross-skills
description: >
  Generate, translate, validate, and maintain AI coding assistant configurations
  across Claude Code, Cursor, OpenAI Codex CLI, and Aider ecosystems.
  Use when: generating configs for a new repo, translating existing configs between
  tools, validating existing config files for errors or conflicts, analyzing a
  codebase to extract its conventions, or building reusable skill files.
  Modes: analyze | generate | translate | validate | build-skill.
  Examples: "generate Cursor rules from this repo", "translate CLAUDE.md to Aider",
  "validate my .cursor/rules", "analyze this codebase and build configs for all agents",
  "build a code-review skill for this project", "set up cross-agent configs".
---

# Cross-Skills: Universal AI Agent Configuration Manager

You are operating as the **cross-skills** meta-skill. Your role is to generate,
translate, validate, and maintain AI coding assistant configuration files across
multiple agent ecosystems using a Universal Intermediate Representation (UIR) as
the common language.

## Project Layout

This skill is part of the `cross-skills` project. Key resource paths:

- **UIR schema**: `schema/uir.schema.json`
- **Ecosystem capability matrix**: `schema/capability-matrix.json`
- **Templates root**: `templates/`
- **Validation rules**: `validation/rules.json`
- **Translation gap reference**: `validation/gap-analysis.md`

---

## Operating Modes

Determine the mode from the user's request, then follow the corresponding module.

### Mode: `analyze`

**Trigger phrases**: "analyze this repo", "scan the codebase", "extract conventions",
"what are the conventions here", "build a UIR for", "onboard this project"

**Action**: Read `modules/analyzer.md` and follow its instructions exactly.

Goal: Survey a repository and produce a `uir.json` file capturing all AI-relevant
conventions, tech stack, rules, permissions, and context.

---

### Mode: `generate`

**Trigger phrases**: "generate configs", "set up agent configs", "create CLAUDE.md",
"create Cursor rules", "generate AGENTS.md", "set up for all agents",
"produce configs from UIR"

**Action**: Read `modules/generator.md` and follow its instructions exactly.

Goal: Accept a UIR document (file path or inline JSON) and produce ecosystem-specific
configuration files for one or more target ecosystems.

---

### Mode: `translate`

**Trigger phrases**: "translate to", "convert from X to Y", "port configs",
"migrate from Cursor to Claude Code", "adapt CLAUDE.md for Aider",
"translate AGENTS.md to Cursor"

**Action**: Read `modules/translator.md` and follow its instructions exactly.

Goal: Parse an existing ecosystem's config files into UIR, then delegate to the
generator to produce output for the target ecosystem. Annotate all fidelity losses.

---

### Mode: `validate`

**Trigger phrases**: "validate", "lint configs", "check for errors", "audit my rules",
"find conflicts", "check my CLAUDE.md", "verify .cursor/rules"

**Action**: Read `modules/validator.md` and follow its instructions exactly.

Goal: Check one or more config files against the validation rules in
`validation/rules.json` and produce a structured report.

---

### Mode: `build-skill`

**Trigger phrases**: "build a skill", "create a skill", "generate a skill for",
"make a reusable skill", "add a skill to the library", "skill for code review",
"custom skill"

**Action**: Read `modules/builder.md` and follow its instructions exactly.

Goal: Generate a new reusable skill using the cross-tool `content.md` layout —
shared instructions in `.ai/skills/<name>/content.md`, per-harness `SKILL.md` files
with harness-specific frontmatter in `.claude/skills/`, `.agents/skills/`,
`.cursor/skills/`, and `.github/skills/`, with symlinks wiring each harness
directory's `content.md` to the shared source. Optionally also translate to
Aider CONVENTIONS.md sections.

---

## Mode Inference (when not explicit)

| User says... | Infer mode |
|---|---|
| References a repo path or directory, no output target | `analyze` |
| "create", "generate", "set up" + ecosystem name | `generate` |
| Two ecosystem names ("X to Y", "from X", "for Cursor") | `translate` |
| "check", "lint", "validate", "audit", "verify" | `validate` |
| "skill", "reusable", "build a prompt", "module" | `build-skill` |
| Ambiguous | Ask: "Should I analyze the repo, generate configs, translate existing configs, validate them, or build a skill?" |

---

## Universal Intermediate Representation

The UIR is a JSON document conforming to `schema/uir.schema.json`. It contains:

- `meta` — identity, version, provenance
- `context` — project summary, tech stack, directory layout, build commands, env vars
- `rules` — behavioral rules (scope, priority, category, content, rationale, examples)
- `permissions` — tool allow/deny/ask lists (Claude Code native)
- `memory` — always-load, on-demand, and ignore file lists
- `hooks` — lifecycle shell commands (Claude Code native)
- `skills` — reusable task skill definitions
- `agents` — sub-agent definitions
- `ignore_patterns` — unified ignore globs
- `extensions` — ecosystem-specific overrides

---

## Ecosystem Support

| Ecosystem ID | Config Files | Notes |
|---|---|---|
| `claude-code` | CLAUDE.md, AGENTS.md, settings.json, `.claude/skills/` | Full UIR fidelity |
| `cursor` | .cursor/rules/*.mdc, `.cursor/skills/` | Permissions/hooks degrade to rule text |
| `codex` | AGENTS.md, system-prompt.txt, `.agents/skills/` | Glob scoping flattened; unknown frontmatter causes errors |
| `aider` | .aider.conf.yml, CONVENTIONS.md, .aiderignore | Least expressive; hooks dropped |
| `copilot` | `.github/skills/` | `name` + `description` frontmatter only |

Skills harness folders follow the cross-tool open standard: `.agents/skills/` is recognized
by Cursor, Copilot, and Codex in addition to their own per-tool directories. Per-tool
directories (`.claude/skills/`, `.cursor/skills/`, `.github/skills/`) are preferred
when harness-specific frontmatter is needed.

Extensible to: windsurf, roo-code, continue, cline, openhand, gemini-cli.

---

## Output Standards

All generated files must:
1. Include a header comment: `# Generated by cross-skills — edit uir.json to update`
2. Use `# CROSS-SKILLS: DEGRADED — <reason>` for any lost-fidelity content
3. Use `# CROSS-SKILLS: NOT TRANSLATABLE — <reason>` for dropped content
4. Follow the exact syntax conventions of the target ecosystem
5. Be complete and immediately usable without further editing (except filling in
   project-specific values marked with `{{PLACEHOLDER}}`)

---

## Error Handling

- If a UIR file is referenced but not found: stop and ask the user for the correct path
- If the source ecosystem config files are missing: list what was expected and ask
- If the UIR fails schema validation: run validate mode first, show the errors, ask
  the user to fix them before proceeding
- If the user's request is ambiguous: ask one clarifying question, do not guess
