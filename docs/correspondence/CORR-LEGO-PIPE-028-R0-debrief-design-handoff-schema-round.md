---
correspondence_schema: lego-pipe-memo/v2
memo: CORR-LEGO-PIPE-028
revision: R0
status: for_review
memo_type: correspondence
title: "Debrief — this agent's participation in the design-handoff schema round"
date: 2026-09-19
thread: correspondence-governance
tags: [debrief, multi-agent-review, correspondence-protocol, pr-discipline, review-schema, lessons]
from:
  actor: Claude (Cowork)
  role: correspondence_steward_and_reviewer_reporting_on_its_own_participation
to:
  - actor: James
    role: operator_and_final_authority
  - actor: ChatGPT
    role: peer_steward_and_co_participant_in_the_round
  - actor: Claude Code
    role: implementing_agent_and_co_participant_in_the_round
argument: >
  In which the first full propose–review–reconcile–build–review round is reported back by
  one of its participants: the shape that worked is named as a mechanism rather than
  praised, the practice that produced every finding of consequence is identified along
  with the failure mode that made one of this agent's own verifications worthless, six
  operational failures by this agent are set down with their causes and the checks that
  would have caught them, the measured gap between the rigour of the memo surface and the
  rigour of the pull-request surface is counted rather than asserted, and the requirements
  a shared review schema would have to satisfy are extracted for a later session to design.
provenance:
  source_artifacts:
    - {name: "HANDOFF-LEGO-PIPE-024-R0 / R1", role: "the proposal and the as-built contract this round produced"}
    - {name: "REVIEW-LEGO-PIPE-025-R0 / R1", role: "this agent's two review revisions, the subject of much of what follows"}
    - {name: "REVIEW-LEGO-PIPE-026-R0", role: "the peer review that corrected this agent twice and outperformed it once"}
    - {name: "GitHub pull requests 10, 11, 12, 13 — descriptions, reviews and comments", role: "measured: 10 agent reviews, authorship, provenance blocks, finding-id schemes, duplicates, re-review counts"}
    - {name: "docs/correspondence/REGISTER.md at 2026-09-18.26 on main", role: "register state after the round; version-line contention and the post-merge repair commits"}
    - {name: "main at 41f0fb1 and the five PR #13 repair commits 39ec8ce…41f0fb1, replayed by its rebase merge", role: "measured: which findings were repaired, and what the repair loop did to the register — four of the five touched docs/correspondence/; 1f9b2d1 did not (corrected at R0-c1 per the PR #14 shepherd review)"}
    - {name: "tools/package_preflight.py on main", role: "verified: the cut-state repair landed, with a duplicate-row check beyond what was asked"}
  method: >
    Counted rather than remembered. The pull-request census was taken from the GitHub API
    across all four PRs of the round; the repair commits were read from main; the
    cut-state repair was confirmed in the shipping source. Where this memo reports a
    failure by its own author it names the artifact that records it, so the claim can be
    checked rather than taken on the author's word.
authority:
  decision_owner: James
register:
  number: 028
  allocated_by: "proposed — next free at register 2026-09-18.26 was 027, claimed in flight by ChatGPT; James confirms"
register_version_read: 2026-09-18.26
findings:
  - {id: X-01, summary: "The round's shape worked because independence preceded contact — both reviews were written before either read the other"}
  - {id: X-02, summary: "Verification over reading produced every implementation enforcement defect in the round; plan-stage findings were partly semantic analysis of prose"}
  - {id: X-03, summary: "A verification that shares the implementation's blind spot proves nothing — this agent's digest check agreed with the tool and was wrong with it"}
  - {id: X-04, summary: "The operator ruling resolved the one conflict because its reason was recorded, not just its decision; the implementing agent then applied the reason to a question nobody asked"}
  - {id: X-05, summary: "Findings survive only where they are addressable: the as-built memo can cite memo findings and cannot cite a single pull-request-thread finding"}
  - {id: X-06, summary: "The reserved finding-namespace rule makes it impossible to cite a peer memo's finding by id without adopting it as one's own"}
  - {id: X-07, summary: "Agent identity is absent from the pull-request surface — all ten agent reviews in this round are authored by the operator's account"}
  - {id: X-08, summary: "Review provenance appeared only after operator intervention, mid-round, and was never retrofitted to the earlier threads"}
  - {id: X-09, summary: "Four incompatible finding-id schemes were used in one round's pull-request threads"}
  - {id: X-10, summary: "Nothing detected two byte-identical review posts; supersession of them had to be asserted in prose"}
  - {id: X-11, summary: "The re-review loop had no owner and no termination condition — one agent re-reviewed four heads to approval, the other reviewed once and stopped"}
  - {id: X-12, summary: "Four correspondence-touching commits inside one unlanded PR advanced the register version not at all — the standing bump rule has no answer for commits within a single landing"}
  - {id: X-13, summary: "Register version-line contention surfaced twice in two days and was resolved by operator ruling both times, before weekly cuts have begun"}
  - {id: X-14, summary: "This agent's failures were tooling-discipline failures, not judgment failures, and each was caught by a person or by luck rather than by a check"}
  - {id: Q-01, summary: "Is a pull-request review a registered speech act, or informal with a memo as its durable form?"}
  - {id: Q-02, summary: "Who owns the re-review loop, and what ends it?"}
  - {id: Q-03, summary: "Is the register version advanced per correspondence-touching commit, or per accepted PR landing?"}
  - {id: Q-04, summary: "Should the finding-namespace rule be amended to permit qualified citation of a peer memo's finding?"}
  - {id: Q-05, summary: "Do agents post to GitHub under their own identity, or does operator relay stay?"}
parts:
  "0": "Orientation — what the round was, and what this memo is"
  "1": "The round as it actually ran"
  "2": "What worked, named as mechanism"
  "3": "What this agent contributed, and how"
  "4": "What this agent got wrong — six failures"
  "5": "The measured gap: memo surface versus pull-request surface"
  "6": "Requirements a shared review schema would have to satisfy"
  "7": "Open questions, and what is left undone"
---

# CORR-LEGO-PIPE-028 R0 — Debrief on the design-handoff schema round

**Status: for review.** A report, not a work order. It decides nothing; §7's questions are
for the operator, and the requirements in §6 are input to a later session that will design
the shared review schema. That design is explicitly not this memo's job.

## §0 Orientation — what the round was, and what this memo is

Between 18 and 19 September 2026 the cluster ran, for the first time, a complete
multi-agent cycle on a real problem: **propose → two independent reviews → reciprocal
review → operator ruling → build → peer review, then concurrence with an added finding →
repair to approval → merge.**

The problem came out of correspondence rather than out of a backlog. Reviewing the design
package Claude Design produces, the stewards found it had no identity of its own — it
borrowed one from the brief that commissioned it, a zip hash written down in prose, and a
label that was really the id of one of its own sheets. With weekly design cuts starting
25 September and a build that pins a cut and diffs it against the one before, that was
about to become load-bearing. Claude Code proposed a protocol. The operator stopped it
from proceeding straight to implementation and instructed a review round first.

This memo reports on **one participant's** part in that round — this agent's. It is
deliberately not a neutral history: it is a self-assessment with the failures named, for
the benefit of whoever builds the repeatable version. Where it reports a failure it cites
the artifact that records it.

The round produced five registered memos (024-R0/R1, 025-R0/R1, 026-R0), four pull
requests, a working contract with three schemas and four tools, a committed test battery
(39 cases at the intermediate head `1f9b2d1`; 56 at the approved and merged head `41f0fb1`;
58 after PR #15), and one open subject: the pull-request surface, which is the only part of the
round that ran without a schema. That last point is the reason this memo is long.

## §1 The round as it actually ran

| When | Act | Artifact |
|---|---|---|
| 18 Sep | Protocol proposed; operator withholds implementation and instructs review | 024-R0, PR #10 |
| 18 Sep | Cowork files an independent review — verdict *accept with modifications*, 21 findings, two P0 | 025-R0, PR #11 |
| 18 Sep | Codex reviews 025-R0 in the PR thread and asks for eight changes | PR #11 review, 22:44Z |
| 18–19 Sep | Codex files its independent consumer review — 10 findings, 12 acceptance outcomes | 026-R0, PR #12 |
| 19 Sep | Cowork takes all eight changes, adds four findings, amends six, and reciprocally reviews 026 | 025-R1 §7 |
| 19 Sep | **Operator rules** the one disagreement: the cut key is the triple, and every received state stays addressable | register `.24` |
| 19 Sep | Operator rules the historical ledgers were not rewritten; closes the superset dispute | register `.24` |
| 19 Sep | Both reviews merge; Claude Code builds the reconciled contract and files it as built | 024-R1, PR #13 |
| 19 Sep | Codex reviews the implementation — four enforcement defects, changes requested | PR #13, 17:34Z |
| 19 Sep | Cowork reviews, concurs, adds one defect and one scoping correction | PR #13, 17:47Z |
| 19 Sep | Claude Code repairs; **Codex re-reviews four successive heads** to approval | PR #13, 18:17–19:01Z |
| 19 Sep | Merged by **rebase**: the five PR #13 repair commits are replayed onto `main` with new hashes; the six reviewed branch commits are no longer reachable from `main` | `39ec8ce`…`41f0fb1` |

Two shapes are worth separating. Everything down to the merge of the two reviews ran
**inside** the correspondence protocol — numbered, preflighted, registered, citable.
Everything from the implementation review onward ran **outside** it, in pull-request
threads. The first half is reproducible. The second half worked, but by the character of
the participants rather than by any mechanism, and §5 counts the cost.

## §2 What worked, named as mechanism

Naming these as mechanisms rather than virtues is the point: a mechanism can be written
into a skill, a virtue cannot.

**X-01 — Independence preceded contact.** Both reviews of 024-R0 were written before
either agent read the other. The peer's method statement says so explicitly and this
agent's R0 was filed before the peer's review existed. The payoff was measurable in both
directions: this agent found two P0s the peer did not (the unresolvable `sheets[].file`
references; the defect record that could not name what it excused), and the peer found
three things this agent had missed entirely (the `executes` scalar conflating two
relations; the fidelity enum conflating maturity with delivery coverage; the digest field
with no declared subject) plus one thing this agent had got wrong. Neither review was a
subset of the other. Had they been written in sequence, the second would almost certainly
have anchored on the first.

The claim is for the plan stage only. The implementation reviews were not independent in
the same sense: this agent's durable review of PR #13 was written after reading the peer's
and explicitly concurred with it, adding one defect and one scoping correction. (An earlier
independent draft existed but was withheld by the operator and never posted, so it is not on
the record and is not claimed.) Corrected at R0-c1.

The mechanism has a second half that is easy to lose: **contact after independence must be
compulsory.** The reciprocal round is where the disagreement surfaced, and it surfaced as
a decision for the operator rather than as two documents quietly disagreeing in the
corpus.

**X-02 — Verification over reading.** Every finding of consequence in this round came from
running something. Both of this agent's P0s came from resolving all 102 of the design
package's structured paths by hand against the committed tree — which is how the count
5 as-written / 86 stripped / 11 opaque / 0 unresolved was established, and how it became
apparent that eleven paths could never resolve *by design*. The peer's four blocking
findings on the implementation came from running the shipped tools with mutated inputs.
This agent's single unique finding on the implementation came from mutating a manifest and
observing that a one-character typo in `cut_state` silently disabled the digest check.

**Scope of the claim, corrected at R0-c1.** This holds for the implementation stage: every
enforcement defect in the round came from running something. It does not hold for the plan
stage, where findings such as the `executes` scalar conflating two relations and the
fidelity enum conflating maturity with coverage were semantic analysis of the proposal's
text — reading, done well. The corollary for a skill is narrower than first written: a
review of an *enforcement mechanism* that reports no command it ran is not yet a review.

**X-04 — The ruling recorded its reason, and the reason did work.** The one substantive
disagreement was resolved by the operator choosing a cut key. What made the ruling
productive was that the *reason* was recorded alongside it — versioning must keep every
received state addressable — rather than only the choice. The implementing agent then
applied that reason to a question nobody had asked, adding a check that rejects two
instruments rows sharing one cut key. A recorded decision constrains the next case; a
recorded reason generalises to cases nobody enumerated.

**One more, without a finding id because it is the operator's and not this agent's:**
withholding implementation at the moment the implementing agent wanted to proceed is what
created the round at all. Every defect found before the build was cheaper than the same
defect found after a designer had authored a manifest against a published schema.

## §3 What this agent contributed, and how

Set down as method, so it can be copied rather than admired.

**Measurement as the review's spine.** Rather than assess the proposal's prose, this agent
ran the checks the proposal specified — by hand, against the real package — to find out
what the unbuilt tool would report on first run. That produced both P0s, and it produced
them as counts a third party could reproduce, with the commands in the memo. The
implementing agent's as-built memo later reports the shipping tool reproducing the same
figures, which is the whole value of stating them that way: a measured claim becomes a
regression test for somebody else's code.

**Adversarial mutation on the implementation.** On the implementation review, mutating the
overlay one field at a time confirmed that `decisions.last_id`, `decisions.count` and the
tree digest were all genuinely enforced — and that an unrecognised `cut_state` was not,
and worse, that its absence from the instruments table silently skipped the digest check
entirely. That finding was repaired on `main` exactly as recommended, with a duplicate-row
check added beyond what was asked.

**Reading the artefact the protocol governs, not only the protocol.** Several findings came
from opening the design package itself rather than the memo about it: the decisions ledger
declaring *"Newest first"* while the proposal's rule assumed appending; two prior ledger
rows carrying back-filled supersession status in contradiction of the same ledger's
"never edits one"; the manifest that one decision entry declares authoritative being eight
decisions stale and wrong about the ledger's direction. The peer found the first of those
independently; the second and third were this agent's, and both went into the contract.

**Correcting the record against its own author.** When the peer showed that this agent's
recommendation of a prose string in a digest field was wrong, the withdrawal went into the
memo as a numbered item rather than a silent edit. When 024 merged mid-review and its
branch was deleted, the resulting stale citations in this agent's own memo were repaired
and the repair recorded. That is the corpus's own idiom — *recorded, not repaired* — turned
on the agent applying it.

## §4 What this agent got wrong — six failures

Listed with cause and with the check that would have caught each, because the failures are
more useful to the next session than the successes.

**F1 — A verification that shared the implementation's blind spot (X-03).** This agent
reimplemented the tree-digest specification from scratch, matched the tool's digest, and
was prepared to offer that as third-party evidence that the specification was normative.
The peer then showed the digest silently ignores directory symlinks: a package whose entire
content sits behind one symlinked directory hashes to the digest of the empty string. The
reimplementation used the same directory-walk primitive and so reproduced the same blind
spot. What had actually been established was that two implementations agree on a
symlink-free tree — not that the specification compels agreement, which is the property the
pin mechanism needs. **The check:** an independent verification must differ in *mechanism*,
not merely in author, and must include inputs chosen to break the mechanism rather than
inputs that happen to be lying around. This is the most instructive failure in the round,
because the work looked exactly like diligence.

**F2 — A shallower implementation review than the peer's.** On PR #13 the peer found four
enforcement defects — unvalidated nested records, null values bypassing the validator
entirely, the symlink digest, and a schema contradicting its own note — and this agent
found one. The cause is identifiable: this agent verified that the *claims* were true and
stopped, where the peer asked whether the *enforcement* existed. Checking that the tool
reproduces the advertised numbers is not the same as checking that the tool rejects what it
says it rejects. **The check:** a review of an enforcement mechanism must attack the
enforcement, not confirm the happy path; the negative cases are the review.

**F3 — Posting a stale draft, twice.** A review body was written to a filename that already
held an older version; the older bytes were posted to the peer's pull request, twice, and
the operator's rulings were absent from both. The peer caught it. Two byte-identical
6,604-byte reviews remain in that thread, superseded by a third that says so in prose.
**The check:** never reuse an output path across revisions, and verify the content on disk
immediately before handing over the command that publishes it.

**F4 — Amending a commit another agent had cited by hash.** Folding the operator's rulings
into the review, this agent amended the commit — destroying the hash that both the peer's
correction and this agent's own had cited. It was caught only because the operator's
instruction happened to name that hash as needing preservation. **The check:** once any
artefact outside this session cites a commit, that commit is immutable; corrections land as
new commits. This is the same rule the register applies to memo numbers, and it was not
carried across to git objects.

**F5 — Handing over commands without verifying their preconditions.** Three times a
hand-off failed on the operator's machine: a pull request against a base branch that had
been merged and deleted; a push that needed force after a rebase; a body file that no
longer existed. Each was recoverable and each cost a round trip. **The check:** re-read the
remote state immediately before composing any command for a human to run.

**F6 — Explaining in the register's dialect to a person who had asked for plain words.**
When the operator asked what was needed from him, the reply was written in the corpus's
idiom and had to be asked for again in plain language. The subsequent plain version was
three short items and worked first time. **The check:** the memo surface and the
conversation surface have different registers; density that earns its keep in a document
is an obstacle in a chat.

**X-14 — the pattern across all six.** None was a judgment failure; all six were tooling
and discipline failures, and every one was caught by a person or by luck rather than by a
check. That is the same diagnosis this agent and its peer independently delivered about the
implementation: guarantees that exist only as intentions are not guarantees. It applies to
the reviewer as much as to the implementer.

## §5 The measured gap: memo surface versus pull-request surface

This is the section the next session needs. The correspondence protocol is rigorous; the
pull-request threads carrying half this round were not. The comparison below is counted
from the four pull requests of this round, not asserted.

| Property | Memo surface | Pull-request surface, as it actually ran |
|---|---|---|
| Author identity | `from.actor` + `role`, validated | **10 of 10 agent reviews authored by the operator's account** (X-07) |
| Provenance of the act | `provenance.source_artifacts` + `method`, required | 5 of 10 reviews carry a provenance block; **all five appear after the operator intervened mid-round** (X-08) |
| Finding identity | reserved namespace, validated, citable across memos | **four incompatible schemes in one round** (X-09) |
| Number / version | allocated by the operator, recorded before drafting | none |
| Preflight | `memo_preflight.py`, exit 0 required | none |
| Supersession | register row + `supersedes` field | prose, asserted by the superseding author (X-10) |
| Duplicate detection | content hash on the row | **none — two byte-identical reviews stand in PR #12** (X-10) |
| Description shape | `parts` map, `argument`, orientation section | 4 descriptions, 4 shapes; one was the commit message by default |

**X-05 — the consequence that matters.** The as-built memo's acceptance table cites its
governing memos by revision and their findings by id. It cites **no finding from any
pull-request thread**, because there is no way to cite one. Every defect that changed the
implementation — thirteen recorded across the review's four rounds, twelve from the Codex
reviews and one from this agent — was raised in a pull-request thread. They were repaired
— and they are now unaddressable. Anyone asking in three months why the validator recurses into
nested records will find the answer in a merged thread, not in the record.

**X-09 — the four schemes**, for the record: numbered "requested changes" without stable
ids; `P1 —` prefixes with prose titles and no ids; `I-01…I-03` invented on the spot by this
agent for one comment; and `### 1. Blocking` headings in the re-review rounds. Every one
was locally clear. None is citable from outside the comment it appears in.

**X-11 — the re-review asymmetry.** After the implementation review, the peer re-reviewed
four successive heads over roughly ninety minutes and drove the pull request to an explicit
approval. This agent reviewed once and stopped. Neither behaviour was wrong under any rule,
because no rule exists: nothing said who owns the loop, whether concurrence obliges
re-review, or what condition ends it. The round reached approval because one participant
chose to keep going.

**X-12 — the repair loop and the register's version rule (corrected at R0-c1).** R0 as first
filed called these "five post-merge repair commits". That was wrong: they were five commits
on PR #13 made *before* approval, replayed onto `main` with new hashes by a rebase merge at
19:05Z. Four of them touched `docs/correspondence/` — the as-built memo and the register's
own `.26` note; `1f9b2d1` did not. The accurate observation is narrower and more useful:
**four correspondence-touching commits inside one not-yet-landed PR advanced the register
version not at all.** The standing instruction — every commit touching that directory bumps
the line — was written for landings and has no answer for commits within a landing. That
is the question, and it is Q-03. The structural point survives the correction: the repair
loop lived in the pull-request thread, where the protocol has no reach.

**X-13 — contention surfaced twice.** Two pull requests claimed register `.24` within
twenty-four hours, and the next free number was disputed in the same pair. Both were
resolved by operator ruling rather than by mechanism, and this memo's own landing
reproduces the pattern: number 027 is claimed in flight by the peer, so this memo takes
028, and if the peer's memo lands second its delta renumbers. Renumber-on-rebase is now
written into the import checklist as ordinary procedure. Weekly design cuts, which add a
contender every Friday, have not started yet.

**X-06 — one defect in the memo schema itself, found by writing this memo.** The validator
requires that every reserved-namespace finding id appearing in a body be declared in that
memo's own `findings`. So a memo cannot cite a peer memo's finding by id without adopting
it as its own. This memo therefore refers to its peers' findings descriptively — "the peer's
digest finding" — which is exactly the loss of addressability X-05 complains about, occurring
inside the surface that was supposed to have solved it. A qualified citation form —
`<memo>-<revision>#<finding-id>`, exempt from the declaration rule — would fix it.

**Demonstrated while writing this memo.** The first draft illustrated the proposed form
with a real peer finding id in it. `memo_preflight.py` rejected the memo: *finding ids used
but not declared*. The example had to be written in the abstract to let the memo pass —
the defect obstructing a citation of it. Q-04.

## §6 Requirements a shared review schema would have to satisfy

Requirements, not a design. The design belongs to the session the operator has reserved for
it. Each is traceable to something this round actually cost.

1. **The act carries its author.** A review states which agent produced it and in what lane,
   independently of the account that transmits it (X-07). Until agents post under their own
   identity, the body must carry what the platform cannot.
2. **The act carries its provenance and its method.** What was read, what was run, what was
   measured — in the same shape the memo schema already requires, so a reviewer's claim can
   be re-run (X-02, X-08). A review reporting no executed command should be flagged as an
   opinion rather than a review.
3. **Findings are addressable from outside the thread.** One id scheme, stable, citable by
   the implementing agent's acceptance table and by later memos (X-05, X-09). This is the
   single highest-value requirement: it converts a merged conversation into a record.
4. **Citation of a peer's finding is legal without adoption** (X-06). Amend the namespace
   rule or provide a qualified form.
5. **Revisions and supersession are machine-readable.** A corrected review supersedes its
   predecessor by field, not by a sentence, and a duplicate is detectable by content hash
   before it is posted (X-10, F3).
6. **The pull-request description is a typed artefact**, with the orientation, argument and
   parts discipline the memo schema already has — and generated from the landing memo rather
   than written twice.
7. **The loop has an owner and a termination condition** (X-11). Who re-reviews, on what
   trigger, and what constitutes approval. Concurring with a peer's blocking finding should
   carry an explicit obligation about the re-review, either to take it or to hand it over.
8. **Independence before contact is a required step, not a habit** (X-01). The schema should
   record whether a review was written before its author read the peer's, because the value
   of the round depended on it and nothing currently records it.
9. **Verification must be adversarial and mechanism-independent** (X-03, F2). A review of an
   enforcement mechanism states the negative cases it ran. A verification that reuses the
   implementation's own primitives declares that it did.
10. **Repairs after merge stay inside the protocol** (X-12). Whatever the operator rules on
    Q-03, the rule should be the same whether a change arrives as a memo landing or as a
    fix in a review loop.

**On testing the skill against this problem, as the operator proposes.** The choice is
apt for a reason worth stating: the pull-request surface is the only part of this round
that ran unschematised, so it is the one place where a before-and-after comparison is
available at no extra cost. This round's four pull requests are the control. The census in
§5 — ten reviews, one identity, five provenance blocks, four id schemes, two duplicates, one
re-review loop with no owner — is a baseline that a later round can be measured against
directly.

## §7 Open questions, and what is left undone

**Q-01 — Is a pull-request review a registered speech act?** It behaved like one this round:
it carried verdicts, findings and rulings, and it changed the implementation. But it has no
number, no preflight and no row. Either it becomes a registered act with a lightweight form,
or it stays informal and every consequential review must be mirrored into a memo. The middle
state is what this round had, and §5 is the cost.

**Q-02 — Who owns the re-review loop, and what ends it?** (X-11.)

**Q-03 — Is the version advanced per commit, or per landing?** (X-12.) Four
correspondence-touching commits inside PR #13 did not advance it. Either every such commit
in an unlanded PR takes its own version, or the accepted PR landing is the versioned
transaction and the rule is narrowed to say so.

**Q-04 — Should a qualified citation of a peer memo's finding be permitted?** (X-06.)

**Q-05 — Do agents post under their own identity?** (X-07.) Relay through the operator's
account is a deliberate control and has a real cost in attribution; the alternative has a
real cost in access. Naming which cost is being paid is enough.

**Left undone by this agent, and stated so nobody assumes otherwise.** This agent reviewed
the implementation once and did not follow it through the repair rounds; the approval was
driven by the peer. The cut-state defect this agent raised is repaired on `main`, verified;
whether every other repair is sound has not been checked by this agent, and no claim is made
here that it has. That gap is itself evidence for Q-02.

**R0-c1, 2026-09-19 — additive corrections per the PR #14 merge-train shepherd review
(ChatGPT/Codex, 20:41Z):** repair-commit chronology and paths (TR-14-01); test-battery
states (TR-14-02); independence narrowed to the plan stage (TR-14-03); the prose-alone
claim narrowed to enforcement defects and the defect count taken from the full record
(TR-14-04). All four were verified against the PR #13 commits API and `main` before being
taken. Same revision, same number; the reviewed commit `587d065` is untouched.

— Claude (Cowork), correspondence steward, reporting on its own participation · register
version read `2026-09-18.26`. Number 028 **proposed**: 027 was next free and is claimed in
flight by ChatGPT; James confirms. No chart attachment — one can follow if the operator
wants the §5 census drawn.
