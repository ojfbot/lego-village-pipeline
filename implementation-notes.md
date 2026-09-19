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
  Left Claude Code's 029 and register edits untouched and moved 027 into an independent clone;
  a first shared-repository worktree was abandoned after another process pruned its Git metadata.
