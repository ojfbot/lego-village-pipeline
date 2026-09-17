---
correspondence_schema: lego-pipe-memo/v1
memo: LEGO-PIPE-011
revision: R2
status: accepted_work_order
memo_type: handoff
title: "From Studio to Stage"
subtitle: "A USD-native asset library, deterministic brick fitment, and a family-safe build loop for the Lego Village Pipeline"
date: 2026-09-17
from: "Claude (Cowork) with James"
to: ["Claude Code (repo)", "ChatGPT (research/review, for confirmation of CORR-013 items)"]
thread: "LEGO Village Pipeline / Studio-to-stage architecture"
reconciled_by: CORR-LEGO-PIPE-013
in_reply_to:
  memo: LEGO-PIPE-012
  revision: R0
cluster: play-well
repos:
  - ojfbot/lego-village-pipeline   # code (exists)
  - ojfbot/play-well-library       # content (to create)
supersedes: HANDOFF-LEGO-PIPE-009-R1
adrs_standing: [0001, 0002, 0003, 0004, 0005]
adrs_proposed: [0006, 0007, 0008, 0009, 0010, 0011, 0012]
spikes: [S1, S2, S3, S4, S5, S6, S7]
review_scale: "P0 blocks work order · P1 fix before affected component · P2 record and schedule"
finding_ids: "R-01…R-26 (LEGO-PIPE-012), C-1…C-6, N-01…N-03 (CORR-013)"
findings:
  - {id: R-15, q: Q12, sev: P0, disposition: accepted, owner: Claude Code, lands: "ADR 0006-R1, 0012-R1"}
  - {id: R-19, q: unasked, sev: P0, disposition: accepted, owner: Claude Code, lands: "ADR 0012-R1, S6"}
  - {id: R-20, q: unasked, sev: P1, disposition: accepted_modified, owner: Claude Code, lands: "memo preflight; this frontmatter"}
  - {id: R-01, q: Q1, sev: P1, disposition: accepted, owner: Claude Code, lands: "ADR 0008-R1"}
  - {id: R-02, q: Q2, sev: P1, disposition: accepted, owner: Claude Code, lands: "ADR 0009-R1, S3"}
  - {id: R-03, q: Q3, sev: P1, disposition: accepted, owner: Claude Code, lands: "S2 exit criteria"}
  - {id: R-04, q: Q3, sev: P1, disposition: accepted, owner: Claude Code, lands: "ADR 0009-R1"}
  - {id: R-05, q: Q4, sev: P1, disposition: accepted, owner: Claude Code, lands: "tool surface R1"}
  - {id: R-06, q: Q5, sev: P2, disposition: accepted, owner: Claude Code, lands: "issue"}
  - {id: R-07, q: Q6, sev: P1, disposition: accepted, owner: Claude (Cowork), lands: "S5 exit criteria"}
  - {id: R-08, q: Q7, sev: P2, disposition: accepted, owner: Claude (Cowork), lands: "S1/S5 scope"}
  - {id: R-09, q: Q8, sev: P1, disposition: accepted, owner: Claude Code, lands: "ADR 0012-R1"}
  - {id: R-10, q: Q8, sev: P1, disposition: accepted_modified, owner: James, lands: "J6; ADR 0011-R1"}
  - {id: R-11, q: Q9, sev: P1, disposition: accepted, owner: Claude Code, lands: "ADR 0011-R1"}
  - {id: R-12, q: Q10, sev: P1, disposition: accepted, owner: James, lands: "phase 5 gate"}
  - {id: R-13, q: Q11, sev: P1, disposition: accepted, owner: Claude Code, lands: "ADR 0012-R1 profile"}
  - {id: R-14, q: Q11, sev: P2, disposition: accepted, owner: Claude Code, lands: "ADR 0012-R1 profile"}
  - {id: R-16, q: Q13, sev: P1, disposition: accepted_modified, owner: Claude Code, lands: "ADR 0012-R1 licensing (per-part)"}
  - {id: R-17, q: Q14, sev: P1, disposition: accepted, owner: Claude Code, lands: "ADR 0012-R1"}
  - {id: R-18, q: Q15, sev: P1, disposition: accepted, owner: all, lands: "spike order R1"}
  - {id: R-21, q: unasked, sev: P1, disposition: accepted, owner: Claude Code, lands: "ADR 0012-R1"}
  - {id: R-22, q: unasked, sev: P1, disposition: accepted, owner: Claude Code, lands: "ADR 0011-R1"}
  - {id: R-23, q: unasked, sev: P2, disposition: accepted, owner: Claude Code, lands: "issue"}
  - {id: R-24, q: unasked, sev: P1, disposition: accepted, owner: Claude Code, lands: "ADR 0007-R1"}
  - {id: R-25, q: unasked, sev: P2, disposition: accepted_modified, owner: James, lands: "ADR 0007-R1 (wording rejected, mechanism adopted)"}
  - {id: R-26, q: unasked, sev: P2, disposition: accepted, owner: Claude (Cowork), lands: "this list"}
  - {id: N-01, q: new, sev: P1, disposition: accepted, owner: James, lands: "correspondence/REGISTER.md"}
  - {id: N-02, q: new, sev: P1, disposition: accepted, owner: Claude Code, lands: "J6; harness API design"}
  - {id: N-03, q: new, sev: P2, disposition: accepted, owner: James, lands: "register rule: attach, don't paste"}
  - {id: C-1, q: disagreement, sev: none, disposition: accepted, owner: Claude Code, lands: "ADR 0010-R1"}
  - {id: C-2, q: disagreement, sev: none, disposition: accepted, owner: Claude Code, lands: "ADR 0012-R1 profile"}
  - {id: C-3, q: disagreement, sev: none, disposition: accepted, owner: Claude Code, lands: "ADR 0008-R1"}
  - {id: C-4, q: disagreement, sev: none, disposition: accepted_modified, owner: James, lands: "J6"}
  - {id: C-5, q: disagreement, sev: none, disposition: accepted, owner: Claude Code, lands: "ADR 0009-R1"}
  - {id: C-6, q: disagreement, sev: none, disposition: accepted, owner: Claude Code, lands: "phase 1 sequencing"}
provenance:
  source_artifacts:
    - {name: "LEGO-PIPE-011-from-studio-to-stage-R1.md", role: "prior revision"}
    - {name: "ChatGPT confirmation of CORR-013 §D.3 (relayed by James, 2026-09-17)", role: "four clarifications; no architectural escalation"}
    - {name: "LEGO-PIPE-012-R0-Review-of-From-Studio-to-Stage.md", role: "review reconciled"}
    - {name: "CORR-LEGO-PIPE-013.md", role: "reconciliation and operator decisions"}
  method: "amendments appended per ADR; no in-place rewrites; operator decisions OD-1..OD-4 applied"
tags:
  - bricklink-studio
  - io-file-format
  - blender-as-workbench
  - claude-blender-connector
  - computer-use
  - ldraw
  - mils
  - brick-fitment
  - connectivity-graph
  - collision-detection
  - calibration-oracle
  - family-safety
  - minors-safeguards
  - drift-detection
  - asset-versioning
  - work-publish-split
  - composition-by-reference
  - openusd
  - semantic-annotation
  - game-studio-pipelines
  - ayon
  - apple-silicon
  - docker
  - stable-identity
  - flatten-manifest
  - usd-profile
  - low-token-family-loop
argument: >-
  In which BrickLink Studio is found to have no door for agents — no API, CLI, script or
  plugin — and its .io files are found to be open zips of LDraw with a legacy password;
  Blender is elected the agents' workbench and Studio demoted to viewer, hand-editor and
  instruction-maker for the family; a deterministic Python layer is specified that snaps every
  brick to an integer lattice and twenty-four rotations, infers stud mates from open snap data,
  detects collisions by voxel, and refuses to call anything valid that it cannot verify; Studio
  is appointed calibration oracle rather than gatekeeper, read only through screenshots and
  synthetic mutations whose answers are known in advance; children are granted unlimited
  freedom to build and none to buy, safety being entrusted to branches rather than limits;
  a folder of files is rejected as too simple and the practices of game and VFX studios —
  the work/publish split, immutable versions, composition by reference, layers as opinions —
  are borrowed instead; OpenUSD is chosen as the canonical scene and annotation format from
  the first day, with LDraw kept as leaf geometry, and a rumoured Apple Silicon incompatibility
  is dispelled and reduced to an arm64-Linux container question; fifteen review questions are
  posed, seven spikes are named, and a protocol for reconciling review into a work order is
  agreed; and, in this revision, the review's twenty-six findings are folded in — identity
  becomes a GUID and the prim path a mere address, flattened Studio files come back as
  overlays with a manifest rather than guesses, the lattice rule moves to connector space,
  the USD profile is narrowed, licences are read per part, children keep unlimited building
  under bounded compute, and the spikes are re-ordered so the irreversible decisions retire
  first.
parts:
  E: "Amendments R1 — appended to Parts C and D; change log in §0a"
  A: "Cover memo — orientation, decisions, review questions, asks, spikes, glossary, reconciliation protocol"
  B: "studio-bridge/research-bricklink-studio-agent-integration.md — in which Studio's install is inspected and its surfaces ranked"
  C: "build-harness/architecture-adrs-and-LEGO-PIPE-010.md — in which the harness, ADRs 0006–0011 and the family roles are set down"
  D: "build-harness/storage-architecture-asset-versioning.md — in which the asset library is modelled on studio pipelines and ADR 0012 elects OpenUSD"
---

# LEGO-PIPE-011 — From Studio to Stage
### A USD-native asset library, deterministic brick fitment, and a family-safe build loop for the Lego Village Pipeline
*R2, accepted work order (cleared by ChatGPT for the limited scope) · 2026-09-17 · play-well cluster · reconciled by CORR-LEGO-PIPE-013 from LEGO-PIPE-012 · supersedes/extends HANDOFF-LEGO-PIPE-009-R1 (mils-integrator); ADRs 0001–0005 remain in force*

**From:** Claude (Cowork) with James · **To:** Claude Code (repo, work order) · ChatGPT (confirmation of CORR-013 §D.3)
**Repos:** `ojfbot/lego-village-pipeline` (code, exists), `ojfbot/play-well-library` (content, to create)

## 0a. Change log

### R1 → R2 (clarifications only; ChatGPT confirmation of CORR-013 §D.3)

| Change | Source |
|---|---|
| ADR 0007: `brick_bench` *hosts and calls* brickcore; it is not itself brickcore. Non-rendering family ops call brickcore without starting Blender; Blender starts only for projection/rendering | R-25 final |
| ADR 0012: licence fields per part — raw header, normalised id, source library version, part hash; missing/ambiguous fails closed for distribution; OMR model licences tracked separately | R-16 final |
| J6: five separate budget ledgers (model tokens/calls · render CPU/GPU · storage · concurrency · wall-time); inspect/history/accept/undo draw on none of the first two | N-02 final |
| Preflight run against this exact artifact (YAML + schema + ID declaration + register uniqueness); result recorded in §10 | R-20/N-03 final |
| `findings:` now also declares C-1…C-6 | preflight rule 5 |

### R0 → R1

| Change | Source |
|---|---|
| Frontmatter conforms to `lego-pipe-memo/v1`; structured `findings:` list added | R-20, R-26 |
| **Requirement J6 added:** ordinary child play must be low-token for long stretches; only a named small subset of actions is token-gated | OD-2 (R-10) |
| ADR 0006/0012: `brick:id` (ULID) is identity; prim path is namespace; `asset:id`, `instance:id`, export-occurrence identity | R-15 (P0) |
| ADR 0012: flattened Studio ingest authors assembly-local overlays by default; sidecar export manifest; explicit edit scope for source promotion | R-19 (P0) |
| ADR 0007: **agents build in Blender through `brick_bench` = brickcore inside Blender; scene never authoritative; raw `bpy` dev-only** (wording of R-25 rejected by operator; mechanism adopted); worker boundary narrowed | OD-1, R-24 |
| ADR 0008: canonical domain is connector space; `ε_snap` normalises only; typed transforms for hinges/turntables | R-01 |
| ADR 0009: brickcore owns the collision narrow phase; verdict vector with per-check `unknown(coverage)`; coverage reported four ways | R-02, R-03, R-04 |
| ADR 0010: Studio is a compatibility/calibration oracle, not ground truth; S5 readout separates UI failure from verdict | C-1, R-07 |
| ADR 0011: three-band intent report; auditable minors checklist; undo = previewed semantic revert; operational quotas separate from creative scope | R-11, R-12, R-22, R-10 |
| ADR 0012: LVP USD profile; physical/derived/presentation layers; content-addressed drafts, serialized allocator, no `@latest` persisted; branch baseline lock; worktree per branch; per-part LDraw licences; merge driver deferred | R-13, R-14, R-17, R-09, R-21, R-16, C-6 |
| Tool surface: compositional macros compiling to `DiffOp[]` | R-05 |
| Spikes re-ordered: contracts → S7 ∥ S1 ∥ S2 → thin vertical harness → S6 → S3 → S4 → S5; exit criteria rewritten for S2, S5, S6 | R-18, R-03, R-07, R-19 |
| Claude Code work order narrowed to contracts + S7/S1/S2 + memo preflight + register until spikes report | R-18, N-01, N-03 |
| Memo register instituted; this package's predecessor is HANDOFF-LEGO-PIPE-009-R1 (was cited as LEGO-PIPE-009-R1, colliding with CORR-LEGO-PIPE-009) | N-01 |
| Part C §6.3 line "Blast radius: kid 60 / parent 500" already withdrawn in R0; §1.3 inconsistency list now also covers Amendments R1 precedence | — |

Amendments are appended to Parts C and D as "Amendments R1" blocks; where they conflict with earlier text, the amendment wins.

## Orientation — read this first

### What the project is
James is building a multi-year LEGO Christmas village: the Winter Holiday Train (10254) running around the family's LEGO Christmas tree (41843), on snowy 32×32 MILS modular bases, expanding year over year with official Winter Village buildings, bridges and elevated track. Alongside the physical build he is building the **Lego Village Pipeline**: an AI-agent pipeline that goes from natural language ("add a bakery next to the station, with snow on the roof") to a validated digital model, to a BrickLink parts order. It lives in `ojfbot/lego-village-pipeline` in the **play-well** cluster of James's @ojfbot fleet (Frame experience plane, Northstar metadata, ADR-driven). You have been the research/review counterpart via numbered **LEGO-PIPE-###** handoff memos; Claude Code maintains the repo; Claude (Cowork, this author) does design and on-Mac work.

### Where we were: LEGO-PIPE-009-R1 (2026-09-16)
The last memo delivered **mils-integrator**: a utility that takes an official set as LDraw (from the LDraw Official Model Repository), analyses its stud-grid footprint, and produces *questions for the builder with precedents attached* (decision points), then validated plans for integrating the set onto a MILS module, with a riser exported as LDraw. Its principles (ADRs 0001–0005): executable spec + a tuned RAG harness with evals rather than a generative brick model; SQLite + content-addressed blobs; stud-grid analysis, not meshes; an eleven-pattern taxonomy with cited evidence; and **the agent asks, it does not guess**. A second utility, **roofsnow** (procedural snow on roof lines as a reviewable per-part diff), uses the same "precedent-study pattern". A family-facing **drafting table** UI is in design (LEGO-PIPE-007).

### What happened today (2026-09-17), in order
1. **Studio integration research.** James installed BrickLink Studio on his Mac and asked how agents (Claude Cowork/Code, OpenCode, the pipeline services) could drive it, ideally like the official Blender↔Claude connector. Answer, verified against his install: Studio is a Unity/Mono app with **no API, CLI, scripting, AppleScript or plugin surface**, and its EULA bars reverse engineering and injection. Its `.io` file is an open zip (older files password `soho0909`) with LDraw inside, and it ships readable part/colour mapping tables. So: integrate **file-first**, use GUI automation (computer use) only for GUI-only actions, render in Blender.
2. **Pivot to Blender as the agent workbench.** James is a long-time Blender user, not a Studio user. Agents will build in Blender programmatically; Studio becomes the viewer/hand-editor/instruction-maker for the family (spouse and kids), who aren't Blender users.
3. **The harness.** James asked for a deterministic Python layer that checks every piece against origin and every other piece "LEGO-style", exports LDraw the way Studio wants it, and uses **Studio as ground-truth validator**, while being safe in the hands of non-developers and children who can't spot drift. Result: the build-harness architecture, ADRs 0006–0011.
4. **Decisions James made:** building is unrestricted for every role and only *purchasing* is gated (safety comes from branch-per-user versioning, not limits); dev storage under `~/Documents`; headless Blender in Docker on the Mac now, cloud later; family free to install Studio on Mac (no iPad build exists).
5. **Storage redesign.** James pushed back that a folder of files was too simple and asked how game/VFX studios version composed asset hierarchies. Result: ADR 0012, a work/publish asset library modelled on OpenUSD composition and AYON's product/version/representation vocabulary.
6. **OpenUSD-native.** James chose to make OpenUSD the canonical composition/annotation format from the start, as a learning entrypoint and for the "rich annotation" ambition, with LDraw as leaf geometry and Studio interchange, plus guardrails. `usd-core` runs natively on Apple Silicon; the only gap is arm64 Linux containers.

### What you're being asked now
Review the whole design (Parts B–D) against the 15 numbered questions in §2, with severities, and add anything we didn't ask. After James and Claude reconcile your findings, the memo becomes R1 and goes to Claude Code as the work order. Nothing has been implemented yet; spikes S1–S7 come before scaffolding.

### Terms you'll meet (one line each)
**BrickLink Studio** — LEGO's free CAD app (Windows/macOS), `.io` files, Eyesight renderer, stability/collision/connectivity checks, Instruction Maker, wanted-list export. **LDraw** — the open text format for LEGO models (−Y up, 20 LDU per stud, 8 per plate, 24 per brick); the OMR is its repository of official sets (CC BY 4.0). **LDCad shadow library** — community stud/anti-stud "snap" metadata for LDraw parts (CC BY-SA 4.0, partial coverage). **MILS** — the modular baseplate standard (surface = baseplate + 4 plates, Technic pin holes at fixed positions). **Claude Blender connector** — official MCP: an add-on inside Blender exposes a local server; Claude runs Python in the live scene. **Computer use** — Claude driving macOS apps by screenshots, menus and clicks; our only handle on Studio's GUI. **OpenUSD** — Pixar's scene-description format/runtime: layers, references, variants, `kind`, instancing; text form `.usda`. **AYON** — an open-source VFX pipeline manager whose publish vocabulary (product/version/representation/hero) we borrow. **brickcore / brick_bench / studio-bridge / studio-oracle** — the four components defined in Part C. **T0/T1/T2, DiffOp, DecisionPoint, `lvp://`** — see the glossary in §7.

## 0. How to use this package

This is one file in four parts so it can be pasted whole into a review session:

- **Part A — this cover memo:** the decisions, the numbered review questions, the asks, the spikes, open items, glossary, and the reconciliation protocol.
- **Part B — `studio-bridge/research-bricklink-studio-agent-integration.md`:** what BrickLink Studio can and cannot do for agents, verified against James's install.
- **Part C — `build-harness/architecture-adrs-and-LEGO-PIPE-010.md`:** the harness architecture, ADRs 0006–0011, and the original LEGO-PIPE-010 memo.
- **Part D — `build-harness/storage-architecture-asset-versioning.md`:** versioned asset library, ADR 0012 (OpenUSD-native).

Where B–D disagree with A, **A wins** (it reflects later decisions); the discrepancies are listed in §1.3 so the reviewer doesn't have to hunt for them.

## 1. Decisions, in order

### 1.1 Standing (from LEGO-PIPE-009-R1)
ADR 0001 corpus → executable spec + RAG harness, no fine-tune · 0002 SQLite + content-addressed blobs · 0003 stud-grid footprint analysis, not meshes · 0004 eleven-pattern taxonomy with evidence · 0005 decision points are first-class; the agent asks, it does not guess.

### 1.2 New in this package (all 2026-09-17)

| # | Decision | Where |
|---|---|---|
| — | Studio has no API/CLI/plugin surface; EULA §4 bars injection or decompilation. Integrate file-first (`.io`/LDraw), use computer use only for GUI-only actions, render in Blender/LeoCAD | Part B |
| 0006 | Canonical BuildDoc is the single source of truth; Blender and Studio are projections/editors; identity by deterministic matching | Part C |
| 0007 | `brickcore` has no Blender dependency (now also: no `pxr` in validators); Blender is an adapter with interactive + headless modes | Part C, amended by D |
| 0008 | Integer-LDU lattice, R24 rotation group, connector-relative ops; `offgrid`/`free` parts flagged, never silently valid | Part C |
| 0009 | Fitment from open data only (LDCad shadow snaps → primitive scan → curated catalog); stud system first; unknown connectivity is never valid | Part C |
| 0010 | Studio is a **calibration oracle** (T0 gate / T1 file signals / T2 computer-use checks + agreement matrix), never an inline gate | Part C |
| 0011 | Family use: role-scoped tools, intent contracts, propose→preview→accept, versioned undo, drift telemetry, minors safeguards | Part C |
| J1 | **Building is unrestricted for every role; purchase actions are the only gate.** Safety comes from branch-per-user + `main` = physical state (dev-merge only). No blast-radius limits | Part C §6.3 |
| J2 | Dev storage under `~/Documents/play-well/`; cloud storage later | Part D §3.6 |
| J3 | Headless Blender in Docker on the Mac for dev; containerize and push to a cloud instance later. James's interactive Blender stays native with the official Claude Blender connector | Part C, D |
| J4 | Family may install Studio on any Mac. **Studio has no iPad build**; iPad users get the drafting table only | Part C asks |
| 0012 | Versioned asset library: two repos (code / content), work→publish split, immutable versions, composition by reference at pinned versions, layers as `DiffOp` products, `lvp://` URIs + resolver, branch flow `play/<user>` → `staging` → `main`, uid-aware merge driver instead of file locking | Part D |
| 0012 §5 | **OpenUSD-native from the start** (`.usda` canonical; LDraw = leaf geometry + Studio interchange). Five guardrails (§5.1). Own-JSON schema kept as fallback if S7 fails | Part D |
| J5 | `usd-core` runs natively on Apple Silicon (universal2 wheel). The only gap is arm64 *Linux* (Docker on the Mac). Dev plan: brickcore native, Blender in Docker; S7 proves an arm64 container via community wheels or source build for the cloud move | this memo |

### 1.3 Known inconsistencies between parts (reviewer: don't flag these)
- Part C's "Infrastructure sketch" is superseded by Part D (it says so inline). Keep only its Docker/worker notes.
- Part C uses `uid` for placement identity; under 0012 §5 the uid **is the USD prim path**. `manifest.json` per published model becomes prim metadata/`customData` where practical; keep a sidecar only for what USD can't hold cheaply (validation reports, blob hashes).
- Part C's `ValidationReport`/`DiffOp` schemas stay; Part D's `assembly.json` is replaced by `assembly.usda`.
- Part C says "brickcore pure Python + numpy"; Part D confines `pxr` to `brickcore.io.usd`. Both true.

## 2. Review questions for ChatGPT

Numbered Q1–Q15. Grade each finding **P0** = blocks the work order · **P1** = fix before the affected component is built · **P2** = record and schedule (the same scale as the LEGO-PIPE-007 design-bundle review). Give each finding an ID `R-nn`, so the reconciliation ledger in §8 can carry it alongside Claude's own findings.

**Fitment & geometry**
1. Exact-integer coincidence for stud mates (0008/0009) vs. a tolerance band: what legitimate builds break under exact matching (jumper/half-stud offsets, SNOT with plates-on-side, hinge-locked angles)? Propose the smallest rule that keeps determinism.
2. Surface-voxel collision (2 LDU, penetration ≥2 voxels) on non-watertight LDraw parts: expected false-positive/negative classes; is BVH-in-Blender arbitration sufficient, or should brickcore own an exact test?
3. Connector coverage: with LDCad shadow snaps + primitive scan, what fraction of Winter Village part instances do you expect to resolve? Which part families will be `connectivity_unknown` and therefore block `valid`?
4. Does connector-relative placement (`on={uid, connector}`) cover the Winter Village vocabulary well enough for an LLM agent, or do we need higher-level ops (wall run, roof course, stud-reversal bracket)?
5. Advisory stability: is a per-component centre-of-mass/overhang heuristic worth shipping, or go straight to a LegoGPT-style force-equilibrium LP as optional v2?

**Studio as oracle**
6. Reading Studio's connectivity/collision/stability colouring from screenshots (S5): failure modes, and whether the synthetic-mutation design (answers known by construction) is enough to certify the readout.
7. Any surface on Studio we missed? (We found: no CLI, no AppleScript, no URL scheme, native NSMenu + NSOpenPanel bundles, Launcher.app owns the `com.bricklink.io` UTI, Mono DLLs present but EULA-barred.)

**Family safety (J1)**
8. Branch-per-user as the sole safety net for unrestricted building: what breaks when a kid's `play/` branch and `main` diverge for months (asset versions pinned vs `@latest`, part-library drift, merge-driver semantics on renames/submodel splits)?
9. Intent-contract conformance (scope, allowed ops, count range, anchor relation) — is this checkable enough to catch semantic drift, or is the vision judge doing the real work?
10. Minors safeguards: is the LEGO-only tool surface + AI disclosure + monitoring adequate for a family app on the Anthropic API, and what would a reviewer expect to see documented?

**Storage & USD (0012)**
11. USD-native from day one for a one-family project: where does the composition model (LIVRPS) bite a small team? Is "base + snow + lighting + validator sublayers" shallow enough to avoid opinion-strength surprises?
12. Prim path as identity: how do renames/moves between submodels and the merge driver interact? Should placements carry a stable `brick:id` GUID in addition to path?
13. Part-USD cache generated from LDraw (instanceable): licence implications (LDraw CC BY; LDCad shadow CC BY-SA 4.0 as data) for a private library vs. any future publication.
14. Work/publish with `@latest` in play branches: race conditions with the catalog's version allocation on branches (`v004-play-eli` scheme) — better alternatives?

**Process**
15. Ordering of spikes S1–S7 and which should be run before scaffolding anything.

## 3. Asks

**ChatGPT:** LEGO-PIPE-012 answered §2; CORR-LEGO-PIPE-013 disposes it. Three items are returned for confirmation (CORR-013 §D.3: R-25 mechanism, R-16 per-part rule, R-20 severity). No further review round is required before spikes start.

**Claude Code (this work order):**
- **Stage 0 contracts** as typed schemas with validators in `ojfbot/lego-village-pipeline`: `BrickId/AssetId/InstanceId`, `VerdictVector`, `ConnectorFrame` + canonical transform, `ExportManifest`, `DiffOp` (shared with mils-integrator/roofsnow), `ValidationReport` (three-band intent fields). Surface every ambiguity as a question; James reviews before anything else is built.
- **Memo preflight**: `lego-pipe-memo/v1` JSON Schema + a CLI that parses frontmatter, checks required keys/types, `(memo, revision)` uniqueness against `correspondence/REGISTER.md`, `in_reply_to`/`supersedes` resolution, and that every `R-`/`N-`/`C-` ID in the body is declared.
- **Register**: create `correspondence/REGISTER.md` from the list in §9 and wire the preflight to it.
- Authorized scope after ChatGPT clearance (2026-09-17): **contracts, register/preflight infrastructure, and spikes S1, S2, S7.** Nothing else.
- **S2** in CI against OMR fixtures (coverage four ways; connector schema from real data). **S7** container half (arm64 image build). Findings notes back to the project.
- Scaffold `brickcore/` only to the extent S2/S7 need: reuse mils-integrator's `ldraw/parser.py` + `catalog.py` (moved, not forked). Package boundaries beyond that wait for S1/S2/S7 reports.
- Register both repos in Northstar under play-well; create `ojfbot/play-well-library` empty with the attribution file and branch-flow CI rule only.

**Claude (Cowork, on the Mac):** S1, S7 (native half), then S6, S4, S5 in the R1 order.

## 4. Spikes — order R1 (by irreversible decision; each ends in a findings note in the project)

**Stage 0 — data contracts first** (no scaffolding of production package boundaries before these are written down): identity (`brick:id`, `asset:id`, `instance:id`), verdict vector with `unknown(coverage)`, connector-space canonical transform, export manifest schema, `lego-pipe-memo/v1` preflight.

| Order | Spike | Question | Done when |
|---|---|---|---|
| 1 ∥ | **S7** `pxr` runtime matrix | `usd-core` native on macOS (universal2); arm64 Linux container via community wheel or source build; Blender imports the composed stage | Both environments load the same stage; decision recorded: native arm64 vs emulated fallback |
| 1 ∥ | **S1** Studio round trip | Minimum `.io` entry set Studio 2.26 accepts; open→save normalisations; does any metadata survive; `open` behaviour with Studio running; passive surfaces (logs, autosave, error files) | Normalisation table; writer produces files Studio opens clean; passive-surface inventory (R-08) |
| 1 ∥ | **S2** Connector extraction | Primitive→connector table; shadow-lib coverage on ~10 Winter Village OMR sets + 41843 + 10254 | Coverage reported four ways (instances, unique parts, connection edges on known-goods, unresolved families by criticality); connector schema defined against real fixtures. **No target asserted in advance** (R-03) |
| 2 | Thin vertical harness | One request → `brick_bench` op → brickcore verdict vector → flatten → `.io` | Exists; disposable |
| 3 | **S6** Composition round trip (USD profile) | Two published buildings + riser + snow layer + season variant → module → flatten with manifest → Studio → hand edit → ingest | Passes when provenance is preserved and ambiguous source mutation is **refused** (overlay by default; DecisionPoint on ambiguity). Automatic source attribution is not required (R-19) |
| 4 | **S3** Collision | Voxel vs proxy vs brickcore exact vs Blender BVH on the same sets, after connector/contact exceptions exist | 0 false positives on known-goods; brickcore narrow phase is authoritative; BVH diagnostic only (R-02) |
| 5 | **S4** Blender adapter | Importer choice, scale constant, instancing at thousands of parts, headless startup + render time, worker boundary | Frames round trip exact on lattice points; numbers recorded; worker runs read-only worktree + output dir |
| 6 | **S5** Oracle readout | Computer use reads Studio's check colouring on synthetic mutations | Deterministic Studio setup; single/multi/no-fault controls; repeated runs; per-verdict screenshot + action log + version + model hash; `abstain` allowed; three separate scores (check ran / UI read correctly / Studio agreed with adjudicated truth) (R-07) |

## 5. Numbers that must not drift
Stud 20 LDU · plate 8 · brick 24 · stud height 4 · baseplate 4 · MILS surface 36 LDU · ε_snap 0.05 LDU · mates on exact integer LDU, antiparallel axes · R24, det +1 · collision voxel 2 LDU, penetration ≥2 voxels · MILS constants per LEGO-PIPE-009-R1 (Technic 1×4 at studs 3–6 and 27–30, holes at 70/90/110/530/550/570 LDU, road 5 plates, rail top 9 plates).

## 6. Open items / unverified
- Studio 2.26 minimum `.io` entry set (S1). — `open -a Launcher.app` with a running instance (S1).
- Studio accessibility tree depth beyond native menus/dialogs (S5).
- macOS user-data paths for Studio (CustomParts, prefs) — likely `~/Library/Application Support/Stud.io`, unverified.
- `brick-mcp` licence (unstated) — ask or reimplement the `.io` writer.
- `ExportLDraw` on Blender 4.x/5.x; is `ldr_tools_blender` import-only.
- Blender arm64 Docker image availability and CPU render times (S4).
- Whether Studio's tables (`StudioPartDefinition2.txt`, `StudioColorDefinition.txt`) may be read at runtime for a private tool — assumed yes; never shipped.

## 9. Memo register (instituted R1, finding N-01)

Single monotonic register across threads and providers; type prefixes `HANDOFF-`, `CORR-`, `REVIEW-`. Historical collisions are kept and disambiguated by prefix. Transfer between providers is by file attachment; the receiver runs the `lego-pipe-memo/v1` preflight before reading.

| Number | Document | Type | Thread | Status |
|---|---|---|---|---|
| 007-R2 | Design brief / design bundle | HANDOFF | design | issued |
| 008 | ChatGPT reconciliation memo on the design bundle | CORR | design | issued |
| 009 | Claude reconciliation response (`design-review/CORR-LEGO-PIPE-009-…`) | CORR | design | issued |
| 009-R1 | mils-integrator handoff (`mils-integrator/architecture-adrs-and-LEGO-PIPE-009.md`) | HANDOFF | build-harness | issued — **collides with CORR-009; cite as HANDOFF-LEGO-PIPE-009-R1** |
| 010 | build-harness memo (inside Part C) | HANDOFF | build-harness | issued — the design thread's planned "HANDOFF-010" must take the next free number |
| 011-R0 / R1 | From Studio to Stage (this document) | HANDOFF | build-harness | R1 accepted |
| 012-R0 | ChatGPT review of 011 | REVIEW | build-harness | issued |
| 013 | Claude reconciliation of 012 | CORR | build-harness | issued |
| 014 | *next free* — reserved for the design thread's focused redesign brief | HANDOFF | design | reserved |

## 10. Preflight record (R-20 / N-03)

Run on the exact assembled artifact `LEGO-PIPE-011-from-studio-to-stage-R2.md` with the reference `preflight.py` (YAML parse; required keys and types; schema id; status/memo_type enums; every `R-`/`N-`/`C-` ID used in the body declared in `findings:`; `in_reply_to`/`supersedes` resolvable in `correspondence/REGISTER.md`; no tabs or duplicate top-level keys). **Result: PASS** — 26 top-level keys, 35 declared findings, 30 IDs used in body, 0 errors, 0 warnings. `CORR-LEGO-PIPE-013` also passes once the schema admits `to:` as an `{actor, role}` mapping (CORR-009 house style) as well as a list; that allowance is recorded in the register. Claude Code's first deliverable replaces this reference script with the versioned JSON Schema and CLI.

## 7. Glossary
**BuildDoc** — the canonical, versioned scene (now: a USD stage rooted at an assembly, LDraw leaves). **Component / assembly / layer** — USD-style kinds: building, module/layout, non-destructive diff product. **Product / version / representation** — AYON-style publish vocabulary. **`lvp://`** — asset URI resolved by brickcore. **T0/T1/T2** — validator tiers (core gate / Studio file signals / Studio oracle). **DiffOp** — add/remove/move/recolor per placement; shared with roofsnow's `SnowDiff` and the drafting table's `ThemeDiffRow`. **DecisionPoint** — a fork raised to the human with precedents (ADR 0005). **`main` / `staging` / `play/<user>`** — physical state / next order / personal worksite. **Studio** — BrickLink Studio 2.26.8 (macOS), file-first integration only.

## 8. Reconciliation protocol
1. ChatGPT returns findings keyed to §2 numbers with P0/P1/P2 severities and `R-nn` IDs.
2. James and Claude merge them into a reconciliation ledger of the same shape as the design-bundle review — `ID · finding · sev · ChatGPT · Claude · reconciled sev · owner · disposition` — under the rule that a finding either reviewer raises stays in unless the other actively refutes it; agreement raises confidence, not severity. Accepted P0/P1 items become amendments appended to the relevant ADR ("Amended R1 — …"), never silent rewrites.
3. Memo bumps to LEGO-PIPE-011-R1 with a change log at the top; Parts B–D are re-emitted with amendments inline.
4. R1 goes to Claude Code with the §3 asks as the work order; Claude Code opens one issue per open item in §6.

---


# PART B — studio-bridge/research-bricklink-studio-agent-integration.md
*In which James's Studio 2.26.8 install is inspected read-only; the .io container is unzipped by era; Eyesight is found to be a 2017-vintage Cycles; the EULA closes the injection route; existing MCPs for .io, LDraw rendering and Rebrickable are catalogued; and a file-first `studio-bridge` with computer-use playbooks is proposed.*

# studio-bridge — research: giving agents access to BrickLink Studio

**Date:** 2026-09-17 · **Cluster:** play-well / ojfbot/lego-village-pipeline · **Status:** research, pre-ADR
**Question:** What already exists, and what surfaces can we build on, so Claude (Cowork/Code), OpenCode, and the pipeline services (mils-integrator, roofsnow, drafting table) can work with BrickLink Studio instances, apps and file formats — ideally as a Blender-connector-style MCP/plugin?

## 1. Bottom line

- **A Blender-style connector for Studio isn't possible the same way.** The Blender connector works because Blender embeds Python: an add-on inside Blender runs a socket server (`localhost:9876`), and a small stdio MCP bridge packaged as a Desktop Extension talks to it. Studio has nothing like that. It is a Unity/Mono C# app with no scripting runtime, no plugin API, no CLI, no AppleScript dictionary and no URL scheme. Its EULA (§4) forbids reverse engineering, modifying, or "separating STUDIO into its component parts", so injecting a server into Studio (BepInEx/Harmony) is out.
- **The workable design is file-first.** Build a local `studio-bridge` MCP that reads and writes `.io` files and uses Studio's own install-side mapping tables at runtime. It hands rendering to Blender (official connector plus an `.io`/LDraw importer) or the LeoCAD CLI, and leaves the few GUI-only actions (instructions, Eyesight render, stability check, BrickLink upload) to **computer use**, packaged as a skill. Studio stays the human's editor. Agents write the files it opens.
- **Reusable prior art exists:** `datakurre/brick-mcp` (.io/.ldr editing MCP), `musharna/ldraw-mcp` (headless Blender renders for vision), `ldr_tools_blender` (imports `.io` directly), `bricks-mcp` (Rebrickable), and Brick Directory (a hosted MCP that aggregates BrickLink prices, Rebrickable and Brickset).

## 2. Verified on James's install (read-only inspection, `/Applications/Studio 2.0`)

| Fact | Evidence |
|---|---|
| Version **2.26.8_1** (All-In-One 2.0.1.0), bundle id `com.BrickLink.Studio` | `version.txt`, `Studio.app/Contents/Info.plist` |
| Unity player on **Mono** (not IL2CPP): `Data/Managed/BrickLink.Studio.*.dll` (BrickLinkAPI, LEGOAPI, Connectivity.Runtime, UI, Common.Runtime) | app bundle |
| `Studio.app` declares **no** document types or URL schemes. `bin/Launcher.app` (`com.bricklink.StudioLauncher`) is the handler for UTI `com.bricklink.io` | plists |
| Native macOS plugins `MenuBar.bundle` and `StandaloneFileBrowser.bundle` → real NSMenu menu bar and NSOpenPanel/NSSavePanel dialogs. Computer use can drive these more reliably than Unity-drawn UI | `Contents/PlugIns` |
| Eyesight renderer: `PhotoRealisticRenderer/mac/eyesight(.app)`, `settings.xml` (`<eyesight version="2.22">`, Cycles-style integrator params), HDRs, ffmpeg libs | folder |
| Bundled LDraw library `ldraw/{parts,p,LEGO,UnOfficial}`, `LDConfig.ldr`, `ldraw/version.txt` = 238 | folder |
| **Proprietary connectivity data:** `ldraw/connectivity/*.conn` (9,198 binary files) + `ldraw/collider/*.col` | folder. Do not redistribute or decode |
| **Mapping tables (tab-separated, human-readable):** `data/StudioPartDefinition2.txt` columns: `Studio ItemNo, BaseStudioItemNo, BL ItemNo, BL ItemKey, LDraw ItemNo, LDD ItemNo, Description, …, IsAssembly?, flexible type, IsDecorated`. `data/StudioColorDefinition.txt` columns: `Studio Color Code, BL Color Code, LDraw Color Code, LDD color code, names…, RGB, Alpha, CategoryName, …, Ins_RGB, Ins_CMYK`. Also `ldraw.xml` (LDraw↔LEGO material), `ldraw_lxfml_mapping.json`, `designid.xml`, `elementInfoList.json`, `LEGOSetList.tsv` | `data/` |

### `.io` container, by era (checked by unzipping bundled samples)

| Era | Encryption | Entries |
|---|---|---|
| Legacy (`.info` version `16.11.1.5`, `1.0.0_13`) | ZipCrypto, password `soho0909` | `model.ldr`, `model2.ldr`, `thumbnail.png`, `errorPartList.err`, `.info` |
| Current (`.info` `{"version":"2.25.11_3","total_parts":186,"parts_db_version":200}`) | **none** | `model.ldr`, `modelv2.ldr`, `model2.ldr`, `model.lxfml`, `model.ins`, `thumbnail.png`, `errorPartList.err`, `.info` |

- `model.ldr` is a normal LDraw MPD using **LDraw colour codes** (e.g. 14 = Yellow, 15 = White). It adds Studio meta lines: `0 CustomBrick`, `0 FlexibleBrickControlPointUnitLength`, `0 FlexibleBrickLockedControlPoint`, `0 NumOfBricks:`, `0 NOFILE`, `0 STEP`.
- `model2.ldr` uses **Studio/BrickLink colour codes** (Yellow = 3, White = 1) and embeds part geometry and BrickLink metadata (`0 BL_Item_No`, `0 BL_Item_Key`, `0 BL_CategoryIndex`, `0 FlexibleType`, `0 RenderAngleOffset`, `0 IsSubModel`).
- `model.ins` is the Instruction Maker layout as XML (`<Instruction><GlobalSetting><PageSetup>…`). `model.lxfml` is LXFML v7 written by "LDraw Converter".
- Readers should try no password first, then `soho0909`. Writers should target the current layout. **Unverified:** the minimum entry set Studio accepts from a third-party writer. `brick-mcp` already writes `.io` that it says opens in Studio, so use it as the reference.

## 3. What already exists (reuse / adapt)

| Project | What it gives us | Notes |
|---|---|---|
| [datakurre/brick-mcp](https://github.com/datakurre/brick-mcp) | MCP (FastMCP) to create, open or save `.io`/`.ldr`/`.mpd`; list parts, BOM, steps; add, move, rotate, recolour parts; parts search | Closest to "Studio file MCP". Python ≥3.14, pyzipper. No collision or validity checks. Licence not stated, so **ask before forking**. Small (9 commits) |
| [musharna/ldraw-mcp](https://github.com/musharna/ldraw-mcp) (`pip install ldraw-mcp`) | `render_ldraw_file`, `render_ldraw_text`, `check_renderer`: headless Blender + ImportLDraw, Cycles CPU, multi-azimuth stitched PNG | MIT, v0.1.1 (Jul 2026). Gives agents "eyes" on a build. LDraw only, so feed it `model.ldr` pulled from the `.io` |
| [ScanMountGoat/ldr_tools_blender](https://github.com/ScanMountGoat/ldr_tools_blender) | Blender 4.1+ importer for LDR/MPD **and current `.io`**. Instancing by part+colour, Geometry Nodes for >10k parts | MIT. Rust core `ldr_tools`. Pairs with the official Blender connector |
| [TobyLobster/ImportLDraw](https://github.com/TobyLobster/ImportLDraw), [cuddlyogre/ExportLDraw](https://github.com/cuddlyogre/ExportLDraw) | Blender LDraw import; ExportLDraw also **exports LDraw from Blender** (round trip for roofsnow-style edits) | ExportLDraw targets Blender 2.82–3.x. Check it on 4.x/5.x |
| [LeoCAD CLI](https://www.leocad.org/docs/cli.html) | Headless-ish `-i` image, `-obj/-3ds/-dae` export, `-csv`, `-html`, step ranges, submodel, camera angles, orthographic | Fastest cheap preview and step-render path. LDraw input |
| LDView / LPub3D | Snapshot CLI (LDView), instruction pipeline (LPub3D) | Studio itself ships LDView-licensed code (`Licenses/LDView*.txt`) |
| [michaelgale/ldraw-py](https://github.com/michaelgale/ldraw-py), [hbmartin/pyldraw3](https://github.com/hbmartin/pyldraw3/) | Python LDraw read/write/generate | mils-integrator already has its own stdlib parser (ADR 0003). These are a reference, not a dependency |
| [wendehals/bricks-mcp](https://github.com/wendehals/bricks-mcp) | Rebrickable MCP: sets, parts, user collections and part lists | Go, EPL-2.0 |
| [Brick Directory](https://brick.directory/docs/faq.html) | Hosted MCP connector: Rebrickable, BrickLink pricing, Brickset, BrickEconomy, BrickOwl | OAuth. Free beta. Third-party hosted |
| BrickLink Store API (OAuth 1.0) e.g. [BricklinkSharp](https://github.com/gebirgslok/BricklinkSharp) | Catalog items, price guide, colours, categories, **item mapping (element id ↔ item no)**, inventory, orders | Needs seller API registration and IP allowlist. **No wanted-list endpoints**, so wanted lists go through Studio's XML export or manual upload |
| [bodog/bricktools#18](https://github.com/bodog/bricktools/issues/18) | Independent conclusion: Studio has no supported CLI or headless API. Use it as a manual tool. Its licence doesn't cover Studio's bundled assets | Confirms §1 |

## 4. Integration surfaces, ranked

1. **File plane (primary).** Read and write `.io`, `.ldr` and `.mpd`. Everything agents need for mils-integrator (`tools.analyze_ldraw`, `tools.riser_ldraw`) and roofsnow lives here. Studio opens the result.
2. **Catalog/mapping plane.** Load `StudioPartDefinition2.txt`, `StudioColorDefinition.txt` and `ldraw.xml` from the local install **at runtime** to translate LDraw ↔ BrickLink ↔ Studio ids and colours. Never commit or ship these files. Rebrickable CSVs and the API are the redistributable fallback. BrickLink API covers price and availability.
3. **Render/preview plane.** Use Blender through the official connector (`execute_blender_code` + `ldr_tools_blender` to import `.io` directly), `ldraw-mcp` for headless multi-angle renders, and LeoCAD CLI for fast thumbnails and step images. This beats calling Eyesight directly: Eyesight is Cycles-derived from about 2017, and running it outside Studio is a EULA grey area.
4. **App-control plane (GUI, computer use).** Open files with `open -a "/Applications/Studio 2.0/bin/Launcher.app" file.io` (**unverified** whether it reuses a running instance). Use the native menu bar (`computer_app_menu`) for *File › Export As* (LDraw, LXFML, POV-Ray, Collada, CSV/TSV parts list, **BrickLink Wanted List XML**) and *Import* (set inventory by number, wanted-list XML → palette). Type paths into native file dialogs with ⌘⇧G. Instruction Maker, Eyesight render queue, stability check and gallery upload are GUI-only. Expect a near-empty accessibility tree inside the Unity viewport, so the viewport is screenshot and coordinate driven.
5. **Not viable:** in-process injection (BepInEx/Harmony on the Mono DLLs), decompiling, decoding `.conn`/`.col` connectivity, or redistributing Studio data. All are blocked by EULA §4.

## 5. Proposed `studio-bridge` MCP (fleet member candidate)

A local stdio MCP in Python/FastMCP that runs on the Mac, mirroring how the Blender connector is packaged:

- **Distribution:** a `.mcpb` Desktop Extension for Cowork. Cloud Cowork sessions then see it through the desktop bridge as `mcp__remote-devices__studio__*`, just like `…__Blender__*` today. The same binary goes in Claude Code `.mcp.json` and OpenCode `opencode.json` (`"mcp": {"studio": {"type": "local", "command": [...]}}`).
- **Config:** `STUDIO_HOME` (default `/Applications/Studio 2.0`), `LDRAW_DIR` (Studio's bundled library or `~/.ldraw`), workspace root for model files.

| Tool | In → Out | Backed by |
|---|---|---|
| `studio.info` | → version, parts_db_version, library version, paths, renderers available | install files |
| `io.read` | path → `{meta, submodels[], parts[{ldraw_id, bl_item_no, studio_color, bl_color, ldraw_color, matrix, step, submodel}], steps, custom_parts, errors}` | zip reader (pwd fallback) + mapping tables |
| `io.write` | LDraw/MPD text or parts JSON → `.io` (current layout, thumbnail optional) | brick-mcp writer logic (licence permitting) |
| `io.extract_ldraw` / `io.from_ldraw` | `.io` ↔ `.ldr/.mpd` (colour-space aware) | same |
| `catalog.map_part`, `catalog.map_color` | any id space → all id spaces | Studio tables → Rebrickable fallback |
| `bom.export` | `.io`/LDraw → BrickLink wanted-list XML, CSV, Rebrickable CSV | mapping + writer. Upload stays manual (no API) |
| `render.preview` | model, views, size → PNG(s) | LeoCAD CLI or ldraw-mcp |
| `render.blender` | model → imports into live Blender via connector | `ldr_tools_blender` |
| `studio.open` | path → launches or focuses Studio with the file | `open` + Launcher.app |
| `mils.*` passthrough | `.io` in → `tools.analyze_ldraw / plan / validate_plan / riser_ldraw` | mils-integrator `tools.py` (accepts `.io` via `io.extract_ldraw`) |

Plus a **skill** (`studio-gui`), not tools: computer-use playbooks for Export As…, import set inventory, render queue, Instruction Maker page export, and stability check. Each playbook sets out preconditions, menu paths, dialog path entry and the expected file on disk, so every GUI step ends in a file the bridge can verify.

**Loop for the drafting table:**

1. The agent plans in LDraw via mils-integrator.
2. `io.write` produces the file and `render.preview` gives a quick visual check.
3. `studio.open` hands the file to James.
4. James edits in Studio.
5. `io.read` diffs his changes back into the plan and stores accepted edits as gold exemplars (ADR 0005).
6. `bom.export` produces the BrickLink order.

## 6. Open items to verify

- [ ] Minimum `.io` entry set Studio 2.26 accepts from a third-party writer (`model.ldr` only? does it need `model2.ldr` or `.info` `parts_db_version`?). Test by round-tripping a `brick-mcp`-written file.
- [ ] `open` via Launcher.app with Studio already running: new window, replace, or prompt?
- [ ] Studio's accessibility tree: does `computer_app_ax_find` see anything beyond the native menu bar and dialogs?
- [ ] Mac user-data paths (CustomParts, preferences, autosave). Likely `~/Library/Application Support/Stud.io/…`, but **unverified**. Needs a folder grant to confirm.
- [ ] brick-mcp licence (unstated). Ask the author or reimplement the writer (the format is simple).
- [ ] ExportLDraw on current Blender. Is `ldr_tools_blender` import-only?
- [ ] Studio's colour/part tables: reading them locally for personal tooling seems fine, but don't commit or ship them. Check the Studio ToS/IP guidance before any public release.

## Sources
Studio Help: [Export formats](https://studiohelp.bricklink.com/hc/en-us/articles/6502197862679-Exporting-to-other-formats) · [Import formats](https://studiohelp.bricklink.com/hc/en-us/articles/6502277722647-Import-formats) · [Software License Agreement](https://studiohelp.bricklink.com/hc/en-us/articles/6606313426711-Studio-Software-License-Agreement) · [Render queue](https://studiohelp.bricklink.com/hc/en-us/articles/6507148199959-Render-queue) · [v2.25.9 critical update](https://studiohelp.bricklink.com/hc/en-us/articles/35041828645143-Studio-v-2-25-9-Critical-Update-released) · [Wikipedia: BrickLink Studio](https://en.wikipedia.org/wiki/BrickLink_Studio) · [LDraw wiki: IO](https://wiki.ldraw.org/wiki/IO) · [LDraw wiki: Eyesight](https://wiki.ldraw.org/wiki/Eyesight) · [LeoCAD #356 (.io contents)](https://github.com/leozide/leocad/issues/356) · [BrickNerd: Hacking Studio renders](https://bricknerd.com/home/hacking-studio-how-to-get-better-renders-like-blender-11-28-23) · [HN: Eyesight/Cycles GPL](https://news.ycombinator.com/item?id=35181954) · [Blender connector architecture (DevelopersIO)](https://dev.classmethod.jp/en/articles/claude-blender-connector-desktop-and-code/) · [OpenCode MCP servers](https://opencode.ai/docs/mcp-servers/) · plus the repos linked in §3.


---

# PART C — build-harness/architecture-adrs-and-LEGO-PIPE-010.md (with Amendments R1 and Clarifications R2)
*In which the four components are named; the integer lattice, rotation group and stud-mate rule are fixed; collision, floating and grounding checks are specified with stability left advisory; three validator tiers put Studio in the oracle's chair; drift is enumerated by kind and answered by control; children build freely and buy nothing; ADRs 0006–0011 are recorded with the original LEGO-PIPE-010 memo; and, appended, the amendments move identity to a GUID, the lattice to connector space, collision into brickcore, and keep agents building in Blender through brick_bench, which hosts brickcore but is not it.*

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


---

# PART D — build-harness/storage-architecture-asset-versioning.md (with Amendments R1 and Clarifications R2)
*In which the folder-of-files is abandoned; the studios' work/publish split, product/version/representation and composition-by-reference are adopted; two repos and a blob store are proposed; `lvp://` URIs and a branch flow replace file locking; OpenUSD is elected canonical under five guardrails (ADR 0012); and, appended, the amendments narrow the USD profile, make flattened ingest an overlay with a manifest, retire branch-prefixed versions, and read LDraw licences per part, failing closed when a licence is missing.*

# build-harness — storage & asset-versioning architecture (supersedes the "Infrastructure sketch" in LEGO-PIPE-010)

**Date:** 2026-09-17 · **Status:** proposed · **ADR:** 0012
**Question:** How do we version a LEGO village that is composed from reusable assets (parts → buildings → modules → layouts → seasons), edited by agents and family on branches, exported to Studio, and grown over years — and what do game/VFX studios already know about this?

## 1. What the problem actually is

Studios separate four things that a single git repo under `~/Documents` conflates:

| Concern | In our project | Studio equivalent |
|---|---|---|
| **Canonical scene data** (small, text, diffable) | LDraw MPD, manifests, layers, validation reports | USD layers, Unreal `.umap` (binary, hence locking) |
| **Derived / heavy data** (regenerable, binary) | `.io` exports, renders, `.blend` scenes, oracle screenshots, voxel caches | DerivedDataCache, textures, baked lighting — kept out of VCS or in LFS/Perforce |
| **Asset hierarchy & composition** (what references what, at which version) | village → modules → buildings → risers/snow layers → parts | USD composition arcs; AYON folder/product/version; Perforce streams |
| **Work vs publish** | a kid's branch vs the layout that's physically built | workfile (mutable, personal) vs published version (immutable, referenced by others) |

Two things make our case *easier* than a game studio's, and we should exploit them:

1. **Our canonical format is text and semantically diffable** (LDraw + the `DiffOp` model). Studios need file locking because `.uasset` can't merge. We don't — a custom merge driver over placements by uid can merge two branches that touched different parts.
2. **Every heavy artifact is regenerable** from the canonical data plus a library version. So the blob store is a cache with provenance, never a source of truth.

## 2. Patterns worth stealing, and the mapping

| Studio pattern | Source | What we adopt |
|---|---|---|
| **Work / publish split.** Artists edit workfiles; `publish` freezes an immutable, numbered version other scenes reference | AYON, ShotGrid, every VFX pipeline | Family branches are workfiles. `publish` is a harness action producing `bakery/model/v003`. Layouts reference published versions only, never branch heads |
| **Product / Version / Representation** | AYON | A *product* is one output type of an asset (`model`, `snow`, `bom`, `render`, `instructions`). Each version has ≥1 *representation* (`.mpd`, `.io`, `.png`, `.xml`). Same version, many formats |
| **Hero / latest pointer** | AYON "hero version" | `@latest` resolves to the newest published version. Layouts pin (`@v3`); play branches may float |
| **Composition by reference, not copy** | USD references/payloads | A module *references* a building at a version and places it with a transform. Editing the building doesn't silently change the module until it re-pins |
| **Layers = non-destructive opinions** | USD sublayers / layer stack, "strongest opinion wins" | roofsnow's `SnowDiff`, a recolor policy, a lighting pass are **layers** over a referenced base. Base stays pristine; layers are versioned products in their own right; flatten composes them |
| **Variants** | USD variant sets | `season: {summer, winter}`, `snow: {none, light, heavy}`, `lighting: {off, on}` as named variants on an asset interface, chosen at reference time |
| **Component vs assembly kinds** | USD model hierarchy (`kind`) | `component` = building, riser, tree, train (self-contained, referenceable). `assembly` = MILS module, layout, season. Components never contain components |
| **Asset interface layer** | USD "asset structure principles" | Each asset has a small `asset.yaml` front door: id, kind, variants, footprint/height hints, extents — readable without loading geometry (our `SetAnalysis` lives here) |
| **Asset resolver + stable URIs** | USD `ArResolver`, Perforce depot paths | `lvp://christmas/buildings/bakery/model@v3` resolved by a tiny resolver to git path + blob hash. Nothing hard-codes filesystem paths |
| **Content-addressed derived data** | DerivedDataCache, git-annex, DVC | Blobs stored by sha256, indexed by (asset, version, representation, library versions). Regenerate on miss |
| **Flatten / package for delivery** | `usdz`, cooked builds | Studio never sees the composition; it gets a flattened MPD/`.io` per published version, with a manifest mapping uids back |
| **Streams** (server-understood branch hierarchy) | Perforce | We don't need Perforce, but we adopt the *shape*: `main` (physical) ← `staging` (next order) ← `play/<user>` |
| **Never reuse a version number** | USD/AYON guidance | Versions are immutable; corrections are new versions |

Things we deliberately *don't* import: file locking (unnecessary with text canonical), Perforce itself, a full AYON server (overkill for one family; adopt the model, not the product), Omniverse/Nucleus as infrastructure (USD the format, yes; the NVIDIA platform, not now).

## 3. Proposed architecture

### 3.1 Repos (play-well cluster, Northstar)

| Repo | Contents | Why separate |
|---|---|---|
| `ojfbot/lego-village-pipeline` (exists) | Code: brickcore, brick_bench, studio-bridge, harness API, mils-integrator, roofsnow, resolver, CLI | Tools evolve independently of content; CI runs tests, not asset diffs |
| `ojfbot/play-well-library` (new) | **Canonical content:** assets (components, assemblies, layers), published version manifests, validation reports, golden set, the catalog index. Text only + LFS pointers for the few blobs worth pinning (thumbnails) | Content history should be readable without code churn; family branches live here; can be private forever |
| blob store (not a repo) | Derived representations by sha256: `.io`, renders, `.blend`, oracle screenshots, voxel caches | Regenerable; huge; never merged. Dev: a directory. Later: S3-compatible bucket, optionally lakeFS if we want branch-aware blobs |
| corpus (exists, mils-integrator) | Harvested precedent, SQLite + blobs | Separate lifecycle (ADR 0002) |

Studios split "engine/tools" from "content depot" for the same reasons.

### 3.2 Library layout (`play-well-library`)

```
library/
  assets/
    buildings/bakery/                 # kind: component
      asset.yaml                      # interface: id, kind, variants, footprint, height, tags, license
      work/                           # NOT published; branch-local edits land here
        model.mpd · manifest.json
      published/
        model/v001/  model.mpd · manifest.json · report.json · blobs.json (sha256 → representation)
        model/v002/ …
        snow/v001/   layer.json (DiffOps) · report.json          # a layer product
        bom/v002/    bom.json · wanted.xml
    modules/M03-bakery-corner/         # kind: assembly
      asset.yaml
      published/assembly/v004/
        assembly.json                 # references: [{ref: lvp://…/bakery/model@v2, xform, variants:{snow: heavy}},
                                      #              {ref: lvp://…/risers/bakery-riser@v1}, {layer: lvp://…/bakery/snow@v1}]
        flat/model.mpd                # flattened composition (cached, also a representation)
    layouts/christmas-2026/            # kind: assembly (top level)
      asset.yaml
      published/assembly/v009/ assembly.json · flat/ · bom/
  golden/                              # OMR known-goods + mutations (CC BY 4.0, attribution file)
  catalog.sqlite                       # index: assets, products, versions, representations, blob hashes, library versions (rebuildable from files)
```

- `work/` is what branches change. `published/**` is append-only on every branch and is the only thing a reference may point at.
- `assembly.json` is the composition document: references (asset URI @ version, transform on the stud lattice, variant selection), layers in strength order, and its own local placements. **A flat MPD is a derived representation of an assembly, not its source.**
- `manifest.json` per published model carries the uid map, lattice classes, provenance, and the library versions it was validated against (LDraw release, shadow-lib commit, Rebrickable dump, brickcore version). Reports are pinned to versions, so "was this ever valid, and under which rules" is always answerable.

### 3.3 URIs and the resolver

`lvp://<layout-or-collection>/<kind>/<asset>/<product>@<version|latest>[#representation]`

Examples: `lvp://christmas/buildings/bakery/model@v3`, `lvp://christmas/modules/M03/assembly@latest#flat.io`.
The resolver (in brickcore) maps a URI to a git path (canonical) or a blob hash (representation). Swapping `~/Documents` for S3 later changes the resolver, not the assets.

### 3.4 Branch model (the Perforce-streams shape in git)

| Branch | Meaning | Who writes |
|---|---|---|
| `main` | What is physically built / ordered. Layout versions here are the real world | dev merge only, full validator + BOM check |
| `staging` | Next order cycle | parent/dev |
| `play/<user>` | Personal worksite; unrestricted building | that user (via the harness) |
| `agent/<request-id>` | Ephemeral; one proposal | harness, deleted after accept/reject |

Merge driver: a brickcore-provided git merge driver for `model.mpd`/`manifest.json` that merges by uid (add/remove/move/recolor) and only conflicts when both sides touched the same uid. `published/**` never conflicts (append-only, version numbers allocated by the catalog with a branch prefix on play branches: `v004-play-eli` until promoted).

### 3.5 Publish pipeline (harness action)

1. Validate work/ (T0) → must have no `block`.
2. Allocate version; freeze `model.mpd` + `manifest.json` + `report.json` under `published/<product>/vNNN/`.
3. Generate representations (flat MPD, `.io`, renders, BOM) → blob store, record hashes in `blobs.json`.
4. Update `catalog.sqlite`; move `@latest`.
5. Assemblies that reference `@latest` get a "new version available" notice in the drafting table; pinned ones don't move.

### 3.6 Dev phase mapping (what actually runs on the Mac this month)

```
~/Documents/play-well/
  play-well-library/      # git clone; branches per user; LFS for thumbnails
  blobs/                  # sha256-addressed derived files (gitignored, regenerable)
  golden/                 # or inside the library repo; decide by size
docker: blender-worker mounts ~/Documents/play-well (rw); harness API reads/writes only through brickcore's resolver
```

Later: `play-well-library` on GitHub (private); blobs → S3-compatible bucket (or lakeFS on top of it if branch-aware blobs earn their keep); resolver config switches; family Macs/iPads reach the drafting table over the web and never touch the repo directly. Studio saves from family Macs arrive via an ingest drop folder → identity diff → commit on that user's play branch.

## 4. How to learn from the studios (concretely)

Rather than reading broadly, port three specific things:

1. **USD asset structure → our `asset.yaml` + `assembly.json`.** Read NVIDIA's *Principles of Scalable Asset Structure in OpenUSD* and the USD glossary entries for *composition arcs, layer stack, variant set, model hierarchy (kind), payload*. Then take one of the public USD reference assets (Pixar's Kitchen Set or the ALab set) and write down, per file, which of our concepts it corresponds to. The exercise is ~2 hours and settles the composition schema.
2. **AYON project anatomy → our catalog.** Read *Project Anatomy* and the glossary (folder / task / product / version / representation / hero). Our `catalog.sqlite` schema should be a strict subset of that model so the vocabulary is standard if we ever adopt a real pipeline manager.
3. **Perforce streams → our branch model.** Read the streams guide only for the *shape* (mainline, development, release; "flow" rules about which direction changes move). Encode the flow rules in the harness (play → staging → main; never sideways) instead of relying on convention.

Then one spike, **S6 composition round trip:** two published buildings + a riser + a snow layer + a `season` variant composed into a module, flattened, opened in Studio, edited by hand, ingested back as a diff on the right asset (not on the flattened module). If S6 works, the whole model works.

## 5. The one real fork: own composition schema vs real OpenUSD

| Option | For | Against |
|---|---|---|
| **A. Own schema now** (JSON `assembly.json` + LDraw leaves; USD *concepts*) — **recommended for phases 1–4** | Tiny; brickcore stays pure Python; family-readable; Studio only ever needs LDraw; nothing to install | We re-implement composition (references, layer strength, variants) ourselves, ~a few hundred lines; no ecosystem tooling |
| **B. Real OpenUSD as canonical** with a custom `Brick` schema (part id, colour, lattice class, connectors as attributes) | Blender imports USD natively; instancing, variants, layers, resolver all exist; industry-standard vocabulary; scales to enormous scenes | `pxr` dependency everywhere (Docker fine, Pi painful); Studio still needs a flattening exporter; USD's float transforms vs our integer lattice needs discipline; family-facing debugging gets harder; overkill for one village |
| C. Flat MPD only | Simplest | No reuse, no layers, no pinned versions — this is the `~/Documents` sketch we're replacing |

**Decision (James, 2026-09-17): B — OpenUSD-native from the start.** Rationale: the project has every USD composition concept naturally (references, layers, variants, kinds, instancing), so it is a good learning vehicle; the "rich annotation" ambition (connectivity, physics, lighting, provenance as schemas/relationships on prims) is exactly what USD is for; skills and tooling transfer across the fleet (asset-foundry). Option A is retained as the documented fallback if S7 fails.

### 5.1 Guardrails that keep B from becoming a tax

1. **USD is the composition + annotation layer; LDraw stays the leaf geometry and the Studio interchange.** A brick prim carries `brick:part`, `brick:color` (LDraw code), `brick:lattice`, an integer-snapped `xformOp:transform`, and `kind`. Part geometry is *not* authored per placement: a part-USD cache (`parts/3001.usd`, generated once from LDraw via ldr_tools/ImportLDraw, `instanceable`) is referenced by every placement. Flatten-to-LDraw walks the composed stage and emits MPD; this is the only Studio-facing exporter.
2. **brickcore's math stays numpy over a plain in-memory model.** `pxr` is confined to `brickcore.io.usd` (read stage → placements; write placements/layers → usda). Validators never call pxr. A flat-LDraw import path stays as the fallback, so CI and any box without `pxr` still validate.
3. **No schema plugin in phase 1.** Use namespaced custom attributes plus `assetInfo`/`customData` and `kind`. Promote to a codeless `Brick` API schema (plugInfo.json + generatedSchema.usda, no C++) at phase 3 once the attribute set has stopped moving. Runtime-registered schemas don't exist in USD today, so the plugin plumbing is unavoidable later; defer it.
4. **Connectivity as relationships.** Mates become `brick:mates` relationships between prims in a validator-written sublayer (never in the base layer), so the connection graph is queryable in `usdview` and diffable, and a human edit can't corrupt it.
5. **Text only:** `.usda` for everything canonical (diffable, git-mergeable by prim path); `.usdc` only as a derived representation in the blob store.

### 5.2 Known costs, priced

| Cost | Size | Mitigation |
|---|---|---|
| `usd-core` wheels: PyPI ships macOS universal2, Linux x86_64, Windows — **no arm64 Linux**, which is what "Docker on Apple Silicon" is | Real | Options: community arm64 wheels (V-Sekai builds 26.8 for py3.12–3.14), `--platform linux/amd64` under Rosetta (slower), or run brickcore natively on the Mac and keep only Blender in Docker. **Spike S7 decides.** |
| Blender doesn't expose `pxr` inside its Python; USD I/O goes through Blender's own importer plus `USDHook` callbacks | Medium | Blender imports the composed stage natively; `brick_bench` reads our attributes via `USDHook.on_import`. Composition/annotation work happens in brickcore, not in Blender's Python |
| Learning LIVRPS (layer/inherit/variant/reference/payload/specialize strength ordering) before designing layers | 1–2 weeks of evenings | Learn it on the S6 spike; the project's layers are shallow (base + snow + lighting + validator) |
| Float transforms vs integer lattice | Small | Snap on read, validate on write; store integers in `customData` as the authority |
| Family-facing debugging is one step further from LEGO | Small | The drafting table never shows USD; `usdview` is a dev tool |

### 5.3 Learning path (USD as the entrypoint)

- NVIDIA *Learn OpenUSD* modules (free): fundamentals → asset structure → composition. Do them against *our* assets, not the sample scenes.
- *USD Survival Guide* (Luca Scheller) for the Python API idioms brickcore will use.
- Pixar's Kitchen Set or ALab: read the file layout, map each file to our `component / assembly / layer`.
- Blender's USD import for immediate visual feedback on every composition experiment; `usdview` for inspecting the layer stack and resolved opinions.
- Spikes: **S6** composition round trip (now in USD) and **S7** `pxr` on the Mac + in Docker.

## ADR 0012 — Versioned asset library: work/publish split, composition by reference, layers, content-addressed derived data

**Status:** proposed · 2026-09-17
**Context:** A village is composed from reusable assets across years, edited by agents and family on branches, exported flat to Studio. A single git repo of MPDs (LEGO-PIPE-010 §Infrastructure sketch) can't express reuse, pinning, non-destructive layers, or "which layout is real". Game/VFX pipelines solved this with the work/publish split, immutable versions, composition arcs, and derived-data caches.
**Decision:**
1. Two repos: `lego-village-pipeline` (code) and `play-well-library` (canonical content, text). Derived representations live in a sha256 blob store outside git.
2. Assets have kinds (`component`, `assembly`, `layer`) and an interface file; assemblies compose by **reference at a pinned version** with a lattice transform and variant selection; layers are versioned `DiffOp` products applied in strength order; flattening is a derived representation.
3. `work/` is mutable and branch-local; `published/<product>/vNNN` is immutable and append-only; references may only target published versions. Versions are never reused.
4. Stable `lvp://` URIs resolved by brickcore; storage location is resolver config.
5. Branch flow `play/<user>` → `staging` → `main`; `main` = physical state; a uid-aware merge driver replaces file locking.
6. **OpenUSD is the canonical composition and annotation format** (`.usda`), with LDraw as leaf geometry and Studio interchange, per the guardrails in §5.1. The own-JSON schema (option A) is the documented fallback if S7 fails.
**Consequences:**
- `pxr` becomes a dependency of `brickcore.io.usd` (not of the validators); ADR 0007's "no Blender dependency" stands, and gains "no pxr in validators".
- The part-USD cache and the flatten-to-LDraw exporter are new phase-1 deliverables; `assembly.json` is dropped in favour of `assembly.usda`.
- Family branches work on `.usda` text; the merge driver operates on prim paths instead of uids (uid = prim path).
- roofsnow and mils-integrator outputs become first-class layer/component products instead of ad-hoc files.
- Every published version records the library versions it was validated under → reproducible verdicts.
- Publishing is a harness action with validation gates; play branches remain unrestricted (James's decision on roles stands).
- One extra spike (S6) before phase 2; `catalog.sqlite` schema and the merge driver are new phase-1 deliverables.

## Sources
OpenUSD, *Generating New Schema Classes* (codeless schemas) — https://openusd.org/release/tut_generating_new_schema.html · AOUSD forum, *Do you need a plugin for custom schema?* — https://forum.aousd.org/t/do-you-need-a-plugin-for-custom-schema/1617 · usd-core wheel coverage / arm64 community builds — https://github.com/V-Sekai-fire/repository-usd-core-wheels · Blender `USDHook` — https://docs.blender.org/api/current/bpy.types.USDHook.html · NVIDIA, *Principles of Scalable Asset Structure in OpenUSD* — https://docs.omniverse.nvidia.com/usd/latest/learn-openusd/independent/asset-structure-principles.html · OpenUSD glossary — https://openusd.org/release/glossary.html · AYON glossary (folder/product/version/representation/hero) — https://help.ayon.app/articles/3030530-ayon-glossary · AYON project anatomy — https://help.ayon.app/articles/3815114-project-anatomy · StraySpark, *Version Control for UE5 Teams: Git LFS vs Perforce vs Anchorpoint* — https://www.strayspark.studio/blog/version-control-ue5-git-lfs-perforce · lakeFS, *DVC vs Git-LFS vs Dolt vs lakeFS* — https://lakefs.io/blog/dvc-vs-git-vs-dolt-vs-lakefs/ · Blender USD import/export manual — https://docs.blender.org/manual/en/latest/files/import_export/usd.html

---

# Amendments R1 (2026-09-17, from CORR-LEGO-PIPE-013 reconciling LEGO-PIPE-012)

*Appended, never rewritten in place. Where an amendment conflicts with text above, the amendment wins.*

## ADR 0012 — Amended R1

**Identity (R-15).** `brick:id` (ULID) is identity; prim path is namespace. `asset:id`, `instance:id` and export-occurrence identity are carried as in ADR 0006-R1. The merge driver keys on `brick:id`. `brick:mates` relationships use paths as USD requires; the validator sublayer also records endpoint GUIDs so relationships survive namespace edits.

**LVP USD profile (R-13, R-14).** v1 permits: references to published assets; a small, ordered sublayer stack; named variant selections; local overrides in one designated edit layer. Deferred/forbidden: inherits, specializes, payloads, relocates, sub-root references, arbitrary list editing, multiple edit targets. Canonical layer order is fixed and linted; `usdchecker` and golden flatten tests run in CI. Layers are classified by effect — **physical** (authored geometry/BOM: base, snow-as-bricks, risers), **derived** (validator relationships/annotations), **presentation** (render-only: lighting, materials) — and publishing logic reads only physical layers.

**Flattened ingest (R-19).** Every flat export (MPD/`.io`) ships a sidecar manifest mapping each occurrence to `{brick:id, asset:id, source_version, instance:id, source_prim_path, export_transform}`. On ingest: edits to an unambiguously matched occurrence become an **assembly-local override** by default; additions become assembly-local placements; delete/move/recolor of a source brick may be *proposed* for source promotion only when the user entered an explicit "edit <asset> source" scope and provenance still matches; ambiguity becomes a `DecisionPoint`; editing one instance never silently mutates all instances. Publishing back into a referenced source is a deliberate promotion operation.

**Versions and `@latest` (R-17, R-09).** Play branches carry immutable, content-addressed draft/revision IDs with author and request metadata — no branch-prefixed semantic versions. Canonical monotonic published versions are allocated only by a serialized publish queue on `staging`/`main`; an immutable asset/version ID is independent of the display label `v004`. `@latest` is a query/UI convenience: proposal creation resolves it and writes a pinned version plus a lock entry. Every play branch has a baseline lock (source commit; resolved asset versions; LDraw/shadow/Rebrickable/validator versions; model-provider config), a "refresh from main" operation that previews a semantic three-way rebase, and a stale/degraded status when dependencies no longer reproduce. `catalog.sqlite` indexes allocation state but is never the sole allocator.

**Concurrency and authority paths (R-21, R-23, R-24).** One git worktree per active family branch, or a service-managed bare repo with ephemeral worktrees per proposal; Studio drop-folder ingest binds each file to a branch/session explicitly. CI proves `catalog.sqlite` regenerates from published manifests and rejects drift; missing blobs regenerate deterministically or surface as "representation unavailable", never as missing canonical content; blob GC is by reachability from manifests with a retention window. The Blender worker mounts the proposal worktree read-only plus a job output directory (ADR 0007-R1).

**Licensing (R-16, corrected).** The LDraw parts library is licensed **per part** — CC BY 2.0, dual CC BY 2.0+4.0, CC BY 4.0-only, or CC0 — and the part's `0 !LICENSE` header is authoritative; the part-USD cache generator records it per part and the attribution manifest per representation lists the distinct licences present. LDCad-derived connector data lives in a separately attributed data layer with source commit and licence (CC BY-SA 4.0), never merged invisibly into code. The geometry cache stays local and regenerable, outside the content repo; model references and our own annotations are what get published, not converted part meshes; a targeted licence review precedes any public or commercial distribution.

**Merge driver sequencing (C-6).** Phase 1 delivers stable IDs and a three-way diff model; automatic semantic merge follows once real branch conflicts exist as fixtures.

## Clarifications R2 (2026-09-17, ChatGPT confirmation of CORR-013 §D.3)

**ADR 0012 — licensing fields (R-16, final).** For every part in the part-USD cache and every attribution manifest, preserve: the raw `0 !LICENSE` header line; a normalised licence identifier (`CC-BY-2.0`, `CC-BY-2.0 AND CC-BY-4.0`, `CC-BY-4.0`, `CC0-1.0`); the source library version (LDraw release id, shadow-library commit); and the part file hash. A part with a missing or ambiguous licence **fails closed for distribution** (the representation may be built locally but is marked `distribution: blocked`). OMR model licensing is tracked separately per model artifact from that artifact's own metadata and is never inferred from the parts it references.
