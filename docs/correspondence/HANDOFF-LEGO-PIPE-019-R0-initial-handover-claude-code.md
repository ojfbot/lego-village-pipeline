---
correspondence_schema: lego-pipe-memo/v1
memo: HANDOFF-LEGO-PIPE-019
revision: R0
status: accepted
memo_type: handoff
title: "Initial handover to Claude Code — stand up the play-well cluster"
subtitle: "Two repos from ~/ojfbot, the correspondence system as first commit, the build-harness work order, the design package under 014, and exactly what is authorised"
date: 2026-09-17
thread: cluster
cluster: play-well
project: LEGO Village Pipeline
from:
  actor: "Claude (Cowork)"
  role: coordinating_reviewer_and_handoff_author
  provider: Anthropic
to:
  - actor: "Claude Code"
    role: implementer
    provider: Anthropic
  - actor: James
    handle: "@ojfbot"
    role: operator_and_final_authority
    provider: operator
in_reply_to:
  memo: HANDOFF-LEGO-PIPE-014
  revision: R0
authority:
  decision_owner: James
  dispatch_authority: James
  implementation_authorized: "founding acts + 011-R2 cleared scope + 018 spikes + 014 Boundary 1 preparation only"
  production_code_authorized: false
register:
  number: 019
  allocated_by: "proposed — James confirms before dispatch (rule: numbers are allocated by the operator)"
  allocated_on: 2026-09-17
repos:
  - ojfbot/lego-village-pipeline
  - ojfbot/play-well-library
tags:
  - initial-handover
  - founding-acts
  - play-well
  - correspondence-register
  - design-package-R1
  - build-harness
  - order-by-gate
argument: >-
  In which Claude Code receives its first message: two empty directories under
  ~/ojfbot become the play-well cluster; the correspondence register and preflight
  are committed first because authority transfers on that commit; the accepted
  build-harness work order (011-R2) and its spikes (018) are handed over unchanged;
  the design package H-01 R1 is handed over with a readiness verdict of "build Tier 1
  from it" plus six known defects, two debts owed by Claude Design, and one operator
  item on the critical path; and the authorised scope is drawn narrowly enough that
  nothing built in the next five weeks hardens a decision the operator has not made.
parts:
  "0": "Orientation — where you are, what exists, what is attached"
  "1": "Founding acts, in order"
  "2": "The play-well cluster — two repos and why"
  "3": "Stream A — build harness (011-R2 + 018), handed over unchanged"
  "4": "Stream B — design package H-01 R1 under 014: readiness verdict"
  "5": "The calendar — the deadline is 21 October, not Christmas"
  "6": "Authorised / not authorised"
  "7": "First deliverables and what to report back"
  "8": "Standing rules"
provenance:
  source_artifacts:
    - {name: "LEGO Village Pipeline 2.zip", role: "design package H-01 R1 (Claude Design session 2)", sha256: "e898a64a7057b49ecb8bfdab1654f5b17a0cfe74b5ffbe48a2b69305c95a7789", bytes: 9850637}
    - {name: "design-review/HANDOFF-LEGO-PIPE-014-R0-design-brief.md", role: "the design work order R1 was built under"}
    - {name: "build-harness/LEGO-PIPE-011-from-studio-to-stage-R2.md", role: "accepted build-harness work order"}
    - {name: "build-harness/HANDOFF-LEGO-PIPE-018-spikes-S1-S7-claude-code.md", role: "spike specifications"}
    - {name: "correspondence/REGISTER.md", role: "register, version 2026-09-17.5"}
    - {name: "correspondence/preflight.py", role: "reference preflight (v1), to be replaced per 011-R2"}
    - {name: "correspondence/ROUTING-2026-09-17.md", role: "routing sheet; its Claude Code preface is folded into §3"}
  method: "package-level readiness review of H-01 R1 against 014 Boundary 1 (no prototype QA — that is Claude Code's job); self-check scripts executed; offline load of all ten sheets; cross-artifact consistency"
---

# HANDOFF-LEGO-PIPE-019 — Initial handover to Claude Code

Claude Code —

You have received nothing before this. Everything below is the founding state. Read §0 and §6 before touching the filesystem.

---

## 0. Orientation

**Where you are.** James will run you from `~/ojfbot`. Two directories exist there and are otherwise empty: `~/ojfbot/lego-village-pipeline` and `~/ojfbot/play-well-library`. No `git init`, no `claude init`, no files. That is deliberate — the first commits are yours, and their order matters (§1).

**Who you are talking to.** James (`@ojfbot`, `@jfo` in the design thread) is the operator and the only decision authority. He is also, until 25 December 2026, the only user. Two other agents have been working upstream of you: Claude (Cowork) — me — as coordinating reviewer and author of the work orders; and ChatGPT as independent reviewer. Claude Design produced the design package. None of us implements; you do.

**What is attached / to be committed.** Every document named in `provenance.source_artifacts`, plus the design package zip. The register (`REGISTER.md`) is the index to all of it. Read it first; it explains the numbering (`HANDOFF-` / `CORR-` / `REVIEW-` + number + revision), the collisions that were recorded rather than repaired, and the rules you now inherit.

**What this project is.** A digital twin for a multi-year LEGO Christmas village — MILS modular snowy landscape, R40 railbed around an owned, built tree (41843, base 16×16 studs, measured), run by an owned Winter Holiday Train (full circle, 16 curves). The software turns designs into validated components, aggregates parts, subtracts inventory, produces purchasing artifacts, and reconciles what was built. Between now and Christmas, James is dogfooding it to buy real parts and build a real railbed. The demo on 25 December is "software planned and delivered a physical thing, and the method scales when the family picks it up." The family arrives after the demo.

---

## 1. Founding acts, in order

Do these before anything in §3 or §4. Order is not optional.

1. **`git init` both repos.** Default branch `main`. Attribution convention in §8.
2. **First commit in `lego-village-pipeline`: the correspondence system.** `docs/correspondence/REGISTER.md` (verbatim from the attached copy, version `2026-09-17.5`) and `tools/preflight.py` (the v1 reference). **Authority over the register transfers to this commit** — the register says so itself. Bump the register version line and add a row for this memo (019) as the first act after the commit.
3. **Commit every correspondence document** under `docs/correspondence/`, filenames as registered. Do not paste content between files; copy files. The register's rule 1 is "attach, never paste," and it has already caught one mangled transfer this week.
4. **Commit the design package** verbatim under `docs/design/H-01-R1/` — the whole `handoff/` tree, including `standalone/` and `dt/` together (the README says why). Record its sha256 (`e898a64a…7789`) in the register row.
5. **`claude init` / `CLAUDE.md` in `lego-village-pipeline`.** Seed it with §8 of this memo and the design package's own `CLAUDE.md`. Keep it short; the register and the work orders are the long form.
6. **Create `play-well-library`** empty except for the attribution file and the branch-flow CI rule, exactly as 011-R2 routing §1 item 5 specifies. Nothing else goes in it yet.
7. **Register both repos in Northstar under `play-well`.**

Then report (§7) before proceeding.

---

## 2. The play-well cluster — two repos and why

From 011-R2 §3.1, accepted:

| Repo | Contents | Why separate |
|---|---|---|
| `ojfbot/lego-village-pipeline` | Code: brickcore, brick_bench, studio-bridge, harness API, mils-integrator, roofsnow, resolver, CLI. Also `docs/` — correspondence, design package, spikes, ADRs | Tools evolve independently of content; CI runs tests, not asset diffs |
| `ojfbot/play-well-library` | Canonical **content**: assets, published version manifests, validation reports, golden set, catalog index. Text + LFS pointers. Family branches live here | Content history readable without code churn; can be private forever |
| blob store (not a repo) | Derived representations by sha256 | Regenerable; never merged. Dev: a directory |

One boundary is **not** settled and you must not settle it by scaffolding: **Frame integration topology and ledger ownership** (014 K-4, DEC-019). You may inspect the existing Frame/app fleet, identify constraints, run bounded spikes, and submit alternatives with consequences. James decides. `repo-structure.md` in the design package proposes a two-app split; it is marked unadjudicated and stays so.

---

## 3. Stream A — build harness, handed over unchanged

**Work order:** `LEGO-PIPE-011-from-studio-to-stage-R2.md` — accepted, cleared by ChatGPT for a limited scope, preflight passed. Read its Orientation and §0a change log first; Parts B–D are the architecture, with ADR amendments appended at the end of Parts C and D (amendments win over earlier text). ADRs 0001–0005 from mils-integrator remain in force.

**Authorised scope, nothing beyond it** (routing sheet §1, reproduced so it is in one place):

1. The Stage-0 data contracts in 011-R2 §3 as typed schemas with validators — **every ambiguity surfaced as a question for James before anything else is built.**
2. `tools/preflight.py` replaced by a versioned `lego-pipe-memo` JSON Schema + CLI, wired to `docs/correspondence/REGISTER.md`. **v1 is the operative contract; v2 is proposed (CORR-016/017) and not ratified.** This memo is issued as v1 and passes the reference preflight. **018 is written as v2 and fails the v1 preflight on `schema id` and `status`** — under register rule 2 it cannot act as a work order until James either ratifies v2 or 018 is re-issued as v1. Do not begin the 018 spikes until one of those has happened; do begin S2 and the S7 container half, which are authorised by 011-R2 (v1, passed).
3. Spike S2 in CI against OMR fixtures, and the container half of S7.
4. `brickcore/` scaffolded only as far as S2/S7 need, **moving** mils-integrator's `ldraw/parser.py` and `catalog.py` rather than forking them.
5. `play-well-library` created empty per §1.6.

**Spikes on the Mac:** `HANDOFF-LEGO-PIPE-018` — S1 (Studio round trip, seven probe files, James presses Save As seven times) and the native half of S7 (USD runtime matrix). Authorised: disposable scripts under `spikes/S1/`, `spikes/S7/` and two findings notes under `docs/spikes/`. Not authorised: anything under `brickcore/`, `brick_bench/`, `studio-bridge/` beyond item 4 above; any modification of Studio.

Each spike ends in a findings note. Open one issue per item in 011-R2 §6 "Open items". **Do not scaffold production package boundaries until S1/S2/S7 have reported.**

---

## 4. Stream B — design package H-01 R1: readiness verdict

**Verdict: build Tier 1 from it.** The package is good enough to carry the procurement spine — geometry → BOM → release gate → order capture — to the 21 October gate. It is not clean, and you are told exactly where it isn't so that nothing surprises you.

### 4.1 What is sound

Claude Design did what 014 asked for Tier 1, and the record shows it. Decision ledger with stable IDs `DEC-001…035`, `supersedes` and status; the tree measured and every placeholder retired (DEC-016); MILS settled as 32×32 with "Section" as the group placeholder (DEC-017); A-01 gained a **3D · CHECK IT** tab reading the same geometry as the plan, with six deterministic fit checks and a propose-then-confirm move pattern (DEC-018/030); the `basis` field split into stored + derived axes with a composed sentence per row (014 §7.2); a new **M-01 Measure and check** sheet for the measurement and verify-a-claim loops (DEC-026); a **ReleaseGate** component at the end of C-01 carrying the 014 §8 record, with P-01 read-only until released, a forced stock/price **revalidation** before any BrickLink link opens, the `ordered → owned` shortcut removed, and **manual / retroactive orders as a first-class case** (DEC-025/034); the family identity `@boys` replaced by initials EH/HH/LH (DEC-027); a semantic retrofit of A-01, C-01, P-01, M-01 (`lang`, `<title>`, one `<h1>`, `role=main`, live regions, accessible names on every control — I measured, not trusted: zero unnamed buttons on any of the ten sheets); `specs/ANNOUNCEMENTS.md` (trigger → region → sentence); accessibility-tree baselines for the three Tier-1 sheets; a contrast contract with a checker; a manifest with declared `path_base`, inline decision records and schema requests, and a drift checker.

The prototypes remain behaviour references. Their code is not to be copied.

### 4.2 Known defects — treat these as first-day facts, not surprises

These are package-integrity findings. I did not QA the prototypes; that is yours.

| # | Defect | Evidence | Your handling |
|---|---|---|---|
| D-1 | **The contrast contract fails its own check.** Blueprint `--dt-block` = 4.27:1 (needs 4.5). DEC-023 darkened paper only. `--dt-block` is the error/blocked colour and is used as text on six sheets. | `node dt/check-contrast.mjs` → `FAIL … 1 contrast failure(s)`, exit 1 | Fix the token in `packages/tokens` when you create it; keep the checker; make it a CI gate. |
| D-2 | **The drift checker crashes and the drift it reports was shipped anyway.** `check-manifest.mjs` reports four state screenshots in `index.json` but not `STATES.md`, then throws `ENOENT` on `.dc.html` source files that aren't in the bundle. | `node handoff/check-manifest.mjs` from archive root → four `MISSING`, four drift lines, uncaught exception, exit 1 | The checker was written against the design session's workspace, not the shipped package. Rewrite it against `docs/design/H-01-R1/` as root. Reconcile `STATES.md` with the four new captures (`10-a01-3d-fit`, `11-c01-release-gate`, `12-p01-manual-order`, `13-m01-claim-draft`). |
| D-3 | **A-01's 3D check surface now loads Three.js from a CDN** (`cdnjs.cloudflare.com/…/three.js/r128/three.min.js`). Offline it does not render — `canvas: 0`. The R0 bundle had Three.js inlined and worked offline; R1 regressed it. The README's "open in any browser, no server" is false for A-01 specifically. | All ten sheets loaded with every non-`file://` request aborted: nine load with zero external requests; A-01 attempts one and fails | The fit proof is Tier-1 critical. When you build A-01, Three.js is a pinned dependency in the repo, never a runtime CDN fetch. Q12 (Three.js imported twice) is still open — resolve both together. |
| D-4 | **`path_base` describes directories that aren't shipped.** It says archive root contains `dt/, handoff/, brief/, prototypes/`; the zip contains only `handoff/`. | `index.json` `path_base` field | Treat `handoff/` (your `docs/design/H-01-R1/`) as root. The design session's `prototypes/` are its sources and stay with it. |
| D-5 | **Accessibility retrofit is Tier-1 scoped, and landmarks are thin even there.** D-01, F-01, H-01, Hub, J-01: no `<h1>`, no `main`. A-01, C-01, P-01: `role=main` present but no banner/nav/contentinfo. Hub and J-01: no live region. | DOM measurement, all ten sheets | Consistent with DEC-021's stated order ("A-01, C-01, P-01 first"). 014 §6 remains the contract for every sheet you build; the design package's partial coverage does not narrow it. |
| D-6 | **H-01's inline file preview does a `fetch()` on a `file://` URL**, which browsers refuse. | Console: `Fetch API cannot load file:///…` | Cosmetic in the prototype. Do not reproduce the pattern. |

### 4.3 Debts owed by Claude Design — not blocking Tier 1, but owed

| # | Gap vs 014 | Why it doesn't block | What you do meanwhile |
|---|---|---|---|
| G-1 | **No journey hierarchy artifact.** 014 §3 asked for L0/L1/L2/L3 with J1–J13 as aliases; the package still carries the flat J1–J13 list. Journeys 2–5 "to screen level" landed as the *sheets* (A-01, C-01, P-01, M-01), not as journey documents. | The sheets are the screen-level design of the spine. The map is needed for the trace matrix and for Boundary 2, not for building the spine. | Build against the sheets. When you write the trace matrix (011-R2 / 014 §11), key it to sheet IDs and the `DEC-` ledger; the journey IDs get joined in when the hierarchy lands. |
| G-2 | **No per-sheet acceptance criteria.** 014 §10.16 asked for them delivered with each sheet. `ANNOUNCEMENTS.md`, the a11y trees, `STATES.md` and each spec's *States* section are acceptance *material*; no sheet states what "done" means. | You can derive them. | For each Tier-1 sheet, **propose** acceptance criteria from the spec's Behaviour + States, `ANNOUNCEMENTS.md`, and the a11y baseline, and submit them with the schema proposal for James's approval. Nothing is "done" until he has signed the criteria it is done against. |

### 4.4 Operator item on the critical path — not yours to resolve, yours to make visible

**Q13 — the fit proof blocks.** A-01's six checks return an honest **BLOCK** on an 8×8 inner-corner overlap: the R40 ring centred on the tree, carried on 2×2 Sections of 32×32 MILS, collides with the 16×16 tree base at the inner corner. This is not a package defect. It is the design doing its job — Tier 1 existed to find exactly this before money is spent. It needs James plus RESEARCH-01 (track-circle geometry: 16 × 53400 at R40 centre-line; Section arrangement for the curve; MILS height under the base). **It sits on the 14 October milestone.** Your job: when the geometry package exists, the same six checks run in code against the same inputs, so that the resolution James chooses is verified, not drawn.

### 4.5 Open items you inherit from the package

Q1 RESEARCH-01 vocabulary (blocks schema naming — use neutral `Item`/`Unit`/`Section` with TODO tags); Q11 `need_origin` row- vs parent-level (with ChatGPT — do not assume either); Q12 Three.js double import; Q13 above; Q5/Q6 wand and procurement data backends (mock today; real is yours but not Tier 1). Q7 responsive and everything in Tier 2/3 are not this round.

---

## 5. The calendar

The demo is 25 December 2026. **That is not the deadline.** Backward from a physical build:

| Date | Milestone |
|---|---|
| **2026-10-14** | Railbed geometry validated — Q13 resolved and verified in code |
| **2026-10-21** | **ORDER-BY GATE** — BOM and procurement plan trusted enough to spend money against |
| 2026-10-28 | Orders placed (multi-shop BrickLink, international, into holiday congestion) |
| 2026-11-25 | Parts received and inspected — Tier 2 (receive → inspect → discrepancy → allocate) must exist by here |
| 2026-11-29 → 12-20 | Physical build and commissioning |
| 2026-12-25 | Demo |

Two prioritisations that are easy to get backwards: **BOM correctness outranks procurement optimisation** (a suboptimal shop set costs dollars; a wrong BOM costs Christmas), and **the record outranks the automation** (what the demo proves is that decisions and provenance were captured and scale). A standing instruction: if the software isn't trustworthy by 21 October, James orders anyway and the system records it after the fact — a retroactively-entered order with honest provenance is a supported case, never a workaround. Do not build anything that makes it impossible to represent.

---

## 6. Authorised / not authorised

**Authorised now:**
- §1 founding acts.
- §3 Stream A scope, items 1–5, and the 018 spikes.
- §4 Stream B, **Boundary 1 preparation only**: propose `packages/schema` (types + runtime validators + state machines) from `schema-requests.md` and 014 §7; propose per-sheet acceptance criteria (G-2); propose the geometry package's canonical representation (integer LDU for X/Y/Z, display units as preference, rotation in its own declared unit — 014 §7.1) with property tests and golden cases; surface every ambiguity as a question. **James approves the schema and the criteria before any workflow UI is built.**

**Not authorised:**
- Production code, production package boundaries, anything under `brick_bench/` or `studio-bridge/` beyond §3 item 4.
- Any workflow UI before the schema gate.
- Frame topology or ledger ownership by scaffolding (§2).
- Modifying Studio, or anything in the design package's `standalone/` — it is a reference, committed verbatim.
- Renumbering anything in the register. Collisions are recorded, not repaired.
- Tier 2 and Tier 3 of 014.

---

## 7. First deliverables and what to report back

In this order, each a separate report (a memo under `docs/correspondence/`, registered, or a PR whose description follows the memo shape):

1. **Founding-acts report** — both repos initialised, register committed and version bumped, correspondence and design package committed with hashes recorded, `CLAUDE.md` seeded, Northstar registration. One page.
2. **Questions before contracts** — every ambiguity found in 011-R2 §3 and in `schema-requests.md` / 014 §7, as a numbered list for James. Do not resolve them by choosing. Batch them; do not trickle.
3. **Spike findings** S1, S7-native (018), S2, S7-container (011-R2) — findings only, under 600 words each, `[unverified]` on anything not directly observed.
4. **Schema + acceptance-criteria proposal** — the Boundary 1 gate package for James.

Every report cites this memo as `HANDOFF-LEGO-PIPE-019` and the work order it executes.

---

## 8. Standing rules

From the design package's `CLAUDE.md`, the 014 constraints, and the register:

- **Every UI is a frictionless teacher.** Plain words first; controls explain consequences; AI questions arrive as conversation; no jargon-first labels. Where rigor and this principle conflict on a family-facing surface, the teacher wins and the rigor moves to the operator side (014 K-7, DEC-022).
- **Evidence axes stay separate** — origin · method · verification · authority · workflow. AI origin is permanently visible. The AI restates what it changed before anything is saved, and the restatement is announced (a live region), because a safety behaviour nobody can perceive is not one.
- **The accessibility tree is the agent-facing contract** (014 §6). One `<h1>`, landmarks, `lang`, `<title>`, accessible names on every control, live regions on every derived or async change, keyboard operation, focus management. An accessibility-tree snapshot per sheet is diffed on change and a regression fails the build — treat it exactly as a broken API. This is not compliance; an empty tree forces every agent, test harness and host into pixel archaeology.
- **Requests are first-class and never deleted.** Basis on every part row. Prices are ranges. Gates are stamps for the record and quiet modals for the act. Purchase stays outside the app.
- **People.** James is a friend of the family — never "Dad", never a parental role. The boys are EH, HH, LH. Kid-facing copy says "James" sparingly and never talks down.
- **All numbers in prototypes are MOCK MATH.** Real values need your implementation plus an independent audit with stated invariants (no negative free area, deterministic tie-breaking in the procurement search, golden cases).
- **Vocabulary is under review** (RESEARCH-01). Neutral internal names with TODO tags until it lands.
- **Register rules 1–6** as written in `REGISTER.md`. Attach, never paste. Filename is not identity. Numbers never move once cited. Collisions recorded, not repaired.
- **Commits** end with the attribution lines the session provides. **Every commit that touches `docs/correspondence/` bumps the register version line.**

— Claude (Cowork), coordinating reviewer and handoff author
Under James (`@ojfbot`), who confirms register number 019 and dispatches.
