# mils-integrator — architecture

```
                      ┌──────────────── harvest (nightly / monthly) ────────────────┐
 feeds ─┐             │ feeds.py   omr.py   youtube.py   rebrickable.py   lego_bi.py │
 OMR ───┼──▶ fetcher ─┤  polite httpx · ETag/If-Modified-Since · robots · ≤1 rps    │
 YT ────┘             └────────────────────────┬────────────────────────────────────┘
                                               ▼
                                   corpus/store.py  (SQLite: sources, documents,
                                   fetch_log, models, analyses, patterns, examples)
                                   blobs/<sha256>   (raw bodies, MPDs, PDFs, captions)
                                               │
              ┌────────────────────────────────┼─────────────────────────────┐
              ▼                                ▼                             ▼
   ldraw/parser.py ──▶ geometry/footprint.py   patterns/extract.py      training/dataset.py
   (MPD flatten, AABB   (ground plane, 32×32    (keyword tagger now,     (analysis × scenario
    from library or      mask, contact/overhang, LLM extraction later →   → plan → validator
    bundled catalog)     bbox, height plates)   IntegrationPattern)       report → JSONL + RAG chunks)
                                               │
                                               ▼
                       planner/decisions.py ── forks raised to the human (with precedent per option)
                       planner/plan.py  ── rule-based candidates narrowed by answers (Plan schema)
                       planner/riser.py ── legolise riser under the footprint
                       planner/validate.py ── fit · stud alignment · height · perimeter clearance
                                               │
                                               ▼
                       harness/retrieve.py · harness/context.py · harness/evals.py
                       (BM25 → grounded context pack → grounding score → eval suite)
                                               ▼
                           cli.py (typer)  ·  tools.py (drafting-table tool surface)
```

## Modules

| Module | Responsibility | Deps |
|---|---|---|
| `mils/spec.py` | The standard as data: LDU constants, `MilsModule` (surface height, perimeter Technic positions, ID corners, CTM feature heights, rail/road variants as parameters), tolerance | stdlib |
| `ldraw/parser.py` | Parse `.ldr/.mpd`, resolve subfiles, flatten to placed parts with 4×4 transforms; compute AABBs recursively from a local LDraw library if present, else from `ldraw/catalog.py` | stdlib |
| `ldraw/catalog.py` | Bundled dimension/behaviour catalog for common parts (plates, bricks, tiles, slopes, baseplates, Technic, jumpers): footprint studs, height plates, studs-on-top, anti-studs-below | stdlib |
| `geometry/footprint.py` | `SetAnalysis`: foundation class, ground plane, footprint mask, contact/overhang/tile cells, bbox studs, height plates, submodels | numpy |
| `patterns/taxonomy.py` | `PatternType` (P1…P11), `IntegrationPattern`, `Evidence` (pydantic) | pydantic |
| `patterns/extract.py` | Offline keyword/regex tagger + prompt builder for LLM extraction into the schema | pydantic |
| `corpus/store.py` | SQLite schema + upserts + blob store + license/use-policy columns | stdlib |
| `harvest/fetch.py` | Polite fetcher (httpx), conditional GET, per-host rate limit, robots (protego if installed), retries | httpx |
| `harvest/feeds.py` | RSS/Atom discovery (stdlib XML; feedparser if installed) | stdlib |
| `harvest/omr.py` | OMR set index crawl → `.mpd` fetch → `models` rows | — |
| `harvest/youtube.py` | Channel RSS → `yt-dlp` captions (subprocess, optional) | — |
| `harvest/rebrickable.py` | CSV dumps (conditional) + API set/parts | — |
| `harvest/lego_bi.py` | Instruction PDF discovery via Brickset `getInstructions2` / slingshot search; personal-use storage | — |
| `planner/decisions.py` | `DecisionPoint`s (foundation, p4_method, level, rotation) with options → patterns → precedent queries; answers in `Scenario.decisions` | pydantic |
| `planner/plan.py` | `Plan` schema; `RulePlanner.decisions()` + `candidates()` narrowed by answers | pydantic |
| `planner/riser.py` | Greedy legolisation of the riser under a mask with interlocking layers; BOM | numpy |
| `planner/validate.py` | Validators returning a `ValidationReport` with per-check pass/fail and metrics | numpy |
| `training/dataset.py` | JSONL exemplar/eval writer (+ near-miss negatives), RAG chunker | — |
| `harness/retrieve.py` | BM25 (stdlib) over pattern records + licence-filtered chunks; domain tokenizer/synonyms; boosts as tuning knobs | stdlib |
| `harness/context.py` | grounded context pack: spec → analysis → decisions with precedents → validated plans with cited rationale → exemplars; `grounding()` self-check | — |
| `harness/evals.py` | eval cases (decisions open, retrieval recall per option, plan invariants, grounding floor); `mils evals` | — |
| `cli.py` | `mils harvest|seed|tag|analyze|plan|context|evals|dataset|status|export` | typer |
| `tools.py` | JSON-in/JSON-out functions for the drafting table / MCP wrapper | — |

## Coordinate conventions
- LDraw: right-handed, **−Y up**, LDU. We keep LDraw Y internally and expose `height_plates` etc. as positive-up integers.
- Module grid: cells `(x, z)` in `0..31`, x along LDraw +X, z along LDraw +Z; cell `(0,0)` is the module's min-X/min-Z corner. Cell centre = `((x+0.5)·20, (z+0.5)·20)` LDU from the module origin.
- Heights in plates are integers above **baseplate top** unless the field name says `above_table`.

## Schedules
- `make nightly`: feeds → new docs → tagger; OMR index delta; YouTube RSS; write `status.json`.
- `make monthly`: LDraw `complete.zip` (conditional), Rebrickable CSVs, re-analyse models whose parts catalog coverage improved.
- `.github/workflows/harvest.yml` runs both on cron and commits `corpus.db` stats (never the blobs) to the repo; blobs go to a release asset or object storage.
# ADR 0001 — The corpus feeds an executable spec and a RAG harness, not model weights

**Status:** accepted · 2026-09-16 · amended R1 (same day) after review

## Context
The goal is a tool that adapts a documented official set onto a MILS module. Prior work (docs/research/04) shows learned brick generators need 50k–300k examples for 82–98 % validity on free-form shapes and still produce physically-valid-but-wrong outputs. Generative modelling is not the problem; giving an agent exactly the right grounded context and the right questions is.

## Decision
1. Encode the MILS standard as executable constraints and validators (deterministic).
2. Harvest builder documentation into a structured, cited pattern corpus and serve it through a tunable retrieval harness (BM25 first, inspectable; embeddings only as a second scorer later).
3. Assemble a grounded context pack per turn whose every rationale line cites a spec constant or a pattern record; score grounding as a harness validator.
4. Maintain a harness eval suite (decisions raised, precedent retrieval, plan invariants, grounding floor) and tune retrieval knobs against it. The JSONL example set is the exemplar pool and regression suite; accepted builder turns become gold exemplars.
5. Fine-tuning is not a planned phase. (R0 listed it as an optional phase 4; withdrawn.)

## Consequences
- Correctness lives in `mils/spec.py`, `planner/validate.py` and `harness/evals.py`; those get the tests.
- Every harvested document and every retrieved hit carries licence/use-policy so the pack can be filtered at query time.
- Retrieval quality is a number in CI, not an impression.
# ADR 0002 — SQLite state + content-addressed blobs; DuckDB/Parquet as optional analytics export

**Status:** accepted · 2026-09-16

## Context
Persistence must survive interrupted runs, run on a laptop, a Raspberry Pi concierge, or GitHub Actions, and need zero services. The F1 project uses DuckDB for analytics; that is the right tool for querying, not for crawl state.

## Decision
- `corpus.db` (SQLite, WAL) holds sources, fetch_log (url, etag, last_modified, sha256, status), documents, models, analyses, patterns, examples.
- Raw bodies live under `blobs/<sha256[:2]>/<sha256>` — dedup by content, never re-fetched when unchanged (conditional GET first, hash second).
- `mils export --parquet` writes tables to Parquet for DuckDB/pandas; DuckDB is an optional extra.

## Consequences
- Stdlib-only persistence; the package installs with httpx + pydantic + numpy + typer.
- Blobs are not committed to git (size, licensing); CI commits only stats.
# ADR 0003 — Set geometry as a stud-grid footprint analysis, not a mesh

**Status:** accepted · 2026-09-16

## Context
MILS integration is decided on the stud grid (which cells contact, which overhang, ground plane, height in plates) plus perimeter clearance. Meshes and full connectivity graphs (BrickNet, LTRON) are heavier than the decision needs and their data is by-request or GPL.

## Decision
- Parse LDraw ourselves (stdlib), flatten MPD submodels with composed 4×4 transforms.
- Part extents come from the local LDraw library when present (recursive AABB over line types 2/3/4 and subfile refs, cached), else from a bundled catalog of common parts with stud/anti-stud semantics.
- The analysis product is `SetAnalysis`: foundation class, ground plane Y, 32×32-aligned masks (contact, overhang, tile/no-connect), bbox in studs, height in plates, per-submodel breakdown, plus catalog-coverage ratio so uncertainty is explicit.
- Optional later: LDCad shadow-library snaps (CC BY-SA) for exact stud/anti-stud points.

## Consequences
- Works offline today; precision improves monotonically as the parts library / snap data are installed.
- Rotations other than multiples of 90° are detected and reported, not modelled.
# ADR 0004 — Eleven-pattern integration taxonomy, versioned, with evidence spans

**Status:** accepted · 2026-09-16

## Context
Builder documentation is unstructured (blogs, transcripts, forum threads). The drafting table needs named, citable moves with numbers.

## Decision
`PatternType` v1 = P1 foundation-class, P2 riser, P3 pocket, P4 baseplate-strip/shim, P5 footprint-fit, P6 seam-blend, P7 winter-surface, P8 road-continuity, P9 rail, P10 lighting-chase, P11 parts-vocabulary (docs/research/02). Every `IntegrationPattern` record carries: pattern type, problem, move (with `delta_plates`, `offset_studs`, `slope_plates_per_stud` where applicable), parts (design ids), `Evidence[]` (document id, quote span, url), confidence, extractor (keyword|llm|human), reviewed flag. Taxonomy changes bump `taxonomy_version`; records are never rewritten in place.

## Consequences
- Extraction can start with a keyword tagger and be upgraded to an LLM pass without schema change.
- A human review queue is a query (`reviewed = 0 ORDER BY confidence`).
# ADR 0005 — Decision points are first-class planner output; the agent asks, it does not guess

**Status:** accepted · 2026-09-16

## Context
R0 computed foundation class (plate-built vs baseplate-built) from the LDraw and planned from it silently. Review objection: that is a fork a builder decides by looking at the set and the layout, and the agent should ask — with precedents attached — rather than resolve it. The same holds for flush-vs-proud, the P4 method for baseplate-built sets, and rotation when both fit.

## Decision
- `planner/decisions.py` defines `DecisionPoint` (id, question, options with pattern references and a precedent query, default, why_now, blocking, evidence from the analysis).
- `RulePlanner.decisions(analysis)` returns the open points under the current answers; `Scenario.decisions` carries the answers; `candidates()` narrows by them. A human answer always overrides the analysis (validators honour it too).
- While a blocking decision is open, candidates are per-option previews. `tools.plan` returns `{decisions_open, blocking, candidates}` and the drafting table must render the decision before presenting a plan as final.
- The harness attaches retrieved precedent to every option (`harness/context.py`), and the evals assert which decisions must be open for which inputs.
- Foundation is always asked (the analysis proposes, with confidence and evidence), because everything downstream depends on it. Project constraint: MILS modules themselves are always baseplate-founded, so the question is only ever about the set.

## Consequences
- The UI contract mirrors ThemeDiffRow: nothing auto-applies; the builder accepts a fork and the plan follows.
- Accepted answers + plans are the gold exemplar stream for the harness.
- Decision ids are stable API (`foundation`, `p4_method`, `level`, `rotation`); adding one is an eval change.
# LEGO-PIPE-009-R1 — mils-integrator handoff memo

**From:** Claude (Fable 5.1, Cowork) · **To:** ChatGPT (research/review) + Claude Code (repo) · **Date:** 2026-09-16 · **Cluster:** play-well / ojfbot/lego-village-pipeline

## What this is
A supporting utility for the drafting table: a persistent reference corpus + executable MILS spec + validators + decision points + a tuned RAG harness (BM25, grounded context pack, evals) that turns a documented official set (LDraw from the OMR) into *questions for the builder with precedents attached* and, once answered, ranked validated integration plans on 32×32 MILS modules with the riser exported as LDraw. R1 (after review): decision points are first-class output; the target is harness quality measured by evals, not a fine-tune. Plus a second utility, `roofsnow`, built on the same precedent-study pattern (organic snow on roof lines as a reviewable per-part-role diff — the ThemeDiffRow contract).

## Decisions taken (ADRs 0001–0005)
1. Corpus feeds an executable spec and a RAG harness with evals, not weights. No generative brick model; fine-tuning is not a planned phase.
5. Decision points (foundation, p4_method, level, rotation) are first-class planner output; the agent asks, it does not guess; a human answer overrides the analysis. Project constraint: MILS modules are always baseplate-founded, so "foundation" is only ever about the set.
2. SQLite + content-addressed blobs; DuckDB/Parquet optional.
3. Geometry = stud-grid footprint analysis, not meshes; exact extents from the LDraw library when present.
4. Eleven-pattern taxonomy v1 with evidence spans; records append-only.

## Numbers that must not drift
Surface = baseplate + 4 plates (36 LDU above table). Technic 1×4 at studs 3–6 and 27–30 on every edge, 2×2 ID corners, holes at 70/90/110/530/550/570 LDU. Edge tolerance ±1 plate. Paved road 5 plates (+1 only), river water 2 plates, path 4 wide, road 16 wide centred. Rail: 4-8-8-8-4, ballast 2 plates (L-Gauge) → rail top 9 plates. Hill 15 plates, mountain 48 plates above ground.

## Asks
- **Claude Code:** land `mils-integrator/` in the repo (subdir or sibling package), run `mils harvest nightly --sets 10254,10259,10267,10275,10293,10308,10325` from a machine with network, commit `status.json`, open an issue per `[unverified]` item in docs/research/03.
- **Drafting table (Claude Design):** render `decisions_open` as cards with precedent chips before any plan is shown as final; log accepted answers + plans as gold exemplars (they feed `mils evals`).
- **ChatGPT review:** challenge (a) the paved-road lateral placement reading (centred vs half-edge), (b) the slope-facing convention in `roofsnow/analyze.py::_facing`, (c) the lever bands in `roofsnow/typology.py::BANDS` — propose bands from the official Winter Village roofs once OMR files are in.
- **James:** fill YouTube `channel_id`s; decide whether `roofsnow` stays here or becomes its own fleet member once a third precedent-study utility appears.

## Interfaces exposed (API-esque, no hosts)
`tools.analyze_ldraw`, `tools.decisions`, `tools.plan` → `{decisions_open, blocking, candidates}`, `tools.context_pack` → grounded pack + prompt + grounding scores, `tools.validate_plan`, `tools.riser_ldraw`, `tools.patterns_search`, `tools.spec`; `roofsnow.analyze_roof / generate / validate_snow / examples_for`. All JSON in/out. Decision ids are stable API.
