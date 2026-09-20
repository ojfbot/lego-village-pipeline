#!/usr/bin/env python3
"""Shared schema-interpreter for the preflight CLIs (REVIEW-025 R-06 / acceptance outcome 13).

Extracted verbatim from tools/memo_preflight.py at register 2026-09-18.26 so that
memo_preflight.py and package_preflight.py interpret JSON Schema subsets through ONE
implementation — a comment is not a mechanism; a shared module is. The v1 reference
tools/preflight.py is frozen (register rows cite it) and does not import this module.

The canonical contract artifacts are the JSON Schema files in tools/schemas/; this module
interprets the subset they use: required, properties, const, enum, type, pattern,
nested required, items.required, additionalProperties, and (since HANDOFF-032) the
combinators oneOf / anyOf / allOf / not. Extend here, never by copy.
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
        hint = ""
        if sub.get("format") == "date" and type(value).__name__ in ("date", "datetime"):
            hint = " — quote the date in YAML so it parses as a string"
        errs.append(f"{label}: wrong type {type(value).__name__}{hint}")
    if "pattern" in sub and isinstance(value, str) and not re.fullmatch(sub["pattern"], value):
        errs.append(f"{label}: {value!r} does not match {sub['pattern']}")
    if "minLength" in sub and isinstance(value, str) and len(value.strip()) < sub["minLength"]:
        errs.append(f"{label}: blank or too short — a named value is required, got {value!r}")
    if sub.get("format") == "date" and isinstance(value, str) and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        errs.append(f"{label}: {value!r} is not a YYYY-MM-DD date")

    # Combinators (register-version/v1, HANDOFF-032 R0 §4 item 8): a per-kind contract
    # is a `oneOf` over branches that each `required`/`not`-forbid keys of the SAME object.
    # Additive — no existing schema under tools/schemas/ uses these keywords, so the memo
    # corpus differential (tests/test_design_package.py) is the proof nothing else moved.
    if "oneOf" in sub:
        matched = [b for b in sub["oneOf"] if not _errs_of(value, b, label)]
        if len(matched) != 1:
            errs.append(f"{label}: matches {len(matched)} of {len(sub['oneOf'])} oneOf branches (exactly 1 required)")
    if "anyOf" in sub:
        if not any(not _errs_of(value, b, label) for b in sub["anyOf"]):
            errs.append(f"{label}: matches none of {len(sub['anyOf'])} anyOf branches")
    if "allOf" in sub:
        for i, b in enumerate(sub["allOf"]):
            for e in _errs_of(value, b, label):
                errs.append(f"{label}: allOf[{i}]: {e}")
    if "not" in sub:
        if not _errs_of(value, sub["not"], label):
            errs.append(f"{label}: matches a forbidden shape ({_describe(sub['not'])})")

    if isinstance(value, dict):
        for rk in sub.get("required", []):
            if rk not in value:
                errs.append(f"{label}.{rk} missing")
        props = sub.get("properties") or {}
        for pk, psub in props.items():
            if pk in value:
                check_value(value[pk], psub, f"{label}.{pk}", errs)
        # Dynamic maps (e.g. the overlay's per-field `evidence`) declare their VALUE
        # schema here. Without it the map is unenforced however well-typed it reads
        # (PR #13 third review round).
        extra = sub.get("additionalProperties")
        if isinstance(extra, dict) and extra:
            for pk, pv in value.items():
                if pk not in props:
                    check_value(pv, extra, f"{label}.{pk}", errs)
        elif extra is False:
            for pk in value:
                if pk not in props:
                    errs.append(f"{label}.{pk}: unexpected key")
    elif isinstance(value, list):
        isub = sub.get("items")
        if isinstance(isub, dict) and isub:
            for i, entry in enumerate(value):
                if isub.get("required") and not isinstance(entry, dict):
                    errs.append(f"{label}[{i}]: must be a mapping")
                    continue
                check_value(entry, isub, f"{label}[{i}]", errs)


def _errs_of(value, sub, label):
    """Errors a value would raise against a sub-schema, without touching the caller's list."""
    inner = []
    check_value(value, sub, label, inner)
    return inner


def _describe(sub):
    keys = []
    if "required" in sub:
        keys.append("required " + "/".join(sub["required"]))
    if "anyOf" in sub:
        keys.append("anyOf " + ", ".join(_describe(b) for b in sub["anyOf"]))
    if "const" in sub:
        keys.append(f"const {sub['const']!r}")
    return "; ".join(keys) or "schema"


def check_against_schema(fm, schema, errs):
    for k in schema.get("required", []):
        if k not in fm:
            errs.append(f"missing {k}")
    for k, sub in schema.get("properties", {}).items():
        if k in fm:
            check_value(fm[k], sub, k, errs)
    # Top-level combinators and additionalProperties are delegated to check_value so a
    # document-level `oneOf` (the register-version per-kind contract) is enforced too.
    top = {k: v for k, v in schema.items() if k in ("oneOf", "anyOf", "allOf", "not", "additionalProperties")}
    if top:
        if "additionalProperties" in top:
            top["properties"] = schema.get("properties", {})
        check_value(fm, top, "document", errs)
