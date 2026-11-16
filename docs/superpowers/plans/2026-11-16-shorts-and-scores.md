# Short Films and Critic Scores Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add short-film slides in a new "Short films" row and dated, linked critic scores to every film on the Wes Anderson TimelineJS site.

**Architecture:** All content changes go in `data/wes-anderson-timeline.csv`. `scripts/csv_to_json.py` regenerates `data/timeline.json`. A new stdlib-only `unittest` suite checks the generated JSON. Layout is checked in a real browser with Playwright.

**Tech Stack:** TimelineJS 3.9.6 (CDN), Python 3 stdlib, static HTML/CSS on GitHub Pages, Playwright MCP for browser checks.

**Spec:** `docs/superpowers/specs/2026-11-16-shorts-and-scores-design.md`

## Global Constraints

- The CSV is the source of truth. After every CSV edit, run `python3 scripts/csv_to_json.py data/wes-anderson-timeline.csv data/timeline.json`.
- Every new slide follows the existing conventions:
  - `<p>` synopsis, then `<ul class="facts">`
  - Media Credit, Media Caption, Alt Text
  - pastel `#RRGGBB` Background with contrast ≥ 9:1 against ink `#2B2118`
- The Critics line has exactly this format, as the last `<li>` in `ul.facts`: `<li><strong>Critics:</strong> <a href="RT_URL">Rotten Tomatoes NN%</a> · <a href="MC_URL">Metacritic NN</a> (as of Nov 2026)</li>`. If one source has no score, leave out that link. If neither has one, leave out the whole `<li>`.
- Every score, date, and trailer is checked against its live source page. Nothing is filled in from memory.
- Media: official or licensed sources only (an official YouTube channel, or Wikimedia Commons with its licence credited). Otherwise leave Media empty.
- Groups are exactly `Live action`, `Stop-motion animation`, `Short films`.
- Work on branch `shorts-and-scores`. Never push without the user's approval.

## Review Focus

1. **Duplicate slide IDs:** the 1994 short's headline "Bottle Rocket" would turn into the same `unique_id` as the feature and break shareable links. Every `unique_id` must be unique (test in Task 1). The short's headline is `Bottle Rocket (short)`.
2. **Slides before any era:** the 1994 short falls before the first era band, which starts in 1996. Every dated event must fall inside an era (test in Task 2). Fix: change the first era's start Year from 1996 to 1994, since the short was co-written with Owen Wilson.
3. **Stale JSON:** a CSV edit without regenerating ships old data. The committed JSON must equal a fresh conversion (test in Task 1).
4. **Crowded Sept 2023 markers:** *Henry Sugar* (Sept 27) and the Dahl trio slide (Sept 28) sit side by side in the shorts row. Both markers and all three row labels must stay readable at 1280px and 390px wide (browser check in Task 4).
5. **Dead or unofficial trailer links:** every YouTube Media URL must pass oEmbed (network check script in Task 2).

---

### Task 1: Test suite guarding the current data

**Files:**
- Create: `tests/test_timeline.py`
- Branch: `git checkout -b shorts-and-scores`

**Interfaces:**
- Produces: `tests/test_timeline.py` with module-level `load()` (returns the parsed `data/timeline.json`), `events()` (returns the list of events), and `contrast(hex_a: str, hex_b: str) -> float` (WCAG ratio). Run with `python3 -m unittest discover -s tests -v`.

- [ ] **Step 1: Write tests that pass on the current data**
  - `test_json_in_sync_with_csv`: run `csv_to_json.main` into a temp file, then assert it equals `data/timeline.json`.
  - `test_unique_ids_unique`: `len(ids) == len(set(ids))` across all events.
  - `test_background_contrast`: every event's `background.color` gives `contrast(color, "#2B2118") >= 9.0`.
  - `test_media_has_alt_and_credit`: every event with `media` has a non-empty `alt` and `credit`.
  - `test_every_event_has_facts`: `'<ul class="facts">'` appears in every event's `text.text`.
- [ ] **Step 2: Run it.** `python3 -m unittest discover -s tests -v`. Expected: all 5 pass. If one fails, the current data has a bug: report it, don't paper over it.
- [ ] **Step 3: Commit.** `git add tests && git commit -m "test: guard timeline data invariants"`

### Task 2: Short-film slides, group row, era start

**Files:**
- Modify: `data/wes-anderson-timeline.csv`, then regenerate `data/timeline.json`
- Modify: `tests/test_timeline.py`
- Create: `scripts/check_media_links.py`

**Interfaces:**
- Consumes: `load()`, `events()` from Task 1.
- Produces: slide `unique_id`s `bottle-rocket-short`, `hotel-chevalier`, `the-swan-the-rat-catcher-and-poison` (headline `The Swan, The Rat Catcher, and Poison`), all with `group == "Short films"`. `the-wonderful-story-of-henry-sugar` moves to `Short films`. `scripts/check_media_links.py` exits 0 when every YouTube Media URL returns HTTP 200 from `https://www.youtube.com/oembed?url=<url>&format=json`.

- [ ] **Step 1: Write the failing tests**
  - `test_groups`: `{e["group"] for e in events()} == {"Live action", "Stop-motion animation", "Short films"}`.
  - `test_short_films_row`: the four IDs above all have group `Short films`.
  - `test_events_inside_eras`: every event's start year falls inside some era's year range.
- [ ] **Step 2: Run the tests.** Expected: all 3 fail, because `Short films` is missing, the IDs are missing, and 1994 is outside every era.
- [ ] **Step 3: Research each short.** Find its release date, distributor or platform, writers, cast, and an official trailer or licensed image. Use sources like the Sundance archive, Fox Searchlight / Apple iTunes for *Hotel Chevalier*, and Netflix for the Dahl shorts. Use cross-checked references and record the sources you used.
- [ ] **Step 4: Add the 3 CSV rows** after the existing rows they belong next to, and set Henry Sugar's Group to `Short films`. Display Date format follows the existing slides: Henry Sugar's display date stays `September 27, 2023 · Short film (Netflix)`, and the trio uses `September 28–30, 2023 · Short films (Netflix)`. Change the first era's Year from `1996` to `1994`. Then regenerate the JSON.
- [ ] **Step 5: Write `scripts/check_media_links.py`** (stdlib `urllib`; takes the JSON path as its only argument; prints one line per URL; exits 1 on any failure).
- [ ] **Step 6: Verify.** Run `python3 -m unittest discover -s tests -v` (expected: all pass), then `python3 scripts/check_media_links.py data/timeline.json` (expected: exit 0, all OK).
- [ ] **Step 7: Commit.** `git commit -am "feat: add short-film slides in a Short films row"` (also `git add scripts/check_media_links.py`).

### Task 3: Critic scores

**Files:**
- Modify: `data/wes-anderson-timeline.csv`, then regenerate `data/timeline.json`
- Modify: `tests/test_timeline.py`

**Interfaces:**
- Consumes: `events()` from Task 1.

- [ ] **Step 1: Write the failing tests**
  - `test_features_have_critics`: every event in groups `Live action` and `Stop-motion animation` contains `<strong>Critics:</strong>`.
  - `test_critics_format`: every Critics `<li>` contains `(as of Nov 2026)`, contains at least one `href` whose host is `www.rottentomatoes.com` or `www.metacritic.com`, and is the last `<li>` of its `ul.facts`.
- [ ] **Step 2: Run the tests.** Expected: `test_features_have_critics` fails (12 features without the line).
- [ ] **Step 3: For each of the 12 features and the 4 short slides, open the film's RT and Metacritic pages and record the current score and URL.** For the Dahl trio slide, list each film's RT score, for example `<a>The Swan 95%</a>`. Keep the "Rotten Tomatoes" label on the first one, and follow the same pattern for Metacritic. Skip any source with no score.
- [ ] **Step 4: Add the Critics lines to the CSV and regenerate.**
- [ ] **Step 5: Verify.** `python3 -m unittest discover -s tests -v`. Expected: all pass.
- [ ] **Step 6: Commit.** `git commit -am "feat: add dated Rotten Tomatoes and Metacritic scores"`

### Task 4: Three-row timeline layout

**Files:**
- Modify: `index.html` (the `timenav_height_percentage` option), and `assets/style.css` only if needed

- [ ] **Step 1: Serve the site locally.** `python3 -m http.server 8000` (in the background). Open `http://localhost:8000/` in Playwright at 1280×900.
- [ ] **Step 2: Check the timeline bar.** All three row labels must show in full. Markers for Henry Sugar and the Dahl trio must not overlap so much that either headline is unreadable. The 1994 marker must sit inside the first era band. Take a screenshot.
- [ ] **Step 3: If any check fails, adjust it.** Raise `timenav_height_percentage` (currently 38) and/or `initial_zoom` (currently 2), or adjust `#timeline-embed` height (currently 740px desktop, 600px under 700px). Re-check after each change.
- [ ] **Step 4: Repeat Steps 2–3 at 390×844.** The page must not scroll horizontally (`document.documentElement.scrollWidth <= 390`).
- [ ] **Step 5: Open `/#event-hotel-chevalier` and `/#event-bottle-rocket-short`.** Each must open on its own slide. Save the final screenshots to the scratchpad and show them to the user.
- [ ] **Step 6: Commit.** `git commit -am "fix: size timeline nav for three group rows"` (skip if nothing changed).

### Task 5: Site copy and README

**Files:**
- Modify: `index.html` (meta description, `.dek`, About "What changed" and "Ideas for further expansion"), `README.md` (recommendations table, ideas list, Files block)
- Modify: `tests/test_timeline.py`

- [ ] **Step 1: Write the failing test.** `test_page_copy`: `index.html` contains `Twelve features and six short films, 1994&ndash;2025` and no longer contains `one Oscar-winning short`.
- [ ] **Step 2: Run the test.** Expected: FAIL.
- [ ] **Step 3: Update the copy.**
  - Set the dek to that exact string. The meta description says "every feature film and short".
  - Add a "What changed" bullet for the short films and one for the critic scores.
  - Remove "Add slides for formative events…" and "Add box-office and critics' scores…" from the ideas lists, and change the box-office idea to "Add box-office figures".
  - Mirror these changes in the README table (rows 10–11) and the ideas list, and add `tests/` and `scripts/check_media_links.py` to the Files block.
- [ ] **Step 4: Run all checks.** `python3 -m unittest discover -s tests -v` and `python3 scripts/check_media_links.py data/timeline.json`. Expected: all pass, exit 0.
- [ ] **Step 5: Commit.** `git commit -am "docs: update site copy and README for shorts and scores"`
