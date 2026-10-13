# Rooms, flights and page thresholds

## Preserve the parallel entry

The house is a parallel way into Drafting Table pages. It does not replace the Hub or establish agent package boundaries. Page names, verbs and forms come from the existing handoff. Roof colours belong to the building and never imply verification, authority or ownership.

The stable page map is `prototype/modules.js`. Twenty-one blocks map to 22 destinations because the BOX study shares the Hub's block. The map is a prototype hypothesis, not a settled taxonomy. Keep primary act, supported capabilities and page identity separate when resolving the typology research.

## Current behavior

Hover or keyboard activation highlights a room. Choosing it opens the mock sheet at the current camera pose, without a flight. Closing returns focus to the activating input and retains scroll. The six scroll chapters narrate the tour; they are not six navigation categories.

## Proposed room flight

Use explicit activation for camera travel. Hover and finder focus only reveal identity or a read-only preview. They must not move the camera.

1. On activation, retain the page identifier, current tour progress, camera pose and activating element.
2. Suspend scroll-tour ownership while a room flight runs. There must be one camera owner, not competing scroll, orbit and room tweens.
3. Follow a visible route to a room threshold. Begin with an exterior approach or a safe lobby route. Do not interpolate a straight line through solid rooms, stairs or trees.
4. Keep gaze changes broad and continuous. Prefer displacement and framing over rapid rotation. Preserve upright camera orientation. The earlier tight ground pivot caused excessive whip and must not return as a default.
5. On arrival, announce the destination and open its dashboard modal. The modal owns focus. A travel animation must not submit, save, approve or change any work.
6. Escape during flight cancels it and returns to the retained entry pose and control. Escape inside the dashboard closes the dashboard according to its own dialog contract.
7. On dashboard exit, restore the entry bookmark before returning camera ownership to the tour. Repeated openings must not drift its scroll position or discard drafts.

For reduced motion, use an immediate threshold change or a short opacity transition, then the same modal and focus result. Keep an explicit direct HTML route available if WebGL fails. Keyboard and touch operation must reach every page without a precise canvas hit.

### Switching rooms from a dashboard

Offer the existing room finder or page links from within the dashboard. Retain the current sheet state before switching. Choose whether a visible room flight adds useful orientation; direct sheet-to-sheet entry remains a valid path. Never make a camera tour a prerequisite to answering a question or reviewing work.

A pending change confirmation stays separate from navigation. Do not infer consent to a change from a room selection. Specify interrupted flight, rapid repeated activation, browser history and lost WebGL context behavior before production implementation.

## Focused room previews

The operator requested a smooth page preview for focused finder items. This is not implemented in R0. Proposed behavior:

- Keep DOM focus in the combobox and identify the active option with `aria-activedescendant`.
- Preview actual page structure and current mock values without exposing editable controls or changing shared state.
- Enter opens the complete dashboard. Tab moves normally; Escape closes the popup. Typing does not choose a destination.
- Expand one preview at a time. Respect reduced motion and avoid a pointer feedback loop caused by rows moving under the cursor.
- Avoid duplicate IDs, live regions or dialog landmarks from miniature copies of full page markup.

Inline expansion versus a neighboring preview is still an operator choice. Build a reviewable comparison before settling placement.

## First observable slice

Implement one block → threshold → near-full-screen A-01 → return, with a direct reduced-motion path and retained camera/focus state. Verify that slice before adding all room routes. Then add a second room to prove switching without losing a draft. This is prototype work only until the corresponding production gates are satisfied.
