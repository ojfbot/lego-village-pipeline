---
correspondence_schema: lego-pipe-memo/v1
memo: HANDOFF-LEGO-PIPE-023
revision: R2
status: for_review
memo_type: handoff
title: "The drafting table on fixtures, and the program around it — built bag by bag, the way a LEGO set is"
subtitle: "R1 with the operator's ten rulings folded in: the thread is named for the whole drafting table, adapters to schema to UI; the dive vocabulary is replaced with LEGO learning-through-play and set-building language; fixtures start from the real village and progress in ambiguity, fidelity and autonomy; cuts are weekly; ChatGPT starts at L1; the board is a file, not a product"
date: 2026-09-18
thread: drafting-table
cluster: play-well
project: LEGO Village Pipeline
register_version_read: "2026-09-18.21"
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
    role: independent_reviewer_and_design_architecture_contributor
    provider: OpenAI
in_reply_to:
  memo: HANDOFF-LEGO-PIPE-019
  revision: R0
supersedes: HANDOFF-LEGO-PIPE-023-R1
authority:
  decision_owner: James
  dispatch_authority: James
  implementation_authorized: "none until James accepts this memo; then Bags 1–3 — Bags 4–6 each wait on the step-back of the bag before"
  production_code_authorized: false
register:
  number: 023
  allocated_by: James
  allocated_on: 2026-09-18
  note: "authored as v1 under the .13 dual-schema migration so the committed validator can pass it; converts to v2 when the v2-aware validator lands, before it acts as a work order"
repos:
  - ojfbot/lego-village-pipeline
  - ojfbot/play-well-library
tags:
  - drafting-table
  - mock-data
  - fixtures
  - schema-gate
  - roadmap
  - learning-through-play
  - program
  - multi-agent
  - design-build-parallel
  - confidence-ladder
attachments:
  - {name: "attachments/HANDOFF-LEGO-PIPE-023-R2-roadmap.html", role: "the chart — the bag sequence, lanes over the calendar with weekly cuts, the design↔build loop, package map, one card per bag; open in any browser, no server"}
argument: >-
  In which the operator's ten rulings on R1 are folded in and nothing else is
  changed: the thread is named `drafting-table` because that is what is being built,
  adapters to schema to UI; the borrowed diving vocabulary is put down and the work
  is described the way a LEGO set is built — numbered bags, an instruction booklet
  per bag, the picture on the box as the test of done, step back and look at the
  end — with the LEGO Foundation's five characteristics of learning through play as
  the reason the cadence looks the way it does; the fixtures are declared to start
  from the real village and to progress along three axes, ambiguity, fidelity and
  autonomy, which is what dogfooding means here; design cuts become weekly on Fridays;
  the design prototypes and the app are to show the same sample village; ChatGPT
  starts at rung L1; the board is a file the fleet reads, not a product; and the
  morning-cockpit question becomes a research item for Claude Code that also
  captures how a cluster is onboarded, for the next one.
parts:
  "0": "Orientation — what R2 changes, what it leaves alone"
  "0a": "Change log R1 → R2 — the ten rulings"
  "1": "The one idea — fixtures are the schema, so the mock UI is the gate package"
  "2": "How each bag is built — learning through play, and the picture on the box"
  "3": "The six bags"
  "4": "The program — actors, lanes, and what each may touch"
  "5": "Design and build in parallel — pin, cut, drift, change request"
  "6": "The rhythm — the week, WIP limits, the before-you-open-the-bag check, the board file"
  "7": "Where the app lives and what the fleet sees"
  "8": "The calendar, with lanes"
  "9": "Amendment to 019 §6 — proposed wording"
  "10": "Rulings recorded, and what is still open"
  "11": "What happens on acceptance"
provenance:
  source_artifacts:
    - {name: "correspondence/HANDOFF-LEGO-PIPE-023-R1-mock-data-ui-roadmap-and-program.md", role: "R1, superseded by this revision; structure and substance carried, vocabulary and rulings changed"}
    - {name: "correspondence/HANDOFF-LEGO-PIPE-019-R0-initial-handover-claude-code.md", role: "founding handover; §6 amended here"}
    - {name: "correspondence/ARCHITECTURE-correspondence-and-research.md", role: "§1a — the design package's borrowed identity, relied on in §5"}
    - {name: "docs/design/H-01-R1/", role: "the pinned design package for Bags 1–3"}
    - {name: "docs/correspondence/REGISTER.md", role: "register read at 2026-09-18.21 on origin/main; 024 next free; the version-dispatching validator (.20) and the Codex lane (.21) landed while R2 was in flight"}
    - {name: "operator rulings on R1 §10, Cowork session 2026-09-18", role: "the ten answers this revision records"}
    - {name: "LEGO Foundation — Five ways to spot playful learning (learningthroughplay.com)", role: "the five characteristics cited in §2 [verified 2026-09-18]"}
    - {name: "LEGO Fair Play policy (lego.com/legal/notices-and-policies/fair-play)", role: "trademark usage applied to all copy here and in the app [verified 2026-09-18]"}
  method: "R1 revised against the operator's rulings; no code; no prototype QA; two web sources read directly"
---

# HANDOFF-LEGO-PIPE-023 R2 — The drafting table on fixtures, and the program around it

James, Claude Code, Claude Design, ChatGPT —

R1 asked ten questions. James answered all ten. This revision records the answers where they bite and changes nothing else. The largest change is language, and it is not cosmetic: the diving metaphor was borrowed; the set-building one is native to the thing we are making and to the people who will use it.

**A word on the word.** LEGO is an adjective, never a noun, and never plural: *LEGO bricks*, *a LEGO set*, never "LEGOs" ([LEGO Fair Play](https://www.lego.com/en-us/legal/notices-and-policies/fair-play), read 2026-09-18). This applies to every sheet, every memo, and every fixture string from here on; it goes into `packages/ui`'s copy lint when that exists.

---

## 0. Orientation

**What exists.** Two repos, founded (020). `lego-pipe-memo/v2` ratified (022, `.13`); PR-flow for every contributor (`.14`); R0 and R1 of this memo on `main` at `.15`–`.19`, with the ARCHITECTURE reference beside them; the version-dispatching validator landed at `.20` and Codex (the ChatGPT desktop agent) gained the relayed-landings self-merge lane at `.21` while this revision was in flight — §4's ChatGPT row should be read with that lane in mind. The design package H-01 R1 is committed verbatim; its identity is borrowed and its manifest is free text (ARCHITECTURE §1a) — that matters for §5. Stream A is in flight under 011-R2 and is not touched. No app code exists.

**What R2 is.** R1 plus rulings. §0a lists them; §1–3 carry the idea and the plan in the new words; §4–6 the program; §10 replaces "questions" with "rulings recorded" and the two items still open.

**What this memo is not.** Not a governance memo — the register, PR-flow and 021/022 govern how correspondence moves; §4–6 govern how work is scheduled and kept from colliding. Where they seem to disagree, they win.

## 0a. Change log R1 → R2 — the ten rulings

| R1 § | Ruling (James, 2026-09-18) | Where it lands |
|---|---|---|
| Q1 morning cockpit | Not a question for James: a **research item for Claude Code** — integrate the play-well cluster with the ojfbot fleet (cockpit included) and capture the cluster onboarding/launch pipeline so the next cluster reuses it | §3 Bag 1 (research, not build) · §7 |
| Q2 thread name | `app-stack` rejected as generic jargon. Thread is **`drafting-table`** — the umbrella for the whole thing, adapters to schema to UI | frontmatter · register rule 16 list · §0 |
| Q3 number | 023 confirmed; 024 next free (read at `.21`) | frontmatter `allocated_by: James` |
| Q4 workbench | **Ladle.** Storybook's overhead rejected | §3 Bag 2 |
| Q5 "check yourself" | Replaced: each booklet **names the slice of work it delivers**; the step-back says whether that slice was delivered and can be described | §2 · §6.3 |
| Q6 vocabulary | **Walk back the diving language.** Lean on LEGO learning through play | §2 rewritten; every "dive/briefing/debrief/open water" replaced throughout |
| Q7 board of record | Rejected — no GitHub Projects, nothing novel in the fleet. **`board.json` only**, feeding the morning cockpit and fleet tracking | §6.4 · §7 |
| Q8 shared sample village | **Yes.** Prototypes and app show the same village. And the stated principle behind it: dogfooding by building from **real-world state with progressive ambiguity, fidelity and autonomy** | §1 rule F5 · §5.2 |
| Q9 cut cadence | **Fixed weekly**, Friday | §5.2 · §6.1 · §8 |
| Q10 ChatGPT rung | **L1 is where we are now** | §4.1 |

Everything in R1 not named above is unchanged in substance.

---

## 1. The one idea — fixtures are the schema, so the mock UI is the gate package

019 §6 says: *no workflow UI before James approves the schema.* The spirit is that a screen built on a guessed data shape hardens the guess. The way through is to make the sample data unable to be a guess:

> **A fixture is a saved instance of a schema type that passes the same validator real data will pass, carries the same evidence axes real data will carry, and is loaded through the same adapter interface real data will be loaded through. The UI cannot tell which one it is looking at.**

| Rule | In code | What it teaches |
|---|---|---|
| **F1 · Typed, validated** | Every fixture file is parsed by `packages/schema`'s runtime validators at load; a failing fixture is a build failure | An unrepresentable case shows up as a broken fixture, not a broken screen |
| **F2 · Evidence-carrying** | Every numeric carries `epistemic_state`; fixture math is `computed` with `method: "fixture"`, never `verified` | The chips (◇ ■ ▲ ○) render honestly from the first render |
| **F3 · One seam** | `DataSource` is an interface with two implementations, `fixtures` and later `real`; sheets import the interface | "Swap mock for real" is one line per entity, in one reviewable place |
| **F4 · Our village, not a sample** | Tree 41843 at 16 × 16 studs, 16 R40 curves at 53400 LDU, Sections of 2 × 2 MILS 32 × 32, railhead unknown, the Q13 overlap present | A-01's checks return the same honest **BLOCK** in code that the prototype returns |
| **F5 · Real-world state, progressing on three axes** *(new — Q8)* | The fixture set is a snapshot of the real village as James knows it today, and every later fixture set moves along one or more of: **ambiguity** (fewer `asserted`, more `measured`/`verified`; fewer parked claims), **fidelity** (closer to real BrickLink lots, real inventory, real geometry), **autonomy** (more changes originated by agents, each restated before save). The **same fixture set seeds the design prototypes**, so prototype and app show one village | Dogfooding is not "use the app"; it is "move the village from guessed to known while the software watches". Each bag's booklet says which axis it advances |

The thing that clears the gate is the same thing that renders the screens: `packages/schema` + fixtures + per-sheet acceptance criteria. You sign that; the UI is already running on it. Not authorised here: real BrickLink, real Blender/Studio, the Frame host.

---

## 2. How each bag is built — learning through play, and the picture on the box

The LEGO Foundation names five characteristics of learning through play: **joyful, meaningful, actively engaged, iterative, socially interactive** ([learningthroughplay.com](https://www.learningthroughplay.com/how-we-play/five-ways-to-spot-playful-learning), read 2026-09-18). The cadence below is built to have all five, and a LEGO set already has the shape:

| In a LEGO set | Here | Artifact | Characteristic it serves |
|---|---|---|---|
| **The numbered bag** — you open one, build it, then the next | A **bag** of work: one bounded slice, built in order | the six bags in §3 | iterative |
| **The instruction booklet** for that bag — pictures, a few words, one step at a time | The **booklet**: a short memo, one diagram, the vocabulary of the bag, the three ways the step goes wrong, and **the slice of work this bag delivers**, stated plainly (Q5) | `CORR-` memo + chart, ≤ 900 words | meaningful |
| **The picture on the box** — what it should look like when it's done | **Acceptance criteria** per sheet, agreed before the bag is opened | the G-2 debt, discharged one sheet at a time | meaningful |
| **The model in the booklet** you look at while you build | **The Claude Design standalone** for that sheet, open beside the spec. Looked at, not copied | `docs/design/H-01-R<n>/standalone/` at the pinned revision | actively engaged |
| **Building it on the table** | The sheet runs on `DataSource = fixtures`; James builds with it; nothing costs money, nothing touches Studio, Blender or the family | the running app | joyful · actively engaged |
| **Step back and look** — does it match the box? what's loose? | The **step-back memo** ≤ 600 words: was the slice delivered, can James describe it, what drifted, what goes back to design | `CORR-` memo | iterative · socially interactive |
| **Real bricks, no glue** | `DataSource = real`, one entity at a time, behind the 14 Oct and 21 Oct gates | Bag 7 | — |

Two rules carry the weight:

- **You can build it again without the booklet.** A bag is done when James can describe the slice and operate the sheet unaided — not when the code merged. If that isn't true, the step-back says so and the next bag stays sealed.
- **Open the bags in order.** No bag starts on the strength of this roadmap. Each has its own booklet, refined by James, naming its slice and its acceptance criteria. This memo is the box; it is not the booklet.

---

## 3. The six bags

Each: what James is shown · what Claude Code builds · what proves it. Sheet behaviour is per the pinned design package; nothing here re-designs a sheet.

**Bag 0 — the box (this memo).** Shown: §1, §2, §4–6, the chart. Built: nothing. Proves it: James's acceptance.

**Bag 1 — Foundations.** Shown: what a pnpm workspace is *for us*; tokens and why no hex in app code; runtime validators and why fixtures go through them; the contrast contract and why D-1 fails it. Built: workspace · `packages/tokens` (design package `dt/tokens.css` verbatim + TS map, **D-1 fixed**, `check-contrast.mjs` as CI gate) · `packages/schema` (types, validators, state machines, fixtures under F1–F5 for every entity the five sheets need; neutral `Item`/`Unit`/`Section` with `TODO(RESEARCH-01)`) · a11y-tree snapshot harness in CI · drift checker rewritten against `docs/design/` (D-2) · `docs/program/` with `board.json` and the before-you-open check (§6) · fleet hook (§7). **Research (Q1):** how the play-well cluster integrates with the ojfbot fleet and the morning cockpit, and a written cluster onboarding/launch pipeline the next cluster can follow — a research document under `docs/research/cluster/`, `[verified]`/`[unverified]` per claim, no code. Slice delivered: *fixtures validate, contrast green, the fleet can see us, and we know how a cluster is born.* Step-back doubles as the questions-before-contracts batch (019 §7.2).

**Bag 2 — The fifteen components.** Shown: why components before sheets; the chips one by one; what an accessible name is and why an agent needs it. Built: `packages/ui` — the 15 in `index.json` + ReleaseGate + PriorityStrip, in **Ladle** (Q4), each with an a11y baseline and its `ANNOUNCEMENTS.md` sentences. Slice delivered: *every component on the table, named, chipped.* Proves it: James reads a BasisChip and names its four axes; zero unnamed controls.

**Bag 3 — Hub with "Right now".** Shown: the app shell; a view over records vs a store. Built: `apps/drafting-table` shell, Hub index + decision log from DEC fixtures, PriorityStrip as a derived view, done / not-today with the A1 no-nag contract, local persistence. Slice delivered: *an app James opens every morning.* Its step-back feeds the Friday cut (§5.2).

**Bag 4 — A-01, geometry in code, the honest BLOCK.** Shown: integer LDU and display units; the six checks, one diagram each; Q13 and why BLOCK is the design working. Built: `packages/geometry` (LDU, R40 at 16 × 53400, envelopes, six deterministic checks with property tests and golden cases), 2D canvas + 3D viewer reading one representation with Three.js pinned (D-3, Q12), exact transform, rig, NE anchor, plantings with restate-before-save on a mocked AI client. Slice delivered: *the six checks return BLOCK on the 8 × 8 inner-corner overlap from the F4 inputs* — the 14 Oct milestone; independent math audit opened as an issue. Axis advanced: ambiguity (Q13 from drawn to computed).

**Bag 5 — M-01 and C-01.** Shown: the two loops and return-to-caller; four stored + two derived axes and why basis was split; GateRecord — quiet stamp, loud record. Built: M-01 facts and claims with pending restatement, earlier-values-kept, blast radius, `?from=`; C-01 schematic, sources by basis, options with stances, requests never deleted, parts list by the four axes with price ranges from `PriceObservation` fixtures, approval trail, ReleaseGate emitting `?released=`. Slice delivered: *BOM rows with honest chips exist before any optimiser.* Proves it: James records a real tree-base measurement and watches C-01 rows go ▲ STALE. Axis advanced: fidelity (measured facts replace asserted ones).

**Bag 6 — P-01.** Shown: the shop-combination search and deterministic ties; revalidation TTL; why a retroactive order is first-class. Built: read-only until released, three priorities with previews, parts × shops paged three at a time, `procurement` search with stated invariants, revalidate on scripted drift, **manual / retroactive order first**, MARK ORDERED → ordered never owned. Slice delivered: *three priorities give three different orders; a hand-entered order counts against the list.* Axis advanced: autonomy (the agent proposes a plan; James restates and accepts).

**Bag 7 — Real bricks** (named so the box is complete; not in scope): `DataSource = real`, one entity at a time, each behind its own booklet.

---

## 4. The program — actors, lanes, and what each may touch

Six parties. Each has a **lane**, a **venue**, and a **may-touch** list. Nothing in one lane edits another lane's artifacts directly; it sends a memo, a PR, or a change request.

| Actor | Lane | Venue | Produces | May touch | May not touch |
|---|---|---|---|---|---|
| **James** | Operator | Mac terminal, Claude Design, every chat | Decisions (DEC-*, register rulings), merges, number allocations, acceptance signatures, measurements, real orders | Everything, by ruling | — |
| **Claude Design** | Design | Claude Design session | Package cuts `H-01 R<n>` (weekly, §5.2), journey hierarchy (G-1), change-request responses | Its own package; `decisions.md` (append) | Repo code, fixtures, the register directly |
| **Claude Code** | Build | The repo, CI, `bag/<n>` branches | Code, fixtures, schema, acceptance-criteria proposals, step-back memos, drift reports, `board.json`, issues, PRs; the Q1 research document | Everything under the repo except the verbatim trees | `docs/design/H-01-R<n>/`, correspondence authored by others |
| **Claude (Cowork)** | Program | Cowork sessions, `correspondence/` branches | Booklets, roadmaps, reconciliations, register bumps for its own memos, `PROGRAM.md` | `docs/correspondence/`, `docs/program/` | Code, design package, others' memos |
| **ChatGPT** | Review + design + architecture | Its own project; PR only (022) | `REVIEW-`/`CORR-` memos; design proposals; architecture proposals (ADR-shaped); P0/P1/P2 findings; code PRs **at rung L1 (Q10)** | Its own memos and proposals via PR; `packages/schema/fixtures/`, `*.test.*`, golden cases, property tests, `tools/` | Direct commits; the verbatim package; code above L1 |
| **GitHub** | Record | both repos | `main`, PR-flow, CI gates, issues, milestones | — | — |
| **Local (Mac)** | Physical | James's machine | The only pushes and merges; the running app; Studio, Blender, dev storage, real measurements | — | — |

### 4.1 ChatGPT's authority, and the confidence ladder

**Design and architecture: full authority to propose.** Journeys, sheets, states, copy, schema shape, package boundaries, implementation patterns, ADRs — as memos or PRs to `docs/design/proposals/` and `docs/architecture/proposals/`. One design package and one schema package, so a proposal becomes real only through a cut, the pin, or a ruling. Proposes everything, decides nothing — same as every agent.

**Code: by ladder.** James moves ChatGPT up or down a rung by register ruling, recorded in `PROGRAM.md`; PR-only and the CI gates apply at every rung. **Current rung: L1** (Q10).

| Rung | May open PRs touching | Typical task | Evidence for the next rung |
|---|---|---|---|
| L0 · Memos | `docs/correspondence/`, the two proposals folders | reviews, proposals | — |
| **L1 · Fixtures & tests** *(now)* | `packages/schema/fixtures/`, `*.test.*`, golden cases, property tests, `tools/` | golden cases for the six fit checks; adversarial fixtures for the four-axis PartRow | tests that caught something; fixtures that validate first time |
| L2 · Packages | `packages/*` except `ui` | procurement invariants; a geometry helper | PRs merged with ≤ 1 round; no a11y or contrast regressions |
| L3 · UI and app | `packages/ui`, `apps/drafting-table` | a component against its a11y baseline | same, on the accessibility-tree contract |

Claude Code remains the implementer of record; ChatGPT's code PRs are contributions to a bag, triaged in the step-back like drift.

Three consequences of the table: transfer is by file, repository-native where the recipient has repo access (022); every lane ends in James, so §6.2 keeps his queue short; sessions are disposable, the record is not — any new session resumes from the register + `board.json` + the pinned package.

---

## 5. Design and build in parallel — pin, cut, drift, change request

The problem: Claude Code builds A-01 from spec R1 over eleven days; meanwhile James and Claude Design improve A-01. The mechanism below refuses all three bad outcomes (ship superseded, freeze design, diverge silently).

### 5.1 Pin
Each booklet states `design_pin: H-01 R<n>` and the sheets it covers. Claude Code reads only that revision for those sheets, verbatim from `docs/design/`. The pin moves only in the next booklet. Bags 1–3 pin R1.

### 5.2 Cut — weekly, Friday (Q9)
Claude Design is never frozen. Every Friday a **cut** is exported: a zip with sha256, imported verbatim to `docs/design/H-01-R<n>/` exactly as 019 §1.4 did R1, register note with hash, `decisions.md` diffed to confirm append-only. Revision numbers advance weekly (R2 25 Sep, R3 2 Oct, R4 9 Oct, R5 16 Oct, R6 23 Oct). A cut with no design change is still cut — it re-seeds from the current fixtures (below) and carries the week's schema answers, so the drift report is small and honest rather than absent.

Two queues, as R1: **design-ahead** (unpinned sheets, journeys, D-01, Tier 2/3, responsive) is unconstrained; **design-behind** (a pinned sheet) lands as DEC entries and change requests, never as a silent edit.

**One village (Q8).** From cut R2, the prototypes are seeded from the F4/F5 fixture JSON, so a prototype and the app side by side show the same tree, track, parts and claims. What flows to Claude Design with every booklet: the current fixture set, the schema package's answers to `schema-requests.md`, the previous step-back's findings, and ChatGPT's proposals from the proposals folders (carried, contested in `decisions.md`, or put to James).

**Precondition (ARCHITECTURE §1a).** Weekly cuts need the package to have an identity of its own: a fielded manifest (`revision`, `executes`, `cut`, `supersedes`, per-sheet fidelity), a name that is not the H-01 sheet ID, and a working drift checker. Bag 1 builds the checker; the manifest and name are §10's open items and are needed **by cut R2 on 25 Sep**.

### 5.3 Drift
On import, the drift checker diffs `R<n>` against `R<n-1>` per sheet — spec · states · a11y tree · schema requests · DEC entries. For each sheet in build or built, Claude Code opens one `design-drift` issue and triages it in the step-back: **absorb**, **defer** (to a named bag), or **contest** (change request back, with reason). Sheets not yet in build take the new revision silently.

### 5.4 Change request
A sheet has one owner at a time (`board.json`). Design → build during a bag: a DEC entry, carried in Friday's cut; if it can't wait, James rules and Claude Code absorbs it with the criteria amended in the same PR. Build → design from a step-back: a `HANDOFF-` change request in the 014 shape, graded P0–P2, answered in the next cut. Ownership flips only at a cut or a dispatched change request.

---

## 6. The rhythm — the week, WIP limits, the before-you-open check, the board file

### 6.1 The week

| Day | Program (Cowork) | Build (Claude Code) | Design (Claude Design) | Review (ChatGPT) | Operator (James) |
|---|---|---|---|---|---|
| **Mon** | Booklet for any bag opening this week; reconcile Friday's register | Read the booklet; run the before-you-open check; open `bag/<n>` | Read the fixtures, schema answers and drift triage from Friday | Read the booklet; pick what to propose, review or test | Refine the booklet the same day; agree the picture on the box |
| **Tue–Thu** | Answer questions; draft the next booklet | Build; open issues; keep `board.json` current | Design-ahead; DEC entries for design-behind | Reviews, proposals, L1 PRs — all by PR | Build with the sheet as it lands; measure; rule on Q-items |
| **Fri** | Register reconciled; `PROGRAM.md` narrative; fleet status pushed | Step-back memo (if a bag closes) + drift triage + PRs ready | **Cut** — every Friday | Reconciliation memo if findings were contested | **Merge day.** Merge; allocate numbers; import the cut; rule on ladder moves |

### 6.2 WIP limits — three
1. One bag open in build. 2. One cut in flight (Friday's, imported and triaged before the next Friday). 3. One PR per lane waiting on James.

### 6.3 Before you open the bag
No bag opens until Claude Code has ticked every line in the booklet's PR description and James has seen it:

- [ ] Booklet accepted; register row moved to *accepted*; **the slice it delivers is stated in one sentence** (Q5)
- [ ] `design_pin` named; that revision on `main`, verbatim, hash recorded
- [ ] Drift report for the pin triaged — no untriaged `design-drift` issues on the bag's sheets
- [ ] Picture on the box agreed: acceptance criteria per sheet, initials in the booklet
- [ ] `pnpm validate:fixtures` green on `main`; contrast green; a11y baselines present for every component the bag uses
- [ ] Register reconciled — no *received, not issued* memo the bag depends on
- [ ] Open questions the bag depends on answered or parked with an owner
- [ ] Previous bag's step-back issued; James described its slice unaided

### 6.4 The board is a file (Q7)
`docs/program/` holds three files: **`PROGRAM.md`** (§4–6 as the living version once this memo is accepted), **`board.json`** (`bags[] {n, sheets, state: sealed·booklet·building·step-back·done, pin, pr}` · `sheets[] {id, owner: design·build, pin, drift_open}` · `cuts[] {rev, friday, landed, sha256}` · `gates {…}` · `wip {…}` · `last_step_back` · `last_cut`; updated by Claude Code in the same PR as the change it describes), and **`before-you-open.md`** (§6.3 as the template). GitHub issues carry `lane:*`, `bag:*`, `sheet:*`, `design-drift`, `change-request` labels and the four milestones. **No GitHub Projects.** The fleet status feed (§7) is a projection of `board.json`, never a second source.

---

## 7. Where the app lives and what the fleet sees

**Where.** One app, `apps/drafting-table`, Vite dev server on the Mac. Not `apps/planner` / `apps/family` — K-4 / DEC-019 stays unadjudicated.

**Frame, experience plane: absent.** No federation, no host shell, no shared theme provider. Own router, own theme toggle, actor stub as data.

**Frame, tooling plane: present from Bag 1, shaped by the Q1 research.** Claude Code's research document says what the morning cockpit and fleet tracking actually consume; `fleet/status.json` is then a projection of `board.json` in that shape, pushed by CI on `main`. `.claude/northstar.md` `current` bumped in each step-back commit. Branches `bag/<n>-<slug>` (build) and `correspondence/<nnn>-<slug>` (program); PR descriptions in memo shape; the session's attribution lines on every commit. The same research document writes down the **cluster onboarding pipeline** — founding acts, register, Northstar, PR-flow, board, status feed — as the checklist the next play-well repo, or the next cluster, follows.

---

## 8. The calendar, with lanes

Today is Friday 18 September. The gate is Wednesday 21 October — 33 days.

| Window | Build | Design (cut every Friday) | Review / Program | Ends with |
|---|---|---|---|---|
| 18 – 22 Sep | Bag 0 (this) | design-ahead: G-1, D-01 lift; **manifest + package name agreed** | ChatGPT reviews 023; Cowork drafts Bag 1 booklet | 023 accepted |
| 22 – 26 Sep | Bag 1 · foundations + Q1 research, pin R1 | **cut R2 · 25 Sep** — first fixture-seeded cut | Bag 2 booklet | fixtures validate; contrast green; fleet sees us; questions-before-contracts |
| 26 Sep – 2 Oct | Bag 2 · components (Ladle), pin R1 | **cut R3 · 2 Oct** | ChatGPT L1: adversarial fixtures | 17 components with a11y baselines |
| 30 Sep – 3 Oct | Bag 3 · Hub, pin R1 | ownership of A-01/M-01/C-01/P-01 → build at R3 | Bag 4 booklet pins R3 | app running |
| 3 – 14 Oct | Bag 4 · A-01 + geometry, pin R3 | **cut R4 · 9 Oct**: Tier 2 receiving sheets begin | ChatGPT L1: golden cases for the six checks | **14 Oct — six checks in code, Q13 BLOCK reproduced** |
| 7 – 17 Oct | Bag 5 · M-01 + C-01, pin R3 (R4 drift triaged) | **cut R5 · 16 Oct**: Tier 2 | Bag 6 booklet | BOM rows with chips; ReleaseGate record |
| 14 – 20 Oct | Bag 6 · P-01, pin R3 | design-ahead on R5 drift | real-bricks booklet for geometry | three diverging orders; retroactive path |
| **21 Oct** | | | | **ORDER-BY GATE** — release on software artifacts, or order by hand and record after the fact |
| 21 Oct – 25 Nov | Bag 7 · real bricks; then Tier 2 sheets from R4/R5 | **cut R6 · 23 Oct** onward, weekly | | parts received and inspected in the system |

Two honesties stand from R1: it is tight and one implementer — if it slips, P-01 optimisation goes first, then 3D look presets, then the rig accordion; the six checks, the M-01 loops and the C-01 rows do not slip. And the gate holds either way: the retroactive-order path is built before the optimiser.

---

## 9. Amendment to 019 §6 — proposed wording

Strike, under *Not authorised*: "Any workflow UI before the schema gate."

Replace with: "Any workflow UI that reads anything other than `packages/schema` fixtures (HANDOFF-LEGO-PIPE-023 §1, rules F1–F5) before the schema gate. The gate is closed by James signing `packages/schema` together with the per-sheet acceptance criteria; those are produced by Bags 1–3 of 023 and are exercised by the running app before signature. `DataSource = real` for any entity remains unauthorised until that entity's booklet is accepted. Design package revisions are imported verbatim per 019 §1.4, weekly, and consumed by build only through a named `design_pin` (023 §5)."

Everything else in 019 §6 stands.

---

## 10. Rulings recorded, and what is still open

**Recorded** (§0a): Q1 → research item · Q2 `drafting-table` · Q3 023 confirmed · Q4 Ladle · Q5 slices · Q6 vocabulary · Q7 file board · Q8 one village, three axes · Q9 weekly Friday cuts · Q10 L1.

**Still open — two, both on the design package (ARCHITECTURE §1a), both needed by cut R2 on 25 Sep:**

1. **The package's own identity.** A fielded manifest (`package.yaml`: name · revision · executes · cut date · supersedes · sheets with fidelity · decisions range · known defects) beside `index.json`, and a **package name that is not a sheet ID** — `LVP-DESIGN` is a placeholder; yours to name. Claude Design produces the manifest; Claude Code's importer records sha256 and bytes beside it.
2. **Where package cuts are registered.** A second register table for instruments (017 §1.2, S-08) — one row per cut: name · revision · executes · sha256 · imported at version · pinned by bags. Or a row in the main table per cut under `HANDOFF-`, as rule 5 already permits. One line from you settles it.

**A rule-7 note, for the record, not a question:** R1 widened recipients (Claude Design, ChatGPT added) and R2 renames the thread. Rule 7 says changed recipients want a new number; rule 6 says a revision keeps author, purpose, authority and scope, all of which held. Treated as a revision on the strength of purpose and scope; if you rule otherwise, R2 becomes 024 and 023 is superseded — nothing else changes.

---

## 11. What happens on acceptance

1. James accepts 023 (R2); the row moves to *accepted*; the register's rule-16 thread list gains `drafting-table`; 019 §6 is amended by a dated entry appended to `docs/design/H-01-R1/decisions.md` pointing here.
2. Claude (Cowork) issues **Bag 1's booklet** as a `CORR-` memo with its chart: workspace diagram, schema entity map, the F4/F5 village, `design_pin: H-01 R1`, the slice it delivers in one sentence, and the picture on the box for Bag 1.
3. Claude Code runs the before-you-open check, opens `bag/1-foundations`, creates `docs/program/`, starts the Q1 research document, and reports by step-back.
4. Claude Design receives the design-ahead queue for 22 Sep – 2 Oct, the fixture JSON to seed cut R2, and the manifest request (§10.1).
5. ChatGPT receives 023 for review by PR, its rung (L1), and the two proposals folders.
6. `docs/program/PROGRAM.md` is seeded from §4–6.

— Claude (Cowork), coordinating reviewer and handoff author · register version read `2026-09-18.21`
Under James (`@ojfbot`), who allocated 023 and rules on §10.
