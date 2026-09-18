# build-harness — storage & asset-versioning architecture (supersedes the "Infrastructure sketch" in LEGO-PIPE-010)

**Date:** 2026-09-17 · **Status:** proposed · **ADR:** 0012
**Question:** How do we version a LEGO village that is composed from reusable assets (parts → buildings → modules → layouts → seasons), edited by agents and family on branches, exported to Studio, and grown over years — and what do game/VFX studios already know about this?

## 1. What the problem actually is

Studios separate four things that a single git repo under `~/Documents` conflates:

| Concern | In our project | Studio equivalent |
|---|---|---|
| **Canonical scene data** (small, text, diffable) | LDraw MPD, manifests, layers, validation reports | USD layers, Unreal `.umap` (binary, hence locking) |
| **Derived / heavy data** (regenerable, binary) | `.io` exports, renders, `.blend` scenes, oracle screenshots, voxel caches | DerivedDataCache, textures, baked lighting — kept out of VCS or in LFS/Perforce |
| **Asset hierarchy & composition** (what references what, at which version) | village → modules → buildings → risers/snow layers → parts | USD composition arcs; AYON folder/product/version; Perforce streams |
| **Work vs publish** | a kid's branch vs the layout that's physically built | workfile (mutable, personal) vs published version (immutable, referenced by others) |

Two things make our case *easier* than a game studio's, and we should exploit them:

1. **Our canonical format is text and semantically diffable** (LDraw + the `DiffOp` model). Studios need file locking because `.uasset` can't merge. We don't — a custom merge driver over placements by uid can merge two branches that touched different parts.
2. **Every heavy artifact is regenerable** from the canonical data plus a library version. So the blob store is a cache with provenance, never a source of truth.

## 2. Patterns worth stealing, and the mapping

| Studio pattern | Source | What we adopt |
|---|---|---|
| **Work / publish split.** Artists edit workfiles; `publish` freezes an immutable, numbered version other scenes reference | AYON, ShotGrid, every VFX pipeline | Family branches are workfiles. `publish` is a harness action producing `bakery/model/v003`. Layouts reference published versions only, never branch heads |
| **Product / Version / Representation** | AYON | A *product* is one output type of an asset (`model`, `snow`, `bom`, `render`, `instructions`). Each version has ≥1 *representation* (`.mpd`, `.io`, `.png`, `.xml`). Same version, many formats |
| **Hero / latest pointer** | AYON "hero version" | `@latest` resolves to the newest published version. Layouts pin (`@v3`); play branches may float |
| **Composition by reference, not copy** | USD references/payloads | A module *references* a building at a version and places it with a transform. Editing the building doesn't silently change the module until it re-pins |
| **Layers = non-destructive opinions** | USD sublayers / layer stack, "strongest opinion wins" | roofsnow's `SnowDiff`, a recolor policy, a lighting pass are **layers** over a referenced base. Base stays pristine; layers are versioned products in their own right; flatten composes them |
| **Variants** | USD variant sets | `season: {summer, winter}`, `snow: {none, light, heavy}`, `lighting: {off, on}` as named variants on an asset interface, chosen at reference time |
| **Component vs assembly kinds** | USD model hierarchy (`kind`) | `component` = building, riser, tree, train (self-contained, referenceable). `assembly` = MILS module, layout, season. Components never contain components |
| **Asset interface layer** | USD "asset structure principles" | Each asset has a small `asset.yaml` front door: id, kind, variants, footprint/height hints, extents — readable without loading geometry (our `SetAnalysis` lives here) |
| **Asset resolver + stable URIs** | USD `ArResolver`, Perforce depot paths | `lvp://christmas/buildings/bakery/model@v3` resolved by a tiny resolver to git path + blob hash. Nothing hard-codes filesystem paths |
| **Content-addressed derived data** | DerivedDataCache, git-annex, DVC | Blobs stored by sha256, indexed by (asset, version, representation, library versions). Regenerate on miss |
| **Flatten / package for delivery** | `usdz`, cooked builds | Studio never sees the composition; it gets a flattened MPD/`.io` per published version, with a manifest mapping uids back |
| **Streams** (server-understood branch hierarchy) | Perforce | We don't need Perforce, but we adopt the *shape*: `main` (physical) ← `staging` (next order) ← `play/<user>` |
| **Never reuse a version number** | USD/AYON guidance | Versions are immutable; corrections are new versions |

Things we deliberately *don't* import: file locking (unnecessary with text canonical), Perforce itself, a full AYON server (overkill for one family; adopt the model, not the product), Omniverse/Nucleus as infrastructure (USD the format, yes; the NVIDIA platform, not now).

## 3. Proposed architecture

### 3.1 Repos (play-well cluster, Northstar)

| Repo | Contents | Why separate |
|---|---|---|
| `ojfbot/lego-village-pipeline` (exists) | Code: brickcore, brick_bench, studio-bridge, harness API, mils-integrator, roofsnow, resolver, CLI | Tools evolve independently of content; CI runs tests, not asset diffs |
| `ojfbot/play-well-library` (new) | **Canonical content:** assets (components, assemblies, layers), published version manifests, validation reports, golden set, the catalog index. Text only + LFS pointers for the few blobs worth pinning (thumbnails) | Content history should be readable without code churn; family branches live here; can be private forever |
| blob store (not a repo) | Derived representations by sha256: `.io`, renders, `.blend`, oracle screenshots, voxel caches | Regenerable; huge; never merged. Dev: a directory. Later: S3-compatible bucket, optionally lakeFS if we want branch-aware blobs |
| corpus (exists, mils-integrator) | Harvested precedent, SQLite + blobs | Separate lifecycle (ADR 0002) |

Studios split "engine/tools" from "content depot" for the same reasons.

### 3.2 Library layout (`play-well-library`)

```
library/
  assets/
    buildings/bakery/                 # kind: component
      asset.yaml                      # interface: id, kind, variants, footprint, height, tags, license
      work/                           # NOT published; branch-local edits land here
        model.mpd · manifest.json
      published/
        model/v001/  model.mpd · manifest.json · report.json · blobs.json (sha256 → representation)
        model/v002/ …
        snow/v001/   layer.json (DiffOps) · report.json          # a layer product
        bom/v002/    bom.json · wanted.xml
    modules/M03-bakery-corner/         # kind: assembly
      asset.yaml
      published/assembly/v004/
        assembly.json                 # references: [{ref: lvp://…/bakery/model@v2, xform, variants:{snow: heavy}},
                                      #              {ref: lvp://…/risers/bakery-riser@v1}, {layer: lvp://…/bakery/snow@v1}]
        flat/model.mpd                # flattened composition (cached, also a representation)
    layouts/christmas-2026/            # kind: assembly (top level)
      asset.yaml
      published/assembly/v009/ assembly.json · flat/ · bom/
  golden/                              # OMR known-goods + mutations (CC BY 4.0, attribution file)
  catalog.sqlite                       # index: assets, products, versions, representations, blob hashes, library versions (rebuildable from files)
```

- `work/` is what branches change. `published/**` is append-only on every branch and is the only thing a reference may point at.
- `assembly.json` is the composition document: references (asset URI @ version, transform on the stud lattice, variant selection), layers in strength order, and its own local placements. **A flat MPD is a derived representation of an assembly, not its source.**
- `manifest.json` per published model carries the uid map, lattice classes, provenance, and the library versions it was validated against (LDraw release, shadow-lib commit, Rebrickable dump, brickcore version). Reports are pinned to versions, so "was this ever valid, and under which rules" is always answerable.

### 3.3 URIs and the resolver

`lvp://<layout-or-collection>/<kind>/<asset>/<product>@<version|latest>[#representation]`

Examples: `lvp://christmas/buildings/bakery/model@v3`, `lvp://christmas/modules/M03/assembly@latest#flat.io`.
The resolver (in brickcore) maps a URI to a git path (canonical) or a blob hash (representation). Swapping `~/Documents` for S3 later changes the resolver, not the assets.

### 3.4 Branch model (the Perforce-streams shape in git)

| Branch | Meaning | Who writes |
|---|---|---|
| `main` | What is physically built / ordered. Layout versions here are the real world | dev merge only, full validator + BOM check |
| `staging` | Next order cycle | parent/dev |
| `play/<user>` | Personal worksite; unrestricted building | that user (via the harness) |
| `agent/<request-id>` | Ephemeral; one proposal | harness, deleted after accept/reject |

Merge driver: a brickcore-provided git merge driver for `model.mpd`/`manifest.json` that merges by uid (add/remove/move/recolor) and only conflicts when both sides touched the same uid. `published/**` never conflicts (append-only, version numbers allocated by the catalog with a branch prefix on play branches: `v004-play-eli` until promoted).

### 3.5 Publish pipeline (harness action)

1. Validate work/ (T0) → must have no `block`.
2. Allocate version; freeze `model.mpd` + `manifest.json` + `report.json` under `published/<product>/vNNN/`.
3. Generate representations (flat MPD, `.io`, renders, BOM) → blob store, record hashes in `blobs.json`.
4. Update `catalog.sqlite`; move `@latest`.
5. Assemblies that reference `@latest` get a "new version available" notice in the drafting table; pinned ones don't move.

### 3.6 Dev phase mapping (what actually runs on the Mac this month)

```
~/Documents/play-well/
  play-well-library/      # git clone; branches per user; LFS for thumbnails
  blobs/                  # sha256-addressed derived files (gitignored, regenerable)
  golden/                 # or inside the library repo; decide by size
docker: blender-worker mounts ~/Documents/play-well (rw); harness API reads/writes only through brickcore's resolver
```

Later: `play-well-library` on GitHub (private); blobs → S3-compatible bucket (or lakeFS on top of it if branch-aware blobs earn their keep); resolver config switches; family Macs/iPads reach the drafting table over the web and never touch the repo directly. Studio saves from family Macs arrive via an ingest drop folder → identity diff → commit on that user's play branch.

## 4. How to learn from the studios (concretely)

Rather than reading broadly, port three specific things:

1. **USD asset structure → our `asset.yaml` + `assembly.json`.** Read NVIDIA's *Principles of Scalable Asset Structure in OpenUSD* and the USD glossary entries for *composition arcs, layer stack, variant set, model hierarchy (kind), payload*. Then take one of the public USD reference assets (Pixar's Kitchen Set or the ALab set) and write down, per file, which of our concepts it corresponds to. The exercise is ~2 hours and settles the composition schema.
2. **AYON project anatomy → our catalog.** Read *Project Anatomy* and the glossary (folder / task / product / version / representation / hero). Our `catalog.sqlite` schema should be a strict subset of that model so the vocabulary is standard if we ever adopt a real pipeline manager.
3. **Perforce streams → our branch model.** Read the streams guide only for the *shape* (mainline, development, release; "flow" rules about which direction changes move). Encode the flow rules in the harness (play → staging → main; never sideways) instead of relying on convention.

Then one spike, **S6 composition round trip:** two published buildings + a riser + a snow layer + a `season` variant composed into a module, flattened, opened in Studio, edited by hand, ingested back as a diff on the right asset (not on the flattened module). If S6 works, the whole model works.

## 5. The one real fork: own composition schema vs real OpenUSD

| Option | For | Against |
|---|---|---|
| **A. Own schema now** (JSON `assembly.json` + LDraw leaves; USD *concepts*) — **recommended for phases 1–4** | Tiny; brickcore stays pure Python; family-readable; Studio only ever needs LDraw; nothing to install | We re-implement composition (references, layer strength, variants) ourselves, ~a few hundred lines; no ecosystem tooling |
| **B. Real OpenUSD as canonical** with a custom `Brick` schema (part id, colour, lattice class, connectors as attributes) | Blender imports USD natively; instancing, variants, layers, resolver all exist; industry-standard vocabulary; scales to enormous scenes | `pxr` dependency everywhere (Docker fine, Pi painful); Studio still needs a flattening exporter; USD's float transforms vs our integer lattice needs discipline; family-facing debugging gets harder; overkill for one village |
| C. Flat MPD only | Simplest | No reuse, no layers, no pinned versions — this is the `~/Documents` sketch we're replacing |

**Decision (James, 2026-09-17): B — OpenUSD-native from the start.** Rationale: the project has every USD composition concept naturally (references, layers, variants, kinds, instancing), so it is a good learning vehicle; the "rich annotation" ambition (connectivity, physics, lighting, provenance as schemas/relationships on prims) is exactly what USD is for; skills and tooling transfer across the fleet (asset-foundry). Option A is retained as the documented fallback if S7 fails.

### 5.1 Guardrails that keep B from becoming a tax

1. **USD is the composition + annotation layer; LDraw stays the leaf geometry and the Studio interchange.** A brick prim carries `brick:part`, `brick:color` (LDraw code), `brick:lattice`, an integer-snapped `xformOp:transform`, and `kind`. Part geometry is *not* authored per placement: a part-USD cache (`parts/3001.usd`, generated once from LDraw via ldr_tools/ImportLDraw, `instanceable`) is referenced by every placement. Flatten-to-LDraw walks the composed stage and emits MPD; this is the only Studio-facing exporter.
2. **brickcore's math stays numpy over a plain in-memory model.** `pxr` is confined to `brickcore.io.usd` (read stage → placements; write placements/layers → usda). Validators never call pxr. A flat-LDraw import path stays as the fallback, so CI and any box without `pxr` still validate.
3. **No schema plugin in phase 1.** Use namespaced custom attributes plus `assetInfo`/`customData` and `kind`. Promote to a codeless `Brick` API schema (plugInfo.json + generatedSchema.usda, no C++) at phase 3 once the attribute set has stopped moving. Runtime-registered schemas don't exist in USD today, so the plugin plumbing is unavoidable later; defer it.
4. **Connectivity as relationships.** Mates become `brick:mates` relationships between prims in a validator-written sublayer (never in the base layer), so the connection graph is queryable in `usdview` and diffable, and a human edit can't corrupt it.
5. **Text only:** `.usda` for everything canonical (diffable, git-mergeable by prim path); `.usdc` only as a derived representation in the blob store.

### 5.2 Known costs, priced

| Cost | Size | Mitigation |
|---|---|---|
| `usd-core` wheels: PyPI ships macOS universal2, Linux x86_64, Windows — **no arm64 Linux**, which is what "Docker on Apple Silicon" is | Real | Options: community arm64 wheels (V-Sekai builds 26.8 for py3.12–3.14), `--platform linux/amd64` under Rosetta (slower), or run brickcore natively on the Mac and keep only Blender in Docker. **Spike S7 decides.** |
| Blender doesn't expose `pxr` inside its Python; USD I/O goes through Blender's own importer plus `USDHook` callbacks | Medium | Blender imports the composed stage natively; `brick_bench` reads our attributes via `USDHook.on_import`. Composition/annotation work happens in brickcore, not in Blender's Python |
| Learning LIVRPS (layer/inherit/variant/reference/payload/specialize strength ordering) before designing layers | 1–2 weeks of evenings | Learn it on the S6 spike; the project's layers are shallow (base + snow + lighting + validator) |
| Float transforms vs integer lattice | Small | Snap on read, validate on write; store integers in `customData` as the authority |
| Family-facing debugging is one step further from LEGO | Small | The drafting table never shows USD; `usdview` is a dev tool |

### 5.3 Learning path (USD as the entrypoint)

- NVIDIA *Learn OpenUSD* modules (free): fundamentals → asset structure → composition. Do them against *our* assets, not the sample scenes.
- *USD Survival Guide* (Luca Scheller) for the Python API idioms brickcore will use.
- Pixar's Kitchen Set or ALab: read the file layout, map each file to our `component / assembly / layer`.
- Blender's USD import for immediate visual feedback on every composition experiment; `usdview` for inspecting the layer stack and resolved opinions.
- Spikes: **S6** composition round trip (now in USD) and **S7** `pxr` on the Mac + in Docker.

## ADR 0012 — Versioned asset library: work/publish split, composition by reference, layers, content-addressed derived data

**Status:** proposed · 2026-09-17
**Context:** A village is composed from reusable assets across years, edited by agents and family on branches, exported flat to Studio. A single git repo of MPDs (LEGO-PIPE-010 §Infrastructure sketch) can't express reuse, pinning, non-destructive layers, or "which layout is real". Game/VFX pipelines solved this with the work/publish split, immutable versions, composition arcs, and derived-data caches.
**Decision:**
1. Two repos: `lego-village-pipeline` (code) and `play-well-library` (canonical content, text). Derived representations live in a sha256 blob store outside git.
2. Assets have kinds (`component`, `assembly`, `layer`) and an interface file; assemblies compose by **reference at a pinned version** with a lattice transform and variant selection; layers are versioned `DiffOp` products applied in strength order; flattening is a derived representation.
3. `work/` is mutable and branch-local; `published/<product>/vNNN` is immutable and append-only; references may only target published versions. Versions are never reused.
4. Stable `lvp://` URIs resolved by brickcore; storage location is resolver config.
5. Branch flow `play/<user>` → `staging` → `main`; `main` = physical state; a uid-aware merge driver replaces file locking.
6. **OpenUSD is the canonical composition and annotation format** (`.usda`), with LDraw as leaf geometry and Studio interchange, per the guardrails in §5.1. The own-JSON schema (option A) is the documented fallback if S7 fails.
**Consequences:**
- `pxr` becomes a dependency of `brickcore.io.usd` (not of the validators); ADR 0007's "no Blender dependency" stands, and gains "no pxr in validators".
- The part-USD cache and the flatten-to-LDraw exporter are new phase-1 deliverables; `assembly.json` is dropped in favour of `assembly.usda`.
- Family branches work on `.usda` text; the merge driver operates on prim paths instead of uids (uid = prim path).
- roofsnow and mils-integrator outputs become first-class layer/component products instead of ad-hoc files.
- Every published version records the library versions it was validated under → reproducible verdicts.
- Publishing is a harness action with validation gates; play branches remain unrestricted (James's decision on roles stands).
- One extra spike (S6) before phase 2; `catalog.sqlite` schema and the merge driver are new phase-1 deliverables.

## Sources
OpenUSD, *Generating New Schema Classes* (codeless schemas) — https://openusd.org/release/tut_generating_new_schema.html · AOUSD forum, *Do you need a plugin for custom schema?* — https://forum.aousd.org/t/do-you-need-a-plugin-for-custom-schema/1617 · usd-core wheel coverage / arm64 community builds — https://github.com/V-Sekai-fire/repository-usd-core-wheels · Blender `USDHook` — https://docs.blender.org/api/current/bpy.types.USDHook.html · NVIDIA, *Principles of Scalable Asset Structure in OpenUSD* — https://docs.omniverse.nvidia.com/usd/latest/learn-openusd/independent/asset-structure-principles.html · OpenUSD glossary — https://openusd.org/release/glossary.html · AYON glossary (folder/product/version/representation/hero) — https://help.ayon.app/articles/3030530-ayon-glossary · AYON project anatomy — https://help.ayon.app/articles/3815114-project-anatomy · StraySpark, *Version Control for UE5 Teams: Git LFS vs Perforce vs Anchorpoint* — https://www.strayspark.studio/blog/version-control-ue5-git-lfs-perforce · lakeFS, *DVC vs Git-LFS vs Dolt vs lakeFS* — https://lakefs.io/blog/dvc-vs-git-vs-dolt-vs-lakefs/ · Blender USD import/export manual — https://docs.blender.org/manual/en/latest/files/import_export/usd.html

---

# Amendments R1 (2026-09-17, from CORR-LEGO-PIPE-013 reconciling LEGO-PIPE-012)

*Appended, never rewritten in place. Where an amendment conflicts with text above, the amendment wins.*

## ADR 0012 — Amended R1

**Identity (R-15).** `brick:id` (ULID) is identity; prim path is namespace. `asset:id`, `instance:id` and export-occurrence identity are carried as in ADR 0006-R1. The merge driver keys on `brick:id`. `brick:mates` relationships use paths as USD requires; the validator sublayer also records endpoint GUIDs so relationships survive namespace edits.

**LVP USD profile (R-13, R-14).** v1 permits: references to published assets; a small, ordered sublayer stack; named variant selections; local overrides in one designated edit layer. Deferred/forbidden: inherits, specializes, payloads, relocates, sub-root references, arbitrary list editing, multiple edit targets. Canonical layer order is fixed and linted; `usdchecker` and golden flatten tests run in CI. Layers are classified by effect — **physical** (authored geometry/BOM: base, snow-as-bricks, risers), **derived** (validator relationships/annotations), **presentation** (render-only: lighting, materials) — and publishing logic reads only physical layers.

**Flattened ingest (R-19).** Every flat export (MPD/`.io`) ships a sidecar manifest mapping each occurrence to `{brick:id, asset:id, source_version, instance:id, source_prim_path, export_transform}`. On ingest: edits to an unambiguously matched occurrence become an **assembly-local override** by default; additions become assembly-local placements; delete/move/recolor of a source brick may be *proposed* for source promotion only when the user entered an explicit "edit <asset> source" scope and provenance still matches; ambiguity becomes a `DecisionPoint`; editing one instance never silently mutates all instances. Publishing back into a referenced source is a deliberate promotion operation.

**Versions and `@latest` (R-17, R-09).** Play branches carry immutable, content-addressed draft/revision IDs with author and request metadata — no branch-prefixed semantic versions. Canonical monotonic published versions are allocated only by a serialized publish queue on `staging`/`main`; an immutable asset/version ID is independent of the display label `v004`. `@latest` is a query/UI convenience: proposal creation resolves it and writes a pinned version plus a lock entry. Every play branch has a baseline lock (source commit; resolved asset versions; LDraw/shadow/Rebrickable/validator versions; model-provider config), a "refresh from main" operation that previews a semantic three-way rebase, and a stale/degraded status when dependencies no longer reproduce. `catalog.sqlite` indexes allocation state but is never the sole allocator.

**Concurrency and authority paths (R-21, R-23, R-24).** One git worktree per active family branch, or a service-managed bare repo with ephemeral worktrees per proposal; Studio drop-folder ingest binds each file to a branch/session explicitly. CI proves `catalog.sqlite` regenerates from published manifests and rejects drift; missing blobs regenerate deterministically or surface as "representation unavailable", never as missing canonical content; blob GC is by reachability from manifests with a retention window. The Blender worker mounts the proposal worktree read-only plus a job output directory (ADR 0007-R1).

**Licensing (R-16, corrected).** The LDraw parts library is licensed **per part** — CC BY 2.0, dual CC BY 2.0+4.0, CC BY 4.0-only, or CC0 — and the part's `0 !LICENSE` header is authoritative; the part-USD cache generator records it per part and the attribution manifest per representation lists the distinct licences present. LDCad-derived connector data lives in a separately attributed data layer with source commit and licence (CC BY-SA 4.0), never merged invisibly into code. The geometry cache stays local and regenerable, outside the content repo; model references and our own annotations are what get published, not converted part meshes; a targeted licence review precedes any public or commercial distribution.

**Merge driver sequencing (C-6).** Phase 1 delivers stable IDs and a three-way diff model; automatic semantic merge follows once real branch conflicts exist as fixtures.

## Clarifications R2 (2026-09-17, ChatGPT confirmation of CORR-013 §D.3)

**ADR 0012 — licensing fields (R-16, final).** For every part in the part-USD cache and every attribution manifest, preserve: the raw `0 !LICENSE` header line; a normalised licence identifier (`CC-BY-2.0`, `CC-BY-2.0 AND CC-BY-4.0`, `CC-BY-4.0`, `CC0-1.0`); the source library version (LDraw release id, shadow-library commit); and the part file hash. A part with a missing or ambiguous licence **fails closed for distribution** (the representation may be built locally but is marked `distribution: blocked`). OMR model licensing is tracked separately per model artifact from that artifact's own metadata and is never inferred from the parts it references.
