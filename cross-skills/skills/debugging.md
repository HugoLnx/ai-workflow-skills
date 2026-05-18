---
name: debugging
description: >
  Systematic bug investigation workflow: reproduce, isolate, hypothesize, test,
  fix, and verify. Guides structured debugging rather than random changes.
  Triggers: "debug this", "investigate this error", "find the bug", "why is this
  failing", "help me debug", "something is broken", "unexpected behavior".
---

## Purpose

Guide a systematic debugging investigation from a symptom (error message, wrong
output, crash) to a confirmed root cause and a minimal targeted fix. Prevents
random trial-and-error by requiring a hypothesis-testing loop.

## Activation Criteria

- User reports an error, exception, or unexpected behavior
- User says "this isn't working", "something is broken", "help me debug"
- User pastes an error message, stack trace, or failing test output
- User describes unexpected behavior with a symptom

## Steps

1. **Gather symptom information**:
   - What is the exact error/symptom? (error message, stack trace, wrong output)
   - What is the expected behavior?
   - When does it happen? (always, intermittently, only in production, specific inputs)
   - What changed recently? (last working commit, recent PRs, env changes)
   If any of this is missing, ask before proceeding.

2. **Reproduce the problem**:
   - Write the simplest possible code to trigger the symptom
   - Confirm the repro is reliable (not intermittent) before proceeding
   - If intermittent: note timing, concurrency, or environment factors

3. **Isolate the scope**:
   - Identify the smallest unit of code that exhibits the problem
   - Binary search: does the problem occur with X removed? With only Y present?
   - Check: is this a data problem (specific inputs trigger it) or a logic problem?

4. **Form hypotheses**:
   Generate 2–3 plausible root causes ranked by likelihood. For each:
   ```
   Hypothesis: <what might be wrong>
   Evidence for: <why this could explain the symptom>
   Evidence against: <why this might not be the cause>
   Test: <what to check or print to confirm/deny>
   ```

5. **Test each hypothesis** (most likely first):
   - Add temporary logging/print statements or use the debugger
   - Check the specific condition the hypothesis predicts
   - Confirm OR eliminate — do not stop at "seems likely"
   - If all hypotheses are eliminated: form new hypotheses with the new information

6. **Identify root cause**:
   State precisely: `Root cause: <exact line/function/condition causing the behavior>`

7. **Design the fix**:
   - Minimal change that addresses the root cause
   - Does not introduce new behavior or refactor surrounding code
   - If multiple fixes are possible: explain the tradeoff and recommend one

8. **Apply and verify**:
   - Apply the fix
   - Re-run the original repro — confirm the symptom is gone
   - Run the full test suite — confirm no regressions
   - If the fix introduced failures: revisit hypothesis

9. **Write a regression test** (if applicable):
   - Add a test that would have caught this bug
   - Verify the test fails without the fix and passes with it

## Output Format

A debugging narrative with numbered findings and a final:
```
Root cause: <explanation>
Fix: <change made>
Verification: <how it was confirmed>
Regression test: <test added or reason none was added>
```

## Scope

All languages and runtimes. Adapt debugging commands to the detected stack.

## Constraints

- Do not apply multiple fixes simultaneously — change one thing at a time
- Do not refactor surrounding code while debugging — stay focused on the root cause
- Do not guess without evidence — every hypothesis must be tested
- Do not abandon the hypothesis loop after only one test

## Edge Cases

- **No error message, just wrong output**: Start with the simplest input that shows
  the difference between expected and actual output
- **Intermittent/race condition**: Add logging with timestamps and thread IDs;
  look for non-deterministic ordering
- **External service failure**: Check if the issue is in the client code, the
  network layer, or the external service by testing each independently
- **Works on my machine**: Document exact environment differences (OS, version, env vars)
  and test in the failing environment
- **Stack trace points to library code**: The bug is almost always in your code's
  input to the library, not the library itself — trace back to your call site

## Cross-Ecosystem Notes

- **Cursor**: Activate with `@50-skill-debugging` when viewing the problematic file
- **Aider**: Share the error message and relevant files; reference the Debugging section
- **Codex**: Reference "Task: Debugging" section with the error message and file
