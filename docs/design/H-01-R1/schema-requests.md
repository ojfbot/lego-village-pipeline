# Schema requests (consolidated)

These are requests against `packages/schema`, never authored here. Grouped by entity. Each names the sheet that needs it.

## Geometry & placement
- **WITHDRAWN (014 §7.1):** ~~`Component.placement` = integer stud position + 22.5° rotation steps~~ — cannot represent ¼-stud fraction mode; `clear_height: bricks` abandons the integer base. **Replaced by:** canonical **integer LDU for X, Y and Z**; studs / plates / bricks are display preferences only; rotation persisted in its own explicitly declared unit, independent of position. The 2D canvas and the 3D viewer read this one representation (K-3). — A-01
- Envelopes (014 §7.4): a single w × h × clear-height box is insufficient under branches and around curved track — request footprint geometry, orientation, keep-out zones, height/clearance profiles. — F-01, A-01
- Build order (014 §7.5): `disassembly_rank` alone cannot derive every valid assembly order — request a dependency graph. — A-01
- Module groups (K-2): how a *group* of standard MILS modules acting as one substrate is named, addressed and selected; placeholder "Section" until RESEARCH-01. — A-01
- `Component.layers` as a tree (Foundation: baseplate · MILS core · snow & groundcover; Transport: railbed · track; Landscape: terrain · planting · snow ornament & narrative), not a flat enum. — A-01
- `disassembly_rank` per submodel; per-brick strata membership (build order derivable, not stored). — A-01
- `Envelope { footprint: {w, h} studs, position, clear_height: bricks }` on every placed thing; `Model.fits(envelope)` as a fitment check. — F-01, A-01
- `Sticker { kind, glyph, label, story, envelope, origin: family, status: proposed }` → story-graph node (J11). Envelope capped at 32 × 32 studs (one MILS module) for now. — F-01
- `Planting { id, position, scale, status: proposed|placed|removed, origin, edits[] }` — A-01
- `RailRightOfWay` — the clear studs the train needs beside the rail (name pending RESEARCH-01). — F-01

## Evidence, decisions, requests
- `ClarificationRequest { field, question, options[], evidence_refs[] }`; `DecisionRecord ↔ field-level link`. — B-01
- `Request { from, asks, attached_work[], status: open|declined|parked|accepted, reasons[], reply }` — never deleted. — C-01, F-01
- `Ask { who, what, why, due, resolved_by }` — C-01
- `Option { modeled_ref, fit_ref, stances[] { who, stance: for|against|neutral|caution, reason } }` — C-01
- `FitmentCheck { rule, tool: studio|blender|manual, status, evidence_ref }` — C-01
- `ActionLog { t, kind: place|move|resize|turn|remove|sticker|model|send|reset|undo, text, before_snapshot? }` per scene — basis for versions, undo, telemetry. — F-01
- `Conversation { turns[], changes[] }` attached to a plan (P-01 ask box; A-01 ASK; B-01). — P-01, A-01, B-01

## Parts, basis, procurement, inventory
- **WITHDRAWN (014 §7.2):** ~~`PartRow.basis: own-on-arrival|buy-adapted|buy-research|story`~~ fuses four axes. **Replaced by** four stored axes on the row — `acquisition: inventory·included_with_set·buy·fabricate` · `transformation: unchanged·recoloured·substituted·adapted` · `epistemic_state: asserted·inferred·measured·computed·verified` · `disposition: proposed·reviewed·approved` (with revision + supersession) — and two **derived** from the parent Design / Request: `need_origin` and `design_origin`. Open: whether `need_origin` must be row-level (returned to ChatGPT; UI must not assume either). A BOM row is a *demand*; fulfilment is never a row state — orders, receipts, inventory lots and allocations satisfy quantities against it. The UI composes one plain-language summary from all of this; users never meet the enums. — C-01, P-01
- `Earmark { part, qty, from_asset, to_model }` — C-01
- `Asset { vendor: lego|bricklink, product_url }` — vendor drives every link. — C-01
- `PriceObservation { part, vendor, price, qty_available, observed_at }` — ranges are low–high across lots. — C-01
- `VendorLot { shop, part, colour, qty_available, price, min_order, ship_est_lo, ship_est_hi, ship_days, observed_at }` — P-01
- `Order { shop, lots[], external_id, placed_at, placed_by }` — P-01
- `VendorProfile { shop, past_orders[], rating, issues[], preference }` from account history. — P-01
- **WITHDRAWN (014 §7.3):** ~~`InventoryLot.lifecycle: owned | in-cart | ordered | planned-for | built-into`~~ — `ordered → owned` skips shipping, receipt, inspection, discrepancy and allocation. **Replaced by** separate dimensions: acquisition · possession · inspection · availability · allocation · location · condition. "Available" exists only after receipt and reconciliation; availability = accepted quantities less holds; allocation is a quantity-bearing relation inventory ↔ baseline demand. — P-01, C-01, future receiving sheet
- Commercial observations (014 §7.9): currency, lot condition, seller region, tax treatment, shipping basis, minimum-purchase rule, observed timestamp, freshness/expiry on every `VendorLot` / `PriceObservation`. — P-01
- Manual / retroactive order capture (014 §3.4): an `Order` placed outside the planner and entered after the fact, with honest provenance (`entered_by`, `entered_at`, `evidence_ref`), is a first-class case. — P-01
- `Design.source: bricklink|own|official`, `Part.brick_source: inventory|with-set|buy` — A-01 follow-up

## Work items, outcomes, versioning, rights, history (014 §7.6–7.8, 7.10–7.11 — Tier 3)
- Unify `ClarificationRequest`, `Request`, `Ask`, `Conversation` into one envelope with typed purpose, or document non-overlapping invariants.
- `Request.status` gains `needs-revision · withdrawn · superseded · implemented · reopened` plus season and archive facets; never deleted.
- Option stances, fit results, measurements, rights decisions and requests each carry subject revision, author, timestamp, supersession.
- Rights are permissions, not a flag: acquire · retain · inspect · transform · derive · render · show-to-family · redistribute · export.
- Action history: define command/event identity, idempotency, undo boundaries and snapshot strategy before relying on the log for recovery.
- `GateRecord` instance for procurement release: `GATE-PROC-001` — findings carry `{ id, severity: high|medium|low, text, why, disposition: open|fixed|waived|deferred, waiver_reason?, owner?, due_trigger? }`; decision ∈ approve · approve-with-waivers · reject · return-for-work; `initials` + timestamp as authority. — P-01
- `PriceRevalidation { plan_ref, ran_at, drift[] { shop, part, was, now }, ttl_minutes }` — the before-you-leave check. — P-01
- Formal gate record (014 §8): `gate_id/type · subject_ref/candidate_revision · entry_criteria[] · required_evidence[] · checks[] · open_findings[] · authority_required · decision · rationale/waivers[] · output_baseline_ref · invalidated_by[] · supersedes`. `Request` and `GateRecord` stay distinct with an explicit join (K-7).

- `WorkItem { id, closes: strike_ref, subject_ref, runner: blender|geometry|studio|research|fit|manual, depends_on[], status: open|queued|running|done|failed|manual, produces: evidence_ref, restated_at, confirmed_by }` — the GapCloser job record; folds into the §7.6 work-item envelope. — D-01 §C2, C-01

- `Measurement { subject, field, value_ldu, display_unit, tool: tape|calipers|studs|photo, by, at, supersedes, evidence_ref }` — one revision per capture; old values kept. `ClaimVerification { claim_ref, status: holds|wrong|parked, method, evidence_ref, by, at, owner?, due_trigger?, supersedes }`. — M-01

## Naming (blocked on RESEARCH-01)
- Do not fix field names that encode scale words (part / piece / element / module / unit / section) until the vocabulary note lands.
