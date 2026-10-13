#!/usr/bin/env python3
"""Package an explicit Git revision and its built R6 preview for Claude upload."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, required=True)
parser.add_argument('--revision', required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
repo = args.repo.resolve()
output = args.output.resolve()
revision = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', f'{args.revision}^{{commit}}'], text=True).strip()
source = Path('docs/design/review/DT-DESIGN-R6-addendum/prototype')
subprocess.run(['git', '-C', str(repo), 'diff', '--exit-code', revision, '--', str(source), 'pnpm-lock.yaml', 'pnpm-workspace.yaml'], check=True, stdout=subprocess.DEVNULL)
preview = repo / source / 'dist'
if not (preview / 'prototypes/House World.dc.html').is_file():
    raise SystemExit('Build the workspace prototype first with pnpm --filter house-world-r6-addendum build.')
output.parent.mkdir(parents=True, exist_ok=True)
prefix = 'lego-village-r6-pickup/'
subprocess.run(['git', '-C', str(repo), 'archive', '--format=zip', f'--prefix={prefix}', f'--output={output}', revision], check=True)
preview_rows = []
with ZipFile(output, 'a', compression=ZIP_DEFLATED, compresslevel=6) as archive:
    for path in sorted(preview.rglob('*')):
        if not path.is_file():
            continue
        data = path.read_bytes()
        name = prefix + 'browser-preview/' + path.relative_to(preview).as_posix()
        archive.writestr(name, data)
        preview_rows.append({'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    archive.writestr(prefix + 'PICKUP-ARCHIVE.json', json.dumps({'source_commit': revision, 'source': 'Tracked Git archive of the explicit revision', 'preview': 'Prebuilt R6 addendum from matching prototype/workspace source', 'preview_files': preview_rows, 'run': 'Serve browser-preview/ as HTTP root; open /prototypes/House%20World.dc.html'}, indent=2) + '\n')
with ZipFile(output) as archive:
    if archive.testzip() is not None:
        raise SystemExit('ZIP integrity check failed.')
data = output.read_bytes()
receipt = {'archive': output.name, 'source_commit': revision, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'preview_files': len(preview_rows)}
output.with_suffix('.receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
