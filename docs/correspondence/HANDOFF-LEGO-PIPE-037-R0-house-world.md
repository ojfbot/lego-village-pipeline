---
correspondence_schema: lego-pipe-memo/v2
memo: HANDOFF-LEGO-PIPE-037
revision: R0
status: for_review
memo_type: handoff
title: The house as an entrance to the drafting table
date: "2026-10-11"
thread: drafting-table
from:
  actor: ChatGPT (Codex)
  role: Parallel design proposer and local prototype author
to:
  - actor: James (@ojfbot)
    role: Operator and sole design decision authority
  - actor: Claude Design, Claude Code and Codex
    role: Design review and scoped follow-on prototype work
argument: "In which the supplied LEGO House becomes a parallel entrance to the drafting table; a runnable scroll study and unchanged Blender assets are transferred; the next room-flight and dashboard threshold are specified without claiming production authority."
tags: [design, house-world, drafting-table, motion, accessibility, build-and-tell]
provenance:
  source_artifacts:
    - artifact: Codex local house-world study and direct operator instructions
      captured: "2026-10-11"
      transfer: docs/design/review/HOUSE-WORLD-R0
    - artifact: Claude Design R4 overlay, PR 44
      head: b9867797e9c9b3ae869b0bd8d70698c0d9a12cab
      package_tree_sha256: c3cb674ae15c1dadb70a1e1c66f49c1f5d38330865a01969f1e9ac689ec18486
      limitation: Source review only; missing overlay parents, not an operative cut
    - artifact: H-01 R1 as-committed
      tree_sha256: b5664a2ad0ed7b7c7f093f4a1b369b32095799f73ade2af074b882e8038b9a1d
      source_main: 8aae0d658b0d8ba458f3adcc7ae79d041aaf2298
    - artifact: legoHouse.blend, supplied by the operator
      sha256: 6c0f6f3bb757370979df0a7d6c5951df1f0ef51716f56412b9d2e55338cc0541
    - artifact: Open research issues 33 through 43
      snapshot: docs/design/review/HOUSE-WORLD-R0/references/research-issues.json
  method: "Direct iterative operator review; independently authored Three.js/GSAP/HTML mock prototype; browser checks of the served build; read-only Blender dependency audit; manifest and source-byte validation. Research claims and production architecture remain unverified."
authority:
  decision_owner: James (@ojfbot)
  authorization: "Direct request to bundle the study, additional design brief and all related Blender assets, commit to GitHub, and allocation of 037 plus HOUSE-WORLD R0 and package-local decision IDs."
  boundary: "Publish through a draft PR. No merge, production implementation, design-cut import, real records, live agent work, purchase or family-data collection is authorized by this brief."
register:
  number: 37
  allocated_by: James (@ojfbot), direct Codex instruction 2026-10-11
register_version_read: "2026-09-18.33"
parts:
  "0": Orientation and learning sequence
  "1": What the runnable study proves
  "2": What the next design slice must do
  "3": Inherited handoff and research boundaries
  "4": Transfer, verification and review
---

# The house as an entrance to the drafting table

## §0 Orientation

The Drafting Table already has page identities, work surfaces and evidence rules. This additional study tests a different way of arriving at those pages: the supplied LEGO House is a navigable model whose blocks correspond to work. James selected a parallel entrance, preserving the ordinary Hub.

HOUSE-WORLD R0 is a separate experimental package at `docs/design/review/HOUSE-WORLD-R0/`. It starts its own lineage and uses package-local decision IDs. It neither replaces DT-DESIGN nor fixes the missing parent cuts of the R4 overlay. The register retains authority; this brief and the package are for review.

Start with [the illustrated overview](../design/review/HOUSE-WORLD-R0/overview.html), then the package README. The overview separates the running opening from a labeled concept of the next dashboard threshold.

### Briefing, demo, practice, requirement, debrief

1. **Briefing:** point to the house, page map and work-box/book/bag distinction. Explain that roof colour and a minifig's location do not establish evidence or authority.
2. **Demo:** run the package, scroll into the lobby, watch the tree pieces seat, then open a room with the header finder. The mock work stays local.
3. **Practice:** open BOX, read the book, try the three bags and change a reading after review. Check retained earlier values, reopened dependent work and unchanged physical inventory.
4. **Requirement:** the next slice must provide explicit room flight, a near-full-screen dashboard and an equivalent direct path with motion disabled or WebGL unavailable.
5. **Debrief:** compare task completion and wayfinding with the ordinary Hub. Ask where the metaphor confused work, consent or meaning. Do not infer a builder's story from the model.

## §1 What the runnable study proves

The current package runs with vanilla Three.js, GSAP ScrollTrigger and HTML working sheets. It contains 21 mapped building blocks and 22 mock destinations. BOX shares the Hub's block and denotes a work outcome; it is not the physical inventory-box page.

The opening is compact and recognizable, with the house separate from PLAY WELL. Room and course gaps reveal gradually as scrolling begins. A wider opening camera eases into the previous lobby route at 18% scroll. The route has one broad tree arc, a rear exit and a return to the front. Earlier tight pivots caused whip and were removed.

Seventy-seven wall/roof courses, 15 stair pieces and eight tree pieces move with different completion times. The tree follows connector-aligned seating paths and a final short stroke. This is authored choreography, not a collision solver. Minifigs remain upright in world space while their roofs move; their activities are fictional examples.

The direct header autocomplete borrows the Hailstone interaction precedent. It keeps focus in the input, uses active-descendant navigation, and has literal matching, normal Tab, Enter activation and Escape dismissal. It currently highlights the room; it does not yet expand a focused page preview.

Exactly six chapter labels have one haiku line each. The six subheads form two English 5/7/5 haikus. The build rejects a wrong chapter count, wrong reviewed syllable total or an unreviewed word. Captions have no solid panel, and PLAY WELL alone transitions through pale yellow. View controls stay in View options.

The current sheet is still a left side panel. Its visible working controls demonstrate one local dependency flow, not the full Claude dashboard or production state. This limitation is preserved in the package rather than hidden by the proposed modal illustration.

## §2 What the next design slice must do

### Fly to a room deliberately

Design explicit travel between building blocks and desk-page thresholds. Hover and focus identify or preview a room without moving the camera. Activation chooses the destination. Suspend scroll ownership during a flight, avoid straight paths through solid rooms, retain broad gaze changes and support Escape cancellation. Reduced motion uses direct entry.

Keep the entry bookmark and activating control. Entering a page never changes work, approves a record or discards a draft. Specify interrupted travel, repeated selection and history behavior before production work. Begin with one block to A-01 and back, then prove a second page switch.

### Give the dashboard its space

Replace the side-sheet concept with a near-full-screen modal. Freeze and ghost the house behind it, while giving the foreground the dashboard real estate established in the existing handoff. Preserve page-specific skeletons: a working canvas and exact controls, an answer-focused column, a ruled inventory view or a quiet gate each have different needs.

Queue, Trail, footer and Benny remain optional capabilities. They do not settle Frame topology or ledger ownership. Keep dialog labeling, focus containment, inert background, Escape, exact return focus and retained state. Local changes must not trigger whole-document flashes.

### Add depth with restraint

More parallax and a better background are open design work. Compare a small set of bounded depth layers, using the same reversible scroll clock. Keep working controls still. Test text and room legibility, reduced motion and device cost. The yellow background wash was rejected; the requested sunrise belongs in the letters.

Focused room previews also remain open work. They must be read-only and avoid duplicate live regions, controls or IDs from a miniature sheet. Inline expansion versus a neighboring preview has not been settled by the operator.

## §3 Inherited handoff and research boundaries

PR #44 remains a draft, non-operative R4 overlay. It has no complete inherited union: its parent R3 is unavailable, and its declared manifest and lineage fail admission. Selected source bytes are preserved as read-only references with commit and file hashes. The earlier H-01 package is unchanged.

Typology Identity v2 investigates form, primary act, page skeleton and threshold context. Its navigator/card lift and Benny behavior are research precedent. Workbench Frame demonstrates optional bars, subgrid alignment, container variants and a ripple grammar. The operator's limitation note records a flawed implementation in which whole-board state and document-level View Transitions cause whole-page flashing. Those wireframes require real technical design; their code is not a production foundation.

Issues 33–43 supply open build-and-tell questions. The local study keeps a builder's words separate from brick facts, shows separate models before a shared concept and treats publication consent separately. It does not establish the effectiveness of an AI host or grant permission to collect family material. The private selfco synthesis was not independently verified; the metadata snapshot records the source gap.

Production evidence axes, consent, durable history, dependency events, routing, scene lifecycle and rendering structure remain separate design work. None is settled by a visual sidebar or building block.

## §4 Transfer, verification and review

The package includes the runnable source, local runtime/font assets, grouped GLB, export script, mock fixtures, selected source references, latest captures, specs and both supplied house Blender revisions. `legoHouse.blend` and `legoHouse.blend1` are unchanged, each about 23.8 MB. Blender's read-only audit found no linked libraries or external images. The asset manifest records exact hashes and sizes.

The sibling receipt gives the normative package tree digest and byte/file count, measured with `tools/design_pkg.py digest`. Use repository, path, commit and content digest together for transfer. The directory name is not identity.

Run the commands in [verification](../design/review/HOUSE-WORLD-R0/verification.md). The root pnpm workspace and lockfile supply the prototype dependencies. The schema and package preflight validate structure, not design acceptance or an accepted production pin. An operative import requires a later authorized process and instruments row.

The first implementation review should demonstrate one explicit block flight into the large dashboard, keyboard/reduced-motion equivalence, a second-page draft retained, and return to the original house bookmark. Judge the visual direction before widening routes or changing render structure.

This PR transfers an additional design proposal. James reviews and merges it under the repository rules. A second steward still checks register finalization at the reviewed head; author checks do not replace that gate.
