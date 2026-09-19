#!/usr/bin/env python3
"""lego-pipe-memo preflight — version-dispatching validator (011-R2 scope item 2).

Replaces the v1 reference `tools/preflight.py` (kept unedited: the register cites it).
Dispatches on `correspondence_schema`; the schema contracts live as JSON Schema files in
tools/schemas/ — those files are the canonical artifact. The subset interpreter is shared
with package_preflight.py via tools/schema_lint.py (REVIEW-025 R-06 / outcome 13).
Never crashes on malformed input: every defect is an ERROR line, exit 1.

Usage: memo_preflight.py MEMO.md REGISTER.md
Exit:  0 pass (warnings allowed) · 1 errors · 2 usage/IO

Dependency note: needs PyYAML. If the running interpreter lacks it, the CLI re-executes
itself with tools/.venv/bin/python when that exists; `tools/setup-preflight.sh` creates it.
"""
import re
import sys

from schema_lint import check_against_schema, load_schema, require_yaml

yaml = require_yaml()

SHEET_PREFIXES = {"A", "C", "F", "H", "J", "P"}


def main():
    if len(sys.argv) != 3:
        sys.stderr.write(__doc__ or "")
        return 2
    memo_path, reg_path = sys.argv[1], sys.argv[2]
    errs, warns = [], []

    try:
        raw = open(memo_path, encoding="utf-8").read()
    except OSError as e:
        sys.stderr.write(f"ERROR: cannot read memo: {e}\n")
        return 2
    try:
        regtxt = open(reg_path, encoding="utf-8").read()
    except OSError as e:
        sys.stderr.write(f"ERROR: cannot read register: {e}\n")
        return 2

    m = re.match(r"^---\n(.*?)\n---\s*\n", raw, re.S)
    if not m:
        print(f"{memo_path}: schema=none")
        print("  ERROR no frontmatter (opening/closing --- fence not found)")
        return 1
    fm_text, body = m.group(1), raw[m.end():]

    if "\t" in fm_text:
        errs.append("tab in frontmatter")
    tops = re.findall(r"^([A-Za-z_][\w-]*):", fm_text, re.M)
    dups = {k for k in tops if tops.count(k) > 1}
    if dups:
        errs.append(f"duplicate keys {sorted(dups)}")

    try:
        fm = yaml.safe_load(fm_text)
    except yaml.YAMLError as e:
        print(f"{memo_path}: schema=unparseable")
        print(f"  ERROR frontmatter is not valid YAML: {str(e).splitlines()[0]}")
        return 1
    if not isinstance(fm, dict):
        print(f"{memo_path}: schema=unparseable")
        print("  ERROR frontmatter did not parse to a mapping")
        return 1

    schema_id = fm.get("correspondence_schema")
    version = {"lego-pipe-memo/v1": "v1", "lego-pipe-memo/v2": "v2"}.get(str(schema_id))
    if version is None:
        errs.append(f"unknown correspondence_schema {schema_id!r} (expected lego-pipe-memo/v1 or /v2)")
        version = "v1"  # evaluate against operative schema so the report is still useful
    schema = load_schema(f"lego-pipe-memo.{version}")
    check_against_schema(fm, schema, errs)

    argument = str(fm.get("argument", "") or "")
    if not argument.lstrip().startswith("In which"):
        (errs if version == "v2" else warns).append('argument does not begin "In which"')

    if version == "v2":
        for rk in schema.get("x-retired-keys", []):
            if rk in fm:
                errs.append(f"retired key present: {rk}")
        if isinstance(fm.get("to"), str) or (
            isinstance(fm.get("to"), list) and any(isinstance(e, str) for e in fm["to"])
        ):
            errs.append("to: string form is retired in v2 — use {actor, role, provider} mappings")
        if fm.get("memo_type") in {"handoff", "work_order"} and "parts" not in fm:
            errs.append(f"parts required for memo_type {fm.get('memo_type')}")
        if "register_version_read" not in fm:
            warns.append("register_version_read absent (session-checklist item)")

    # ---- finding-ID discipline ----
    pattern = schema["x-body-rules"]["finding_id_pattern"]
    used = set(re.findall(pattern, body))
    declared_entries = fm.get("findings") or []
    declared = {f.get("id") for f in declared_entries if isinstance(f, dict)}
    if version == "v1":
        if "findings" in fm:
            undeclared = sorted(u for u in used if u not in declared)
            if undeclared:
                errs.append(f"finding ids used but not declared: {undeclared}")
    else:
        undeclared = sorted(u for u in used if u not in declared)
        if undeclared:
            errs.append(
                f"finding ids used but not declared: {undeclared}"
                + ("" if "findings" in fm else " (findings: key required when the body cites reserved-namespace IDs)")
            )
        bad_declared = sorted(
            str(d) for d in declared
            if not re.fullmatch(r"(R|N|X|S|Q|K|OD|D)-\d{2}", str(d))
        )
        if bad_declared:
            errs.append(f"finding ids outside the reserved namespace: {bad_declared}")
        sheet_cited = sorted(set(re.findall(r"\b([ACFHJP]-\d{2})\b", body)) - used)
        f_cited = [s for s in sheet_cited if s.startswith("F-")]
        if f_cited:
            errs.append(
                f"F-nn cited as finding ids in a v2 memo: {f_cited} — F- is a sheet prefix; "
                "021's F-01…F-08 are frozen aliases for S-15…S-22"
            )

    # ---- register cross-checks ----
    memo_id = fm.get("memo")
    if isinstance(memo_id, str) and memo_id:
        num = memo_id.split("-")[-1]
        key = f"{num}-{fm.get('revision')}"
        if key in regtxt and "superseded" not in regtxt.split(key, 1)[1].split("\n", 1)[0]:
            warns.append(f"{key} already listed in register (expected on re-run)")
    else:
        errs.append("memo identifier missing — register uniqueness not checkable")
        num = None

    irt = fm.get("in_reply_to")
    if irt:
        n = str(irt.get("memo") if isinstance(irt, dict) else irt).split("-")[-1]
        if n not in regtxt:
            errs.append(f"in_reply_to {n} not in register")
    sup = fm.get("supersedes")
    if sup:
        parts = str(sup).split("-")
        target = parts[-2] if len(parts) >= 2 else str(sup)
        if target not in regtxt:
            errs.append(f"supersedes {sup} not in register")

    thread = fm.get("thread")
    tm = re.search(r"Current names:\s*([^\n]+)", regtxt)
    if thread and tm:
        names = {t.strip().strip("`.") for t in tm.group(1).split(",")}
        if thread not in names:
            warns.append(f"thread {thread!r} not in the register's rule-16 list ({sorted(names)})")

    print(
        f"{memo_path}: schema={schema_id} memo={memo_id} rev={fm.get('revision')} "
        f"status={fm.get('status')} keys={len(fm)} findings={len(declared_entries)} ids_used_in_body={len(used)}"
    )
    for w in warns:
        print("  WARN", w)
    for e in errs:
        print("  ERROR", e)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
