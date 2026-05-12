---
name: code-review
description: >
  Review changed code for bugs, style violations, security issues, and performance
  problems. Use when asked to review a PR, diff, or specific files. Produces
  inline-style comments with severity ratings and a prioritized summary.
  Triggers: "review this", "review the changes", "code review", "review PR",
  "check for issues", "review my code".
---

## Purpose

Systematically analyze code changes (diffs, PRs, or file contents) and produce
structured feedback categorized by severity. Outputs actionable, inline-style
comments and a prioritized summary. Does not apply fixes — only identifies issues
and explains how to resolve them.

## Activation Criteria

- User asks to review code, a diff, a PR, or specific files
- User says "check for issues", "what's wrong with this", "is this correct"
- User mentions "PR review", "code review", "review before merge"
- User pastes code and asks for feedback

## Steps

1. **Gather scope**: Identify what to review — a git diff (`git diff HEAD`), specific files,
   or inline code. If not specified, ask: "Should I review the current diff, specific files,
   or code you'll paste?"

2. **First pass — bugs and correctness**:
   - Null/undefined/nil dereferences
   - Off-by-one errors in loops and array accesses
   - Race conditions and concurrency issues
   - Incorrect boolean logic or comparison operators
   - Missing error handling or unchecked return values
   - Type mismatches or unsafe casts

3. **Second pass — security**:
   - SQL injection, XSS, command injection attack surfaces
   - Hardcoded secrets, API keys, or passwords
   - Insecure deserialization
   - Missing input validation at system boundaries
   - Overly permissive access control

4. **Third pass — code style and conventions**:
   - Naming conventions (per project conventions from CLAUDE.md if available)
   - Function/method length and single-responsibility
   - Code duplication that should be extracted
   - Missing or incorrect documentation/comments
   - Inconsistent patterns with the rest of the codebase

5. **Fourth pass — performance**:
   - N+1 queries or unnecessary repeated calls
   - Inefficient algorithms for the data size
   - Missing indexes, caching opportunities
   - Memory leaks or large allocations in hot paths

6. **Format findings** as inline-style comments:
   ```
   <file>:<line> [SEVERITY] <issue>
   Why: <explanation>
   Fix: <suggested change>
   ```
   Severity levels: `CRITICAL` (bug/security), `MAJOR` (logic/design), `MINOR` (style/readability), `NIT` (optional polish)

7. **Produce summary**:
   ```
   ## Review Summary
   Critical: N | Major: N | Minor: N | Nits: N
   
   ### Must Fix Before Merge
   - <top critical/major items>
   
   ### Nice to Have
   - <minor items>
   
   ### Good Practices Noted
   - <things done well — always include at least one>
   ```

## Output Format

Inline-style comment list followed by the Review Summary section. Always include
at least one positive observation. Keep each comment self-contained.

## Scope

All file types, all languages. Adapt terminology to the detected language/framework.

## Constraints

- Do not apply fixes — report only, never modify files in this skill
- Do not rewrite code snippets as "alternatives" unless a fix is genuinely unclear
- Do not flag issues already fixed in later parts of the diff
- Limit to the code provided; do not speculate about code not shown
- Do not flag subjective style preferences as MAJOR or CRITICAL

## Edge Cases

- **Empty diff**: Report "No changes to review."
- **Minified/generated code**: Note it appears to be generated; skip style/naming feedback
- **Test files only**: Skip security checks; focus on coverage gaps and assertion correctness
- **Very large diff (>500 lines)**: Prioritize — focus on CRITICAL and MAJOR only; note you are
  doing a partial review and recommend splitting the PR

## Cross-Ecosystem Notes

- **Cursor**: Activate with `@50-skill-code-review` in a prompt while viewing a file
- **Aider**: `/add CONVENTIONS.md`, then ask: "Follow the Code Review skill from CONVENTIONS.md and review this file"
- **Codex**: Reference the "Task: Code Review" section in AGENTS.md in your prompt
