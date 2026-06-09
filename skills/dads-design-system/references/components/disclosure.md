# Disclosure

Purpose: Hide supplementary information inside a section.

Use when extra content is useful but not required for the first pass.

Avoid when the hidden content is essential or the whole section should collapse.

Key rules:
- Keep the title stable across open and closed states.
- Optional return links should point back to the title.
- Prefer native disclosure behavior when possible.
- Nested disclosures are acceptable with restraint.
- Do not put an accordion inside a disclosure.

Accessibility: Custom implementations need keyboard support and state exposure.

Related: `accordion`.
