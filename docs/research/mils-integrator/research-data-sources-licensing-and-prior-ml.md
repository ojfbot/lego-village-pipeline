# Research brief 03 — Machine-readable sources, endpoints, licensing

Compiled 2026-09-16. [verified] = read from the primary page; [unverified] = prior knowledge / secondary. Drives `mils_integrator.harvest.*` and `config/sources.toml`.

## LDraw
- **OMR** (official sets as MPD): browse `https://library.ldraw.org/omr` and `/omr/sets` (paginated HTML; set pages keyed by internal id, not set number). File URL pattern `https://library.ldraw.org/library/omr/<setnum>-<qualifier>.mpd` (e.g. `10001-1.mpd`, `10001-1_B-Model-from-Instruction.mpd`) [verified]. No zip, no JSON API → crawl the index, fetch with conditional requests. License **CC BY 4.0** [verified]. Winter Village coverage is set-by-set [unverified].
- **Parts library**: `https://library.ldraw.org/library/updates/complete.zip`; monthly `lcadYYMM.zip` (latest 2026-08) [verified]. License CC BY 4.0 / CC0 per part [verified]. Layout `ldraw/parts`, `ldraw/parts/s`, `ldraw/p`, `ldraw/p/8`, `ldraw/p/48`, `LDConfig.txt`.
- **Format** (spec article 218): right-handed, **−Y up**, LDU; line types 0–5; `1 colour x y z a b c d e f g h i file` with row-major 3×3; colour 16 inherit / 24 edge; BFC extension (415); MPD `0 FILE` blocks (47). Studio-exported LDraw carries `PE_TEX_INFO` metas.
- **Tooling**: `pyldraw` on PyPI is dead (2019). `ldr_tools_py` (Rust/PyO3, MIT, reads `.io`) is the best parser if Rust is available. TobyLobster/ImportLDraw (v1.2.3, Apr 2026, Blender 2.81→5.1, GPL) for Blender import; LeoCAD CLI for headless renders (needs GL context / xvfb). Writing a parser is realistic: the grammar is trivial; work is in subfile resolution (parts/, p/, MPD subfiles, case-insensitivity, backslashes), matrix composition and BFC.
- **Connectivity metadata**: LDCad Shadow Library (`SNAP_CYL gender=M|F` for studs/anti-studs, `SNAP_INCL` grid repetition; CC BY-SA 4.0; subset coverage) — https://github.com/RolandMelkert/LDCadShadowLibrary ; Studio `.conn` files (reverse-engineered); BrickNet ships connector labels + collision meshes.

## Rebrickable
- API v3 `https://rebrickable.com/api/v3/`, header `Authorization: key <KEY>`, ~1 req/s, 429 then bans; pagination `page`, `page_size` ≤1000 [verified]. Endpoints: `lego/sets/`, `lego/sets/{set}/parts/`, `lego/parts/{p}/`, `lego/parts/{p}/colors/{c}/`, `lego/elements/{id}/`, `lego/themes/`; parts carry `external_ids.LDraw` [verified]. **MOC endpoints removed 2020-04-19** [verified].
- CSV dumps `https://cdn.rebrickable.com/media/downloads/<table>.csv.gz` — themes, colors, part_categories, parts, part_relationships, elements, sets, minifigs, inventories, inventory_parts, inventory_sets, inventory_minifigs; daily; "free for any purpose, mention us" [verified URLs].
- MOC instructions: designer copyright, free vs premium; **metadata only** in our corpus.

## LEGO.com building instructions
- Per-set page `https://www.lego.com/en-us/service/building-instructions/<setnum>` (SPA). PDF CDN `https://www.lego.com/cdn/product-assets/product.bi.core.pdf/<7-digit asset id>.pdf` [verified one example].
- Backend used by the site: `POST https://services.slingshot.lego.com/api/v4/lego_historic_product_read/_search` with a public front-end `x-api-key` and an ES-style body filtering `product_number`; `product_versions[].building_instructions[]` holds PDF URLs [verified via community gist; key may rotate]. Older `/service/biservice/search?prefix=` endpoint status unknown.
- robots.txt: no rule against `/service/` or `/cdn/product-assets/`; sitemap index at `/service/sitemapindex.xml` [verified].
- Legal: LEGO copyright, freely downloadable for personal use; store locally, **never redistribute**. LEGO Builder 3D data = Unity asset bundles, not accessible.

## BrickLink
- Studio `.io` = ZIP with password `soho0909` containing `model.ldr` (+ `model2.ldr`, thumbnail) [verified]; `ldr_tools` reads natively. Exports: ldr/mpd, lxfml, dae, csv, wanted-list xml.
- API `https://api.bricklink.com/api/store/v1/` OAuth 1.0a, IP-registered; `/items/{type}/{no}`, `/subsets`, `/supersets`, `/price`, `/item_mapping`; ~5k req/day [unverified].
- ToS §17 bans robots/spiders on web pages [verified] → API only, never scrape HTML.

## Brickset
- API v3 `https://brickset.com/api/v3.asmx/<method>` JSON; `getSets` with params JSON (`theme`, `subtheme: "Winter Village"`, `setNumber`, `extendedData`), `getInstructions2(setNumber)` mirrors LEGO CDN links; only `getSets` counts against quota [verified].
- RSS: `https://brickset.com/feed`, `/feed/activity` [verified].

## YouTube
- Channel RSS `https://www.youtube.com/feeds/videos.xml?channel_id=UC...` (last ~15). yt-dlp: `--skip-download --write-info-json --write-subs --write-auto-subs --sub-langs "en.*" --sub-format json3 --download-archive`; Data API 10k units/day, search=100 units — use uploads playlist instead. Whisper (`faster-whisper large-v3-turbo`) for uncaptioned videos. Downloads are ToS-grey; private research only.

## Blogs / forums
Brick Architect `/feed/`; BrickNerd `?format=rss`; New Elementary `/feeds/posts/default?alt=rss` (or `alt=json`); Brothers Brick `/feed/`; Eurobricks Invision per-forum `.xml` feeds (Cloudflare); BricksRSS aggregator; Reddit OAuth free tier **prohibits ML training**; Flickr API with per-photo CC filter, caching only for "reasonable periods".

## Crawl stack (2026)
httpx + tenacity (respect Retry-After), per-host ≤1 rps, descriptive UA with contact, protego for robots, ETag/If-Modified-Since, SHA-256 dedup on normalised body, trafilatura for article bodies, feedparser, pypdf/pymupdf for PDFs, storage raw blobs by hash + SQLite/DuckDB state + Parquet export. Feeds/APIs/CDN pass edge bot management; HTML at volume gets challenged — never use CF-bypass tooling.

## Licensing summary

| Source | Store locally | Redistribute | Private training / RAG |
|---|---|---|---|
| LDraw parts | yes | yes, attribution | yes |
| LDraw OMR | yes | yes, CC BY 4.0 | yes |
| Rebrickable CSV | yes | informal "mention us" | yes |
| Rebrickable MOC instructions | only purchased | no | metadata only |
| LEGO PDFs | yes, personal | **no** | private research (no explicit permission) |
| BrickLink API | for your app | no | private |
| Brickset API/RSS | yes | no bulk | private |
| YouTube captions | ToS-grey | no | private research |
| Blogs | yes (RSS offered) | no | TDM for private research generally OK |
| Reddit | via OAuth | no | **not permitted** |
| Flickr | short periods, CC only | CC terms | CC only |

## Sources
https://library.ldraw.org/omr · https://library.ldraw.org/omr/sets/657 · https://www.ldraw.org/article/593.html · https://library.ldraw.org/updates?latest= · https://ldraw.org/article/218.html · https://www.ldraw.org/article/415.html · https://www.ldraw.org/article/47.html · https://www.ldraw.org/pt-policies.html · https://github.com/TobyLobster/ImportLDraw · https://github.com/ScanMountGoat/ldr_tools_blender · https://www.leocad.org/docs/cli.html · https://rebrickable.com/api/v3/docs/ · https://rebrickable.com/downloads/ · https://github.com/hbmartin/rebrickable · https://gist.github.com/antiops/ba75c409c4814886e1a152c0b4878484 · https://www.lego.com/robots.txt · https://forums.ldraw.org/thread-26536.html · https://wiki.ldraw.org/wiki/IO · https://v2.bricklink.com/en-us/terms-of-service · https://brickset.com/article/52664/api-version-3-documentation · https://brickset.com/article/52663/index-of-rss-feeds · https://www.flickr.com/help/terms/api · https://www.socialcrawl.dev/blog/reddit-data-api-2026
# Research brief 04 — Prior computational work on LEGO assemblies, and what to borrow

Compiled 2026-09-16. Conclusion first: **do not train a generative brick model.** Every learned system needs tens of thousands of examples and still yields 82–98 % validity on free-form shapes; our problem is narrow, structured, and has a deterministic core. Use an LLM planner + deterministic geometry/solver tools + automatic validators, fed by a well-tuned retrieval harness with evals; the builder answers the forks (ADR 0005). Fine-tuning is not a planned phase.

## Learned systems

| Work | Representation | Model | Data | License / code |
|---|---|---|---|---|
| LegoGPT / BrickGPT (CMU, ICCV 2025) | text, one brick per line `hxw (x,y,z)` in a 20³ grid, 8 brick types, no rotation token | LLaMA-3.2-1B SFT; validity + physics-aware rollback; Gurobi force-equilibrium stability | StableText2Lego 47k structures, GPT-4o captions | MIT; github.com/AvaLovelace1/LegoGPT |
| BrickNet (CVPR 2026) | connectivity graph (stud/hinge/axle/ball/fixed) serialised as spanning-tree "path text"; angles to 1°, slides to 1 LDU | Qwen-3 0.6B–14B LoRA | 320k PT / 67k SFT from OMR + others, **by request** | MIT code, `pip install bricknet`, 1.6 GB collision meshes |
| LegoACE (VAST, SIGGRAPH Asia 2025) | per-brick (pos LDU, rot48, type id) | 243M decoder, CLIP + DINOv2 conditioning, DPO | LegoVerse 55k, proprietary | weights on HF |
| LTRON / Break and Make (ECCV 2022, 2024) | native LDraw + LDCad snap graph | seq2seq imitation, builds its own instruction book | OMR + fan models, procedural vehicles | github.com/aaronwalsman/ltron |
| Brick-by-Brick / BrECS (NeurIPS 2021, 2022) | directed graph / 64³ voxels with brick-shaped conv validators | RL, sparse U-Net | ModelNet40 targets, 2×4 only | POSTECH-CVLab |
| MEPNet (ECCV 2022), Brick-Composer (2026), LEGO Co-builder (2026) | manual → executable plan; step-wise pose prediction from renders | keypoint / MLLM | synthetic LDraw manuals; BC-Bench | MIT |
| 2026 RL post-training (arXiv 2606.07602) | on LegoGPT-style output | PVPO | — | identifies "PhysHack": physically valid but semantically wrong |

Not what they sound like: LEGO-Net (furniture), "Stackable LEGO Bricks" (diffusion metaphor), "LEGO: LLM Skill-Based Front-End" (web UI).

## Procedural / optimisation
- Testuz, Schwartzburg, Pauly (EG 2013): mesh → voxels → greedy merge → graph structural analysis → local repair.
- Luo et al. "Legolization" (SIGGRAPH Asia 2015): force-based stability as a convex program; ancestor of LegoGPT's Gurobi check.
- Procedia CIRP 2024: greedy random merge with weighted cost + DFS connectivity per layer; 11 brick types.
- Brick Yourself (Tsinghua AIR): constraint integer program over a preset library.

**Mapping to a riser:** a riser is a legolisation of a *known* solid (extruded footprint mask × required height) with interface constraints (top must present studs under every set anti-stud; bottom sits on the MILS ground; edges match the 4-plate surface). 2.5-D tiling — greedy merge + alternating brick direction per layer + DFS connectivity suffices; stability is trivially satisfied for a solid plinth. The hard part is the interface, not the body.

## Geometry analysis tooling
- Studio's "ground" auto-lowers under the lowest part — a display convention, not stored data.
- Robust ground-plane recipe: flatten the MPD, collect anti-stud points and part AABBs, take max-Y (−Y up) over the largest-area cluster; baseplate parts (3811, 3867) are a strong prior; do it per submodel for multi-height sets.
- Python parsers (pyldraw/michaelgale, pyldraw3, LDRParser) give flattened part lists; none computes connectivity. LDCad shadow snaps or BrickNet's converter provide stud/anti-stud points.
- lego-mcp (Glama) is a template for a validator-enforcing MCP tool (place/remove/check/export LDraw + Blender).

## RAG / LLM assistants
No published work uses AFOL technique text as a RAG corpus for a design assistant. Brick Generator (text → LDraw via off-the-shelf LLM) is "less than ideal"; Brick Directory MCP is catalog-only. The MILS spec itself is small and CC-friendly — retrieval mainly injects exact numeric rules into the prompt.

## Recommendation adopted in this repo (three layers)
1. **Analysis layer (computed):** parse OMR/Studio LDraw → per-part AABB, stud/anti-stud cells, ground plane, 32×32 footprint mask, contact/overhang cells, bbox in studs, height in plates, submodules. JSON; this is all the planner sees about the set.
2. **Plan layer (LLM or rules, JSON schema):** placement (x, z, rot90), riser (height plates, top mask, style solid|hollow|stepped), terrain blend per side, MILS perimeter rule, road/river alignment. Discrete tokens (stud offsets, plate counts, 0/90/180/270) — small enough that a retrieval-grounded LLM with exemplars handles it; forks go to the human as decision points.
3. **Realisation layer (solver):** riser body legolised (greedy merge + interlock + DFS); interface layer so every contact cell lands on a stud; MILS perimeter as a fixed sub-assembly; optional LegoGPT stability module.

**Dataset shape:** `(analysis_json, constraints_json) → plan_json → validator_report`, ~100–300 OMR sets × scenarios (flat, road edge, river edge, ±N plates, corner); solver-generated plans with randomised valid choices + the builder's accepted turns as gold exemplars; rejected samples kept as preference pairs for a reranker and for anti-pattern retrieval. Used as harness exemplars and evals, not for weight updates.

**Automatic metrics:** fit validity (mask ⊂ module, no collision); stud alignment (fraction of contact cells over a stud, target 100 %); height compliance (edges = baseplate + 4 plates, +1 for roads; riser height ≡ 0 mod plate; adjacent step within tolerance); connectivity (single component incl. baseplate; perimeter Technic present); stability (LegoGPT score or BrECS-style checks; overhang ratio per layer for hollow/stepped risers); parts budget; semantic (rubric / LLM-as-judge, never CLIP).

## Sources
https://arxiv.org/abs/2505.05469 · https://github.com/AvaLovelace1/LegoGPT · https://huggingface.co/datasets/AvaLovelace/StableText2Brick · https://arxiv.org/abs/2606.07602 · https://kulits.github.io/BrickNet/ · https://github.com/kulits/BrickNet · https://xjtang.com/assets/files/publications/2025Lego/main.pdf · https://github.com/aaronwalsman/ltron · https://arxiv.org/abs/2207.13738 · https://arxiv.org/abs/2410.01111 · https://arxiv.org/abs/2110.15481 · https://arxiv.org/html/2210.01021 · https://github.com/Relento/lego_release · https://arxiv.org/html/2606.05445 · https://arxiv.org/abs/2507.05515 · https://infoscience.epfl.ch/record/189856 · https://history.siggraph.org/learning/legolization-optimizing-lego-designs/ · https://www.sciencedirect.com/science/article/pii/S2212827124009314 · https://wiki.ldraw.org/wiki/Part_Snapping_Language_Extension · https://github.com/RolandMelkert/LDCadShadowLibrary/ · https://studiohelp.bricklink.com/hc/en-us/articles/6481520864279-The-ground · https://glama.ai/mcp/servers/Axel-Jalonen/lego-mcp
