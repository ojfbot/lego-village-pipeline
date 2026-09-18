---
correspondence_schema: lego-pipe-memo/v1
memo: HANDOFF-LEGO-PIPE-014
revision: R0
status: accepted
memo_type: handoff
title: "Focused redesign brief to Claude Design — journey architecture, control loops, gates, accessibility contract"
date: 2026-09-17
thread: design
cluster: design-definition
from:
  actor: Claude (Cowork)
  role: coordinating_reviewer_and_handoff_author
to:
  - actor: Claude Design
    role: design_session
  - actor: James
    handle: "@jfo"
    role: decision_owner_and_dispatch_authority
repos:
  - "lego-village (proposed; not yet created — see K-4)"
tags:
  - lego-village-pipeline
  - design-definition
  - journey-architecture
  - accessibility-contract
  - gate-model
  - procurement-critical-path
argument: >-
  In which the reconciled review is converted into a design work order sequenced
  against a physical order-by gate five weeks out rather than the Christmas demo,
  the family surface is removed from the critical path, the accessibility tree is
  made an acceptance-gating agent contract, and authority over Frame topology is
  kept with the operator.
supersedes: HANDOFF-LEGO-PIPE-010-R1
supersedes_scope_of: HANDOFF-LEGO-PIPE-007-R2
project: LEGO Village Pipeline
project_phase: design_definition
in_reply_to:
  memo: CORR-LEGO-PIPE-015
  note: "ChatGPT dispatch addendum, issued as CORR-LEGO-PIPE-011 — renumbered 015 on registration (011 was taken by the build-harness thread)"
parts:
  "0": what happened and what this brief is
  "1": settled constraints (K-1…K-9)
  "2": mechanical integrity pass
  "3": journey architecture and binding work order
  "4": A-01 3D viewer posture
  "5": four subjourneys requiring design
  "6": accessibility contract (acceptance-gating)
  "7": schema corrections to carry
  "8": gate contract, formal gates only
  "9": human-experience corrections
  "10": deliverables in tier order
  "11": readiness boundaries and staged code handoffs
  "12": dispatch dispositions against CORR-015
provenance:
  chain:
    - HANDOFF-LEGO-PIPE-007-R2
    - "Initial LEGO Village Pipeline Design Bundle.zip · sha256 377e230a…85f9"
    - REVIEW-claude-review-of-design-bundle-R0
    - CORR-LEGO-PIPE-008
    - CORR-LEGO-PIPE-009
    - "Operator dispositions, 2026-09-17"
    - CORR-LEGO-PIPE-015
  evidence_artifacts:
    - offline-render-test.py
    - evidence-A01-threejs-webgl-offline.png
  method:
    - independent_review
    - peer_reconciliation
    - headless_offline_render_verification
    - backward_schedule_planning
authority:
  decision_owner: James
  dispatch_authority: James
  operator_decisions_settled: [D-1, D-2, D-3, D-4, D-5]
  implementation_authorized: false
  production_code_authorized: false
delivery_context:
  demo_date: 2026-12-25
  hard_gate: "2026-10-21 — BOM and procurement plan trusted enough to spend money against"
  sole_user_until_demo: "James (@jfo), simulating other roles"
  family_turnover: "after the 2026 demo; not on the critical path"
  dogfooding: "the operator builds a real MILS landscape, railbed and ballast for the Winter Holiday Train using these tools"
trace_forward_as:
  - HANDOFF-LEGO-PIPE-014
---

# HANDOFF-LEGO-PIPE-014 — focused redesign brief to Claude Design

**Cites:** `CORR-LEGO-PIPE-008` · `CORR-LEGO-PIPE-009` · `CORR-LEGO-PIPE-015`
**Supersedes:** the draft circulated as `HANDOFF-LEGO-PIPE-010` v1.1, which used a number already held by the build-harness thread. Register reserved **014** for this document; that is its number.
**Authority:** James (`@jfo`). Every constraint in §1 is settled and is not open for redesign.
**Not authorized:** production implementation, schema authoring, repo mutation, Frame contract decisions.

---

## 0. What happened, and what this brief is

Your bundle was reviewed independently by two agents, whose findings were then reconciled against each other and re-tested empirically. The outcome, plainly:

**The conceptual layer is strong and survives intact.** Evidence axes kept separate, requests first-class and never deleted, basis before price, gates as stamps-for-the-record, the sticker→envelope→model chain, prices as ranges, purchase outside the app, family users given the real tools, RESEARCH-01 filed rather than guessed. None of this is being renegotiated. Build on it.

**Two reviewer criticisms were withdrawn after testing, in your favour.** An offline render test (all non-`file://` requests aborted at the route layer) proved the standalone prototypes are genuinely self-contained — zero external requests, React and fonts correctly inlined — and that A-01's Three.js WebGL viewer is real and works offline. Both reviewers had wrongly inferred otherwise from static inspection. Your bundling is sound.

**What is not yet sound is structural**, and that is what this cycle fixes: the journey model is not MECE, gates are drawn but not defined, several data types fuse independent axes, essential return loops are missing, artifacts contradict each other, and the accessibility layer is close to absent.

This brief is scoped to design work only. No implementation follows from it.

**One thing to understand before reading further.** This is not a greenfield product cycle. Between now and 25 December 2026 the operator is the only user, and he is using these tools to buy real parts with real money and build a real MILS landscape, railbed and ballast around a tree that is already standing, for a train whose track he already has. The Christmas moment is a demonstration that software planned and delivered a physical thing, and that the method scales when the family picks it up afterwards.

That changes what "good" means here. Correctness of the parts list and the receiving record outranks completeness of the journey map. The family surface, which an earlier review made a P0, is no longer on the critical path — its users arrive after the demo. And the real deadline is not the demo: it is the date the operator must trust the plan enough to spend money against it, which is **five weeks out**, not fourteen. §3.4 sets the work order accordingly and is binding.

---

## 1. Settled constraints — not open for redesign

| ID | Constraint | Consequence for you |
|---|---|---|
| **K-1** | **The tree (41843) base is 16×16 studs.** Measured and settled by the operator. | Supersedes F-01's 32×32 default and the "to be measured" line in `decisions.md`. F-01's Tweaks panel loses the base-size placeholder. Fit checks and the branch-overhang circle run against a real 16×16 obstacle. Record as a new dated decision citing this brief; do not edit the old entry. |
| **K-2** | **MILS modules are 32×32 studs** (with intermediate 16×32, 8×16). Curved track is carried by a **group** of standard modules acting as one substrate — not by an oversized module. | A-01's "48×48 · MILS" label is wrong. Do not invent a 48×48 class. The real modelling problem is how a *group* of modules is named, addressed and selected as one thing — hand this to RESEARCH-01 alongside the unit/module/quadrant call, and use a neutral placeholder until it lands. |
| **K-3** | **A-01's 3D viewer is both a preview and a verification surface.** Lo-fi render, truthful dimensions, driven by the same canonical geometry as the 2D canvas. It carries basic transform tools that **propose** changes for confirmation; it never persists a mutation directly. | See §4 for the full posture. This is an expansion of the viewer's role, not a deletion. |
| **K-4** | **Frame integration topology and ledger ownership are unresolved *operator* decisions.** They are out of scope for this design cycle and are **not** delegated to any agent. Claude Code may inspect the existing Frame/app fleet, identify constraints, run bounded spikes and submit alternatives with consequences; **James decides**, before any repo structure or persistence boundary makes the choice expensive to reverse. | Do not design around either answer. `repo-structure.md`'s two-app split is **unadjudicated** — mark it so. Keep `seam.md` as assumptions; add nothing to it. No agent may settle this by scaffolding. |
| **K-5** | **Full journey hierarchy is purchased** — all 8 lifecycle journeys and all 9 control loops designed to screen level — **but it is sequenced behind a physical deadline.** | See §3 for the model and **§3.4 for the work order, which is now binding rather than advisory.** Scope is unchanged; order is not negotiable. |
| **K-8** | **One user until the demo.** James is the only real user between now and 2026-12-25 and will simulate other roles. Family turnover happens *after* the demo and is explicitly not a surprise. | F-01's iPad responsive cycle **leaves the critical path**. The earlier P0 on it was premised on imminent child users; that premise is retired. Design it, but behind §3.4's Tier 1. |
| **K-9** | **This is a dogfooding build with real money and real bricks.** The operator will use these tools to specify, buy, receive and build an actual MILS landscape, railbed and ballast for the Winter Holiday Train. | Correctness of the **BOM and the receiving record** outranks every other quality in this cycle. A wrong BOM means wrong bricks and no village. See §3.4. |
| **K-6** | **The accessibility contract in §6 is mandatory** and is acceptance-gating on every sheet. | Not a polish pass. Read §6 before designing anything. |
| **K-7** | **Proportionality rule.** Where systems rigor and the frictionless-teacher principle conflict on a **family-facing** surface, the teacher principle wins and the rigor moves to the operator side of the join. | This is a standing instruction. A brief full of "gate", "baseline", "invalidation" and "supersession" will produce a compliance interface if you let it. Do not let it. |

---

## 2. Mechanical integrity pass

Do this first. It is low-judgment, it makes the package trustworthy to every downstream agent, and several items block the design work.

**Ledger and index**

- Assign stable decision IDs `DEC-001…DEC-013`, oldest first. Add `supersedes`, `status`, `effective_revision`. Append-only remains the rule.
- Declare `path_base` in `index.json` (paths resolve from **archive root**, which was never stated) and add a resolver test. *Note: paths are not broken — an earlier review claimed this in error and it is retracted.*
- Fix `"tokens": "dt/tokens.css"` — it resolves under no base. Either point at the shipped `handoff/tokens/tokens.css` or mark it explicitly as a forward reference to the future repo path.
- Put structured decision records and schema requests **in** `index.json`, or correct the README, which currently promises both.
- Reconcile the component inventory: `repo-structure.md` lists 10, `index.json` and D-01 list 15. The missing five are ApprovalGate, EvidenceChips, SegmentedLine, StatusLine, ActionLog.
- Add `states/09-f01.jpg` to `STATES.md` and `index.json` (30 files, 29 listed).

**Contradictions**

- Apply K-1 everywhere the tree base appears.
- Mark `brief/LEGO-PIPE-007-R2.md` as **historical input**, superseded where later decisions differ. Its "P/F/H planned" status lines are stale.
- Fix J-01: it renders F-01 and O4 under "ON THE HORIZON" while the package reports F-01 built. Reconcile every journey status against `index.json`.
- Add an automated cross-artifact status/fact check so this class of drift fails rather than ships.

**Prototype defects**

- **Contrast.** Paper theme fails the brief's own fixed WCAG 2.2 AA constraint: `--dt-accent` 4.13:1, `--dt-prov` 3.54:1, `--dt-unres` 2.12:1 (`--dt-unres` also fails in blueprint at 2.93:1). The `-deep` variants already pass. Fix the values and add a contrast assertion to the token file so it cannot regress. Decide explicitly whether `--dt-unres` is ever text or only ever a fill.
- **Mock invariants.** F-01 displays "ENVELOPE · STUDS 104 of **−10,300 free**" and a tree at **−50 bricks**. Negative free area and negative height are not unaudited-but-plausible — they are impossible. Add range and invariant checks to the mocks themselves.
- **P-01 trade-off.** All three priorities currently produce identical outcomes (2 shops, $57.54–$62.34, ~9 days). The sheet's entire premise is showing a trade-off; re-seed the shop set so lowest-total, fewest-parcels and soonest visibly diverge.
- **Rail / Ring.** F-01's toggle says "Rail" while its own readouts say "overlaps the ring" and "inside the ring". Pick one string now; RESEARCH-01 settles it later.
- **Three.js is imported twice** in A-01 (`WARNING: Multiple instances of Three.js being imported`). Duplicate instances break `instanceof` across module boundaries.
- `<title>` is empty on all nine sheets. `<html lang>` is absent on all nine. Both trivial; both in §6's contract.
- Layout: A-01 and C-01 titles collide with the meta row at ~1280px; C-01's "IN THE VILLAGE" toggle label is clipped; C-01's schematic labels overlap.
- Drop the "Prototype A/C/P —" title prefixes for production naming. (Cosmetic — "Prototype" is a build-status prefix, not the prepositional jargon the naming rule targets.)

**Capture**

- Re-capture screenshots **full-page**, both themes. The current set is 924×540 viewport crops, so everything below the fold on every sheet is unreviewable by anyone who cannot run the prototypes.

---

## 3. Journey architecture — full hierarchy

The current J1–J13 list mixes entry channels, lifecycle phases, analysis activities and cross-cutting governance. Overlaps make ownership ambiguous; gaps leave real work unmodelled. Known collisions: J1/J2 are one human episode; J3/J6 both decompose a model; J4/J8 are both integration verification; J5 colour adaptation is a controlled transformation, not a lifecycle stop; O4/J11/F-01 are one family journey at three zoom levels; J9 measurement and J12 agent review are cross-cutting loops wrongly pinned to single stops.

**Preserve J1–J13 as traceable aliases.** Do not delete them; map each to its new home so existing specs, screenshots and decisions stay citable.

### 3.1 L0 — the annual human story

> Together, the family imagines a village, proves it can fit and run, obtains only what is needed, builds and enjoys it, then preserves what was learned for next year.

### 3.2 L1 — eight lifecycle journeys

Each gets: intent · entry condition · exit condition · owner · gate (if any) · what it produces · which sheets instantiate it · open questions.

1. **Frame the season** — intent, boundaries, people, budget, schedule, existing assets.
2. **Grow the design** — bring in sources or ideas, qualify them, create components, explore options, compose the layout.
3. **Prove the plan** — verify geometry, operations, appearance, evidence, stakeholder alignment; resolve uncertainty.
4. **Commit the baseline** — review a defined configuration, accept or waive findings, release an exact shortage list.
5. **Source the gap** — observe lots, choose a strategy, order externally, record confirmations, manage drift.
6. **Build and commission** — receive, inspect, stage, assemble, test, diagnose, accept.
7. **Enjoy and adapt** — operate it; respond to failures and new story ideas through controlled change.
8. **Close the season** — reconcile as-built, disassemble, inventory, store, record lessons, branch next year.

### 3.3 L2 — nine cross-cutting control loops

Each may begin inside any lifecycle journey and **must return the user to the work they interrupted**. That return is the part most likely to be skipped; it is mandatory here.

Resolve an ambiguity · capture a measurement · raise and answer a request · compare alternatives and record a decision · verify a claim and attach evidence · review/approve/waive a gate · assess blast radius and invalidate stale results · recover, undo, supersede or resume · review an agent handoff.

### 3.4 Work order — binding

The demo is 2026-12-25, which is 14 weeks out. **That is not the deadline.** The deadline is set by physical lead times, and it is roughly five weeks away:

| Date | Weeks from issue (2026-09-17) | Milestone |
|---|---|---|
| 2026-10-14 | 4 weeks | **Railbed geometry validated** — the layout provably fits around the 16×16 tree with the train's known track |
| **2026-10-21** | **5 weeks** | **ORDER-BY GATE — BOM and procurement plan trusted enough to spend money against** |
| 2026-10-28 | 6 weeks | Orders placed (multi-shop BrickLink, international, into holiday congestion) |
| 2026-11-25 | 10 weeks | All parts received and inspected |
| 2026-11-29 | 10.5 weeks | Physical build begins |
| 2026-12-20 | 13.5 weeks | Build and commissioning complete |
| 2026-12-25 | 14 weeks | Demo |

Everything in this brief is sequenced against the **order-by gate**, not against the demo.

**Tier 1 — must be right before 2026-10-21.** The spine that turns a design into correct bricks:

- **Journey 2 · Grow the design** and **Journey 3 · Prove the plan** — enough to establish that the railbed, ballast and MILS landscape fit the 16×16 tree and the train's track.
- **Journey 4 · Commit the baseline** — releasing an exact, versioned shortage list.
- **Journey 5 · Source the gap** — through order placement, per §5D.
- **Geometry correctness** (§7.1) and **BOM correctness by basis** (C-01).
- The **capture measurement** and **verify a claim** control loops — these produce the evidence the BOM rests on.
- The §8 gate contract, for the **procurement release gate only**.

**Tier 2 — must exist before parts arrive (2026-11-25).**

- **Journey 6 · Build and commission**, and the whole of §5D from *record external order confirmation* onward: shipped → delivered → receive → inspect → discrepancy → allocate.
- Schema §7.3 (inventory dimensions). This is where the ordered→owned defect stops being theoretical: real parcels will arrive with wrong colours, short counts and substitutions, and if the model cannot represent that, the record is falsified at exactly the moment the demo depends on it.

**Tier 3 — designed in parallel, lands behind the build.**

- Journeys 1, 7, 8; the remaining control loops; the four subjourneys in §5 A–C; **F-01's iPad cycle**; the family-side gate experience; the A-01 viewer/canvas split.

Two prioritisations inside Tier 1 that are easy to get backwards:

1. **BOM correctness outranks procurement optimisation.** If the shop-combination search picks a suboptimal set, the cost is a few dollars. If the BOM is wrong, the cost is Christmas. Get the parts list and its basis right first; the optimiser can stay rough.
2. **The record outranks the automation.** What the demo proves is that the decisions, provenance and plan were captured and can scale — not that every step was automated. Capture first, optimise later.

**A standing instruction to protect the build:** if the procurement path is not trustworthy by 2026-10-21, **the operator orders anyway** by whatever hybrid means works, and the system records it after the fact. The physical deadline is hard; the software's is not. Do not design anything that makes a manual or semi-manual first order impossible to represent — a retroactively-entered order with honest provenance is a supported case, not a workaround.

### 3.5 L3 — interaction flows

Screen-level states, commands, errors, announcements and recovery paths, for every designed loop. **A sheet is not a journey.** One sheet may implement several L3 flows; say which.

---

## 4. A-01's 3D viewer — settled posture (K-3)

The viewer is real, works offline, and is currently a 756×240 strip that reads as decoration. Its role is now larger and specific:

- **One source of truth.** The 3D view and the 2D canvas render the *same* canonical geometry. Not a parallel model, not an export. If they can disagree, the design is wrong.
- **Lo-fi render, truthful dimensions.** No brick-accurate meshes. Massing only — but every dimension, clearance and position is real, so what you see is checkable. Fidelity is in the measurements, not the materials.
- **It answers questions.** Clearance under the branches against the 16×16 tree, track banking and grade, collisions between placed things, what a separation peel actually reveals, whether the train's right-of-way is clear. These are the questions the 2D canvas cannot answer honestly.
- **Transforms propose, never persist.** Adjusting in 3D produces a *proposed* change the operator confirms. This maps exactly onto patterns already in the bundle — A-01's dashed-proposed vs solid-placed plantings, and the restate-before-save rule. Reuse them rather than inventing a third pattern.
- **It needs real screen space** and its own acceptance criteria. A verification surface you cannot see is not one.

Design consequence worth stating: because both surfaces now read one canonical representation, the geometry decision in §7 is load-bearing for two views, not one.

---

## 5. Four subjourneys requiring explicit design

### A. Family idea → visible outcome

Rejoin (what changed since last visit) → imagine (tap/type/voice/reference) → rough-place (reserve space without pretending a build exists) → understand consequences (fit, height, track, cost, and *what is still unknown*, in age-appropriate language) → refine → **choose evidence depth** → submit (preview exactly what James receives, and what is still a guess) → collaborate (answer a clarification, revise, withdraw) → receive the decision (accepted / parked / declined / needs revision, with the reason in the family's language and what happens next) → see it realized (connect the approved request to its place in the village).

Two requirements:

- **Modelling is not a mandatory final step.** Step 4 "Model it" is adult-shaped and currently sits at the end of a child-shaped flow. Sending must be available after the story step, with modelling as an optional return visit.
- **Sending cannot feel like throwing an idea over a wall.** The next visit must show whether James answered and what changed because of it. This is the single most important human requirement in this brief.

### B. Agent uncertainty → safe resumption

Detect ambiguity and identify the exact affected field → stop propagation only where it matters, let unrelated work continue → ask the smallest answerable question, with source wording, interpretation and consequence → person answers by tap/type/talk or parks it → **pending restatement**: "I will change X from A to B; this will affect Y" → person confirms or corrects → commit a new field revision with evidence and authority, invalidate dependent checks → **resume the interrupted activity at the exact point it can safely continue**.

Amend "never asks twice" to: never re-ask a resolved ambiguity **for the same source revision**. New or conflicting evidence may reopen it by superseding the prior resolution.

The pending-restatement state is a **new explicit state**, not a toast. It is also the clearest instance of §6: an AI restatement that is not announced is not perceivable.

### C. Review → controlled baseline

Identify the exact candidate revision → summarize changes since last baseline, grouped by human consequence → show unmet requirements, failed/not-run checks, unresolved requests, evidence freshness → inspect alternatives and stances, **without treating AI stance as authority** → resolve findings (correct / accept / waive with rationale / defer with owner and due trigger / reject) → preview downstream impact (BOM, cost, procurement, build order, story, prior approvals that will change) → approve the exact baseline with role and timestamp → freeze outputs, generate downstream work → on later change, **mark affected results stale and open a change review**.

A change pulse is feedback, not impact management. A changed dependency must visibly stale or reopen what depends on it.

### D. Procurement approval → usable inventory

Receive an approved, versioned shortage list → fetch and cache dated lot observations (currency, condition, region, quantity, source policy) → produce genuinely distinct strategies and explain the trade-offs → **revalidate availability and price immediately before the user leaves to buy** → record external order confirmation **without claiming possession** → track ordered → shipped → delivered → receive and inspect quantity, identity, colour, condition; record discrepancies and returns → move accepted pieces into available inventory, then allocate to a specific baseline → recompute shortages and surface any remaining gap.

`ordered → owned` is the single most damaging simplification in the current package. It skips shipping, receipt, inspection, discrepancy and allocation, and it will silently falsify every subsequent shortage calculation.

---

## 6. Accessibility contract — mandatory, acceptance-gating

**Read this as an architectural requirement, not a compliance chore.**

The accessibility tree is the only stable, semantic, queryable surface a browser exposes. Assistive technology reads it. So do agents driving the UI, test harnesses, evals, and any host trying to route. When it is empty, all of them fall back to pixel and DOM archaeology against generated class names that change every build. This project's entire premise is agents and humans operating on the same surfaces — which makes a missing accessibility tree a failure of the *agentic* architecture as much as of inclusion.

The current state, measured across five sheets under a real browser:

| Sheet | `<h1>` | landmarks | `lang` | `<title>` | `aria-live` |
|---|---|---|---|---|---|
| C-01 | 0 | none | absent | empty | 1 |
| F-01 | 0 | none | absent | empty | 1 |
| A-01 | 0 | none | absent | empty | 1 |
| Hub | 0 | none | absent | empty | **0** |
| P-01 | 0 | none | absent | empty | **0** |

Hub carries **zero ARIA attributes of any kind**. P-01 re-prices an entire procurement plan on a priority change and announces nothing.

Most pointedly: the bundle's own safety pattern — *"the AI restates what it changed before anything is saved"* — is specified and then built somewhere no assistive technology and no agent can observe it. A safety behaviour that cannot be perceived is not a safety behaviour.

**Required on every sheet:**

1. Exactly one `<h1>`; a correct heading hierarchy below it; no styled text standing in for a heading.
2. A landmark skeleton — `banner` / `nav` / `main` / `complementary` / `contentinfo` as applicable — so a sheet can be navigated structurally.
3. `<html lang="en">` and a meaningful, unique `<title>`.
4. An accessible name on **every** interactive control. Icon-only and glyph-only controls included; the sticker palette especially.
5. A live region for every derived or asynchronous change: P-01 repricing, A-01 placement and validation, F-01 status line and fit flags, Hub filtering, gate invalidation, and **every AI restatement**. Politeness level specified per case.
6. Keyboard operation for every canvas interaction, and the nonvisual spatial alternative the original brief already mandated and no sheet has yet.
7. Focus management on every disclosure, popover, modal and card expansion — including where focus goes on dismiss.
8. Per-sheet **announcement spec**: for each state change, what is announced, in what words, at what politeness. This goes in the spec, not just the build.

**Acceptance criteria — these fail a build, not a review:**

- Automated axe-style check passes with zero serious/critical violations.
- An **accessibility-tree snapshot** is captured per sheet and diffed on change. This is the agent-facing contract; treat a regression in it exactly as you would a broken API.
- Contrast assertions pass in both themes (see §2).
- Every control reachable and operable by keyboard alone, verified per sheet.

---

## 7. Schema corrections to carry (requests, not authoring)

`packages/schema` remains the contract and is not authored here. Record these as requests.

**7.1 Geometry — the correction that invalidates a pending request.** `Component.placement = integer stud position` **cannot represent** the ¼-stud fraction mode that the A-01 spec and decision `09-16 10:48` both promise, and `clear_height: bricks` abandons the declared integer base for Z. Request instead: canonical **integer LDU** for X/Y/Z; studs, plates and bricks as *display preferences only*; rotation persisted in its own explicitly declared unit, independent of position. Per K-3, both the 2D canvas and the 3D viewer read this one representation.

**7.2 Split `basis`.** `own-on-arrival | buy-adapted | buy-research | story` fuses acquisition, transformation, epistemic maturity and rationale in one field — a direct violation of the bundle's own axis-separation rule. Proposed: four axes stored on the row, two derived.

| Axis | Stored | Values |
|---|---|---|
| `acquisition` | PartRow | `inventory · included_with_set · buy · fabricate` |
| `transformation` | PartRow | `unchanged · recoloured · substituted · adapted` |
| `epistemic_state` | PartRow | `asserted · inferred · measured · computed · verified` |
| `disposition` | PartRow (design side only) | `proposed · reviewed · approved`, with revision and supersession |
| `need_origin` | *derived* from parent Request/Design | `story · design · operational · replacement · policy` |
| `design_origin` | *derived* from parent Design | `official · external_moc · own · generated · reconstructed` |

Origin is a property of why a thing exists — the Design or the Request — not of each BOM row. **Open:** whether `need_origin` must be row-level (a part serving two needs). Returned to ChatGPT; treat as provisional and do not design a UI that assumes either answer is final.

**Fulfilment is not a state of the BOM row.** An earlier draft proposed `workflow_state = proposed · reviewed · approved · ordered · received · allocated` on `PartRow`. That reproduced exactly the defect this section exists to fix — it fuses design disposition, order fulfilment, receipt/inspection and inventory reservation into one enum, and contradicts §7.3. It is **withdrawn**. A BOM row is a *demand*; it never becomes "received". Orders, receipt records, inventory lots and allocations satisfy quantities against it. Express fulfilment as typed relations and independent records:

- **design disposition** on the BOM/design row, with revision and supersession (above);
- **order-line state** on procurement records;
- **receipt and inspection results** on received lots;
- **availability** derived from accepted quantities less holds;
- **allocation** as a quantity-bearing relation between inventory and a baseline/BOM demand.

Exact names and cardinalities are the schema owner's call.

The UI keeps composing one plain-language summary from all of this. **Users must never meet a wall of enums** — the composition is the deliverable, the axes are the plumbing.

**7.3 Inventory.** Separate acquisition · possession · inspection · availability · allocation · location · condition. These are not one lifecycle enum. "Owned/available" occurs only after receipt and reconciliation.

**7.4 Envelopes.** A single width × height × clear-height box is insufficient under branches and around curved track. Request footprint geometry, orientation, keep-out zones and height/clearance profiles.

**7.5 Build order.** `disassembly_rank` alone cannot derive every valid assembly order or parallelizable sub-build. Request a dependency graph.

**7.6 Work items.** Unify `ClarificationRequest`, `Request`, `Ask` and `Conversation` into one envelope with typed purpose — or document non-overlapping invariants and transitions. Four near-synonyms will be used interchangeably otherwise.

**7.7 Request outcomes.** Add `needs-revision · withdrawn · superseded · implemented · reopened`, plus season and archive facets. Never deleted stays — but a multi-year project needs archival and supersession or the card silently fills.

**7.8 Versioning.** Option stances, fit results, measurements, rights decisions and requests each need subject revision, author, timestamp, supersession.

**7.9 Commercial observations.** Currency, lot condition, seller region, tax treatment, shipping basis, minimum-purchase rule, observed timestamp, freshness/expiry.

**7.10 Rights are permissions, not a pass/fail flag.** Distinguish acquire · retain · inspect · transform · derive · render · show-to-family · redistribute · export.

**7.11 Action history.** Do not assume the action log is an event-sourcing model. Define command/event identity, idempotency, undo boundaries and snapshot strategy before relying on it for recovery.

---

## 8. Gate contract — formal gates only

Every **formal** gate — baseline release, procurement release, rights pass — is representable as: `gate_id` / `gate_type` · `subject_ref` / `candidate_revision` · `entry_criteria[]` · `required_evidence[]` (types, methods, freshness) · `checks[]` (pass/fail/not-run/waived, with deterministic rule versions) · `open_findings[]` (severity, owner, due trigger, disposition) · `authority_required` · `decision` (approve / approve-with-waivers / reject / return-for-work) · `rationale` / `waivers[]` · `output_baseline_ref` · `invalidated_by[]` · `supersedes`.

The interface still presents this as a quiet modal and a friendly stamp. The rigor lives underneath; it is not reduced to the stamp.

**The family surface is excluded by design (K-7).** F-01's send is a **proposal**, not a gate submission. `Request` and `GateRecord` stay distinct types with an explicit join; the gate happens on James's side when he folds a proposal into a baseline. A gate contract applied to a nine-year-old placing a snowman converts the best property of this design — *the kids use the real tools* — into paperwork experienced as rejection. A proposal can be answered conversationally; a gate decision cannot.

Also: **AI is not a peer decision authority.** It may offer analysis or a recommendation carrying its method and evidence. Human decision authority stays separate and visibly so.

---

## 9. Human-experience corrections

- **Teach at the decision point, not all at once.** Several opening explainers — P-01's especially — are dense walls before the user has a reason to care.
- **"Envelope" should not become family vocabulary.** It is useful internal structure. Present it as *idea → the space it needs → a build that fits*. "Make a scene" remains the strongest family metaphor; keep it.
- **F-01 has high hidden-mode risk.** Armed placement, selection, pan, resize, side views and zoom all compete on one surface. Require persistent mode feedback, escape/cancel available everywhere, and short reversible operations.
- **Design for interruption.** Every return to any sheet answers three questions: *What changed? What needs me? What is safe to do next?*
- **`@boys` is insufficient as a stakeholder identity.** Individual family members may disagree; authorship, consent and replies must stay attributable without overexposing private detail.
- **Phone read-only is a feature, not a fallback.** Design "see my scene / see the answer" as a positive experience. The boys will want to look at their village on a phone.
- **Kid-facing register holds:** plain, never talking down, ages ~9.5–11. James named sparingly.

---

## 10. Deliverables — in tier order (§3.4)

**Tier 1 — by 2026-10-21, the order-by gate**

1. **Geometry and fit**: the §7.1 canonical-representation request, A-01's 3D viewer per §4 as a *verification* surface, and proof that the railbed, ballast and MILS landscape fit the 16×16 tree and the train's track.
2. **BOM correctness**: C-01's parts-list-by-basis with the §7.2 axis split, and the measurement + verification control loops that its numbers rest on.
3. **Journeys 2, 3, 4, 5** designed to screen level (L1 + L2 + L3).
4. **Procurement release gate** per §8, plus the §5D flow through order placement — including the retroactive/manual-order case from §3.4.
5. **Mechanical integrity pass** per §2 — it gates trust in everything above.
6. **Accessibility contract** per §6 applied to A-01, C-01 and P-01 first.

**Tier 2 — before parts arrive, 2026-11-25**

7. **Journey 6 · Build and commission**, and §5D from order confirmation onward: shipped → delivered → receive → inspect → discrepancy → allocate → recompute shortages.
8. Schema requests §7.3 (inventory dimensions) and §7.9 (commercial observations).
9. Accessibility contract extended to the remaining Tier-1/2 sheets.

**Tier 3 — in parallel, landing after the build**

10. **Journey model completion**: L0 statement; all 8 L1 journeys; all 9 L2 control loops; L3 flows; J1–J13 alias/trace map.
11. **Subjourneys §5 A, B, C** with states, errors, recovery and announcements.
12. **F-01 responsive cycle** — iPad landscape and portrait, touch, interruption, undo, submit → response → realization, re-entry. Retains its full requirements; loses its urgency (K-8).
13. **A-01 viewer/canvas split** specced properly, or an explicit deferral recorded as a decision. Do not hand it to Claude Code under-specified.
14. **Family-side gate experience** with the §8 exclusion made visible in the design.
15. Remaining schema requests §7.4–7.8, 7.10–7.11.

**Throughout**

16. **Per-sheet acceptance criteria** and §6 announcement specs, delivered with each sheet rather than batched.
17. **Full-page screenshots**, both themes, per sheet as it lands.
18. **New dated decision entries** for K-1 … K-9, citing `HANDOFF-LEGO-PIPE-010`. Append; never edit prior entries.

**Out of scope:** Frame contract decisions (K-4); schema authoring; any production code; the two engineering spikes, which sit with Claude Code.

---

## 11. Readiness boundaries — two staged code handoffs

An earlier draft said no code handoff occurs until the *entire* journey hierarchy and cross-surface package were complete, and then named the family slice as the first thing to build. Read literally that postponed the procurement spine until after the build it exists to support, while building a deferred surface first. Both halves are corrected here.

**Boundary 1 — scoped Tier-1 handoff.** Permitted once these are coherent: the §2 mechanical integrity pass; the §7.1 canonical geometry request; the §7.2 BOM axis correction; Journeys 2–5 at Tier-1 depth; the procurement-release gate (§8); the measurement and verification control loops; and acceptance criteria for A-01, C-01 and P-01.

This authorizes **an operator-facing thin slice only**, and remains subject to James's explicit implementation authorization. The first end-to-end slice follows the actual critical path:

> canonical/measured geometry → verified design baseline → exact shortage list (BOM) → procurement-release decision → export or **manual-order capture with provenance**

That last step is deliberate: it is the §3.4 escape hatch made buildable, so a hybrid first order is a first-class recorded case rather than a gap in the record.

**Boundary 2 — full-platform handoff.** Follows completion of the remaining lifecycle journeys, the remaining control loops, the family journeys, and the cross-surface acceptance contract. The family slice — **family proposal → operator review → accepted layout branch** — is the first slice of *this* boundary, not of Boundary 1, unless James explicitly reprioritizes it.

**What "complete" means at Boundary 2:** one authoritative fact and status manifest with no contradictions; the journey hierarchy complete with J1–J13 traceable into it; every formal gate carrying entry, exit, waiver and invalidation rules; the canonical geometry decision settled with both views reading it; accessibility announcements and the accessibility-tree contract specified per sheet and passing; representative error, stale-data, interrupted and recovery states; and per-sheet acceptance criteria.

## 12. Dispatch dispositions against CORR-LEGO-PIPE-015

| Item | Disposition |
|---|---|
| **A-01 · frontmatter** | **Accepted on conclusion, rejected on diagnosis.** The reviewed copy was `Pasted markdown(6).md`; pasting mangled the block. The issued artifact opens `---`, closes `---`, parses as YAML, and contains no `## document_id` heading. **But** its frontmatter was missing nine keys required by `lego-pipe-memo/v1`, so it genuinely could not enter the register or act as a work order. Repaired and preflight-passed. **Root cause is register rule N-03: transfer by attachment, never paste.** |
| **A-02 · Frame authority** | **Accepted in full.** K-4 rewritten to your language. Claude Code evidences and recommends; James decides; no settling by scaffolding. |
| **A-03 · staged handoffs** | **Accepted in full.** §11 replaced with two readiness boundaries; the first slice now follows the procurement spine; the family slice moved to Boundary 2. |
| **A-04 · `workflow_state`** | **Accepted in full, and it was the worse error of the two.** §7.2 had reproduced the exact defect it rejects `basis` for. Withdrawn; fulfilment expressed as typed relations per your list. |
| **Clerical · time axis** | **Accepted.** Column relabelled "Weeks from issue"; demo row completed at 14 weeks. |
| **New · numbering** | Your memo was issued as `CORR-LEGO-PIPE-011`, a number held by the build-harness thread (`LEGO-PIPE-011-from-studio-to-stage`, R2 accepted). Registered as **015**. This brief takes **014**, which the register had reserved for it. |
| **New · ID namespace collision** | The preflight's finding-ID pattern `[RNC]-\d{1,2}` also matches **sheet** IDs — `C-01` is a sheet, `C-1` was a constraint. Constraints in this brief are renamed **K-1…K-9**. Recommend the register adopt a reserved prefix for findings and forbid `A/B/C/D/F/H/J/P` as finding prefixes. |

— issued by Claude (Cowork), under James (`@jfo`)
Citing `CORR-LEGO-PIPE-008` and `CORR-LEGO-PIPE-009`
