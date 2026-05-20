# Core: Folder Structure and Equivalences

Always load this reference. It defines where things live and what they mean.

---

## Hard Restriction

The agent writes **only** to `.ai/` source files. The build scripts are the sole writers of harness output.

Never write to `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `.github/copilot-instructions.md`, `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, or `.github/skills/` directly. If you catch yourself about to do so, stop and consult `multi-ai-wall`.

---

## `.ai/project-context.md` — Project Context Source of Truth

A single markdown file containing always-on project-level context. Distributed to all harnesses via symlinks:

| Symlink | Points to |
|---|---|
| `CLAUDE.md` | `.ai/project-context.md` |
| `AGENTS.md` | `.ai/project-context.md` |
| `.cursorrules` | `.ai/project-context.md` |
| `.github/copilot-instructions.md` | `.ai/project-context.md` |

**Equivalence**: `.ai/project-context.md` IS `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, and `.github/copilot-instructions.md` — they are the same file via symlinks. Edit only the source.

**Forbidden**: `.ai/rules/`, `.cursor/rules/`, `.github/instructions/` — these folders must not exist.

Build symlinks with:
```bash
python .ai/skills/multi-ai/scripts/build-context.py
```

---

## `.ai/skills/` — Skill Source of Truth

```
.ai/skills/<name>/
  content.md          # Skill body — pure markdown, no frontmatter
  frontmatter/
    claude.yaml       # Frontmatter for Claude Code
    codex.yaml        # Frontmatter for OpenAI Codex CLI
    cursor.yaml       # Frontmatter for Cursor
    copilot.yaml      # Frontmatter for GitHub Copilot
  references/         # Progressive-disclosure reference files (symlinked to harness folders)
  scripts/            # Helper scripts (symlinked to harness folders)
```

The build script generates one output folder per skill per harness:

| Harness | Output folder |
|---|---|
| Claude Code | `.claude/skills/<name>/` |
| OpenAI Codex CLI | `.agents/skills/<name>/` |
| Cursor | `.cursor/skills/<name>/` |
| GitHub Copilot | `.github/skills/<name>/` |

Each harness output folder contains:
- `SKILL.md` — frontmatter from `frontmatter/<harness>.yaml` + `@content.md` (nothing else)
- `content.md` — symlink to `.ai/skills/<name>/content.md`
- All other files/folders — symlinked at the same relative path (never copied)

**Equivalence**: `.ai/skills/<name>/content.md` is the same thing as the harness `SKILL.md` in meaning and purpose.

Build all harness skill output with:
```bash
python .ai/skills/multi-ai/scripts/build-skills.py
```
