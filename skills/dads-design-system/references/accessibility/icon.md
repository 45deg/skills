# Icon

Icons are often ambiguous on their own, so the safest default is to pair them with visible text.

- Pair icons with visible text labels whenever possible.
- If an icon accompanies a label, keep it decorative in the accessibility tree by avoiding a competing accessible name.
- If an icon and label form one link or button, keep both inside one interactive element so the hit area and accessibility tree stay unified.
- If an icon must stand alone, give it an accessible name that replaces the missing label and use at least a `44 x 44 CSS px` hit area.
- Use `alt=""` for decorative `<img>` icons, and avoid adding `aria-label` to purely decorative background or list-mark icons.
- Keep icon contrast at `4.5:1` when it may function like text, and never below `3:1` for non-text UI that is clearly not text-like.
