#!/bin/sh
# One-time setup for tools/memo_preflight.py: creates tools/.venv with PyYAML,
# fixing the recorded gotcha that macOS system python3 lacks it (register .11).
set -eu
cd "$(dirname "$0")"
python3 -m venv .venv
./.venv/bin/pip install --quiet pyyaml
echo "OK: tools/.venv ready; memo_preflight.py will use it automatically."
