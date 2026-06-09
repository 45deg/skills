# Typography

Typography supports readability, structure, density, and product identity.

Family and weight:
- Use a readable sans-serif family for general content.
- Use a monospaced family for code-like content, tokens, identifiers, and aligned technical readouts.
- Treat `N` as normal weight around `400`.
- Treat `B` as bold weight around `700`.
- Keep font choice resilient to system fallback and user-controlled font settings.

Size bands:
- `48-64 CSS px`: display-scale text for rare, high-impact headline moments.
- `16-45 CSS px`: the main band for headings, body text, and ordinary readable content.
- `14 CSS px`: constrained support text or dense UI only.
- Avoid text smaller than `14 CSS px`.
- Treat `16 CSS px` as the practical baseline for body and UI readability.

Line height:
- `100%`: one-line control labels and compact UI labels.
- `120-130%`: dense operational screens and table-like information density.
- `140%`: larger headings.
- `150%`: the minimum comfortable rhythm for prose-like body text.
- `160-175%`: comfortable reading rhythm for longer passages.

Implementation guidance:
- Use unitless CSS `line-height` values even when design tokens are expressed as percentages.
- Let enlarged text reflow cleanly instead of relying on fixed-height containers.
- Preserve readability before density when content is user-facing and explanatory.
