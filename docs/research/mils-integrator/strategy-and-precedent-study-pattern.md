# mils-integrator — strategy (R1, 2026-09-16)

*Supporting utility for the Lego Village Pipeline drafting table. play-well cluster, @ojfbot fleet. R1 supersedes R0 after review: decision points are first-class, the target is a well-tuned RAG harness with evals, not a fine-tune fallback.*

## 1. The problem, stated as geometry — and as questions

"Integrate an official set into MILS" decomposes into a few discrete quantities and a few forks a builder decides by looking:

1. **Foundation class** — plate-built (anti-studs, ground floor 1–2 plates above its base) or baseplate-built (no clutch, ½ plate thin). The analysis *proposes* this from the LDraw; the builder *confirms* it. Every Winter Village building is plate-built; Modulars and City are baseplate-built; some sets are mixed. This is the first decision point, not a computed value.
2. **Ground plane and contact mask** — computed: which 32×32 cells touch, overhang, or are tiled.
3. **Δ height** — an integer number of plates between where the set's ground floor wants to be and the MILS surface (baseplate + 4 plates = 36 LDU above the table), ±1 plate at module *edges only*.
4. **Placement** — integer stud offset and rotation ∈ {0, 90, 180, 270}; 45° is a pattern (turntable), not a rotation.
5. **Level** — flush (pocket the module under the footprint) or proud (stand on the surface, dress the seam). Both are legal for most sets; this is an aesthetic decision point with precedents on each side.
6. **P4 method** when baseplate-built — strip and rebuild on plates, shim ½ plate, or swap a third-party anti-stud baseplate. Decision point.
7. **Seam treatment and edge features** — stepped skirt at 1 plate/stud, long slope at 1 plate/2 studs, pocket rim, curved-snow; road/river/rail continuity at the heights the standard fixes.

Master builders solve this every winter and write it down (brief 02 catalogs eleven recurring patterns). Our project constraint: MILS modules are always baseplate-founded — the canonical stack — so "foundation" is only ever a question about the *set*.

## 2. Thesis: an extremely well-tuned RAG harness, with the human at the forks

Generative brick modelling is out of scope (prior work needs 50k–300k examples for 82–98 % validity and still produces physically-valid-but-wrong output — brief 04). What we want is a harness that, for one integration turn, gives the drafting-table agent exactly the right context, grounded and cited, and asks the builder the right questions rather than guessing. The corpus serves that harness four ways:

1. **Executable spec.** The MILS numbers become a typed module model (`mils.spec`) and validators (`planner.validate`). Deterministic; this is where correctness lives.
2. **Decision points with precedents.** `planner.decisions` raises the forks above as `DecisionPoint`s: question, options, the pattern each option invokes, the default it would take if forced, why it is asking now. The harness attaches retrieved precedent to every option. Answers narrow the candidates; unanswered blocking decisions mean candidates are previews per option, never a verdict.
3. **Grounded context pack.** `harness.context` assembles, in a fixed order: binding spec constants → set analysis → open decisions with precedents → validated candidate plans whose every rationale line cites a spec constant or a pattern record → nearest accepted exemplars. `grounding()` scores the pack; a pack that cannot cite fails the harness's own validator.
4. **Evals, not weights.** `harness.evals` pins, per (fixture, scenario, answers): which decisions must be open, which pattern types retrieval must surface for which option, top-plan invariants, and a grounding floor. Retrieval knobs (BM25 k1/b, chunk size, pattern/reviewed boosts, domain synonyms) are tuned against these. The JSONL example set (`training/dataset.py`) is the exemplar pool and regression suite for the harness — and the builder's accepted plans become gold exemplars — not a fine-tuning corpus.

## 3. What "sustainable and persistent" means here

- **Incremental, resumable, polite.** Feeds/APIs/CDN first; conditional requests (ETag/Last-Modified); content-hash dedup; ≤1 req/s per host; robots honoured; descriptive UA. State in one SQLite file, raw blobs by hash. A run that dies mid-way resumes without re-fetching.
- **Licensing is a first-class column** on documents and on every retrieved hit, so the context pack can be filtered by use policy at query time. OMR = CC BY 4.0. LEGO PDFs = personal use, never redistribute. Reddit = excluded. Rebrickable MOCs = metadata only.
- **Two clocks.** Nightly discovery (feeds, OMR index, YouTube RSS) + monthly heavy refresh (LDraw parts library, Rebrickable CSVs). Both `make` targets and one GitHub Actions workflow; evals run after every harvest so a corpus change that degrades retrieval is caught.
- **Fleet-shaped.** Northstar `northstar.json`, LEGO-PIPE handoff memo, ADRs, JSON tool surface for the drafting table (`analyze_ldraw`, `decisions`, `plan`, `context_pack`, `validate_plan`, `riser_ldraw`, `patterns_search`, `spec`).

## 4. Phasing

| Phase | Outcome | Evidence of done |
|---|---|---|
| 0 (this delivery) | Spec model, LDraw parser + footprint analysis, taxonomy P1–P11, harvesters with state, decision points, rule planner + validators, riser legoliser, BM25 harness + context pack + grounding, evals, seed corpus from the research briefs | 23 tests green; 5/5 harness evals green on the seeded corpus; fails honestly on an empty corpus |
| 1 | Real corpus: OMR crawl for Winter Village / Creator houses / Modulars; LDraw library for exact extents; feeds + YouTube transcripts flowing; LLM extraction pass over harvested docs → reviewed pattern records | ≥100 analyses; ≥200 pattern records; evals extended per harvested precedent; retrieval recall on eval queries ≥0.9 |
| 2 | Drafting-table integration: decision points rendered as cards with precedent chips; plans previewed per option; accepted plans logged as gold exemplars; ThemeDiffRow-style accept/skip for seams | gold ≥50; grounding ≥0.95 on gold turns |
| 3 | Harness tuning loop: eval suite grows from every accepted/rejected turn; reranker over BM25 (optional embeddings as a second scorer) | eval pass rate tracked per harvest in CI |

## 5. Non-goals
Generative brick modelling; fine-tuning as a planned phase; scraping BrickLink HTML; redistributing instruction PDFs; Reddit; anything that requires Cloudflare bypass; resolving a decision point without the builder.
# The precedent-study pattern (abstracted from mils-integrator)

*How to turn "master builders solve this and document it" into a retrieval-grounded, validatable procedural utility with the human at the forks. Written 2026-09-16 after the MILS-integration build; first re-application: snow on roofs.*

## The shape

Every one of these utilities has the same five parts. Naming them keeps agents honest about which part they are touching.

1. **Typology decomposition.** Break the design problem into sub-typologies small enough that each has a finite, nameable move set. MILS: foundation class × footprint fit × seam × edge feature. Roof snow: roof-line type (gable, hip, shed, gambrel, dormer, flat/parapet, stepped) × snow pattern type (blanket, cornice lip, ridge cap, wind drift, melt patch, valley fill, icicle line). The classification is never neutral — it decides what the model can express — so it is versioned (`taxonomy_version`) and records are never rewritten in place.
2. **Precedent corpus.** Two kinds of precedent, kept apart: **known-goods** (official sets — how LEGO's designers did it, geometry available as LDraw under CC BY 4.0) and **builder documentation** (blogs, transcripts, MOCs — techniques with numbers, licensed for private research/RAG). Harvest is incremental, polite, licence-tagged.
3. **Executable spec + validators.** The numbers and rules become code before anything is learned. Validators return graded checks, not booleans, so rejected outputs are still data.
4. **Levers with known-good bands.** Each sub-typology exposes a small set of procedural levers (integers/enums/0–1 floats). Precedent analysis yields the *band* each lever sits in for known-goods; an agent adjusting levers inside the band produces novel-but-plausible output, outside it produces near-miss negatives for the reranker and anti-pattern retrieval.
5. **Decision points, then a reviewable diff — never auto-apply.** Forks a builder decides by looking (foundation class, flush vs proud, roof-line type, wind direction) are raised as `DecisionPoint`s with retrieved precedent per option; the agent asks, it does not guess (ADR 0005). Then the generator emits a diff per part role (recolor / add / remove with part id, colour, position, cost/availability hooks) that the drafting table renders as `ThemeDiffRow`s. "Snow is a policy" — the human accepts or skips each row; accepted rows become gold examples.

## Harness and dataset shape (identical across utilities)

The corpus is served by a tunable retrieval harness (BM25 over pattern records + chunks, licence-filtered), assembled into a grounded context pack (spec constants → analysis → open decisions with precedents → validated candidates with cited rationale → nearest accepted exemplars), and tuned against an eval suite (which decisions must be open, which pattern types retrieval must surface, output invariants, a grounding floor). The JSONL set `(analysis_json, levers_or_scenario_json) → output_json → validator_report` with `valid`, `gold`, `chosen_id`, `prompt`, `completion` is the exemplar pool and regression suite; negatives (levers out of band, structural mutations) are the rejected side of preference pairs for a reranker and anti-pattern retrieval. Not a fine-tuning corpus.

## Applying it to roof snow

| Part | MILS integration | Roof snow |
|---|---|---|
| Analysis (computed) | footprint mask, ground plane, base thickness | roof faces from slope/plate parts: orientation, pitch, top-Y, eave rows, ridge lines, valleys |
| Sub-typologies | P1…P11 | `RoofLineType` × `SnowPatternType` |
| Known-goods | OMR geometry of Winter Village sets; MILS spec numbers | how 10259/10267/10275/10325 dress roofs: white 1×1 quarter tiles at eaves, curved slopes as drifts, white cheese slopes, ridge tiles; colour policy (white 15, trans-clear for ice) |
| Levers | placement offset, rotation, pocket/riser plates, seam style | `coverage`, `drift_bias` (wind vector), `eave_lip_depth`, `ridge_cap`, `roughness`, `melt_patches`, `icicles`, `seed` |
| Validators | fit, reserved clearance, seam arithmetic, edge height | support (adds sit on a real top face), no-float, coverage within band, lip depth in band, colour policy, ops restricted to roof roles |
| Output | Plan (+ riser LDraw) | `SnowDiff`: list of `DiffOp` per part role (+ LDraw of added parts) |

## What "organic" means here

Organic ≠ random. The generator uses a seeded, smooth value-noise field over the roof-face cells, biased by a wind vector (drift accumulates on the lee face and against vertical obstructions such as chimneys/dormers), thresholded by `coverage`, and softened by `roughness`. Precedent bands constrain the result to what real winter-village roofs look like; the seed gives novelty. Every generated diff is scored, and the ones James accepts in the UI become gold — so the bands tighten around his taste over time rather than around a generic prior.
