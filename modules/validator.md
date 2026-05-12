# Module: Validator

**Invoked by**: `skill.md` when mode is `validate`

**Purpose**: Check one or more configuration files or a UIR document for structural
errors, broken references, conflicts, syntax issues, and coverage gaps. Produce
a structured report with severity-ranked findings.

---

## Inputs

- **Target**: One of:
  - A path to a `uir.json` file
  - A path to a specific config file (CLAUDE.md, .mdc file, AGENTS.md, .aider.conf.yml)
  - A directory (validates all recognizable config files within it)
  - `all` — validate both UIR and all generated configs in the current directory tree

- **Ecosystem filter** (optional): Limit validation to one ecosystem's rules.
  Values: `claude-code`, `cursor`, `codex`, `aider`, `uir` (UIR schema only).

---

## Validation Rule Set

Rules are defined in `validation/rules.json`. They are grouped into categories.
Each rule produces a finding with:
- **Rule ID** (e.g. `STR-001`)
- **Severity**: `ERROR` (blocks generation/use), `WARNING` (proceed with caution), `INFO` (suggestion)
- **Location**: file path + line number if determinable
- **Message**: human-readable description of the problem
- **Fix**: suggested remediation action

---

## Category: STRUCTURE (STR)

Check that files conform to their expected schema and format.

**STR-001** (ERROR) — Required frontmatter fields present
- For `.mdc` files: `description` and `alwaysApply` must be present in YAML frontmatter
- For `skill.md` files: `name` and `description` must be present in YAML frontmatter
- For `uir.json`: `meta`, `context`, `rules` must be top-level keys

**STR-002** (ERROR) — YAML frontmatter is valid YAML
- Parse the `---` block; if it throws a YAML parse error, report the line and message
- Common mistakes: unquoted colons, tabs instead of spaces, invalid boolean values

**STR-003** (WARNING) — UIR version is valid semver
- `meta.version` must match `^\d+\.\d+\.\d+$`

**STR-004** (ERROR) — UIR enum fields use allowed values
- `meta.source.method`: must be one of `analyze`, `manual`, `translate`
- `meta.source.from_ecosystem`: must be a known ecosystem id or null
- `rules[].scope`: must be one of `global`, `file-glob`, `directory`, `language`, `task-type`
- `rules[].category`: must be a known category value
- `hooks[].event`: must be a known event name

**STR-005** (ERROR) — Cursor `.mdc` `alwaysApply` is a boolean, not a string
- `alwaysApply: true` is valid; `alwaysApply: "true"` is invalid (Cursor parses it as a string)

**STR-006** (WARNING) — UIR `context.project_summary` is substantive
- Warn if under 50 characters; likely a placeholder was not filled in

**STR-007** (INFO) — UIR `rules[]` is non-empty
- A UIR with zero rules will produce configs with no behavioral guidance

---

## Category: REFERENCES (REF)

Check that file paths, IDs, and cross-references resolve.

**REF-001** (WARNING) — `memory.always_load` paths exist
- Each path in `memory.always_load[]` must exist relative to the repo root
- If repo root is unknown, skip with INFO note

**REF-002** (WARNING) — `memory.on_demand` paths exist
- Same as REF-001 for `memory.on_demand[]`

**REF-003** (ERROR) — `rules[].id` values are unique
- No two rules may share the same `id` value within the UIR

**REF-004** (ERROR) — `agents[].id` values are unique

**REF-005** (ERROR) — `skills[].id` values are unique

**REF-006** (WARNING) — Template variable references resolve
- In any `.tmpl` file: every `{{VARIABLE}}` placeholder must correspond to a UIR field
- Unknown placeholders that are not standard template variables: flag as WARNING

**REF-007** (ERROR) — CLAUDE.md `@import` paths exist
- Each `@path/to/file` reference in CLAUDE.md must resolve to an existing file

---

## Category: CONFLICTS (CON)

Check for contradictory or mutually exclusive settings.

**CON-001** (WARNING) — Two rules with same scope have contradictory content
- Heuristic: if two rules with identical `scope` + `scope_value` contain opposite
  keywords (e.g. "always use X" vs "never use X"), flag both with a conflict warning
- Message: "Rules <id1> and <id2> may conflict. Review manually."

**CON-002** (ERROR) — Pattern in both `permissions.allow` and `permissions.deny`
- Check for identical or substring-overlapping patterns in both lists
- Message: "Pattern '<p>' appears in both allow and deny; deny takes precedence in Claude Code."

**CON-003** (ERROR) — File in both `memory.always_load` and `memory.ignore`
- A file that is always loaded cannot also be ignored

**CON-004** (WARNING) — Same rule `id` defined in UIR and in `extensions` override
- The extensions version will overwrite the UIR version; flag for review

**CON-005** (WARNING) — Cursor `.mdc` file has both `alwaysApply: true` and `globs:`
- In Cursor, `globs:` has no effect when `alwaysApply: true`; remove globs or set alwaysApply to false

---

## Category: SYNTAX (SYN) — Ecosystem-specific

**SYN-001** (WARNING) — Cursor glob patterns are valid
- Use picomatch semantics; check for: unbalanced braces, invalid `**` usage, empty patterns

**SYN-002** (WARNING) — Unreachable Cursor rule
- A `.mdc` file with `alwaysApply: false` AND no `globs:` AND no `description` will never auto-activate
- It can only be used with `@filename` manual reference

**SYN-003** (WARNING) — Claude Code hook `command` references undefined env vars
- Check `$VAR` / `${VAR}` references in hook commands; warn if they don't appear in
  `settings.json` env block or common system vars

**SYN-004** (WARNING) — Claude Code permission pattern format
- Patterns should be: bare tool name (`Read`), or `ToolName(glob)` format (`Bash(git *)`)
- Warn on patterns that don't match either form

**SYN-005** (WARNING) — Aider model value format
- `.aider.conf.yml` `model:` value should match `provider/model-name` or known shorthand
  (e.g. `claude-sonnet-4-5`, `gpt-4o`, `gemini-2.0-flash`)

**SYN-006** (ERROR) — `.aider.conf.yml` is valid YAML
- Parse and report any YAML errors

---

## Category: DUPLICATES (DUP)

**DUP-001** (WARNING) — Two rules have identical content
- Compare `rules[].content` after trim/normalize; flag if identical
- Deduplicate by keeping the one with more fields populated

**DUP-002** (ERROR) — Two rules share the same `id`
- IDs must be unique (same as REF-003; cross-check)

**DUP-003** (WARNING) — Same file glob in multiple Cursor `.mdc` files with `alwaysApply: true`
- Both files will always load for matching files, potentially with conflicting guidance

**DUP-004** (INFO) — Same ignore pattern listed multiple times
- Deduplicate `ignore_patterns[]` and `memory.ignore[]` after merging

---

## Category: CIRCULAR (CIR)

**CIR-001** (ERROR) — CLAUDE.md `@import` chain has cycles
- Build a directed graph of `@import` references; detect cycles with DFS
- Message: "Circular @import detected: A → B → C → A"

**CIR-002** (WARNING) — UIR skill cross-references cycle
- Check if `skills[].instructions` references another skill by name that references back

---

## Category: COVERAGE (COV)

**COV-001** (WARNING) — UIR `hooks[]` non-empty but target ecosystem is not Claude Code
- Hooks are Claude Code-native. If generating for Cursor/Codex/Aider, hooks will be
  degraded or dropped. Remind the user.

**COV-002** (WARNING) — UIR `permissions` non-empty but target ecosystem is not Claude Code
- Permissions are Claude Code-native. Will be converted to rule text in other ecosystems.

**COV-003** (WARNING) — UIR `agents[]` non-empty but target is Cursor or Aider
- Sub-agent orchestration is not supported; agents will be flattened to context sections.

**COV-004** (WARNING) — UIR `rules[]` has `scope: "file-glob"` entries and target is Codex or Aider
- File-glob scoping is not natively supported; rules will be flattened.

**COV-005** (INFO) — UIR `permissions.allow` and `permissions.deny` are both empty
- Consider adding explicit permission rules for security-sensitive projects.

**COV-006** (INFO) — UIR `skills[]` is empty
- Consider running `build-skill` mode to generate reusable skill files for this project.

---

## Validation Execution Order

1. Parse the target file(s) / UIR
2. Run STRUCTURE checks first (fail fast on unparseable files)
3. Run REFERENCES checks
4. Run CONFLICTS checks
5. Run SYNTAX checks (ecosystem-specific)
6. Run DUPLICATES checks
7. Run CIRCULAR checks
8. Run COVERAGE checks (only if a target ecosystem is known)

---

## Output Format

```
## Validation Report
File/UIR: <path>
Ecosystem: <target or "uir">
Timestamp: <ISO 8601>

### Errors (N)
[STR-001] <file>:<line> — <message>
  Fix: <suggested action>

### Warnings (N)
[CON-002] <file> — <message>
  Fix: <suggested action>

### Info (N)
[COV-006] uir.json — No skills defined. Consider running build-skill mode.

---
Summary: N errors, N warnings, N info
Status: PASS (0 errors) | FAIL (N errors)
```

If target is a directory: run per-file and aggregate all findings with file paths.

Exit with FAIL status if any ERROR findings exist. WARN and INFO do not fail.
