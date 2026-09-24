# Brickcrafts and the Brick Builder Software Stack — Play-Well evidence extension

**Date:** 2026-09-20 · **Cluster:** Play-Well / `ojfbot/lego-village-pipeline` · **Status:** research, pre-ADR
**Seed:** uploaded PDF, *Brickcrafts and the Brick Builder Software Stack* (`sha256:37ab964f5e25eed3ca231c96ceb69a8a562517497607298a141f536caea5d1a9`)
**Provenance:** requested in ChatGPT conversation `6ab0a117-acb4-83ea-acbe-9e00ce941d4c`; sources re-checked against primary papers, official repositories, specifications, product documentation, and the repository's current governing correspondence.
**Scope:** this document extends and audits the seed; it does not authorize implementation, supersede correspondence, or amend an ADR.

## Evidence labels

- **[verified: external]** — supported by a linked primary paper, official project/repository, specification, or product documentation.
- **[verified: repository]** — supported by current Play-Well correspondence, ADR material, or repository state.
- **[inference: Play-Well]** — an architectural or research recommendation derived from verified evidence; not a decided design.
- **[unverified/open]** — not established by the available evidence, or dependent on a future test, licence review, or human decision.

Labels apply to the complete bullet or table row in which they occur. A linked source may establish only the factual premise; the consequence for Play-Well remains an inference when labelled as such.

## 1. Bottom line

1. **[unverified/open] The public evidence does not establish Brickcrafts' exact software stack.** The seed's creator-specific reconstruction—Studio, custom scripting, an internal parts library, render tools, or hand-authored mechanisms—is a plausible hypothesis, not a verified teardown. No identified creator statement, repository, project file, or workflow demonstration closes that gap.
2. **[verified: external] The surrounding stack is real and now substantially richer than the seed implies.** BrickLink Studio imports and exports LDraw, produces instructions, and offers a conservative stability check; LDraw supplies an open textual interchange; BrickGPT generates stable structures from a small brick vocabulary; and BrickNet now learns a typed connection graph and build paths over thousands of LDraw part types.
3. **[inference: Play-Well] BrickNet is the most consequential update to the seed.** It makes a broad-parts `assembly graph → build path` substrate concrete. It does not make that graph Play-Well's canonical scene, prove physical stability or function, establish inventory truth, or encode the evidence/authority/workflow axes already required by Play-Well.
4. **[verified: repository] Play-Well already has the stronger systems boundary.** The current design makes the OpenUSD BuildDoc canonical; LDraw is leaf geometry and Studio interchange; `brickcore` owns deterministic checks; Blender and Studio are projections/editors; and every check returns `valid | invalid | unknown(coverage)` rather than a single confidence score.
5. **[inference: Play-Well] The useful synthesis is not a monolithic “text-to-LEGO” model.** It is a sequence of typed, inspectable projections: intent → required behaviour → candidate mechanism/assembly → canonical BuildDoc → verifier vector → human/physical evidence. Models may propose each transition; deterministic tools and people own acceptance.
6. **[inference: Play-Well] The first valuable vertical slice remains narrower than the seed's full compiler.** Ingest an LDraw model, derive a connection graph, validate the checks Play-Well can actually cover, round-trip through Studio, emit a BOM, and preserve all evidence. Mechanism retrieval, instruction quality, camera inventory, and narrative lowering should enter as separate measurable slices.

## 2. Audit of the seed scaffold

| Seed claim or direction | Evidence verdict | Consequence for Play-Well |
|---|---|---|
| Brickcrafts likely uses Studio plus private scripts and hand-built assets | **[unverified/open]** No public first-party workflow evidence was found | Do not cite Brickcrafts as architecture precedent; use the channel only as a requirements elicitation source if creator evidence becomes available |
| Studio is a practical hub for modelling, rendering, checking, instructions, and wanted-list handoff | **[verified: external]** Official Studio documentation supports file import/export, Instruction Maker, PDF/PNG instruction export, and stability checking | Keep Studio as human editor, instruction authoring surface, and calibration oracle—not canonical truth |
| LDraw is a useful open interchange | **[verified: external]** The official specification defines LDR/DAT/MPD text records, transforms, units, and `0 STEP` | Preserve LDraw at the interchange/leaf layer; do not overload it with Play-Well authority and provenance semantics |
| BrickGPT generates buildable/stable brick structures from text | **[verified: external]** ICCV 2025 paper, official project, and repository establish the generation and rollback pipeline | Use as a small-vocabulary generation baseline and failure corpus, not a general LEGO designer |
| BrickGPT uses “47k+ stable structures / 28k+ objects / 21 categories / 20³ grid / eight bricks” | **[verified: external]** The project and paper support these figures; the eight-piece vocabulary is `1×1`, `1×2`, `1×4`, `1×6`, `1×8`, `2×2`, `2×4`, `2×6` | Treat its apparent success as conditional on severe vocabulary and discretization constraints |
| BrickGPT was an ICCV 2025 best paper | **[verified: external]** Official project page identifies the Marr Prize / Best Paper recognition | Useful evidence of research importance, not evidence of production readiness |
| A general connection graph was a missing research branch | **[verified: external]** This is outdated as a blanket statement: BrickNet (CVPR 2026) provides a graph-backed, typed connector representation and path serialization over a much larger part vocabulary | Evaluate BrickNet as an adapter/input and benchmark; do not replace the BuildDoc or Play-Well evidence model |
| Rebrickable can supply a mineable MOC corpus through its API | **[verified: external]** Current Rebrickable API documentation says v3 does not provide MOC data or MOC inventories except alternate builds | Use Rebrickable for catalog, mappings, sets, and authenticated collections; acquire any MOC research corpus through separately licensed channels |
| Image recognition can automate inventory | **[verified: external]** Published systems demonstrate promising recognition, especially under controlled capture, but also class confusions and synthetic-to-real gaps | Recognition yields an evidence-bearing observation requiring reconciliation; it never silently mutates canonical inventory |
| `0 STEP` or a graph traversal is an instruction generator | **[verified: external]** LDraw defines step boundaries; BrickNet samples spanning-tree build paths. Neither establishes readable, safe, pedagogically useful instructions | Treat build order and instruction presentation as separate artefacts with separate validation and physical user tests |
| A single play-value metric can guide generation | **[unverified/open]** The LEGO Foundation/ACER literature describes observable characteristics of playful learning, not an automatic CAD score | Store human observations and criteria separately; avoid an invented scalar reward until it predicts real sessions |
| Narrative can compile directly into a mechanism | **[unverified/open]** No verified end-to-end system found in this review performs story → function → LEGO mechanism → validated instructions and inventory | Make the intermediate requirements, behaviours, mechanism family, and evidence explicit; evaluate each lowering step independently |

## 3. What the current ecosystem actually supplies

### 3.1 BrickGPT: a constrained generator with an explicit repair loop

- **[verified: external]** BrickGPT converts ShapeNet objects into a `20 × 20 × 20` brick grid, creates randomized layouts, filters for stability, renders 24 views for captions, and fine-tunes a Llama-3.2-1B model to emit brick placements sequentially. [[project](https://avalovelace1.github.io/BrickGPT/)] [[paper](https://openaccess.thecvf.com/content/ICCV2025/html/Pun_Generating_Physically_Stable_and_Buildable_Brick_Structures_from_Text_ICCV_2025_paper.html)]
- **[verified: external]** Its inference loop checks output format, part existence, collision, and physical stability; when a partial assembly becomes unstable it rolls back a suffix and samples again. The released outputs are LDraw, and the repository publishes code, models, and StableText2Brick under MIT for the material it owns. [[repository](https://github.com/AvaLovelace1/BrickGPT)]
- **[verified: external]** The more exact stability analysis uses Gurobi; without it the repository falls back to a simpler and explicitly less accurate connectivity heuristic. This matters when reproducing reported behaviour.
- **[inference: Play-Well]** The durable idea is the loop, not the language model: propose one state transition, run external checks, retain the counterexample, and roll back to the last accepted state. Play-Well's verdict vector is a better acceptance interface because it can preserve `unknown(coverage)` rather than compress incomplete verification into a yes/no signal.
- **[inference: Play-Well]** StableText2Brick is appropriate as a bounded benchmark for parsing, collision, connectedness, rollback traces, and physical-build reproduction. Its eight-part vocabulary makes it a poor proxy for the Winter Village catalog, Technic mechanisms, decorated parts, or procurement.

### 3.2 BrickNet: connection-aware scale, with important omissions

- **[verified: external]** BrickNet (CVPR 2026) represents an assembly as a graph whose nodes contain part vocabulary IDs, colours, and connector definitions and whose edges describe connections. Its five connection families are stud, hinge, axle, ball, and fixed. [[project](https://kulits.github.io/BrickNet/)] [[paper](https://openaccess.thecvf.com/content/CVPR2026/html/Kulits_BrickNet_Graph-Backed_Generative_Brick_Assembly_CVPR_2026_paper.html)]
- **[verified: external]** The published project reports 320,808 pretraining samples spanning 9,743 part types and 67,185 supervised samples spanning 6,457 part types, compared with BrickGPT's 28,259 objects over eight part types. The data documentation gives 253,623 pretraining graphs containing 38.8 million parts and 125.8 million edges, plus 67,185 supervised graphs containing 1.77 million parts and 4.12 million edges. [[data schema](https://github.com/kulits/BrickNet/blob/master/DATA.md)]
- **[verified: external]** Edge records carry connection kind, connector indices, yaw/slide, flip, ball rotations, and axle rotation. The released code converts LDraw to graph, graph to a quantized spanning tree/path, and paths back to assemblies; published scoring includes parse and collision outcomes. [[repository](https://github.com/kulits/BrickNet)]
- **[verified: external]** The code is MIT, but the dataset is request-gated. An MIT code licence does not by itself establish permission to redistribute or train on every source model represented in the data.
- **[inference: Play-Well]** BrickNet's graph is best treated as an imported evidence-bearing representation, not a new system of record. A Play-Well adapter should preserve source model, dataset release, conversion version, original part IDs, graph hash, failed/unknown mappings, and licences.
- **[inference: Play-Well]** Its edge types are a valuable test against Play-Well's planned stud-first connector work. The mismatch is informative: Play-Well needs deterministic connector-space transforms, per-part provenance, coverage, collision/stability/kinematics verdicts, inventory identity, and reversible projection to the canonical USD stage.
- **[unverified/open]** BrickNet does not establish full physical stability, load capacity, human assemblability, mechanism function, instruction quality, inventory availability, or purchase readiness. These should remain separate verdicts unless a dedicated verifier supplies evidence.

### 3.3 LDraw, Studio, and the file boundary

- **[verified: external]** LDraw defines a compact text representation for part references and transforms. Its coordinate convention uses negative Y as up; 20 LDraw Units equal one stud, 8 one plate, and 24 one brick; `0 STEP` marks a build-step break. [[format specification](https://www.ldraw.org/article/218.html)]
- **[verified: external]** The Official Model Repository provides known models under OMR rules requiring CC BY 4.0 statements. LDraw library material must still be read per-file: historical official-part headers and contributions do not justify rewriting every licence as a single blanket grant. [[OMR](https://library.ldraw.org/omr)] [[rules](https://www.ldraw.org/docs-main/official-model-repository-omr/rules-and-procedures-for-the-official-model-repository.html)] [[legal](https://www.ldraw.org/legal-info)]
- **[verified: external]** The LDraw Part Snapping Language is a draft extension used by LDCad shadow files to describe mating hotspots and connector shapes. It is valuable metadata but is not a ratified complete ground truth. [[draft specification](https://wiki.ldraw.org/wiki/Part_Snapping_Language_Extension)]
- **[verified: external]** Studio officially imports `.io`, LDraw `.ldr/.mpd`, LDD, wanted-list XML, set inventories, meshes, and images; it exports model and instruction artefacts. [[imports](https://studiohelp.bricklink.com/hc/en-us/articles/6502277722647-Import-formats)] [[exports](https://studiohelp.bricklink.com/hc/en-us/articles/6502197862679-Exporting-to-other-formats)]
- **[verified: external]** Studio's Instruction Maker lays out steps and can export PDF or page PNGs. Its stability checker evaluates connectedness/support and explicitly warns that it is conservative and may flag well-connected parts. [[Instruction Maker](https://studiohelp.bricklink.com/hc/en-us/articles/5626403887511-Introduction-to-instructions-maker)] [[instruction export](https://studiohelp.bricklink.com/hc/en-us/articles/5628123432215-Exporting-Instructions)] [[stability check](https://studiohelp.bricklink.com/hc/en-us/articles/6501498505111-Stability-check)]
- **[verified: external]** Studio's licence forbids reverse engineering, modification, and separating components. [[software licence](https://studiohelp.bricklink.com/hc/en-us/articles/6606313426711-Studio-Software-License-Agreement)]
- **[inference: Play-Well]** These facts reinforce the existing file-first boundary: generate/open/round-trip supported files; let people use Studio's editor and instruction tooling; record Studio signals as T1/T2 evidence; never redistribute or decode its proprietary connectivity/collider data.

### 3.4 Catalog and procurement surfaces

- **[verified: external]** Rebrickable v3 exposes catalog and user collection resources and offers bulk catalog downloads, but its current documentation excludes MOC data/MOC inventories (apart from alternate builds) and price data. [[API](https://rebrickable.com/api/)] [[v3 documentation](https://rebrickable.com/api/v3/docs/)]
- **[verified: external]** BrickLink's Store API exposes catalog items, subsets/supersets, colours, mappings, price guides, store inventory, and orders. Its reference does not expose wanted-list endpoints; BrickLink supports wanted-list XML upload through the website. [[API reference](https://www.bricklink.com/v3/api.page?page=references)] [[catalog representations](https://www.bricklink.com/v3/api.page?page=resource-representations-catalog)] [[wanted-list upload](https://www.bricklink.com/help.asp?helpID=207)]
- **[inference: Play-Well]** The safe purchasing boundary is therefore an export artefact plus human action: resolve identifiers and colours, subtract reconciled inventory, generate a BOM and uploadable wanted-list XML, record the exact artefact, and keep order submission outside the autonomous path.

### 3.5 Recognition is an observation, not inventory truth

- **[verified: external]** Brickognize reports a Mask R-CNN trained on synthetic renders plus a smaller real-image set for 76 classes; it reports strong AP50, especially in controlled conditions, while identifying similar axes/lengths and transparent/flexible parts as difficult. [[paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC9967933/)]
- **[verified: external]** A separate published dataset contains roughly 155,000 photographs and 1.5 million renders labelled by part identity/category, providing a larger substrate for recognition research. [[dataset paper](https://www.nature.com/articles/s41597-023-02682-2)]
- **[verified: external]** OpenBlok is an open-source camera-and-sorter project and a useful systems reference, but its existence does not establish complete catalog coverage or production accuracy. [[repository](https://github.com/blokbot-io/OpenBlok)]
- **[inference: Play-Well]** Every recognition result should be stored as an `inventory_observation`: image/content hash, capture setup, model and weights version, candidate part/colour IDs, top-k scores, calibration state, and human disposition. Only a confirmed reconciliation event should change inventory.
- **[inference: Play-Well]** A controlled capture rig is likely higher leverage than another model family: fixed background, scale, lighting, views, and a known candidate bin shrink the domain gap and create reproducible counterexamples.

### 3.6 Build order and instructions are distinct products

- **[verified: external]** Brick-by-Brick frames construction as sequential choice under legal-connection and non-overlap constraints, using a validity predictor to filter invalid actions. [[NeurIPS 2021 paper](https://proceedings.neurips.cc/paper/2021/hash/2d4027d6df9c0256b8d4474ce88f8c88-Abstract.html)]
- **[verified: external]** Image2LEGO converts images to voxel/brick representations and demonstrates step instructions/animations, but its evidence is primarily about shape reconstruction rather than broad-part, mechanism, or user-instruction quality. [[paper](https://arxiv.org/abs/2108.08477)]
- **[verified: external]** Component-based instruction research identifies weakly connected and floating regions, segments assemblies, and orders components; its user study motivates something richer than naive layer-by-layer steps. [[paper](https://www.tandfonline.com/doi/abs/10.1080/16864360.2016.1240450)]
- **[verified: external]** MEPNet solves the reverse problem—manual page images to machine-executable component poses—using neural predictions plus geometric constraints. Its schemas and evaluation ideas are relevant even though its direction is not Play-Well's. [[paper](https://arxiv.org/abs/2207.12572)]
- **[inference: Play-Well]** Preserve at least three separate artefacts: an assembly graph, one or more feasible build sequences, and a presented instruction document. The first can be structurally correct while the second traps later placements or the third is unreadable.
- **[inference: Play-Well]** Instruction acceptance needs mechanical checks plus a physical user test: no inaccessible insertion, no unsupported intermediate state, no excessive reorientation, legible camera/occlusion, consistent callouts, correct BOM, and successful completion without undocumented intervention.

### 3.7 Mechanism synthesis requires a function/behaviour layer

- **[verified: external]** *Computational LEGO Technic Design* automatically maps sketches and motion annotations to Technic mechanisms, evaluates input fidelity, simplicity, structural integrity, balance, stress, and assemblability, and produces instructions and physical examples. [[paper](https://arxiv.org/abs/2007.02245)]
- **[verified: external]** LINKS contributes 100 million planar one-degree-of-freedom linkages and 1.1 billion coupler curves for path-generation research; the authors report that infeasibility becomes dominant for larger linkage graphs. [[project](https://decode.mit.edu/projects/links/)] [[paper](https://arxiv.org/abs/2208.14567)]
- **[verified: external]** GenMech explores image-conditioned generation of planar mechanisms. It is evidence for mechanism-family proposal, not for LEGO-specific realization or validation. [[project](https://jl6017.github.io/GenMech/)]
- **[inference: Play-Well]** The reliable lowering is `intended function → required behaviour/trajectory/load → mechanism family and parameters → LEGO realization → simulation → physical evidence`. This follows the useful separation in Function–Behaviour–Structure design models; it does not imply that FBS supplies the domain ontology automatically. [[situated FBS](https://www.sciencedirect.com/science/article/pii/S0142694X03000735)]
- **[inference: Play-Well]** Start with one mechanism family and a bounded acceptance envelope—for example a crank-slider or four-bar moving a known payload through a target path. A text model may select/retrieve candidates; a deterministic kinematics solver and physical build decide acceptance.
- **[unverified/open]** Community projects such as [LegoTechnicSimulation](https://github.com/yoff/LegoTechnicSimulation) and [SimStudio](https://github.com/WorketeWorks/SimStudio) are spike candidates. Their coverage, numerical behaviour, part mappings, licences, and maintenance must be tested before they become dependencies.

### 3.8 Agentic design works only when acceptance is outside the model

- **[verified: external]** LLM-Modulo proposes pairing a potentially unreliable generator with external verifiers; a technical evaluation shows guarantees only in settings where the verifier set is sound and complete for the tested domain. [[position](https://arxiv.org/abs/2402.01817)] [[evaluation](https://arxiv.org/abs/2411.14484)]
- **[verified: external]** CAD-Assistant and newer text-to-CAD systems show useful tool-using and feedback-driven CAD agents, but these results do not make visual-language-model judgement a geometric proof. [[CAD-Assistant](https://openaccess.thecvf.com/content/ICCV2025/papers/Mallis_CAD-Assistant_Tool-Augmented_VLLMs_as_Generic_CAD_Task_Solvers_ICCV_2025_paper.pdf)] [[CADFusion](https://proceedings.mlr.press/v267/wang25eg.html)] [[TOOLCAD](https://arxiv.org/abs/2604.07960)]
- **[inference: Play-Well]** Agents should propose typed operations against the BuildDoc and consume structured counterexamples. Deterministic validators own lattice, identity, known connector, collision, inventory arithmetic, and any kinematics they actually cover. Vision-language models may diagnose presentation or likely intent failures, but their results stay evidence, not proof.
- **[verified: repository]** Play-Well's per-check `unknown(coverage)` state is essential here. “No verifier found a failure” may become `valid` only for the checks and domain that were covered; it cannot become a universal valid build.

## 4. Fit with the current Play-Well architecture

| Existing Play-Well boundary | Research connection | Recommended treatment |
|---|---|---|
| OpenUSD BuildDoc is canonical; LDraw is leaf geometry and Studio interchange | BrickGPT outputs LDraw; BrickNet imports/exports LDraw graphs and paths | **[inference: Play-Well]** Add reversible adapters/projections. Do not make either learned representation canonical |
| `brickcore` owns deterministic domain checks without a Blender dependency | BrickGPT/BrickNet each contain partial validity logic | **[inference: Play-Well]** Reproduce useful checks as independently tested `brickcore` capabilities; retain upstream results as comparative evidence |
| `brick_bench` is the Blender projection/agent work surface | Agentic CAD benefits from tool feedback and visual diagnostics | **[inference: Play-Well]** Agents act through domain operations; raw scene edits re-enter as a diff, never authority |
| Studio is human editor and calibration oracle | Official stability/instruction tools are useful but conservative/GUI-bound | **[verified: repository]** Keep file-first integration and record Studio outputs as tiered evidence |
| Verdict vector separates checks and coverage | Published generators often report aggregate success | **[inference: Play-Well]** Preserve each verifier's domain, version, coverage, counterexample, and authority |
| Asset library separates work/publish, uses content identity, and branches `play/<user> → staging → main` | External corpora and generated candidates have heterogeneous licences and evidence | **[inference: Play-Well]** Ingest into quarantined research/work states; promote only with identity, provenance, licence, and validation manifests |
| Golden set uses known-good models plus synthetic mutations | OMR, StableText2Brick, BrickNet graphs, and local physical builds offer complementary cases | **[inference: Play-Well]** Build a stratified benchmark; never report one aggregate score that hides part-family or verifier coverage |
| Purchasing is gated and reconciled with physical inventory | Catalog APIs and vision produce uncertain mappings/observations | **[inference: Play-Well]** Preserve candidate mappings and human confirmation; output reviewable BOM/wanted-list artefacts, not autonomous purchases |

### 4.1 A candidate projection contract—not a schema decision

**[inference: Play-Well]** The following records make the boundaries testable without replacing the BuildDoc. Names are deliberately descriptive; adopting them would require a schema/ADR decision.

| Record | Minimum content | Authority |
|---|---|---|
| `source_asset` | origin URL/path, content hash, retrieved time, licence assertion and evidence, upstream IDs | Provenance only |
| `assembly_graph_projection` | source BuildDoc version, adapter version, nodes/edges/connectors, unknown mappings, round-trip digest | Derived; never canonical |
| `intent_contract` | natural-language request, actors, constraints, forbidden states, acceptance observations, unresolved ambiguity | Human-authored/confirmed |
| `behaviour_requirement` | motion/path/load/timing/interactions with units and tolerance | Human-confirmed; machine-testable where possible |
| `mechanism_candidate` | family, parameters, referenced parts, predicted behaviours, generation trace | Proposal |
| `build_sequence_candidate` | graph/version, ordered placements/subassemblies, insertion transforms, intermediate checks | Proposal until verified |
| `inventory_observation` | image hash, capture rig, model/version, top-k part/colour candidates, confidence/calibration, human disposition | Evidence only |
| `verifier_result` | check, implementation/version, domain, result, coverage, counterexample, input hash, time | Authority only for its declared check/domain |
| `physical_build_observation` | BuildDoc/version, builder, date, deviations, failures, photos, successful motion/play observations | Highest practical evidence; still not universal proof |

### 4.2 One graph, several meanings

**[inference: Play-Well]** “Connection graph” should not remain a single overloaded object.

1. **Geometric candidate graph:** mating surfaces/connectors could align.
2. **Assembly graph:** placements claim specific connections in a concrete build.
3. **Load/support graph:** forces/support transfer under a declared pose and load case.
4. **Kinematic graph:** rigid bodies, joints, constraints, actuation, and permitted degrees of freedom.
5. **Instruction dependency graph:** what must precede what for access and stability.
6. **Evidence graph:** which source and verifier supports each edge/claim.

**[inference: Play-Well]** BrickNet supplies a strong candidate for (1) and (2), plus sampled paths relevant to (5). It does not collapse the other graphs. Play-Well can link them by stable placement/connector identity while retaining their different semantics and coverage.

## 5. Dataset and benchmark plan

| Slice | Use | Required controls | Main risk |
|---|---|---|---|
| Official Model Repository | Known-good LDraw structure, parsing, round-trip, common assemblies | Preserve MPD authorship/licence and per-part headers; detect unsupported/custom parts | “Official model” is mistaken for proof that every geometry/connector is complete |
| LDraw official/unofficial parts + LDCad shadow metadata | Geometry and candidate connector derivation | Source/version/hash each file; track connector coverage by part family; fail closed on missing licence | Partial draft metadata is promoted to truth |
| StableText2Brick | Small-vocabulary generation and rollback benchmark | Reproduce solver configuration; keep train/validation/test identities; physically sample outputs | Reported stability depends on solver and restricted parts |
| BrickNet PT/SFT | Broad part/connection/path benchmark and adapter spike | Obtain dataset under explicit terms; preserve original model provenance; create contamination policy | Gated corpus and upstream model licences are flattened into “MIT dataset” |
| Published recognition datasets | Baseline part recognition and domain-shift tests | Honour dataset terms; stratify controlled/uncontrolled capture; calibrate top-k | Synthetic score is treated as shelf accuracy |
| Play-Well synthetic mutations | Negative cases for lattice, collision, connectivity, identity, inventory, and sequence | Store mutation operator/seed; assert expected failing check and unaffected checks | Mutations only mirror current verifier assumptions |
| Local accepted overlays and physical builds | Family-specific gold evidence | Explicit consent/roles; version and hash artefacts; record deviations and rework | Small, changing sample is overgeneralized |

**[inference: Play-Well] Benchmark reporting should be stratified** by part family, connection kind, build size, source corpus, seen/unseen identity, and verifier coverage. Each test case should name both the expected failure and checks expected to remain valid. This prevents a new detector from “improving” by turning unrelated results into unknown or invalid.

**[inference: Play-Well] Split by model lineage, not just files.** Related variants, instruction-derived models, recolours, mirrored models, and generated paraphrases can leak across random splits and inflate retrieval/generation performance.

## 6. Verifier matrix

| Check | Deterministic target | Learned/heuristic contribution | Honest acceptance state |
|---|---|---|---|
| Parse/schema | Exact syntax, references, IDs, transforms | Repair suggestion | Valid/invalid for supported format; unknown on unsupported extension |
| Catalog/identity | Resolved part+colour mapping with source/version | Candidate mapping/search | Valid only when mapping is deterministic or confirmed |
| Lattice/alignment | Coordinate/orientation tolerances | Candidate snap | Valid for declared connector families and tolerance |
| Collision | Broad+narrow phase for covered geometry | Prioritize likely collisions | Unknown where collision geometry is missing |
| Connectivity | Declared connector mating and connected components | Predict connector type/edge | Unknown for unresolved parts/connectors; never inferred-valid |
| Static stability | Declared pose/load and solver assumptions | Rank likely unstable states | Solver-scoped result, plus physical evidence where material |
| Kinematics | Joint constraints, collision sweep, target path/load | Mechanism retrieval/parameter proposal | Valid only within modeled joints, tolerances, and loads |
| Assemblability | Insertion access, intermediate support, dependency graph | Propose/order steps | Machine result plus physical-build confirmation |
| Inventory | Exact confirmed counts minus reserved/consumed state | Recognition candidates | No mutation until reconciled |
| Instructions | Step consistency, part callouts, camera/visibility checks | Layout/camera/callout proposals | Physical user completion and recorded interventions |
| Intent/function | Measurable behaviour vs confirmed contract | Parse, retrieve, critique | Human owns ambiguity and semantic acceptance |
| Play observation | Structured session evidence | Summarize patterns | No universal pass and no scalar without predictive validation |

## 7. Recommended vertical slices

### Slice A — LDraw → graph projection → verdicts → Studio → BOM

**[inference: Play-Well]** Start with an OMR or existing village model. Ingest LDraw, produce the canonical BuildDoc and a derived graph, run supported `brickcore` checks, export/reopen in Studio, re-ingest the result, and emit a BOM/wanted-list XML without placing an order.

**Done when:** round-trip identity is measured; graph round-trip loss is explicit; every check has coverage; Studio changes return as a reviewable diff; BOM identifiers are traceable; the branch cannot publish while any required check is invalid or unknown.

### Slice B — Controlled camera → inventory observation → human reconcile

**[inference: Play-Well]** Fix one capture rig and a bounded candidate inventory. Store images and top-k candidates, require a human confirmation/correction, then append one inventory event and feed corrections into an evaluation set.

**Done when:** repeated captures are reproducible; the model/version and calibration are recorded; no unconfirmed observation changes stock; confirmed errors become regression cases.

### Slice C — One mechanism family, one physical task

**[inference: Play-Well]** Select a mechanism family with a measurable motion and load. Retrieve or generate parameter candidates, realize them in Technic, simulate the declared envelope, produce a sequence, and perform a physical build/run.

**Done when:** target behaviour and tolerance precede generation; solver assumptions are explicit; the physical result and deviations are recorded; failures are classified as mechanism, realization, instruction, or material/tolerance failures.

### Slice D — Build-sequence quality

**[inference: Play-Well]** Begin with an accepted static assembly. Compare a BrickNet/tree path, a simple dependency heuristic, and a human-authored sequence. Render with LPub3D or Studio, then run a blinded build test.

**Done when:** structural validity and presentation quality are scored separately; interventions, backtracking, inaccessible placements, unsupported states, and time-to-completion are captured.

### Slice E — Narrative lowering, last

**[inference: Play-Well]** Parse one story beat into actors, actions, forbidden states, and observable behaviours. Require human confirmation. Map the confirmed behaviour to the bounded mechanism-family task from Slice C.

**Done when:** every downstream requirement traces to confirmed text or a recorded human decision; alternative interpretations are preserved; success is measured by the behaviour contract and session observation, not semantic similarity to the prompt.

## 8. Research threads, ordered by Play-Well leverage

1. **[inference: Play-Well] R0 — Freeze representation/evidence benchmarks.** Build the stratified known-good/mutation suite and adapter round-trip tests before adopting a generative model.
2. **[inference: Play-Well] R1 — BrickNet due diligence and adapter spike.** Obtain dataset terms, sample provenance, measure LDraw↔graph loss, map connector semantics, and compare coverage against the current connector plan.
3. **[inference: Play-Well] R2 — Evidence-bearing inventory observations.** Controlled capture, calibrated top-k, human reconciliation, and append-only inventory events.
4. **[inference: Play-Well] R3 — Build sequence as its own benchmark.** Feasibility, intermediate stability, access, orientation, presentation, and physical completion.
5. **[inference: Play-Well] R4 — One mechanism family.** Use kinematics retrieval/synthesis only after a behaviour contract exists; link simulation and physical observations to the same candidate/version.
6. **[inference: Play-Well] R5 — Agent/verifier traces.** Standardize proposal, tool call, counterexample, rollback, coverage, and human decision records across generators.
7. **[inference: Play-Well] R6 — Narrative and play evidence.** Only after the mechanical and sequence loops are measurable; preserve criteria and observations instead of inventing a single reward.

**[verified: repository]** This ordering is research prioritization, not authority to expand the current work order or delay a purchasing deadline. Active correspondence and the operator's order-by gate outrank this document.

## 9. Decisions this research should not smuggle in

- **[inference: Play-Well] Do not replace OpenUSD with BrickNet's graph.** The graph is a useful projection; the canonical stage carries composition, annotation, identity, provenance, and workflow state that the research graph does not.
- **[inference: Play-Well] Do not let a model write “valid.”** It may propose placements, edges, steps, mechanism families, diagnoses, or repairs. A named verifier or person issues each acceptance claim.
- **[inference: Play-Well] Do not treat missing failure as success.** Missing geometry, connectors, licences, load cases, or solver support produce `unknown(coverage)`.
- **[inference: Play-Well] Do not train on scraped MOCs by convenience.** Rebrickable's API does not provide the assumed corpus, and public visibility is not a training/redistribution licence.
- **[inference: Play-Well] Do not conflate path, instructions, and successful build.** Each has its own representation and evidence.
- **[inference: Play-Well] Do not mutate inventory from computer vision.** Reconciliation is a separate, attributable event.
- **[inference: Play-Well] Do not optimize an invented “play score.”** Begin with structured observations derived from published playful-learning constructs and the family's actual sessions.
- **[inference: Play-Well] Do not hide uncertainty in aggregate model scores.** Report per-family and per-verifier coverage, and keep counterexamples addressable.

## 10. Play and family-workflow evidence

- **[verified: external]** The LEGO Foundation/ACER review frames play through characteristics including joy, meaning, active engagement, iteration, and social interaction. It is a measurement literature for observed learning/play settings, not a CAD validator. [[measurement review](https://research.acer.edu.au/monitoring_learning/50/)] [[learning through play](https://research.acer.edu.au/learning_processes/22/)]
- **[inference: Play-Well]** For an early Play-Well session, capture separate observations: who initiated changes; whether the mechanism's cause/effect was discoverable; number and type of iterations; collaboration/turn-taking; repair and remix behaviour; time to first success; and whether the build invited a second story/action.
- **[inference: Play-Well]** Link observations to BuildDoc version, instruction version, participants/roles, session context, and media with consent. A later metric is credible only if it predicts these observations across builds and sessions.
- **[verified: repository]** This fits the existing family-workbench posture: roles, intent contracts, decision points, branch freedom, and a gated path from play to staging/main. The record of what happened outranks a generated aesthetic judgement.

## 11. Direct answers to the seed's workstreams

| Seed workstream | Current answer |
|---|---|
| WS0 — domain IR and constraints | **[inference: Play-Well]** Keep BuildDoc canonical; derive typed assembly/load/kinematic/instruction/evidence graphs. Define verifier domains and coverage before adding generation |
| WS1 — narrative → causal graph | **[inference: Play-Well]** Parse to an intent contract and observable behaviours, then require human confirmation. Preserve alternatives/unknowns |
| WS2 — causal graph → requirements | **[inference: Play-Well]** Use function/behaviour/structure separation: measurable motion/load/timing and forbidden states, with units/tolerances |
| WS3 — requirements → mechanism | **[inference: Play-Well]** Retrieve/parameterize a bounded mechanism family using Computational LEGO Technic Design and LINKS as research precedents |
| WS4 — mechanism → buildable layout | **[inference: Play-Well]** Candidate assembly graph + BuildDoc realization; `brickcore` verifies only covered geometry/connectors/collision/kinematics |
| WS5 — play-value metric | **[unverified/open]** Replace a scalar with structured family-session observations until predictive validity exists |
| WS6 — agentic orchestration | **[inference: Play-Well]** Generator → typed tool operation → verifier vector/counterexample → repair/rollback → human gate; record the trace |

## 12. Source register

### Primary research

- BrickGPT — [project](https://avalovelace1.github.io/BrickGPT/) · [ICCV 2025 paper](https://openaccess.thecvf.com/content/ICCV2025/html/Pun_Generating_Physically_Stable_and_Buildable_Brick_Structures_from_Text_ICCV_2025_paper.html) · [official repository](https://github.com/AvaLovelace1/BrickGPT)
- BrickNet — [project](https://kulits.github.io/BrickNet/) · [CVPR 2026 paper](https://openaccess.thecvf.com/content/CVPR2026/html/Kulits_BrickNet_Graph-Backed_Generative_Brick_Assembly_CVPR_2026_paper.html) · [repository](https://github.com/kulits/BrickNet) · [data schema](https://github.com/kulits/BrickNet/blob/master/DATA.md)
- [Brick-by-Brick](https://proceedings.neurips.cc/paper/2021/hash/2d4027d6df9c0256b8d4474ce88f8c88-Abstract.html) · [Image2LEGO](https://arxiv.org/abs/2108.08477) · [component-based instructions](https://www.tandfonline.com/doi/abs/10.1080/16864360.2016.1240450) · [MEPNet](https://arxiv.org/abs/2207.12572)
- [Computational LEGO Technic Design](https://arxiv.org/abs/2007.02245) · [LINKS](https://arxiv.org/abs/2208.14567) · [GenMech](https://jl6017.github.io/GenMech/)
- [Brickognize](https://pmc.ncbi.nlm.nih.gov/articles/PMC9967933/) · [LEGO image/render dataset](https://www.nature.com/articles/s41597-023-02682-2)
- [LLM-Modulo](https://arxiv.org/abs/2402.01817) · [technical evaluation](https://arxiv.org/abs/2411.14484) · [CAD-Assistant](https://openaccess.thecvf.com/content/ICCV2025/papers/Mallis_CAD-Assistant_Tool-Augmented_VLLMs_as_Generic_CAD_Task_Solvers_ICCV_2025_paper.pdf) · [CADFusion](https://proceedings.mlr.press/v267/wang25eg.html) · [TOOLCAD](https://arxiv.org/abs/2604.07960)
- [Situated Function–Behaviour–Structure](https://www.sciencedirect.com/science/article/pii/S0142694X03000735) · [critical analysis of FBS](https://doi.org/10.1007/s00163-005-0058-z)
- [ACER/LEGO Foundation measurement review](https://research.acer.edu.au/monitoring_learning/50/) · [Learning through play at school](https://research.acer.edu.au/learning_processes/22/)

### Specifications and product documentation

- LDraw — [format](https://www.ldraw.org/article/218.html) · [OMR](https://library.ldraw.org/omr) · [OMR rules](https://www.ldraw.org/docs-main/official-model-repository-omr/rules-and-procedures-for-the-official-model-repository.html) · [legal](https://www.ldraw.org/legal-info) · [part snapping draft](https://wiki.ldraw.org/wiki/Part_Snapping_Language_Extension)
- BrickLink Studio — [imports](https://studiohelp.bricklink.com/hc/en-us/articles/6502277722647-Import-formats) · [exports](https://studiohelp.bricklink.com/hc/en-us/articles/6502197862679-Exporting-to-other-formats) · [Instruction Maker](https://studiohelp.bricklink.com/hc/en-us/articles/5626403887511-Introduction-to-instructions-maker) · [instruction export](https://studiohelp.bricklink.com/hc/en-us/articles/5628123432215-Exporting-Instructions) · [stability](https://studiohelp.bricklink.com/hc/en-us/articles/6501498505111-Stability-check) · [licence](https://studiohelp.bricklink.com/hc/en-us/articles/6606313426711-Studio-Software-License-Agreement)
- Rebrickable — [API overview](https://rebrickable.com/api/) · [v3 documentation](https://rebrickable.com/api/v3/docs/)
- BrickLink — [API reference](https://www.bricklink.com/v3/api.page?page=references) · [catalog representations](https://www.bricklink.com/v3/api.page?page=resource-representations-catalog) · [wanted-list upload](https://www.bricklink.com/help.asp?helpID=207)

### Community spike candidates

- [OpenBlok](https://github.com/blokbot-io/OpenBlok) · [LegoTechnicSimulation](https://github.com/yoff/LegoTechnicSimulation) · [SimStudio](https://github.com/WorketeWorks/SimStudio) · [LPub3D](https://trevorsandy.github.io/lpub3d/)

## 13. Unresolved questions

1. **[unverified/open]** What direct creator evidence would establish Brickcrafts' actual modelling, rendering, mechanism, and instruction workflow?
2. **[unverified/open]** What exact rights and source-model provenance accompany the requested BrickNet dataset, and can Play-Well retain required attribution through derived graph/path artefacts?
3. **[unverified/open]** On a Winter Village/MILS sample, what fraction of part instances and connections can BrickNet, LDCad shadow metadata, and Play-Well's primitive scan each resolve—and where do they disagree?
4. **[unverified/open]** Can BrickNet's graph round-trip through the canonical BuildDoc without losing submodels, flexible parts, decorations, connection ambiguity, or stable placement identity?
5. **[unverified/open]** Which kinematics backend can deterministically cover the first selected mechanism family on the actual deployment targets?
6. **[unverified/open]** Which machine-checkable proxies predict successful human instruction use, and which merely correlate with neat diagrams?
7. **[unverified/open]** Which observed play characteristics matter to this family's sessions, and what evidence would justify turning any of them into a design objective?
8. **[unverified/open]** How should physical build results and inventory observations be signed, corrected, and retained so later agents cannot silently rewrite history?
