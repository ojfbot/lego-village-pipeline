# Proposed research task: efficient rendering for LEGO House navigation

Disposition: file when the actual implementation begins. This is a reviewable issue draft; it has not been filed. The prototype remains outside the production application.

## Question

Which asset and scene structure gives a responsive scroll flight, piece assembly, reliable picking, and readable HTML sheets across the supported devices, while retaining stable identities for rooms and artifacts?

## Current evidence

The detailed scene uses 232,625 triangles and 172 draw calls in the final view. The compressed asset is about 757 KB. It merges bricks into 77 wall/roof courses and keeps eight tree pieces and fifteen stair pieces movable; sample figures are procedural. Detailed geometry and transparent glass still dominate the scene. The preview now coalesces paint requests, caches room picking bounds and viewport measurements, and caps pixel density at 1.25. Draco reduces transfer size, not triangle work. A fast Apple M3 Max desktop sample did not expose a significant frame-rate difference from these changes.

## Compare using the same interaction slice

Use the real supplied geometry and the existing reversible camera/tree/stair/room choreography for each candidate. Keep identical destination identifiers and working DOM sheets.

- Shared part geometry plus InstancedMesh or BatchedMesh, with explicit per-part transforms and stable identifiers. Compare batching per room against batching across the whole house; measure the cost of piece motion and picking.
- A prepared glTF with exterior/interior levels of detail, removable hidden surfaces, shared materials, and a lightweight picking proxy. Check whether culling and transparency sorting still work during the exploded sequence.
- Simplified navigation geometry with detailed parts loaded only for close work. Compare transfer, decode, route continuity, visual recognition, and the cost of switching quality.

Do not select a renderer or data structure solely from library bundle size. First determine whether the limiting work is main-thread updates, driver submission, vertex processing, transparent overdraw, raster resolution, decoding, or browser compositing.

## Measurement and review

Agree device/browser coverage and budgets before benchmarking. Include a low-power phone, a typical laptop, retina density, the in-app preview, and the supported browser engines. Measure cold transfer/decode, first usable interaction, CPU/GPU frame time and missed frames, memory, picking latency, and idle work. Repeat the same scripted scroll and pointer sequence with the same assets, resolution, and visible scene. Report sample distributions and environment details, rather than a single average FPS.

Verify room selection and exact return from sheets, backwards scroll, still/reduced-motion behavior, browser history, touch scrolling, context loss, quality fallback, and the accessible 2D destination list. Review motion comfort with the user alongside performance; a faster frame is not proof that the choreography feels comfortable.

## Expected output

A measured comparison, chosen scene/asset structure, stable identity and picking contract, export/validation steps, quality/fallback policy, agreed budgets, and one runnable integration slice. Record rejected approaches and remaining device gaps. Preserve the original Blender model as an input asset and keep evidence/authority separate from architectural colours.
