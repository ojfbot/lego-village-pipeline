> **HISTORICAL INPUT (marked 2026-09-17).** Superseded where later decisions differ — see `handoff/decisions.md` and HANDOFF-LEGO-PIPE-014. The P/F/H "planned" status lines in this document are stale; `handoff/index.json` is authoritative.

# Handoff to Claude Design: LEGO Village Pipeline — planner UX and design library

**Handoff:** LEGO-PIPE-007-R2 (from: claude-chat + claude-design session, to: claude-design / claude-code)
**Date:** 2026-09-16
**Supersedes:** LEGO-PIPE-007-R1. Folds in what the prototype sessions settled. Changes vs R1 are tagged **[R2]**; everything else carries forward unchanged in intent.
**Purpose:** Project-specific design library and interactive prototypes for the planner, stitched into the Frame host. Output: design system, prototypes, Claude Code handoff package. Production implementation is not authorized.

---

## 0. [R2] What the sessions settled (read first)

| Decision | Status | Where |
|---|---|---|
| Visual system: **Drafting Table** — paper / blueprint dual theme, Spectral + Libre Franklin + Azeret Mono, one shared token file (`dt/tokens.css`) every sheet links. Organic/Carbon/Plex not inherited. | accepted | D-00, D-01, Hub log 09:12 |
| **Principle: every UI is a frictionless teacher of how to use it well.** Plain words first; controls explain consequences; AI questions arrive as conversation (tap / type / talk); no prepositional jargon in titles. | operator-mandated | CLAUDE.md, Hub log 11:36 |
| Family posture: **Workbench Junior** — kids use the real drafting tools, simplified. A proposed scene (stickers, names, lore) is a layout branch with `origin: family · workflow: proposed` and deterministic consequences. | accepted | Hub log 09:41 |
| Gates: **stamps for the record, quiet modals for the act.** Ladder: no gate → reviewed diff → initials + stamp → purchase outside the app. | accepted (operator may override) | Hub log 10:05, C-01 |
| Geometry units: **LDU is the integer base**; whole mode (stud XY, 22.5° track quantum, Z in plates or bricks) vs fraction mode (¼ stud, 0.1°, 1 LDU). Labels follow the chosen unit. | accepted | A-01, Hub log 10:48 |
| Shadows / radii grammar: two-layer "vapor" offset shadow; cards carry three fillets + one **stud corner**; circles reserved for gauges and studs. | accepted | D-01 §02 |
| **Requests are first-class.** Any "+1" (a story ask, an AI suggestion) surfaces in the summary card as an open, traceable item until answered — decline / park / accept, each with reasons and a reply in the requester's words. Nothing is deleted. Requests show **attached work** (model? fit check?) so "words only" is visible. | accepted | C-01, Hub log 12:31 |
| **Basis is a first-class field** on every part row and diagram element: `own-on-arrival · buy-adapted · buy-research · story`. Vendor is per asset (LEGO direct vs BrickLink) and drives every link. Prices are **low–high ranges across available lots**, never a single mid. | accepted | C-01, Hub log 13:24 |
| Options carry worked-out state: `modeled? · fit-checked? · stances[]` (for / against / neutral / caution per stakeholder with a one-line reason). | accepted | C-01 |
| Every value that changes gets one unified, subtle **change pulse** (token-level keyframe) so toggling an option shows its ripple. | accepted | dt/tokens.css, C-01 |
| Part references are interactive everywhere — a **part popover** (image slot, id, colour, basis, use, quantities, BrickLink / Rebrickable / inventory links). | accepted (data flow TBD) | C-01 |
| Decision log: scrollable, minute-stamped, each entry an accordion with inputs, and **blast radius** as interactive chips (⌕ trace tags filter the sheet index; ▤ file chips preview the file inline). | accepted | Hub |
| Cards: grow with content to a per-card cap, then scroll inside; ⤢ expands one card while neighbours collapse to title rows. Full animated grid reflow is an **open design-system session**. | first pass | C-01, D-01 §02 |
| Layer taxonomy split: Foundation = baseplate · MILS core · **snow & groundcover** (covers core internals); Transport = railbed · track; Landscape = **terrain (relief/contour)** · **planting** · **snow (ornament & narrative)**. Schema still to be resolved. | accepted, schema open | A-01 |
| Planting proposals: dashed = proposed (AI or family), solid = placed; PLACE / DROP / ↺ keep proposals on record; **ASK** edits a proposal in natural language and the AI echoes exactly what it changed. | accepted | A-01 |
| All prototype numbers are **MOCK MATH** — real values need Claude Code implementation plus independent agent audit. | standing caveat | A-01, C-01 |
| Slice C re-scoped to **one facet**: matching the train's track to the MILS railbed and buying only the gap + embed parts. Vendor-smart ordering is its own sheet (**P-01 Procurement**, planned). | accepted | C-01, Hub |
| A-01 is doing double duty (model-component interface + layout canvas) — **split**; the viewer must also inspect by design source and brick source. | follow-up | Hub log 13:41 |

## 1. What this product is

Unchanged from R1: a digital twin for a multi-year LEGO Christmas village — snowy modular railway (MILS, R40) around an owned centerpiece tree (LEGO 41843), run by an owned train (LEGO 10254). The software turns designs into validated components, aggregates parts, subtracts owned inventory, produces purchasing artifacts, renders the scene, and reconciles what was actually built. The UI makes state, provenance, validation results, and approval gates legible; deterministic libraries and a CLI do the work.

**[R2] Corrected domain facts (seed all prototypes with these):**
- **10254 Winter Holiday Train** provides a **full circle of track only** (16 × 53400 curves). No straights. Bought from **LEGO direct**. Its track is *owned on arrival* and earmarked for the railbed.
- **bl-741807 (MILS quarter circle R40)** provides the **modular Technic landscape frame and the pieces that attach track to it**. It does **not** include ballast. Used ×4 to carry the circle. Its parts **cannot be bought as listed** — colours must be adapted to the winter palette (e.g. tan → white, dark tan → light bluish gray). Every adapted row records `colour_source → colour_chosen`.
- **Ballast** (single / double plate under the rail) is a **research choice**, in neither source.
- The **Family Christmas Tree (41843)** is owned and built; its 16×16 base is a fixed obstacle for fit checks.

## 2. Frame: host, not skin

Unchanged. Frame provides stitching, routing, shared context, navigation shell, fleet conventions. It does not provide the visual language. **[R2]** The Drafting Table token file is the project's single source of truth; Frame host aliases (theme mode, density, nav slots) map onto `dt/tokens.css` variables. The seam document (H-01) is still owed; list assumptions and integration questions, do not invent a contract.

Token hierarchy: `base primitives → semantic application tokens → LEGO Village domain tokens → Frame host aliases`. **[R2]** Domain tokens now also include: basis (own / adapted / research / story), request state (open / declined / parked / accepted), option state (modeled / fit-checked), stance (for / against / neutral / caution), and the change-pulse keyframe.

## 3–4. Permissions and fixed constraints

Unchanged from R1 (prototypes yes; repo mutation, authoritative schema, production logic, architecture choice — no; `packages/schema` is the contract; DEC-RIGHTS-01; evidence axes; DEC-P01 gates; React/TS/Three.js; WCAG 2.2 AA + nonvisual spatial alternatives).

**[R2] Additional fixed constraints from the sessions:**
- No prepositional-jargon titles ("Evidence to decision" → "When the AI isn't sure").
- No verbose, explanatory AI copy in the UI. Terse. The AI restates what it heard before anything is saved.
- Private listing visibility is a **control**, not a hard exclusion: the *downloaded file* stays operator-only until rights pass; the *listing* may be shown to family.
- Vendor-specific links must be dynamic per asset (LEGO.com product page vs BrickLink catalog/design page).

## 5. Human postures and system actors

Unchanged. **[R2]** Named actors in prototypes: `@jfo` (operator), `@boys` (family stakeholders), `AI`. Tag states are distinct and inspectable: `◇ needed from` · `■ did` · `○ waiting on`.

## 6. Design principles

Unchanged, plus **[R2]**: the teacher principle (§0); requests never slip and never nag; basis before price; choices show their ripple.

## 7. Evidence model

Unchanged (five separate axes, never collapsed). **[R2]** Plain-language presentation adopted on B-01: WHO WROTE IT · HOW · HOW SURE · WHO DECIDED · STATUS, full chain behind disclosure. Chips read `◇ AI GUESS`, `■ MACHINE-CHECKED`, `■ CONFIRMED`, `▲ CORRECTED`, `○ ON HOLD`.

## 8. Canonical synthetic scenario

Unchanged (synthetic-r40-snowy-quadrant, bl-741807 reference). **[R2]** The ambiguity to exercise in B: the creator's "for 4 tracks" means four track *pieces* forming one curve, not four parallel tracks — the AI's literal reading is the thing the human corrects.

## 9. User journeys (J1–J13) — with [R2] screen assignments

- **J1 Reference intake & triage** → B-01 (rights, acquisition trail, listing visibility control).
- **J2 Source acquisition** → B-01 FILES & LINKS (browser download → drop → hash; immutable artifact; operator-only until rights pass).
- **J3 Component extraction** → A-01 viewer + layer rig (split follow-up; inspect by design source and brick source).
- **J4 Layout composition** → A-01 canvas (drag + exact entry, whole/fraction, plates/bricks, endpoint match, planting proposals, versioned save).
- **J5 Theme / snow policy** → D-01 ThemeDiffRow specimen; **[R2]** colour adaptation of source parts (C-01) is J5 in miniature.
- **J6 BOM, inventory, shortage** → C-01 parts list by basis (inventory layer later).
- **J7 Procurement release** → C-01 approval trail + **P-01 Procurement (planned)**.
- **J8 Render review** → C-01 "Does it fit?" (Studio + Blender) — dedicated sheet later.
- **J9 Measurement capture** → planned (MeasurementCapture specimen in D-01).
- **J10 As-built reconciliation** → planned.
- **J11 Story graph** → C-01 chain back to the story; F-01 Workbench Junior study (planned).
- **J12 Agent handoff review** → Hub decision log (blast radius, inputs, file previews).
- **J13 Year-over-year** → planned (versions list in A-01 is the seed).

## 10. Data the UI consumes

Unchanged entities. **[R2] Schema requests accumulated** (recorded, never authored):
- `Component.layers` as a tree, not a flat enum; `disassembly_rank` per submodel; per-brick strata membership (build order derivable).
- `Component.placement` = integer stud position + 22.5° rotation steps; Z in LDU with unit preference.
- `ClarificationRequest {field, question, options[], evidence_refs[]}`; `DecisionRecord ↔ field-level link`.
- `Request {from, asks, attached_work[], status, reasons[], reply}`.
- `PartRow {part, colour_source, colour_chosen, basis, from_asset, author}`; `Earmark {part, qty, from_asset, to_model}`.
- `Asset {vendor, product_url}`; `PriceObservation {part, vendor, price, qty_available, observed_at}`.
- `Option {modeled_ref, fit_ref, stances[]}`; `FitmentCheck {rule, tool, status, evidence_ref}`; `Ask {who, what, why, due, resolved_by}`.
- `Planting {id, position, scale, status: proposed|placed|removed, origin, edits[]}`.
- `Part ↔ InventoryLot[]` with lifecycle {owned, in-cart, planned-for, built-into} (later layer).

## 11. Prototype scope — [R2] status

- **A-01 Layout Canvas** — built. Drag + exact entry, whole/fraction, plates/bricks, 8-strata layer rig, planting proposals with ASK, synced 3D viewer with engine. Follow-up: split into model-component interface vs canvas; add source facets.
- **B-01 When the AI isn't sure** — built. Conversation (tap / type / talk), paper trail, files & links, listing visibility control.
- **C-01 Railbed: own, adapt, buy** — built, landed. Hero by basis, choices with worked-out state, requests first-class, parts list by basis with popovers, approval trail with @tags, chain back to the story, ranged costs → P-01.
- **P-01 Procurement** — planned (vendor lot grouping, shipping, minimums; purchase stays on BrickLink).
- **F-01 Workbench Junior** — planned (story-driven forking).
- **H-01 Frame seam + schema requests + Claude Code handoff** — planned.

## 12. Screens, components, tokens, states, accessibility

Unchanged lists, plus **[R2]** domain components added: `RequestCard` (open / declined / parked / accepted, reasons, reply, attached work), `StanceChip`, `OptionStateRow` (modeled / fit / delta), `PartPopover`, `BasisChip`, `PlantingRow` (proposed / placed / dropped, ASK), `ChangePulse` (token keyframe), `DecisionLogEntry` (inputs, blast radius: ⌕ trace / ▤ file). Card behaviour spec in D-01 §02; animated grid reflow is an open session.

## 13. Responsive behavior

Unchanged.

## 14. Answers to R1's questions

1. Design language: **custom — Drafting Table** (argued and chosen from three built candidates).
2. Frame seam: still owed as H-01; assumptions to be listed, not a contract.
3. Compact evidence: plain-language five-row trail + chips (B-01).
4. Canvas model: integer LDU base; whole/fraction modes; drag and exact entry coexist, both snap (A-01).
5. Operator ↔ family: same tools, simplified (Workbench Junior); family proposals are layout branches with basis `story`.
6. Token grammar: `--dt-*` base/semantic/domain in one file; host aliases map onto it.
7. Slice order: A first (built), then B, then C — all three built.

## 15. Requested output — [R2] remaining

1–5, 7 delivered in part (D-00, D-01, A/B/C). Still owed: **6** journey map J-01 · **8** family study F-01 · **9** responsive spec · **2/10/11/12** as H-01 (seam, schema requests consolidated, operator decisions, Claude Code package) · P-01.

## 16. Non-goals

Unchanged.

```yaml
handoff_id: LEGO-PIPE-007-R2
supersedes: LEGO-PIPE-007-R1
date: 2026-09-16
objective: Same as R1, updated with settled decisions, corrected domain facts, and remaining scope
acceptance_criteria_additions:
  - teacher principle visible on every sheet (plain-words opener, consequence-explaining controls)
  - requests surface until answered; decline/park/accept recorded with reasons and reply
  - basis on every part row; vendor-dynamic links; ranged prices
  - option worked-out state (modeled / fit) and stances visible before approval
  - layer taxonomy split as §0; planting proposals distinguishable from placed
  - all numbers labeled mock pending Claude Code + independent audit
```
