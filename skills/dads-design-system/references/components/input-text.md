# Input Text

Purpose: Collect one-line text input.

Use for short values such as a name, phone number, address fragment, code, or identifier.

Avoid multi-line responses, fake fill-in-the-blank sentences, split email parts, and blocked field states.

Key rules:
- Use clear labels and support text.
- Do not rely on placeholders for instructions.
- Avoid unnecessary character-type restrictions.
- Explain errors precisely.
- Do not use `maxlength` as the primary limiter when avoidable.

Accessibility: Avoid disabled/readonly unless unavoidable, do not block copy/paste, do not use live regions for routine validation, and do not trigger unpredictable UI changes from field edits.

Related: `textarea`, `date-picker`, `select`.
