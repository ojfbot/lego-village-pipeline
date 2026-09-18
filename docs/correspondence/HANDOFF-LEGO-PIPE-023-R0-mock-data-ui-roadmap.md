---
correspondence_schema: lego-pipe-memo/v1
memo: HANDOFF-LEGO-PIPE-023
revision: R0
status: for_review
memo_type: handoff
title: "The drafting table on fixtures — a mock-data UI roadmap, taught before it is built"
subtitle: "How the Claude Design prototypes become a running app against typed fixtures; why the fixtures are the schema gate; what the fleet sees; and the teach-first cadence every dive follows"
date: 2026-09-18
thread: app-stack
cluster: play-well
project: LEGO Village Pipeline
from:
  actor: "Claude (Cowork)"
  role: coordinating_reviewer_and_handoff_author
  provider: Anthropic
to:
  - actor: James
    handle: "@ojfbot"
    role: operator_and_final_authority
    provider: operator
  - actor: "Claude Code"
    role: implementer
    provider: Anthropic
in_reply_to:
  memo: HANDOFF-LEGO-PIPE-019
  revision: R0
authority:
  decision_owner: James
  dispatch_authority: James
  implementation_authorized: "none until James accepts this memo; then Dives 1–3 (foundations, components, Hub) — Dives 4–6 each wait on the debrief of the dive before"
  production_code_authorized: false
register:
  number: 023
  allocated_by: "proposed — James confirms before dispatch (rule: numbers are allocated by the operator)"
  allocated_on: 2026-09-18
  note: "authored as v1 under the .13 dual-schema migration so the committed validator can pass it; re-issue as v2 at R1"
repos:
  - ojfbot/lego-village-pipeline
  - ojfbot/play-well-library
tags:
  - app-stack
  - mock-data
  - fixtures
  - schema-gate
  - drafting-table
  - roadmap
  - pedagogy
  - fleet-tracking
attachments:
  - {name: "attachments/HANDOFF-LEGO-PIPE-023-R0-roadmap.html", role: "the chart — ladder, timeline to the 21 October gate, package dependency map, one card per dive; open in any browser, no server"}
argument: >-
  In which the app stack, which today exists only as ten Claude Design prototypes,
  is given a road to running code without breaking the gate in 019 §6; the operator's
  ruling that the mock fixtures ARE the schema gate is worked out into a rule for what
  a fixture must be; the Tier-1 spine (Hub, A-01, C-01, P-01, M-01) is cut into six
  dives on a PADI-shaped ladder — briefing, demonstration, confined water, performance
  requirement, debrief — each taught to the operator by memo and chart before anything
  is built; Frame is kept out of the experience plane and in the tooling plane, where
  the fleet's morning cockpit watches the dives land; the calendar is drawn backward
  from 21 October; and six questions are put to the operator that nothing below may
  answer by scaffolding.
parts:
  "0": "Orientation — what exists, what this memo changes, how to read it"
  "1": "The one idea — fixtures are the schema, so the mock UI is the gate package"
  "2": "The ladder — PADI pedagogy as the cadence of this track"
  "3": "The six dives — scope, what is taught, what is built, what proves it"
  "4": "Where the app lives and what Frame sees"
  "5": "The calendar, backward from 21 October"
  "6": "Amendment to 019 §6 — proposed wording"
  "7": "Questions for James — nothing below may answer these by building"
  "8": "What happens on acceptance"
provenance:
  source_artifacts:
    - {name: "correspondence/HANDOFF-LEGO-PIPE-019-R0-initial-handover-claude-code.md", role: "the founding handover; §6 is what this memo amends"}
    - {name: "docs/design/H-01-R1/", role: "design package as committed (sha256 e5b4857c…70ce); specs/, schema-requests.md, seam.md, ADDENDUM-A1 read in full"}
    - {name: "docs/correspondence/CORR-LEGO-PIPE-020-founding-acts-report.md", role: "repo state as founded"}
    - {name: "docs/correspondence/REGISTER.md", role: "register read at 2026-09-18.14 on branch governance/pr-flow — v2 ratified at .13, PR-flow in force at .14"}
    - {name: "operator answers, Cowork session 2026-09-18", role: "four rulings: fixtures are the gate; Frame at tooling level only; Tier-1 spine + Hub; teach-first by memo and chart"}
  method: "read of both repos and the design package as they stand today; roadmap derived from the sheet specs' 'mock boundaries' sections and schema-requests.md; no prototype QA; no code"
---

# HANDOFF-LEGO-PIPE-023 — The drafting table on fixtures

James, Claude Code —

This is the first memo in a new thread, **app-stack**. It answers one question: *how does the app that today exists only as Claude Design prototypes become a running thing on your Mac, on fake data, without breaking a rule we wrote last night?* It is written to be argued with. The chart in `attachments/` is not decoration; read it first, then come back.

---

## 0. Orientation

**What exists.** Two repos, founded (020). Since this morning: `lego-pipe-memo/v2` is ratified (CORR-022, register `.13`) and PR-flow is in force for every contributor (`.14`). This memo is authored as **v1** so the committed reference validator can pass it, exactly as the `.13` transition memos were; it is re-issued as v2 (R1) once the v2-aware validator lands and before it acts as a work order. It reaches `main` by pull request. The design package H-01 R1 is committed verbatim with ten sheets as standalone HTML, per-sheet specs, `schema-requests.md`, and a decision ledger to DEC-035. Stream A (the build harness — Studio, Blender, USD, brickcore) is in flight under 011-R2 and is **not** touched by this memo. No app code exists. No `package.json` exists.

**What the operator ruled today** (Cowork session, 2026-09-18), which this memo turns into a plan:

1. The mock fixtures **are** the schema gate — sequenced schema-first, the same work satisfies 019 §6 rather than dodging it.
2. Frame does **not** need to exist at the UI or experience level yet. It needs to be integrated at the tooling level and with ojfbot fleet tracking, so the **morning cockpit** sees this work.
3. Scope is the Tier-1 spine plus the Hub: **Hub · A-01 · C-01 · P-01 · M-01**. B-01 as a shared pattern only.
4. Before anything is implemented — service architecture, schema shape, application design — it is **taught to James and refined by memo correspondence**, leaning on visual artifacts and strong didactic patterns. PADI pedagogy is the named model.

**How to read this.** §1 is the idea; if you disagree with §1, stop and say so, the rest falls. §2 is the cadence. §3 is the plan. §4–5 are where and when. §6 is the amendment. §7 is what I need from you. Claude Code builds nothing from this memo until it is accepted and a number is confirmed.

---

## 1. The one idea — fixtures are the schema, so the mock UI is the gate package

019 §6 says: *no workflow UI before James approves the schema.* The spirit of that rule is that a screen built on a guessed data shape hardens the guess. The letter would forbid a mock-data UI outright.

The way through is to make the mock data *unable* to be a guess:

> **A fixture is a record that passes the same validator real data will pass, carries the same evidence axes real data will carry, and is loaded through the same adapter interface real data will be loaded through. The UI cannot tell which one it is looking at.**

Four consequences, each of which is a rule Claude Code follows:

| Rule | What it means in code | What it teaches |
|---|---|---|
| **F1 · Typed, validated** | Every fixture file is parsed by `packages/schema`'s runtime validators at load. A fixture that fails is a build failure. | The schema is exercised by the UI from day one, so an unrepresentable case (a retroactive order, a parked claim) shows up as a *broken fixture*, not a broken screen. |
| **F2 · Evidence-carrying** | Every numeric value in a fixture carries `epistemic_state` (asserted · inferred · measured · computed · verified). Fixture numbers are never `verified`; MOCK MATH is `computed` with a `method: "fixture"` marker at the adapter boundary. | The evidence chips (◇ ■ ▲ ○) render honestly from the first render. The design package's standing rule — *every number shown carries its chip* — is enforced by the type, not by discipline. |
| **F3 · One seam** | `DataSource` is an interface with two implementations: `fixtures` and, later, `real`. Sheets import the interface. Nothing else in the app knows the difference. | "Swap mock for real" is a one-line change per entity, and the place where the two differ is visible and reviewable. |
| **F4 · Scenario, not sample** | The fixture set is **our village**: the 41843 tree at 16 × 16 studs, 16 R40 curves at 53400 LDU, Sections of 2 × 2 MILS 32 × 32, railhead height unknown, the Q13 inner-corner overlap present. Not lorem-ipsum bricks. | The fit checks in A-01 return the same honest **BLOCK** the prototype returns, in code, from the same inputs — which is exactly what 019 §4.4 asks for on 14 October. |

With those rules, the thing that clears the gate is the same thing that renders the screens: `packages/schema` + its fixtures + the per-sheet acceptance criteria (the G-2 debt from 019 §4.3). You sign that package; the UI is already running on it. That is what "mocks are the gate" means, made precise.

What this does **not** do: it does not authorise real BrickLink fetches, real Blender/Studio calls, or the Frame host. Those stay behind their own gates (Q5, Q6, 011-R2, K-4).

---

## 2. The ladder — PADI pedagogy as the cadence of this track

You asked for teach-first with strong didactic patterns, and named PADI. Taking that seriously, not as a metaphor: an Open Water course has a fixed shape, and it has that shape because it works on people who are about to do something with real consequences on the first try.

| PADI | Here | Artifact |
|---|---|---|
| **Knowledge development** — theory before water, in short sections with a quiz at the end of each | **Briefing memo** per dive: one diagram, the vocabulary of that dive, the three ways it can go wrong, and a short *check yourself* (five questions James answers in the reply) | `CORR-` memo + chart, ≤ 900 words |
| **Demonstration** — the instructor does the skill, slowly, before the student tries | **The Claude Design standalone** for that sheet, opened side by side with the spec. Not built from; watched. | `docs/design/H-01-R1/standalone/*.html` |
| **Confined water** — the skill, in a pool, where mistakes are cheap | **Fixtures.** The sheet runs on `DataSource = fixtures`. James operates it. Nothing costs money, nothing touches Studio or Blender, nothing touches the family. | the running app |
| **Performance requirement** — the thing the student must be able to *do*, stated before the dive, mastery not exposure | **Per-sheet acceptance criteria**, proposed in the briefing, signed by James before the dive starts, checked at the end | the G-2 debt, discharged one sheet at a time |
| **Debrief** — what happened, what to fix, logged | **Findings memo** ≤ 600 words, `[unverified]` on anything not directly observed, and a register row | `CORR-` memo |
| **Open water** — the real thing, under supervision | `DataSource = real`, one entity at a time, behind the 14 Oct and 21 Oct gates | Dive 7, not in this memo's scope |

Two PADI rules carry over unchanged and are the spine of the cadence:

- **Mastery, not exposure.** A dive is not done because the code merged. It is done when James can explain the mechanism back (the *teach-back*) and operate the sheet without help. If that isn't true, the debrief says so and the next dive waits.
- **Never skip the briefing.** Claude Code does not start a dive on the strength of this roadmap. Each dive has its own briefing memo, which James refines, and which allocates the dive's acceptance criteria. This roadmap is the course outline; it is not the lesson.

---

## 3. The six dives

Each row: what James is taught · what Claude Code builds · what proves it. Sheet behaviour is per the design package specs; nothing here re-designs a sheet.

### Dive 0 — Briefing (this memo)
- **Taught:** the fixture rule (§1), the ladder (§2), the map (chart).
- **Built:** nothing.
- **Proves it:** James's reply — refinements, confirmations, answers to §7.

### Dive 1 — Foundations: the workspace, the tokens, the schema-with-fixtures
- **Taught:** what a pnpm workspace is *for us* (one repo, several packages, one lockfile); what a token package is and why no hex is allowed in app code; what a runtime validator is and why fixtures go through it; what the contrast contract is and why D-1 fails it today.
- **Built:** `pnpm` workspace · `packages/tokens` (the design package's `dt/tokens.css` verbatim + generated TS map + **D-1 fixed** — `--dt-block` in blueprint lifted to ≥ 4.5:1 — with `check-contrast.mjs` as a CI gate) · `packages/schema` — types, runtime validators, state machines, **fixtures under F1–F4** for every entity the five sheets need (from `schema-requests.md`: Measurement, ClaimVerification, Request, Ask, Option, FitmentCheck, the four-axis PartRow, VendorLot, Order incl. manual/retroactive, GateRecord, PriceRevalidation, Priority-as-view, DecisionRecord, ActionLog) · neutral names `Item`/`Unit`/`Section` with `TODO(RESEARCH-01)` tags · a11y-tree snapshot harness (the design package's `dt/a11y-tree.js` walker, run in CI against each sheet, diff fails the build) · the fleet-tracking hook (§4).
- **Proves it:** every fixture validates; contrast check green; the *questions-before-contracts* batch (019 §7.2) delivered as this dive's debrief, because writing the validators is where the ambiguities surface.

### Dive 2 — The fifteen components, on fixtures
- **Taught:** why components come before sheets (a sheet is a composition; a component is a promise); what the evidence chips mean, one by one; what an accessible name is and why an agent needs it.
- **Built:** `packages/ui` — the 15 domain components in `index.json` (RequestCard, BasisChip, StanceChip, OptionStateRow, PartPopover, PlantingRow, ChangePulse, DecisionLogEntry, EnvelopeBadge, StickerTile, ApprovalGate, EvidenceChips, SegmentedLine, StatusLine, ActionLog) plus **ReleaseGate** and **PriorityStrip** from R1/A1, each rendered against fixtures in a component workbench, each with an a11y-tree baseline and its announcement sentences from `specs/ANNOUNCEMENTS.md`.
- **Proves it:** James opens the workbench, reads a BasisChip and says in plain words what the four axes on it are. Zero unnamed controls (measured, as 019 measured).

### Dive 3 — Hub with "Right now" — the first running sheet
- **Taught:** what the app shell is (routing by sheet id, theme, one `<h1>` per sheet, landmarks); what a *view over records* is (Priority derives from findings, facts-without-method and Q-items — it is not a store).
- **Built:** `apps/drafting-table` shell · Hub sheet index + decision log from the DEC ledger fixtures · **PriorityStrip** as a derived view over fixture records, the three cards seeded from the real state (measure the tree base · order the train · confirm the fit) · done / not-today with the no-nag contract from ADDENDUM-A1 · persistence of dispositions (local, dev storage per 011-R2).
- **Proves it:** a running app on `localhost` that James opens every morning; the A1 review question ("does no-guilt hold when all three are parked?") answered by use, not by argument.

### Dive 4 — A-01 Layout Canvas: geometry in code, the six checks, the honest BLOCK
- **Taught:** integer LDU and why studs/plates/bricks are display units only (014 §7.1); what the six fit checks are, one diagram each; what Q13 is and why a BLOCK here is the design doing its job.
- **Built:** `packages/geometry` — canonical integer LDU for X/Y/Z, rotation in its own declared unit, R40 math (16 × 53400 centre-line), envelope + the **six deterministic fit checks** with property tests and golden cases · 2D canvas and 3D viewer (Three.js **pinned in the repo**, never CDN — D-3; Q12 resolved in the same act) reading one representation · exact-transform card · layer rig · Section selection with NE as anchor · planting proposals with the restate-before-save pattern on a mocked AI client.
- **Proves it:** the six checks run in code on the F4 scenario and return **BLOCK** on the 8 × 8 inner-corner overlap, with the same numbers the prototype shows. That is the 14 October milestone. An independent audit of the math is opened as an issue, not assumed.

### Dive 5 — M-01 and C-01: the evidence, then the list that rests on it
- **Taught:** the two loops in M-01 (measure · verify a claim) and the return-to-caller rule; the four stored axes and two derived axes on a part row and why "basis" was split (014 §7.2); what a GateRecord is and why the stamp is quiet and the record is loud.
- **Built:** M-01 (facts and claims on fixtures, pending restatement, earlier-values-kept, blast-radius list, `?from=` return) · C-01 (schematic toggle, sources by basis, options with stances, requests never deleted, parts list by the four axes with BrickLink low–high ranges from `PriceObservation` fixtures, approval trail, **ReleaseGate** at the end emitting `?released=`).
- **Proves it:** James records a real measurement of the tree base in M-01 and watches which C-01 rows go ▲ STALE. The BOM rows exist with honest chips before any procurement optimisation exists — *BOM correctness outranks procurement optimisation.*

### Dive 6 — P-01: buying the gap, on six mock shops
- **Taught:** the shop-combination search (exhaustive small-n, heuristic beyond) and what deterministic tie-breaking means; revalidation TTL; why a retroactive order is a first-class case and not a workaround.
- **Built:** P-01 read-only until released · three priorities with previews · parts × shops schedule paged three at a time · `procurement` package search with stated invariants (no negative quantities, deterministic ties, uncovered parts named) · revalidate-before-buy on scripted drift · **manual / retroactive order capture** with `entered_by / entered_at / evidence_ref` · MARK ORDERED → ordered, never owned.
- **Proves it:** on the fixtures, the three priorities produce three *different* orders (the six-shop seed diverges, as WP0 fixed); a retroactive order entered by hand shows ■ ORDERED · BY HAND and counts against the C-01 list.

### Dive 7 — Open water (out of scope here; named so the ladder is complete)
`DataSource = real`, one entity at a time: geometry first (14 Oct), BOM rows from real inventory + PriceObservations (21 Oct), BrickLink store data (Q6). Each behind its own briefing.

---

## 4. Where the app lives and what Frame sees

**Where.** One app, `apps/drafting-table`, running on a Vite dev server on the Mac. Not `apps/planner` and not `apps/family` — that split is K-4 / DEC-019 and stays unadjudicated. One app with sheet-level role filtering deferred is the choice that settles nothing. The name is the operator surface's own name and is neutral to the split.

**Frame, experience plane: absent.** No module federation, no instance federation, no host shell, no shared theme provider. The `seam.md` assumptions stay assumptions. The app has its own tiny router, its own theme toggle (`body.dt-blueprint`), and its own actor stub (`@jfo`, `AI`, initials EH/HH/LH as data only).

**Frame, tooling plane: present from Dive 1.** Proposal, to be corrected by your answer to Question 1:

| Hook | What | When it fires |
|---|---|---|
| Northstar | `.claude/northstar.md` `current` values bumped in each debrief commit (P1 climbs as dives land; P2 climbs with every registered memo) | debrief commit |
| Status feed | `fleet/status.json` at repo root — `{dive, sheet, state: briefing·building·debrief·done, gate: {"2026-10-14": …, "2026-10-21": …}, last_debrief: memo id}` — schema proposed in Dive 1's briefing; **this is the record the morning cockpit reads** | CI on `main` |
| Branch flow | one branch per dive, `dive/<n>-<slug>`; PR description in the memo shape; merge = debrief accepted | per dive |
| Attribution | the session's attribution lines on every commit | every commit |

I do not know what the morning cockpit consumes today — a Northstar read, a status file, a heartbeat, an Obsidian canvas. Question 1 asks. Whatever it is, the hook is a Dive 1 deliverable and the app is invisible to the fleet until it lands.

---

## 5. The calendar, backward from 21 October

Today is Friday 18 September. The gate is Wednesday 21 October — 33 days. The chart draws this; the table is the same thing in words.

| Dive | Window | Ends with |
|---|---|---|
| 0 · Briefing | 18 – 22 Sep | this memo accepted, number confirmed |
| 1 · Foundations | 22 – 26 Sep | fixtures validate · contrast green · questions-before-contracts batch |
| 2 · Components | 26 Sep – 2 Oct | fifteen + two components, a11y baselines |
| 3 · Hub + Right now | 30 Sep – 3 Oct | app running; James opens it daily |
| 4 · A-01 + geometry | 3 – 14 Oct | **14 Oct — six checks in code, Q13 BLOCK reproduced** |
| 5 · M-01 + C-01 | 7 – 17 Oct | BOM rows with honest chips; ReleaseGate record |
| 6 · P-01 | 14 – 20 Oct | three diverging orders; retroactive order path |
| — | **21 Oct** | **ORDER-BY GATE** — release on software artifacts, or order anyway and record it after the fact |

Two honesties about this table:

- **It is tight, and it is one implementer.** Dives 4–6 overlap on purpose: geometry can be written while components are still being polished, and C-01's rows don't wait for the 3D viewer. If it slips, the order of sacrifice is fixed by 019 §5: **P-01 optimisation goes first** (a suboptimal shop set costs dollars), then the 3D viewer's look presets, then the layer rig's accordion. The six fit checks, the M-01 loops and the C-01 rows with chips do not slip — they are what the gate is *for*.
- **The gate holds either way.** If on 21 October the software is not trusted, James orders by hand and Dive 6's retroactive-order path records it with honest provenance. That path is therefore built *before* the optimiser, not after.

Each dive's briefing memo re-cuts its own window; this table is the outline, not the promise.

---

## 6. Amendment to 019 §6 — proposed wording

Strike, under *Not authorised*:

> Any workflow UI before the schema gate.

Replace with:

> Any workflow UI that reads anything other than `packages/schema` fixtures (HANDOFF-LEGO-PIPE-023 §1, rules F1–F4) before the schema gate. The gate is closed by James signing `packages/schema` together with the per-sheet acceptance criteria; those are produced by Dives 1–3 of 023 and are exercised by the running app before signature. `DataSource = real` for any entity remains unauthorised until that entity's open-water briefing is accepted.

Everything else in 019 §6 stands, including: no production package boundaries before S1/S2/S7 report (Stream A — this memo does not touch `brickcore/`, `brick_bench/`, `studio-bridge/`); no Frame topology by scaffolding (§4 above keeps the experience plane empty on purpose); nothing in `standalone/` is edited.

---

## 7. Questions for James

Nothing below may be answered by building. Numbered plainly; not findings.

1. **The morning cockpit.** What does it read today — Northstar `current` values, a status file, a heartbeat endpoint, an Obsidian canvas, something in Leo? Name the contract and I will make `fleet/status.json` (or whatever it is) the Dive 1 deliverable in that shape.
2. **Thread name.** This memo opens `app-stack` as a fourth thread beside design, build-harness, cluster and correspondence-governance. Confirm the name, or give it yours.
3. **Number.** 023 is next free at register `.14` (022 went to ChatGPT's reconciliation record this afternoon). Confirm.
4. **Component workbench.** Storybook is the known thing; Ladle is smaller and faster and does the same job for us. I lean Ladle. Rule, or leave it to Dive 1's briefing.
5. **The briefing's "check yourself."** Five questions at the end of every briefing memo, answered in your reply, PADI-style. Do you want that, or does it cross from teaching into homework?
6. **Vocabulary in fixtures.** RESEARCH-01 has not landed. Fixtures will say `Item`, `Unit`, `Section` with `TODO(RESEARCH-01)`. If the research lands mid-track, do we rename fixtures in place (cheap now) or at open water (safer)? My lean: in place, the moment it lands.

---

## 8. What happens on acceptance

1. James confirms 023 and answers §7 in a reply memo (or in chat, relayed — but the answers get a memo, because a fixture rule and a fleet contract are decisions, and decisions live in the register).
2. Claude (Cowork) issues **Dive 1's briefing** as a `CORR-` memo with its own chart: the workspace diagram, the schema entity map drawn from `schema-requests.md`, the fixture scenario, and the acceptance criteria for Dive 1.
3. Claude Code starts Dive 1 only from that briefing, on `dive/1-foundations`, and reports by debrief memo.
4. This memo's register row moves from *for review* to *accepted* when James says so; 019 §6 is amended by a dated entry appended to the decision ledger (`docs/design/H-01-R1/decisions.md`, append-only — the one file in the package that is meant to grow) pointing here.

— Claude (Cowork), coordinating reviewer and handoff author
Under James (`@ojfbot`), who confirms register number 023 and dispatches.
