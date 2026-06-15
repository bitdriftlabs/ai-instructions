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
2. Apply those conventions unless closer repository instructions override them.
3. Prefer focused verification on modified crates, then broaden only when the change risk requires it.
