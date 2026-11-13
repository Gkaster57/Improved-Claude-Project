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

## Ideas for further expansion
- Add slides for the 1994 *Bottle Rocket* short, the *Hotel Chevalier* prologue, and the other three Roald Dahl shorts (2023–24).
- Use licensed stills or posters as slide backgrounds.
- Make a companion timeline of recurring collaborators (Murray, Wilson, Schwartzman, Coppola, Desplat, Yeoman).
- Add sourced box-office and critics' scores.
- Map filming locations with StoryMapJS.

## Editing the timeline

`data/wes-anderson-timeline.csv` is the source of truth. It uses the exact column headers of the official TimelineJS Google Sheets template.

- **To edit here:** change the CSV, then run
  ```sh
  python3 scripts/csv_to_json.py data/wes-anderson-timeline.csv data/timeline.json
  ```
  Then commit and push. GitHub Pages redeploys automatically.
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
```

## Credits
Built with TimelineJS (Northwestern University Knight Lab). Title photo: Martin Kraft, Wikimedia Commons, CC BY-SA 4.0.
Trailers are embedded from official or licensed YouTube channels.
