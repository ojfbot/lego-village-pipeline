# Landing revision: an architectural play poster

The user endorsed the close, exploded architectural view and the proposed scroll reveal, then asked for a more graphic landing with bubble lettering. The current dashboard chrome competed with the geometry. This revision makes the house and its title the composition.

## Working plan

- Colour: blueprint navy #172B40, warm white #FFF4D6, brick red #FF533D, roof blue #4BADD1, leaf green #70AD72. Roof colours remain architectural. Drafting Table sheet tokens remain the sheet palette.
- Type: DynaPuff bubble accents for PLAY WELL, chapter titles, room names and sheet headings; plain small UI labels and body text. Type is the primary graphic intervention.
- Layout: one full-width sticky house scene across a short scroll sequence. A large two-line PLAY WELL wordmark sits at the left of the opening composition, a broad cropped house fills the right. The user confirmed this wordmark. The wordmark leaves the frame as scrolling opens the blocks. Find a room is an editable header autocomplete with a dismissible suggestions popup. Settings are a small second drawer.
- Motion: following the user’s subsequent explicit request, scroll position drives a drone path into the lobby, along one broad curve around the trees, through the rear, then around the exterior to face the front. Three.js splines set camera position and gaze; GSAP ScrollTrigger synchronizes the house assembly and title. No autoplay or trailing scrub momentum. Reduced motion and a Still view control preserve static scenes. Orbit remains an explicit drag action.
- Entry: selecting a room reveals a working sheet on the left in the wordmark’s space, keeping the architecture visible on the right. No camera relocation. Escape/Back returns to the exact scene and scroll position. Existing mock work and research interactions remain usable.

## Alternatives considered

A centred bubble wordmark above a complete model would leave the current poster looking like a generic title over a product hero. A wallpaper of floating bricks would obscure the supplied house and dilute its useful structure. The chosen asymmetrical composition puts the lettering and architecture in an active relationship, with the close exploded view as the second scroll chapter.

## Acceptance observations

Inspect the actual opening graphic, the exploded scroll composition, the scene beside a selected sheet, drawer and keyboard behaviour, mobile width, still/reduced-motion settings, and the existing three-bag demo. The user’s references will further shape the aesthetic; this revision is a concrete proposal, not visual signoff.

## Lobby assembly revision

All animated parts begin from scroll zero with a sine ease and zero initial velocity. Tree bases and stem seat before the canopy; the last layer seats at 50.5 percent; stair steps/supports span 35–46.2 percent. Room horizontal, depth and height rates differ slightly to add parallax; rear rooms drift only a little before their final descent, keeping the exit clear. The camera eases out of rest and retains one broad interior arc. The ground-pivot experiment was removed after the user reported whip. Every pose is derived from scroll progress; still view freezes it and reverse scroll reproduces it. Close glass sorting remains visible; this is authored choreography, not a collision simulation.

PLAY WELL opens 75% larger on desktop and 18% larger on mobile. Through the first 8.5% of the route it shrinks into its previous placement while the letters pass through a cream/brick-red gradient. It stays opaque during this settlement, then fades over 9–16%, before entering the lobby. Size and colour are frozen in still/reduced-motion mode.

## Header room finder

An editable search field now lives directly in the header. Its suggestions follow the Hailstone reference, with page code, title and action/status. Empty input offers all destinations; query filtering includes the supplemental work box. Focus stays in the input while arrows change the active option; Enter opens, Escape dismisses, and Tab leaves without committing. Room selection preserves the camera and returning from a sheet preserves the query.

## Latest visual correction

The full-screen letter wipe was too extreme, and overlay captions/buttons added noise. The current graphic is large but readable. Chapter captions have since returned one at a time, with a fade through zero at each chapter boundary. They clear while the finder, settings or a sheet is open. Floating flight buttons remain in settings. Flight seeking, restart and prototype notes sit in View options. The work box remains available through header autocomplete.

The building assembles in 77 grouped wall/roof courses, seating inside its parent blocks before the blocks reach their house positions. Every course starts from scroll zero and has a different completion time. Tree layers descend along their connection axis and finish with a short seating stroke; the branch leaf attaches horizontally from outside. The diagonal tree drift was removed.


An intermediate iteration tried a yellow/off-yellow horizon wash behind the house, which the user rejected. It peaks at 5.5% scroll and fades to the normal backdrop by 16%. The left side stays dark enough to hold PLAY WELL; reduced motion freezes the wash with the scene.


The caption panel now uses an even backdrop rather than a gradient edge. Copy is shorter and the panel sizes to its content. All four visible chapter titles and descriptions each fit on one line at desktop 1440px, mobile 390px and narrow mobile 320px. Text can still wrap when needed at larger text sizes. The later sunrise clarification moves the color transition into PLAY WELL’s lettering and removes the background wash.


The current chapter rule is six labels with subheads forming two 5–7–5 haikus in order. The poems are in README.md and are enforced before each build. The blue backdrop stays constant; PLAY WELL transitions through pale yellow during the opening scroll.


## Compact opening composition

The opening presents a compact exploded house beside PLAY WELL on desktop, and below it on mobile. Room separation begins at 40% of the former opening distance; wall/roof course separation begins at 20%. Both open gradually to the existing spread by 16% scroll, revealing the layers as the title settles and fades. The opening camera is pulled back and aims higher, with additional distance for narrow screens. Its extra offset fades out by 18%, rejoining the existing lobby route.

The wordmark’s initial scale is now 1.28 on desktop and 1.05 on mobile. Its pale-yellow transition, six haiku chapter lines, transparent captions and upright minifigs remain. First-load camera framing now includes aspect ratio in its cache key.
