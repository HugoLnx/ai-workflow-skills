# Mode: validate

**Triggers**: "validate skills", "audit skills", "check harness files", "lint skills", "are skills in sync"

**Goal**: audit the four harness skill folders for correctness and report findings.

---

## Checks

Run all checks and collect findings before printing the report. Do not stop at the first error.

| Severity | Check | Description |
|---|---|---|
| error | Missing `content.md` | `.ai/skills/<name>/` directory exists but no `content.md` |
| error | Missing `.yaml` file | Any of `claude.yaml`, `codex.yaml`, `cursor.yaml`, `copilot.yaml` absent from `.ai/skills/<name>/` |
| error | Broken symlink | Harness `content.md` symlink missing or pointing to a non-existent target |
| error | Duplicated inline content | `SKILL.md` in a harness folder contains the full skill body instead of `@content.md` — no-duplication violation |
| error | Missing required frontmatter field | Required fields absent per harness (consult `references/harness-frontmatter.md`) |
| error | YAML parse error | Malformed `.yaml` file; show path and parse error |
| warning | Stale `SKILL.md` | Frontmatter in a harness `SKILL.md` does not match the corresponding `<harness>.yaml` — suggest re-running the build script |
| info | Extra files | Files in a harness skill folder that are neither `SKILL.md`, `content.md`, nor a symlink into `.ai/skills/<name>/` |

---

## Report format

Print one line per finding, grouped by skill then harness:

```
✓  my-skill    claude   SKILL.md OK, symlink OK
✓  my-skill    codex    SKILL.md OK, symlink OK
✗  my-skill    cursor   SKILL.md contains inline body — violation: no duplication
⚠  my-skill    copilot  SKILL.md frontmatter stale — re-run build script
✗  other-skill claude   content.md symlink broken → .ai/skills/other-skill/content.md not found
✗  bad-skill   (source) content.md missing in .ai/skills/bad-skill/
⚠  solo-skill  (source) cursor.yaml missing — harness will be skipped by build script
```

End with a summary line:

```
Validation complete: 2 errors, 1 warning, 1 info — run .ai/build-skills.ps1 to fix stale files
```

Exit (or return an error indicator) if any errors were found.
