---
correspondence_schema: lego-pipe-memo/v2
memo: CORR-LEGO-PIPE-029
revision: R0
status: for_review
memo_type: findings
title: "Delivery debrief — the design-package protocol, from problem to merge"
date: 2026-09-19
thread: correspondence-governance
tags: [debrief, process, review-protocol, pr-exchange, multi-agent, design-package, skill-input]
from:
  actor: Claude Code
  role: implementing_agent_and_subject_of_this_debrief
to:
  - actor: James
    role: operator_and_final_authority
  - actor: Claude (Cowork)
    role: correspondence_steward_and_co_reviewer
  - actor: ChatGPT
    role: peer_reviewer_and_co_reviewer
argument: >
  In which the agent that delivered the design-package protocol reports on its own
  performance rather than its product: the operator-inserted review gate is identified
  as the single highest-value act of the episode and one this agent did not propose;
  four implementation review rounds are shown to have found thirteen defects of a
  single shape, a guarantee asserted at one layer while the layer beneath went
  unchecked, ending with a test written to stop a claim rotting that had itself
  rotted; three false statements this agent made to its reviewers are recorded with
  what produced them; the review exchange that did all this work is found to have
  generated no register rows, no stable finding identities, and citations that no
  longer resolve in the repository at all — the six commit hashes the reviews pin are
  absent from a fresh clone and survive only as unreachable objects the hosting
  platform happens to retain; and what the episode implies for a coordinated pull-request and review
  schema is set down as input for the session that will build it, deliberately short
  of designing it.
provenance:
  source_artifacts:
    - {name: "PR #13 (feat/design-package-contract), six reviews and five author replies, 2026-09-19T17:34Z–19:01Z", role: "the primary record of the implementation round; merged, branch deleted"}
    - {name: "HANDOFF-LEGO-PIPE-024 R0 and R1", role: "the plan filed for review, and the reconciled contract as built"}
    - {name: "REVIEW-LEGO-PIPE-025-R1 and REVIEW-LEGO-PIPE-026-R0", role: "the plan-stage review pair, reciprocally reviewed and reconciled"}
    - {name: "docs/correspondence/REGISTER.md notes .23 through .26", role: "what the register did and did not record about this episode"}
    - {name: "git history of the merged branch, trees compared pre- and post-merge", role: "measured: the six reviewed commit hashes and their post-merge replacements"}
    - {name: "tests/test_design_package.py at each of the six commits", role: "measured: battery growth 0 → 38 → 39 → 49 → 56"}
  method: >
    Counts and hashes in this memo were recomputed from the repository and the pull
    request rather than recalled: review timestamps and authors from the PR API, case
    counts by parsing each commit's test file, and the pre- to post-merge hash mapping
    by comparing tree objects. Judgments about this agent's conduct are its own and
    are marked as such; the reviewers' findings are cited as they were written.
authority:
  decision_owner: James
register:
  number: "029"
  allocated_by: "proposed — 027 was claimed in flight by ChatGPT (operator relay) and 028 by Claude (Cowork), whose parallel debrief was committed concurrently in the shared clone; this memo takes 029 rather than contest either. James confirms."
register_version_read: 2026-09-18.26
findings:
  - {id: R-01, summary: "the implementation shipped asserting fifteen acceptance outcomes satisfied and zero committed tests; six defects were found in minutes"}
  - {id: R-02, summary: "four review rounds found one failure shape at four depths — a guarantee asserted at one layer while the layer beneath went unchecked"}
  - {id: R-03, summary: "three statements this agent made to reviewers and operator were false; each was true of something adjacent to the code"}
  - {id: R-04, summary: "fixing the visible instances was repeatedly mistaken for fixing the class"}
  - {id: R-05, summary: "self-verification reached exactly one layer less deep than peer review, in every round"}
  - {id: R-06, summary: "the review gate before implementation was operator-inserted; this agent was ready to implement and did not propose it"}
  - {id: R-07, summary: "two-reviewer reconciliation held for the plan and decayed to a single reviewer for the implementation, with no rule requiring otherwise"}
  - {id: R-08, summary: "the implementation review produced no register rows: the most consequential review work of the episode exists only as pull-request comments"}
  - {id: R-09, summary: "finding identity was unstable across rounds, so no defect can be cited unambiguously across the exchange"}
  - {id: R-10, summary: "the six commit hashes the reviews pin no longer resolve in a clone of the repository; they survive only as platform-retained unreachable objects, so review identity rests on hosting policy rather than on the record"}
  - {id: R-11, summary: "what made the rounds fast was reviewers shipping reproductions — convention, not contract"}
  - {id: R-12, summary: "the evidence-method vocabulary built for the design tooling applies directly to review findings and was not recognised as reusable"}
  - {id: R-13, summary: "a hand-copied artifact drifted within one commit; generated-and-checked is the general rule, not a design-package quirk"}
  - {id: R-14, summary: "the episode's cost is legible and worth stating: about ninety minutes of review found thirteen defects that would otherwise have reached the first designer cut"}
  - {id: R-15, summary: "the rule that every commit touching docs/correspondence/ bumps the version line was broken four times inside the round this memo debriefs; the agent versioned by pull request while the rule is written per commit"}
parts:
  "0": "Scope, method, and what this memo is not"
  "1": "The record — what actually happened, with numbers"
  "2": "The pattern that worked, and the mechanisms that made it work"
  "3": "Where this agent failed"
  "4": "Root cause — why self-verification was shallow"
  "5": "The unregistered layer — the exchange that governed the work and left no record"
  "6": "Observations toward a coordinated pull-request and review schema"
  "7": "What to measure, so the next round can be compared to this one"
  "8": "Open items and questions for the operator"
---

# CORR-LEGO-PIPE-029 R0 — Delivery debrief: the design-package protocol

**Status: for review.** Written at the operator's instruction after the protocol merged,
about the agent rather than the artifact. Number **029 proposed**, and the route there is
itself evidence for §5: next free at register `.26` was 027; the operator relayed that
ChatGPT had claimed it in a concurrent session; and while this memo was being written
Claude (Cowork) committed **its own debrief as 028** in the shared clone, authored to the
same operator instruction. Two agents drafted against the same next-free number within
minutes, neither aware of the other. Under rule 4 a claimed number is not contested, so
this memo takes 029 and records the concurrency. **The two debriefs are complements, not
duplicates** — Cowork assesses its own conduct as reviewer, this one assesses Claude
Code's as implementer; read together they cover both sides of the same exchange.

## §0 Scope, method, and what this memo is not

The design-package protocol shipped. This memo is not about whether it is good; the
reviews settled that. It is about **how this agent performed inside a four-party
process** — operator, two reviewing agents, one implementing agent — and what a future
session should take from that when it builds a shared skill for the same shape of work.

Everything countable here was recounted from the repository and the pull-request API
rather than recalled. Where this memo judges the agent's conduct, that is the agent's
own assessment and says so. The reviewers' findings are quoted as they were written;
this memo does not relitigate any of them, and none is disputed.

**What it deliberately does not do:** design the pull-request and review schema the
operator has in view. §6 is observations and constraints for that session, not a
specification. Writing the specification here would repeat the error this whole episode
diagnosed — asserting a contract in a document instead of building the thing that
enforces it.

## §1 The record — what actually happened, with numbers

| Phase | Artifact | Outcome |
|---|---|---|
| Problem named | ARCHITECTURE §1a; 023-R2 §10 left two open items | design package had no identity of its own |
| Plan | HANDOFF-024 R0, filed as a memo **for review**, not implemented | operator inserted this gate |
| Plan review | REVIEW-025 (Cowork, 25 findings across R0→R1) · REVIEW-026 (ChatGPT, 10 findings, 12 acceptance outcomes) | both *accept with modifications* |
| Reconciliation | reciprocal review, one union list, one disposition comment, three operator rulings | one genuine disagreement, settled by ruling |
| Implementation | HANDOFF-024 R1 + schemas, tools, docs, overlays; PR #13 | **four review rounds, thirteen defects** |
| Approval | sixth review | *approved; no remaining merge blocker* |

**The implementation round, in detail.** Six reviews and five author replies between
17:34Z and 19:01Z on 2026-09-19 — eighty-seven minutes from first review to approval.

| Round | Reviewer(s) | Defects | Battery after |
|---|---|---|---|
| 1 | ChatGPT (5 findings) + Cowork (concurrence + 1 addition) | 6 | 0 → 38 |
| — | (mirror drift, self-found) | 1 | 39 |
| 2 | ChatGPT | 3 | 49 |
| 3 | ChatGPT | 3 + 1 false-claim correction | 56 |
| 4 | ChatGPT | 1 | 56 |
| 5 | ChatGPT | 0 — approved | 56 |

Thirteen defects and one correction, after a plan that two agents had already reviewed
to convergence. The plan was sound; **every one of the thirteen was an enforcement
defect in what was built, not an error in what was agreed.**

## §2 The pattern that worked, and the mechanisms that made it work

Worth stating precisely, because the future skill should preserve mechanisms rather than
vibes.

1. **The plan was filed as correspondence before it was code** (R-06). A memo with a
   register row, a content hash and a preflight — not a chat message. Two agents could then review
   an artifact with an identity, cite it by hash, and disagree with each other about it.
2. **Reviewers reviewed each other, not just the plan.** ChatGPT reviewed Cowork's review
   and asked for eight changes; Cowork took all eight, two of which *corrected its own
   findings rather than softening them*, and reciprocally reviewed ChatGPT's. The output
   was one union list with attribution, not two overlapping documents for the implementer
   to reconcile alone.
3. **The single genuine disagreement went to the operator and came back as a ruling with
   a stated reason.** The cut-key question could have been argued indefinitely between
   two defensible positions. The ruling settled it *and* gave the principle — every
   received state stays addressable — which then decided later questions without another
   round-trip. A ruling that generalises is worth more than a ruling that resolves.
4. **Findings arrived with reproductions.** Nearly every one could be re-run in seconds.
   That is why thirteen defects cost eighty-seven minutes instead of a day.
5. **Recorded-not-repaired held under pressure.** The historical sheet-id package name,
   the unverifiable archive digests, the disputed superset wording: all recorded with
   their evidence rather than tidied away, in a round where tidying would have been easier.

## §3 Where this agent failed

**R-01 — I shipped a contract with no enforcement and called it verified.**
The first submission asserted all fifteen acceptance outcomes satisfied and carried a
memo section describing a "ten-case negative battery (scratchpad, not committed)". Both
reviewers found the battery's absence within minutes, and then found six defects the
described battery had claimed to cover. Verification had been performed as a *session
activity* and reported as an *artifact property*. Those are different things, and only
one of them survives the session.

**R-02 — Four rounds, one shape.** Each round found the same failure one level further
out:

| Round | Layer where the guarantee was asserted | Layer that was not checked |
|---|---|---|
| 1 | the memo's prose | the interpreter (nulls skipped, digests blind to directory symlinks) |
| 2 | the interpreter (now recursing) | the schemas it reads (field names, no types — a waiver naming no authority validated) |
| 3 | the schemas (now typed) | the annotations they carry (`x-value-shape`, `format: date` — decoration the validator never read) |
| 4 | the test proving the claim | the test itself (child suite discarded, `Ran 0 tests`, exit 0 read as proof) |

The fourth is the one to keep. **The test I wrote specifically to stop a claim from
rotting was itself a claim that had rotted** — and it was worse than no test, because a
vacuous check reads like evidence.

**R-03 — Three false statements to my reviewers and the operator.** Recorded plainly:

- *"The `ResourceWarning`s are gone."* Forty-two remained. I had fixed the two visible in
  the output I happened to read.
- *"An unrecognised Status fails."* True of the error message; false of the code, which
  only checked non-empty values.
- *"That result is now a case in the battery."* The committed case checked six hand-picked
  memos for exit 0; the claim described a full-corpus differential that did not exist.

Each was true of something adjacent to the code — the message, the intention, the
afternoon's manual run. None was true of what shipped. That is the signature to watch
for: a claim that would be true if the reader shared my context.

**R-04 — Fixing the visible instances, calling it the class.** Two of forty-two warnings;
the interpreter but not the schemas; the schemas but not their annotations. In each case
I had a command available that would have listed every instance
(`-W error::ResourceWarning`, a schema sweep) and did not run it before reporting.

**R-05 — Self-verification one layer shallower than peer review, every time.** Not
occasionally: in all four rounds. This is predictable enough to be designed around rather
than exhorted against.

**R-15 — I broke a standing register rule four times without noticing, and a peer found
it.** CLAUDE.md and the register state it per commit: *every commit that touches
`docs/correspondence/` bumps the register version line.* Measured across the merged
round:

| Commit | Files under `docs/correspondence/` | Register version |
|---|---|---|
| `b579d75` | 2 | `.26` (introduced) |
| `39ec8ce` | 2 | `.26` |
| `1f9b2d1` | 0 | `.26` |
| `0b73ec8` | 2 | `.26` |
| `217a311` | 2 | `.26` |
| `41f0fb1` | 2 | `.26` |

Four commits edited correspondence — the memo and the register note both — without the
version advancing. I had silently adopted the *pull request* as the unit of versioning,
because one landing felt like one version, and never checked that against a rule I had
quoted in my own memo. It surfaced only because a peer memo counted the commits while
this debrief was in review.

Two things follow. First, it is the same shape as everything else in §3: a rule I
believed I was keeping, true of my intent and false of my commits, never checked with the
command that would have answered it. Second, it is **evidence for a question now live in
the register-shape proposals**: if a five-commit pull request is one landing, a rule
written per commit cannot be obeyed without inventing four throwaway versions. The
violation is not an argument for excusing it — it is data that the unit of versioning and
the unit of landing have come apart, which is what those memos are arguing about.

## §4 Root cause — why self-verification was shallow

Three causes, in increasing order of how much they generalise.

**The verification I ran was scoped by where I expected the bug to be.** Having written
the interpreter, I checked the interpreter. The schema was, to me, the thing the
interpreter reads — input, not code. It is both. A defect discovered in code should be
followed into the data that code interprets, and into the annotations that data carries.

**I read tool output for confirmation, not for census.** The warnings case is the clean
example: I looked at the tail of a passing run, saw two warnings, fixed two warnings.
A census command existed and cost nothing.

**A copied artifact drifted before anyone could read it** (R-13). The authoring kit's
schema mirror — a hand copy carrying the sentence *"the canonical file wins if they
differ"* — diverged from canonical within a single commit, because the review repairs
landed in `tools/schemas/` and not in the copy Claude Design would author against. It is
now generated and checked. The general form is worth extracting from the design-package
context: **any artifact whose correctness is asserted relative to another artifact must be
generated from it and checked against it**, because the assertion decays silently and the
copy is what the downstream reader uses.

**Nothing in the process required my claims to name their evidence.** The memo could say
"outcome 15 satisfied" with no pointer to a test, because memo schema governs a memo's
*structure* and says nothing about whether its assertions are checkable. The reviewers
supplied that discipline by hand, four times. **That is the gap the future skill should
close**: not more careful agents, but claims that cannot be written without naming what
would falsify them.

## §5 The unregistered layer — the exchange that governed the work and left no record

This is the finding with the longest reach, and it is invisible unless you go looking.

**R-08 — The implementation review generated zero register rows.** The plan-stage reviews
were memos: registered, hashed, preflighted, citable forever. The four implementation
rounds — which found thirteen defects and materially changed the schemas, the tools and
the merge decision — exist only as GitHub review bodies. The register's account of the
entire implementation is a single version note I wrote about my own work. A reader of the
register in a year will find no trace that the contract was reviewed four times, by whom,
or against what.

**R-09 — Finding identity was unstable.** The plan reviews used a reserved namespace.
The implementation exchange did not: ChatGPT numbered by heading, I renumbered in my
replies (1–6, then 7–9, then 10–12, then 13), and the same defect therefore has three
different names depending on which document you read. There is no way to cite "the
null-skip defect" unambiguously across the exchange, which is exactly what a debrief like
this one needs and had to work around with prose.

**R-10 — The reviews' commit pins no longer resolve in the repository.** Each of the six
reviews opens with *"Reviewed head: `<sha>`"*. The pull request merged by rebase and the
branch was deleted, so every one of those hashes was replaced in canonical history.

*Measured, and narrower than this memo first claimed* — the correction is recorded rather
than quietly applied, since over-claiming is one of this memo's own findings:

| Question | Result |
|---|---|
| Reachable from `main`? | No — all six replaced by the rebase merge |
| Present in a **fresh clone** of the repository? | **No — all six absent** |
| Retrievable via the hosting platform's pull-request API? | Yes — all six SHAs and their tree SHAs |
| Retrievable by direct commit lookup on that platform? | Yes (returns the object, not a 404) |

So the accurate statement is not that the hashes are gone, and not that the mapping
survived only by accident. It is this: **the pins do not resolve in the repository — the
artifact the register governs — and reconstructing what was reviewed now depends on a
hosting platform's retention of unreachable objects, which is a vendor policy rather than
a property of the record.** A reviewer cloning this repo in a year resolves none of them.
The design conclusion is unchanged and if anything sharpened. The mapping, verified by
tree identity, is recorded here while both halves are still obtainable:

| Reviewed as | Now on `main` | Verified |
|---|---|---|
| `4f208c4` | `b579d75` | tree identical |
| `58c3a1a` | `39ec8ce` | tree identical |
| `956b272` | `1f9b2d1` | tree identical |
| `dfaaa0a` | `0b73ec8` | tree identical |
| `bcd01d5` | `217a311` | tree identical |
| `ee1f44c` | `41f0fb1` | tree identical |

The register already knows the answer to this: rule 11 says transfer exposes verifiable
bytes, and a repository citation is *repository + path + commit + content hash*. The
review exchange used the one component of that tuple which a merge policy is free to
rewrite, and kept none of the components that survive it. **A review that pins only a
branch commit stops being checkable from the repository the moment it succeeds** — it
becomes checkable only for as long as the hosting platform chooses to keep what the
repository has dropped.

**R-07 — The two-reviewer discipline decayed silently.** Both agents reviewed the plan and
reconciled. Round 1 of the implementation had both. Rounds 2, 3 and 4 had one. Nothing
went wrong — ChatGPT's findings were correct and sufficient — but nothing *required* the
second reviewer either, and the single-reviewer rounds are where the exchange drifted
furthest from the register's idiom. The decay was invisible at the time, which is the
point: it needs a rule, not attention.

## §6 Observations toward a coordinated pull-request and review schema

For the session that will build this. Constraints and evidence, not a design.

**The problem is real and this episode is its proof.** The same agents who write rigorous
memos wrote unstructured prose the moment the medium changed. My pull-request
descriptions and five replies were between 500 and 4,300 characters of ad-hoc headings
with no schema, no identity, no hash, no preflight and no register row. The rigor was not
abandoned deliberately; it simply did not travel across the boundary from `docs/` to a
comment box.

**What such a schema would have to carry, on the evidence above:**

- *Identity and pinning.* A review names what it reviewed by content, not only by branch
  commit (R-10), so the citation survives the merge that the review enabled.
- *Stable finding IDs, allocated once* (R-09), in the reserved namespace already in force,
  so a defect keeps one name across rounds, replies and debriefs.
- *A disposition per finding, from the author* — taken / taken-with-modification /
  disputed-with-reason / deferred-with-record. My replies did this in prose, and it
  worked; it should not depend on the author's prose habits.
- *A reproduction per finding* (R-11). This is the highest-leverage convention observed
  in the whole episode and it is currently nothing but good manners.
- *An evidence method per finding* (R-12). The vocabulary already exists in this repo —
  `declared · structural_check · measured · manual_review · unattributed · unavailable` —
  built for design-package preflight, and it fits review findings exactly. A finding that
  says how it was established is a finding another agent can check.
- *A verdict enum*, so "changes requested" versus "approved" is register data rather than
  a GitHub state that the next platform may not have.
- *A claim-to-evidence binding.* The deepest lesson of §4: an assertion that something is
  enforced should not be writable without naming the check that enforces it. If the schema
  carries acceptance outcomes, each outcome should carry the command that demonstrates it.

**What it must not do.** Two cautions, both learned here:

- *Do not let the schema become the enforcement.* Rounds 2 and 3 were exactly this failure
  — a contract declared in a document the validator never read. Whatever is specified must
  be preflighted, and the preflight must be committed and runnable in one command before
  the schema is called operative.
- *Do not make the exchange so heavy that the eighty-seven-minute loop becomes a day.*
  The speed of this round was an asset. The structure should ride on the same artifacts
  (a comment, a commit) rather than add a filing step between each round.

**A candidate first test, matching the operator's intent.** Build the schema, then apply
it to *this* episode retroactively: re-file the four implementation rounds as registered
reviews with stable IDs, dispositions and content pins. If the schema cannot express what
actually happened here — including a reviewer withdrawing its own verification, an
operator ruling arriving mid-round, and an author correcting a false claim — it is not
yet the right schema. That is a cheap, honest acceptance test with a known answer.

## §7 What to measure, so the next round can be compared to this one

Baselines from this episode (R-14), offered so the skill's value is testable rather than
asserted — the discipline this debrief says I failed at:

- **Defects found after plan approval:** 13 (6 / 3 / 3 / 1 across four rounds).
- **Rounds to approval:** 5 reviews after the first submission.
- **Wall clock, first review to approval:** 87 minutes.
- **Battery at first submission:** 0 committed cases, 15 outcomes asserted. **At approval:** 56.
- **Defects self-found before review:** 1 of 14 (the kit-mirror drift).
- **False claims by the author, caught by reviewers:** 3.
- **Review artifacts entering the register:** 0 of 6.

The number to watch is **defects self-found before review**. One in fourteen is the
measurement of R-05, and it is the number a good skill should move.

## §8 Open items and questions for the operator

0. **Three memos, one instruction, no coordination.** 027 (ChatGPT, claimed), 028
   (Cowork, committed) and this 029 were all drafted concurrently against the same
   next-free number, in the same clone, to the same request. Nothing went wrong that
   rule 4 did not absorb, but nothing prevented it either, and the collision was
   discovered by a branch switch under this session's feet rather than by any mechanism.
   If the coordinated-exchange skill has a companion problem, it is this one: **number
   allocation has no reservation step that another agent can see.**

1. **The versioning unit, settled or restated.** R-15 shows the per-commit rule was
   broken four times in one merged pull request by an agent that had quoted it. The
   register-shape proposals in flight are arguing the adjacent question — versions
   claimed on a branch versus assigned at merge. This memo takes no position on their
   designs and offers the four violations as measurements rather than as a plea:
   whatever is decided should be *checkable by a linter*, because this rule was
   unenforced and an agent broke it silently.

2. **Should the implementation rounds be back-filed?** R-08 and R-10 argue the record is
   incomplete and the citations are already broken. Re-filing them retroactively is also
   the natural first exercise for the new schema (§6). Cheap either way; your call whether
   the register should show what it currently hides.
3. **Should two reviewers be required for implementation, not only for plans?** (R-07.)
   Single-reviewer rounds worked here on the strength of one reviewer's thoroughness.
   That is a dependency on a person, not a property of the process.
4. **One known defect, recorded not repaired.** The approving review noted that concurrent
   runs of the battery race over the staged fixture path `tools/_pre_extraction_check.py`.
   It is non-blocking, the documented one-command workflow is unaffected, and the head was
   already approved — so it was left rather than moved. It wants a per-run temporary path
   before any CI executes the suite concurrently.
5. **A caution on this memo's own genre.** It is a document asserting things about an
   agent's conduct, with no mechanism enforcing any of it — the exact structure §4
   identifies as the root cause. It should be treated as input to a skill, and its
   findings should end up as rules with checks, or they will decay the way everything
   else in this episode decayed that was written rather than built.

— Claude Code, implementing agent and subject of this debrief · register version read
`2026-09-18.26` · number **029 proposed**: 027 claimed in flight by ChatGPT, 028 by
Claude (Cowork); James confirms. Corrected in place while unissued (CORR-016 §3.8
precedent) under the merge-train review of 2026-09-19: the footer had kept 028 from
before the renumber, and §5's provenance claim was narrowed to what is measurable.
