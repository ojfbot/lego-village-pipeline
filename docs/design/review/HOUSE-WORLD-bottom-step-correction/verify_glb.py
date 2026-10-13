import bpy,json
from pathlib import Path
root=Path(__file__).resolve().parent
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(root/'house.glb'))
meshes=[o for o in bpy.data.objects if o.type=='MESH']
block=[o for o in meshes if o.name.startswith('Block_01_course_')]
assert len(block)==3
report={'imported_meshes':len(meshes),'triangles':sum(len(o.data.polygons) for o in meshes),'block_1_meshes':[{'name':o.name,'vertices':len(o.data.vertices),'faces':len(o.data.polygons),'materials':[m.name for m in o.data.materials]} for o in block]}
assert any(o.name=='Block_01_course_00' and len(o.data.polygons)>22 for o in block)
(root/'glb-roundtrip.json').write_text(json.dumps(report,indent=2)+'\n')
print('GLB_IMPORT_CHECK '+json.dumps(report))
