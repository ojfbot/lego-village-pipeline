# LEGO Village Pipeline — design handoff (H-01)

**Handoff:** LEGO-PIPE-007-R2 → H-01 · **Date:** 2026-09-17 · **From:** claude-design session · **To:** Claude Code (build), Claude chat / ChatGPT (research, review, continuity)
**Status:** design complete for slices A, B, C, P, F, M at prototype fidelity; **HANDOFF-LEGO-PIPE-014 Tier 1 applied (WP0–WP4)** — see `decisions.md` DEC-016…035. **This is review round R1** — read `REVIEW-R1.md` first if you are a reviewing agent. Production implementation is authorized only through this package, after R1 closes; nothing in the prototypes is production code.

## How to read this (for any agent or person)
1. Start with `decisions.md` — every settled call, dated, with what it touched. Treat these as constraints, not suggestions; only @jfo (the operator) can overturn one, and a new dated entry records it.
2. `schema-requests.md` — everything the UI needs the data model to have. These are *requests*: `packages/schema` is the contract; do not invent fields, propose them against this list.
3. `seam.md` — assumptions about the Frame host. Listed, not contracted.
4. `open-questions.md` — unresolved items, each with an owner type (research agent · design session · operator · Claude Code).
5. `specs/*.md` — one page per sheet: purpose, behaviour, states, copy rules, what is mock. Read these before building a screen. The prototypes in `standalone/` (open in any browser, no server) are the reference implementation of *behaviour*; their code is not to be copied.
6. `index.json` — the manifest and single source of status: sheets ↔ journeys ↔ components, plus pointers to decision records (`decisions.ids`) and schema requests (`schema_requests`). Paths resolve from **archive root** (`path_base`); `check-manifest.mjs` fails on drift.
7. `screenshots/` — what each sheet looked like at handoff, both themes; `screenshots/states/` + `screenshots/STATES.md` — the sheets driven through their interactions (armed placement, side views, asks, approvals, orders, sent state, logs). Use for recognition, not measurement.
8. `responsive.md` — target devices and what collapses. **Responsive design for iPhone and iPad has not been done**; this is a spec of intent for further design cycles.

## Standing rules (from CLAUDE.md and the decision log)
- Every UI is a frictionless teacher: plain words first, controls explain their consequences, AI questions arrive as conversation (tap / type / talk), no jargon-first labels or prepositional titles.
- Evidence axes stay separate (origin · method · verification · authority · workflow). AI origin is permanently visible. Verified values read as trustworthy.
- Requests are first-class and never deleted; basis is on every part row; prices are ranges; gates are stamps for the record and quiet modals for the act; purchase stays outside the app.
- People: the operator is James (@jfo), a friend of the family; the boys are his partner's sons. Never "Dad", never a parental role. Kid-facing copy says "James" sparingly and never talks down.
- All numbers in prototypes are MOCK MATH pending implementation plus an independent audit.
- Vocabulary (parts · pieces · elements · modules · units) is under review — see `open-questions.md` → RESEARCH-01 (`brief/RESEARCH-01-nomenclature.md`). Do not hard-code these words into schema names until it lands.

## What is here
| Path | What |
|---|---|
| `REVIEW-R1.md` | **Start here if reviewing** — what changed since 014, what to check, how to answer |
| `ADDENDUM-A1-right-now.md` | Added after the R1 cut: the Hub's three-priority strip and the no-nag contract it tests |
| `decisions.md` | Dated decision ledger (source: Hub decision log) |
| `schema-requests.md` | Consolidated schema requests, grouped by entity |
| `seam.md` | Frame host seam: assumptions and integration questions |
| `open-questions.md` | Open items with owner and where they surface |
| `responsive.md` | Device targets and collapse rules (intent only) |
| `repo-structure.md` | Proposed fresh-repo layout for Claude Code |
| `specs/` | Per-sheet behaviour specs |
| `index.json` | Machine-readable index |
| `screenshots/` | Sheet captures at handoff |
| `standalone/` | Self-contained offline copies of every sheet. **Keep `standalone/` and `dt/` together** — embedded hover-card components resolve `../dt/overlay.js` etc. relative to the standalone |
| `dt/` | Runtime helpers the standalones load: `tokens.css`, `overlay.js` (hover-card lifecycle), `landing.js` (card registry for CrossRef), `a11y-tree.js` (walker), `check-contrast.mjs` |
| `brief/` | The R2 brief (**historical input**, superseded where later decisions differ) and RESEARCH-01 (copies) |
| `tokens/tokens.css` | Same file as `dt/tokens.css` (kept for older references); contrast contract enforced by `dt/check-contrast.mjs` |
| `check-manifest.mjs` | Cross-artifact status/fact check (paths, J-01 ↔ index statuses, STATES.md ↔ index) |
| `CLAUDE.md` | Project instructions in force during the session |

- `specs/ANNOUNCEMENTS.md` — what a screen reader hears, per trigger.
- `a11y/` — accessibility-tree baselines per sheet (+ walker at `dt/a11y-tree.js`).
