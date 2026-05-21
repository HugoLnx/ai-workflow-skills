# ai-workflow-skills

A collection of AI assistant skills that support the full software development workflow — from specification to implementation — without being tied to any specific AI coding tool.

Skills are authored once under `.ai/skills/` and distributed automatically to **Claude Code**, **OpenAI Codex CLI**, **Cursor**, and **GitHub Copilot** via a build script. One source, four harnesses.

---

## Why

Every AI coding assistant has its own format for custom instructions and skills. Maintaining four separate copies means edits diverge, tooling changes break things, and you're locked into whichever harness you configured first.

This project solves that with a single-source-of-truth layout: write your skill once in `.ai/skills/<name>/`, run the build script, and every supported harness gets an up-to-date output — as symlinks, never copies.

---

## Skills Included

### `lnx-grill-me` — Specification Interviewer

Interviews you one question at a time to produce a **Feature Specification** or **Technical Architecture Specification**. For every answer it writes a critic (issues, missing info, edge cases) before moving on. Session state persists in `.ai/grills/` as `todo.md`, `knowledge.md`, and `history.md`.

- Pluggable **grillers** define the domain and design tree to walk
- Built-in grillers: Generalist Feature, Generalist Technical Architecture, Unity 3D Technical, Game Feature
- Supports `@specialist` skills for parallel domain-enriched critiques
- Recommendations hidden by default — revealed only on request

```
/lnx-grill-me "user authentication flow"
/lnx-grill-me @lnx-security "payment processing"
```

---

### `lnx-ai-global-skills` — Global Skill Manager

Installs, lists, and removes skills from the user's **global** harness folders (`~/.claude/skills/`, `~/.agents/skills/`, etc.) so they're available in every project on the machine.

```
/lnx-ai-global-skills install .ai/skills/lnx-grill-me
/lnx-ai-global-skills list-global
/lnx-ai-global-skills list-local
/lnx-ai-global-skills remove lnx-grill-me
```

`list-local` shows all skills found in the current project with a per-harness build status indicator — `!harness` means the skill exists in source but hasn't been built to that harness yet.

Supports Windows (Developer Mode) and Linux.

---

### `lnx-multi-ai` — Skill & Context Manager

The meta-skill for managing this repository itself. Use it to design, build, migrate, and validate skills and project context across all harnesses.

```
/lnx-multi-ai build skills
/lnx-multi-ai validate
```

---

### `lnx-multi-ai-wall` — Write Guard *(always-on)*

Intercepts any attempt to write directly to harness output files (`CLAUDE.md`, `.claude/skills/`, etc.) and redirects to the correct workflow. Prevents accidental edits to generated files.

---

## How It Works

```
.ai/skills/<name>/
├── content.md              ← skill logic (single source of truth)
├── frontmatter/
│   ├── claude.yaml         ← Claude Code descriptor
│   ├── codex.yaml          ← Codex CLI descriptor
│   ├── cursor.yaml         ← Cursor descriptor
│   └── copilot.yaml        ← GitHub Copilot descriptor
└── references/             ← optional deep-dive reference files
    └── *.md
```

Running the build script distributes each skill to all four harness output folders. Output files are symlinks to the source — edits to `.ai/skills/` are reflected immediately without rebuilding.

| Harness | Output folder | Context file |
|---|---|---|
| Claude Code | `.claude/skills/` | `CLAUDE.md` |
| Codex CLI | `.agents/skills/` | `AGENTS.md` |
| Cursor | `.cursor/skills/` | `.cursorrules` |
| GitHub Copilot | `.github/skills/` | `.github/copilot-instructions.md` |

---

## Getting Started

**Requirements**: Python 3.9+, PyYAML

```bash
git clone https://github.com/<you>/ai-workflow-skills
cd ai-workflow-skills
pip install -r requirements.txt

# Build all skills to harness output folders
python .ai/skills/lnx-multi-ai/scripts/build-skills.py

# Build project context symlinks
python .ai/skills/lnx-multi-ai/scripts/build-context.py
```

Both scripts are idempotent — safe to run any number of times.

### Install skills globally (optional)

Make skills available across all your projects:

```bash
python .ai/skills/lnx-ai-global-skills/scripts/lnx-ai-global-skills.py install .ai/skills/lnx-grill-me
python .ai/skills/lnx-ai-global-skills/scripts/lnx-ai-global-skills.py install .ai/skills/lnx-multi-ai
# ... or install all at once from Claude Code:
# /lnx-ai-global-skills install all local skills
```

---

## Adding Your Own Skills

1. Create `.ai/skills/<your-skill>/content.md` with your skill logic
2. Add `frontmatter/<harness>.yaml` for each harness you want to target
3. Run `python .ai/skills/lnx-multi-ai/scripts/build-skills.py`

The `lnx-multi-ai` skill can guide you through design, frontmatter, and validation interactively.

### Adding a Custom Griller

Drop a `<name>-griller.md` into `.ai/skills/lnx-grill-me/references/` — no rebuild needed, the `references/` folder is symlinked directly.

---

## Project Structure

```
.ai/
├── project-context.md      ← always-on context (symlinked to CLAUDE.md etc.)
├── config.yml              ← harness enable/disable and path overrides
└── skills/
    ├── lnx-grill-me/
    ├── lnx-ai-global-skills/
    ├── lnx-multi-ai/
    └── lnx-multi-ai-wall/

.claude/skills/             ← generated (do not edit directly)
.agents/skills/             ← generated
.cursor/skills/             ← generated
.github/skills/             ← generated
```

---

## Contributing

Contributions welcome — new skills, new grillers, additional harness support. Open an issue to discuss before sending a large PR.

Please keep each skill focused on a single domain, follow the existing `content.md` structure (purpose statement, When to Use, When NOT to Use, process flow, anti-patterns, output contracts), and run the build script before committing.

---

## License

MIT
