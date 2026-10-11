# Schema requests — addendum R4 (2026-10-10)

Additive to `handoff/schema-requests.md`.

1. **Page index as data.** Benny routes against `data/pages-index.json` (code, title, href, why, keywords). Production should expose the same from the sheet registry so the chief of staff and Hub cards read one source.
2. **Change provenance on every status line.** The ripple needs, per dependent value: `changedBy {sheet, action, at}`, `previous` and `acknowledgedAt`. Today W-00 fakes this in component state.
3. **Dependency edges.** "Grade & banking waits on railhead height" is hard-coded. A `dependsOn` list per check/task lets the ripple be computed, not scripted.
4. **Kind per sheet.** Each sheet declares its `kind` (one of the ten) so nameplate, verb line, threshold strip and title block can be generated, not hand-written.
