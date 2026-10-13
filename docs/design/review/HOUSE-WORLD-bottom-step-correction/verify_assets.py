"""Verify the received correction pair and its preserved Blender source."""
from pathlib import Path
import hashlib
import json
import struct

root = Path(__file__).resolve().parent
manifest = json.loads((root / "manifest.json").read_text())
for item in manifest["files"]:
    path = root / item["path"]
    data = path.read_bytes()
    assert len(data) == item["bytes"], f"Size differs: {path}"
    assert hashlib.sha256(data).hexdigest() == item["sha256"], f"Hash differs: {path}"
source = root.parent / "HOUSE-WORLD-R0/assets/blender/legoHouse.blend"
assert hashlib.sha256(source.read_bytes()).hexdigest() == manifest["source_sha256"], "Source model differs"
metadata = json.loads((root / "house-metadata.json").read_text())
blob = (root / "house.glb").read_bytes()
magic, version, length = struct.unpack_from("<III", blob)
assert (magic, version, length) == (0x46546C67, 2, len(blob)), "Invalid GLB header"
assert hashlib.sha256(blob).hexdigest() == metadata["export_sha256"], "GLB and metadata do not match"
chunk_length, chunk_type = struct.unpack_from("<II", blob, 12)
assert chunk_type == 0x4E4F534A, "GLB JSON chunk missing"
gltf = json.loads(blob[20:20 + chunk_length])
expected = ["Block_01_course_00", "Block_01_course_01", "Block_01_course_02"]
assert sorted(node["name"] for node in gltf["nodes"] if node.get("name", "").startswith("Block_01_course_")) == expected
courses = [part for part in metadata["building_courses"] if part["block"] == 1]
assert [part["name"] for part in courses] == expected
assert courses[0]["bricks_joined"] == 18, "Bottom step is not joined to its adjoining course"
assert len(metadata["building_courses"]) == 76
assert metadata["source_sha256"] == manifest["source_sha256"]
print(f"Correction verified: {len(manifest['files'])} files; paired GLB and metadata; 76 courses; unchanged source.")
