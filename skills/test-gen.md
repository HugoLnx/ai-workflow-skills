---
name: test-gen
description: >
  Generate tests for untested or under-tested code. Covers unit tests, integration
  tests, and edge cases. Detects the project's test framework and follows its
  conventions. Triggers: "generate tests", "write tests for", "add test coverage",
  "test this function", "missing tests", "increase coverage".
---

## Purpose

Analyze a function, module, or class and generate a comprehensive test suite covering
happy paths, edge cases, error conditions, and boundary values. Detects and follows
the project's existing test framework and file naming conventions.

## Activation Criteria

- User asks to generate, write, or add tests for specific code
- User mentions "test coverage", "missing tests", "untested"
- User says "test this function/class/module"
- User asks to verify behavior through tests

## Steps

1. **Identify target**: What needs tests? A function, class, module, or file.
   If not specified, ask or use the currently open/changed file.

2. **Detect test framework** (in priority order):
   - Check existing test files in the repo for import patterns
   - Check `package.json` devDependencies (jest, vitest, mocha, jasmine, tape)
   - Check `pyproject.toml` / `pytest.ini` for pytest
   - Check `Cargo.toml` for Rust built-in tests
   - Check for Go `_test.go` files
   - Fallback: ask the user

3. **Detect test file conventions**:
   - File location: colocated (`foo.test.ts`) vs separate directory (`tests/`)
   - Naming pattern: `*.test.*`, `*.spec.*`, `*_test.*`, `test_*.py`
   - Import style used in existing tests

4. **Analyze target code**:
   - List all public functions/methods/endpoints
   - Identify parameters, return types, and their valid/invalid ranges
   - Identify side effects (DB writes, HTTP calls, file I/O, state mutations)
   - Identify thrown/returned errors and when they occur
   - Identify external dependencies that need mocking

5. **Plan test cases** (enumerate before writing):
   ```
   Function: <name>
   Happy paths:
   - [normal input] → expected output
   Edge cases:
   - [empty/null/zero input] → expected behavior
   - [boundary values] → expected behavior
   Error cases:
   - [invalid input] → expected error/exception
   - [external failure] → expected fallback
   ```

6. **Generate tests**:
   - One `describe`/`test class` block per function or concern
   - Each test: arrange → act → assert pattern
   - Mock external dependencies (HTTP, DB, file system) using the project's mock library
   - Use meaningful test names: `"returns empty array when no items match filter"`
   - Avoid testing implementation details; test behavior and contracts

7. **Write to correct file**:
   - Follow detected naming convention for test file name
   - Place in the detected location (colocated or test directory)
   - Add necessary imports

## Output Format

A complete, runnable test file. Not a snippet — a full file with imports,
describe blocks, and all test cases. Include a comment at the top noting
what the tests cover and any manual setup required.

## Scope

All languages and test frameworks. Adapt syntax to detected framework.

## Constraints

- Do not modify the source file being tested
- Do not use `any` types or skip TypeScript types in generated tests
- Do not generate tests that pass trivially (e.g. `expect(true).toBe(true)`)
- Do not mock the module under test itself — only its dependencies
- Do not generate tests for private/internal functions unless specifically asked
- Keep tests independent: no shared mutable state between test cases

## Edge Cases

- **No existing test framework detected**: Ask the user which framework to use;
  default to jest for Node.js, pytest for Python, built-in for Go/Rust
- **Complex integration dependencies**: Generate unit tests with mocks + note that
  integration tests would require a running <service>
- **Async code**: Use appropriate async patterns (`async/await`, pytest-asyncio,
  tokio::test, etc.) — never mix sync and async test utilities
- **Very large target file (>300 lines)**: Ask which functions to prioritize

## Cross-Ecosystem Notes

- **Cursor**: Activate with `@50-skill-test-gen` while the source file is open
- **Aider**: `/add <source-file> CONVENTIONS.md`, then ask to write tests
- **Codex**: Reference "Task: Test Generation" in your prompt with the target file
