---
name: devops
description: >
  Generate CI/CD pipelines, Dockerfiles, infrastructure configs, and deployment
  scripts. Follows detected tooling and security best practices. Triggers:
  "generate pipeline", "create Dockerfile", "set up CI", "GitHub Actions",
  "containerize this", "write a deploy script", "infrastructure config".
---

## Purpose

Generate production-quality DevOps configuration files: CI/CD pipelines (GitHub Actions,
GitLab CI, CircleCI), Dockerfiles, docker-compose files, Terraform modules, and
deployment scripts. Follows the project's detected tech stack and security best practices.

## Activation Criteria

- User asks to generate or improve CI/CD pipelines
- User asks to containerize the application (Dockerfile, docker-compose)
- User wants to set up automated testing, linting, or deployment
- User asks about infrastructure configuration (Terraform, Pulumi, Kubernetes)
- User asks for deployment scripts or automation

## Steps

1. **Identify target and existing tooling**:
   - CI system: check for `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/`
   - Container: check for existing `Dockerfile`, `docker-compose.yml`
   - Runtime: detect from package manifests
   - Build commands: use from `package.json` scripts, Makefile, or similar
   - If ambiguous: ask which CI system to target

2. **For CI/CD pipelines** (GitHub Actions example flow):
   - Detect trigger events: push to main, PRs, tags for releases
   - Install step: use detected package manager (`npm ci`, `pip install -r requirements.txt`, etc.)
   - Cache step: cache dependencies by lockfile hash
   - Lint step: use detected linter command
   - Test step: use detected test command with coverage if available
   - Build step: use detected build command
   - Artifact upload: for built binaries or Docker images
   - Deploy step (if requested): environment-gated, with secrets via env vars only

3. **For Dockerfiles**:
   - Use official base images pinned to a specific version (not `latest`)
   - Multi-stage build: separate builder and runtime stages
   - Runtime stage: use minimal base (alpine or distroless)
   - Run as non-root user
   - Copy only what's needed (use `.dockerignore`)
   - Set `WORKDIR`, `EXPOSE`, `ENV`, `CMD`/`ENTRYPOINT` appropriately
   - Layer ordering: dependencies before source code (maximizes cache hits)

4. **For docker-compose**:
   - Service per component (app, database, cache, etc.)
   - Named volumes for persistent data
   - Health checks for services with dependencies
   - Environment variables via `.env` file (never hardcode secrets)
   - Networks: isolate services that don't need to communicate

5. **For Terraform**:
   - Provider and version pinning in `required_providers`
   - Remote state backend configuration
   - Variables with types, descriptions, and defaults
   - Outputs for values needed by other modules
   - Separate files: `main.tf`, `variables.tf`, `outputs.tf`, `versions.tf`
   - Tag all resources with at minimum: `project`, `environment`, `managed-by=terraform`

6. **Security review of generated config**:
   - No hardcoded secrets or tokens
   - Secrets injected via environment variables or secret management
   - Minimal permissions (least privilege for IAM roles, service accounts)
   - Pinned versions to prevent supply chain attacks
   - Dependencies cached but also verified (lockfiles)

## Output Format

Complete, production-ready configuration files with inline comments explaining
non-obvious choices. For multi-file outputs, include a manifest of files and
their purpose.

## Scope

All common CI systems, container tools, and IaC tools. Ask if the target is ambiguous.

## Constraints

- Never hardcode credentials, tokens, or secrets in generated config
- Always pin versions — never use `latest` tags in production configs
- Do not generate configs for technologies not detected in the project without asking
- Follow security best practices: non-root containers, minimal permissions, etc.

## Edge Cases

- **Monorepo**: Generate matrix builds or per-package workflows as appropriate
- **Multiple deployment environments**: Use environment variables and conditional logic;
  create separate workflow files for staging vs. production if needed
- **Legacy build system** (Makefile, Ant): Wrap with CI commands rather than reimplementing
- **Private registries**: Leave registry URLs as `{{REGISTRY_URL}}` placeholders

## Cross-Ecosystem Notes

- **Cursor**: Activate with `@50-skill-devops` for in-context DevOps config generation
- **Aider**: Reference the DevOps section in CONVENTIONS.md with the target config type
- **Codex**: Reference "Task: DevOps Configuration" in AGENTS.md
