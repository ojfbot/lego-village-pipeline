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
        "null": type(None),
    }
    if isinstance(ty, list):
        return any(type_ok(value, t) for t in ty)
    exp = m.get(ty)
    if exp is None:
        return True
    if exp is bool:
        return isinstance(value, bool)
    if exp in ((int, float), int) and isinstance(value, bool):
        return False  # bool is an int in Python; a flag is not a number
    return isinstance(value, exp)


def _declares_null(sub):
    ty = sub.get("type")
    return ty == "null" or (isinstance(ty, list) and "null" in ty)


def check_value(value, sub, label, errs):
    """Validate one value against a schema subset, recursing into objects and arrays.

    Null is validated, never skipped (PR #13 review, both stewards): a null passes only
    where the schema declares "null" among its types, or where no type is declared at
    all. Skipping nulls made `required` mean nothing but "the key exists".
    """
    import re
    if value is None:
        if "type" in sub and not _declares_null(sub):
            errs.append(f"{label}: null not permitted (type {sub['type']})")
        elif "const" in sub:
            errs.append(f"{label}: expected {sub['const']!r}, got None")
        elif "enum" in sub and None not in sub["enum"]:
            errs.append(f"{label}: None not in {sub['enum']}")
        return

    if "const" in sub and value != sub["const"]:
        errs.append(f"{label}: expected {sub['const']!r}, got {value!r}")
    if "enum" in sub and value not in sub["enum"]:
        errs.append(f"{label}: {value!r} not in {sub['enum']}")
    if "type" in sub and not type_ok(value, sub["type"]):
        errs.append(f"{label}: wrong type {type(value).__name__}")
    if "pattern" in sub and isinstance(value, str) and not re.fullmatch(sub["pattern"], value):
        errs.append(f"{label}: {value!r} does not match {sub['pattern']}")

    if isinstance(value, dict):
        for rk in sub.get("required", []):
            if rk not in value:
                errs.append(f"{label}.{rk} missing")
        for pk, psub in (sub.get("properties") or {}).items():
            if pk in value:
                check_value(value[pk], psub, f"{label}.{pk}", errs)
    elif isinstance(value, list):
        isub = sub.get("items")
        if isinstance(isub, dict) and isub:
            for i, entry in enumerate(value):
                if isub.get("required") and not isinstance(entry, dict):
                    errs.append(f"{label}[{i}]: must be a mapping")
                    continue
                check_value(entry, isub, f"{label}[{i}]", errs)


def check_against_schema(fm, schema, errs):
    for k in schema.get("required", []):
        if k not in fm:
            errs.append(f"missing {k}")
    for k, sub in schema.get("properties", {}).items():
        if k in fm:
            check_value(fm[k], sub, k, errs)
