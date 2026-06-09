# Color

Use color to carry brand tone, hierarchy, interaction state, and meaning. Build the system from a small set of key colors, shared neutrals, functional colors, accent colors, and semantic colors.

Core rules:
- Text must meet `4.5:1` contrast against its actual background.
- Non-text UI, icons, controls, and boundaries must meet `3:1` contrast against adjacent backgrounds.
- Check final foreground/background pairings; token validity alone is not enough.
- Do not rely on color as the only signal for state, severity, or importance.

Role map:
- Primary color: the main brand tone, primary actions, active states, and the strongest visual cue in the UI.
- Secondary and tertiary colors: supporting hierarchy and alternative states that should stay subordinate to the primary tone.
- Background colors: section and surface colors that must be validated with every foreground placed on them.
- Common neutrals: text, borders, dividers, surfaces, disabled-like chrome, and low-contrast structure.
- Functional colors: links and other interaction-specific cues with conventional meaning.
- Accent colors: sparse emphasis for highlights or occasional calls to action.
- Semantic colors: success, warning, error, and similar meaning-bearing states; keep each meaning consistent across the product.

Selection heuristics:
- Prefer one coherent key-color family, then derive lighter and darker steps for hierarchy and state changes.
- Use chromatic colors only when they help the user decide, act, or recognize meaning.
- If a brand color fails contrast, adjust its lightness for UI use or reserve it for non-UI brand expression.
- For links, preserve familiar visited/unvisited differentiation while still meeting contrast requirements.
- For charts or other color-coded content, provide nearby text so meaning survives outside color.
