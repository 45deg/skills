# Layout

Layout should make the structure of a page easy to scan and predict. Treat the grid as the system that keeps alignment, grouping, and spacing coherent across templates.

Grid fundamentals:
- Margins protect the page edges and prevent content from feeling pinned to the viewport.
- Columns define the main content lanes.
- Gutters keep adjacent columns from visually merging.
- Menu or navigation regions may reserve their own fixed or flexible track.
- A 12-column grid is a practical default when you need many combinations without creating new templates.

Choose the layout by task:
- Use one column for reading, forms, and focused workflows.
- Use two columns for content plus supporting material, or for comparing two primary areas.
- Use three or four columns for dashboards, catalogs, and other parallel views.
- Use offsets sparingly when a page needs a stronger focal block.

Responsive guidance:
- Prefer liquid, responsive behavior over fixed-width pages.
- Use `768px` as the default breakpoint only when the product does not already define a better split.
- Collapse or simplify structure as width narrows, but keep the compact and wide versions clearly related.
- Preserve readable line lengths and avoid layouts that force unnecessary zooming or horizontal movement.

Implementation guidance:
- Build layouts so content can reflow rather than depending on a single viewport size.
- Let templates express repeated page patterns instead of hand-tuning each page.
- Keep layout decisions stable enough that spacing, typography, and components can reuse the same grid rules.
