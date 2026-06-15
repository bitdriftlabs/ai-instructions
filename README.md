# ai-instructions

Public collection of AI instructions used at bitdrift.

This repo keeps shared guidance in tool-neutral Markdown, then renders thin adapters for the
coding agents used across the company.

## Layout

- `instructions/`: canonical instruction sources.
- `.agents/plugins/marketplace.json`: Codex plugin marketplace for this repository.
- `.github/instructions/`: GitHub Copilot path-specific custom instructions.
- `.claude/rules/`: Claude Code path-scoped rules.
- `codex/bitdrift-instructions/`: Codex plugin with checked-in skill wrappers and synced references.
- `opencode/skills/`: OpenCode skills with checked-in wrappers and synced references.
- `scripts/sync-adapters.py`: regenerates tool-specific instruction payloads from `instructions/`.
- `.github/workflows/verify-adapters.yml`: CI check that generated adapters are current.

## Updating Instructions

Edit the canonical file first, then regenerate adapters:

```sh
python3 scripts/sync-adapters.py
```

For Rust, edit `instructions/rust.md`. The sync script updates:

- `.github/instructions/rust.instructions.md`
- `.claude/rules/rust.md`
- `codex/bitdrift-instructions/skills/rust/references/rust.md`
- `opencode/skills/bitdrift-rust/references/rust.md`

The harness wrapper files such as `SKILL.md`, plugin manifests, and marketplace metadata are
checked in directly and should stay thin.

## Codex

The Codex adapter is packaged as a plugin with a checked-in `bitdrift-rust` skill wrapper. The
skill is intended to be invoked implicitly for Rust work, or explicitly with `$bitdrift-rust`.

Install the marketplace locally:

```sh
codex plugin marketplace add ~/src/ai-instructions
```

Then restart Codex, open `/plugins`, select the `bitdrift` marketplace, and install
`bitdrift-instructions`.

For company-wide installs from GitHub:

```sh
codex plugin marketplace add bitdriftlabs/ai-instructions --ref main
```

Use repository `AGENTS.md` files for repo-specific overrides and routing. For example:

```md
- For Rust work, use the `bitdrift-rust` skill.
```

## Claude Code

The Claude adapter is a path-scoped rule at `.claude/rules/rust.md`.

For a single repository, copy or symlink it into that repository:

```sh
mkdir -p /path/to/repo/.claude/rules
ln -s ~/src/ai-instructions/.claude/rules/rust.md /path/to/repo/.claude/rules/rust.md
```

For local use across repositories, symlink it into your user-level Claude rules:

```sh
mkdir -p ~/.claude/rules
ln -s ~/src/ai-instructions/.claude/rules/rust.md ~/.claude/rules/bitdrift-rust.md
```

Claude Code resolves symlinked rule files and applies the `paths` frontmatter when it works with
matching Rust and Cargo files.

## OpenCode

The OpenCode adapter is a skill, not a plugin. OpenCode plugins are JavaScript/TypeScript event
hooks; reusable coding guidance belongs in a checked-in `SKILL.md` so OpenCode can expose it
through the native `skill` tool and load it on demand.

For local use across repositories, symlink the skill into OpenCode's global skill directory:

```sh
mkdir -p ~/.config/opencode/skills
ln -s ~/src/ai-instructions/opencode/skills/bitdrift-rust ~/.config/opencode/skills/bitdrift-rust
```

For a single repository, symlink it into the project:

```sh
mkdir -p /path/to/repo/.opencode/skills
ln -s ~/src/ai-instructions/opencode/skills/bitdrift-rust /path/to/repo/.opencode/skills/bitdrift-rust
```

Use repository `AGENTS.md` files for repo-specific overrides and routing. For example:

```md
- For Rust work, use the `bitdrift-rust` skill.
```
