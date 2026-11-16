# Short films and critic scores: design

Date: 2026-11-16 · Status: approved

## Intent
Class assignment: improve an existing project, using the Superpowers brainstorm → design → plan → build process.
This round makes the timeline a more complete record of Anderson's work and adds a sourced measure of how each film was received.
A collaborators view may follow in a later round, if time allows. It gets its own design.

## Goals
- Add short-film slides:
  - the 1994 *Bottle Rocket* short
  - *Hotel Chevalier* (2007)
  - one combined slide for *The Swan*, *The Rat Catcher*, and *Poison* (2023)
- Move the existing *The Wonderful Story of Henry Sugar* slide into a new "Short films" group row.
- Add a "Critics" line to each film's key-facts list: Rotten Tomatoes Tomatometer and Metacritic Metascore, each linked to its source page, with an "as of Nov 2026" date.
- Update the site's text to match:
  - masthead subtitle
  - About section ("What changed" and "Ideas for further expansion")
  - README

## Non-goals
- Box-office figures.
- Collaborators view (next round).
- Palette or layout redesign beyond what a third group row needs.

## Anti-goals
- Any score, date, or fact taken from memory without checking it against a live source.
- Unofficial or pirated video uploads used as slide media.
- A timeline bar where slides overlap or a group row label is cut off.

## Constraints
- `data/wes-anderson-timeline.csv` stays the source of truth, using TimelineJS template columns. `data/timeline.json` is regenerated with `scripts/csv_to_json.py`.
- Every new slide follows the conventions the existing slides use:
  - synopsis paragraph
  - `ul.facts` key-facts list
  - media credit and caption
  - alt text
  - a pastel background with dark text (contrast 9:1 or better)
- The site is hosted on GitHub Pages. Nothing is pushed without the user's approval.

## Approaches considered
1. **Fill in the short films and add critic scores. Chosen.** It's a clear before/after, stays inside the existing data pipeline, and comes with checkable steps.
2. Companion collaborators view. Deferred to a later round because it's a new page with its own open design questions.
3. StoryMapJS filming-locations map. Rejected for this round because most of the work happens in Knight Lab's web editor, outside the repo and the build process being demonstrated.

## Decisions
- **Combine the three Dahl shorts into one slide.** Releasing on consecutive days would otherwise stack them on *Henry Sugar* in the timeline bar.
- **Use both RT and Metacritic, dated.** Scores drift, and the date keeps them honest. Where a source has no score, that part is left off. If neither has one, the whole line is left off.
- **Groups become three rows:** Live action, Stop-motion animation, Short films. The timenav height and CSS are adjusted so all three row labels show. This is verified in a browser at desktop and phone widths.
- **Shorts without an official trailer** use a licensed image (for example, from Wikimedia Commons) or no media.

## Left to the builder
- Exact background colours for the new slides, within the existing pastel scheme and contrast rule.
- Which official trailer or channel to use for each short, checked with YouTube oEmbed the way the existing 13 links were.
- Wording of the synopses and the updated About/README text.
