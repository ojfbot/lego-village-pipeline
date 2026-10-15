# Verification and limits

## Observed in Chrome

The local preview at port 4200 was exercised at 320×740, 390×844, 768×1024, 1024×768, 1440×900 and 844×390. Browser evidence is recorded in `evidence/responsive-browser-checks.json`.

The 320-pixel pass exposed page overflow in Hub, B-01, P-01, I-03, M-01 and T-01. After corrections, those pages' scroll widths equal the viewport width. The shop matrix has its own scroll region. The other recorded inherited pages had no page-level overflow at 320 pixels. This is layout evidence, not a claim that every interaction is complete or every element has an ideal phone design.

Finder Enter opened the real Layout Canvas, Workbench and Drafting Table sheets. The mobile dashboard filled the viewport. Its final 390-pixel header measured 108 pixels high and its tabs measured 366 pixels wide. Initial matrix measurements include the entrance animation and precede the final mobile header refinement. The final phone screenshot and header record are the later evidence.

Back followed by scrolling returned camera ownership to `tour`. A wheel gesture at the page end also resumed the tour. Finder entry to Drafting Table reported flight block 1. Physical clicks in other rooms forwarded blocks 5, 14 and 22. The code forwards Drafting Table block 13 through the same activation path, but a physical click on block 13 was not separately verified. Workbench expansion kept the other cards and the reviewed tab reported no console errors or warnings.

The paired browser model assets match the corrected PR #45 bytes. Both Blender source files match the previously transferred source hashes. The received R6 overlay has 22 files, 1,445,058 bytes and tree digest `2aa80e465949a7294c26eca116af39b8d5f915f039e9c7b1ab661c446f253797`.

## Reproduce the bundle checks

From the repository root:

```sh
python3 docs/design/review/DT-DESIGN-R6-addendum/tools/verify_bundle.py
pnpm --filter house-world-r6-addendum install --frozen-lockfile --ignore-scripts
pnpm --filter house-world-r6-addendum build
```

The verifier checks the transferred file list and each byte hash. It rejects symbolic links and excludes local `node_modules` and `dist` folders. The build includes the six-chapter haiku gate. `evidence/build-verification.json` records the repository reproduction result.

## Corrections to received R6 claims

R6's received D-14 says `house.glb` was absent from PR #45 at `bbaeec06ef09`. That asset was present at `docs/design/review/HOUSE-WORLD-R0/prototype/house.glb`. This derivative uses the later corrected pair at `aef20a6` and includes it directly.

Received D-17 describes an unassigned model Block 8. The supplied metadata has 21 block groups with IDs 1 through 7 and 9 through 22. There is no Block 8 group. Every existing block is mapped to one of the eight R6 rooms. Neither the original received statement nor the model numbering was silently rewritten.

## Remaining limits

- Safari, physical phones, virtual keyboards, touch hover behavior and GPU performance have not been verified.
- This is an available-source reconstruction. V-01 and V-02 source implementations are missing. The routes open explicit unavailable-page messages.
- Some legacy Hub and Handoff links point at candidate and handoff files outside the runnable source subset. This is not a complete portable archive of every historical design document.
- Reduced motion inherits the source flight and CSS behavior. It has not had a new device/accessibility audit. Keyboard operation was exercised through the finder and Back. A full iframe focus and Escape audit remains.
- Mock data, keyword routing, dynamic source runtime, iframe lifecycle, browser history, context loss and rapid repeated activation remain prototype concerns.
- More parallax layers, background design and continuous block-to-block flights remain design work. Near-full-screen sheets now run, but full dashboard composition still needs refinement against the Claude handoff.
- Vite reports a large Three bundle and leaves legacy non-module scripts to the static copy step. A successful build is not a performance benchmark.
- Google-hosted inherited typefaces remain network dependencies. The model, Draco decoders and bubble font are local.

The source diff retains trailing whitespace in copied F-01/R-01 markup and the received font licence, plus blank stage lines and intentional Markdown haiku breaks. `git diff --check` reports those formatting facts. It is not a clean-whitespace claim.
