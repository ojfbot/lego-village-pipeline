---
correspondence_schema: lego-pipe-memo/v2
memo: HANDOFF-LEGO-PIPE-032
revision: R1
status: for_review
memo_type: work_order
title: "Register migration — operator-ratified work order (R1: the accepted R0 plan with every docket item decided; still plan-only)"
date: 2026-09-20
thread: correspondence-governance
tags: [register, migration, work-order, ratified, docket, version-journal, allocation-ledger, finalization, lint, freeze, rehearsal, canary, plan-only]
from:
  actor: Claude Code
  role: implementation_work_order_author_and_implementing_agent_on_the_separate_implementation_pr
to:
  - actor: James
    role: operator_and_final_authority_whose_docket_this_revision_records
  - actor: ChatGPT
    role: merge_train_lead_and_exact_head_reviewer
    provider: OpenAI
  - actor: Claude (Cowork)
    role: independent_protocol_and_migration_fidelity_reviewer
    provider: Anthropic
argument: >
  In which the register-migration work order returns from its review rounds as the plan the
  operator accepted at an exact head, with all fourteen docket items answered as James ratified
  them and nothing else changed; the parameterized branches R0 carried for the undecided
  questions collapse to the ratified ones — an all-main cutover freeze after the cut-R2 import
  PR lands, six resolution records for the versions with no bytes of their own, the migration
  PR's own version from the first real finalizer run, registered implementation reviews under
  numbers that are now allocated identities; the boundary is kept exactly where R0 put it —
  one later atomic implementation PR, and no tool, schema, workflow, setting, allocation
  artifact or register edit in this revision; and the implementation is bound to remeasure its
  real protected-main base after the freeze opens rather than reuse the figures this plan was
  reasoned on.
provenance:
  source_artifacts:
    - {name: "HANDOFF-LEGO-PIPE-032-R0 at PR #21 head 48bcbf50a2e10ec5495169b165d740fd98b74deb, memo sha256 d7980999a57231585cd0fbdcc8fe53302c7c0dc221656d3eac3e4bf59c4861ea", role: "the accepted plan this revision ratifies; every section reference below (R0 §n) is to that exact head's bytes; R0 stays on disk unchanged and remains the full technical specification"}
    - {name: "James's operator decision docket, PR #21 comment 5752476543 (2026-09-20T20:32:48Z), https://github.com/ojfbot/lego-village-pipeline/pull/21#issuecomment-5752476543", role: "the authority for every Q-01…Q-14 answer recorded in §2; relayed through the Codex train lead; decisions only — it makes no merge, implementation, register edit, settings change or allocation artifact, and neither does this revision"}
    - {name: "PR #21 review record: Codex TR-32-01…03, TR-32-R2-01…05, TR-32-R4-01…03; Cowork CW-32-01…09, CW-32-R3-01…08; lead reconciliations RR-32-01…11, RR-32-R3-01…09, RR-32-R4-01/02", role: "the five repair rounds R0 passed through between 20af9f54 and 48bcbf50; all closed at the accepted head; nothing in them is reopened here"}
    - {name: "canonical main 582fb63d63c3f9188516faade67fd6a8116287a3 (register 2026-09-18.31)", role: "R0's plan base and still the base of this branch; the migration's own base will be later and must be remeasured (§6)"}
  method: >
    Transcription, not re-derivation: each ratified answer is copied from the decision comment
    and placed against the R0 section it settles; where an R0 passage was written as a
    parameterized choice, this revision states which branch is now in force and what that
    changes in R0's worked examples. No measurement in R0 is re-run here, on purpose — §6 binds
    the implementation to re-run all of them at its real base. No artifact outside this memo and
    the deviation log was touched.
authority:
  decision_owner: James
register:
  number: "032"
  allocated_by: "James, 2026-09-20 — PR #21 decision docket (comment 5752476543), Q-01, relayed through the Codex train lead; revision R1 consumes no number (rule 8)"
register_version_read: 2026-09-18.31
in_reply_to:
  memo: CORR-LEGO-PIPE-031
  revision: R0
supersedes: HANDOFF-LEGO-PIPE-032-R0
findings:
  - {id: N-01, summary: "Carried from R0: at 582fb63 the version line is 39,268 bytes, 30 versions, 24 own-note slices, 70-byte preamble; .2–.7 live inside .8's bytes — a plan-base figure, to be remeasured at the migration base (§6)"}
  - {id: N-02, summary: "Carried from R0: the naive seam rule yields one spurious boundary; the manifest is reviewed data and the adversarial fixture (R0 G-02) is required"}
  - {id: N-03, summary: "Carried from R0: at 582fb63 all three merge methods are enabled and no status check is required — now to be changed by James under Q-06/Q-09, read and posted before approval (R0 §8 step 7)"}
  - {id: N-06, summary: "Carried from R0 and recurring here: this revision, like R0, is committed to the unmerged draft branch under docs/correspondence/ with no register bump; logged again in implementation-notes.md (§7); the policy itself is settled by Q-02/Q-10 and takes effect only when the migration PR merges"}
  - {id: Q-01, summary: "Ratified: 032 = this work order (HANDOFF); 033 = Cowork implementation review (REVIEW); 034 = Codex implementation review (REVIEW); 035 = post-migration as-built/canary report (CORR) — allocated identities from 2026-09-20; no register row changes until the migration lands"}
  - {id: Q-02, summary: "Ratified: one register version per accepted landing transaction"}
  - {id: Q-03, summary: "Ratified: versions assigned only during finalization against protected main; branches carry pending notes, never claimed versions"}
  - {id: Q-04, summary: "Ratified: one immutable per-version file"}
  - {id: Q-05, summary: "Ratified: the enumerated authority set rooted at REGISTER.md; no generated REGISTER-LOG.md in slice 1"}
  - {id: Q-06, summary: "Ratified: disable squash and rebase merging repository-wide; retain merge commits; do not require linear history"}
  - {id: Q-07, summary: "Ratified: all-main cutover freeze, opened after the cut-R2 import PR lands, running from first finalization through exact-head approval and James's merge; the only exception is a James-authorized security/outage fix, which forces a renewed finalization and check"}
  - {id: Q-08, summary: "Ratified: the landing PR's author finalizes; the other steward reruns --check; Codex verifies the exact head"}
  - {id: Q-09, summary: "Ratified: register-lint becomes a required check on main"}
  - {id: Q-10, summary: "Ratified: the migration PR updates the per-commit-bump policy text and tool references in REGISTER.md, AGENTS.md and CLAUDE.md"}
  - {id: Q-11, summary: "Ratified: option (a) — .2–.7 preserved as six resolution records into .8's bytes, each with anomaly data; lowest_version is .2"}
  - {id: Q-12, summary: "Ratified: self-hosting — the migration PR receives its own version from the first real finalizer run, after the rehearsal; no bootstrap-kind record is produced"}
  - {id: Q-13, summary: "Ratified: update the 030/031 status cells and make next-free derived from the allocation ledger"}
  - {id: Q-14, summary: "Ratified: implementation reviews are registered memos 033/034 with content pins"}
parts:
  "0": "Status, pins and what this revision is"
  "1": "What R1 changes relative to R0, and what it does not"
  "2": "The ratified docket, Q-01 through Q-14, placed against R0"
  "3": "Allocations 032–035: identities now, rows later"
  "4": "The plan as it now stands — R0 with the branches collapsed"
  "5": "Boundary: nothing implemented here; one later atomic PR"
  "6": "Remeasure at the real base — the standing instruction to the implementer"
  "7": "This commit's deviation, recorded"
---

# HANDOFF-LEGO-PIPE-032 R1 — Register migration, operator-ratified work order

**Status: for review — plan only, still non-operative.** This revision records James's answers
to every docket item and changes nothing else about the plan. It does not implement, it does not
edit the register, and PR #21 remains a draft that is not to be merged as it stands. The
implementation happens in a **separate** PR, opened only after this revision has passed
exact-head review (Codex, then Cowork's narrow confirmation).

## §0 Status, pins and what this revision is

| Pin | Value |
|---|---|
| Decision authority | James / `@ojfbot`, relayed through the Codex train lead |
| Decision comment | https://github.com/ojfbot/lego-village-pipeline/pull/21#issuecomment-5752476543 (posted 2026-09-20T20:32:48Z) |
| Plan accepted at | PR #21 head `48bcbf50a2e10ec5495169b165d740fd98b74deb` |
| R0 memo sha256 at that head | `d7980999a57231585cd0fbdcc8fe53302c7c0dc221656d3eac3e4bf59c4861ea` |
| R0 file | `docs/correspondence/HANDOFF-LEGO-PIPE-032-R0-register-migration.md` — **unchanged by this commit**, byte-identical to the accepted head; every "R0 §n" below is that file |
| Base of this branch | canonical `main` `582fb63d63c3f9188516faade67fd6a8116287a3`, register `.31` — unchanged; the register is untouched |
| Relationship | R1 **supersedes** R0 under rule 6 (same author, recipients, authority, purpose, scope; revision consumes no number). R0's bytes stay on disk because the decision comment and five review rounds cite them by hash |

R1 is deliberately short. R0 is the full technical specification — target shape, artifacts,
finalization algorithm, guarantee → artifact → test table, lint tiers, cutover, rehearsal,
canary, ownership — and it was written so that each open question was a labelled branch. R1's
job is to say which branch is now in force at each of the fourteen places, to convert the
proposed numbers into allocated identities, and to restate the boundary. An implementer reads R0
for *how* and R1 for *which*.

## §1 What R1 changes relative to R0, and what it does not

**Changes.** (1) Each Q-01…Q-14 is now a ratified decision, not a docket item (§2). (2) R0's
parameterized worked examples (the "Q-11(a)/Q-11(b)" pairs, the "if Q-12 self-hosts" clauses,
the Q-07 scope choice) collapse to one branch each (§4). (3) 032–035 are allocated identities
(§3). (4) The implementer is bound to remeasure at the real base (§6).

**Does not change.** The target shape (R0 §3), the artifact inventory (R0 §4, all twelve items
plus 4a), the finalization algorithm and its refusal codes RF-01…RF-04 (R0 §5), the guarantee
table G-01…G-16a with its checks RL-01…RL-18 and mutation cases (R0 §6), the lint tiers (R0 §7),
the cutover and review/repair loop (R0 §8/§8a), the acceptance outcomes AO-01…AO-19 and the
rehearsal (R0 §9), the ownership table and the 027/028/029 constraints (R0 §10), the risks and
non-goals (R0 §11), the proposed register delta text (R0 §13). None of the five review rounds'
closures is reopened. No new finding is raised; the N-ids and Q-ids declared here are R0's, carried
so that this memo can cite them.

## §2 The ratified docket, Q-01 through Q-14, placed against R0

Each row: the item, James's answer **exactly as ratified**, the R0 location it settles, and the
effect on R0's text. The middle column is transcription from the decision comment; nothing is
paraphrased into a stronger or weaker claim.

| Item | Ratified decision (verbatim from the docket) | Settles R0 at | Effect |
|---|---|---|---|
| **Q-01** | Allocate 032 = HANDOFF work order; 033 = Cowork implementation review; 034 = Codex implementation review; 035 = post-migration as-built/canary report. | R0 §12 Q-01; R0 §10 "As-built report" row; R0 §13 proposed delta | §3 below. The as-built is 035, a CORR — not 032-R2 |
| **Q-02** | One register version per accepted landing transaction. | R0 §12 Q-02; R0 §5; R0 §6 G-16 | The per-landing unit is policy; RL-10/G-16 enforce it; Q-10 changes the text that said otherwise |
| **Q-03** | Assign versions only during finalization against protected `main`; branches carry pending notes, never claimed versions. | R0 §12 Q-03; R0 §5 algorithm; R0 §6 G-07 (RL-11) | Branch-time version claims end with the migration landing; `register_version_read` stays the only version a memo states |
| **Q-04** | One immutable per-version file. | R0 §12 Q-04; R0 §3 tree `register/versions/`; R0 §6 G-04 (RL-09) | `REGISTER-LOG.md` as a writable log is not built |
| **Q-05** | Enumerated authority set rooted at `REGISTER.md`; no generated `REGISTER-LOG.md` in slice 1. | R0 §12 Q-05; R0 §3 authority declaration; R0 §6 G-09 (RL-03) | The authority sentence in R0 §3 lands verbatim in the migration PR; `register_lint.py render` remains the on-demand reading surface; RL-15 (drift check for a generated view) is not built |
| **Q-06** | Disable squash and rebase merging repository-wide; retain merge commits; do not require linear history. | R0 §12 Q-06; R0 §4 item 11 (Rule 18); R0 §6 G-11/G-11a (RL-18); R0 §8 step 7; AO-14 | James changes the settings and the migration PR adds Rule 18 to `REGISTER.md`; AO-14 runs in its **enforcing** state; RL-18's ratchet applies from the landing |
| **Q-07** | **All-`main` cutover freeze**, after the cut-R2 import PR lands. The freeze runs from first finalization through exact-head approval and James's merge; only a James-authorized security/outage fix is an exception, with a renewed finalization and check. | R0 §12 Q-07 (scope **a**, timing **ii**); R0 §8 step 2; R0 §8a step 2; R0 §11 "Exact-head freshness" | §4 below states it precisely. R0's scope-(b) retry-churn text becomes the description of the one exception path, not of the ordinary case |
| **Q-08** | Landing-PR author finalizes; the other steward reruns `--check`; Codex verifies the exact head. | R0 §12 Q-08; R0 §5 "Who runs it"; R0 §8a; AO-09, AO-19 | As recommended; AO-19's CI merge-base check remains the unattended backstop |
| **Q-09** | `register-lint` becomes a required check on `main`. | R0 §12 Q-09; R0 §4 item 10; R0 §6 G-15; R0 §8 step 7 | James makes it required; AO-14's read includes the required-check state |
| **Q-10** | The migration PR updates the per-commit-bump policy text and tool references in `REGISTER.md`, `AGENTS.md`, and `CLAUDE.md`. | R0 §12 Q-10; R0 §4 items 11–12 | In the migration PR, not a separate one; the three files change only in those sentences |
| **Q-11** | Preserve `.2`–`.7` as six resolution records into `.8`'s bytes, with anomaly data. | R0 §12 Q-11 (option **a**); R0 §4 items 2, 3, 5, 8; R0 §6 G-03, G-03a, G-03b, G-03d; AO-04 | Every "Q-11(a) worked example" in R0 is now simply the specification: 30 migrated records at the plan base, `lowest_version: .2`, the `.2` record carries `previous_version: null`, six `resolutions[]` entries each with `shared_slice: true` and an anomaly id. The Q-11(b) counterparts in R0 are inert |
| **Q-12** | The migration PR receives its own version from the first real finalizer run, after rehearsal. | R0 §12 Q-12 (self-hosting); R0 §4 item 3 per-kind table; R0 §6 G-16/G-16a (RL-17); AO-17; R0 §8 step 8 | The migration PR's own version is an ordinary `kind: finalized` record; **no `kind: bootstrap` record is produced** (that kind exists in the schema only for the alternative James did not take, and RL-17's "at most one" reads as "zero" in this repository); the canary is the second finalizer run |
| **Q-13** | Update 030/031 status cells and make next-free derived from the allocation ledger. | R0 §12 Q-13; R0 §4 item 11; R0 §6 G-13 (RL-13 whitelist) | RL-13's permitted-row set in the migration PR is exactly: the 032 row added, the 030 and 031 status cells, the next-free row's prose replaced by the derived pointer. Every other data row byte-identical |
| **Q-14** | Implementation reviews are registered 033/034 memos with content pins. | R0 §12 Q-14 and Q-01; R0 §8a; R0 §10 review rows | Cowork files `REVIEW-LEGO-PIPE-033`, Codex files `REVIEW-LEGO-PIPE-034`, each pinning the reviewed head by sha **and** content digest (R0 §10 constraints); one of them is the natural canary landing (R0 §9) |

## §3 Allocations 032–035: identities now, rows later

From 2026-09-20, by Q-01, these are **operator-allocated identities** (rule 1: James allocates;
rule 2: allocation is recorded as reserved before drafting):

| Number | Identity | Author | Purpose |
|---|---|---|---|
| 032 | `HANDOFF-LEGO-PIPE-032` (this work order, R0 accepted, R1 ratified) | Claude Code | the plan |
| 033 | `REVIEW-LEGO-PIPE-033` | Claude (Cowork) | independent review of the implementation PR; content-pinned |
| 034 | `REVIEW-LEGO-PIPE-034` | ChatGPT / Codex | independent review of the implementation PR; content-pinned |
| 035 | `CORR-LEGO-PIPE-035` | Claude Code | post-migration as-built and canary report |

**No canonical register row changes now.** The register at `.31` still reads `032+` as next free
and has no row for any of these. Under rule 13 and the register's own first paragraph, an
allocation takes effect as register data only when merged to canonical `main`; under Q-03, no
branch claims the version that landing will receive. The four allocations therefore enter the
register **in the atomic migration landing itself**: as `reserved`/`in_flight` entries in
`register/ALLOCATIONS.yaml` (R0 §4 item 4), as the 032 row R0 §13 already drafted, and as the
derived next-free pointer `036+` (Q-13). Until that landing, the decision comment pinned in §0
is the record of the allocation, and any mirror or memo that needs to cite 033–035 cites it. If
the migration never lands, the four numbers stay consumed (rule 2) and are recorded as such in
whatever landing next touches the register.

## §4 The plan as it now stands — R0 with the branches collapsed

R0 stands in full. The following restates, in plain words and in one place, what each ratified
answer makes true of it, so that no implementer or reviewer has to reconstruct the state from
fourteen table rows.

**Freeze (Q-07), stated precisely.** The freeze is **all-`main`**: from the moment the first
finalization commit is made on the migration branch until James's merge commit lands, **no pull
request of any kind merges to `main`** — not correspondence, not code, not documentation. It
opens **after the cut-R2 import PR has landed** (R0 §12 Q-07 timing (ii): the week of
2026-09-28, once cut R2's import is on `main` under the current rules with one more manually
assigned version). The lead opens it by naming base commit `B` (R0 §8 step 2) and closes it on
AO-16 (the canary green on `main`, verified by the other steward). **The single exception:** a
security or outage fix that James authorizes **by name**, in the PR thread, before it merges.
Such a fix advances `main`, so it **forces a renewed finalization and a renewed `--check`** —
RF-03 (R0 §5 step 4) refuses the stale finalization, the author merges `origin/main` and reruns,
the other steward re-posts `--check` against the new `observed_main`, and Codex re-verifies the
new exact head; the exception and its consequence are recorded in the PR. Nothing else is an
exception. Consequence, from R0 §11: because the freeze is all-`main`, strict serialization is
bounded — a finalization and its `--check` stay valid until the merge unless the named exception
fires. R0's description of retry churn under a correspondence-only freeze describes the
exception path only, never the ordinary one.

**Data shape (Q-11(a)).** At the plan base: 30 `kind: migrated` records, `.2`–`.31`; 24 with a
`slice` of their own (`.8`–`.31`), 6 with a `resolution` into `.8`'s slice (`.2`–`.7`), each of
the six carrying `shared_slice: true` and its anomaly id; `lowest_version: .2`; the `.2` record
carries `previous_version: null` and no other record does. These counts are the plan-base
figures and are remeasured under §6; the *shape* is fixed.

**The migration PR's own version (Q-12).** Produced by `register_finalize.py`'s first real run,
after the two-branch rehearsal (R0 §9) has passed in the battery and live, as the last commit on
the migration branch — an ordinary `kind: finalized` record with `finalized_from_main` naming
the freeze's base `B` (or its successor if the Q-07 exception fired). The canary (R0 §9) is the
finalizer's **second** run. No `bootstrap` record exists in this repository.

**Merge method and required check (Q-06, Q-09).** James disables squash and rebase merging
repository-wide, keeps merge commits, does not enable required linear history, and makes
`register-lint` a required check on `main` — **before** §8a step 5's approval confirmation (R0
§8 step 7, RR-32-R4-02). ChatGPT posts AO-14's read against the review head in its enforcing
state. The migration PR adds Rule 18 to `REGISTER.md` (R0 §4 item 11); RL-18's ratchet applies
from the moment that lands.

**Rows (Q-13).** The migration PR's permitted changes to the correspondence table are exactly
the 032 row, the 030 and 031 status cells, and the next-free row; RL-13 whitelists those and
nothing else; the instruments table is byte-identical (RL-14).

**Reviews (Q-14, Q-08).** The implementation PR is reviewed independently and before contact by
Cowork (as 033) and Codex (as 034), each rerunning every pre-merge outcome it verifies
(AO-01…AO-15, AO-17…AO-19) and pinning the reviewed head by sha and content digest; the landing
author finalizes; the other steward reruns `--check`; Codex verifies the exact head; James
merges by merge commit (R0 §8a). AO-16 follows the merge.

**Policy text (Q-10, Q-02).** In the migration PR, the sentence "every commit that touches
`docs/correspondence/` bumps the register version line" is replaced, in `REGISTER.md`,
`AGENTS.md` and `CLAUDE.md`, by the per-landing sentence and the tool references (R0 §4 items
11–12). Until that PR merges, the old sentence stands — which is why §7 records this commit's
departure from it rather than claiming the new rule already applies.

## §5 Boundary: nothing implemented here; one later atomic PR

This revision, like R0, **builds nothing**. Specifically, this commit adds this file and one
bullet in `implementation-notes.md`, and touches no other path: **no** `tools/register_*.py`,
**no** `tools/schemas/register-version.v1.schema.json`, **no** `.github/workflows/register-lint.yml`,
**no** `register/` directory or any file under it, **no** `tests/test_register.py`, **no**
repository-settings change, **no** allocation artifact, **no** edit to `REGISTER.md`, `AGENTS.md`
or `CLAUDE.md`, and **no** edit to R0. The ratified decisions are recorded here; they are
*executed* only in **one later, separate, atomic implementation PR** (R0 §4: all twelve items
plus 4a, landing together, James-merged), opened after this revision passes exact-head review
and after the Q-07 freeze opens. PR #21 stays a draft and is not merged as it stands — it is the
review record for the plan, and merging it would itself be a correspondence landing needing a
version under either the old rule or the new.

## §6 Remeasure at the real base — the standing instruction to the implementer

Every number in R0 §2 — 72,260 bytes, 97 lines, 37 data rows, a 39,268-byte version line, 30
versions, 24 slices (N-01), 24 seam candidates of which one is spurious at byte 26,240 (N-02),
283 non-ASCII bytes, the 24 reference slice digests, and the repository-settings read (N-03) —
was measured at `582fb63`. The migration's base `B`
will be later: at minimum the cut-R2 import PR (Q-07 timing) and whatever else lands before the
freeze opens. **The implementation must not reuse any of those figures.** Concretely, and as
acceptance evidence (R0 §9 AO-01…AO-03, R0 §6 G-03c/RL-16):

1. `register_migrate.py` is run against `git show B:docs/correspondence/REGISTER.md` — never
   against a working copy, never against `582fb63` — and the manifest's `base_commit`,
   `source_sha256`, `line_sha256`, `line_bytes`, `version_count`, `slice_count`,
   `resolution_count`, `lowest_version`, every slice digest and every seam offset are **recomputed
   at `B`** and committed as measured there.
2. The seam manifest is read afresh by both stewards **at `B`** (AO-03). The one spurious
   candidate at `582fb63` may be joined by others in notes written since; the descending-by-one
   rule is re-applied and every rejected candidate re-justified. R0's adversarial fixture (G-02,
   AO-18) is rebuilt from `B`'s bytes, not `582fb63`'s.
3. The row-identity baseline for RL-13/RL-14 (AO-12) is `B`'s data-row set, whose count will
   exceed 37 if cut R2 added an instruments row.
4. The corpus differential (AO-11) is taken between `B` and the migration head, not between
   `582fb63` and anything.
5. `lowest_version` is confirmed `.2` at `B` by reading the line, not assumed from R0.
6. The PR body states `B`, `sha256(REGISTER.md @ B)`, and the recomputed figures side by side
   with R0's `582fb63` figures, so a reviewer can see exactly what moved. A figure that is quoted
   from R0 rather than recomputed at `B` is a defect in the evidence block, of the kind 029's
   third finding names.

R0 §2's figures remain useful as the plan's worked example and as the thing the reviewers
reproduced five times; they are not the migration's inputs.

## §7 This commit's deviation, recorded

This commit adds a file under `docs/correspondence/` and does not bump the register version line
— the same departure R0's commits made, for the same reason, and logged the same way (N-06):
the register is not to be edited before the atomic landing (§3, §5), and no version is claimed on
a branch (Q-03). The factual bullet is appended to `implementation-notes.md` `## Deviations` in
this commit. The rule that makes this a departure is the one Q-02/Q-10 retire — but it retires
only when the migration PR merges, so until then the departure is recorded, not excused.

— Claude Code, implementing agent on the separate implementation PR · register version read
`2026-09-18.31` · canonical `main` `582fb63` · number 032 allocated by James 2026-09-20 (PR #21
decision docket) · R1 supersedes R0 (rule 6) · nothing implemented · PR #21 not to be merged.
