# Verify this cut and the next slice

## Reproduce the current package

From the repository root:

```sh
python3 docs/design/review/HOUSE-WORLD-R0/tools/verify_received.py
pnpm --filter house-world-study install --frozen-lockfile
pnpm --filter house-world-study build
pnpm --filter house-world-study preview --port 4189
python3 tools/memo_preflight.py docs/correspondence/HANDOFF-LEGO-PIPE-037-R0-house-world.md docs/correspondence/REGISTER.md
```

Use `tools/setup-preflight.sh` once if the Python validator needs PyYAML. The root pnpm lockfile is the active dependency contract. The package receipt gives the expected digest. The asset manifest gives source-file hashes and byte counts.

`verify_received.py` extracts this package from the current Git HEAD into a temporary directory, measures it with the repository's normative algorithm, checks the sibling receipt, runs structural package preflight and verifies asset bytes. Raw `design_pkg.py digest` is valid on the source tree before installing/building, but generated `node_modules` and `dist` must not be counted as received artifacts. Verify the committed snapshot after reproduction.

The package preflight is structural. Its register-reference lookup does not establish design acceptance. HOUSE-WORLD has no accepted instruments row in this PR and the brief is for review. Do not import it or issue a production pin merely because the commands pass.

## Current browser checks

1. Load `?variant=exploded`, wait for the supplied model, then return to the start. The compact house fits beside the title on desktop and below it on mobile.
2. Scroll through all six captions. Each shows one haiku line. Chapter changes occur at zero caption opacity.
3. Scroll 8% → 40% → 8%. Read-only `window.houseDemo.diagnostics()` reports the same camera and piece positions at both 8% samples.
4. Inspect the trees during the close pass. Their final strokes follow connector axes. Inspect all three minifigs in the full and Lite modes; their heads stay above their feet and their world up vectors are upright.
5. In Find a room, type `M01`, select with arrows and open with Enter. Escape and Tab dismiss normally. Closing the sheet restores the activating control, query and scene position.
6. Open BOX and follow the book and three mock bags. Change the reading after a review; retained earlier readings and reopened dependent checks are visible, while unrelated inventory stays unchanged.
7. Enable Still view or reduced motion. Scrolling does not move the retained camera. Open pages directly. With `?no3d=1`, the finder still reaches the same HTML destinations.

The session's earlier checks and captures are in `prototype/VERIFICATION.md` and `prototype/review-captures/latest/`. These are browser observations. They do not claim physical VoiceOver/NVDA testing, a complete phone canvas design, universal collision safety, real agents or a device performance benchmark.

## Acceptance for the next room/modal slice

- One block reaches A-01 through an explicit, cancellable threshold flight. Hover/focus causes no camera travel.
- The dashboard occupies near-full-screen space and displays the handoff's intended page skeleton. The ghosted house remains frozen and inert behind it.
- Keyboard activation, modal focus containment, Escape, browser history, reduced motion and renderer failure reach equivalent destinations.
- A second page can be opened and left without losing a form draft or the initial tour bookmark.
- There is no document-level flash for a local card change or Benny response.
- The six-haiku copy gate remains in the build. Preserved source Blender files match their hashes.

Review this observable slice before implementing all block routes, more parallax layers or a new background.
