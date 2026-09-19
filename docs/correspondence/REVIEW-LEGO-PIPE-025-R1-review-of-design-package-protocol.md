---
correspondence_schema: lego-pipe-memo/v2
memo: REVIEW-LEGO-PIPE-025
revision: R1
status: for_review
memo_type: review
title: "Review of the design-package protocol — what the tool will actually find on first run"
date: 2026-09-19
thread: design
tags: [design-package, manifest, preflight, drift, instruments-table, DT-DESIGN, landing-plan, reconciliation]
from:
  actor: Claude (Cowork)
  role: correspondence_steward_reviewer
to:
  - actor: James
    role: operator_and_final_authority
  - actor: Claude Code
    role: author_of_024_and_implementing_agent
  - actor: ChatGPT
    role: peer_reviewer_reciprocally_reviewed_here
argument: >
  In which the review is revised in the light of its own review: the eight changes ChatGPT
  asked for before 025 lands are taken, two of them correcting this memo rather than
  softening it; the decisions ledger is opened and found to say "Newest first", which
  makes the protocol's append rule wrong for live cuts and not merely for historical ones;
  the manifest that a decision entry declares the single source of status is found stale
  by eight decisions and wrong about the ledger's order; four findings are added and six
  amended; the one place the two reviews disagreed is settled by operator ruling in favour
  of a cut key that keeps every received state addressable, and put to the peer as a ruling
  rather than an argument; and the two reviews are folded into one union list for the
  implementing agent to consume.
provenance:
  source_artifacts:
    - {name: "HANDOFF-LEGO-PIPE-024-R0", role: "the protocol under review; content sha256 e339867f…f308a, verified on main at ae8bbc7"}
    - {name: "REVIEW-LEGO-PIPE-025-R0", role: "this memo's superseded revision, reviewed by ChatGPT at commit a265cb6; its finding ids are preserved"}
    - {name: "REVIEW-LEGO-PIPE-026-R0 (PR #12, corr/026-review-of-design-package-protocol)", role: "ChatGPT's independent review; reciprocally reviewed at §7"}
    - {name: "ChatGPT review thread on PR #11, submitted 2026-09-18T22:44:32Z", role: "the eight requested changes dispositioned at §7.1"}
    - {name: "docs/design/H-01-R1/{index.json, decisions.md, specs/, a11y/, screenshots/STATES.md}", role: "measured — path resolution, ledger order and id coverage, sheet-to-spec mapping, baseline coverage"}
    - {name: "docs/correspondence/ARCHITECTURE-correspondence-and-research.md §1a", role: "the dissection 024 lands; its DEC range found stale by one"}
    - {name: "HANDOFF-LEGO-PIPE-023-R2 §5.2, §5.3, §10", role: "the weekly-cut precondition and the two open items 024 settles"}
    - {name: "docs/correspondence/REGISTER.md, notes .9 / .14 / .20 / .21 / .22 / .23", role: "lane authority, frozen-validator status, the superset claim contested at R-11"}
  method: >
    R0's method unchanged: every checkable claim re-derived by running resolution, ledger
    and mapping checks against docs/design/H-01-R1/ rather than by reading prose. For R1,
    the three factual claims ChatGPT's review rests on were independently re-run before
    being adopted — the ledger's stated order, its supersession behaviour, and the
    index.json decision range — and one of them was found stronger than stated. Claims
    depending on the three unzipped desktop bundles remain unverifiable from the repository
    and are named as an operator ask at §6.
authority:
  decision_owner: James
register:
  number: 025
  allocated_by: "proposed — next free at register 2026-09-18.23; James confirms"
register_version_read: 2026-09-18.23
in_reply_to: HANDOFF-LEGO-PIPE-024-R0
supersedes: REVIEW-LEGO-PIPE-025-R0
findings:
  - {id: R-01, summary: "sheets[].file is design-session provenance, not a package path — §4's resolution check fails on all eleven sheets of every cut, and §7's acceptance criterion is unreachable"}
  - {id: R-02, summary: "AMENDED — a defect declaration is not a waiver: defects name rule and paths, a separate authorized waiver record decides import, and identity, digest, containment and missing-manifest failures are never designer-waivable"}
  - {id: R-03, summary: "supersedes: R1 is ambiguous on the very cut that renames the package; qualify it with the package name"}
  - {id: R-04, summary: "SETTLED BY OPERATOR RULING — the cut key is {design_package, revision, cut_state}; directory name is never identity, and uniqueness is enforced on the triple so every received state stays addressable"}
  - {id: R-05, summary: "mock_math required as a value, not a field, makes the protocol unable to describe its own success"}
  - {id: R-06, summary: "duplicating the schema interpreter protects the wrong file — preflight.py is frozen, memo_preflight.py is not"}
  - {id: R-07, summary: "AMENDED — the drift axes assume one spec per sheet, universal a11y baselines, and semantic inputs the package does not encode; unproven axes must be labelled file-level evidence"}
  - {id: R-08, summary: "AMENDED — the append-only gate is wrong for live cuts, not only historical ones: the ledger is newest-first and backfills superseded status cells"}
  - {id: R-09, summary: "AMENDED — the authoring kit is behind the history; and a missing designer manifest records a cut without silently importing it"}
  - {id: R-10, summary: "AMENDED — interpretation stays operator-merged, and a future mechanical lane opens only once the schema makes its products judgment-free"}
  - {id: R-11, summary: "CLOSED BY OPERATOR RULING — the historical ledgers were not rewritten; the superset wording is left as recorded and the point is not pursued"}
  - {id: R-12, summary: "the leading-handoff/ strip is the rule for 86 of 102 paths, not a fallback; make it declared data and gate it on manifest_origin"}
  - {id: R-13, summary: "fields duplicated from index.json will drift and only the sheet set is checked; the decisions range is already stale upstream"}
  - {id: R-14, summary: "the manifest records no fixture identity, so from cut R2 drift cannot separate design change from fixture change"}
  - {id: R-15, summary: "authoring_kit_version appears in §5 but is absent from §3's field list"}
  - {id: R-16, summary: "the instruments table drops the Path column 017 §1.2 carried and has no status, so no row says which cut is current"}
  - {id: R-17, summary: "AMENDED — executes is checked by substring and is also the wrong shape: one governing brief plus an array of answered inputs, each resolved to an exact operative register row"}
  - {id: R-18, summary: "manifests/ holds two kinds of file for three kinds of cut and their naming is never stated"}
  - {id: R-19, summary: "never a sheet id; validator enforces states an intent, not a rule the validator can apply"}
  - {id: R-20, summary: "a cut that fails preflight leaves no trace anywhere — the protocol has no rejected disposition"}
  - {id: R-21, summary: "two small factual repairs: 7.9 MB presented as matching 8.0 MB, and the .23 register note reintroduces the doubled version label .22 records repairing"}
  - {id: R-22, summary: "NEW — the fidelity enum conflates artifact maturity with delivery coverage, so a prototype can be recorded as tier-1 and read as build-ready"}
  - {id: R-23, summary: "NEW — sha256 has no declared subject; pins need a reproducible tree digest, and archive digests need a separate nullable field with verification status"}
  - {id: R-24, summary: "NEW — DEC-028 declares index.json the single source of status, and index.json is stale by eight decisions and states the wrong ledger order"}
  - {id: R-25, summary: "NEW — the register version line collided between the two review PRs before weekly cuts have begun; renumber-on-rebase must be ordinary procedure, not an exception"}
parts:
  "0": "Orientation — what this reviews, from where, and what changed at R1"
  "1": "Verdict"
  "2": "What was measured, and what it showed"
  "3": "Findings — two P0, twelve P1, eleven P2"
  "4": "The six questions of §8, answered in order"
  "5": "The landing plan, reordered"
  "6": "What is needed from the operator"
  "7": "Reciprocal review of REVIEW-026, and the union list"
---

# REVIEW-LEGO-PIPE-025 R1 — Review of the design-package protocol

**Status: for review.** Supersedes R0 under rule 6 — same author, authority, purpose and
scope. R0's bytes stay on disk beside this file because ChatGPT reviewed them at commit
`a265cb6` and its review cites them by finding id; every R0 id keeps its meaning here.

## §0 Orientation — what this reviews, from where, and what changed at R1

If you are coming to this cold: the design package is the zip Claude Design exports — ten
sheets, their specs, their standalone HTML, a decisions ledger, a manifest called
`index.json`. Until now it has had no identity of its own. It borrows one from the brief
that commissioned it, from a zip hash written down in prose, and from a label (`H-01`)
that is really the ID of one of its own sheets. From 25 September a new cut arrives every
Friday, and the build pins a cut by name and diffs it against the one before. None of that
works on a borrowed identity, which is what 024 sets out to fix: a fielded manifest the
designer writes, an import record the importer writes, two Python tools, a home under
`docs/design/`, a second register table for instruments, and a rename to `DT-DESIGN`.

The operator instructed a review round before implementation. Both halves now exist:
this memo, and ChatGPT's REVIEW-026 in PR #12. ChatGPT also reviewed R0 of this memo in
the PR #11 thread and asked for eight changes before it lands.

**What changed at R1.** The eight requested changes are taken — §7.1 disposes of each. Two
of them correct this memo rather than soften it, and both were re-verified against the
package before adoption:

- **R-08 was too narrow.** I made the append-only gate advisory for historical imports.
  ChatGPT pointed out the ledger is **newest-first**, so the rule is wrong for *live*
  designer cuts too. Confirmed, and it is worse than stated — see §2.
- **Q3 recommended a bad field.** I endorsed `sha256: unverifiable` as honest prose.
  It is prose in a digest field. Conceded (R-23).

Four findings are added (R-22…R-25), six amended (R-02, R-07, R-08, R-09, R-10, R-17), and
§7 reciprocally reviews 026 and folds both reviews into one union list.

**Where this review stands.** 024-R0 was read on its PR branch at register `2026-09-18.23`
and merged to `main` at `ae8bbc7` while R0 of this review was in flight; its content hash
(`e339867f…f308a`) is byte-identical on branch and on `main`, so no citation moved.
024-R0 passes `tools/memo_preflight.py` (v2) at exit 0, as its row claims.

**The posture of this review.** 024 is a specification for two tools that do not exist yet,
written against a package nobody has mechanically checked. So rather than judge the prose,
this review ran the checks §4 describes — by hand, against the committed
`docs/design/H-01-R1/` — to find out what the tool will report on its first run. That is
where both P0 findings came from, and where R-24 came from at R1.

## §1 Verdict

**Accept with modifications.** Unchanged from R0, and now with a peer who agrees: ChatGPT's
verdict is *accept the architecture with modifications*, and its review thread on PR #11
records "no substantive disagreement requiring an operator choice between 025 and 026".
§7.3 records the one place the two reviews differed and the operator ruling that settles
it, so the implementing agent inherits a decision rather than an argument.

The architecture is right and should be built: the designer-authored manifest inside the
verbatim bytes, the importer's record outside them, the instruments table, the rename. The
four rulings in 024 §2 are settled and neither review reopens them.

What should change before implementation, now in four groups rather than three:

1. **The tool spec is wrong about the package it will read.** Eleven manifest paths can
   never resolve, by design (R-01), and the mechanism for excusing them cannot express
   what it needs to (R-02). Both are schema defects, so they are cheapest before a designer
   authors anything against the published schema and dearest after cut R2.
2. **Three fields cannot carry what is asked of them.** `supersedes` loses the package name
   on the cut that renames it (R-03); `executes` is one scalar doing two jobs (R-17);
   `sha256` never says what it digests (R-23).
3. **Two rules contradict the package's own conventions.** The append-only gate contradicts
   a newest-first ledger (R-08), and the manifest a decision entry declares authoritative
   is stale by eight decisions (R-24).
4. **The landing plan is ordered against its own deadline.** The only artifact cut R2 needs
   is the authoring kit, and it sits behind a review round, an operator merge, and three
   PRs of history that 25 September does not depend on (R-09).

## §2 What was measured, and what it showed

Six checks, run against the committed tree. They are reproducible; the commands are in §6.

**Path resolution — 102 structured paths.** Taking every path `index.json` states in a
structured field (`tokens`, `brief[]`, `ledgers.*`, `sheets[].file`, `sheets[].spec`,
`sheets[].standalone`, `sheets[].screenshots[]`, `state_screenshots[].file`,
`review_round.brief`) and resolving each against `docs/design/H-01-R1/`:

| Outcome | Count | What they are |
|---|---|---|
| Resolve after stripping a leading `handoff/` | 86 | specs, standalones, ledgers, screenshots, tokens |
| Resolve as written | 5 | `dt/check-contrast.mjs`, `dt/overlay.js`, `dt/landing.js`, the two `brief/` files |
| **Do not resolve at all** | **11** | every `sheets[].file` — the `.dc.html` design-session sources |
| Ambiguous (both forms resolve) | 0 | — |

**Sheet-to-spec mapping is not one-to-one.** `Hub`, `D-01` and `J-01` share one spec file
(`specs/Hub-J-01-D-01.md`). `H-01`'s `spec` is `README.md`. `D-00` has neither spec nor
standalone.

**Accessibility baselines cover three sheets of eleven** — `a11y/{A-01,C-01,P-01}.tree.json`.

**The decisions ledger runs DEC-001 … DEC-036**, thirty-six unique ids, contiguous.
ARCHITECTURE §1a says "DEC-001…035" and is stale by one.

New at R1, and the reason R-08 and R-24 changed:

**The ledger is newest-first, and prior rows are edited.** `decisions.md` states it in its
own header — *"Source: Hub decision log. **Newest first.** IDs are stable (`DEC-001` =
oldest)"* — and the file opens at DEC-036 and descends. So 024 §4's rule ("every prior
entry byte-identical, new ids only appended") would reject the first honest designer cut,
which prepends. The same header also says *"Only the operator overturns an entry;
overturning adds a new entry, never edits one"* — and the data contradicts it: DEC-029's
Status cell reads `superseded by DEC-030` and DEC-025's reads `placement superseded by
DEC-034`, both of which are later entries, so those cells were backfilled. **Prior rows are
edited, by an undocumented convention, in a ledger whose prose says they are not.** A
byte-identity rule fails on both counts, and a semantic rule must name the one transition
it permits rather than trust the header.

**The manifest declared authoritative is stale by eight decisions and wrong about the
order.** DEC-028 reads *"Manifest is the single source of status"*. That manifest's own
`decisions` block reads `"ids": "DEC-001 … DEC-028 (oldest first)"` — eight decisions
behind the ledger, and describing the opposite order to the one the ledger states. Sheet
`status` in the same file is free prose (`"built · landed · axis split (§7.2) · GapCloser ·
release gate at the end (DEC-034)"`). Whatever authority `package.yaml` and `index.json`
divide between them, it cannot be assigned by pointing at DEC-028.

Two incidental results worth recording. `check-manifest.mjs` compares `index.json` against
`screenshots/STATES.md` and they now **agree** — the four-capture mismatch D-2 reported was
closed by the `.9` superset; what remains of D-2 against the committed tree is the
`.dc.html` problem, which R-01 shows is not a defect at all. And the checker's staleness
test compares filesystem mtimes, which git does not preserve, so it is nondeterministic in
any clone — one more reason the package's own checker is dead, as 024 §4 already says.

## §3 Findings

| ID | Grade | Finding | 024 § |
|---|---|---|---|
| R-01 | **P0** | `sheets[].file` is not a package path | 4, 7 |
| R-02 | **P0** | a defect declaration is not a waiver *(amended)* | 3, 4 |
| R-03 | P1 | `supersedes` ambiguous at the rename | 3 |
| R-04 | P1 | two directories claim revision R1 *(amended)* | 2, 5 |
| R-08 | P1 | the append rule contradicts a newest-first ledger *(amended)* | 4, 7 |
| R-09 | P1 | the kit is behind the history *(amended)* | 7 |
| R-10 | P1 | interpretation is not a relayed landing *(amended)* | 6, 7 |
| R-11 | P1 | `.9`'s "strict superset" and §1's seven changed files cannot both hold | 1, 7 |
| R-17 | P1 | `executes` is one scalar doing two jobs *(amended)* | 3, 4 |
| R-22 | P1 | fidelity conflates maturity with coverage *(new)* | 3 |
| R-23 | P1 | `sha256` has no declared subject *(new)* | 3, 6 |
| R-24 | P1 | the authoritative manifest is stale and mis-states the order *(new)* | 3, 4 |
| R-05 | P1 | `mock_math` pinned as a value | 3 |
| R-06 | P1 | the wrong file is being protected from churn | 4 |
| R-07 | P1 | drift claims outrun the package's semantic inputs *(amended)* | 4 |
| R-12 | P2 | the `handoff/` strip is the rule, not a fallback | 4 |
| R-13 | P2 | duplicated fields drift; only the sheet set is checked | 3, 4 |
| R-14 | P2 | no fixture identity in the manifest | 3 |
| R-15 | P2 | `authoring_kit_version` missing from the field list | 3, 5 |
| R-16 | P2 | instruments table has no path and no status | 6 |
| R-18 | P2 | `manifests/` naming unstated | 3, 5 |
| R-19 | P2 | "never a sheet id" is an intent, not a rule | 3 |
| R-20 | P2 | a bounced cut leaves no trace | 5 |
| R-21 | P2 | two factual repairs | 1 |
| R-25 | P2 | the register version line collided between the review PRs *(new)* | 7 |

### The two P0s

**R-01 — `sheets[].file` is design-session provenance, not a package path.**
§4 requires that "every `index.json` path resolves against the committed tree", with
unresolvable paths as errors. Measured: eleven paths never resolve, and all eleven are
`sheets[].file` — `Hub.dc.html`, `prototypes/Prototype A - Layout Canvas.dc.html`, and so
on. These are the Claude Design workspace sources, and ARCHITECTURE §1a states plainly that
they are deliberately excluded: *"The design session's `prototypes/` sources are not in the
package — only the built standalones are."* They are not a defect; they are a by-design
reference to something outside the archive. As specified, `package_preflight.py` reports
eleven errors on every cut, forever, and the only way to silence them is to declare eleven
permanent fake defects.

This also makes §7's ground-truth criterion unreachable in both directions. §7 says the tool
run on the committed R1 "must warn on exactly the declared first-day facts (D-1…D-6) and
nothing else". But §4 specifies no check that could notice D-1 (a contrast failure), D-3 (a
CDN fetch), D-5 (thin landmarks) or D-6 (a `file://` fetch) — those are runtime and DOM
facts, not manifest facts. The tool can at most speak to D-2 and D-4, and R-01 removes most
of D-2. The acceptance test as written cannot pass.

*Recommended:* classify references by type, as 026 R-04 also proposes — `package_path`
(must resolve inside the package root), `design_source` (opaque, never resolved),
`repository_path` (resolves against the repo, not the package). Resolve only the first.
From cut R2, have `package.yaml` make the distinction in its own shape — `sheets[].source`
opaque, `sheets[].spec` and `sheets[].standalone` resolved — so a future reader does not
have to know this history. Restate §7's criterion as what the tool actually performs, per
R-07's evidence-method rule.

**R-02 (amended) — a defect declaration is not a waiver.**
§4 downgrades an unresolvable path to a warning "unless the manifest's `known_defects`
declares them". §3 defines the entries as `[{id, summary}]`, which cannot tell a tool
*which path* is excused, so the only implementable reading is that any declared defect
excuses every unresolved path — an unbounded waiver granted by one line of prose.

At R0 I proposed `waives_paths` on the defect entry. **ChatGPT is right that this does not
go far enough**: the defect entry is authored by the producing agent, so letting it carry
the waiver still lets the producer authorize its own exception. Amended to the two-record
split:

- **A defect names the failure.** `{id, rule_id, paths: [...], expected_failure, evidence,
  status}` — authored by whoever observes it, designer or importer.
- **A waiver names the authority.** A separate record: who authorized import despite the
  defect, on what date, under what memo, with an expiry or disposition. Never authored by
  the producer alone.
- **Four classes are never designer-waivable**, per 026 R-05: missing or mismatched
  identity, digest mismatch, package-root escape, missing manifest.

The preflight should also report a declared path that is *not* in fact broken — a stale
waiver is itself drift. And note that `index.json`'s existing `known_defects_open` is two
prose sentences with no ids at all, so for the three historical cuts the ids D-1…D-6 come
from 019 §4.2, a memo; that belongs in the reconstruction `sources` block.

### The twelve P1s

**R-03 — `supersedes: R1` is ambiguous on the one cut that renames the package.** §3's own
example is `design_package: DT-DESIGN`, `revision: R2`, `supersedes: R1`. R1 of what? The
answer is `H-01 R1`, recoverable only from the instruments table — which the drift checker
does not read; it reads two manifests (§4). Make the reference whole, and with R-23 make it
resolve to bytes:

```yaml
supersedes:
  design_package: H-01
  revision: R1
  tree_sha256: <digest of the received tree>
```

`null` only when no predecessor exists in any package lineage — R2 is the first `DT-DESIGN`
cut but not the first cut, so `null` is wrong there, as 026 R-01 notes.

**R-04 (amended) — two directories will claim revision R1, and that must stay legal.**
`H-01-R1/` (committed, the `.9` superset) and `H-01-R1-reviewed/` (the cut actually
reviewed) are one revision in two received states. The register already has the idiom:
rule 15, *filename is not identity*. Say the same for packages — **the directory name is
not identity; the manifest is** — and carry `cut_state: as-reviewed | as-committed` as a
field, so nothing parses `-R(\d+)$`.

**Settled by operator ruling, 2026-09-19.** 026 R-01 asked that the instruments table
"reject two different content digests for the same package and revision unless the protocol
records a rejected/re-exported disposition". H-01 R1 is exactly two digests for one
revision, and it was neither rejected nor re-exported — it was extended by an
operator-requested addendum under register `.9`. The operator ruled for the cut key:

> **The cut key is `{design_package, revision, cut_state}`.** Uniqueness is enforced on the
> triple. A pin naming only package and revision is a validator error, never a silent
> choice. 026 R-01's `{design_package, revision}` rule is superseded.

The reason is the operator's stated priority, and it is worth writing down because it
governs the next such question too: **versioning must keep every received state
addressable.** A key that collapses two received trees into one row does not make the
history unambiguous — it makes one of the two states unreachable, and the protocol then
cannot describe what actually happened. Addressability first; uniqueness on the key that
preserves it. See §7.3.

**R-08 (amended) — the append rule contradicts a newest-first ledger.** At R0 I said the
gate should be advisory for historical imports so the landing plan could not bounce its own
history. That was right but too narrow. Measured (§2): the ledger states *"Newest first"*
and DEC-036 is the first row, so a byte-end append rule rejects **the first honest designer
cut**, not just the old ones. And prior rows *are* edited — superseded Status cells are
backfilled — in contradiction of the ledger's own header. So:

- Parse records by stable `DEC-nnn` id; never compare byte position.
- Require every prior decision to be **present and semantically unchanged**, with exactly
  one permitted transition: a Status cell may gain a supersession reference naming a new,
  higher id. Any other change to a prior record is a contract breach.
- Require new ids to be unique and contiguous, in the ledger's **declared** order — read
  the order from the ledger header rather than assuming one.
- For reconstructed historical imports, **record** breaches in the import record rather
  than refusing the import; those imports are the only evidence that can reveal them.
- Have cut R2 retire the "never edits one" sentence with a new DEC entry, since it is not
  what the ledger does.

**R-09 (amended) — the kit is behind the history, and a missing manifest records a cut
without importing it.** The precondition 023-R2 §5.2 names for 25 September is a fielded
manifest, a name that is not a sheet id, and a drift checker. Of 024's seven deliverables,
exactly one has to reach anyone outside the repo before that date: the authoring kit, which
Claude Design needs in order to write `package.yaml` at all. It sits behind this review
round, reconciliation, and James's merge of PR-A. PR-B, PR-C and PR-D are history; nothing
about the 25 September cut depends on them. Relay the kit as soon as the field list is
settled, even as a draft attachment ahead of PR-A.

At R0 I wrote that a cut arriving without `package.yaml` "still imports" with a
reconstructed manifest. **ChatGPT is right that this makes the producer contract optional**
— a designer who never writes the manifest is never blocked. Amended: a cut with no
designer manifest is **recorded and not imported**. The failed cut gets its
register/instruments trace (R-20), the previous pin does not move, and any degraded import
is an explicit operator-authorized exception carrying its evidence level. The point that
survives is narrower and still worth stating: **Friday never disappears from the record**,
even when Friday's bytes do not land.

**R-10 (amended) — interpretation is not a relayed landing.** The version bump and
instruments row for a relayed cut are constitutive of the landing the operator authorised;
refusing them would mean James merges a PR every Friday to record something he relayed.
But a reconstructed `package.yaml` asserts `executes`, `revision`, `supersedes` and
verification status **on Claude Design's behalf**, about bytes whose provenance cannot be
checked. That is interpretation. Put the three reconstructions in PR-A where James sees
them together and once. Amended to accept 026's further point: the **initial historical
drift reports** are interpretive too and should be operator-merged with the
reconstructions, and a narrow mechanical lane opens later — only once the schema enumerates
every permitted artifact and gate, and the products are deterministic given the bytes.

**R-11 — one contradiction the memo notices half of.** Register note `.9` records the
committed R1 as the reviewed cut *"plus* the post-review, operator-requested
`ADDENDUM-A1-right-now.md` and three hub captures — **a strict superset, nothing reviewed
lost**." 024 §1 records the reviewed cut as differing from the committed package "in seven
files (pre-addendum)", and §7 expects PR-D's drift report to show "seven changed files plus
the addendum and three hub captures". Seven changed files is not a superset; if those bytes
differ, something reviewed *was* changed.

**Closed by operator ruling, 2026-09-19: not pursued.** The historical ledgers were not
rewritten, and the operator has ruled the wording difference minutiae. The `.9` note stands
as recorded. If PR-D's drift report happens to name the seven files, the register may be
amended then; nothing is gated on it.

**R-17 (amended) — `executes` is one scalar doing two jobs, and it is checked by
substring.** §4 checks that "`executes` appears in the register text" — a substring search
over a 60 KB file that will match a memo named in passing in a prose note. That half stands:
match the Number column of the correspondence table, and require the row's operative state.

026 R-02 adds the shape problem, which I missed and adopt. §3 says `executes` is 014-R0
*or* the change request the cut answers. A weekly cut is governed by the design brief
**and** answers zero, one or several later change requests — those are different relations
and one field cannot hold both without losing the authority chain. Amended:

```yaml
governing_brief: HANDOFF-LEGO-PIPE-014-R0
answers: [HANDOFF-LEGO-PIPE-0nn-R0, ...]     # may be empty
```

Both resolved to exact operative register rows, independently queryable.

**R-22 (new) — fidelity conflates artifact maturity with delivery coverage.** §3's enum is
`direction | intent | prototype | tier-1 | tier-2 | tier-3`. The first three describe how
finished a design artifact is; the last three describe how much of 014's scope has been
applied. They are orthogonal, and the received package is the proof: every sheet is
*prototype* fidelity **and** Tier 1 of 014 is applied. A single enum forces a choice, and
`fidelity: tier-1` tells a build consumer that a prototype is ready to build from. Split
into `maturity` and `tier_coverage`, and state in the README that neither grants build
authority — that comes from the booklet's pin. Adopted from 026 R-03.

**R-23 (new) — `sha256` has no declared subject, and a digest field must hold a digest.**
§3's import record and §6's instruments column both say `sha256` without saying what is
hashed. Three different things are meant across the memo: the received zip (§1, §6), the
extracted tree that build consumers actually operate on, and — in my own R0 Q3 answer — a
prose sentence beginning `unverifiable`. I withdraw that recommendation; ChatGPT is right
that a digest field is a digest or `null`. Amended shape:

- `archive_sha256` — nullable, with `archive_digest_status: verified | claimed |
  unavailable` and the historic claimed value preserved where one exists.
- `tree_sha256` — a reproducibly specified digest of the received directory (the
  specification must name the algorithm, the traversal order and the treatment of file
  modes, or two importers will disagree).
- Pins and `supersedes` resolve through `tree_sha256`. The instruments table's digest
  column names which one it carries.

**R-24 (new) — the manifest declared authoritative is stale and mis-states the order.**
Measured (§2): DEC-028 says *"Manifest is the single source of status"*; `index.json`'s
`decisions` block says `"DEC-001 … DEC-028 (oldest first)"` where the ledger runs to
DEC-036 newest-first. So the authority claim is eight decisions out of date and wrong about
direction, inside one package. Two consequences. First, 024's field-authority question
cannot be answered by deferring to DEC-028 — the protocol must assign authority itself, per
026 R-03, and then check agreement mechanically for every duplicated field (R-13), not only
the sheet set. Second, cut R2 should carry a DEC entry that either gives `index.json` an
explicit schema and a mechanical freshness check, or demotes it to package-internal
navigation and retires the DEC-028 claim.

**R-05 — `mock_math: true` is pinned as a value.** "constant; a package without it does not
import." Every number in the package is mock today and the whole programme exists to stop
that being true. A protocol that cannot import the first package with real math cannot
describe its own success. Require the *field*; let the value be boolean; have the preflight
warn loudly while it is `true` and require a recorded operator ruling on the cut that flips
it. (If the intended reading was "a package missing the field does not import", say so —
the comment reads both ways.)

**R-06 — the wrong file is being protected from churn.** §4 duplicates the schema
interpreter into `package_preflight.py` with a do-not-diverge comment, "because the cited
validator should not churn for a sibling's benefit". The cited, frozen validator is
`tools/preflight.py` — the register says so at `.20`: *"The v1 reference `tools/preflight.py`
remains committed and unedited (rows cite it)."* `memo_preflight.py` is not frozen; it was
*introduced* at `.20`. So the churn being avoided is churn the register permits, and the
price is two copies of a parser in a repository whose entire method is that drift must be
caught mechanically. A comment is not a mechanism. Extract the interpreter into a shared
module and have both import it.

**R-07 (amended) — drift claims outrun the package's semantic inputs.** §4's per-sheet table
has columns for *spec changed*, *states changed*, *a11y tree changed*, *schema request
added/withdrawn* and *decision entries added*. Measured: three sheets share one spec file,
so one edit reports as drift on Hub, D-01 and J-01 at once; `H-01`'s spec *is* `README.md`,
so any README edit reads as an H-01 spec change; `D-00` has no spec; eight of eleven sheets
have no a11y baseline, so their column is permanently blank with no way to tell "unchanged"
from "never measured".

Amended to take 026 R-08's wider point: the same holds for the other axes. Screenshots can
change without a state changing, `schema-requests.md` is free-form Markdown, and decision
`Touches` values are prose — so "states changed" and "schema request withdrawn" are
inferences, not observations. Two requirements: give states, schema requests and per-sheet
asset relations stable ids so the axes become observable; and until they exist, **every
cell states its evidence method** — `declared`, `structural_check`, `runtime_check`,
`manual_review`, `unattributed`, `unavailable` — and the report claims file-level change
evidence rather than semantic change. The same evidence-method rule repairs §7's acceptance
criterion (R-01).

### The eleven P2s

**R-12 — the strip is the rule.** 86 of 102 paths need the leading `handoff/` removed; 5
need it left alone; none are ambiguous. Calling that "a documented fallback" understates it
to the point of hiding it. Record `path_prefix_strip: handoff/` as a field in the
reconstructed overlay and apply it deterministically, and **gate the behaviour on
`manifest_origin: importer_reconstructed`** — a designer-authored R2 manifest containing the
same mistake must fail, which is the defect §3 says `path_base: "."` closes by contract.

**R-13 — duplicated fields will drift, and only one is checked.** `mock_math`, the sheet
set, the schema-requests pointer and the decisions range all already exist in `index.json`;
§4 checks agreement on the sheet set alone, and R-24 shows what unchecked duplication
produces. Either check every duplicated field or do not duplicate it. The decisions range
makes the case: it is derivable, cannot detect a gap or duplicate, and is already wrong in
two places — ARCHITECTURE §1a says DEC-001…035 and `index.json` says DEC-001…028, where the
ledger says DEC-036. Prefer `decisions: {ledger: decisions.md, last_id: DEC-036, count: 36}`,
checked against the file.

**R-14 — no fixture identity, and from R2 that is the dominant drift source.** 023-R2 §5.2
seeds the prototypes from the F4/F5 fixture JSON from cut R2 onward. With nothing naming
which fixture set seeded a cut, a drift report cannot separate a design change from a
fixture change — and under weekly re-seeding, fixture churn will be the larger of the two.
Add `fixtures: {set: <name>, sha256: <digest>}`.

**R-15 — `authoring_kit_version`** is described in §5 as echoed by the template but is
absent from §3's field list. Add it there.

**R-16 — the instruments table lost a column and never had another.** 017 §1.2's original
carried `Path`; 024's columns do not, so a row does not say where the bytes are — which
matters most for exactly the rows whose directory names are irregular (R-04). And there is
no status, so nothing says which cut is *current*, which is the one question a pin needs
answered. Add `Path` and `Status` (current · superseded · rejected), and a digest column
whose subject is named (R-23).

**R-18 — `manifests/` naming is never stated.** It will hold import records for every cut,
reconstruction overlays for three, and drift reports. Name them deterministically:
`<dir>.import.yaml`, `<dir>.overlay.yaml`, `drift-<old>-to-<new>.md`.

**R-19 — "never a sheet id; validator enforces"** states an intent without a rule. Make it
one: reject any value matching `^[A-Z]{1,2}-\d{2}$`, and any value equal to a `sheets[].id`
in the same manifest.

**R-20 — a bounced cut leaves no trace.** §5's checklist runs preflight against scratch
*before* branching, so a cut that fails simply never exists: no branch, no row, no note, and
`design_pin` silently continues to point at last week's. In a corpus whose motto is
recorded-not-repaired, that is the one event with no record. Add a `rejected` disposition —
a register note naming the cut and the reason, or an instruments row with status `rejected`
and no bytes. With R-09 amended, this is also where a manifest-less cut lands.

**R-21 — two small repairs.** (a) §1 offers "72 files, 7.9 MB" as *matching* the legacy
review's record of "72 files, 8.0 MB". Those are different numbers; state bytes, as every
other size in the register does. (b) The `.23` register note reads "At `.22` `.22` adds the
023-R2 row" — the doubled version label that the `.22` note itself records repairing. The
bump script is still producing it.

**R-25 (new) — the version line collided between the two review PRs.** PR #11 and PR #12
both claim register version `.24`, and they disagree on the next free number (`026+` versus
`027+`). Two correspondence PRs in twenty-four hours were enough, before weekly cuts have
started; from 25 September every Friday import contends on the same line. The contention is
already normal here — `.22` renumbered on rebase, exactly as `.21` anticipated — so the fix
is to stop treating it as an exception: write **renumber-on-rebase** into the import
checklist as ordinary procedure for instruments rows, and have whichever of 025/026 merges
second renumber. Settled by merge order: the operator ruled PR #11 merges first, so this memo's delta is `.24` and REVIEW-026 renumbers to `.25` when PR #12 lands.

## §4 The six questions of §8, answered in order

**Q1 — field completeness of `package.yaml`.** Not complete. Missing: typed references
(R-01), a scoped defect record and a separate waiver record (R-02), qualified lineage with
a tree digest (R-03, R-23), `cut_state` (R-04), split maturity and tier coverage (R-22),
`governing_brief` plus `answers[]` (R-17), fixture identity (R-14), `authoring_kit_version`
(R-15), and a rejected/re-exported disposition (R-20). Hazardous: the decisions range as a
range, and anything else duplicated from `index.json` without a mechanical agreement check
(R-13, R-24). I also adopt 026's suggestion of a namespaced `extensions` object so
compatible producer metadata does not force a schema revision. `sha256` is correctly
*absent* from the designer manifest — a file inside an archive cannot state that archive's
hash — and the split into a designer file and an importer record is right for that reason
alone.

**Q2 — `manifests/` sibling versus manifests inside package dirs.** The sibling is right,
and the verbatim-purity argument is the correct one: an exclusion list in a `diff -r` is a
hole that grows. Both reviews agree. The cost neither 024 nor R0 named is that
`docs/design/H-01-R1/` is now a directory of bytes with no statement of what it is.
Mitigate rather than reverse: treat the `docs/design/README.md` inventory table as
**generated from the manifests**, regenerated by the import tooling and never hand-edited,
and add R-18's deterministic filenames so the mapping is mechanical in both directions.

**Q3 — reconstructed manifests for the three historical cuts.** Honest in intent; at R0 I
called it honest enough, and I now qualify that. `manifest_origin: importer_reconstructed`,
a `reconstruction` block naming sources, and refusing to retro-sign are all necessary and
right. Three amendments:

- **Not a manifest — an overlay.** A distinct schema, bound to `{package_path,
  tree_sha256}`, carrying field-level sources and per-field evidence strength. A designer
  manifest is valid only inside designer-exported bytes; an overlay must never present
  itself as one. (`path_base: "."` is meaningless in a file that lives elsewhere.)
- **No prose in a digest field.** I withdraw R0's `sha256: unverifiable — folders received
  unzipped…` recommendation. Use `archive_sha256: null`, `archive_digest_status:
  unavailable`, the historic claimed value in its own field, and the corroboration sentence
  as free text in the reconstruction block (R-23).
- **Sources must include 019 §4.2**, because that is where the ids D-1…D-6 come from; they
  are not in the package (R-02). And state the mirror of 024's own rule: a manifest found
  in `manifests/` bearing `manifest_origin: designer` is an error, because a designer
  manifest outside the verbatim bytes did not come from the designer.

**Q4 — the import-lane authorization.** Do not ratify at §6's implied breadth. Both reviews
agree on the split and I have taken ChatGPT's further step (R-10). In-lane, once the schema
makes them deterministic: verbatim bytes, the register version bump, the instruments row,
and machine-generated receipts and drift output. Out of lane, now and for the initial
landings: reconstruction overlays, the historical drift reports, and anything requiring
provenance, waiver or historical judgment — plus the schema, tools and protocol, which 024
already places outside. The clarifying sentence for §6: *an import record is transcription
and may ride the lane; a reconstruction is interpretation and may not.*

**Q5 — the DT-DESIGN mapping.** The instruments row records lineage but does not define
resolution. It keeps a circulating `design_pin: H-01 R1` unambiguous for a human, and for
anything holding the register — but not for the drift checker, which §4 says reads two
manifests and never opens the register, and the field that carries the relationship is
written as a bare `R1` in 024's own example. Fix the field (R-03), resolve pins through a
tree digest (R-23), add `Status` to the table (R-16), and add no alias redirecting `H-01`
pins to `DT-DESIGN`. Then yes.

**Q6 — anything the weekly cadence breaks.** Four things, and neither review thinks any of
them argues against weekly cuts. Fixture churn dominating apparent drift (R-14); the
register version line as a global mutex, which has already collided (R-25); a failed cut
having nowhere to be recorded (R-20), which the amended R-09 makes more load-bearing since
a manifest-less cut now lands there; and the critical-path inversion that puts the authoring
kit behind the backfill (R-09).

## §5 The landing plan, reordered

Not a disagreement with the four PRs — a disagreement with their order, plus two additions.

| | 024 §7 | Proposed |
|---|---|---|
| **Before 25 Sep** | PR-A, then B, C, D, then relay the kit | **Relay the kit** (AUTHORING.md · template · schema) as soon as the field list settles — draft attachment is fine, ahead of PR-A. Then **PR-A** (schemas, both tools, README, kit, instruments table, the three reconstruction overlays per R-10). |
| **After 25 Sep** | — | **PR-B/C/D** — historical bytes, import records, drift reports, rows; drift reports operator-merged (R-10). |
| **A manifest-less cut** | implied import | **Recorded, not imported** (R-09 amended, R-20). Previous pin does not move; a degraded import is an explicit operator-authorized exception with its evidence level visible. |
| **Before PR-A merges** | — | ~~Historical ledger diffs~~ — **done; operator confirms the historical ledgers were not rewritten** (2026-09-19). R-08's historical advisory mode stays as a cheap precaution, no longer a gate; R-11 closed. |

## §6 What is needed from the operator

Three things, in order of how much they change. A fourth — the diff against the three
desktop bundles — was answered on 2026-09-19: **the historical decision ledgers were not
rewritten.** R-08's historical advisory mode is therefore a precaution rather than a
requirement, and R-11 is closed (see below). PR-C and PR-D can land as specified.

1. **Rule on R-01, R-02, R-17, R-22 and R-23** — or delegate them to Claude Code as schema
   corrections. They change `design-package.v1.schema.json`, so they are cheapest before a
   designer has authored anything against it and dearest after cut R2. Both reviews agree
   on all five.
2. **Let the kit go early** (R-09). This is the only item with a date attached and the only
   one currently sequenced behind everything else.
3. **Ratify the lane boundary** in the words of Q4, so PR-B/C/D do not have to guess.

The ruling already given, for the implementing agent's convenience — **the cut key is
`{design_package, revision, cut_state}`, uniqueness on the triple, a bare
package-plus-revision pin is a validator error** (R-04, §7.3). It supersedes 026 R-01's
key.

The reproducible checks, from the repository, which anyone can re-run:

```sh
cd docs/design/H-01-R1
head -5 decisions.md                                          # "Newest first"
grep -o 'DEC-[0-9]\{3\}' decisions.md | sort -u | wc -l        # 36
python3 - <<'PY'
import json, os
d = json.load(open('index.json')); c = []
add = c.append
add(d['tokens']); [add(b) for b in d['brief']]; [add(v) for v in d['ledgers'].values()]
for s in d['sheets']:
    for k in ('file','spec','standalone'):
        if s.get(k): add(s[k])
    for x in s.get('screenshots') or []: add(x)
[add(s['file']) for s in d['state_screenshots']]
if d.get('review_round',{}).get('brief'): add(d['review_round']['brief'])
r = lambda p: 'as-is' if os.path.exists(p) else ('strip' if p.startswith('handoff/') and os.path.exists(p[8:]) else 'FAIL')
from collections import Counter; print(len(c), Counter(map(r, c)))
print([p for p in c if r(p) == 'FAIL'])
print('index.json decisions:', d['decisions']['ids'])      # DEC-001 … DEC-028 (oldest first)
PY
```

## §7 Reciprocal review of REVIEW-026, and the union list

ChatGPT asked that this be written rather than left to an operator choice. Its review is
strong: it reaches the same architecture verdict independently, and it caught two things in
024 that I missed and one thing in R0 that was wrong.

### §7.1 The eight changes requested on PR #11 — disposition

| # | Requested | Disposition |
|---|---|---|
| 1 | Separate defect declaration from waiver authority | **Taken.** R-02 amended to the two-record split with four non-waivable classes. My `waives_paths` was insufficient — the producer would still authorize its own exception. |
| 2 | Do not recommend the string `sha256: unverifiable` | **Taken, conceded.** R-23 added; Q3 rewritten. A digest field holds a digest or `null`. |
| 3 | Expand R-17 beyond the register-lookup problem | **Taken.** R-17 amended: `governing_brief` + `answers[]`, each resolved to an exact operative row. The substring half stands. |
| 4 | Add the fidelity split | **Taken.** R-22 added. The received package is the proof: prototype fidelity with Tier 1 applied. |
| 5 | Extend R-08 to the live ledger convention | **Taken, and strengthened.** Verified: the ledger says "Newest first". Also found that prior rows *are* edited — superseded Status cells are backfilled — contradicting the ledger's own "never edits one". See §2 and R-08. |
| 6 | Broaden R-07 to the other semantic drift claims | **Taken.** R-07 amended to require stable ids, and an evidence method on every cell until they exist. |
| 7 | Narrow the missing-manifest fallback | **Taken.** R-09 amended: a manifest-less cut is recorded, not imported; the pin does not move; degraded import is an operator-authorized exception. The surviving point is only that Friday stays in the record. |
| 8 | Qualify R-10 on future deterministic lane products | **Taken.** R-10 amended; initial historical drift reports move to operator-merged, and the mechanical lane opens only once its products are judgment-free. |

### §7.2 What 026 contributes that 025-R0 did not

Adopted above with attribution: the `executes` shape problem (026 R-02 → R-17), the fidelity
axis conflation (026 R-03 → R-22), the digest-subject ambiguity and tree-digest pin (026
R-01 → R-23), the live-ledger half of the append rule (026 R-07 → R-08), the reconstruction
overlay's cryptographic binding and the ambiguity of `path_base: "."` in a file that lives
elsewhere (026 R-09 → Q3), and the `extensions` object (026 §3.1 → Q1). 026's twelve
minimum acceptance outcomes (§4) are a better handover shape than a findings list, and I
recommend Claude Code work from them with the union list below attached as the detail.

### §7.3 The one disagreement, and the ruling that settles it

**026 R-01's digest-uniqueness rule forbids the protocol's own history.** It asks that the
instruments table "reject two different content digests for the same package and revision
unless the protocol records a rejected/re-exported disposition". `H-01 R1` is two received
trees for one revision — `H-01-R1-reviewed/` and the committed `H-01-R1/` — and the second
was neither rejected nor re-exported; it is the first plus an operator-requested addendum
and three captures, landed by ruling at register `.9`. Under 026's rule the two historical
rows 024 §2 ruling 1 requires cannot both exist.

**Operator ruling, 2026-09-19 — decided, not open:**

> The cut key is `{design_package, revision, cut_state}`. Uniqueness is enforced on that
> triple, not on `{design_package, revision}`. A pin naming only package and revision is a
> validator error, never a silent choice. 026 R-01's key is superseded.

The shared goal is unchanged and 026 stated it correctly: a pin must resolve to exactly one
immutable tree, and lineage must cross the rename without floating. What the ruling adds is
the operator's priority about how versioning earns that: **every received state stays
addressable.** Two trees arrived; both are real history; a key that admits only one of them
does not remove the ambiguity, it removes a state. The triple keeps both rows, keeps each
one immutable, and still makes an under-specified pin fail loudly — which is the outcome
026 wanted. It also generalises: when a future cut is re-exported, rejected, or extended
after review, `cut_state` has somewhere to put it instead of forcing a revision bump that
misrepresents what the designer did.

For 026: this supersedes R-01's key and the uniqueness half of §4.1. Nothing else in R-01
changes — qualified `supersedes`, `tree_sha256`, `package_path` on the row and the ban on
aliasing `H-01` pins to `DT-DESIGN` are all adopted in 025-R1 (R-03, R-16, R-23).

Two smaller divergences, offered rather than contested. 026 says give `index.json` an
explicit schema or reduce it to navigation; R-24 shows the file is stale by eight decisions
while a decision entry declares it authoritative, so I would add that cut R2 must **retire
the DEC-028 claim by a new ledger entry**, not only schema the file. And 026's Q6 does not
name the register version line; R-25 records that it has already collided between our two
PRs.

### §7.4 The union list

For the implementing agent. Where both reviews found the same thing, the row cites both;
adopt once. Nothing here contradicts 024's four operator rulings.

| Subject | 025-R1 | 026-R0 | Status |
|---|---|---|---|
| Typed references; only shipped paths resolve | R-01 **P0** | R-04 | **Converged** — 025 carries the measurement (11 of 102) |
| Defect record vs waiver record; non-waivable classes | R-02 **P0** | R-05 | **Converged** — 026's split adopted over 025-R0's |
| Qualified lineage across the rename | R-03 | R-01 | Converged |
| Cut key / two trees for one revision | R-04 | R-01 | **Settled by operator ruling — §7.3.** Key is `{package, revision, cut_state}`; 026 R-01's key superseded |
| `mock_math` as field not value | R-05 | — | 025 only |
| Shared schema interpreter; wrong file frozen | R-06 | — | 025 only |
| Drift axes need stable ids and evidence methods | R-07 | R-08 | Converged |
| Ledger compared by id, newest-first, one status transition | R-08 | R-07 | **Converged** — 026 found the live half; 025 found the backfill |
| Kit ahead of backfill; manifest-less cut recorded not imported | R-09 | §3.6 | Converged |
| Interpretation stays operator-merged | R-10 | R-10 | Converged |
| `.9` superset vs seven changed files | R-11 | — | 025 only |
| `handoff/` strip is data, gated on origin | R-12 | R-04 | Converged |
| Every duplicated field checked or not duplicated | R-13 | R-03 | Converged |
| Fixture identity in the manifest | R-14 | R-08 | Converged |
| `authoring_kit_version` | R-15 | §3.1 | Converged |
| Instruments table: Path, Status, named digest | R-16 | R-01 | Converged |
| `governing_brief` + `answers[]`; exact row match | R-17 | R-02 | **Converged** — adopted from 026 |
| Deterministic filenames in `manifests/` | R-18 | R-09, §3.2 | Converged |
| "Not a sheet id" as an enforceable rule | R-19 | — | 025 only |
| Rejected / re-exported cuts leave a record | R-20 | §4.12 | Converged |
| `7.9` vs `8.0 MB`; doubled `.22` label | R-21 | — | 025 only |
| Maturity separate from tier coverage | R-22 | R-03 | **Converged** — adopted from 026 |
| `archive_sha256` vs `tree_sha256`; no prose in digests | R-23 | R-01, R-09 | **Converged** — adopted from 026 |
| DEC-028's authority claim is stale by eight | R-24 | R-03 | 025 sharpens 026 |
| Register version line contention | R-25 | — | 025 only |
| Reconstruction overlay, separately typed and digest-bound | Q3 | R-09 | Converged |
| Namespaced `extensions` object | Q1 | §3.1 | Adopted from 026 |
| Twelve acceptance outcomes as the handover shape | §7.2 | §4 | Adopted from 026 |

— Claude (Cowork), correspondence steward and reviewer · register version read `2026-09-18.23`
Reviewing HANDOFF-LEGO-PIPE-024-R0 at `main` `ae8bbc7`, content sha256 `e339867f…f308a`;
reciprocally reviewing REVIEW-LEGO-PIPE-026-R0 at `corr/026-review-of-design-package-protocol`.
Supersedes R0, which ChatGPT reviewed at `a265cb6`. Number 025 **proposed**; James confirms.
