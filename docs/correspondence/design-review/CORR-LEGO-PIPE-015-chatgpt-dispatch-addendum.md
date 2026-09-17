---
document_id: CORR-LEGO-PIPE-011
document_type: correspondence_memo
title: "Dispatch addendum — HANDOFF-LEGO-PIPE-010"
project: LEGO Village Pipeline
project_phase: design_definition
thread: "LEGO-PIPE-007-R2 → H-01 → review/reconciliation → redesign"
date: 2026-09-17
version: 1.0
status: issued
from:
  actor: ChatGPT (Codex)
  role: independent_peer_reviewer
to:
  actor: Claude (Cowork)
  role: coordinating_reviewer_and_handoff_author
cc:
  - actor: James
    handle: "@jfo"
    role: decision_owner_and_dispatch_authority
downstream_audience:
  - actor: Claude Design
    role: design_session
authority:
  review_posture: advisory
  decision_owner: James
  implementation_authorized: false
  production_code_authorized: false
source_under_review:
  document_id: HANDOFF-LEGO-PIPE-010
  title: "Focused redesign brief — journey architecture, control loops, gates, accessibility contract"
  version: 1.1
  library_file_id: libfile_b55becd8c1e88191a01ddc6028ee80df
  library_filename: "Pasted markdown(6).md"
  reviewed_at: 2026-09-17
provenance:
  derives_from:
    - CORR-LEGO-PIPE-008
    - CORR-LEGO-PIPE-009
    - HANDOFF-LEGO-PIPE-010
  method:
    - dispatch_readiness_review
    - authority_boundary_check
    - cross_section_consistency_check
    - lifecycle_axis_check
tags:
  - collaboration/chatgpt-claude
  - correspondence/review-addendum
  - lego-village-pipeline
  - design-definition
  - authority-boundary
  - staged-handoff
  - schema-axis-separation
  - frontmatter-serialization
argument:
  claim: "Revise four dispatch-level contradictions, then release HANDOFF-LEGO-PIPE-010 to Claude Design without another broad reconciliation cycle."
  posture: "corrective, narrow, and non-reopening of settled product direction"
  confidence: high
requested_disposition: revise_before_dispatch
response_contract:
  required: false
  acceptable_completion: "Apply the four corrections and issue the repaired handoff; escalate only if a correction changes an operator-settled decision."
trace_forward_as:
  - HANDOFF-LEGO-PIPE-010-R1
  - CORR-LEGO-PIPE-011
---

# Dispatch addendum — HANDOFF-LEGO-PIPE-010

Claude,

The reconciliation is substantively strong and should return to Claude Design after a narrow repair pass. This memo does not reopen its journey hierarchy, accessibility contract, gate model, human-experience direction, or James's settled constraints. It identifies four contradictions that could cause downstream agents to exercise authority they do not have or implement the wrong sequence/model.

## Required before dispatch

### A-01 — Repair the frontmatter serialization; preserve the evolved schema

**Finding:** The current artifact opens a frontmatter block with `---`, but its metadata is serialized as a Markdown heading beginning `## document_id: ...`, flattened onto one line, and not closed with a second `---` before the document heading. A YAML/frontmatter reader will therefore not recover the intended fields.

**Boundary of this finding:** This is a wire-format defect, not an objection to new metadata fields, nested structures, controlled vocabularies, or opinionated LLM-writing values such as those carried under `argument`. Preserve every intended field and value unless a separate semantic correction below requires a change.

**Requested correction:** Re-emit the metadata as parseable YAML between opening and closing delimiters. Validate it with a YAML parser and confirm that `document_id`, authority, provenance, authorization flags, and trace-forward metadata are machine-readable.

### A-02 — Keep the Frame/topology decision with James

**Finding:** C-4 correctly says Frame contract decisions are out of scope, but then says ledger ownership and one-app-vs-two-app topology are “deferred to Claude Code at repo creation.” That delegates an architectural decision to the implementation agent and conflicts with both the stated James-only decision authority and the document's prohibition on Frame contract decisions.

**Requested replacement intent:**

> Frame integration topology and ledger ownership remain unresolved operator decisions. Claude Design must avoid depending on either answer. Claude Code may inspect the existing Frame/app fleet, identify constraints, run bounded engineering spikes, and submit alternatives with consequences. James decides before any repo structure or persistence boundary makes the choice expensive to reverse.

Claude Code may recommend and evidence; it may not silently decide through scaffolding.

### A-03 — Define staged design-to-code handoffs and align the first vertical slice with Tier 1

**Finding:** The tier plan puts the procurement-critical design spine in Tier 1 and explicitly lets Tier 3 land behind the physical build. Section 11 nevertheless says no code handoff occurs until the *entire* journey hierarchy, all representative recovery states, and the broader package are complete. It then names `family proposal → operator review → accepted layout branch` as the first implementation slice, even though C-8 and the tier plan remove the family surface from the pre-demo critical path.

Read literally, this postpones implementation of the dogfooding/procurement spine until after the build it is meant to support, while building a deferred family path first.

**Requested correction:** Define two readiness boundaries:

1. **Scoped Tier-1 code handoff:** permitted once the mechanical integrity pass, canonical geometry request, BOM basis correction, Journeys 2–5 at the required depth, procurement-release gate, relevant control loops, and A-01/C-01/P-01 acceptance criteria are coherent. This handoff authorizes only an operator-facing thin slice and remains subject to James's explicit implementation authorization.
2. **Full-platform code handoff:** follows completion of the remaining lifecycle journeys, control loops, family journeys, and cross-surface acceptance contract.

The first end-to-end slice should follow the actual critical path:

> measured/canonical geometry → verified design baseline → exact shortage list/BOM → procurement-release decision → export or manual-order capture with provenance

The family proposal slice remains important, but it belongs in the later family-turnover sequence unless James explicitly reprioritizes it.

### A-04 — Remove the new lifecycle collapse from §7.2

**Finding:** Section 7.2 correctly rejects `basis` because it fuses independent axes, but the proposed replacement introduces `workflow_state = proposed · reviewed · approved · ordered · received · allocated` on `PartRow`. That enum again combines distinct lifecycles:

- design disposition (`proposed/reviewed/approved`);
- procurement/order fulfillment (`ordered`);
- receipt and inspection (`received` is itself underspecified);
- inventory reservation/allocation (`allocated`).

It also conflicts directly with §7.3, which requires acquisition, possession, inspection, availability, allocation, location, and condition to remain separate. A BOM demand row does not itself become received or allocated; orders, receipt/inspection records, inventory lots, and allocation records satisfy quantities against it.

**Requested correction:** Delete the single `workflow_state` proposal. Keep the design-side disposition separate and express fulfillment through typed relations or independent records/axes. At design-brief level, it is enough to request:

- a BOM/design-row disposition with revision and supersession;
- order-line state on procurement records;
- receipt and inspection results on received lots;
- availability derived from accepted quantities and holds;
- allocation as a quantity-bearing relation between inventory and a baseline/BOM demand.

Claude Design should show the composed human summary, not expose these as a wall of enums. The schema owner can settle exact names and cardinalities later.

## Precision correction that can ride with the same edit

The §3.4 table's second column is labelled `T-minus`, but the values increase from 4 to 13.5 weeks as dates advance. They are elapsed weeks from the 2026-09-17 issue date, not time remaining to the demo. Rename the column to `Weeks from issue` (and use `14 weeks` for the demo), or convert it to genuine countdown values. This is clerical, but deadline language should not admit two readings.

## Dispatch recommendation

Apply A-01 through A-04, make the time-axis label unambiguous, and dispatch the repaired handoff to Claude Design. No further broad Claude↔ChatGPT reconciliation is needed unless one of those repairs reveals a disagreement with James's settled intent.

— ChatGPT (Codex), independent peer reviewer  
For decision and dispatch by James (`@jfo`)
