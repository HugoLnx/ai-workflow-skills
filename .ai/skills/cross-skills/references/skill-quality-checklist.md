# Skill Quality Checklist

Consult this file as the final gate before publishing any generated skill. A skill is ready when every applicable axis passes.

---

## Description Formula

```
[What it does] [When to use it] [Trigger keywords]. NOT for [Exclusions].
```

- Length: 25–50 words ideal, 100 words maximum
- Must contain at least one explicit NOT clause
- Trigger keywords must match the words users actually type
- Example:
  > Generate, translate, validate, and maintain AI coding-assistant skills across Claude Code, Cursor, Codex, and Copilot from a single source of truth. Use when authoring new skills, porting configs, or auditing harness folders. NOT for CLAUDE.md, AGENTS.md, or any project-level harness config.

---

## 10-Axis Quality Rubric

### Axis 1 — Description Quality (2× weight)
- [ ] Follows `[What] [When] [Keywords]. NOT for [Exclusions]` formula
- [ ] 25–50 words (flag if >100)
- [ ] NOT clause names specific exclusions, not vague categories

### Axis 2 — Scope Discipline (2× weight)
- [ ] Skill covers exactly one expertise domain
- [ ] `When to use` section lists concrete trigger phrases
- [ ] `NOT for` section lists concrete exclusions

### Axis 3 — Progressive Disclosure
- [ ] `content.md` is under 500 lines
- [ ] Deep content lives in `references/` files
- [ ] Every reference file is listed in content.md's References table with a one-line "Consult When" description

### Axis 4 — Anti-Pattern Coverage
- [ ] At least 3 anti-patterns present
- [ ] Each uses the full 5-field template (see below)
- [ ] Timelines use concrete dates or version anchors, not vague "before/after"

### Axis 5 — Self-Contained Tools
- [ ] Any referenced script is complete (no pseudocode stubs)
- [ ] Scripts include error handling and a usage/help line
- [ ] Dependencies are documented; OR "no tools needed" is explicitly stated

### Axis 6 — Activation Precision
- [ ] Trigger keywords are domain-specific, not generic ("skill generation" not "files")
- [ ] NOT clause prevents at least one realistic false-positive scenario
- [ ] Skill does not overlap an adjacent skill without an explicit boundary statement

### Axis 7 — Visual Artifacts
- [ ] Every decision tree or branching flow has a Mermaid `flowchart TD` diagram
- [ ] Multi-column comparisons use markdown tables, not prose
- [ ] Diagrams are placed adjacent to the prose they illustrate

### Axis 8 — Output Contracts
- [ ] Each mode or major action defines an explicit output format
- [ ] Templates use `<angle-bracket>` placeholders for variable slots
- [ ] Edge cases (empty result, error state, already-exists) are documented

### Axis 9 — Temporal Awareness
- [ ] `content.md` contains an `as of [YYYY-MM-DD]` marker
- [ ] `CHANGELOG.md` exists in the skill folder with at least one dated entry
- [ ] Any third-party API behavior described is dated

### Axis 10 — Documentation Quality
- [ ] `CHANGELOG.md` follows: `## [version] — YYYY-MM-DD` / `### Added / Changed / Fixed`
- [ ] Reference filenames are self-describing (`mode-generate.md`, not `ref2.md`)
- [ ] Every cross-reference in content.md points to an actually existing file (no phantoms)

---

## Anti-Pattern Template

Copy this block for each anti-pattern:

```markdown
### Anti-Pattern: [Short Name]
**Novice**: "[Wrong assumption stated as the novice would say it]"
**Expert**: [Why it is wrong + the correct approach in 2–4 sentences]
**Timeline**: [Date/version]: [old behavior] → [Date/version]: [new behavior]
**LLM mistake**: [Why language models default to the wrong pattern]
**Detection**: [Concrete signal that this anti-pattern is present in a file or output]
```

---

## Pre-Publish Gate

Run in order before finalizing any generated skill:

1. **Word-count the description** — if >100 words, trim before proceeding
2. **Count anti-patterns** — must be ≥3 with all 5 fields; add more if short
3. **Check decision flows** — every branching process must have a Mermaid diagram; add any missing
4. **Confirm CHANGELOG.md** exists with a dated `[0.1.0]` entry
5. **Confirm `as of [date]`** marker is present in `content.md`

Only after all 5 pass: run validate mode on the generated skill folder, then print the creation summary.
