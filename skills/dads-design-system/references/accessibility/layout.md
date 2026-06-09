# Layout

Layout affects whether content remains understandable when the viewport changes or when assistive technology follows the page structure.

- Prefer liquid, responsive layouts over fixed-width layouts.
- Allow horizontal scrolling when it is genuinely unavoidable, and keep the scrollbar visible.
- Keep visual order close to DOM order, reading order, and focus order.
- Use CSS ordering only for small visual adjustments, not to rewrite the logic of the page.
- If a layout needs major visual reordering, change the markup structure instead of forcing it with CSS.
- Be careful with grids and multi-column pages that split related content across separate visual positions.
- Ensure the compact version still exposes the same information and actions, not a reduced or hidden version of the page.
