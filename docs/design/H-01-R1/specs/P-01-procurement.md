# P-01 — Buying the gap: which shops, in what order

**File:** `prototypes/Prototype P - Procurement.dc.html` · **Journeys:** J7 · **Status at handoff:** built
Behaviour reference is the live prototype; its code is not to be copied. All numbers are mock pending real math + audit.

## Purpose
Only buys. Takes the list C-01 approved and turns it into real BrickLink orders; recorded orders flow back to inventory (ordered → owned).

## Behaviour
- **01 What matters most?** three priorities (lowest total · fewest parcels · here soonest), each showing the order it would produce before it is picked; a "let one part come from two shops" toggle with its consequence. Locked once any order is recorded.
- **02 The order, in one line** + readouts (shops, total range, pieces covered, last parcel) and a naive-baseline comparison. Not-covered warning names the parts.
- **03 Who sells what** — parts × shops schedule: rows by basis, shop columns **paged 3 at a time** (chosen first, or search order), chosen lot filled, stocked-not-chosen outlined, "only N" when too few, per-shop footers (parts, minimum shortfall, postage range, total), "If you drop it" consequence, SKIP / BRING BACK. An **ask box** on top converses about the plan (keyword mock: skip/bring back a shop, only US shops, priorities, splitting, "why <shop>"); the AI restates what it changed; refuses while locked. Each shop column shows a reputation line from account history (mock).
- **04 Place the orders**: one parcel per shop; Open on BrickLink; MARK ORDERED → order number recorded → stamp; UNDO allowed until shipped.

## Algorithm (mock, real in code)
Exhaustive over shop subsets (n ≤ ~12; heuristic beyond): each part to the cheapest lot in the subset (split fills across lots when allowed); minimum-order shortfall counted as cost; postage as a range; score by priority. Infeasible subsets skipped; uncovered parts reported.

## States
priority · split · skipped shops · page · plan-first sort · ask turns · marking · orders recorded (frozen).


## Revision R1 — procurement-release gate, revalidation, manual orders (HANDOFF-LEGO-PIPE-014 §5D, §8, §3.4 · DEC-025)

**The gate moved (DEC-034, operator call after seeing it on P-01): it now sits at the END of C-01**, after the approval trail, as the reusable **ReleaseGate** component (D-01 §C5). P-01 opens with a one-line status bar — ○ NOT RELEASED (read-only, CrossRef back to C-01#gate) or ■ RELEASED TO BUY · date · initials — and reads the result via `?released=INITIALS|DATE` from C-01's "Continue to P-01" button. Everything below describes the gate wherever it is mounted.
- *What's being released*: the C-01 shortage list at its revision, who approved it, a CrossRef back to the list.
- *Evidence it rests on*: each item with badge (■ MEASURED · ■ HOLDS · ■ APPROVED · ○ NOT RUN · ◇ n DAYS OLD), freshness, and a CrossRef to where it lives (M-01 facts / claims, C-01 list, A-01 fit).
- *Open findings*: severity (▲ HIGH blocks · ◇ MEDIUM · ○ LOW), why it matters, and three calls per finding — **fix** (CrossRef to the sheet that closes it), **waive** (a reason sentence, ≥ 6 chars, goes on the record), **defer** (owner + due trigger). Done findings show their stamp and ↺.
- *Decision*: initials + **Release to buy** (label becomes "· with waivers" when any waiver/deferral exists); **Send back to C-01** records return-for-work. Approve is disabled while any HIGH is open or initials are missing; the reason is written next to the button.
- *The record behind the stamp* (disclosure): the §8 GateRecord fields — gate_id · type · subject_ref · candidate_revision · entry_criteria · required_evidence · checks · open_findings · authority_required · decision · output_baseline_ref · invalidated_by · supersedes. Rigor underneath; a quiet card and a friendly stamp on top. AI stance is analysis, never authority.
- Passed → ■ RELEASED TO BUY · date · initials stamp; REOPEN THE GATE is always available.

**04 · Revalidate before you leave (§5D).** After release, a *Re-check stock and prices* step gates the BrickLink links: ◇ 5 DAYS OLD → (first run) ▲ PRICES MOVED with the drift spelled out and the plan re-priced → ■ CHECKED JUST NOW (links live 30 min). Clicking a locked link explains why instead of opening.

**Recording an order says *ordered*, nothing more.** Owned arrives only after receive + inspect (Tier 2 sheet). Copy on 04 and the intro say so; the ordered→owned shortcut is gone.

**Manual / retroactive order (§3.4) — always open, no gate.** "Already bought something outside this plan?" → shop · order number · placed on · total paid · lines (id × qty colour). Pending restatement: "I will record an order you placed yourself … Provenance: entered by James, now, after the fact. It counts against the C-01 list as ORDERED — not owned …" → Yes / Not yet. Recorded orders show as ■ ORDERED · BY HAND with entered_by/entered_at. The intro bar, while the gate is open, links here: *order anyway and record it here after the fact — that is a supported case, not a workaround.*

**Announcements (§6).** Gate tag is a polite live region ("▲ 2 BLOCKING" → "◇ 2 TO CALL" → "○ READY FOR INITIALS" → "■ RELEASED"); the two restatements (manual order) are `role=status aria-live=assertive`; locked-link attempts write to the ask-box chat log (polite).

**Mock boundaries.** Findings are seeded from today's real state (railhead unknown, Q13 overlap, recolour claim, price age). Revalidation drift is scripted. Manual order lines are not parsed into part rows yet.
