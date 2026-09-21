#!/usr/bin/env python3
"""register_migrate.py — one-time mechanical migration of the register's version line
(HANDOFF-LEGO-PIPE-032-R1; R0 §4 items 1–5). Rerunnable by any reviewer from
`git show <base>:docs/correspondence/REGISTER.md`; the committed tree must reproduce exactly.

What it does, against the base bytes and nothing else:
  1. locates the version line, splits it at the preamble and at every accepted `At \\`.n\\``
     seam (descending-by-one rule, R0 §2 N-02) and records EVERY candidate — accepted or
     rejected — in the seam manifest, with byte offsets and a human-readable reason;
  2. writes register/MIGRATION-<base>.yaml (the reviewed data: base, digests, partition,
     resolutions, seams, known in-place repairs, table baseline);
  3. writes one immutable `kind: migrated` record per version under register/versions/:
     24 via `slice`, and — Q-11(a) — six (`.2`–`.7`) via a `resolution` into the `.8`
     slice's bytes, each with `shared_slice: true` and its anomaly id;
  4. seeds register/ALLOCATIONS.yaml from the correspondence table's first column plus the
     operator's Q-01 reservations, and register/KNOWN-ANOMALIES.yaml with exactly the
     irregularities a lint rule would otherwise flag;
  5. rewrites REGISTER.md's version line to preamble + current version + pointer, touching
     nothing else in the file. Idempotent: a second run on the migrated file is a no-op.

Usage:
  register_migrate.py --base COMMIT [--repo DIR] [--check]
  register_migrate.py --source REGISTER.md [--repo DIR] [--check]
--check writes into a temporary directory and diffs against the committed tree (exit 1 on
any difference) — the reviewer's "rerun to an empty diff" for the migration itself.

What --check proves, and what it deliberately leaves to other tools (F-08, H4): the
migration's OWN artifacts are immutable and are compared byte-for-byte — every `kind:
migrated` record, the manifest, KNOWN-ANOMALIES.yaml. The three surfaces the migration
seeded but later landings legitimately move are compared STRUCTURALLY against the seed:
  * register/versions/: extra records are allowed only if `kind: finalized`/`bootstrap`
    (finalization's products); any missing or altered migrated record is a difference;
  * REGISTER.md's version line: must be the migrated pointer template with a version >=
    the migrated one (later finalizations advance it); anything else is a difference;
  * register/ALLOCATIONS.yaml: every seeded entry must still exist with every field
    byte-equal except `state`/`landed_version`, whose only legal movement is forward along
    reserved → in_flight → landed, a `landed` entry naming a `landed_version` whose finalized
    record exists in the committed tree and lists the key in `allocations_consumed`; new
    entries may be appended only at or above the seeded next_free, and the file must be the
    fixed emitter's own serialisation. Anything else — a changed seeded field, a backwards
    transition, a dangling landed_version, an entry removed, an out-of-order number — is a
    difference. This is NOT "ignore the ledger": a corrupted seeded entry still fails.
Whether the forward state itself is right (chain, pointer = newest record, landing facts)
is register_lint's and register_finalize --check's job, run separately.
Exit: 0 · 1 difference/refusal · 2 usage/IO
"""
import os
import re
import sys
import tempfile

from register_lint import (REGISTER_DIR_REL, REGISTER_REL, SEAM_RE, DOUBLED_LABEL_RE, dump_yaml,
                           git_bytes, parse_record, read_bytes, record_bytes, sha256,
                           table_data_rows, write_bytes)

NEW_VERSION_LINE = (
    "**Register version: {version}** — one register version per accepted landing transaction, "
    "assigned only at finalization against protected `main` by `tools/register_finalize.py` "
    "(Q-02/Q-03, HANDOFF-LEGO-PIPE-032-R1); never claimed on a branch, never bumped by hand. "
    "The version history is one immutable record per version under `register/versions/` "
    "(`tools/register_lint.py render` reads it newest first); this line is the pointer, not the log."
)

# Version-name prefixes (identity, not a landing fact): read at the base from each landing's
# own version line in Git history — 5446e6e (.6) … 30c3b93 (.10) carry 2026-09-17, 4896a0d
# (.11) … 582fb63 (.31) carry 2026-09-18. .2–.5 predate the committed register (project-side
# copies) and take 2026-09-17, the date the register's own `.2`–`.6` text gives them
# ("circulated earlier today", "first committed version … 2026-09-17").
VERSION_PREFIX = {n: "2026-09-17" for n in range(2, 11)}
VERSION_PREFIX.update({n: "2026-09-18" for n in range(11, 32)})
VERSION_NAME_BASIS = (
    "date prefix per version: .2–.10 → 2026-09-17, .11–.31 → 2026-09-18; .6–.31 read from each "
    "landing's version line in Git history at the base (5446e6e … 582fb63, first-parent); .2–.5 "
    "predate the committed register and take the date the register's own text gives them"
)

KNOWN_IN_PLACE_REPAIRS = [
    {"repaired_at": "2026-09-18.14", "target": "2026-09-18.11",
     "note": "the .14 note: \"`.14` also corrects a duplicated phrase in the `.11` note below\""},
    {"repaired_at": "2026-09-18.22", "target": "2026-09-18.15 … 2026-09-18.19",
     "note": "the .22 note: \"`.22` also repairs doubled version labels (\\\"At `.n` `.n`\\\") left in the `.15`–`.19` notes by a bump script\""},
]

# Where the version notes state a row's landing version. Rows that predate the committed
# register (present at .6) carry null and a basis string — the notes do not state a version.
LANDED_VERSION = {
    "020-R0": "2026-09-17.10", "021-R0": "2026-09-18.12", "022-R0": "2026-09-18.13",
    "016-R1": "2026-09-18.13", "023-R0": "2026-09-18.15", "023-R1": "2026-09-18.16",
    "023-R2": "2026-09-18.22", "024-R0": "2026-09-18.23", "025-R0": "2026-09-18.24",
    "025-R1": "2026-09-18.24", "026-R0": "2026-09-18.25", "024-R1": "2026-09-18.26",
    "027-R0": "2026-09-18.27", "028-R0": "2026-09-18.28", "029-R0": "2026-09-18.29",
    "030-R0": "2026-09-18.30", "031-R0": "2026-09-18.31",
}
PRE_COMMIT_BASIS = "row present at 2026-09-17.6, the first committed version; the version notes do not state a landing version for it"

# Q-01, ratified 2026-09-20 (PR #21 decision docket, comment 5752476543). 032 is in flight on
# the migration branch (row present, version assigned at finalization); 033–035 are reserved.
DOCKET = "James, 2026-09-20 — PR #21 decision docket (https://github.com/ojfbot/lego-village-pipeline/pull/21#issuecomment-5752476543), Q-01"
RESERVATIONS = [
    {"key": "032-R1", "number": 32, "identity": "HANDOFF-LEGO-PIPE-032", "type": "HANDOFF",
     "thread": "correspondence-governance", "actor": "Claude Code", "allocated_by": DOCKET,
     "date": "2026-09-20", "state": "in_flight", "landed_version": None,
     "basis": "R0 accepted at PR #21 head 48bcbf50 (sha256 d7980999…61ea), superseded by R1 (sha256 0ef0fe82…9438); consumed by the migration landing's own finalization"},
    {"key": "033", "number": 33, "identity": "REVIEW-LEGO-PIPE-033", "type": "REVIEW",
     "thread": "correspondence-governance", "actor": "Claude (Cowork)", "allocated_by": DOCKET,
     "date": "2026-09-20", "state": "reserved", "landed_version": None,
     "basis": "independent review of the implementation PR, content-pinned (Q-14); no row until it lands"},
    {"key": "034", "number": 34, "identity": "REVIEW-LEGO-PIPE-034", "type": "REVIEW",
     "thread": "correspondence-governance", "actor": "ChatGPT / Codex", "allocated_by": DOCKET,
     "date": "2026-09-20", "state": "reserved", "landed_version": None,
     "basis": "independent review of the implementation PR, content-pinned (Q-14); no row until it lands"},
    {"key": "035", "number": 35, "identity": "CORR-LEGO-PIPE-035", "type": "CORR",
     "thread": "correspondence-governance", "actor": "Claude Code", "allocated_by": DOCKET,
     "date": "2026-09-20", "state": "reserved", "landed_version": None,
     "basis": "post-migration as-built and canary report; no row until it lands"},
]

PERMITTED_TABLE_CHANGES = {
    "rows_added": ["032-R1"],
    "rows_modified": ["030-R0", "031-R0"],
    "next_free_row": True,
    "basis": "Q-13 and the lead's carried condition 2 (PR #21 comment 5752637376): the 032-R1 row added, the 030-R0 and 031-R0 status cells updated, the next-free row replaced by the ledger-derived pointer; every other data row byte-identical (RL-13), instruments rows byte-identical (RL-14)",
}


def vname(n):
    return f"{VERSION_PREFIX[n]}.{n}"


def split_line(line):
    """Apply the seam rule to the version line bytes. Returns (preamble_end, current, seams)."""
    pm = re.match("\\*\\*Register version: (\\d{4}-\\d{2}-\\d{2}\\.(\\d+))\\*\\* — bump this line on every edit\\. ".encode("utf-8"), line)
    if not pm:
        raise ValueError("version line does not open with the expected pre-migration preamble")
    current = int(pm.group(2))
    expected = current - 1
    seams = []
    for m in SEAM_RE.finditer(line):
        n = int(m.group(1))
        before = line[max(0, m.start() - 48):m.start()].decode("utf-8", errors="replace")
        after = line[m.end():m.end() + 48].decode("utf-8", errors="replace")
        entry = {"byte_offset": m.start(), "matched": m.group(0).decode("utf-8"), "version_named": n,
                 "context_before": before, "context_after": after}
        if n == expected:
            entry["accepted"] = True
            entry["reason"] = f"introduces the .{n} note: the next expected version in the descending scan"
            expected -= 1
        else:
            entry["accepted"] = False
            entry["reason"] = (f"names .{n} where .{expected} was expected — a label quoted inside the .{expected + 1} note "
                               f"describing a historical label, not introducing a new one")
        seams.append(entry)
    return pm.end(), current, seams


def resolutions_in_slice(slice_bytes, slice_start):
    """Byte sub-ranges inside the .8 slice's `Superseded versions:` enumeration for .2–.7."""
    i = slice_bytes.find(b"Superseded versions: ")
    if i < 0:
        raise ValueError("the .8 slice carries no `Superseded versions:` enumeration")
    enum = slice_bytes[i:]
    out = {}
    for n in (6, 5, 4, 3, 2):
        m = re.search(rb"`\." + str(n).encode() + rb"` \((?:[^()]|\([^()]*\))*\)", enum)
        if not m:
            raise ValueError(f"no clause for .{n} in the enumeration")
        out[n] = (slice_start + i + m.start(), slice_start + i + m.end(),
                  f"the `.{n}` clause of the .8 note's `Superseded versions:` enumeration")
    m7 = re.search(rb"`\.7` records [^)]*", enum)
    if not m7:
        raise ValueError("no clause for .7 in the enumeration")
    out[7] = (slice_start + i + m7.start(), slice_start + i + m7.end(),
              "the `.7` sub-clause inside the `.6` clause of the .8 note's `Superseded versions:` enumeration (nested: .6's parenthesis contains it)")
    return out


def anomaly_entries(slices_by_n, resolutions, line):
    entries = []
    aid = 1
    # doubled label occurrences in the notes' own bytes — .22 carries it, .24 quotes it
    for n, (start, end) in sorted(slices_by_n.items()):
        text = line[start:end].decode("utf-8", errors="replace")
        m = DOUBLED_LABEL_RE.search(text)
        if m:
            entries.append({
                "id": f"A-{aid:02d}", "kind": "doubled_label", "affects": vname(n),
                "observed": m.group(0),
                "cited_by": ("the .22 note itself (\"At `.22` `.22` adds the 023-R2 row\"), reported by the .24 note (R-21) and left as written"
                             if n == 22 else "the .24 note, which quotes the .22 label it reports (\"the `.23` note reintroduced the doubled version label\")"),
                "permits": "RL-07", "frozen": True,
            })
            aid += 1
    for n in (7, 6, 5, 4, 3, 2):
        start, end, where = resolutions[n]
        entries.append({
            "id": f"A-{aid:02d}", "kind": "no_slice_of_its_own", "affects": vname(n),
            "observed": f"version .{n} has no note of its own on the version line; it is named only inside {where}",
            "cited_by": "HANDOFF-LEGO-PIPE-032-R1 Q-11 (ratified option a: six resolution records into .8's bytes, PR #21 comment 5752476543)",
            "permits": "RL-07", "frozen": True,
        })
        aid += 1
    return entries


def seed_ledger(regtxt):
    rows = table_data_rows(regtxt)["correspondence"]
    entries = []
    reserved_keys = {r["key"] for r in RESERVATIONS}
    for key, row in rows:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if re.fullmatch(r"\d{3}\+", key) or key in reserved_keys:
            continue
        num_m = re.match(r"(\d{3})", key)
        number = int(num_m.group(1)) if num_m else None
        typ, thread, author = cells[2], cells[3], cells[4]
        disc_m = re.search(r"\*\((.*?)\)\*", key)
        rev_m = re.search(r"-(R\d+)", key)
        ident = (f"{typ}-LEGO-PIPE-{number:03d}" if number is not None else "legacy-unnumbered-review") + (f" ({disc_m.group(1)})" if disc_m else "")
        entries.append({
            "key": key, "number": number, "identity": ident, "revision": rev_m.group(1) if rev_m else None,
            "type": typ, "thread": thread, "actor": author,
            "allocated_by": "James (rule 1) — allocation notes, where recorded, are in the row's status cell",
            "date": None, "state": "landed",
            "landed_version": LANDED_VERSION.get(key),
            "basis": "landing version stated by the version note named in landed_version" if key in LANDED_VERSION else PRE_COMMIT_BASIS,
        })
    entries.extend(RESERVATIONS)
    numbers = [e["number"] for e in entries if isinstance(e["number"], int)]
    return {
        "schema": "register-allocations/v1",
        "purpose": "every memo number ever allocated, with its lifecycle (reserved | in_flight | landed | withdrawn); numbers are never recycled (rules 2, 3); next_free is derived, never hand-maintained; no landing_pr field exists (RR-32-R2-03)",
        "seeded_from": "the correspondence table's first column at the migration base (R0 §4 item 4) plus the operator's Q-01 reservations",
        "next_free": max(numbers) + 1,
        "allocations": entries,
    }


def migrate(source_bytes, base_commit, out_root):
    """Produce the migrated register tree under out_root from the base bytes. Returns the
    manifest dict. Pure function of its inputs: no clock, no environment."""
    lines = source_bytes.split(b"\n")
    idx = next(i for i, l in enumerate(lines) if l.startswith(b"**Register version: "))
    line = lines[idx]
    pre_end, current, seams = split_line(line)
    accepted = [s for s in seams if s["accepted"]]
    bounds = [pre_end] + [s["byte_offset"] for s in accepted] + [len(line)]
    labels = [current] + [s["version_named"] for s in accepted]
    slices, slices_by_n = [], {}
    for i, n in enumerate(labels):
        start, end = bounds[i], bounds[i + 1]
        slices.append({"id": f"s-{n:02d}", "version": vname(n), "start": start, "end": end,
                       "sha256": sha256(line[start:end])})
        slices_by_n[n] = (start, end)
    lowest_slice = min(slices_by_n)
    res = resolutions_in_slice(line[slices_by_n[lowest_slice][0]:slices_by_n[lowest_slice][1]], slices_by_n[lowest_slice][0])
    anomalies = anomaly_entries(slices_by_n, res, line)
    anomaly_for = {a["affects"]: a["id"] for a in anomalies if a["kind"] == "no_slice_of_its_own"}
    resolutions = []
    for n in sorted(res, reverse=True):
        start, end, where = res[n]
        resolutions.append({"version": vname(n), "in_slice": f"s-{lowest_slice:02d}",
                            "range": {"start": start, "end": end}, "sha256": sha256(line[start:end]),
                            "reason": anomaly_for[vname(n)], "where": where})
    regtxt = source_bytes.decode("utf-8")
    rows = table_data_rows(regtxt)
    lowest = min(res)
    manifest = {
        "schema": "register-migration/v1",
        "base_commit": base_commit,
        "source_path": "docs/correspondence/REGISTER.md",
        "source_sha256": sha256(source_bytes),
        "source_bytes": len(source_bytes),
        "source_lines": source_bytes.count(b"\n"),
        "line_number": idx + 1,
        "line_sha256": sha256(line),
        "line_bytes": len(line),
        "line_characters": len(line.decode("utf-8")),
        "line_non_ascii_bytes": sum(1 for c in line if c > 127),
        "encoding": "utf-8",
        "offsets_are": "byte offsets into the raw UTF-8 line, never character offsets (CW-33-P05, RR-32-07)",
        "verbatim_as_of": base_commit,
        "known_in_place_repairs": KNOWN_IN_PLACE_REPAIRS,
        "version_count": len(slices) + len(resolutions),
        "slice_count": len(slices),
        "resolution_count": len(resolutions),
        "lowest_version": vname(lowest),
        "current_version": vname(current),
        "version_name_basis": VERSION_NAME_BASIS,
        "preamble": {"start": 0, "end": pre_end, "sha256": sha256(line[:pre_end]), "text": line[:pre_end].decode("utf-8")},
        "slices": slices,
        "resolutions": resolutions,
        "seams": seams,
        "table_baseline": {"correspondence_rows": len(rows["correspondence"]), "instruments_rows": len(rows["instruments"]),
                           "definition": "data rows only — header and separator lines excluded (RR-32-07)",
                           "permitted_changes": PERMITTED_TABLE_CHANGES},
    }
    reg_dir = os.path.join(out_root, REGISTER_DIR_REL)
    write_bytes(os.path.join(reg_dir, f"MIGRATION-{base_commit}.yaml"), dump_yaml(manifest).encode("utf-8"))
    # records
    all_versions = sorted(list(slices_by_n) + list(res))
    for n in all_versions:
        prev = None if n == lowest else vname(n - 1)
        fm = {"register_version": vname(n), "previous_version": prev, "kind": "migrated"}
        if n in slices_by_n:
            start, end = slices_by_n[n]
            fm["slice"] = f"s-{n:02d}"
        else:
            start, end, _ = res[n]
            fm["resolution"] = {"in_slice": f"s-{lowest_slice:02d}", "range": {"start": start, "end": end}}
            fm["shared_slice"] = True
            fm["anomaly"] = anomaly_for[vname(n)]
        body = line[start:end]
        fm["note_sha256"] = sha256(body)
        write_bytes(os.path.join(reg_dir, "versions", f"{vname(n)}.md"), record_bytes(fm, body))
    write_bytes(os.path.join(reg_dir, "KNOWN-ANOMALIES.yaml"), dump_yaml({
        "schema": "register-anomalies/v1",
        "purpose": "frozen historical irregularities the checker would otherwise flag, as data (031 §7.2, CW-18-03); RL-07 accepts a flagged shape only where an entry permits it for that version; RL-08 refuses any entry newer than the migration base — a new irregularity fails, it is not baselined; never a live policy lever (RR-32-R3-02)",
        "anomalies": anomalies,
    }).encode("utf-8"))
    write_bytes(os.path.join(reg_dir, "ALLOCATIONS.yaml"), dump_yaml(seed_ledger(regtxt)).encode("utf-8"))
    # version line → preamble + pointer, nothing else in the file
    new_line = NEW_VERSION_LINE.format(version=vname(current)).encode("utf-8")
    lines[idx] = new_line
    write_bytes(os.path.join(out_root, REGISTER_REL), b"\n".join(lines))
    return manifest


def rewrite_register_in_place(repo, source_bytes, migrated_register_bytes):
    """Idempotent version-line rewrite of the checked-out REGISTER.md. Refuses if the
    checked-out line is neither the base line nor already migrated (baseline moved)."""
    path = os.path.join(repo, REGISTER_REL)
    cur = read_bytes(path)
    cur_lines, src_lines, mig_lines = cur.split(b"\n"), source_bytes.split(b"\n"), migrated_register_bytes.split(b"\n")
    idx = next(i for i, l in enumerate(cur_lines) if l.startswith(b"**Register version: "))
    if cur_lines[idx] == mig_lines[idx]:
        return "no-op: version line already migrated"
    if cur_lines[idx] != src_lines[idx]:
        raise RuntimeError("REGISTER.md's version line is neither the base line nor the migrated line — baseline moved; refusing")
    cur_lines[idx] = mig_lines[idx]
    write_bytes(path, b"\n".join(cur_lines))
    return "rewrote the version line (preamble + pointer); nothing else touched"


LIFECYCLE = ("reserved", "in_flight", "landed")
VERSION_LINE_RE = re.compile(rb"^\*\*Register version: (\d{4}-\d{2}-\d{2})\.(\d+)\*\* \xe2\x80\x94 one register version per accepted landing")


def ledger_forward_diffs(seed, committed, committed_versions_dir):
    """Differences between the migration's seeded ledger and the committed one, allowing only
    legitimate forward lifecycle movement (see the module docstring). Returns a list of strings."""
    diffs = []
    if not isinstance(seed, dict) or not isinstance(committed, dict):
        return ["ALLOCATIONS.yaml: not a mapping"]
    seed_entries = {e["key"]: e for e in seed.get("allocations", [])}
    committed_entries = {}
    for e in committed.get("allocations", []):
        if e.get("key") in committed_entries:
            diffs.append(f"ALLOCATIONS.yaml: duplicate key {e.get('key')}")
        committed_entries[e.get("key")] = e
    # finalized records available to justify a landed_version
    finalized = {}
    if os.path.isdir(committed_versions_dir):
        for name in os.listdir(committed_versions_dir):
            if name.endswith(".md"):
                try:
                    fm, _ = parse_record(read_bytes(os.path.join(committed_versions_dir, name)))
                except Exception:  # noqa: BLE001 — an unreadable record is reported by lint, not here
                    continue
                if fm.get("kind") in ("finalized", "bootstrap"):
                    finalized[fm.get("register_version")] = fm
    for key, se in seed_entries.items():
        ce = committed_entries.get(key)
        if ce is None:
            diffs.append(f"ALLOCATIONS.yaml: seeded entry {key} is missing")
            continue
        for f in sorted(set(se) | set(ce)):
            if f in ("state", "landed_version"):
                continue
            if se.get(f) != ce.get(f):
                diffs.append(f"ALLOCATIONS.yaml: {key}.{f} changed from seed ({se.get(f)!r} → {ce.get(f)!r}); only state/landed_version may move")
        s_state, c_state = se.get("state"), ce.get("state")
        if c_state not in LIFECYCLE or s_state not in LIFECYCLE:
            diffs.append(f"ALLOCATIONS.yaml: {key} state {c_state!r} (seed {s_state!r}) not in {LIFECYCLE}")
        elif LIFECYCLE.index(c_state) < LIFECYCLE.index(s_state):
            diffs.append(f"ALLOCATIONS.yaml: {key} moved backwards {s_state} → {c_state}")
        if c_state == "landed":
            lv = ce.get("landed_version")
            if se.get("state") == "landed":
                if lv != se.get("landed_version"):
                    diffs.append(f"ALLOCATIONS.yaml: {key} was seeded landed at {se.get('landed_version')!r} but now names {lv!r}")
            elif lv not in finalized:
                diffs.append(f"ALLOCATIONS.yaml: {key} is landed at {lv!r} but no finalized record with that version exists in the committed tree")
            elif key not in (finalized[lv].get("allocations_consumed") or []):
                diffs.append(f"ALLOCATIONS.yaml: {key} is landed at {lv} but that record's allocations_consumed does not name it")
        elif ce.get("landed_version") not in (None,):
            diffs.append(f"ALLOCATIONS.yaml: {key} is {c_state} but carries landed_version {ce.get('landed_version')!r}")
    seed_next = seed.get("next_free")
    for key, ce in committed_entries.items():
        if key in seed_entries:
            continue
        if not isinstance(ce.get("number"), int) or not isinstance(seed_next, int) or ce["number"] < seed_next:
            diffs.append(f"ALLOCATIONS.yaml: new entry {key} carries number {ce.get('number')!r} below the seeded next_free {seed_next!r}")
    if isinstance(seed_next, int) and isinstance(committed.get("next_free"), int) and committed["next_free"] < seed_next:
        diffs.append(f"ALLOCATIONS.yaml: next_free went backwards {seed_next} → {committed['next_free']}")
    for f in sorted(set(seed) | set(committed)):
        if f in ("allocations", "next_free"):
            continue
        if seed.get(f) != committed.get(f):
            diffs.append(f"ALLOCATIONS.yaml: top-level {f} changed from seed")
    return diffs


def reproduction_diffs(produced_root, repo, manifest):
    """Compare a fresh migration (under produced_root) with the committed tree under repo.
    Migration-owned artifacts byte-for-byte; the three forward-moving surfaces structurally."""
    diffs = []
    produced = os.path.join(produced_root, REGISTER_DIR_REL)
    committed = os.path.join(repo, REGISTER_DIR_REL)
    ledger_rel = "ALLOCATIONS.yaml"
    for root, _, files in os.walk(produced):
        for f in files:
            p = os.path.join(root, f)
            rel = os.path.relpath(p, produced)
            q = os.path.join(committed, rel)
            if not os.path.exists(q):
                diffs.append(f"missing in committed tree: register/{rel}")
            elif rel == ledger_rel:
                try:
                    seed = yaml_load(read_bytes(p))
                    com_bytes = read_bytes(q)
                    com = yaml_load(com_bytes)
                except Exception as e:  # noqa: BLE001
                    diffs.append(f"differs: register/{rel} (unparsable: {e})")
                    continue
                if dump_yaml(com).encode("utf-8") != com_bytes:
                    diffs.append(f"differs: register/{rel} is not the fixed emitter's serialisation")
                diffs.extend(ledger_forward_diffs(seed, com, os.path.join(committed, "versions")))
            elif read_bytes(p) != read_bytes(q):
                diffs.append(f"differs: register/{rel}")
    for root, _, files in os.walk(committed):
        if os.path.basename(root) == "pending":
            continue
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), committed)
            if os.path.exists(os.path.join(produced, rel)) or rel.startswith("pending"):
                continue
            fm_kind = None
            if rel.startswith("versions"):
                try:
                    fm_kind = parse_record(read_bytes(os.path.join(root, f)))[0].get("kind")
                except Exception:  # noqa: BLE001
                    fm_kind = None
            if fm_kind in ("finalized", "bootstrap"):
                continue  # produced by finalization, not by this tool; lint checks its chain
            diffs.append(f"extra in committed tree: register/{rel}")
    # version line: the migrated pointer template, at the migrated version or later
    cur_lines = read_bytes(os.path.join(repo, REGISTER_REL)).split(b"\n")
    mig_lines = read_bytes(os.path.join(produced_root, REGISTER_REL)).split(b"\n")
    idx = manifest["line_number"] - 1
    if idx >= len(cur_lines) or not cur_lines[idx].startswith(b"**Register version: ") or not mig_lines[idx].startswith(b"**Register version: "):
        diffs.append("version line not found at the manifest's line_number")
    elif cur_lines[idx] != mig_lines[idx]:
        mc, mm = VERSION_LINE_RE.match(cur_lines[idx]), VERSION_LINE_RE.match(mig_lines[idx])
        if not mc or not mm:
            diffs.append("REGISTER.md version line is not the migrated pointer line")
        elif (mc.group(1), int(mc.group(2))) < (mm.group(1), int(mm.group(2))):
            diffs.append(f"REGISTER.md pointer {mc.group(1).decode()}.{mc.group(2).decode()} is behind the migrated version {mm.group(1).decode()}.{mm.group(2).decode()}")
        elif cur_lines[idx][mc.end():] != mig_lines[idx][mm.end():]:
            diffs.append("REGISTER.md version line's pointer text differs from the migrated template")
    # REGISTER.md's other lines are the tables and rules: the migration landing changed exactly
    # the ratified Q-13 rows, which RL-13 proves against B with the bound whitelist. This tool
    # does not re-prove rows (it never did at H0–H2); it proves its own artifacts.
    return diffs


def yaml_load(data):
    import yaml  # PyYAML, present via the tools venv (register_lint imports it)
    return yaml.safe_load(data.decode("utf-8"))


def main(argv):
    args = list(argv)
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if "--repo" in args:
        i = args.index("--repo"); repo = os.path.abspath(args[i + 1]); del args[i:i + 2]
    check = "--check" in args
    if check:
        args.remove("--check")
    if len(args) != 2 or args[0] not in ("--base", "--source"):
        sys.stderr.write(__doc__ or "")
        return 2
    if args[0] == "--base":
        base = args[1]
        try:
            base = git_bytes(repo, "rev-parse", "--verify", base + "^{commit}").decode().strip()
            source = git_bytes(repo, "show", f"{base}:{REGISTER_REL.replace(os.sep, '/')}")
        except RuntimeError as e:
            sys.stderr.write(f"ERROR: {e}\n")
            return 2
    else:
        source = read_bytes(args[1])
        base = "source-file"
    with tempfile.TemporaryDirectory() as tmp:
        try:
            manifest = migrate(source, base, tmp)
        except ValueError as e:
            sys.stderr.write(f"ERROR: {e}\n")
            return 1
        produced = os.path.join(tmp, REGISTER_DIR_REL)
        committed = os.path.join(repo, REGISTER_DIR_REL)
        if check:
            diffs = reproduction_diffs(tmp, repo, manifest)
            for d in diffs:
                print("  " + d)
            print(f"register_migrate --check: {len(diffs)} differences against base {base[:12]}")
            return 1 if diffs else 0
        # real run: copy produced files into the repo, rewrite the version line in place
        for root, _, files in os.walk(produced):
            for f in files:
                p = os.path.join(root, f)
                rel = os.path.relpath(p, produced)
                write_bytes(os.path.join(committed, rel), read_bytes(p))
        try:
            msg = rewrite_register_in_place(repo, source, read_bytes(os.path.join(tmp, REGISTER_REL)))
        except RuntimeError as e:
            sys.stderr.write(f"ERROR: {e}\n")
            return 1
    print(f"migrated {manifest['version_count']} versions ({manifest['slice_count']} slices + {manifest['resolution_count']} resolutions) from {base[:12]}; {msg}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
