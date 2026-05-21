# Validator

Validates that the project structure matches the lnx-multi-ai architecture. Run all checks before printing the report — do not stop at the first finding.

---

## Project-Context Checks

| Severity | Check | Description |
|---|---|---|
| error | Missing `project-context.md` | `.ai/project-context.md` does not exist |
| error | Harness file not a symlink | `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, or `.github/copilot-instructions.md` exists but is a regular file instead of a symlink |
| error | Symlink wrong target | Any of the four harness symlinks does not point to `.ai/project-context.md` |
| error | Forbidden folder exists | `.ai/rules/`, `.cursor/rules/`, or `.github/instructions/` directory exists |
| warning | Harness symlink missing | Any of the four harness symlinks does not exist — run `build-context.py` |
| warning | Project context approaching limit | `.ai/project-context.md` exceeds 200 lines |
| error | Project context too long | `.ai/project-context.md` exceeds 350 lines |

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

## Report Format

Print one line per finding:

```
✓  CLAUDE.md              symlink → .ai/project-context.md
✓  AGENTS.md              symlink → .ai/project-context.md
✓  .cursorrules           symlink → .ai/project-context.md
✗  .github/copilot-instructions.md  missing — run build-context.py
✓  project-context.md     42 lines — within budget
✗  .ai/rules/             forbidden folder exists — delete it
✓  my-skill    claude      SKILL.md OK, symlink OK
✗  my-skill    cursor      SKILL.md contains inline body — no-duplication violation
⚠  my-skill    copilot     SKILL.md frontmatter stale — re-run build script
```

End with a summary line:

```
Validation complete: N errors, N warnings — run build scripts to fix
```

Return an error signal if any errors were found.
