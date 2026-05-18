# Module: Analyzer

**Invoked by**: `skill.md` when mode is `analyze`

**Purpose**: Survey a repository and produce a `uir.json` file that captures all
AI-relevant conventions, tech stack, rules, and context — ready for the generator
to consume.

---

## Inputs

- **Repo path**: A directory path provided by the user (absolute or relative to CWD).
- **Output path** (optional): Where to write `uir.json`. Default: `<repo-path>/uir.json`.
- **Depth** (optional): `quick` (structure only), `standard` (default), `deep` (includes
  all convention files, existing agent configs).

---

## Phase 1 — Structural Survey

Read the following files and directories to understand the project shape.
**Always read all that exist; skip silently if absent.**

### Package Manifests (tech stack detection)
- `package.json` → languages: JavaScript/TypeScript; extract `scripts`, `dependencies`, `devDependencies`
- `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` → package manager
- `pyproject.toml` / `setup.py` / `setup.cfg` / `requirements.txt` → Python
- `Cargo.toml` → Rust
- `go.mod` → Go
- `pom.xml` / `build.gradle` / `build.gradle.kts` → Java/Kotlin
- `*.csproj` / `*.sln` → C# / .NET
- `Gemfile` → Ruby
- `composer.json` → PHP
- `pubspec.yaml` → Dart/Flutter
- `mix.exs` → Elixir

### Config Files (tooling detection)
- `.eslintrc*` / `eslint.config.*` → ESLint (JS/TS linter)
- `.prettierrc*` / `prettier.config.*` → Prettier (formatter)
- `biome.json` → Biome (linter+formatter)
- `tsconfig.json` / `tsconfig.*.json` → TypeScript config (strict mode, paths, target)
- `jest.config.*` / `vitest.config.*` → Test framework
- `playwright.config.*` / `cypress.config.*` → E2E test framework
- `.mocharc*` → Mocha
- `pytest.ini` / `pyproject.toml [tool.pytest]` → pytest
- `mypy.ini` / `pyproject.toml [tool.mypy]` → mypy
- `ruff.toml` / `pyproject.toml [tool.ruff]` → Ruff (Python linter)
- `Dockerfile` / `docker-compose.yml` → Docker
- `*.tf` / `*.tfvars` → Terraform
- `*.yaml` in `.github/workflows/` → GitHub Actions CI
- `.gitlab-ci.yml` → GitLab CI
- `Jenkinsfile` → Jenkins
- `.circleci/config.yml` → CircleCI
- `turbo.json` → Turborepo
- `nx.json` → Nx
- `.nvmrc` / `.node-version` / `.python-version` → runtime version pinning

### Directory Layout Survey
List top-level directories and identify their purpose:
- `src/` or `app/` → application source
- `lib/` or `packages/` → libraries or monorepo packages
- `tests/` or `__tests__/` or `spec/` → test suite
- `docs/` → documentation
- `infra/` or `terraform/` or `pulumi/` → infrastructure
- `scripts/` → utility scripts
- `public/` or `static/` or `assets/` → static files
- `migrations/` or `db/` → database
- `.github/` → GitHub config and CI

### Monorepo Detection
If `turbo.json`, `nx.json`, `pnpm-workspace.yaml`, or `packages/` with multiple
`package.json` files exist: set `context.monorepo`. List each workspace path.

---

## Phase 2 — Convention Extraction

Read these files deeply to extract coding conventions and rules.

### Existing Documentation
- `README.md` — extract: project summary, setup instructions, contributing guidelines
- `CONTRIBUTING.md` — extract: PR workflow, branch naming, commit message format
- `ARCHITECTURE.md` / `docs/architecture.md` / `docs/ARCHITECTURE.md` — extract: architectural decisions
- `CHANGELOG.md` — extract: versioning scheme (semver, calver, etc.)

### Code Convention Files
- `.editorconfig` → indentation, line endings, charset
- `.gitignore` / `.gitignore_global` → ignore patterns
- Any `*.md` in `docs/` matching `conventions*`, `style*`, `guide*`

### Existing Agent Configs (extract rules from them)
- `CLAUDE.md` → parse sections as global rules; parse `@import` references
- `AGENTS.md` → parse agent definitions; extract instructions as agent records
- `.cursor/rules/*.mdc` → parse each file: frontmatter (alwaysApply, globs) + body as rules
- `.aider.conf.yml` → parse model, read files, commit prompt
- `CONVENTIONS.md` → treat each `##` section as a rule category

---

## Phase 3 — Framework/Stack-Specific Rule Inference

Based on detected tech stack, infer standard conventions. Only add inferred rules
if no explicit rule covers the same ground (avoid duplication).

| Stack | Inferred rules to check for |
|---|---|
| React | Component file naming (PascalCase), hooks prefix (use*), props interface naming |
| Next.js | Route file conventions (page.tsx, layout.tsx), server vs client component rules |
| TypeScript | Strict mode enforcement, no-any preference, interface vs type preference |
| Python | PEP 8 compliance, type hint usage, docstring format (Google/NumPy/reStructuredText) |
| Go | gofmt compliance, error handling pattern (check immediately, no panic in libraries) |
| Rust | clippy compliance, unsafe block documentation |
| Unity/C# | MonoBehaviour naming, coroutine vs async patterns, ScriptableObject usage |
| Docker | Multi-stage builds, non-root user, .dockerignore coverage |
| GitHub Actions | Secret handling, matrix strategy, artifact retention |
| Terraform | Module structure, state backend, naming conventions |

For each inferred rule:
- Set `scope: "global"` or narrower if appropriate
- Set `category` based on content
- Set `priority: 5` (standard convention)
- Set `rationale: "Inferred from detected stack: <stack-name>"`
- Tag with `["inferred"]`

---

## Phase 4 — UIR Assembly

Construct the UIR object following `schema/uir.schema.json`:

```
meta:
  id: <generate UUID v4>
  name: <repo directory name>
  version: "1.0.0"
  generated_at: <current ISO 8601 timestamp>
  source:
    method: "analyze"
    from_ecosystem: null
    repo_path: <absolute path>

context:
  project_summary: <synthesized from README + package.json description>
  tech_stack: <from Phase 1 detection, ordered by importance>
  directory_layout: <top-level dirs mapped to purpose>
  entry_points: <main files/commands>
  build_commands: <from package.json scripts or Makefile targets>
  environment_variables: <from .env.example, README env section, or docker-compose env>
  monorepo: <null or populated object>

rules: <all extracted + inferred rules, deduplicated by content>

permissions:
  allow: []   # Cannot be auto-detected; leave empty for manual population
  deny: []    # Cannot be auto-detected; leave empty for manual population
  ask_on: []

memory:
  always_load: <CLAUDE.md @imports, key architecture docs>
  on_demand: []
  ignore: <from .gitignore patterns worth forwarding to AI>

hooks: []   # Cannot be auto-detected; leave empty for manual population

skills: []  # Leave empty; use build-skill mode to add skills

agents: <from AGENTS.md if present, else []>

ignore_patterns: <from .gitignore, .aiderignore, .cursorignore>

extensions: {}
```

### Rule Deduplication
Before finalizing `rules[]`:
1. Remove exact duplicates (same `content` after trim)
2. Merge rules with same `id` — keep the one with more fields populated
3. Flag potential conflicts: two rules with same scope + scope_value + contradictory content → add `tags: ["conflict-candidate"]` to both

---

## Phase 5 — Gap Report

After assembling the UIR, produce a gap report in this format:

```
## UIR Gap Report for <repo-name>

### Populated fields
- context.project_summary ✓
- context.tech_stack: <N> entries ✓
- rules: <N> rules extracted ✓
...

### Empty fields requiring manual population
- permissions.allow — could not auto-detect tool permissions
- permissions.deny — could not auto-detect tool restrictions
- hooks — lifecycle hooks are project-specific
- skills — use build-skill mode to add reusable skills

### Low-confidence fields
- <field>: <reason for low confidence>

### Conflicts detected
- rules[<id1>] vs rules[<id2>]: <description>

### Recommendations
- Run `validate` mode on the generated uir.json before generating configs
- Review inferred rules (tagged "inferred") for accuracy
- Add permissions manually if this project has security-sensitive tooling
```

---

## Output

Write the assembled UIR to the output path as valid JSON (pretty-printed, 2-space indent).

Print the gap report to the conversation.

Confirm: `UIR written to <path>. Run cross-skills in generate mode to produce ecosystem configs.`
