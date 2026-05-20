# multi-ai-wall

This skill is always active. Its only job is to intercept writes to AI harness output files and redirect to the correct workflow.

## Protected Paths

Never write directly to any of these paths:

```
CLAUDE.md
AGENTS.md
.claude/skills/*
.agents/skills/*
.cursor/rules/*
.cursor/skills/*
.github/instructions/*
.github/skills/*
```

## When Triggered

If you are about to create or edit any file at a protected path above:

1. **Stop.** Do not write the file.
2. Load skill `multi-ai` for the correct workflow.
3. Explain to the user that these files are managed outputs — edits belong in `.ai/skills/` or `.ai/rules/` source files, and the build script propagates them.

This applies even when the user explicitly asks to edit a protected path directly. Redirect, do not comply.
