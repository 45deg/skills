# SVG Check Reference

## Severity Model

- `error`: A structural, safety, reference, or explicit-requirement failure according to the static model. Rendering-dependent requirement checks can produce false positives or miss defects; reconcile them as described below.
- `warning`: A likely geometry or connector problem that normally requires rendered confirmation.
- `info`: Inventory data or a non-blocking observation.

Exit code `0` means no errors, `1` means at least one error, and `2` means the input could not be parsed or inspected. Warnings intentionally leave the exit code at `0`.

## Static Checks

`validate` checks:

- XML parsing and an SVG root element;
- `<script>`, inline event handlers, and external or script-like links;
- positive width and height when numeric values are present;
- a valid, positive `viewBox`;
- duplicate IDs and unresolved local fragment references;
- empty `<text>` elements;
- title and description availability;
- explicit required labels and IDs.

`labels` inventories normalized text considered visible by the static model, stable or generated element keys, font size, anchor, position, and an estimated bounding box.

`connectors` inventories line-like elements, marker references, endpoints, and optional structured relationships.

## Approximate Geometry

The CLI parses basic coordinates and common transforms, then estimates text width from Unicode character classes and `font-size`. It does not load fonts, perform browser layout, execute CSS, expand `<use>` geometry, or calculate arbitrary path bounds.

Treat these checks as candidate generators:

- label-to-label intersection;
- label overflow outside a containing shape;
- labels outside the `viewBox`;
- connector segments passing through label bounds;
- intersections between structured shapes that declare `data-role`.

Transforms, nested coordinate systems, CSS typography, path-following text, filters, masks, and clipping paths can make estimates inaccurate. Confirm material warnings in a renderer before editing.

## Structured Connectors

For semantic edge checks, annotate connectors with stable source and target keys:

```xml
<path id="approve-edge"
      data-role="connector"
      data-source="review"
      data-target="approved"
      marker-end="url(#arrow)"
      d="M 100 80 L 220 80" />
```

The CLI can then compare the edge with a requirement specification. Without this metadata, it can inspect endpoints and markers but cannot reliably infer which nodes the edge connects.

## Requirement Specification

Pass a JSON object with any of these arrays:

```json
{
  "required_labels": ["Review", "Approved"],
  "required_ids": ["review", "approved", "approve-edge"],
  "required_edges": [
    {"source": "review", "target": "approved", "marker_end": true}
  ]
}
```

Command-line `--required-label` and `--required-id` values are merged with the JSON requirements. Labels are compared after collapsing whitespace; IDs and edge endpoints are exact.

Pass the requirement object for the current SVG, not an entire multi-case catalog. Requirements outside this schema, such as mandatory top-level title/description elements, must be checked separately. A zero exit code does not establish that those requirements were met.

## False-Positive Handling

- Treat box-label containment as expected, not overlap.
- Allow connectors to touch label bounds at a deliberate port, but investigate a segment that crosses the label interior.
- Check whether repeated text is intentional before calling it a duplicate.
- Distinguish a shape that is deliberately behind another shape from an accidental collision.
- Do not infer a wrong relationship merely from proximity. Use explicit metadata or the source specification.
- A passing static report does not validate visual balance, legibility at the delivery size, or domain semantics.

## Reconcile Rendering-Dependent Requirements

The inventory is not the rendered accessibility or display tree. Stylesheet selectors are not applied, inline/presentation style precedence is incomplete, and reusable `<use>` instances are not expanded. Masks, clipping, and later paint can hide text that is still inventoried. These limits affect required-label errors as well as geometry warnings.

For affected content, trace the visible instance back to its source, check CSS precedence and paint order where relevant, and compare exact required text with the render. A visible label rendered through a local `<use>` can satisfy the requirement even if the CLI calls it missing; a covered or CSS-hidden label cannot satisfy a visibility requirement merely because the CLI lists it. Do not duplicate visible labels or rewrite working reuse/CSS to silence the checker. Report the checker limitation separately, and state uncertainty if no reliable render is available. Safety errors still require resolution or isolation before rendering.
