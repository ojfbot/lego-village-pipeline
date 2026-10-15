# HW-01 rev 2 — The fly-through

Source: `sources/prototypes/House World.dc.html` (logic class) + `sources/prototypes/house/house-stage.js` (`<house-stage>`). Answers HANDOFF-LEGO-PIPE-037-R0 §2 and HOUSE-WORLD-R0 `specs/navigation.md`, `motion-and-background.md`. Prototype; all work is mock. Replaces R5's HW-01.

## 1. One camera owner

The camera is owned by exactly one of four modes; nothing else may move it.

| owner | who drives | enters when | leaves when |
|---|---|---|---|
| `tour` | scroll progress 0–1 on the R0 flight spline (ported verbatim) | page load; end of a blend | a flight starts (bookmarks pose + progress) |
| `flight` | a Catmull-Rom route over `flightSeconds` (centripetal) | activation of a room | arrival (→ `threshold`), Esc (→ tween to bookmark → `tour`) |
| `threshold` | held pose outside the room | arrival; Back from the dashboard | next scroll of > 0.002 progress (→ `blend`); "Back to the start" |
| `blend` | 700 ms ease from the held pose into the spline sample | leaving threshold | k ≥ 1 (→ `tour`) |

Scroll events are ignored while a room or a flight is active; `document.body.overflow` is hidden in both.

## 2. The tour

- Page height 600vh (`tourOn`); stage is sticky 100vh. Progress is quantised to 1/400 before it reaches React so the poster and captions don't re-render per pixel.
- Six chapters at progress 0 / .25 / .34 / .46 / .58 / .86 — *Pieces at dawn · Come on in · Around the trees · Step by step · Through the other side · One house, many builds* — each with its 5-7-5 line. Captions are hidden until 12 %, while the finder list is open, while flying, settled, or in a sheet. Each chapter title re-animates in (`hwCaption`, .5 s).
- **Poster framing.** While the wordmark owns the left of the screen the camera's view offset pushes the house right (`setViewOffset`, tour and blend only, viewports ≥ 740 px); the offset decays to 0 by 20 %. Wordmark scale 1.14 → 1 over 0–8.5 %, opacity 1 → 0 over 7–12 %; once past 12 % the poster is gone until the user is back under 0.5 %.
- R0 choreography kept: courses settle, stairs rise, tree fills in, the interior lights as the camera enters; roof colours come from the model (`roofs: model`) or flatten to grey — colour is never evidence or authority.

## 3. Pointing at a room (the hover card)

- The stage raycasts every pointer move; a hit resolves to a **room** (HW-02), never a bare block. Card shows `R-code · room title · KIND`, the room's "what", its sheet count and sheet titles, and `CLICK TO FLY IN`. The whole room's blocks highlight.
- **Hysteresis.** A change of hit must persist 45 ms to switch rooms and 110 ms to clear (so crossing a gap between blocks does not blink). A first hit from nothing commits immediately.
- **Follows the camera.** While the view moves (tour, blend, flight) the stage re-picks under the still pointer at ≤ 30 Hz so the card tracks what is really under it.
- **Settle rule** (`scrollHover: settle`, default). Any scroll of > 1 px dismisses the card and suspends picking; picking resumes 260 ms after the last scroll event and re-picks once. The alternative `live` keeps picking during scroll.
- **Placement.** Card is positioned directly on each event (no re-render); 16 px off the pointer, flipped left/up at the viewport edge, and it will never cover the ask bar — if it would, it moves above the pointer.
- Hidden while flying, in a sheet, or while the finder list is open (the finder's own highlight wins; ↑↓ highlights without moving the camera).

## 4. Room flight

Activation = click/tap a block, Enter on a finder row, Go in the ask bar, or the brand button (HUB).

1. Bookmark pose + progress + the activating control. Close the finder, clear hover, clear "settled".
2. Choose a style: `reduced` motion → `direct`; otherwise `flightStyle`. Announce "Flying to … Press Escape to stop." and show the status pill with **ESC · STOP**.
3. `flyTo(firstBlock, {style, pose, seconds, slide})`:
   - **liftoff** (default, P-R5-3) — rise to a plan view over the room, then the room's block **slides toward the viewer** (520 ms) while the others dim.
   - **exterior** — wide swing around the house, then descend to the threshold.
   - **lobby** — in through the front door. Rooms with `lobby: true` (R1) always use the fixed lobby pose (`position (.48,.58,.78) · target (−.23,.49,0) · fov 52`) at 1.3× the flight time, with no slide (P-R5-1).
   - **direct** — 10 ms tween, no slide.
4. Nothing opens until arrival. Esc / STOP cancels, un-slides (350 ms), tweens to the bookmark (600 ms), announces "Flight stopped. Back where you were."
5. Arrival → owner `threshold`, the stage **freezes** (no further frames), the dashboard opens on the chosen sheet (HW-02 §4).

## 5. Return

- **Back / Esc** closes the dashboard. If the sheet now on top lives in a different room than the one flown to (after Switch room), `landAt(room.block[0], lobbyPose?)` puts the camera and the lifted block outside *that* room first — so Back always lands where the open sheet actually lives.
- `returnPose: threshold` (default) — camera holds; the pill says *You're outside R-n. Scroll to keep flying through the house* with **↑ BACK TO THE START**; the next scroll blends back into the tour over 700 ms. `bookmark` — 900 ms tween to the saved pose and progress.
- Focus returns to the activating control, else the finder input — and the finder list does **not** reopen on that focus.

## 6. Equivalents

- Reduced motion (prop or media query) → `direct` style, smooth-scroll off.
- WebGL / three.js unavailable or the stage fails → `stagefail` → a room-list grid (R1–R8 cards with their sheets) replaces the canvas; every sheet still opens in the dashboard; the live region says so.
- No pointer: the finder (↑↓ ↵ Esc) and the brand button reach every room; Tab is contained inside the dashboard.

## 7. `<house-stage>` API (as implemented)

Attributes: `data-src` (metadata JSON; `house.glb` is looked for beside it).

| method | does |
|---|---|
| `setProgress(p)` | tour progress 0–1; from `threshold` a change > .002 starts a blend |
| `setRoofMode('model'|'grey')` · `setTheme(dark)` | roof colours; exposure/paving per theme |
| `highlight(blocks|null)` | outline a set of blocks (finder / hover) |
| `flyTo(block, {style, pose, seconds, slide}) → Promise<ok>` | room flight; resolves false on cancel |
| `cancelFlight(silent?)` | stop; tween to bookmark unless silent |
| `lobbyPose()` · `roomPose(block, style)` · `pose()` · `bookmark()` | poses |
| `freeze(on)` | stop/restart the frame loop while a sheet is open |
| `landAt(block, pose?)` | jump the held pose outside a room without animating |
| `returnFrom('threshold'|'bookmark', ms) → Promise` | after Back |
| `startBlend()` | leave threshold into the tour |
| `repick()` · `suspendHover` | hover under a moving camera / settle rule |

Events: `ready` · `stagefail {why}` · `roomhover {block, x, y}` (block null = cleared) · `roomactivate {block}` · `model {model: 'glb'}` (after `house.glb` is adopted in place — `Block_N` / course / stair / tree naming from R0's `world.js`, Draco-decoded, schematic hidden).

## 8. Variation controls (Tweaks on the root)

Room flight: `flightStyle` liftoff | exterior | lobby | direct · `flightSeconds` 0.4–3 (1.4) · `returnPose` threshold | bookmark · `motion` full | reduced. House: `tourOn` · `roofs` model | grey · `scrollHover` settle | live · `theme` blueprint | paper. Sheet: `ghost` scrim | blur | none · `modalInset` 0–80 (24) · `previewMode` inline | none.

## 9. Open

Supplied-model render budget (N-03); vector wordmark (HW-04 §7); depth layers / background comparison (037 §2.3); browser history; lost WebGL context mid-flight; rapid repeated activation; whether a flight should play on sheet-to-sheet switch (today: none); block 8 (D-17).
