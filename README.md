# The Films of Wes Anderson: An Improved TimelineJS Project

**Live site:** https://gkaster57.github.io/Improved-Claude-Project/

This is a revised and expanded version of a [TimelineJS](https://timeline.knightlab.com/) timeline of Wes Anderson's feature films.
The original Google Sheet is saved for comparison as [`data/original-sheet.csv`](data/original-sheet.csv).

## Recommendations (all implemented here)

| # | Problem in the original | Change |
|---|---|---|
| 1 | Stopped at *The French Dispatch* (2021) | Added *Asteroid City* (2023), *The Phoenician Scheme* (2025), and the Oscar-winning short *The Wonderful Story of Henry Sugar* (2023) |
| 2 | Each slide had one line of text | Added a synopsis, why each film matters (awards, firsts, production details), and key facts: distributor, writers, cast |
| 3 | `Group` column unused; no eras | Films are grouped by format (live action / stop-motion animation), and four career-phase eras are shaded on the timeline |
| 4 | TimelineJS draws **white text on every coloured background**, so light colours such as `#89CFF0`, `#FFB6C1`, `#AFE1AF`, and `#B2BEB5` gave text about 1.5:1 contrast | A film-inspired pastel palette with a CSS override for dark text (every slide at 9:1 or better) |
| 5 | Title image was a Google image-search thumbnail (`encrypted-tbn0.gstatic.com`), which can expire and has no licence | Openly licensed Wikimedia Commons photo, credited under CC BY-SA 4.0 |
| 6 | Placeholder `asdf` left in the title row's Alt Text; no alt text or captions elsewhere | Alt text and captions on every slide |
| 7 | Trailer credits were approximate (for example, "Rotten Tomatoes") | Credits name the actual YouTube channel. All 13 links were checked with YouTube's oEmbed API |
| 8 | Slides couldn't be linked individually | `hash_bookmark` is on, so every slide has its own URL |
| 9 | Depended on a published Google Sheet | Data is version-controlled in this repo and rendered from JSON on GitHub Pages |
| 10 | Short films left out | A third **Short films** row: the 1994 *Bottle Rocket* short, *Hotel Chevalier* (2007), *Henry Sugar*, and one slide for *The Swan*, *The Rat Catcher*, and *Poison*. The first era now starts in 1994 |
| 11 | No sense of how the films were received | Rotten Tomatoes and Metacritic scores on every film that has them, linked to the source and dated (Nov 2026) |
| 12 | A TimelineJS 3.9.6 bug hid the last row label ("Stop-motion animation") | A small workaround in `index.html` keeps every row label visible, including after zooming |

## Ideas for further expansion
- Use licensed stills or posters as slide backgrounds.
- Make a companion timeline of recurring collaborators (Murray, Wilson, Schwartzman, Coppola, Desplat, Yeoman).
- Add sourced box-office figures.
- Map filming locations with StoryMapJS.

## Editing the timeline

`data/wes-anderson-timeline.csv` is the source of truth. It uses the exact column headers of the official TimelineJS Google Sheets template.

- **To edit here:** change the CSV, then run
  ```sh
  python3 scripts/csv_to_json.py data/wes-anderson-timeline.csv data/timeline.json
  ```
  Then run the checks, commit, and push. GitHub Pages redeploys automatically.
  ```sh
  python3 -m unittest discover -s tests -v          # data checks (offline)
  python3 scripts/check_media_links.py data/timeline.json   # trailer links still work (needs network)
  ```
- **To use Google Sheets instead:** paste the CSV into a copy of the TimelineJS template, publish it, and generate an embed at timeline.knightlab.com.
  Note that the dark-text colour fix (#4) needs the custom CSS on this site. A plain Knight Lab embed will show white text.

## Files
```
index.html                    page + TimelineJS embed
assets/style.css              page styling and TimelineJS overrides
data/wes-anderson-timeline.csv  revised spreadsheet (TimelineJS template columns)
data/timeline.json            generated TimelineJS JSON
data/original-sheet.csv       original spreadsheet, for comparison
scripts/csv_to_json.py        CSV → TimelineJS JSON converter
scripts/check_media_links.py  checks every YouTube trailer link via oEmbed
tests/test_timeline.py        data checks: JSON in sync, unique slide IDs, contrast, groups, eras, critics lines
docs/superpowers/             design and plan for the short-films and scores update
```

## Credits
Built with TimelineJS (Northwestern University Knight Lab). Title photo: Martin Kraft, Wikimedia Commons, CC BY-SA 4.0.
Trailers are embedded from official or licensed YouTube channels. Critics' scores: Rotten Tomatoes and Metacritic, checked November 2026.
