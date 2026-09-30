# Drafting Table: Right now demo

This is one local, fixture-backed slice of the H-01 R1 Hub addendum. It gives James three ordered priorities, their reasons, done / not today / undo actions, a paper / blueprint switch, and browser-local state. DEC-016 already records the tree measurements; the first priority stays open as a practice recheck, not an assertion that the tree was never measured. A parked card returns in a new browser session. Done stays done until undone.

The fixture is hand-seeded from `docs/design/H-01-R1/ADDENDUM-A1-right-now.md` and validated at load by `packages/schema`. This validator covers the Hub demo fixture only. It is not the schema gate for C-01, procurement, inventory, or geometry. The app imports the committed Drafting Table token CSS directly. It does not copy code from `standalone/`.

## Run

From the repository root:

```sh
pnpm install --frozen-lockfile
pnpm validate:fixtures
pnpm test
pnpm dev
```

Open http://127.0.0.1:4173.

## Boundary

James authorized a narrow fixture-backed app slice ahead of the S1/S2/S7 reports in the 2026-09-29 Codex chat. This branch proposes the code for his review. It does not accept all of HANDOFF-LEGO-PIPE-023-R2, open any numbered bag, declare the Boundary 1 schema approved, release a BOM, or enable an order. The H-01 design package stays byte-for-byte unchanged. The LEGO listing opens outside this app and must be checked for current availability and price.

The committed handoff records five tree dimensions but did not include the inventory photos. James supplied three first rough photos on 2026-09-29. Their EXIF capture times are 2026-09-19; DEC-016 is dated 2026-09-17. The app treats the photos as later context for the set and measurement setup, not independent proof of the five numbers. The original JPEG bytes are kept under `evidence/tree-41843/rough-2026-09-19/`; the fixture records their SHA-256 digests. Any replacement photo set gets a new path so this one remains traceable.

## Review gates

The inherited H-01 R1 contrast checker reports one failure: blueprint `--dt-block` is 4.27:1 on `--dt-sheet`, below its 4.5:1 contract. The demo uses `--dt-block-deep` for warning text and leaves the pinned design file unchanged. The pull request workflow runs the original checker and stays red until that source defect is resolved through the design-cut process.

The browser accessibility tree was checked manually for one heading, landmarks, named controls, and the live announcement. A repeatable Hub accessibility-tree snapshot check is still needed before this branch is merge-ready.
