# Review of the R6 addendum

## The prototype is ready for another design pass

The weakest part remains the layout and interaction structure. This addendum fixes observed responsive failures, but it still adapts inherited inline layouts and an iframe-based dashboard. Successful screenshots do not establish a robust Grid/Subgrid system, reliable draft ownership or a complete navigation and transformation contract.

Accept this derivative for continued prototype review. Keep PR #46's non-operative, do-not-merge boundary. Production architecture and a complete operative R6 import remain gated by the existing work orders and correspondence rules.

## Dedicated follow-up assignments

These are assigned owner roles for future sessions. No live chat has been created or messaged. The machine-readable task briefs are in [follow-up-tasks.json](follow-up-tasks.json).

| Task | Implementation owner | Reviewer | Required result |
|---|---|---|---|
| R6-NEXT-GRID | Claude Code, dedicated layout session | Codex and James | Grid/Subgrid contracts and responsive/state evidence across every available page, with missing sources named explicitly |
| R6-NEXT-NAV | Codex, dedicated navigation session | Claude Design and James | Usable controls and an explicit block/room/sheet/return/history/draft state model |
| R6-NEXT-MOTION | Codex, dedicated motion/transformation session | Claude Design and James | Comfortable, interruptible transforms across cards, grids, sheets, camera and assembling pieces |
| R6-NEXT-RENDER | Claude Code, dedicated render research session | Codex and James | Measured render-structure recommendation that preserves model quality and animation identities |

### Grid/Subgrid covers the full page set

Inventory every room sheet, the typology studies, Workbench Frame and linked design-library pages. Review expanded, collapsed, empty, error and loading states, not only opening screenshots. V-01 and V-02 stay visible as missing-source obligations.

Define named page regions and container-driven tracks before replacing layout code. Preserve distinct work skeletons and verbs. Use subgrid to align related title, content and status bands. Check narrow viewports, sidebar changes, long labels and larger text. Bound intentional diagram/table scroll. Validate reading order and keyboard reachability.

### Navigation has a dedicated control and state pass

Define who owns tour progress, the clicked block, room threshold, current sheet, bookmark and draft. Redesign finder previews, tabs, room switching, direct-page entry, stop, Back and Escape as one coherent control system. Test touch, keyboard, iframe focus, browser history, virtual keyboards, rapid activation and both scroll boundaries.

### Motion follows the layout and navigation contracts

Give every transition one owner. Compare native View Transitions with transform/opacity motion for Grid/Subgrid expansion, card transformation and dashboard entry. Define origins, clipping, acceleration, cancellation and reduced-motion equivalents. Keep text readable. Audit brick assembly for alignment and attachment before seating. Avoid intersecting pieces, depth-changing focus effects and camera whip.

## Evidence and limits

The frozen repository install and build passed. The packaged build loaded the full GLB and opened the real Layout Canvas through finder Enter without console warnings or errors. The manifest verifier proves transferred bytes and preservation of the received R6 overlay. The source preview has responsive evidence at six viewport sizes.

Physical-device, Safari/Firefox, full accessibility, reduced-motion and performance checks remain future work. R3/R5 are unavailable and V-01/V-02 have fallback messages. Preserve these limits in any follow-on review. This addendum does not accept the received package's unverified architecture or proposal ledger.
