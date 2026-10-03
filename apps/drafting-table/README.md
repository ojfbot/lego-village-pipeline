# Drafting Table: Right now demo

This is one local, fixture-backed slice of the H-01 R1 Hub addendum. It gives James three ordered priorities, their reasons, done / not today / undo actions, a paper / blueprint switch, and browser-local state. DEC-016 already records the tree measurements; the first priority stays open as a practice recheck, not an assertion that the tree was never measured. A parked card returns in a new browser session. Done stays done until undone.

The fixture is hand-seeded from `docs/design/H-01-R1/ADDENDUM-A1-right-now.md` and validated at load by `packages/schema`. This validator covers the Hub demo fixture only. It is not the schema gate for C-01, procurement, inventory, or geometry. The app imports the committed Drafting Table token CSS through a small app-owned contrast correction in `packages/tokens`; it does not copy code from `standalone/`.

The three priority `source_ref.id` strings are fixture-local pointers for this demo. They are not allocated correspondence identities or approved evidence IDs. The real tree measurement citation is DEC-016; its recorded values remain separate from these pointers.

A1 says “Order the Winter Holiday Train from LEGO.” The Hub fixture says “Check the Winter Holiday Train listing” because this demo only opens the listing and cannot authorize or record an order. This is a deliberate prototype wording deviation, not a change to A1 or a purchasing decision.

## Run

From the repository root:

```sh
pnpm install --frozen-lockfile
pnpm validate:fixtures
pnpm validate:contrast
pnpm test
pnpm exec playwright install chromium
pnpm test:a11y
pnpm dev
```

Open http://127.0.0.1:4173.

## Boundary

James authorized a narrow fixture-backed app slice ahead of the S1/S2/S7 reports in the 2026-09-29 Codex chat. This branch proposes the code for his review. It does not accept all of HANDOFF-LEGO-PIPE-023-R2, open any numbered bag, declare the Boundary 1 schema approved, release a BOM, or enable an order. The H-01 design package stays byte-for-byte unchanged. The LEGO listing opens outside this app and must be checked for current availability and price.

The committed handoff records five tree dimensions but did not include the inventory photos. James supplied three first rough photos on 2026-09-29. Their EXIF capture times are 2026-09-19; DEC-016 is dated 2026-09-17. The app treats the photos as later context for the set and measurement setup, not independent proof of the five numbers. The original JPEG bytes are kept under `evidence/tree-41843/rough-2026-09-19/`; the fixture records their SHA-256 digests. Any replacement photo set gets a new path so this one remains traceable.

## Review gates

The inherited H-01 R1 blueprint `--dt-block` is 4.27:1 on `--dt-sheet`, below its 4.5:1 contract. The app-owned token layer sets that one effective value to `#F08B7B` (6.03:1), while importing the pinned design CSS unchanged. `pnpm validate:contrast` checks every effective text token in both themes against the same 4.5:1 threshold and fails CI on regression. The source design defect remains recorded as D-1.

`pnpm test:a11y` compares the rendered Hub accessibility tree before and after marking a priority done. It also asserts the page title, language, one H1, landmarks, load and failure announcements, and all computed text-token contrast values in both themes. CI runs this gate in Chromium.
