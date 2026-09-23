# ecosystem — research: from Brickcrafts to BrickGPT, extended for play-well

**Date:** 2026-09-20, revised 2026-09-23 · **Cluster:** play-well / ojfbot/lego-village-pipeline · **Status:** research, pre-ADR
**Question:** Which parts of the open LEGO software ecosystem — creator tooling, LDraw/Blender bridges, connectivity data, sourcing, generative models, train firmware, play research — bear on play-well, and in what order?

**Provenance.** Two passes. (1) A skeleton written by James in the Dia browser, starting from the Brickcrafts YouTube channel and walking the ecosystem, revised by him on 2026-09-23 with a much fuller account of the creator's operation (committed beside this file as `sources/brickcrafts-to-brickgpt-dia-skeleton-2026-09-23.pdf`, sha256 `8659c0bc79cb4262ba18e2cdabb6b4e1c8a9e45de2685591c7a8296724cdd7f8`). (2) A verification-and-extension pass by Claude Advanced Research (claude.ai, 2026-09-20), which checked the skeleton's claims against primary sources and re-framed each thread for play-well. Claims below carry their source URLs in the final section. **Nothing here was re-verified inside this repo**; where a claim becomes load-bearing for a decision, re-check it first. Figures marked *approximate* are third-party and time-varying.

## 1. Bottom line

- **The skeleton holds up, but two things have moved.** BrickGPT (CMU, ICCV 2025 Best Paper) is, for play-well, overtaken by **BrickNet (CVPR 2026)**: a graph-backed, connectivity-first assembler trained on a 320,000-sample LDraw dataset spanning 24,000+ real part replicas — much closer to play-well's real-part, LDraw-native world than BrickGPT's 8 bricks on a 20×20×20 grid. And mils-integrator's stance — *well-tuned retrieval with human decision points, not a generative model* — is supported by the planning literature (LLM-Modulo).
- **For the Christmas 2026 demo the useful stack is deterministic and already open-source:** MILS (HispaBrick 013–017), BlueBrick or LDCad for R40 geometry, **ldr_tools_blender** (MIT) as the Blender import venue, **ExportLDraw** for the return trip to LDraw/Studio, the **LDCad shadow library** as the connectivity source for the fitment validator, and **Rebrickable → BrickLink XML wanted list** as the purchasing path.
- **Three gaps no project fills:** no LDraw→OpenUSD path exists (the canonical-USD layer is play-well's own work, and Blender's USD exporter does not carry geometry-node instances cleanly); BrickLink's marketplace is shrinking by country, so the purchasing path should never assume a stable programmatic cart; and the "narrative → mechanism" problem class is multi-year research, not demo scope.

## 2. Verification of the skeleton

| Claim | Verdict | Notes |
|---|---|---|
| Brickcrafts = Marcus Ungermanns, Innsbruck; City/trains speedbuilds and MOCs | confirmed | Subscribers *approximate*: SPEAKRJ ~571K, Feedspot 2026 list ~658K. |
| Not one channel but four: Brickcrafts (EN, 2020, ~660K), Bob Brickman (DE, 2018, ~335K), **Brickman Brothers** (the technical channel — light control, train control, button-pressers), Brickstory (museum vlogs) — skeleton revision 2026-09-23 | confirmed in substance | The two launch years reconcile the earlier date conflict: Bob Brickman 2018, Brickcrafts 2020. The Brickman Brothers channel exists and is cited as the source for museum walkthroughs. |
| The physical anchor is the Bob Brickman & Brickstory Museum, Rosenheim (350 m²) with moving trains, lit houses, sound effects, button-press actions and a day/night simulation | confirmed | bobstory.de: Ellmaierstraße 18, 83022 Rosenheim; 350 m²; the English page lists exactly those effects. Caveat: the museum is a **joint** venture with the separate creator Brickstory, so not every effect is necessarily Ungermanns's own build. Opening month (March 2024) not independently checked — *approximate*. |
| BrickGPT: CMU, ICCV 2025 Best Paper (Marr Prize); Llama-3.2-1B-Instruct; StableText2Brick 47k+ structures / 28k+ objects; 20×20×20 grid; 8 brick types; physics-aware rollback | confirmed | Pun, Deng, Liu, Ramanan, Liu, Zhu. arXiv 2505.05469. Renamed from LegoGPT. Stability analysis uses Gurobi. |
| ldr_tools_blender ~7 s vs ~100 s on UCS Falcon | confirmed | MIT licence; Rust core + PyO3 bindings + thin addon; Blender 4.1+. Developer benchmark (forums.ldraw.org #27191, 10179-1): 7 s vs ImportLDraw 100 s vs ExportLDraw 68 s. Reads current Studio `.io` directly; old password-protected `.io` must be resaved. Geometry Nodes instancing recommended above ~10k parts. |
| Brickrail: Godot GUI + Python BLE server + on-hub Pybricks; colored block markers | confirmed | Now runs on standard Pybricks firmware. The "~3 → ~7–8 hubs" figure is consistent with the architecture but not independently verified — *approximate*. |
| brickscope: MCP server wrapping Brickognize + Rebrickable | confirmed | NazarLysyi/brickscope, MIT; needs a Rebrickable key. |
| GitHub counts (~1,118 `lego`, ~88 `ldraw`) | snapshot | Checked qualitatively only. |

## 3. Threads, re-framed for play-well

### 3.1 MILS and track geometry — high relevance now

- **MILS** (Modular Integrated Landscaping System) comes from HispaBrick Magazine 013–017, Antonio Bellón. Core module 32×32 (16×32 and 8×16 allowed if they mate to a 32×32); ground level 4 plates above the baseplate; modules join with 1×4 Technic bricks and pins; 2×2 ID corners; a centre pass-through for wiring; about 3 plates of below-grade room. This is the same stack as play-well's baseplate-built rule.
- **Track.** 10254 ships 16 R40 curves — one full circle; LEGO gives the diameter as over 70 cm. Wider radii step by 16 studs (R56, R72, R88, R104 …) from TrixBrix, BrickTracks and Fx Bricks; 4DBrix and Brick Train Depot are mostly printed. Parallel spacing is 8 studs R40↔R56. Elevation precedents: **ViaTrack** (modular viaduct standard) and MILS grade-transition modules.
- **Planning tools.** BlueBrick (GPL-3.0 — use as a tool, don't link it) and LDCad both handle R40 layouts.

### 3.2 Blender / LDraw / USD bridge — high relevance now, USD later

- **Importers.** ldr_tools_blender (MIT; fastest; `.io` native; instancing) for the agent venue. **ExportLDraw** is the only one of the three that also *exports* LDraw — needed to send agent edits back to something Studio opens. ImportLDraw (GPL-2.0+) is mature but slow.
- **Units.** 1 brick = 20 LDU wide × 24 LDU tall; 1 plate = 8 LDU; 1 LDU ≈ 0.4 mm.
- **OpenUSD.** No LDraw→USD tool was found. Blender's USD exporter does not export geometry-node instances cleanly (Blender issues #139654, #96747). The practical reading for play-well: the USD layer should *reference and annotate* LDraw part instances, not bake instanced geometry through Blender's exporter.
- **Blender MCP.** ahujasid/blender-mcp (now `mcp-for-blender`) is the common server — an addon socket inside Blender plus a Python MCP. `datakurre/brick-mcp` edits `.io`/`.ldr` directly without Blender. Both already appear in `docs/research/studio-bridge/`.

### 3.3 Fitment and connectivity — high relevance now

- The **LDCad shadow library** (RolandMelkert/LDCadShadowLibrary) stores `!LDCAD SNAP_*` metas in shadow files beside official parts: `SNAP_CYL` (studs, holes, pins — the workhorse, with gender and radius sections), `SNAP_CLP` (clips), plus `SNAP_FGR`, `SNAP_GEN`, `SNAP_SPH`. This is open data a deterministic Python validator can read.
- Studio's connectivity data is separate, proprietary and not interchangeable (`studio-bridge` §2 records it on disk as 9,198 binary `.conn` files, not to be decoded). That fits the existing decision: Studio is the calibration oracle, not a library.
- A web editor, `chenlongtoh/eb-ldraw-shadow-editor`, shows and edits snap overlays.
- Precedents for the connection model: BrickGPT's rollback; BrickNet's five typed connection kinds (stud, hinge, axle, ball, fixed).

### 3.4 Sourcing and the purchase gate — high relevance now

- The worn path: Rebrickable exports a parts list as **BrickLink XML** → upload to a BrickLink Wanted List (Rebrickable's BrickLink/BrickOwl integration can also fill lists). BrickStore is an offline BrickLink inventory tool.
- **Marketplace contraction.** BrickLink closed China (Aug 2024), the Philippines (May 2025) and roughly 35 more countries from 12 Dec 2025. The US is unaffected so far, but the gate should treat manual XML upload as the baseline and any API automation as a bonus. Relevant to the 2026-10-21 ORDER-BY gate.

### 3.5 Retrieval over precedent corpora — high relevance (mils-integrator)

- Sources: Rebrickable MOCs (API with MOC inventories), Brickset, Eurobricks, The Brothers Brick, BrickNerd (Winter Village techniques), Flickr (master-builder photos), YouTube.
- Photos are individually copyrighted, often under non-commercial Creative Commons terms; Rebrickable's API has terms; BrickLink catalog data is proprietary. Build **retrieval with attribution, not redistribution**. `docs/research/mils-integrator/research-data-sources-licensing-and-prior-ml.md` covers licensing in more depth.

### 3.6 Snow on roofs (roofsnow) — medium now, high next

No published procedural LEGO-snow work was found. Nearest ideas: mesh→brick and heightmap→plate tools (LSculpt, lego-art-remix) and Mecabricks/BrickFX scattering. Best treated as an original Blender geometry-nodes asset with a deterministic check (snow only on valid stud surfaces; thickness in plate units), calibrated against scraped roof-snow precedents.

### 3.7 Generative and vision frontier — low now, medium–high later

- **BrickNet** (Kulits et al., CVPR 2026, arXiv 2604.22984): parts carry typed connectors; a build is serialized as a spanning tree over the connection graph; trained on 320k LDraw samples. Known weakness: collisions in long sequences. The model to study for play-well's connection graph.
- Adjacent CAD-agent work: LLM-generated CAD programs with visual feedback (Cambridge, *Proceedings of the Design Society*); Text-to-CADQuery; CAD-MLLM. All use a verifier in the loop.
- **Brickognize / brickscope** make photo → part ID callable by an agent — relevant to inventory later.

### 3.8 Train control — medium now, high later, and no longer hypothetical

The skeleton's 2026-09-23 revision changes the standing of this branch. A whole channel of the family, **Brickman Brothers**, is devoted to the museum's technical layer — train control (*Zugsteuerung*), light control (*Lichtsteuerung*) and physical button-pressers (*Knopfdrücker*) — and bobstory.de describes automated trains and a day/night simulation across 350 m². So a layout of roughly play-well's eventual ambition, run under program control, exists and is documented in public, in German, by its builder. Which stack he uses (Pybricks, MattzoBricks/Rocrail, or something bespoke) is not stated in English; that makes Brickman Brothers a **precedent corpus worth watching** for the mils-integrator retrieval work and for the later automation layer, with the language barrier as the cost of entry.

10254 can be motorized; a modern conversion uses a Powered Up City hub and train motor, programmable with **Pybricks**. A constant-speed loop sensing ties or colored markers is a small program; **Brickrail** is the step up for blocks and schedules. Motorizing is a physical change the family should decide on.

### 3.9 Play value — relevant to the drafting table and any play-value measure

The LEGO Foundation's *Learning through play: a review of the evidence* (Zosh et al., 2017) names five characteristics: joyful, meaningful, actively engaging, iterative, socially interactive. A play-value measure would do better to score these five than to invent a new scale; PCG "expressive range" analysis covers variety across generated options.

### 3.10 Narrative → mechanism (skeleton §IX) — research, not demo

The framing stands. **Function–Behaviour–Structure** (Gero 1990; situated FBS, Gero & Kannengiesser 2004) is the backbone for turning a required function into structure. **LLM-Modulo** (Kambhampati et al., ICML 2024) is the backbone for orchestration: the model proposes, sound external checkers judge, a human confirms at forks. The riskiest workstreams stay the two the skeleton named — reading unstated requirements, and scoring faithfulness to the story. Neither has a starting artifact.

## 4. Map to play-well components

| Thread | play-well component | Reusable (licence) | Christmas 2026 | Later |
|---|---|---|---|---|
| MILS | landscape modules, baseplate stack | HispaBrick 013–017; BrickNerd (docs) | high | high |
| BlueBrick / LDCad | R40 loop around the tree | BlueBrick (GPL-3.0, tool only); LDCad (freeware) | high | high |
| Track geometry | railbed, ballast; elevation later | TrixBrix, BrickTracks, Fx Bricks; ViaTrack | high / medium | high |
| ldr_tools_blender | brick_bench import | MIT | high | high |
| ExportLDraw | return trip to LDraw / Studio | open source | high | high |
| LDraw → USD | OpenUSD annotation layer | none — build it | low | high |
| Blender MCP | agent venue | mcp-for-blender; brick-mcp | high | high |
| LDCad shadow library | fitment validator | shadow library; shadow editor | high | high |
| Studio checks | calibration oracle | proprietary | high | medium |
| Rebrickable / BrickLink | purchase gate | Rebrickable API; BrickLink XML; BrickStore | high | high |
| Precedent retrieval | mils-integrator | Rebrickable MOC API; curated scrape | high | high |
| Procedural snow | roofsnow | Blender geometry nodes | medium | high |
| BrickGPT / BrickNet | watch, don't depend | BrickGPT repo; BrickNet paper | low | medium–high |
| Brickognize / brickscope | photo → inventory | MIT | medium | high |
| Pybricks / Brickrail | train control | open source | medium | high |
| FBS / LLM-Modulo | narrative → mechanism | literature | low | high |

## 5. Suggested spikes (proposals — nothing here is authorized)

Two of these touch spikes already ordered: HANDOFF-LEGO-PIPE-018 orders S1 (Studio round trip) and S7 (USD runtime matrix). Item 2 and the USD finding in §3.2 are input to those, not a parallel plan.

1. **Fitment validator on the shadow library.** Parse LDraw placements plus `SNAP_*` metas; check stud/pin connection and collision; calibrate against Studio. Suggested bar: agrees with Studio on ≥95% of a hand-labelled MILS + track set before an agent loop relies on it.
2. **MILS + R40 in headless Blender.** Docker Blender + ldr_tools_blender + mcp-for-blender; import one module and the loop; return via ExportLDraw; open the result in Studio.
3. **Purchase path.** Design → parts list → BrickLink XML wanted list, as the only gated action, with manual upload as the baseline.
4. **Precedent retrieval for mils-integrator.** Attributed corpus; options returned as forks for the human.
5. **roofsnow** after (1) generalizes to surface checks.
6. **Train control** after the demo.

What would change the plan: an open, permissively licensed, LDraw-native generator with real connection validity (revisit "retrieval, not generation" for the hard integration cases); first-class instanced USD export in Blender (cheaper USD layer); a restored BrickLink cart/wanted-list API (automate the gate).

## 6. Caveats

- Subscriber counts and the Brickrail hub figure are third-party and approximate.
- OpenUSD-as-canonical, narrative → mechanism, and procedural LEGO snow have no turnkey precedent.
- Precedent imagery is individually copyrighted.
- BrickLink availability is shrinking by country.

## 7. Terms worth linking

**People:** Marcus Ungermanns; Antonio Bellón; Michael Gale; Ava Pun; Jun-Yan Zhu; Deva Ramanan; Changliu Liu; Peter Kulits; Subbarao Kambhampati; John Gero; Roland Melkert; Piotr Rybak.
**Tools:** ldr_tools_blender; ExportLDraw; ImportLDraw; LDCad; LDCad shadow library; BlueBrick; LeoCAD; LPub3D; BrickStore; Brickognize; brickscope; mcp-for-blender; brick-mcp; Pybricks; Brickrail; MattzoBricks; TrixBrix; BrickTracks; Fx Bricks; Rebrickable; BrickLink; BrickLink Studio; Mecabricks; LSculpt.
**Papers and standards:** BrickGPT / StableText2Brick; BrickNet; LLM-Modulo; Function–Behaviour–Structure; MILS; ViaTrack; *Learning through play* (LEGO Foundation, 2017).
**Sets and units:** 10254 Winter Holiday Train; 41843 Family Christmas Tree; R40 / R56 / R104; LDU.

## 8. Sources

- Brickcrafts and family: youtube.com/@Brick_Crafts · youtube.com/@BobBrickman · youtube.com/@BrickmanBrothers · youtube.com/@brickstoryofficial · bobstory.de/en/ (museum, effects, address)
- Brickcrafts (stats) · galaxus.de/en/page/lego-city-youtuber-fulfils-dream-and-opens-museum-31244 · speakrj.com/audit/report/UCTGHqw41qk_WyK3wJK7nweg/youtube · videos.feedspot.com/lego_youtube_channels/
- BrickGPT: avalovelace1.github.io/BrickGPT · github.com/AvaLovelace1/BrickGPT · arxiv.org/abs/2505.05469 · iccv.thecvf.com/virtual/2025/poster/390
- BrickNet: arxiv.org/abs/2604.22984 · openaccess.thecvf.com (CVPR 2026)
- BrickSim (related simulator): arxiv.org/abs/2603.16853
- ldr_tools_blender: github.com/ScanMountGoat/ldr_tools_blender · forums.ldraw.org/thread-27191.html
- ExportLDraw: github.com/cuddlyogre/ExportLDraw · ImportLDraw: github.com/TobyLobster/ImportLDraw
- Blender USD instancing: projects.blender.org/blender/blender/issues/139654
- MILS: bricknerd.com/home/how-to-modularize-your-lego-train-layout-with-mils-7-27-21 · abellon.net/MILS/
- Track: lego.com/product/winter-holiday-train-10254 · trixbrix.eu · bricktraindepot.com · transponderings.blog/2024/05/03/the-straight-the-curved-and-the-pointy-of-lego-compatible-train-track/ · l-gauge.org/wiki/index.php?title=Modular_Standards
- Shadow library: github.com/RolandMelkert/LDCadShadowLibrary · melkert.net/LDCad/tech/shadowLib · melkert.net/LDCad/tech/meta · github.com/chenlongtoh/eb-ldraw-shadow-editor · forums.ldraw.org/thread-28625.html
- BlueBrick: github.com/Lswbanban/BlueBrick
- Sourcing: rebrickable.com/help/bricklink/ · rebrickable.com/blog/92/bricklink-brickowl-integration/ · en.wikipedia.org/wiki/BrickLink · webpronews.com/bricklink-to-suspend-operations-in-35-countries-from-december-2025/
- Blender MCP: github.com/ahujasid/blender-mcp · github.com/datakurre/brick-mcp
- Train control: github.com/Novakasa/brickrail · rebrickable.com/blog/739/pybricks-part-2/
- brickscope: glama.ai/mcp/servers/NazarLysyi/brickscope
- Play: cms.learningthroughplay.com/media/wmtlmbe0/learning-through-play_web.pdf
- Narrative → mechanism: arxiv.org/abs/2402.01817 (LLM-Modulo) · icml.cc/virtual/2024/poster/33965 · arxiv.org/abs/1504.00542 (FBS composition)
