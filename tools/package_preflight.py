#!/usr/bin/env python3
"""design-package preflight — structural admission check (HANDOFF-LEGO-PIPE-024-R1).

Usage:
  package_preflight.py PACKAGE_DIR REGISTER.md [--overlay PATH]
                       [--import-record PATH] [--previous PREV_DIR]

A designer cut carries package.yaml (design-package/v1) at its root; a historical cut
has no designer manifest and is described by an importer overlay (--overlay,
design-package-overlay/v1). Exactly one of the two must be present.

Every result line names its evidence method (025 R-07 / 026 R-06):
  [structural_check]  derived mechanically from the committed bytes
  [measured]          recomputed digests
  [declared]          asserted by a cited document, not verified by this tool
  [unavailable]       input this tool needed but could not find
This tool performs ONLY structural checks. Runtime facts (contrast, CDN fetches,
landmark coverage, file:// behaviour — D-1/D-3/D-5/D-6) are reported as declared
observations citing their source; the tool never claims to verify them.

Never crashes on malformed input: defects are ERROR lines. Exit 0 pass / 1 errors / 2 usage-IO.
Interpreter shared with memo_preflight.py via schema_lint.py (outcome 13).
"""
import json
import os
import sys

from design_pkg import (
    SHEET_ID_RE, read_json, read_text, collect_index_refs, compare_ledgers, cut_state_vocabulary,
    instruments_rows, memo_ref_operative, parse_ledger, resolve_ref, tree_sha256,
)
from schema_lint import check_against_schema, check_value, load_schema, require_yaml

yaml = require_yaml()

NON_WAIVABLE_NOTE = "identity, digest mismatch, package-root escape and missing manifest are never designer-waivable"


def load_yaml_doc(path, errs, label):
    try:
        with open(path, encoding="utf-8") as f:
            doc = yaml.safe_load(f)
    except OSError as e:
        errs.append(f"[structural_check] cannot read {label}: {e}")
        return None
    except yaml.YAMLError as e:
        errs.append(f"[structural_check] {label} is not valid YAML: {str(e).splitlines()[0]}")
        return None
    if not isinstance(doc, dict):
        errs.append(f"[structural_check] {label} did not parse to a mapping")
        return None
    return doc


def main():
    args = sys.argv[1:]
    opts = {"--overlay": None, "--import-record": None, "--previous": None}
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
    pkg_dir, reg_path = pos
    errs, warns, notes = [], [], []

    if not os.path.isdir(pkg_dir):
        sys.stderr.write(f"ERROR: not a directory: {pkg_dir}\n")
        return 2
    try:
        regtxt = read_text(reg_path)
    except OSError as e:
        sys.stderr.write(f"ERROR: cannot read register: {e}\n")
        return 2

    # ---- locate the manifest: designer package.yaml XOR importer overlay ----
    pkg_yaml = os.path.join(pkg_dir, "package.yaml")
    has_designer = os.path.isfile(pkg_yaml)
    historical = opts["--overlay"] is not None
    if has_designer and historical:
        errs.append("[structural_check] both package.yaml and --overlay present — a cut has exactly one description")
    if not has_designer and not historical:
        print(f"{pkg_dir}: manifest=MISSING")
        print(f"  ERROR [structural_check] no package.yaml in the tree and no --overlay given — {NON_WAIVABLE_NOTE}")
        print("  ERROR [structural_check] a manifest-less cut is recorded, not imported (disposition recorded_not_imported); the previous pin does not move")
        return 1

    if has_designer:
        manifest = load_yaml_doc(pkg_yaml, errs, "package.yaml")
        schema = load_schema("design-package.v1")
        origin = "designer"
    else:
        manifest = load_yaml_doc(opts["--overlay"], errs, "overlay")
        schema = load_schema("design-package-overlay.v1")
        origin = "importer_reconstructed"
    if manifest is None:
        print(f"{pkg_dir}: manifest=unparseable origin={origin}")
        for e in errs:
            print("  ERROR", e)
        return 1

    sferrs = []
    check_against_schema(manifest, schema, sferrs)
    errs += [f"[structural_check] {e}" for e in sferrs]

    # A designer manifest outside the exported bytes did not come from the designer.
    if historical and manifest.get("manifest_origin") == "designer":
        errs.append("[structural_check] overlay claims manifest_origin: designer — a reconstruction must never present itself as a designer manifest")

    # ---- identity: not a sheet id (025 R-19). Historical names never move (024 ruling 4):
    # the H-01 overlays record the collision rather than repair it; DT-DESIGN from cut R2. ----
    name = str(manifest.get("design_package", ""))
    if SHEET_ID_RE.fullmatch(name):
        msg = f"design_package {name!r} matches the sheet-id pattern — a package name is not a sheet id"
        if historical:
            warns.append(f"[structural_check] {msg} (recorded, not repaired: historical name; DT-DESIGN from cut R2)")
        else:
            errs.append(f"[structural_check] {msg}")

    # ---- prefix strip is overlay-only declared data (025 R-12) ----
    strip = None
    if historical:
        strip = manifest.get("path_prefix_strip")
    elif "path_prefix_strip" in manifest:
        errs.append("[structural_check] path_prefix_strip in a designer manifest — prefix normalization is reconstruction-only; fix the paths (path_base '.')")

    # ---- governing_brief / answers: exact operative register rows (025 R-17) ----
    for label, refs in (("governing_brief", [manifest.get("governing_brief")]),
                        ("answers", manifest.get("answers") or [])):
        for ref in refs:
            if ref is None:
                continue
            state, detail = memo_ref_operative(ref, regtxt)
            if state == "ok":
                notes.append(f"[structural_check] {label} {ref} → operative register row {detail}")
            elif state == "superseded":
                errs.append(f"[structural_check] {label} {ref}: {detail} — must cite the operative revision")
            else:
                errs.append(f"[structural_check] {label}: {detail}")

    # ---- mock_math (025 R-05 / outcome 15) ----
    if manifest.get("mock_math") is True:
        warns.append("[declared] MOCK MATH: every number in this package is mock; nothing here is a computed quantity. Flipping this field requires a recorded operator ruling.")
    elif manifest.get("mock_math") is False:
        warns.append("[declared] mock_math is FALSE — confirm the operator ruling that authorized real math is recorded on this cut")

    # ---- cut-key uniqueness against the instruments table (operator ruling 2026-09-19) ----
    cut_state = str(manifest.get("cut_state", ""))
    triple = (name, str(manifest.get("revision", "")), cut_state)
    vocab = cut_state_vocabulary(regtxt)
    undeclared_state = bool(vocab) and cut_state not in vocab
    if undeclared_state:
        # Rule-16 idiom: vocabulary is register data, so a new state stays legal — but it
        # is coined in the REGISTER first, never in a manifest. A typo here would
        # otherwise mint an identity and skip the check protecting it (PR #13 review).
        warns.append(f"[structural_check] cut_state {cut_state!r} is not in the register's declared list ({sorted(vocab)}) — declare a new received state in the register before using it")
    inst = instruments_rows(regtxt)
    if inst:
        matched = 0
        for row in inst:
            row_triple = (row.get("Instrument", ""), row.get("Revision", ""), row.get("Cut state", ""))
            if row_triple != triple:
                continue
            matched += 1
            row_digest = row.get("tree_sha256", "")
            my_digest = str(manifest.get("tree_sha256", "")) if historical else None
            if my_digest and row_digest and my_digest not in row_digest:
                errs.append(f"[structural_check] instruments row for {triple} carries a different tree_sha256 — two trees may not share one cut key; a new received state needs a new cut_state")
            else:
                notes.append(f"[structural_check] cut key {triple} matches its instruments row")
        if matched > 1:
            errs.append(f"[structural_check] {matched} instruments rows share the cut key {triple} — uniqueness is enforced on the triple")
        elif matched == 0:
            # No row means the digest binding went UNCHECKED — never silence it (PR #13
            # review). But a cut's row is written at landing, AFTER this check passes, so
            # an unregistered key is normal for a new cut and must not fail it. The typo
            # case is separated by the vocabulary: an undeclared cut_state with no row is
            # an invented identity that also disabled its own check — that is an error.
            msg = (f"no instruments row for the cut key {triple} — the digest binding that "
                   "enforces the cut-key ruling went unchecked")
            if undeclared_state:
                errs.append(f"[structural_check] {msg}, and {cut_state!r} is not a declared cut state: an undeclared state with no row is an invented identity, not a new one")
            else:
                warns.append(f"[structural_check] {msg}; expected for a cut whose row lands with its bytes — add the row in the landing PR")
    else:
        warns.append("[unavailable] no instruments table found in the register — cut-key uniqueness not checkable")

    # ---- reference resolution over index.json (025 R-01 P0 / 026 R-04) ----
    index_rel = manifest.get("index") if has_designer else "index.json"
    index_path = os.path.join(pkg_dir, index_rel or "index.json")
    counts = {"as-written": 0, "stripped": 0, "design_source": 0, "unresolved": 0, "escape": 0}
    unresolved_paths = []
    index = None
    if not os.path.isfile(index_path):
        errs.append(f"[structural_check] index not found at {index_rel!r}")
    else:
        try:
            index = read_json(index_path)
        except (OSError, json.JSONDecodeError) as e:
            errs.append(f"[structural_check] index.json unreadable: {str(e).splitlines()[0]}")
    if index:
        # In designer mode the strip is pure DIAGNOSTIC: a path resolving only after it
        # still fails, but the error names the mistake (025 R-12) instead of a bare miss.
        detect_strip = strip if historical else "handoff/"
        for path, ref_type, where in collect_index_refs(index):
            if ref_type == "design_source":
                counts["design_source"] += 1  # opaque provenance, never resolved
                continue
            status, _ = resolve_ref(pkg_dir, path, strip_prefix=detect_strip)
            counts[status if status != "unresolved" else "unresolved"] += 1
            if status == "escape":
                errs.append(f"[structural_check] {where} escapes the package root: {path!r} — {NON_WAIVABLE_NOTE}")
            elif status == "stripped" and not historical:
                errs.append(f"[structural_check] {where} resolves only after a prefix strip: {path!r} — designer manifests declare path_base '.' and ship correct paths")
            elif status == "unresolved":
                unresolved_paths.append((where, path))

        # ---- defect / waiver split (025 R-02 P0 / 026 R-05) ----
        defects = manifest.get("known_defects") or []
        defect_paths = {}
        for d in defects:
            if isinstance(d, dict):
                for p in d.get("paths") or []:
                    defect_paths[p] = d.get("id", "?")
        waived_ids = set()
        if opts["--import-record"]:
            rec = load_yaml_doc(opts["--import-record"], errs, "import record")
            if rec is not None:
                rerrs = []
                check_against_schema(rec, load_schema("design-package-import.v1"), rerrs)
                # x-conditional-required: bytes landed → path and digest are not optional
                if rec.get("disposition") == "imported":
                    for k in ("package_path", "tree_sha256"):
                        if rec.get(k) is None:
                            rerrs.append(f"{k} is null but disposition is 'imported' — null is for rejected / recorded_not_imported, where no bytes landed")
                errs += [f"[structural_check] import record: {e}" for e in rerrs]
                # Only a SCHEMA-VALID waiver waives: a record with a defect_id and no
                # authority is not a waiver, and must not act as one (PR #13 re-review).
                witems = (load_schema("design-package-import.v1")
                          .get("properties", {}).get("waivers", {}).get("items", {}))
                for i, w in enumerate(rec.get("waivers") or []):
                    werrs = []
                    check_value(w, witems, f"waivers[{i}]", werrs)
                    # The authority a waiver cites must itself be real: an operative
                    # register row, not merely a well-formed memo id.
                    if not werrs and isinstance(w, dict):
                        state, detail = memo_ref_operative(w.get("memo"), regtxt)
                        if state != "ok":
                            werrs.append(f"waivers[{i}].memo: {detail}")
                    if werrs:
                        # The field-level errors are already reported by the record-level
                        # schema check above; add only what it cannot say.
                        errs += [f"[structural_check] import record: {e}" for e in werrs
                                 if f"[structural_check] import record: {e}" not in errs]
                        errs.append(f"[structural_check] import record: waivers[{i}] is not a valid waiver and grants nothing — a waiver names authority")
                    elif w.get("defect_id"):
                        waived_ids.add(w["defect_id"])
                rec_digest = rec.get("tree_sha256")
                if rec_digest:
                    digest, total, count, digerrs = tree_sha256(pkg_dir)
                    errs += [f"[measured] {e}" for e in digerrs]
                    if digest != rec_digest:
                        errs.append(f"[measured] tree_sha256 mismatch: recomputed {digest}, import record says {rec_digest} — {NON_WAIVABLE_NOTE}")
                    else:
                        notes.append(f"[measured] tree_sha256 verified: {digest} ({count} files, {total} bytes)")

        for where, path in unresolved_paths:
            did = defect_paths.get(path)
            if did and did in waived_ids:
                warns.append(f"[declared] {where} unresolved: {path!r} — declared defect {did}, import waived by authority in the import record")
            elif did:
                msg = f"{where} unresolved: {path!r} — declared defect {did} has no waiver record; a defect names a failure, a waiver names authority"
                (warns if historical else errs).append(f"[structural_check] {msg}")
            else:
                # historical imports record breaches, never refuse (025 R-08/R-09)
                msg = f"{where} does not resolve: {path!r}"
                (warns if historical else errs).append(f"[structural_check] {msg}" + ("" if historical else " — undeclared"))

        # stale declaration is itself drift (025 R-02) — checkable only for the one rule
        # this tool verifies (path-resolution); runtime defects are declared, never judged
        for d in defects:
            if not isinstance(d, dict) or d.get("rule_id") != "path-resolution":
                continue
            if "closed" in str(d.get("status", "")).lower():
                continue
            fine = [p for p in d.get("paths") or []
                    if resolve_ref(pkg_dir, p, strip_prefix=strip)[0] in ("as-written", "stripped")]
            if fine and len(fine) == len(d.get("paths") or []):
                warns.append(f"[structural_check] declared defect {d.get('id', '?')} names only paths that resolve fine — stale declaration is itself drift")

        # ---- sheet-set agreement, duplicated-field checks (025 R-13 / R-24 / outcome 4) ----
        idx_sheets = [s.get("id") for s in index.get("sheets") or []]
        if has_designer:
            man_sheets = [s.get("id") for s in manifest.get("sheets") or []]
            if sorted(man_sheets) != sorted(x for x in idx_sheets if x):
                errs.append(f"[structural_check] sheet set disagrees: manifest {sorted(man_sheets)} vs index {sorted(x for x in idx_sheets if x)}")
            if name in man_sheets:
                errs.append(f"[structural_check] design_package {name!r} equals a sheets[].id — a package name is not a sheet id")
        if name in idx_sheets and not historical:
            errs.append(f"[structural_check] design_package {name!r} equals a sheet id in index.json — a package name is not a sheet id")

    # ---- decisions ledger (025 R-08 / 026 R-07) ----
    dec = manifest.get("decisions") or {}
    ledger_rel = dec.get("ledger")
    ledger = None
    if ledger_rel:
        status, resolved = resolve_ref(pkg_dir, ledger_rel, strip_prefix=strip)
        if status in ("as-written", "stripped"):
            ledger_text = read_text(os.path.join(pkg_dir, resolved))
            ledger = parse_ledger(ledger_text)
            if ledger["order"] == "unknown":
                warns.append("[structural_check] ledger declares no order in its header — comparison is by DEC id regardless, but the header should state it")
            else:
                notes.append(f"[structural_check] ledger order (declared in header): {ledger['order']}")
            if ledger["duplicate_ids"]:
                errs.append(f"[structural_check] duplicate ledger ids: {ledger['duplicate_ids']}")
            nums = sorted(e["num"] for e in ledger["entries"])
            if nums and nums != list(range(nums[0], nums[-1] + 1)):
                errs.append("[structural_check] ledger ids are not contiguous")
            last = f"DEC-{max(nums):03d}" if nums else None
            if dec.get("last_id") and dec["last_id"] != last:
                errs.append(f"[structural_check] decisions.last_id {dec['last_id']!r} but the ledger runs to {last}")
            if dec.get("count") is not None and dec["count"] != len(nums):
                errs.append(f"[structural_check] decisions.count {dec['count']} but the ledger holds {len(nums)} unique ids")
        else:
            errs.append(f"[structural_check] decisions.ledger {ledger_rel!r} does not resolve")

    if ledger and opts["--previous"]:
        prev_dir = opts["--previous"]
        prev_ledger_path = None
        for cand in ("decisions.md", "handoff/decisions.md"):
            if os.path.isfile(os.path.join(prev_dir, cand)):
                prev_ledger_path = os.path.join(prev_dir, cand)
                break
        if prev_ledger_path is None:
            warns.append(f"[unavailable] no decisions.md found under --previous {prev_dir}")
        else:
            prev = parse_ledger(read_text(prev_ledger_path))
            breaches, lnotes, new_ids = compare_ledgers(prev, ledger)
            for n in lnotes:
                notes.append(f"[structural_check] {n}")
            if new_ids:
                notes.append(f"[structural_check] new ledger entries: {new_ids}")
            for b in breaches:
                # historical imports RECORD breaches — they are the only evidence that can reveal them
                (warns if historical else errs).append(f"[structural_check] ledger: {b}" + (" (recorded, not refused — historical import)" if historical else ""))

    # ---- standalone/ + dt/ co-presence (024 §4, kept from R0) ----
    if os.path.isdir(os.path.join(pkg_dir, "standalone")) and not os.path.isdir(os.path.join(pkg_dir, "dt")):
        msg = "standalone/ present without dt/ — standalone pages resolve ../dt/* and ship together"
        (warns if historical else errs).append(f"[structural_check] {msg}" + (" (recorded — pre-dt/ layout)" if historical else ""))

    # ---- declared facts: report, never verify (026 R-06) ----
    for d in manifest.get("known_defects") or []:
        if isinstance(d, dict):
            warns.append(f"[declared] defect {d.get('id', '?')} ({d.get('rule_id', '?')}): {str(d.get('expected_failure', ''))[:120]} — declared per {d.get('evidence', 'cited document')}; not verified by this tool")

    print(
        f"{pkg_dir}: manifest_origin={origin} package={name} rev={manifest.get('revision')} "
        f"cut_state={manifest.get('cut_state')} refs={counts} mock_math={manifest.get('mock_math')}"
    )
    for n in notes:
        print("  NOTE", n)
    for w in warns:
        print("  WARN", w)
    for e in errs:
        print("  ERROR", e)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
