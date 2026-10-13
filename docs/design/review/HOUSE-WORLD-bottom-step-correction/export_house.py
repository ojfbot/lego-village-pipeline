"""Export a browser-sized copy of the provided LEGO House Blender scene.

The source .blend is opened read-only. Run this file with Blender in background
mode; it writes only to the adjacent house.glb and house-metadata.json.
"""

import bpy
import hashlib
import json
from collections import Counter
from pathlib import Path
from mathutils import Vector, kdtree

HERE = Path(__file__).resolve().parent
SOURCE = Path(bpy.data.filepath)
KEEP = {"Base Plate", "Int Glass", "Int Tree", "Paving Tiles"}
KEEP.update(c.name for c in bpy.data.collections if c.name.startswith("Building Block "))

def bounds(objects):
    points = [obj.matrix_world @ Vector(corner) for obj in objects for corner in obj.bound_box]
    low = [min(point[i] for point in points) for i in range(3)]
    high = [max(point[i] for point in points) for i in range(3)]
    return low, high

def geometry_signature(objects):
    positions = Counter(tuple(round(v, 2) for v in (obj.matrix_world @ vertex.co))
                        for obj in objects if obj.type == "MESH" for vertex in obj.data.vertices)
    return {"vertices": sum(positions.values()),
            "faces": sum(len(obj.data.polygons) for obj in objects if obj.type == "MESH"),
            "world_positions_sha256": hashlib.sha256(json.dumps(sorted(positions.items())).encode()).hexdigest()}

source_objects = list({obj for col in bpy.data.collections if col.name in KEEP
                       for obj in col.objects if obj.type == "MESH"})
original_geometry = geometry_signature(source_objects)
source_positions = [obj.matrix_world @ vertex.co for obj in source_objects for vertex in obj.data.vertices]

metadata = {"source": str(SOURCE), "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(), "groups": []}
# The old scene uses viewport diffuse colours rather than exportable PBR nodes.
# Rebuild simple materials in the in-memory copy; never save the source .blend.
for material in bpy.data.materials:
    colour = tuple(material.diffuse_color)
    material.use_nodes = True
    material.node_tree.nodes.clear()
    shader = material.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
    shader.inputs['Base Color'].default_value = colour
    shader.inputs['Roughness'].default_value = .72
    output = material.node_tree.nodes.new('ShaderNodeOutputMaterial')
    material.node_tree.links.new(shader.outputs['BSDF'], output.inputs['Surface'])

export_objects = []
for name in sorted(KEEP):
    collection = bpy.data.collections.get(name)
    if collection is None:
        continue
    objects = [obj for obj in collection.objects if obj.type == "MESH"]
    if not objects:
        continue
    low, high = bounds(objects)
    center = Vector([(low[i] + high[i]) / 2 for i in range(3)])
    label = name.replace("Building Block ", "Block ")
    anchor = bpy.data.objects.new(label, None)
    bpy.context.scene.collection.objects.link(anchor)
    anchor.location = center
    bpy.context.view_layer.update()

    if name == "Int Tree":
        pieces = []
        objects.sort(key=lambda obj: sum(bounds([obj])[j][2] for j in (0, 1)))
        for index, obj in enumerate(objects):
            part_low, part_high = bounds([obj])
            world = obj.matrix_world.copy()
            obj.animation_data_clear()
            obj.name = f"Tree_piece_{index + 1:02d}"
            obj.parent = anchor
            obj.matrix_parent_inverse = anchor.matrix_world.inverted()
            obj.matrix_world = world
            pieces.append({"name": obj.name, "order": index, "center": [(part_low[j] + part_high[j]) / 2 for j in range(3)], "faces": len(obj.data.polygons)})
        bpy.context.view_layer.update()
        export_objects.extend([anchor, *objects])
        metadata["tree_pieces"] = pieces
        metadata["groups"].append({"name": label, "source_collection": name, "center": list(center), "size": [high[j]-low[j] for j in range(3)], "objects_joined": 0, "pieces_preserved": len(objects), "faces": sum(len(obj.data.polygons) for obj in objects)})
        continue

    if name.startswith("Building Block "):
        number = int(name.removeprefix("Building Block "))
        courses = {}
        for obj in objects:
            part_low, part_high = bounds([obj])
            height = (part_low[2]+part_high[2])/2
            band = min(3, max(0, int(4*(height-low[2])/max(1,high[2]-low[2]))))
            courses.setdefault(band, []).append(obj)
        if number == 1:
            # The low corner tile is the first step, not an independent wall course.
            # Keep it with its adjoining lower structure during course animation.
            lowest = courses.get(0, [])
            if len(lowest) != 1 or lowest[0].name != "00072_3070b.dat.001" or 1 not in courses:
                raise RuntimeError("Block 1 source changed; inspect its bottom step before regrouping")
            courses[1].extend(courses.pop(0))
            metadata.setdefault("export_corrections", []).append({
                "source_collection": name,
                "source_object": "00072_3070b.dat.001",
                "action": "Group the bottom step tile with the adjoining lower course",
                "geometry_changed": False,
            })
        pieces = []
        for order, (_, bricks) in enumerate(sorted(courses.items())):
            part_low, part_high = bounds(bricks)
            bpy.ops.object.select_all(action="DESELECT")
            for obj in bricks:
                obj.select_set(True)
            bpy.context.view_layer.objects.active = bricks[0]
            bpy.ops.object.join()
            mesh = bricks[0]
            mesh.name = f"Block_{number:02d}_course_{order:02d}"
            mesh.animation_data_clear()
            world = mesh.matrix_world.copy()
            mesh.parent = anchor
            mesh.matrix_parent_inverse = anchor.matrix_world.inverted()
            mesh.matrix_world = world
            pieces.append({"name": mesh.name, "block": number, "order": order, "center": [(part_low[j]+part_high[j])/2 for j in range(3)], "size": [part_high[j]-part_low[j] for j in range(3)], "faces": len(mesh.data.polygons), "bricks_joined": len(bricks)})
            export_objects.append(mesh)
        bpy.context.view_layer.update()
        export_objects.append(anchor)
        metadata.setdefault("building_courses", []).extend(pieces)
        metadata["groups"].append({"name": label, "source_collection": name, "center": list(center), "size": [high[j]-low[j] for j in range(3)], "objects_joined": len(objects), "pieces_preserved": len(pieces), "faces": sum(part["faces"] for part in pieces)})
        continue

    if name == "Int Glass":
        # The lobby stair shares a collection with the perimeter glazing.
        # Preserve only bricks inside its assembled footprint; join the rest.
        stair = []
        for obj in objects:
            part_low, part_high = bounds([obj])
            if part_low[0] >= -60.001 and part_high[0] <= .001 and part_low[1] >= -60.001 and part_high[1] <= .001:
                stair.append(obj)
        stair.sort(key=lambda obj: (sum(bounds([obj])[j][2] for j in (0, 1)), obj.name))
        pieces = []
        for index, obj in enumerate(stair):
            part_low, part_high = bounds([obj])
            world = obj.matrix_world.copy()
            obj.animation_data_clear()
            obj.name = f"Stair_piece_{index + 1:02d}"
            obj.parent = anchor
            obj.matrix_parent_inverse = anchor.matrix_world.inverted()
            obj.matrix_world = world
            pieces.append({"name": obj.name, "order": index, "center": [(part_low[j] + part_high[j]) / 2 for j in range(3)], "size": [part_high[j] - part_low[j] for j in range(3)], "transparent": all(mat.name == "Material_47_c" for mat in obj.data.materials), "faces": len(obj.data.polygons)})
        export_objects.extend(stair)
        metadata["stair_pieces"] = pieces
        objects = [obj for obj in objects if obj not in stair]

    bpy.ops.object.select_all(action="DESELECT")
    for obj in objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.join()
    mesh = objects[0]
    mesh.name = f"{label} mesh"
    mesh.animation_data_clear()
    world = mesh.matrix_world.copy()
    mesh.parent = anchor
    mesh.matrix_parent_inverse = anchor.matrix_world.inverted()
    mesh.matrix_world = world
    bpy.context.view_layer.update()
    export_objects.extend([anchor, mesh])
    metadata["groups"].append({
        "name": label,
        "source_collection": name,
        "center": [round(v, 3) for v in center],
        "size": [round(high[i] - low[i], 3) for i in range(3)],
        "objects_joined": len(objects),
        "faces": len(mesh.data.polygons),
        "materials": len(mesh.material_slots),
    })

derived_geometry = geometry_signature(export_objects)
derived_positions = [obj.matrix_world @ vertex.co for obj in export_objects
                     if obj.type == "MESH" for vertex in obj.data.vertices]
def maximum_distance(points, reference):
    tree = kdtree.KDTree(len(reference))
    for index, point in enumerate(reference):
        tree.insert(point, index)
    tree.balance()
    return max(tree.find(point)[2] for point in points)
max_error = max(maximum_distance(source_positions, derived_positions),
                maximum_distance(derived_positions, source_positions))
if (derived_geometry["vertices"] != original_geometry["vertices"] or
        derived_geometry["faces"] != original_geometry["faces"] or max_error > .001):
    raise RuntimeError("Course regrouping changed source geometry: " + repr((original_geometry, derived_geometry, max_error)))
metadata["geometry_verification"] = {"source": original_geometry, "derived": derived_geometry,
                                     "bidirectional_maximum_vertex_error": max_error,
                                     "tolerance_blender_units": .001,
                                     "matches_within_tolerance": True}

bpy.ops.object.select_all(action="DESELECT")
for obj in export_objects:
    obj.select_set(True)
bpy.ops.export_scene.gltf(
    filepath=str(HERE / "house.glb"),
    export_format="GLB",
    use_selection=True,
    export_lights=False,
    export_cameras=False,
    export_texcoords=False,
    export_normals=True,
    export_animations=False,
    export_draco_mesh_compression_enable=True,
    export_draco_mesh_compression_level=6,
    export_draco_position_quantization=14,
    export_draco_normal_quantization=10,
)
metadata["export_sha256"] = hashlib.sha256((HERE / "house.glb").read_bytes()).hexdigest()
(HERE / "house-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
print("HOUSE_EXPORT", HERE / "house.glb", (HERE / "house.glb").stat().st_size, "bytes")
