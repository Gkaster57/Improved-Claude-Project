#!/usr/bin/env python3
"""Check that every YouTube media link in a TimelineJS JSON file still works.

Usage:
    python3 scripts/check_media_links.py data/timeline.json

Asks YouTube's oEmbed endpoint about each video; prints one line per link
(with the channel name) and exits 1 if any link fails.
"""
import json
import sys
import urllib.parse
import urllib.request


def check(url):
    q = "https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(url, safe="")
    try:
        with urllib.request.urlopen(q, timeout=20) as r:
            return True, json.load(r).get("author_name", "")
    except Exception as e:  # HTTP 401/404 = private or removed video
        return False, str(e)


def main(path):
    with open(path, encoding="utf-8") as f:
        doc = json.load(f)
    slides = doc["events"] + ([doc["title"]] if "title" in doc else [])
    failed = 0
    for s in slides:
        url = s.get("media", {}).get("url", "")
        if "youtube.com" not in url and "youtu.be" not in url:
            continue
        ok, info = check(url)
        failed += not ok
        print(f"{'OK  ' if ok else 'FAIL'} {s.get('unique_id', 'title'):40} {url}  ({info})")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
