#!/usr/bin/env python3
"""Verify transferred addendum bytes and preservation of the received R6 overlay."""
import hashlib
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
repo = root.parents[3]
manifest = json.loads((root / 'manifest.json').read_text())
expected = {row['path']: row for row in manifest['files']}
actual = {}
for path in root.rglob('*'):
    relative = path.relative_to(root)
    if {'node_modules', 'dist', '__pycache__'} & set(relative.parts):
        continue
    if path.is_symlink():
        raise SystemExit(f'Symbolic link is not a portable source asset: {relative}')
    if path.is_file() and relative.as_posix() != 'manifest.json':
        actual[relative.as_posix()] = path
if set(expected) != set(actual):
    raise SystemExit(f'File set differs. Missing: {set(expected)-set(actual)}. Extra: {set(actual)-set(expected)}')
for name, path in actual.items():
    data = path.read_bytes()
    row = expected[name]
    if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
        raise SystemExit(f'Received bytes differ: {name}')
for row in manifest['workspace_files']:
    data = (repo / row['path']).read_bytes()
    if hashlib.sha256(data).hexdigest() != row['sha256']:
        raise SystemExit(f'Workspace reproduction file differs: {row["path"]}')
sys.path.insert(0, str(repo / 'tools'))
from design_pkg import tree_sha256
base = manifest['base']
digest, total, count, errors = tree_sha256(repo / base['path'])
if errors or digest != base['tree_sha256'] or total != base['bytes'] or count != base['file_count']:
    raise SystemExit(f'Received R6 overlay differs: {errors}, {digest}, {total}, {count}')
print(f'Verified {len(expected)} addendum files, workspace lock/membership, and unchanged {count}-file R6 overlay.')
