# UD Color Design Rules

Use these rules to transform a design.

## Information Design

- Treat color as one channel, never the only channel.
- Add direct labels to routes, slices, bars, data series, warnings, and map regions whenever space allows.
- For legends, keep label names near marks or repeat labels at endpoints; distant legends increase color-matching effort.
- Combine hue with at least one redundant cue: shape, icon, pattern, line dash, line width, border, fill texture, position, or explicit text.
- For print, avoid very thin colored strokes; low ink coverage and paper texture can erase distinctions.
- For UI state, pair color with text such as `Error`, `Selected`, `Required`, or `Unavailable`.

## Palette Selection

- Use accent colors for small/high-signal elements and base colors for large areas.
- Avoid mixing many accent colors with many base colors in the same legend unless grouping and labels make the logic obvious.
- Prefer fewer categories over a rainbow palette; split a complex chart into facets if category count becomes high.
- Keep neutral colors available for hierarchy, background, gridlines, disabled states, and text.
- When categories have semantic names, keep names visible.

## Known Risk Patterns

- Red/green, pink/sky, green/gray, purple/gray, and red/brown distinctions can fail depending on size, lighting, medium, and observer.
- Similar light base colors can blur together in large fills unless separated by borders, labels, or patterns.
- Pale base colors are poor for small text, fine strokes, tiny icons, and low-resolution screens.
- Yellow and cream require dark text or outlines when used as backgrounds.
- White, light gray, and pale colors need borders when adjacent to white page backgrounds.

## Web Checklist

- Define palette tokens and apply them consistently.
- Run the project's accessibility, lint, visual regression, or screenshot checks when available.
- Check normal, hover, active, selected, disabled, success, warning, and error states.
- Verify high-density charts at actual display size, not only enlarged previews.
- If using CSS, include non-color affordances such as `text-decoration`, `border-style`, `font-weight`, `aria-label`, visible text, or icons.

## DTP Checklist

- Use CMYK values for process print workflows unless a printer or brand workflow says otherwise.
- Ask for printer profile, paper stock, proofing constraints, and spot-color needs when production accuracy matters.
- Keep route maps and signs readable in grayscale by adding route numbers, symbols, line styles, and station labels.
- Check overprint, transparency, rich black, and knockout behavior before final PDF export.
- Export a proof PDF and inspect whether labels, borders, and patterns survive at final size.

## Output Patterns

CSS custom properties:

```css
:root {
  --ud-red: #FF4B00;
  --ud-blue: #005AFF;
  --ud-sky: #4DC4FF;
  --ud-green: #03AF7A;
  --ud-orange: #F6AA00;
  --ud-purple: #990099;
  --ud-black: #000000;
  --ud-white: #FFFFFF;
}
```

DTP swatch naming:

```text
UD Red / CUD process / C0 M75 Y90 K0
UD Blue / CUD process / C100 M45 Y0 K0
UD Light Sky / CUD process / C30 M0 Y0 K0
```

Chart encoding:

```text
Series A: ud-blue, solid line, circle marker, endpoint label
Series B: ud-orange, dashed line, square marker, endpoint label
Series C: ud-green, dotted line, triangle marker, endpoint label
```
