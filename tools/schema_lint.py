#!/usr/bin/env python3
"""Shared schema-interpreter for the preflight CLIs (REVIEW-025 R-06 / acceptance outcome 13).

Extracted verbatim from tools/memo_preflight.py at register 2026-09-18.26 so that
memo_preflight.py and package_preflight.py interpret JSON Schema subsets through ONE
implementation — a comment is not a mechanism; a shared module is. The v1 reference
tools/preflight.py is frozen (register rows cite it) and does not import this module.

The canonical contract artifacts are the JSON Schema files in tools/schemas/; this module
interprets the subset they use: required, properties, const, enum, type, pattern,
nested required, items.required. Extend here, never by copy.
"""
import json
import os
import sys

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))


def require_yaml(env_flag="MEMO_PREFLIGHT_REEXEC"):
    """Import PyYAML, re-executing the calling script under tools/.venv if needed.

    tools/setup-preflight.sh creates the venv. Returns the yaml module or exits 2.
    """
    try:
        import yaml
        return yaml
    except ImportError:
        venv_py = os.path.join(TOOLS_DIR, ".venv", "bin", "python")
        script = os.path.abspath(sys.argv[0])
        if os.path.exists(venv_py) and not os.environ.get(env_flag):
            os.environ[env_flag] = "1"
            os.execv(venv_py, [venv_py, script] + sys.argv[1:])
        sys.stderr.write(
            "ERROR: PyYAML not available. Run tools/setup-preflight.sh once to create tools/.venv\n"
        )
        sys.exit(2)


def load_schema(stem):
    """Load tools/schemas/<stem>.schema.json (e.g. 'lego-pipe-memo.v2', 'design-package.v1')."""
    p = os.path.join(TOOLS_DIR, "schemas", f"{stem}.schema.json")
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def type_ok(value, ty):
    m = {
        "object": dict, "array": list, "string": str,
        "number": (int, float), "integer": int, "boolean": bool,
    }
    if isinstance(ty, list):
        return any(type_ok(value, t) for t in ty)
    exp = m.get(ty)
    return exp is None or isinstance(value, exp)


def check_against_schema(fm, schema, errs):
    import re
    for k in schema.get("required", []):
        if k not in fm:
            errs.append(f"missing {k}")
    for k, sub in schema.get("properties", {}).items():
        if k not in fm or fm[k] is None:
            continue
        v = fm[k]
        if "const" in sub and v != sub["const"]:
            errs.append(f"{k}: expected {sub['const']!r}, got {v!r}")
        if "enum" in sub and v not in sub["enum"]:
            errs.append(f"{k}: {v!r} not in {sub['enum']}")
        if "type" in sub and not type_ok(v, sub["type"]):
            errs.append(f"{k}: wrong type {type(v).__name__}")
        if "pattern" in sub and isinstance(v, str) and not re.fullmatch(sub["pattern"], v):
            errs.append(f"{k}: {v!r} does not match {sub['pattern']}")
        for rk in sub.get("required", []):
            if isinstance(v, dict) and rk not in v:
                errs.append(f"{k}.{rk} missing")
        item_req = sub.get("items", {}).get("required", [])
        if item_req and isinstance(v, list):
            for i, entry in enumerate(v):
                if not isinstance(entry, dict):
                    errs.append(f"{k}[{i}]: must be a mapping")
                    continue
                for rk in item_req:
                    if rk not in entry:
                        errs.append(f"{k}[{i}].{rk} missing")
