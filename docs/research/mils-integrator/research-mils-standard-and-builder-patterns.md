# Research brief 01 — The MILS standard, as numbers

Compiled 2026-09-16 from primary sources (HispaBrick Magazine #13–#17 and #29, abellon.net/MILS, LUG standards decks) for the `mils_integrator.mils.spec` module. Units: 1 stud pitch = 20 LDU, 1 plate = 8 LDU, 1 brick = 24 LDU, baseplate = 4 LDU (LDraw `s\3811s01.dat`; physical 1.6 mm).

## Footprint and stack

| Layer | Part | Height |
|---|---|---|
| 0 | 32×32 baseplate (3811) — or 2×16×32, 4×16×16 | 4 LDU |
| 1 | Bricks (1×4 Technic at edges + filler) | 24 LDU |
| 2 | Plates (top "ground" surface) | 8 LDU |
| Surface | baseplate + 4 plates | **top at 36 LDU above table, 32 LDU above baseplate top** |

Agreed by HispaBrick I, abellon.net, Brick Rodeo, VLC, BrickNerd, Cactus Brick, Brick Model Railroader. Known errata: the L-Gauge wiki's "1 brick (3 plates) above baseplate" and The Earl of Bricks' "~3 plates / pins at 4-12-20-28" contradict every primary source — treat as errors, not variants.

Half modules (16×32, 16×16) are accepted when their edges comply. 48×48 has no canonical rule beyond edge compatibility. The spec's TTM (Transition Terrain Module) may be any size.

Tolerance: unevenness at a side within **one plate** is allowed. "The surface level only matters at the edges, interior can be any height" (Cactus Brick) — encode as an edge-profile constraint only.

## Edge connection (1-indexed studs from each corner along a 32-stud edge)

- Studs 1–2: reserved 2×2 ID corner (colour brick/plates), no Technic.
- Studs 3–6: 1×4 Technic brick (3701), long axis along the edge, sitting on the baseplate (layer 1).
- Studs 7–26: free (filler bricks; walls not fixed).
- Studs 27–30: 1×4 Technic brick.
- Studs 31–32: ID corner.

Six pin holes per edge at 70/90/110 and 530/550/570 LDU from the corner; hole axis 14 LDU above baseplate top (LDraw 3701 geometry; physical ≈5.8 mm). Symmetric about the midpoint, so a BTM mates in any rotation. Pins: frictionless 3673 preferred (HispaBrick #29); half-pin 4274 dresses unmated holes; pins are optional ("great if tables are uneven"). Kit variants add more Technic bricks (every 8 studs, or 1×2 3700) — canonical positions required, extras optional.

## CTM feature table (heights above baseplate top)

| Feature | Width / position on edge | Surface | LDU | Notes |
|---|---|---|---|---|
| Ground (BTM) | — | 4 plates | 32 | |
| Path | 4 studs, centred (15–18) | 4 plates | 32 | brown/DBG/LBG/tan; ±1 plate |
| Dirt track | 8 studs, centred (13–20) | 4 plates | 32 | ±1 plate |
| Paved road | 16 studs, centred (9–24) [ambiguity: HBM says "start at the centre of the edge"] | 5 plates | 40 | DBG tiles; +1 plate only |
| River | 8 studs, centred | water at 2 plates | 16 | banks rise 1 plate/stud to 4 |
| Coast | boundary at 16 studs (half edge is water) | water 1 plate | 8 | land rises 1 plate/stud |

Hills (HBM III): target 5 bricks (15 plates, 120 LDU) above ground; edge profiles Null / Long (1 plate per 2 studs over 32) / Short (1 plate per stud over 16, then flat) / Full; ±1 plate. Mountains: 16 bricks (384 LDU) above ground; profiles in bricks; ±1 brick. Modules named by clockwise profiles ("Mountain null-short-long-null").

## Rail (community convention; not in the 2012 spec)

- Track placement 4-8-8-8-4: track beds at studs 5–12 and 21–28; centrelines at 8 and 24 studs (160/480 LDU) from the edge; 16 studs between centres.
- Ballast: 2 plates above MILS surface (L-Gauge v1.3, PennLUG, NILTC) → track underside at 6 plates (48 LDU) above baseplate top; rail top at 9 plates (72 LDU). GFLUG/Cactus use 1-plate ballast (rail top 8 plates). Parameterise.
- LEGO track piece (53401): sleeper 8 LDU + rails 16 LDU = 3 plates total.
- Mainline no grade, R104 min; branch ≤ 1 plate / 16 studs. Baseplate-level ↔ MILS transition = 6 plates over 96 studs (three modules).
- R40 90° corner occupies a 2×2 module block.

## Roads (later extensions, mutually incompatible at the edge — per-layout parameter)

- HispaBrick paved road: 5 plates (40 LDU).
- MultiRoad (Michael Gale 2016 / L-Gauge): road 6 plates (48), walkway 8 plates (64), 22 studs wide.
- VLC brick-built: road inset 2 plates below ground (16), sidewalk 1 tile above (40).
- zaLUG standard: 7-plate base (56) — incompatible with MILS.

## Vertical extension / non-MILS content

- Raise a baseplate-mounted element to MILS ground by placing it on supports of 3 plates + 1 tile (32 LDU) standing on the table; +4 LDU if standing on a MILS baseplate (within tolerance).
- Two-level construction: supports "4 bricks + 2 plates + 1 tile" (120 LDU) match a Full hill; "15 bricks + 2 plates + 1 tile" (384 LDU) a Full mountain. Piles of bricks are not enough — needs contact surface.
- No canonical rule for sets whose ground level differs; see brief 02 patterns.

## Representative BOM, minimal canonical BTM

1× 3811; 8× 3701 (Technic 1×4); 4× 3003 ID corner; ~10× 1×6/1×8/1×10 fillers; 2×2/2×4 interior pillars on a ≤4-stud grid ("any gap larger than 4 studs has too much flex"); 4× 16×16 (91405) or 64× 4×4 (3031) plates; 0–24× 3673/4274.

## Sources
- https://www.hispabrickmagazine.com/pdfs/HBM014_EN/HBM014_EN-61-63.pdf
- https://lowlug.com/wp-content/uploads/2015/03/bb_ltc-MILS-combined-01-05.pdf
- https://www.hispabrickmagazine.com/pdfs/HBM029_EN/HBM029_EN-22-24.pdf
- https://abellon.net/MILS/index.html
- https://cactusbrick.org/wp-content/assets/MILS-Bricks-by-the-Bay-2018.pdf
- https://brickrodeo.com/images/account/instructions/2023/pdf/BR202304-Instructions.pdf
- https://vlc.ca/wp-content/uploads/2021/01/Moving-to-MILS-Bricks-LA-2021-N-Snowball-2021-01-10_Optimized.pdf
- https://bricknerd.com/home/how-to-modularize-your-lego-train-layout-with-mils-7-27-21
- https://l-gauge.org/wiki/index.php?title=Modular_Standards
- https://brickmodelrailroader.com/wp-content/uploads/2019/11/L-Gauge-Modular-Standard-v1.3.pdf
- https://lgms.org/wp-content/uploads/2021/07/LGMS-v1.5.pdf
- https://www.flickr.com/photos/michaelgale/29260750952 , https://www.flickr.com/photos/michaelgale/29029717990
- https://niltc.org/standards/track-specifications , https://renlug.org/resources/building-standards/train-and-track-standards/ , https://gflug.org/standards
- https://www.zalug.co.za/zalug-integrated-landscaping-standard/
- https://brickmodelrailroader.com/index.php/2022/06/10/review-brickyard-building-blocks-lego-compatible-baseplate/
- https://library.ldraw.org/library/official/parts/3701.dat , https://library.ldraw.org/library/official/parts/53401.dat , https://library.ldraw.org/parts/18489
- https://www.bricktraindepot.com/wp-content/uploads/2020/02/Cams-Brick-MILS-BTM-Green.pdf
- https://bricksandfigs.blogspot.com/2025/12/how-to-make-mils-baseplate-for-my.html
- Flagged low reliability: https://theearlofbricks.com/build-mils-plates/
# Research brief 02 — How builders put official sets onto MILS (pattern catalog v0)

Compiled 2026-09-16. These eleven patterns are the seed of the `mils_integrator.patterns.taxonomy` enum. Each pattern names a problem, a geometric move in studs/plates, typical parts, cited examples and pitfalls. Items marked [unverified] come from search metadata only (Rebrickable, Bricking Ohio, Reddit and YouTube watch pages were blocked from the research sandbox).

## P1 — plates-not-baseplates: classify the set's foundation
Every Winter Village building from 10199 to the current wave is built on stacked ordinary plates, not a baseplate (10325 Alpine Lodge: "two layers of standard plates" — Brick Architect). Ground level therefore sits 1–2 plates above whatever it stands on, and the set has anti-studs that lock onto a MILS top. Sets shipped on a 32×32/16×32 baseplate (Modular Buildings, City, 60304 road plates) have a half-plate baseplate with no anti-studs: it cannot clutch to MILS and sits ½ plate low. Classify each set: plate-built → P2/P3; baseplate-built → P4.

## P2 — plinth / riser: lift to MILS surface
A plate-built set on a MILS top stands 1–2 plates proud of surrounding terrain; on the bare table beside MILS it sits 4.5 plates low. Standard riser under a set on the table = baseplate + 1 brick + 1 plate (build a BTM under it — VLC). Fine-tune ±1 plate (Bricks & Figs raises a shop exactly one plate to level a swing-out section, and back-sets the building 2 studs to gain sidewalk, filling with tiles). Parts: 2×2/2×4 bricks on a ≤4-stud grid under 16×16 or 8×8 plates; 1×4 Technic at edges; white 4×4 plates on top for winter. Examples: Bricksie "How to Build a MILS Plate & Transfer a Modular Building" (yt TCQAMP_pqAY); Preston_builds (QZvIBYlob1o); JAYSTEPHER (ykMuSiOBlkQ); Miami Brick Architect (_uwGj4fwhXg); Bricking Ohio "MILS Placement: 10267 Gingerbread House" [unverified]. Pitfall: 1×2 Technic bricks clutch poorly; tie edges with top plates.

## P3 — pocket / sink: omit the top plate under the footprint
Build the BTM foundation (baseplate + brick layer) and leave the top-plate layer off under the set's footprint so the set's own bottom plates become the module's top layer, landing ground floor exactly at grade (VLC: "modular buildings can sit directly on foundation studs without top plates"). Deeper pockets (pond 2 plates below grade) follow the river rule: bottom at 2 plates, banks 1 plate/stud. Example: NCX BriX "Frozen Winter Lake – MILS Module" MOC-163246 [unverified]. Pitfall: one-plate-thick bases flex on a coarse grid — put 2×2 bricks under every plate corner.

## P4 — strip or shim the baseplate
Order of community preference: (1) rebuild the ground layer on ordinary plates over a MILS foundation and discard the baseplate, adding 2×2 side-stud bricks so the façade plugs into the base (Bricks & Figs); (2) keep the baseplate loose on the brick layer with a craft-foam shim (~½ plate) (Brickset forum); (3) use 3.2 mm third-party baseplates with anti-studs as the MILS top (Brick Model Railroader); (4) 60304 road plates are a brick tall — lower 1 plate inside the shell and curb with 6091 (My LEGO City).

## P5 — footprint-to-module fit
Winter Village footprints are odd (10308 shops 6 studs deep; 10293 L-shaped). Moves: half-stud centring with jumpers 15573/87580; 2-stud back-set for sidewalk; shallow sets along the rear edge as backdrop; corner/L-shaped sets into module corners; bigger-than-module → "modgrup" (only the outer border must comply — HispaBrick; VLC: compliance only at the interface between builders), e.g. gabizon's 12-set Winter Village display base MOC-199368 [unverified]; 48×48 grids in touring displays. 45°: 10259 rotates its entrance on a 4×4 turntable in a square hole; whole-set rotation uses a 2×2/4×4 turntable — true 45° is irrational, accept legal near-45° (6×9 + 2×7) or tolerate stress; keep the rotated footprint inside 32×32 (diagonal ≈ 1.41n) or make a 2-module modgrup.

## P6 — terrain blending / skirting the seam
Step down 1 plate per stud (short profile) or per 2 studs (long profile) from the set base to the module surface. Snow skirting: white 1×2/1×3 curved slopes, wedge plates, 1×1 quarter-round tiles (as 10259's platform), 1×1 round plates, cheese slopes, SNOT brackets for drifts. Public edges in solid surface colour so pins/gaps don't show. Low-effort: batting "snow blanket" over the seam.

## P7 — winter landscaping conventions on MILS
White 4×4 plates (cheapest per stud) with occasional 8×8; mix white and light-bluish-grey for packed paths/ice; exposed studs = crunch, tiles = packed snow. Winter pathway CTM (Cactus Brick): 4 plates high, 4–8 studs wide, grey 1×1 round plates. Ice: trans-dark-blue tiles over blue/white plates at 2 plates. Snow-on-detail vocabulary: white horns, claws, cones, lever bases, bulbs, fangs, plates-with-handle. Bricking Ohio white MILS kit: 1× white 3811, 64× white 4×4, 73× 2×2 bricks, 8× white 3701, 4 friction pins.

## P8 — road / path / sidewalk continuity
Paved road CTM 16 wide centred at 5 plates; path 4 wide at surface; MultiRoad 22 wide at 6 plates; VLC brick road 22 wide inset 2 plates. Sidewalk recipe (Modular standard): ~8 studs deep, LBG 1×8 tile curb, DBG tiles, 2×2 jumpers, grille tiles. Road/rail/river CTMs cannot be freely rotated; BTMs can. Downloadable: Legofan21 "MILS Road Plates Pack", Hannas.Beverly "MILS Street 32x32 Curve", cehbricks "Tram Street MILS Plate", cscott "MILS Road and Tram Track" [unverified].

## P9 — train track on MILS (and the 10254 loop)
Track floats on tiles 2 plates above the MILS surface, held by jumper plates at intervals; rail top ≈ 9 plates above baseplate top; centreline 8 studs in from the edge, two tracks per module 8 studs apart; ballast DBG plates with 1×1 LBG/black stones, ties 1×4 tiles; R40 90° corner = 2×2 modules, curves float on a tile bed with a plate ballast shoulder; baseplate↔MILS transition 6 plates at 1 plate/16 studs over three modules; cable pass = 1×4 arch or open 1×4 gap per side. Winter Village specifics: 10254 loop is R40 + straights; 10259's platform is raised 2 bricks + 2 plates to meet the train floor, so ballasting the track +2 plates requires raising the station the same 2 plates; 10308's tram runs without rails; winter track MOCs MOC-108441, MOC-124104 [unverified]; free PDF MILS track modules at Brick Train Depot. Pitfalls: track clips horizontally so modules with track on both edges can't lift straight out; road-over-track crossings need the road to climb 3 plates.

## P10 — lighting under MILS
The 1-brick cavity is the wire chase; leave a full 1×4 gap per side; hide battery boxes in service alleys. Light My Bricks publishes per-set Winter Village install guides documenting where wires exit each set (10216, 10254…). Warm white in windows, cool white for snow sparkle.

## P11 — recurring parts cheat-sheet
3701 + 4274/2780/3673 (module joint); 32064 + 4L axle (stiffer joint); 2×2/2×4 bricks ≤4-stud grid (support); 65803 16×16 Technic brick (one-piece riser); 4×4/8×8/16×16 plates (top); 15573/87580 jumpers (half-stud centring, track hold-down); 2×2/4×4 turntables (45°); 2×2 side-stud bricks (façade anchor); 6091 (curb); 1×4 arch (cable); white ¼ tiles, curved slopes, round plates, cheese slopes (snow skirting); 1×4 tiles + 1×1 round tiles (track bed); trans-dark-blue tile, trans-clear plate (ice).

## Where builders document this (scrapability)

| Source | Value | Feed / API |
|---|---|---|
| L-Gauge wiki | canonical MILS/track/road numbers | MediaWiki api.php; use `index.php?title=` |
| abellon.net/MILS + HispaBrick PDFs | the spec | static; robots-blocked in sandbox, mirrors on Lowlug |
| BrickNerd | MILS train how-to, WV customisation | `https://bricknerd.com/home?format=rss` |
| Brick Architect | reviews with base/footprint notes | `/feed/` |
| The Brothers Brick | snow techniques, WV reviews | `/feed/`, `/tag/snow/feed/` |
| New Elementary | angle/parts techniques | `/feeds/posts/default` |
| Brickset | reviews, forum "My Winter Village Project" | `https://brickset.com/feed`, API v3 |
| Eurobricks | "MILS modules with track", "MILS tips and tricks" | Invision per-forum RSS |
| Rebrickable | MOC metadata for MILS plates/road packs | API v3 (no MOC endpoints); HTML pages blocked at volume |
| Brick Train Depot | free PDF MILS track modules | static |
| YouTube: Bricksie, Preston_builds, JAYSTEPHER, Miami Brick Architect, BRiXTOF, Brick Scavenger | MILS conversions and WV builds | `feeds/videos.xml?channel_id=` |
| Flickr "MILS Modules" group | photos | Flickr API |
| Bricking Ohio | "MILS Placement: 10267", white kits | Squarespace RSS (host blocked in sandbox) |
| The Brick Blogger | yearly WV diorama round-ups | `/feed/` |
| LUG standards (RenLUG, VLC, Cactus Brick, PennLUG, LUKR, LGMS) | exact numbers | static PDFs |
| Facebook WV groups, Reddit | most active, but not scrapable / ML use not permitted | — |

## Seed URLs (see `config/sources.toml`)
1. https://l-gauge.org/wiki/index.php?title=Modular_Standards
2. https://lowlug.com/wp-content/uploads/2015/03/bb_ltc-MILS-combined-01-05.pdf
3. https://www.hispabrickmagazine.com/pdfs/HBM014_EN/HBM014_EN-61-63.pdf
4. https://vlc.ca/wp-content/uploads/2021/01/Moving-to-MILS-Bricks-LA-2021-N-Snowball-2021-01-10_Optimized.pdf
5. https://cactusbrick.org/wp-content/assets/MILS-Bricks-by-the-Bay-2018.pdf
6. https://bricknerd.com/home/how-to-modularize-your-lego-train-layout-with-mils-7-27-21
7. https://renlug.org/resources-2/standards/train-and-track-standards/
8. https://www.flickr.com/photos/michaelgale/29029717990
9. https://bricktraindepot.com/resources/free-layout/
10. https://www.brickingohio.com/blog/mils-placement-10267-gingerbread-house
11. https://bricksandfigs.blogspot.com/2025/12/how-to-make-mils-baseplate-for-my.html
12. https://bricksandfigs.blogspot.com/2024/12/how-to-make-raised-baseplate-mils-for.html
13. https://theearlofbricks.com/build-mils-plates/ (BOM only; pin positions wrong)
14. https://mylegocity.substack.com/p/build-adapting-the-new-lego-roads
15. https://forum.brickset.com/discussion/25994/my-winter-village-project/p13
16. https://www.eurobricks.com/forum/forums/topic/173483-mils-modules-with-track/
17. https://rebrickable.com/mocs/?q=MILS+plate
18. https://rebrickable.com/mocs/MOC-199368/
19. https://www.youtube.com/watch?v=G8Snh5VzBI0
20. https://htbi-moc.com/blogs/guides/lego-christmas-village-the-ultimate-winter-wonderland-moc-guide-hand-picked-models

Full source list (70+ URLs) retained in the research agent transcript; the seed config carries the actionable subset.
