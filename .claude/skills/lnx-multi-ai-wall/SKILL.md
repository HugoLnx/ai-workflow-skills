---
description: |
  Guard that intercepts writes to AI harness output files. Always active.
  Blocks any attempt to write CLAUDE.md, AGENTS.md, .cursorrules,
  .github/copilot-instructions.md, .claude/skills/, .agents/skills/,
  .cursor/skills/, or .github/skills/ and redirects to the lnx-multi-ai skill.
  NOT for: reading those files, running build scripts, or editing .ai/ source files.
---

@content.md
