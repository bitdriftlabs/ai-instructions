#!/usr/bin/env python3
"""Render tool-specific instruction adapters from canonical sources."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def write(path: str, content: str) -> None:
    destination = ROOT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")


def markdown_with_trailing_newline(path: str) -> str:
    content = (ROOT / path).read_text(encoding="utf-8").strip()
    return f"{content}\n"


rust = markdown_with_trailing_newline("instructions/rust.md")

write(
    ".github/instructions/rust.instructions.md",
    f"""---
name: 'Rust Standards'
description: 'Coding conventions for Rust files'
applyTo: '**/*.rs'
---
{rust}""",
)

write(
    ".claude/rules/rust.md",
    f"""---
paths:
  - "**/*.rs"
  - "**/Cargo.toml"
  - "**/Cargo.lock"
---
{rust}""",
)

write("codex/bitdrift-instructions/skills/rust/references/rust.md", rust)
write("opencode/skills/bitdrift-rust/references/rust.md", rust)
