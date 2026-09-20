#!/usr/bin/env python3
"""register_lint.py — structural checker for the correspondence register (HANDOFF-LEGO-PIPE-032-R1).

The register is the enumerated set rooted at docs/correspondence/REGISTER.md (R0 §3):
REGISTER.md itself, register/ALLOCATIONS.yaml, register/KNOWN-ANOMALIES.yaml,
register/MIGRATION-*.yaml and every file under register/versions/. This tool checks
STRUCTURE only (R0 §7). It does not claim that a row's path exists, that status prose is
consistent, that supersession chains in prose resolve, or that thread names in rows are
current — those wait for typed per-memo records. A green run is not a semantic pass.

Rule ids are RL-nn (R0 §6). Every rule has a positive and a mutation case in
tests/test_register.py; the battery's meta-test fails if one is missing.

  Offline (no .git needed): RL-01 raw-slice partition · RL-02 allocation ledger ·
    RL-03 authority-set completeness · RL-04 one version pointer · RL-05 version chain
    and resolution · RL-06 previous_version chain · RL-07 anomalies permit, never launder ·
    RL-08 no anomaly newer than the migration base · RL-09 old records immutable (against a
    supplied prior tree) · RL-11 no hand-written records (shape) · RL-12 record schema ·
    RL-13 migration-mode row identity · RL-14 instruments rows identical · RL-18 Rule 18
    merge-method sentinel (presence; ratchet against a prior tree).
  Needs .git and origin/main (--git): RL-10 Git-derived landing facts + one finalized
    record per landing · RL-16 baseline drift · RL-17 one-time introduction of migrated
    records · RL-11 stale-base half · RL-09/RL-18 prior tree taken from origin/main.
  Skipped Git-tier checks WARN by name — never silently passed. No check at any tier
  calls a hosting API (RR-32-R2-03).

Usage:
  register_lint.py [--repo DIR] [--git] [--migration BASE_REGISTER_MD] [--prior-tree DIR]
  register_lint.py resolve (VERSION | --all) [--repo DIR]
  register_lint.py render [--repo DIR]            # concatenation, newest first (Q-05)
  register_lint.py rule18 [--repo DIR]            # prints `present` or `absent` (RL-18 state for CI)
Exit: 0 pass (warnings allowed) · 1 errors · 2 usage/IO

Needs PyYAML: re-execs itself under tools/.venv (tools/setup-preflight.sh creates it).
"""
import glob
import hashlib
import os
import re
import subprocess
import sys

from schema_lint import check_against_schema, load_schema, require_yaml

yaml = require_yaml("REGISTER_LINT_REEXEC")

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REPO = os.path.dirname(TOOLS_DIR)

REGISTER_REL = os.path.join("docs", "correspondence", "REGISTER.md")
REGISTER_DIR_REL = os.path.join("docs", "correspondence", "register")
CORRESPONDENCE_REL = "docs/correspondence/"

VERSION_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.(\d+)$")
PREAMBLE_RE = re.compile(r"^\*\*Register version: (\d{4}-\d{2}-\d{2}\.\d+)\*\* — ")
SEAM_RE = re.compile(rb"At `\.(\d+)`")
DOUBLED_LABEL_RE = re.compile(r"At `\.(\d+)` `\.\1`")
ANOMALY_ID_RE = re.compile(r"^A-\d{2}$")
AUTHORITY_RE = re.compile(r"The canonical register is the enumerated set rooted at `docs/correspondence/REGISTER\.md`:(.*?)\. Each component is authoritative")
RULE18_RE = re.compile(r"^18\. \*\*Merge-method enforcement:\*\* canonical `main` accepts only merge commits; `register-lint\.yml`'s settings check fails a PR that finds squash or rebase merging enabled\. Ratified .*$", re.M)
SUPERSEDES_RULE18_RE = re.compile(r"^\d+\. \*\*Supersedes Rule 18", re.M)
LEDGER_STATES = ("reserved", "in_flight", "landed", "withdrawn")


# ---------------------------------------------------------------- shared helpers

def sha256(b):
    return hashlib.sha256(b).hexdigest()


def vnum(v):
    m = VERSION_RE.match(str(v))
    if not m:
        raise ValueError(f"not a register version: {v!r}")
    return int(m.group(2))


def vprefix(v):
    return VERSION_RE.match(str(v)).group(1)


def dump_yaml(obj):
    """The one fixed emitter (R0 §5 step 7): sorted keys, LF, unicode kept, no wrapping,
    no timestamps or environment values ever put into `obj` by callers."""
    return yaml.safe_dump(obj, sort_keys=True, allow_unicode=True, default_flow_style=False,
                          width=10 ** 9)


def read_bytes(path):
    with open(path, "rb") as f:
        return f.read()


def write_bytes(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)


def load_yaml_file(path):
    with open(path, "rb") as f:
        return yaml.safe_load(f.read().decode("utf-8"))


def record_bytes(frontmatter, body):
    """A version record: `---\\n<yaml>---\\n<body bytes>` — body byte-exact, no trailing
    newline normalisation (R0 §4 item 3)."""
    return b"---\n" + dump_yaml(frontmatter).encode("utf-8") + b"---\n" + body


def parse_record(data):
    """(frontmatter dict, body bytes) or raises ValueError."""
    if not data.startswith(b"---\n"):
        raise ValueError("record does not open with a --- fence")
    end = data.find(b"\n---\n", 4)
    if end < 0:
        raise ValueError("record has no closing --- fence")
    fm_text = data[4:end + 1].decode("utf-8")
    body = data[end + 5:]
    fm = yaml.safe_load(fm_text)
    if not isinstance(fm, dict):
        raise ValueError("frontmatter is not a mapping")
    return fm, body


def register_version_line(regtxt):
    """(line_index_0based, line_text, current_version) of the version line."""
    for i, line in enumerate(regtxt.split("\n")):
        m = PREAMBLE_RE.match(line)
        if m:
            return i, line, m.group(1)
    return None, None, None


def table_data_rows(regtxt):
    """{'correspondence': [(key, row_text)], 'instruments': [...]} — data rows only;
    header and separator lines excluded (RR-32-07: 37 at the plan base)."""
    out = {"correspondence": [], "instruments": []}
    mode = None
    for line in regtxt.split("\n"):
        if line.startswith("| Number |"):
            mode = "correspondence"
            continue
        if line.startswith("| Instrument |"):
            mode = "instruments"
            continue
        if not line.startswith("|") or re.match(r"^\|[-\s|:]+\|$", line):
            if mode and not line.startswith("|"):
                mode = None
            continue
        if mode:
            key = line.strip().strip("|").split("|")[0].strip()
            out[mode].append((key, line))
    return out


def next_free_row_number(regtxt):
    for key, _ in table_data_rows(regtxt)["correspondence"]:
        m = re.fullmatch(r"(\d{3})\+", key)
        if m:
            return int(m.group(1))
    return None


def git(repo, *args, check=True):
    p = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {p.stderr.strip()}")
    return p.stdout


def git_bytes(repo, *args):
    p = subprocess.run(["git", *args], cwd=repo, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {p.stderr.decode(errors='replace').strip()}")
    return p.stdout


class Register:
    """Everything the checker reads from the enumerated set, loaded once."""

    def __init__(self, repo):
        self.repo = os.path.abspath(repo)
        self.register_path = os.path.join(self.repo, REGISTER_REL)
        self.dir = os.path.join(self.repo, REGISTER_DIR_REL)
        self.regtxt = read_bytes(self.register_path).decode("utf-8")
        self.manifest_paths = sorted(glob.glob(os.path.join(self.dir, "MIGRATION-*.yaml")))
        self.manifest = load_yaml_file(self.manifest_paths[0]) if self.manifest_paths else None
        self.ledger_path = os.path.join(self.dir, "ALLOCATIONS.yaml")
        self.anomalies_path = os.path.join(self.dir, "KNOWN-ANOMALIES.yaml")
        self.versions_dir = os.path.join(self.dir, "versions")
        self.pending_dir = os.path.join(self.dir, "pending")
        self.ledger = load_yaml_file(self.ledger_path) if os.path.exists(self.ledger_path) else None
        self.anomalies = load_yaml_file(self.anomalies_path) if os.path.exists(self.anomalies_path) else None
        self.records = {}      # version -> (frontmatter, body, filename)
        self.record_errors = []
        if os.path.isdir(self.versions_dir):
            for name in sorted(os.listdir(self.versions_dir)):
                if not name.endswith(".md"):
                    continue
                path = os.path.join(self.versions_dir, name)
                try:
                    fm, body = parse_record(read_bytes(path))
                except (ValueError, yaml.YAMLError, UnicodeDecodeError) as e:
                    self.record_errors.append(f"{name}: unreadable record: {e}")
                    continue
                v = fm.get("register_version")
                if not isinstance(v, str) or not VERSION_RE.match(v):
                    self.record_errors.append(f"{name}: register_version missing or malformed")
                    continue
                if v != name[:-3]:
                    self.record_errors.append(f"{name}: filename does not match register_version {v}")
                if v in self.records:
                    self.record_errors.append(f"{name}: duplicate record for {v}")
                self.records[v] = (fm, body, name)

    def current_version(self):
        return register_version_line(self.regtxt)[2]

    def sorted_versions(self):
        return sorted(self.records, key=vnum)

    def slices(self):
        return {s["id"]: s for s in (self.manifest or {}).get("slices", [])}

    def resolutions(self):
        return {r["version"]: r for r in (self.manifest or {}).get("resolutions", [])}

    def reconstruct_line(self):
        """Preamble text + slice record bodies in manifest order → the base line bytes."""
        m = self.manifest
        out = m["preamble"]["text"].encode("utf-8")
        for s in m["slices"]:
            rec = self.records.get(s["version"])
            if rec is None:
                raise KeyError(s["version"])
            out += rec[1]
        return out


# ---------------------------------------------------------------- the rules

class Lint:
    def __init__(self, reg, git_mode=False, migration_base=None, prior_tree=None):
        self.reg = reg
        self.git_mode = git_mode
        self.migration_base = migration_base
        self.prior_tree = prior_tree
        self.errs, self.warns, self.notes = [], [], []

    def err(self, rule, msg):
        self.errs.append(f"{rule} ERROR {msg}")

    def warn(self, rule, msg):
        self.warns.append(f"{rule} WARN {msg}")

    def note(self, rule, msg):
        self.notes.append(f"{rule} {msg}")

    # -- RL-03 -------------------------------------------------------------------------
    def rl03_authority_set(self):
        m = AUTHORITY_RE.search(self.reg.regtxt)
        if not m:
            self.err("RL-03", "REGISTER.md carries no authority declaration enumerating the register's components")
            return False
        components = re.findall(r"`([^`]+)`", m.group(1))
        missing = []
        for c in components:
            p = os.path.join(self.reg.repo, "docs", "correspondence", c) if not c.startswith("docs/") else os.path.join(self.reg.repo, c)
            if c == "this file":
                continue
            if "*" in c:
                if not glob.glob(p):
                    missing.append(c)
            elif c.endswith("/"):
                if not os.path.isdir(p) or not os.listdir(p):
                    missing.append(c)
            elif not os.path.exists(p):
                missing.append(c)
        for c in missing:
            self.err("RL-03", f"authority-set component missing: {c} — a copy lacking any component is not the register")
        if missing:
            return False
        self.note("RL-03", f"authority set complete: {len(components)} enumerated components present")
        return True

    # -- RL-04 -------------------------------------------------------------------------
    def rl04_pointer(self):
        count = sum(1 for l in self.reg.regtxt.split("\n") if PREAMBLE_RE.match(l))
        if count != 1:
            self.err("RL-04", f"expected exactly one version pointer line, found {count}")
            return
        cur = self.reg.current_version()
        if not self.reg.records:
            self.err("RL-04", "no version records under register/versions/")
            return
        newest = self.reg.sorted_versions()[-1]
        if cur != newest:
            self.err("RL-04", f"pointer says {cur} but the newest record is {newest}")
        else:
            self.note("RL-04", f"pointer {cur} equals the newest record")

    # -- RL-12 -------------------------------------------------------------------------
    def rl12_schema(self):
        try:
            schema = load_schema("register-version.v1")
        except OSError:
            self.err("RL-12", "tools/schemas/register-version.v1.schema.json is missing — records cannot be validated (fail closed)")
            return
        for e in self.reg.record_errors:
            self.err("RL-12", e)
        bootstrap = 0
        for v in self.reg.sorted_versions():
            fm, body, name = self.reg.records[v]
            errs = []
            check_against_schema(fm, schema, errs)
            for e in errs:
                self.err("RL-12", f"{name}: {e}")
            if fm.get("kind") == "bootstrap":
                bootstrap += 1
            if fm.get("note_sha256") != sha256(body):
                self.err("RL-12", f"{name}: note_sha256 does not match the body bytes")
        if bootstrap > 1:
            self.err("RL-12", f"{bootstrap} bootstrap records; at most one may ever exist")
        self.note("RL-12", f"{len(self.reg.records)} records validate against register-version/v1")

    # -- RL-01 / RL-05 / RL-06 / RL-07 / RL-08 -----------------------------------------
    def rl01_partition(self):
        m = self.reg.manifest
        pre = m["preamble"]
        pre_bytes = pre["text"].encode("utf-8")
        if pre["start"] != 0 or pre["end"] != len(pre_bytes) or sha256(pre_bytes) != pre["sha256"]:
            self.err("RL-01", "preamble start/end/sha256 disagree with its text")
        pos = pre["end"]
        total = pre["end"]
        seen_versions = set()
        for s in m["slices"]:
            if s["start"] != pos:
                self.err("RL-01", f"slice {s['id']} starts at {s['start']}, expected {pos} (partition must be contiguous and non-overlapping)")
            if s["end"] <= s["start"]:
                self.err("RL-01", f"slice {s['id']} has an empty or negative range")
            if s["version"] in seen_versions:
                self.err("RL-01", f"slice {s['id']} duplicates version {s['version']}")
            seen_versions.add(s["version"])
            pos = max(pos, s["end"])
            total += s["end"] - s["start"]
            rec = self.reg.records.get(s["version"])
            if rec is None:
                self.err("RL-01", f"slice {s['id']} names version {s['version']} which has no record")
                continue
            body = rec[1]
            if len(body) != s["end"] - s["start"]:
                self.err("RL-01", f"slice {s['id']} record body is {len(body)} bytes, range says {s['end'] - s['start']}")
            if sha256(body) != s["sha256"]:
                self.err("RL-01", f"slice {s['id']} ({s['version']}) body sha256 does not match the manifest")
        if total != m["line_bytes"]:
            self.err("RL-01", f"preamble + Σ slices = {total} bytes, line_bytes is {m['line_bytes']}")
        if pos != m["line_bytes"]:
            self.err("RL-01", f"partition ends at {pos}, not at line_bytes {m['line_bytes']}")
        try:
            line = self.reg.reconstruct_line()
        except KeyError as e:
            self.err("RL-01", f"cannot reconstruct: record {e} missing")
            return
        if len(line) != m["line_bytes"] or sha256(line) != m["line_sha256"]:
            self.err("RL-01", f"reconstructed line is {len(line)} bytes sha256 {sha256(line)[:12]}…, manifest says {m['line_bytes']} / {m['line_sha256'][:12]}…")
        # G-02: every accepted seam's matched text sits at its committed byte_offset, and the
        # slice boundaries equal the accepted seams' offsets exactly — not merely the count.
        accepted = [s for s in m["seams"] if s["accepted"]]
        boundaries = [s["start"] for s in m["slices"][1:]]
        offsets = [s["byte_offset"] for s in accepted]
        if boundaries != offsets:
            self.err("RL-01", f"slice boundaries {boundaries[:3]}… do not equal the accepted seam offsets {offsets[:3]}… (G-02: a consistent decomposition is not the right one)")
        for s in m["seams"]:
            at = line[s["byte_offset"]:s["byte_offset"] + len(s["matched"].encode("utf-8"))]
            if at != s["matched"].encode("utf-8"):
                self.err("RL-01", f"seam at byte {s['byte_offset']} does not read {s['matched']!r} in the reconstructed line")
        candidates = [mm.start() for mm in SEAM_RE.finditer(line)]
        recorded = sorted(s["byte_offset"] for s in m["seams"])
        if candidates != recorded:
            self.err("RL-01", f"manifest records {len(recorded)} seam candidates, the line has {len(candidates)} — every candidate, accepted or rejected, must be recorded")
        if not self.errs:
            self.note("RL-01", f"partition exact: preamble {pre['end']} + {len(m['slices'])} slices = {m['line_bytes']} bytes; {len(accepted)} accepted / {len(m['seams']) - len(accepted)} rejected seams")

    def rl05_chain(self):
        m = self.reg.manifest
        lowest, current = m["lowest_version"], self.reg.current_version()
        try:
            lo, cur = vnum(lowest), vnum(current)
        except ValueError as e:
            self.err("RL-05", str(e))
            return
        by_num = {vnum(v): v for v in self.reg.records}
        for n in range(lo, cur + 1):
            if n not in by_num:
                self.err("RL-05", f"no record for version number {n} (chain {lowest}…{current} must be continuous)")
        slices, resolutions = self.reg.slices(), self.reg.resolutions()
        slice_versions = {s["version"] for s in m["slices"]}
        if m["version_count"] != m["slice_count"] + m["resolution_count"]:
            self.err("RL-05", f"version_count {m['version_count']} != slice_count {m['slice_count']} + resolution_count {m['resolution_count']}")
        if m["slice_count"] != len(m["slices"]) or m["resolution_count"] != len(m["resolutions"]):
            self.err("RL-05", "slice_count/resolution_count do not match the manifest's own lists")
        mig_current = vnum(m["current_version"])
        if m["version_count"] != mig_current - lo + 1:
            self.err("RL-05", f"version_count {m['version_count']} != current({mig_current}) − lowest({lo}) + 1")
        for n in range(lo, mig_current + 1):
            v = by_num.get(n)
            in_slice, in_res = v in slice_versions, v in resolutions
            if in_slice == in_res:
                self.err("RL-05", f"{v or n}: must have exactly one manifest entry (slice or resolution), has {int(in_slice) + int(in_res)}")
        for v in self.reg.sorted_versions():
            fm, body, name = self.reg.records[v]
            if fm.get("kind") != "migrated":
                continue
            if "slice" in fm:
                s = slices.get(fm["slice"])
                if s is None:
                    self.err("RL-05", f"{name}: cites slice {fm['slice']} which the manifest lacks")
                elif s["version"] != v:
                    self.err("RL-05", f"{name}: cites slice {fm['slice']} whose version is {s['version']}")
            if "resolution" in fm:
                r = fm["resolution"]
                s = slices.get(r["in_slice"])
                mr = resolutions.get(v)
                if s is None:
                    self.err("RL-05", f"{name}: resolution cites in_slice {r['in_slice']} which the manifest lacks")
                else:
                    if not (s["start"] <= r["range"]["start"] < r["range"]["end"] <= s["end"]):
                        self.err("RL-05", f"{name}: resolution range [{r['range']['start']},{r['range']['end']}) is not inside slice {r['in_slice']} [{s['start']},{s['end']})")
                    host = self.reg.records.get(s["version"])
                    if host is not None:
                        sub = host[1][r["range"]["start"] - s["start"]:r["range"]["end"] - s["start"]]
                        if sub != body:
                            self.err("RL-05", f"{name}: body is not the cited sub-range of {s['version']}'s bytes")
                if mr is None:
                    self.err("RL-05", f"{name}: no resolutions[] entry in the manifest")
                elif mr["in_slice"] != r["in_slice"] or mr["range"] != r["range"] or mr["sha256"] != sha256(body):
                    self.err("RL-05", f"{name}: record resolution disagrees with the manifest entry")
        if not any(e.startswith("RL-05") for e in self.errs):
            self.note("RL-05", f"chain {lowest}…{current} continuous; {m['slice_count']} slices + {m['resolution_count']} resolutions = {m['version_count']} migrated versions")

    def rl06_previous(self):
        lowest = self.reg.manifest["lowest_version"]
        by_num = {vnum(v): v for v in self.reg.records}
        nulls = []
        for v in self.reg.sorted_versions():
            fm, _, name = self.reg.records[v]
            prev = fm.get("previous_version")
            if prev is None:
                nulls.append(v)
                if v != lowest:
                    self.err("RL-06", f"{name}: previous_version null but lowest_version is {lowest} (second chain start)")
                if fm.get("kind") != "migrated":
                    self.err("RL-06", f"{name}: a {fm.get('kind')} record may not carry previous_version null")
                continue
            expected = by_num.get(vnum(v) - 1)
            if expected is None:
                self.err("RL-06", f"{name}: previous_version {prev} names a record that does not exist")
            elif prev != expected:
                self.err("RL-06", f"{name}: previous_version {prev}, expected {expected}")
        if len(nulls) != 1:
            self.err("RL-06", f"exactly one record must carry previous_version null (the manifest's lowest_version {lowest}); found {nulls}")
        elif not any(e.startswith("RL-06") for e in self.errs):
            self.note("RL-06", f"previous_version chain exact; boundary at {lowest}")

    def rl07_rl08_anomalies(self):
        entries = (self.reg.anomalies or {}).get("anomalies", [])
        by_id = {}
        for a in entries:
            if not ANOMALY_ID_RE.match(str(a.get("id"))):
                self.err("RL-08", f"anomaly id {a.get('id')!r} malformed")
                continue
            if a["id"] in by_id:
                self.err("RL-08", f"duplicate anomaly id {a['id']}")
            by_id[a["id"]] = a
            for k in ("affects", "observed", "cited_by", "permits", "kind"):
                if not a.get(k):
                    self.err("RL-08", f"{a['id']}: field {k} missing or blank")
            if a.get("frozen") is not True:
                self.err("RL-08", f"{a['id']}: frozen must be true — an anomaly is a historical fact, not a live lever")
        mig_current = vnum(self.reg.manifest["current_version"])
        for a in by_id.values():
            try:
                if vnum(a["affects"]) > mig_current:
                    self.err("RL-08", f"{a['id']}: affects {a['affects']}, newer than the migration base {self.reg.manifest['current_version']} — new irregularities fail, they are not baselined")
            except ValueError:
                self.err("RL-08", f"{a['id']}: affects {a['affects']!r} is not a version")
            if a["affects"] not in self.reg.records:
                self.err("RL-08", f"{a['id']}: affects {a['affects']} which has no record")

        def permitted(version, kind):
            return [a for a in by_id.values() if a["affects"] == version and a["kind"] == kind and a["permits"] == "RL-07"]

        for v in self.reg.sorted_versions():
            fm, body, name = self.reg.records[v]
            text = body.decode("utf-8", errors="replace")
            if DOUBLED_LABEL_RE.search(text):
                hits = permitted(v, "doubled_label")
                if not hits:
                    self.err("RL-07", f"{name}: doubled version label in the note and no anomaly entry permits it")
            if "resolution" in fm:
                aid = fm.get("anomaly")
                hits = [a for a in permitted(v, "no_slice_of_its_own") if a["id"] == aid]
                if not hits:
                    self.err("RL-07", f"{name}: resolves into another version's bytes but anomaly {aid!r} does not permit RL-07 for {v}")
                if fm.get("shared_slice") is not True:
                    self.err("RL-07", f"{name}: resolution-bearing record must carry shared_slice: true")
        if not any(e.startswith(("RL-07", "RL-08")) for e in self.errs):
            self.note("RL-07", f"{len(by_id)} anomaly entries, all frozen, none newer than the migration base")

    # -- RL-02 -------------------------------------------------------------------------
    def rl02_ledger(self):
        L = self.reg.ledger or {}
        entries = L.get("allocations", [])
        rows = dict(table_data_rows(self.reg.regtxt)["correspondence"])
        keys, numbers = set(), []
        for e in entries:
            key = str(e.get("key"))
            if key in keys:
                self.err("RL-02", f"duplicate ledger key {key}")
            keys.add(key)
            if e.get("state") not in LEDGER_STATES:
                self.err("RL-02", f"{key}: state {e.get('state')!r} not in {LEDGER_STATES}")
            n = e.get("number")
            if n is not None:
                if not isinstance(n, int):
                    self.err("RL-02", f"{key}: number must be an integer or null")
                else:
                    numbers.append(n)
            for k in ("identity", "allocated_by", "actor"):
                if not e.get(k):
                    self.err("RL-02", f"{key}: {k} missing or blank")
            if e.get("state") == "landed":
                if key not in rows:
                    self.err("RL-02", f"{key}: landed but no correspondence-table row carries that key")
                lv = e.get("landed_version")
                if lv is not None and lv not in self.reg.records:
                    self.err("RL-02", f"{key}: landed_version {lv} has no version record")
            if e.get("state") in ("reserved", "withdrawn") and key in rows:
                self.err("RL-02", f"{key}: state {e['state']} but a table row exists")
        for key in rows:
            if re.fullmatch(r"\d{3}\+", key) or key == "—":
                continue
            if key not in keys:
                self.err("RL-02", f"table row {key} has no ledger entry")
        nf = next_free_row_number(self.reg.regtxt)
        derived = (max(numbers) + 1) if numbers else None
        if nf is None:
            self.err("RL-02", "no next-free row (NNN+) in the correspondence table")
        elif derived is not None and nf != derived:
            self.err("RL-02", f"next-free row says {nf:03d}+ but the ledger derives {derived:03d}+ (max allocated number + 1)")
        if L.get("next_free") is not None and L.get("next_free") != derived:
            self.err("RL-02", f"ledger next_free {L.get('next_free')} != derived {derived}")
        if not any(e.startswith("RL-02") for e in self.errs):
            self.note("RL-02", f"{len(entries)} ledger entries; next free derived {derived:03d}+")

    # -- RL-09 -------------------------------------------------------------------------
    def rl09_immutable(self, prior_versions):
        """prior_versions: {filename: bytes} from a prior tree (fixture, or origin/main)."""
        for name, prior in sorted(prior_versions.items()):
            path = os.path.join(self.reg.versions_dir, name)
            if not os.path.exists(path):
                self.err("RL-09", f"{name} exists on the prior tree and was deleted")
            elif read_bytes(path) != prior:
                self.err("RL-09", f"{name} differs from the prior tree — merged version records are immutable; correct forward with a new version")
        if not any(e.startswith("RL-09") for e in self.errs):
            self.note("RL-09", f"{len(prior_versions)} prior records byte-identical")

    # -- RL-11 -------------------------------------------------------------------------
    def rl11_shape(self):
        for v in self.reg.sorted_versions():
            fm, _, name = self.reg.records[v]
            if fm.get("kind") == "migrated" and v not in self.reg.slices() and v not in self.reg.resolutions() \
                    and v not in {s["version"] for s in self.reg.manifest["slices"]}:
                self.err("RL-11", f"{name}: kind migrated but the manifest knows nothing of it (hand-written?)")
            if fm.get("kind") == "finalized" and not fm.get("finalized_from_main"):
                self.err("RL-11", f"{name}: finalized record without finalized_from_main (hand-written?)")

    def rl11_stale(self, origin_main_sha, on_main):
        for v in self.reg.sorted_versions():
            fm, _, name = self.reg.records[v]
            if name in on_main or fm.get("kind") != "finalized":
                continue
            if fm.get("finalized_from_main") != origin_main_sha:
                self.err("RL-11", f"{name}: not on origin/main and finalized_from_main {str(fm.get('finalized_from_main'))[:12]} != origin/main {origin_main_sha[:12]} — finalized against a stale base or hand-written")

    # -- RL-13 / RL-14 -----------------------------------------------------------------
    def rl13_rl14_rows(self, base_regtxt):
        m = self.reg.manifest
        base, head = table_data_rows(base_regtxt), table_data_rows(self.reg.regtxt)
        permitted = m.get("table_baseline", {}).get("permitted_changes", {})
        added = set(permitted.get("rows_added", []))
        modified = set(permitted.get("rows_modified", []))
        base_rows, head_rows = dict(base["correspondence"]), dict(head["correspondence"])
        if len(base["correspondence"]) != m["table_baseline"]["correspondence_rows"] or len(base["instruments"]) != m["table_baseline"]["instruments_rows"]:
            self.err("RL-13", f"base data rows {len(base['correspondence'])}+{len(base['instruments'])} != manifest baseline {m['table_baseline']['correspondence_rows']}+{m['table_baseline']['instruments_rows']}")
        for key, text in base_rows.items():
            nf = re.fullmatch(r"\d{3}\+", key)
            if nf:
                if permitted.get("next_free_row") is not True and (key not in head_rows or head_rows[key] != text):
                    self.err("RL-13", f"next-free row changed but the manifest does not permit it")
                continue
            if key not in head_rows:
                self.err("RL-13", f"row {key} present at base is missing at HEAD")
            elif head_rows[key] != text and key not in modified:
                self.err("RL-13", f"row {key} differs from base and is not a permitted change")
        for key in head_rows:
            if key in base_rows:
                continue
            if re.fullmatch(r"\d{3}\+", key):
                if permitted.get("next_free_row") is not True:
                    self.err("RL-13", f"new next-free row {key} not permitted")
                continue
            if key not in added:
                self.err("RL-13", f"row {key} added at HEAD is not a permitted addition")
        if base["instruments"] != head["instruments"]:
            self.err("RL-14", "instruments table data rows differ from base")
        if not any(e.startswith(("RL-13", "RL-14")) for e in self.errs):
            self.note("RL-13", f"{len(base_rows)} + {len(base['instruments'])} base data rows: every row byte-identical except {sorted(added)} added, {sorted(modified)} modified, next-free {'replaced' if permitted.get('next_free_row') else 'unchanged'}")

    # -- RL-18 -------------------------------------------------------------------------
    def rl18_rule18(self, prior_regtxt=None):
        present = bool(RULE18_RE.search(self.reg.regtxt))
        self.note("RL-18", f"Rule 18 merge-method sentinel {'present' if present else 'absent'} — settings check {'enforcing' if present else 'report-only'}")
        if prior_regtxt is None:
            return present
        prior = RULE18_RE.search(prior_regtxt)
        if prior:
            head = RULE18_RE.search(self.reg.regtxt)
            if head is None or head.group(0) != prior.group(0):
                if SUPERSEDES_RULE18_RE.search(self.reg.regtxt) and not SUPERSEDES_RULE18_RE.search(prior_regtxt):
                    self.note("RL-18", "Rule 18 superseded by an explicitly numbered successor rule in this head")
                else:
                    self.err("RL-18", "Rule 18 is present on the prior tree and is absent or altered here — the ratchet permits only an explicitly numbered successor rule (\"Supersedes Rule 18\"), never deletion or in-place edit")
        return present

    # -- Git tier ----------------------------------------------------------------------
    def git_tier(self):
        repo = self.reg.repo
        try:
            git(repo, "rev-parse", "--is-inside-work-tree")
            origin_main = git(repo, "rev-parse", "origin/main").strip()
        except RuntimeError as e:
            for r in ("RL-10", "RL-16", "RL-17", "RL-11(stale)", "RL-09(origin/main)", "RL-18(ratchet)"):
                self.warn(r, f"skipped — {e}")
            return
        m = self.reg.manifest
        vdir = REGISTER_DIR_REL.replace(os.sep, "/") + "/versions/"
        # prior tree from origin/main for RL-09 and RL-18
        on_main = {}
        for line in git(repo, "ls-tree", "--name-only", origin_main, vdir, check=False).split("\n"):
            if line.strip():
                name = line.strip().split("/")[-1]
                on_main[name] = git_bytes(repo, "show", f"{origin_main}:{line.strip()}")
        self.rl09_immutable(on_main)
        try:
            prior_reg = git_bytes(repo, "show", f"{origin_main}:{REGISTER_REL.replace(os.sep, '/')}").decode("utf-8")
        except RuntimeError:
            prior_reg = None
        self.rl18_rule18(prior_reg)
        self.rl11_stale(origin_main, on_main)
        # RL-16 baseline drift
        base = m["base_commit"]
        try:
            base_reg = git_bytes(repo, "show", f"{base}:{REGISTER_REL.replace(os.sep, '/')}")
        except RuntimeError as e:
            self.err("RL-16", f"cannot read REGISTER.md at base_commit {base[:12]}: {e}")
            base_reg = None
        if base_reg is not None and sha256(base_reg) != m["source_sha256"]:
            self.err("RL-16", f"sha256(REGISTER.md @ {base[:12]}) != manifest source_sha256")
        if subprocess.run(["git", "merge-base", "--is-ancestor", base, "HEAD"], cwd=repo).returncode != 0:
            self.err("RL-16", f"base_commit {base[:12]} is not an ancestor of HEAD")
        manifest_rel = os.path.relpath(self.reg.manifest_paths[0], repo).replace(os.sep, "/")
        mig = git(repo, "log", "--first-parent", "--diff-filter=A", "--format=%H", "HEAD", "--", manifest_rel).strip().split("\n")[-1]
        if not mig:
            self.warn("RL-16", "manifest not yet committed — the base..migration commit-range check is skipped")
        if mig:
            between = git(repo, "log", "--format=%H", f"{base}..{mig}^", "--", CORRESPONDENCE_REL, check=False).split()
            between = [c for c in between if c != mig]
            if between:
                self.err("RL-16", f"commits between base and the migration commit touch docs/correspondence/: {[c[:12] for c in between]}")
            else:
                self.note("RL-16", f"baseline fixed at {base[:12]}; migration commit {mig[:12]}; nothing in between touches docs/correspondence/")
        # RL-17 one-time introduction
        introducers = {}
        for v in self.reg.sorted_versions():
            fm, _, name = self.reg.records[v]
            if fm.get("kind") in ("migrated", "bootstrap"):
                c = git(repo, "log", "--first-parent", "--diff-filter=A", "--format=%H", "HEAD", "--", vdir + name).strip().split("\n")[-1]
                introducers.setdefault(c, []).append(name)
        if len(introducers) > 1:
            self.err("RL-17", f"migrated/bootstrap records introduced by {len(introducers)} different first-parent commits: {sorted(k[:12] for k in introducers)}")
        elif introducers:
            self.note("RL-17", f"all {sum(len(v) for v in introducers.values())} migrated records introduced by one first-parent commit {list(introducers)[0][:12]}")
        # RL-10 landing facts and one finalized record per landing, on origin/main
        finalized_on_main = {name for name in on_main if parse_record(on_main[name])[0].get("kind") == "finalized"}
        for name in sorted(finalized_on_main):
            fm = parse_record(on_main[name])[0]
            c = git(repo, "log", "--first-parent", "--diff-filter=A", "--format=%H", origin_main, "--", vdir + name).strip().split("\n")[-1]
            parents = git(repo, "rev-list", "--parents", "-n", "1", c).split()
            first = parents[1] if len(parents) > 1 else None
            second = parents[2] if len(parents) > 2 else None
            date = git(repo, "log", "-1", "--format=%cI", c).strip()
            if first != fm.get("finalized_from_main"):
                self.err("RL-10", f"{name}: introduced by {c[:12]} whose first parent {str(first)[:12]} != finalized_from_main {str(fm.get('finalized_from_main'))[:12]} — finalized against a base that was not the merge base")
            else:
                self.note("RL-10", f"{name}: landed by {c[:12]} (first parent {first[:12]}, landing head {second[:12] if second else 'none — not a merge commit'}, landed {date}) — derived, never stored")
        merges = git(repo, "log", "--first-parent", "--format=%H", f"{base}..{origin_main}", "--", CORRESPONDENCE_REL, check=False).split()
        for c in merges:
            added_files = [l for l in git(repo, "diff-tree", "--no-commit-id", "-r", "--diff-filter=A", "--name-only", "-m", "--first-parent", c).split("\n") if l.startswith(vdir)]
            kinds = []
            for f in added_files:
                try:
                    kinds.append(parse_record(git_bytes(repo, "show", f"{c}:{f}"))[0].get("kind"))
                except (RuntimeError, ValueError):
                    kinds.append("unreadable")
            n_fin = kinds.count("finalized")
            if n_fin == 0 and kinds and all(k in ("migrated", "bootstrap") for k in kinds):
                continue  # the migration merge: invisible to this rule by construction (G-16)
            if n_fin != 1:
                self.err("RL-10", f"first-parent commit {c[:12]} on main touches docs/correspondence/ and introduces {n_fin} finalized records (exactly one per landing, Q-02)")

    # -- driver ------------------------------------------------------------------------
    def run(self):
        if not self.rl03_authority_set():
            return
        if self.reg.manifest is None:
            self.err("RL-03", "no MIGRATION-*.yaml manifest")
            return
        self.rl04_pointer()
        self.rl12_schema()
        self.rl01_partition()
        self.rl05_chain()
        self.rl06_previous()
        self.rl07_rl08_anomalies()
        self.rl02_ledger()
        self.rl11_shape()
        if self.prior_tree:
            pv = {}
            pdir = os.path.join(self.prior_tree, "versions")
            if os.path.isdir(pdir):
                for n in os.listdir(pdir):
                    pv[n] = read_bytes(os.path.join(pdir, n))
            self.rl09_immutable(pv)
            preg = os.path.join(self.prior_tree, "REGISTER.md")
            self.rl18_rule18(read_bytes(preg).decode("utf-8") if os.path.exists(preg) else None)
        elif not self.git_mode:
            self.warn("RL-09", "skipped — no --prior-tree and no --git; immutability not checked")
            self.rl18_rule18(None)
        if self.migration_base:
            self.rl13_rl14_rows(read_bytes(self.migration_base).decode("utf-8"))
        elif self.git_mode and self.reg.manifest:
            # Migration mode applies while the migration is still a proposal: once the manifest
            # is on origin/main the row baseline is history, and later landings add rows.
            try:
                manifest_rel = os.path.relpath(self.reg.manifest_paths[0], self.reg.repo).replace(os.sep, "/")
                on_main = git(self.reg.repo, "ls-tree", "--name-only", "origin/main", manifest_rel, check=False).strip()
                if on_main:
                    self.note("RL-13", "migration already on origin/main — row identity was checked at its landing; not re-applied to later landings")
                else:
                    self.rl13_rl14_rows(git_bytes(self.reg.repo, "show", f"{self.reg.manifest['base_commit']}:{REGISTER_REL.replace(os.sep, '/')}").decode("utf-8"))
            except RuntimeError as e:
                self.warn("RL-13", f"skipped — {e}")
        else:
            self.warn("RL-13", "skipped — no --migration BASE and no --git; row identity not checked")
        if self.git_mode:
            self.git_tier()
        else:
            for r in ("RL-10", "RL-16", "RL-17", "RL-11(stale)"):
                self.warn(r, "skipped — needs .git and origin/main (--git)")


def run_lint(repo, git_mode=False, migration_base=None, prior_tree=None, out=print):
    try:
        reg = Register(repo)
    except (OSError, yaml.YAMLError, UnicodeDecodeError) as e:
        out(f"ERROR cannot load the register at {repo}: {e}")
        return 2
    lint = Lint(reg, git_mode=git_mode, migration_base=migration_base, prior_tree=prior_tree)
    lint.run()
    for n in lint.notes:
        out("  " + n)
    for w in lint.warns:
        out("  " + w)
    for e in lint.errs:
        out("  " + e)
    out(f"register_lint: {len(lint.errs)} errors, {len(lint.warns)} warnings (structural checks only — not a semantic pass)")
    return 1 if lint.errs else 0


# ---------------------------------------------------------------- subcommands

def resolve(reg, version):
    """(kind, locator, sha256, body) for one version — a citation such as 'the .9 note'."""
    rec = reg.records.get(version)
    if rec is None:
        # a citation such as "the .9 note" — bare numeric suffix, with or without the dot
        m = re.fullmatch(r"\.?(\d+)", str(version))
        if m:
            by_num = {vnum(v): v for v in reg.records}
            rec = reg.records.get(by_num.get(int(m.group(1))))
        if rec is None:
            raise KeyError(version)
    fm, body, name = rec
    if "slice" in fm:
        return "slice", fm["slice"], sha256(body), body
    if "resolution" in fm:
        return "resolution", fm["resolution"], sha256(body), body
    return fm.get("kind"), fm.get("finalized_from_main"), sha256(body), body


def main(argv):
    args = list(argv)
    repo = DEFAULT_REPO
    if "--repo" in args:
        i = args.index("--repo")
        repo = args[i + 1]
        del args[i:i + 2]
    if args and args[0] == "resolve":
        reg = Register(repo)
        targets = reg.sorted_versions() if "--all" in args[1:] else args[1:2]
        if not targets:
            sys.stderr.write("usage: register_lint.py resolve (VERSION | --all)\n")
            return 2
        bad = 0
        for v in targets:
            try:
                kind, loc, digest, body = resolve(reg, v)
            except KeyError:
                print(f"{v}: ERROR no record")
                bad += 1
                continue
            manifest_digest = None
            if kind == "slice":
                manifest_digest = reg.slices()[loc]["sha256"]
            elif kind == "resolution":
                manifest_digest = reg.resolutions()[v]["sha256"]
            ok = manifest_digest in (None, digest)
            print(f"{v}: {kind} {loc if isinstance(loc, str) else loc['in_slice'] + str([loc['range']['start'], loc['range']['end']])} sha256 {digest} {len(body)} bytes {'OK' if ok else 'ERROR digest != manifest'}")
            bad += 0 if ok else 1
        return 1 if bad else 0
    if args and args[0] == "render":
        reg = Register(repo)
        for v in reversed(reg.sorted_versions()):
            fm, body, _ = reg.records[v]
            sys.stdout.write(f"## {v}\n\n{body.decode('utf-8', errors='replace')}\n\n")
        return 0
    if args and args[0] == "rule18":
        reg = Register(repo)
        print("present" if RULE18_RE.search(reg.regtxt) else "absent")
        return 0
    git_mode = "--git" in args
    migration_base = args[args.index("--migration") + 1] if "--migration" in args else None
    prior_tree = args[args.index("--prior-tree") + 1] if "--prior-tree" in args else None
    for flag in ("--git",):
        if flag in args:
            args.remove(flag)
    for flag in ("--migration", "--prior-tree"):
        if flag in args:
            i = args.index(flag)
            del args[i:i + 2]
    if args:
        sys.stderr.write(__doc__ or "")
        return 2
    return run_lint(repo, git_mode=git_mode, migration_base=migration_base, prior_tree=prior_tree)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
