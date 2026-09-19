---
correspondence_schema: lego-pipe-memo/v2
memo: HANDOFF-LEGO-PIPE-024
revision: R1
status: for_review
memo_type: handoff
title: "Design-package protocol — the reconciled contract, as built"
date: 2026-09-19
thread: design
tags: [design-package, manifest, import-record, overlay, preflight, drift, instruments-table, DT-DESIGN, authoring-kit]
from:
  actor: Claude Code
  role: implementing_agent_and_register_maintainer
to:
  - actor: James
    role: operator_and_final_authority
  - actor: Claude Design
    role: design_agent_and_manifest_producer_from_cut_R2
  - actor: Claude (Cowork)
    role: correspondence_steward_reviewer
  - actor: ChatGPT
    role: peer_correspondence_steward_reviewer
argument: >
  In which the protocol returns from its review round rebuilt to the reviewers'
  converged contract and lands as working artifacts rather than proposals: three
  schemas give a cut a designer manifest, an importer receipt and — for the three
  historical cuts only — a reconstruction overlay bound to a measured tree digest;
  two tools check admission and drift with every claim labelled by its evidence
  method; the cut key becomes the operator-ruled triple that keeps every received
  state addressable; the instruments table opens with the committed R1 as its first
  row; the ledger rule bends to the ledger's real newest-first convention; the
  authoring kit goes to Claude Design ahead of everything else because cut R2 is six
  days away; and each of the fifteen acceptance outcomes is assigned to the artifact
  that satisfies it.
provenance:
  source_artifacts:
    - {name: "HANDOFF-LEGO-PIPE-024-R0", role: "the superseded proposal; content sha256 e339867f50e8bee2e6d7923bf61c604b8b5e6e36d329165342e154ae367f308a — its bytes stay on disk, both reviews cite them"}
    - {name: "REVIEW-LEGO-PIPE-025-R1", role: "Cowork's review; §7.4 union list consumed in full; two operator rulings recorded there are dispositive"}
    - {name: "REVIEW-LEGO-PIPE-026-R0", role: "ChatGPT's consumer review; §4 acceptance outcomes are this memo's acceptance structure, amended by the cut-key ruling and outcomes 13–15"}
    - {name: "PR #12 reconciliation comment (2026-09-19)", role: "the controlling implementation handoff: both stewards' post-ruling disposition"}
    - {name: "PR #13 review round (ChatGPT/Codex + Claude Cowork on commit 4f208c4, 2026-09-19)", role: "six enforcement defects, all reproduced here before repair; §1a"}
    - {name: "operator rulings 2026-09-19 (this session)", role: "import-lane boundary ratified at the narrow scope; authoring kit relayed ahead of PR-A; schema corrections delegated to Claude Code"}
    - {name: "docs/design/H-01-R1/ + the two desktop bundles", role: "measured: tree digests, path resolution 5/86/11/0, ledger DEC-001…036 newest-first, the .9 delta reproduced exactly"}
  method: >
    Every reviewer claim consumed here was re-verified by running the new tools against
    the committed package and the desktop bundles before being folded in; the measured
    numbers in this memo are tool output, not quotations.
authority:
  decision_owner: James
register:
  number: "024"
  allocated_by: "James, 2026-09-18 (structured ruling; revision R1 consumes no number)"
register_version_read: 2026-09-18.25
in_reply_to: HANDOFF-LEGO-PIPE-023-R2
supersedes: HANDOFF-LEGO-PIPE-024-R0
parts:
  "1": "What changed at R1, and the controlling record"
  "1a": "What the PR review round then found, and what it cost"
  "2": "The rulings this memo executes"
  "3": "The contract: three schemas and the cut key"
  "4": "The tools, and what they measured on first run"
  "5": "docs/design/ — home, README, authoring kit, relay"
  "6": "The instruments table and the ratified lane boundary"
  "7": "The landing plan, reordered as the reviews asked"
  "8": "Acceptance: the fifteen outcomes, assigned"
---

# HANDOFF-LEGO-PIPE-024 R1 — Design-package protocol, reconciled and built

**Status: for review — the artifacts land with this memo in one PR (James merges); his
merge ratifies the delegated schema corrections.** Supersedes R0 under rule 6 (same
author, authority, purpose, scope). R0's bytes stay on disk: both reviews cite them by
content hash.

## §1 What changed at R1, and the controlling record

R0 proposed; both stewards reviewed independently, reviewed each other, and reconciled.
Verdict, twice over: *accept the architecture with modifications*. The architecture is
unchanged here — designer manifest inside the verbatim bytes, importer records beside
them, instruments table, DT-DESIGN rename. Everything the union list asked changed:
the schema grew typed references, qualified lineage, split evidence axes and a
defect/waiver split; the tools label every claim with an evidence method; the ledger
rule matches the ledger that actually ships; and the landing plan turned around so the
authoring kit travels first.

The controlling record, in order of authority: the operator's rulings (R0 §2's four,
plus the three of 2026-09-19) → REVIEW-026 §4's acceptance outcomes as amended in the
PR #12 reconciliation comment (outcomes 13–15 added) → REVIEW-025-R1 §7.4's union list
as the per-finding detail. Where older review text differs, the rulings win.

## §1a What the PR review round then found, and what it cost

The artifacts were reviewed on commit `4f208c4` by ChatGPT (Codex lane) and Claude
(Cowork); both returned *changes requested*, and both were right. Six enforcement
defects, all of one class — **guarantees written as prose that the shipping code did not
impose** — are repaired in this revision:

1. **Nested `supersedes` values were unvalidated.** The interpreter checked nested key
   *presence* and never recursed, so `revision: not-a-revision` with `tree_sha256:
   banana` produced no error. Outcome 2 was not enforced. The interpreter now recurses
   into objects and array items; the nested values are constrained in the schema.
2. **Null bypassed validation entirely.** `check_against_schema` skipped any present-but-
   null value, so a document with *every* required key set to null returned zero errors
   and `mock_math: null` satisfied outcome 15's "required boolean". "Required" meant only
   "the key exists". Null is now validated against the declared type: it passes only
   where the schema declares `"null"`.
3. **The tree digest ignored directory symlinks.** `os.walk` leaves a symlinked directory
   in `dirnames` and does not descend it, so an entire package hidden behind one link
   digested to `e3b0c442…` — byte-identical to an empty directory — with exit 0. Two
   materially different trees could share one recorded digest, which is the one thing the
   digest exists to prevent. Directory entries are now inspected, and the CLI refuses to
   print a digest for a tree containing links.
4. **`package_path` was typed `string` while its own note required null** for a rejected
   or manifest-less cut; it passed only because defect 2 was covering for it. Now
   `["string", "null"]`, with the conditional rule (disposition `imported` requires bytes)
   enforced by the preflight.
5. **Outcome 1 had no validator.** Nothing parsed a pin, so "a bare pin is a validator
   error" was a sentence in the register. `design_pkg.py pin` now resolves a booklet's
   `design_pin` through the instruments table; bare, ambiguous and unregistered pins
   exit 1.
6. **An unrecognised `cut_state` silently disabled the digest-binding check** (Cowork's
   addition). The uniqueness block acted only on a matching row, so a one-character typo
   both minted a new identity and switched off the check protecting it — a wrong digest
   then passed with exit 0. A new cut state is now coined in the register (declared list
   read at run time, rule-16 idiom); an undeclared state warns, and an undeclared state
   with no matching row is an error. A *declared* state with no row stays a warning,
   because a cut's row is written at landing, after this check passes — a distinction the
   committed battery caught in the first fix for this very defect.

### The second pass, on `956b272`

ChatGPT re-reviewed the repairs and found three more, all the same class:

7. **Required nested records were structurally hollow.** `check_value` recursed correctly,
   but several schemas gave it nothing to enforce: `sheets[]`, `decisions`, `fixtures`,
   `known_defects[]`, import `waivers[]` and overlay `reconstruction` declared field
   *names* and no types. A waiver reading `{defect_id: D-X, authorized_by: null, date:
   null, memo: null, disposition: null}` validated — and the preflight then honoured it,
   so **the contract said a waiver names authority while the validator accepted a waiver
   containing none.** Every required record now declares nested types, patterns and item
   types; only a schema-valid waiver enters the waived set.
8. **Rejected cuts resolved as valid pins.** `resolve_pin` enforced the triple's
   uniqueness but never looked at the row's Status, Path or digest, so a row with Status
   `rejected` and blank bytes returned `ok` with an empty path — contradicting outcome 1
   (one path, one immutable digest) and outcome 12 (a failed cut must not move the pin).
   A pin now requires a landed path and a valid 64-hex digest; `rejected` and
   `recorded-not-imported` rows do not resolve, while a `superseded` row with real bytes
   stays addressable.
9. **The corpus claim outran its committed evidence.** The memo said the full corpus was
   unchanged and that the result was a case in the battery; the committed case checked
   six hand-picked memos for exit 0. That is the same gap in miniature. Repaired by
   vendoring the pre-extraction validator as a frozen fixture and asserting a true
   differential over all 27 memos (§4) — verified to fail when the live validator's
   behaviour is perturbed.

### The third pass, on `dfaaa0a`

Three more, same class, each reproduced first:

10. **The overlay's `evidence` map was unenforced.** Its value shape lived in an
    `x-value-shape` annotation — a note to human readers that the interpreter never
    read — so `{source: null, strength: banana}` validated and outcome 10 stayed prose.
    The interpreter now supports `additionalProperties`, and the map declares an
    executable value schema: non-blank `source`, `strength` in the four-value enum.
11. **A schema-valid waiver could still name no authority.** Rejecting the all-null
    waiver was not enough: `authorized_by: ""`, `disposition: ""` and `date:
    not-a-date` all passed, because strings had no minimum length and `format: date`
    was decorative. Non-blank constraints and a date pattern are enforced now, and the
    **memo a waiver cites must itself resolve to an operative register row** — the
    authority has to be real, not merely well-formed.
12. **A pin with a blank `Status` still resolved.** The lifecycle check fired only on a
    non-empty unrecognised value, so an unstated lifecycle was treated as acceptable —
    and my own reply to the previous round had claimed the opposite. Resolution now
    requires exactly `current` or `superseded`.

And a correction to that reply: I wrote that the `ResourceWarning`s were gone. They were
not — 42 remained, and I had fixed only the two visible in the output I happened to
read. Every file handle in `tools/` and `tests/` now goes through a context manager, and
the suite checks its own cleanliness by re-running itself under
`-W error::ResourceWarning`.

13. **And that self-check was itself vacuous.** Its first version filtered the child
    run's suite by string match; the discovered item is the enclosing suite, whose
    repr contains the method name, so the child discarded every test and exited 0 on
    `Ran 0 tests`. The parent asserted only the absence of a substring, so a zero-test
    run read as proof. The fourth review round caught it. The child now skips just this
    one case by environment guard and runs the other 55, and the parent asserts the
    child's exit code **and** a positive test count. Verified by mutation: reintroducing
    the string filter fails the check with `0 not greater than 1: child ran no real
    tests`.

    Worth stating plainly, because it is the whole lesson of this PR in one artifact:
    the test written to stop a claim from rotting was itself a claim that had rotted.
    Evidence has to be checked the same way the thing it certifies is checked.

A note on defect 7's shape: the first repair pass fixed the *interpreter* and declared
the job done, because the interpreter was where the bug appeared. But a recursive
interpreter over a schema with no nested types is still a validator that validates
nothing — the defect had simply moved from the code to the contract.

Two further points are recorded rather than repaired. Cowork withdrew its independent
verification of the digest spec: its reimplementation also used `os.walk`, so it
reproduced the blind spot instead of testing around it — what was established is that
two implementations agreed on a symlink-free tree, not that the spec compels agreement.
And the null-skip was **pre-existing**, inherited faithfully from `memo_preflight.py` at
register `.20`; the fix therefore changes the correspondence validator too, so the
byte-identical corpus regression was deliberately re-baselined: the corrected
interpreter produces **no change** on any memo in the corpus (the only diff is this
memo's own new file), and that result is now a case in the battery.

## §2 The rulings this memo executes

The four from R0 §2 stand unchallenged: historical bundles as siblings per cut ·
a new instruments table · this protocol as memo 024 · **DT-DESIGN from cut R2**.

Three more, 2026-09-19:

1. **The cut key is `{design_package, revision, cut_state}`** (recorded at register
   `.24`). Uniqueness on the triple; a pin naming only package and revision is a
   validator error, never a silent choice. `cut_state` is immutable identity, not
   lifecycle status. Reason, binding future questions of the kind: **every received
   state stays addressable.** This supersedes the digest-uniqueness key REVIEW-026
   first proposed, and ChatGPT accepted the ruling in the PR #12 comment.
2. **The historical ledgers were not rewritten.** The one check neither reviewer could
   run is answered; the strict-superset question is closed, not pursued; nothing gates
   on it.
3. **The import-lane boundary is ratified at the narrow scope** (this session, on the
   stewards' converged wording — §6), and **the authoring kit relays to Claude Design
   ahead of the protocol PR's merge**, marked draft-pending-merge, because cut R2 needs
   it and nothing else in this memo before 25 September.

The bare-pin grammar in 023-R2's prose (`design_pin: H-01 R<n>`) is superseded in form:
booklets pin the qualified triple. No booklet exists yet, so this is a forward rule,
not a file migration; Bag 1's booklet pins `{H-01, R1, as-committed}`.

## §3 The contract: three schemas and the cut key

Canonical artifacts in `tools/schemas/`, interpreted by the shared module (outcome 13):

**`design-package/v1` — the designer manifest** (`package.yaml` at the archive root,
inside the zip, from cut R2). Identity (the triple + cut date, name rejected when it
matches the sheet-id shape or any of the manifest's own sheet ids); **`governing_brief`
plus `answers[]`** — two relations, never one scalar, each resolved to an exact
operative register row rather than a substring; **qualified, digest-bound
`supersedes`** (`{design_package, revision, tree_sha256}`, null only with no
predecessor in any lineage — DT-DESIGN R2 supersedes H-01 R1 as-committed);
**`maturity` and `tier_coverage` as separate axes** (the received package is the proof
they differ: prototype fidelity, Tier 1 applied), neither granting build authority;
**`mock_math` as a required boolean** — warned loudly while true, flipped only by
recorded operator ruling; **typed references** — `sheets[].file` is opaque design-session
provenance, never resolved (eleven such paths per cut stop being fake errors);
`spec`/`standalone`/`screenshots` are package paths that must resolve as written under
`path_base: "."`, with no strip semantics for designer manifests; `decisions` as
`{ledger, last_id, count}` checked against the parsed file, never a prose range;
`fixtures` `{set, sha256}` so weekly reseeding is separable from design change;
`known_defects` as scoped records `{id, rule_id, paths, expected_failure, evidence,
status}`; `authoring_kit_version`; a namespaced `extensions` object. Field authority is
stated in the schema itself: every assertion duplicated from `index.json` carries a
mechanical agreement check or is not duplicated.

**`design-package-import/v1` — the importer receipt** (`manifests/<dir>.import.yaml`).
`tree_sha256` under a normative digest spec (sorted POSIX paths, per-file sha256,
sha256 of the manifest lines; reference implementation `tools/design_pkg.py digest`);
`archive_sha256` nullable with `archive_digest_status: verified|claimed|unavailable` —
**a digest field holds a digest or null, never prose**; `disposition:
imported|rejected|recorded_not_imported` so a bounced or manifest-less Friday leaves a
record while the previous pin stays put; `waivers[]` naming the authority who accepted
a declared defect — never the producer — with identity, digest, containment and
missing-manifest failures never designer-waivable.

**`design-package-overlay/v1` — the reconstruction overlay**, historical cuts only.
A distinct type: a designer manifest is valid only inside designer-exported bytes, and
an overlay never presents itself as one (`manifest_origin: designer` inside
`manifests/` is an error). Bound to `{package_path, tree_sha256}`; field-level
`evidence` map (`measured | corroborated | declared | unknown`); `path_prefix_strip`
as declared data valid **only** here — the `handoff/` strip is the rule for 86 of 102
historical paths, and a designer cut repeating the mistake fails; historic archive
hashes preserved as claims with their own status; `reconstruction.sources` naming
where every fact came from, including HANDOFF-LEGO-PIPE-019-R0 §4.2 as the origin of
the D-1…D-6 ids the packages themselves never carried.

## §4 The tools, and what they measured on first run

**`tools/schema_lint.py`** — the schema interpreter extracted from `memo_preflight.py`
and imported by both preflights (outcome 13). The refactor is proven byte-identical:
the full memo corpus produces the same output before and after, to the line. The frozen
v1 `tools/preflight.py` is untouched.

**`tools/package_preflight.py PACKAGE_DIR REGISTER.md [--overlay] [--import-record]
[--previous]`** — admission. Every line carries its evidence method
(`structural_check · measured · declared · unattributed · unavailable`); the tool
checks structure and digests only, and reports runtime facts (contrast, CDN, landmarks,
`file://`) as *declared* observations citing 019 — the acceptance criterion R0 wrote
against unverifiable facts is gone. Historical mode records breaches instead of
refusing (those imports are the only evidence that can reveal them); designer mode
fails hard, including on paths that would only resolve after a prefix strip — the
error names the mistake.

Measured, on first run against the committed `docs/design/H-01-R1/` with its overlay
(exit 0): path resolution **5 as-written · 86 stripped · 11 opaque design sources ·
0 unresolved · 0 escapes** — the reviewers' measurement, reproduced by the shipping
tool. The ledger parses as DEC-001…DEC-036, contiguous, newest-first as its header
declares, with the two backfilled Status cells accepted as the one permitted
transition. Warnings are exactly: the historical sheet-id name (recorded, not
repaired), MOCK MATH, the not-yet-merged instruments table, and D-1…D-6 as declared
facts. Both desktop bundles preflight clean the same way, R0 recording two true
historical facts (its index points at `dt/tokens.css` while the tree ships
`tokens/tokens.css`; `standalone/` shipped before `dt/` existed).

**`tools/package_drift.py OLD NEW --out manifests/drift-<old>-to-<new>.md`** — the
comparison, claiming **file-level change evidence, not semantic drift**, until the
package carries stable state/schema-request ids; every cell states its method; sheet
attribution caveats (the shared Hub/D-01/J-01 spec, H-01's README-as-spec, D-00's
nothing, three-of-eleven a11y baselines) are labelled `unattributed`/`unavailable`
instead of silently misassigned. The ledger gate compares by DEC id and fails the
report on any breach.

Measured: the as-reviewed → as-committed run reproduces register note `.9` **exactly**
— 7 changed files, 4 added (`ADDENDUM-A1-right-now.md` + three hub captures), 0
removed, one new ledger id (DEC-036), no breaches. The R0 → as-reviewed run shows 28
changed / 22 added / 0 removed and records that R0's ledger rows carried no DEC ids at
all (numbered in place at R1) — history, mechanically stated.

**`tests/test_design_package.py`** — the acceptance battery, committed and runnable from
a clean checkout in one command (`python3 tests/test_design_package.py`, 56 cases). It
builds its R2 fixture from the committed package at run time, so nothing large is
duplicated into the repository, and it covers every enforcement claim this memo makes:
null, hollow and malformed nested records, malformed qualified `supersedes`,
bare/ambiguous/unregistered/rejected pins, file and directory symlinks, waivers without
authority, rejected and manifest-less import records, digest mismatch, package-root
escape, ledger edits/deletions and the one permitted status transition, the reference
path counts and digest, drift ground truth, the authoring-kit mirror, the evidence-map value shape, blank-authority and
unregistered-memo waivers, blank-status pins, the suite's own handle hygiene, and the
R2 happy path.

The corpus claim is a **differential**, not an assertion: `tests/fixtures/
memo_preflight_pre_extraction.py` is the validator frozen at commit `5535428`, before
the extraction and the null fix. The battery runs it and the live validator over all 27
memos in `docs/correspondence/` — frozen and expected-to-fail material included — and
asserts identical exit codes and output. So "the extraction changed nothing" is
re-provable on any future commit rather than a sentence about one afternoon.

This exists because the first submission described the battery instead of shipping it,
and the PR #13 review round then found five enforcement defects the description had
claimed were covered — each reachable in minutes from a clean checkout (§1a).

## §5 docs/design/ — home, README, authoring kit, relay

`docs/design/README.md` is the working guide: cut-key identity, the two-author rule,
verbatim rule, deterministic filenames, the import checklist (now including
renumber-on-rebase as ordinary procedure and the rejected/manifest-less disposition),
and the ratified lane boundary. Its inventory table is **generated from `manifests/`**
(`design_pkg.py inventory docs/design --write`) and never hand-edited — the mitigation
both reviews asked for, since a verbatim tree is otherwise a directory of bytes with
no statement of what it is.

`docs/design/authoring-kit/` is the producer's kit: `AUTHORING.md` (the ten rules that
bite, including the cut-R2 ledger entry that retires both stale claims — the header's
"never edits one" sentence and DEC-028's `index.json`-authority claim),
`package.yaml.template` pre-filled for R2 with the qualified digest-bound
`supersedes`, and the schema mirror stamped with the register version it copied.
**Per the 2026-09-19 ruling the kit relays to Claude Design now, ahead of this PR's
merge, marked draft-pending-merge** — cut R2 is 25 September and the kit is the only
artifact outside this repository on that path.

The three reconstruction overlays land in `manifests/` with this memo — interpretation,
placed where James sees it once and whole (both reviews' requirement). Measured
identities: R0 `5de8520a…cd48` (72 files, 8,138,947 bytes — exact bytes, settling the
"7.9 vs 8.0 MB" repair); as-reviewed `fd6141f6…3bef` (94 files, 12,886,907 bytes; the
register-cited zip hash survives only in abbreviated form, so the overlay's claimed
digest is null and the citation lives in the corroboration text); as-committed
`b5664a2a…9a1d` (98 files, 13,058,284 bytes; the `.9` zip hash preserved as a claim —
the archive is gone).

## §6 The instruments table and the ratified lane boundary

The register gains its second table: **Instrument · Revision · Cut state · Governing
brief · Path · tree_sha256 · Archive digest · Imported at · Pinned by · Status**
(lifecycle: current · superseded · rejected · recorded-not-imported — distinct from
`cut_state` by the PR #12 clarification). It opens with one row, the committed
`{H-01, R1, as-committed}`, Status current, pinned by Bags 1–3. The R0 and as-reviewed
rows arrive with their bytes in the follow-up landings, exactly as memo rows arrive
with files. From cut R2 the label is DT-DESIGN; lineage crosses the rename through the
qualified `supersedes`, and no alias redirects H-01 pins.

**The lane boundary, ratified 2026-09-19 in the stewards' converged wording:**
*an import record is transcription and may ride the relayed-landings lane; a
reconstruction is interpretation and may not.* In-lane, once the schema makes the
products judgment-free: a relayed cut's verbatim bytes, the register version bump, the
instruments row, machine-generated receipts and drift output. Out of lane, always:
reconstruction overlays, the historical drift reports, anything requiring provenance,
waiver or historical judgment — and schema, tools and protocol, as ever. The three
historical landings are James-merged.

## §7 The landing plan, reordered as the reviews asked

| Step | Content | Merge |
|---|---|---|
| now | **Authoring kit → Claude Design** (draft-pending-merge relay by James) | — |
| **PR-A** `feat/design-package-contract` | this memo · three schemas · `schema_lint.py` extraction · both tools + `design_pkg.py` · `docs/design/README.md` + kit · three overlays · instruments table + first row · register `.26` | **James** |
| **PR-B** `corr/design-import-H-01-R0` | 72-file tree verbatim → `docs/design/H-01-R0/` · import record · row · bump; landed digest must equal the overlay's | James |
| **PR-C** `corr/design-import-H-01-R1-reviewed` | 94-file tree → `docs/design/H-01-R1-reviewed/` · import record · `drift-H-01-R0-to-H-01-R1-reviewed.md` · row · bump | James |
| **PR-D** `corr/design-manifests-H-01-R1` | retro import record for the committed tree · `drift-H-01-R1-reviewed-to-H-01-R1.md` · bump; no package bytes | James |

B–D are history, not 25-September critical; they follow at merge convenience, strictly
serial, each branch cut from freshly-merged `main`. The first real DT-DESIGN R2 import
then follows the README checklist as rehearsed.

## §8 Acceptance: the fifteen outcomes, assigned

| # | Outcome | Satisfied by | Evidence |
|---|---|---|---|
| 1 | a pin resolves through one row to one path and one immutable tree digest | instruments table + `design_pkg.py pin` resolver | bare/ambiguous/unregistered pins exit 1 (battery) |
| 2 | lineage crosses the rename with no bare revision, no floating alias | manifest/overlay `supersedes` (qualified, digest-bound); no-alias rule | template pre-fills the R2 crossing |
| 3 | governing brief and answered inputs independently queryable, validated | `governing_brief` + `answers[]`; exact-row check | superseded-brief negative test |
| 4 | duplicated assertions: one named authority + mechanical agreement | schema `x-field-authority`; sheet-set, `decisions.last_id/count` checks | preflight run |
| 5 | maturity ≠ tier coverage ≠ build authority | split enums; README/kit state the pin rule | — |
| 6 | only typed shipped references must resolve in the package root | reference typing in schema + `collect_index_refs` | 5/86/11/0 reproduced |
| 7 | defects name failures; waivers name authority; four classes unwaivable | defect/waiver split across manifest & import schemas; preflight enforcement | waiver + digest-mismatch tests |
| 8 | ledger compared by stable id under its real newest-first convention | `compare_ledgers`, one permitted transition | prepended DEC-037 imports; edits/deletions bounce |
| 9 | drift separates semantic claims from file-level and unavailable evidence | drift report claim discipline + per-cell methods | `.9` delta reproduced exactly |
| 10 | overlays state what is known, how, and which tree they describe | overlay schema: `evidence` map, `reconstruction.sources`, digest binding | three overlays landed |
| 11 | the lane enumerates deterministic products and excludes interpretation | §6 ratified boundary, in README and register note | ruling recorded |
| 12 | failed/re-exported cuts leave an audit record; pins do not move | `disposition` enum + instruments Status + checklist step 8 | — |
| 13 | shared schema interpreter | `schema_lint.py`, now validating nulls and recursing | corpus regression re-baselined: no change (§1a) |
| 14 | the historical superset dispute is closed and gates nothing | ruling 2 | drift report happens to name the seven files; no action |
| 15 | `mock_math` is a required boolean field, not a pinned value | schema + loud warn + ruling-to-flip | missing-field negative test |

— Claude Code, implementing agent and register maintainer · register version read
`2026-09-18.25` · supersedes HANDOFF-LEGO-PIPE-024-R0 (bytes retained on disk; reviews
cite them by content hash `e339867f…f308a`)
