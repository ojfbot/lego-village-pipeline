#!/usr/bin/env python3
"""Package an explicit Git review revision and a separate built preview for upload."""
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
parser.add_argument('--preview-output', type=Path, required=True)
args = parser.parse_args()
repo = args.repo.resolve()
output = args.output.resolve()
preview_output = args.preview_output.resolve()
revision = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', f'{args.revision}^{{commit}}'], text=True).strip()
source = Path('docs/design/review/DT-DESIGN-R6-addendum/prototype')
subprocess.run(['git', '-C', str(repo), 'diff', '--exit-code', revision, '--', str(source), 'pnpm-lock.yaml', 'pnpm-workspace.yaml'], check=True, stdout=subprocess.DEVNULL)
preview = repo / source / 'dist'
if not (preview / 'prototypes/House World.dc.html').is_file():
    raise SystemExit('Build first with pnpm --filter house-world-r6-addendum build.')
for path in [output, preview_output]:
    path.parent.mkdir(parents=True, exist_ok=True)
paths = ['CLAUDE-DESIGN-PICKUP.md', 'CLAUDE-DESIGN-PICKUP.json', 'AGENTS.md', '.gitignore', 'package.json', 'pnpm-lock.yaml', 'pnpm-workspace.yaml', 'tools/design_pkg.py', 'tools/package_r6_pickup.py', 'docs/correspondence', 'docs/design/review/DT-DESIGN-R6-overlay', 'docs/design/review/DT-DESIGN-R6-addendum', 'docs/design/review/DT-DESIGN-R6-addendum-RECEIPT.json']
prefix = 'lego-village-r6-pickup/'
subprocess.run(['git', '-C', str(repo), 'archive', '--format=zip', f'--prefix={prefix}', f'--output={output}', revision, '--', *paths], check=True)
with ZipFile(output, 'a', compression=ZIP_DEFLATED, compresslevel=6) as archive:
    archive.writestr(prefix + 'PICKUP-ARCHIVE.json', json.dumps({'source_commit': revision, 'source': 'Tracked review-source subset of the explicit revision', 'included_git_paths': paths, 'preview_archive': preview_output.name}, indent=2) + '\n')
preview_rows = []
with ZipFile(preview_output, 'w', compression=ZIP_DEFLATED, compresslevel=6) as archive:
    for path in sorted(preview.rglob('*')):
        if not path.is_file():
            continue
        data = path.read_bytes()
        name = 'browser-preview/' + path.relative_to(preview).as_posix()
        archive.writestr(name, data)
        preview_rows.append({'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    archive.writestr('PREVIEW-ARCHIVE.json', json.dumps({'source_commit': revision, 'source_archive': output.name, 'preview': 'Prebuilt R6 addendum from matching prototype/workspace source', 'preview_files': preview_rows, 'run': 'Serve browser-preview/ as HTTP root; open /prototypes/House%20World.dc.html'}, indent=2) + '\n')
for path in [output, preview_output]:
    with ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise SystemExit(f'ZIP integrity check failed: {path}')
    data = path.read_bytes()
    receipt = {'archive': path.name, 'source_commit': revision, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    path.with_suffix('.receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt))
