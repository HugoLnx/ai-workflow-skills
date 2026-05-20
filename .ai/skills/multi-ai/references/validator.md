# Validator

Validates that the project structure matches the multi-ai architecture. Run all checks before printing the report — do not stop at the first finding.

---

## Skill Structure Checks

| Severity | Check | Description |
|---|---|---|
| error | Missing `content.md` | `.ai/skills/<name>/` exists but no `content.md` |
| error | Missing `.yaml` file | Any of `claude.yaml`, `codex.yaml`, `cursor.yaml`, `copilot.yaml` absent from `.ai/skills/<name>/frontmatter/` |
| error | Broken symlink | Harness `content.md` symlink missing or pointing to non-existent target |
| error | Duplicated inline content | Harness `SKILL.md` contains the full skill body instead of `@content.md` |
| error | Missing required frontmatter field | Required fields absent per harness (consult `skill-frontmatter-expert.md`) |
| error | YAML parse error | Malformed `.yaml` file; show path and parse error |
| warning | Stale `SKILL.md` | Frontmatter in a harness `SKILL.md` does not match the corresponding `<harness>.yaml` — re-run build script |
| info | Extra files | Files in a harness skill folder that are neither `SKILL.md`, `content.md`, nor a symlink into `.ai/skills/<name>/` |

---

## Rules Structure Checks

| Severity | Check | Description |
|---|---|---|
| error | Orphaned sidecar | `.ai/rules/*.yml` with no matching `.md` |
| error | Invalid YAML | `.yml` sidecar fails to parse; show path and error |
| error | Master root too long | `CLAUDE.md` or `AGENTS.md` exceeds 350 lines |
| warning | Master root approaching limit | `CLAUDE.md` or `AGENTS.md` exceeds 200 lines |
| warning | Multiple rule files | More than one `.ai/rules/*.md` — prefer consolidating |
| warning | Sidecar-less rules | `.ai/rules/*.md` with no matching `.yml` — treated as always-on |
| warning | Stale generated files | `.cursor/rules/*.mdc` or `.github/instructions/*.md` out of sync with source |
| warning | Stale import blocks | Managed block missing rules present in `.ai/rules/` or referencing non-existent paths |
| warning | Code style in rules | Rule body contains `eslint`, `prettier`, `biome`, `ruff`, or style-guide prose |
| warning | Conditional content | Rule body contains "if … then …" patterns — context-specific content belongs in a skill |

---

## Report Format

Print one line per finding:

```
✓  my-skill      claude    SKILL.md OK, symlink OK
✓  my-skill      codex     SKILL.md OK, symlink OK
✗  my-skill      cursor    SKILL.md contains inline body — no-duplication violation
⚠  my-skill      copilot   SKILL.md frontmatter stale — re-run build script
✗  other-skill   claude    content.md symlink broken → .ai/skills/other-skill/content.md not found
✗  bad-skill     (source)  content.md missing in .ai/skills/bad-skill/
✓  CLAUDE.md               152 lines — within budget
⚠  AGENTS.md               224 lines — approaching 200-line preference
✗  legacy.yml   (rules)    orphaned sidecar — no matching .ai/rules/legacy.md
```

End with a summary line:

```
Validation complete: N errors, N warnings — run build script to fix stale files
```

Return an error signal if any errors were found (non-zero exit or explicit error indicator).
