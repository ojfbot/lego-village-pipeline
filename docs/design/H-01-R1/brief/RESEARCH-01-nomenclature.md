# Research note RESEARCH-01 — Decomposition vocabulary (for a research agent, not design)

**Filed:** 2026-09-17 · **From:** claude-design session (F-01 / P-01 review) · **Requested by:** @jfo
**Status:** open · **Blocks:** schema naming in `packages/schema`; copy on every sheet; kid-facing copy on F-01

## The problem
Our sheets currently say "8 parts, 288 pieces", "bricks, about 140", "MILS module / quadrant / unit", "section", "sub-build", "component", "sticker → envelope → model". These are design placeholders. We are describing **decomposition at several scales and along several axes** and need the exact vocabulary LEGO, AFOL culture, BrickLink/Rebrickable and MILS use — chosen per audience (operator sheets vs family workbench) and enforced everywhere.

## Questions to answer (with sources)
1. **Element / part / piece / brick** — LEGO official usage ("element" = part + colour; "design ID" vs "element ID"), BrickLink usage ("part", "item", "lot"), Rebrickable usage. When does a count mean distinct designs vs total pieces vs lots? Recommend the terms for: distinct designs · distinct design+colour · total physical pieces · purchasable lots.
2. **Scale ladder** — what is the accepted ladder from a single element up to a display: element → sub-assembly / sub-build → module (MILS) → section / baseplate → layout → display / village? Where do "MOC", "set", "build", "model", "kit" sit? What does MILS specifically call its 32×32 units, corner/half units, and stacked heights?
3. **Track & rail** — official names for 53400/53401/53407 (curve, straight, switch), "R40", radius/gauge conventions, "railbed" vs "ballast" vs "roadbed" vs "right of way" in AFOL train circles (LUG/LTC usage). Which word for the studs a train needs clear beside the rail?
4. **Landscape** — "baseplate", "MILS core", "groundcover", "terrain", "planting", "snow" — do these match MILS/AFOL usage or are they ours? Preferred terms.
5. **Inventory lifecycle** — BrickLink/Rebrickable/official words for owned · in cart · ordered · on order · planned/earmarked · built-into · loose/parted out.
6. **Audience register** — which of the above are safe for a 9–11-year-old builder without becoming babyish (e.g. "piece" vs "element"; "build" vs "model").

## Deliverable
- A short glossary table: our current word → recommended word (operator) → recommended word (family) → source(s) → note.
- A list of hard rules a linter could enforce (e.g. "never 'parts' for a piece count; 'parts' means distinct designs").
- Explicit calls on the two live disputes: **"Ring" vs "Rail"** on F-01's layer toggle, and **"unit / module / quadrant"** for the MILS pieces in A-01's rig.

## Where the placeholders live today
- P-01 opener: "buy 8 parts, 288 pieces" · parts × shops schedule · "lot", "pieces covered"
- C-01: "Parts list — by basis", "TO BUY · N PIECES"
- A-01: "Quadrant module 1/2", "MILS units in the rig", layer names
- F-01: "sticker · envelope · model", "bricks, about", "studs claimed", "Rail"
- Hub log 09-17 12:10 (schema entry) and 09-17 "Rail" note
