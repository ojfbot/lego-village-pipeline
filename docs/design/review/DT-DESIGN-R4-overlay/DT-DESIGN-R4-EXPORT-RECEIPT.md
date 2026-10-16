# DT-DESIGN R4 — export receipt (designer side)

**Bundle:** `handoff-r4/` — an **overlay**: unpack R2 rev-b, then R3, then this folder on top. The union is the R4 tree.
**exported:** 2026-10-10 by Claude Design · **theme captured:** none (no driven frames this cut) · **sources copied:** 6 sheets/studies + Hub + dt/tokens.css + R-01 photo assets

**Supersedes** DT-DESIGN R3 (`DT-DESIGN-R3-walkthroughs-overlay.zip`, sha256 `e21975a4…5183`). Nothing in `walkthroughs/`, `handoff/`, `fixtures/`, `library/` or the R3 sheet sources changed. `decisions.last_id` is still `DEC-043`; five decisions are **proposed** in `decisions-proposed.md` and take ids only when the operator accepts them.

## What R4 adds (all work dated 2026-10-10, across chat sessions)

**New sheet — R-01 "Bringing things into the house"** (`sources/prototypes/Prototype R - …`, two variants). Photos of a receipt and the things on it → the AI crops, reads, fills a form per thing and matches it to what was waiting → nothing counts as in the house until James OKs it. Three ways in: a planned buy, an unplanned buy, loose parts to count. The one-page variant shows everything at once; the step-by-step variant walks Ordered → Here → Counted → In the house with a running "from this receipt" ledger. Hub gained the R-01 card and a "bought in store 10-10" line in the task-1 popover. Spec: `specs/R-01-bringing-things-in.md`.

**Study — X-01 Typology identity.** The question: every sheet opens the same way, so only the letter in the code tells a workspace from a question from a register from an approval. `Typology Identity.dc.html` is the canvas board: a ten-kind census (one verb each), the problem, five approaches drawn on the same four sheets (1a nameplate · 1b verb-as-headline · 1c plan-as-identity · 1d drawing-set title block · 1e threshold), and a recommendation to layer them. `Typology Identity v2.dc.html` is the same content as a **single-viewport navigator**: eight cards, tap to open (shared-element move, the rest collapse to a right rail), the census opens a third level where each kind renders as a specimen on nested 12-column subgrids; the canvas breathes (grid loosens, two washes gather); **Benny**, the chief of staff, is a left column that pushes the board (2px → 8px on hover → 340px) and routes by plain-language chat. Spec: `specs/X-01-typology-identity.md`.

**Study — W-00 Workbench frame.** Header rule, optional left/right sidebars (collapse to 48px rails), a 12-column main whose cards are row-subgrids (heads/bodies/status lines align across a row), footer ledger, and a worked **ripple**: signing a measurement on M-01 draws connectors to A-01, C-01, queue #3 and the trail, pulses them once, shows old → new on each status line, hangs a CHANGED chip until acknowledged, and states the consequence in the ledger. Spec: `specs/W-00-workbench-frame.md`.

**Token.** `--dt-plate` / `--dt-on-plate` added to `dt/tokens.css`: the filled emphasis surface, dark in both themes, so a filled plate never reads as a white block on blueprint. Applied on X-01 v2 only (debt listed).

## Standing notes (read these first)

- **N-01** — X-01 and W-00 are **wireframes**, not implementation guides. The whole page re-renders and re-snapshots on every transition (D-13). Dedicated agent sessions are needed to build this properly: component-scoped state, element-scoped transitions, a real layout-animation library, container queries in stylesheets.
- **N-02** — Open and unanswered: gradient/wash design, tonal steps per state, the icon set, and most copy. Real progress on structure and motion; not a visual sign-off.

## Not authorized by this export

Folder, not a landing: no instruments row, no register bump, no PR, no import record. `tree_sha256` is the importer's field. Run `python3 tools/design_pkg.py digest <unpacked>` and take that value.
