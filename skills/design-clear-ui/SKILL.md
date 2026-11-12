---
name: design-clear-ui
description: "Design, review, and improve web and app UI to reduce memory, attention, reading, and decision demands. Use for confusing flows, demanding choices, UI copy, feedback, and interruption or recovery. Not for general prose editing or purely decorative changes."
---

# Design Clear UI

Reduce what people must remember, search for, reread, and decide to complete their task. Judge support where it is needed, not by whether a component exists somewhere.

## Establish the task before choosing the UI

Inspect requirements and actual artifacts. Preserve domain rules, explicit constraints, and requested scope. Use the existing design system; ask about a new visual direction unless delegated. A copy edit does not authorize rebuilding state management.

For each decision in the affected flow, identify the target, required facts, available actions and their effects, and the route to continue. Design and verify from these needs, not a list of components. Keep this reasoning out of product copy. Preserve working support when changing existing UI.

When retention is unspecified, preserve work costly to reconstruct across ordinary departure and reopening. Choose the mechanism afterward; optional technology does not make the user need optional. Explicit privacy or product restrictions take precedence. For stateful work, read [continuity.md](references/continuity.md) before choosing storage or recovery behavior.

## Carry those needs through the flow

- **Start and pace:** Make the first useful action reachable before optional setup. Give lengthy work meaningful stopping points and visible scope. Reuse known values and defer unrelated decisions; defaults must not grant consent or make consequential choices for the user.
- **Recognize and decide:** Keep recognizable targets and required reference values available through navigation and narrow layouts. Where actions compete, distinguish what each reads, changes, preserves, or discards at the choice. Offer the action appropriate to the known state; expose alternatives when they serve a real decision, not merely because handlers exist.
- **Find and continue:** For each kind of work needing user attention, make its targets and scoped next action reachable without scanning unrelated content. A summary must lead to the work it describes. Preserve position and focus during updates. On return, restore this route with actual progress or uncertainty; do not force exploration into a sequence.
- **Explain only what is missing:** Compose the state with labels, values, controls, and feedback first. Add prose only for a specific unanswered question about scope, conditions, consequences, or recovery. Keep necessary accessible feedback. If nearby content already answers the question, omit the sentence, including in empty states. Exclude decoration, promotion, and design rationale.
- **Keep control:** Let people revise, leave, continue, and discard deliberately. Acknowledge actions promptly and retain important outcomes beyond transient notices. Protect attention from nonessential interruptions. Honor platform preferences; add adjustments only for unmet needs. Preserve keyboard operation, labels, focus, contrast, non-color cues, reduced motion, zoom, and reflow.

## Verify the same needs in the actual UI

Use [verification.md](references/verification.md) on affected paths through relevant populated, failure, and return states. Check information when the action occurs, including before processing or after interruption.

Correct gaps within scope and recheck. Reviews report findings; proposals describe expected behavior. Report remaining demands and unverified limits. Functional success does not establish understandable use; inspection does not establish measured usability benefits.
