# Visual Rendering Routes

Choose a route after validating the SVG. Keep rendering orchestration in the Coding Agent workflow rather than adding renderer discovery, subprocess execution, or image generation to `svg_check.py`.

## Discover Candidates

Inspect the current session's tool and skill catalog for native image viewing, browser control, computer use, or artifact rendering. When shell access is available, use normal executable discovery such as `command -v` for plausible local renderers. Adapt the search to the environment instead of maintaining a required tool list in the Skill or Python CLI.

Prefer an already available option. Do not assume that command presence proves compatibility with the target SVG, and do not install packages or browser binaries unless the user authorizes it.

## Choose a Route

| Route | Good fit | Main limitation |
| --- | --- | --- |
| `rsvg-convert` | Headless rasterization with Cairo, Pango, and font shaping | Browser-specific CSS and scripting are not reproduced. |
| Inkscape CLI | Complex authored SVG and Inkscape features | May be unavailable or slower. |
| `resvg` or `svgexport` | Fast deterministic conversion | Feature and font support depend on the installed build. |
| ImageMagick | Convenient conversion and image inspection | Its SVG delegate varies; font-family lists can fail. |
| Browser tools | Browser CSS, fonts, filters, and final viewport behavior | Requires stronger permissions and careful isolation. |
| Session-native viewer | Direct visual inspection with minimal setup | Export dimensions and renderer details may be less controllable. |

Do not enforce this table as a fixed priority. Choose based on availability, SVG features, security constraints, output size, and whether browser fidelity matters.

## Probe the Actual SVG

Render to a new PNG and verify its dimensions and readability. Examples:

```bash
rsvg-convert --background-color white --width 1200 --keep-aspect-ratio \
  --output diagram.png diagram.svg

inkscape diagram.svg --export-filename=diagram.png --export-width=1200

svgexport diagram.svg diagram.png 2x

magick -background white -density 144 diagram.svg diagram.png
```

For `resvg`, browser CLIs, and version-sensitive tools, read the installed command's help instead of guessing flags. If ImageMagick reports a font or delegate error, switch to `rsvg-convert`, Inkscape, or a browser rather than rewriting the SVG merely to satisfy that renderer.

## Use a Browser Safely

Use a browser when CSS layout, web fonts, filters, clipping, animation state, or viewport behavior makes a native rasterizer insufficient.

- Validate the SVG first and reject scripts, event handlers, and external URLs.
- Use an isolated temporary session without a personal profile, cookies, credentials, extensions, or restored state.
- Restrict or disable network access when the browser tool supports it.
- Use an absolute local path or a minimal local HTML wrapper. Avoid serving unrelated workspace files.
- Set an explicit viewport and device scale before taking the screenshot.
- Close the session after capturing the image.

For an installed `agent-browser`, consult its version-matched core skill with `agent-browser skills get core --full`. A typical local sequence is conceptually: open the absolute `file://` URL in an isolated session, set the viewport, take a PNG screenshot, and close that session. Follow the installed version's exact syntax and the current environment's approval rules.

Treat `browser-use`, Playwright, an in-app browser, and computer-use capabilities the same way: use their own current instructions, keep the session isolated, and avoid remote providers for sensitive local SVGs unless the user explicitly chooses one.

## Inspect the Render

Inspect at both the intended delivery size and a zoomed view. Check:

- label collisions, clipping, truncation, line breaks, and unreadably small text;
- repeated-row and column alignment, spacing, and baseline consistency;
- connector routing through labels or nodes, arrow direction, and marker scale;
- content touching the `viewBox` edge or disappearing under a mask or clip path;
- contrast, color-only distinctions, and behavior on the intended background;
- missing fonts, images, filters, markers, or symbols that indicate renderer failure.

Render before and after an edit with the same tool, dimensions, background, and viewport. Use a second renderer only when the first output is suspect or browser fidelity is material. Record the renderer, version when relevant, output dimensions, and any limitation in the review result.
