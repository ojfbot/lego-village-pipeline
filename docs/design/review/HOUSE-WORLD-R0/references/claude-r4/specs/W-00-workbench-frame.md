# W-00 — Workbench frame (study)

Source: `sources/Workbench Frame.dc.html`. Wireframe (N-01). The operator's note: not every page has every bar, and bars must NOT all share one chrome; the frame proves the capability, not a default.

## Shell
Header (flat 2px ink rule, title · plain-words "what's happening" line · controls) · left sidebar THE QUEUE (ruled, no card chrome; collapses to 48px; dot when something inside changed) · main (12 columns) · right sidebar THE TRAIL (ruled; entries wear evidence chrome: solid pass, dashed prov) · footer LEDGER (dashed rule). Bars are optional props (leftBar, rightBar, footerBar); sidebars collapse automatically under 1100px.

## Cards as row-subgrids
Each card spans three rows (head · body · status) with `grid-template-rows: subgrid`, so heads, bodies and status lines align across a row regardless of content. Containment (`container-type`) must sit on an inner wrapper, never on the subgrid element. Open a card → it takes the top band; the others drop their body row (head + status only). Card chrome varies by state: trusted sheet = hatch + shadow; unknown-bearing (M-01 before signing) = dashed unres, no shadow, becomes solid on signing; register (I-01) = light rule, no hatch.

## The ripple (sign a measurement on M-01)
0 ms the unknown row flips to measured · 120 ms accent connectors draw from M-01 to A-01, C-01, queue #3, the trail (SVG cubic paths from element rects) · 520 ms targets pulse once, status lines show old → new (old struck), CHANGED BY M-01 · OK chip until acknowledged (dot on collapsed rails) · 900 ms the ledger states it in words; the header sentence changes. Hovering a changed thing redraws the seam back to its cause. I-01 is untouched on purpose. RESET replays.
