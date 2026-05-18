# Mode: analyze

**Triggers**: "analyze codebase", "survey conventions", "what conventions does this project use", "extract conventions", "codebase analysis"

**Goal**: understand the project's coding conventions well enough to inform skill authoring.

---

## Steps

1. **Scan key files** — read as many of the following as exist:
   - `CLAUDE.md`, `AGENTS.md`, `README.md`
   - `package.json`, `pyproject.toml`, `Gemfile`, `go.mod`, `Cargo.toml`
   - `.editorconfig`, `.eslintrc*`, `.prettierrc*`, `rubocop.yml`, `pyproject.toml` (tool sections)
   - Existing `.ai/skills/` contents (what skills are already defined?)
   - CI config files (`.github/workflows/*.yml`, `.circleci/config.yml`)

2. **Identify conventions** across these dimensions:
   - Language and framework stack
   - Testing approach (framework, file location pattern, style — unit vs integration)
   - Code style (linter, formatter, key enforced rules)
   - Naming conventions (files, variables, functions, modules)
   - PR and commit conventions (conventional commits? squash policy? PR template?)
   - Any documented rules already in agent configs

3. **Output a structured notes block**:

```
## Codebase Analysis

- Stack         : [languages, frameworks, notable libraries]
- Testing       : [framework, test file pattern, approach]
- Style         : [linter/formatter and key rules]
- Naming        : [file naming convention, variable naming patterns]
- Commits/PRs   : [commit style, PR template presence]
- Existing skills: [list names if .ai/skills/ has any, else "none"]
- Observations  : [anything non-obvious that should be encoded in a skill]

## Recommended skills to author
- [skill-name]: [one-line rationale]
- [skill-name]: [one-line rationale]
```

4. **Follow up**: ask the user which conventions to encode, then offer to invoke `generate` or `build-skill` mode for the chosen skill.
