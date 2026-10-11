# The house as an entrance to the drafting table

HOUSE-WORLD R0 is an additional experimental design package from the Codex prototyping session, governed for review by HANDOFF-LEGO-PIPE-037-R0. James allocated both identities on 2026-10-11. This starts a separate lineage. It neither supersedes DT-DESIGN nor imports the incomplete R4 overlay.

**Status: runnable mock prototype plus proposed next design work.** A schema-valid manifest or a passing structural preflight does not approve this design, authorize production work, or create an accepted instrument pin. James reviews the PR. The existing build work orders and frozen H-01 package retain their authority.

## Start here

1. Open [the illustrated overview](overview.html). It distinguishes the current browser prototype from the proposed dashboard threshold.
2. Read [navigation](specs/navigation.md) and [dashboard space](specs/dashboard-modal.md).
3. Run the prototype from the repository root:

   ```sh
   pnpm --filter house-world-study install --frozen-lockfile
   pnpm --filter house-world-study build
   pnpm --filter house-world-study preview --port 4189
   ```

4. Open `http://127.0.0.1:4189/?variant=exploded`. Scroll from the start, open a room with the header input, and return to the same scene position.
5. Follow [verification](verification.md) before extending the study. The current side sheet is an observable limitation, not the desired dashboard layout.

`prototype/` is a pnpm workspace member for reproducible execution. It is design-reference code, not a proposed production package boundary. The root lockfile governs installs. Its original standalone lockfile is retained as provenance, not a second active dependency resolver.

## What runs today

- Vanilla Three.js and GSAP ScrollTrigger render a derived glTF of the supplied LEGO House model. HTML holds the room finder, working sheets, focus and announcements.
- The compact exploded opening separates the house from PLAY WELL. Rooms begin at 40% and wall/roof courses at 20% of the previous spread, then reveal their layers during the opening approach. A wider camera joins the earlier lobby flight at 18% scroll.
- Scroll drives one broad lobby/tree arc, rear exit and return to the front. There is no autoplay or additional tight pivot. Reversing the scroll reverses the same scene state.
- Twenty-one mapped building blocks reach 22 mock destinations. BOX is a work-box study under the Hub; it is separate from documenting physical inventory boxes.
- Seventy-seven wall/roof courses, 15 stair pieces and eight tree pieces move. These are grouped courses, not individual building bricks. Tree seating follows the supplied connection axes, with a short final seating stroke. It is authored choreography, not a general collision solver.
- Three sample minifigs stay world-up while attached to moving roofs. They denote fictional activity, not running services or autonomous authority.
- The header autocomplete has literal token matching, keyboard active-descendant navigation, Enter activation, Escape dismissal and normal Tab behavior. Focus stays in the input. Hailstone supplied the interaction precedent; its raw-regex and keyboard traps were not reproduced.
- One tab-local demonstration connects a work box, an instruction book, numbered bags, a reading, a layout check and a parts review. A changed reading retains the earlier value and reopens its dependent checks; physical inventory remains separate.
- Six chapter labels have one haiku line each. Chapters 1–3 form 5–7–5, as do chapters 4–6. `check-chapters.js` enforces the count using reviewed pronunciations before a build. Bubble type is an accent; values, forms and body copy remain readable UI text.
- Captions have transparent backgrounds and text shadows. Pale yellow travels through the opening letters of PLAY WELL. The scene backdrop remains the blueprint grid. View controls live in View options.

## What agents must design next

| Area | Current behavior | Next requirement |
|---|---|---|
| Room flight | Selecting a block opens a sheet immediately; camera stays fixed | Explicit, cancellable flight between blocks and safe room thresholds |
| Dashboard space | Left side sheet consumes about 57% of desktop width | Near-full-screen modal, with the frozen house ghosted behind it and the sheet's intended dashboard space restored |
| Finder preview | Active row highlights its room | Read-only page preview on focus, with a clean expansion and no automatic camera travel. Final preview placement remains open. |
| Parallax | Camera, room axes and assembly have different scroll rates | A small number of deliberate depth layers, with comfort review and reduced-motion equivalents |
| Background | Flat blueprint grid | Compare restrained background treatments that keep room identity, text and depth legible |
| Rendering | On-demand rendering, grouped geometry, capped pixel ratio | Measure the asset and draw-call budget on actual devices before choosing instancing, merging or levels of detail |
| Research | Scripted build/story/compare examples | Evaluate the methods and consent model with humans; do not infer meaning from geometry |

These are design and prototype slices. Storage, durable history, evidence schemas, permissions, production routing, real agents and procurement gates need separate technical design and existing authorization gates.

## Package contents and source boundary

- `package.yaml`, `index.json` and the package-local `decisions.md` follow `design-package/v1`.
- `prototype/` is the runnable session snapshot. Its earlier notes describe intermediate revisions and are evidence, not current instructions. This README and `specs/` describe this cut's current state and next requirements.
- `assets/blender/legoHouse.blend` is the exact supplied source. `legoHouse.blend1` is its exact matching backup. Both contain 1,459 objects, including 1,457 mesh objects, and neither has linked Blender libraries or external images. See [asset provenance](assets/README.md).
- `assets/manifest.json` records byte sizes and SHA-256 hashes. No source file is resaved. The browser uses the derived `prototype/house.glb` rather than loading Blender files.
- `references/` contains selected unchanged Claude R4 source/spec excerpts at PR #44 head `b9867797e9c9b3ae869b0bd8d70698c0d9a12cab`, plus research issue metadata and body hashes. This does not reconstruct the missing overlay parents or make those sources runnable.
- `fixtures/session-fixtures.json` contains the initial mock state and page map. All work quantities are MOCK MATH. File sizes, hashes and renderer diagnostics are measured artifact facts.

The authoring schema is `tools/schemas/design-package.v1.schema.json`. The correspondence schema is `tools/schemas/lego-pipe-memo.v2.schema.json`. The sibling receipt identifies this package's exact tree; a directory name alone is never its identity.

Use `python3 docs/design/review/HOUSE-WORLD-R0/tools/verify_received.py` to check the committed source snapshot against that receipt. This materializes Git's received tree in a temporary directory so ignored `node_modules` and `dist` output cannot change the measured cut.
