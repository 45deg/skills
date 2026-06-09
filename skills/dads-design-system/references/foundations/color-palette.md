# Color Palette

Use primitive color families as the base for product themes, then derive controlled lighter and darker steps. Add a new hue only when the product truly needs a different visual system.

Use neutrals for:
- Text hierarchy and body copy.
- Borders, dividers, focus-adjacent structure, and other low-importance separators.
- Backgrounds and surfaces.
- Disabled-looking but still readable secondary chrome.

Practical guardrails:
- Reuse palette steps rather than hand-tuning each component.
- Keep neutral ramps wide enough to support both light and dark surfaces.
- Keep chromatic colors tied to brand, interaction, emphasis, or semantic meaning.
- Treat palette steps as reusable building blocks, not one-off component colors.

Token heuristics:
- `Gray-420`: a useful non-text boundary on light surfaces.
- `Gray-536`: a midpoint neutral that can still work for text.
- `Gray-600`: a useful non-text boundary on dark surfaces.
- If a pair needs to carry meaning or state, prefer a semantic or functional token over a decorative accent.
