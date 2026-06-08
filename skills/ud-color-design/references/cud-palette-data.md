# CUD Palette Data

Use this file for factual palette data only. Generate all swatches, diagrams, charts, and design examples yourself.

## Groups

- `accent`: high-saturation colors for small marks, text, lines, route colors, signs, chart series, and strong categorical distinctions.
- `base`: lower-to-medium saturation colors for large filled areas such as maps, panels, bands, and area charts.
- `neutral`: white, grays, and black for text, backgrounds, separators, and non-color encodings.
- `alternate`: paint-only alternatives; do not use for web or process print unless the user explicitly requests paint/signage matching.

## Screen RGB

Values are intended for sRGB-style screen use.

| token | Japanese name | group | rgb | hex |
|---|---:|---|---:|---|
| `ud-red` | red | accent | `255,75,0` | `#FF4B00` |
| `ud-yellow` | yellow | accent | `255,241,0` | `#FFF100` |
| `ud-green` | green | accent | `3,175,122` | `#03AF7A` |
| `ud-blue` | blue | accent | `0,90,255` | `#005AFF` |
| `ud-sky` | sky | accent | `77,196,255` | `#4DC4FF` |
| `ud-pink` | pink | accent | `255,128,130` | `#FF8082` |
| `ud-orange` | orange | accent | `246,170,0` | `#F6AA00` |
| `ud-purple` | purple | accent | `153,0,153` | `#990099` |
| `ud-brown` | brown | accent | `128,64,0` | `#804000` |
| `ud-light-pink` | light pink | base | `255,202,191` | `#FFCABF` |
| `ud-cream` | cream | base | `255,255,128` | `#FFFF80` |
| `ud-light-yellow-green` | light yellow green | base | `216,242,85` | `#D8F255` |
| `ud-light-sky` | light sky | base | `191,228,255` | `#BFE4FF` |
| `ud-beige` | beige | base | `255,202,128` | `#FFCA80` |
| `ud-light-green` | light green | base | `119,217,168` | `#77D9A8` |
| `ud-light-purple` | light purple | base | `201,172,230` | `#C9ACE6` |
| `ud-white` | white | neutral | `255,255,255` | `#FFFFFF` |
| `ud-light-gray` | light gray | neutral | `200,200,203` | `#C8C8CB` |
| `ud-gray` | gray | neutral | `132,145,158` | `#84919E` |
| `ud-black` | black | neutral | `0,0,0` | `#000000` |

## Print CMYK

Values are intended for four-color process print. Keep these separate from screen RGB tokens.

| token | Japanese name | group | cmyk |
|---|---:|---|---:|
| `ud-red` | red | accent | `0,75,90,0` |
| `ud-yellow` | yellow | accent | `0,0,100,0` |
| `ud-green` | green | accent | `75,0,65,0` |
| `ud-blue` | blue | accent | `100,45,0,0` |
| `ud-sky` | sky | accent | `55,0,0,0` |
| `ud-pink` | pink | accent | `0,55,35,0` |
| `ud-orange` | orange | accent | `0,45,100,0` |
| `ud-purple` | purple | accent | `30,95,0,0` |
| `ud-brown` | brown | accent | `55,90,100,0` |
| `ud-light-pink` | light pink | base | `0,25,15,0` |
| `ud-cream` | cream | base | `0,0,40,0` |
| `ud-light-yellow-green` | light yellow green | base | `25,0,80,0` |
| `ud-light-sky` | light sky | base | `30,0,0,0` |
| `ud-beige` | beige | base | `0,25,45,0` |
| `ud-light-green` | light green | base | `45,0,45,0` |
| `ud-light-purple` | light purple | base | `25,30,0,0` |
| `ud-white` | white | neutral | `0,0,0,0` |
| `ud-light-gray` | light gray | neutral | `15,10,10,0` |
| `ud-gray` | gray | neutral | `18,10,0,55` |
| `ud-black` | black | neutral | `50,50,50,100` |

## Paint-Only Alternates

These are for paint/signage matching, not default web or DTP use.

| token | Japanese name | group | JPMA | Munsell |
|---|---:|---|---|---|
| `ud-alt-yellow` | alternate yellow | alternate | `J27-90P` | `7.5Y 9/8` |
| `ud-alt-green` | alternate green | alternate | `J45-60L` | `5G 6/6` |

## Practical Starting Sets

- `2 categories`: use hue plus label/shape, for example `ud-blue` and `ud-orange`; avoid relying on hue alone.
- `3-5 small marks`: start with `ud-blue`, `ud-orange`, `ud-green`, `ud-purple`, `ud-sky`, then verify against the actual background and mark size.
- `large filled areas`: start with `ud-light-sky`, `ud-cream`, `ud-light-green`, `ud-light-purple`, `ud-beige`; add boundaries and labels.
- `text`: prefer `ud-black` or sufficiently dark text on light backgrounds; do not use pale base colors as small text.
- `warning/error`: if using red, pair it with words, iconography, or position; red alone is not enough.
