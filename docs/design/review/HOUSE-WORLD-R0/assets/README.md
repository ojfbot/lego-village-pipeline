# Blender sources and browser derivative

`blender/legoHouse.blend` is the exact user-supplied source used by the prototype. `blender/legoHouse.blend1` is its exact matching backup, included as a source asset rather than used interchangeably for export. Both were inspected with Blender 5.1.1 without saving. Neither references linked Blender libraries or external images. Their sizes and SHA-256 hashes are in `manifest.json`, with the read-only audit in `blender/audit.json`.

The browser derivative is `../prototype/house.glb`. `../prototype/house-metadata.json` maps the derived groups, and `../prototype/export_house.py` records the conversion. The original Blender animation and material system are not browser-ready: export freezes the assembled pose and rebuilds viewport colours as simple PBR materials in memory. Only the house collections are exported; all original source objects remain in the Blender files.

To experiment with a regenerated copy, first copy the package to a scratch directory. From that directory, run:

```sh
blender --disable-autoexec --background assets/blender/legoHouse.blend --python prototype/export_house.py
```

The script writes the derived GLB and metadata beside itself. It does not save the Blender source. Renderer/exporter versions can change derived bytes; measure a regenerated artifact rather than assuming its hash. Preserve this received cut and author a new revision for a changed export.

The supplied geometry's provenance is the operator's source file. No new license or official LEGO affiliation is asserted. Third-party runtime/font licenses are preserved in `../prototype/THIRD-PARTY.md` and its local font directory.
