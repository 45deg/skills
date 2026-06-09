# Color

- Meet `4.5:1` for text against its background; do not depend on a large-text exception.
- Meet `3:1` for non-text UI, icons, controls, and focus indicators.
- Set both foreground and background colors explicitly, especially for surfaces that are not plain white or black.
- Do not use color as the only way to distinguish state, severity, or importance.
- If a brand color fails contrast, adjust its lightness or reserve it for decorative branding use.
- For charts, diagrams, and image-like content, add nearby text or a full text alternative so meaning survives without color.
- Design palettes for color-vision differences and low-color contexts.
- Treat link and visited-link colors as functional signals, not decoration.
- Validate semantic colors on every background they can appear on; a token that works on white may fail on tinted surfaces.
