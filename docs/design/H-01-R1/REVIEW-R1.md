# REVIEW-R1 — independent review brief (for Claude chat and ChatGPT)

**Package:** LEGO Village Pipeline · H-01 · revised under HANDOFF-LEGO-PIPE-014 · 2026-09-17
**Operator:** James (@jfo). **Your role:** independent reviewer. You do not implement; you find what is wrong, missing, or unproven, and say so plainly. Reconcile with the other reviewer before handing back, as you did for 014.
**After R1:** Claude Code builds from this package. Anything you don't catch now gets built.

## 1 · What changed since your 014 change request
014 asked for Tier 1 in a fixed order. All of it landed; the operator made calls along the way. In order:

| WP | 014 item | What landed | Where to look |
|---|---|---|---|
| WP0 | §2 drift, K-1…K-9, contrast, ledger ids | Tree measured (DEC-016: 16×16 · 40 br · 8 br base · r28 · 10 br clear); DEC-001…035 with supersedes; tokens darkened for 4.5:1 (`dt/check-contrast.mjs`); single manifest `index.json` + `check-manifest.mjs`; `@boys` → initials EH/HH/LH; "quadrant" → **Section** | `decisions.md`, `index.json`, `tokens/tokens.css` |
| WP1 | §4 viewer expansion, Journey 3 fit proof | A-01: PLAN / **3D · CHECK IT** tab; both views read one geometry (tree, right-of-way band 36–44 st, sections, plantings); **"Does it fit?"** — six deterministic checks, honest BLOCK on the 8×8 inner-corner overlap (**Q13**, open for the operator); **"Try a move"** proposes with a pending restatement, Yes/No | `specs/A-01…md` R1, `states/10-a01-3d-fit.jpg` |
| WP2 | §7.2 axis split, measurement + verification loops | C-01 basis split into stored + derived axes with a composed plain-language sentence per row; new sheet **M-01 Measure and check** (facts with method/proof/history; claims drafted → method · words · proof → restatement → holds / wrong / parked; blast-radius list) | `specs/C-01…md`, `specs/M-01…md`, `states/13-m01-claim-draft.jpg` |
| WP3 | §8 gate, §5D through order, §3.4 manual order | **ReleaseGate** component (DEC-025 content; DEC-034 placement: **end of C-01**, not head of P-01). P-01 reads the result, forces a stock/price **revalidation** before BrickLink links open, drops the ordered→owned shortcut, and takes **manual / retroactive orders** with after-the-fact provenance | `specs/P-01…md` R1, `specs/C-01…md` R1, `states/11…`, `states/12…` |
| WP4 | §6 accessibility | `role=main`, `<h2>` titles, `<section>` cards, full-sentence names on every icon/summary/choice; **`specs/ANNOUNCEMENTS.md`** (trigger → region → sentence); **`a11y/*.tree.json`** baselines + walker | `specs/ANNOUNCEMENTS.md`, `a11y/` |
| new | operator asks mid-cycle | **SetRef** (hover card → BrickLink stable URL for sets/Studio models), **CrossRef** (every claim links back to its origin and forward to what leans on it; preview in a popover; landing flash), **Blocker** ("blocked by" is never a bare label — preview + clear-it-here), **GapCloser** (queue Blender/Studio/research runners to close a strike), shared **`dt/overlay.js`** lifecycle. All drawn in D-01 §C1–C6 | `standalone/D-01…html`, `decisions.md` DEC-029…035 |

## 2 · What to check (in priority order)
1. **Truthfulness of the fit proof.** Open `standalone/A-01 Layout Canvas.html` → 3D · CHECK IT. Are the six checks the right six? Is the Q13 block correct geometry (ring centred on the tree; 2×2 sections of 32×32 MILS; inner corner under a 16×16 base)? Is anything claimed that isn't computed? The `MOCK MATH` labels — are they on everything that is mock, and nothing that isn't?
2. **The gate.** `standalone/C-01 Railbed.html` → drive the trail to Approve (RESET DEMO, Save draft, Respond→Park, Confirm + derive, Run, Reviewed, Approve). Does the ReleaseGate carry the §8 record faithfully? Is "waive with a reason / defer with owner + trigger" sufficient authority for a family purchase? Should HIGH be waivable at all? Is P-01's read-only-until-released the right consequence?
3. **Evidence axes stay separate.** On C-01 open "THE SIX AXES BEHIND THAT SENTENCE" on any part row. Does the composed sentence ever collapse two axes? On M-01, does "Holds" ever get recorded without method + proof? (It shouldn't since the operator's correction — try it.)
4. **Frictionless-teacher principle.** Every sheet must open by saying what's happening in plain words; every control must teach its consequence before commit. Flag any label that is jargon-first or any action that commits without restating.
5. **People.** James is a friend of the family; never "Dad". Boys are EH/HH/LH. Flag any drift.
6. **Cross-reference integrity.** Hover any `↖`/`→` chip: does the preview describe the right card? Does clicking land on it with the flash? Are there claims with no back-link?
7. **Accessibility.** Read `specs/ANNOUNCEMENTS.md` against the sheets: is any state change silent? Compare `a11y/*.tree.json` to what you see: unnamed or misnamed controls?
8. **Schema requests.** `schema-requests.md` — does the UI ask for anything the axes model can't carry (Q11 `need_origin`)? Are GateRecord and PriceRevalidation shaped right?
9. **Open questions.** `open-questions.md` — each one either has an owner and a trigger or it's a stub. Which are stubs?

10. **Addendum A1 — the "Right now" strip on the Hub.** Read `ADDENDUM-A1-right-now.md`. Does the no-nag / no-guilt contract hold in every state (all open · mixed · all parked · all done)? Is "three, in order, with the reason" the right shape for a type-generic priority surface?

## 3 · Known and accepted (don't re-report)
- All numbers are MOCK MATH; Claude Code + independent audit before anything is trusted.
- Screenshots are viewport crops; A-01's WebGL canvas reads blank in captures. Use the standalones.
- Responsive iPhone/iPad is not done (Q7). Tier 2 (receive → inspect → discrepancy → allocate) and Tier 3 are not in this round.
- The Organic design system is attached to the project but scrapped by the operator; adherence warnings are ignored by instruction.
- D-01 carries **copies** of the five component DCs so its standalone can embed them; `prototypes/` is the source (`library/SYNC.md`).

## 4 · How to answer
Return one reconciled document, same shape as 014: numbered findings, each with **severity** (blocks build · should fix before build · fix during build · note), **where** (sheet · card · file), **what is wrong**, **what would satisfy you**. Cite decision ids when you disagree with a decision — only the operator can overturn one, and he needs to know which. Do not restate what is fine.

## 5 · File map for this round
`README.md` (how to read) · `decisions.md` · `schema-requests.md` · `open-questions.md` · `seam.md` · `responsive.md` · `repo-structure.md` (unadjudicated, K-4) · `specs/` (one per sheet + ANNOUNCEMENTS) · `a11y/` · `standalone/` (open in any browser) · `screenshots/` + `screenshots/states/` + `STATES.md` · `index.json` + `check-manifest.mjs` · `tokens/tokens.css` · `brief/` (014's inputs: 007-R2 historical, RESEARCH-01).
