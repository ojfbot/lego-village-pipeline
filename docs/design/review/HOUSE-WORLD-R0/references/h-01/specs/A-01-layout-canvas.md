# A-01 — Layout Canvas

**File:** `prototypes/Prototype A - Layout Canvas.dc.html` · **Journeys:** J3 J4 (J13 seed) · **Status at handoff:** built; to be split into viewer + canvas in code
Behaviour reference is the live prototype; its code is not to be copied. All numbers are mock pending real math + audit.

## Purpose
Place, rotate and mate two R40 quadrant modules by drag **and** exact numeric entry, with live endpoint validation, semantic layers, separation peel, planting proposals, versioned save and a synced 3D massing view.

## Behaviour
- Canvas: stud grid (1 / 8 / 32 patterns); module NE fixed, module NW draggable (pointer) and keyboard-movable (arrows; R rotates). Position snaps to whole studs in whole mode, ¼ stud in fraction mode; rotation in 22.5° steps (0.1° in fraction mode). Labels follow the chosen unit (plates | bricks for Z).
- Endpoint mate: NE·b ↔ NW·a compared on position, heading and elevation; pass shows a snap pulse and runs the train; fail shows the gap/heading/elevation delta in plain words.
- Exact transform card: X, Y, rotation, Z inputs mirror the drag; typing moves the module; both snap.
- Layer rig: **Scene** tab = semantic tree (Foundation · Transport · Landscape with sub-layers, per-row ON/OFF, planting rows expandable to individual proposals). **Separation** tab = depth slider 0–8 removing strata top-down (not build order). **MILS units in the rig** list scopes both tabs to ticked modules; unticked modules stay whole and dim.
- Planting proposals: dashed = proposed (AI or family), solid = placed. PLACE / DROP / ↺ keep the record. ASK edits a proposal in natural language (keyword mock: direction, studs, size); the AI echoes exactly what changed.
- Versions: save creates rN; freeze is a separate act (gate ladder).
- 3D viewer: same modules, layers and plantings; visibility follows the rig; train runs on pass; reduced-motion renders stills.

## States
whole/fraction · unit plates/bricks · mated/not · layer on/off per row · peel 0–8 · units in rig · proposal proposed/placed/removed · asking · saved rN.

## Copy rules
Plain words; "Separation depth" not "peel level"; validation reads as a sentence with the delta and unit.

## Follow-ups (Q3, Q10)
Split into (1) Component viewer — inspect by scene layer, separation, **design source** (BrickLink · own · official) and **brick source** (inventory · with set · buy); (2) Layout canvas. Build order as a derived view.


## Revision R1 — 3D viewer as verification surface (HANDOFF-LEGO-PIPE-014 §4 · K-3 · DEC-018)

**What changed.** The **ComponentViewer strip stays** under the plan (always visible, follows the layer rig and separation depth). The canvas card gains two tabs — **PLAN** and **3D · CHECK IT** — and the 3D tab moves the same renderer into the full canvas area with LOOK presets and "Try a move". Operator settled this after seeing tabbed-only and side-by-side variants (DEC-029/030). The viewer/canvas *split* (Q3) stays deferred.

**One geometry.** Plan and 3D read the same state: Section NW position/rotation, plantings (px → studs), the tree (DEC-016: 16×16 base, 8 br base, 40 br, canopy r28 from 10 br), the train right-of-way band 36–44 studs from the ring centre (F-01's numbers; name pending RESEARCH-01). The ring centre is the tree centre. The plan draws all of these to scale; the 3D view draws them as massing with true dimensions. If they can disagree, the design is wrong.

**Checks ("Does it fit?" card, right column, always visible).** Deterministic, re-run on every change, each with a badge (■ PASS · ▲ BLOCK · ○ NOT RUN) and a plain-words detail:
1. The ring fits the table — 88 studs needed across, 112 available.
2. Nothing sits under the tree base — overlap of each Section with the 16×16 base, in studs. **Today this blocks honestly:** with the ring centred on the tree, the inner 8×8 corner of each 2×2 section lies under the base. Remedy is a notch or a ring-centre offset — Q13.
3. Everything under the branches is ≤10 bricks — plantings inside r28 vs. height (mock: (2 + 10.5 × scale) studs → bricks).
4. The train's right-of-way is clear — planting discs vs. the 36–44 band.
5. The two sections' track meets — the existing endpoint match.
6. Grade and banking — NOT RUN until the railhead Z resolves; says so.
Verdict line: "Yes — every check that can run passes" / "Not yet — n of m checks block". Offending plantings glow block-red in 3D; the NE overlap is hatched in both views.

**Transforms (§4).** No separate 3D move tools — the operator judged them a duplicate of *Exact transform*, which remains the single way to move a section by number; dragging on the plan is the direct way. The proposal/restatement pattern (§5B) is still owed for AI-originated changes and lives in the planting ASK flow; the `proposalFor` helper and ghost outline stay in the code for that reuse.

**Announcement (tab):** Tab to 3D → polite: "3D view. {verdict}. Massing only; every dimension is real."

**Look presets.** AROUND (slow orbit, default) · ABOVE · ALONG TRACK · UNDER BRANCHES. Presets hold the camera; reduced-motion renders stills.

**Accessibility (§6, first pass — full retrofit in WP4).** Tabs are `role=tablist/tab` with `aria-selected`; the 3D canvas is `role=img` whose name carries the verdict and every blocking detail (the nonvisual alternative to the picture); the verdict line is `aria-live=polite`; the pending restatement is `role=status aria-live=assertive`; every move tool has a full-sentence `aria-label`. Announcement spec:
- Look preset → polite: "Looking {preset}."
- Any geometry change → polite verdict line re-announces only when its text changes.

**Mock boundaries.** Planting height formula, the 8 × 8 overlap sampling, the 36–44 band, endpoint tolerance 0. MOCK MATH — Claude Code + independent audit.

**Selection (operator ask 2026-09-17).** Either section can be selected: tap it on the plan (Enter/Space from the keyboard), or tap its name in *MILS units in the rig* (■ still toggles rig membership; SELECT/SELECTED sits at the row end). The selected section carries an accent outline in the plan and drives *Exact transform*. Section NE is the **anchor** this year — its numbers show read-only with a note pointing to Q13 (ring-centre offset) for moving the whole layout. Selecting a planting clears section selection and vice versa. Announcement: "Section NW selected. Drag it, use the arrows, or type exact numbers." / "Section NE selected — the anchor; read-only."

**Scene accordion (operator ask 2026-09-17).** Every sub-layer row expands: Planting to its proposals (unchanged); every other layer to its brick-level composition per section — name ×qty, colour, and a basis chip (■ OWN · ◆ ADAPTED · ◇ RESEARCH · ★ STORY) matching C-01. Counts are MOCK; C-01 owns the real BOM. The Separation tab still owes the same accordion.
