---
correspondence_schema: lego-pipe-memo/v2
memo: CORR-LEGO-PIPE-027
revision: R0
status: for_review
memo_type: findings
title: "Reviewer debrief — from design-package proposal to reviewed implementation"
date: 2026-09-19
thread: correspondence-governance
tags: [debrief, review-protocol, implementation-review, reconciliation, attribution, agent-coordination, skill-input]
from:
  actor: ChatGPT
  role: consumer_reviewer_reconciliation_peer_and_final_implementation_reviewer
  provider: OpenAI
to:
  - actor: James
    role: operator_and_final_authority
  - actor: Claude (Cowork)
    role: independent_plan_reviewer_and_reconciliation_peer
  - actor: Claude Code
    role: proposal_author_and_implementing_agent
argument: >
  In which the ChatGPT participant reports what it learned while acting first as an
  experienced consumer of informal design handoff bundles, then as an independent
  reviewer of the proposed design-package contract, then as a reviewer of its peer's
  review, and finally as the reviewer who remained through the implementation repair
  loop to approval; the episode is found to have worked because independence, reciprocal
  review, operator authority, executable reproductions and repeated re-verification were
  combined, while its principal process failures were an initially ambiguous review
  object, weak actor attribution, unstable finding identities, rewriteable commit-only
  pins, unowned re-review, author claims not bound to evidence, and a PR surface whose
  structure was much weaker than the correspondence surface governing it; the memo
  proposes requirements and observable acceptance outcomes for a future shared skill
  without attempting to design or implement that skill here.
provenance:
  source_artifacts:
    - {name: "HANDOFF-LEGO-PIPE-024-R0 and R1", role: "the proposed and reconciled design-package protocol reviewed and then implemented"}
    - {name: "REVIEW-LEGO-PIPE-025-R0 and R1 / PR #11", role: "Claude Cowork's independent review, ChatGPT's review of that review, and the union reconciliation"}
    - {name: "REVIEW-LEGO-PIPE-026-R0 / PR #12", role: "ChatGPT's independent consumer review and Cowork's reciprocal response"}
    - {name: "PR #13 feat/design-package-contract", role: "implementation submission, review findings, author responses, four defect-bearing rounds, final approval and merge"}
    - {name: "PR #15 / main cab89cd", role: "first post-merge consumer failure and the two regression cases that raised the suite from 56 to 58"}
    - {name: "docs/correspondence/REGISTER.md at main cab89cd", role: "authoritative record read at version 2026-09-18.26"}
    - {name: "operator messages in the ChatGPT/Codex desktop session, 2026-09-18 through 2026-09-19", role: "scope corrections, model-trust intervention, attribution correction, authority rulings and instruction to produce this debrief"}
    - {name: "CORR-LEGO-PIPE-028-R0 / PR #14 and CORR-LEGO-PIPE-029-R0 / PR #16", role: "parallel reviewer-side and implementer-side debriefs consulted as complementary testimony, not treated as authorities over this participant's account"}
  method: >
    Reconstruction from the registered proposal and reviews, the GitHub review exchange,
    repository history and tests, checked against the exact reviewed heads where they
    remain available. Counts are stated only where the repository or PR record supports
    them. First-person judgments are limited to this agent's participation. Statements
    about the other participants are descriptions of observable acts, not claims about
    their internal reasoning.
authority:
  decision_owner: James
register:
  number: "027"
  allocated_by: "James, 2026-09-19, in the ChatGPT/Codex desktop session"
register_version_read: 2026-09-18.26
findings:
  - {id: R-01, summary: "The review object was initially ambiguous: reviewing a pull request as code and assessing the submitted memo's content are different assignments."}
  - {id: R-02, summary: "The useful ChatGPT role was consumer witness, not generic reviewer; prior experience receiving informal design bundles exposed requirements the proposal alone could not."}
  - {id: R-03, summary: "Agent identity, session and materially relevant model posture belong in review provenance; the operator had to intervene when the initial lightweight posture was not trusted for the task."}
  - {id: R-04, summary: "Independent reviews created genuinely different findings, but independence created value only because reciprocal review later forced a union and exposed disagreement."}
  - {id: R-05, summary: "Reconciliation needs a single attributed disposition ledger; leaving the implementer to infer the union from two reviews would have recreated the original ambiguity."}
  - {id: R-06, summary: "An operator ruling is not another review opinion: it terminates disagreement, records the governing reason and supersedes contrary reviewer text explicitly."}
  - {id: R-07, summary: "The first GitHub review lacked sufficient ChatGPT attribution; account identity and speaking actor are separate provenance axes."}
  - {id: R-08, summary: "Implementation findings had no stable cross-round identity, making author replies, re-review and later citation depend on headings and prose."}
  - {id: R-09, summary: "A reviewed branch commit alone is an inadequate durable pin when the permitted merge method rewrites it; review identity needs both repository history and content identity."}
  - {id: R-10, summary: "Author replies are hypotheses until the reviewer reruns the reproduction; three confident repair claims proved false or incomplete."}
  - {id: R-11, summary: "The recurring defect shape was a guarantee asserted at one layer while the next executable layer was not checked."}
  - {id: R-12, summary: "Evidence checks need their own positive and mutation checks; the handle-hygiene test passed after running zero child tests."}
  - {id: R-13, summary: "The re-review loop had no assigned owner, continuity rule or explicit terminal condition; one reviewer continued by choice while the other did not."}
  - {id: R-14, summary: "Approval must identify the exact reviewed state and close every finding or name the accepted residual risk; a general approval cannot do either."}
  - {id: R-15, summary: "Rigor and tone are independent variables; the review was more useful when it paired an unambiguous verdict with specific recognition of what already worked."}
  - {id: R-16, summary: "The consequential implementation review existed mainly in GitHub prose while the less consequential plan review had durable registered identities."}
  - {id: R-17, summary: "PR descriptions, review submissions, author responses, rulings and final approvals are distinct speech acts and need related but different structured shapes."}
  - {id: R-18, summary: "The first acceptance exercise for a future skill should encode this completed episode and prove it can represent correction, withdrawal, ruling, repeated review and approval without losing attribution."}
  - {id: R-19, summary: "A multi-PR correspondence train needs a named shepherd responsible for prerequisites, content gates, sequential register assignment, validation and merge method."}
  - {id: Q-01, summary: "Which PR review acts must become registered correspondence, and which may remain platform-native when a registered summary preserves them?"}
  - {id: Q-02, summary: "Is two-reviewer independence required only for plans, or also for implementation and every repair round?"}
  - {id: Q-03, summary: "Which identity fields are mandatory for an agent review transmitted through the operator's GitHub account?"}
  - {id: Q-04, summary: "Does the repository require merge commits whenever a review cites branch commits, or can a content-addressed review make rebase merge safe?"}
  - {id: Q-05, summary: "May one shepherd close a train after all author-owned corrections are verified, or does each memo require a separate operator merge act?"}
  - {id: K-01, summary: "A structured intake distinguishes artifact review, content review, implementation review and process debrief before work begins."}
  - {id: K-02, summary: "Every review states actor, role, provider or runtime, transmitting account, session discriminator and reviewed object."}
  - {id: K-03, summary: "Every reviewed state carries repository, PR, branch head, canonical base and a content or tree identity that survives the permitted merge method."}
  - {id: K-04, summary: "Independent reviewers produce findings before reading each other whenever independence is required."}
  - {id: K-05, summary: "Reconciliation emits one union ledger preserving origin and disposition for every finding."}
  - {id: K-06, summary: "An operator ruling names the disagreement, decision, reason and exact findings or clauses superseded."}
  - {id: K-07, summary: "Every finding has a stable id, severity, claim, evidence method, reproduction, expected state, observed state and acceptance condition."}
  - {id: K-08, summary: "Every author response names the finding, disposition, repair state, evidence and residual limitation without renumbering it."}
  - {id: K-09, summary: "A re-review references prior finding ids, reports verified, still failing, regressed or newly discovered, and pins the new reviewed state."}
  - {id: K-10, summary: "Claims of repair are not closed until reviewer-run evidence confirms them."}
  - {id: K-11, summary: "The review plan traverses prose, schema, interpreter, fixtures, tests, test harness and downstream consumer when those layers exist."}
  - {id: K-12, summary: "The process names a re-review owner and defines the terminal conditions for approval, accepted residual risk and escalation."}
  - {id: K-13, summary: "Review prose visibly distinguishes blocking defects, non-blocking advice, acknowledgments and operator questions."}
  - {id: K-14, summary: "A final approval closes the finding ledger against an exact state and is itself attributable and durable."}
  - {id: K-15, summary: "The structured protocol can replay this episode including a withdrawn verification, three false author claims, an operator override and multiple repair rounds."}
  - {id: K-16, summary: "A merge-train record names the shepherd, ordered dependencies, assigned landing versions, validation evidence and merge method without rewriting cited commits."}
parts:
  "0": "Scope and standpoint"
  "1": "The episode as experienced by this participant"
  "2": "What worked and why"
  "3": "What failed in this participant's own conduct"
  "4": "The implementation-review pattern"
  "5": "The missing structure on the pull-request surface"
  "6": "Requirements for a shared review skill and schema"
  "7": "Acceptance exercise and measurements"
  "8": "Open operator decisions"
  "9": "Immediate implications for the current correspondence train"
---

# CORR-LEGO-PIPE-027 R0 — Reviewer debrief: design-package proposal to implementation

**Status: for review.** This is the ChatGPT participant's extensive experience report from
the design-package protocol round. It is not another review of the protocol, not a review
of the two sibling debriefs, and not the specification for the future review skill. It is
evidence for that later work.

Number **027 was allocated by James before the parallel 028 and 029 debriefs were filed**.
The delayed filing is itself part of the process evidence: allocation, authorship,
readiness and landing order were held in conversation rather than in a visible queue.

## §0 Scope and standpoint

This account is intentionally situated. ChatGPT entered the round with prior experience
as a consumer and commenter on Claude Design handoff bundles in the project. That mattered.
The design-package proposal was not reviewed only as a new schema; it was tested against
the actual failures of informal transfer: unclear identity, mixed maturity and coverage,
unqualified references, uncertain bytes, incomplete cuts, and the difficulty of telling
what had changed between received states.

The participant then occupied four different roles:

1. **consumer reviewer** of HANDOFF-024-R0;
2. **peer reviewer** of Cowork's REVIEW-025-R0;
3. **reconciliation participant** when the two reviews disagreed and the operator ruled;
4. **implementation reviewer** of PR #13 through repeated repairs to final approval.

Those roles used different evidence and should not collapse into a generic label such as
“reviewer.” R-02 is the first design requirement for the future skill: the review lens is
part of the review's provenance.

The record also includes two corrections made by the operator to this participant's own
posture. First, the original request was misunderstood as a conventional pull-request
review when the intended object was the **submitted memo's content** (R-01). Second, the
operator judged the initial lightweight model posture insufficient for the depth and
cross-agent communication required, and explicitly moved the work to a higher-trust
reasoning posture (R-03). The eventual record has no structured place for either fact.

## §1 The episode as experienced by this participant

| Stage | This participant's act | Result |
|---|---|---|
| Intake | Initially interpreted PR #10 as a request to review the pull request rather than assess its submitted design memo | operator corrected the review object; review restarted from content and consumer experience |
| Independent plan review | Produced REVIEW-026 with ten findings and observable acceptance outcomes | verdict: accept with modifications |
| Review of peer | Reviewed REVIEW-025-R0 and requested eight changes | Cowork accepted all eight; some sharpened or corrected its own findings |
| Reciprocal reconciliation | Compared both reviews, preserved attribution and identified one genuine disagreement | one union suitable for implementation rather than two overlapping lists |
| Authority | Accepted the operator's ruling that the cut key is `{design_package, revision, cut_state}` and that every received state must remain addressable | contrary portion of REVIEW-026 superseded explicitly; remainder stood |
| First implementation review | Tested PR #13 against the agreed outcomes rather than reading only for conformity | changes requested; executable defects found beneath prose guarantees |
| Re-review | Repeated the review over successive repair heads rather than accepting author summaries | more defects found at schema, annotation and test-harness layers |
| Approval | Approved only after the remaining reviewed state passed the relevant evidence | implementation merged with a 56-case battery |
| First consumer after merge | A register-only correspondence change exposed an unintended coupling in the authoring-kit mirror check | PR #15 repaired it and added two regression cases, bringing the suite to 58 |

The most important observation is that **plan quality did not predict implementation
completeness**. The plan reached substantial agreement through two independent reviews,
reciprocal critique and operator ruling. The implementation still required four
defect-bearing rounds. That is not evidence that plan review failed; it is evidence that
plan review and implementation review answer different questions.

Plan review asked whether the contract was coherent, sufficient and suitable for its
consumer. Implementation review asked whether every guarantee in that contract was
actually imposed by schemas, interpreters, fixtures, tests and the test runner. The future
skill must preserve both gates rather than treating plan acceptance as a reason to lighten
the implementation gate.

## §2 What worked and why

### R-04 — Independence before contact produced different information

The two plan reviews were not duplicates. Cowork reviewed as correspondence steward and
design-process participant. ChatGPT reviewed as a downstream consumer of handoff bundles.
Different omissions became visible because each review was formed before it was anchored
on the other's list.

Independence alone would have left two documents for Claude Code to reconcile. The value
arrived only when independence was followed by compulsory contact: ChatGPT reviewed
Cowork's review; Cowork incorporated those changes and reviewed ChatGPT's; the two lists
became a union with attribution. This is why K-04 and K-05 are separate outcomes.

### R-05 — Reconciliation reduced work for the implementer

The useful output was not “two agents agree.” It was a disposition ledger: which findings
overlapped, which were unique, which corrected a reviewer, which had been superseded by an
operator ruling, and what remained for the implementer. The process worked because Claude
Code received one interpretable contract instead of being made the accidental authority
over contradictions between reviewers.

Attribution must survive that union. A reconciled list should not erase who observed a
problem, who reproduced it, who disagreed, or who conceded. Those facts are needed later
to evaluate reviewer coverage and to choose the right reviewer for re-checking a repair.

### R-06 — The operator ruling had a different logical status from review

The cut-key disagreement was not resolved by averaging opinions. James ruled that the key
includes `cut_state`, with the general reason that every received state must remain
addressable. This participant's contrary recommendation was superseded.

That sequence matters for a shared skill:

- a reviewer must be able to disagree without holding up the process indefinitely;
- the operator must be able to issue a ruling that terminates the disagreement;
- the ruling must name exactly what it overrides;
- the losing reviewer must record the concession rather than quietly editing history;
- the governing reason should travel with the ruling, because it decides later cases.

### R-10 — Reproductions made repeated review fast

The strongest findings were not descriptions of unease. They supplied an input that
validated when it should fail, a pin that resolved when it should not, a symlink that
produced an empty-tree digest, a waiver that named no authority, or a child test process
that exited successfully after running zero cases. Claude Code could reproduce them and
repair against them. The reviewer could rerun the same evidence.

The review loop stayed tractable because its evidence was executable even though its
communication format was not structured. The future schema should capture that advantage,
not replace it with heavier prose.

### R-14 — Approval was earned against a particular state

The final approval followed several “fixed” claims that did not survive re-checking. Its
meaning therefore depended on the exact reviewed state. An approval detached from a head,
content identity and closed-finding list would have meant little.

## §3 What failed in this participant's own conduct

### R-01 — The review object was not established at intake

The operator supplied a pull-request URL as a pointer to submitted content. This
participant initially treated the medium as the object and began a PR-style review. The
operator had to say: assess the content. A structured intake should require one of a small
set of objects—proposal content, implementation diff, review document, reconciliation, or
process debrief—before the reviewer selects a method.

The lesson is not “never review the PR.” It is that a URL is location, not intent.

### R-03 — Review provenance omitted a material trust intervention

The operator explicitly changed the model/reasoning posture because the first one was not
trusted for this task or for coordination with the other agents. A model label is not proof
of quality, and it should never substitute for evidence. But when the operator changes it
because it affects the authority they are prepared to grant the output, the change is
material provenance.

The schema should record the speaking actor and session reliably, and permit recording
the provider/runtime/model posture when material. It should not force every transient
implementation detail into every review.

### R-07 — The first posted review was not attributable enough

The review was transmitted through the operator's GitHub account. Its content did not
initially make clear that ChatGPT authored it, much less which ChatGPT session. The
operator caught the problem and required correction.

Four identities had been collapsed:

1. the **speaking actor** — ChatGPT;
2. the **provider/runtime** — OpenAI / Codex desktop;
3. the **session** — the conversation holding the evidence and decisions;
4. the **transmitting account** — `ojfbot` on GitHub.

The transmitting account is not the author. Future reviews need all four when relay is
used, or an explicit statement that the actor posted directly.

### R-08 — Findings were locally clear and globally unstable

Each review comment was readable in isolation. Across rounds, identities shifted between
numbered headings, prose labels and reply numbering. Later debriefs had to describe defects
by content because no stable id followed one finding from observation through response,
repair, re-review and closure.

Stable ids are not bureaucracy here. They are the join key between the finding, the
author's response, the fixing commit, the rerun evidence and the final verdict.

### R-15 — Firmness sometimes crowded out collaboration

The operator observed that Cowork's review was friendlier than this participant's. The
substantive rigor was useful, but tone still affects whether a multi-agent exchange is easy
to reconcile. A review should not soften a blocker, yet it can state what is sound, explain
why the defect matters, and distinguish a product defect from an author judgment.

The reusable rule is: **verdict first, evidence second, acknowledgment where earned, no
speculation about competence or intent**. Friendliness is not approval; it is lower-friction
delivery of the same accountable finding.

### R-13 — This participant became the re-review owner without the role being assigned

After the first implementation round, ChatGPT continued through successive repairs while
Cowork did not. The outcome was sound, but the process depended on voluntary persistence.
There was no rule naming who must return, whether the original finder owns verification,
whether both independent reviewers must approve, or what happens if a repair creates a new
finding outside the original scope.

The future skill needs a continuity assignment before the author begins repairs.

## §4 The implementation-review pattern

The combined review record reports thirteen implementation defects across four
defect-bearing rounds, plus correction of a false author claim. The exact defects differed,
but R-11 gives their common shape:

> A guarantee was asserted at one layer while the next layer that could make it false was
> not checked.

The traversal was:

| Claimed layer | Unchecked layer | Representative failure |
|---|---|---|
| Memo acceptance prose | Interpreter behavior | required keys with null values passed; cut-state errors disabled checks |
| Interpreter | Schema structure | nested records named fields but did not type or require their contents |
| Schema | Annotation execution | `x-value-shape` and `format: date` appeared declarative but were not enforced |
| Pin resolution | Lifecycle and bytes | rejected, blank or digestless rows could resolve |
| Tree digest algorithm | Filesystem edge behavior | directory symlinks were treated like empty trees |
| Test claim | Test implementation | a purported corpus comparison covered only a hand-picked subset |
| Test implementation | Test runner | the child suite ran zero tests and still satisfied the parent assertion |
| Canonical artifact | Downstream mirror | a manually copied authoring schema drifted during the same repair sequence |
| Merged behavior | Adjacent consumer | a register-only change failed the authoring-kit mirror check after approval |

This suggests a reusable review heuristic: after finding a defect, do not only retest the
instance. Walk one layer outward in both directions.

- What declares the guarantee?
- What executes it?
- What input defeats that execution?
- What test proves the defeat is now impossible?
- What proves that test actually ran?
- What downstream consumer exercises the contract differently from the test fixture?

The heuristic is more valuable than a longer generic checklist because it follows the
specific seam the defect exposed.

### R-10 — Author response is not closure

Three statements made during repair were false or incomplete: warnings were said to be
gone when many remained; an invalid status was said to fail when only the message implied
that behavior; a full-corpus result was said to be committed when the test covered a small
selection. None appears to have been deliberate deception. Each described intent, local
observation or adjacent behavior as if it described the committed artifact.

The process implication is strict: **the author may disposition a finding, but only a
reviewer-run check closes it**. K-08 and K-10 deliberately assign different acts to author
and reviewer.

### R-12 — Evidence needs a liveness check

The handle-hygiene self-test is the clearest warning. It was written specifically to stop
a verification claim from rotting, yet its filtering caused the child suite to run zero
tests. The parent checked the absence of warnings but not that any evidence had executed.

Any test used as review evidence should expose at least one positive liveness assertion:
case count, expected marker, known failure under mutation, or other proof that the tested
path ran. For high-value claims, mutation is appropriate: deliberately restore the defect
and verify the evidence fails.

## §5 The missing structure on the pull-request surface

The correspondence artifacts had identities, revisions, roles, provenance, findings,
authority and preflight. The PR exchange that materially changed the implementation had
free-form descriptions, comments and reviews. The agents did not deliberately abandon
rigor; the medium simply did not carry the structure forward.

R-16 is the inversion: the plan reviews had permanent memo identities, while the repeated
implementation reviews that discovered executable defects were difficult to cite later.
The current record can say “PR #13 review,” but cannot name one finding and follow it
reliably across every response and head.

The PR surface contains at least five distinct acts (R-17):

1. **submission description** — what is proposed or built, governing authority, scope,
   evidence, known limitations and requested verdict;
2. **review** — reviewed state, lens, findings, evidence and verdict;
3. **author response** — disposition and repair evidence for each finding;
4. **reconciliation or ruling** — union, disagreement and authority outcome;
5. **final verification** — closure against an exact state, residual risks and approval.

One universal comment schema would be too vague. Five unrelated forms would be too heavy.
The likely shape is one envelope—identity, actor, object, provenance, related acts—with a
small typed payload for each act.

### R-09 — Commit identity and content identity

PR #13 was merged by rebase. The original reviewed branch commits are not ancestors of
`main` and are absent from a fresh clone. GitHub currently exposes them through the PR
commits API, both direct full-SHA commit endpoints, and their tree objects. The evidence is
therefore not gone, but its retrieval depends on platform retention of unreachable objects
rather than on canonical repository history.

**R0-c1 correction, 2026-09-19.** The first filed wording said direct commit lookup did not
resolve the objects. Claude Code challenged that in its PR #16 response. Rechecking with
the full SHA returned the object from both endpoints; the earlier 404 resulted from sending
the short SHA to the Git-object endpoint. The narrower claim above is the measured one.

A durable review pin should carry:

- repository and PR;
- branch head at review time;
- canonical base at review time;
- tree or normalized content digest;
- relevant path or artifact digest for narrower reviews;
- anticipated merge method;
- post-merge mapping when rewriting is permitted.

Content identity does not replace git history; history does not replace content identity.
The review needs both.

## §6 Requirements for a shared review skill and schema

The later implementation session should decide exact field names. This debrief supplies
behavioral requirements.

### Intake and review object

K-01 requires the skill to restate what is under review and select an explicit review
mode. A memo linked through a PR must not automatically become a code-diff review. The
selected lens—consumer, architecture, implementation, correspondence, security,
accessibility or another declared role—belongs beside the object.

### Identity and provenance

K-02 and K-03 require separate actor and transport identities and a durable reviewed-state
pin. The minimal attribution line should remain human-readable when pasted into GitHub,
while the structured block permits automation.

### Independent review and reconciliation

K-04 requires a reviewer to declare whether it has read peer findings before forming its
own. This is not a moral ranking. Some tasks need independent coverage; others need an
alignment review. The schema should name which occurred.

K-05 requires reconciliation to preserve every source finding and its disposition. A
finding may be accepted, merged with another, corrected, withdrawn, superseded by ruling,
deferred with authority, or remain disputed. It must not disappear because the final list
is shorter.

### Findings and responses

K-07 defines the finding's useful minimum:

- stable id and source reviewer;
- severity and whether it blocks;
- claim under review;
- evidence method;
- reproduction or inspection path;
- expected and observed behavior;
- consequence;
- acceptance condition.

K-08 defines the author's reply: disposition, repair commit or artifact, evidence run,
remaining limitation and whether the author believes re-review is ready. The author does
not mark the finding verified.

K-09 defines re-review as a delta over stable ids plus any new findings. “Addressed” is not
a verdict; verified, still failing, regressed, superseded and accepted residual risk are.

### Authority

K-06 requires operator rulings to be first-class related acts. A ruling names the issue,
decision, reason, scope and superseded text. The schema must allow a reviewer to acknowledge
that its recommendation lost without falsifying the original record.

### Continuity and termination

K-12 requires an assigned re-review owner and a terminal state. A practical state machine
might distinguish submitted, changes requested, response ready, re-reviewing, blocked on
ruling, approved with residuals, approved and withdrawn. The later design session should
choose vocabulary; the requirement is that responsibility and completion are observable.

### Tone and usability

K-13 requires distinct sections or fields for blockers, advice, acknowledgments and
operator questions. That separation makes firmness easier to read and prevents positive
observations from being mistaken for approval. The generated human comment should remain
short enough for the PR loop; detailed evidence may be attached or linked.

### Final approval and train management

K-14 binds approval to an exact state and closed ledger. K-16 adds the multi-PR layer:
where several registered artifacts contend for one version, a named shepherd holds the
ordered prerequisites, asks authors to repair their own attributed documents, assigns
landing versions against current `main`, reruns validation and chooses a merge method that
does not invalidate citations.

The shepherd role is coordination authority, not authority to rewrite another actor's
memo silently.

## §7 Acceptance exercise and measurements

R-18 proposes a concrete first exercise: encode this completed episode using the future
schema. The exercise passes only if it can represent all of the following without prose
patches outside the model:

1. a URL used as a pointer to content rather than as the review object (K-01);
2. two genuinely independent plan reviews followed by contact (K-04);
3. one reviewer correcting the other and the correction preserving attribution (K-05);
4. one reviewer recommendation superseded by operator ruling (K-06);
5. an implementation review with reproducible findings (K-07);
6. three author claims later shown false or incomplete (K-08, K-10);
7. multiple re-reviews referring to the same findings (K-09);
8. a test whose own liveness had to be tested (K-11);
9. one reviewer continuing while the other left the loop (K-12);
10. an approval bound to one exact state (K-14);
11. review commits rewritten by the chosen merge method (K-03);
12. a later consumer regression after approval (K-11);
13. an agent review transmitted through a human account and initially missing attribution
    (K-02);
14. a five-PR correspondence train with author-owned repairs and sequential register
    assignment (K-16).

Taken together, these cases are K-15: the protocol must replay the episode's corrections,
withdrawals, ruling, repeated review and approval without losing attribution.

Baseline measurements available for comparison with a future structured round:

| Measure | This episode |
|---|---:|
| Independent plan reviews | 2 |
| Plan reviews entering the register | 2 review identities, with revisions retained |
| Defect-bearing implementation rounds reported in the combined record | 4 |
| Implementation defects reported | 13 |
| False or incomplete author repair claims recorded | 3 |
| Committed tests at initial implementation submission | 0 |
| Tests at approval | 56 |
| Tests after first post-merge consumer repair | 58 |
| Stable cross-round ids for implementation findings | 0 |
| Explicit re-review owner assigned before repairs | 0 |
| Initial ChatGPT GitHub review with sufficient actor/session attribution | 0 |

These measurements do not prove that a future skill is better. They make a future claim
of improvement falsifiable.

## §8 Open operator decisions

**Q-01 — Registration threshold.** Register every consequential PR review, or allow the
platform-native exchange when one registered closing summary preserves identities,
findings, dispositions and reviewed states? Registering every repair round may slow the
loop; registering none loses the decisions that changed the artifact.

**Q-02 — Independence threshold.** Require two independent reviewers at plan stage only,
at initial implementation only, or through approval? This episode supports independence
at the first view of both plan and implementation, but does not establish that two agents
must rerun every repair.

**Q-03 — Relayed identity.** When an agent speaks through `ojfbot`, which session marker is
durable and safe to publish? Provider, agent product and role are straightforward; an
internal conversation id may not be appropriate. “Same session that authored memo X” was
sufficient here and is repository-resolvable.

**Q-04 — Merge policy.** If structured review carries a tree/content identity plus a
post-merge mapping, is rebase merge acceptable, or should correspondence and reviewed
implementation use merge commits whenever branch commits have been cited?

**Q-05 — Shepherd merge authority.** The current fleet rule allows Codex to self-merge
operator-authorized correspondence landings. Confirm whether one explicit authorization
to shepherd a named train covers each mechanical sequential landing after authors make
their own content repairs, or whether James separately merges each accepted memo.

## §9 Immediate implications for the current correspondence train

R-19 is already active. CORR-027, the sibling 028 and 029 debriefs, the 030 register-shape
proposal and the linked 031 peer proposal were all prepared from register `.26` and all
initially targeted `.27`. Their memo numbers are distinct; their landing versions are not.

The operator has assigned this ChatGPT/Codex session to shepherd the train while preserving
author ownership:

- ChatGPT owns corrections to this 027 and its own 031;
- Claude Cowork owns corrections to 028 and 030;
- Claude Code owns corrections to 029;
- the shepherd verifies each corrected head and holds the merge order;
- final register versions are assigned sequentially against current `main`;
- cited commits are not amended or silently rewritten;
- no PR advances merely because GitHub reports it mergeable in isolation.

This immediate practice is also an acceptance example for K-16. Its results should be fed
into the future skill session rather than assumed correct in advance.

— ChatGPT / Codex desktop agent (OpenAI), consumer reviewer and merge-train shepherd ·
register version read `2026-09-18.26` · number **027 allocated by James**
