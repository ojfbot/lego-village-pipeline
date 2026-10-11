# Depth without another whip

## Preserve the current choreography

The compact opening, broad tree arc, rear clearance, connector-aligned tree assembly, course assembly, upright minifigs and reversible scroll clock are R0's working baseline. The latest camera changes alter the opening approach; they rejoin the previous route at 18% scroll. The rejected tight stair/tree pivot and background colour wash are historical experiments, not current directions.

All current animation is scroll-owned. Keep gradual starts and short, legible settling. Treat the visible appearance of bricks meeting as a design claim to inspect from multiple viewpoints. The tree paths are connection-aligned; there is no general interpenetration proof for the building.

## Parallax proposal

Compare a small set of depth layers rather than adding motion to every object:

1. Distant background, with very low apparent movement.
2. House modules and course assembly, carrying the main depth information.
3. Foreground tree or part silhouettes during the lobby pass, moving only where they clarify distance.
4. The HTML wordmark and captions, which settle or fade without joining the camera's orbit.

Keep layer movement tied to the same scroll value, reversible and bounded. Use phase and depth differences rather than abrupt delayed starts. Never make controls or form fields parallax targets. Reduced motion freezes spatial layers while retaining direct navigation and readable chapter information.

## Background proposal

The current background is a restrained blueprint grid. The operator wants a better treatment, but no replacement is selected. Compare a quieter drafting-paper field, a subtle light field, and a simplified studio backdrop. Judge them against room silhouettes, ghosted modal context and text legibility.

The opening's pale-yellow sunrise belongs in PLAY WELL's letters, not in a radial yellow overlay blended over blue. Caption panels have no solid background; their text shadows supply anchoring and legibility. Keep one visible caption at a time.

## Strict chapter rule

Exactly six labels, one subhead per label. In chapter order the subheads form two English haikus: 5–7–5, then 5–7–5. `prototype/AGENTS.md` records the rule and `prototype/check-chapters.js` checks it before a build. Its pronunciation ledger is manually reviewed for this copy; it does not guess arbitrary English syllables.

| Label | Subhead | Syllables |
|---|---|---|
| Pieces at dawn | Loose bricks greet the dawn | 5 |
| Come on in | Soft light slips through open doors | 7 |
| Around the trees | Green leaves find their home | 5 |
| Step by step | Steps rise from the floor | 5 |
| Through the other side | Small rooms gather round the tree | 7 |
| One house, many builds | New worlds wait for hands | 5 |

Prefer one visual line where possible, but allow wrapping under text enlargement. A new chapter count or syllable pattern requires an explicit operator change to the rule.

## Rendering research task

The full study currently reports 172 draw calls and 232,625 triangles in the final assembled frame. The supplied GLB is 756,868 bytes. Pixel ratio is capped at 1.25 and rendering is coalesced on demand. These are observed implementation facts, not a promise of smoothness on every browser.

Before production selection, measure CPU and GPU work, memory, asset decode, frame consistency and interaction latency on representative low-power devices. Compare instancing repeated bricks, merged course geometry and levels of detail while preserving selectable room identity and the pieces needed for assembly. A smaller JavaScript framework alone does not prove a faster renderer. Include WebGL loss, fallback and dormant-background behavior. Do not select a universal frame-rate claim or performance budget from desktop preview observations alone.
