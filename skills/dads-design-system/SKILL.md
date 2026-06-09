---
name: dads-design-system
description: Apply the Digital Agency Design System design foundations, accessibility rules, and component decision guidance. Use when designing, reviewing, or implementing Japanese government-style web UI, choosing DADS components, checking color, typography, layout, spacing, icon, link, elevation, form, navigation, content, feedback, or data-display patterns, or auditing UI against DADS-oriented accessibility constraints.
license: Digital Agency Design System content is governed by the official usage notice and Digital Agency copyright policy; this skill is an edited/distilled derivative and is not official.
compatibility: Requires only Markdown reading. No network or scripts required.
---

# DADS Design System

Use this skill to make design, implementation, and review decisions using a distilled DADS-oriented reference set.

## Read Order

1. Start with `references/foundations/index.md`.
2. For visual and structural decisions, read the relevant `references/foundations/*.md` file before component files.
3. For accessibility review or risk checks, read `references/accessibility/index.md` and the relevant accessibility file.
4. For concrete UI parts, read `references/components/index.md`, then the matching component file.

## Reference Routing

- Color, state, contrast, severity, chart color: read `references/foundations/color.md`, `references/foundations/color-palette.md`, then `references/accessibility/color.md`.
- Typography, body text, heading rhythm, line length, dense content: read `references/foundations/typography.md`, `references/foundations/typography-text-style.md`, then `references/accessibility/typography.md`.
- Page structure, responsive behavior, grid, alignment: read `references/foundations/layout.md`, then `references/accessibility/layout.md`.
- Spacing, grouping, scan rhythm, touch spacing: read `references/foundations/spacing.md`, then `references/accessibility/spacing.md`.
- Icons, link labels, elevation, corner shape, surface cues: read the matching file in `references/foundations/`, then the matching file in `references/accessibility/` when it affects operation or meaning.
- Forms, navigation, feedback, data display, or content components: read `references/components/index.md`, choose the component file, then check `references/accessibility/component-checks.md`.

## Operating Rules

- Treat foundations as the canonical design layer.
- Treat accessibility files as constraints and review checks.
- Treat component files as applied patterns, not as replacements for foundations.
- Prefer the simplest component that satisfies the task.
- Preserve component status notes such as deprecated, pending guidance, or sparse guidance.
- Do not copy external wording into user output. Use the distilled rules here to produce fresh guidance.
- When publishing or reusing DADS-derived content, cite the Digital Agency Design System source, state that this material was edited/distilled, and do not imply Digital Agency authorship or endorsement.

## When Unsure

- Read `references/foundations/color.md`, `references/foundations/typography.md`, and `references/foundations/spacing.md` for general visual decisions.
- Read `references/accessibility/component-checks.md` for implementation review.
- Compare related component files before choosing: button vs link, radio vs checkbox vs select, accordion vs disclosure, card vs table, notification banner vs emergency banner, drawer vs dialog.
