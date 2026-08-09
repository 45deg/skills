# SVG Review Heuristics

Build the review around the current artifact, its intended use, and explicit requirements. Do not assume a universal defect ranking from a prior review set.

## Establish the Review Context

Determine what the SVG represents, where it will be displayed, its intended dimensions and background, and which content or relationships must be preserved. Note whether the artifact depends on interaction, animation, external fonts, or browser-specific rendering.

Adapt the depth of inspection to the artifact. A small icon, a dense architecture diagram, a chart, and a map need different emphases.

## Select Relevant Passes

Use the passes that fit the SVG rather than treating this as a mandatory fixed sequence.

### Integrity and Safety

- Check parsing, dimensions, `viewBox`, IDs, references, and unsupported or unsafe markup.
- Confirm that required resources are embedded or intentionally external.
- Distinguish an invalid SVG from a renderer-specific failure.

### Content and Semantics

- Compare visible labels, values, symbols, and relationships with the source requirements.
- Verify connector direction, grouping, hierarchy, ordering, and legends where they carry meaning.
- Do not infer missing content or a wrong relationship from geometry alone.

### Typography and Labels

- Inspect collisions, truncation, wrapping, baseline consistency, and readability at the delivery size.
- Check font fallback and shaping when the output contains non-Latin text or specialized symbols.
- Treat estimated text bounds as candidates for visual confirmation.

### Geometry and Composition

- Compare alignment and spacing across repeated structures.
- Inspect transformed or nested elements near boundaries, masks, and clipping paths.
- Decide whether overlap and containment are intentional before reporting them.

### Connectors and Markers

- Check routes through labels or nodes, detached endpoints, arrow direction, and marker scale.
- Use stable IDs or structured source/target metadata when available.
- Confirm ambiguous relationships against the specification or user intent.

### Rendering and Accessibility

- Inspect the intended background, scale, viewport, and color scheme.
- Check contrast, color-only distinctions, small text, and missing visual resources.
- Try another renderer when fonts, filters, masks, markers, or symbols look suspicious.

## Require Appropriate Evidence

Classify findings by evidence instead of by a fixed category priority:

- Treat invalid markup, unresolved references, and explicit requirement failures as deterministic.
- Treat estimated geometry and renderer-dependent behavior as provisional until visually confirmed.
- Treat domain meaning as uncertain until supported by requirements, metadata, or user intent.

Report only actionable defects. A tight gap, touching endpoint, repeated label, unconventional layout, or deliberate overlap is not automatically wrong. When evidence remains ambiguous, describe the uncertainty and the check needed to resolve it.
