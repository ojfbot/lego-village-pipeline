"""Verify the committed cut rather than counting local install/build artifacts."""
from pathlib import Path
import importlib.util
import json
import subprocess
import sys
import tarfile
import tempfile

package = Path(__file__).resolve().parents[1]
repo = Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], cwd=package, text=True).strip())
relative = package.relative_to(repo).as_posix()
receipt = json.loads((package.parent / 'HOUSE-WORLD-R0-RECEIPT.json').read_text())
spec = importlib.util.spec_from_file_location('design_pkg', repo / 'tools/design_pkg.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

with tempfile.TemporaryDirectory(prefix='house-world-received-') as directory:
    scratch = Path(directory)
    archive = scratch / 'source.tar'
    with archive.open('wb') as stream:
        subprocess.run(['git', 'archive', f'HEAD:{relative}'], cwd=repo, stdout=stream, check=True)
    source = scratch / 'source'
    source.mkdir()
    with tarfile.open(archive) as stream:
        stream.extractall(source, filter='data')
    tree, size, count, errors = module.tree_sha256(source)
    actual = {'tree_sha256': tree, 'bytes': size, 'file_count': count}
    if errors or any(actual[key] != receipt[key] for key in actual):
        raise SystemExit(f'Received cut differs: {actual}; {errors}')
    print(f'Received cut matches receipt: {tree}, {size} bytes, {count} files.', flush=True)
    subprocess.run([sys.executable, str(repo / 'tools/package_preflight.py'), str(source), str(repo / 'docs/correspondence/REGISTER.md')], check=True)
    subprocess.run([sys.executable, str(source / 'tools/verify_assets.py')], check=True)
