
"""Regression tests for the detector's CLI and JSON output."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


DETECTOR = os.environ.get("SLOP_DETECTOR_PATH", str(Path(__file__).with_name("detect_slop.py")))


def analyze(*args, text=None):
    result = subprocess.run(
        [sys.executable, DETECTOR, "--json", *args],
        input=text if text is not None else "",
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


class DetectorTests(unittest.TestCase):
    def test_mixed_lines_are_kept(self):
        result = analyze(text="短いコピー\n1. 番号付きのコピー\n番号なしのコピー\n")
        self.assertEqual(result["total"], 3)

    def test_number_restarts_begin_new_batches(self):
        repeated = "■ 同じ題材\n【同じ条件】\n01. 山へ\n02. 街から山へ"
        result = analyze(text=f"{repeated}\n\n{repeated}\n")
        self.assertEqual(result["total"], 4)
        self.assertEqual(result["batch_structure"]["group_count"], 0)

        one_section = "01. 秋\n02. 春\n03. 夏\n01. 山\n02. 川\n03. 海\n"
        result = analyze(text=one_section)
        self.assertEqual(result["batch_structure"]["group_count"], 2)
        self.assertNotEqual(result["items"][0]["batch_id"], result["items"][3]["batch_id"])

    def test_unnumbered_lines_are_independent(self):
        result = analyze(text="山\n山へ\n街から山へ\n")
        self.assertEqual(result["batch_structure"]["group_count"], 0)

    def test_copy_words_and_brief_are_not_used_as_tags(self):
        result = analyze(
            "--brief", "ごろっと果肉を残す",
            text="その先へ\n何が決まった？\nごろっと果肉\n",
        )
        self.assertEqual([item["tags"] for item in result["items"]], [[], [], []])
        self.assertEqual(result["items"][2]["brief"], "ごろっと果肉を残す")
        self.assertNotIn("matched_brief_keywords", result["items"][2])
        self.assertNotIn("avg_brief_coverage", result["batch_structure"])
        self.assertNotIn("theme_non_brief_props", result)

    def test_blank_after_heading_preserves_brief(self):
        result = analyze(text="■ 園芸\n\nベランダ向けの苗を届ける\n01. ベランダの苗\n")
        self.assertEqual(result["total"], 1)
        self.assertEqual(result["items"][0]["brief"], "ベランダ向けの苗を届ける")

    def test_short_comma_tag_does_not_depend_on_endings(self):
        result = analyze(text="夜が明けた、家に帰ります\n")
        self.assertEqual(
            result["items"][0]["tag_spans"]["P4_DRAMATIC_COMMA_NO_PERIOD"],
            [{"start": 5, "end": 6, "text": "、"}],
        )

    def test_work_title_period_is_not_a_sentence_break(self):
        result = analyze(text="映画『君の名は。』を上映\n")
        self.assertEqual(result["tag_stats"]["P3_MULTI_SENTENCE"]["count"], 0)

        result = analyze(text="閉店した。「またどこかで。」\n")
        self.assertEqual(result["tag_stats"]["P3_MULTI_SENTENCE"]["count"], 1)

    def test_duplicates_include_copies_differing_only_in_the_final_period(self):
        result = analyze(text="苗の便り\n苗の便り\n果樹の便り。\n果樹の便り\n")
        self.assertEqual(
            [(entry["text"], entry["count"]) for entry in result["exact_duplicates"]],
            [("苗の便り", 2)],
        )
        self.assertEqual(result["normalized_duplicates_count"], 2)

    def test_json_uses_ids_and_reports_all_tag_spans(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "copies.jsonl"
            path.write_text(
                json.dumps(
                    {"id": "head-1", "copy": "　桃、ごろり。\n次の一皿へ。", "brief": "桃の果肉"},
                    ensure_ascii=False,
                )
                + '\n\n{"copy":"商品情報"}\n',
                encoding="utf-8",
            )
            result = analyze(str(path))
        self.assertIn("items", result)
        first, second = result["items"]
        self.assertEqual(first["id"], "head-1")
        self.assertEqual(first["brief"], "桃の果肉")
        self.assertEqual(second["id"], f"{path}:3")
        self.assertEqual(second["tags"], [])
        self.assertEqual(set(first["tags"]), set(first["tag_spans"]))
        self.assertEqual(first["text"], "桃、ごろり。 次の一皿へ。")
        self.assertEqual(first["tag_spans"]["P1_COMMA_PERIOD"], [
            {"start": 1, "end": 2, "text": "、"},
            {"start": 12, "end": 13, "text": "。"},
        ])
        self.assertEqual(first["tag_spans"]["P3_MULTI_SENTENCE"], [
            {"start": 5, "end": 6, "text": "。"},
        ])
        for spans in first["tag_spans"].values():
            for span in spans:
                self.assertEqual(first["text"][span["start"]:span["end"]], span["text"])


if __name__ == "__main__":
    unittest.main()
