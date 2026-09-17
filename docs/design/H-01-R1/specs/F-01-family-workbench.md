# F-01 — Family Workbench

**File:** `F-01 Workbench Junior.dc.html (rename file to F-01 Family Workbench)` · **Journeys:** J11 · O4 Dream it · **Status at handoff:** built at tablet fidelity; iPad/iPhone responsive not designed
Behaviour reference is the live prototype; its code is not to be copied. All numbers are mock pending real math + audit.

## Purpose
The boys use the real drafting tools at tablet density to propose a scene. A scene is a real layout branch (origin family · status proposed) that **claims envelopes** on the table, with consequences worked out before it reaches James as the same request card C-01 answers.

## Schema on this page
**Sticker** (the idea: kind, glyph, label, story) → **Envelope** (footprint in studs × clear height at that spot) → **Model** (Studio file, photos, or wand proposal; must fit the envelope).

## Behaviour
1. **Pick a sticker** — one-row palette (Minifig 2×2 · Horse 2×4 · Lamp post 1×1/2×2 · Snowman 2×2/4×4 · Tree 2/4/6 · Building 8×8/8×16/16×16 · Train stop 4×16/6×16) each with heights in bricks; **✦ Something else** describes a new sticker (type/talk) → glyph and starting size inferred from words. Tapping a sticker **arms** placement (solid); one drop disarms; tap again to cancel. Default mode is select — tapping snow when unarmed never drops.
2. **Put it on the map** — controls as three equal segmented lines: SHOW (Rail · Tree · Stickers · Studs) · LOOK (Above · South · East · North · West) · ZOOM (Table · Closer · Studs; disabled in side views). A fixed-height status line gives feedback (flashes after actions with ↶ UNDO) and never overlays the map. Map = 112 × 112 studs to scale, stud rings at every zoom, 4- and 16-stud lines; R40 rail band 36–44 studs from centre; tree base (default 32×32) fixed with a dashed branch-overhang circle and headroom figure. Gestures: tap snow → drop (when armed) · tap sticker → pick · tap picked sticker or empty snow → put down · drag sticker → move · drag orange corner handle → resize (1–32 studs) · drag empty ground → pan when zoomed. Ghost preview follows the cursor while armed (orange fits / red blocked). Cursor: copy · not-allowed · grab · grabbing · nwse-resize · default. Blocked: tree base, other stickers. Flagged (not blocked): rail overlap → fit check; too tall under branches → height warning. Side views draw the table in bricks: base, trunk, cone, rails + train envelope, headroom line, brick courses, stickers as boxes (nearer in front, too-tall red).
3. **Tell its story** — scene name + what happens (type/mic).
4. **Model it** — three flat tinted cards on one row (2+1 landscape when narrow): Build it in Studio (Open Studio · Attach .io) · Build it for real, then photograph it (Add photos) · Try the magic wand (mock: staged status → 3 precedents → proposal; keep / try again). Copy frames the wand as a starting point the builder owns.
- **Right column**: What your scene would need (per-sticker rows, selectable → highlights on map; readouts bricks · envelope studs · track? · envelope height) · **Selected sticker card** (persistent; empty state explains) with ITS STORY (who/what + what it does, mic), FOOTPRINT presets, # × # CUSTOM popover (1–32 steppers, fit note), ↻ Turn it, Take it off · Send it to James → (needs ≥1 sticker and a name) → ◇ SENT · PROPOSED with the request-card preview (FROM · ASKS · CLAIMS · ATTACHED WORK · ORIGIN · STATUS).
- **Action log**: every place/move/resize/turn/remove/sticker/model/send/reset is recorded with time; collapsed "WHAT HAPPENED · n" strip; UNDO restores the previous sticker state and is itself logged.
- **Tweaks**: theme; tree base / height / base height / canopy radius / canopy bottom (◇ to be measured).

## Copy rules
Plain, never talking down (ages 9.5–11). James named sparingly (the send button, the request card); the family never addressed as children. "Rail" is a placeholder (RESEARCH-01).

## Not done
Responsive layouts for iPad portrait and iPhone; pinch zoom; keyboard placement; real wand backend.
