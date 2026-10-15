# handoff-r6 — DT-DESIGN R6 overlay (2026-10-12)

Read `DT-DESIGN-R6-EXPORT-RECEIPT.md` first, then the four specs in order, then `package.yaml`.

- `package.yaml` — designer manifest (design-package/v1), supersedes R5.
- `specs/HW-01-fly-through.md` — camera ownership, tour, hover card, room flights, return, equivalents, `<house-stage>` API. Replaces R5's HW-01.
- `specs/HW-02-rooms-and-sheets.md` — rooms as kinds of work; block → room → sheet map; finder, tabs, Switch room.
- `specs/HW-03-ask-bar.md` — the plain-language prompt (type / talk) and what it does today.
- `specs/HW-04-graphic-text.md` — layered-stroke wordmark, captions, bubbles, gradient sweep, studio palette; the brief for the vector version.
- `notes/` — N-05 shared theme preference, N-06 ask bar is a router (N-03, N-04 carried from R5).
- `sources/prototypes/House World.dc.html` + `sources/prototypes/house/` + `sources/dt/theme.js` — the running study.
- `decisions-proposed.md` — seven proposals awaiting the operator; ledger unchanged (DEC-043).

Behaviour is authoritative in the sources; where a spec and the source disagree, the source is what was reviewed. HOUSE-WORLD R0 (PR #45) is the brief this answers; it is not replaced.
