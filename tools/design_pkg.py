#!/usr/bin/env python3
"""Shared design-package helpers (HANDOFF-LEGO-PIPE-024-R1).

Library for package_preflight.py and package_drift.py, plus the reference
implementation of the tree digest:

    python3 tools/design_pkg.py digest DIR      # tree_sha256, bytes, file count

Tree digest (normative — design-package-import/v1 x-tree-digest-spec): regular files
only (symlinks and special files are an error), POSIX relative paths sorted bytewise,
per-file sha256 over bytes, tree digest = sha256 of the UTF-8 concatenation of
'<hex>  <path>\\n' lines (sha256sum-manifest style). Modes and mtimes are ignored.
"""
import hashlib
import os
import re
import sys

SHEET_ID_RE = re.compile(r"^[A-Z]{1,2}-\d{2}$")
MEMO_REF_RE = re.compile(r"^(HANDOFF|CORR|REVIEW)-LEGO-PIPE-\d{3}-R\d+$")
DEC_ID_RE = re.compile(r"DEC-(\d{3})")


def iter_files(root):
    """Sorted POSIX relative paths of regular files under root. Errors on symlinks."""
    out, errors = [], []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            if os.path.islink(full):
                errors.append(f"symlink in tree: {rel}")
                continue
            if not os.path.isfile(full):
                errors.append(f"special file in tree: {rel}")
                continue
            out.append(rel)
    return sorted(out), errors


def tree_sha256(root):
    """(digest_hex, total_bytes, file_count, errors) per the normative spec."""
    paths, errors = iter_files(root)
    lines, total = [], 0
    for rel in paths:
        full = os.path.join(root, rel)
        h = hashlib.sha256()
        with open(full, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
                total += len(chunk)
        lines.append(f"{h.hexdigest()}  {rel}\n")
    digest = hashlib.sha256("".join(lines).encode("utf-8")).hexdigest()
    return digest, total, len(paths), errors


def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---- decisions.md ----

def parse_ledger(text):
    """Parse a decisions.md ledger.

    Returns {order, entries, duplicate_ids} where entries is a list of
    {id, num, cells, raw} in file order and cells are the pipe-split columns.
    Declared order is read from the header text (025 R-08: read, never assume).
    """
    order = "unknown"
    head = text[:2000].lower()
    if "newest first" in head:
        order = "newest-first"
    elif "oldest first" in head:
        order = "oldest-first"
    entries, seen, dups = [], set(), []
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or not re.fullmatch(r"DEC-\d{3}", cells[0]):
            continue
        dec_id = cells[0]
        if dec_id in seen:
            dups.append(dec_id)
        seen.add(dec_id)
        entries.append({
            "id": dec_id,
            "num": int(dec_id.split("-")[1]),
            "cells": cells,
            "raw": line.strip(),
        })
    return {"order": order, "entries": entries, "duplicate_ids": dups}


def _status_cell_index(cells):
    # Ledger columns: ID | When | Decision | Touches | Status | Effective revision | Supersedes
    return 4 if len(cells) >= 5 else None


def compare_ledgers(old, new):
    """Compare two parsed ledgers by stable DEC id (never byte position).

    Exactly one prior-row transition is permitted: the Status cell may gain a
    supersession reference naming a new, higher id (verified convention: DEC-029
    'superseded by DEC-030', DEC-025 'placement superseded by DEC-034').
    Returns (breaches, notes, new_ids).
    """
    breaches, notes = [], []
    old_by = {e["id"]: e for e in old["entries"]}
    new_by = {e["id"]: e for e in new["entries"]}

    for dec_id, o in old_by.items():
        n = new_by.get(dec_id)
        if n is None:
            breaches.append(f"{dec_id} removed — every prior decision must remain present")
            continue
        if o["raw"] == n["raw"]:
            continue
        si = _status_cell_index(o["cells"])
        cells_equal_otherwise = (
            si is not None
            and len(o["cells"]) == len(n["cells"])
            and all(a == b for i, (a, b) in enumerate(zip(o["cells"], n["cells"])) if i != si)
        )
        if cells_equal_otherwise:
            refs = [int(m) for m in DEC_ID_RE.findall(n["cells"][si])]
            if "supersed" in n["cells"][si] and refs and max(refs) > o["num"]:
                notes.append(
                    f"{dec_id} status gained a supersession reference "
                    f"(the one permitted transition): {n['cells'][si]!r}"
                )
                continue
        breaches.append(f"{dec_id} changed beyond the permitted status transition")

    new_ids = sorted((e["num"] for e in new["entries"] if e["id"] not in old_by))
    if new_ids:
        max_old = max((e["num"] for e in old["entries"]), default=0)
        expected = list(range(max_old + 1, max_old + 1 + len(new_ids)))
        if new_ids != expected:
            breaches.append(
                f"new ids not unique+contiguous after DEC-{max_old:03d}: "
                f"got {['DEC-%03d' % n for n in new_ids]}"
            )
    return breaches, notes, [f"DEC-{n:03d}" for n in new_ids]


# ---- index.json reference classification ----

def collect_index_refs(index):
    """Classify every structured path in index.json (025 R-01 / 026 R-04).

    Returns a list of (path, ref_type, where): ref_type is 'design_source' for
    sheets[].file (opaque design-session provenance, never resolved) and
    'package_path' for everything else.
    """
    refs = []

    def add(p, ty, where):
        if isinstance(p, str) and p:
            refs.append((p, ty, where))

    add(index.get("tokens"), "package_path", "tokens")
    for i, b in enumerate(index.get("brief") or []):
        add(b, "package_path", f"brief[{i}]")
    for k, v in (index.get("ledgers") or {}).items():
        add(v, "package_path", f"ledgers.{k}")
    for s in index.get("sheets") or []:
        sid = s.get("id", "?")
        add(s.get("file"), "design_source", f"sheets[{sid}].file")
        add(s.get("spec"), "package_path", f"sheets[{sid}].spec")
        add(s.get("standalone"), "package_path", f"sheets[{sid}].standalone")
        for j, sc in enumerate(s.get("screenshots") or []):
            add(sc, "package_path", f"sheets[{sid}].screenshots[{j}]")
    for i, st in enumerate(index.get("state_screenshots") or []):
        add(st.get("file"), "package_path", f"state_screenshots[{i}].file")
    rr = index.get("review_round") or {}
    add(rr.get("brief"), "package_path", "review_round.brief")
    return refs


def resolve_ref(root, path, strip_prefix=None):
    """Resolve a package_path inside root. Returns (status, resolved_rel).

    status: 'as-written' | 'stripped' | 'unresolved' | 'escape'.
    Containment is checked with realpath — escaping the package root is never
    waivable (design-package/v1 x-never-designer-waivable).
    """
    root_real = os.path.realpath(root)

    def inside(candidate_rel):
        full = os.path.realpath(os.path.join(root, candidate_rel))
        if not (full == root_real or full.startswith(root_real + os.sep)):
            return "escape"
        return "ok" if os.path.isfile(full) else "missing"

    st = inside(path)
    if st == "escape":
        return "escape", None
    if st == "ok":
        return "as-written", path
    if strip_prefix and path.startswith(strip_prefix):
        stripped = path[len(strip_prefix):]
        st2 = inside(stripped)
        if st2 == "escape":
            return "escape", None
        if st2 == "ok":
            return "stripped", stripped
    return "unresolved", None


# ---- register lookups ----

def register_rows(regtxt):
    """Parse the correspondence table: number-revision → status cell text."""
    rows = {}
    for line in regtxt.splitlines():
        m = re.match(r"^\|\s*([0-9]{3}(?:-R\d+)?)[^|]*\|", line)
        if m:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            rows[m.group(1)] = cells[-1] if cells else ""
    return rows


def memo_ref_operative(ref, regtxt):
    """('ok'|'unknown'|'superseded'|'malformed', detail) for a fully qualified memo ref
    against the register table's Number column (025 R-17: exact row, never substring)."""
    if not MEMO_REF_RE.fullmatch(str(ref)):
        return "malformed", f"{ref!r} is not a fully qualified memo revision"
    num_rev = str(ref).split("LEGO-PIPE-")[1]  # e.g. 014-R0
    rows = register_rows(regtxt)
    status = rows.get(num_rev)
    if status is None:
        status = rows.get(num_rev.split("-")[0])  # rows keyed without revision
    if status is None:
        return "unknown", f"{num_rev} has no row in the register table"
    if status.lower().startswith("**superseded") or status.lower().startswith("superseded"):
        return "superseded", f"{num_rev} row is superseded"
    return "ok", num_rev


def instruments_rows(regtxt):
    """Parse the instruments table if present: list of dicts keyed by column header."""
    lines = regtxt.splitlines()
    rows, headers, in_table = [], None, False
    for line in lines:
        if re.match(r"^\|\s*Instrument\s*\|", line):
            headers = [c.strip() for c in line.strip().strip("|").split("|")]
            in_table = True
            continue
        if in_table:
            if not line.lstrip().startswith("|"):
                in_table = False
                headers = None
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if cells and set(c.strip("-: ") for c in cells) == {""}:
                continue  # separator row
            if headers and len(cells) >= 3:
                rows.append(dict(zip(headers, cells)))
    return rows


INV_BEGIN = "<!-- inventory:begin (generated by `python3 tools/design_pkg.py inventory docs/design --write` — never hand-edit) -->"
INV_END = "<!-- inventory:end -->"


def build_inventory(design_dir):
    """Render the docs/design/README.md inventory table from manifests/ (025 Q2:
    generated from the manifests, regenerated by the import tooling, never hand-edited)."""
    from schema_lint import require_yaml
    yaml = require_yaml()
    man_dir = os.path.join(design_dir, "manifests")
    rows = []
    for name in sorted(os.listdir(man_dir)) if os.path.isdir(man_dir) else []:
        if not (name.endswith(".overlay.yaml") or name.endswith(".import.yaml")):
            continue
        doc = yaml.safe_load(open(os.path.join(man_dir, name), encoding="utf-8"))
        if not isinstance(doc, dict):
            continue
        kind = "overlay" if name.endswith(".overlay.yaml") else "import record"
        rows.append({
            "key": (doc.get("design_package", "?"), doc.get("revision", "?"), doc.get("cut_state", "?")),
            "kind": kind,
            "file": f"manifests/{name}",
            "path": doc.get("package_path", "—"),
            "tree": doc.get("tree_sha256") or "—",
            "brief": doc.get("governing_brief", "—"),
        })
    # Merge overlay + import record for the same cut key into one line each kind listed
    lines = [
        "| Cut key {package · revision · cut_state} | Package path | tree_sha256 | Governing brief | Record |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        k = r["key"]
        tree = r["tree"] if r["tree"] == "—" else f"`{r['tree']}`"
        lines.append(
            f"| {k[0]} · {k[1]} · {k[2]} | `{r['path']}` | {tree} | {r['brief']} | [{r['kind']}]({r['file']}) |"
        )
    return "\n".join(lines)


def write_inventory(design_dir):
    readme = os.path.join(design_dir, "README.md")
    text = open(readme, encoding="utf-8").read()
    if INV_BEGIN not in text or INV_END not in text:
        sys.stderr.write("ERROR: inventory markers not found in README.md\n")
        return 1
    head, rest = text.split(INV_BEGIN, 1)
    _, tail = rest.split(INV_END, 1)
    table = build_inventory(design_dir)
    open(readme, "w", encoding="utf-8").write(head + INV_BEGIN + "\n" + table + "\n" + INV_END + tail)
    print(f"inventory regenerated in {readme}")
    return 0


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "digest":
        root = sys.argv[2]
        if not os.path.isdir(root):
            sys.stderr.write(f"ERROR: not a directory: {root}\n")
            return 2
        digest, total, count, errors = tree_sha256(root)
        for e in errors:
            print(f"ERROR {e}")
        print(f"tree_sha256: {digest}")
        print(f"bytes: {total}")
        print(f"file_count: {count}")
        return 1 if errors else 0
    if len(sys.argv) >= 3 and sys.argv[1] == "inventory":
        design_dir = sys.argv[2]
        if "--write" in sys.argv[3:]:
            return write_inventory(design_dir)
        print(build_inventory(design_dir))
        return 0
    sys.stderr.write(__doc__ or "")
    return 2


if __name__ == "__main__":
    sys.exit(main())
