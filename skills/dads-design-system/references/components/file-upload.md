# File Upload

Purpose: Let users choose and upload files, with drag-and-drop as an optional aid.

Use when a form or file list needs file selection.

Avoid drag-only upload flows.

Key rules:
- Always provide a standard file picker button.
- Treat drag-and-drop expansion as optional.
- Show file summaries and errors near the control.
- Keep removal or retry actions close to each file.

Accessibility: A single-pointer fallback is required. Do not disable away the only completion route.

Related: `progress-indicator`, `input-text`.
