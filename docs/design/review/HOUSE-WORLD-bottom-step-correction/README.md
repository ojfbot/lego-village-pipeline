# Bottom step export correction

The isolated white tab in the JSON schematic maps to `00072_3070b.dat.001` in `Building Block 1`. This is the legitimate bottom 1×1 tile of the exterior stair terrace. The source render highlights it in pink. The original model uses an orange material for that tile.

The old exporter put that tile alone in `Block_01_course_00`. The schematic represents the course with a white box and moves it independently. The corrected exporter groups the tile with its adjoining lower structure. It removes the separate animation group, preserves the source brick, and retains its original material in the GLB.

## Use the corrected assets

Replace both `house.glb` and `house-metadata.json` in the receiving prototype with the files beside this README. Use the new JSON course membership for the schematic as well as the full model. Block 1 now has three courses numbered 00, 01, and 02. The whole building has 76 courses instead of 77. Do not mix these files with the old metadata or hardcode the former course count.

These are corrected derivatives of the PR #45 source cut at `bbaeec06ef09d60a39c7fdfa8163054667ac17ee`. They are not a new registered design-package cut. The source `.blend` and the published R0 cut retain their original bytes.

## Verification

Run `python3 docs/design/review/HOUSE-WORLD-bottom-step-correction/verify_assets.py` from the repository root to verify all correction files and the preserved source against their SHA-256 records. The correction manifest identifies received bytes. Regenerating derivatives creates a new measured asset pair rather than silently refreshing those hashes.


`verification.json` records the source SHA-256, corrected GLB SHA-256, course membership, and geometry comparison before GLB compression. Both sides contain 152,029 vertices and 137,413 faces. The largest vertex difference in either direction is 0.0000432 Blender units, within the 0.001-unit tolerance. The small difference comes from transform rounding when Blender joins meshes.

`glb-roundtrip.json` records successful import of the compressed GLB through Blender's Draco decoder. All three Block 1 course meshes imported, including the lower course with white, transparent, and orange materials. The browser model contains 232,433 triangles.

## Regenerate

Run this command from the repository root. It uses the preserved source in the R0 package:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --disable-autoexec --background docs/design/review/HOUSE-WORLD-R0/assets/blender/legoHouse.blend --python docs/design/review/HOUSE-WORLD-bottom-step-correction/export_house.py
```

The script writes both derivatives beside itself. It does not save the source. It fails if the expected bottom step no longer occupies the same source course, if vertex or face counts change, or if world positions exceed the comparison tolerance.

To repeat the compressed GLB import check in an empty background Blender process:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --disable-autoexec --background --python docs/design/review/HOUSE-WORLD-bottom-step-correction/verify_glb.py
```

That check rewrites its local import report. A subsequent asset check reports any changed received bytes.

## Deviations

- 2026-10-12: The suspected extra source brick is a valid bottom step tile. Correct the export grouping rather than delete source geometry.
