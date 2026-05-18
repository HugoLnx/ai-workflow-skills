---
name: docs
description: >
  Generate or update documentation: function docstrings, JSDoc, README sections,
  API docs, or inline comments. Detects the project's documentation style and
  follows it. Triggers: "document this", "generate docs", "write docstrings",
  "update README", "add JSDoc", "document the API", "missing documentation".
---

## Purpose

Generate accurate, useful documentation for code. Extracts function signatures,
parameters, return types, side effects, and examples to produce documentation
in the project's preferred format. Does not invent behavior — documents what
the code actually does.

## Activation Criteria

- User asks to document code, add docstrings, write JSDoc, or update README
- User says "missing documentation", "undocumented", "add comments"
- User wants to document an API, module, or function
- User asks to generate API reference docs

## Steps

1. **Identify documentation target and format**:
   - What to document: function, class, module, API endpoint, or README section
   - What format: detect from existing code
     - TypeScript/JavaScript: JSDoc (`/** */`) or TSDoc
     - Python: Google-style, NumPy-style, or reStructuredText docstrings
     - Go: package comments and function comments (`// FuncName does X`)
     - Rust: `///` doc comments with Markdown
     - C#: XML doc comments (`/// <summary>`)
   - If no existing style is found: ask or default to the most common for the language

2. **Read and understand the target**:
   - Read the full implementation before writing docs
   - Do not document based on function names alone — verify actual behavior
   - Note any discrepancies between the name and implementation

3. **For each function/method/class, document**:
   - **Purpose**: what it does (one sentence, active voice)
   - **Parameters**: name, type, description, whether optional, valid range/format
   - **Return value**: type and meaning; what it returns when there's nothing to return
   - **Throws/errors**: under what conditions, what type
   - **Side effects**: mutations, I/O, state changes that callers should know about
   - **Examples**: at least one usage example for public API functions

4. **For README sections, include**:
   - **Installation**: exact commands for the detected package manager
   - **Quick start**: minimal working example
   - **Configuration**: all options with types, defaults, descriptions
   - **API reference** (link to generated docs if separate)
   - **Contributing**: how to set up dev environment, run tests

5. **Write documentation**:
   - Accurate: reflects actual behavior
   - Concise: no filler phrases ("this function is used to...")
   - In the right format for the language/framework
   - Include `@param`, `@returns`, `@throws` tags as appropriate for the format

6. **Check for missing docs**:
   - List all public functions/methods in the target file
   - Flag any that still have no documentation

## Output Format

The documentation inserted inline in the source file (as a diff), or a complete
README section as standalone markdown. Include a list of what was documented.

## Scope

All languages. Adapt doc format to the detected language and existing style.

## Constraints

- Do not document private/internal functions unless asked
- Do not add comments explaining what code does line-by-line — document WHY and WHAT, not HOW
- Do not add documentation that will go stale immediately (references to "current sprint", etc.)
- Do not invent parameter descriptions — read the implementation to understand intent
- Keep examples simple and runnable

## Edge Cases

- **Undocumentable code** (spaghetti, unclear purpose): Note the unclear behavior in a
  comment and recommend a refactoring first
- **Generated code**: Do not add docstrings to generated files — document the generator's
  output schema instead
- **Complex algorithm**: Explain the algorithm at the function level; link to the original
  paper/source if applicable

## Cross-Ecosystem Notes

- **Cursor**: Activate with `@50-skill-docs` while the file to document is open
- **Aider**: `/add <target-file>`, reference the Documentation section in CONVENTIONS.md
- **Codex**: Reference "Task: Documentation" in your prompt with the target file
