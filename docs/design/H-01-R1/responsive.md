# Responsive spec — intent only

**Status: not designed.** Everything below is a statement of targets and collapse rules so Claude Code can lay the plumbing. Real iPhone and iPad layouts need their own design sessions; F-01 was built tablet-first at rough fidelity and nothing else was touched for small screens.

## Targets
| Target | Who | Sheets | Posture |
|---|---|---|---|
| Laptop ≥ 1280 | operator | A-01, B-01, C-01, P-01, J-01, D-01, Hub, H-01 | primary; multi-column cards as prototyped |
| iPad landscape (1180 × 820) | family, operator review | F-01 first; C-01/P-01 read + approve | two columns; 44px targets |
| iPad portrait (820 × 1180) | family | F-01 | single column: steps 1–4 stacked, needs/selected/send cards below; map full width |
| Phone (390 × 844) | anyone | Hub, J-01, request cards, approval trail | read-only; no canvas editing; one card per screen |

## Collapse rules (to design, then build)
- Cards: multi-column grids collapse to one column below 720px container width; the Model-it row already does 3 → 2+1 with the third card going landscape. Card headers are grids (number · title / description) — never wrapping flex rows.
- Control rows (SHOW / LOOK / ZOOM) stay single lines: equal-width segments, labels ≤ 9 characters, no glyphs.
- Map (F-01): square, fills width; pan by drag; zoom pills; side views fit width. Minimum readable stud ≈ 3 px → whole-table view on phone is view-only.
- Tables (C-01 parts, P-01 schedule): page columns rather than horizontal scroll (P-01 already pages shops 3 at a time). On phone, one column per page.
- Text inputs: 48px tall on tablet; one per row; mic button 48 × 48.
- Toasts/status: fixed-height status line, never overlaying the work surface.
- Hit targets ≥ 44 px on any touch target.

## Not covered
Gestures beyond tap/drag (pinch zoom on the map), keyboard-only placement, screen-reader flows for the canvas — all to be designed.
