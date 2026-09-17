# M-01 — Measure and check

**Journey home:** L2 control loops *capture a measurement* and *verify a claim* (HANDOFF-LEGO-PIPE-014 §3.3); alias J9. **Tier 1** — the evidence the BOM rests on. Decided as one sheet (DEC-026) linked from A-01 and C-01.

## Purpose
Every number the plan leans on, in one place, each with *how we know it*. Two loops, one return rule: **the user goes back to exactly where they were**.

## Return-to-caller (the mandatory part)
- Entry carries `?from=<sheet>&what=<the chip's text>`. The **YOU CAME FROM** bar restates it and offers one primary action: *← Back to A-01*. On a real sheet the return restores scroll position and selection; the prototype links to the sheet.
- No caller → the bar explains how the sheet is meant to be entered and offers the Hub.

## Things to measure
Row = one physical fact: name · why the plan needs it · value + unit · status (■ MEASURED · ◇ GUESS · ○ UNKNOWN) · tool · by · when · LDU. Tap to open: plain how-to, **What the tape says** (in the tape's unit; stored as integer LDU per §7.1), **Measured with**, photo attach (mock).
Typing a different value produces a **pending restatement** (§5B, explicit state): "I will change X from A to B (n LDU), measured with T by James. This will mark stale: … The old value stays on record." → *Yes, record it* / *Not yet*. On yes: new field revision; old value struck through under *Earlier values · kept, never edited* (§7.8); dependents pushed to **What changed because of this**.
Seed: the five DEC-016 tree facts (measured), railhead height (unknown — it gates grade/banking and the flush check), table top (guess).

## Claims to check
Row = a statement the plan depends on: text · said by · leans on it. States ◇ UNCHECKED · ■ HOLDS · ▲ WRONG · ○ PARKED. Actions open a **draft**, never commit directly (operator correction 2026-09-17): *Holds · attach proof* asks **how you checked** (listing · counted · measured · test piece · agent report) + **what you saw, in your words** + **proof attached** (waived only for methods that carry their own evidence); *Wrong · say why* asks method + words + proof and lists what will reopen; *Can't check yet* asks what's in the way + the trigger (parcel arrives · model exists · build starts · a date). Only when the draft is complete does the **pending restatement** appear — "I will mark … as HOLDS — method …; your note …; proof attached. Checked by James, now." — with *Yes, record it* / *Not yet*. Done rows offer *↺ new evidence* — never re-ask for the same source revision; new evidence may reopen (§5B amendment).

## Links (operator ask 2026-09-17)
Every claim row links **back** to its origin (SAID BY → the stable source URL or the sheet/decision that produced it, with a note on what we hold: snapshot, trail, research note) and **forward** to everything that leans on it — one chip per dependent, deep-linked to the card on that sheet (`#parts`, `#fit`, `#rig`, or a row id here). Measurement rows carry the same forward chips in their open state. Set / MOC / part numbers in claim text are SetRefs.

## What changed because of this
Blast radius, not a change pulse (§5C): each committed measurement / refuted claim lists the dependent checks per sheet with ▲ STALE / ▲ REOPENED and a link.

## Accessibility & announcements (§6)
`<h1>`, banner/nav/main landmarks, two labelled sections. Row header is a button with `aria-expanded`; the input carries the fact's name and unit. Live regions: measured/hold counters (polite), the sheet narration line (polite: how-to on open; "X recorded: v unit. n dependent checks marked stale." on commit; "Left X as it was." on cancel), the pending restatement (`role=status aria-live=assertive`).

## Mock boundaries
LDU factors (stud 20 · brick 24 · plate 8 · mm 2.5), dependency map, photo attach, claim evidence text. Schema request: `Measurement { subject, field, value_ldu, display_unit, tool, by, at, supersedes, evidence_ref }`; claim verification folds into the §7.8 versioning request.

## Open
- OW-01: the measurement row and claim row belong in D-01 (fold in when D-01 is next touched).
- Q13: ring-centre offset vs section notch is decided *with* these numbers, not here.
