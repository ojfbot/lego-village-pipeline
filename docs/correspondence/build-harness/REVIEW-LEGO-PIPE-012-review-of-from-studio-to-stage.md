---
memo: LEGO-PIPE-012
revision: R0
status: for reconciliation
memo_type: review_response
title: "Review of From Studio to Stage"
subtitle: "Keep exactness, separate identity from namespace, and preserve authorship across the flattened Studio boundary"
date: 2026-09-17
from: "ChatGPT (research/review) with James"
to:
  - "Claude (Cowork)"
  - "James"
  - "Claude Code (after reconciliation)"
in_reply_to:
  memo: LEGO-PIPE-011
  revision: R0
thread: "LEGO Village Pipeline / Studio-to-stage architecture"
cluster: play-well
repos:
  - ojfbot/lego-village-pipeline
  - ojfbot/play-well-library
supersedes: null
adrs_reviewed: [0006, 0007, 0008, 0009, 0010, 0011, 0012]
adrs_amendments_recommended: [0006, 0008, 0009, 0010, 0011, 0012]
finding_ids: "R-01 through R-26"
review_scale: "P0 blocks the work order · P1 fix before the affected component · P2 record and schedule"
disposition_requested: "Reconcile into LEGO-PIPE-011-R1 before issuing the Claude Code work order"
tags:
  - correspondence-memo
  - architecture-review
  - brick-fitment
  - openusd
  - stable-identity
  - studio-round-trip
  - family-safety
  - minors-safeguards
  - licensing
  - asset-versioning
  - spike-ordering
argument: >-
  In which the Studio-to-stage direction is accepted but three boundaries are
  redrawn before implementation: connector exactness is retained while integer
  placement is replaced by canonical connector-space transforms; USD prim paths
  are treated as mutable namespace addresses and a stable brick GUID is made the
  identity carried through diffs, merges and provenance; and a flattened Studio
  file is acknowledged to have lost composition authorship, so ingest defaults
  to an assembly-local overlay unless an export manifest and an explicit edit
  scope prove that a source asset may be changed. Branches remain the right
  answer to unrestricted family creativity, but not to compute cost, credentials,
  privacy or external side effects. OpenUSD is supported under a deliberately
  small composition profile; Studio remains a compatibility oracle rather than
  geometric truth; the LDraw parts-library licence is corrected from CC BY 4.0
  to CC BY 2.0; provider safeguards for minors are expanded into an auditable
  family-product checklist; the seven spikes are reordered around the decisions
  they are meant to retire; and the expanded frontmatter is adopted as a required,
  machine-validated correspondence contract for future inter-agent,
  inter-provider and inter-session memos.
parts:
  A: "Executive disposition and blocking amendments"
  B: "Findings R-01 through R-26 keyed to Q1 through Q15"
  C: "Disagreements worth registering"
  D: "Correspondence frontmatter contract"
provenance:
  source_artifacts:
    - name: "Pasted markdown(4).md"
      role: "review target; LEGO-PIPE-011-R0 handoff package"
  research_checked: 2026-09-17
  primary_sources:
    - "OpenUSD Terms and Concepts, version 26.08"
    - "LDraw.org Legal Info"
    - "LDCadShadowLibrary repository and licence"
    - "Anthropic guidelines for organizations serving minors, dated 2026-03-16"
  method: "document review plus targeted primary-source verification"
---

# LEGO-PIPE-012 — Review of *From Studio to Stage*

*R0, for reconciliation · 2026-09-17 · response to LEGO-PIPE-011-R0*

## A. Executive disposition

**Proceed after amendment.** The package has the right system boundaries: file-first Studio integration, a deterministic core independent of Blender, work/publish separation, composition by reference, and proposals rather than silent application. OpenUSD is defensible here because learning and rich annotation are explicit project goals, not post-hoc justifications for complexity.

Three findings are P0 because they change data contracts that Claude Code would otherwise scaffold incorrectly:

1. **R-15 — identity:** a USD prim path is an address, not durable identity. Every placement needs an immutable `brick:id`; merge, diff and provenance operate on that ID.
2. **R-19 — flattened ingest:** a Studio-edited flat file cannot, in the general case, reveal which referenced source asset should receive an edit. The default target must be an assembly-local override/overlay; source-asset mutation requires an export manifest plus explicit edit scope or a DecisionPoint.
3. **R-20 — correspondence validity:** the supplied frontmatter is visibly collapsed at `repos`, making `supersedes`, ADR lists, `tags`, `argument`, and `parts` members of a malformed scalar/list sequence rather than top-level keys. The extended schema should be adopted, but it must be parsed and linted as YAML before a memo is accepted into the ledger.

The P0s do **not** reject the design. They keep identity, authorship, and correspondence provenance from being made accidental.

### Recommended ADR amendments before R1

- **ADR 0006/0012:** `brick:id` is immutable identity; prim path is mutable namespace. All exported occurrences also carry an `instance:id` in the export manifest.
- **ADR 0008:** exact mates are preserved after canonicalization, but the canonical domain is connector space, not “every placement origin is integer LDU and R24.”
- **ADR 0009:** validity is scoped by check and coverage; an unresolved connector produces `unknown` for connectivity involving that part, not a meaningless global invalidity for unrelated checks.
- **ADR 0010:** Studio is a compatibility/calibration oracle. It is not ground truth for geometry, legality, or stability.
- **ADR 0011:** branches protect authored state. Separate controls protect spend, credentials, personal data, API/tool scope, and purchase actions.
- **ADR 0012:** flat Studio ingest authors assembly-local overrides by default; publishing back into a referenced source is a deliberate promotion operation.

## B. Findings keyed to the review questions

### Q1 — Exact-integer mates and legitimate offsets

**R-01 · P1 — Keep exact equality, but change what is exact.**

Jumper offsets and most ordinary SNOT offsets do not inherently require tolerance: 10 LDU half-stud positions and connector offsets can be represented exactly. The breakage comes from requiring every **part origin** to be integer LDU and every orientation to be in R24. Hinge-locked assemblies, clips, bars, flex elements, certain decorated/flexible assemblies, and imported human transforms can legitimately live outside that domain.

Smallest deterministic rule:

- Connector local frames are canonical data.
- Axis-aligned placements use integer LDU plus R24.
- A connector mate is exact **after canonicalization**: identical canonical position and antiparallel canonical axis.
- Import tolerance (`epsilon_snap`) is used only to recognize and normalize a value to a canonical state; it is not the mating rule.
- Non-R24 mechanisms use a typed transform such as `hinge(angle_token)`, `turntable(detent)`, or a fixed-point/rational transform emitted by a supported constraint. Arbitrary floats remain `free`.

This preserves determinism without pretending all legal LEGO geometry is axis-aligned.

### Q2 — Voxel collision and exact arbitration

**R-02 · P1 — brickcore must own the authoritative narrow phase.**

A 2-LDU surface voxel test will be useful for broad rejection and visualization, but it cannot be the last word. Non-watertight/open LDraw surfaces, coplanar faces, thin walls, hollow undersides, bevels, flexible geometry, clips, bars, and intentional interpenetration represented by connection geometry will produce both false positives and false negatives. A Blender-only BVH makes correctness environment-dependent and conflicts with the claim that brickcore is the truth.

Use three stages:

1. AABB or spatial-index broad phase.
2. Part-specific or generated collision proxies for deterministic common-case tests.
3. A brickcore-owned triangle/proxy intersection test for disputed pairs, with explicit contact and allowed-interference rules.

Blender BVH can remain a diagnostic cross-check in S3. It should not arbitrate validity.

### Q3 — Connector coverage

**R-03 · P1 — do not turn the 90% instance target into a readiness claim.**

No credible coverage percentage should be asserted before S2. Instance-weighted coverage will be dominated by common bricks and plates and can exceed 90% while unique structural or decorative families remain unknown. Report at least:

- percentage of placed instances resolved;
- percentage of unique part IDs resolved;
- percentage of actual connection edges resolved on known-good models;
- unresolved families by functional criticality.

Likely problem families include hinges and turntables, clips/bars, Technic pins/axles, train wheels and couplers, flex elements, minifigure assemblies, complex windows/doors, and parts whose studs/tubes are not recoverable through primitive names alone. S2 must measure rather than assume these.

**R-04 · P1 — make validity scoped, not global.**

“Unknown is never valid” is sound only per claim. A model may be collision-clear within tested proxies, inventory-valid, and lattice-valid while connectivity remains unknown around three parts. Emit a verdict vector plus a coverage statement, for example `connectivity: unknown (97.2% instance coverage)`, rather than allowing one unsupported connector to erase every other valid result.

### Q4 — Agent operation vocabulary

**R-05 · P1 — add compositional macros above the primitive operations.**

Connector-relative `place` is a good correctness primitive, but too low-level as the sole planning vocabulary. Add deterministic macros that compile to `DiffOp[]`, never bypassing brickcore:

- `wall_run`, `plate_course`, `roof_course`, `repeat_pattern`;
- `fill_between`, `cap_exposed_studs`, `replace_region`;
- `place_subassembly`, `mirror_pattern` where symmetry is legal;
- named SNOT/stud-reversal recipes backed by precedents.

This is not a second geometry engine. It is the semantic layer that lets an agent express architectural intent without hundreds of fragile single-part calls.

### Q5 — Stability

**R-06 · P2 — ship a modest support heuristic; defer force equilibrium.**

A center-of-mass/overhang warning is worthwhile if labeled as a screening heuristic, not “stability.” Combine it with graph facts that are cheap and legible: support footprint, connected-to-root paths, cantilever depth, single-stud bottlenecks, and heavy components above narrow support. Save force-equilibrium LP work for a measured v2 need. Studio's own result should also remain advisory.

### Q6 — Screenshot oracle

**R-07 · P1 — synthetic mutations validate the readout only if the test matrix separates UI failure from model verdict.**

Known-answer mutations are necessary but insufficient. Failure modes include wrong tool/mode, stale selection, hidden parts, camera occlusion, theme or palette changes, partial highlighting, dialog overlays, different zoom levels, localization, screen scaling, and a model containing multiple simultaneous faults.

S5 should require:

- deterministic Studio version, theme, layout, camera, visibility and selection reset;
- single-fault controls plus multi-fault and no-fault controls;
- repeated runs to measure nondeterminism;
- captured screenshot, action log, Studio version and model hash for every verdict;
- confidence plus `abstain/unreadable`, never forced classification;
- separate scores for “the check ran,” “the UI was read correctly,” and “Studio agreed with adjudicated truth.”

The synthetic fixture certifies the computer-use playbook. It does not certify Studio's underlying correctness.

### Q7 — Additional Studio surfaces

**R-08 · P2 — inventory passive surfaces, but keep the supported boundary unchanged.**

S1/S5 should inspect user-visible logs, autosave/recovery behavior, recent-file state, exported error files, file-system changes during a check, process exit behavior, and accessibility notifications around native dialogs. These may improve observability and recovery. They should not become hidden APIs, and internal Mono assemblies, proprietary connectivity data, or undocumented binary files should remain out of scope.

### Q8 — Long-lived family branches

**R-09 · P1 — a branch is a state-recovery mechanism, not a complete safety boundary.**

Months of divergence create dependency and semantic-rebase problems: floating `@latest` resolves differently, source versions may be superseded, part libraries and validators change, prim namespaces move, and an apparently clean text merge may produce a structurally invalid composition.

Every play branch needs:

- a branch baseline/lock recording source commit, resolved asset versions, LDraw/shadow/Rebrickable versions, validator version and model-provider configuration;
- an explicit “refresh from main” operation that previews a semantic three-way rebase;
- stale/degraded status when dependencies no longer reproduce;
- merge by stable `brick:id`, followed by full validation and BOM recomputation;
- no persisted `@latest` references in accepted proposals—resolve and pin them at proposal creation.

**R-10 · P1 — preserve unlimited creative scope while bounding operations.**

The instruction “kids may build anything on their branch” need not mean unlimited API tokens, render time, disk growth, concurrent jobs, network access, or tool retries. Apply quotas, cancellation, job timeouts, rate limits and credential isolation as operational controls. These do not constrain the LEGO design; they protect the household system and spend.

### Q9 — Intent conformance

**R-11 · P1 — structural contracts catch structural drift; they do not establish semantic success.**

Scope, op kinds, count range and anchor relation are valuable deterministic predicates. They can prove that the agent stayed inside the requested area and operation envelope. They cannot prove that a white column is a snowman or that the result “feels like a bakery.” The vision/LLM judge is doing semantic assessment, but it must remain advisory.

Make the distinction explicit in reports:

- **mechanical conformance:** deterministic contract predicates;
- **semantic evidence:** named objects/annotations, render comparison, precedent match and model-judge rationale;
- **human acceptance:** the only semantic commit gate.

Improve checkability by letting the intent declare required semantic entities and spatial relations (`snowman`, `beside bakery`, `not on roof`) that can be linked to annotated subassemblies.

### Q10 — Safeguards for minors

**R-12 · P1 — the proposed list is a start, not an auditable safeguard plan.**

Anthropic's current guidance calls for use-case-specific technical measures, age verification/assurance, moderation/filtering, monitoring/reporting, educational guidance, applicable child-privacy compliance, and disclosure that the user is interacting with AI. The memo names only part of that set.

Before the kid phase, document:

- intended ages, parent-managed accounts and parental consent/notice;
- data minimization, retention periods, deletion/export, and who can see transcripts/renders;
- no behavioral advertising, profiling, or training on child interactions;
- input/output moderation and a safe failure experience;
- report/escalation path and parent-visible review controls;
- provider/model version, child-safety prompt, evals, incident log and change review;
- credential isolation and a narrow LEGO-only tool allowlist;
- a jurisdiction review for COPPA and other applicable child/privacy rules.

For a private household deployment this can be proportionate and simple, but it should still be explicit.

### Q11 — USD-native composition

**R-13 · P1 — define an LVP USD profile, not merely five guardrails.**

The proposed stack is shallow enough only if the allowed composition features are constrained. In v1 permit:

- references to published assets;
- a small, ordered sublayer stack;
- named variant selections;
- local overrides in a designated edit layer.

Forbid or defer inherits, specializes, payloads, relocates, sub-root references, arbitrary list editing and authoring into multiple edit targets. OpenUSD's own documentation makes clear that LIVERPS is a strength ordering across multiple arc types, not just “top layer wins.” A tiny profile, canonical layer order, `usdchecker`, and golden flatten tests make the complexity tractable.

**R-14 · P2 — separate physical from presentation layers.**

Snow made of bricks changes collision, connectivity and BOM; lighting does not. Do not put `base + snow + lighting + validator` into one undifferentiated layer model. Classify layers by effect:

- physical authored geometry/BOM;
- derived validation relationships/annotations;
- presentation/render-only state.

This keeps a stronger lighting opinion from accidentally participating in physical publishing logic.

### Q12 — Prim path as identity

**R-15 · P0 — add a stable GUID; never equate identity with prim path.**

Prim paths are namespace addresses. Renaming a prim, moving it beneath another submodel, splitting a submodel, or creating a local instance changes that address. USD can translate relationship targets through composition and provides relocates for some namespace edits, but neither capability makes the path a durable domain identifier for git merges, audit history, Studio round trips, or external provenance.

Each placed brick needs:

- immutable `brick:id` (UUIDv7/ULID or content-independent random GUID);
- mutable USD prim path chosen for readability;
- `asset:id` for the defining asset;
- `instance:id` when a referenced asset is instantiated in an assembly;
- export-occurrence identity in the flatten manifest.

The merge driver keys on `brick:id`; path change is a rename/reparent operation. Duplicate IDs in a composed stage are a blocking validation error. `brick:mates` relationships may use paths as USD requires, but the validator also records endpoint GUIDs so relationships can be rebuilt after namespace edits.

### Q13 — Licensing

**R-16 · P1 — distinguish the LDraw parts-library licence from model-level licences and split the publication cases.**

The package must not collapse the licence of the LDraw parts library, the LDraw website, and individual OMR model artifacts into one generic “LDraw CC BY” label. LDraw's legal page states that the CA-approved **parts library** is CC BY 2.0; website content is separately CC BY 4.0. Record the licence and attribution of each OMR fixture from that artifact's own metadata. Model files that only reference official parts are treated differently from converted/copied part geometry. A generated part-USD cache that embeds converted LDraw geometry is therefore a derivative distribution concern, whereas a private model that merely references locally installed parts is materially simpler.

The LDCad Shadow Library is CC BY-SA 4.0. If connector records are copied or adapted into a distributed cache/catalog, assume attribution and share-alike review is required; do not merge that data invisibly into a differently licensed code package.

Recommended packaging:

- keep LDraw-derived geometry cache local/regenerable and outside the content repo;
- keep LDCad-derived connector data in a separately attributed data layer with source commit and licence;
- publish model references and your own annotations where possible, not converted part meshes;
- add an attribution/provenance manifest to every representation;
- obtain a targeted licence review before any public or commercial distribution.

This is architectural licence hygiene, not legal advice.

### Q14 — Versions and `@latest`

**R-17 · P1 — branch-prefixed semantic versions should not become published identity.**

`v004-play-eli` creates promotion and collision problems: renumbering breaks references, while retaining it makes canonical ordering branch-dependent. Use:

- immutable draft/revision IDs on play branches, preferably content-addressed plus author/request metadata;
- a canonical monotonic published version allocated only by a serialized merge/publish queue on `staging` or `main`;
- an immutable asset/version ID independent of the display label `v004`;
- `@latest` as a query/UI convenience only. Proposal creation resolves it and writes a pinned version plus lock entry.

The rebuildable catalog may index allocation state, but a committed `catalog.sqlite` should not be the sole allocator under concurrent branches.

### Q15 — Spike ordering

**R-18 · P1 — sequence spikes by irreversible decision, not component number.**

Before broad scaffolding:

1. Reconcile the data-contract amendments from R-01, R-04, R-15, R-19 and R-20.
2. **S7** — prove the minimum USD runtime matrix and choose native arm64 versus emulated/container fallback.
3. **S1** — prove the supported Studio round trip and record normalization behavior.
4. **S2** — measure connector coverage and define the connector schema against real fixtures.

Then build only a thin vertical spike harness and continue:

5. **S6** — exercise the restricted USD profile, flatten manifest, explicit edit scope and assembly-local overlay ingest. Do not require automatic source attribution.
6. **S3** — compare voxel/proxy/exact collision after connector/contact exceptions exist.
7. **S4** — validate Blender projection, scale, instancing and render performance against the now-stable canonical model.
8. **S5** — validate the Studio oracle after S1 has fixed GUI/file behavior and S2/S3 have produced adjudicable fixtures.

S1, S2 and S7 may run in parallel. “Before scaffolding anything” should mean before committing production package boundaries, not before writing disposable spike code.

## Unasked findings

### Flattening destroys source authorship

**R-19 · P0 — revise the S6 success criterion and ingest contract.**

“Flatten → Studio → hand edit → ingest as a diff on the right asset” is not generally decidable from the edited flat model. Flattening erases composition arcs; Studio may discard custom metadata; identical assets may be instanced more than once; and a newly added brick has no source asset at all.

Every flat export needs a sidecar manifest mapping each occurrence to `{brick:id, asset:id, source_version, instance:id, source_prim_path, export_transform}`. On ingest:

- edits to an unambiguously matched occurrence become an **assembly-local override** by default;
- additions become assembly-local placements;
- deletion/move/recolor of a source brick may be proposed for source promotion only when the user entered an explicit “edit bakery source” scope and provenance still matches;
- ambiguity becomes a DecisionPoint;
- editing one instance never silently mutates every instance.

S6 passes when the system preserves provenance and refuses ambiguous source mutation—not when it guesses a source.

### Correspondence frontmatter is currently invalid in the supplied rendering

**R-20 · P0 — adopt and validate the extended schema.**

The new `argument` form is valuable: it records the argumentative movement of the memo, which survives better across provider/session boundaries than a terse abstract. But the exemplar's frontmatter has collapsed keys after `repos`, and the one-line argument obscures YAML boundaries.

Adopt the contract in Part D below and add a CI/preflight parser. A memo with invalid frontmatter may still be read by a human, but it may not enter the automated correspondence ledger or be used as a work order.

### Git/worktree concurrency

**R-21 · P1 — branches alone do not isolate concurrent filesystem writers.**

If the harness serves several users from one checkout, switching branches changes the working tree underneath other jobs. Use one git worktree per active family branch or a service-managed bare repo with ephemeral worktrees per proposal. Studio drop-folder ingest must bind each file to a branch/session explicitly.

### Undo semantics

**R-22 · P1 — define undo as a new revert commit.**

“Every commit is undoable” becomes unsafe after intervening edits. `build.undo(commit_id)` should calculate and preview a semantic revert against the current head, detect conflicts by stable ID, validate the result, and append a new commit. It should never rewrite history or blindly apply an old inverse diff.

### Derived catalog and cache truth

**R-23 · P2 — keep rebuildable indexes and blobs out of authority paths.**

If `catalog.sqlite` is rebuildable, CI should prove it can be regenerated from published manifests and should reject drift. Missing blobs must produce deterministic regeneration or an explicit unavailable representation, never missing canonical content. Blob garbage collection needs reachability from manifests and a retention window.

### Worker filesystem and credentials

**R-24 · P1 — narrow the Blender worker boundary.**

A container mounting all of `~/Documents/play-well` read-write gives render/import code more authority than it needs. Mount the proposal worktree read-only plus a job-specific output directory; let the harness/brickcore service perform validated commits. Do not put BrickLink, GitHub or provider credentials in the worker environment.

### Core versus Blender wording

**R-25 · P2 — say that agents build through brickcore and inspect through Blender.**

The package alternates between “the agent builds in Blender” and “BuildDoc/brickcore is truth; Blender is an adapter.” The second is the safer architecture. Domain operations should mutate the plain model through brickcore; Blender projects, previews and supports James's expert dev workflow. This wording prevents later code from accidentally making scene state authoritative.

### Machine-readable severity ledger

**R-26 · P2 — put findings in structured metadata or a companion ledger.**

`finding_ids: "R-01 through R-24"` is readable but not queryable. Once the reconciliation schema stabilizes, add a compact structured `findings` list or generated ledger containing ID, question, severity, owner and disposition. Keep the prose below authoritative for rationale.

## C. Disagreements worth registering

These are positions I would argue in reconciliation without calling the current choice a defect:

1. **Studio is not ground truth.** It is the target compatibility implementation and a valuable calibration oracle. Adjudicated fixtures plus explicit project rules are the truth for this pipeline.
2. **OpenUSD from day one is reasonable here.** For a one-family utility it would normally be excessive; for a project explicitly intended to teach USD and support rich annotations, it is justified if the LVP USD profile is narrow.
3. **Exact mating is preferable to tolerance mating.** Tolerance belongs at import/canonicalization. Allowing tolerance in the final mate predicate would make results depend on ordering and epsilon choices.
4. **Creative blast radius can remain unlimited.** Operational blast radius cannot. A child may recolor the entire village; that job still gets bounded tokens, runtime, storage and tools.
5. **`unknown` should be visible, not contagious.** Conservative uncertainty is correct, but validation must report the exact unsupported claim and coverage boundary.
6. **A semantic merge driver is not the first milestone.** Stable IDs and a three-way diff model should land first; automatic merge can follow once real branch conflicts have been collected as fixtures.

## D. Correspondence frontmatter contract

The expanded frontmatter should become the required house style for substantive inter-agent, inter-provider and inter-session memos in the LEGO Village Pipeline.

### Required top-level fields

```yaml
memo: LEGO-PIPE-NNN
revision: R0
status: draft | for_review | for_reconciliation | accepted | superseded
memo_type: handoff | review_response | decision | work_order | findings
title: "..."
date: YYYY-MM-DD
from: "provider/agent plus human attribution"
to: ["..."]
thread: "stable conversation/workstream name"
cluster: play-well
repos: ["owner/repo"]
tags: ["..."]
argument: >-
  A grammatical narrative of the reasoning movement: the premises encountered,
  turns made, conflicts resolved, conclusions reached, and work now requested.
parts:
  A: "..."
provenance:
  source_artifacts: []
  method: "..."
```

### Conditional fields

Use `in_reply_to`, `supersedes`, `adrs_reviewed`, `adrs_proposed`, `finding_ids`, `review_scale`, `disposition_requested`, `primary_sources`, and `generated_from` when applicable. Do not emit empty ornamental structures merely to satisfy a template; use `null` only where absence itself is important.

### `argument` semantics

The `argument` field is not a summary, table of contents, or list of decisions. It should:

- use a YAML folded block (`>-`) rather than an unbounded single line;
- be written as a compact narrative, conventionally beginning “In which …”;
- preserve causal sequence—what was found, what changed, why, and what follows;
- name material dissent and constraints;
- avoid implementation detail already recoverable from `parts` or tags.

This memo uses that form as the response example.

### Validation rule

Before a memo is handed to another provider or accepted as a work order:

1. parse the frontmatter as YAML;
2. validate required keys and types against a versioned schema;
3. require globally unique `(memo, revision)`;
4. verify `in_reply_to`/`supersedes` references when the referenced memo is present;
5. verify every finding ID used in the body is declared or generated into the ledger;
6. reject tabs, collapsed top-level keys, duplicate keys and scalar/list type drift.

Suggested schema identifier for the first implementation: `correspondence_schema: lego-pipe-memo/v1`. Add it to both LEGO-PIPE-011-R1 and this memo during reconciliation.

## Sources checked

- [OpenUSD Terms and Concepts](https://openusd.org/release/glossary.html) — composition arcs, LIVERPS, relationships, asset identity metadata and relocates.
- [LDraw.org Legal Info](https://www.ldraw.org/legal-info) — parts-library CC BY 2.0 terms and the distinction between referenced models and converted part geometry.
- [LDCad Shadow Library](https://github.com/RolandMelkert/LDCadShadowLibrary) — CC BY-SA 4.0 licence.
- [Anthropic guidelines for organizations serving minors](https://support.claude.com/en/articles/9307344-responsible-use-of-anthropic-s-models-guidelines-for-organizations-serving-minors) — technical measures, privacy/regulatory compliance and AI disclosure.

## Requested reconciliation outcome

Accept R-15, R-19 and R-20 before issuing any scaffold work order. Reconcile the P1 findings into the affected ADRs and spike exit criteria. Carry P2 findings into the issue ledger. Reissue the package as LEGO-PIPE-011-R1 with valid `lego-pipe-memo/v1` frontmatter, then send the amended work order to Claude Code.
