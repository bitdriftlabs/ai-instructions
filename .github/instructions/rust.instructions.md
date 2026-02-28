---
name: 'Rust Standards'
description: 'Coding conventions for Rust files'
applyTo: '**/*.rs'
---
# Rust coding standards
## Build/Lint/Test Commands
- Build: `cargo build --workspace`
- Lint: `cargo clippy --workspace --bins --examples --tests -- --no-deps`
- Format: `cargo +nightly fmt`
- Test (all): `cargo nextest run`
- Test (single): `cargo nextest run test_name`
- Test (specific crate): `cargo nextest run -p crate-name`
- Coverage: `cargo tarpaulin --engine llvm -o html`
- When verifying, just run cargo commands directly. Do not prefix with SKIP_PROTO_GEN=1.

## Code Style Guidelines
- Use 2-space indentation (no tabs)
- Max line width: 100 characters
- Error handling: Use `anyhow` for general errors, `thiserror` for custom error types
- Imports: Group imports with `One` style, module granularity, and `HorizontalVertical` layout
- Always put imports at the top of the file.
- Use workspace dependencies from Cargo.toml where available
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
- Do NOT be lazy and leave around function parameters prefixed with _ to fix compile errors. Remove
  the parameter and fix callers.
- When setting expectations on `Arc`-wrapped mocks, use `bd_test_helpers::make_mut` to get a mutable
  reference for configuring the mock.
- Structs/enums and their implementation should be delimited with a multi-line comment header like
  the following:

```rust
//
// StructName
//
```

## Documentation Guidelines
- Avoid redundant documentation for the sake of convention. For example:
    - Don't include an Errors section if the only errors are generic failures
    - Don't include an Arguments section if the arguments are obvious based on the function signature

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
* **ALWAYS** start by checking IDE/editor errors using the `get_errors` tool before making any
  changes. This is much faster than running cargo commands and catches issues immediately.
* When writing code for faster iteration, continuously use `get_errors` to check for compilation
  errors after each change (like Rust Analyzer in VS Code or vim).
* If `get_errors` keeps reporting errors that do not seem correct, try compiling. If the errors
  persist, tell the user to restart Rust Analyzer.
* **CRITICAL**: At the end of ANY task that modifies code, ALWAYS verify with the `get_errors` tool
  to check IDE errors across the ENTIRE workspace (do not pass file paths). If there are errors
  fix the entire project.
