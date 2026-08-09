#!/usr/bin/env python3
"""Inspect standalone SVG diagrams without external dependencies.

The CLI deliberately avoids launching browsers or GUI processes. Geometry for text is
estimated from SVG attributes and Unicode character widths, so overlap findings are
reported as review candidates rather than definitive rendering failures.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence


SCHEMA_VERSION = 1
TOOL_VERSION = "0.1.0"
MAX_SVG_BYTES = 2_097_152
IDENTITY = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
NUMBER_RE = re.compile(r"[-+]?(?:\d+\.?(?:\d*)?|\.\d+)(?:[eE][-+]?\d+)?")
TRANSFORM_RE = re.compile(r"([A-Za-z]+)\s*\(([^)]*)\)")
PATH_TOKEN_RE = re.compile(r"[A-Za-z]|[-+]?(?:\d+\.?(?:\d*)?|\.\d+)(?:[eE][-+]?\d+)?")
REFERENCE_RE = re.compile(r"url\(\s*['\"]?#([^)'\"\s]+)")
EXTERNAL_URL_RE = re.compile(r"(?:https?:|file:|javascript:|data:|//)", re.IGNORECASE)
FORBIDDEN_ELEMENTS = {"script", "foreignObject", "iframe", "object", "embed", "audio", "video"}
NON_RENDERED_ANCESTORS = {"defs", "clipPath", "mask", "marker", "pattern", "symbol"}
SHAPE_TAGS = {"rect", "circle", "ellipse", "polygon", "polyline", "path", "image", "use"}
CONNECTOR_TAGS = {"line", "polyline", "path"}
INHERITED_STYLE_KEYS = {
    "font-size",
    "font-family",
    "font-weight",
    "font-style",
    "text-anchor",
    "visibility",
    "fill",
    "stroke",
    "stroke-width",
    "opacity",
}

Matrix = tuple[float, float, float, float, float, float]
BBox = tuple[float, float, float, float]
Point = tuple[float, float]


class CliError(Exception):
    """An input or runtime error that should produce exit code 2."""


@dataclass
class Record:
    key: str
    element_id: str
    tag: str
    role: str
    group_id: str
    parent_key: str
    bbox: BBox | None
    points: list[Point]
    text: str
    x: float | None
    y: float | None
    font_size: float | None
    text_anchor: str
    line_count: int
    style: dict[str, str]
    attrs: dict[str, str]
    approximate: bool


@dataclass
class SvgDocument:
    path: Path
    data: bytes
    root: ET.Element
    width: float | None
    height: float | None
    view_box: BBox | None
    records: list[Record]


def local_name(name: str) -> str:
    return name.rsplit("}", 1)[-1]


def normalized_text(value: str) -> str:
    return " ".join(value.split())


def first_number(value: str | None, default: float | None = None) -> float | None:
    if value is None:
        return default
    match = NUMBER_RE.search(value)
    if not match:
        return default
    try:
        return float(match.group(0))
    except ValueError:
        return default


def positive_length(value: str | None) -> float | None:
    number = first_number(value)
    return number if number is not None and number > 0 else None


def parse_numbers(value: str | None) -> list[float]:
    return [float(item) for item in NUMBER_RE.findall(value or "")]


def parse_style(value: str | None) -> dict[str, str]:
    result: dict[str, str] = {}
    for declaration in (value or "").split(";"):
        if ":" not in declaration:
            continue
        key, raw = declaration.split(":", 1)
        key = key.strip()
        raw = raw.strip()
        if key and raw:
            result[key] = raw
    return result


def multiply(left: Matrix, right: Matrix) -> Matrix:
    a, b, c, d, e, f = left
    g, h, i, j, k, l = right
    return (
        a * g + c * h,
        b * g + d * h,
        a * i + c * j,
        b * i + d * j,
        a * k + c * l + e,
        b * k + d * l + f,
    )


def apply_matrix(matrix: Matrix, point: Point) -> Point:
    a, b, c, d, e, f = matrix
    x, y = point
    return (a * x + c * y + e, b * x + d * y + f)


def parse_transform(value: str | None) -> Matrix:
    matrix = IDENTITY
    for name, raw_args in TRANSFORM_RE.findall(value or ""):
        args = parse_numbers(raw_args)
        name = name.lower()
        current = IDENTITY
        if name == "matrix" and len(args) == 6:
            current = tuple(args)  # type: ignore[assignment]
        elif name == "translate" and args:
            current = (1.0, 0.0, 0.0, 1.0, args[0], args[1] if len(args) > 1 else 0.0)
        elif name == "scale" and args:
            current = (args[0], 0.0, 0.0, args[1] if len(args) > 1 else args[0], 0.0, 0.0)
        elif name == "rotate" and args:
            angle = math.radians(args[0])
            rotation = (math.cos(angle), math.sin(angle), -math.sin(angle), math.cos(angle), 0.0, 0.0)
            if len(args) >= 3:
                before = (1.0, 0.0, 0.0, 1.0, args[1], args[2])
                after = (1.0, 0.0, 0.0, 1.0, -args[1], -args[2])
                current = multiply(multiply(before, rotation), after)
            else:
                current = rotation
        elif name == "skewx" and args:
            current = (1.0, 0.0, math.tan(math.radians(args[0])), 1.0, 0.0, 0.0)
        elif name == "skewy" and args:
            current = (1.0, math.tan(math.radians(args[0])), 0.0, 1.0, 0.0, 0.0)
        matrix = multiply(matrix, current)
    return matrix


def bbox_from_points(points: Sequence[Point]) -> BBox | None:
    if not points:
        return None
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return (min(xs), min(ys), max(xs), max(ys))


def transform_bbox(bbox: BBox | None, matrix: Matrix) -> BBox | None:
    if bbox is None:
        return None
    x1, y1, x2, y2 = bbox
    return bbox_from_points(
        [
            apply_matrix(matrix, (x1, y1)),
            apply_matrix(matrix, (x2, y1)),
            apply_matrix(matrix, (x2, y2)),
            apply_matrix(matrix, (x1, y2)),
        ]
    )


def bbox_area(bbox: BBox | None) -> float:
    if bbox is None:
        return 0.0
    return max(0.0, bbox[2] - bbox[0]) * max(0.0, bbox[3] - bbox[1])


def bbox_center(bbox: BBox) -> Point:
    return ((bbox[0] + bbox[2]) / 2.0, (bbox[1] + bbox[3]) / 2.0)


def bbox_contains(outer: BBox, inner: BBox, tolerance: float = 0.0) -> bool:
    return (
        inner[0] >= outer[0] - tolerance
        and inner[1] >= outer[1] - tolerance
        and inner[2] <= outer[2] + tolerance
        and inner[3] <= outer[3] + tolerance
    )


def point_in_bbox(point: Point, bbox: BBox, tolerance: float = 0.0) -> bool:
    return (
        bbox[0] - tolerance <= point[0] <= bbox[2] + tolerance
        and bbox[1] - tolerance <= point[1] <= bbox[3] + tolerance
    )


def bbox_intersection(first: BBox, second: BBox, tolerance: float = 0.0) -> BBox | None:
    x1 = max(first[0], second[0])
    y1 = max(first[1], second[1])
    x2 = min(first[2], second[2])
    y2 = min(first[3], second[3])
    if x2 - x1 <= tolerance or y2 - y1 <= tolerance:
        return None
    return (x1, y1, x2, y2)


def bbox_json(bbox: BBox | None) -> list[float] | None:
    return [round(value, 3) for value in bbox] if bbox is not None else None


def parse_points(value: str | None) -> list[Point]:
    numbers = parse_numbers(value)
    return [(numbers[index], numbers[index + 1]) for index in range(0, len(numbers) - 1, 2)]


def parse_path_points(value: str | None) -> list[Point]:
    tokens = PATH_TOKEN_RE.findall(value or "")
    if not tokens:
        return []
    counts = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "A": 7}
    points: list[Point] = []
    current = (0.0, 0.0)
    subpath_start = current
    command = ""
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token.isalpha():
            command = token
            index += 1
            if command.upper() == "Z":
                current = subpath_start
                points.append(current)
                command = ""
                continue
        if not command:
            break
        upper = command.upper()
        count = counts.get(upper)
        if count is None or index + count > len(tokens) or any(item.isalpha() for item in tokens[index : index + count]):
            break
        args = [float(item) for item in tokens[index : index + count]]
        index += count
        relative = command.islower()
        base_x, base_y = current
        if upper in {"M", "L", "T"}:
            x, y = args
            current = (x + base_x, y + base_y) if relative else (x, y)
            if upper == "M":
                subpath_start = current
                command = "l" if relative else "L"
            points.append(current)
        elif upper == "H":
            x = args[0] + base_x if relative else args[0]
            current = (x, base_y)
            points.append(current)
        elif upper == "V":
            y = args[0] + base_y if relative else args[0]
            current = (base_x, y)
            points.append(current)
        elif upper == "C":
            pairs = [(args[0], args[1]), (args[2], args[3]), (args[4], args[5])]
            absolute = [(x + base_x, y + base_y) for x, y in pairs] if relative else pairs
            points.extend(absolute)
            current = absolute[-1]
        elif upper in {"S", "Q"}:
            pairs = [(args[0], args[1]), (args[2], args[3])]
            absolute = [(x + base_x, y + base_y) for x, y in pairs] if relative else pairs
            points.extend(absolute)
            current = absolute[-1]
        elif upper == "A":
            x, y = args[5], args[6]
            current = (x + base_x, y + base_y) if relative else (x, y)
            points.append(current)
    return points


def approximate_text_width(text: str, font_size: float, letter_spacing: float = 0.0) -> float:
    units = 0.0
    for character in text:
        if character.isspace():
            units += 0.33
        elif unicodedata.east_asian_width(character) in {"W", "F", "A"}:
            units += 1.0
        elif character.isalnum():
            units += 0.58
        elif unicodedata.category(character).startswith("P"):
            units += 0.5
        else:
            units += 0.8
    return units * font_size + max(0, len(text) - 1) * letter_spacing


def anchored_x(x: float, width: float, anchor: str) -> float:
    if anchor == "middle":
        return x - width / 2.0
    if anchor == "end":
        return x - width
    return x


def text_geometry(element: ET.Element, style: dict[str, str]) -> tuple[str, float | None, float | None, float, str, int, BBox | None]:
    text = normalized_text("".join(element.itertext()))
    font_size = positive_length(style.get("font-size")) or 16.0
    anchor = style.get("text-anchor", element.attrib.get("text-anchor", "start"))
    x = first_number(element.attrib.get("x"), 0.0)
    y = first_number(element.attrib.get("y"), 0.0)
    tspans = [child for child in element.iter() if child is not element and local_name(child.tag) == "tspan"]
    lines = [normalized_text("".join(child.itertext())) for child in tspans]
    lines = [line for line in lines if line] or ([text] if text else [])
    if not lines or x is None or y is None:
        return text, x, y, font_size, anchor, len(lines), None
    letter_spacing = first_number(style.get("letter-spacing"), 0.0) or 0.0
    line_height = font_size * 1.2
    line_boxes: list[BBox] = []
    current_y = y
    for line_index, line in enumerate(lines):
        tspan = tspans[line_index] if line_index < len(tspans) else None
        line_x = first_number(tspan.attrib.get("x"), x) if tspan is not None else x
        explicit_y = first_number(tspan.attrib.get("y")) if tspan is not None else None
        dy = first_number(tspan.attrib.get("dy"), 0.0) if tspan is not None else 0.0
        if explicit_y is not None:
            current_y = explicit_y
        elif line_index > 0:
            current_y += line_height
        current_y += dy or 0.0
        width = positive_length(tspan.attrib.get("textLength")) if tspan is not None else None
        width = width or approximate_text_width(line, font_size, letter_spacing)
        start_x = anchored_x(line_x or 0.0, width, anchor)
        line_boxes.append((start_x, current_y - font_size, start_x + width, current_y + font_size * 0.22))
    union = bbox_from_points([(box[0], box[1]) for box in line_boxes] + [(box[2], box[3]) for box in line_boxes])
    return text, x, y, font_size, anchor, len(lines), union


def shape_geometry(element: ET.Element, tag: str) -> tuple[BBox | None, list[Point]]:
    if tag == "rect" or tag in {"image", "use"}:
        x = first_number(element.attrib.get("x"), 0.0) or 0.0
        y = first_number(element.attrib.get("y"), 0.0) or 0.0
        width = positive_length(element.attrib.get("width"))
        height = positive_length(element.attrib.get("height"))
        return ((x, y, x + width, y + height), []) if width and height else (None, [])
    if tag == "circle":
        cx = first_number(element.attrib.get("cx"), 0.0) or 0.0
        cy = first_number(element.attrib.get("cy"), 0.0) or 0.0
        radius = positive_length(element.attrib.get("r"))
        return ((cx - radius, cy - radius, cx + radius, cy + radius), []) if radius else (None, [])
    if tag == "ellipse":
        cx = first_number(element.attrib.get("cx"), 0.0) or 0.0
        cy = first_number(element.attrib.get("cy"), 0.0) or 0.0
        rx = positive_length(element.attrib.get("rx"))
        ry = positive_length(element.attrib.get("ry"))
        return ((cx - rx, cy - ry, cx + rx, cy + ry), []) if rx and ry else (None, [])
    if tag == "line":
        points = [
            (first_number(element.attrib.get("x1"), 0.0) or 0.0, first_number(element.attrib.get("y1"), 0.0) or 0.0),
            (first_number(element.attrib.get("x2"), 0.0) or 0.0, first_number(element.attrib.get("y2"), 0.0) or 0.0),
        ]
        return bbox_from_points(points), points
    if tag in {"polyline", "polygon"}:
        points = parse_points(element.attrib.get("points"))
        if tag == "polygon" and points:
            points.append(points[0])
        return bbox_from_points(points), points
    if tag == "path":
        points = parse_path_points(element.attrib.get("d"))
        return bbox_from_points(points), points
    return None, []


def is_visible(style: dict[str, str], hidden_ancestor: bool) -> bool:
    if hidden_ancestor or style.get("display") == "none" or style.get("visibility") in {"hidden", "collapse"}:
        return False
    opacity = first_number(style.get("opacity"), 1.0)
    return opacity is None or opacity > 0


def build_records(root: ET.Element) -> list[Record]:
    records: list[Record] = []
    counter = 0

    def walk(
        element: ET.Element,
        parent_matrix: Matrix,
        inherited_style: dict[str, str],
        parent_key: str,
        group_id: str,
        hidden_ancestor: bool,
        non_rendered_ancestor: bool,
    ) -> None:
        nonlocal counter
        counter += 1
        tag = local_name(element.tag)
        element_id = element.attrib.get("id", "")
        key = element_id or f"{tag}-{counter}"
        next_group_id = element_id if tag == "g" and element_id else group_id
        style = {key: value for key, value in inherited_style.items() if key in INHERITED_STYLE_KEYS}
        style.update(parse_style(element.attrib.get("style")))
        for name in INHERITED_STYLE_KEYS | {"display", "letter-spacing"}:
            if name in element.attrib:
                style[name] = element.attrib[name]
        matrix = multiply(parent_matrix, parse_transform(element.attrib.get("transform")))
        hidden = hidden_ancestor or not is_visible(style, hidden_ancestor)
        non_rendered = non_rendered_ancestor or tag in NON_RENDERED_ANCESTORS
        text = ""
        x: float | None = None
        y: float | None = None
        font_size: float | None = None
        anchor = ""
        line_count = 0
        local_bbox: BBox | None = None
        points: list[Point] = []
        approximate = False
        if not hidden and not non_rendered:
            if tag == "text":
                text, x, y, font_size, anchor, line_count, local_bbox = text_geometry(element, style)
                approximate = True
            else:
                local_bbox, points = shape_geometry(element, tag)
        world_bbox = transform_bbox(local_bbox, matrix)
        world_points = [apply_matrix(matrix, point) for point in points]
        records.append(
            Record(
                key=key,
                element_id=element_id,
                tag=tag,
                role=element.attrib.get("data-role", ""),
                group_id=next_group_id,
                parent_key=parent_key,
                bbox=world_bbox,
                points=world_points,
                text=text,
                x=apply_matrix(matrix, (x, y))[0] if x is not None and y is not None else None,
                y=apply_matrix(matrix, (x, y))[1] if x is not None and y is not None else None,
                font_size=font_size,
                text_anchor=anchor,
                line_count=line_count,
                style=style,
                attrs={local_name(name): value for name, value in element.attrib.items()},
                approximate=approximate,
            )
        )
        for child in element:
            walk(child, matrix, style, key, next_group_id, hidden, non_rendered)

    walk(root, IDENTITY, {}, "", "", False, False)
    return records


def load_document(path: Path) -> SvgDocument:
    if not path.is_file():
        raise CliError(f"SVG file does not exist: {path}")
    data = path.read_bytes()
    if len(data) > MAX_SVG_BYTES:
        raise CliError(f"SVG exceeds the {MAX_SVG_BYTES}-byte inspection limit")
    prefix = data[:4096].decode("utf-8", errors="ignore").lower()
    if "<!doctype" in prefix or "<!entity" in prefix:
        raise CliError("DOCTYPE and ENTITY declarations are not accepted")
    try:
        root = ET.fromstring(data)
    except (ET.ParseError, UnicodeDecodeError) as exc:
        raise CliError(f"invalid SVG/XML: {exc}") from exc
    width = positive_length(root.attrib.get("width"))
    height = positive_length(root.attrib.get("height"))
    values = parse_numbers(root.attrib.get("viewBox"))
    view_box = (values[0], values[1], values[0] + values[2], values[1] + values[3]) if len(values) == 4 and values[2] > 0 and values[3] > 0 else None
    return SvgDocument(path.resolve(), data, root, width, height, view_box, build_records(root))


def load_spec(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise CliError(f"cannot read spec: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise CliError(f"spec is not valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise CliError("spec root must be a JSON object")
    return value


def issue(code: str, message: str, severity: str, **evidence: Any) -> dict[str, Any]:
    result: dict[str, Any] = {"code": code, "severity": severity, "message": message}
    if evidence:
        result["evidence"] = evidence
    return result


def requested_values(args: argparse.Namespace, spec: dict[str, Any], cli_name: str, spec_names: Sequence[str]) -> list[str]:
    result = list(getattr(args, cli_name, []) or [])
    for name in spec_names:
        values = spec.get(name, [])
        if isinstance(values, list):
            result.extend(str(value) for value in values)
    return list(dict.fromkeys(normalized_text(value) for value in result if normalized_text(value)))


def structural_analysis(document: SvgDocument, args: argparse.Namespace, spec: dict[str, Any]) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    root = document.root
    if local_name(root.tag) != "svg":
        errors.append(issue("invalid_root", "Root element must be svg.", "error"))
    width_value = root.attrib.get("width")
    height_value = root.attrib.get("height")
    if width_value is None or height_value is None:
        warnings.append(issue("missing_dimensions", "Add explicit width and height for a predictable standalone viewport.", "warning"))
    elif document.width is None or document.height is None:
        errors.append(issue("invalid_dimensions", "width and height must be positive numeric lengths.", "error"))
    if document.view_box is None:
        errors.append(issue("invalid_viewbox", "viewBox must contain x, y, positive width, and positive height.", "error"))
    ids: set[str] = set()
    duplicates: set[str] = set()
    references: set[str] = set()
    element_counts: dict[str, int] = {}
    for element in root.iter():
        tag = local_name(element.tag)
        element_counts[tag] = element_counts.get(tag, 0) + 1
        if tag in FORBIDDEN_ELEMENTS:
            errors.append(issue("forbidden_element", f"Forbidden element: {tag}.", "error", tag=tag))
        element_id = element.attrib.get("id")
        if element_id:
            if element_id in ids:
                duplicates.add(element_id)
            ids.add(element_id)
        if tag == "style" and element.text and ("@import" in element.text or EXTERNAL_URL_RE.search(element.text)):
            errors.append(issue("external_style", "Style contains an external or data URL.", "error"))
        for raw_name, value in element.attrib.items():
            name = local_name(raw_name)
            if name.lower().startswith("on"):
                errors.append(issue("event_handler", f"Event attribute is forbidden: {name}.", "error", attribute=name))
            if name in {"href", "src"}:
                if value.startswith("#"):
                    references.add(value[1:])
                elif value.strip():
                    errors.append(issue("external_reference", f"Non-local {name} is forbidden.", "error", value=value))
            if EXTERNAL_URL_RE.search(value):
                errors.append(issue("external_url", f"External URL in {name}.", "error", value=value))
            references.update(REFERENCE_RE.findall(value))
    visible_count = sum(1 for record in document.records if record.bbox is not None)
    for element_id in sorted(duplicates):
        errors.append(issue("duplicate_id", f"Duplicate ID: {element_id}.", "error", element_id=element_id))
    for reference in sorted(references - ids):
        errors.append(issue("broken_reference", f"Missing referenced ID: {reference}.", "error", reference=reference))
    if visible_count == 0:
        errors.append(issue("empty_drawing", "No visible SVG elements were found.", "error"))
    top_level = {local_name(child.tag) for child in root}
    if "title" not in top_level:
        warnings.append(issue("missing_title", "Add a top-level title element.", "warning"))
    if "desc" not in top_level:
        warnings.append(issue("missing_desc", "Add a top-level desc element.", "warning"))
    labels = [record.text for record in document.records if record.tag == "text" and record.text]
    required_labels = requested_values(args, spec, "required_label", ("required_labels", "must_include_text"))
    missing_labels = [value for value in required_labels if value not in labels]
    for value in missing_labels:
        errors.append(issue("missing_required_label", f"Missing required label: {value}.", "error", label=value))
    required_ids = requested_values(args, spec, "required_id", ("required_ids",))
    for value in required_ids:
        if value not in ids:
            errors.append(issue("missing_required_id", f"Missing required ID: {value}.", "error", element_id=value))
    return {
        "errors": errors,
        "warnings": warnings,
        "metrics": {
            "bytes": len(document.data),
            "sha256": hashlib.sha256(document.data).hexdigest(),
            "width": document.width,
            "height": document.height,
            "view_box": bbox_json(document.view_box),
            "visible_elements": visible_count,
            "element_counts": element_counts,
            "ids": len(ids),
            "references": len(references),
            "labels": len(labels),
            "missing_required_labels": missing_labels,
        },
    }


def label_rows(document: SvgDocument) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in document.records:
        if record.tag != "text" or not record.text:
            continue
        rows.append(
            {
                "key": record.key,
                "id": record.element_id,
                "text": record.text,
                "x": round(record.x, 3) if record.x is not None else None,
                "y": round(record.y, 3) if record.y is not None else None,
                "bbox": bbox_json(record.bbox),
                "font_size": round(record.font_size, 3) if record.font_size is not None else None,
                "text_anchor": record.text_anchor,
                "line_count": record.line_count,
                "group_id": record.group_id,
                "approximate_bbox": record.approximate,
            }
        )
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["text"]] = counts.get(row["text"], 0) + 1
    for row in rows:
        row["duplicate_text"] = counts[row["text"]] > 1
    return rows


def segment_intersects_bbox(start: Point, end: Point, bbox: BBox) -> bool:
    if point_in_bbox(start, bbox) or point_in_bbox(end, bbox):
        return True

    def orientation(a: Point, b: Point, c: Point) -> float:
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    def intersects(a: Point, b: Point, c: Point, d: Point) -> bool:
        first = orientation(a, b, c)
        second = orientation(a, b, d)
        third = orientation(c, d, a)
        fourth = orientation(c, d, b)
        return first * second <= 0 and third * fourth <= 0

    x1, y1, x2, y2 = bbox
    edges = [((x1, y1), (x2, y1)), ((x2, y1), (x2, y2)), ((x2, y2), (x1, y2)), ((x1, y2), (x1, y1))]
    return any(intersects(start, end, edge_start, edge_end) for edge_start, edge_end in edges)


def connector_records(document: SvgDocument) -> list[Record]:
    result: list[Record] = []
    for record in document.records:
        if record.tag not in CONNECTOR_TAGS or len(record.points) < 2:
            continue
        marker = record.attrs.get("marker-start") or record.attrs.get("marker-end")
        fill = record.style.get("fill", record.attrs.get("fill", ""))
        stroke = record.style.get("stroke", record.attrs.get("stroke", ""))
        if record.tag in {"line", "polyline"} or record.role == "connector" or marker or (stroke and fill in {"", "none"}):
            result.append(record)
    return result


def overlap_analysis(document: SvgDocument, tolerance: float) -> dict[str, Any]:
    labels = [record for record in document.records if record.tag == "text" and record.text and record.bbox]
    shapes = [record for record in document.records if record.tag in SHAPE_TAGS and record.bbox]
    connectors = connector_records(document)
    findings: list[dict[str, Any]] = []
    for index, first in enumerate(labels):
        for second in labels[index + 1 :]:
            intersection = bbox_intersection(first.bbox, second.bbox, tolerance)  # type: ignore[arg-type]
            if intersection:
                findings.append(
                    issue(
                        "label_label_overlap",
                        f"Approximate label boxes overlap: {first.key} and {second.key}.",
                        "warning",
                        elements=[first.key, second.key],
                        overlap_bbox=bbox_json(intersection),
                        overlap_area=round(bbox_area(intersection), 3),
                        approximate=True,
                    )
                )
    if document.view_box:
        for label in labels:
            if not bbox_contains(document.view_box, label.bbox, tolerance):  # type: ignore[arg-type]
                findings.append(
                    issue(
                        "label_outside_viewbox",
                        f"Approximate label box extends outside the viewBox: {label.key}.",
                        "warning",
                        element=label.key,
                        bbox=bbox_json(label.bbox),
                        view_box=bbox_json(document.view_box),
                        approximate=True,
                    )
                )
    for label in labels:
        center = bbox_center(label.bbox)  # type: ignore[arg-type]
        containers = [shape for shape in shapes if point_in_bbox(center, shape.bbox)]  # type: ignore[arg-type]
        if containers:
            container = min(containers, key=lambda item: bbox_area(item.bbox))
            if bbox_area(container.bbox) > bbox_area(label.bbox) and not bbox_contains(container.bbox, label.bbox, tolerance):  # type: ignore[arg-type]
                findings.append(
                    issue(
                        "label_overflow",
                        f"Approximate label box crosses its smallest containing shape: {label.key}.",
                        "warning",
                        elements=[label.key, container.key],
                        label_bbox=bbox_json(label.bbox),
                        container_bbox=bbox_json(container.bbox),
                        approximate=True,
                    )
                )
        for shape in shapes:
            if shape.role not in {"node", "icon"} or point_in_bbox(center, shape.bbox):  # type: ignore[arg-type]
                continue
            intersection = bbox_intersection(label.bbox, shape.bbox, tolerance)  # type: ignore[arg-type]
            if intersection:
                findings.append(
                    issue(
                        "label_shape_overlap",
                        f"Approximate label box overlaps a structured {shape.role}: {label.key} and {shape.key}.",
                        "warning",
                        elements=[label.key, shape.key],
                        overlap_bbox=bbox_json(intersection),
                        approximate=True,
                    )
                )
    for connector in connectors:
        for label in labels:
            if any(segment_intersects_bbox(start, end, label.bbox) for start, end in zip(connector.points, connector.points[1:])):  # type: ignore[arg-type]
                findings.append(
                    issue(
                        "connector_through_label",
                        f"A connector segment crosses the approximate label box: {connector.key} and {label.key}.",
                        "warning",
                        elements=[connector.key, label.key],
                        label_bbox=bbox_json(label.bbox),
                        approximate=True,
                    )
                )
    structured_shapes = [shape for shape in shapes if shape.role in {"node", "icon"}]
    for index, first in enumerate(structured_shapes):
        for second in structured_shapes[index + 1 :]:
            intersection = bbox_intersection(first.bbox, second.bbox, tolerance)  # type: ignore[arg-type]
            if intersection:
                findings.append(
                    issue(
                        "structured_shape_overlap",
                        f"Structured shapes overlap: {first.key} and {second.key}.",
                        "warning",
                        elements=[first.key, second.key],
                        overlap_bbox=bbox_json(intersection),
                        approximate=False,
                    )
                )
    return {
        "findings": findings,
        "metrics": {
            "labels_checked": len(labels),
            "shapes_checked": len(shapes),
            "connectors_checked": len(connectors),
            "finding_count": len(findings),
            "tolerance": tolerance,
        },
        "limitations": [
            "Text boxes are estimates based on font size and Unicode character widths.",
            "CSS classes, font fallback, filters, and exact path curvature are not rendered.",
            "Treat overlap findings as review candidates, not definitive rendering failures.",
        ],
    }


def distance_to_bbox(point: Point, bbox: BBox) -> float:
    dx = max(bbox[0] - point[0], 0.0, point[0] - bbox[2])
    dy = max(bbox[1] - point[1], 0.0, point[1] - bbox[3])
    return math.hypot(dx, dy)


def marker_index(document: SvgDocument) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for element in document.root.iter():
        if local_name(element.tag) != "marker" or not element.attrib.get("id"):
            continue
        marker_id = element.attrib["id"]
        result[marker_id] = {
            "id": marker_id,
            "marker_width": first_number(element.attrib.get("markerWidth"), 3.0),
            "marker_height": first_number(element.attrib.get("markerHeight"), 3.0),
            "marker_units": element.attrib.get("markerUnits", "strokeWidth"),
            "ref_x": first_number(element.attrib.get("refX"), 0.0),
            "ref_y": first_number(element.attrib.get("refY"), 0.0),
            "orient": element.attrib.get("orient", "0"),
        }
    return result


def marker_reference(value: str | None) -> str:
    matches = REFERENCE_RE.findall(value or "")
    return matches[0] if matches else ""


def nearest_shape(point: Point, shapes: list[Record]) -> tuple[str, float]:
    candidates = [(shape.key, distance_to_bbox(point, shape.bbox)) for shape in shapes if shape.bbox]
    return min(candidates, key=lambda item: item[1]) if candidates else ("", math.inf)


def connector_analysis(document: SvgDocument, spec: dict[str, Any], detach_threshold: float) -> dict[str, Any]:
    connectors = connector_records(document)
    view_area = bbox_area(document.view_box)
    shapes = [
        record
        for record in document.records
        if record.tag in SHAPE_TAGS
        and record.bbox
        and (record.role in {"node", "icon"} or (record.element_id and (not view_area or bbox_area(record.bbox) < view_area * 0.5)))
    ]
    markers = marker_index(document)
    rows: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    for connector in connectors:
        start = connector.points[0]
        end = connector.points[-1]
        start_shape, start_distance = nearest_shape(start, shapes)
        end_shape, end_distance = nearest_shape(end, shapes)
        marker_start = marker_reference(connector.attrs.get("marker-start"))
        marker_end = marker_reference(connector.attrs.get("marker-end"))
        row = {
            "key": connector.key,
            "id": connector.element_id,
            "tag": connector.tag,
            "source": connector.attrs.get("data-source", ""),
            "target": connector.attrs.get("data-target", ""),
            "start": [round(value, 3) for value in start],
            "end": [round(value, 3) for value in end],
            "nearest_start_shape": start_shape,
            "start_distance": round(start_distance, 3) if math.isfinite(start_distance) else None,
            "nearest_end_shape": end_shape,
            "end_distance": round(end_distance, 3) if math.isfinite(end_distance) else None,
            "marker_start": marker_start,
            "marker_end": marker_end,
            "stroke_width": first_number(connector.style.get("stroke-width"), 1.0),
        }
        rows.append(row)
        if connector.attrs.get("data-source") and start_distance > detach_threshold:
            findings.append(issue("detached_source", f"Connector source is far from a node: {connector.key}.", "warning", connector=connector.key, distance=round(start_distance, 3)))
        if connector.attrs.get("data-target") and end_distance > detach_threshold:
            findings.append(issue("detached_target", f"Connector target is far from a node: {connector.key}.", "warning", connector=connector.key, distance=round(end_distance, 3)))
        for marker_id in (marker_start, marker_end):
            marker = markers.get(marker_id)
            if not marker:
                continue
            width = marker.get("marker_width") or 0.0
            height = marker.get("marker_height") or 0.0
            if marker.get("marker_units") == "strokeWidth" and max(width, height) > 10:
                findings.append(
                    issue(
                        "marker_scale_risk",
                        f"Marker may render very large relative to stroke width: {marker_id}.",
                        "warning",
                        connector=connector.key,
                        marker=marker,
                    )
                )
    required_edges = spec.get("required_edges", spec.get("edges", []))
    if isinstance(required_edges, list):
        for edge in required_edges:
            if not isinstance(edge, dict):
                continue
            source = str(edge.get("source", ""))
            target = str(edge.get("target", ""))
            candidates = [row for row in rows if row["source"] == source and row["target"] == target]
            if source and target and not candidates:
                findings.append(issue("missing_required_edge", f"Missing structured edge: {source} -> {target}.", "error", source=source, target=target))
                continue
            if edge.get("marker_start") is True and not any(row["marker_start"] for row in candidates):
                findings.append(issue("missing_required_marker_start", f"Structured edge lacks a start marker: {source} -> {target}.", "error", source=source, target=target))
            if edge.get("marker_end") is True and not any(row["marker_end"] for row in candidates):
                findings.append(issue("missing_required_marker_end", f"Structured edge lacks an end marker: {source} -> {target}.", "error", source=source, target=target))
    return {
        "connectors": rows,
        "markers": list(markers.values()),
        "findings": findings,
        "metrics": {"connector_count": len(rows), "marker_count": len(markers), "finding_count": len(findings)},
        "limitations": [
            "Semantic edge validation requires data-source/data-target attributes and a spec.",
            "Curved path routing is approximated from path coordinates rather than rendered pixels.",
        ],
    }


def base_payload(command: str, document: SvgDocument) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "tool_version": TOOL_VERSION,
        "command": command,
        "source": str(document.path),
    }


def validate_payload(document: SvgDocument, args: argparse.Namespace, spec: dict[str, Any]) -> dict[str, Any]:
    analysis = structural_analysis(document, args, spec)
    return {
        **base_payload("validate", document),
        "valid": not analysis["errors"],
        **analysis,
    }


def labels_payload(document: SvgDocument, args: argparse.Namespace, spec: dict[str, Any]) -> dict[str, Any]:
    rows = label_rows(document)
    required = requested_values(args, spec, "required_label", ("required_labels", "must_include_text"))
    missing = [value for value in required if not any(value == row["text"] for row in rows)]
    return {
        **base_payload("labels", document),
        "labels": rows,
        "required_labels": required,
        "missing_required_labels": missing,
        "metrics": {"label_count": len(rows), "duplicate_text_count": sum(1 for row in rows if row["duplicate_text"]), "missing_required_count": len(missing)},
    }


def overlaps_payload(document: SvgDocument, args: argparse.Namespace) -> dict[str, Any]:
    return {**base_payload("overlaps", document), **overlap_analysis(document, args.tolerance)}


def connectors_payload(document: SvgDocument, args: argparse.Namespace, spec: dict[str, Any]) -> dict[str, Any]:
    return {**base_payload("connectors", document), **connector_analysis(document, spec, args.detach_threshold)}


def report_payload(document: SvgDocument, args: argparse.Namespace, spec: dict[str, Any]) -> dict[str, Any]:
    structural = structural_analysis(document, args, spec)
    geometry = overlap_analysis(document, args.tolerance)
    connectors = connector_analysis(document, spec, args.detach_threshold)
    errors = list(structural["errors"]) + [finding for finding in connectors["findings"] if finding["severity"] == "error"]
    warnings = list(structural["warnings"]) + geometry["findings"] + [finding for finding in connectors["findings"] if finding["severity"] != "error"]
    return {
        **base_payload("report", document),
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "labels": label_rows(document),
        "connectors": connectors["connectors"],
        "markers": connectors["markers"],
        "metrics": {
            "structural": structural["metrics"],
            "geometry": geometry["metrics"],
            "connectors": connectors["metrics"],
        },
        "limitations": list(dict.fromkeys(geometry["limitations"] + connectors["limitations"])),
    }


def table(headers: Sequence[str], rows: Iterable[Sequence[Any]]) -> str:
    rendered = [["" if value is None else str(value) for value in row] for row in rows]
    widths = [len(header) for header in headers]
    for row in rendered:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))
    lines = ["  ".join(header.ljust(widths[index]) for index, header in enumerate(headers))]
    lines.append("  ".join("-" * width for width in widths))
    lines.extend("  ".join(value.ljust(widths[index]) for index, value in enumerate(row)) for row in rendered)
    return "\n".join(lines)


def format_bbox(value: Any) -> str:
    return ",".join(str(item) for item in value) if isinstance(value, list) else ""


def emit_table(payload: dict[str, Any]) -> None:
    command = payload["command"]
    if command == "labels":
        print(
            table(
                ("key", "text", "x", "y", "font", "bbox", "group", "duplicate"),
                (
                    (row["key"], row["text"], row["x"], row["y"], row["font_size"], format_bbox(row["bbox"]), row["group_id"], row["duplicate_text"])
                    for row in payload["labels"]
                ),
            )
        )
        if payload["missing_required_labels"]:
            print("\nMissing required labels: " + ", ".join(payload["missing_required_labels"]))
        return
    if command == "overlaps":
        print(
            table(
                ("severity", "code", "elements", "message"),
                ((item["severity"], item["code"], ",".join(item.get("evidence", {}).get("elements", [])), item["message"]) for item in payload["findings"]),
            )
        )
        return
    if command == "connectors":
        print(
            table(
                ("key", "source", "target", "start-near", "end-near", "marker-start", "marker-end"),
                (
                    (row["key"], row["source"], row["target"], row["nearest_start_shape"], row["nearest_end_shape"], row["marker_start"], row["marker_end"])
                    for row in payload["connectors"]
                ),
            )
        )
        if payload["findings"]:
            print("\nFindings")
            print(table(("severity", "code", "message"), ((item["severity"], item["code"], item["message"]) for item in payload["findings"])))
        return
    print(f"valid: {payload.get('valid', True)}")
    if payload.get("errors"):
        print("\nErrors")
        print(table(("code", "message"), ((item["code"], item["message"]) for item in payload["errors"])))
    if payload.get("warnings"):
        print("\nWarnings")
        print(table(("code", "message"), ((item["code"], item["message"]) for item in payload["warnings"])))
    if command == "report":
        print(f"\nlabels: {len(payload['labels'])}")
        print(f"connectors: {len(payload['connectors'])}")


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("svg", type=Path, help="standalone SVG file")
    parser.add_argument("--spec", type=Path, help="optional JSON requirements file")
    parser.add_argument("--required-label", action="append", default=[], help="required visible label; repeat as needed")
    parser.add_argument("--required-id", action="append", default=[], help="required SVG element ID; repeat as needed")
    parser.add_argument("--format", choices=("json", "table"), default="json")
    parser.add_argument("--compact", action="store_true", help="emit compact JSON")


def add_geometry_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--tolerance", type=float, default=0.5, help="minimum overlap in SVG units")


def add_connector_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--detach-threshold", type=float, default=12.0, help="structured connector endpoint warning distance")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect standalone SVG diagrams without external dependencies")
    parser.add_argument("--version", action="version", version=TOOL_VERSION)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (
        ("validate", "validate SVG structure, safety, IDs, references, and required labels"),
        ("labels", "list visible SVG text with approximate geometry"),
        ("overlaps", "list approximate label, shape, connector, and viewBox conflicts"),
        ("connectors", "list connectors, markers, endpoints, and structured edge findings"),
        ("report", "run all checks and emit one report"),
    ):
        subparser = subparsers.add_parser(name, help=help_text)
        add_common_arguments(subparser)
        if name in {"overlaps", "report"}:
            add_geometry_arguments(subparser)
        if name in {"connectors", "report"}:
            add_connector_arguments(subparser)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        document = load_document(args.svg)
        spec = load_spec(args.spec)
        if args.command == "validate":
            payload = validate_payload(document, args, spec)
        elif args.command == "labels":
            payload = labels_payload(document, args, spec)
        elif args.command == "overlaps":
            payload = overlaps_payload(document, args)
        elif args.command == "connectors":
            payload = connectors_payload(document, args, spec)
        else:
            payload = report_payload(document, args, spec)
    except CliError as exc:
        print(json.dumps({"schema_version": SCHEMA_VERSION, "tool_version": TOOL_VERSION, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    if args.format == "table":
        emit_table(payload)
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=None if args.compact else 2, sort_keys=True))
    if payload.get("valid") is False or payload.get("missing_required_labels"):
        return 1
    if any(item.get("severity") == "error" for item in payload.get("findings", [])):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
