# R6 addendum: responsive house and sheet navigation

James requested this addendum in the Codex session on 2026-10-12 and selected PR #46 as its destination. It supplements the received R6 overlay at `defff46251f3e98c44ba3a2f3ddada768e9328a0`.

The interface base is R6. Model quality comes from the GPT renderer and corrected asset pair in PR #45 at `aef20a673ccded5259fb5548ccd450cc6c86caba`. The runnable source combines the available R2 rev-b, R4 and R6 exports. R3 and R5 are unavailable, so this is a documented reconstruction rather than a complete inherited R6 cut. V-01 and V-02 retain explicit unavailable-page messages.

This is a supplemental review artifact under HANDOFF-LEGO-PIPE-037-R0. `manifest.json` records the derivative files, sources and asset hashes. It does not replace the received `package.yaml`, allocate a correspondence number, create an instruments row or authorize production work. Prototype code remains a behavior reference.

## Start here

- [Posted-review content and dedicated assignments](review.md) defines the next Grid/Subgrid, navigation, motion and render sessions.
- [Change ledger](changes.md) records the operator requests and their implementation.
- [Responsive and interaction specification](specs/responsive-and-navigation.md) defines the layout and camera behavior.
- [Verification and remaining work](verification.md) separates observed behavior from unverified device and production concerns.
- [Next research and technical design](next-work.md) covers render structure, accessible navigation and Grid/Subgrid motion.
- [File manifest](manifest.json) identifies every transferred byte except itself.
- [Phone dashboard](evidence/responsive-phone-dashboard.jpg) and [desktop opening](evidence/responsive-desktop-landing.jpg) show the reviewed result.

## Run from the repository root

Use Node 22.12 or later, or Node 20.19 or later, as required by Vite 8. The repository pins pnpm 9.15.4.

```sh
pnpm --filter house-world-r6-addendum install --frozen-lockfile --ignore-scripts
pnpm --filter house-world-r6-addendum build
pnpm --filter house-world-r6-addendum dev --port 4200 --strictPort
```

Open `http://127.0.0.1:4200/prototypes/House%20World.dc.html`. Stop an existing server on that port before starting this copy. To serve the built files, stop the dev server and run:

```sh
pnpm --filter house-world-r6-addendum preview --port 4200 --strictPort
```

The source snapshot needs no local directory links. The workspace lock supplies Three and Vite. Model assets, Draco decoder files and the DynaPuff font and licence are included. Google Fonts still provide the inherited sheet typefaces, so full offline font fidelity is not claimed.

## Model assets are included

`prototype/prototypes/house/house.glb` and `house-metadata.json` are the matched corrected pair. Replace them together when exporting a new model. The pair includes the valid Block 1 bottom step in its adjoining course. No source brick was removed.

`assets/blender/legoHouse.blend` and `legoHouse.blend1` preserve both supplied Blender revisions. Browser framing, lighting and material changes do not modify their source geometry. `tools/verify_bundle.py` checks these and every other transferred file.

## Boundaries

All inherited MOCK MATH, evidence distinctions and builder-owned meaning remain. Minifigs and roof colours do not establish agent status or authority. The ask bar routes literal text to a room. Talk remains a labelled stub. Research doors remain concepts.

The received R6 overlay stays byte-identical. Its claims that PR #45 lacked `house.glb` and that model Block 8 was unassigned are corrected in this addendum's verification note, without rewriting the received document.
