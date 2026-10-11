"""Verify the received source and derivative bytes from the package manifest."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / 'assets/manifest.json').read_text())
for item in manifest['files']:
    path = (root / item['path']).resolve()
    if not path.is_relative_to(root):
        raise SystemExit(f"Asset path escapes the package: {item['path']}")
    data = path.read_bytes()
    if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
        raise SystemExit(f"Asset bytes differ: {item['path']}")
print(f"Verified {len(manifest['files'])} source, audit and derivative files.")
