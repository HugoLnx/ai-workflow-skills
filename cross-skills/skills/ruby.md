---
name: ruby
description: >
  Idiomatic Ruby development assistance focused on Clean Code, SOLID, DRY, and
  The Ruby Way. Covers naming conventions (snake_case methods/vars, predicate
  methods ending in `?`, bang methods ending in `!`), block/proc/lambda usage,
  Enumerable idioms, module mixins, composition over inheritance, and the
  standard toolset (Bundler, RSpec, RuboCop, rake, IRB/Pry, OptionParser/Thor
  for CLIs). Rails-agnostic — applies to plain Ruby gems, libraries, scripts,
  and command-line tools. Triggers: "ruby", ".rb", "gem", "Gemfile", "RSpec",
  "rake task", "module", "mixin", "block", "duck typing", "ruby cli",
  "refactor ruby", "ruby style", "rubocop", "the ruby way".
---

## Purpose

Provide Ruby-specialized AI assistance for writing, reviewing, and refactoring
idiomatic Ruby code in non-Rails contexts (gems, libraries, scripts, CLIs,
service objects, plain OOP applications). The skill applies Clean Code and SOLID
principles through a Ruby-native lens: prefers expressive method names, small
focused objects, modules for shared behavior, Enumerable for collection
processing, and the community style guide for surface conventions. Toolset
guidance is grounded in Bundler, RSpec/Minitest, RuboCop, rake, and the
OptionParser/Thor CLI ecosystem.

This skill is explicitly Rails-agnostic. It does not invoke ActiveRecord,
ActionController, ActiveSupport conveniences, or Rails generators. If the
codebase is a Rails application, prefer a Rails-specific skill for framework
concerns and use this skill only for the underlying Ruby code.

## Activation Criteria

Use this skill when:

- The user is writing, reviewing, or refactoring `.rb` files in a non-Rails project.
- The user mentions Ruby, a gem, `Gemfile`, `Rakefile`, `.gemspec`, RSpec,
  Minitest, RuboCop, or `bundle exec`.
- The user asks about idiomatic Ruby patterns: blocks, procs, lambdas, modules,
  mixins, duck typing, method missing, refinements, or `Enumerable`.
- The user asks about Ruby naming, formatting, or "the Ruby Way".
- The user is building a Ruby command-line tool, library, or background worker
  outside a web framework.
- The user mentions style enforcement (RuboCop, Standard) or code review of Ruby.

Do NOT use this skill (or use sparingly) when:

- The task is framework-specific (Rails controllers/models, Sinatra routes,
  Hanami actions). Prefer a framework-specific skill.
- The task is purely DevOps/infra with no Ruby code authoring.

## Steps

1. **Detect Ruby project shape and toolchain**:
   - Check for `Gemfile`, `Gemfile.lock`, `*.gemspec`, `Rakefile`, `bin/`, `lib/`,
     `spec/`, `test/`, `.ruby-version`, `.tool-versions`, `.rubocop.yml`.
   - Read `Gemfile` and `.gemspec` to identify Ruby version, runtime gems,
     development gems, and stated style guide (RuboCop, Standard, custom).
   - Confirm this is NOT a Rails project (no `config/application.rb`, no
     `rails` gem). If Rails is present, narrow scope to plain Ruby concerns.
   - Note the test framework (RSpec if `spec/spec_helper.rb`; Minitest if
     `test/test_helper.rb`) so generated tests match.

2. **Apply Ruby naming conventions (The Ruby Way)**:
   - `snake_case` for methods, local variables, instance variables, file names.
   - `CamelCase` (PascalCase) for classes and modules.
   - `SCREAMING_SNAKE_CASE` for constants.
   - Predicate methods that return a boolean end in `?`: `empty?`, `valid?`,
     `active?`. Never name them `is_empty` or `get_active`.
   - "Dangerous" or in-place mutating methods end in `!`: `sort!`, `compact!`.
     Only pair a `!` method with a non-bang counterpart when both make sense;
     do not add `!` just to signal "important".
   - Setter-like methods that pair with a reader use `name=`: `def name=(value)`.
   - Avoid Java/JS/Python conventions: no `getFoo`/`setFoo`, no `camelCase`
     methods, no `IFoo` interface prefixes, no `_private` underscore prefix
     (use `private` keyword instead).
   - File name matches the primary constant defined: `class FooBar` lives in
     `foo_bar.rb`; one top-level class or module per file.
   - Use 2-space indentation, no tabs, no trailing whitespace, newline at EOF.

3. **Write idiomatic Ruby (Clean Code through a Ruby lens)**:
   - **Keep methods small.** Aim for under ~10 lines and a single level of
     abstraction. Extract private methods rather than nesting conditionals.
   - **Use guard clauses and early returns** instead of deep `if`/`else` nesting:
     `return nil if user.nil?` rather than wrapping the body in `if user`.
   - **Prefer `unless` for negative single-condition guards**, but never
     `unless ... else` (rewrite as `if`). Prefer `until` over `while !`.
   - **Use the ternary operator for short, simple expressions**, never nested.
     Use `if`/`else` when either branch is non-trivial.
   - **Expression-oriented**: methods return their last expression. Avoid
     explicit `return` unless using it for an early exit / guard clause.
   - **String interpolation** (`"Hello, #{name}"`) over concatenation
     (`"Hello, " + name`). Single-quoted strings when no interpolation is needed.
   - **Symbols** (`:active`) for fixed identifiers, hash keys, and method names.
     Strings for human-facing or mutable text.
   - **Hash shorthand**: prefer `{ name: "Ada" }` over `{ :name => "Ada" }`.
   - **Block delimiters**: `do...end` for multi-line blocks; `{ ... }` for
     single-line blocks. Never chain off a `do...end` block.
   - **Use `&:symbol` shorthand** when passing a single method as a block:
     `names.map(&:upcase)` not `names.map { |n| n.upcase }`.
   - **Default assignment** with `||=`: `@cache ||= build_cache`.
   - **Safe navigation** (`&.`) when a nil receiver is expected:
     `user&.address&.city`. Do not use `&.` to mask bugs.
   - **Frozen string literal** magic comment at the top of every source file:
     `# frozen_string_literal: true`.
   - **Avoid `for ... in`**; use `each`, `map`, `select`, `reduce`. `for`
     leaks the loop variable and is non-idiomatic.
   - **No semicolons**; one statement per line.

4. **Apply SOLID and design principles in Ruby form**:
   - **Single Responsibility**: one reason to change per class. Split when a
     class accumulates unrelated state or behaviors (e.g. extract a
     `PriceCalculator` from an `Order` that also formats receipts).
   - **Open/Closed**: extend via modules or composition, not by editing every
     consumer. Reach for mixins, strategy objects, or block parameters.
   - **Liskov Substitution**: subclasses must honor the parent contract.
     Beware overriding methods to raise `NotImplementedError` — that is a
     signal to use composition instead.
   - **Interface Segregation in Ruby = duck typing**: depend on the methods
     you need, not on a class. `obj.respond_to?(:each)` over `obj.is_a?(Array)`.
   - **Dependency Inversion**: inject collaborators through the initializer
     rather than instantiating them inside the class. Use keyword arguments
     with sensible defaults: `def initialize(logger: Logger.new($stdout))`.
   - **Composition over inheritance**: prefer `has_a`/mixin to `is_a`. Use
     `Module#prepend` for cross-cutting concerns. Reserve inheritance for
     true sub-type relationships.
   - **DRY pragmatically**: extract duplication that represents the same
     concept; tolerate incidental duplication that may diverge. Two methods
     that look similar today but model different domain rules should stay
     separate.
   - **Tell, Don't Ask**: send messages to objects rather than asking for
     their data and acting on it externally.
   - **Law of Demeter**: avoid long chains across unrelated objects
     (`a.b.c.d`); add a method to the intermediate object instead.

5. **Mix OOP and functional styles deliberately**:
   - Use classes/modules to model **stateful** concepts (identity, lifecycle,
     coordinated state mutation).
   - Use **blocks, procs, and lambdas** for stateless transformations,
     callbacks, and DSLs.
   - Prefer **`Enumerable`** for collection work: `map`, `select`, `reject`,
     `reduce`/`inject`, `each_with_object`, `group_by`, `partition`,
     `find`/`detect`, `flat_map`, `tally`, `chunk_while`.
   - Avoid mutating arguments. Return new collections rather than calling
     `.push`/`.<<` on inputs the caller still uses.
   - Use `Struct` or `Data` (Ruby 3.2+) for simple immutable value objects
     before reaching for a full class with `attr_reader`.
   - Use `Comparable` and `Enumerable` mixins when you implement `<=>` or
     `each`; do not reimplement what they already give you.
   - Reach for `Forwardable` (`def_delegators`) to expose specific collaborator
     methods rather than leaking the collaborator itself.

6. **Encapsulation and visibility**:
   - Use `attr_reader`, `attr_writer`, `attr_accessor` for trivial accessors.
     Write the method by hand only when behavior is needed.
   - Mark non-public methods with the `private` (most common) or `protected`
     keyword. Do not prefix with underscore.
   - Treat instance variables as implementation details; prefer reader methods
     within the class so that derived values and lazy initialization can be
     introduced without rewriting call sites (DHH-style preference for sending
     messages over reaching for ivars directly).
   - Avoid global state and class variables (`@@var`). Prefer constants,
     `Module#module_function`, or a configuration object.
   - Use `Module.new` and `Class.new` only for metaprogramming. Reserve
     `define_method` and `method_missing`/`respond_to_missing?` for cases that
     genuinely require dynamic dispatch (and always implement
     `respond_to_missing?` alongside `method_missing`).

7. **Errors and exceptions**:
   - Raise specific exception classes that descend from `StandardError`.
     Never raise bare `Exception`, and never `rescue Exception` (it catches
     `SignalException`, `SystemExit`, etc.).
   - Define a project-scoped base error: `class MyGem::Error < StandardError; end`
     and inherit specific errors from it so callers can rescue the family.
   - Rescue the narrowest class possible; rescue inside the smallest block
     that can recover. Avoid bare `rescue` (defaults to `StandardError` and
     swallows everything).
   - Use `raise SomeError, "message"` (not `raise SomeError.new("message")`)
     for the common case. Add context to messages — what was attempted, with
     which inputs.
   - Use `ensure` for cleanup that must run (closing files, releasing locks).

8. **Toolchain conventions**:

   **Bundler & gem layout**:
   - Gem source goes in `lib/<gem_name>/`. Top-level constant defined in
     `lib/<gem_name>.rb` and `lib/<gem_name>/version.rb`.
   - Use a `Gemfile` for applications and a `.gemspec` + `Gemfile` for gems.
     In gems, the `Gemfile` should `gemspec` and not duplicate runtime deps.
   - Pin Ruby version in `.ruby-version` (and `required_ruby_version` in the
     gemspec for libraries).
   - Run commands with `bundle exec` to use the locked gem versions.
   - Use semantic versioning in `lib/<gem_name>/version.rb`.

   **RSpec** (preferred when present):
   - One `describe` per class; nested `describe ".class_method"` /
     `describe "#instance_method"` blocks.
   - `context "when <condition>"` for branching scenarios.
   - One expectation per `it` when practical; descriptive names without "should".
   - Use `let` (memoized, lazy) and `let!` (eager) for setup data; use
     `subject` to name the object under test.
   - Prefer `expect(x).to eq(y)` style. Use `have_attributes`, `include`,
     `change`, `raise_error`, `satisfy` matchers idiomatically.
   - Test doubles: `instance_double(Klass)` and `class_double(Klass)` over
     plain `double` so the test fails when the real interface changes.
   - Avoid `before(:all)` / `before(:context)` unless setup is truly read-only
     and expensive; otherwise state leaks between examples.

   **Minitest** (if the project uses it instead):
   - `Minitest::Test` subclasses; methods start with `test_`.
   - Assertions (`assert_equal`, `assert_raises`) or `Minitest::Spec` DSL
     (`describe`/`it`) — match the project's existing convention.

   **RuboCop / Standard**:
   - Follow the project's `.rubocop.yml`. If absent, follow the community
     Ruby Style Guide defaults (rubocop.org) or Standard Ruby (standardrb.com).
   - Run `bundle exec rubocop -A` to auto-correct trivially fixable offenses
     before hand-editing. Never blanket-disable cops; if a rule is wrong for
     a file, disable with a comment that explains why.

   **rake**:
   - Tasks live in `Rakefile` and `lib/tasks/*.rake`. Namespace related tasks:
     `namespace :db do ... end`.
   - Provide `desc` for every public task. Default task usually runs tests
     (and the linter), e.g. `task default: [:spec, :rubocop]`.

   **CLI tools (ruby-cli, OptionParser, Thor)**:
   - For small CLIs, use stdlib `OptionParser`. For richer CLIs with
     sub-commands, use Thor (`bundle add thor`).
   - Place the executable in `exe/<name>` (or `bin/<name>`), `chmod +x`, and
     list it under `spec.executables` in the gemspec.
   - Start the executable with `#!/usr/bin/env ruby` and a `require` of the
     library. Keep `exe/<name>` thin — parse args, then hand off to
     `Lib::CLI.new(argv).run`.
   - Exit with non-zero status on failure (`exit 1` or `abort "message"`).
   - Print errors to `$stderr`, normal output to `$stdout`.

   **REPL / debugging**:
   - Use `binding.irb` (Ruby 2.5+) or `binding.pry` (with the `pry-byebug` gem)
     to drop into a REPL at a breakpoint during development.
   - Use the stdlib `debug` gem (Ruby 3.1+) for the modern debugger.
   - Never commit `binding.irb` / `binding.pry` calls. A pre-commit hook or
     RuboCop cop (`Lint/Debugger`) should catch them.

9. **Documentation**:
   - Use YARD-style comments for public APIs: `@param`, `@return`, `@raise`,
     `@example`. Document the behavior and contract, not the obvious
     mechanics.
   - Add a `README.md` with installation, usage, and a runnable example.
   - Add a `CHANGELOG.md` and update it with every release.

10. **Produce the code**:
    - Generate complete, runnable Ruby files (not snippets) with the
      `# frozen_string_literal: true` header and `require` lines at the top.
    - Define one top-level constant per file; place it under
      `lib/<gem_name>/...` matching the constant path.
    - Include or update the corresponding spec/test file alongside non-trivial
      changes, using the project's existing test framework.

## Output Format

Complete Ruby source files with the frozen-string-literal header, requires,
namespacing, and matching tests. When refactoring, also produce a brief
summary listing each change (what was extracted, what was renamed, what
contract was preserved) so the diff is reviewable. When reviewing, return a
structured report with findings grouped by file and severity (style, design,
bug, security).

## Scope

`**/*.{rb,rake,gemspec}`, `Gemfile`, `Rakefile`, `bin/*`, `exe/*`.

Excludes Rails-specific paths (`app/`, `config/`, `db/migrate/`); if those
appear, defer framework-specific concerns to a Rails skill and apply this
skill only to library code under `lib/`, scripts, and tests.

## Constraints

1. **Never** rename methods or variables to non-Ruby conventions (no
   `camelCase`, no `getFoo`/`setFoo`, no `PascalCase` methods).
2. **Never** use `rescue Exception` or bare `rescue` — always rescue
   `StandardError` or a more specific subclass.
3. **Never** introduce Rails-specific dependencies, methods, or idioms
   (`ActiveSupport`'s `present?`/`blank?`, `ActiveRecord`, `params`, etc.).
   If a Rails-only helper is requested, decline and suggest the plain Ruby
   equivalent.
4. **Never** mutate input arguments unless the method is explicitly
   destructive (ends in `!`) and the contract documents it.
5. **Never** monkey-patch core classes (`String`, `Array`, `Hash`, `Object`)
   in library code. If extending core types is essential, use refinements
   (`using` scope) and document the trade-off.
6. **Never** leave `binding.irb`, `binding.pry`, `puts` debug prints, or
   `byebug` calls in committed code.
7. **Never** add a gem dependency without justifying it and pinning a
   sensible version constraint in the Gemfile or gemspec.
8. **Never** add `# rubocop:disable` blanket comments without an inline
   reason and the narrowest cop scope.

## Edge Cases

- **Ruby version differences**: If the project pins an older Ruby (`.ruby-version`),
  avoid syntax/features that postdate it: pattern matching `in` (3.0+), `Data.define`
  (3.2+), endless methods `def foo = ...` (3.0+), `it` implicit block param (3.4+).
  Confirm the target version before using new features.
- **Concurrency**: `Thread` is preemptive in MRI but the GVL limits true
  parallelism for pure-Ruby code. Use `Mutex` to protect shared mutable
  state. For I/O concurrency, consider `Fiber` (Ruby 3+ scheduler) or
  threading. For CPU work, separate processes (Ractor, fork, or a job queue).
- **Encoding**: Ruby strings are encoded; default is UTF-8. Mixing
  encodings raises `Encoding::CompatibilityError`. Use
  `String#force_encoding` only when you know the underlying bytes; use
  `String#encode` to convert.
- **`nil` vs. missing**: `nil` is an object. `nil?`, `respond_to?`, and
  pattern matching are safer than `==` checks. Avoid using `false` to mean
  "missing" — that conflates two states.
- **Numeric types**: `Integer` and `Float` do not auto-promote across all
  operations the same way. `1 / 2 == 0`; use `1.0 / 2` or `Rational(1, 2)`
  when fractional results matter. Use `BigDecimal` for money.
- **`Struct` vs `Data` vs `Class`**: `Struct` is mutable by default;
  `Data` (Ruby 3.2+) is immutable and is usually what you want for value
  objects. Use a plain class when you need behavior beyond accessors.
- **Hash ordering**: insertion-ordered since Ruby 1.9. Do not rely on
  sortedness; sort explicitly when needed.
- **`Kernel#load` vs `require`**: `require` loads once and is what you almost
  always want. `load` re-evaluates each time — useful in REPLs, rarely
  elsewhere.
- **Frozen strings with mutation**: if you need a mutable string in a file
  with `# frozen_string_literal: true`, use `String.new("...")` or `+"..."`
  rather than removing the header.

## Cross-Ecosystem Notes

- **Claude Code**: Place this file at `.claude/skills/ruby.md` (or invoke via
  the Skill tool by name `ruby`). Triggers automatically on Ruby-related
  keywords listed in the description.
- **Cursor**: Install the translated rule at `.cursor/rules/50-skill-ruby.mdc`.
  Activation is manual (use `@50-skill-ruby` in a prompt) or scope it to
  `**/*.rb` for auto-attach. The `.mdc` translation drops Claude-specific
  metadata and folds the steps into Cursor's rule format.
- **Codex (OpenAI Codex CLI)**: Append the translated task section to
  `AGENTS.md` under `## Available Tasks`. Reference "Task: Ruby Development"
  in prompts. Codex has no native skill activation, so the rule is applied
  by referring to it explicitly.
- **Aider**: Append the CONVENTIONS.md section, then `/add CONVENTIONS.md` in
  the Aider session. (Not requested for this build, but supported if needed.)
