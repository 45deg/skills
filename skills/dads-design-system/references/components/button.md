# Button

Purpose: Trigger actions or page transitions.

Use when the user must submit, confirm, cancel, navigate, continue, or run an operation.

Avoid when a plain link is the right semantic element, when multiple primary actions compete, or when a disabled button would become the main workflow gate.

Key rules:
- Use one primary action per screen or local decision context.
- Keep secondary actions limited.
- Use tertiary style for cancellation, stop, or low-emphasis actions.
- Target area should be at least `44 x 44 CSS px`.
- Visual hierarchy must not depend on color alone.

Accessibility: Label icon-only buttons, keep DOM and focus order aligned, avoid `disabled` when the flow can explain next steps instead.

Related: `dialog`, `notification-banner`, `emergency-banner`, `header-container`.
