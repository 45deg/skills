# Elevation

Use elevation to show layering and interaction depth. Most components should stay at level `0`; raise only the surfaces that need to read above surrounding content.

Rules:
- Use subtle shadows for ordinary raised controls and reserve stronger elevation for overlays, dialogs, and other surfaces that must sit on top.
- Define elevation levels system-wide so the same component role always feels like the same layer.
- Do not rely on shadow alone to satisfy contrast or boundary requirements.
- Raised surfaces still need borders or another clear edge when contrast or forced-color behavior makes that necessary.
- If a component rises on hover, make sure the movement does not trigger unwanted layout shift.

Overlay behavior:
- An overlay should sit above existing elevated content.
- Modal overlays should block interaction with the content underneath.
- Overlay shade can reset the effective surface level for content placed above it, so shadows and stacking should be planned relative to the shade, not only the page body.
