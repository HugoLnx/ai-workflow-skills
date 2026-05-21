# Cleanup: Remove Disabled Harness Output and Legacy Folders

---

## When to run

After disabling one or more harnesses in `.ai/config.yml`, run cleanup to remove their stale output. The script also detects legacy folders (`.cursor/rules/`, `.github/integrations/`) that should not exist in a lnx-multi-ai project.

---

## How to run

```bash
python .ai/skills/lnx-multi-ai/scripts/cleanup.py
```

The script lists everything it would delete — split into harness outputs and legacy folders — then asks for a single confirmation before acting.

---

## What gets deleted

**Harness outputs** (for each disabled harness):

| Harness | Skills folder | Context file |
|---------|--------------|--------------|
| `claude` | `.claude/skills/` | `CLAUDE.md` |
| `codex` | `.agents/skills/` | `AGENTS.md` |
| `cursor` | `.cursor/skills/` | `.cursorrules` |
| `copilot` | `.github/skills/` | `.github/copilot-instructions.md` |

**Legacy folders** (if present, regardless of enabled harnesses):

| Folder | Reason |
|--------|--------|
| `.cursor/rules/` | Old Cursor rules directory — superseded by `.ai/skills/` |
| `.github/integrations/` | Legacy Copilot integrations directory — not used by lnx-multi-ai |

---

## Re-enabling a harness

Re-enable it in `.ai/config.yml`, then rebuild:

```bash
python .ai/skills/lnx-multi-ai/scripts/build-skills.py
python .ai/skills/lnx-multi-ai/scripts/build-context.py
```
