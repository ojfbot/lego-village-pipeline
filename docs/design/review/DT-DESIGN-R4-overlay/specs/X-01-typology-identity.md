# X-01 — Typology identity (study)

Sources: `sources/Typology Identity.dc.html` (v1, canvas board) · `sources/Typology Identity v2.dc.html` (navigator + Benny). Wireframe (N-01).

## The problem
Every sheet opens with a serif title, a mono code line, ← HUB and a paragraph in the same column. The kind of page is carried by one 9.5px letter. Colour cannot carry it: every hue is an evidence state and the axes stay separate. So kind must be carried by **form**: a mark, a word, a silhouette, a position.

## The census: ten kinds, one verb each
See today (HUB) · Arrange (A-01 V-02 F-01) · Answer (B-01) · Look up (I-01 M-01 T-01) · Look closely (I-03) · Confirm (R-01 I-02 V-01) · Approve (C-01 gate) · Buy (P-01) · Find your way (J-01) · Hand over (H-01).

## Five approaches (each drawn on A-01, B-01, I-01, C-01)
- **1a Nameplate** (Rams · Rand): fixed plate top-left, mark + plain noun; same mark on Hub cards, chips, links.
- **1b Verb is the headline** (Lois): one line, verb bold, name as caption; the one shout per page. Must stay one line at all widths via shorter wordings, never wrapping or ellipsis.
- **1c Plan is the identity** (Koolhaas): one page skeleton per kind: workspace full-bleed; question narrow column; register ruled rows; approval funnels to initials.
- **1d Drawing set** (Sachs / construction documents): title block, plain name first, trade name (plan, schedule, RFI, submittal, PO, receiving report, transmittal) second.
- **1e Threshold** (Peter Carl): where you came from · here you … · when you leave.
- **Recommendation:** layer, don't blend: 1c skeleton → 1b verb → 1e strip → 1a mark elsewhere → 1d at the foot. Operator pick pending.

## v2 navigator behaviour
- Eight cards on a 20×14 grid; tap → the card lifts to 80% width, the rest stack in a right rail; Esc/✕ returns. Two overview layouts (3-over-5 at ≥ 900px board width; 2×4 below).
- Census → third level: a kind lifts, the other nine stack in a right rail; the open kind renders a **specimen** on a 12-column grid whose strips are subgrids (nameplate 1–3 · verb 4–9 · title block 10–12; threshold strip cells under them; skeleton zones on the same columns; the kind's real sheets each spanning 12/N).
- Canvas breathes with depth 0/1/2: grid 24→36→48px and fades; accent wash gathers behind the open card, info wash answers from the rail; hatch follows state (open tint · rail draft · overview card).
- **Benny** (chief of staff, AI, always labelled): left column 2px → 8px on hover (tab appears) → 340px on click or header button; pushes the board. Chat routes to sheets from `data/pages-index.json` (stop-words dropped, keyword > title > code, first content word ×2). He never changes a sheet.
- Tweaks: blueprint; motion expressive / productive / off.
