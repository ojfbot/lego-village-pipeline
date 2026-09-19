#!/usr/bin/env python3
"""design-package drift report — file-level comparison of two cuts (HANDOFF-LEGO-PIPE-024-R1).

Usage:
  package_drift.py OLD_DIR NEW_DIR [--out PATH] [--old-manifest P] [--new-manifest P]

Writes a markdown report (stdout or --out; convention:
docs/design/manifests/drift-<old>-to-<new>.md — 025 R-18 deterministic names).

This report claims FILE-LEVEL CHANGE EVIDENCE, not semantic drift (025 R-07 / 026 R-08):
the package does not yet carry stable ids for states, schema requests or per-sheet asset
relations, so "spec changed" here means the mapped file's bytes changed — nothing more.
Every cell states its evidence method. Sheet attribution caveats are structural facts of
the received packages: sheets can share one spec file (Hub/D-01/J-01), a sheet's spec can
be the package README (H-01), a sheet can have no spec (D-00), and a11y baselines may
cover a subset of sheets — affected cells are labelled unattributed / unavailable.

The decisions ledger is compared by stable DEC id under the header-declared order —
never byte position — with exactly one permitted prior-row transition (a Status cell
gaining a supersession reference naming a new, higher id). A ledger breach FAILS the
report: exit 1. Otherwise exit 0 (2 = usage/IO).
"""
import json
import os
import sys

from design_pkg import compare_ledgers, file_sha256, iter_files, parse_ledger, tree_sha256
from schema_lint import require_yaml

yaml = require_yaml()


def load_index(root):
    for cand in ("index.json", "handoff/index.json"):
        p = os.path.join(root, cand)
        if os.path.isfile(p):
            try:
                return json.load(open(p, encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                return None
    return None


def load_manifest(root, explicit):
    path = explicit or os.path.join(root, "package.yaml")
    if not os.path.isfile(path):
        return None
    try:
        doc = yaml.safe_load(open(path, encoding="utf-8"))
        return doc if isinstance(doc, dict) else None
    except (OSError, yaml.YAMLError):
        return None


def load_ledger(root):
    for cand in ("decisions.md", "handoff/decisions.md"):
        p = os.path.join(root, cand)
        if os.path.isfile(p):
            return parse_ledger(open(p, encoding="utf-8").read())
    return None


def norm(path):
    return path[len("handoff/"):] if path and path.startswith("handoff/") else path


def main():
    args = sys.argv[1:]
    opts = {"--out": None, "--old-manifest": None, "--new-manifest": None}
    pos = []
    i = 0
    while i < len(args):
        if args[i] in opts:
            if i + 1 >= len(args):
                sys.stderr.write(f"ERROR: {args[i]} needs a value\n")
                return 2
            opts[args[i]] = args[i + 1]
            i += 2
        else:
            pos.append(args[i])
            i += 1
    if len(pos) != 2:
        sys.stderr.write(__doc__ or "")
        return 2
    old_dir, new_dir = pos
    for d in (old_dir, new_dir):
        if not os.path.isdir(d):
            sys.stderr.write(f"ERROR: not a directory: {d}\n")
            return 2

    old_files, oerr = iter_files(old_dir)
    new_files, nerr = iter_files(new_dir)
    old_set, new_set = set(old_files), set(new_files)
    added = sorted(new_set - old_set)
    removed = sorted(old_set - new_set)
    changed = sorted(
        p for p in (old_set & new_set)
        if file_sha256(os.path.join(old_dir, p)) != file_sha256(os.path.join(new_dir, p))
    )
    old_digest = tree_sha256(old_dir)
    new_digest = tree_sha256(new_dir)

    # ---- sheet mapping from the NEW index (fall back to old) ----
    index = load_index(new_dir) or load_index(old_dir)
    delta = set(changed) | set(added) | set(removed)

    def touched(path):
        if not path:
            return False
        return path in delta or norm(path) in delta

    spec_owners = {}
    if index:
        for s in index.get("sheets") or []:
            sp = norm(s.get("spec") or "")
            if sp:
                spec_owners.setdefault(sp, []).append(s.get("id"))

    sheet_rows = []
    if index:
        for s in index.get("sheets") or []:
            sid = s.get("id", "?")
            sp = norm(s.get("spec") or "")
            spec_cell = "—"
            if not sp:
                spec_cell = "no spec file · unavailable"
            elif touched(sp):
                owners = spec_owners.get(sp, [])
                if len(owners) > 1:
                    spec_cell = f"file changed · structural_check, unattributed (shared with {', '.join(o for o in owners if o != sid)})"
                elif sp.lower().endswith("readme.md"):
                    spec_cell = "file changed · structural_check, unattributed (spec is the package README)"
                else:
                    spec_cell = "file changed · structural_check"
            else:
                spec_cell = "unchanged · structural_check" if sp else spec_cell
            sa = norm(s.get("standalone") or "")
            stand_cell = ("file changed · structural_check" if touched(sa)
                          else ("unchanged · structural_check" if sa else "no standalone · unavailable"))
            shots = [norm(x) for x in s.get("screenshots") or []]
            shot_hits = [x for x in shots if touched(x)]
            shot_cell = (f"{len(shot_hits)} of {len(shots)} changed · structural_check (screenshot change does not prove a state change)"
                         if shot_hits else (f"unchanged ({len(shots)}) · structural_check" if shots else "none · unavailable"))
            a11y = f"a11y/{sid}.tree.json"
            a11y_cell = ("file changed · structural_check" if touched(a11y)
                         else ("unchanged · structural_check" if a11y in new_set or a11y in old_set
                               else "no baseline · unavailable (cannot distinguish unchanged from never measured)"))
            sheet_rows.append((sid, spec_cell, stand_cell, shot_cell, a11y_cell))

    # ---- ledger ----
    old_led, new_led = load_ledger(old_dir), load_ledger(new_dir)
    breaches, lnotes, new_ids = [], [], []
    ledger_line = "unavailable — a decisions.md was missing"
    if old_led and new_led:
        breaches, lnotes, new_ids = compare_ledgers(old_led, new_led)
        ledger_line = (
            f"order declared: {old_led['order']} → {new_led['order']} · "
            f"{len(new_ids)} new id(s) {new_ids or ''} · "
            f"{len(lnotes)} permitted status transition(s) · {len(breaches)} breach(es)"
        )

    # ---- manifests / fixtures / package delta ----
    om = load_manifest(old_dir, opts["--old-manifest"])
    nm = load_manifest(new_dir, opts["--new-manifest"])

    def man_field(m, key):
        return m.get(key) if m else None

    def fmt_pair(key):
        a, b = man_field(om, key), man_field(nm, key)
        if om is None and nm is None:
            return "unavailable (no manifests)"
        marker = "unchanged" if a == b else f"**{a} → {b}**"
        return f"{a} → {b} · declared" if a != b else f"{marker} ({a}) · declared"

    fixtures_line = "unavailable — no fixture identity on one or both cuts (pre-R2 packages carry none; from R2 fixture churn would otherwise dominate apparent drift — 025 R-14)"
    if man_field(om, "fixtures") and man_field(nm, "fixtures"):
        fa, fb = om["fixtures"], nm["fixtures"]
        fixtures_line = ("unchanged · declared" if fa == fb
                         else f"**fixture set changed** {fa} → {fb} · declared — separate fixture churn from design change before triage")

    on = os.path.basename(os.path.normpath(old_dir))
    nn = os.path.basename(os.path.normpath(new_dir))
    lines = []
    a = lines.append
    a(f"# Drift report — {on} → {nn}")
    a("")
    a("**Claim discipline:** this is *file-level change evidence*, not semantic drift")
    a("(025 R-07 / 026 R-08). A changed screenshot does not prove a state change; a shared")
    a("spec file cannot attribute a change to one sheet. Evidence methods:")
    a("`structural_check` (derived from bytes) · `declared` (asserted by a manifest/overlay)")
    a("· `unattributed` · `unavailable`.")
    a("")
    a("## Trees")
    a("")
    a(f"| | {on} | {nn} |")
    a("|---|---|---|")
    a(f"| tree_sha256 (measured) | `{old_digest[0]}` | `{new_digest[0]}` |")
    a(f"| files | {old_digest[2]} | {new_digest[2]} |")
    a(f"| bytes | {old_digest[1]} | {new_digest[1]} |")
    a("")
    a(f"## File-level delta · structural_check")
    a("")
    a(f"**{len(changed)} changed · {len(added)} added · {len(removed)} removed**")
    a("")
    for title, group in (("Changed", changed), ("Added", added), ("Removed", removed)):
        if group:
            a(f"### {title}")
            for p in group:
                a(f"- `{p}`")
            a("")
    a("## Per-sheet view")
    a("")
    if sheet_rows:
        a("| Sheet | Spec | Standalone | Screenshots | A11y baseline |")
        a("|---|---|---|---|---|")
        for row in sheet_rows:
            a("| " + " | ".join(row) + " |")
    else:
        a("unavailable — no index.json in either tree")
    a("")
    a("## Decisions ledger · structural_check (compared by DEC id, never byte position)")
    a("")
    a(ledger_line)
    for n in lnotes:
        a(f"- {n}")
    for b in breaches:
        a(f"- **BREACH:** {b}")
    a("")
    a("## Fixtures")
    a("")
    a(fixtures_line)
    a("")
    a("## Package delta · declared (from manifests/overlays)")
    a("")
    a(f"- maturity: {fmt_pair('maturity')}")
    a(f"- tier_coverage: {fmt_pair('tier_coverage')}")
    a(f"- mock_math: {fmt_pair('mock_math')}")
    if om or nm:
        a(f"- known_defects: {len(man_field(om, 'known_defects') or [])} → {len(man_field(nm, 'known_defects') or [])} · declared")
        a(f"- debts: {len(man_field(om, 'debts') or [])} → {len(man_field(nm, 'debts') or [])} · declared")
    a("")
    a("## Triage")
    a("")
    a("- [ ] Every changed file above either maps to an expected change (a new DEC entry,")
    a("      an answered change request) or is raised with the designer.")
    a("- [ ] Ledger breaches (if any) resolved before the pin moves.")
    a("- [ ] Fixture churn separated from design change before any finding is filed.")
    a("")
    verdict = "FAIL — ledger breach(es)" if breaches else "PASS"
    a(f"**Ledger gate: {verdict}**")
    a("")
    for e in oerr + nerr:
        a(f"ERROR {e}")

    report = "\n".join(lines)
    if opts["--out"]:
        with open(opts["--out"], "w", encoding="utf-8") as f:
            f.write(report + "\n")
        print(f"wrote {opts['--out']} ({'FAIL' if breaches else 'PASS'})")
    else:
        print(report)
    return 1 if (breaches or oerr or nerr) else 0


if __name__ == "__main__":
    sys.exit(main())
