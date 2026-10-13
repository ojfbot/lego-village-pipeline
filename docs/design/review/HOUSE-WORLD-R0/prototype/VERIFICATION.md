# Browser verification — 2026-10-10 local / 2026-10-11 UTC

Built with `pnpm build` and served using `pnpm preview --port 4188`. Exercised the built artifact through the Playwright browser connector, using real rendered controls and the read-only `window.houseDemo` state/scene diagnostics. Screenshots were inspected after the model conversion and responsive checks.

| Scenario | Observed result |
| --- | --- |
| Supplied GLB rendering | Initially failed visually despite a successful parse. Found animated zero-scale starting poses; froze the assembled pose and rebuilt PBR colours. Final house visibly rendered, with zero collapsed node scales and no exported animations. |
| Pointer roof selection | Projected Block 22’s roof through the real scene camera, hovered and clicked it. Label and opened sheet both identified F8 / How agents work. |
| Full journey | Work box → book → 18-stud measurement → 9-stud offset → fit check → initialled parts review → H-01 completion. All shared-state transitions observed. |
| Earlier readings | First confirmed change retained 16. Subsequent what-if retained 18 as well, yielding `[16,18]` with the new reading 20. |
| Dependency invalidation | What-if after approval reopened the layout check and parts review. Receipt/inventory state remained unchanged. |
| Camera return | Before and after room entry, camera and target matched within floating-point rounding. |
| Keyboard return | Closing M-01 returned focus to its Block 3 page-list button. Start-demo entry returned focus to Start demo. |
| Return to caller | A-01 → return to M-01 restored focus to the original A-01 link and retained caller scroll. |
| Dialog and Benny focus | Focus stayed within the sheet; Tab from the final visible Benny form control wrapped to the sheet’s Back button. Escape first closed Benny, then the sheet. |
| Deep link and browser Back | `#M-01` opened the sheet. Browser Back after closing reopened it without adding an extra navigation entry. |
| Reduced motion | Emulated `prefers-reduced-motion: reduce`; camera entry completed immediately rather than running the 750 ms flight. Manual motion off also removes sheet transitions. |
| Lite mode | 21 destinations remained. 52 unselected draw calls, 708 triangles. Starting with `?lite=1` made no GLB request. |
| Failed detailed asset | Aborted the GLB request. Lite house remained usable; M-01 opened and its input worked. |
| 2D fallback | `?no3d=1` did not create a renderer. List navigation opened M-01. Quality toggle caused no exception. |
| Idle rendering | Frame counter increased by zero across a 1.2-second idle interval. |
| Story gate | Attempting to show a story before the local-session checkbox kept the recorded story empty. After choosing it, the exact typed words were retained. |
| Compare-before-share | Shared preview was disabled until both sample stories were heard. Both original model/story panels remained after preview. |
| Scripted AI | Benny’s model-meaning reply asked the builder to point to the relevant part and explicitly left meaning to the builder. No state editing or AI service request occurred. |
| Responsive layout | At 390 × 844, document width was 390; sheet client/scroll width both 390. No horizontal overflow in the checked views. |
| Build | Succeeded. Vite’s large-chunk advisory remains an explicit performance limitation. |

A deliberately aborted GLB request produced the expected browser network error during that test. Normal loads had no application exceptions; an earlier missing favicon was corrected.

These checks establish a runnable interaction prototype. They are not an accessibility conformance audit, real family co-design study, real math verification, multi-browser signoff, or performance test on a low-power device.

## PLAY WELL scroll revision

Built and exercised the updated served artifact in desktop Chromium (1440 × 960) and a responsive 390 × 844 viewport. These observations supersede the original motion defaults above.

| Scenario | Observed result |
| --- | --- |
| Scroll route | Inspected actual renders at 0, 18, 28, 40, 54, 61, 69, 85, and 100 percent. Lobby and tree remain visible through the exit; final view faces the assembled front. |
| Rear obstruction | Initial route entered a descending rear room at 61 percent. Delayed rear assembly; repeated 58, 61, 64, and 67 percent views showed the exit clear of that solid-wall obstruction. This is visual route verification, not a general collision solver. |
| Reverse scrolling | Returned from 70 to 28 percent. Camera coordinates matched the prior 28 percent sample exactly. |
| Sheet return | Opened M-01 at 28 percent, then Escape. Camera delta `[0,0,0]`, scroll delta `0`, focus returned to the same room-list button. |
| Still view | Froze at 28 percent and scrolled to 70. Camera delta `[0,0,0]`. Follow scroll resumed the route. |
| Reduced motion | Browser emulated reduce preference before navigation. Scrolled from 0 to 60 percent; camera delta `[0,0,0]`, still state true. |
| Keyboard route | End on the range control reached 100 percent and announced the final chapter through aria-valuetext. |
| Pointer destination | Clicked the actual projected Block 22 roof in the final assembled view; F8 / How agents work opened. |
| Idle renderer | No additional scene frames over 1.2 seconds after movement settled. GSAP still has its own timing machinery; this observation concerns Three.js renders. |
| Playable work | Repeated box → book → width 18 → clear offset → check → initials → completion. What-if changed width to 20, retained `[16,18]`, reopened checked/approved flags. |
| Mobile layout | Document width 390 at viewport width 390, one H1. Revised wordmark bounds x25.5–350.6 fit the viewport. Sheet fills the narrow viewport and scrolls. Canvas touch-action pan-y; wheel over canvas scrolled the document by 750px. Real touchscreen/Safari behavior remains untested. |
| 2D fallback | Rechecked the new room drawer with no3d=1; M-01 opened and its measurement control remained usable. |
| Errors | No page exceptions during the return, reverse, still, and keyboard route check. Two automation attempts used incorrect locators (multiple search matches; handoff already opened automatically) and were corrected; both completed checks passed. |

A numerical sample of the route at 2,000 equal progress increments found maximum camera step 0.03245 scene units, maximum gaze turn 0.3044 degrees per increment, and minimum gaze distance 1.054 scene units. These describe curve continuity; they are not measured frame rates or evidence of motion comfort. The user must judge the choreography. Detailed geometry remains 232,625 triangles when fully visible, and Vite continues to warn about the approximately 821 KB JavaScript chunk.

## Tree assembly and preview work reduction

The refreshed GLB has eight separate supplied tree pieces. Screenshots at 28, 36, 43, 49, 53, and 65 percent showed staggered settlement. At 53 percent every part position exactly matched its saved home transform; a 43 → 53 → 43 sequence reproduced all eight part positions and assembly fractions exactly. The lite scene exposed eight procedural pieces with the same completion behavior. Emulated reduced motion preserved all tree transforms while scrolling. Source SHA-256 matched the retained original.

Pointer selection of Block 22 still opened F8. Broad-phase picking narrowed that tested ray to four candidate rooms out of 21 and excluded floor/glass/tree geometry. Repeated paint requests were coalesced: a short navigation/entry sample recorded 20 requests and seven actual scene renders. Idle added zero renders over 1.2 seconds. No page exceptions occurred during the tree reversal, pointer-selection, and render scheduling check. The caption returned correctly after entering and closing M-01.

A 100-frame scripted 20–50 percent scroll on Chromium/ANGLE Metal Apple M3 Max at DPR 1 measured requestAnimationFrame interval median 8.3 ms and p95 9.4 ms before these changes; after, median 8.3 ms and p95 9.1 ms. The near-identical result does not support a meaningful FPS improvement claim. These are browser frame intervals under this short script, not isolated GPU render times or a test of the user's in-app browser. The changes remove redundant work; portable efficiency requires the research described in RENDER-RESEARCH.md. The detailed final view now has 94 draw calls and the same 232,625 triangles.

## Low pivot and early assembly revision

Actual Chromium renders were inspected at 22, 35, 40, 44, 48 and 55 percent. The low turn faces the smaller tree and then pulls back to the reference composition. Numerical comparison against saved pre-detour samples found zero camera-position and lens delta at 0, 10, 28, 54, 55, 60, 69, 85 and 100 percent.

The derived GLB now exposes eight tree and fifteen stair pieces, including transparent supports. At 18 percent the lower tree and all stair pieces had already begun a gentle drift; by 22 percent every tree layer was moving. At 51 percent all tree/stair transforms were seated. A 40 → 55 → 40 scroll sequence reproduced all piece transforms, assembly fractions and camera position exactly. Still and emulated reduced motion froze the camera and both assemblies while scrolling. Lite mode exposed the same piece counts and completed the assembly. No page exceptions occurred. Source SHA-256 remained unchanged. The final detailed view now uses 108 draw calls / 232,625 triangles; the GLB is 691,456 bytes. Earlier measurements above document prior revisions.

## Final motion correction and room autocomplete

The user reported excessive whip in the low-pivot experiment. Removed that detour and its gaze/lens override, returning to the original broad interior arc. Inspected actual renders at 28, 40, 48 and 55 percent; the camera remains nearly level during the circle and tree/stair assembly keeps its extended easing schedule. The prior detour observations above are historical.

Hailstone’s local search component informed the input/suggestions pattern. The final choice places the input directly in the header. Verified the following using real Chromium UI interactions:

- Empty focus listed all 22 destinations. M01 matched only M-01; “story model” matched F5. Literal `[` produced zero matches and a visible no-results explanation, without an exception.
- ArrowDown set aria-activedescendant while DOM focus remained in the combobox. ArrowUp from no selection reached the final work-box option and scrolled it into view; another ArrowUp selected F8. Home/Shift+End retained native input selection.
- Enter opened M-01; Escape from the sheet returned focus to module-search with the query retained, zero scroll delta and identical camera position.
- Tab after selecting a “parts” suggestion moved to View options, collapsed the popup and opened no sheet. Escape dismissed suggestions while retaining text and input focus. Outside click also dismissed them.
- Pointer selection opened the supplemental BOX sheet. The same action worked at 390×844; document width stayed 390, the popup occupied x=20…370, and the input font was 16px.
- With no3d=1, typing M01 and Enter opened the working measurement sheet. No WebGL renderer was created.
- No page exceptions occurred during these checks. Manual VoiceOver/NVDA and physical touch-device verification remain outstanding.

## Continuous start and larger wordmark — latest revision

The user requested movement from scroll zero instead of staggered start points. Replaced start thresholds with zero-velocity sine curves and different completion times. At 1 percent, all eight tree pieces and all fifteen stair pieces had nonzero assembly fractions. All were seated by 51 percent. Inspected actual renders at 0, 4, 8.5, 28, 40 and 61 percent; the tree circle and rear passage remain visible.

At scroll zero the desktop title scale was 1.32. At 4 percent it had shrunk partway and showed the warm/blue gradient; at 8.5 percent scale was 1 with opacity 1. At 13 percent opacity was about .394; at 18 percent it was zero. A 4 → 60 → 4 sequence reproduced the camera, both assemblies, title transform and gradient exactly. Emulated reduced motion froze the camera, both assemblies, title size and gradient while scrolling.

At 390×844 the larger title stayed inside the viewport (x=23.85…364.41) and document width remained 390. The header’s combobox/listbox/options and result status were present in the accessibility snapshot, with one document H1. Returning from M-01 at 55 percent retained camera, scroll, query and input focus. A browser-restored reload at 55 percent now synchronized the scene to that scrollbar position; an initial reset found during verification was corrected. No page exceptions occurred during the continuous-motion sample. Earlier timing observations above describe superseded revisions.

## Building courses, tree seating and quieter scene

The derived GLB exposes 77 wall/roof courses across all 21 blocks (103 mesh groups total). At 1 percent every course was moving; by 60 percent every course exactly matched its home transform. A 28 → 61 → 28 sequence reproduced all course transforms. Reduced motion froze them; lite mode exposed all 77 courses and completed them. Pointer selection still opened F8, and header autocomplete still opened M-01. Sample figures now move with their roof course; broad-phase bounds include the assembly envelope.

Tree layers now remain on their assembled horizontal axes and descend vertically, while the side leaf approaches along the outside branch axis. The final 2.5 percent of each part’s timeline is a short seating stroke. In actual scene samples at every 1 percent from 0 through 51, each stacked pair’s vertical spacing stayed at least as large as its final assembled spacing (minimum extra gap 0). All transforms matched home at 51 percent. This checks the authored stacked-layer path; it is not a general collision-simulation guarantee. Inspected actual tree renders at 28, 36, 40 and 46 percent.

The full-screen wipe was reduced after user review. The current scale is 1.75 desktop / 1.18 mobile. In that iteration, scene captions, deck copy, start-demo button and floating footer were removed. The next section records the subsequent caption restoration. Flight slider and Return to the start work from View options; the BOX sheet opens from the header finder. Document width remains 390 at 390×844. No page exceptions occurred in the quiet-scene control and sheet checks.

Current detailed final view: 172 draw calls / 232,625 triangles. GLB: 756,868 bytes. Source Blender SHA-256 still matches the original. Build passes with Vite’s existing large-chunk advisory. Earlier counts, title sizes and timing measurements above are historical.


## One caption at a time and bubble accents

Built with `pnpm build`. Tested the built artifact with real browser scrolling at 0%, 16%, 20%, 31.5%, 33.9%, 34%, 36.5%, 44%, 51%, 55%, 86%, 90% and 100%. Caption opacity is zero at each title-change boundary, reaches one within its chapter, and the opening caption stays hidden while PLAY WELL is visible. There is one caption element. Opening the room finder hides it; Enter on A01 still opens the full sheet. Computed room and sheet title fonts are DynaPuff.

At 390×844, document width is 390 and the M-01 title fits within the sheet. Reduced motion keeps the caption transform at the identity matrix. The document retains one H1. Inspected desktop tree-caption, finder, sheet and mobile-caption captures. This is browser verification, not a physical screen-reader test.

## Opening sunrise wash

The transparent WebGL canvas reveals a scroll-driven yellow and off-yellow radial horizon. Its cosine ease starts at zero, peaks at 5.5% scroll and returns to zero at 16%, before the lobby caption enters. Inspected 0%, 2.5%, 5.5%, 10% and 16% and the peak screenshot. Reduced motion retains the current wash, and reversing to 5.5% restores the identical gradient. This adds no scene geometry or lighting pass.


## Clean caption panels

The caption panel now uses an even backdrop rather than a gradient edge. Copy is shorter and the panel sizes to its content. All four visible chapter titles and descriptions each fit on one line at desktop 1440px, mobile 390px and narrow mobile 320px. Text can still wrap when needed at larger text sizes. The opening sunrise behind the house is separate and remains in place.


## Six haiku lines and yellow lettering, current

`pnpm build` passes with the 5–7–5 / 5–7–5 copy gate. Exercised negative cases: five chapters, a four-syllable first line, and an unreviewed word each throw. The pronunciation ledger covers this deliberately chosen copy; it does not claim automatic pronunciation of arbitrary English.

Scrolled to each visible chapter at 20%, 28%, 39%, 52%, 70% and 92%. All six labels and haiku lines render at full opacity and remain one visual line at 1440, 390 and 320px viewport widths. The five change boundaries at 25%, 34%, 46%, 58% and 86% each have opacity zero. Changing composition and entering/returning from M-01 retain the haiku instead of overwriting it with navigation instructions. The flight slider’s accessible value includes the current poem line.

The stage background contains only its original blueprint grid. Inspected the pale-yellow lettering at 4.25% and all six captions after the full supplied model finished loading. Camera and assembly curves are unchanged.


## Compact opening, current

`pnpm build` passes, including the six-chapter 5–7–5 / 5–7–5 gate. Inspected the full supplied model at opening, 4%, 8%, 12%, 18% and 28%, then desktop 1440×1000 and mobile 390×844 first-load frames after the projection correction. Mobile document width remains 390. The opening model fits in the viewport.

Scrolling 8% → 40% → 8% restores identical camera, course and minifig diagnostics. Reduced motion retains the camera while the scrollbar moves. Sampling the camera just before and after the 18% join, at ±0.000001, changes position by 0.0000323 scene units and target by 0.0000113. Opening room/course spreads start at 0.4/0.2 and reach 1 at 16%. The later lobby and tree route points are unchanged.

First-load verification exposed a stale projection aspect ratio; adding aspect to the framing cache key repairs this. This is a layout and choreography check, not a measured GPU performance claim.
