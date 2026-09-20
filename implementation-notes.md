# Implementation notes — lego-village-pipeline

## Deviations

- 2026-09-17 (founding, 019 §1.2): 019 instructed committing REGISTER.md "verbatim from the
  attached copy, version 2026-09-17.5"; the operator-exported copy was version **.6**, which
  supersedes .5 and itself instructs holders of older copies to discard them. Committed .6.
- 2026-09-17 (founding, 019 §1.3): "commit every correspondence document" — 10 registered rows
  had no on-disk file at the receiver (legacy review R0, 008, 009, 009-R1, 010 build-harness,
  011-R0, 014-R0, 016-R0, 017-R2, 018-R0). Committed the 7 files present; gap recorded at the
  register `.8` version line; files follow by attachment (rule 1).
- 2026-09-17 (founding, 019 §1.4): design package committed from `LEGO Village Pipeline
  LATEST.zip` (sha256 `e5b4857c…70ce`) rather than the memo-hashed `2.zip` (`e898a64a…7789`) —
  operator ruling: LATEST = same cut + post-review operator-requested ADDENDUM-A1 + 3 captures.
  Lineage recorded at register `.9`.
- 2026-09-17 (founding): HANDOFF-019 itself arrived by operator paste (register rule-1
  deviation). Operator ruled the paste authoritative; transcription committed with its sha256
  recorded at register `.7` (016 reconstruction precedent).
- 2026-09-17 (founding, 019 §1.6 vs §1.7): play-well-library is "empty except the attribution
  file and branch-flow CI rule", but act 7 (Northstar registration) requires a
  registry-resolvable `.claude/northstar.md` in-repo. Included it; flagged for operator
  ratification with the northstar proposals.
- 2026-09-17 (tooling): macOS system `python3` lacks PyYAML, so `tools/preflight.py` runs used
  the newline-course venv interpreter. Input to the 011-R2 preflight-CLI replacement: vendor its
  deps properly.
- 2026-09-18 (register `.12`): Cowork's instruction said "note in the research rows", but
  research documents have no memo identity (prefix+number+revision) and table rows are sticky
  forever under "rows stand". Recorded the research landing + concatenation note in the `.12`
  version note instead of adding unnumbered table rows. Cowork/operator can override.
- 2026-09-18 (register `.12`): Cowork's manifest said two untracked additions; the tree had a
  third — `Claude outputs/CORR-LEGO-PIPE-021….md` at repo root, a byte-identical duplicate of
  the committed 021 (transfer artifact from the drop location). Verified sha256 equal, removed,
  recorded in the version note. Not committed.
- 2026-09-18 (governance, register `.14`): the founding acts assumed direct commits to `main`
  were the mandated form ("first commit lands…"); the fleet norm the operator expected was
  PR-flow. All direct pushes through `a7ce78c` stand (hashes are cited in the register — the
  record is never rewritten); PR-flow + branch protection in force from `.14`. Discovered
  en route: the account is GitHub Free, not Pro — play-well-library (private) cannot get
  server-side protection until upgrade or visibility change; hook + CI only there.
- 2026-09-18 (publish sweep): pre-publish PII sweep flagged `v004-play-eli` (branch-name
  example, 9 occurrences in registered documents, unredactable — hash is identity). Operator
  human review ruled: not a name, not PII. Repo flipped public on that ruling.
- 2026-09-18 (desktop-guidance PR): the review plan assumed stable repository references while
  the two guidance commits were prepared; another local desktop process advanced pipeline `main`
  and published the same one-file feature branch concurrently. Kept the refreshed remote branch
  after verifying its PR contains only `AGENTS.md`; no history was rewritten.
- 2026-09-19 (CORR-027 merge-train shepherding): the plan assumed the allocated 027 branch would
  retain the shared checkout while its memo was prepared; Claude Code switched that checkout to
  PR #16 and began its author-owned corrections, leaving both agents' uncommitted files together.
  Left Claude Code's 029 and register edits untouched and moved 027 into an independent clone.
  Cowork later identified its global `git worktree prune` as the process that removed the first
  worktree's metadata; agents now avoid global pruning in the shared repository and use isolated
  clones or remove only their own worktrees by explicit path.
- 2026-09-20 (CORR-031 train finalization): the plan assumed a chained `git worktree add` then
  `git merge` would run the merge inside the new PR #18 worktree; the shell retained the source
  checkout as its working directory and made a local-only merge there instead. Left that merge
  unpushed and repeated the operation from the explicitly selected PR #18 worktree.
- 2026-09-20 (proposed HANDOFF-LEGO-PIPE-032-R0 draft, PR #21): the standing rule assumed every
  commit touching `docs/correspondence/` bumps the register version line; the operator instructed
  that this draft, non-operative, unallocated work order be **committed to the unmerged draft
  branch** `corr/032-register-migration-work-order` under `docs/correspondence/`, with canonical
  `main` and the register left unchanged (TR-32-R2-05: this commit has not landed — "landed"
  means merged to canonical `main`, which the register itself defines as where correspondence
  takes effect, and PR #21 remains open and unmerged). Took the conservative option — committed
  the memo without a version edit, no register row, no allocation — and recorded it here per the
  lead's reconciled repair request (RR-32-11) rather than deciding the per-commit-versus-per-
  landing question, which stays open on the memo's own operator docket (Q-02, Q-10).
- 2026-09-20 (HANDOFF-LEGO-PIPE-032-R1, PR #21): the standing rule assumed every commit touching
  `docs/correspondence/` bumps the register version line; the operator's ratified docket (PR #21
  comment 5752476543) directed a ratified R1 revision to be committed to the same unmerged draft
  branch, with the register still unedited until the separate atomic migration landing and no
  version claimed on a branch (Q-03). Took the conservative option — added the R1 memo only,
  no register row, no version edit, R0 untouched — and recorded it here; the per-commit rule
  is retired by Q-02/Q-10 only when the migration PR merges, so this is a recorded departure,
  not an application of the new rule.
- 2026-09-20 (HANDOFF-LEGO-PIPE-032-R1 implementation, PR `feat/032-register-migration`): R0 §4
  item 8 assumed the record schema's per-kind `oneOf` could be "validated by the existing
  `schema_lint.py` subset interpreter (no new interpreter)" and the §4 inventory lists no change
  to `tools/schema_lint.py`; the territory: the subset interpreted only required / properties /
  const / enum / type / pattern / items / additionalProperties — no combinator, so a per-kind
  required/forbidden-key contract was inexpressible. Took the conservative option — extended the
  ONE shared interpreter in place (`oneOf`, `anyOf`, `allOf`, `not`; the module's own "extend
  here, never by copy" rule) rather than a second interpreter or a prose-only contract; the memo
  corpus differential (`tests/test_design_package.py`, frozen fixture vs live, and
  `tests/test_register.py` base-vs-head) is the proof nothing else moved.
- 2026-09-20 (032-R1 implementation): Q-13's recommended cell text "accepted as amended by
  HANDOFF-032 at `.next`" and Rule 18's template "register `<version>`" assumed the landing
  version could be written into `REGISTER.md` on the branch; Q-03 forbids a branch claiming a
  version, and the finalizer edits only the pointer, the record and the ledger. Took the
  conservative option — the 030/031 cells and Rule 18 cite the memo and the landing ("the
  migration landing's version record names it"; "lands with the HANDOFF-LEGO-PIPE-032-R1
  migration, register read `.31`"), and the version record's `affected_memos` carries the link.
- 2026-09-20 (032-R1 implementation, G-12): the plan assumed `memo_preflight.py`'s output was
  independent of the version line ("exit code + output … equal"); the territory: its register
  cross-check (`key in regtxt` … "superseded" not on the rest of that line) scanned the whole
  file by substring, so at `B` the 39 KB version line masked the WARN "NNN-Rn already listed in
  register (expected on re-run)" for 15 of 34 memos, and with the line migrated the WARN appears.
  `memo_preflight.py` is a non-goal (R0 §11), so it was not touched. Took the conservative option —
  the differential asserts exit codes identical for every memo and outputs identical except that
  exact WARN line (and asserts every remaining difference IS that line, present at head, absent at
  base); raised on the PR as a numbered finding for the reviewers, not settled here.
- 2026-09-20 (032-R1 implementation): R0 §5 named four refusal codes (RF-01…RF-04); the
  territory needed two more named exits — RF-05 (nothing to finalize / `--check` on a head that
  is not yet finalized) and RF-06 (lint error after the writes → every write reverted). Added
  them additively with positive and mutation cases; the meta-test enumerates them.
- 2026-09-20 (032-R1 implementation): R0 §4 item 5 seeded "the doubled `.22` label" as one
  anomaly; the check as written (`At \`.n\` \`.n\``) also matches the `.24` note, which QUOTES
  the label it reports. Took the conservative option — recorded a second `doubled_label` entry
  (A-02, affects `.24`, cited as a quotation) rather than special-casing quoted text in the
  checker; both are frozen data.
- 2026-09-20 (032-R1 implementation, test fixture): the two-branch rehearsal's RF-03
  correspondence variant first landed the intervening branch by fast-forward push; RL-10 then
  correctly refused the tree (a correspondence commit on `main`'s first-parent line with no
  version record, and a record whose `finalized_from_main` was not its introducing commit's first
  parent). The fixture was corrected to land by merge commit — the test was not weakened; the
  refusal is the Q-06 merge-commit setting's rationale, demonstrated.
- 2026-09-20 (032-R1 implementation, live rehearsal): R0 §3's tree lists `register/pending/`
  holding only branch-side notes; the territory: a landing that consumes every note in
  `pending/` while adding a record whose body is the note makes git's directory-rename
  detection infer `pending/ → versions/` and relocate a concurrent branch's newly added note
  into `versions/` on `git merge origin/main` (observed live as a conflict on
  `versions/091.md`, then refused by RF-04). Took the conservative option — a
  `register/pending/.gitkeep` (not authority, not a note) so the directory is never emptied,
  written by the finalizer if absent; the battery reproduces the hazard without it and its
  absence with it. One file added to the inventory, recorded here.
