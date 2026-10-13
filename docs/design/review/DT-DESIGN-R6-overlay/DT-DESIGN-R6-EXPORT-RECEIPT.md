# DT-DESIGN R6 — export receipt (designer side)

**Bundle:** `handoff-r6/` — an **overlay**: unpack R2 rev-b, then R3, R4, R5, then this folder on top. The union is the R6 tree.
**exported:** 2026-10-12 by Claude Design · **sources copied:** the HW-01 study as it stands tonight (`House World.dc.html`, `house/house-stage.js`, `house/house-metadata.json`, DynaPuff + OFL, reference captures) + the new shared theme script `dt/theme.js` · **no existing sheet changed**

**Supersedes** DT-DESIGN R5 (`handoff-r5/`). R5's HW-01 spec is replaced by four specs that describe the same study in full; nothing in R4's sheets, `dt/tokens.css`, fixtures or ledger changed. `decisions.last_id` is still `DEC-043`; R5's three proposals are carried and four more are **proposed** in `decisions-proposed.md`.

## What R6 adds (all work dated 2026-10-12)

**Fly-through, completed as a spec (HW-01 rev 2).** One camera owner at a time (tour → flight → threshold → blend); the hover card that names the room under the pointer, with hysteresis and a "settle" rule so nothing flickers while the page scrolls; Back lands the camera outside the room whose sheet was actually open; the stage adopts `house.glb` in place when the file is dropped beside the metadata. Full event/method table for `<house-stage>`.

**Rooms as kinds of work (HW-02).** The house is no longer "one block = one sheet". Eight rooms (R1–R8), each one kind of work (work management, design & planning, verification, review & approval, procurement & receiving, inventory, programme & handoff, research), each holding its sheets; the full block → room → sheet map, the finder's matching rules, tabs inside the dashboard, and "Switch room".

**Agent input — the ask bar (HW-03).** The PLAY WELL bubble became a plain-language prompt: *Describe what you want to build or change…*, with a talk button marked "coming later". Today it routes: a match flies to the room; no match hands the words to the finder. The spec says exactly what it does now, what it must never pretend to do, and what the future agent inherits.

**Graphic text, bubbles and gradients (HW-04).** The layered-stroke wordmark technique (yellow outline · ink outline · gradient-swept fill · hard red drop shadow), its four sizes (poster, chapter caption, sheet title, concept-door title), the studio palette per theme, the gradient sweep timing, the pill/bubble vocabulary, and what a vector version must preserve (N-04 still stands).

## Standing notes (read these first)

- **N-03** — the house is a stand-in until `house.glb` is supplied (adoption is wired and tested against the R0 naming).
- **N-04** — PLAY WELL should become a vector graphic; HW-04 is the brief for it.
- **N-05** (new) — theme preference is shared: `dt/theme.js` persists blueprint/paper in `localStorage.dtTheme` and syncs across the house and every sheet in its iframes.
- **N-06** (new) — the ask bar is a router, not an agent. No copy may imply the table drafts anything yet.
- N-01 / N-02 from R4 still stand.

## Not authorized by this export

Folder, not a landing: no instruments row, no register bump, no PR, no import record, no change to HOUSE-WORLD R0. `tree_sha256` is the importer's field — run `python3 tools/design_pkg.py digest <unpacked>`.
