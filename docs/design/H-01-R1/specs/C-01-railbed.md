# C-01 — Railbed: what the train brings, what to buy

**File:** `prototypes/Prototype C - Measurement to Procurement.dc.html` · **Journeys:** J5 J6 J7 J8 J11 · **Status at handoff:** built, landed
Behaviour reference is the live prototype; its code is not to be copied. All numbers are mock pending real math + audit.

## Purpose
One facet of slice C: match the Winter Holiday Train's track to the MILS railbed segment by segment, buy only the gap + embed parts, check fit, clear asks, then release to P-01.

## Behaviour
- Header schematic with **NEW ONLY / IN THE VILLAGE** toggle: colour = new work by basis, grey = already built (tree, other builds); legend states the difference.
- **Sources by basis**: ■ OWN · SET (train, LEGO direct) · ▤ BUY · ADAPTED (bl-741807, colours adapted, rows record colour_source → colour_chosen) · ◇ BUY · RESEARCH (ballast).
- **In one line** summary with readouts; every changed value pulses once (token keyframe).
- **Choices — and how far each is worked out**: ballast none/single/double, siding; each option shows modeled? · fit-checked? · stances (for/against/neutral/caution per stakeholder with reason) and cost delta.
- **Needed from you / In progress / Does it fit?**: asks with @tags (◇ needed from · ■ did · ○ waiting on), progress dots, fit checks (Studio, Blender) with evidence refs.
- **Requests** (first-class): open until answered — decline / park / accept, reasons, reply in requester's words, attached work visible ("words only" is visible).
- **Parts list by basis**: rows with basis chip, need/own/buy, BrickLink low–high range; part name opens the part popover (image slot, id, colour, basis, use, quantities, BrickLink/Rebrickable/inventory links); vendor-dynamic links.
- **Approval trail**: draft → review by basis → initials + stamp → cart link appears only after the stamp; blockers listed on the gate. Cards grow to a cap then scroll; ⤢ expands one while neighbours collapse.
- **Chain back to the story**: why this facet exists.

## States
ballast none/single/double · siding on/off · derived on/off · fit run · boys OK · gates 0–3 · filter by basis · request open/declined/parked/accepted · popover open · card expanded.


## Revision R1 — release gate at the end of the sheet (DEC-034)
After **Approve with initials** the approval trail's last rung reads *Release gate → then buy on P-01*, and a full-width **ReleaseGate** (D-01 §C5) opens under the cards: what is being released (this list at its revision, CrossRef ↑), the evidence it rests on (M-01 facts and claims, this sheet's approval, A-01 fit, price age — each a CrossRef), open findings with fix → / waive (reason) / defer (owner + trigger), initials + **Release to buy** or **Back to the list** (withdraws the approval, list editable again). Passing shows the stamp and a **Continue to P-01** button that carries `?released=INITIALS|DATE`. Reopening the gate makes P-01 read-only again. Basis split (§7.2) and GapCloser (§C2) are described in D-01.
