# Authoring a design-package cut — kit for Claude Design

**Kit version 1.0 · schema `design-package/v1` · governed by HANDOFF-LEGO-PIPE-024-R1.**
From cut **R2 (Friday 2026-09-25)** every exported archive carries a `package.yaml` at
its root, following `package.yaml.template` in this kit. The schema mirror
(`design-package.v1.schema.json`) is a copy taken at register version
`2026-09-18.26`; the canonical file lives in the repository at
`tools/schemas/design-package.v1.schema.json` and wins if they ever differ.

## What changes for you, in one paragraph

Your package stops borrowing identity. The zip you export names itself
(`DT-DESIGN`, `R2`, `as-exported`), names the brief it executes and the change
requests it answers, declares its predecessor with a digest, states honest
paths, and lists its own known defects. The importer verifies all of it
mechanically before the cut lands, and a build pin resolves to your exact bytes
forever. Ten minutes of manifest, in exchange for never being misquoted.

## The rules that will actually bite

1. **The package is `DT-DESIGN` now** (operator ruling 2026-09-18). `H-01` remains a
   *sheet* id — a package name matching `^[A-Z]{1,2}-\d{2}$` or equal to any sheet id
   is rejected. History keeps the H-01 label; nothing renames backwards.
2. **`path_base` is `"."` and paths are real.** Every `spec` / `standalone` /
   `screenshots` path in `index.json` must resolve inside the archive exactly as
   written — the R1 archive needed a `handoff/` prefix stripped from 86 of 102 paths,
   and that mistake now *fails* a designer cut instead of being quietly normalized.
   Design-session sources (`*.dc.html` under `prototypes/`, `candidates/`, `library/`)
   are welcome in `sheets[].file` — they are typed as opaque provenance and never
   resolved. Ship `standalone/` and `dt/` together.
3. **The decisions ledger is compared by DEC id, newest-first.** Prepend new entries as
   you always have. Every prior entry must survive **semantically unchanged**, with one
   exception: a prior row's Status cell may gain a supersession reference naming a new,
   higher id (`superseded by DEC-041`). Anything else — rewording, renumbering,
   deleting — bounces the cut. **In cut R2, add a DEC entry that (a) retires the ledger
   header's "never edits one" sentence (the backfilled Status cells on DEC-025/DEC-029
   contradict it) and (b) retires DEC-028's claim that `index.json` is the single source
   of status** — `package.yaml` and the ledger own their facts now; `index.json` is
   package-internal navigation.
4. **`governing_brief` + `answers`, both exact.** The brief that governs the cut
   (`HANDOFF-LEGO-PIPE-014-R0` until a new one is issued) and the list — possibly
   empty — of change requests this cut answers. Fully qualified (`…-R0`), matching a
   live register row.
5. **`supersedes` is qualified and digest-bound.** For R2:
   `{design_package: H-01, revision: R1, tree_sha256:
   b5664a2ad0ed7b7c7f093f4a1b369b32095799f73ade2af074b882e8038b9a1d}` (the committed
   as-committed state your R2 grows from). `null` only for a cut with no predecessor
   in any lineage — R2 is not that.
6. **`maturity` and `tier_coverage` are different axes.** `prototype` + `tier-1` is the
   honest pair today. Neither grants build authority; only a booklet's pin does.
7. **`mock_math` is a boolean you must state.** It stays `true` until an operator
   ruling on a specific cut says otherwise; the importer warns loudly either way.
8. **A defect names a failure — it cannot excuse one.** `known_defects` entries carry
   `{id, rule_id, paths, expected_failure, evidence, status}`. Declaring a defect never
   authorizes import; waivers are a separate importer-side record naming the authority.
   Identity, digest, containment and missing-manifest failures cannot be waived by
   anyone but the operator explicitly.
9. **`fixtures` names what seeded the cut** (set name + sha256). Weekly reseeding
   otherwise reads as design drift.
10. **Every required record is structurally checked, not just present.** `decisions`,
    `fixtures`, `sheets[]` and `known_defects[]` have typed fields: a null or malformed
    value inside one is an error, not a shrug.
11. **A Friday without a manifest is recorded, not imported.** The previous pin stays;
    the record shows a cut that didn't land. If you can't finish the manifest, say so
    in the relay instead of shipping without it.

## Checklist before export

- [ ] `package.yaml` at archive root, `manifest_schema: design-package/v1`, filled from
      the template — including `authoring_kit_version: "1.0"`.
- [ ] `design_package: DT-DESIGN`, `revision`, `cut_state: as-exported`, `cut` date
      **quoted** (`cut: "2026-09-25"` — unquoted YAML yields a date object and fails).
- [ ] Every `index.json` structured path opens from the archive root as written.
- [ ] New DEC entries prepended, contiguous after the last id; nothing else changed.
- [ ] `decisions.last_id` / `count` match the ledger.
- [ ] `sheets` list matches `index.json` exactly.
- [ ] R2 only: the DEC entry from rule 3 above.
