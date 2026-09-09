# CSS Core Standards

## Scope and Existing Styles

- These standards apply to plain `.css` files. Follow the owning repository's instructions for
  preprocessors, CSS-in-JS, framework styling systems, supported browsers, and validation commands.
- Before changing a stylesheet, inspect its entrypoint, nearby styles, existing design tokens, and
  the components that consume it. Preserve established local organization unless the task includes
  a deliberate migration.
- Use the bundled CSS reset only as a starting point for a new stylesheet entrypoint. Do not apply
  a reset wholesale to an existing application without a deliberate compatibility review and
  visual-regression testing.
- Add a root stacking context only when the owning application needs it, and target that
  application's actual root explicitly rather than assuming a framework-specific root ID.

## Design Tokens and Values

- Reuse the project's existing semantic design tokens and custom properties for color, spacing,
  typography, radii, elevation, and control dimensions.
- Add a shared custom property only when a value has a reusable semantic role. Name tokens by their
  purpose, not their current appearance, such as `--palette-text-muted` or `--space-4`.
- Keep one-off layout values local. Do not introduce a token merely to avoid a single literal.
- Use custom-property overrides for themes and component variants rather than duplicating complete
  rule sets or hard-coding alternate-theme values.
- Use `rem` for font sizing and user-scalable dimensions where appropriate. Reserve fixed units for
  deliberate physical details such as borders, and match local conventions for all other units.

## Inline Styles

- Do not add inline `style` attributes or framework style props for static presentation. Keep
  styling in the stylesheet so it can reuse tokens, respond to themes and media queries, and remain
  reviewable with the component's other styles.
- Use inline custom properties only when runtime data must supply a dynamic value that cannot be
  represented by an existing class or stylesheet state. Keep the inline value narrow and consume it
  from a class-based stylesheet rule.

## Selectors and Cascade

- Name component classes in lowercase kebab-case and choose names that communicate the component or
  its role. Use class selectors for component parts and states.
- Keep specificity low: prefer a single class selector when it expresses the rule. Avoid IDs for
  styling and do not use `!important` except for a documented interoperability or intentional
  global-override case.
- Do not target raw elements through nested component selectors, such as `.card { & p { ... } }`.
  Give the styled element a class and target that class instead.
- Element selectors are appropriate only for intentional global base styles, resets, and semantic
  document defaults. Do not use broad descendant selectors to reach into another component.
- Keep CSS nesting shallow. Nest pseudo-classes, pseudo-elements, and tightly coupled class states
  only when nesting makes the relationship clearer without increasing specificity unexpectedly.
- Use the cascade deliberately. Prefer local component ownership and existing cascade layers over
  selector escalation.

## Layout, Responsiveness, and Organization

- Use Flexbox for one-dimensional alignment along a row or column. Use CSS Grid when a layout needs
  coordinated rows and columns, explicit placement, or repeated two-dimensional structures such as
  cards, forms, and data displays. Prefer `gap` for spacing between siblings over margin-based
  layout hacks.
- Consider `subgrid` when a nested component must align its tracks with its parent grid, such as a
  card's header and body aligning with neighboring cards. Use it only when the project's browser
  support allows it; otherwise preserve the alignment with explicitly shared track definitions.
- Use intrinsic and fluid sizing (`min()`, `max()`, `clamp()`, `minmax()`, `auto-fit`, and
  `auto-fill`) where they express the layout directly. Choose breakpoints based on content failure,
  not device names.
- Use container queries for component-local responsiveness when the project's browser support
  allows them; otherwise use focused media queries.
- Prefer logical properties when they make the rule work naturally in different writing directions.
- Keep stylesheets focused and arrange rules in a consistent local order: global/base rules first,
  then layout and component rules, followed by states, responsive overrides, and utilities as used
  by the project. Comment non-obvious cascade, layout, or browser-compatibility decisions.

## Accessibility and User Experience

- Preserve semantic HTML and visible keyboard focus. Never remove an outline unless an equivalent
  or stronger focus indicator is provided for the same interaction state.
- Use token combinations that meet the project's accessibility requirements, including sufficient
  text and interactive-control contrast in every supported theme.
- Test interactive states: hover where relevant, focus-visible, disabled, selected, invalid, and
  loading states. Do not communicate state through color alone.
- Respect `prefers-reduced-motion`; make decorative animation optional and avoid motion that blocks
  comprehension or interaction.
- Prevent accidental overflow with responsive layouts, flexible text wrapping, and responsive media
  defaults. Verify the UI at narrow and wide sizes relevant to the changed component.

## Validation

- Run the formatter, linter, build, and visual or browser checks configured by the owning
  repository. Do not invent universal CSS commands.
- For changes to global styles, tokens, resets, or themes, broaden verification to affected routes,
  color schemes, and interactive states. Treat unexpected visual changes as regressions until they
  are understood and accepted.
