# Announcement specs — what a screen reader hears (HANDOFF-LEGO-PIPE-014 §6 · WP4)

Applies to A-01, C-01, P-01, M-01 and the shared components. Format: **trigger → live region (politeness) → sentence**. "Verdict" = the sheet's plain-words fit line. All sentences are the same text a sighted user reads; nothing is announced that isn't on screen.

## Shared rules
- One `aria-live="polite"` narration line per sheet (the mono line under the main card). Every state change writes one sentence there. It re-announces only when the text changes.
- Pending restatements (a proposal before Yes/No) are `role="status" aria-live="assertive"` — they interrupt, because the next key could commit.
- Every card is a `<section>` with an `<h2>` title (Spectral). Landmarks: one `role="main"`; header nav is `<nav>`.
- Icon-only buttons carry a full-sentence `aria-label` and `aria-expanded` where they toggle.
- Toggle groups use `aria-pressed`; tab strips use `role="tablist"/"tab"` + `aria-selected`.
- Hover cards (SetRef, CrossRef, Blocker): the anchor has `aria-describedby` → the card id; the card is `role="tooltip"` (SetRef/CrossRef) or `role="dialog"` (Blocker, because it has an action). Open on focus as well as hover; Esc closes; one open page-wide.
- Provenance glyphs (◇ AI, ◇ boys/initials, ■ verified, ▲ block, ○ not run) are text, so they are read as-is. They precede the label they qualify.

## A-01 Layout canvas
| Trigger | Region | Sentence |
|---|---|---|
| Section selected (click / Tab) | polite | "Section {NW|NE} selected. {Mated to Section X | Not yet mated}." |
| Arrow nudge / R rotate / drag end | polite | "Section {id} at {x}, {y} studs, rotation {r} degrees. Gap {n} studs, heading off by {d} degrees." or "… Endpoints mate." |
| PLAN tab | polite | "Plan view. Same geometry as the 3D view." |
| 3D · CHECK IT tab | polite | "3D view. {verdict} Massing only; every dimension is real." |
| LOOK preset | polite | "Looking {around | from above | along the track | under the branches}." |
| Try-a-move tool | assertive | "I will move Section {id} from {x, y · r°} to {x, y · r°}. The track gap goes from {a} to {b}; the tree-base overlap {stays at | goes from … to} {n} studs. Nothing is saved until you say yes." |
| Yes, move it | polite | the nudge sentence above |
| No, leave it | polite | "Left it where it was. The proposal is discarded; nothing changed." |
| Layer toggle | polite | "{Layer} {shown | hidden}." |
| Fit verdict changes | polite (verdict line) | "Yes — every check that can run passes." / "Not yet — {n} of {m} checks block." |
| 3D canvas (static) | `role="img"` name | "3D massing of the layout, same geometry as the plan. {verdict} {each blocking check: name: detail}" |

## C-01 Railbed: own, adapt, buy
| Trigger | Region | Sentence |
|---|---|---|
| Ballast choice | polite | "Ballast: {none | single | double}. {strikes summary if any}." |
| Derive rows | polite | "Ballast rows derived; 3 recolours confirmed as worked out." |
| Run fitment | polite | "Fitment run: {n} pass, {m} not run." |
| Request decline / park / accept | polite | "Request {declined | parked | accepted} — reply sent in LH’s words." |
| Trail rung done | polite | "{Saved | Reviewed | Approved}. {next consequence}." |
| Blocker chip (hover/focus) | dialog name | "Blocker: {label}" then card content |
| Blocker action | polite | "{Rows derived | Fitment run | Request parked} from the blocker popover." |
| ReleaseGate tag | polite | "▲ {n} BLOCKING" → "◇ {n} TO CALL" → "○ READY FOR INITIALS" → "■ RELEASED" |
| Waiver recorded | polite | "Finding {id} → waived." |
| Release to buy | polite | "Released to buy · {decision} · {initials}. P-01 is live." |
| Back to the list | polite | "Returned for work with {n} open finding(s). Approval withdrawn; the list is editable." |
| Expand card (⤢) | `aria-expanded` | label: "Expand {card name}" |

## P-01 Buying the gap
| Trigger | Region | Sentence |
|---|---|---|
| Sheet opens, not released | `role="status"` | "The list hasn’t passed its release gate yet …" (the status bar) |
| Priority pick | polite | "Priority: {label}. {plan summary line}." |
| Split toggle | polite | "{Splitting across shops | One shop where possible}. {n} parcels." |
| Re-check stock and prices | polite | "Checking…" then "▲ Prices moved: {drift}" or "■ Checked just now. Links live for 30 minutes." |
| Locked link attempt | polite (chat log) | "Pass the release gate at the end of C-01 first — shops are read-only until then." / "Re-check stock and prices first …" |
| Record order (BrickLink) | polite | "Order {no} recorded for {shop}: ordered, not owned." |
| Manual order restatement | assertive | "I will record an order you placed yourself: … Nothing else changes." |
| Yes, record it | polite | "Recorded. ■ ORDERED · BY HAND — {shop} {no}." |

## M-01 Measure and check
| Trigger | Region | Sentence |
|---|---|---|
| Measurement entered | polite | "{Fact} = {value} {unit}, measured by James, now. {n} things read it." |
| Photo attached | polite | "Photo attached to {fact}; hashed." |
| Claim: start Holds / Wrong / Can’t check | polite | "Drafting: {holds | wrong | parked}. Still needed: {list}." |
| Restatement ready | assertive | "I will mark “{claim}” as {HOLDS | WRONG} — method …; your note …" / "I will park …" |
| Yes, record it | polite | "Claim “{text}” → {holds | wrong | parked}." |
| Ripple (refute) | polite | "“{claim}” refuted — {dependents} reopen." |

## Acceptance (for Claude Code)
- axe: zero critical/serious on each sheet in both themes.
- `handoff/a11y/*.tree.json` are the accessibility-tree snapshots captured from the prototypes (name, role, level, states) — diff the build against them; additions are fine, missing nodes are not.
- Every sentence above must appear verbatim in the live region within 500 ms of its trigger.
