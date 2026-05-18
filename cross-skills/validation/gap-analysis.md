# Cross-Agent Translation Gap Analysis

This document describes what is preserved, degraded, and lost when translating
configurations between AI coding assistant ecosystems via the UIR.

See `schema/capability-matrix.json` for the machine-readable version.

---

## Fidelity Scores (1–10)

| Source → Target | Score | Notes |
|---|---|---|
| Claude Code → Cursor | 7/10 | Permissions/hooks degrade; env vars dropped |
| Claude Code → Codex CLI | 6/10 | Glob scoping lost; hooks dropped |
| Claude Code → Aider | 5/10 | Most scoping lost; hooks dropped |
| Cursor → Claude Code | 8/10 | High fidelity; Cursor has no permissions/hooks to lose |
| Aider → Claude Code | 6/10 | Good context recovery; permissions/hooks cannot be inferred |
| Codex CLI → Claude Code | 7/10 | Agents translate well; no scoping to recover |

---

## Claude Code → Cursor

### Transferred with full fidelity
- Global rules (all categories) → `00-critical.mdc`, `01-conventions.mdc`
- File-glob scoped rules → individual `.mdc` files with `globs:` frontmatter
- Project context (summary, tech stack, directory layout) → `index.mdc`
- Ignore patterns → `.cursorignore`
- Memory always-load → `alwaysApply: true` rules (content, not file-loading)
- Language-scoped rules → `.mdc` files with language-specific globs

### Degraded (reduced functionality)
- **Permissions allow/deny** → Converted to `alwaysApply: true` rule text.
  No enforcement — the AI can read these as guidance, but Cursor has no tool
  permission system. The intent is preserved; the enforcement is not.
  _Output annotation_: `# CROSS-SKILLS: DEGRADED — permissions converted to rule text (no enforcement)`

- **Lifecycle hooks** → Converted to "always do X before/after Y" rule text.
  The hook commands are not executed. The developer must wire them up manually.
  _Output annotation_: `# CROSS-SKILLS: DEGRADED — hook converted to rule text (not executed automatically)`

- **Skills** → Converted to manual-activation `.mdc` files (`50-skill-*.mdc`).
  Must be referenced with `@filename` in the prompt. No structured activation.
  _Output annotation_: `# CROSS-SKILLS: DEGRADED — skill converted to manual .mdc; activate with @50-skill-<id>`

- **Sub-agents** → Flattened to a context section in `index.mdc`.
  Agent role descriptions are preserved; orchestration capability is lost.
  _Output annotation_: `# CROSS-SKILLS: DEGRADED — sub-agents flattened to context (no orchestration in Cursor)`

### Dropped (no equivalent)
- **Environment variable definitions** → Not supported in Cursor configs.
  _Output annotation_: `# CROSS-SKILLS: NOT TRANSLATABLE — Cursor has no env var config`

---

## Claude Code → OpenAI Codex CLI

### Transferred with full fidelity
- Project context (summary, tech stack, directory layout, build commands)
- Global rules → flat numbered list in `AGENTS.md ## Instructions`
- Sub-agent definitions → `AGENTS.md ## AgentName` sections (native format)
- Agent roles and tool lists

### Degraded (reduced functionality)
- **File-glob scoped rules** → Flattened to global instructions with
  `(applies when working on: <glob>)` text annotation. Codex applies these
  globally but the intended scope is documented.
  _Output annotation_: `# CROSS-SKILLS: DEGRADED — file-glob scoping not supported; rule flattened`

- **Permissions** → Converted to instruction text (`Do not run: <pattern>`)
  _Output annotation_: `# CROSS-SKILLS: DEGRADED — permissions converted to instruction text`

- **Memory always_load** → Listed as "always consider these files for context"
  in the Instructions section. Codex CLI does not automatically include them.
  _Output annotation_: `# CROSS-SKILLS: DEGRADED — memory files listed as context hints; not auto-loaded`

- **Skills** → Appended as `## Available Tasks` section entries.
  No activation mechanism — must be referenced in prompts manually.

### Dropped (no equivalent)
- **Lifecycle hooks** → No equivalent in Codex CLI.
  _Output annotation_: `# CROSS-SKILLS: NOT TRANSLATABLE — lifecycle hooks not supported in Codex CLI`

- **Ignore patterns** → Codex CLI has no ignore configuration.
  _Output annotation_: `# CROSS-SKILLS: NOT TRANSLATABLE — Codex CLI has no ignore file support`

- **Environment variables** → Codex CLI environment is managed externally.
  _Output annotation_: `# CROSS-SKILLS: NOT TRANSLATABLE`

---

## Claude Code → Aider

### Transferred with full fidelity
- Project context → `CONVENTIONS.md` overview section
- Global rules → `CONVENTIONS.md` category sections
- Memory always_load → `.aider.conf.yml` `read:` list
- Ignore patterns → `.aiderignore`
- Environment variables → `.aider.conf.yml` (as `--env-file` reference, example only)
- Model selection → `.aider.conf.yml` `model:`

### Degraded (reduced functionality)
- **File-glob scoped rules** → Flattened to global convention sections with
  `(applies to: <glob>)` annotation. Aider applies all CONVENTIONS.md globally.
  _Output annotation_: `# CROSS-SKILLS: DEGRADED — file-glob scoping not supported; rule flattened`

- **Directory-scoped rules** → Same as file-glob: flattened.

- **Permissions** → Deny list becomes "Never run: <pattern>" in CONVENTIONS.md.
  Allow list is omitted (Aider doesn't restrict by default).
  _Output annotation_: `# CROSS-SKILLS: DEGRADED — permissions converted to convention text`

- **Sub-agents** → Each agent becomes a named `## <Agent Name> Role` section
  in CONVENTIONS.md. No orchestration — context only.
  _Output annotation_: `# CROSS-SKILLS: DEGRADED — sub-agents flattened to CONVENTIONS.md sections`

- **Skills** → Each skill becomes a `## Skill: <name>` section in CONVENTIONS.md.
  Users must reference it manually in their Aider prompts.
  _Output annotation_: `# CROSS-SKILLS: DEGRADED — skill converted to CONVENTIONS.md section`

### Dropped (no equivalent)
- **Lifecycle hooks** → No equivalent.
  _Output annotation_: `# CROSS-SKILLS: NOT TRANSLATABLE — hooks not supported in Aider`

---

## Cursor → Claude Code

Very high fidelity — Cursor has fewer features than Claude Code, so nothing
is lost in this direction. The translation adds Claude Code capabilities (permissions,
hooks, skills) that must be populated manually after translation.

### Transferred with full fidelity
- Always-apply `.mdc` rules → CLAUDE.md `## AI Behavior Rules` sections
- Glob-scoped `.mdc` rules → CLAUDE.md `## File-Specific Rules` sections, or nested CLAUDE.md files
- Project context from `index.mdc` → CLAUDE.md header sections
- Ignore patterns from `.cursorignore` → `ignore_patterns[]` in UIR → respected by Claude Code

### Fields added (not in source)
After translation, these UIR fields will be empty and require manual population:
- `permissions.allow` / `permissions.deny`
- `hooks[]`
- `skills[]` (unless manual `.mdc` files existed)

---

## Aider → Any Ecosystem

Aider is the **least expressive** source format. UIR produced from Aider will have:
- Many rules with `_degraded: true` (scope annotations from conventions but no real scoping)
- Empty `hooks[]` (no equivalent in Aider)
- Empty `permissions` (no equivalent in Aider)
- Empty or minimal `agents[]` (unless CONVENTIONS.md had named agent sections)

When translating Aider → Claude Code or Aider → Cursor, you gain capabilities
(permissions, hooks, scoping) that were never in Aider. These must be added manually.

---

## Recommended Practices

1. **Start with analyze mode**: Point `cross-skills analyze` at your repo to get
   an accurate UIR rather than translating from a potentially incomplete config.

2. **Claude Code as source of truth**: Claude Code has the highest UIR fidelity.
   If you maintain multiple ecosystems, generate all from Claude Code UIR.

3. **Validate before translating**: Run `cross-skills validate` on the source configs
   before translation to catch issues that would compound in the output.

4. **Review degradation annotations**: After translation, search for
   `CROSS-SKILLS: DEGRADED` and `CROSS-SKILLS: NOT TRANSLATABLE` in output files
   and decide whether the degraded behavior is acceptable.

5. **Keep UIR as the single source**: After initial setup, edit `uir.json` and
   regenerate rather than editing ecosystem config files directly.
