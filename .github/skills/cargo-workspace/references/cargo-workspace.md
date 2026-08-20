# Cargo Workspace Execution Profile

Use this profile when execution-profile resolution selects `cargo-workspace`: either the
command-owning checkout root declares `Execution profile: cargo-workspace`, or that root declares
no profile and Cargo is the default.

## Command Authority

This profile selects the normal Rust formatter, build, lint, and test commands. It overrides
command examples in any shared language guidance.

- Build: `cargo build --workspace`
- Lint: `cargo clippy --workspace --bins --examples --tests -- --no-deps`
- Format: `cargo +nightly fmt`
- Test all: `cargo nextest run`
- Test one: `cargo nextest run <test-name>`
- Test one crate: `cargo nextest run -p <crate-name>`
- Coverage: `cargo tarpaulin --engine llvm -o html`

Run Cargo commands directly. Do not prefix them with `SKIP_PROTO_GEN=1`.
Use `cargo nextest` instead of `cargo test` unless a debugger or profiler requires `cargo test`.
