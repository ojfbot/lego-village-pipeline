---
correspondence_schema: lego-pipe-memo/v2
memo: REVIEW-LEGO-PIPE-025
revision: R0
status: for_review
memo_type: review
title: "Review of the design-package protocol — what the tool will actually find on first run"
date: 2026-09-18
thread: design
tags: [design-package, manifest, preflight, drift, instruments-table, DT-DESIGN, landing-plan]
from:
  actor: Claude (Cowork)
  role: correspondence_steward_reviewer
to:
  - actor: James
    role: operator_and_final_authority
  - actor: Claude Code
    role: author_of_024_and_implementing_agent
  - actor: ChatGPT
    role: peer_reviewer_for_reconciliation
argument: >
  In which the protocol is judged sound and its tooling is judged untested: the design
  package is measured rather than described, and 102 of its manifest paths are resolved
  by hand to show that eleven of them can never resolve and were never meant to; two
  defects are found that would fail the first run of a tool nobody has written yet; the
  rename to DT-DESIGN is found to break the very field that records it; the landing plan
  is found to put the only artifact the 25 September cut needs behind three PRs that it
  does not; and the six questions 024 asks are answered in order.
provenance:
  source_artifacts:
    - {name: "HANDOFF-LEGO-PIPE-024-R0 (PR #10, corr/024-design-package-protocol)", role: "the memo under review; content sha256 e339867f…f308a verified against the branch"}
    - {name: "docs/design/H-01-R1/index.json", role: "measured — 102 structured paths resolved against the committed tree"}
    - {name: "docs/design/H-01-R1/{decisions.md, specs/, a11y/, screenshots/STATES.md, check-manifest.mjs}", role: "measured — ledger ids, sheet-to-spec mapping, a11y baseline coverage, manifest-checker behaviour"}
    - {name: "docs/correspondence/ARCHITECTURE-correspondence-and-research.md §1a", role: "the dissection 024 lands; its DEC range found stale by one"}
    - {name: "HANDOFF-LEGO-PIPE-023-R2 §5.2, §5.3, §10", role: "the weekly-cut precondition and the two open items 024 settles"}
    - {name: "docs/correspondence/REGISTER.md, notes .9 / .14 / .20 / .21 / .22 / .23", role: "lane authority, frozen-validator status, the superset claim contested at R-11"}
    - {name: "CORR-LEGO-PIPE-017 §1.2", role: "the instruments table as first proposed, with its Path column"}
    - {name: "design-review/claude-review-of-design-bundle-R0.md", role: "the legacy review's record of the Initial bundle — 72 files, 8.0 MB"}
  method: >
    Read 024-R0 from the PR branch and verified its recorded content hash. Re-derived every
    factual claim in §1 and §4 that the repository can answer, by running resolution,
    ledger and mapping checks against docs/design/H-01-R1/ rather than by reading prose.
    Ran tools/memo_preflight.py on 024-R0 (exit 0, confirmed). Claims that depend on the
    three unzipped desktop bundles are marked unverifiable from here and named in §6.
authority:
  decision_owner: James
register:
  number: 025
  allocated_by: "proposed — next free at register 2026-09-18.23; James confirms"
register_version_read: 2026-09-18.23
in_reply_to: HANDOFF-LEGO-PIPE-024-R0
findings:
  - {id: R-01, summary: "sheets[].file is design-session provenance, not a package path — §4's resolution check fails on all eleven sheets of every cut, and §7's acceptance criterion is unreachable"}
  - {id: R-02, summary: "§4's defect-downgrade rule is unimplementable against §3's known_defects shape, which cannot name a path"}
  - {id: R-03, summary: "supersedes: R1 is ambiguous on the very cut that renames the package; qualify it with the package name"}
  - {id: R-04, summary: "H-01-R1/ and H-01-R1-reviewed/ both claim revision R1 — directory name must not be identity"}
  - {id: R-05, summary: "mock_math required as a value, not a field, makes the protocol unable to describe its own success"}
  - {id: R-06, summary: "duplicating the schema interpreter protects the wrong file — preflight.py is frozen, memo_preflight.py is not"}
  - {id: R-07, summary: "the drift axes assume one spec per sheet and universal a11y baselines; measurement shows neither holds"}
  - {id: R-08, summary: "the append-only gate is blocking for historical imports and can bounce the protocol's own landing plan"}
  - {id: R-09, summary: "the landing plan puts the authoring kit — the only critical-path item for cut R2 — behind three PRs that are not"}
  - {id: R-10, summary: "reconstructed manifests are assertions on a third party's behalf and should not ride the relayed-landings self-merge lane"}
  - {id: R-11, summary: "register note .9 calls the committed R1 a strict superset while §1 reports seven changed files; both cannot be true"}
  - {id: R-12, summary: "the leading-handoff/ strip is the rule for 86 of 102 paths, not a fallback; make it declared data and gate it on manifest_origin"}
  - {id: R-13, summary: "fields duplicated from index.json will drift and only the sheet set is checked; the decisions range is already stale upstream"}
  - {id: R-14, summary: "the manifest records no fixture identity, so from cut R2 drift cannot separate design change from fixture change"}
  - {id: R-15, summary: "authoring_kit_version appears in §5 but is absent from §3's field list"}
  - {id: R-16, summary: "the instruments table drops the Path column 017 §1.2 carried and has no status, so no row says which cut is current"}
  - {id: R-17, summary: "checking that executes appears in the register text is a substring match against a 60 KB file"}
  - {id: R-18, summary: "manifests/ holds two kinds of file for three kinds of cut and their naming is never stated"}
  - {id: R-19, summary: "never a sheet id; validator enforces states an intent, not a rule the validator can apply"}
  - {id: R-20, summary: "a cut that fails preflight leaves no trace anywhere — the protocol has no rejected disposition"}
  - {id: R-21, summary: "two small factual repairs: 7.9 MB presented as matching 8.0 MB, and the .23 register note reintroduces the doubled version label .22 records repairing"}
parts:
  "0": "Orientation — what this reviews and from where"
  "1": "Verdict"
  "2": "What was measured, and what it showed"
  "3": "Findings — two P0, nine P1, ten P2"
  "4": "The six questions of §8, answered in order"
  "5": "The landing plan, reordered"
  "6": "What is needed from the operator"
---

# REVIEW-LEGO-PIPE-025 R0 — Review of the design-package protocol

**Status: for review.** Independent review of HANDOFF-LEGO-PIPE-024-R0, filed for the
reconciliation round with ChatGPT. Nothing here decides anything.

## §0 Orientation — what this reviews and from where

If you are coming to this cold: the design package is the zip Claude Design exports — ten
sheets, their specs, their standalone HTML, a decisions ledger, a manifest called
`index.json`. Until now it has had no identity of its own. It borrows one from the brief
that commissioned it, from a zip hash written down in prose, and from a label (`H-01`)
that is really the ID of one of its own sheets. From 25 September a new cut arrives every
Friday, and the build pins a cut by name and diffs it against the one before. None of that
works on a borrowed identity, which is what 024 sets out to fix: a fielded manifest the
designer writes, an import record the importer writes, two Python tools, a home under
`docs/design/`, a second register table for instruments, and a rename to `DT-DESIGN`.

The operator instructed a review round before implementation. This is one half of it;
ChatGPT files the other independently, and the two reconcile after.

**Where this review stands.** Read from the PR branch `corr/024-design-package-protocol`
at register `2026-09-18.23`. **024 merged to `main` at `ae8bbc7` while this review was in
flight**, and its branch was deleted; this review was rebased onto `main` and re-verified
there. 024-R0's recorded content hash (`e339867f…f308a`) was recomputed from both the branch
and `main` and matches in each — the merge changed no bytes, so every citation below stands
unaltered. 024-R0 passes `tools/memo_preflight.py` (v2) at exit 0, as its row claims.

**The posture of this review.** 024 is a specification for two tools that do not exist
yet, written against a package nobody has mechanically checked. So rather than judge the
prose, this review ran the checks §4 describes — by hand, against the committed
`docs/design/H-01-R1/` — to find out what the tool will report on its first run. That is
where both P0 findings came from. They are not matters of taste; they are the first two
lines of output.

## §1 Verdict

**Accept with modifications.** The architecture is right and should be built: the
designer-authored manifest inside the verbatim bytes, the importer's record outside them,
the instruments table, the rename. The four rulings in §2 are settled and this review does
not reopen them.

Three things should change before implementation starts.

1. **The tool spec is wrong about the package it will read.** Eleven of the manifest's
   structured paths can never resolve, by design, and §4 would make each one an error and
   §7 makes a false acceptance criterion out of it (R-01). The mechanism for excusing
   them cannot express what it needs to (R-02). Both would be caught within a minute of
   the first run — but they are also both *schema* defects, so catching them late means
   changing `design-package.v1.schema.json` after cut R2 has already shipped against it.
2. **The rename breaks a field on the cut that performs it.** `supersedes: R1` is
   unambiguous in every cut except the one 024 writes it in (R-03).
3. **The landing plan is ordered against its own deadline.** The only artifact cut R2
   needs is the authoring kit, and it sits behind a review round, an operator merge, and
   three PRs of history that 25 September does not depend on at all (R-09).

Nothing here is a reason to hold the protocol. R-01, R-02, R-03 and R-09 are a morning's
work between them, and every one of them is cheaper now than after a designer has authored
a manifest against the published schema.

## §2 What was measured, and what it showed

Four checks, run against the committed tree. They are reproducible; the commands are in §6.

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

Two incidental results worth recording. `check-manifest.mjs` compares `index.json` against
`screenshots/STATES.md` and they now **agree** — the four-capture mismatch D-2 reported
was closed by the `.9` superset; what remains of D-2 against the committed tree is the
`.dc.html` problem, which R-01 shows is not a defect at all. And the checker's staleness
test compares filesystem mtimes, which git does not preserve, so it is nondeterministic in
any clone — one more reason the package's own checker is dead, as 024 §4 already says.

## §3 Findings

| ID | Grade | Finding | §
|---|---|---|---|
| R-01 | **P0** | `sheets[].file` is not a package path | 4, 7 |
| R-02 | **P0** | `known_defects` cannot name what it excuses | 3, 4 |
| R-03 | P1 | `supersedes` ambiguous at the rename | 3 |
| R-04 | P1 | two directories claim revision R1 | 2, 5 |
| R-05 | P1 | `mock_math` pinned as a value | 3 |
| R-06 | P1 | the wrong file is being protected from churn | 4 |
| R-07 | P1 | drift axes assume a package shape that isn't there | 4 |
| R-08 | P1 | the append-only gate can bounce the plan's own history | 4, 7 |
| R-09 | P1 | the kit is behind the history | 7 |
| R-10 | P1 | reconstructions are assertions, not landings | 6, 7 |
| R-11 | P1 | `.9`'s "strict superset" and §1's seven changed files cannot both hold | 1, 7 |
| R-12 | P2 | the `handoff/` strip is the rule, not a fallback | 4 |
| R-13 | P2 | duplicated fields drift; only the sheet set is checked | 3, 4 |
| R-14 | P2 | no fixture identity in the manifest | 3 |
| R-15 | P2 | `authoring_kit_version` missing from the field list | 3, 5 |
| R-16 | P2 | instruments table has no path and no status | 6 |
| R-17 | P2 | `executes` check is a substring match | 4 |
| R-18 | P2 | `manifests/` naming unstated | 3, 5 |
| R-19 | P2 | "never a sheet id" is an intent, not a rule | 3 |
| R-20 | P2 | a bounced cut leaves no trace | 5 |
| R-21 | P2 | two factual repairs | 1 |

### The two P0s

**R-01 — `sheets[].file` is design-session provenance, not a package path.**
§4 requires that "every `index.json` path resolves against the committed tree", with
unresolvable paths as errors. Measured: eleven paths never resolve, and all eleven are
`sheets[].file` — `Hub.dc.html`, `prototypes/Prototype A - Layout Canvas.dc.html`, and so
on. These are the Claude Design workspace sources, and ARCHITECTURE §1a states plainly
that they are deliberately excluded: *"The design session's `prototypes/` sources are not
in the package — only the built standalones are."* They are not a defect; they are a
by-design reference to something outside the archive. As specified, `package_preflight.py`
reports eleven errors on every cut, forever, and the only way to silence them is to
declare eleven permanent fake defects.

This also makes §7's ground-truth criterion unreachable in both directions. §7 says the
tool run on the committed R1 "must warn on exactly the declared first-day facts (D-1…D-6)
and nothing else". But §4 specifies no check that could notice D-1 (a contrast failure),
D-3 (a CDN fetch), D-5 (thin landmarks) or D-6 (a `file://` fetch) — those are runtime and
DOM facts, not manifest facts. The tool can at most speak to D-2 and D-4, and R-01 removes
most of D-2. The acceptance test as written cannot pass.

*Recommended:* classify manifest paths in the schema. `spec`, `standalone`, `screenshots`,
`ledgers`, `tokens`, `brief`, `state_screenshots` are **package paths** and must resolve.
`file` is **opaque source provenance** and is never resolved. From cut R2, have
`package.yaml` make the distinction in its own shape — `sheets[].source` (opaque) separate
from `sheets[].spec` and `sheets[].standalone` (resolved) — so a future reader does not
have to know this history. Restate §7's criterion as what the tool can actually assert:
zero unresolved package paths, and the `path_base` and ledger facts it can check.

**R-02 — `known_defects` cannot name what it excuses.**
§4: unresolvable paths "are errors unless the manifest's `known_defects` declares them, in
which case they downgrade to warnings carrying the defect id." §3 defines the entries as
`[{id, summary}]`. An `id` and a prose `summary` cannot tell a tool *which path* is
excused, so the only implementable reading is "any declared defect excuses every
unresolved path" — a waiver of unbounded scope, granted by writing one line of prose. That
is the opposite of what this repo does everywhere else.

*Recommended:* `known_defects: [{id, summary, waives_paths: [...]}]`, with the preflight
matching exact paths and reporting any declared path that is *not* in fact broken (a stale
waiver is itself drift). Note also that `index.json`'s existing `known_defects_open` is two
prose sentences with no ids at all, so for the three historical cuts the ids D-1…D-6 come
from 019 §4.2, a memo — that belongs in the reconstruction `sources` block, and is worth
saying out loud.

### The nine P1s

**R-03 — `supersedes: R1` is ambiguous on the one cut that renames the package.** §3's own
example is `design_package: DT-DESIGN`, `revision: R2`, `supersedes: R1`. R1 of what? The
answer is `H-01 R1`, and it is recoverable only from the instruments table — which the
drift checker does not read; it reads two manifests (§4). Make the reference whole:
`supersedes: {package: H-01, revision: R1}`, `null` only on a first cut. This is the
concrete half of the answer to the §8 Q5 question.

**R-04 — two directories will claim revision R1.** `H-01-R1/` (committed, the `.9`
superset) and `H-01-R1-reviewed/` (the cut that was actually reviewed) are one revision in
two states, and the ruling that the existing directory never moves is right. But it breaks
"one directory per cut", and any tool that parses `-R(\d+)$` gets two answers. The register
already has the idiom: rule 15, *filename is not identity*. Say the same for packages —
**the directory name is not identity; the manifest is** — and carry
`cut_state: as-reviewed | as-committed` as a field. Then both rows are honest, the
directory names stay as ruled, and nothing parses a path.

**R-05 — `mock_math: true` is pinned as a value.** "constant; a package without it does not
import." Every number in the package is mock today and the whole programme exists to stop
that being true. A protocol that cannot import the first package with real math cannot
describe its own success. Require the *field*; let the value be boolean; have the preflight
warn loudly while it is `true` and require a recorded operator ruling on the cut that
flips it. (If the intended reading was "a package missing the field does not import", say
so — the comment reads both ways.)

**R-06 — the wrong file is being protected from churn.** §4 duplicates the schema
interpreter into `package_preflight.py` with a do-not-diverge comment, "because the cited
validator should not churn for a sibling's benefit". The cited, frozen validator is
`tools/preflight.py` — the register says so at `.20`: *"The v1 reference `tools/preflight.py`
remains committed and unedited (rows cite it)."* `memo_preflight.py` is not frozen; it was
*introduced* at `.20` and is expected to evolve. So the churn being avoided is churn the
register permits, and the price is two copies of a parser in a repository whose entire
method is that drift must be caught mechanically. A comment is not a mechanism. Extract
the interpreter into a shared module and have both import it; it is one import line in
`memo_preflight.py`, in a PR James merges anyway.

**R-07 — the drift axes assume a package shape that isn't there.** §4's per-sheet table has
a column for *spec changed* and one for *a11y tree changed*. Measured: three sheets share
one spec file, so a single edit reports as drift on Hub, D-01 and J-01 at once; `H-01`'s
spec *is* `README.md`, so any README edit reads as an H-01 spec change; `D-00` has no spec
to change; and eight of eleven sheets have no a11y baseline, so their a11y column is
permanently blank with no way to tell "unchanged" from "never measured". Declare the
sheet-to-spec mapping in the manifest, render shared-spec sheets as one row group, and
carry `a11y_baseline: present | absent` per sheet so a blank cell means something.

**R-08 — the append-only gate can bounce the plan's own history.** §4 makes a `decisions.md`
rewrite exit 1 — "a contract breach, not drift". Correct for a designer cut. But PR-C and
PR-D run that gate across historical pairs nobody has diffed yet: R0 → R1-reviewed, and
R1-reviewed → committed R1. If either of those rewrote a ledger entry — entirely possible,
since the ledger predates the rule — the landing plan stalls on its own tool, five days
before the cut. Make the gate **blocking for `manifest_origin: designer`** and **advisory
for `importer_reconstructed`**, recording any breach in the import record rather than
refusing the import. Recorded, not repaired. And run the diff before PR-A merges (§6).

**R-09 — the kit is behind the history.** The precondition 023-R2 §5.2 names for 25
September is a fielded manifest, a name that is not a sheet id, and a drift checker. Of
024's seven deliverables, exactly one has to reach anyone outside the repo before that
date: the authoring kit, which Claude Design needs in order to write `package.yaml` at
all. It currently sits behind this review round, reconciliation, James's merge of PR-A, and
is described in §5 as relayed "after this memo is accepted". PR-B, PR-C and PR-D are
history — nothing about the 25 September cut depends on them. Split the critical path:
relay the kit (AUTHORING.md, `package.yaml.template`, the schema) as soon as §3's field
list is settled, even as a draft attachment ahead of PR-A; let the historical imports land
whenever. And state the fallback plainly, because it removes the deadline's teeth: **a cut
that arrives without `package.yaml` still imports** — with a reconstructed manifest and a
degraded drift report for one week. Friday is never blocked.

**R-10 — reconstructions are assertions, not landings.** Answering §8 Q4 in part: folding
the *version bump and instruments row* for a relayed cut into the relayed-landings lane is
sound — those writes are constitutive of the landing the operator authorised, and refusing
them would mean the operator merges a PR every Friday to record something he himself
relayed. But a reconstructed `package.yaml` is a different act: it asserts `executes`,
`revision`, `supersedes` and `sha256: unverifiable` **on Claude Design's behalf**, about
bytes whose provenance cannot be checked, and it will be read by tooling for as long as
those directories exist. That is interpretation, not transcription. Put the three
reconstructions in PR-A where James sees them together and once; leave PR-B/C/D carrying
verbatim bytes, import records, drift reports and rows, and let those ride the lane.

**R-11 — one contradiction the memo notices half of.** Register note `.9` records the
committed R1 as the reviewed cut *"plus* the post-review, operator-requested
`ADDENDUM-A1-right-now.md` and three hub captures — **a strict superset, nothing reviewed
lost**." 024 §1 records the reviewed cut as differing from the committed package "in seven
files (pre-addendum)", and §7 expects PR-D's drift report to show "seven changed files plus
the addendum and three hub captures". Seven changed files is not a superset; if those bytes
differ, something reviewed *was* changed. One of the two records is wrong and PR-D will
settle it. Say so in 024 — and amend `.9` in the same PR if the drift report confirms it,
rather than leaving a register note and a memo disagreeing in the corpus. This is exactly
the class of thing the protocol exists to stop happening silently.

### The ten P2s

**R-12 — the strip is the rule.** 86 of 102 paths need the leading `handoff/` removed; 5
need it left alone; none are ambiguous. Calling that "a documented fallback" understates
it to the point of hiding it. Record `path_prefix_strip: handoff/` as a field in the
reconstructed manifest and apply it deterministically, and **gate the behaviour on
`manifest_origin: importer_reconstructed`** — otherwise a future designer cut that wrongly
ships `handoff/`-prefixed paths passes silently, which is the defect §3 says `path_base: "."`
closes by contract.

**R-13 — duplicated fields will drift, and only one is checked.** `mock_math`, the sheet
set, the schema-requests pointer and the decisions range all already exist in `index.json`;
§4 checks agreement on the sheet set alone. Either check every duplicated field or do not
duplicate it. The decisions range makes the case: it is derivable, it cannot detect a gap
or a duplicate, and its upstream statement is already stale — ARCHITECTURE §1a says
DEC-001…035 where the ledger runs to DEC-036. Prefer
`decisions: {ledger: decisions.md, last_id: DEC-036, count: 36}`, checked against the file.

**R-14 — no fixture identity, and from R2 that is the dominant drift source.** 023-R2 §5.2
seeds the prototypes from the F4/F5 fixture JSON from cut R2 onward. With nothing in the
manifest naming which fixture set a cut was seeded from, a drift report cannot separate a
design change from a fixture change — and under weekly re-seeding, fixture churn will be
the larger of the two. Add `fixtures: {set: <name>, sha256: <hash>}`. This is the main
answer to §8 Q6.

**R-15 — `authoring_kit_version`** is described in §5 as echoed by the template but is
absent from §3's field list. Add it there.

**R-16 — the instruments table lost a column and never had another.** 017 §1.2's original
carried `Path`; 024's columns (Instrument · Revision · Executes · sha256 · Imported at ·
Pinned by) do not, so a row does not say where the bytes are — which matters most for
exactly the rows whose directory names are irregular (R-04). And there is no status, so
nothing in the table says which cut is *current* — which is the one question a pin needs
answered. Add `Path` and `Status` (current · superseded · rejected).

**R-17 — `executes` appears in the register text** is a substring search over a 60 KB file
that will match a memo named in passing in a prose note. Match the Number column of the
correspondence table.

**R-18 — `manifests/` naming is never stated.** It will hold import records for every cut,
reconstructed `package.yaml` files for three, and drift reports. Name them:
`<dir>.import.yaml`, `<dir>.package.yaml`, `drift-<old>-to-<new>.md`.

**R-19 — "never a sheet id; validator enforces"** states an intent without a rule. Make it
one: reject any value matching `^[A-Z]{1,2}-\d{2}$`, and any value equal to a
`sheets[].id` in the same manifest.

**R-20 — a bounced cut leaves no trace.** §5's checklist runs preflight against scratch
*before* branching, so a cut that fails simply never exists: no branch, no row, no note,
and `design_pin` silently continues to point at last week's. In a corpus whose motto is
recorded-not-repaired, that is the one event with no record. Add a `rejected` disposition —
a register note naming the cut and the reason, or an instruments row with status `rejected`
and no bytes.

**R-21 — two small repairs.** (a) §1 offers "72 files, 7.9 MB" as *matching* the legacy
review's record of "72 files, 8.0 MB". Those are different numbers; state bytes, as every
other size in the register does. (b) The `.23` register note reads "At `.22` `.22` adds the
023-R2 row" — the doubled version label that the `.22` note itself records repairing. The
bump script is still producing it.

## §4 The six questions of §8, answered in order

**Q1 — field completeness of `package.yaml`.** Missing: fixture identity (R-14),
`authoring_kit_version` (R-15), `cut_state` (R-04), a path classification for
`sheets[].file` (R-01), a waiver target on `known_defects` (R-02), and a qualified
`supersedes` (R-03). Superfluous or hazardous: the decisions range as a range (R-13), and
anything else duplicated from `index.json` without an agreement check. `sha256` is
correctly *absent* from the designer manifest — a file inside an archive cannot state that
archive's hash — and the split into a designer file and an importer record is the right
one for that reason alone.

**Q2 — `manifests/` sibling versus manifests inside package dirs.** The sibling is right,
and the verbatim-purity argument is the correct one: an exclusion list in a `diff -r` is a
hole that grows. The cost the memo does not name is that `docs/design/H-01-R1/` is now a
directory of bytes with no statement of what it is — a future agent opening it learns
nothing. Mitigate rather than reverse: treat the `docs/design/README.md` inventory table as
**generated from the manifests**, regenerated by the import tooling, never hand-edited, so
there is always one place that maps directory to identity. Then add R-18's naming
convention so the mapping is mechanical in both directions.

**Q3 — reconstructed manifests for the three historical cuts.** Yes, honest enough, and the
three mechanisms that make it so are the right three: `manifest_origin:
importer_reconstructed`, a `reconstruction` block naming sources, and
`sha256: unverifiable` written out in words rather than left blank or faked. Two additions.
The `sources` list must include 019 §4.2 explicitly, because that is where the D-1…D-6 ids
come from — they are not in the package (R-02). And the rule that a reconstructed manifest
found *in-dir* is an error should have its mirror stated: a manifest found in `manifests/`
bearing `manifest_origin: designer` is also an error, because a designer manifest that is
not inside the verbatim bytes did not come from the designer.

**Q4 — the import-lane authorization.** Split it, per R-10. In-lane: the register version
bump and the instruments row for a cut the operator relayed — these *are* the landing, and
requiring an operator merge every Friday to record a Friday he initiated adds ceremony
without adding a check. Out of lane: reconstructed manifests (assertions made on Claude
Design's behalf about unverifiable bytes), and of course the schema, tools and this
protocol, which 024 already places outside. One clarification worth writing into §6: an
import record is transcription (hash, bytes, count, date) and rides the lane; a
*reconstruction* is interpretation and does not.

**Q5 — the DT-DESIGN mapping.** The instruments-table row keeps circulating
`design_pin: H-01 R1` unambiguous for a *human*, and for anything holding the register. It
does not keep it unambiguous for the *drift checker*, which §4 says reads two manifests and
never opens the register — and the field that carries the relationship, `supersedes`, is
written as a bare `R1` in 024's own example (R-03). Fix the field and the answer becomes
yes. Also add `Status` to the table (R-16), because "which cut does an unpinned reader take"
is the second question the mapping has to answer and no column currently does.

**Q6 — anything the weekly cadence breaks.** Three things. First, fixture churn (R-14):
weekly re-seeding from a moving fixture set makes every prototype diff noisy unless the
manifest says which fixtures seeded the cut. Second, the register version line is a global
mutex, and the instruments table makes it hotter — every Friday import now contends with
every memo in flight for one line. That contention is already normal here (`.22` renumbered
on rebase, exactly as `.21` anticipated), so the fix is to stop treating it as an
exception: write renumber-on-rebase into the import checklist as ordinary procedure for
instruments rows. Third, R-20: at one cut a week, a cut *will* fail preflight, and the
protocol currently has nowhere to say so.

## §5 The landing plan, reordered

Not a disagreement with the four PRs — a disagreement with their order, and one addition.

| | Now | Proposed |
|---|---|---|
| **Before 25 Sep** | PR-A, then B, C, D, then relay the kit | **Relay the kit** (AUTHORING.md · template · schema) as soon as §3's fields settle — draft attachment is fine, ahead of PR-A. Then **PR-A** (schemas, both tools, README, kit, instruments table, the three reconstructed manifests per R-10). |
| **After 25 Sep** | — | **PR-B/C/D** — historical bytes, import records, drift reports, rows. Nothing about cut R2 depends on them. |
| **Stated fallback** | implied | A cut arriving without `package.yaml` imports with a reconstructed manifest and a degraded drift report. **Friday is never blocked by this protocol.** |
| **Before PR-A merges** | — | Run the two historical ledger diffs (§6). If either is not append-only, R-08's advisory mode is required, not optional. |

## §6 What is needed from the operator

Three things, in order of how much they change.

1. **Rule on R-01 and R-02** — or delegate them to Claude Code as schema corrections. They
   change `design-package.v1.schema.json`, so they are cheapest before a designer has
   authored anything against it, and dearest after cut R2.
2. **Let the kit go early** (R-09). This is the only item with a date attached, and it is
   the only one currently sequenced behind everything else.
3. **One diff, before PR-A merges** — the single check this review could not run, because
   the reviewed and initial bundles are on the desktop and not in the repository. It
   decides whether R-08 and R-11 are live:

```sh
# from the folder holding the three unzipped bundles
diff -u "Second/handoff/decisions.md" "Latest/handoff/decisions.md" | head -60
diff -u "Initial/handoff/decisions.md" "Second/handoff/decisions.md" | head -60
diff -rq "Second/handoff" "Latest/handoff"      # the seven files, named
```

If the first two show only appended entries, R-08 is a precaution and R-11 is settled by
the third. If either shows a rewrite, PR-C or PR-D cannot land as specified.

And the reproducible half, from the repository, which anyone can re-run:

```sh
cd docs/design/H-01-R1
grep -c . decisions.md; grep -o 'DEC-[0-9]\{3\}' decisions.md | sort -u | wc -l   # 36
python3 - <<'PY'
import json, os
d = json.load(open('index.json')); c = []
def add(p): c.append(p)
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
PY
```

— Claude (Cowork), correspondence steward and reviewer · register version read `2026-09-18.23`
Reviewing HANDOFF-LEGO-PIPE-024-R0 at `main` `ae8bbc7`, content sha256 `e339867f…f308a`.
Number 025 **proposed**; James confirms. Reconciliation with ChatGPT's independent review follows.
