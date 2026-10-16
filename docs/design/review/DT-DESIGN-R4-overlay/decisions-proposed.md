# Proposed decisions — R4 (2026-10-10)

Not in the ledger. Provisional ids; they become DEC-044… only when the operator accepts, in `handoff/decisions.md`, newest first. Touches = blast radius now.

| Provisional | Decision | Touches | Evidence |
|---|---|---|---|
| P-R4-1 | **A filled emphasis surface is a plate, not ink.** Badges, hot zones, primary buttons and "you" bubbles fill with `--dt-plate` and read `--dt-on-plate`; both dark in paper and blueprint. `--dt-ink` stays a text/line token. | tokens.css, every sheet | Operator 2026-10-10: "I never want to see big blocks of white background, even on buttons." X-01 v2 converted. |
| P-R4-2 | **Benny pushes, never covers.** The chief-of-staff column is part of the page grid (2px rest · 8px peek · 340px open); the board reflows and each component re-picks its size variant. | X-01 v2, future shell | Operator 2026-10-10: "make what is visible smaller, not slide over it." |
| P-R4-3 | **Every component ships size variants, chosen by its own width.** Overview / rail / open; full / short / verb-only wording; glyph-only rails. No ellipsis as a design outcome. | X-01 v2, W-00, D-01 | Operator's one-line rule for 1b, generalised. |
| P-R4-4 | **Motion choreography has three classes**: lift (the opening thing leads, on top), rail (follows +70ms, 80% duration), rest (+40ms, 90%); old faces exit in ~120ms, new faces enter after ~100ms over ~260ms; Carbon curves; duration scales with distance; reduced-motion honoured. | X-01 v2, W-00 | Operator: transitions "jarring / multiple visible at once" → fixed by this ordering. |
| P-R4-5 | **A change made here is shown there.** When an action on one component changes another, the ripple grammar is: connector from cause to effect → one pulse → old → new on the status line → CHANGED chip until acknowledged → the ledger says it in words. One accent, one meaning: changed-by-you-just-now. | W-00, Hub, M-01, A-01, C-01, T-01, B-01 | Operator 2026-10-10: "this should be STRONGLY communicated intuitively." Precedents: Rams (colour means function), Lois (one shout), Sachs (show the seam), Carl (state the consequence). |

Deferred (not proposed yet): which identity layering (X-01 recommendation); operator pick pending.
