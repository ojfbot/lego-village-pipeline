---
correspondence_schema: lego-pipe-memo/v2
memo: HANDOFF-LEGO-PIPE-024
revision: R0
status: for_review
memo_type: handoff
title: "Design-package protocol — fielded identity, instruments registration, DT-DESIGN"
date: 2026-09-18
thread: design
from:
  actor: Claude Code
  role: implementing_agent_and_register_maintainer
to:
  - actor: Claude (Cowork)
    role: correspondence_steward_reviewer
  - actor: ChatGPT
    role: peer_correspondence_steward_reviewer
  - actor: James
    role: operator_and_final_authority
  - actor: Claude Design
    role: design_agent_downstream
argument: >
  In which the design package stops being a black box with borrowed identity: the
  operator's four rulings of 2026-09-18 are recorded, the fielded manifest and
  instruments-table registration that ARCHITECTURE §1a proposed and 023-R2 §10 left
  open are specified, three historical bundles get verbatim homes, and the whole
  protocol is put to both stewards for commentary before any of it is implemented.
provenance:
  source_artifacts:
    - {name: "operator directive, 2026-09-18", role: "a dedicated subdirectory for design handoff bundles + a structure and schema integrated with the correspondence system; review round instructed before implementation"}
    - {name: "operator rulings, 2026-09-18 (structured question)", role: "the four rulings recorded in §2: siblings per-cut, instruments table, memo 024, DT-DESIGN"}
    - {name: "docs/correspondence/ARCHITECTURE-correspondence-and-research.md", role: "§1a — the design package dissected; this memo lands its four proposals"}
    - {name: "correspondence/HANDOFF-LEGO-PIPE-023-R2-drafting-table-on-fixtures-and-the-program.md", role: "§5.2 weekly cuts precondition, §10 open items 1–2 settled here"}
    - {name: "three unzipped desktop bundles (Initial / Second / Latest)", role: "verified byte-for-byte against docs/design/H-01-R1/ and each other; lineage in §1"}
    - {name: "docs/correspondence/REGISTER.md", role: "register read at 2026-09-18.22 on origin/main; 024 allocated by operator ruling"}
authority:
  decision_owner: James
register:
  number: 024
  allocated_by: "James, 2026-09-18 (structured ruling: protocol ships as registered memo 024)"
register_version_read: 2026-09-18.22
parts:
  "1": "Why now — the black box, the deadline"
  "2": "The operator's four rulings, recorded"
  "3": "The manifest contract — designer file, importer record"
  "4": "Tooling — package preflight and drift checker"
  "5": "The docs/design/ home — layout, README, authoring kit"
  "6": "Register integration — instruments table, import lane"
  "7": "Landing plan — four PRs, before cut R2 (25 Sep)"
  "8": "What the reviewers are asked"
---

# HANDOFF-LEGO-PIPE-024 R0 — Design-package protocol

**Status: for review.** Claude Cowork and ChatGPT are asked for commentary before
implementation begins. Nothing below is built; the operator's rulings in §2 are settled,
everything else is proposal.

## §1 Why now — the black box, the deadline

A design package today has no identity of its own. ARCHITECTURE §1a says it plainly: it
carries no memo frontmatter, nothing in it states a revision, what brief it executes, or
when it was cut, as a field. Identity is borrowed — the executing brief's register row, a
zip sha256 recorded in prose, and a label (`H-01`) that is really a sheet id. 023-R2 §5.2
moves to weekly Friday cuts and names the precondition: a fielded manifest, a name that is
not the sheet id, and a working drift checker, **needed by cut R2 on 25 Sep**. Its §10
leaves two items open — the manifest and where cuts are registered — saying one line from
the operator settles them. That line has now been spoken (§2).

Separately, the operator holds three unzipped bundles on the desktop. Verified against the
repo byte-for-byte:

- **"Initial"** = the R0 bundle: 72 files, 7.9 MB — matching the legacy unnumbered
  review's record of the bundle it reviewed (72 files, 8.0 MB). Not in the repo.
- **"Second"** = the reviewed R1 cut: 94 files — the cut whose zip sha256 (`e898a64a…7789`)
  the 014-R0 row cites. Its bytes are not in the repo; it differs from the committed
  package in seven files (pre-addendum).
- **"Latest"** = byte-identical to `docs/design/H-01-R1/` (verified `diff -r` empty).
  Nothing to land.

The zips themselves are gone; only unzipped folders remain. The register-cited hashes are
therefore not recomputable — the import records in §3 say so honestly rather than
pretending verification that did not happen.

## §2 The operator's four rulings, recorded

Taken 2026-09-18 by structured question; James is decision owner on all four.

1. **Historical bundles land as siblings per-cut**: `docs/design/H-01-R0/` (Initial) and
   `docs/design/H-01-R1-reviewed/` (Second). One directory per cut stays the convention;
   the existing `H-01-R1/` never moves.
2. **Cuts are registered in a new instruments table** in REGISTER.md — the second table
   proposed at 017 §1.2 and ARCHITECTURE §1a: name · revision · executes · sha256 ·
   imported at version · pinned by bags. This settles 023-R2 §10 item 2: instruments
   table, not per-cut `HANDOFF-` rows in the main table.
3. **The protocol ships as this registered memo**, number 024 allocated by the operator in
   the same ruling.
4. **The package label renames to `DT-DESIGN` from cut R2.** Future cuts land as
   `docs/design/DT-DESIGN-R2/`, `DT-DESIGN-R3/`, …. Existing `H-01-*` directories and
   every existing citation keep their names; the instruments table records the mapping
   (DT-DESIGN R2 supersedes H-01 R1), so `design_pin: H-01 R1` in circulating briefs stays
   valid until a bag boundary moves it.

## §3 The manifest contract — designer file, importer record

Two artifacts, two authors, two homes.

**`package.yaml` — designer-authored, at archive root, inside the zip.** From cut R2,
Claude Design writes it before export, so it arrives inside the verbatim bytes. Fields:

```yaml
manifest_schema: design-package/v1
design_package: DT-DESIGN        # never a sheet id; validator enforces
revision: R2
executes: HANDOFF-LEGO-PIPE-014-R0   # or the change request this cut answers
cut: 2026-09-25
supersedes: R1                   # null only on a package's first cut
manifest_origin: designer
path_base: "."                   # names the shipped root — closes defect D-4 by contract
index: index.json
sheets:                          # every sheet, honest fidelity
  - { id: A-01, title: Layout Canvas, fidelity: tier-1 }
  # fidelity: direction | intent | prototype | tier-1 | tier-2 | tier-3
decisions: { ledger: decisions.md, range: [DEC-001, DEC-041] }
schema_requests: schema-requests.md
known_defects: [ { id: D-7, summary: "…" } ]   # declared defects import as warnings
debts: [ { id: G-1, summary: "journey hierarchy", owner: claude-design } ]
mock_math: true                  # constant; a package without it does not import
```

**Import record — importer-authored, in `docs/design/manifests/`, never inside the
package.** The verbatim rule stays mechanically checkable (`diff -r` against the archive
is empty, no exclusion list), and the drift checker never sees importer files as drift.
Fields: `import_record_schema: design-package-import/v1`, `package_dir`, `design_package`,
`revision`, `sha256`, `bytes`, `file_count`, `imported_at_register_version`,
`import_date`, `imported_by`, `executes`.

**Historical packages get reconstructed manifests, marked honestly.** R0, R1-reviewed and
the committed R1 cannot carry a designer manifest — Claude Design cannot retro-sign bytes
it did not export, and the trees are frozen. Their `package.yaml` files live in
`manifests/` with `manifest_origin: importer_reconstructed` and a `reconstruction` block
(authored_by · date · sources), the sources being the register version notes and rows the
fields were read from. Where the zip hash is unrecomputable (§1), the import record says
`sha256: unverifiable — folders received unzipped; identity corroborated by file count,
size and content diff against the committed R1 tree`. Recorded, not repaired.

## §4 Tooling — package preflight and drift checker

Both Python, in `tools/`, sharing the `tools/.venv` provisioned by `setup-preflight.sh`.
`memo_preflight.py` and the frozen `preflight.py` are not touched; the small
schema-interpreter is duplicated into the new file with a do-not-diverge provenance note,
because the cited validator should not churn for a sibling's benefit.

**`tools/package_preflight.py PACKAGE_DIR REGISTER.md [--previous PREV_DIR] [--manifest
PATH]`** — exit 0 pass / 1 errors / 2 usage. Checks, in order: manifest present (in-dir
preferred; `manifests/` fallback for reconstructed; a reconstructed manifest found in-dir
is itself an error); schema-valid against `tools/schemas/design-package.v1.schema.json`,
dispatching on `manifest_schema`; `design_package` is not a sheet id; `standalone/` and
`dt/` co-present with every `../dt/*` reference resolvable; every `index.json` path
resolves against the committed tree, with a documented leading-`handoff/` strip fallback
— unresolvable paths are errors unless the manifest's `known_defects` declares them, in
which case they downgrade to warnings carrying the defect id; `decisions.md` append-only
against `--previous` (every prior entry byte-identical, new ids only appended — a rewrite
is a contract breach, not drift); `mock_math` true; manifest and `index.json` agree on the
sheet set; `executes` appears in the register text. Report style mirrors
`memo_preflight.py` so operators read one idiom.

**`tools/package_drift.py OLD_DIR NEW_DIR [--out PATH]`** — the drift checker 023-R2 §5.2
requires, per the axes of 023-R1 §5.3: a per-sheet markdown table (spec changed · states
changed · a11y tree changed · schema request added/withdrawn · decision entries added),
per-sheet detail sections, a package-level section (new decision ids, defects/debts delta,
per-sheet fidelity changes from the two manifests), and the ledger append-only gate up
front (failure exits 1 — a cut that rewrites history is bounced, not triaged). Reports are
committed to `docs/design/manifests/drift-<old>-to-<new>.md` as part of each import. The
package's own `check-manifest.mjs` stays what it is: frozen historical bytes, defective
against the committed tree, superseded by this repo-side tool.

## §5 The docs/design/ home — layout, README, authoring kit

```
docs/design/
  README.md              # the subdirectory contract: inventory table, verbatim rule,
                         # naming, identity, the import checklist, pointers to 023-R2 §5
  authoring-kit/         # exportable to the Claude Design session via operator relay
    AUTHORING.md         # the design-session checklist (see below)
    package.yaml.template
    design-package.v1.schema.json   # byte-copy mirror, headed by the register version copied
  manifests/             # importer records + drift reports, outside every package dir
  H-01-R0/               # 72 files, verbatim           (this memo's landing plan)
  H-01-R1-reviewed/      # 94 files, verbatim           (this memo's landing plan)
  H-01-R1/               # existing, untouched
  DT-DESIGN-R2/          # 25 Sep, the first designer-manifested cut
```

**The import checklist** (formalizing 019 §1.4, to live in the README): operator relays
the zip and states its sha256 → receiver recomputes and verifies → unzip to scratch →
`package_preflight.py` passes against scratch → branch `corr/design-import-<dir>` → commit
verbatim, verify `diff -r` empty → author the import record → run `package_drift.py`
against the previous cut, commit the report → bump the register version line and add the
instruments row in the same PR → PR; self-merge only under the relayed-landings lane.

**The authoring kit** is how the contract reaches Claude Design, which never touches the
repo: after this memo is accepted, James relays the three kit files into the design
session. AUTHORING.md carries the design-side lessons in imperative form: `package.yaml`
at archive root beside `index.json`; every `index.json` path resolves from the shipped
root (the defect-D-4 lesson, stated); `decisions.md` only ever appends — a rewrite bounces
the cut; `standalone/` and `dt/` ship together; every sheet listed with honest fidelity;
declare the defects you know — a declared defect imports as a warning, an undeclared one
as a finding; export one zip of the whole tree and the operator states its sha256 on
relay. The template echoes `authoring_kit_version` so the importer knows which kit
produced a cut.

## §6 Register integration — instruments table, import lane

**The instruments table** lands in REGISTER.md as a second table under its own heading,
columns per §2 ruling 2: `Instrument · Revision · Executes · sha256 · Imported at ·
Pinned by`. First rows: H-01 R0, H-01 R1-reviewed, H-01 R1 (pinned by bags 1–3), then
DT-DESIGN R2 onward. The correspondence table stays what it is — speech acts only.

**Import-lane authorization (proposed, needs the operator's ratification with this
memo):** the register writes that an import produces — the version-line bump and the
instruments row for a cut the operator relayed — are part of the relayed landing itself
and ride the relayed-landings self-merge lane defined at register `.14` and extended at
`.21`. Protocol changes, schema changes and this memo remain outside that lane; James
merges them.

## §7 Landing plan — four PRs, before cut R2 (25 Sep)

Strictly serial; every one edits the register version line, so each branch cuts from
freshly-merged `main`.

- **PR-A `feat/design-package-contract` — James merges** (code, schema, policy): the two
  JSON schemas, `package_preflight.py`, `package_drift.py`, shared helper,
  `docs/design/README.md`, the authoring kit, the instruments table, and this memo's
  status flip on acceptance.
- **PR-B `corr/design-import-H-01-R0` — relayed-landings lane**: R0 verbatim,
  reconstructed manifests, register bump + instruments row.
- **PR-C `corr/design-import-H-01-R1-reviewed` — same lane**: the reviewed cut verbatim,
  manifests, the R0→R1-reviewed drift report, register bump + row.
- **PR-D `corr/design-manifests-H-01-R1` — same lane**: no package bytes; reconstructed
  manifests for the committed R1, the R1-reviewed→R1 drift report — which must show
  exactly the known delta: seven changed files plus the addendum and three hub captures —
  register bump + row.

Then the kit is relayed, and cut R2 on 25 Sep is the first designer-manifested import.
Ground-truth verification is built in: the PR-D drift report's expected answer is already
recorded at register note `.9`, and `package_preflight.py` on the committed R1 must warn
on exactly the declared first-day facts (D-1…D-6) and nothing else.

## §8 What the reviewers are asked

Commentary before implementation, in whatever form your lane supports (PR review comments
on this memo's PR, or a reply memo). Sharpest known tensions, to save you the excavation:

1. **Field completeness of `package.yaml`** — is anything the drift loop or the pin
   discipline needs missing or superfluous? (Compare 023-R2 §5.2's needs and §1a's
   proposal.)
2. **The `manifests/` sibling vs manifests inside package dirs** — the verbatim-purity
   argument won here; is there a review or implementation cost we are not seeing?
3. **Reconstructed manifests for the three historical cuts** — is
   `manifest_origin: importer_reconstructed` + declared sources honest enough, given the
   original zips are unrecoverable?
4. **The import-lane authorization in §6** — is folding instruments-row writes into the
   relayed-landings lane sound, or should every register write stay operator-merged?
5. **The DT-DESIGN mapping** — does recording "DT-DESIGN R2 supersedes H-01 R1" in the
   instruments table keep every circulating `design_pin: H-01 R1` unambiguous?
6. **Anything the weekly cadence breaks** — the protocol was designed against 023-R1's
   fortnightly cuts and re-checked against 023-R2's weekly ones; a fresh eye may catch a
   seam we missed.
