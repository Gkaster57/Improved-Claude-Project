#!/usr/bin/env python3
"""Convert a TimelineJS Google Sheets template (exported as CSV) into TimelineJS JSON.

Usage:
    python3 scripts/csv_to_json.py data/wes-anderson-timeline.csv data/timeline.json

The CSV uses the exact column headers of the official TimelineJS spreadsheet
template, so the same file can be pasted into Google Sheets or rendered here.
"""
import csv
import json
import sys


def date(row, prefix=""):
    """Build a TimelineJS date object from Year/Month/Day/Time columns."""
    out = {}
    for col, key in (("Year", "year"), ("Month", "month"), ("Day", "day")):
        val = row.get(prefix + col, "").strip()
        if val:
            out[key] = int(val)
    t = row.get(prefix + "Time", "").strip()
    if t:
        parts = t.split(":")
        for key, val in zip(("hour", "minute", "second"), parts):
            out[key] = int(val)
    return out or None


def slide(row):
    s = {}
    start, end = date(row), date(row, "End ")
    if start:
        if row.get("Display Date"):
            start["display_date"] = row["Display Date"]
        s["start_date"] = start
    if end:
        s["end_date"] = end
    if row.get("Headline") or row.get("Text"):
        s["text"] = {"headline": row.get("Headline", ""), "text": row.get("Text", "")}
    if row.get("Media"):
        s["media"] = {k: row[c] for k, c in (("url", "Media"), ("credit", "Media Credit"),
                                             ("caption", "Media Caption"), ("thumbnail", "Media Thumbnail"),
                                             ("alt", "Alt Text")) if row.get(c)}
    if row.get("Group"):
        s["group"] = row["Group"]
    if row.get("Background"):
        bg = row["Background"].strip()
        s["background"] = {"color": bg} if bg.startswith("#") else {"url": bg}
    if row.get("Headline"):
        s["unique_id"] = "".join(ch if ch.isalnum() else "-" for ch in row["Headline"].lower()).strip("-")
        while "--" in s["unique_id"]:
            s["unique_id"] = s["unique_id"].replace("--", "-")
    return s


def main(src, dst):
    doc = {"events": [], "eras": []}
    with open(src, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            kind = row.get("Type", "").strip().lower()
            s = slide(row)
            if kind == "title":
                s.pop("start_date", None)
                doc["title"] = s
            elif kind == "era":
                doc["eras"].append({k: s[k] for k in ("start_date", "end_date", "text") if k in s})
            else:
                doc["events"].append(s)
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print(f"Wrote {dst}: {len(doc['events'])} events, {len(doc['eras'])} eras")


if __name__ == "__main__":
    main(*sys.argv[1:3])
