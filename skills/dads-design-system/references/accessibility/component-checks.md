# Component Checks

## General

- Confirm semantic structure, keyboard support, focus order, and visible focus.
- Check contrast for text, icons, controls, and states.
- Keep labels visible and meaningful.
- Avoid relying on placeholder text, color alone, or hidden-only cues.

## Button

- Do not depend on color alone to distinguish button importance.
- Avoid disabled controls when the flow can be redesigned.
- If disabled is unavoidable, explain the state nearby.
- Icon-only buttons need an accessible name.
- Keep focus order aligned with DOM order.
- Use a `44 x 44 CSS px` target size.

## Heading

- Do not skip heading levels.
- Use headings for section structure, not list-like styling.
- Use description lists for repeated term-definition pairs.
- Align injected headings with the surrounding document structure.

## List

- Use semantic lists instead of simulating lists with punctuation or spacing.
- Keep nesting truly nested in markup.
- Keep ordinal text stable and copyable when the number itself is content.

## Table

- Keep tables as simple as possible.
- Split complex groupings into separate tables when that reduces structural burden.
- Prefer one record per row.
- Avoid heavy cell merging when a flatter structure works.

## Carousel

- Avoid carousels unless the use case really needs one.
- Keep slide text short and slide count low.
- Ensure keyboard operation, focus visibility, and status updates.
- Avoid auto-advancing motion and drag-only interaction.

## Input Text

- Use persistent support text instead of placeholder-only instructions.
- Avoid disabled and readonly fields unless truly required.
- Do not use `maxlength` as the primary enforcement mechanism.
- Never block copy or paste.
- Do not split a single value across multiple fields when one works better.
- Do not trigger unexpected page changes or focus jumps on input.
- Do not use live regions for routine validation text.

## Date Picker

- Prefer direct text entry for year, month, and day.
- Use a calendar as an optional aid only when helpful.
- Avoid select-based or native date controls when they create excessive scrolling or awkward navigation.
- Set relevant autocomplete tokens.

## File Upload

- Always provide a file picker button.
- Do not make drag-and-drop the only completion path.
