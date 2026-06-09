# Text Styles

Use text-style families as a vocabulary:
- `Dsp`: display text for large, sparse headline moments.
- `Std`: standard headings and body copy.
- `Dns`: dense information-heavy screens.
- `Oln`: compact one-line UI labels and controls.
- `Mono`: code, identifiers, tokens, and aligned technical text.

Token names combine family, size, weight, and line height. Example pattern: `Std-17N-170`.

Selection rules:
- Choose the family by use case first, then size and weight.
- Use the smallest style that still reads clearly in the target layout.
- Keep headings visually distinct from body text.
- Avoid mixing families casually inside one visual region.
- Use dense styles for operational density, not ordinary prose.

Style cues:
- `Dsp` implies a strong opening or presentation-like emphasis.
- `Std` is the default readable workhorse for most content.
- `Dns` trades breathing room for compact information display.
- `Oln` assumes one-line controls where vertical padding must stay tight.
- `Mono` should preserve alignment and token readability even when content varies in length.
