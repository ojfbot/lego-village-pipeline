---
correspondence_schema: lego-pipe-memo/v2
memo: HANDOFF-LEGO-PIPE-018
revision: R0
status: issued
memo_type: handoff
title: "Spikes S1 and S7 on the Mac"
subtitle: "Studio round-trip contract and the USD runtime matrix, run by Claude Code, findings only"
date: 2026-09-17
thread: build-harness
cluster: play-well
project: LEGO Village Pipeline
from:
  actor: "Claude (Cowork)"
  role: design_author
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
  memo: HANDOFF-LEGO-PIPE-011
  revision: R2
authority:
  decision_owner: James
  implementation_authorized: spikes_S1_S7_only
  production_code_authorized: false
register:
  number: 018
  allocated_by: James
  allocated_on: 2026-09-17
repos:
  - ojfbot/lego-village-pipeline
tags:
  - spike
  - bricklink-studio
  - io-file-format
  - studio-round-trip
  - openusd
  - usd-core
  - apple-silicon
  - docker
argument: >-
  In which two spikes that 011-R2 had assigned to Claude Cowork are reassigned to
  Claude Code on the operator's Mac, because Claude Code can write the probe files and
  run the diffs while the operator does the one thing only a human can, which is press
  Save in Studio; the Studio round trip is specified as a fixed sequence of probe files
  whose only output is a normalisation table and a minimum-entry contract; the USD
  runtime matrix is specified as four import attempts whose only output is a decision
  row; and nothing beyond a findings note and disposable scripts under spikes/ is
  authorised.
parts:
  "1": "Scope and what is not authorised"
  "2": "S1 — Studio round trip: probes, procedure, exit criteria"
  "3": "S7 — USD runtime matrix: attempts, exit criteria"
  "4": "Deliverables and where they go"
provenance:
  source_artifacts:
    - {name: "build-harness/LEGO-PIPE-011-from-studio-to-stage-R2.md", role: "accepted work order; spike definitions §4"}
    - {name: "studio-bridge/research-bricklink-studio-agent-integration.md", role: "verified facts about the Studio install and .io container"}
  method: "spike specifications derived from 011-R2 §4 and Part B §2; no new research"
---

# HANDOFF-LEGO-PIPE-018 — Spikes S1 and S7 on the Mac

## 1. Scope

Two spikes from 011-R2 §4, reassigned from Claude Cowork to Claude Code because both run on James's Mac. Everything else in 011-R2 (Stage-0 contracts, preflight, register, S2, the container half of S7) is unchanged.

**Authorised:** disposable scripts under `spikes/S1/` and `spikes/S7/`; two findings notes; nothing else. **Not authorised:** any file under `brickcore/`, `brick_bench/` or `studio-bridge/`; any change to package boundaries; installing anything into `/Applications/Studio 2.0` or Studio's user data. Studio is never modified, only launched and used through its own File menu by James.

Facts to rely on (verified in Part B of 011-R2): Studio 2.26.8_1 at `/Applications/Studio 2.0`; opener is `bin/Launcher.app` (owns UTI `com.bricklink.io`); current `.io` is an unencrypted zip with `model.ldr`, `modelv2.ldr`, `model2.ldr`, `model.lxfml`, `model.ins`, `thumbnail.png`, `errorPartList.err`, `.info`; legacy `.io` is ZipCrypto with password `soho0909`; samples in `/Applications/Studio 2.0/Sample/*.io`; `model.ldr` uses LDraw colour codes, `model2.ldr` uses Studio/BrickLink codes.

## 2. S1 — Studio round trip

**Question.** What is the minimum `.io` a third-party writer must produce for Studio to open it cleanly, and what does Studio change between open and save?

**Probe files** (write each with a script; keep the script and the file):

| Probe | Contents | Tests |
|---|---|---|
| P1 | `model.ldr` only (5 parts: 3001, 3003, 3020, 3068b, 3024 on a 3811 baseplate, LDraw colours, integer LDU, identity rotations) | minimum entry set |
| P2 | P1 + `.info` `{"version":"2.26.8_1","total_parts":6}` | whether `.info` is required or rewritten |
| P3 | P2 + `errorPartList.err` = `[]` + a 1×1 PNG `thumbnail.png` | full legacy-style set |
| P4 | P3 with one part at a non-integer position (x = 10.5) and one rotated 45° about Y | how Studio reports/normalises off-lattice and free parts |
| P5 | P3 with a `0 !BRICKCORE id=01J…` meta line after each part line and a custom `0 LVP_MANIFEST …` header | whether any custom meta survives save |
| P6 | P3 as an MPD with two submodels (`0 FILE`/`0 NOFILE`) and one `0 STEP` per submodel | submodel and step preservation |
| P7 | one bundled sample (`Sample/Banana.io`) copied unchanged | control: Studio's own file, open→save diff |

**Procedure per probe.** Script writes the file to `~/Documents/play-well/spikes/S1/in/PN.io`, then runs `open -a "/Applications/Studio 2.0/bin/Launcher.app" <file>`. James does, by hand: note any import dialog or error text, **File › Save As** to `…/spikes/S1/out/PN.io`, close the model. Script unzips both, and diffs: entry list; `.info` contents; every `1` line of `model.ldr` (colour, position, matrix, part) in a normalised form; presence of custom meta lines; submodel names and step counts; `model2.ldr` `BL_Item_No` per part. Also record whether Launcher reused the running Studio instance or opened a second one, and list files that changed under `~/Library/Application Support` (`Stud.io`, `Studio`) and `~/Library/Caches` during the run (passive surfaces).

**Exit criteria.** A findings note containing: (a) the minimum entry set that opens without error; (b) a normalisation table — for each field, `preserved | rewritten(how) | dropped`; (c) whether any custom meta survives; (d) how off-lattice and 45° parts are handled; (e) Launcher behaviour with a running instance; (f) the list of passive surfaces touched. No recommendation section; the writer contract is decided in the next revision of 011.

## 3. S7 — USD runtime matrix (native half)

**Question.** Does `usd-core` load and compose a stage on this Mac, natively, and does Blender import what it writes?

**Attempts.**

| Attempt | Command | Record |
|---|---|---|
| A1 | `python3 -m venv ~/Documents/play-well/spikes/S7/venv && pip install usd-core` | Python version, `usd-core` version, wheel tag, wall time |
| A2 | `from pxr import Usd, UsdGeom, Sdf`; author `bakery.usda` (one Xform with 5 child `Xform` prims carrying custom attrs `brick:part`, `brick:color`, `brick:id`), `module.usda` referencing it twice at two transforms with a `variantSet season {summer, winter}`; `Usd.Stage.Open(...).Flatten()` | success/failure, composed prim count, flattened file size |
| A3 | `usdchecker module.usda`; `usdcat --flatten` | pass/fail text verbatim |
| A4 | Blender.app (native): `File › Import › USD` on `module.usda`; then `blender -b --python-expr` doing the same headless | objects created, custom attrs visible on objects (yes/no), import time |

Also try `import pxr` from Blender's bundled Python and record the result (expected: not available).

**Exit criteria.** A one-row decision in the findings note: `native macOS: OK|FAIL (versions)`, `Blender import: OK|FAIL (attrs preserved: yes/no)`, `Blender python has pxr: yes/no`. The container half of S7 (arm64 Linux) stays with the 011-R2 work order.

## 4. Deliverables

- `spikes/S1/` and `spikes/S7/` with scripts, inputs, outputs, diffs.
- `docs/spikes/S1-studio-round-trip.md` and `docs/spikes/S7-usd-runtime-native.md` — findings only, each under 600 words, tables preferred, `[unverified]` on anything not directly observed.
- One-line summary of each in the commit message. Commits follow the repo's attribution convention.

James's hands-on part is limited to: pressing Save As in Studio seven times, and confirming the register number before dispatch.
