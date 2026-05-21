# Core: Folder Structure and Equivalences

Always load this reference. It defines where things live and what they mean.

---

## Hard Restriction

The agent writes **only** to `.ai/` source files. The build scripts are the sole writers of harness output. Active harnesses and output paths are configured in `.ai/config.yml` — edit it to enable, disable, or relocate harness output.

Never write to `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `.github/copilot-instructions.md`, `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, or `.github/skills/` directly. If you catch yourself about to do so, stop and consult `lnx-multi-ai-wall`.

---

## `.ai/project-context.md` — Project Context Source of Truth

A single markdown file containing always-on project-level context. The project-context builder ensures `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, and `.github/copilot-instructions.md` always reflect this file.

**Equivalence**: `.ai/project-context.md` has the same meaning and purpose as `CLAUDE.md` and `AGENTS.md` — it is the project-level context the agent reads on every session.

Edit only `.ai/project-context.md` — never the harness files directly.

**Forbidden**: `.ai/rules/`, `.cursor/rules/`, `.github/instructions/` — these folders must not exist.

---

## `.ai/skills/` — Skill Source of Truth

Each skill lives under `.ai/skills/<name>/` as a directory with a `content.md` body and per-harness frontmatter. The skill builder ensures the four harness skill folders (`.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`) always reflect the source.

Edit only files under `.ai/skills/` — never the harness skill folders directly.
