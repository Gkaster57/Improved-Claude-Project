"""Checks on the generated TimelineJS data. Run: python3 -m unittest discover -s tests -v"""
import json
import os
import re
import sys
import tempfile
import unittest
import urllib.parse

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

    def test_groups(self):
        self.assertEqual({e["group"] for e in events()},
                         {"Live action", "Stop-motion animation", "Short films"})

    def test_short_films_row(self):
        by_id = {e["unique_id"]: e for e in events()}
        for uid in ("bottle-rocket-short", "hotel-chevalier",
                    "the-wonderful-story-of-henry-sugar", "the-swan-the-rat-catcher-and-poison"):
            self.assertIn(uid, by_id)
            self.assertEqual(by_id[uid]["group"], "Short films", uid)

    def test_features_have_critics(self):
        for e in events():
            if e["group"] in ("Live action", "Stop-motion animation"):
                self.assertIn("<strong>Critics:</strong>", e["text"]["text"], e["unique_id"])

    def test_critics_format(self):
        for e in events():
            t = e["text"]["text"]
            if "<strong>Critics:</strong>" not in t:
                continue
            facts = t[t.index('<ul class="facts">'):]
            items = re.findall(r"<li>.*?</li>", facts)
            line = items[-1]
            self.assertIn("<strong>Critics:</strong>", line, f"{e['unique_id']}: Critics must be the last fact")
            self.assertIn("(as of Nov 2026)", line, e["unique_id"])
            hosts = {urllib.parse.urlparse(h).netloc for h in re.findall(r'href="([^"]+)"', line)}
            self.assertTrue(hosts and hosts <= {"www.rottentomatoes.com", "www.metacritic.com"},
                            f"{e['unique_id']}: {hosts}")

    def test_page_copy(self):
        with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as f:
            page = f.read()
        self.assertIn("Twelve features and six short films, 1994&ndash;2025", page)
        self.assertNotIn("one Oscar-winning short", page)

    def test_no_claim_of_every_short(self):
        # Anderson made shorts not on this timeline (e.g. Castello Cavalcanti, 2013),
        # so copy must not claim the shorts are complete.
        with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as f:
            page = f.read()
        title = load()["title"]["text"]
        self.assertNotIn("every feature film and short", page)
        self.assertNotIn("and his short films", title["text"])
        self.assertNotIn("Feature Film Timeline", title["headline"])

    def test_events_inside_eras(self):
        eras = load()["eras"]
        for e in events():
            y = e["start_date"]["year"]
            self.assertTrue(any(er["start_date"]["year"] <= y <= er["end_date"]["year"] for er in eras),
                            f"{e['unique_id']} ({y}) is outside every era")


if __name__ == "__main__":
    unittest.main()
