# build-harness — architecture, ADRs 0006–0011, and LEGO-PIPE-010

**Date:** 2026-09-17 · **Cluster:** play-well / ojfbot/lego-village-pipeline · **Status:** proposed (design only, no code yet)
**Builds on:** `studio-bridge/research-bricklink-studio-agent-integration.md`, `mils-integrator/*` (ADRs 0001–0005, briefs 03/04)
**One line:** Natural language in. An agent works in Blender through a constrained, deterministic LEGO layer. Every change becomes a validated, reviewable diff to a single canonical LDraw build that family members open and edit in Studio. Studio calibrates the validator; it does not sit in the loop.

---

## 1. Requirements

1. **Agent path.** A user describes a change. An LLM agent carries it out in Blender, because Blender can be scripted and Studio can't. The result exports as LDraw/`.io` that Studio opens with no repair.
2. **Deterministic fitment.** A Python layer checks every part against the model origin and against every other part: grid alignment, stud/anti-stud connection, collision, floating parts, grounding. Same input → same report, every time.
3. **Studio is the reference.** Our validator must agree with Studio's import, connectivity, collision and stability checks. Disagreements are tracked and resolved.
4. **Multiple users, most not Blender users.** James works in Blender. The adult family user and the kids work in Studio by hand, and make natural-language changes through the drafting table app. Their language changes still run through the Blender agent path under the hood.
5. **Drift is caught by the system, not by James.** Non-developers and children can't spot geometric, semantic, state or inventory drift. The harness has to detect it, explain it simply, block what is unsafe, and keep every step undoable.
6. **Output can be bought.** Parts lists map correctly to BrickLink and flag part/colour combinations that were never produced. Nothing is ever ordered automatically.

## 2. Architecture

```
          family (Studio, by hand)                 family / James (natural language)
                   │  save .io                                │
                   ▼                                          ▼
      studio-bridge ingest ──────────┐          drafting table (Frame app)
      (watch folder, read .io,       │           role-scoped tools only
       normalise, identity-match)    │                        │
                   │                 ▼                        ▼
                   │        ┌────────────────── build-harness API ───────────────────┐
                   │        │  propose(request, scope) → Proposal                     │
                   │        │  accept / reject / undo / history / export              │
                   │        └───────┬───────────────────────────────┬─────────────────┘
                   │                │ domain ops                    │ renders
                   ▼                ▼                               ▼
          ┌─────────────────────────────────────┐     ┌──────────────────────────────┐
          │ brickcore  (pure Python + numpy)    │◀────│ brick_bench Blender add-on   │
          │  ldraw/io · frames · lattice        │     │  scene = projection of doc   │
          │  connectors · collision · graph     │     │  snapped domain ops → core   │
          │  stability(adv) · inventory · diff  │     │  previews (Workbench/Cycles) │
          │  validate → ValidationReport        │     │  modes: interactive (James,  │
          │  + mils-integrator / roofsnow checks│     │  official connector) ·       │
          └───────────────┬─────────────────────┘     │  headless worker (family)    │
                          │ commit                    └──────────────────────────────┘
                          ▼
          BuildDoc store (versioned): canonical MPD + manifest + reports + renders
                          │                                   ▲
                          ▼ write .io / .ldr                  │ agreement matrix
                   Studio (open via Launcher)      studio-oracle skill (computer use,
                                                    golden set, on demand)
```

### Components

| Component | Responsibility | Runs where | Depends on |
|---|---|---|---|
| `brickcore` | The truth. Parse/write LDraw and `.io`; coordinate frames; lattice snapping; connector extraction; connection graph; collision; advisory stability; inventory mapping; identity diff; validators | Anywhere Python runs: Mac, CI, Pi. **No `bpy`** | numpy; LDraw library; LDCad shadow library; Rebrickable data |
| `brick_bench` (Blender add-on) | Builds the Blender scene from a BuildDoc. Exposes snapped domain ops that call brickcore. Renders previews. Handles dev-mode sync from hand-edited scenes | Interactive: native Blender.app on James's Mac via the official connector. Worker: headless `blender -b` in Docker on the Mac (dev), later a cloud instance | brickcore; ImportLDraw or ldr_tools geometry |
| `studio-bridge` | Read/write `.io`, open files in Studio, watch the shared model folder, map Studio ids and colours | Mac | brickcore; Studio install tables (read at runtime, never shipped) |
| `studio-oracle` (skill) | Computer-use playbooks that run Studio's import, connectivity, collision and stability checks on a file and record the verdicts | Mac with Studio idle | Studio, computer use |
| build-harness API | Proposal lifecycle, role scoping, versioned store, audit log, drift telemetry | Mac (LAN service) | all of the above |
| drafting table | Family-facing interface: request box, proposal cards, before/after renders, accept/undo, parts list and cost | Frame fleet app | build-harness API |

## 3. Core model and numbers

### 3.1 BuildDoc (single source of truth)

- **`model.mpd`** is canonical LDraw. LDraw colour codes. Positions are integer LDU wherever they are on the lattice. Rotation matrices are exact 0/±1 entries from the rotation group. Line order is kept, because steps depend on it. Number formatting is normalised.
- **`manifest.json`** holds:
  - a stable uid per placed part (`uid → part, colour, submodel, line index`)
  - lattice class per part
  - provenance (author role, request id)
  - library versions (LDraw release, shadow library commit, Rebrickable dump date)
- **History:** every accepted change is a commit. Each commit carries: author role, request text, `ChangeIntent`, diff, `ValidationReport`, before/after renders, BOM delta. Git fits well (repo per village), or content-addressed snapshots in SQLite following ADR 0002.
- **Studio drops our metadata. Assume it keeps nothing.** Identity is rebuilt by matching (§3.5), never read back from the file.

### 3.2 Frames

- LDraw: right-handed, **−Y up**, units LDU. This is brickcore's internal frame, the same as mils-integrator.
- Blender: +Z up. One conversion in `brickcore.frames`: `B = S · A · L`, with A mapping (x, y, z) → (x, z, −y) and S a fixed scale. The scale must match the importer in use; spike S4 confirms it.
- Every Blender↔core crossing goes through this single function. It gets a property test: the round trip is exact on lattice points.

### 3.3 Lattice (spec constants, versioned)

| Constant | Value |
|---|---|
| Stud pitch | 20 LDU |
| Plate | 8 LDU |
| Brick | 24 LDU |
| Stud height | 4 LDU |
| Baseplate | 4 LDU (MILS surface 36 LDU = baseplate + 4 plates) |
| Snap tolerance ε_snap | 0.05 LDU (Blender float noise is far smaller; Studio writes exact decimals) |
| Rotation group | the 24 proper axis-aligned rotations (det = +1). Mirror matrices (det = −1) are rejected |

**Lattice classes:**

- `lattice`: integer LDU after snapping, rotation in the group. Full fitment checks apply.
- `offgrid`: rotation in the group, position not integer LDU. Reported and blocked for agent ops. Allowed in human Studio edits, with a warning.
- `free`: rotation outside the group (hinges, turntables, flex parts, minifig poses). Excluded from strict fitment. Needs Studio or human review before it can count as valid.

### 3.4 Fitment

**Connectors.** A part's connectors are records of `(kind, gender, position, axis)`. Sources, in priority order:

1. **LDCad shadow library** (`SNAP_CYL` with gender M/F, `SNAP_INCL` grid repetition; CC BY-SA 4.0; partial coverage).
2. **Primitive scan** of the LDraw part tree. Stud primitives count as male; anti-stud and tube primitives count as female. The exact primitive→connector table is itself a versioned constant and needs a spike.
3. **mils-integrator `ldraw/catalog.py`** hand-curated entries.

v1 covers the stud system only (stud ↔ anti-stud/tube, including SNOT through connector axes). Technic, clip/bar and hinge connectors come in v2. A part with no resolvable connectors is `connectivity_unknown`, and **can never be reported valid** (ADR 0009).

**Connection.** Each connector's axis points out of its part: a stud's axis points up (−Y), an anti-stud's points down. Male connector m on part A mates with female connector f on part B when all three hold:

- their world positions are equal in integer LDU
- their axes are antiparallel
- m is not already mated

Matching is deterministic: sort by (uid, connector index) and pick greedily.

**Collision.** Two-phase, run on geometry with stud primitives removed:

- *Broad phase:* AABB overlap.
- *Narrow phase:* surface voxels at a fixed resolution (2 LDU). Penetration of 2 voxels or more is a collision. Face-to-face contact is not.
- *Stud intrusion:* a male stud whose cylinder enters another part's volume without a mate is a `stud_blocked` collision.
- *Disputed pairs* go to the exact mesh BVH in Blender (`mathutils.bvhtree`) when available.
- Studio's `collider/*.col` and `connectivity/*.conn` are never read (EULA; see research doc).

**Graph checks.** Built over parts (nodes) and mates (edges):

- `floating`: a part with no mates that isn't a root. Roots are baseplates, MILS module bases, or user-declared.
- `disconnected_component`: a component not linked to any root.
- `weak_link` (advisory): an articulation part joined by a single stud that carries more than N parts.
- `overhang` (advisory): a centre-of-mass heuristic per component.

Stability stays **advisory**. Studio's own stability check describes itself as "very conservative". A force-equilibrium LP (brief 04, LegoGPT-style) is an optional v2 module.

### 3.5 Identity and diff

Given two BuildDocs, match placements in passes:

1. Exact (part, colour, snapped transform).
2. Same part and transform, different colour → `recolor`.
3. Same part and colour, minimum-cost pairing on transform distance → `move` (Hungarian, deterministic tie-break).
4. Whatever is left → `add` / `remove`.

Submodels are matched by name first, then by content hash. The diff is the unit everything else works on: proposals, Studio ingest, history, undo, eval fixtures. It is the same `DiffOp` shape as roofsnow and ThemeDiffRow.

### 3.6 Inventory

`BOM(LDraw id, LDraw colour)` is mapped to BrickLink item and colour through Rebrickable (`external_ids`, part-colour availability), with the local Studio tables as a cross-check. Each line gets one status:

- `ok`: mapped, and the part/colour combination exists.
- `never_produced`: blocks family acceptance unless an adult marks it "custom".
- `unmapped`: blocks until mapping is fixed.
- `alias`: mold variant, BrickLink id differs.

Every commit checks that the BOM matches the model, so no inventory drift.

## 4. Validation tiers

| Tier | When | What | Gate? |
|---|---|---|---|
| T0 core | Every op (incremental) and every proposal (full) | Frames round trip, lattice class, mates, collision, floating/grounding, BOM ≡ model, part/colour availability, MILS/roofsnow validators, intent contract (§6) | **Blocking** for `block`-severity checks |
| T1 Studio file signals | Every Studio save that is ingested | `errorPartList.err` is empty; part count and identity diff match what was expected; Studio's `model2.ldr` `BL_Item_No` agrees with our mapping; Studio normalisations are learned into a table | Unrecognised parts hold the ingest as "needs fix" (not committed, not reverted); everything else commits with warnings |
| T2 Studio oracle | Golden set on library or validator changes (scheduled on the Mac); on-demand "Ask Studio" per build | Studio import, connectivity, collision, stability, run through computer use; verdicts recorded per check | Never inline; produces the agreement matrix and eval cases |

`ValidationReport` stays graded (`check id, severity block|warn|info, parts[], metric, message_dev, message_family`), matching mils-integrator. `message_family` is written for a child to read ("This roof piece isn't attached to anything — it would fall off").

## 5. Studio as calibration oracle

- **Golden set:**
  - known-goods: ~10 Winter Village and holiday sets from OMR (CC BY 4.0), plus James's owned anchors
  - synthetic mutations of each: remove a supporting part (floating), shift 1 LDU (misaligned), overlap two parts (collision), rotate 45° (free), swap to a never-produced colour, delete a submodel
  - accepted family builds, added over time
- **Procedure (skill):**
  1. `studio.open(file)`.
  2. Record the import dialog and error list.
  3. Stability tool → screenshot; Connectivity tab → screenshot; Collision on → screenshot.
  4. A vision pass returns a structured verdict per check with the flagged parts highlighted.
  5. Save as a new file → T1 signals.
- **Agreement matrix:** our verdict vs Studio's, per check type.
  - *Studio flags, we pass:* expected sometimes, because Studio is conservative and misalignment-sensitive. James adjudicates.
  - *We flag, Studio passes:* our false positive. Fix it or add an exception.
  - Every adjudicated disagreement becomes a regression fixture.
- **Targets for "calibrated":**
  - 100% detection of the synthetic `floating`, `collision` and `offgrid` mutations
  - zero `valid` verdicts on `connectivity_unknown`
  - ≥95% agreement with adjudicated truth on known-goods
- **Honest limit:** Studio's verdicts are read from screenshots, so the oracle is only as reliable as its readout and James's adjudication. That is why it calibrates the validator and never gates changes.

## 6. Family use: safety and drift model

### 6.1 What can drift, and the control for each

| Drift | Example | Control |
|---|---|---|
| Semantic | "Add a snowman by the bakery" → a snowman on the roof, or a white column | `ChangeIntent` contract checked against the diff; before/after renders; human accept |
| Geometric | Float accumulation, half-stud offsets, parts slightly apart | Snapped ops only; lattice class; exact-integer mates; round-trip idempotence test |
| State | Blender scene ≠ BuildDoc ≠ Studio file; edits in two places at once | BuildDoc is the only truth; the scene is rebuilt from it, never the reverse, except dev-mode sync; optimistic concurrency on base version; Studio ingest before any agent op |
| Inventory | BOM stale, wrong BrickLink colour, never-produced part/colour | BOM ≡ model per commit; mapping status; purchase gate |
| Destructive | "Delete everything", "make it all purple" | Branch-per-user; `main` is dev-merge only; one-tap undo; history is never rewritten; part-count delta stated on the card. No blast-radius limits (James's decision) |
| Content / safety | Kids take the assistant off-topic | LEGO-only tool surface and system prompt; AI disclosure; filtering and monitoring per Anthropic's guidance for products serving minors |
| Silent degradation | Library update changes connector extraction | Golden set and evals on every library or validator change; oracle agreement tracked |

### 6.2 Proposal lifecycle (nothing auto-applies, following ADR 0005 and ThemeDiffRow)

1. **Scope.** The user picks or confirms a scope (whole village, one module, one building/submodel). Agent ops outside the scope are rejected by brickcore, not by the prompt. Scope is about making the agent's work predictable, not about limiting the user: "whole village" is a valid scope for any role.
2. **Intent first.** The agent emits a `ChangeIntent` before building: target scope, allowed op kinds, expected part-count range, an anchor ("next to uid 412, east side"), and a one-sentence plan. Ambiguous requests produce a `DecisionPoint` card ("Big snowman or small one?") rather than a guess.
3. **Build.** The Blender worker runs snapped domain ops. brickcore validates each op as it goes; an op that fails a blocking check is rolled back and the agent gets the report to try again (bounded retries).
4. **Conformance.** The diff is checked against the intent: inside scope, only allowed ops, count within range, anchor relation holds. A vision/LLM judge compares the renders to the request **as advice only**.
5. **Proposal card.** Before/after renders, a plain-language summary, green/yellow/red checks with family messages, parts added/removed and cost delta. Accept, reject, or "try again with…".
6. **Commit.** Accept → commit → write `.io` as a new version (the previous version is kept) → Studio opens it if requested.
7. **Studio edits flow back.** A family member edits in Studio and saves → ingest → identity diff → T0 + T1 → recorded as a human commit. Warnings show in the drafting table; human edits are never auto-reverted.

### 6.3 Roles

| Role | Tools | Limits |
|---|---|---|
| `dev` (James) | Everything, including `bench.exec` (raw Blender Python through the connector), dev-mode scene sync, overrides with a reason, branch merges to `main` | Overrides logged |
| `parent` | propose, accept, undo, history, export BOM, place orders, approve "custom" colours, Ask Studio | None on building. Purchase actions gated behind explicit confirmation |
| `kid` | propose, accept, undo, history, own branches, export BOM (read-only, priced) | None on building. **No purchase actions.** LEGO-only assistant |

**Decision (James, 2026-09-17): building is free for everyone; only purchasing is gated.** No blast-radius limits, no destructive-op confirmations for kids. The safety property comes from versioning instead: every change is a commit on a branch, and no branch is "real" until James merges it to `main` (which mirrors the physical layout and the order pipeline). A kid can turn the whole village purple on their branch and nothing is lost. Destructive changes still get a plain-language "this removes 340 parts" line on the proposal card so the user knows what they accepted.

`main` = what's built or ordered. Family branches = play. Merging is a dev action with the full validator run.

### 6.4 James's view of drift

A weekly digest (a dashboard artifact) covers:

- proposals and acceptance rate by role
- blocking failures by check
- retries per request
- intent-conformance failures
- overrides
- Studio ingest warnings
- oracle agreement trend
- the requests the judge scored lowest

Red alerts fire on any `valid` verdict later contradicted by Studio or adjudication, and on mapping errors in an exported BOM. Family requests can be promoted to eval cases with one action.

## 7. Tool surface (JSON in/out; decision and check ids are stable API)

**Harness (drafting table):**
- `build.open(model_id)`
- `build.propose(request, scope)` → `{intent, decisions_open, diff, report, renders, bom_delta}`
- `build.answer(decision_id, option)`
- `build.accept(proposal_id)`, `build.reject(proposal_id, reason)`
- `build.undo(commit_id)`, `build.history(model_id)`
- `bom.export(model_id, format)` (parent-gated)
- `studio.open(model_id)`
- `oracle.ask_studio(model_id)`

**brickcore / brick_bench domain ops (agent-facing; the only way the agent changes geometry):**
- `place(part, colour, at={stud_x, stud_z, plate_y} | on={uid, connector} , rot=R24)`
- `move(uid, d_studs, d_plates)`, `rotate(uid, quarter_turns, axis)`
- `remove(uid)`, `recolor(uid, colour)`
- `fill_rect(part, colour, region, layer)`
- `group(uids, submodel_name)`
- `apply(pattern_output)` (mils riser LDraw, roofsnow `SnowDiff`)

Connector-relative placement (`on={uid, connector}`) is the main mode, because it is easier for an LLM to get right than raw coordinates.

**Queries:** `inspect(uid)`, `neighbors(uid)`, `free_connectors(scope)`, `validate(scope)`, `bom(scope)`, `render(views)`.

**Dev only:** `bench.exec(code)`, `bench.sync_from_scene()` → diff for approval.

---

# ADR 0006 — BuildDoc (canonical LDraw + manifest) is the single source of truth

**Status:** proposed · 2026-09-17
**Context:** Three editors touch the same model: the agent in Blender, family members in Studio, and pipeline utilities (mils-integrator, roofsnow). If any editor's native state is treated as the truth, the others drift. Studio drops custom metadata. Blender state can be hand-edited.
**Decision:**
- The canonical artifact is a versioned BuildDoc: normalised MPD plus manifest.
- Blender scenes are rebuilt from it.
- Studio files are written from it and ingested back into it as diffs.
- Identity is recomputed by deterministic matching and never trusted from file metadata.
- Every change is a commit holding intent, diff, report and renders.
**Consequences:**
- Undo, history, concurrency, audit and eval fixtures all come from the diff.
- Ingest has to handle Studio's normalisations; these are learned into a table by the oracle.
- The Blender→core direction exists only in dev mode, as a reviewable diff.

# ADR 0007 — brickcore has no Blender dependency; Blender is an adapter

**Status:** proposed · 2026-09-17
**Context:** Fitment truth has to run where Blender doesn't: CI, Studio ingest on save, a Pi, evals. Blender stays the agent's workspace and renderer, in two modes: James interactively through the official connector, and a headless worker for family requests.
**Decision:**
- All geometry, connectivity, collision, inventory and validation logic lives in `brickcore` (pure Python + numpy).
- `brick_bench` is a thin add-on: scene projection, snapped ops that delegate to brickcore, renders, and optional exact-mesh BVH for disputed collisions.
- The frames conversion exists in exactly one function.
**Consequences:**
- The same report comes out whether a change started in Blender or Studio.
- Blender version and importer choice can change without touching correctness.
- The family path needs a headless Blender only for renders. Validation keeps working if Blender is down.

# ADR 0008 — Integer LDU lattice with the 24-rotation group; connector-relative ops; free-form parts flagged

**Status:** proposed · 2026-09-17
**Context:** LLMs are unreliable with raw float transforms. LEGO fit is discrete. Some legitimate builds (hinges, turntables, flex parts) are not.
**Decision:**
- Agent ops take stud/plate units or a connector reference, and snap to integer LDU and a rotation from R24. Mirror matrices are rejected.
- Every part gets a lattice class (`lattice | offgrid | free`).
- Agents may not create `offgrid` parts. `free` parts need review.
- Tolerances are versioned spec constants with tests.
**Consequences:**
- Geometric drift is impossible through the agent path.
- Angled and technic builds get honest "can't verify" states instead of false passes.
- Human Studio edits can bring in `offgrid` parts; these produce warnings, not rejection.

# ADR 0009 — Fitment = connector graph + voxel collision from open data; unknown is never valid

**Status:** proposed · 2026-09-17
**Context:** Studio's connectivity and collider data are proprietary and EULA-protected. Open sources are the LDraw library (CC BY), the LDCad shadow library (CC BY-SA 4.0, partial coverage) and primitive analysis.
**Decision:**
- Connectors come from shadow snaps, then the primitive scan, then the curated catalog.
- v1 is the stud system only.
- Mates require exact integer coincidence with antiparallel axes.
- Collision uses AABB then surface voxels at 2 LDU on stud-stripped geometry, plus a stud-intrusion test, with BVH arbitration in Blender.
- Stability is advisory.
- Every model reports connector coverage.
- A part with unresolved connectors makes any verdict about it `unknown`. It is never `valid`.
**Consequences:**
- Correctness improves as coverage grows and is measured.
- The CC BY-SA shadow data must stay a separately attributed input: vendor it as data, not code, and check share-alike obligations for any published derivative.
- The primitive→connector table and the voxel rules need spikes S2 and S3 before v1.

# ADR 0010 — Studio is a calibration oracle, not an inline gate

**Status:** proposed · 2026-09-17
**Context:** Studio has no API. Its checks run only in the GUI, only on a Mac that is awake, and it describes its own stability check as conservative. Putting it inline would make every family request slow and fragile.
**Decision:**
- T0 (brickcore) gates every change.
- T1 reads Studio-produced file signals on every ingest.
- T2 runs Studio's checks through computer use on a golden set (scheduled after library or validator changes) and on demand, and keeps an agreement matrix.
- James adjudicates disagreements, and each becomes a regression fixture.
**Consequences:**
- "Studio is ground truth" is kept as a measured agreement rate, not a per-change dependency.
- The oracle readout (screenshot → verdict) is itself validated against the synthetic mutations, whose correct answers are known by construction.

# ADR 0011 — Family use: role-scoped tools, intent contracts, propose→preview→accept, versioned undo, drift telemetry

**Status:** proposed · 2026-09-17
**Context:** Most users can't debug the stack and some are children. Drift has to be caught, explained and reversible without James.
**Decision:**
- The family agent gets only domain ops. No code execution.
- Scope locks are enforced in brickcore (predictability, not restriction).
- The agent declares a `ChangeIntent` before building, and conformance is checked on the diff.
- Ambiguity becomes decision cards.
- Every change is a proposal with renders and child-readable checks; nothing auto-applies.
- Every user works on their own branch; `main` (the physical/ordered state) is dev-merge only. Every commit is undoable.
- **Building is unrestricted for all roles. Only purchase actions are gated** (parent confirms; kids cannot order). "Custom" colours need a parent only at order time.
- The assistant is LEGO-only, discloses it is AI, and runs content filtering and monitoring per Anthropic's guidelines for products serving minors.
- James gets a weekly drift digest and red alerts.
**Consequences:**
- Somewhat slower interactions in exchange for trust.
- Family requests feed the eval suite.
- The drafting table has to render proposals, decisions and history as first-class UI (extends the LEGO-PIPE-007 design work).

---

# LEGO-PIPE-010 — build-harness handoff memo

**From:** Claude (Cowork) · **To:** Claude Code (repo) + ChatGPT (review) · **Date:** 2026-09-17 · **Cluster:** play-well / ojfbot/lego-village-pipeline

## What this is
The design for the harness that turns natural-language requests into validated LEGO builds. The agent works in Blender through a deterministic LEGO layer (`brickcore` + `brick_bench`). The canonical LDraw BuildDoc is the single truth. Family members edit it by hand in Studio. Studio calibrates the validator. It adds family roles, intent contracts and drift telemetry, because most users will be non-developers and children.

## Decisions (ADRs 0006–0011)
6. BuildDoc is the single source of truth; Blender and Studio are projections/editors; identity by deterministic matching.
7. `brickcore` has no `bpy`; Blender is an adapter (interactive + headless worker).
8. Integer LDU lattice, R24 rotations, connector-relative ops; `offgrid`/`free` flagged.
9. Fitment from open data (shadow snaps → primitive scan → catalog), stud system first; unknown connectivity is never valid.
10. Studio is a calibration oracle (T0 gate / T1 file signals / T2 computer-use checks + agreement matrix).
11. Family safety: role-scoped tools, scope and blast-radius limits, ChangeIntent, propose→preview→accept, versioned undo, weekly drift digest, minors safeguards.

*Numbering assumes ADRs are repo-wide after mils-integrator's 0001–0005; renumber if those are package-local.*

## Numbers that must not drift
- Stud pitch 20 LDU · plate 8 · brick 24 · stud height 4 · baseplate 4 · MILS surface 36 LDU.
- ε_snap 0.05 LDU. Mates on exact integer LDU with antiparallel axes. R24, det +1.
- Collision voxel 2 LDU; penetration ≥2 voxels.
- No blast-radius limits. Purchase actions are the only role gate.

## Spikes before implementation (each ends in a short findings note in the project)
- **S1 Studio round trip:**
  - minimum `.io` set Studio 2.26 accepts
  - what Studio normalises on open → save (floats, colour codes, part aliases, step order, submodel names)
  - whether any per-line metadata survives
  - `open` behaviour with Studio already running
- **S2 Connector extraction:**
  - primitive→connector table
  - shadow library coverage on ~10 Winter Village OMR sets + 41843 + 10254
  - target ≥90% of part instances resolved
- **S3 Collision:** surface-voxel rules vs. BVH on the same sets. False-positive rate on known-goods must be 0 after the stud-strip and face-contact rules.
- **S4 Blender adapter:** importer choice (ImportLDraw GPL vs ldr_tools MIT), scale constant, instancing for thousands of parts, headless worker startup time and render time on the Mac.
- **S5 Oracle readout:** can computer use reliably read Studio's connectivity/collision/stability colouring on the synthetic mutations? Accuracy is known by construction.

## Phasing

| Phase | Outcome | Done when |
|---|---|---|
| 1 | brickcore v1 (frames, lattice, stud connectors, graph, collision, inventory, diff, reports) + golden set + CLI | Round-trip idempotence 100%; synthetic mutations 100% detected; 0 `valid` on unknown; runs in CI |
| 2 | brick_bench + domain ops; James-only dev mode through the Blender connector | James builds a MILS module + one Winter Village integration end to end; the `.io` opens clean in Studio (T1 green) |
| 3 | studio-bridge ingest + studio-oracle skill + agreement matrix | ≥95% adjudicated agreement on known-goods; Studio normalisation table populated |
| 4 | Harness API + drafting table proposal flow; parent role first | 20 parent requests accepted with zero post-hoc contradictions; drift digest live |
| 5 | Kid role with minors safeguards | Parent sign-off on the safeguard checklist; purchase gate verified; weekly digest reviewed |

## Asks
- **Claude Code:** scaffold `brickcore/` (reuse mils-integrator `ldraw/parser.py` and `catalog.py`; move shared LDraw code into brickcore instead of forking it) and run spikes S2/S3 in CI against OMR fixtures. Keep `ValidationReport` and `DiffOp` schemas shared with mils-integrator and roofsnow.
- **Claude (Cowork, on the Mac):** run S1, S4 and S5 with Studio, Blender and computer use; write the findings notes.
- **ChatGPT review:** challenge
  - (a) exact-integer mating vs a tolerance band
  - (b) surface-voxel collision on non-watertight LDraw parts
  - (c) whether connector-relative ops cover the Winter Village vocabulary (SNOT, jumpers, half-stud offsets)
  - (d) the branch-per-user model as the sole safety net for unrestricted kid building (what breaks if a kid's branch and `main` diverge for months?)
- **James (answered 2026-09-17):**
  - **Storage:** a directory under `~/Documents` on the Mac for initial development; proper cloud storage later. → Revised same day into a versioned asset library (work/publish split, composition by reference, layers, blob store): see `storage-architecture-asset-versioning.md`, ADR 0012. `~/Documents/play-well/` holds the library clone + blob dir; Docker bind-mounts it.
  - **Blender worker:** headless Blender in Docker on the Mac for dev; containerise properly and push to a cloud instance afterwards. → `brick_bench` must run under `blender -b` with no GPU (Cycles CPU or Workbench for previews). James's interactive Blender stays native `Blender.app` + the official connector; both modes load the same add-on. Watch for Rosetta/arm64 Blender image availability and the bind-mount path rules on macOS Docker.
  - **Studio on family devices:** everyone is free to install Studio on Mac and iPad. → **Caveat: Studio has no iPad build** (Windows/macOS only; the "iPad" options online are remote-desktop services). iPad users get the drafting table (web) with renders, proposals and accept/undo; hand-editing in Studio needs a Mac. Worth deciding whether the family Macs share the `~/Documents` folder over iCloud/LAN now or wait for the cloud store.
  - **Roles:** building is unrestricted for all roles; purchases are the only gate. Adopted above.

## Infrastructure sketch (dev phase) — **superseded by `build-harness/storage-architecture-asset-versioning.md` (ADR 0012)**; kept for the Docker/worker notes only

```
~/Documents/lego-village/            # BuildDoc store (git)
  villages/<name>/model.mpd · manifest.json · exports/<name>.io · renders/
  golden/ · reports/
Docker (Mac): blender-worker image  → bind-mounts ~/Documents/lego-village, runs brick_bench headless, exposes the harness API on the LAN
Native:       Blender.app + Claude Blender connector (James, interactive) · Studio 2.0 (any family Mac) · studio-oracle via computer use
Later:        same image on a cloud instance; store moves to cloud storage; family Macs/iPads reach the drafting table over the web
```

Concurrency in the dev phase: git branches per user avoid iCloud sync conflicts as long as only the Mac's checkout is written by the worker; Studio saves from other Macs come in through a drop folder the bridge ingests, not by writing the repo directly.

## Sources
LDCad Shadow Library (CC BY-SA 4.0): https://github.com/RolandMelkert/LDCadShadowLibrary/ · LDCad shadow library tech: https://www.melkert.net/LDCad/tech/shadowLib · Studio Stability check: https://studiohelp.bricklink.com/hc/en-us/articles/6501498505111-Stability-check · Studio Connectivity check: https://studiohelp.bricklink.com/hc/en-us/articles/6501624386071-Connectivity-check · Studio Collision: https://studiohelp.bricklink.com/hc/en-us/articles/5412820155927-Collision · Anthropic, guidelines for organizations serving minors: https://support.claude.com/en/articles/9307344-responsible-use-of-anthropic-s-models-guidelines-for-organizations-serving-minors · Blender as a Python module: https://docs.blender.org/api/current/info_advanced_blender_as_bpy.html · LDraw legal/licence: https://www.ldraw.org/legal-info · Rebrickable API v3: https://rebrickable.com/api/v3/docs/ · plus sources in briefs 03/04 and the studio-bridge research doc.

---

# Amendments R1 (2026-09-17, from CORR-LEGO-PIPE-013 reconciling LEGO-PIPE-012)

*Appended, never rewritten in place. Where an amendment conflicts with text above, the amendment wins.*

## Requirement J6 (added, operator decision OD-2)
Ordinary child play must run for prolonged stretches on minimal tokens. The family path is mostly deterministic and local: `brick_bench` ops, cached renders, drafting-table UI state and precedent retrieval; the LLM is invoked only to interpret a request and plan. `inspect`, `undo`, `history`, `accept`, `reject` never call a model. The token-intensive subset that operational quotas may gate is named and small: large re-plans, the vision/LLM judge, high-resolution renders. Operational quotas (tokens, runtime, storage, concurrent jobs, retries, credential isolation) protect the household system and spend; they never constrain what may be built.

## ADR 0006 — Amended R1 (R-15)
Identity is a stable, immutable `brick:id` (ULID) per placement; the USD prim path is a mutable namespace address chosen for readability. Placements also carry `asset:id` (defining asset) and `instance:id` (when a referenced asset is instantiated in an assembly). Diff, merge, undo, provenance and Studio round-trip key on `brick:id`; a path change is a rename/reparent op. Duplicate `brick:id` in a composed stage is a blocking validation error. The identity-matching passes in §3.5 remain the fallback for files that lost their IDs (Studio ingest without a manifest).

## ADR 0007 — Amended R1 (R-25 as ruled by OD-1; R-24)
**Agents build in Blender through `brick_bench`, and `brick_bench` is brickcore running inside Blender's Python.** Write path: agent → Blender connector → `brick_bench` domain op → brickcore validates and mutates the BuildDoc → scene re-projected. The scene is never authoritative. Raw `bpy` mutation is dev-only (James) and re-enters as a reviewable diff via `bench.sync_from_scene`. Deployment option (not an architecture change): the family worker may execute the same `brick_bench` ops against a headless projection, or none, when cost (J6) favours it.
Worker boundary: the Blender worker mounts the proposal worktree read-only plus a job-specific output directory; validated commits are performed only by the harness/brickcore service. No BrickLink, GitHub or model-provider credentials in the worker environment.

## ADR 0008 — Amended R1 (R-01)
Exact mates are preserved; the canonical domain is **connector space**, not "every part origin is integer LDU and R24". Rules: connector local frames are canonical data; axis-aligned placements use integer LDU + R24; a mate is exact after canonicalisation (identical canonical position, antiparallel canonical axis); `ε_snap` is used only to recognise and normalise an imported value to a canonical state, never as the mating rule; non-R24 mechanisms use typed transforms (`hinge(angle_token)`, `turntable(detent)`, rational transforms emitted by a supported constraint); arbitrary floats remain `free`. Half-stud (10 LDU) and jumper offsets are exact and lattice-legal.

## ADR 0009 — Amended R1 (R-02, R-03, R-04)
- Collision is three-stage and **brickcore owns the authoritative narrow phase**: (1) AABB/spatial-index broad phase; (2) part-specific or generated collision proxies for deterministic common cases; (3) brickcore-owned triangle/proxy intersection for disputed pairs with explicit contact and allowed-interference rules. Blender BVH is a diagnostic cross-check in S3 only.
- Validity is **scoped per check**: the report is a verdict vector (`lattice`, `collision`, `connectivity`, `inventory`, `intent`, …), each `valid | invalid | unknown(coverage)`. An unresolved connector yields `connectivity: unknown (coverage %)` for the affected parts; it does not erase other valid results. `unknown` is visible, never contagious; a model with any `unknown` cannot be *published* as fully valid, but can be committed on a play branch.
- Connector coverage is reported four ways (placed instances, unique part IDs, connection edges on known-goods, unresolved families by criticality). No coverage figure is asserted before S2.

## ADR 0010 — Amended R1 (C-1, R-07)
Studio is a **compatibility and calibration oracle**, not ground truth for geometry, legality or stability. Adjudicated fixtures plus the project's explicit rules are the truth. The S5 oracle readout must separate "the check ran", "the UI was read correctly" and "Studio agreed with adjudicated truth"; allow `abstain/unreadable`; capture screenshot, action log, Studio version and model hash per verdict; include no-fault and multi-fault controls and repeated runs.

## ADR 0011 — Amended R1 (R-10/OD-2, R-11, R-12, R-22, J6)
- Branches protect authored state. Separate controls protect spend, credentials, personal data, tool scope and purchase actions (operational quotas per J6).
- Intent conformance reports in three bands: **mechanical conformance** (deterministic predicates: scope, op kinds, count range, anchor relation, declared entities/relations), **semantic evidence** (annotations, render comparison, precedent match, judge rationale — advisory), **human acceptance** (the only semantic commit gate).
- Phase 5 gate is the auditable safeguard checklist from LEGO-PIPE-012 R-12 (ages and parent-managed accounts; data minimisation, retention, deletion/export, transcript visibility; no profiling or training on child interactions; input/output moderation with a safe failure experience; report/escalation path; provider/model version, child-safety prompt, evals, incident log; credential isolation and LEGO-only tool allowlist; jurisdiction review incl. COPPA).
- `build.undo(commit_id)` computes and previews a semantic revert against the current head, detects conflicts by `brick:id`, validates, and appends a new commit. History is never rewritten.

## Tool surface — Amended R1 (R-05)
Compositional macros, deterministic, compiling to `DiffOp[]` and passing through brickcore: `wall_run`, `plate_course`, `roof_course`, `repeat_pattern`, `fill_between`, `cap_exposed_studs`, `replace_region`, `place_subassembly`, `mirror_pattern` (where symmetry is legal), and named SNOT/stud-reversal recipes backed by precedents.

## Clarifications R2 (2026-09-17, ChatGPT confirmation of CORR-013 §D.3)

**ADR 0007 — boundary wording (R-25, final).** `brick_bench` *hosts and calls* brickcore inside Blender's Python; it is not itself brickcore (brickcore stays `bpy`-free per ADR 0007). Blender remains the agent workspace and the projection layer, never the authoritative state. Non-rendering family operations (`inspect`, `history`, `accept`, `reject`, `undo`, validation, BOM) call brickcore directly without starting Blender; Blender starts only when geometry projection or rendering is needed. This replaces the R1 sentence "`brick_bench` is brickcore running inside Blender's Python".

**J6 — resource budgets (N-02, final).** Budgets are kept as separate ledgers, never one pooled quota: (a) model tokens/calls; (b) render CPU/GPU time; (c) storage; (d) concurrency; (e) wall-time per job. Ordinary inspect/history/accept/undo operations are deterministic and model-free and draw on none of (a) or (b).
