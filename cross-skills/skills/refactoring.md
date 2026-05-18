---
name: refactoring
description: >
  Safe, incremental structural improvement of code without changing external behavior.
  Identifies code smells, plans changes, verifies no behavior change, and applies
  improvements incrementally. Triggers: "refactor this", "clean up this code",
  "improve this", "restructure", "remove duplication", "simplify".
---

## Purpose

Apply targeted structural improvements to code while guaranteeing the external
behavior remains unchanged. Uses incremental steps with verification at each stage
to prevent introducing bugs during cleanup.

## Activation Criteria

- User asks to refactor, clean up, simplify, or restructure code
- User points to specific code smells (long functions, duplication, deep nesting)
- User says "this is hard to read/understand/maintain"
- User wants to improve testability of existing code

## Steps

1. **Understand the target**:
   - Read the code to refactor completely before suggesting changes
   - Understand what it does — do not refactor code you haven't fully understood
   - Identify all callers/consumers that must not be affected

2. **Assess test coverage**:
   - Check if existing tests cover the code being refactored
   - If no tests exist: write a characterization test (a test that documents current
     behavior, even if behavior is imperfect) BEFORE refactoring
   - Never refactor code with zero test coverage without first establishing a baseline

3. **Identify code smells** (list them before fixing any):
   - Long function/method (>20-30 lines): extract sub-functions
   - Deep nesting (>3 levels): early return / guard clauses / extract function
   - Duplicate code (2+ identical or near-identical blocks): extract common function
   - Large class/module: split by responsibility
   - Long parameter list (>3-4 params): introduce a params object
   - Primitive obsession: replace primitives with value objects
   - Feature envy: code that uses another module's data more than its own
   - Dead code: unused variables, functions, imports
   - Misleading names: rename to reflect actual behavior

4. **Plan the refactoring** (before applying any changes):
   - List each change as a separate step
   - Order steps so each can be committed independently
   - Identify which steps might affect callers (interface changes) vs. which are
     purely internal (safe to do without coordination)

5. **Apply changes incrementally**:
   - One logical change at a time
   - After each step: run tests to verify behavior is unchanged
   - If tests fail after a refactoring step: undo and rethink (behavior change = bug)

6. **Verify equivalence**:
   - Run full test suite after all changes
   - Check that callers/consumers still work as expected
   - If the code has no tests: describe what manual verification was done

7. **Clean up**:
   - Remove the characterization tests added in step 2 if they were only scaffolding
     (or keep them — they might be valuable permanent tests)
   - Update inline comments if they described the old structure

## Output Format

A diff of the refactored code. For each logical change, briefly explain:
`Step N: <what changed> — <why this improves the code>`

## Scope

Any language. Adapt naming conventions and refactoring patterns to the detected language.

## Constraints

- Do not change external behavior — if in doubt, do not refactor that part
- Do not add features while refactoring — separate concerns
- Do not refactor code that is about to be deleted or replaced
- Do not apply all changes in one massive commit — incremental is safer
- Do not rename public APIs without checking all callers first

## Edge Cases

- **No tests**: Write characterization tests first; offer to do this as a preliminary step
- **Performance-critical hot path**: Note that refactoring may affect performance;
  benchmark before and after if the function is in a hot path
- **Generated code**: Do not refactor generated code — fix the generator instead
- **Third-party code**: Do not refactor vendored or copy-pasted third-party code;
  upgrade the dependency instead

## Cross-Ecosystem Notes

- **Cursor**: Activate with `@50-skill-refactoring` while the target file is open
- **Aider**: `/add <target-file> <test-file>`, reference the Refactoring section
- **Codex**: Reference "Task: Refactoring" in AGENTS.md with the target file
