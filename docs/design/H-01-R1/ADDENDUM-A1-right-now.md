# ADDENDUM A1 — "Right now": three priorities on the Hub

**Added:** 2026-09-17, after the R1 bundle was cut. **Operator ask.** Ships with R1 for review.
**Where:** `Hub.dc.html` → section `#now`, directly above SHEET INDEX. Standalone: `standalone/Hub.html`. Captures: `screenshots/states/14-hub-right-now-paper.jpg`, `…-blueprint.jpg`, `15-hub-right-now-closing.jpg`.

## What it is
Three horizontal pill-cards, always in order, each one small and concrete:

1. **Measure the Christmas tree's base** — ON THE TABLE · 5 MIN → *Measure it →* (M-01 #tree-base)
2. **Order the Winter Holiday Train from LEGO** — ONLINE · 10 MIN → *Open the listing →* (lego.com 10254)
3. **Confirm the train's rails fit the MILS modules around the tree** — AFTER 1 + 2 · A-01 → *See the fit →* (A-01 #fit)

Each card: a numbered dot · title · a one-line *why* that names what leans on it · one primary action · two quiet round buttons: **■ done** and **○ not today**.

## Why it looks the way it does (the principle under test)
This is the first instance of a **type-generic** card — a system for keeping immediate priorities surfaced and actionable **without nagging or guilt**. The rules it encodes, to be tested against how James actually uses it:

- **Three, never more.** A fourth thing is not a priority; it lives on its sheet.
- **In order, with the reason.** The *why* says what the item unblocks, not why James is behind. The first open item is the only one with the accent ring and the shadow; the others wait their turn visually.
- **Two ways out, both honest.** *■ done* closes the loop and the card says what just got unblocked ("A-01 fit checks stop saying 'from memory'"). *○ not today* parks it with **PARKED · NO GUILT** and a promise: "It won't pester you before tomorrow." Both are undoable in place (↺ / *now*).
- **Time-boxed, not deadline-boxed.** The tag says how long it takes (5 MIN · 10 MIN), never how overdue it is.
- **The lede changes tone with progress, never with delay.** "Small, concrete, in order… none of them are urgent tonight." → "1 left. 2 closed — thank you." → "All three closed. The village is unblocked — nothing here needs you." There is no state that scolds.
- **Every change speaks once, politely.** One `aria-live=polite` line under the strip narrates done / parked / back; nothing else moves or flashes.

## What is mock
- The three items are hand-seeded. In the system they derive from the open findings (ReleaseGate), the M-01 facts with no method, and Q-items with a `due trigger` — ranked by *how much they unblock*, not by age.
- "Back tomorrow" is a label; there is no clock. Real behaviour: a parked item returns at the next session start, once, without a badge.
- No persistence in the prototype (reload resets).

## Requests
- **Schema:** `Priority { id, title, why, unlocks, action_href, effort_label, source_ref (finding | fact | question), disposition: open | done | parked, parked_until?, closed_at? }` — a *view* over existing records, not a new store.
- **D-01:** lift as **PriorityStrip** (§C7) once the shape survives a week of real use.
- **Review question for R1:** does the "no guilt" contract hold when all three are parked? Today the lede says "Nothing open today. Parked items come back tomorrow, quietly." — is that the right sentence?
