---
name: bitdrift-css
description: Use when editing, reviewing, testing, or debugging plain CSS stylesheets, layout, themes, tokens, or CSS reset behavior in bitdrift repositories.
---

Follow the CSS standards in `references/css.md`.

Before editing or reviewing CSS:

1. Read `references/css.md` and inspect the owning repository's stylesheet conventions and
   validation commands.
2. Reuse the local design tokens and component styling patterns; do not model new component styles
   on nested selectors that target raw elements.
3. Use `references/css-reset.css` only when creating a new stylesheet entrypoint. Do not retrofit
   it into an existing application without explicit scope and visual-regression coverage.
4. Validate the affected responsive sizes, themes, and interactive states in proportion to the
   change risk.
