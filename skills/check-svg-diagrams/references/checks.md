# SVG Check Reference

## Severity Model

- `error`: A deterministic structural, safety, reference, or explicit-requirement failure.
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

`labels` inventories normalized visible text, stable or generated element keys, font size, anchor, position, and an estimated bounding box.

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

Command-line `--require-label` and `--require-id` values are merged with the JSON requirements. Labels are compared after collapsing whitespace; IDs and edge endpoints are exact.

## False-Positive Handling

- Treat box-label containment as expected, not overlap.
- Allow connectors to touch label bounds at a deliberate port, but investigate a segment that crosses the label interior.
- Check whether repeated text is intentional before calling it a duplicate.
- Distinguish a shape that is deliberately behind another shape from an accidental collision.
- Do not infer a wrong relationship merely from proximity. Use explicit metadata or the source specification.
- A passing static report does not validate visual balance, legibility at the delivery size, or domain semantics.
