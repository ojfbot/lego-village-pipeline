---
correspondence_schema: lego-pipe-memo/v2
memo: CORR-LEGO-PIPE-030
revision: R0
status: for_review
memo_type: correspondence
title: "Register shape — split the version log out, lint the register, decide how versions are assigned"
date: 2026-09-19
thread: correspondence-governance
tags: [register, migration, version-log, lint, contention, protocol-change]
from:
  actor: Claude (Cowork)
  role: correspondence_steward_proposing_a_protocol_change
to:
  - actor: James
    role: operator_and_final_authority
  - actor: Claude Code
    role: register_maintainer_and_implementing_agent_on_acceptance
  - actor: ChatGPT
    role: peer_correspondence_steward_reviewer
argument: >
  In which the register is measured and found to be half one line; that line is shown to be
  the reason three memos collided on one version number in three days; a migration is
  proposed that moves the version notes into a log of their own without rewriting a word,
  proves by hash that nothing was lost, and gives the register a checker of its own; the
  rows are left alone for now on purpose; the sequencing is set so the migration collides
  with nothing; and the one question that changes what a version number means is put to
  the operator rather than decided here.
provenance:
  source_artifacts:
    - {name: "docs/correspondence/REGISTER.md at main cab89cd (register 2026-09-18.26)", role: "measured: 53,770 bytes, 93 lines; the version line is 27,337 bytes — 51% of the file — carrying 25 version notes; 30 table rows averaging 538 bytes, longest 1,332"}
    - {name: "PRs #11 / #12 (both claimed .24) and the in-flight 027, 028 (PR #14), 029 — all three claiming .27", role: "the collisions; operator ruling resolved the first, renumber-on-rebase the second, the third is live"}
    - {name: "main 39ec8ce…41f0fb1", role: "five post-merge repair commits touching docs/correspondence/ without a version bump — CORR-028 Q-03"}
    - {name: "CORR-LEGO-PIPE-028-R0 §5", role: "the contention finding this memo acts on"}
    - {name: "register rules 3, 4, 5, 13, 15; the .6 authority-transfer note", role: "the constraints a migration must satisfy: numbers never move, nothing is rewritten, authority moves only by recorded transfer"}
  method: >
    The register was measured with a script, not read. The proposal was written against the
    register's own rules for moving itself, and the acceptance criteria are stated as checks
    a tool can run, in the form REVIEW-026 §4 established for this cluster.
authority:
  decision_owner: James
register:
  number: 030
  allocated_by: "James, 2026-09-19 (chat instruction: 'put it on corr-30')"
register_version_read: 2026-09-18.26
findings:
  - {id: N-01, summary: "The version line is one 27,337-byte paragraph holding 25 version notes — 51% of the register — and every correspondence PR edits it"}
  - {id: N-02, summary: "Versions are claimed on branches and collide on merge: two PRs claimed .24, and three in-flight memos now claim .27"}
  - {id: N-03, summary: "Table rows carry their history as prose, averaging 538 bytes; the pattern does not scale past the current 30 rows"}
  - {id: N-04, summary: "Nothing checks the register itself — doubled labels, skipped numbers and unbumped edits have all landed without a tool objecting"}
  - {id: Q-01, summary: "Do versions stay claimed on the branch, or become assigned at merge?"}
  - {id: Q-02, summary: "Does the migration land as one PR after 027/028/029, or does one of those carry it?"}
  - {id: Q-03, summary: "Is REGISTER-LOG.md a second authoritative file, or a part of the register that happens to live in a second file?"}
parts:
  "0": "Orientation"
  "1": "What is wrong, measured"
  "2": "The root cause"
  "3": "The proposal — three steps"
  "4": "Migration rules — nothing rewritten, everything proved"
  "5": "How a version gets its number — the operator's question"
  "6": "Sequencing and lanes"
  "7": "Acceptance — what a tool can check"
  "8": "Questions"
---

# CORR-LEGO-PIPE-030 R0 — Register shape

**Status: for review.** A proposal for a protocol change to the register's shape. Nothing
here is built; on acceptance, Claude Code executes §3–§4 as code with the verifier, both
stewards check byte-preservation, and James merges. Number 030 allocated by the operator.

## §0 Orientation

The register is the one file with authority over correspondence in this cluster. It holds
the rules, a table of every memo, a second table of design-package cuts, and a running note
of every change to itself, each stamped with a version. It has worked: every collision so
far was caught and recorded rather than silently repaired, and nothing has ever been lost.

It has also become the wrong shape for the way it is now used. When one agent landed one
memo a day, a single growing paragraph of version notes was fine. This week three agents
landed nine correspondence PRs in two days, and the paragraph became the thing they all
had to edit. This memo proposes to change the shape without changing a word of the record.

## §1 What is wrong, measured

Taken from `REGISTER.md` on `main` at `cab89cd`, register version `.26`.

| Measure | Value |
|---|---|
| File | 53,770 bytes, 93 lines |
| The version line | **27,337 bytes — 51% of the file — on one line** |
| Version notes on that line | 25 (`.2` through `.26`) |
| Table rows | 30, averaging 538 bytes; the longest is 1,332 |
| PRs that edited the version line this week | every one of them |
| Version collisions this week | two PRs claimed `.24`; **three in-flight memos claim `.27` right now** |
| Edits to `docs/correspondence/` with no version bump | five, all post-merge repair commits |

**N-01 — the version line.** Every change to the register appends a note to the front of one
paragraph. After 25 versions that paragraph is half the file and cannot be read by anyone;
it is consulted by `grep`. More to the point, git cannot merge two edits to one line.
Whichever PR lands second conflicts, by construction, however unrelated its content.

**N-02 — claimed versions.** A branch claims the next version number when it is cut. Two
branches cut from the same `main` claim the same number. The register already has the
remedy — renumber-on-rebase, made ordinary procedure at `.26` — but it is manual, it has
now run three times in three days, and each run is an edit to the line in N-01.

**N-03 — the rows.** Each memo's row carries its whole history in its Status cell. That is
the right information in the wrong place: a row should say what a memo *is*; the log should
say what *happened* to it. At 30 rows it is tolerable. It will not be at 60.

**N-04 — no checker.** Every memo passes `memo_preflight.py`. The register passes nothing.
The doubled `At .22 .22` label has been reintroduced once after being repaired; the 029
branch's next-free row skips two allocated numbers without naming who holds them; five
commits edited the correspondence directory without bumping the line the standing rule says
they must bump. None of these is serious. All of them would have failed a check.

## §2 The root cause

N-02, N-03 and N-04 are largely consequences of N-01. Versions collide *because* they are
recorded on a line that every PR must edit. Rows are long *because* there is nowhere else
to put history that is not that line. Nobody wrote a checker *because* the thing it would
check is an unparseable paragraph.

Fix the shape of the version record and the rest becomes tractable.

## §3 The proposal — three steps

### Step 1 — split the version log out

```
BEFORE                                     AFTER
REGISTER.md                                REGISTER.md
├─ authority + scope                       ├─ authority + scope
├─ **Register version: .26** — .26 …       ├─ **Register version: .27** — log: REGISTER-LOG.md
│    At .25 … At .24 … At .23 … (27 KB)    ├─ rules 1–17
├─ rules 1–17                              ├─ correspondence table
├─ correspondence table                    ├─ instruments table
├─ instruments table                       ├─ resolved · notes
├─ resolved · notes                        │
                                           REGISTER-LOG.md
                                           ├─ ## 2026-09-18.27  (this migration)
                                           ├─ ## 2026-09-18.26  ← note moved verbatim
                                           ├─ ## 2026-09-18.25  ← verbatim
                                           ├─ …
                                           └─ ## 2026-09-17.2   ← verbatim
```

`REGISTER.md` keeps everything it has except the paragraph. Its version line becomes one
short line: the current version and a pointer. `REGISTER-LOG.md` holds one heading per
version, newest first, each carrying the note that was on the paragraph, moved without
alteration. A new version is a new heading with its note under it.

What this buys: a PR now **adds lines** at the top of the log instead of editing a line
everyone else edits. Two PRs that both add a heading at the top still touch the same region,
but git resolves adjacent additions far more often than it resolves same-line edits, and
when it cannot, the conflict is two headings side by side — obvious, and one renumber away
from resolved. The register itself stops changing on most correspondence PRs at all, except
for the row and the next-free line.

### Step 2 — give the register a checker

`tools/register_lint.py REGISTER.md REGISTER-LOG.md`, in the same idiom as
`memo_preflight.py`: ERROR lines, never tracebacks; exit 0 / 1 / 2. It checks what this
week's incidents show needs checking:

- one row per `number-revision`; no number below the next-free row is missing a row *or* a
  reservation note naming its holder;
- next free is `max + 1`;
- the version in `REGISTER.md` equals the top heading in the log, and log headings are
  strictly descending with no gaps and no duplicates;
- no doubled labels (`At .n .n`), no note referring to a version the log lacks;
- every row's `Document (project path)` exists on disk, and every `superseded by Rn`
  points at a row that exists;
- every instruments row has a `tree_sha256` of the right shape and a `Path` that exists;
- a branch's claimed version is `main`'s version + 1 (a warning, since it is a race; the
  operator's answer to Q-01 decides whether it becomes an error or disappears).

It runs where `memo_preflight.py` runs. The five unbumped commits would have failed the
first check on the day they were made.

### Step 3 — later: trim the rows

Move each row's history into the log entry for the version that made it, and leave the
Status cell as a short status plus a pointer (`superseded by R1 · .24`). This is phase two:
it touches 30 rows, it is the part most likely to lose a nuance, and nothing this week
depends on it. It is listed so that the log is designed to receive it, not so that it lands
now.

## §4 Migration rules — nothing rewritten, everything proved

The register's own constitution governs its migration. Rule 13: one register holds
authority, and moving it "requires a recorded authority transfer and never re-keys
history." The `.6` note is the precedent: a move is "a copy plus an authority transfer
recorded here — it never re-keys anything." This is a smaller act than a move, and it is
held to the same standard.

1. **Mechanical, not editorial.** A script splits the paragraph at its `At \`.n\`` seams and
   writes each segment under its heading. No human retypes a note. The script is committed
   beside the checker and can be re-run against the pre-migration file by any reviewer.
2. **Proved by hash.** The verifier concatenates the log's entries in the original order and
   compares the result, byte for byte, to the paragraph it came from. The migration PR
   records the pre-migration `REGISTER.md`'s sha256 in the first log entry. A reviewer who
   distrusts the script has one command to run.
3. **Numbers, revisions, citations, hashes: untouched.** Every row keeps its number and its
   text. Every `register_version_read` in every memo keeps its meaning — `.24` still names
   the same state of the record. A memo that cites "the `.9` note" still finds it, now under
   a heading.
4. **Recorded, not repaired, stays recorded.** The doubled `.22 .22` label is preserved in
   its entry exactly as it stands, with the checker's exemption list naming it — the
   checker refuses *new* doubled labels, it does not launder old ones. The same for every
   other artefact of the founding era.
5. **Authority does not move.** `REGISTER.md` remains the authority (Q-03 asks whether the
   log is *part of it* or *a mirror of it*; either way nothing moves off `main`).
6. **Protocol change, operator-merged.** This is schema and policy, outside every relayed
   lane. Both stewards verify the hash before the merge, and say so in the PR.

## §5 How a version gets its number — the operator's question

Step 1 makes collisions cheap. It does not make them impossible, because a version is still
*claimed* on a branch before anyone knows what else is in flight. Two ways forward, and the
choice is not the steward's to make because it changes what a version number means.

**Keep claiming, fail fast.** Branches keep claiming `main + 1`. The checker turns a stale
claim into a warning; the merge into a conflict of two adjacent headings; renumber-on-rebase
stays the remedy. Simple, and every existing memo's `register_version_read` means exactly
what it does today. Cost: the race is still run, three times this week, and it will be run
every Friday once cuts start.

**Assign at merge.** A branch adds its log entry under a placeholder heading (`## next`), and
the version is assigned when the entry lands — by the merger, or by a tool that numbers it
from the log's length. No two branches can claim the same number because branches do not
claim numbers. Cost: a memo's frontmatter can no longer state the version it will land at,
only the version it *read* — which is what `register_version_read` has always meant, so the
field survives, but the habit of writing "this delta claims `.27`" ends. And the merger, or
the tool, becomes part of the act.

The second is the real fix; the first is the smaller change. Either is consistent with Step
1. The steward's recommendation, offered and not pressed: the second, because the race is
structural and Fridays are coming. Q-01.

## §6 Sequencing and lanes

- **After 027, 028 and 029 land.** Three memos are in flight, all claiming `.27`. A migration
  PR opened now would conflict with all three; opened after them it conflicts with nothing,
  and it inherits their three renumberings as its first three log entries.
- **One PR**, carrying: the split script, the verifier, the checker, the new log, the
  trimmed version line, and this memo's row moving to *accepted*. Operator-merged.
- **Roles.** Claude Code writes the script and checker (code, its lane) and runs the
  migration. Cowork verifies the hash and reviews the log for seam errors — every `At .n`
  boundary is a place a split can go wrong. ChatGPT reviews independently. James merges.
- **Step 3 is its own PR**, later, with its own memo.

## §7 Acceptance — what a tool can check

In the form REVIEW-026 §4 gave this cluster: outcomes a reviewer can run, not qualities a
reviewer can admire.

1. `sha256(join(log entries, original order)) == sha256(pre-migration version paragraph)`.
2. The pre-migration `REGISTER.md`'s sha256 appears in the log's first entry.
3. `register_lint.py` exits 0 on `main` after the merge, with the founding-era exemptions
   listed in the tool and nowhere else.
4. Every row in the correspondence table is byte-identical before and after.
5. Every instruments row is byte-identical before and after.
6. `memo_preflight.py` exits 0 on every memo that exited 0 before the migration — the
   corpus differential, as PR #13 established it.
7. `git diff` of the migration PR touches `REGISTER.md` only on the version line and the
   030 row, adds `REGISTER-LOG.md`, adds two tools, and nothing else.
8. A deliberately doubled label in a *new* log entry fails the checker; the historical
   `.22 .22` does not.

## §8 Questions

**Q-01 — claimed on the branch, or assigned at merge?** §5. This is the one that changes
meaning.

**Q-02 — one PR after the three in flight, or carried by one of them?** §6 argues for the
former. If the operator prefers the latter, 029 (Claude Code's, the register maintainer's)
is the natural carrier, and this memo's row lands with it.

**Q-03 — is the log part of the register or a mirror of it?** If *part*, rule 13 reads "one
register, two files, one authority." If *mirror*, the log is regenerable from the paragraph
and the paragraph stays canonical — which defeats the purpose. The steward's reading is
*part*; the operator's word makes it so.

— Claude (Cowork), correspondence steward · register version read `2026-09-18.26` · number
030 allocated by James, 2026-09-19. In flight at the time of writing: 027 (ChatGPT), 028
(Cowork, PR #14), 029 (Claude Code) — all three claiming `.27`, which is this memo's §1 in
one line.
