"""Checks on the generated TimelineJS data. Run: python3 -m unittest discover -s tests -v"""
import json
import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(ROOT, "data", "wes-anderson-timeline.csv")
JSON = os.path.join(ROOT, "data", "timeline.json")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import csv_to_json  # noqa: E402

INK = "#2B2118"


def load():
    with open(JSON, encoding="utf-8") as f:
        return json.load(f)


def events():
    return load()["events"]


def _luminance(hex_color):
    h = hex_color.lstrip("#")
    chans = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in chans]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(hex_a, hex_b):
    la, lb = sorted((_luminance(hex_a), _luminance(hex_b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


class TimelineData(unittest.TestCase):
    def test_json_in_sync_with_csv(self):
        with tempfile.TemporaryDirectory() as d:
            out = os.path.join(d, "t.json")
            csv_to_json.main(CSV, out)
            with open(out, encoding="utf-8") as f:
                self.assertEqual(json.load(f), load(), "Regenerate data/timeline.json from the CSV")

    def test_unique_ids_unique(self):
        ids = [e["unique_id"] for e in events()]
        self.assertEqual(len(ids), len(set(ids)), ids)

    def test_background_contrast(self):
        for e in events():
            c = e["background"]["color"]
            self.assertGreaterEqual(contrast(c, INK), 9.0, f"{e['unique_id']} {c}")

    def test_media_has_alt_and_credit(self):
        for e in events():
            if "media" in e:
                self.assertTrue(e["media"].get("alt"), e["unique_id"])
                self.assertTrue(e["media"].get("credit"), e["unique_id"])

    def test_every_event_has_facts(self):
        for e in events():
            self.assertIn('<ul class="facts">', e["text"]["text"], e["unique_id"])


if __name__ == "__main__":
    unittest.main()
