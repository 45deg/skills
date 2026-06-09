# Spacing

Spacing is a structural tool. Use it to separate groups, preserve rhythm, and make relationships obvious without adding extra decoration.

Core rules:
- Prefer a small, named spacing scale instead of one-off values.
- `8 CSS px` is a practical base unit when the system does not already define one.
- Three to five primary spacing steps are usually enough for a whole design system.
- Use padding for internal breathing room.
- Use margin or layout gap for external separation between elements, groups, and columns.

How spacing communicates:
- Small gaps suggest tight association or dependency.
- Larger gaps signal a section break or a weaker relationship.
- Repeated spacing patterns make templates feel stable and easier to scan.
- Spacing can support hierarchy, but it should reinforce the structure rather than carry it alone.

Implementation guidance:
- Apply the same spacing tokens to the same kinds of components.
- Let spacing scale with the layout when content moves between compact and wide views.
- Watch for CSS behavior such as vertical margin collapse.
- Avoid tuning layout with ad hoc pixel values unless the component truly needs an exception.
