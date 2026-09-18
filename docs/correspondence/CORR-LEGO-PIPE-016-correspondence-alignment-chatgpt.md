---
correspondence_schema: lego-pipe-memo/v2
document_id: CORR-LEGO-PIPE-016
document_type: lego-pipe-memo
memo: CORR-LEGO-PIPE-016
revision: R0
memo_type: correspondence
status: for_reconciliation
title: Correspondence numbering and exchange alignment
date: 2026-09-17
from:
  actor: ChatGPT
  role: correspondence_steward
  provider: OpenAI
to:
  - actor: James (@ojfbot)
    role: operator_and_final_authority
thread: correspondence-governance
argument: >-
  In which the ChatGPT-side register discrepancies are identified, a compact
  lego-pipe-memo/v2 contract is proposed, allocation and transfer rules are
  established, and prior ChatGPT memos are classified for migration or legacy
  retention.
findings:
  - id: N-01
    summary: CORR-LEGO-PIPE-011-Dispatch-Addendum.md is missing and collides with HANDOFF-011.
  - id: N-02
    summary: The registered and observed filenames for REVIEW-012-R0 differ.
  - id: N-03
    summary: The registered and observed filenames for CORR-013 differ.
  - id: N-04
    summary: Identities of occupied numbers 014 and 015 are unverified here.
  - id: C-01
    summary: Existing issued identifiers must remain immutable.
  - id: C-02
    summary: Provider projects are mirrors of the provider-neutral register.
  - id: C-03
    summary: Transfer requires attachment and receiver-side preflight.
  - id: C-04
    summary: The reference preflight validator may require a v2 update.
provenance:
  source_artifacts:
    - REGISTER.md
    - preflight.py
    - LEGO-PIPE-011-from-studio-to-stage-R2.md
    - CORR-LEGO-PIPE-013.md
  method: Attached-artifact and provider-project correspondence audit
  in_reply_to: []
  supersedes: []
tags:
  - correspondence
  - register
  - frontmatter
  - preflight
---

# Correspondence alignment

## 1. Register audit

The existing register covers 007-R2 through 013. These additional or inconsistent
artifacts are known in this provider project:

| Number | Proposed document entry | Type | Thread | Author | Proposed status |
|---|---|---|---|---|---|
| 011 collision | `CORR-LEGO-PIPE-011-Dispatch-Addendum.md` | CORR | design | ChatGPT | Created; transfer/issuance **[unverified]**. If issued, add as an immutable collision. If never transferred, do not register it as issued; allocate a fresh number before use. |
| 012-R0 | `LEGO-PIPE-012-R0-Review-of-From-Studio-to-Stage.md` | REVIEW | build-harness | ChatGPT | Possible mirror filename for registered `build-harness/REVIEW-LEGO-PIPE-012-review-of-from-studio-to-stage.md`; identity equivalence **[unverified]**. Verify content/hash, then record as an alias rather than a new memo. |
| 013 | `CORR-LEGO-PIPE-013.md` | CORR | build-harness | Claude (Cowork) | Possible mirror filename for registered `build-harness/CORR-LEGO-PIPE-013-reconciliation.md`; identity equivalence **[unverified]**. |
| 014 | Identity **[unverified]** | **[unverified]** | **[unverified]** | **[unverified]** | Occupied per operator; canonical row required. |
| 015 | Identity **[unverified]** | **[unverified]** | **[unverified]** | **[unverified]** | Occupied per operator; canonical row required. |
| 016-R0 | `CORR-LEGO-PIPE-016-correspondence-alignment-chatgpt.md` | CORR | correspondence-governance | ChatGPT | for reconciliation |

Do not renumber any issued artifact. The 011 collision is governed by C-01.
Numbers 014 and 015 remain placeholders until James supplies or confirms their
canonical identities (N-04).

## 2. Proposed `lego-pipe-memo/v2`

```yaml
---
# Required
correspondence_schema: lego-pipe-memo/v2
document_id: CORR-LEGO-PIPE-016
document_type: lego-pipe-memo
memo: CORR-LEGO-PIPE-016
revision: R0
memo_type: correspondence
# enum: handoff | correspondence | review | review_response |
#       decision | work_order | findings
status: for_reconciliation
# enum: draft | reserved | for_review | for_reconciliation |
#       issued | accepted | superseded | closed
title: Correspondence alignment
date: 2026-09-17
from:
  actor: ChatGPT
  role: correspondence_steward
  provider: OpenAI
to:
  - actor: James (@ojfbot)
    role: operator_and_final_authority
argument: >-
  In which one concise sentence states the memo's action, conclusion, or dispute.
findings:
  - id: N-01
    summary: One independently referenceable finding.
provenance:
  source_artifacts:
    - REGISTER.md
  method: Document audit
  in_reply_to: []
  supersedes: []

# Optional
thread: correspondence-governance
cluster: null
repos: []
tags: []
trailer:
  transfer: attachment
  preflight: pending
---
```

## 3. Register protocol

1. The provider-neutral, git-backed register is the single source of truth (C-02).
   Provider registers are read-only mirrors between reconciliations.
2. James allocates numbers or explicitly delegates an allocation. An agent must
   not infer a free number from its local mirror.
3. Allocation is recorded as `reserved` before drafting. Reservation and issue
   consume the number; abandoned reservations remain visible.
4. Use a revision when correcting or superseding the same speech act while
   retaining its author, recipients, authority, purpose, and scope. Use a new
   number for a reply, review, decision, new work authorization, changed
   recipients, changed authority, or materially changed scope.
5. Canonical prefixes are `HANDOFF-`, `CORR-`, and `REVIEW-`. Historical
   unprefixed artifacts retain their filenames but receive a prefixed citation
   form in the register.
6. A memo is issued only when its final file is authorized by James or an
   explicitly delegated issuer, frozen at a revision, entered in the canonical
   register, and transferred to its recipient as a file attachment. Creation,
   pasting, or mentioning a draft does not issue it.
7. Transfer is by file attachment, never pasted text. The receiver runs
   preflight against the received file before relying on it or executing a work
   order (C-03).
8. A failed preflight may be read by a human but cannot become an operative work
   order. The sender repairs the same unissued revision or creates the next
   revision if the earlier file was already issued.
9. Historical collisions are never repaired by silent renumbering. Record both
   rows, cite the prefix and revision, and add a collision note.

## 4. ChatGPT memo migration

| Memo | v2 breakage | Treatment |
|---|---|---|
| CORR-LEGO-PIPE-008 | House-style keys do not establish the v2 schema, normalized memo/revision, enums, findings, and provenance contract. | Already issued: mark legacy; do not edit in place. Add register metadata or an alias only. |
| `CORR-LEGO-PIPE-011-Dispatch-Addendum.md` | Number collides with HANDOFF-011; v2 identity and provenance fields may differ. Issuance is **[unverified]** (N-01). | If never issued, migrate content in place but allocate a new number before transfer. If issued, preserve it as a legacy collision. |
| REVIEW-LEGO-PIPE-012-R0 | v1 status/memo-type enums and recipient/provenance shapes differ from v2; observed filename differs from the registered path (N-02). | Already issued: mark legacy; verify and register the mirror filename as an alias. |
| CORR-LEGO-PIPE-016-R0 | None by design. The reference validator may still reject the new schema identifier or enums (C-04). | Reconcile v2 first, then update the validator and run preflight before issue. |

The attached `preflight.py` is known to validate the v1 schema contract. Whether
it already accepts v2 is **[unverified]**; schema-ID, enum, recipient-shape, and
findings checks must be reconciled before C-04 can be closed.

<!-- ===== RECEIPT NOTE — added by Claude (Cowork), not part of the memo =====

TRANSFER METHOD NON-CONFORMING. This file is a reconstruction. CORR-LEGO-PIPE-016
reached the Claude session as chat-pasted text on 2026-09-17, in two parts: a first
paste truncated inside the section 2 YAML example, and a second carrying the
complete document. Rule 9 of the register (attach, never paste) was not met in
either.

WHAT THE RECEIVER RESTORED, and nothing else:
  - closed the unterminated code fence at the end of section 2;
  - restored the `## 3.` and `## 4.` headings, which arrived as bare text;
  - restored the ordered-list markers in section 3, whose nine rules arrived as
    running paragraphs;
  - restored the pipe delimiters and header row of the section 4 table, which
    arrived tab-separated;
  - added backticks to filenames and prefixes in sections 3 and 4 to match the
    document's own convention.
No word of the memo was added, removed, reordered or reworded. The frontmatter is
byte-identical to the sender's.

REGISTER CONSEQUENCE: this is not the sender's file and its hash is not the
sender's hash (rule 12). The register row reads `received — reconstruction on
file; transfer non-conforming`, not `issued`. Ask ChatGPT to attach the original
`.md`; replace this file with it, record the sha256 at that point, and the row can
move to `issued`. Do not merge the two — replace.

Reconciled against by CORR-LEGO-PIPE-017-R2, which treats sections 1-4 as
authoritative on content.

===== end receipt note ===== -->
