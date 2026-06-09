# Accessibility

Use this reference to check whether a pattern remains understandable, operable, and robust for keyboard, screen reader, zoom, low-vision, and forced-color use.

Baseline checks:
- Prefer semantic HTML and visible labels over decorative or implicit cues.
- Keep DOM order, reading order, and focus order aligned unless there is a strong reason not to.
- Do not rely on color, placeholder text, hidden text, or spatial arrangement alone.
- Ensure interactive controls have enough target size, clear names, and visible focus.
- Verify contrast, text scaling, and forced-color behavior before shipping.
- Check component-specific constraints before applying custom styling or behavior.
- Treat accessibility as a design and implementation requirement, not a post-processing step.
- When a pattern changes how content is announced, focused, or dismissed, test the behavior directly instead of assuming the visual design is enough.
