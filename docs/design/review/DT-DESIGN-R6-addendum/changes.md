# Changes reviewed by the operator

These IDs identify changes within this addendum. They are not additions to the canonical DEC ledger.

| ID | Operator request | Implemented behavior | Main source |
|---|---|---|---|
| R6A-01 | Keep R6, with the GPT model quality | Local modern Three loader, ACES and sRGB output, original GPT lights and roughness, full corrected GLB and local Draco | `prototype/prototypes/house/three-modern.js`, `house-stage.js` |
| R6A-02 | Work across responsive screen sizes | Adaptive header, finder, wordmark and ask bar. Portrait overview framing accounts for aspect ratio. Compact landscape composition. | `prototype/prototypes/house/house-responsive.css`, `house-stage.js` |
| R6A-03 | Edge-to-edge dashboard on narrow screens | Phone and short mobile landscape dashboard fills the viewport. Mobile subgrid aligns Back and room title. Sheet tabs use the full width and scroll horizontally. | `prototype/prototypes/House World.dc.html`, `house-responsive.css` |
| R6A-04 | Improve the inherited sheets at small widths | Split layouts stack. Auto grids cap their minimum width at the containing sheet. Long headings and chips wrap. Measurement rows stack. Shop comparison scrolls within its table. | `prototype/dt/responsive.css`, annotated sheet sources |
| R6A-05 | Stop focused rooms making adjacent rooms ghosty | Removed focus-triggered opacity changes and hover lift/scale. Small emissive colour emphasis remains. Physical glass and tour interior transparency retain their roles. | `prototype/prototypes/house/house-stage.js` |
| R6A-06 | Resume scrolling after closing sheets | Lowered the progress-change threshold. Wheel or touch gestures can resume from a held room even at a page boundary. Restored focus uses `preventScroll`. | `prototype/prototypes/House World.dc.html`, `house-stage.js` |
| R6A-07 | Drafting Table flies to the clicked block | Activation forwards the source block. Drafting Table no longer forces a lobby camera pose. Header and finder use the room's first block. | `prototype/prototypes/House World.dc.html` |
| R6A-08 | Clear the agent input from the LEGO House label | Closing overview shifts upward. Input position changes no longer animate across screen-size changes. | `prototype/prototypes/house/house-responsive.css`, `house-stage.js` |
| R6A-09 | Preserve usable dashboard focus | Ask bar is inert while a sheet is open. Parent focus trap ignores hidden frames and disabled controls. | `prototype/prototypes/House World.dc.html` |

The six chapter lines remain two approved haikus, with one line beneath each label. The build checks the six-line content gate. R6 graphics, theme controls, room map, finder, sheet tabs and source tour remain the base of this derivative.

The source delta against the local pre-responsive integration is retained in `evidence/responsive-source-edits.json`. Runtime differences from the received R6 stage are in `prototype/integration-receipt.json`. Its preserved-method flags apply to that renderer comparison, not to every later edit of the House component.
