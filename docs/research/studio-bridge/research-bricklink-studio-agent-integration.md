# studio-bridge — research: giving agents access to BrickLink Studio

**Date:** 2026-09-17 · **Cluster:** play-well / ojfbot/lego-village-pipeline · **Status:** research, pre-ADR
**Question:** What already exists, and what surfaces can we build on, so Claude (Cowork/Code), OpenCode, and the pipeline services (mils-integrator, roofsnow, drafting table) can work with BrickLink Studio instances, apps and file formats — ideally as a Blender-connector-style MCP/plugin?

## 1. Bottom line

- **A Blender-style connector for Studio isn't possible the same way.** The Blender connector works because Blender embeds Python: an add-on inside Blender runs a socket server (`localhost:9876`), and a small stdio MCP bridge packaged as a Desktop Extension talks to it. Studio has nothing like that. It is a Unity/Mono C# app with no scripting runtime, no plugin API, no CLI, no AppleScript dictionary and no URL scheme. Its EULA (§4) forbids reverse engineering, modifying, or "separating STUDIO into its component parts", so injecting a server into Studio (BepInEx/Harmony) is out.
- **The workable design is file-first.** Build a local `studio-bridge` MCP that reads and writes `.io` files and uses Studio's own install-side mapping tables at runtime. It hands rendering to Blender (official connector plus an `.io`/LDraw importer) or the LeoCAD CLI, and leaves the few GUI-only actions (instructions, Eyesight render, stability check, BrickLink upload) to **computer use**, packaged as a skill. Studio stays the human's editor. Agents write the files it opens.
- **Reusable prior art exists:** `datakurre/brick-mcp` (.io/.ldr editing MCP), `musharna/ldraw-mcp` (headless Blender renders for vision), `ldr_tools_blender` (imports `.io` directly), `bricks-mcp` (Rebrickable), and Brick Directory (a hosted MCP that aggregates BrickLink prices, Rebrickable and Brickset).

## 2. Verified on James's install (read-only inspection, `/Applications/Studio 2.0`)

| Fact | Evidence |
|---|---|
| Version **2.26.8_1** (All-In-One 2.0.1.0), bundle id `com.BrickLink.Studio` | `version.txt`, `Studio.app/Contents/Info.plist` |
| Unity player on **Mono** (not IL2CPP): `Data/Managed/BrickLink.Studio.*.dll` (BrickLinkAPI, LEGOAPI, Connectivity.Runtime, UI, Common.Runtime) | app bundle |
| `Studio.app` declares **no** document types or URL schemes. `bin/Launcher.app` (`com.bricklink.StudioLauncher`) is the handler for UTI `com.bricklink.io` | plists |
| Native macOS plugins `MenuBar.bundle` and `StandaloneFileBrowser.bundle` → real NSMenu menu bar and NSOpenPanel/NSSavePanel dialogs. Computer use can drive these more reliably than Unity-drawn UI | `Contents/PlugIns` |
| Eyesight renderer: `PhotoRealisticRenderer/mac/eyesight(.app)`, `settings.xml` (`<eyesight version="2.22">`, Cycles-style integrator params), HDRs, ffmpeg libs | folder |
| Bundled LDraw library `ldraw/{parts,p,LEGO,UnOfficial}`, `LDConfig.ldr`, `ldraw/version.txt` = 238 | folder |
| **Proprietary connectivity data:** `ldraw/connectivity/*.conn` (9,198 binary files) + `ldraw/collider/*.col` | folder. Do not redistribute or decode |
| **Mapping tables (tab-separated, human-readable):** `data/StudioPartDefinition2.txt` columns: `Studio ItemNo, BaseStudioItemNo, BL ItemNo, BL ItemKey, LDraw ItemNo, LDD ItemNo, Description, …, IsAssembly?, flexible type, IsDecorated`. `data/StudioColorDefinition.txt` columns: `Studio Color Code, BL Color Code, LDraw Color Code, LDD color code, names…, RGB, Alpha, CategoryName, …, Ins_RGB, Ins_CMYK`. Also `ldraw.xml` (LDraw↔LEGO material), `ldraw_lxfml_mapping.json`, `designid.xml`, `elementInfoList.json`, `LEGOSetList.tsv` | `data/` |

### `.io` container, by era (checked by unzipping bundled samples)

| Era | Encryption | Entries |
|---|---|---|
| Legacy (`.info` version `16.11.1.5`, `1.0.0_13`) | ZipCrypto, password `soho0909` | `model.ldr`, `model2.ldr`, `thumbnail.png`, `errorPartList.err`, `.info` |
| Current (`.info` `{"version":"2.25.11_3","total_parts":186,"parts_db_version":200}`) | **none** | `model.ldr`, `modelv2.ldr`, `model2.ldr`, `model.lxfml`, `model.ins`, `thumbnail.png`, `errorPartList.err`, `.info` |

- `model.ldr` is a normal LDraw MPD using **LDraw colour codes** (e.g. 14 = Yellow, 15 = White). It adds Studio meta lines: `0 CustomBrick`, `0 FlexibleBrickControlPointUnitLength`, `0 FlexibleBrickLockedControlPoint`, `0 NumOfBricks:`, `0 NOFILE`, `0 STEP`.
- `model2.ldr` uses **Studio/BrickLink colour codes** (Yellow = 3, White = 1) and embeds part geometry and BrickLink metadata (`0 BL_Item_No`, `0 BL_Item_Key`, `0 BL_CategoryIndex`, `0 FlexibleType`, `0 RenderAngleOffset`, `0 IsSubModel`).
- `model.ins` is the Instruction Maker layout as XML (`<Instruction><GlobalSetting><PageSetup>…`). `model.lxfml` is LXFML v7 written by "LDraw Converter".
- Readers should try no password first, then `soho0909`. Writers should target the current layout. **Unverified:** the minimum entry set Studio accepts from a third-party writer. `brick-mcp` already writes `.io` that it says opens in Studio, so use it as the reference.

## 3. What already exists (reuse / adapt)

| Project | What it gives us | Notes |
|---|---|---|
| [datakurre/brick-mcp](https://github.com/datakurre/brick-mcp) | MCP (FastMCP) to create, open or save `.io`/`.ldr`/`.mpd`; list parts, BOM, steps; add, move, rotate, recolour parts; parts search | Closest to "Studio file MCP". Python ≥3.14, pyzipper. No collision or validity checks. Licence not stated, so **ask before forking**. Small (9 commits) |
| [musharna/ldraw-mcp](https://github.com/musharna/ldraw-mcp) (`pip install ldraw-mcp`) | `render_ldraw_file`, `render_ldraw_text`, `check_renderer`: headless Blender + ImportLDraw, Cycles CPU, multi-azimuth stitched PNG | MIT, v0.1.1 (Jul 2026). Gives agents "eyes" on a build. LDraw only, so feed it `model.ldr` pulled from the `.io` |
| [ScanMountGoat/ldr_tools_blender](https://github.com/ScanMountGoat/ldr_tools_blender) | Blender 4.1+ importer for LDR/MPD **and current `.io`**. Instancing by part+colour, Geometry Nodes for >10k parts | MIT. Rust core `ldr_tools`. Pairs with the official Blender connector |
| [TobyLobster/ImportLDraw](https://github.com/TobyLobster/ImportLDraw), [cuddlyogre/ExportLDraw](https://github.com/cuddlyogre/ExportLDraw) | Blender LDraw import; ExportLDraw also **exports LDraw from Blender** (round trip for roofsnow-style edits) | ExportLDraw targets Blender 2.82–3.x. Check it on 4.x/5.x |
| [LeoCAD CLI](https://www.leocad.org/docs/cli.html) | Headless-ish `-i` image, `-obj/-3ds/-dae` export, `-csv`, `-html`, step ranges, submodel, camera angles, orthographic | Fastest cheap preview and step-render path. LDraw input |
| LDView / LPub3D | Snapshot CLI (LDView), instruction pipeline (LPub3D) | Studio itself ships LDView-licensed code (`Licenses/LDView*.txt`) |
| [michaelgale/ldraw-py](https://github.com/michaelgale/ldraw-py), [hbmartin/pyldraw3](https://github.com/hbmartin/pyldraw3/) | Python LDraw read/write/generate | mils-integrator already has its own stdlib parser (ADR 0003). These are a reference, not a dependency |
| [wendehals/bricks-mcp](https://github.com/wendehals/bricks-mcp) | Rebrickable MCP: sets, parts, user collections and part lists | Go, EPL-2.0 |
| [Brick Directory](https://brick.directory/docs/faq.html) | Hosted MCP connector: Rebrickable, BrickLink pricing, Brickset, BrickEconomy, BrickOwl | OAuth. Free beta. Third-party hosted |
| BrickLink Store API (OAuth 1.0) e.g. [BricklinkSharp](https://github.com/gebirgslok/BricklinkSharp) | Catalog items, price guide, colours, categories, **item mapping (element id ↔ item no)**, inventory, orders | Needs seller API registration and IP allowlist. **No wanted-list endpoints**, so wanted lists go through Studio's XML export or manual upload |
| [bodog/bricktools#18](https://github.com/bodog/bricktools/issues/18) | Independent conclusion: Studio has no supported CLI or headless API. Use it as a manual tool. Its licence doesn't cover Studio's bundled assets | Confirms §1 |

## 4. Integration surfaces, ranked

1. **File plane (primary).** Read and write `.io`, `.ldr` and `.mpd`. Everything agents need for mils-integrator (`tools.analyze_ldraw`, `tools.riser_ldraw`) and roofsnow lives here. Studio opens the result.
2. **Catalog/mapping plane.** Load `StudioPartDefinition2.txt`, `StudioColorDefinition.txt` and `ldraw.xml` from the local install **at runtime** to translate LDraw ↔ BrickLink ↔ Studio ids and colours. Never commit or ship these files. Rebrickable CSVs and the API are the redistributable fallback. BrickLink API covers price and availability.
3. **Render/preview plane.** Use Blender through the official connector (`execute_blender_code` + `ldr_tools_blender` to import `.io` directly), `ldraw-mcp` for headless multi-angle renders, and LeoCAD CLI for fast thumbnails and step images. This beats calling Eyesight directly: Eyesight is Cycles-derived from about 2017, and running it outside Studio is a EULA grey area.
4. **App-control plane (GUI, computer use).** Open files with `open -a "/Applications/Studio 2.0/bin/Launcher.app" file.io` (**unverified** whether it reuses a running instance). Use the native menu bar (`computer_app_menu`) for *File › Export As* (LDraw, LXFML, POV-Ray, Collada, CSV/TSV parts list, **BrickLink Wanted List XML**) and *Import* (set inventory by number, wanted-list XML → palette). Type paths into native file dialogs with ⌘⇧G. Instruction Maker, Eyesight render queue, stability check and gallery upload are GUI-only. Expect a near-empty accessibility tree inside the Unity viewport, so the viewport is screenshot and coordinate driven.
5. **Not viable:** in-process injection (BepInEx/Harmony on the Mono DLLs), decompiling, decoding `.conn`/`.col` connectivity, or redistributing Studio data. All are blocked by EULA §4.

## 5. Proposed `studio-bridge` MCP (fleet member candidate)

A local stdio MCP in Python/FastMCP that runs on the Mac, mirroring how the Blender connector is packaged:

- **Distribution:** a `.mcpb` Desktop Extension for Cowork. Cloud Cowork sessions then see it through the desktop bridge as `mcp__remote-devices__studio__*`, just like `…__Blender__*` today. The same binary goes in Claude Code `.mcp.json` and OpenCode `opencode.json` (`"mcp": {"studio": {"type": "local", "command": [...]}}`).
- **Config:** `STUDIO_HOME` (default `/Applications/Studio 2.0`), `LDRAW_DIR` (Studio's bundled library or `~/.ldraw`), workspace root for model files.

| Tool | In → Out | Backed by |
|---|---|---|
| `studio.info` | → version, parts_db_version, library version, paths, renderers available | install files |
| `io.read` | path → `{meta, submodels[], parts[{ldraw_id, bl_item_no, studio_color, bl_color, ldraw_color, matrix, step, submodel}], steps, custom_parts, errors}` | zip reader (pwd fallback) + mapping tables |
| `io.write` | LDraw/MPD text or parts JSON → `.io` (current layout, thumbnail optional) | brick-mcp writer logic (licence permitting) |
| `io.extract_ldraw` / `io.from_ldraw` | `.io` ↔ `.ldr/.mpd` (colour-space aware) | same |
| `catalog.map_part`, `catalog.map_color` | any id space → all id spaces | Studio tables → Rebrickable fallback |
| `bom.export` | `.io`/LDraw → BrickLink wanted-list XML, CSV, Rebrickable CSV | mapping + writer. Upload stays manual (no API) |
| `render.preview` | model, views, size → PNG(s) | LeoCAD CLI or ldraw-mcp |
| `render.blender` | model → imports into live Blender via connector | `ldr_tools_blender` |
| `studio.open` | path → launches or focuses Studio with the file | `open` + Launcher.app |
| `mils.*` passthrough | `.io` in → `tools.analyze_ldraw / plan / validate_plan / riser_ldraw` | mils-integrator `tools.py` (accepts `.io` via `io.extract_ldraw`) |

Plus a **skill** (`studio-gui`), not tools: computer-use playbooks for Export As…, import set inventory, render queue, Instruction Maker page export, and stability check. Each playbook sets out preconditions, menu paths, dialog path entry and the expected file on disk, so every GUI step ends in a file the bridge can verify.

**Loop for the drafting table:**

1. The agent plans in LDraw via mils-integrator.
2. `io.write` produces the file and `render.preview` gives a quick visual check.
3. `studio.open` hands the file to James.
4. James edits in Studio.
5. `io.read` diffs his changes back into the plan and stores accepted edits as gold exemplars (ADR 0005).
6. `bom.export` produces the BrickLink order.

## 6. Open items to verify

- [ ] Minimum `.io` entry set Studio 2.26 accepts from a third-party writer (`model.ldr` only? does it need `model2.ldr` or `.info` `parts_db_version`?). Test by round-tripping a `brick-mcp`-written file.
- [ ] `open` via Launcher.app with Studio already running: new window, replace, or prompt?
- [ ] Studio's accessibility tree: does `computer_app_ax_find` see anything beyond the native menu bar and dialogs?
- [ ] Mac user-data paths (CustomParts, preferences, autosave). Likely `~/Library/Application Support/Stud.io/…`, but **unverified**. Needs a folder grant to confirm.
- [ ] brick-mcp licence (unstated). Ask the author or reimplement the writer (the format is simple).
- [ ] ExportLDraw on current Blender. Is `ldr_tools_blender` import-only?
- [ ] Studio's colour/part tables: reading them locally for personal tooling seems fine, but don't commit or ship them. Check the Studio ToS/IP guidance before any public release.

## Sources
Studio Help: [Export formats](https://studiohelp.bricklink.com/hc/en-us/articles/6502197862679-Exporting-to-other-formats) · [Import formats](https://studiohelp.bricklink.com/hc/en-us/articles/6502277722647-Import-formats) · [Software License Agreement](https://studiohelp.bricklink.com/hc/en-us/articles/6606313426711-Studio-Software-License-Agreement) · [Render queue](https://studiohelp.bricklink.com/hc/en-us/articles/6507148199959-Render-queue) · [v2.25.9 critical update](https://studiohelp.bricklink.com/hc/en-us/articles/35041828645143-Studio-v-2-25-9-Critical-Update-released) · [Wikipedia: BrickLink Studio](https://en.wikipedia.org/wiki/BrickLink_Studio) · [LDraw wiki: IO](https://wiki.ldraw.org/wiki/IO) · [LDraw wiki: Eyesight](https://wiki.ldraw.org/wiki/Eyesight) · [LeoCAD #356 (.io contents)](https://github.com/leozide/leocad/issues/356) · [BrickNerd: Hacking Studio renders](https://bricknerd.com/home/hacking-studio-how-to-get-better-renders-like-blender-11-28-23) · [HN: Eyesight/Cycles GPL](https://news.ycombinator.com/item?id=35181954) · [Blender connector architecture (DevelopersIO)](https://dev.classmethod.jp/en/articles/claude-blender-connector-desktop-and-code/) · [OpenCode MCP servers](https://opencode.ai/docs/mcp-servers/) · plus the repos linked in §3.
