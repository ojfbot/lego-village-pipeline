# Responsive house and navigation behavior

## Layout follows available space

At widths up to 600 pixels, the dashboard is edge-to-edge. It is also edge-to-edge on viewports up to 900 pixels wide and 560 pixels high. Larger viewports retain the configured inset over the ghosted house. The phone header uses CSS subgrid where supported, with a stacked fallback. Back and the room selector share one row. Sheet tabs occupy the next full-width row and may scroll horizontally.

The house header becomes a compact brand row and a finder/theme row below 900 pixels. The finder results use the viewport width on phones. Preview text can wrap. Controls retain their accessible names when their visible labels compress.

The wordmark keeps the R6 layered bubble treatment. Its size and placement change for portrait and short landscape layouts. It shrinks and fades with the opening scroll. The chapter labels remain one at a time with text shadow rather than an opaque caption panel.

The opening and closing overview camera distances account for narrow aspect ratios. Portrait framing places the opening house below the wordmark. The closing framing shifts the house upward to clear the ask bar. The lobby route and assembly curves remain R6's choreography.

## Sheets adapt within their iframe

Layouts adapt to iframe width, not the host monitor width. Split work areas stack below 900 pixels. Phone layouts wrap long headers and metadata, stack measurement titles above values, and cap auto-grid minimums at the available width.

Workbench retains its desktop 12-column grid and row subgrids. Below 1000 pixels, it uses two card columns. Below 600 pixels, cards form one column. An expanded card retains its content while neighboring cards compress. The typology board uses readable cards on narrow screens instead of compressing its 20-column overview. Its named View Transitions remain source behavior. The shop comparison keeps its row and column relationship in a horizontally scrolling region.

## Focus does not change spatial depth

Pointer or finder focus identifies a room with a small colour emphasis and the R6 label. It does not make adjacent blocks transparent, lift hovered blocks or scale their geometry. The tour's interior transparency helps expose the lobby during its passage. Glass stays transparent. The near-full-screen dashboard retains the ghosted house behind it on larger screens.

## Every room uses its entry block

Clicking a block opens that block's mapped room and passes the clicked block as the flight destination. This includes Drafting Table's blocks 1 and 13. A header, finder or router entry uses the room's first block because no source block was clicked. The existing room flight styles remain available.

Back closes the dashboard at the room threshold. If the user switched rooms inside the dashboard, Back places the camera at that new room's first block. The next wheel or touch movement resumes the scroll tour. Small scroll changes must also resume it. A gesture at either page boundary must not leave the camera permanently held. Restoring focus must not change the page's scroll position.

The current return blends back to the tour's current progress. Continuous flights from one block to another and bookmark/history semantics still need technical design.

## Chapter content is strict

The six subheads form two haikus in chapter order. Their approved syllable counts are 5, 7, 5, then 5, 7, 5.

> Loose bricks greet the dawn  
> Soft light slips through open doors  
> Green leaves find their home

> Steps rise from the floor  
> Small rooms gather round the tree  
> New worlds wait for hands

The content gate checks the six approved lines. Future copy changes require a new syllable review and an explicit update to that gate.
