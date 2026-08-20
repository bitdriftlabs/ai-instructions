---
name: bitdrift-rust
description: Use when editing, reviewing, testing, or debugging Rust code, Cargo manifests, Rust SQL queries in Rust, Rust protobuf bindings, or Rust CI failures in bitdrift repositories.
compatibility: opencode
metadata:
  source: bitdrift-ai-instructions
---

Follow the Rust standards in `references/rust.md`.

Before editing or reviewing Rust:

1. Load `references/rust.md` with the skill context.
2. Identify the checkout root that owns formatter, build, lint, or test commands, then resolve its
  execution profile as described in `references/rust.md`.
3. Load the matching execution-profile skill when it is available. Otherwise, follow the commands
  in the command-owning checkout's instructions.
4. Apply the Rust core conventions and the selected profile, then prefer focused verification on
  modified crates before broadening for change risk.
