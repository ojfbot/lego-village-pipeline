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
