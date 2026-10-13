# Next research and technical design

The assigned owner roles, dependencies, deliverables and acceptance checks are in [review.md](review.md) and [follow-up-tasks.json](follow-up-tasks.json).

## Measure a render structure before production implementation

Compare the current GLB hierarchy against batched static geometry and instanced repeated parts. Preserve block, course, stair and tree identities for assembly and picking. Measure draw calls, CPU frame time, GPU frame time, loading/decode cost, memory and visual fidelity on representative integrated GPUs and phones. Use the same camera progression and viewport sizes for each candidate.

Choose when the renderer needs a new frame. Compare continuous rendering with invalidation after scroll, pointer, resize and animation updates. Evaluate adaptive pixel ratio, geometry detail, compressed geometry and context-loss recovery. Record device and browser versions with every result. Do not infer a production architecture from the preview's smoothness.

## Give each navigation transition one owner

Design explicit states for the scroll tour, room flight, open sheet, switched room, return and interrupted flight. Define the bookmark and scroll position each transition retains. Test rapid selection, cancellation, keyboard entry, touch entry, browser Back and lost WebGL context. Keep camera acceleration and depth cues comfortable. Avoid opacity changes that imply pieces moved through each other.

## Continue typology, Grid and Subgrid research

Use R4's Typology Identity v2 and Workbench Frame as precedents. Preserve distinct work skeletons and verbs for each sheet. Size cards from their containing region and align related title, content and status bands with subgrid. Treat mobile reflow as a designed composition.

Compare native View Transitions with transform/opacity transitions for card expansion and sheet entry. Verify text remains readable while layouts move. Define reduced-motion behavior, focus destination and announcement for each transition. Do not use a camera flight as the only route to a page.

## Keep build-and-tell meaning with its builder

R6 research doors remain concepts. A minifig or model position may identify a builder, agent or artifact only when that meaning was assigned explicitly. Keep the builder's story distinct from inferred geometry and software evidence. Document consent and facilitation before proposing collaborative model interpretation. Carry the existing LEGO SERIOUS PLAY research issues forward as inputs rather than treating the visual metaphor as validation of the method.
