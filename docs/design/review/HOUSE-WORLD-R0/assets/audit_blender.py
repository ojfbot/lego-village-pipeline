"""Run with Blender in background mode; inspect both sources without saving."""
import bpy
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
report = []
for filename in ['legoHouse.blend', 'legoHouse.blend1']:
    path = root / 'blender' / filename
    bpy.ops.wm.open_mainfile(filepath=str(path), load_ui=False)
    report.append({
        'file': filename,
        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'bytes': path.stat().st_size,
        'objects': len(bpy.data.objects),
        'mesh_objects': sum(obj.type == 'MESH' for obj in bpy.data.objects),
        'libraries': [lib.filepath for lib in bpy.data.libraries],
        'external_images': [image.filepath for image in bpy.data.images if image.filepath and not image.packed_file],
    })
print(json.dumps(report, indent=2))
