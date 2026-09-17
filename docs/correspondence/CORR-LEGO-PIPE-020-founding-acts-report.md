---
correspondence_schema: lego-pipe-memo/v1
memo: CORR-LEGO-PIPE-020
revision: R0
status: for_review
memo_type: findings
title: "Founding-acts report — the play-well cluster stands"
subtitle: "Both repos initialised and pushed; register committed at v.6 and now v.10; correspondence and design package committed with hashes; Northstar PR open; the gaps, verbatim"
date: 2026-09-17
thread: cluster
cluster: play-well
project: LEGO Village Pipeline
from:
  actor: "Claude Code"
  role: implementer
  provider: Anthropic
to:
  - actor: James
    handle: "@ojfbot"
    role: operator_and_final_authority
    provider: operator
  - actor: "Claude (Cowork)"
    role: coordinating_reviewer_and_handoff_author
    provider: Anthropic
in_reply_to:
  memo: HANDOFF-LEGO-PIPE-019
  revision: R0
authority:
  decision_owner: James
  dispatch_authority: James
register:
  number: 020
  allocated_by: "proposed — James confirms (rule: numbers are allocated by the operator)"
  allocated_on: 2026-09-17
repos:
  - ojfbot/lego-village-pipeline
  - ojfbot/play-well-library
tags:
  - founding-acts
  - report
  - play-well
argument: >-
  In which Claude Code reports the founding acts complete in the mandated order —
  register-first commit, version bumps on every correspondence touch, seven of
  seventeen registered documents landed as files with hashes, the design package
  committed as the operator-ruled LATEST superset, both repos pushed private and
  registered in Northstar — and itemises exactly what is still owed and by whom,
  so the record is honest before any Stream A or Stream B work begins.
parts:
  "1": "What was done, in commit order"
  "2": "Hashes of record"
  "3": "Gaps and deviations"
  "4": "What I wait on / what comes next"
provenance:
  source_artifacts:
    - {name: "correspondence/HANDOFF-LEGO-PIPE-019-R0-initial-handover-claude-code.md", role: "the work order this report executes"}
    - {name: "correspondence/REGISTER.md", role: "register, committed at v2026-09-17.6, now v2026-09-17.10"}
  method: "direct execution; every claim below is verifiable in this repo's git history"
---

# CORR-LEGO-PIPE-020 — Founding-acts report

Executes `HANDOFF-LEGO-PIPE-019` §1, reporting per §7.1.

## 1. What was done, in commit order

| Commit | Act | Content |
|---|---|---|
| `5446e6e` | §1.2 | **First commit: the correspondence system.** `docs/correspondence/REGISTER.md` verbatim from the operator-exported copy — **version 2026-09-17.6**, not the `.5` cited in 019 (.6 supersedes .5 and instructs discarding older copies) — plus `tools/preflight.py` (v1 reference, verbatim). Authority transferred on this commit. |
| `c70daee` | §1.2 | Register **v.7**: 019 number confirmed and dispatched by James (2026-09-17); paste transfer recorded as rule-1 deviation with the transcription's sha256 (016 reconstruction precedent). |
| `d8eb371` | §1.3 | Register **v.8** + the seven registered documents on disk, copied never re-typed: 011-R1, 011-R2, REVIEW-012 (alias mirror), CORR-013 (hash-verified), CORR-015 (from its CORR-011 alias, `document_id` unedited), 019-R0 transcription, ROUTING-2026-09-17. Path mapping: registered `correspondence/` prefix = `docs/correspondence/` itself; thread dirs are subdirectories. Preflight on 019 vs the committed register: **exit 0**. |
| `1da34d5` | §1.4 | Register **v.9** + design package **H-01 R1 committed verbatim** to `docs/design/H-01-R1/` — whole `handoff/` tree, 98 files, `standalone/` + `dt/` together; tree diffed file-for-file and spot-checked byte-identical against the archive. |
| `45aac81` | §1.5 | `CLAUDE.md` seeded (019 §8 + package CLAUDE.md); `.claude/northstar.md` (l1-lego-village-pipeline, targets are proposals); `implementation-notes.md` deviations log. |
| `0ba0f4c` (play-well-library) | §1.6 | `ATTRIBUTION.md` (LDraw/OMR CC BY 4.0; LDCad shadow CC BY-SA 4.0; Studio EULA boundary) + branch-flow CI rule (`play/<user>` → `staging` → `main`) + `.claude/northstar.md`. Otherwise empty. |
| core PR **#487** | §1.7 | Both repos registered in Northstar; ladder to `l2-ojfbot` (cluster tier designed-not-built; play-well grouping in registry comments, cluster-golf precedent). `northstar-lint`: 0 errors. Both repos pushed **private** to `ojfbot/…`. |

## 2. Hashes of record

| Artifact | sha256 |
|---|---|
| Design package as committed (`LEGO Village Pipeline LATEST.zip`, 10,013,923 B) | `e5b4857c4f4ed222fee496b1852285d329410ff5ed1023d2a8fbde5f8a6270ce` |
| Design package as reviewed in 019 (`LEGO Village Pipeline 2.zip`, 9,850,637 B) | `e898a64a7057b49ecb8bfdab1654f5b17a0cfe74b5ffbe48a2b69305c95a7789` |
| 019-R0 transcription as committed | `6ba46fc0ea016cccaa6ece551d4af45c85586383adf7cd9ec2cb60de742f1f71` |
| CORR-013 as committed (matches register record `572ce267…`) | `572ce2673e3a2e168df7bf19c8c119fa1e2a6a0692e9d328a626b557ed6d3fd2` |
| REVIEW-012 as received (sender hash still unconfirmed) | `43d25c0d721503b5b2558aa963aec0e16def7e509bf51300b60ab04a97e6ec9a` |

LATEST = the reviewed cut **plus** `ADDENDUM-A1-right-now.md` and three hub captures (states 14–15), added post-review at operator ask; committed by operator ruling 2026-09-17. Nothing reviewed was lost.

## 3. Gaps and deviations

1. **Ten registered rows have no file at the receiver:** legacy review R0 · 008 · 009 · 009-R1 · 010 (build-harness) · 011-R0 · **014-R0** · 016-R0 · 017-R2 · **018-R0**. Rows stand; files land by attachment when exported (rule 1). 014-R0 and 018-R0 matter most: 014 is 019's `in_reply_to` and Stream B's contract; 018 is the spike spec (v2, unratified — cannot act as a work order regardless, per its row).
2. **019 arrived by operator paste**, not attachment — recorded, not repaired, at register v.7.
3. **Register version drift from the memo:** 019 said commit `.5`; the export was `.6`. Committed `.6`.
4. **play-well-library carries one file beyond "attribution + CI rule only":** `.claude/northstar.md`, required by act 7's registry path convention. Flagged for ratification with the northstar proposals.
5. **Northstar targets in both repos are numeric proposals** awaiting operator calibration (core PR #487 note).
6. Desktop file `claude-design-handoff-LEGO-PIPE-007-R1.md` and Downloads file `LEGO-Village-Design-Bundle-Reconciled-Review.md` were **not committed** — neither maps unambiguously to a registered row (007 is registered at R2, inside the design package; the review file may be 008 or the legacy review). Operator identification requested rather than a guess.
7. Tooling: system `python3` lacks PyYAML; preflight runs used a venv interpreter. Input to the 011-R2 preflight-CLI replacement.

## 4. What I wait on / what comes next

- **From James:** confirm number 020 for this report · exports of the ten missing files (014-R0 and 018-R0 first) · identify the two unmapped documents (gap 6) · merge or amend core PR #487 · calibrate northstar numbers · ratify or re-issue 018 (v2 question) when ready.
- **Next, already authorised (no gate):** §7.2 questions-before-contracts batch from 011-R2 §3 + `schema-requests.md` / 014 §7; then S2 and the S7 container half.

— Claude Code, implementer
Under James (`@ojfbot`), who confirms register number 020.
