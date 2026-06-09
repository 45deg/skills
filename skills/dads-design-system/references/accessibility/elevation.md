# Elevation

Elevation has accessibility consequences because shadows can disappear or flatten in forced colors and dark themes.

- Do not rely on shadow alone to convey elevated surfaces.
- Plan overlays and modal surfaces for forced-color modes and dark themes from the start, not as an afterthought.
- Give overlay content a border, even when contrast appears sufficient; a border preserves the edge when shadow cues are removed.
- Treat overlay structure as an accessibility concern, not only a visual layer.
- Make sure modal overlays truly prevent interaction with the content beneath them, and keep the dismissal behavior consistent with the rest of the dialog pattern.
