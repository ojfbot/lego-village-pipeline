# The house at the drafting table

A runnable local proposal: the supplied LEGO House becomes a parallel entry to Drafting Table sheets. Choose a block, work on a 2D sheet, and return to the same view. The current revision is a PLAY WELL architectural poster with a scroll-driven drone route. Scroll into the lobby, follow a broad curve around the trees, exit at the rear, and swing around to face the front while the rooms assemble. The header’s Find a room autocomplete gives the same destinations by keyboard or without 3D.

## Open the demo

The running preview is **http://127.0.0.1:4188** on this computer.

| Direction | URL | Interaction |
| --- | --- | --- |
| House composition | http://127.0.0.1:4188/?variant=house | Begin with a tighter house; the rooms open for the same scroll flight. |
| PLAY WELL scroll flight | http://127.0.0.1:4188/?variant=exploded | Graphic landing → lobby → broad tree curve → rear exit → exterior return. Rooms settle as the camera clears them. |
| Builder landscape | http://127.0.0.1:4188/?variant=landscape | Compare separate models and their builders’ stories before previewing a shared concept. |
| Lite house | http://127.0.0.1:4188/?lite=1 | Simplified geometry with identical destinations; no detailed GLB download. |
| 2D fallback | http://127.0.0.1:4188/?no3d=1 | Static model image and direct sheet list; does not create a WebGL renderer. |

The requested scroll flight is enabled unless the system requests reduced motion or the URL includes `motion=off`. View options → Still view freezes the current scene; Follow scroll resumes at the current scrollbar position. The range control provides keyboard seeking. Motion uses direct scroll scrubbing, with no autoplay or trailing catch-up. Sheet entry keeps the camera fixed. Sheets also have hash URLs, for example `/#M-01`.

To restart from this directory:

```sh
pnpm install --frozen-lockfile
pnpm dev --port 4188
```

To run the built version:

```sh
pnpm build
pnpm preview --port 4188
```

Use another port if the existing preview is still running. This application binds to loopback. No external account or backend is required.

## Try the playable journey

1. In **Find a room**, type “box” and select **A box of work**. Open the demo box and read its instruction book.
2. **Bag 1 / M-01:** enter a sample base width, review the restatement, then confirm it. The earlier reading remains available.
3. **Bag 2 / A-01:** try a clear position and check the layout against that reading.
4. **Bag 3 / C-01:** inspect the parts and their basis, add initials, and record a demo review.
5. The handoff confirms the demo journey is complete. Try the wider-base what-if: layout and parts review reopen, earlier readings remain, and physical inventory stays unchanged.
6. Return to the house. The camera view and all tab-local work remain. Reload clears the sample work.

The work box is a separately marked `BOX` view entered through the Hub. **I-02 remains physical inventory boxes.** Numbered bags express a bounded order of work; exploded building modules express a system view. They are different relationships.

## What is working

- Real supplied geometry, 21 selectable blocks, hover identity, manual orbit/pan, scroll flight and assembly. Wheel/touch scroll follows the route; choosing a room opens its sheet without camera travel.
- Seventeen design-bundle destinations, four research destinations, and the supplemental work-box view. All have rendered sheets; the measurement/layout/parts journey shares interactive mock state.
- PLAY WELL graphic landing, two starting house compositions, the builder landscape, paper/blueprint sheets, still and reduced-motion views, lite geometry, and a static fallback.
- Three small procedural figures mark sample activity. They are **not live agents**. Benny is a labelled, scripted assistant that proposes questions or routes and cannot edit a sheet.
- Builder wording is retained verbatim in the tab. Sample models remain visible after a shared-concept preview. A human host, builder-owned meaning, and separate feasibility facts are visible in the interaction.
- One document H1, labelled landmarks and dialog, named controls, live announcements, focus containment, Escape, return-to-caller scroll/focus, browser history, and a keyboard page list.

## Model and performance evidence

The source is `legoHouse.blend`, SHA-256 `6c0f6f3bb757370979df0a7d6c5951df1f0ef51716f56412b9d2e55338cc0541`. It was opened without saving. `export_house.py` freezes the assembled pose, excludes the off-scene parts library, joins bricks into 77 movable wall/roof courses across the 21 building blocks, while preserving eight tree pieces and fifteen stair steps/supports, and exports a Draco-compressed GLB. Simplified PBR colours reproduce viewport diffuse colours; this is not a photoreal material conversion.

| Observed quantity | Result |
| --- | --- |
| Visible block groups | 21 |
| Exported mesh groups | 103, including 77 building courses, eight tree pieces and fifteen stair pieces |
| Uncompressed assembled GLB | 7,485,424 bytes |
| Compressed GLB | 756,868 bytes |
| Detailed scene, unselected | 172 draw calls / 232,625 triangles (final front view) |
| Lite scene | 77 simplified building courses, eight tree pieces and fifteen stair pieces |
| Pixel-density cap | 1.25 |
| Idle render work | 0 added frames over a measured 1.2-second interval |
| App JavaScript build | About 845 KB minified / 235 KB gzip, before server configuration |
| Active WASM decoder | 192 KB plus 58 KB wrapper, loaded for the detailed model |

Draco reduces transfer size; it does not reduce the detailed scene’s triangle count. The lite route avoids the detailed asset and decoding. The renderer has no continuous orbit or animation loop. The static PNG loads only when the fallback is shown. Vite emits a large-chunk advisory for the Three.js application bundle; the study is not a production performance signoff.

Testing used desktop Chromium and a 390 × 844 responsive viewport. Local model load/decode took roughly 62 ms in one warm loopback run; that is **not** a phone, cold-network, or frame-rate benchmark. Physical low-power phones, Safari, Firefox, thermal behaviour, and lost-context recovery still need device testing before making a broad compatibility claim.

## Design and research evidence

- [PR #44](https://github.com/ojfbot/lego-village-pipeline/pull/44), branch `corr/review-dt-design-r4`, reviewed at `b9867797e9c9b3ae869b0bd8d70698c0d9a12cab`: X-01 v2 identity/motion/categorization research, page index, tokens, Benny, W-00 frame, N-01/N-02 limitations. This remains a draft research overlay, not an operative handoff.
- H-01-R1 M-01, A-01, and C-01 behaviour specs informed the sheets. The frozen standalone implementation was not copied. This prototype uses deliberately simpler geometry and state than those specs.
- The local writing series’ “picture on the box / instruction book / numbered bag / step back” delivery vocabulary informed the guided journey. It is labelled as an experimental UX mapping.
- [LEGO SERIOUS PLAY research umbrella #33](https://github.com/ojfbot/lego-village-pipeline/issues/33) and issues #34–43 informed the family research destinations. The private selfco synthesis cited there was unavailable; no matching public selfco issue body was found. These are open research hypotheses, not accepted policy.
- [Official LEGO background](https://www.lego.com/en-us/themes/serious-play/background) and [open-source guide](https://www.lego.com/cdn/cs/set/assets/blt8ec1d6ff766ddfd4/LEGO_SERIOUS_PLAY_OpenSource_14mb.pdf) establish the method’s context. This app is a research adaptation, not an official workshop or evidence of effective AI facilitation.
- The user’s [gingerbread house inspiration](https://www.reddit.com/r/lego/comments/1wqtbhg/gingerbread_lego_house_my_moc_for_the_masterpiece/) informs visible activity around the house; its photograph is not the supplied model’s geometry.

The specific design decisions, research mapping, and alternatives are in `DESIGN.md`; browser observations are in `VERIFICATION.md`.

## Technical proposal

Start with **vanilla Three.js + GSAP ScrollTrigger + HTML sheets**, as implemented here. [ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/) synchronizes the camera, room assembly, title, and scroll position; Three.js supplies the geometry and continuous camera/gaze curves. React is unnecessary for this interaction. WebGL2 renders the house; HTML handles work, accessibility, and fallback. The scene and the sheets share identifiers, not canvas-based form controls.

| Candidate | Useful when | Trade-off for this prototype |
| --- | --- | --- |
| [Three.js](https://threejs.org/docs/pages/WebGLRenderer.html) | Importing the supplied glTF, camera controls, picking, and a small custom scene | More renderer code than a minimal wrapper, but ready-made [glTF](https://threejs.org/docs/pages/GLTFLoader.html), [picking](https://threejs.org/docs/pages/Raycaster.html), and [Draco](https://threejs.org/docs/pages/DRACOLoader.html) support. |
| [OGL](https://github.com/oframe/ogl) | A tightly controlled, shader-oriented scene with a small API | More custom work around asset loading, controls, and interaction. A smaller API alone does not establish a faster application. |
| [Babylon.js](https://doc.babylonjs.com/features/featuresDeepDive/importers/glTF/) | Richer scene behaviour, simulation, or editor tooling | Investigate its [tree-shaking imports](https://doc.babylonjs.com/setup/frameworkPackages/es6Support/treeShaking/usingPureImports/) against a real slice before choosing it. |
| [PlayCanvas](https://developer.playcanvas.com/user-manual/engine/supported-browsers/) | A game-like world and a scene-production workflow | Larger workflow change; its WebGL2/browser support still requires fallback/device checks. |

The next technical design should specify the routing boundary to the real sheets, model asset budgets and mobile quality policy, scene lifecycle, stable artifact identifiers, separate evidence axes, and production storage. It should also test whether people actually find work more easily in the house. The 2D Hub remains the direct entry.

## Limits and disposition

This is retained as a **marked local prototype**, at the user’s request for a runnable review artifact. It is not committed as a production implementation, deployed, or attached to a new PR. The only tracked repository edit is the required deviation log in `implementation-notes.md`; source code and assets live in this artifact directory. Browser tooling also writes temporary review captures in the checkout.

All counts, measurements, prices, fit tests, stories, receipts, approvals, and activity are **MOCK MATH / fictional demo state**. No live agents, durable evidence records, purchase, publishing, or authoritative merge exists. A 21-room map can still be harder to learn than a list. Test destination-finding and recall before expanding the spatial metaphor.

## Review feedback — 2026-10-10

The user rejected the dashboard-portal visual direction and reported nausea from the transitions/discontinuities. The first corrective revision disabled motion and kept the camera unchanged on sheet entry. Verified no camera displacement and a zero-second sheet transition. The subsequent revision implements the user’s confirmed PLAY WELL wordmark and explicitly requested scroll drone choreography. This supersedes the original portal composition; the report of nausea remains the reason for direct scrubbing, fixed-camera sheet entry, and an accessible still alternative. The current proposal still awaits visual review.

## Scroll choreography

`flight-path.js` owns a continuous position spline, a corresponding gaze spline, and a monotone clock that gives the interior more scroll space. The lens widens through the lobby and returns to an exterior view. `world.js` derives every room transform from the same progress; the rear rooms wait until the camera clears the facade. The scroll sequence occupies eight viewport heights. `app.js` uses `scrub: true` and a native scrollbar, so reverse scrolling reconstructs the same scene. There is no physics engine or free-flight collision system. The supplied model’s interior and materials are approximate browser conversions, and glass sorting remains visible in close views.

The latest design plan is in `LANDING-DIRECTION.md`. Screenshots in `review-captures/` show the opening, interior, exit, assembled front, responsive layout, and a sheet beside the house.

## Tree assembly and preview rendering

The supplied Int Tree collection contains eight parts across the two lobby plants. The browser copy now preserves those pieces. Every tree and stair piece begins moving from scroll zero, with zero initial velocity. Tree layers remain aligned above their connectors; the side branch approaches horizontally from outside. The final 2.5 percent before each tree piece seats is a short stud-connection stroke. Different completion times stagger the motion without delayed starts: tree bases/stem seat first, and the last canopy layer seats at 50.5 percent, and stair pieces between 35 and 46.2 percent. Rooms also begin from zero, using slightly different horizontal/depth/height rates. Rear rooms make a small early drift before completing their descent as the camera clears them. The camera’s initial approach eases out of rest; the interior remains one broad curve. All are seated before the rear exit; reverse scroll restores the prior partial assembly. The lite scene runs the same choreography with simple procedural parts. The source Blender file remains unchanged.

Preview optimizations coalesce render requests into one paint per browser animation frame, reuse room bounds for pointer broad-phase picking, avoid repeated hover redraws and chapter text replacement, cache viewport/framing data, and cap pixel density at 1.25. These reduce avoidable work without establishing a portable FPS improvement. Preserving building courses, tree and stair pieces increases the final detailed scene from 88 to 172 draw calls; its triangle count is unchanged. This is an explicit animation/performance trade-off to examine in render research.

`RENDER-RESEARCH.md` holds the proposed research task for the real implementation. It is a local task brief, not a filed GitHub issue or an accepted technical design.

## Room autocomplete

Find a room is an editable input directly in the header, following the user’s final placement choice. Focus it to browse all 22 destinations, or type a title, action or page code. Codes such as M01 also match M-01. Multiple words may appear anywhere in the destination text; code/title matches rank first. Query characters are treated as literal text.

Arrow keys select a suggestion while focus stays in the input. Enter opens the selected room (or the sole match). Escape dismisses suggestions without clearing the query. Tab leaves normally and never opens a room. Pointer/touch selection opens the same sheet, and closing it restores query, focus, scroll and camera. Mobile uses a 16px text input and a viewport-contained popup.

The starting interaction was inspected in [Hailstone’s search component](https://github.com/ojfbot/hailstone/blob/main/src/scripts/components/_searchBar.js) in the local checkout. This version uses explicit combobox/listbox/option semantics and active-descendant focus per the [WAI-ARIA combobox pattern](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/). Hailstone’s Tab-to-select and raw regular-expression matching were replaced. Keyboard and DOM checks pass; physical screen-reader testing remains to be done.

The requested ground-pivot experiment was subsequently removed after the user reported excessive whip. The current route restores one broad interior arc, nearly level height, a steady tree-facing target and the original lobby lens. Early tree/stair assembly remains.

## Continuous opening parallax

All animated parts now begin from the first scroll, easing out of rest. Different room-axis rates and piece completion times give staggered depth while keeping the scene reversible. No timer or trailing scrub drives the geometry. The initial camera approach is slower; the tight ground pivot remains removed.

PLAY WELL begins 75% larger on desktop (18% on narrow screens), shifts through a cream/brick-red gradient while shrinking into its prior placement over the first 8.5% of the route, then fades from 9–16% before the lobby. Still/reduced-motion freezes its size and gradient alongside the scene; opacity can still dismiss the title.

## Quieter scene and internal building assembly — current

The full-screen wordmark experiment was scaled back after user review. The view now has the wordmark, architecture and header controls. Chapter captions have returned one at a time, with scroll-owned fades between titles. Captions clear while the finder, View options or a sheet is open. Marketing copy and the work-box button remain off the scene; the box is available through Find a room. Room names and sheet accent headings now use the locally bundled DynaPuff bubble font. Flight seeking and Return to the start moved into View options. Loading status remains available to assistive technology.

The building’s 77 wall/roof courses begin easing from scroll zero and finish within their parent blocks by 59.5 percent, while those blocks continue assembling into the house. Sample figures follow their roof course. These are grouped source bricks, not independently simulated individual bricks. The source geometry is unaltered. Course count/extra draw calls are measured prototype costs to include in the implementation research.


## Strict chapter copy rule

Exactly six chapter labels, with one haiku line beneath each. Chapters 1–3 form a 5–7–5 English haiku; chapters 4–6 form the second. `pnpm build` runs `check-chapters.js`, which checks chapter count, order, line structure, reviewed word pronunciations and syllable totals. Unknown words need deliberate pronunciation review. The rule is also recorded in this prototype’s `AGENTS.md`.

| Chapter | Subhead | Syllables |
|---|---|---|
| Pieces at dawn | Loose bricks greet the dawn | 5 |
| Come on in | Soft light slips through open doors | 7 |
| Around the trees | Green leaves find their home | 5 |
| Step by step | Steps rise from the floor | 5 |
| Through the other side | Small rooms gather round the tree | 7 |
| One house, many builds | New worlds wait for hands | 5 |

The first caption appears after PLAY WELL fades. All six share one caption element, and text changes while its opacity is zero. The opening sunrise now transitions the lettering through pale yellow, with no background wash.


## Compact opening composition

The opening presents a compact exploded house beside PLAY WELL on desktop, and below it on mobile. Room separation begins at 40% of the former opening distance; wall/roof course separation begins at 20%. Both open gradually to the existing spread by 16% scroll, revealing the layers as the title settles and fades. The opening camera is pulled back and aims higher, with additional distance for narrow screens. Its extra offset fades out by 18%, rejoining the existing lobby route.

The wordmark’s initial scale is now 1.28 on desktop and 1.05 on mobile. Its pale-yellow transition, six haiku chapter lines, transparent captions and upright minifigs remain. First-load camera framing now includes aspect ratio in its cache key.
