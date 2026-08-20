# Bazel Monorepo Execution Profile

Use this profile only when the command-owning checkout root declares
`Execution profile: bazel-monorepo`.

## Command Authority

This profile selects the normal Rust formatter, build, lint, and test commands. It overrides
command examples in any shared language guidance.

- Format: `just rustfmt <touched-rust-paths>`
- Lint: `./bazelw test --config=clippy //path/to/package/...`
- Test: `./bazelw test <focused-target>`

Do not use `cargo fmt`, raw `rustfmt`, `cargo clippy`, `cargo nextest`, or `cargo test` for normal
formatting, linting, or test validation. Cargo is allowed only for repository-documented generation
or maintenance steps.

Run `just rustfmt <touched-rust-paths>` after any Clippy-driven source change, then rerun focused
Clippy. Use repository instructions for submodule-specific Bazel targets and workflows.
