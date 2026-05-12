---
name: onboarding
description: >
  Guide new developers through a codebase: explain architecture, key files, setup
  steps, and development workflows. Generates an onboarding document or answers
  "how does this work" questions. Triggers: "onboard me", "explain the codebase",
  "new to this project", "how does this project work", "give me a tour",
  "developer guide", "getting started".
---

## Purpose

Help new developers get productive quickly by explaining the codebase structure,
setting up the development environment, and explaining key workflows. Can generate
a permanent onboarding document or answer one-off "how does X work" questions.

## Activation Criteria

- User asks to be onboarded or given a codebase tour
- User says "I'm new to this project" or "help me get started"
- User asks "how does this project work", "what does X do", "explain the architecture"
- User asks how to set up the development environment

## Steps

1. **Determine the onboarding goal**:
   - Full onboarding document → proceed through all steps below
   - Quick orientation → steps 2-4 only
   - Specific "how does X work" question → focus on the relevant subsystem

2. **Project overview** (read from README, package.json, existing docs):
   - What does this project do? Who uses it?
   - What is the tech stack at a high level?
   - What is the deployment model (cloud service, desktop app, library, CLI, etc.)?

3. **Development environment setup**:
   - Prerequisites: runtime versions, required global tools
   - Clone and install: exact commands (copy-paste ready)
   - Environment configuration: which env vars are required, where to get them
   - First run: how to start the development server / run the app
   - Verify it works: what to check to confirm setup succeeded
   - Common setup issues: known gotchas (OS-specific steps, permission issues, etc.)

4. **Codebase tour**:
   - Top-level directory map with plain-English purpose for each
   - Entry points: where execution starts (main file, router, app bootstrap)
   - Key abstractions: the 3-5 most important concepts/types to understand
   - Data flow: how a typical request or user action flows through the system
   - Configuration: where and how the app is configured (env vars, config files, feature flags)

5. **Development workflow**:
   - Branch strategy: naming convention, when to create branches
   - Commit message format (if enforced)
   - PR/MR process: draft vs. ready, who to assign, what reviewers look for
   - How to run tests: unit, integration, E2E
   - How to lint and format: commands to run before committing
   - How to add a new feature: step-by-step from branch → merge

6. **Common tasks** (with exact commands):
   - Run the development server
   - Run the test suite
   - Add a new dependency
   - Generate a database migration
   - Build for production
   - Deploy (or how to trigger deployment)

7. **Architecture summary**:
   - Pattern used (MVC, hexagonal, feature-based, etc.)
   - Key design decisions and why they were made (link to ADRs if available)
   - What not to do (common mistakes new devs make in this codebase)

8. **Contacts and resources**:
   - Where to ask questions (Slack channel, GitHub Discussions, etc.)
   - Key documentation links
   - Who owns which parts of the codebase (if available in CODEOWNERS)

## Output Format

If generating a document: write to `docs/ONBOARDING.md` or `ONBOARDING.md`.
If answering a question: structured response with sections as needed.

## Scope

The entire repository. Read broadly — this skill is about understanding, not deep implementation.

## Constraints

- Use exact, copy-paste-ready commands
- Do not describe how things "should" work — describe how they actually work
- Do not assume the reader knows the framework — explain relevant concepts briefly
- Keep the document maintainable: avoid embedding information that changes frequently

## Edge Cases

- **Large monorepo**: Start with the workspace-level overview, then offer package-level
  tours for each sub-package on request
- **No README or documentation**: Note the absence; generate a starter README as part of onboarding
- **Complex build system**: Provide more detail on the build steps; note non-obvious requirements

## Cross-Ecosystem Notes

- **Cursor**: Activate with `@50-skill-onboarding` at the start of a session in a new repo
- **Aider**: Reference the Onboarding section in CONVENTIONS.md in your first message
- **Codex**: Reference "Task: Onboarding" in AGENTS.md when starting work on a new codebase
