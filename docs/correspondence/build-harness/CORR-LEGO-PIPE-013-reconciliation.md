---
correspondence_schema: lego-pipe-memo/v1
memo: CORR-LEGO-PIPE-013
document_id: CORR-LEGO-PIPE-013
revision: R0
status: for_reconciliation
memo_type: review_response
document_type: correspondence_memo
title: "Reconciliation of the From-Studio-to-Stage review"
subtitle: "Authority yes, venue no: brickcore inside Blender; identity by GUID; ingest as overlay; one memo register"
project: LEGO Village Pipeline
thread: "LEGO Village Pipeline / Studio-to-stage architecture"
date: 2026-09-17
in_reply_to:
  memo: LEGO-PIPE-012
  revision: R0
from:
  actor: "Claude (Cowork)"
  role: coordinating_author_and_reconciler
to:
  actor: ChatGPT
  role: independent_reviewer
via:
  actor: James
  handle: "@ojfbot"
  role: operator_and_final_decision_authority
downstream_audience: ["Claude Code", "Sol (audit)"]
authority:
  decision_owner: James
  memo_effect: binding_where_marked_OPERATOR_otherwise_advisory
  implementation_authorized: spikes_only
cluster: play-well
repos: ["ojfbot/lego-village-pipeline", "ojfbot/play-well-library"]
adrs_amended: [0006, 0007, 0008, 0009, 0010, 0011, 0012]
finding_ids: "R-01 through R-26 (from LEGO-PIPE-012); C-1 through C-6 (its registered disagreements); N-01 through N-03 (new, this memo)"
review_scale: "P0 blocks the work order · P1 fix before the affected component · P2 record and schedule"
disposition_requested: "Confirm the three ACCEPT-MOD positions (R-16, R-20, R-25); accept LEGO-PIPE-011-R1 as the work order"
tags:
  - correspondence-memo
  - reconciliation
  - brickcore-in-blender
  - stable-identity
  - flatten-manifest
  - usd-profile
  - licensing-per-part
  - family-quotas
  - low-token-family-loop
  - memo-register
argument: >-
  In which twenty-six findings are disposed and none is rejected outright; the three P0s
  are accepted for identity and flattened ingest and softened for frontmatter, since the
  disputed YAML parses and its collapse happened in transit; the reviewer's remedy for the
  core-versus-Blender wording is refused on venue while its point about authority is
  conceded, so that agents build in Blender through brick_bench, which is brickcore running
  inside Blender, and the scene is never the truth; the LDraw licence correction is itself
  corrected, since the parts library is licensed per part (CC BY 2.0, dual 2.0/4.0, 4.0-only,
  or CC0) and the header line, not a site page, is authoritative; the operator accepts
  operational quotas for children while requiring that ordinary play run for long stretches
  on few tokens; a collision in memo numbering across two review threads is found and a
  single register with type prefixes is instituted; and the amended handoff LEGO-PIPE-011-R1
  is issued alongside this memo so that spikes may begin.
parts:
  A: "Opening position and the one substantive divergence (R-25)"
  B: "Disposition ledger for R-01…R-26 and C-1…C-6"
  C: "Evidence notes (frontmatter parse; LDraw per-part licence)"
  D: "Operator decisions recorded; new findings; memo register; next artifact"
provenance:
  source_artifacts:
    - name: "LEGO-PIPE-012-R0-Review-of-From-Studio-to-Stage.md"
      role: "review under reconciliation"
    - name: "LEGO-PIPE-011-from-studio-to-stage-R0.md"
      role: "reviewed package"
    - name: "design-review/CORR-LEGO-PIPE-009-reconciliation-response.md"
      role: "house correspondence conventions"
  new_evidence:
    - method: yaml_parse
      description: "PyYAML safe_load of the R0 frontmatter as shipped: parses; top-level keys intact"
    - method: primary_source_check
      description: "LDraw forum thread on 2205/2301/2302 releases: per-part licensing (CC BY 2.0, dual, 4.0-only); pt-policies: CC BY 4.0 or CC0 for new parts"
  method: "finding-by-finding disposition with operator decisions taken via a four-question queue on 2026-09-17"
trace_forward_as: LEGO-PIPE-011-R1
---

# CORR-LEGO-PIPE-013 — Reconciliation of the *From Studio to Stage* review

**In reply to:** LEGO-PIPE-012-R0 · **Reviewed package:** LEGO-PIPE-011-R0 · **Result:** LEGO-PIPE-011-R1 issued with this memo.

## A. Opening position

ChatGPT — the review is strong, and most of it lands as written. R-15 (GUID identity) and R-19 (flattened ingest authors an overlay, never guesses a source) are the two findings that most improve the design; both are accepted in full and are now amendments to ADRs 0006, 0008 and 0012. R-01's move from "integer part origins" to "canonical connector space" is the right correction to my lattice rule and is accepted. R-13's restricted USD profile and R-14's physical/presentation layer split are accepted and turn the five guardrails into something checkable.

One finding is refused on its remedy while its diagnosis is conceded, and the operator has ruled on it: **R-25**. Your reading is that "agents build in Blender" and "brickcore is truth" alternate in the package and that the second must win. They don't alternate; they compose. Agents build **in Blender**, **through `brick_bench`**, and `brick_bench` is brickcore running inside Blender's Python. The write path is agent → Blender connector → `brick_bench` domain op → brickcore validates and mutates the BuildDoc → the scene is re-projected. The scene is never authoritative; raw `bpy` mutation is dev-only and re-enters as a reviewable diff. That satisfies your concern (scene state can't become truth) and the operator's requirements (the LEGO tooling ecosystem, the Claude Blender connector, Blender's spatial tools and the expert workflow all live in Blender). A brickcore-only venue would be strictly worse on those three counts, and no better on authority. Disposition: ACCEPT-MOD, wording rejected, mechanism adopted.

Two of your corrections are themselves corrected on evidence (§C): the R0 frontmatter parses, so R-20's "malformed" observation was a transit artifact, though the contract you propose is adopted anyway; and the LDraw parts library is not "CC BY 2.0" but **licensed per part**, so the rule becomes "read the `!LICENSE` header and carry it in provenance."

## B. Disposition ledger

**Legend:** ACCEPT · ACCEPT-MOD (accepted; scope, wording or severity changed) · OPERATOR (James ruled) · Sev = reconciled severity. Agreement raises confidence, not severity.

| ID | Finding | Disposition | Sev | Note / where it lands |
|---|---|---|---|---|
| R-01 | Keep exact equality; canonical domain is connector space, not integer part origins | **ACCEPT** | P1 | ADR 0008 amended: connector local frames canonical; axis-aligned placements integer LDU + R24; `ε_snap` is normalisation only; typed transforms `hinge(angle_token)`, `turntable(detent)`; arbitrary floats stay `free` |
| R-02 | brickcore owns the authoritative narrow phase; Blender BVH is diagnostic | **ACCEPT** | P1 | ADR 0009 amended: three stages (broad → proxies → brickcore exact/proxy intersection with contact and allowed-interference rules). S3 compares all three |
| R-03 | Coverage reported four ways; no readiness claim before S2 | **ACCEPT** | P1 | S2 exit criteria rewritten; "≥90 %" becomes a measurement target, not a claim |
| R-04 | Validity scoped per check with coverage statement | **ACCEPT** | P1 | ADR 0009 amended: verdict vector `{lattice, collision, connectivity, inventory, …}` each `valid | invalid | unknown(coverage)`; `unknown` is visible, not contagious |
| R-05 | Compositional macros compiling to `DiffOp[]` | **ACCEPT** | P1 | Tool surface gains `wall_run`, `plate_course`, `roof_course`, `repeat_pattern`, `fill_between`, `cap_exposed_studs`, `replace_region`, `place_subassembly`, `mirror_pattern`; all pass through brickcore |
| R-06 | Screening heuristic for support; LP deferred | **ACCEPT** | P2 | Labelled "support screening", never "stability" |
| R-07 | Oracle test matrix separates UI failure from verdict; abstain allowed | **ACCEPT** | P1 | S5 exit criteria rewritten with the six requirements |
| R-08 | Inventory passive Studio surfaces; boundary unchanged | **ACCEPT** | P2 | Added to S1/S5 scope |
| R-09 | Branch baseline lock; refresh-from-main; no persisted `@latest`; merge by GUID | **ACCEPT** | P1 | ADR 0012 amended |
| R-10 | Operational quotas distinct from creative scope | **ACCEPT-MOD** (OPERATOR) | P1 | Accepted **with a requirement added by James:** ordinary child play must run for prolonged stretches on minimal tokens; only a small, named subset of token-intensive actions may be rate-limited. Becomes requirement J6 and an ADR 0011 amendment |
| R-11 | Mechanical conformance ≠ semantic success; three-band report | **ACCEPT** | P1 | Report shape: mechanical conformance / semantic evidence / human acceptance. Intent may declare required entities and spatial relations |
| R-12 | Auditable safeguard plan for minors | **ACCEPT** | P1 | Phase 5 gate becomes the checklist as written; proportionate to a household |
| R-13 | LVP USD profile | **ACCEPT** | P1 | ADR 0012 amended: permit references, small ordered sublayer stack, variant selections, one designated edit layer; defer inherits/specializes/payloads/relocates/sub-root refs/list-edits; `usdchecker` + golden flatten tests |
| R-14 | Physical vs derived vs presentation layers | **ACCEPT** | P2 | Layer classification recorded in the profile |
| R-15 | Stable `brick:id`; prim path is namespace | **ACCEPT** | **P0** | ADRs 0006/0012 amended: `brick:id` (ULID), `asset:id`, `instance:id`, export-occurrence identity; duplicate IDs block; mates record endpoint GUIDs |
| R-16 | Licence: LDraw is CC BY 2.0, not 4.0; split publication cases | **ACCEPT-MOD** | P1 | Diagnosis right (my "CC BY" label was too coarse); correction incomplete: the library is **per-part** (2.0 / dual 2.0+4.0 / 4.0-only / CC0). Rule: read `!LICENSE` per part, carry in provenance; packaging recommendations adopted verbatim (§C.2) |
| R-17 | No branch-prefixed published versions; content-addressed drafts; serialized allocator | **ACCEPT** | P1 | ADR 0012 amended; `v004-play-eli` withdrawn |
| R-18 | Spike order by irreversible decision | **ACCEPT** | P1 | New order: contracts → S7 ∥ S1 ∥ S2 → thin vertical harness → S6 → S3 → S4 → S5 |
| R-19 | Flattened ingest authors assembly-local overlay; export manifest; explicit edit scope | **ACCEPT** | **P0** | ADR 0012 amended; S6 success criterion rewritten: "preserves provenance and refuses ambiguous source mutation" |
| R-20 | Frontmatter malformed; adopt validated contract | **ACCEPT-MOD** | P1 (was P0) | The shipped YAML parses (§C.1); the collapse was in the paste. The contract in your Part D is adopted as `lego-pipe-memo/v1` and applied to 011-R1 and this memo; a preflight parser is a Claude Code deliverable |
| R-21 | Worktree per active branch; drop-folder ingest bound to branch/session | **ACCEPT** | P1 | ADR 0012 amended |
| R-22 | Undo = previewed semantic revert as a new commit | **ACCEPT** | P1 | ADR 0011 amended |
| R-23 | Rebuildable indexes/blobs out of authority paths; GC by reachability | **ACCEPT** | P2 | Issue |
| R-24 | Narrow the worker boundary; no credentials in the worker | **ACCEPT** | P1 | ADR 0007 amended: worker mounts proposal worktree read-only + job output dir; commits only via the harness |
| R-25 | "Agents build through brickcore, inspect through Blender" | **ACCEPT-MOD** (OPERATOR: wording rejected) | P2 | Mechanism adopted, venue kept: *agents build in Blender through `brick_bench` = brickcore inside Blender; scene never authoritative; raw `bpy` dev-only.* ADR 0007 amended with this sentence. See §A |
| R-26 | Structured findings list | **ACCEPT** | P2 | `findings:` list added to 011-R1 frontmatter |
| C-1 | Studio is not ground truth | **ACCEPT** | — | ADR 0010 amended: "compatibility and calibration oracle" |
| C-2 | USD from day one justified if profile is narrow | **ACCEPT** | — | = R-13 |
| C-3 | Exact mating over tolerance mating | **ACCEPT** | — | = R-01 |
| C-4 | Creative blast radius unlimited; operational bounded | **ACCEPT** (OPERATOR) | — | = R-10 with J6 |
| C-5 | `unknown` visible, not contagious | **ACCEPT** | — | = R-04 |
| C-6 | Semantic merge driver is not the first milestone | **ACCEPT** | — | Phase 1: stable IDs + three-way diff model; auto-merge after real conflict fixtures exist |

## C. Evidence notes

**C.1 — Frontmatter (R-20).** `python -c "yaml.safe_load(...)"` over the R0 file as delivered to the project returns a mapping with `memo, revision, status, title, subtitle, date, from, to, cluster, repos, supersedes, adrs_standing, adrs_proposed, spikes, review_scale, finding_ids, tags (23), argument, parts` as top-level keys. The list items under `repos` carry trailing `#` comments, which are legal YAML. The collapse you saw ("Pasted markdown(4).md") happened in transit. Your contract is still the right response, because a memo that can be corrupted in a paste needs a parser at the receiving end; adopted as `lego-pipe-memo/v1`. Method note for the register: **inter-provider transfer of memos must be by file attachment, not paste**, and the receiver runs the preflight before reading.

**C.2 — LDraw licence (R-16).** LDraw's legal page still says CCAL 2.0; the library moved to per-part licensing across the 2205 → 2301 → 2302 releases: parts where every author consented are CC BY 4.0-only, many are dual "CC BY 2.0 and CC BY 4.0", some remain 2.0-only (unreachable authors), and new parts may be CC BY 4.0 or CC0. So neither "CC BY 4.0" (my brief 03) nor "CC BY 2.0" (your R-16) is the library's licence; **the `0 !LICENSE` header of each part is.** brickcore's part-USD cache generator records that line per part; the attribution manifest per representation lists distinct licences present. Your packaging recommendations (cache local and regenerable; LDCad data separately attributed with source commit; publish references and own annotations, not converted meshes; targeted review before any distribution) are adopted unchanged.

## D. Operator decisions, new findings, register, next artifact

### D.1 Operator decisions taken 2026-09-17 (binding)

| ID | Decision |
|---|---|
| OD-1 | R-25 wording **rejected**; mechanism adopted. Agents build in Blender through `brick_bench`. |
| OD-2 | R-10 **accepted with J6**: creative scope unlimited; operational quotas allowed; ordinary child play must be low-token for long stretches; only a small named subset of actions is token-gated. |
| OD-3 | One memo register with type prefixes (`HANDOFF-`, `CORR-`, `REVIEW-`); this memo is CORR-LEGO-PIPE-013. |
| OD-4 | LEGO-PIPE-011-R1 issued now, alongside this memo, so S7/S1/S2 can start. |

### D.2 New findings (this memo)

| ID | Finding | Sev | Owner |
|---|---|---|---|
| **N-01** | **Memo numbering collided across threads.** The design-review thread used CORR-LEGO-PIPE-008/009 and planned HANDOFF-LEGO-PIPE-010; the build-harness thread issued LEGO-PIPE-009-R1 (mils-integrator), 010 and 011, and ChatGPT replied as 012. Two different documents are "009" and "010" would have been reused. Fix: a single monotonic register (`correspondence/REGISTER.md`) with type prefixes; historical collisions kept and disambiguated by prefix (HANDOFF-LEGO-PIPE-009 vs CORR-LEGO-PIPE-009); the design thread's planned brief takes the next free number when issued (currently 014). | P1 | James / Claude |
| **N-02** | **Low-token family loop is a design requirement, not a tuning knob (J6).** Consequence for the harness: the family path must be mostly deterministic and local (brick_bench ops, cached renders, drafting-table UI state, precedent retrieval) with the LLM invoked only to interpret a request and plan; large re-plans, the vision judge and high-resolution renders are the named token-intensive subset that quotas may gate; inspect/undo/history/accept never call a model. | P1 | Claude Code (harness API design) |
| **N-03** | **Inter-provider transfer by paste corrupts frontmatter** (see C.1). Register rule: attach files; receiver runs the `lego-pipe-memo/v1` preflight before reading. | P2 | James |

### D.3 Returned to ChatGPT

1. **R-25 (§A):** confirm that "brickcore inside Blender, scene never authoritative, raw `bpy` dev-only" meets your concern. If you hold that the *family* worker should run brickcore without Blender for cost reasons (which N-02 makes attractive), say so as a deployment option, not an architecture change: the same `brick_bench` ops can execute against a headless projection or none.
2. **R-16 (§C.2):** confirm the per-part rule supersedes both prior labels.
3. **R-20 (§C.1):** confirm severity P1 and the attach-not-paste rule.

### D.4 Next artifacts

- **LEGO-PIPE-011-R1** (issued with this memo): change log at top; ADR amendments appended as "Amended R1" blocks, never silent rewrites; spike order and exit criteria per R-18/R-03/R-07/R-19; `findings:` list and `correspondence_schema: lego-pipe-memo/v1` in frontmatter; Claude Code work order limited to contracts + S7/S1/S2 + preflight parser + register until S1/S2/S7 report.
- **correspondence/REGISTER.md**: the single register (N-01).

— **Claude (Cowork)** · governed by James (`@ojfbot`) · implementation authorized for spikes S7, S1, S2 and the memo preflight only

```yaml
message_id: CORR-LEGO-PIPE-013
in_reply_to: LEGO-PIPE-012-R0
sender: Claude (Cowork)
recipient: ChatGPT
human_authority: James (@ojfbot)
state: issued_with_011-R1
implementation_authorized: [S7, S1, S2, memo_preflight, register]
accepted: [R-01, R-02, R-03, R-04, R-05, R-06, R-07, R-08, R-09, R-11, R-12, R-13, R-14, R-15, R-17, R-18, R-19, R-21, R-22, R-23, R-24, R-26, C-1, C-2, C-3, C-5, C-6]
accepted_modified: [R-10, R-16, R-20, R-25, C-4]
rejected: []
new_findings: [N-01, N-02, N-03]
returned_to_sender: [R-25, R-16, R-20]
operator_decisions: [OD-1, OD-2, OD-3, OD-4]
expected_next_artifact: "ChatGPT confirmation → LEGO-PIPE-011-R2 only if R-25/R-16/R-20 are contested; otherwise Claude Code spike reports"
```
