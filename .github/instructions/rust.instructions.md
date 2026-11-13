---
name: 'Rust Standards'
description: 'Coding conventions for Rust files'
applyTo: '**/*.rs'
---
# Rust Core Standards

## Execution Profile Resolution

This document intentionally does not prescribe concrete formatter, build, lint, or test commands.
Resolve the execution profile before running those commands:

1. Identify the checkout root that owns the command. An enclosing monorepo root owns commands for
  its nested repositories; otherwise, the repository root owns its own commands.
2. If that root's `AGENTS.md` declares `Execution profile: <name>`, load and apply that profile.
3. If the command-owning root declares no profile, use the Cargo Workspace Execution Profile.

Child repository instructions may add repository-specific constraints, but do not select an
execution profile that overrides their command-owning checkout root.

## Code Style Guidelines

- In general do NOT duplicate code. Practice DRY and favor moving shared code to a common helper.
- Use 2-space indentation (no tabs)
- Max line width: 100 characters
- Error handling: Use `anyhow` for general errors, `thiserror` for custom error types. In a
  `Result`-returning function, prefer `anyhow::bail!("...")` for an immediate validation or
  guard-clause error instead of `return Err(anyhow::anyhow!("..."))`.
- Imports: Group imports with `One` style, module granularity, and `HorizontalVertical` layout
- Always put imports at the top of the file.
- Use workspace dependencies from `Cargo.toml` where available
- Edition: Rust 2024
- If rustfmt reports a line width error for imports, split the path by importing a prefix module and
  then importing items from that prefix
- Use pattern matching with if-let and match expressions for error handling
- When you write comments, flow them out to 100 columns for wrapping
- The code you write *should* have comments. I don't want overly verbose comments, but if a section
  of code is not obvious from a very quick read, it should have a one or two sentence comment above
  it explaining it. The comment length can increase with the complexity of what is being documented.
  Any very long functions should have minimal comments above logical sections with a brief summary
  of that section
- ALWAYS use imports for structs, enums, etc. to avoid verbose code. NEVER use fully qualified names
  like `crate::module::Struct` in the code without importing `Struct` at the top of the file.
- **NEVER** use `.context()` on anyhow errors unless explicitly requested. It makes the code more
  verbose and is not the style used in this codebase. Use `anyhow::anyhow!()` with `ok_or_else()`
  instead of `.context()` when adding error messages to Option types.
- Do NOT be lazy and leave around function parameters prefixed with `_` to fix compile errors.
  Remove the parameter and fix callers.
- When setting expectations on `Arc`-wrapped mocks, use `bd_test_helpers::make_mut` to get a mutable
  reference for configuring the mock.
- Code that is only used by tests should either be placed in the test file, or if it needs to be
  used by multiple test files, it should be placed in a `test` module in the crate. If the code is
  only used within the crate, the module can be `#[cfg(test)]`, but if it needs to be used by other
  crates, it should not be `#[cfg(test)]`, and can be public.
- Logical sections of code > than approximately 250 lines should go in its own module. Do not write
  gigantic monolithic modules.
- DO add logging to written code using the log crate. High frequency code should use trace/debug
  level. Startup/shutdown and important low frequency events should use the info level. For handled
  errors that can occur at high frequency use the `warn_every` macro from `bd_log` to rate limit the
  logging.
- When debugging unclear asynchronous, concurrent, or lifecycle behavior, add narrow trace/debug
  logs for the relevant state transitions and blocking predicates before making further speculative
  changes. Use the resulting trace to choose the next hypothesis, and retain logs that provide
  durable operational observability after the immediate issue is fixed.
- Structs/enums and their implementation should be delimited with a multi-line comment header like
  the following:

```rust
//
// StructName
//
```

## Synchronization guidelines
- Do NOT use tokio::sync::Mutex unless there is no way to avoid it and its use must be justified by
  comments. It is prone to deadlocks. Use parking_lot for Mutex and RwLock.

## Documentation Guidelines

- Avoid redundant documentation for the sake of convention. For example:
  - Don't include an Errors section if the only errors are generic failures
  - Don't include an Arguments section if the arguments are obvious based on the function signature

## What to Test

Each test must catch a specific bug. Apply these rules to every test you add or change:

- Name the bug the test catches before writing it. If you cannot name one, do not write the test.
- The test must fail when that bug is present: on the code before a fix, or against a plausible
  wrong version of new code (an off-by-one, a missing branch, a validator that rejects too much). A
  test that would pass either way tests nothing; strengthen it or drop it. When you add a check that
  rejects input, keep one test that valid input still passes it.
- Put each case at the cheapest level that can observe it. Integration tests cover wiring, with one
  case per call site; never repeat the same inputs at two levels.
- Do not test what the compiler, a plain derive (`Default`, `Clone`, `PartialEq`), `std` or a
  third-party crate already guarantees (such as `clap` parsing or `?` propagation), constants, or
  constructors and accessors that only store or return a field.
- A mapping a reviewer can verify by reading, such as a short `match` or a field copy, does not
  need its own unit test. Prove its consequence once, where it is observable.
- Do not add tests that check removed code is gone: a deleted field absent from output, a removed
  endpoint returning 404, a dropped config key being ignored. Nothing will re-add it by accident,
  and the compiler or existing tests catch remaining uses. Check it locally if you need to, but do
  not commit the test. This does not cover tests that invalid input is rejected, which test
  behavior. When the absence is itself a requirement (a secret or personal field must never be
  logged or exported, a revoked permission must stay denied), it is a contract: test it.
- A serializer and deserializer generated from the same definition, whether `serde` derives or
  protobuf codegen, cannot catch a renamed field or a changed field number, because both sides
  change together. When a format is a contract (wire, storage, config, or another service's
  input), decode a fixture or snapshot of bytes from the other side's current version, covering
  attributes such as `rename`, `skip_serializing`, `default` and `flatten`. A round trip between
  independently written directions, such as a parser and a formatter, is valid when fidelity is
  the requirement.
- With a mock, assert what crosses the boundary when that is the behavior: a request field sent, a
  message published, bytes charged, no write made. Do not assert call counts, call order, or
  arguments the code only passes through.
- A concurrency, cancellation or shutdown test must assert an effect the wrong ordering would
  change. Forcing a drop or interleaving and then observing nothing does not test it.
- Test through the function or type that other code calls, not helpers that only it uses. Cover
  cases that differ only in input with one table-driven test, and extend an existing test before
  adding a new one.
- Fewer tests is fine. When you change code, merge or delete tests in that code that duplicate
  each other.

## Test File Conventions

1. Test files should be placed adjacent to the implementation file they're testing
2. Test files should be named with a `_test.rs` suffix (e.g., `network_quality_test.rs`)
3. Link test files in the implementation file using the following pattern at the top of the file,
   right below the license header (if applicable) and optional module-level docs.

   ```rust
   #[cfg(test)]
   #[path = "./file_name_test.rs"]
   mod tests;
   ```

4. Tests in the same file as the implementation code must be avoided
5. Test names should *not* start with `test_`, as this is redundant
6. Use module-level clippy allow blocks instead of per-test allows if applicable. Example:

   ```rust
   #![allow(clippy::unwrap_used)]
   ```

   This should be placed at the top of the test file, after the license header (if applicable) and
   before imports.

## Code Quality Checks

- Always run tests on modified crates.
- After generating or modifying code, always run clippy to check and fix static lint violations on
  modified crates.
- After fixing clippy issues, format the code.

## get_errors tool

CRITICAL: ONLY follow the below guidelines if the `get_errors` tool is available.

- **ALWAYS** start by checking IDE/editor errors using the `get_errors` tool before making any
  changes. This is much faster than running cargo commands and catches issues immediately.
- When writing code for faster iteration, continuously use `get_errors` to check for compilation
  errors after each change (like Rust Analyzer in VS Code or vim).
- If `get_errors` keeps reporting errors that do not seem correct, try compiling. If the errors
  persist, tell the user to restart Rust Analyzer.
- **CRITICAL**: At the end of ANY task that modifies code, ALWAYS verify with the `get_errors` tool
  to check IDE errors across the ENTIRE workspace (do not pass file paths). If there are errors fix
  the entire project.

## SQL Testing Guidelines

- It is *CRITICAL* to write integration tests that validate SQL via the associated database
  (Clickhouse/Postgres/sqlite). Testing SQL queries/fragments as text can have its place but *DOES
  NOT* replace integration test coverage.
