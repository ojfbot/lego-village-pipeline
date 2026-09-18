# Independent review — Claude Design bundle (LEGO-PIPE-007-R2 → H-01)

**Reviewer:** Claude (Cowork), independent of the design session
**Reviewed:** `Initial LEGO Village Pipeline Design Bundle.zip` — 72 files, 8.0 MB, dated 2026-09-17
**Scope:** package integrity · design system & accessibility · domain correctness · product substance · build-readiness for Claude Code
**Posture:** this is a rough-fidelity starting point by the operator's own framing. Findings are graded against *"can Claude Code build from this without inventing"*, not against production polish.
**Intended use:** reconcile against the ChatGPT review, then fold the surviving items into the Claude Code handoff.

---

## 1. Verdict

**The thinking is well ahead of the artifact.** The conceptual work — evidence axes kept separate, requests as first-class and never deleted, basis before price, gates as stamps vs. modals, the sticker→envelope→model chain, RESEARCH-01 filed instead of guessed — is the strongest part of this bundle and I would not renegotiate any of it. That layer is genuinely ready to build against.

**The package mechanics are not yet handoff-grade.** `index.json` — the machine-readable entry point the README tells every downstream agent to use — does not resolve a single path as shipped. The "self-contained, open in any browser, no server" prototypes require internet access to unpkg.com and Google Fonts. The token file ships colors that fail the WCAG 2.2 AA constraint the brief declares fixed. These are cheap to fix and expensive to leave, because Claude Code will hit all three in its first hour.

**The riskiest substantive gap is F-01's responsive state.** The family workbench is the only sheet with non-operator users (two kids, on a tablet), and it is the one sheet whose target device has no designed layout. Everything else can ship rough; that one can't.

**Recommended disposition:** do not send this to Claude Code as-is. One short remediation pass (§3 P0 items, ~half a day of design-session work) makes it a clean handoff. Then gate the build behind `packages/schema` landing first (§6).

---

## 2. What's working — keep these, don't let reconciliation erode them

| | Why it matters |
|---|---|
| **Decision ledger with blast radius** (`decisions.md`) | Dated, append-only, each entry naming what it touched. This is the single best artifact in the bundle and the reason a third party can review it at all. |
| **Requests never deleted** (decline / park / accept, with reasons + reply in the requester's words) | Correctly models a family process, not a ticket queue. The "attached work" field — making *words-only* visible — is a sharp detail. |
| **Basis as a first-class field** (`own-on-arrival · buy-adapted · buy-research · story`) | Right primitive. It carries provenance, cost consequence, and trust in one field, and it survives into procurement. |
| **Prices as ranges; purchase stays outside the app** | Honest about BrickLink lot reality and avoids a payments surface entirely. Correct scope discipline. |
| **Schema *requests*, not authored schema** | The right posture for a design session. Preserve it — see §6 for how to close it properly. |
| **RESEARCH-01 filed rather than resolved** | Recognising that "8 parts, 288 pieces" is a vocabulary bug and not a copy bug is good judgment. Don't let anyone short-circuit this with a guess. |
| **Token discipline inside the prototypes** | `var(--dt-*)` used 169–414× per sheet; raw hex is confined to the token file and the bundler's own chrome. The prototypes actually honour the "no hex in app code" rule they're asking the repo to adopt. |
| **Reduced-motion respected** | Global duration clamp in `tokens.css`, plus A-01 rendering stills. Rare to see this in a prototype. |

---

## 3. Findings

Severity: **P0** = blocks handoff · **P1** = fix before the affected screen is built · **P2** = record and schedule.

### A. Package integrity

**R-01 · P0 · `index.json` paths are all wrong by one level.**
Every path in `index.json` is prefixed `handoff/` (`handoff/specs/A-01-layout-canvas.md`, `handoff/standalone/Hub.html`, …), but `index.json` itself lives *inside* `handoff/`. All 68 referenced paths fail to resolve from the file's own location; the inverse-check shows all 72 real files as "unreferenced". The one artifact explicitly designed for machine consumption is the one that doesn't work.
→ Strip the `handoff/` prefix, or move `index.json` to the zip root. Add a CI check that every path in the index exists.

**R-02 · P0 · The standalone prototypes are not self-contained.**
README §5 and the file table both claim "open in any browser, no server" / "self-contained offline copies". All nine load React 18.3.1 UMD from `unpkg.com` and fonts from `fonts.googleapis.com` at runtime. Offline, or behind a locked-down network, they render the bundler's loading chrome and nothing else. They are also ~600–840 KB each of minified bundler runtime plus an opaque encoded payload — reviewable only by clicking, not by reading or diffing.
→ Either inline React + fonts and re-verify offline, or delete the offline claim from the README and state the dependency explicitly. For ChatGPT's review in particular, assume it could not actually run these.

**R-03 · P1 · `index.json` under-delivers what the README promises.**
README §6 describes it as mapping "sheets ↔ journeys ↔ components ↔ requests ↔ decisions". It contains sheets, journeys, components, and *file paths* to the ledgers — there are no decision entries and no schema requests in structured form. The 13 decisions and ~25 schema requests exist only as prose tables.
→ Either promote decisions and schema requests into the index as arrays with stable IDs, or correct the README. Given R-05, promoting them is the better call.

**R-04 · P1 · `index.json` names the wrong token path.** `"tokens": "dt/tokens.css"`; the file ships at `tokens/tokens.css`. Same class of error as R-01.

**R-05 · P1 · Decisions have no IDs.**
`decisions.md` says "only the operator overturns an entry; overturning adds a new entry, never edits one" — but entries are addressable only by timestamp (`09-17 12:10`). Nothing in code, a commit message, or a ChatGPT reconciliation note can cite one durably. The brief already uses IDs elsewhere (`DEC-RIGHTS-01`, `DEC-P01`), so the convention exists and wasn't applied.
→ Assign `DEC-001`…`DEC-013` now, oldest-first, before anything cites them. Retrofitting after the build starts is much worse.

**R-06 · P2 · Screenshot set is incomplete and inconsistent.** `states/09-f01.jpg` exists on disk but appears in neither `STATES.md` (29 rows) nor `index.json` (29 entries). All 44 captures are 924×540 viewport crops, not full-page — below-the-fold content on every sheet is unreviewable. README partially disclaims this ("recognition, not measurement"), but a reviewer who can't run the prototypes (see R-02) has no way to see most of each sheet.
→ Re-capture full-page, or state plainly that the screenshots cover the fold only.

### B. Design system & accessibility

**R-07 · P0 · The token file ships colors that fail the declared WCAG 2.2 AA constraint.**
Computed against `--dt-sheet` / `--dt-bg`:

| Token | Paper theme | Blueprint theme | Role |
|---|---|---|---|
| `--dt-accent` (#C65A33) | **4.13 / 3.83** — fails AA normal text | 4.73 / 5.35 — passes | primary action, links, borders |
| `--dt-prov` (#B07C10) | **3.54 / 3.28** — fails | 6.63 / 7.50 — passes | provisional / ◇ AI GUESS |
| `--dt-unres` (#A8B0B8) | **2.12 / 1.96** — fails badly | **2.93 / 3.31** — fails | unresolved state |
| `--dt-block` (#C0392B) | 5.26 / 4.87 — passes | **4.27** on sheet — large-text only | blocked / error |

The brief names "WCAG 2.2 AA + nonvisual spatial alternatives" as a **fixed constraint** (§3–4), so this is a constraint violation, not a preference. Mitigating: evidence state is also carried by glyph (◇ ■ ▲ ○), so meaning isn't color-only. Aggravating: `--dt-accent` is the primary action color in the theme the operator uses by default, and `--dt-prov` is the AI-guess color — the two that most need to read clearly.
→ Darken the paper-theme accent and provisional values (the `-deep` variants already pass — `--dt-accent-deep` is 5.91). Decide explicitly whether `--dt-unres` is ever text or only ever a fill. Add a contrast assertion to `packages/tokens` so this can't regress.

**R-08 · P1 · No `<html lang>` and no viewport meta on any of the nine sheets.**
Screen readers get no language; mobile browsers get desktop-width emulation. Both are one line. Relevant because `responsive.md` names a phone target and the bundle claims AA.

**R-09 · P1 · ARIA coverage is uneven and thin.** Per sheet: F-01 has 36 aria attributes and A-01 has 19; Hub has **zero**, D-01 has one. Only A-01 has keyboard handlers. `aria-live` is present on 5 of 9 sheets — notably absent from Hub, P-01 and J-01, which all mutate content in place (decision log expansion, plan re-pricing, journey filtering).
→ The prototypes' code isn't being copied, so treat this as a *spec* gap: the per-sheet specs don't state announcement behaviour. Add a "what gets announced" line to each spec, especially P-01 (plan re-priced) and A-01 (canvas placement, which needs the nonvisual spatial alternative the brief mandates and no one has specced).

**R-10 · P1 · Emoji as domain iconography (F-01 sticker palette).**
🎄 🐴 ⛄ 💡 are used as the sticker glyphs. These render differently per OS and font, have no size/stroke control, don't inherit theme color, and read inconsistently against both paper and blueprint. D-01 already lists iconography as open — this is the concrete instance.
→ Decide: commissioned glyph set in `packages/ui`, or explicitly accept emoji and document the fallback. Given this is the kid-facing surface, it's worth real glyphs.

**R-11 · P2 · Layout defects visible in the handoff captures.** A-01 and C-01 sheet titles wrap and collide with the meta row at 924 px; C-01's "IN THE VILLAGE" toggle label is clipped; C-01's schematic has overlapping labels ("VILLAGE / MILS MODULE / BUY · ADAPTED"). Micro-labels are ~10 px mono small-caps throughout, which is at the legibility floor.

### C. Domain correctness & internal consistency

**R-12 · P0 · MILS module size contradicts itself across sheets.**
`schema-requests.md` caps a sticker envelope at "32 × 32 studs (**one MILS module**)". A-01's canvas labels its MILS units "**48×48 · MILS**". One of these is wrong, and the disagreement is load-bearing — it sets the envelope grid, the fit checks, the R40 ring math, and what a "unit" means in the layer rig.
→ Settle before any geometry code. This belongs in RESEARCH-01's scope (question 2 already asks what MILS calls its 32×32 units) but it's a factual conflict, not a vocabulary preference, and shouldn't wait on the full glossary.

**R-13 · P1 · The "Rail" / "Ring" drift is already live in shipped copy.**
Decision `09-17 12:10` records "Rail" as the placeholder on F-01's layer toggle. In `states/03-f01.jpg` the toggle reads **Rail** while the readouts in the same viewport read "overlaps **the ring** — fit check" and "inside **the ring**, by the tree". Two names for one thing, three inches apart, on the kid-facing sheet.
→ Exactly the failure mode RESEARCH-01 exists to prevent, which strengthens the case for landing it before build. In the interim, pick one string and use it everywhere.

**R-14 · P1 · F-01's mock math produces visibly nonsensical values, presented as if valid.**
`states/03-f01.jpg`: "ENVELOPE · STUDS **104** of **−10,300 free**" and a tree at "**−50 bricks**". Negative free area and negative height are not plausible-but-unverified numbers — they're broken. The "all numbers are MOCK MATH" caveat covers *unaudited*; it doesn't cover *arithmetically impossible*, and shipping them in the handoff captures trains a reader to stop looking at the numbers.
→ Either fix the mock so every displayed value is plausible, or annotate the capture. More importantly: the audit spec (§6) needs a "no impossible values" invariant, not just "verify against real math".

**R-15 · P1 · P-01's core interaction is unfalsified by its own mock data.**
The sheet's premise is "each choice shows the order it would produce *before* you pick it". In `p01-paper.jpg`, all three priorities — lowest total, fewest parcels, here soonest — produce **identical** outcomes: 2 shops, $57.54–$62.34, ~9 days. The one screen whose value is showing a trade-off currently demonstrates that there isn't one.
→ Re-seed the mock shop set so the three priorities genuinely diverge (they must, or the feature doesn't earn its place). This also matters for reviewing the algorithm: a reviewer can't tell whether the scoring works.

**R-16 · P1 · A-01's "3D viewer" is not 3D, and Three.js is unvalidated.**
`repo-structure.md` names Three.js a fixed constraint and the A-01 spec says "synced 3D viewer **with engine**". No prototype contains a `<canvas>`, a WebGL context, or any Three.js reference — the massing views are SVG (A-01's viewer, F-01's side elevations). Nothing in the bundle exercises the 3D approach.
→ Fine as a scope decision; not fine as an unstated one. Either correct the A-01 spec to say "SVG massing, 3D deferred", or make "prove the Three.js viewer" an explicit early Claude Code spike with its own acceptance criteria. The layer rig + separation peel + synced visibility is a non-trivial thing to get right in a real engine.

**R-17 · P2 · Sheet titles violate the naming rule inconsistently.** The operator-mandated rule is plain-language titles. F-01 complies ("Family Workbench"). A-01, C-01 and P-01 still read "**Prototype A** — Layout Canvas", "**Prototype C** — Railbed…", "**Prototype P** — Buying the gap". Cosmetic, but it's the one rule the ledger says is operator-mandated.

**R-18 · P2 · Component lists disagree.** `repo-structure.md` lists 10 components for `packages/ui`; `index.json` and the D-01 spec list **15** (adds ApprovalGate, EvidenceChips, SegmentedLine, StatusLine, ActionLog). Claude Code will build from `repo-structure.md` and silently drop five.

### D. Product substance

**R-19 · P0 · The family surface has no designed layout for its actual device.**
`responsive.md` is explicitly "not designed — statement of intent". F-01 is "tablet fidelity, rough". The operator sheets can live at laptop width indefinitely; F-01 cannot, because its users are two kids on an iPad and the sheet's whole interaction model is touch (arm → ghost preview → tap to drop → drag corner to resize → pan). The collapse rules in `responsive.md` are sensible but untested, and the hardest parts are listed under "not covered": pinch zoom, keyboard placement, screen-reader flows for the canvas.
→ This is the highest-value next design cycle, ahead of the A-01 split. Recommend F-01 iPad landscape + portrait get a dedicated session before Claude Code touches the family app.

**R-20 · P1 · Q3 asks Claude Code to design, not build.**
`open-questions.md` Q3: "A-01 split — decision: spec only in this handoff; **build as two screens in code**." There is no spec for either screen. The component-viewer half has genuinely new requirements (inspect by design source *and* brick source, both faceted) with no wireframe, no state list, no copy. Owner is listed as "Claude Code (build) · design session (review)", which inverts the bundle's own rule that production is authorized only through the design package.
→ Either spec the split, or descope A-01 to the existing single sheet for v1 and schedule the split.

**R-21 · P1 · No vendor-data rights position.**
Q9 covers rights review for *downloaded designs*. Nothing covers **BrickLink data**: P-01's real implementation wants price-guide and store-inventory fetches (Q6), the parts list wants catalog images in the part popover, and links point at `bricklink.com` and `rebrickable.com` throughout. BrickLink's API terms, rate limits, and image-hosting rules are a hard external constraint on P-01's architecture — and the one thing in this project that could genuinely block a feature.
→ Add as an open question with owner = research agent, resolved before P-01 is built. It may change the procurement design (cached observations with `observed_at` — which `PriceObservation` already anticipates — vs. live fetch).

**R-22 · P2 · The gate ladder ends in an unverifiable step.** "Purchase stays outside the app" is correct scope discipline, but it means `Order.external_id` is operator-typed and unvalidated, and `InventoryLot.lifecycle: ordered → owned` depends entirely on someone coming back and saying so. P-01 already handles part of this (MARK ORDERED, UNDO until shipped). Worth an explicit decision on what happens when reconciliation never occurs — the stale-order case will happen every year.

**R-23 · P2 · No acceptance criteria per sheet.** The specs describe behaviour and states well, but nothing says what "done" means. The R2 brief has six acceptance criteria for the *design*; there are none for the *build*. Claude Code will need these, and writing them is design work, not engineering work.

### E. Build-readiness

**R-24 · P0 · There is no schema, and the requests aren't specific enough to become one without invention.**
This is the structural gap. `schema-requests.md` is good prose, but Claude Code cannot produce types from it without deciding: are envelope dimensions integers in studs or LDU? Is `Envelope.position` the same coordinate space as `Component.placement`? Is `Request.attached_work[]` a union of Studio file / photo / wand proposal, or a free reference? What identifies a `Part` — BrickLink part ID, design ID, or element ID (part + colour)? RESEARCH-01 answers the last one, and until it lands, `PartRow` can't be typed at all.
→ **Recommended gate:** Claude Code's first deliverable is `packages/schema` as TypeScript + runtime validators derived from `schema-requests.md`, with every ambiguity surfaced as an explicit question — and **no screen is built until James reviews it**. This preserves the "schema is the contract, never authored by design" rule while actually producing the contract. Naming of scale words stays neutral (`Item`, `Unit`) with TODO tags per `repo-structure.md`.

**R-25 · P1 · The Frame seam is assumptions-only, and two of them are architectural.**
`seam.md` is appropriately labelled "not a contract", but two questions can't be deferred past the first sprint: *does Frame own the decision log or do sheets post to it* (determines whether `decisions.md` has a runtime counterpart at all), and *where does the family posture live — role-gated sheets or a separate surface* (determines whether `apps/planner` and `apps/family` share a deployment, an auth model, and a request queue). `repo-structure.md` has already assumed the answer to the second by splitting the apps.
→ Get these two answered before the repo is scaffolded; the rest can stay open.

**R-26 · P1 · The audit surface is asserted, not specified.**
`audits/` is "independent agent audits of every MOCK MATH replaced by real math" — but nothing says what an audit checks, who runs it, or what makes one pass. The deterministic pieces (R40 ring math, envelope fit, endpoint mate, shop-combination search) are exactly the kind of thing that should be property-tested, not eyeballed.
→ Per deterministic library, specify: invariants (e.g. no negative free area — see R-14), a golden-case set, and determinism/tie-breaking rules for the procurement optimiser (identical-cost subsets must resolve the same way every run, or the approval trail is meaningless).

**R-27 · P2 · P-01's algorithm sketch needs its edges written down.** "Exhaustive over shop subsets (n ≤ ~12; heuristic beyond)" is 4,096 subsets — trivially fast, fine. The unstated parts are the ones that bite: tie-breaking, how minimum-order shortfall is charged when a shop is *nearly* met, how postage ranges compose across shops (the displayed range is presumably min-of-mins to max-of-maxes, which overstates spread), and what "uncovered parts" does to a subset's score. All are decisions with user-visible consequences.

---

## 4. Disagreements worth registering

Not defects — places where I'd argue the other side, for the operator to settle.

1. **"Never deleted" requests will accrete.** Decline/park/accept with reasons is right, but over a multi-year project with two kids proposing scenes, the C-01 request card will fill with parked items. There's no archive, no aging, no "this season / past seasons" axis. I'd add a time or season dimension to `Request` now rather than retrofit it in year two.

2. **The evidence-chip vocabulary may be one term too many.** ◇ AI GUESS · ■ MACHINE-CHECKED · ■ CONFIRMED · ▲ CORRECTED · ○ ON HOLD — two of five share a glyph (■), and MACHINE-CHECKED vs CONFIRMED is the distinction most likely to be misread under pressure. Worth a usability check with the actual family before it's built into `packages/evidence`.

3. **F-01's four-step flow may be one step too long for the audience.** Pick → place → tell its story → model it. Step 4 (Studio file / photos / wand) is an adult-shaped task sitting at the end of a kid-shaped flow. Consider whether "send it to James" should be available after step 3, with modelling as an optional return visit. The action log and request card already support that shape.

4. **I'd question "Family Workbench" as tablet-only.** The kids will want to look at their scene on a phone. `responsive.md` puts phone at read-only, which is probably right — but "see my scene" read-only on phone is a real feature, not a degraded fallback, and deserves designing as such.

---

## 5. Reconciliation ledger

For merging with the ChatGPT review. Suggested handling: any finding either review raises stays in unless the other actively refutes it; agreement raises confidence, not severity.

| ID | Finding (one line) | Sev | Mine | ChatGPT | Reconciled sev | Owner | Disposition |
|---|---|---|---|---|---|---|---|
| R-01 | index.json paths off by one level | P0 | ✓ | | | design session | |
| R-02 | Prototypes need unpkg + Google Fonts; not offline | P0 | ✓ | | | design session | |
| R-07 | Token colors fail declared AA constraint | P0 | ✓ | | | design session | |
| R-12 | MILS module 32×32 vs 48×48 contradiction | P0 | ✓ | | | operator / research | |
| R-19 | F-01 has no designed layout for its target device | P0 | ✓ | | | design session | |
| R-24 | No schema; requests not typable without invention | P0 | ✓ | | | Claude Code + operator | |
| R-03 | index.json under-delivers README's promise | P1 | ✓ | | | design session | |
| R-04 | index.json token path wrong | P1 | ✓ | | | design session | |
| R-05 | Decisions have no stable IDs | P1 | ✓ | | | design session | |
| R-08 | No lang / viewport on any sheet | P1 | ✓ | | | Claude Code | |
| R-09 | ARIA + live-region coverage uneven; not specced | P1 | ✓ | | | design session | |
| R-10 | Emoji as domain iconography | P1 | ✓ | | | design session | |
| R-13 | Rail/Ring drift live in shipped copy | P1 | ✓ | | | research (RESEARCH-01) | |
| R-14 | Mock math shows impossible values (−10,300 free) | P1 | ✓ | | | design session | |
| R-15 | P-01's three priorities produce identical outcomes | P1 | ✓ | | | design session | |
| R-16 | "3D viewer" is SVG; Three.js unvalidated | P1 | ✓ | | | Claude Code (spike) | |
| R-20 | Q3 asks Claude Code to design the A-01 split | P1 | ✓ | | | operator | |
| R-21 | No BrickLink vendor-data rights position | P1 | ✓ | | | research | |
| R-23 | No per-sheet acceptance criteria | P1 | ✓ | | | design session | |
| R-25 | Two Frame seam questions are architectural | P1 | ✓ | | | Frame team | |
| R-26 | Audit surface asserted, not specified | P1 | ✓ | | | Claude Code + operator | |
| R-06 | Screenshot set incomplete (09-f01), fold-only | P2 | ✓ | | | design session | |
| R-11 | Layout defects in handoff captures | P2 | ✓ | | | design session | |
| R-17 | "Prototype A/C/P" titles violate naming rule | P2 | ✓ | | | design session | |
| R-18 | Component lists disagree (10 vs 15) | P2 | ✓ | | | design session | |
| R-22 | Order reconciliation unverifiable / stale orders | P2 | ✓ | | | operator | |
| R-27 | P-01 algorithm edges unspecified | P2 | ✓ | | | Claude Code | |

---

## 6. Recommended sequence

If the reconciled findings hold, this is the order I'd run it:

1. **Remediation pass on the package** (design session, short) — R-01, R-02, R-03, R-04, R-05, R-06, R-17, R-18. Mechanical; makes the bundle trustworthy to an agent.
2. **Settle the two factual conflicts** (operator) — R-12 (MILS size) and R-16 (is Three.js in v1 or not). Both change what gets built first.
3. **Token contrast fix** (design session) — R-07, with an assertion in `packages/tokens` so it can't regress.
4. **RESEARCH-01 lands** (research agent) — unblocks `PartRow`, every count label, and R-13.
5. **Schema gate** (Claude Code → operator review) — R-24. `packages/schema` + validators, ambiguities surfaced as questions, nothing else built until James signs it.
6. **F-01 responsive design cycle** (design session) — R-19, plus R-10 glyphs. Ahead of the A-01 split.
7. **Then build**, geometry-first (`packages/geometry` with property tests per R-26), because the fit checks are what every other sheet reads from.

Items that can run in parallel without blocking anything: R-21 (BrickLink rights research), R-25 (Frame seam questions to the Frame team), R-23 (acceptance criteria).

---

## 7. Open questions this review can't settle — for James

1. **MILS unit size** — 32×32 or 48×48 for the R40 quadrant modules? (R-12) Everything geometric waits on this.
2. **Is the Three.js viewer in v1?** (R-16) If yes it deserves an early spike; if no, correct the A-01 spec and `repo-structure.md`.
3. **A-01 split: spec it, or descope it?** (R-20) I'd descope for v1.
4. **Does Frame own the decision log at runtime, or is `decisions.md` a docs-only artifact?** (R-25) Changes whether the Hub is a real screen or a rendered file.
5. **One app with role gates, or two apps?** (R-25) `repo-structure.md` has already assumed two.
6. **How far do you want the offline claim honoured?** (R-02) Inlining React and fonts is easy but makes each sheet ~1 MB heavier; dropping the claim is free.
