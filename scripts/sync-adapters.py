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


rust_core = markdown_with_trailing_newline("instructions/rust.md")
css_core = markdown_with_trailing_newline("instructions/css.md")
css_reset = (ROOT / "instructions/css-reset.css").read_text(encoding="utf-8").strip()
css_reset = f"{css_reset}\n"
cargo_workspace = markdown_with_trailing_newline("instructions/cargo-workspace.md")
bazel_monorepo = markdown_with_trailing_newline("instructions/bazel-monorepo.md")

write(
    ".github/instructions/rust.instructions.md",
    f"""---
name: 'Rust Standards'
description: 'Coding conventions for Rust files'
applyTo: '**/*.rs'
---
{rust_core}""",
)

write(
    ".claude/rules/rust.md",
    f"""---
paths:
  - "**/*.rs"
  - "**/Cargo.toml"
  - "**/Cargo.lock"
---
{rust_core}""",
)

write(
    ".github/instructions/css.instructions.md",
    f"""---
name: 'CSS Standards'
description: 'Coding conventions for CSS files'
applyTo: '**/*.css'
---
{css_core}""",
)

write(
    ".claude/rules/css.md",
    f"""---
paths:
  - "**/*.css"
---
{css_core}""",
)

write("codex/bitdrift-instructions/skills/rust/references/rust.md", rust_core)
write("opencode/skills/bitdrift-rust/references/rust.md", rust_core)
write("codex/bitdrift-instructions/skills/css/references/css.md", css_core)
write("opencode/skills/bitdrift-css/references/css.md", css_core)
write("codex/bitdrift-instructions/skills/css/references/css-reset.css", css_reset)
write("opencode/skills/bitdrift-css/references/css-reset.css", css_reset)

for adapter_path, profile in (
    (".github/skills/cargo-workspace/references/cargo-workspace.md", cargo_workspace),
    (".github/skills/bazel-monorepo/references/bazel-monorepo.md", bazel_monorepo),
    (
        "codex/bitdrift-instructions/skills/cargo-workspace/references/cargo-workspace.md",
        cargo_workspace,
    ),
    (
        "codex/bitdrift-instructions/skills/bazel-monorepo/references/bazel-monorepo.md",
        bazel_monorepo,
    ),
    ("opencode/skills/cargo-workspace/references/cargo-workspace.md", cargo_workspace),
    ("opencode/skills/bazel-monorepo/references/bazel-monorepo.md", bazel_monorepo),
):
    write(adapter_path, profile)
