---
name: ud-color-design
description: Apply Color Universal Design and UD color principles to web UI, charts, slides, print layouts, signs, maps, and DTP files. Use when asked to make colors easier to distinguish for diverse color vision, apply CUD/UD colors, create accessible palettes, revise diagrams that rely on color, choose RGB/CMYK values for screen or print, or audit visual information design for color-only communication risks.
license: MIT
metadata:
  author: zkr
  version: "1.0.0"
---

# Apply UD Color Design

## Workflow

1. Identify the medium: `web/screen`, `DTP/print`, `slides`, `signage`, `maps`, or `charts`.
2. Read `references/cud-palette-data.md` for RGB/CMYK values and palette groups.
3. Read `references/cud-combination-guidance.md` for starter sets and hard-to-distinguish pairs.
4. Read `references/ud-color-design-rules.md` for labels, redundant cues, contrast, legends, and export checks.
5. Preserve the design intent, but do not rely on color alone. Add labels, icons, patterns, line styles, borders, shapes, ordering, or annotations.
6. Deliver the artifact the user needs: file edits, CSS variables, design tokens, chart palettes, SVG styles, slide notes, or DTP swatch values.

## Medium Defaults

For web/screen:

- Use `screen-rgb` values.
- Define named tokens such as `--ud-red`, `--ud-blue`, and `--ud-light-sky`.
- Check text/background contrast separately; distinguishable palette colors are not automatically readable text colors.
- Pair UI state color with visible text, icons, borders, underline, position, or motion.

For DTP/print:

- Use `print-cmyk` values for process color workflows.
- Keep RGB and CMYK palettes separate unless the project has a conversion workflow.
- Use base colors for broad fills and accent colors for small/high-signal marks.
- Proof final-size output when production accuracy matters.

For charts/maps/infographics:

- Start with the smallest candidate set that covers the categories.
- Prefer direct labels over distant legends.
- Add dash styles, marker shapes, boundaries, patterns, or endpoint labels.
- Split or facet complex visuals before adding too many hues.

## Output Notes

- Mention whether the output used `screen-rgb`, `print-cmyk`, or both.
- Note residual risks when the design still depends heavily on color, has many categories, uses tiny marks, or needs production proofing.
