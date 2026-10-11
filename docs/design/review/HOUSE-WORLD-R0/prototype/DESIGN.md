# House world: navigation study

Status: local, non-operative experiment. It does not change the Drafting Table, the design register, the page schema, or PR #44.

## Brief

Make the existing LEGO House model a parallel entry to Drafting Table pages. A building block is selectable in 3D and through header autocomplete. Selection opens a 2D dashboard beside the current view. Scroll alone owns the flight and assembly. The dashboard is an interaction sketch using the design bundle's page names and tokens, not a copy of the X-01 or W-00 wireframe code.

The gingerbread house photograph is a reference for future visible activity around the building. The supplied `legoHouse.blend` is the geometry reference for this study.

## Visual plan

- Base: Drafting Table paper `#F6F2E9`, sheet `#FDFBF5`, ink `#22303C`, muted `#5E6B76`.
- Accent: `#B84F2B` means the user's current selection or recent change. It does not encode origin, authority, or verification.
- Model: the supplied roof colours remain architectural colour, with no semantic legend.
- Type: locally bundled DynaPuff for PLAY WELL, chapter captions, room names and sheet accent headings. Body text, values and controls retain their readable UI typography. No external font request is required.
- Structure: a full-width sticky model viewport with a graphic wordmark, direct page finding, and sheets opening on the left. The sheet rules and columns follow the Drafting Table language.

## Three distinct directions

| Direction | Interaction | What it could prove | Main risk |
|---|---|---|---|
| House portal | The house opens along a scroll-owned route; selecting a block immediately opens its 2D page beside the retained scene. Direct page finding offers the same destinations. | Whether the physical model improves entry and recall. | Twenty-one block locations may be harder to learn than page names. |
| Exploded systems table | The supplied building blocks separate spatially and assemble during the flight. Their mapping to modules is a proposal; no production dependency topology is implied. | Whether the agent stack becomes legible as a system. | It may turn the house into an architecture diagram and imply unsettled ownership or topology. |
| Builder landscape | Individual ideas sit around the village and remain separate until people compare and merge them. | Whether spatial arrangement supports the build-and-tell loop. | It needs a story, consent, contributor, and merge record that the open research issues have not settled. |

The exploded composition is the current default after the user’s visual feedback. Both house compositions remain a parallel entry. The runnable prototype also exposes the exploded systems table and builder landscape as separate interaction directions via the view selector and variant URLs. Their block ownership, group topology, and collaboration semantics remain research hypotheses.

## Interaction contract for this study

1. The list is usable before and without WebGL. Each item names the destination and whether it is an existing page or an open research concept.
2. Pointer selection and list selection reach the same result. Sheet selection does not move the camera. Scroll owns the flight; reduced motion freezes it.
3. The relevant 2D dashboard takes focus while the scene retains its view. Escape and Back return focus to the originating input or control.
4. The prototype has no agent execution, purchase, publication, merge, or durable save action. All sample work is marked as mock.
5. A builder's account of a model is separate from brick facts. The prototype may ask about a model; it does not tell a builder what the model means. Technical checks describe fit, parts, and cost, without grading the idea.
6. A story or a contributor's proposal never disappears through an automatic merge. A later landscape prototype should make each idea visible before any merge action.

## Research boundary

The issue set is open research intake, not accepted policy. The strongest direct UX implications are:

- [#34](https://github.com/ojfbot/lego-village-pipeline/issues/34): distinguish builder meaning from feasibility facts; test agent phrasing.
- [#35](https://github.com/ojfbot/lego-village-pipeline/issues/35): keep a human host in the family session concept until evidence supports a different role for AI.
- [#36](https://github.com/ojfbot/lego-village-pipeline/issues/36): compare child-centred session methods before fixing a family flow.
- [#37](https://github.com/ojfbot/lego-village-pipeline/issues/37): page and family vocabulary are still under review, so this study reuses existing page titles and uses plain labels for research concepts.
- [#38](https://github.com/ojfbot/lego-village-pipeline/issues/38): a build/story card and session record require a schema decision; no story is persisted here.
- [#39](https://github.com/ojfbot/lego-village-pipeline/issues/39): compare ideas before merge, retaining contributor identity per element.
- [#40](https://github.com/ojfbot/lego-village-pipeline/issues/40): a What-If prompt should come from a cited situation, not a random decorative card.
- [#41](https://github.com/ojfbot/lego-village-pipeline/issues/41): the building might also teach the agent stack to developers, but that is a separate audience test.
- [#42](https://github.com/ojfbot/lego-village-pipeline/issues/42) and [#43](https://github.com/ojfbot/lego-village-pipeline/issues/43): public naming, story consent, attribution, and publishing remain open. This prototype stays local.

The private selfco synthesis is cited in [umbrella issue #33](https://github.com/ojfbot/lego-village-pipeline/issues/33). It was not available from the `ojfbot/selfco` repository's open issues, so this design uses the public issue text as research context.

## Technical hypothesis and measures

Vanilla Three.js plus DOM is the first engine candidate. It needs no React runtime. The Blender scene has 21 named block collections, 1,457 mesh objects, and 250,173 faces including off-scene parts. The export script excludes the off-scene `Collection` and joins building collections while preserving eight tree and fifteen stair parts, producing 103 mesh groups. The current Draco-compressed export is 756,868 bytes; the detailed final view uses 172 draw calls and 232,625 triangles. This is a measured input, not a performance promise.

The scene renders on demand, caps pixel density, and supplies a low-detail model and a 2D index. Test the complete interaction on a lower-power phone and on keyboard-only input before claiming it runs for everyone. Compare initial load, draw calls, frame time during orbit, and the number of wrong destinations chosen against the existing Hub. If the 3D route does not improve finding work, retain it only as an optional exploratory view.

## Research translated into observable interaction

| Open question | Prototype choice | What remains unproved |
| --- | --- | --- |
| #34 builder meaning / agent etiquette | Story words are verbatim. Technical facts occupy a separate column. Benny asks about a model and cannot interpret its meaning or edit state. | Typed turn enforcement and audit across real agent/tool calls. |
| #35–36 facilitator and family method | A human host is named; no automated session leader. The user can build, tell, and compare. | Whether this adaptation works with EH/HH/LH, or whether another child co-design method works better. |
| #37 vocabulary | I-02 concerns physical boxes. BOX is a separate work metaphor study under the Hub. Book and numbered bags teach the bounded delivery sequence. | Whether people understand the two meanings without explanation. |
| #38 build/story record | A separate consent choice precedes showing a story in the local session. Reload clears all data. | The actual schema, consent versioning, record ownership, storage, and export. |
| #39 landscape before merge | Separate model/story panels remain visible; both stories must be heard before a shared-concept preview. | Genuine contributor consent, conflict handling, and per-element provenance in a real shared model. |
| #40 what-if | A wider base after review reopens dependent checks and retains old readings. Inventory remains separate. | The production dependency graph and authority/release semantics. |
| #41 teach the stack | Box/result → book/context → bag/agent work → model/story/evidence is an inspectable diagram. Three sample figures mark activity in the house. | Whether the metaphor accurately teaches the actual harness; the building does not establish package boundaries. |
| #42–43 naming / publishing | The UI calls this a research adaptation, and has no publication or real merge action. | Licensing, public naming, and consent-to-publish workflow. |

## X-01 v2 and W-00 inheritance

The threshold carries page code, plain title, and action verb separately. The selected sheet takes the foreground, with contextual links at the side. Architectural roof colours remain architectural; hatches remain texture. Neither is allowed to silently encode evidence, authority, or ownership. Benny's origin is always visible.

The source frame's whole-page flashing was an implementation defect, not motion direction to reproduce. The current version opens the sheet immediately beside a fixed camera. Scroll drives the model and flight. It does not use document-level View Transitions. World navigation is separate from form controls and the HTML accessibility tree. A real implementation still needs scene lifecycle, routing, a durable event/dependency model, container behaviour, and a measured mobile budget.

The strongest remaining challenge is wayfinding: 21 building modules can conceal destinations. The header autocomplete, explicit roof hover identity, and guided journey keep a direct path while the spatial hypothesis is tested. A usability comparison should measure correct destination, time, wrong-room entries, and recall against the current Hub.

## Current opening motion

The current opening uses continuous, scroll-derived parallax rather than delayed starts. Each animated tree/stair piece and room axis eases from zero immediately, with different completion times. The camera takes one broad interior arc; the requested ground pivot was removed after it caused excessive whip. The larger gradient wordmark settles into its earlier size before fading out. This responds to the user’s latest motion direction; comfort and wayfinding remain user-review questions.

Chapter captions have returned after user review. One caption appears per chapter, fading to zero at the text-change boundaries. The opening wordmark takes precedence, and captions clear while the finder, View options or a sheet is open. Floating flight buttons remain in View options. Flight controls and prototype notes live in View options; the work box is found in the header autocomplete. Seventy-seven grouped wall/roof courses now assemble within the building modules. The tree uses connection-aligned vertical seating and an outside horizontal branch attachment, replacing diagonal trajectories that made pieces appear to intersect.
