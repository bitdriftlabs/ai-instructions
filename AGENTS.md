# ai-instructions repository guidance

This repository keeps one canonical set of instructions and renders thin adapters for each agent
harness.

## Parity model

- Treat `instructions/*.md` as the source of truth for shared guidance.
- Treat generated files in `.github/instructions/`, `.claude/rules/`,
  `codex/bitdrift-instructions/skills/*/references/`, and `opencode/skills/*/references/` as
  rendered outputs. Do not hand-edit them unless you are also updating the generator.
- Harness-specific wrapper files such as `SKILL.md`, plugin metadata, and marketplace metadata
  are checked in directly and should stay thin. They may describe how a harness loads the shared
  instructions, but they should not fork the Rust guidance itself.
- Parity means the substantive Rust instructions are the same across harnesses. Small harness-level
  differences are acceptable only when required by frontmatter, metadata, or invocation mechanics.

## Updating shared instructions

1. Edit the canonical file under `instructions/`.
2. Run `python3 scripts/sync-adapters.py`.
3. Review the regenerated adapter files and keep checked-in wrapper text aligned with the same
   parity model.

## Adding a new harness

- Add a thin adapter that points at or embeds the canonical instruction content.
- Extend `scripts/sync-adapters.py` so the adapter is generated from `instructions/`.
- Keep CI enforcing that generated files are committed and in sync.
