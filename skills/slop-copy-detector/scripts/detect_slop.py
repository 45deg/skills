#!/usr/bin/env python3
"""Measure punctuation, length, and exact repetition in Japanese copy batches."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

# Keep only stops followed by text outside balanced brackets.
BRACKETS = dict(zip("「『（(【［[〈《“‘", "」』）)】］]〉》”’"))
INTERNAL_PERIOD_RE = re.compile(r"。[^\w。]*[^\W_]")
TAG_LABELS = {
    "P1_COMMA_PERIOD": "P1 読点があり、句点で終わる",
    "P2_TWO_BEAT_SLOGAN": "P2 18字以内で読点が1つ",
    "P3_MULTI_SENTENCE": "P3 括弧の外に文中句点",
    "P4_DRAMATIC_COMMA_NO_PERIOD": "P4 24字以内で読点が1つ、句点なし",
}


@dataclass
class CopyItem:
    file: str
    theme: str
    brief: str
    condition: str
    index: int | None
    text: str
    tags: list[str] = field(default_factory=list)
    source_line: int | None = None
    input_id: str | int | None = None
    batch_id: int | None = None
    tag_spans: dict[str, list[tuple[int, int]]] = field(default_factory=dict)



def parse_source(lines: list[str], source_name: str, cli_brief: str = "") -> list[CopyItem]:
    """Read independent lines and numbered runs, with optional section metadata."""
    has_section = any(line.lstrip().startswith("■ ") for line in lines)
    items: list[CopyItem] = []
    has_list = any(re.match(r"^(?:\d+\.|[-*])\s+\S", line.strip()) for line in lines)
    theme = "(default)" if has_section or has_list else "(plain)"
    condition = theme
    brief = cli_brief
    in_section = not has_section
    expect_brief = False
    previous_index: int | None = None
    batch_id = 0

    for source_line, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("■ "):
            theme = line[2:].strip()
            style = re.fullmatch(r"(.*?)[（(]([^）)]+)[）)]", theme)
            condition = "(default)"
            if style:
                theme, condition = (part.strip() for part in style.groups())
            brief = cli_brief
            in_section = True
            expect_brief = True
            previous_index = None
            continue

        if not in_section:
            # Everything before the first section belongs to the file preamble.
            continue

        if line.startswith("【") and line.endswith("】") and len(line) <= 30 and has_section:
            condition = line[1:-1].strip()
            expect_brief = False
            previous_index = None
            continue

        numbered = re.fullmatch(r"(\d+)\.\s+(\S.*)", line)
        bullet = re.fullmatch(r"[-*]\s+(\S.*)", line)
        if expect_brief and not (numbered or bullet):
            brief = cli_brief or line
            expect_brief = False
            continue

        index = int(numbered[1]) if numbered else None
        if index is not None and (previous_index is None or index <= previous_index):
            batch_id += 1
        previous_index = index
        copy = numbered[2] if numbered else bullet[1] if bullet else line
        items.append(
            CopyItem(
                file=source_name,
                theme=theme,
                brief=brief,
                condition=condition,
                index=index,
                text=copy,
                source_line=source_line,
                batch_id=batch_id if index is not None else None,
            )
        )
        expect_brief = False

    return items


def parse_jsonl(lines: list[str], source_name: str, cli_brief: str = "") -> list[CopyItem]:
    """Load independent examples from JSON Lines without creating numbered batches."""
    items: list[CopyItem] = []
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        location = f"{source_name}:{line_number}"
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValueError(f"{location}: {error.msg}") from error

        if not isinstance(record, dict):
            raise ValueError(f"{location}: expected an object")
        input_id = record.get("id")
        if input_id is not None and not (
            type(input_id) is int or isinstance(input_id, str) and input_id.strip()
        ):
            raise ValueError(f"{location}: 'id' must be a nonempty string or integer")
        copy = record.get("copy")
        if not isinstance(copy, str) or not copy.strip():
            raise ValueError(f"{location}: 'copy' must be a nonempty string")
        for key in ("field", "placement", "brief"):
            if record.get(key) is not None and not isinstance(record[key], str):
                raise ValueError(f"{location}: '{key}' must be a string")

        items.append(
            CopyItem(
                file=source_name,
                theme=record.get("field") or "(default)",
                brief=record.get("brief") or cli_brief,
                condition=record.get("placement") or "(default)",
                index=None,
                text=" ".join(copy.strip().splitlines()),
                source_line=line_number,
                input_id=input_id,
            )
        )
    return items


def _is_two_beat_slogan(text: str) -> bool:
    if len(text) > 18 or "。" in text[:-1] or text.count("、") != 1:
        return False
    left, right = [p.strip() for p in text.rstrip("。").split("、", 1)]
    return bool(left and right and len(left) <= 10 and len(right) <= 10)


def _is_short_comma_no_period(text: str) -> bool:
    if len(text) > 24 or "。" in text or text.count("、") != 1:
        return False
    left, right = (part.strip() for part in text.split("、"))
    return bool(left and right and len(left) <= 12 and len(right) <= 12)


def _unquoted_text(text: str) -> str:
    """Mask balanced brackets while retaining character offsets."""
    result = list(text)
    stack: list[tuple[str, int]] = []
    for index, char in enumerate(text):
        if char in BRACKETS:
            stack.append((BRACKETS[char], index))
        elif stack and char == stack[-1][0]:
            _, start = stack.pop()
            if not stack:
                result[start:index + 1] = " " * (index + 1 - start)
    return "".join(result)


def detect_item_tags(item: CopyItem) -> None:
    text = item.text
    unquoted = _unquoted_text(text)
    periods = [
        match.start()
        for match in INTERNAL_PERIOD_RE.finditer(text)
        if unquoted[match.start()] == "。"
    ]
    commas = [(index, index + 1) for index, char in enumerate(text) if char == "、"]
    spans: dict[str, list[tuple[int, int]]] = {}

    if commas and text.endswith("。"):
        spans["P1_COMMA_PERIOD"] = [*commas, (len(text) - 1, len(text))]
    if _is_two_beat_slogan(text):
        spans["P2_TWO_BEAT_SLOGAN"] = commas
    if periods:
        spans["P3_MULTI_SENTENCE"] = [(index, index + 1) for index in periods]
    if _is_short_comma_no_period(text):
        spans["P4_DRAMATIC_COMMA_NO_PERIOD"] = commas

    item.tags = list(spans)
    item.tag_spans = spans


def analyze_batch(items: list[CopyItem]) -> dict:
    for item in items:
        detect_item_tags(item)

    total = len(items)
    if total == 0:
        return {"total": 0}

    avg_len = sum(len(x.text) for x in items) / total
    avg_tags = sum(len(x.tags) for x in items) / total
    clean_count = sum(1 for x in items if not x.tags)

    tag_counts = Counter()
    tag_examples: dict[str, list[dict]] = defaultdict(list)
    for x in items:
        for t in x.tags:
            tag_counts[t] += 1
            if len(tag_examples[t]) < 20:
                tag_examples[t].append(
                    {"text": x.text, "theme": x.theme, "condition": x.condition, "file": x.file}
                )

    # Numbered groups with at least three candidates.
    groups: dict[tuple[str, int], list[CopyItem]] = defaultdict(list)
    for x in items:
        if x.batch_id is not None:
            groups[(x.file, x.batch_id)].append(x)

    valid_groups = [group for group in groups.values() if len(group) >= 3]
    monotonic_groups = 0
    min_max_groups = 0
    idx_lengths: dict[int, list[int]] = defaultdict(list)

    first_lens: list[int] = []
    last_lens: list[int] = []

    for grp in valid_groups:
        lens = [len(i.text) for i in grp]
        first_lens.append(lens[0])
        last_lens.append(lens[-1])
        if all(lens[j] <= lens[j + 1] for j in range(len(lens) - 1)):
            monotonic_groups += 1
        if lens[0] == min(lens) and lens[-1] == max(lens):
            min_max_groups += 1
        for pos, item in enumerate(grp, start=1):
            idx_lengths[item.index or pos].append(len(item.text))

    # Check exact copies and copies differing only in final periods.
    exact_counter = Counter(x.text for x in items)
    exact_dups = [
        {
            "text": txt,
            "count": cnt,
            "locations": [f"{Path(x.file).name}:{x.theme}/{x.condition}" for x in items if x.text == txt],
        }
        for txt, cnt in exact_counter.most_common()
        if cnt >= 2
    ]

    norm_counter = Counter(x.text.rstrip("。") for x in items)
    norm_dups = [
        {"text": txt, "count": cnt}
        for txt, cnt in norm_counter.most_common()
        if cnt >= 2
    ]

    # Per-condition breakdown
    cond_groups: dict[str, list[CopyItem]] = defaultdict(list)
    for x in items:
        cond_groups[x.condition].append(x)

    by_condition = {}
    for cond, sub in cond_groups.items():
        n = len(sub)
        by_condition[cond] = {
            "count": n,
            "avg_len": round(sum(len(i.text) for i in sub) / n, 1),
            "period_end_rate": round(sum(1 for i in sub if i.text.endswith("。")) / n, 3),
            "comma_rate": round(sum(1 for i in sub if "、" in i.text) / n, 3),
            "P1_rate": round(sum(1 for i in sub if "P1_COMMA_PERIOD" in i.tags) / n, 3),
            "P3_rate": round(sum(1 for i in sub if "P3_MULTI_SENTENCE" in i.tags) / n, 3),
            "clean_rate": round(sum(1 for i in sub if not i.tags) / n, 3),
        }

    return {
        "total": total,
        "avg_len": round(avg_len, 1),
        "avg_tags_per_item": round(avg_tags, 2),
        "clean_count": clean_count,
        "clean_rate": round(clean_count / total, 3),
        "tag_stats": {
            t: {
                "label": TAG_LABELS[t],
                "count": tag_counts[t],
                "rate": round(tag_counts[t] / total, 3),
                "examples": tag_examples[t],
            }
            for t in TAG_LABELS
        },
        "batch_structure": {
            "group_count": len(valid_groups),
            "monotonic_groups": monotonic_groups,
            "monotonic_rate": round(monotonic_groups / len(valid_groups), 3) if valid_groups else None,
            "min_max_groups": min_max_groups,
            "min_max_rate": round(min_max_groups / len(valid_groups), 3) if valid_groups else None,
            "first_avg_len": round(sum(first_lens) / len(first_lens), 1) if first_lens else None,
            "last_avg_len": round(sum(last_lens) / len(last_lens), 1) if last_lens else None,
            "avg_len_by_index": {
                k: round(sum(v) / len(v), 1) for k, v in sorted(idx_lengths.items())
            },
        },
        "exact_duplicates": exact_dups,
        "normalized_duplicates_count": len(norm_dups),
        "by_condition": by_condition,
    }


def render_markdown(report: dict, examples: int, by_condition: bool) -> str:
    if report.get("total", 0) == 0:
        return "検出対象のコピー／タイトルが見つかりませんでした。"

    lines: list[str] = []
    lines.append("# コピー・見出しの形式集計")
    lines.append("")
    lines.append("## 1. 全体サマリー")
    lines.append("タグは句読点の配置と文字数を示す。")
    lines.append("")
    lines.append(f"- 対象案数: **{report['total']}案**")
    lines.append(f"- 平均文字数: **{report['avg_len']}字**")
    lines.append(f"- 1案あたり平均検出タグ数: **{report['avg_tags_per_item']}個**")
    lines.append(
        f"- タグ0件の案: **{report['clean_count']}/{report['total']} ({report['clean_rate']:.1%})**"
    )
    bs = report["batch_structure"]
    lines.append("")
    lines.append("## 2. 句読点パターン")
    lines.append("| パターン | 検出数 | 割合 | 代表例 |")
    lines.append("| :--- | ---: | ---: | :--- |")
    sorted_tags = sorted(
        report["tag_stats"].items(), key=lambda kv: kv[1]["count"], reverse=True
    )
    for _, info in sorted_tags:
        ex_list = [f"`{e['text']}`" for e in info["examples"][:examples]]
        ex_str = " / ".join(ex_list) if ex_list else "-"
        lines.append(
            f"| {info['label']} | {info['count']} | {info['rate']:.1%} | {ex_str} |"
        )

    lines.append("")
    lines.append("## 3. 候補順と文字数")
    if bs["group_count"] > 0:
        lines.append(f"- 番号付きグループ数（3案以上）: **{bs['group_count']}グループ**")
        lines.append(
            f"- 単調増加（短→長）グループ率: **{bs['monotonic_groups']}/{bs['group_count']} ({bs['monotonic_rate']:.1%})**"
        )
        lines.append(
            f"- `01=最短` かつ `最終番号=最長` グループ率: **{bs['min_max_groups']}/{bs['group_count']} ({bs['min_max_rate']:.1%})**"
        )
        lines.append(
            f"- 初番と最終番の平均文字数: **{bs['first_avg_len']}字 → {bs['last_avg_len']}字**"
        )
        len_seq = " → ".join(f"`{k:02d}`:{v}" for k, v in bs["avg_len_by_index"].items())
        lines.append(f"- 番号別の平均文字数推移: {len_seq}")
    else:
        lines.append("- 番号付きグループ（3案以上）は検出されませんでした。")

    lines.append("")
    lines.append("## 4. 重複")
    dups = report["exact_duplicates"]
    lines.append(
        f"- 完全一致: {len(dups)}種類（末尾の句点を除いて比較: {report['normalized_duplicates_count']}種類）"
    )
    for duplicate in dups[:10]:
        locations = duplicate["locations"]
        locs = ", ".join(locations[:4])
        more = f" 他{len(locations) - 4}件" if len(locations) > 4 else ""
        lines.append(f"  - [{duplicate['count']}回] `{duplicate['text']}` ({locs}{more})")

    if by_condition and len(report["by_condition"]) > 1:
        lines.append("")
        lines.append("## 5. 条件別集計")
        lines.append("| 条件 | 件数 | 平均字数 | 句点止め率 | 読点率 | P1 | P3 | タグ0件率 |")
        lines.append("| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
        for cond, st in report["by_condition"].items():
            lines.append(
                f"| {cond} | {st['count']} | {st['avg_len']} | {st['period_end_rate']:.0%} | "
                f"{st['comma_rate']:.0%} | {st['P1_rate']:.0%} | {st['P3_rate']:.0%} | "
                f"{st['clean_rate']:.0%} |"
            )

    return "\n".join(lines)


def item_result(item: CopyItem) -> dict:
    return {
        "id": item.input_id if item.input_id is not None else f"{item.file}:{item.source_line}",
        "file": item.file,
        "line": item.source_line,
        "theme": item.theme,
        "condition": item.condition,
        "batch_id": item.batch_id,
        "index": item.index,
        "text": item.text,
        "tags": item.tags,
        "tag_spans": {
            tag: [{"start": start, "end": end, "text": item.text[start:end]} for start, end in matches]
            for tag, matches in item.tag_spans.items()
        },
        "brief": item.brief,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Measure Japanese copy punctuation, length, and duplicates."
    )
    parser.add_argument(
        "files",
        nargs="*",
        help=(
            "Text or .jsonl files (JSONL requires copy; optional id, field, placement, brief). "
            "Reads plain text from stdin if omitted or '-'."
        ),
    )
    parser.add_argument(
        "--brief",
        default="",
        help="Fallback brief text to include as context in JSON output.",
    )
    parser.add_argument(
        "--by-condition",
        action="store_true",
        help="Include per-condition breakdown table in Markdown output.",
    )
    parser.add_argument(
        "--examples",
        type=int,
        default=3,
        help="Maximum number of examples per pattern in Markdown output (default: 3).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output statistics and per-input punctuation tags with spans in items[].text.",
    )
    args = parser.parse_args()

    all_items: list[CopyItem] = []
    if not args.files or args.files == ["-"]:
        text = sys.stdin.read()
        all_items.extend(parse_source(text.splitlines(), "<stdin>", cli_brief=args.brief))
    else:
        for fp in args.files:
            if fp == "-":
                text = sys.stdin.read()
                all_items.extend(parse_source(text.splitlines(), "<stdin>", cli_brief=args.brief))
            else:
                path = Path(fp)
                text = path.read_text(encoding="utf-8")
                if path.suffix.lower() == ".jsonl":
                    try:
                        all_items.extend(parse_jsonl(text.split("\n"), fp, cli_brief=args.brief))
                    except ValueError as error:
                        parser.error(str(error))
                else:
                    all_items.extend(parse_source(text.splitlines(), fp, cli_brief=args.brief))

    report = analyze_batch(all_items)
    if args.json:
        report["items"] = [item_result(item) for item in all_items]
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report, examples=args.examples, by_condition=args.by_condition))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
