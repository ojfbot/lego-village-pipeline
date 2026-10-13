# Pick up the current House World design in Claude Design

## Select the correct branch

Use repository `ojfbot/lego-village-pipeline`, branch **`corr/review-dt-design-r6`**, PR **#46**.

The delivered prototype is pinned at commit `4bf12c8370d341a2bd8d1094491e281ebd6637ec`. It is under **`docs/design/review/DT-DESIGN-R6-addendum/prototype/`**. The branch now carries this pickup guide as well.

PR #45 and branch `feat/house-world-design-brief` contain the earlier HOUSE-WORLD R0 study and model correction. Use them for history. Reading only that branch cannot reveal the R6 addendum. `main` does not contain these unmerged review artifacts.

If your connector reads branches by name, supply `corr/review-dt-design-r6` literally, including its slash. Read the files listed below from that branch. If it cannot access that branch, report the failed branch/ref operation. Do not conclude that R6 does not exist from a search of `main` or PR #45.

## Read in this order

1. [`docs/design/review/DT-DESIGN-R6-addendum/README.md`](https://github.com/ojfbot/lego-village-pipeline/blob/4bf12c8370d341a2bd8d1094491e281ebd6637ec/docs/design/review/DT-DESIGN-R6-addendum/README.md).
2. [`docs/design/review/DT-DESIGN-R6-addendum/changes.md`](https://github.com/ojfbot/lego-village-pipeline/blob/4bf12c8370d341a2bd8d1094491e281ebd6637ec/docs/design/review/DT-DESIGN-R6-addendum/changes.md), for fixes already implemented.
3. [`docs/design/review/DT-DESIGN-R6-addendum/review.md`](https://github.com/ojfbot/lego-village-pipeline/blob/4bf12c8370d341a2bd8d1094491e281ebd6637ec/docs/design/review/DT-DESIGN-R6-addendum/review.md), for gaps and required follow-up.
4. [`docs/design/review/DT-DESIGN-R6-addendum/follow-up-tasks.json`](https://github.com/ojfbot/lego-village-pipeline/blob/4bf12c8370d341a2bd8d1094491e281ebd6637ec/docs/design/review/DT-DESIGN-R6-addendum/follow-up-tasks.json), for dependencies, deliverables and acceptance checks.
5. [`docs/design/review/DT-DESIGN-R6-addendum/specs/responsive-and-navigation.md`](https://github.com/ojfbot/lego-village-pipeline/blob/4bf12c8370d341a2bd8d1094491e281ebd6637ec/docs/design/review/DT-DESIGN-R6-addendum/specs/responsive-and-navigation.md).
6. [`docs/design/review/DT-DESIGN-R6-addendum/verification.md`](https://github.com/ojfbot/lego-village-pipeline/blob/4bf12c8370d341a2bd8d1094491e281ebd6637ec/docs/design/review/DT-DESIGN-R6-addendum/verification.md) and its screenshots and browser evidence.
7. `docs/design/review/DT-DESIGN-R6-addendum/prototype/prototypes/House World.dc.html`, `prototype/prototypes/house/house-stage.js`, `prototype/prototypes/house/house-responsive.css`, and `prototype/dt/responsive.css`.

The [actual posted Codex review](https://github.com/ojfbot/lego-village-pipeline/pull/46#pullrequestreview-5498479017) is mirrored in `review.md` and the task briefs. You can pick up from those files if your connector cannot read PR reviews. This follow-up is a repository addendum and GitHub review, not a new numbered REVIEW memo.

The original received Claude R6 overlay is at `docs/design/review/DT-DESIGN-R6-overlay/`, with HW-01 through HW-04, the ask bar, shared theme script and rooms R1 through R8. Its bytes are frozen. Use the **addendum prototype** as the working source for this iteration. That source already incorporates the responsive, model-quality and navigation fixes.

## Verify what you received before redesigning

Start the house, confirm the full model loads, and open Layout Canvas with the finder. Inspect the phone dashboard and the desktop opening screenshots. Record the source branch, pinned commit and files you actually accessed in your first response.

The complete matched model pair is included:

- [docs/design/review/DT-DESIGN-R6-addendum/prototype/prototypes/house/house.glb](https://github.com/ojfbot/lego-village-pipeline/blob/4bf12c8370d341a2bd8d1094491e281ebd6637ec/docs/design/review/DT-DESIGN-R6-addendum/prototype/prototypes/house/house.glb)
- [docs/design/review/DT-DESIGN-R6-addendum/prototype/prototypes/house/house-metadata.json](https://github.com/ojfbot/lego-village-pipeline/blob/4bf12c8370d341a2bd8d1094491e281ebd6637ec/docs/design/review/DT-DESIGN-R6-addendum/prototype/prototypes/house/house-metadata.json)

Keep these files together. The GLB is 755,960 bytes, SHA-256 `7932e86c69229f78eed135163161e12ebf158f8d07c7eb57f527ae4f357bb140`. The JSON is 40,082 bytes, SHA-256 `a4fcf44231688102eceade279f490c216decc101061bcf88c5e108c519423a75`. Both source `.blend` revisions are included under `docs/design/review/DT-DESIGN-R6-addendum/assets/blender/`.

This pair already incorporates the bottom-step course correction. Do not apply that correction again or delete a source brick. Block 1 has three courses. The model has 76 building courses and 21 blocks. There is no Block 8 group.

The addendum source receipt is `docs/design/review/DT-DESIGN-R6-addendum-RECEIPT.json`. Its tree digest is `a47c4ecd9c98188b0a47158366928a0602a2c08c904818351a826567f316cafa`. Its manifest checks the transferred bytes. The `package.yaml` inside the frozen received overlay describes that older export, not the addendum's current runtime.

## Run or import the available source

With a checkout and Node available, run from the repository root:

```sh
python3 docs/design/review/DT-DESIGN-R6-addendum/tools/verify_bundle.py
pnpm --filter house-world-r6-addendum install --frozen-lockfile --ignore-scripts
pnpm --filter house-world-r6-addendum build
pnpm --filter house-world-r6-addendum dev --port 4200 --strictPort
```

Open `/prototypes/House%20World.dc.html` on that server. Port 4200 on James's Mac is a local preview, not a remotely accessible source for Claude Design.

If using the supplied archives, extract `claude-design-r6-pickup.zip` for the review source, tools, model and Blender assets under `lego-village-r6-pickup/`. It is a tracked review-source subset, not a complete repository clone. The companion `claude-design-r6-preview.zip` contains **`browser-preview/`**, a prebuilt copy for environments that cannot run the source build. Serve `browser-preview/` as the HTTP root and open `/prototypes/House%20World.dc.html`. A `file://` tab does not reproduce the model fetches or module loading. The source `three-modern.js` has package imports that require the Vite build; do not paste that file into an unbundled HTML document and replace the resulting failed model with boxes.

If the connector cannot fetch the binary GLB, use its direct raw download or ask James to attach the pickup ZIP. Identify binary-fetch access as the blocker. JSON-only access is not evidence that the model is missing. A schematic fallback may explain a load failure, but cannot serve as the visual baseline for this design iteration.

## Own this design round

For this Claude Design session, own the design specification and prototype iteration for all three priorities below. The owner roles in `follow-up-tasks.json` describe future engineering sessions. They do not prevent Claude Design from refining the designs now.

### First, robust Grid and Subgrid across all pages

Inventory every room sheet, standalone typology study, Workbench Frame and linked design-library page. State which source pages are unavailable. Define named regions, container-driven tracks and breakpoints. Preserve the different work skeletons and verbs. Align related title, content and status bands with subgrid.

Design expanded, collapsed, empty, error and loading states at 320, 390, 768, 1024 and 1440 pixels, plus short landscape, long labels and larger text. Bound intentional table or diagram scrolling. Review keyboard and reading order during reflow. Use R4 Typology Identity v2 and Workbench Frame as precedents, but improve their weak narrow-screen layouts rather than importing their fixed viewport assumptions.

### Second, navigation controls and state

Improve the finder preview, room selector, sheet tabs, direct page entry, stop, Back and Escape. Separate focus/preview from opening a page. Specify who owns the clicked block, current room, current sheet, bookmark, scroll progress and draft. Define touch and keyboard paths, iframe focus, browser Back, virtual keyboard behavior, interrupted flights and rapid activation.

Keep the house as a parallel entrance. A clicked block remains the destination, including Drafting Table. A person must be able to reach every page without completing the tour.

### Third, motion and transformation

Use the layout and navigation contracts to design card expansion, Grid/Subgrid transformations, finder previews, dashboard entry/exit, room switches and camera flights. Compare native View Transitions with transform/opacity approaches. Keep text readable, transitions interruptible and reduced-motion paths explicit.

Retain the simplified tour. Avoid whip turns, abrupt starts and focus-triggered depth changes. Audit wall/roof courses, stair/support pieces and tree pieces for alignment before seating and visible body intersections. Treat this as a transformation design/build task, not only a selection of easing curves.

Render efficiency remains a separate measured research task before production. Do not reduce model quality to avoid that research.

## Preserve the reviewed progress

- Use R6 interface behavior with the GPT-quality renderer and full corrected model.
- Retain the direct header finder, responsive house framing and near-full-screen dashboard. On phones the dashboard is edge-to-edge.
- Keep adjacent rooms opaque and geometry steady during focus. Keep scroll resumption after Back, including small deltas and page boundaries.
- Retain the PLAY WELL layered bubble treatment and appropriate bubble accent titles. The sunrise transition belongs in the lettering.
- Keep six chapter labels with one subhead each. Together their lines form two approved 5/7/5 haikus. Retain the content gate.
- Keep captions one at a time, with legibility shadow rather than a solid background panel.
- Preserve upright minifigs and distinguish builder-assigned stories from evidence, agent status and software authority.
- Retain MOCK MATH, labelled research/concept doors and the honest ask-bar routing/talk-stub limits.

V-01 and V-02 are unavailable in the received source union and use explicit fallback messages. If this Claude session retains their genuine R3/R5 source, recover it with provenance. Otherwise record the gap. Do not fabricate replacement sheets or remove their routes. The complete R3/R5 union is not claimed by this addendum.

## Return a reviewable design export

First return a short inventory confirming access to the branch, source prototype, full model, review and task briefs. Then state the layout, navigation and motion plan before substantial changes.

Export a clearly named derivative. Keep the received R6 overlay and Codex addendum byte-frozen. Carry the model pair and original Blender sources, dependencies, styles and required runtime assets. Include an index of every page, changed files, preserved/fixed/unresolved behavior, screenshots at the tested widths, and the result of each task's acceptance checks. Distinguish a performed browser check from a design intention.

Follow the existing package schema and report unresolved parent/index/fixture/ledger defects. Do not claim a complete operative cut, allocate correspondence numbers, accept proposal-ledger items or modify real inventory. James controls design acceptance and operative import.
