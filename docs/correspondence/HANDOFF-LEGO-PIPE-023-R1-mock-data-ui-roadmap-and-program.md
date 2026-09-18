---
correspondence_schema: lego-pipe-memo/v1
memo: HANDOFF-LEGO-PIPE-023
revision: R1
status: for_review
memo_type: handoff
title: "The drafting table on fixtures, and the program around it — how five agents and one operator build in parallel"
subtitle: "R0's mock-data roadmap, unchanged in substance, plus the layer it lacked: actors and lanes, design iterating in Claude Design while Claude Code builds, the pin / cut / drift / change-request loop, the weekly rhythm, WIP limits, and the pre-dive check"
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
  - actor: "Claude Design"
    role: designer
    provider: Anthropic
  - actor: ChatGPT
    role: independent_reviewer
    provider: OpenAI
in_reply_to:
  memo: HANDOFF-LEGO-PIPE-019
  revision: R0
supersedes: HANDOFF-LEGO-PIPE-023-R0
authority:
  decision_owner: James
  dispatch_authority: James
  implementation_authorized: "none until James accepts this memo; then Dives 1–3 — Dives 4–6 each wait on the debrief of the dive before"
  production_code_authorized: false
register:
  number: 023
  allocated_by: "proposed — James confirms before dispatch (rule: numbers are allocated by the operator)"
  allocated_on: 2026-09-18
  note: "authored as v1 under the .13 dual-schema migration so the committed validator can pass it; re-issue as v2 at R2"
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
  - program
  - multi-agent
  - design-build-parallel
  - sdlc
attachments:
  - {name: "attachments/HANDOFF-LEGO-PIPE-023-R1-roadmap.html", role: "the chart — ladder, lanes over the calendar, the design↔build loop, package map, dives, sheet ownership; open in any browser, no server"}
argument: >-
  In which R0's roadmap is kept whole and given the layer the operator found
  missing: the five agents and one human are named with their lanes and what each
  may touch; design is allowed to keep moving in Claude Design while a dive builds,
  by pinning a package revision per dive and routing every change through the ledger
  as a cut, a drift report, or a change request; a sheet has one owner at a time;
  the week gets a rhythm and three WIP limits so the operator's Mac — the only place
  a merge or a Studio file happens — is never the bottleneck by accident; a pre-dive
  check is written down PADI-style so no dive starts on a stale package, an invalid
  fixture, or an unreconciled register; the calendar gains a design lane with two
  cuts; and the questions to the operator grow from six to nine.
parts:
  "0": "Orientation — what R1 adds, what it leaves alone"
  "0a": "Change log R0 → R1"
  "1": "The one idea — fixtures are the schema, so the mock UI is the gate package"
  "2": "The ladder — PADI pedagogy as the cadence of every dive"
  "3": "The six dives"
  "4": "The program — actors, lanes, and what each may touch"
  "5": "Design and build in parallel — pin, cut, drift, change request"
  "6": "The rhythm — the week, WIP limits, the pre-dive check, the board"
  "7": "Where the app lives and what the fleet sees"
  "8": "The calendar, with lanes"
  "9": "Amendment to 019 §6 — proposed wording"
  "10": "Questions for James"
  "11": "What happens on acceptance"
provenance:
  source_artifacts:
    - {name: "correspondence/HANDOFF-LEGO-PIPE-023-R0-mock-data-ui-roadmap.md", role: "R0, superseded by this revision; §1–3 carried verbatim in substance"}
    - {name: "correspondence/HANDOFF-LEGO-PIPE-019-R0-initial-handover-claude-code.md", role: "founding handover; §6 amended here; §1.4 is the design-package import precedent"}
    - {name: "correspondence/CORR-LEGO-PIPE-022-R0-chatgpt-reconciliation.md", role: "PR-only contributions and repository-native transfer, relied on in §4"}
    - {name: "docs/design/H-01-R1/", role: "the pinned design package for Dives 1–3; decisions.md, schema-requests.md, open-questions.md, check-manifest.mjs"}
    - {name: "docs/correspondence/REGISTER.md", role: "register read at 2026-09-18.15"}
    - {name: "operator review of R0, Cowork session 2026-09-18", role: "the criticism this revision answers: no account of multi-agent coordination or of design iterating in parallel with build"}
  method: "R0 extended; program layer derived from the register's rules, 019's founding acts, 022's contribution path, and the design package's own ledgers; no code; no prototype QA"
---

# HANDOFF-LEGO-PIPE-023 R1 — The drafting table on fixtures, and the program around it

James, Claude Code, Claude Design, ChatGPT —

R0 planned one lane: build. You pointed out that four other lanes exist and R0 said nothing about how they run beside it — least of all how *you* keep refining prototypes, journeys and fidelity in Claude Design while Claude Code is building against a package that is supposed to hold still. This revision adds that layer (§4–6) and touches nothing in the idea, the ladder or the dives except where the new layer reaches into them. The chart is revised to match; read it first.

---

## 0. Orientation

**What exists.** Two repos, founded (020). `lego-pipe-memo/v2` ratified (022, `.13`); PR-flow in force for every contributor (`.14`); this memo's R0 landed on a branch at `.15`. The design package H-01 R1 is committed verbatim with ten sheets, per-sheet specs, `schema-requests.md`, `open-questions.md` and a decision ledger to DEC-035. Stream A (build harness) is in flight under 011-R2 and is not touched here. No app code exists.

**Who is in the water.** Six parties, one of them human. R0 addressed two. R1 addresses all six (§4).

**What this memo is not.** It is not a new governance memo — the register, PR-flow and the protocol memo (021, as amended by 022) already govern *how correspondence moves*. §4–6 sit on top of those: they govern *how work is scheduled and kept from colliding*. Where this memo and 021/022 seem to disagree, 021/022 win and I have made a mistake; say so.

**How to read this.** §1 is still the idea; if you reject it, stop. §4–6 are the new layer and the reason for R1. §10 has nine questions; three are new and two of them gate Dive 1.

## 0a. Change log R0 → R1

| § | Change |
|---|---|
| 0 | Recipients widened to Claude Design and ChatGPT; orientation rewritten |
| 1–3 | Unchanged in substance. Dive 1 gains one deliverable (the drift checker rewrite, D-2) and one artifact (`docs/program/`). Dive 3's debrief becomes the trigger for design cut R2 |
| 4–6 | **New.** Actors and lanes · parallel design/build · rhythm, WIP, pre-dive check, board |
| 7 | Was §4. Fleet hooks now derive from the board (§6.4), not the reverse |
| 8 | Was §5. Calendar gains the design lane with cuts R2 and R3, and the review lane |
| 9 | Was §6. Unchanged |
| 10 | Was §7. Questions 7–9 added |
| 11 | Was §8. Sequence extended to the design and review lanes |

---

## 1. The one idea — fixtures are the schema, so the mock UI is the gate package

019 §6 says: *no workflow UI before James approves the schema.* The spirit is that a screen built on a guessed data shape hardens the guess. The letter would forbid a mock-data UI outright. The way through is to make the sample data *unable* to be a guess:

> **A fixture is a saved instance of a schema type that passes the same validator real data will pass, carries the same evidence axes real data will carry, and is loaded through the same adapter interface real data will be loaded through. The UI cannot tell which one it is looking at.**

| Rule | In code | What it teaches |
|---|---|---|
| **F1 · Typed, validated** | Every fixture file is parsed by `packages/schema`'s runtime validators at load; a failing fixture is a build failure | An unrepresentable case (a retroactive order, a parked claim) shows up as a broken fixture, not a broken screen |
| **F2 · Evidence-carrying** | Every numeric carries `epistemic_state`; fixture math is `computed` with `method: "fixture"`, never `verified` | The chips (◇ ■ ▲ ○) render honestly from the first render, enforced by the type |
| **F3 · One seam** | `DataSource` is an interface with two implementations, `fixtures` and later `real`; sheets import the interface | "Swap mock for real" is one line per entity, in one reviewable place |
| **F4 · Our village, not a sample** | Tree 41843 at 16 × 16 studs, 16 R40 curves at 53400 LDU, Sections of 2 × 2 MILS 32 × 32, railhead unknown, the Q13 overlap present | A-01's checks return the same honest **BLOCK** in code that the prototype returns — what 019 §4.4 asks for on 14 October |

The thing that clears the gate is the same thing that renders the screens: `packages/schema` + fixtures + per-sheet acceptance criteria (019's G-2 debt). You sign that; the UI is already running on it. Not authorised by this: real BrickLink, real Blender/Studio, the Frame host.

---

## 2. The ladder — PADI pedagogy as the cadence of every dive

| PADI | Here | Artifact |
|---|---|---|
| Knowledge development | **Briefing memo** per dive: one diagram, the dive's vocabulary, the three ways it goes wrong, a short *check yourself* | `CORR-` memo + chart, ≤ 900 words |
| Demonstration | **The Claude Design standalone** for that sheet, opened beside its spec. Watched, not copied | `docs/design/H-01-R<n>/standalone/` at the pinned revision (§5.1) |
| Confined water | **Fixtures.** The sheet runs on `DataSource = fixtures`; James operates it; nothing costs money or touches Studio, Blender or the family | the running app |
| Performance requirement | **Per-sheet acceptance criteria**, proposed in the briefing, signed by James before the dive, checked at the end | G-2 discharged one sheet at a time |
| Debrief | **Findings memo** ≤ 600 words, `[unverified]` on anything not observed, register row, and — new in R1 — the *drift and change-request* list (§5.4) | `CORR-` memo |
| Open water | `DataSource = real`, one entity at a time, behind the 14 Oct and 21 Oct gates | Dive 7 |

Two PADI rules are the spine: **mastery, not exposure** (done when James can explain it back and operate it unaided; else the next dive waits), and **never skip the briefing** (this roadmap is the course outline; each dive has its own lesson). R1 adds a third from the same source: **plan the dive, dive the plan** — the pre-dive check (§6.3) is what makes that literal.

---

## 3. The six dives

Each: what James is taught · what Claude Code builds · what proves it. Sheet behaviour is per the pinned design package; nothing here re-designs a sheet.

**Dive 0 — Briefing (this memo).** Taught: §1, §2, §4–6, the chart. Built: nothing. Proves it: your reply.

**Dive 1 — Foundations.** Taught: what a pnpm workspace is *for us*; tokens and why no hex in app code; runtime validators and why fixtures go through them; the contrast contract and why D-1 fails it. Built: workspace · `packages/tokens` (design package `dt/tokens.css` verbatim + TS map, **D-1 fixed**, `check-contrast.mjs` as CI gate) · `packages/schema` (types, validators, state machines, fixtures under F1–F4 for every entity the five sheets need, neutral `Item`/`Unit`/`Section` with `TODO(RESEARCH-01)`) · a11y-tree snapshot harness in CI · **the drift checker rewritten against `docs/design/` as root (D-2) so it can diff package revisions (§5.3)** · `docs/program/` with the board and the pre-dive check (§6) · fleet hook (§7). Proves it: fixtures validate; contrast green; the *questions-before-contracts* batch (019 §7.2) as the debrief.

**Dive 2 — The fifteen components.** Taught: why components before sheets; the chips one by one; what an accessible name is and why an agent needs it. Built: `packages/ui` — the 15 in `index.json` + ReleaseGate + PriorityStrip, in a component workbench, each with an a11y baseline and its `ANNOUNCEMENTS.md` sentences. Proves it: James reads a BasisChip and names its four axes; zero unnamed controls.

**Dive 3 — Hub with "Right now".** Taught: the app shell; a view over records vs a store. Built: `apps/drafting-table` shell, Hub index + decision log from DEC fixtures, PriorityStrip as a derived view, done / not-today with the A1 no-nag contract, local persistence. Proves it: an app James opens every morning; A1's review question answered by use. **Debrief triggers design cut R2 (§5.2).**

**Dive 4 — A-01, geometry in code, the honest BLOCK.** Taught: integer LDU and display units; the six checks, one diagram each; Q13 and why BLOCK is the design working. Built: `packages/geometry` (LDU, R40 at 16 × 53400, envelopes, six deterministic checks with property tests and golden cases), 2D canvas + 3D viewer reading one representation with Three.js pinned (D-3, Q12), exact transform, rig, NE anchor, plantings with restate-before-save on a mocked AI client. Proves it: BLOCK on the 8 × 8 inner-corner overlap from the F4 inputs — the 14 Oct milestone; independent math audit opened as an issue.

**Dive 5 — M-01 and C-01.** Taught: the two loops and return-to-caller; four stored + two derived axes and why basis was split; GateRecord — quiet stamp, loud record. Built: M-01 facts and claims with pending restatement, earlier-values-kept, blast radius, `?from=`; C-01 schematic, sources by basis, options with stances, requests never deleted, parts list by the four axes with price ranges from `PriceObservation` fixtures, approval trail, ReleaseGate emitting `?released=`. Proves it: James records a real tree-base measurement and watches C-01 rows go ▲ STALE. BOM rows with honest chips exist before any optimiser.

**Dive 6 — P-01.** Taught: the shop-combination search and deterministic ties; revalidation TTL; why a retroactive order is first-class. Built: read-only until released, three priorities with previews, parts × shops paged three at a time, `procurement` search with stated invariants, revalidate on scripted drift, **manual / retroactive order first**, MARK ORDERED → ordered never owned. Proves it: three priorities give three different orders; a hand-entered order shows ■ ORDERED · BY HAND and counts against the list.

**Dive 7 — Open water** (named so the ladder is complete; not in scope): `DataSource = real`, one entity at a time, each behind its own briefing.

---

## 4. The program — actors, lanes, and what each may touch

Six parties. Each has a **lane** (what it produces), a **venue** (where it works), and a **may-touch** list. Nothing in one lane edits another lane's artifacts directly; it sends a memo, a PR, or a change request. That is the whole coordination model; the rest is scheduling.

| Actor | Lane | Venue | Produces | May touch | May not touch |
|---|---|---|---|---|---|
| **James** | Operator | Mac terminal, Claude Design, every chat | Decisions (DEC-*, register rulings), merges, number allocations, acceptance signatures, measurements, real orders | Everything, by ruling | — |
| **Claude Design** | Design | Claude Design session, the H-01 project | Design package cuts `H-01 R<n>` (sheets, specs, `decisions.md`, `schema-requests.md`, `open-questions.md`, `STATES.md`, a11y trees, D-01), journey hierarchy (G-1), change-request responses | Its own package; `decisions.md` (append) | Repo code, fixtures, the register directly (its cuts are imported by Claude Code, §5.2) |
| **Claude Code** | Build | The repo, CI, `dive/<n>` branches, Claude Code sessions | Code, fixtures, schema, acceptance-criteria proposals, debrief memos, drift reports, issues, PRs | Everything under the repo except the two verbatim trees | `docs/design/H-01-R<n>/` (verbatim, never edited), correspondence authored by others |
| **Claude (Cowork)** | Program | Cowork sessions on the LEGO Village project, `correspondence/` branches | Briefings, roadmaps, reconciliations, register bumps for its own memos, the program board's narrative | `docs/correspondence/`, `docs/program/` | Code, design package, other authors' memos |
| **ChatGPT** | Review | Its own project; contributes by PR only (022) | `REVIEW-` memos, reconciliation `CORR-` memos, schema review (Q11), P0/P1/P2 findings | Its own memos via PR | Anything else; no direct commits |
| **GitHub** | Record | `ojfbot/lego-village-pipeline`, `play-well-library` | `main` (canonical), PR-flow, CI gates (preflight · contrast · a11y snapshot · main-guard · drift), issues, milestones, the project board | — | — |
| **Local (Mac)** | Physical | James's machine | Pushes and merges (the only credentialed place), the running app, Studio, Blender, dev storage, real measurements | — | — |

Three things fall out of the table:

- **Transfer is by file, and repository-native where the recipient has repo access** (rule 1 as amended by 022). Cowork and Claude Code read each other in the repo. Claude Design and ChatGPT do not: their input arrives as an attached package or a PR; their reading is a mirror.
- **Every lane ends in James.** Merges, numbers, acceptance, DEC entries. This is correct and it is also the bottleneck; §6.2 limits WIP so the queue at his desk stays short.
- **Sessions are disposable; the record is not.** No lane depends on chat memory. A new Cowork session, a new Claude Code session, a new Claude Design session must be able to resume from the register + the board + the pinned package. That is why §6.4 exists.

---

## 5. Design and build in parallel — pin, cut, drift, change request

The problem stated plainly: Claude Code builds A-01 from spec R1 over eleven days; meanwhile you and Claude Design improve A-01. Either the build ships something already superseded, or design is frozen for a month, or the two silently diverge. The mechanism below refuses all three.

### 5.1 Pin — a dive builds against one package revision, named in the briefing

Each briefing states `design_pin: H-01 R<n>` and the sheets it covers. Claude Code reads only that revision for those sheets, from `docs/design/H-01-R<n>/`, committed verbatim. The pin moves only at a dive boundary, in the next briefing. Dives 1–3 pin **R1**. Dive 4 pins whatever cut exists on 3 October — **R2** if it has landed (§5.2), else R1.

### 5.2 Cut — Claude Design keeps working; its work reaches the repo as a versioned package

Claude Design is not frozen. It works two queues:

- **Design-ahead** (default, unconstrained): anything not on the current dive's pinned sheets — Tier 2 receiving sheets, F-01, D-01 lift (OW-01), the journey hierarchy (G-1), responsive (Q7), B-01, the ledger.
- **Design-behind** (constrained, §5.4): changes to a sheet currently in build. Allowed, but they land as a *change request* against the dive, not as a silent edit to the spec the builder is reading.

A **cut** is a zip of the whole package with a sha256, imported exactly as 019 §1.4 did R1: committed verbatim to `docs/design/H-01-R<n>/`, register row with hash, `decisions.md` diffed to confirm it is append-only. **Two cuts are scheduled** (§8): **R2 on 3 Oct** (absorbs Dive 1's schema answers, the Q-item rulings, and Dive 2/3 debrief findings) and **R3 on 17 Oct** (Tier 2 receive → inspect → discrepancy → allocate, which must exist by 25 Nov). A cut can also be called ad hoc by James.

What flows *back* to Claude Design with each briefing, so the next cut is grounded: the schema package's answers to `schema-requests.md` (what was accepted, renamed, split, refused), the fixture scenario (F4) so the prototypes can be re-seeded with the same village — optionally consuming the fixture JSON directly (Question 8) — and the debrief's findings against the pinned sheets.

### 5.3 Drift — every cut is diffed, and the diff is a work item

On import, the rewritten drift checker (Dive 1, D-2) diffs `R<n>` against `R<n-1>` and emits a **drift report**: per sheet, *spec changed · states changed · a11y tree changed · schema request added/withdrawn · DEC entries added*. For each sheet that is **in build or already built**, Claude Code opens one issue labelled `design-drift · sheet:X · dive:N` and triages it in the next debrief: **absorb** (in scope of the current dive), **defer** (to a named later dive), or **contest** (send back as a change request with the reason). Nothing about a cut is merged into code without passing through this triage. Sheets not yet in build take the new revision silently — that is the design-ahead queue doing its job.

### 5.4 Change request — the constrained path, in both directions

Two shapes, same rule: **a sheet has one owner at a time**, shown on the board (§6.4).

- **Design → build**, during a dive, for a pinned sheet: Claude Design records the change as a DEC entry with `blast_radius: sheet` and it is carried into the next cut; if it cannot wait, James rules and Claude Code absorbs it as a scoped change with the acceptance criteria amended in the same PR. No spec file under a pinned revision is ever edited in place — that is what the verbatim rule protects.
- **Build → design**, from a debrief: findings that mean *the design is wrong or under-specified* (a state the spec forgot, an announcement that cannot be true, a schema request the data cannot satisfy) go to Claude Design as a `HANDOFF-` change request in the 014 shape, graded P0/P1/P2, answered in the next cut. Findings that mean *the build is wrong* stay in the build lane as issues.

Ownership flips only at a cut (design → build for newly pinned sheets) or at a change request James dispatches (build → design for a sheet returned for work). The board shows the current holder of each of the ten sheets.

---

## 6. The rhythm — the week, WIP limits, the pre-dive check, the board

### 6.1 The week

Dives are not weeks — Dive 4 is eleven days, Dive 3 is four — but the *program* keeps a weekly beat so the lanes synchronise even when the dive does not end. Times are yours to move; the order matters.

| Day | Program (Cowork) | Build (Claude Code) | Design (Claude Design) | Review (ChatGPT) | Operator (James) |
|---|---|---|---|---|---|
| **Mon** | Issue the briefing for any dive starting this week; reconcile last Friday's register | Read the briefing; run the pre-dive check; open `dive/<n>` | Read the schema answers and drift triage from Friday | — | Refine the briefing the same day; sign acceptance criteria |
| **Tue–Thu** | Answer questions; draft the next briefing | Build; open issues; keep the board current | Design-ahead queue; DEC entries for design-behind | Review the briefing or the previous debrief; findings by PR | Operate the sheet as it lands; measure; rule on Q-items |
| **Fri** | Register reconciled; board narrative updated; fleet status pushed | Debrief memo (if a dive ends) + drift triage + PRs ready for merge | Cut, if one is scheduled or called | Reconciliation memo if findings were contested | **Merge day.** Merge PRs; allocate numbers; call or decline a cut |

If a dive ends mid-week, its debrief is issued that day and Friday still happens. If nothing ends, Friday is reconciliation only and is short.

### 6.2 WIP limits — three, and they protect the operator

1. **One dive in build.** Dives 4–6 overlap in *elapsed time* (§8) only because their early work is package-level; the sheet work is serial. The board shows one dive as *building* at a time.
2. **One cut in flight.** A cut is called, imported and triaged before the next is called.
3. **One PR per lane waiting on James.** Build, program and review each get one open PR at a time awaiting merge. A second waits on its branch. This is what keeps merge day to minutes.

### 6.3 The pre-dive check — buddy check, written down

No dive starts until Claude Code has ticked every line in the briefing's PR description and James has seen it. Same idea as a buddy check: it takes a minute, and it is the minute in which stale packages and unsigned criteria get caught.

- [ ] Briefing accepted by James; register row moved to *accepted*
- [ ] `design_pin` named; the pinned revision is on `main`, verbatim, hash recorded
- [ ] Drift report for the pinned revision triaged (no untriaged `design-drift` issues on the dive's sheets)
- [ ] Acceptance criteria for each sheet signed by initials in the briefing
- [ ] `pnpm validate:fixtures` green on `main`; contrast check green; a11y baselines present for every component the dive uses
- [ ] Register reconciled — no *received, not issued* memo the dive depends on
- [ ] Open questions the dive depends on are answered or explicitly parked with an owner
- [ ] Previous dive's debrief issued and its teach-back recorded

### 6.4 The board — one place that says where everything is

`docs/program/` holds three files, all authored in-repo:

- **`PROGRAM.md`** — §4–6 of this memo, maintained as the living version once this memo is accepted (the memo stays the record of the decision; the file is the current state).
- **`board.json`** — machine-readable: `{dives: [{n, sheet(s), state: planned·briefing·building·debrief·done, pin, pr}], sheets: [{id, owner: design·build, pin, drift_open}], cuts: [{rev, scheduled, landed, sha256}], gates: {"2026-10-14": …, "2026-10-21": …, "2026-11-25": …}, wip: {...}, last_debrief, last_cut}`. Updated by Claude Code in the same PR as the change it describes.
- **`pre-dive-check.md`** — §6.3, the template the briefing PR copies.

GitHub carries the same state where it is native: **issues** with labels `lane:*`, `dive:*`, `sheet:*`, `design-drift`, `change-request`; **milestones** 14 Oct · 21 Oct · 25 Nov · 25 Dec; and, if you want it, a **GitHub Projects board** as the visual board with `board.json` derived from it rather than the reverse (Question 7). The fleet status feed (§7) is a projection of `board.json`, never a second source.

---

## 7. Where the app lives and what the fleet sees

**Where.** One app, `apps/drafting-table`, Vite dev server on the Mac. Not `apps/planner` / `apps/family` — that split is K-4 / DEC-019 and stays unadjudicated; one app with role filtering deferred settles nothing.

**Frame, experience plane: absent.** No federation, no host shell, no shared theme provider. `seam.md` stays assumptions. The app has its own router, theme toggle (`body.dt-blueprint`) and actor stub (`@jfo`, `AI`, EH/HH/LH as data).

**Frame, tooling plane: present from Dive 1**, and now derived from the board:

| Hook | What | When |
|---|---|---|
| Status feed | `fleet/status.json` — a projection of `docs/program/board.json` in whatever shape the morning cockpit reads (Question 1) | CI on `main` |
| Northstar | `.claude/northstar.md` `current` bumped in each debrief commit — P1 with dives, P2 with every registered memo | debrief commit |
| Branch flow | `dive/<n>-<slug>` for build, `correspondence/<nnn>-<slug>` for program, ChatGPT's own for review; PR descriptions in memo shape | per PR |
| Attribution | the session's attribution lines on every commit | every commit |

---

## 8. The calendar, with lanes

Today is Friday 18 September. The gate is Wednesday 21 October — 33 days. The chart draws the lanes; the table is the same in words.

| Window | Build | Design | Review / Program | Ends with |
|---|---|---|---|---|
| 18 – 22 Sep | Dive 0 (this) | Design-ahead: G-1 journey hierarchy, D-01 lift | ChatGPT reviews 023; Cowork drafts Dive 1 briefing | 023 accepted; number confirmed |
| 22 – 26 Sep | Dive 1 · foundations, pin R1 | Design-ahead; receives Dive 1 schema answers Fri | Cowork: Dive 2 briefing | Fixtures validate; contrast green; questions-before-contracts |
| 26 Sep – 2 Oct | Dive 2 · components, pin R1 | Prepares **cut R2** from schema answers + Q rulings | ChatGPT reviews schema (Q11) | 17 components with a11y baselines |
| 30 Sep – 3 Oct | Dive 3 · Hub, pin R1 | **Cut R2 lands 3 Oct**; drift report; ownership of A-01/M-01/C-01/P-01 → build | Cowork: Dive 4 briefing pins R2 | App running; Dive 3 debrief |
| 3 – 14 Oct | Dive 4 · A-01 + geometry, pin R2 | Design-ahead: Tier 2 receiving sheets; design-behind by DEC only | ChatGPT reviews geometry invariants | **14 Oct — six checks in code, Q13 BLOCK reproduced** |
| 7 – 17 Oct | Dive 5 · M-01 + C-01, pin R2 | **Cut R3 lands 17 Oct** (Tier 2) | Cowork: Dive 6 briefing | BOM rows with chips; ReleaseGate record |
| 14 – 20 Oct | Dive 6 · P-01, pin R2 | Design-ahead on R3 drift | Cowork: open-water briefing for geometry | Three diverging orders; retroactive path |
| **21 Oct** | | | | **ORDER-BY GATE** — release on software artifacts, or order by hand and record after the fact |
| 21 Oct – 25 Nov | Dive 7 · open water, then Tier 2 sheets from R3 | Design-ahead: Tier 3, F-01 responsive | | Parts received and inspected in the system |

Two honesties: it is tight and it is one implementer; if it slips, P-01 optimisation goes first, then 3D look presets, then the rig accordion — the six checks, the M-01 loops and the C-01 rows with chips do not slip. And the gate holds either way: the retroactive-order path is built before the optimiser.

---

## 9. Amendment to 019 §6 — proposed wording

Strike, under *Not authorised*: "Any workflow UI before the schema gate."

Replace with: "Any workflow UI that reads anything other than `packages/schema` fixtures (HANDOFF-LEGO-PIPE-023 §1, rules F1–F4) before the schema gate. The gate is closed by James signing `packages/schema` together with the per-sheet acceptance criteria; those are produced by Dives 1–3 of 023 and are exercised by the running app before signature. `DataSource = real` for any entity remains unauthorised until that entity's open-water briefing is accepted. Design package revisions are imported verbatim per 019 §1.4 and consumed by build only through a named `design_pin` (023 §5)."

Everything else in 019 §6 stands.

---

## 10. Questions for James

Nothing below may be answered by building.

1. **The morning cockpit.** What does it read today — Northstar currents, a status file, a heartbeat, an Obsidian canvas, Leo? `fleet/status.json` will be a projection of `board.json` in that shape.
2. **Thread name** `app-stack` — confirm or rename.
3. **Number 023** — confirm (next free was 023 at `.14`; R0 is on the branch at `.15`).
4. **Component workbench** — Storybook or Ladle? Lean Ladle.
5. **"Check yourself"** at the end of each briefing — teaching or homework?
6. **RESEARCH-01 mid-track** — rename fixtures in place or at open water? Lean in place.
7. **The board of record.** GitHub Projects (visual, API-readable by the cockpit, `board.json` derived from it) or `board.json` alone (repo-native, no second tool)? Lean Projects if you already look at GitHub daily; `board.json` alone if you don't.
8. **Design on fixtures.** Should Claude Design's prototypes be re-seeded from the F4 fixture JSON at cut R2, so design and build share one village? It costs Claude Design a data-loading step; it buys drift reports that compare like with like. Lean yes.
9. **Cut cadence.** Two scheduled cuts (R2 3 Oct, R3 17 Oct) plus ad hoc by your call — or a fixed Friday cut every week? Lean scheduled: weekly cuts would put a drift triage in every debrief.

---

## 11. What happens on acceptance

1. James confirms 023 and answers §10 in a reply memo (or in chat, relayed into a memo — the fixture rule, the pin rule and the fleet contract are decisions and live in the register).
2. Claude (Cowork) issues **Dive 1's briefing** as a `CORR-` memo with its chart: workspace diagram, schema entity map from `schema-requests.md`, the F4 scenario, `design_pin: H-01 R1`, and Dive 1's acceptance criteria.
3. Claude Code runs the pre-dive check, starts Dive 1 on `dive/1-foundations`, creates `docs/program/`, and reports by debrief.
4. Claude Design receives, with the briefing, the design-ahead queue for 22 Sep – 3 Oct and the cut R2 target; ChatGPT receives 023 for review by PR.
5. This memo's row moves to *accepted* when James says so; 019 §6 is amended by a dated entry appended to `docs/design/H-01-R1/decisions.md` pointing here; `docs/program/PROGRAM.md` is seeded from §4–6.

— Claude (Cowork), coordinating reviewer and handoff author
Under James (`@ojfbot`), who confirms register number 023 and dispatches.
