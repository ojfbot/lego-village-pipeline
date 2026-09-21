#!/usr/bin/env python3
"""Acceptance battery for the register migration (HANDOFF-LEGO-PIPE-032-R1; R0 §6, §9).

Two explicitly named modes (RR-32-08):

    python3 tests/test_register.py              # offline: no .git, no origin/main needed
    python3 tests/test_register.py --with-git   # also the Git-tier rules and the two-branch
                                                # rehearsal, in temporary repositories the
                                                # battery builds itself — plus the migration
                                                # reproduction from the manifest's base commit
                                                # (the one case that reads the project's .git)

Every RL-nn / RF-nn id declared in tools/register_lint.py and tools/register_finalize.py has a
positive case and a mutation case here; RULE_TESTS maps each id to both, and the meta-test
fails if any id lacks either (029's "ran 0 tests" shape: the battery cannot silently cover
fewer rules than the tools declare). Quote the mode with every count you cite from this file.

Needs PyYAML: re-execs itself under tools/.venv (tools/setup-preflight.sh creates it).
"""
import copy
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(REPO, "tools")
sys.path.insert(0, TOOLS)

from schema_lint import check_against_schema, load_schema, require_yaml  # noqa: E402

yaml = require_yaml("REGISTER_TESTS_REEXEC")

import register_lint as RL  # noqa: E402
import register_migrate as RM  # noqa: E402
import register_finalize as RF  # noqa: E402

WITH_GIT = "--with-git" in sys.argv or os.environ.get("REGISTER_TESTS_WITH_GIT") == "1"
if "--with-git" in sys.argv:
    sys.argv.remove("--with-git")

REGISTER = os.path.join(REPO, RL.REGISTER_REL)
REG_DIR = os.path.join(REPO, RL.REGISTER_DIR_REL)
CORR = os.path.join(REPO, "docs", "correspondence")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run_tool(script, *args, cwd=REPO, env=None):
    p = subprocess.run([sys.executable, os.path.join(TOOLS, script), *args],
                       capture_output=True, text=True, cwd=cwd, env=env)
    return p.returncode, p.stdout + p.stderr


def lint_errs(repo, **kw):
    reg = RL.Register(repo)
    lint = RL.Lint(reg, **kw)
    lint.run()
    return lint.errs, lint.warns, lint.notes


def errs_for(rule, errs):
    return [e for e in errs if e.startswith(rule + " ")]


def bootstrap_tree(tmp, name="repo"):
    """The MIGRATION's own output — the bootstrap state — constructed explicitly, never copied
    from the live tree (F-08/H4). At H0–H2 the live tree happened to equal this; after the
    first real finalization it legitimately does not (pointer .32, a finalized record, a
    consumed allocation), and a fixture that copied it asserted bootstrap facts against
    forward state. Built by running register_migrate.migrate() over the offline-reconstructed
    base (its version line is proved identical to B's by the manifest digests) and overlaying
    the committed manifest, which is migration-owned and immutable — the only artifact whose
    whole-file source fields cannot be recomputed without B's rows. Result: 30 `kind:
    migrated` records, pointer at the manifest's current_version, the seed ledger (032-R1
    in_flight, 033/034/035 reserved), the anomalies — and nothing produced by finalization."""
    root = os.path.join(tmp, name)
    live = RL.Register(REPO)
    RM.migrate(reconstruct_base_register(REPO), live.manifest["base_commit"], root)
    produced_manifest = manifest_path(root)
    committed_manifest = live.manifest_paths[0]
    prod = RL.load_yaml_file(produced_manifest)
    for k in ("line_sha256", "line_bytes", "slices", "resolutions", "seams", "preamble", "lowest_version", "version_count", "current_version"):
        assert prod[k] == live.manifest[k], f"bootstrap fixture: migrator no longer reproduces manifest.{k}"
    shutil.copyfile(committed_manifest, produced_manifest)
    reg = RL.Register(root)
    assert len(reg.records) == 30 and all(fm["kind"] == "migrated" for fm, _, _ in reg.records.values())
    assert RL.register_version_line(reg.regtxt)[2] == reg.manifest["current_version"]
    return root


def copy_tree(tmp):
    """Bootstrap-state working tree for mutation (kept under its historical name; see
    bootstrap_tree — this is no longer a copy of the live tree)."""
    return bootstrap_tree(tmp)


def migration_note_bytes():
    """The 032 migration's pending note, for fixtures that need a real-sized note: read from
    register/pending/ on a pre-finalization tree, or re-derived from the finalized record that
    consumed it on a post-finalization tree (frontmatter from the record's fields, body byte-
    exact — the finalizer's note_sha256 is sha256(body), so the derived note finalizes to the
    same digest)."""
    pending = os.path.join(REG_DIR, "pending", "032-register-migration.md")
    if os.path.exists(pending):
        return RL.read_bytes(pending)
    reg = RL.Register(REPO)
    for fm, body, _ in reg.records.values():
        if fm.get("kind") == "finalized" and fm.get("allocations_consumed") == ["032-R1"]:
            return RL.record_bytes({"affected_memos": list(fm["affected_memos"]), "allocations_consumed": ["032-R1"]}, body)
    raise AssertionError("neither the 032 pending note nor its finalized record is present")


def manifest_path(root):
    return RL.Register(root).manifest_paths[0]


def edit_yaml(path, fn):
    with open(path, "rb") as f:
        doc = yaml.safe_load(f.read().decode("utf-8"))
    fn(doc)
    RL.write_bytes(path, RL.dump_yaml(doc).encode("utf-8"))


def edit_record(root, version, fn_fm=None, body=None):
    p = os.path.join(root, RL.REGISTER_DIR_REL, "versions", f"{version}.md")
    fm, b = RL.parse_record(RL.read_bytes(p))
    if fn_fm:
        fn_fm(fm)
    if body is not None:
        b = body
    if "note_sha256" in fm and body is not None:
        fm["note_sha256"] = sha(b)
    RL.write_bytes(p, RL.record_bytes(fm, b))
    return p


def write_record(root, fm, body):
    p = os.path.join(root, RL.REGISTER_DIR_REL, "versions", f"{fm['register_version']}.md")
    fm = dict(fm)
    fm["note_sha256"] = sha(body)
    RL.write_bytes(p, RL.record_bytes(fm, body))
    return p


def base_register_bytes():
    """The base REGISTER.md bytes: from the project's git when available, else reconstructed
    from the manifest (preamble + slices) into the migrated file — the offline mode's source."""
    reg = RL.Register(REPO)
    m = reg.manifest
    if WITH_GIT:
        return RL.git_bytes(REPO, "show", f"{m['base_commit']}:docs/correspondence/REGISTER.md")
    return None


def reconstruct_base_register(root):
    """Rebuild the pre-migration REGISTER.md bytes offline: the migrated file with its version
    line replaced by preamble + slices. Valid only for the version line; rows are as at HEAD,
    so RL-13 offline cases build their own base from this and mutate HEAD."""
    reg = RL.Register(root)
    data = RL.read_bytes(os.path.join(root, RL.REGISTER_REL))
    lines = data.split(b"\n")
    idx = reg.manifest["line_number"] - 1
    lines[idx] = b"**Register version: " + reg.manifest["current_version"].encode() + b"** \xe2\x80\x94 bump this line on every edit. " + reg.reconstruct_line()[reg.manifest["preamble"]["end"]:]
    return b"\n".join(lines)


def pre_migration_rows(base):
    """Undo the permitted table changes so a HEAD-derived register models B's table offline."""
    out = []
    for l in base.decode("utf-8").split("\n"):
        if l.startswith("| 032-R1 |"):
            continue
        if l.startswith("| 036+ |"):
            l = "| 032+ | next free — (base) | | | | |"
        if l.startswith("| 030-R0 |") or l.startswith("| 031-R0 |"):
            l = l.replace("**accepted as amended by HANDOFF-LEGO-PIPE-032-R1** (operator docket 2026-09-20, PR #21 comment 5752476543; the migration landing's version record names it) — was: for review", "**for review")
            l = l.replace("2026-09-19. Landed", "2026-09-19.** Landed")
        out.append(l)
    return "\n".join(out).encode("utf-8")


def finalized_fm(version="2026-09-18.32", prev="2026-09-18.31", main="a" * 40):
    return {"register_version": version, "previous_version": prev, "kind": "finalized",
            "finalized_from_main": main, "affected_memos": ["X-LEGO-PIPE-099"], "allocations_consumed": ["099"]}


# ======================================================================= schema (RL-12)

class RecordSchema(unittest.TestCase):
    """register-version/v1 encodes R0 §4 item 3's per-kind table exactly (RR-32-R2-01)."""

    def setUp(self):
        self.schema = load_schema("register-version.v1")

    def errs(self, doc):
        e = []
        check_against_schema(doc, self.schema, e)
        return e

    def base(self, **kw):
        d = {"register_version": "2026-09-18.31", "previous_version": "2026-09-18.30",
             "kind": "migrated", "note_sha256": "0" * 64}
        d.update(kw)
        return d

    def test_positive_migrated_slice(self):
        self.assertEqual(self.errs(self.base(slice="s-31")), [])

    def test_positive_migrated_resolution_with_shared_slice_and_anomaly(self):
        self.assertEqual(self.errs(self.base(resolution={"in_slice": "s-08", "range": {"start": 1, "end": 2}},
                                             shared_slice=True, anomaly="A-03")), [])

    def test_positive_finalized_matches_the_finalizer_output(self):
        current, main = "2026-09-18.31", "b" * 40
        nxt, fm, body = RF.compute(current, main, [("n.md", {"affected_memos": ["M"], "allocations_consumed": ["032-R1"]}, b"note")])
        self.assertEqual(nxt, "2026-09-18.32")
        self.assertEqual(self.errs(fm), [])

    def test_positive_bootstrap(self):
        self.assertEqual(self.errs(self.base(kind="bootstrap", manifest_ref="register/MIGRATION-x.yaml")), [])

    def test_positive_lowest_record_carries_null(self):
        self.assertEqual(self.errs(self.base(register_version="2026-09-17.2", previous_version=None,
                                             resolution={"in_slice": "s-08", "range": {"start": 1, "end": 2}},
                                             shared_slice=True, anomaly="A-08")), [])

    def test_negative_required_key_omissions(self):
        for k in ("register_version", "previous_version", "kind", "note_sha256"):
            d = self.base(slice="s-31")
            del d[k]
            self.assertTrue(self.errs(d), k)
        self.assertTrue(self.errs(self.base()), "migrated without slice or resolution")
        self.assertTrue(self.errs(self.base(resolution={"in_slice": "s-08", "range": {"start": 1, "end": 2}}, shared_slice=True)),
                        "resolution without anomaly id")
        self.assertTrue(self.errs(self.base(kind="finalized", affected_memos=["m"], allocations_consumed=["a"])),
                        "finalized without finalized_from_main")
        self.assertTrue(self.errs(self.base(kind="bootstrap")), "bootstrap without manifest_ref")

    def test_negative_forbidden_key_presence(self):
        self.assertTrue(self.errs(self.base(slice="s-31", shared_slice=True)), "slice-bearing migrated with shared_slice (CW-32-R3-03)")
        self.assertTrue(self.errs(self.base(slice="s-31", anomaly="A-01")), "slice-bearing migrated with anomaly id")
        self.assertTrue(self.errs(self.base(slice="s-31", finalized_from_main="c" * 40)), "migrated with finalized_from_main")
        fin = self.base(kind="finalized", finalized_from_main="c" * 40, affected_memos=["m"], allocations_consumed=["a"])
        self.assertTrue(self.errs(dict(fin, slice="s-1")), "finalized carrying slice (TR-32-R2-01)")
        self.assertTrue(self.errs(dict(fin, resolution={"in_slice": "s-08", "range": {"start": 1, "end": 2}})), "finalized carrying resolution")
        self.assertTrue(self.errs(dict(fin, previous_version=None)), "finalized carrying null")
        boot = self.base(kind="bootstrap", manifest_ref="x")
        self.assertTrue(self.errs(dict(boot, finalized_from_main="c" * 40)), "bootstrap with finalized_from_main")
        self.assertTrue(self.errs(dict(boot, previous_version=None)), "bootstrap carrying null")
        self.assertTrue(self.errs(self.base(slice="s-31", landing_pr=21)), "landing_pr on any kind")
        self.assertTrue(self.errs(self.base(slice="s-31", kind="rebuilt")), "fourth kind")

    def test_negative_second_bootstrap_rejected_by_lint(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            for v in ("2026-09-18.32", "2026-09-18.33"):
                write_record(root, {"register_version": v, "previous_version": f"2026-09-18.{int(v[-2:]) - 1}", "kind": "bootstrap",
                                    "manifest_ref": "register/MIGRATION-x.yaml"}, b"x")
            RL.write_bytes(os.path.join(root, RL.REGISTER_REL), RF.pointer_line(RL.read_bytes(os.path.join(root, RL.REGISTER_REL)).decode(), "2026-09-18.33").encode())
            errs, _, _ = lint_errs(root)
            self.assertTrue(any("bootstrap records; at most one" in e for e in errs_for("RL-12", errs)), errs)

    def test_negative_invented_predecessor_is_rejected_by_lint(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            edit_record(root, "2026-09-17.2", lambda fm: fm.update(previous_version="2026-09-17.1"))
            errs, _, _ = lint_errs(root)
            self.assertTrue(any("names a record that does not exist" in e for e in errs_for("RL-06", errs)), errs)
            self.assertTrue(any("exactly one record must carry previous_version null" in e for e in errs_for("RL-06", errs)), errs)

    def test_mutation_schema_missing_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            real = RL.load_schema
            RL.load_schema = lambda stem: (_ for _ in ()).throw(OSError("gone"))
            try:
                errs, _, _ = lint_errs(root)
            finally:
                RL.load_schema = real
            self.assertTrue(any("fail closed" in e for e in errs_for("RL-12", errs)), errs)

    def test_mutation_forbidden_key_in_a_committed_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            edit_record(root, "2026-09-18.31", lambda fm: fm.update(finalized_from_main="c" * 40))
            errs, _, _ = lint_errs(root)
            self.assertTrue(errs_for("RL-12", errs), errs)

    def test_mutation_note_sha_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            edit_record(root, "2026-09-18.31", lambda fm: fm.update(note_sha256="f" * 64))
            errs, _, _ = lint_errs(root)
            self.assertTrue(any("note_sha256" in e for e in errs_for("RL-12", errs)), errs)


# ======================================================================= migration proof

class MigrationProof(unittest.TestCase):
    """G-01 / G-02 / G-03 / G-03a / G-03b / G-03d — the partition, the seams, the resolver."""

    def test_committed_tree_is_green_offline(self):
        errs, warns, notes = lint_errs(REPO)
        self.assertEqual(errs, [], errs)
        self.assertTrue(any("RL-01 partition exact" in n for n in notes), notes)

    def test_positive_rl01_reconstruction_and_digests(self):
        reg = RL.Register(REPO)
        m = reg.manifest
        line = reg.reconstruct_line()
        self.assertEqual(len(line), m["line_bytes"])
        self.assertEqual(sha(line), m["line_sha256"])
        self.assertEqual(m["preamble"]["end"] + sum(s["end"] - s["start"] for s in m["slices"]), m["line_bytes"])
        for s in m["slices"]:
            self.assertEqual(sha(line[s["start"]:s["end"]]), s["sha256"], s["id"])
        self.assertEqual(m["slice_count"], 24)
        self.assertEqual(m["resolution_count"], 6)
        self.assertEqual(m["version_count"], 30)
        self.assertEqual(m["lowest_version"], "2026-09-17.2")
        self.assertEqual(len([s for s in m["seams"] if s["accepted"]]), 23)
        rejected = [s for s in m["seams"] if not s["accepted"]]
        self.assertEqual([(s["byte_offset"], s["version_named"]) for s in rejected], [(26240, 22)])
        self.assertTrue(rejected[0]["reason"])

    def test_mutation_rl01_shift_one_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            def mut(m):
                m["slices"][5]["start"] += 1
            edit_yaml(manifest_path(root), mut)
            errs, _, _ = lint_errs(root)
            self.assertTrue(errs_for("RL-01", errs), errs)

    def test_mutation_rl01_remove_one_slice(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            edit_yaml(manifest_path(root), lambda m: m["slices"].pop(10))
            errs, _, _ = lint_errs(root)
            self.assertTrue(errs_for("RL-01", errs), errs)

    def test_mutation_rl01_overlapping_slice_declared(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            def mut(m):
                s8 = next(s for s in m["slices"] if s["id"] == "s-08")
                m["slices"].append({"id": "s-06", "version": "2026-09-17.6", "start": s8["start"] + 10, "end": s8["end"], "sha256": "0" * 64})
            edit_yaml(manifest_path(root), mut)
            errs, _, _ = lint_errs(root)
            self.assertTrue(any("contiguous and non-overlapping" in e or "partition" in e for e in errs_for("RL-01", errs)), errs)

    def _base_line(self):
        reg = RL.Register(REPO)
        return reg.reconstruct_line(), reg.manifest

    def _inject(self, line, m, into_version, label):
        seam = next(s for s in m["seams"] if s["accepted"] and s["version_named"] == into_version)
        ip = seam["byte_offset"] + 500
        return line[:ip] + b' (the label "At `' + label.encode() + b'`" was quoted here)' + line[ip:], ip

    def test_adversarial_seam_next_expected_version_is_caught_by_byte_offset(self):
        """RR-32-02 / CW-32-01 / AO-18: a quoted label equal to the next expected version defeats
        the descending rule — slice count and whole-line reconstruction both pass on the wrong
        decomposition; only the manifest's committed byte_offset per seam catches it."""
        line, m = self._base_line()
        true25 = next(s for s in m["seams"] if s["accepted"] and s["version_named"] == 25)["byte_offset"]
        self.assertEqual(true25, 20508)
        bad, ip = self._inject(line, m, 26, ".25")
        pre_end, current, seams = RM.split_line(bad)
        accepted = [s for s in seams if s["accepted"]]
        self.assertEqual(len(accepted) + 1, 24, "slice count unchanged on the wrong decomposition")
        wrong25 = next(s for s in accepted if s["version_named"] == 25)["byte_offset"]
        self.assertEqual(wrong25, 12511, "the .25 boundary moved into the .26 note")
        bounds = [pre_end] + [s["byte_offset"] for s in accepted] + [len(bad)]
        self.assertEqual(pre_end + sum(bounds[i + 1] - bounds[i] for i in range(len(bounds) - 1)), len(bad), "reconstruction still byte-exact")
        # The tool, applied naively, commits the wrong decomposition; a steward reading the seam
        # manifest corrects it (rejects the quoted candidate, accepts the true one). RL-01 must
        # then go red on byte_offset — the slice boundaries no longer equal the accepted seams.
        with tempfile.TemporaryDirectory() as tmp:
            src = RL.read_bytes(REGISTER).split(b"\n")
            src[m["line_number"] - 1] = bad
            RM.migrate(b"\n".join(src), "adversarial", tmp)
            mp = RL.Register(tmp).manifest_paths[0]
            def correct(man):
                for s in man["seams"]:
                    if s["byte_offset"] == wrong25:
                        s["accepted"] = False
                        s["reason"] = "quoted inside the .26 note (adversarial fixture)"
                    if s["byte_offset"] == true25 + len(bad) - len(line):
                        s["accepted"] = True
            edit_yaml(mp, correct)
            self._fix_authority(tmp)
            errs, _, _ = lint_errs(tmp)
            self.assertTrue(any("G-02" in e for e in errs_for("RL-01", errs)), errs)

    def test_adversarial_seam_arbitrary_label_is_correctly_rejected(self):
        """Negative control: an arbitrary quoted label (.19 where .25 is expected) is rejected
        by the rule, recorded with a reason, and the decomposition is unchanged."""
        line, m = self._base_line()
        bad, ip = self._inject(line, m, 26, ".19")
        _, _, seams = RM.split_line(bad)
        rejected = [s for s in seams if not s["accepted"]]
        self.assertEqual(len(rejected), 2)
        self.assertIn(bad.index(b"At `.19`"), [s["byte_offset"] for s in rejected])
        self.assertTrue(all(s["reason"] for s in rejected))
        accepted = [s for s in seams if s["accepted"]]
        self.assertEqual(len(accepted), 23)
        with tempfile.TemporaryDirectory() as tmp:
            src = RL.read_bytes(REGISTER).split(b"\n")
            src[m["line_number"] - 1] = bad
            RM.migrate(b"\n".join(src), "control", tmp)
            self._fix_authority(tmp)
            errs, _, _ = lint_errs(tmp)
            self.assertEqual(errs_for("RL-01", errs), [], errs)

    def _fix_authority(self, root):
        pass  # the migrated REGISTER.md written by migrate() already carries the declaration

    def test_utf8_adversarial_split_is_by_bytes_not_characters(self):
        """CW-33-P05 / RR-32-07: an em dash and a curly quote inserted across a slice boundary
        leave the byte-offset split unaffected, while a character-offset implementation would
        cut at the wrong place."""
        line, m = self._base_line()
        seam = next(s for s in m["seams"] if s["accepted"] and s["version_named"] == 20)["byte_offset"]
        mutated = line[:seam - 3] + "—“".encode("utf-8") + line[seam - 3:]
        pre, cur, seams = RM.split_line(mutated)
        new20 = next(s for s in seams if s["accepted"] and s["version_named"] == 20)["byte_offset"]
        self.assertEqual(new20, seam + len("—“".encode("utf-8")))
        self.assertEqual(mutated[new20:new20 + 8], b"At `.20`")
        char_offset = len(mutated[:new20].decode("utf-8"))
        self.assertNotEqual(char_offset, new20, "byte and character offsets differ on this line")
        self.assertNotEqual(mutated[char_offset:char_offset + 8], b"At `.20`", "a character-offset split would land elsewhere")
        self.assertGreater(m["line_non_ascii_bytes"], 0)
        self.assertEqual(m["line_bytes"] - m["line_characters"], 283)

    def test_positive_rl05_resolve_every_version_and_compare_digests(self):
        """30 MIGRATED records always; the live tree may carry finalized records on top
        (31 at H3). The distinction is asserted, not blurred."""
        reg = RL.Register(REPO)
        migrated = {v: r for v, r in reg.records.items() if r[0]["kind"] == "migrated"}
        finalized = {v: r for v, r in reg.records.items() if r[0]["kind"] in ("finalized", "bootstrap")}
        self.assertEqual(len(migrated), 30)
        self.assertEqual(len(reg.records), 30 + len(finalized))
        via_slice = via_res = 0
        for v in reg.sorted_versions():
            kind, loc, digest, body = RL.resolve(reg, v)
            if v in finalized:
                self.assertEqual(kind, "finalized")
                self.assertEqual(digest, finalized[v][0]["note_sha256"])
                continue
            if kind == "slice":
                via_slice += 1
                self.assertEqual(digest, reg.slices()[loc]["sha256"], v)
            else:
                via_res += 1
                self.assertEqual(kind, "resolution")
                self.assertEqual(digest, reg.resolutions()[v]["sha256"], v)
        self.assertEqual((via_slice, via_res), (24, 6))
        code, out = run_tool("register_lint.py", "resolve", "--all")
        self.assertEqual(code, 0, out)
        self.assertEqual(out.count(" OK"), len(reg.records))
        self.assertIn("2026-09-17.6: resolution s-08[38728, 38930]", out)
        # bootstrap state: exactly 30, none finalized
        with tempfile.TemporaryDirectory() as tmp:
            boot = RL.Register(bootstrap_tree(tmp))
            self.assertEqual(len(boot.records), 30)
            self.assertFalse(any(r[0]["kind"] != "migrated" for r in boot.records.values()))

    def test_positive_resolution_records_are_real_bytes_inside_dot8(self):
        reg = RL.Register(REPO)
        body6 = reg.records["2026-09-17.6"][1]
        body8 = reg.records["2026-09-17.8"][1]
        self.assertIn(body6, body8)
        self.assertTrue(body6.startswith(b"`.6` (first committed version"))
        body7 = reg.records["2026-09-17.7"][1]
        self.assertIn(body7, body6, ".7's clause is nested inside .6's")

    def test_mutation_rl05_delete_a_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            os.remove(os.path.join(root, RL.REGISTER_DIR_REL, "versions", "2026-09-18.13.md"))
            errs, _, _ = lint_errs(root)
            self.assertTrue(any("13" in e for e in errs_for("RL-05", errs)), errs)

    def test_mutation_rl05_resolution_range_outside_its_slice(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            edit_record(root, "2026-09-17.6", lambda fm: fm["resolution"]["range"].update(end=10 ** 6))
            errs, _, _ = lint_errs(root)
            self.assertTrue(any("not inside slice" in e for e in errs_for("RL-05", errs)), errs)

    def test_mutation_rl05_counts_checked_separately(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            edit_yaml(manifest_path(root), lambda m: m.update(version_count=25, slice_count=25, resolution_count=0))
            errs, _, _ = lint_errs(root)
            self.assertTrue(errs_for("RL-05", errs), errs)

    def test_mutation_rl05_version_with_both_slice_and_resolution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            edit_yaml(manifest_path(root), lambda m: m["resolutions"].append({"version": "2026-09-18.31", "in_slice": "s-31", "range": {"start": 70, "end": 80}, "sha256": "0" * 64, "reason": "A-01"}))
            errs, _, _ = lint_errs(root)
            self.assertTrue(any("exactly one manifest entry" in e for e in errs_for("RL-05", errs)), errs)

    def test_mutation_rl05_lowest_version_above_an_existing_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            edit_yaml(manifest_path(root), lambda m: m.update(lowest_version="2026-09-17.3"))
            errs, _, _ = lint_errs(root)
            self.assertTrue(errs_for("RL-05", errs) or errs_for("RL-06", errs), errs)

    def test_positive_rl06_chain(self):
        errs, _, notes = lint_errs(REPO)
        self.assertTrue(any("RL-06 previous_version chain exact; boundary at 2026-09-17.2" in n for n in notes), notes)

    def test_mutation_rl06_second_chain_start(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            edit_record(root, "2026-09-17.9", lambda fm: fm.update(previous_version=None))
            errs, _, _ = lint_errs(root)
            self.assertTrue(any("second chain start" in e for e in errs_for("RL-06", errs)), errs)

    def test_mutation_rl06_finalized_record_with_null(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            write_record(root, finalized_fm(prev=None), b"x")
            errs, _, _ = lint_errs(root)
            self.assertTrue(any("may not carry previous_version null" in e for e in errs_for("RL-06", errs)), errs)

    def test_mutation_rl06_delete_lowest_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            os.remove(os.path.join(root, RL.REGISTER_DIR_REL, "versions", "2026-09-17.2.md"))
            errs, _, _ = lint_errs(root)
            self.assertTrue(errs_for("RL-05", errs), errs)
            self.assertTrue(errs_for("RL-06", errs), errs)


# ======================================================================= anomalies

class Anomalies(unittest.TestCase):
    def test_positive_rl07_historical_doubled_label_and_shared_slices_green(self):
        errs, _, notes = lint_errs(REPO)
        self.assertEqual(errs_for("RL-07", errs) + errs_for("RL-08", errs), [])
        reg = RL.Register(REPO)
        ids = {a["id"]: a for a in reg.anomalies["anomalies"]}
        self.assertEqual(len(ids), 8)
        self.assertEqual({a["affects"] for a in ids.values() if a["kind"] == "doubled_label"}, {"2026-09-18.22", "2026-09-18.24"})
        self.assertEqual(len([a for a in ids.values() if a["kind"] == "no_slice_of_its_own"]), 6)
        self.assertTrue(all(a["frozen"] is True and a["permits"] == "RL-07" for a in ids.values()))

    def test_mutation_rl07_remove_dot6_anomaly(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            edit_yaml(os.path.join(root, RL.REGISTER_DIR_REL, "KNOWN-ANOMALIES.yaml"),
                      lambda d: d["anomalies"].remove(next(a for a in d["anomalies"] if a["affects"] == "2026-09-17.6")))
            errs, _, _ = lint_errs(root)
            self.assertTrue(any("2026-09-17.6" in e for e in errs_for("RL-07", errs) + errs_for("RL-08", errs)), errs)

    def test_mutation_rl07_new_record_with_doubled_label(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            write_record(root, finalized_fm(), b"At `.32` `.32` adds a row")
            RL.write_bytes(os.path.join(root, RL.REGISTER_REL), RF.pointer_line(RL.read_bytes(os.path.join(root, RL.REGISTER_REL)).decode(), "2026-09-18.32").encode())
            errs, _, _ = lint_errs(root)
            self.assertTrue(any("doubled version label" in e for e in errs_for("RL-07", errs)), errs)
            # RL-08: back-dating an anomaly entry for it is refused
            edit_yaml(os.path.join(root, RL.REGISTER_DIR_REL, "KNOWN-ANOMALIES.yaml"),
                      lambda d: d["anomalies"].append({"id": "A-09", "kind": "doubled_label", "affects": "2026-09-18.32", "observed": "x", "cited_by": "y", "permits": "RL-07", "frozen": True}))
            errs, _, _ = lint_errs(root)
            self.assertTrue(any("newer than the migration base" in e for e in errs_for("RL-08", errs)), errs)

    def test_mutation_rl08_frozen_false(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            edit_yaml(os.path.join(root, RL.REGISTER_DIR_REL, "KNOWN-ANOMALIES.yaml"), lambda d: d["anomalies"][0].update(frozen=False))
            errs, _, _ = lint_errs(root)
            self.assertTrue(errs_for("RL-08", errs), errs)

    def test_mutation_g03b_dot6_claims_a_slice_is_an_overlap(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            reg = RL.Register(root)
            s8 = reg.slices()["s-08"]
            r6 = reg.resolutions()["2026-09-17.6"]
            edit_yaml(manifest_path(root), lambda m: m["slices"].append({"id": "s-06", "version": "2026-09-17.6", "start": r6["range"]["start"], "end": r6["range"]["end"], "sha256": r6["sha256"]}))
            edit_record(root, "2026-09-17.6", lambda fm: (fm.pop("resolution"), fm.pop("shared_slice"), fm.pop("anomaly"), fm.update(slice="s-06")))
            errs, _, _ = lint_errs(root)
            self.assertTrue(errs_for("RL-01", errs), errs)


# ======================================================================= ledger, set, pointer

class LedgerSetPointer(unittest.TestCase):
    def test_positive_rl02_ledger_seed_complete_and_next_free_derived(self):
        """Live tree (whatever forward state it is in) AND the bootstrap state, separately."""
        reg = RL.Register(REPO)
        keys = {e["key"] for e in reg.ledger["allocations"]}
        rows = [k for k, _ in RL.table_data_rows(reg.regtxt)["correspondence"] if not re.fullmatch(r"\d{3}\+", k)]
        self.assertTrue(set(rows) <= keys, set(rows) - keys)
        self.assertEqual(reg.ledger["next_free"], RL.next_free_row_number(reg.regtxt))
        self.assertEqual(reg.ledger["next_free"], max(e["number"] for e in reg.ledger["allocations"] if isinstance(e["number"], int)) + 1)
        entries = {e["key"]: e for e in reg.ledger["allocations"]}
        for k in ("032-R1", "033", "034", "035", "031-R0"):
            self.assertIn(k, entries)
        # 032-R1 is in_flight (bootstrap) or landed at a finalized record that names it (forward)
        e = entries["032-R1"]
        if e["state"] == "landed":
            rec = reg.records.get(e["landed_version"])
            self.assertIsNotNone(rec, e)
            self.assertEqual(rec[0]["kind"], "finalized")
            self.assertIn("032-R1", rec[0]["allocations_consumed"])
        else:
            self.assertEqual(e["state"], "in_flight")
            self.assertIsNone(e["landed_version"])
        self.assertEqual(entries["031-R0"]["state"], "landed")
        self.assertTrue(all("landing_pr" not in x for x in reg.ledger["allocations"]))
        errs, _, _ = lint_errs(REPO)
        self.assertEqual(errs_for("RL-02", errs), [])
        # bootstrap state, constructed explicitly: exactly the seed
        with tempfile.TemporaryDirectory() as tmp:
            boot = RL.Register(bootstrap_tree(tmp))
            states = {x["key"]: x["state"] for x in boot.ledger["allocations"]}
            self.assertEqual(states["032-R1"], "in_flight")
            self.assertEqual({states["033"], states["034"], states["035"]}, {"reserved"})
            self.assertEqual(boot.ledger["next_free"], 36)
            self.assertEqual(RL.next_free_row_number(boot.regtxt), 36)
            self.assertTrue(all(x["landed_version"] is None for x in boot.ledger["allocations"] if x["state"] != "landed"))

    def test_positive_rl02_five_reserved_with_zero_rows_is_green(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            lp = os.path.join(root, RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml")
            def mut(d):
                for n in range(40, 45):
                    d["allocations"].append({"key": f"{n:03d}", "number": n, "identity": f"CORR-LEGO-PIPE-{n:03d}", "type": "CORR", "thread": "cluster", "actor": "x", "allocated_by": "James", "date": "2026-09-21", "state": "reserved", "landed_version": None, "basis": "test"})
                d["next_free"] = 45
            edit_yaml(lp, mut)
            regp = os.path.join(root, RL.REGISTER_REL)
            RL.write_bytes(regp, RL.read_bytes(regp).replace(b"| 036+ |", b"| 045+ |"))
            errs, _, _ = lint_errs(root)
            self.assertEqual(errs_for("RL-02", errs), [], errs)

    def test_mutation_rl02_duplicate_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            edit_yaml(os.path.join(root, RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml"), lambda d: d["allocations"].append(dict(d["allocations"][-1])))
            errs, _, _ = lint_errs(root)
            self.assertTrue(any("duplicate ledger key" in e for e in errs_for("RL-02", errs)), errs)

    def test_mutation_rl02_landed_without_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            edit_yaml(os.path.join(root, RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml"), lambda d: next(e for e in d["allocations"] if e["key"] == "033").update(state="landed"))
            errs, _, _ = lint_errs(root)
            self.assertTrue(any("033: landed but no correspondence-table row" in e for e in errs_for("RL-02", errs)), errs)

    def test_mutation_rl02_next_free_row_disagrees_with_ledger(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            regp = os.path.join(root, RL.REGISTER_REL)
            RL.write_bytes(regp, RL.read_bytes(regp).replace(b"| 036+ |", b"| 033+ |"))
            errs, _, _ = lint_errs(root)
            self.assertTrue(any("next-free row says 033+" in e for e in errs_for("RL-02", errs)), errs)

    def test_positive_rl03_set_complete(self):
        errs, _, notes = lint_errs(REPO)
        self.assertTrue(any("RL-03 authority set complete: 4" in n for n in notes), notes)

    def test_mutation_rl03_register_alone_is_not_the_register(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "docs", "correspondence"))
            shutil.copyfile(REGISTER, os.path.join(tmp, RL.REGISTER_REL))
            errs, _, _ = lint_errs(tmp)
            named = [e for e in errs_for("RL-03", errs)]
            self.assertEqual(len(named), 4, errs)
            for c in ("ALLOCATIONS.yaml", "KNOWN-ANOMALIES.yaml", "MIGRATION-*.yaml", "versions/"):
                self.assertTrue(any(c in e for e in named), c)
            code, out = run_tool("register_lint.py", "--repo", tmp)
            self.assertEqual(code, 1, out)

    def test_positive_rl04_pointer(self):
        # live tree: the pointer equals whatever the newest record is (bootstrap .31, or later)
        reg = RL.Register(REPO)
        newest = reg.sorted_versions()[-1]
        self.assertEqual(RL.register_version_line(reg.regtxt)[2], newest)
        errs, _, notes = lint_errs(REPO)
        self.assertTrue(any(f"RL-04 pointer {newest} equals the newest record" in n for n in notes), notes)
        # bootstrap state: the pointer is the migrated version
        with tempfile.TemporaryDirectory() as tmp:
            root = bootstrap_tree(tmp)
            _, _, notes = lint_errs(root)
            self.assertTrue(any("RL-04 pointer 2026-09-18.31 equals the newest record" in n for n in notes), notes)

    def test_mutation_rl04_pointer_behind_and_doubled(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            regp = os.path.join(root, RL.REGISTER_REL)
            RL.write_bytes(regp, RF.pointer_line(RL.read_bytes(regp).decode(), "2026-09-18.30").encode())
            errs, _, _ = lint_errs(root)
            self.assertTrue(any("pointer says 2026-09-18.30" in e for e in errs_for("RL-04", errs)), errs)
            txt = RL.read_bytes(regp).decode()
            RL.write_bytes(regp, (txt + "\n" + txt.split("\n")[6]).encode())
            errs, _, _ = lint_errs(root)
            self.assertTrue(any("exactly one version pointer" in e for e in errs_for("RL-04", errs)), errs)


# ======================================================================= immutability, hand-writing, rows, rule 18

class ImmutabilityRowsRule18(unittest.TestCase):
    def _prior(self, tmp, root):
        prior = os.path.join(tmp, "prior")
        shutil.copytree(os.path.join(root, RL.REGISTER_DIR_REL, "versions"), os.path.join(prior, "versions"))
        shutil.copyfile(os.path.join(root, RL.REGISTER_REL), os.path.join(prior, "REGISTER.md"))
        return prior

    def test_positive_rl09_against_a_prior_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            prior = self._prior(tmp, root)
            errs, _, notes = lint_errs(root, prior_tree=prior)
            self.assertEqual(errs, [], errs)
            self.assertTrue(any("RL-09 30 prior records byte-identical" in n for n in notes), notes)

    def test_mutation_rl09_edit_one_byte_and_regenerate_pointer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            prior = self._prior(tmp, root)
            p = os.path.join(root, RL.REGISTER_DIR_REL, "versions", "2026-09-18.20.md")
            data = RL.read_bytes(p)
            fm, body = RL.parse_record(data)
            body2 = body[:-1] + (b"!" if body[-1:] != b"!" else b"?")
            fm["note_sha256"] = sha(body2)
            RL.write_bytes(p, RL.record_bytes(fm, body2))
            # regenerate everything that could be regenerated to agree (031 outcome 10)
            edit_yaml(manifest_path(root), lambda m: next(s for s in m["slices"] if s["version"] == "2026-09-18.20").update(sha256=sha(body2)))
            errs, _, _ = lint_errs(root, prior_tree=prior)
            self.assertTrue(any("2026-09-18.20.md differs from the prior tree" in e for e in errs_for("RL-09", errs)), errs)

    def test_positive_rl11_shape(self):
        errs, _, _ = lint_errs(REPO)
        self.assertEqual(errs_for("RL-11", errs), [])

    def test_mutation_rl11_hand_written_finalized_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            fm = finalized_fm()
            del fm["finalized_from_main"]
            write_record(root, fm, b"hand-written")
            RL.write_bytes(os.path.join(root, RL.REGISTER_REL), RF.pointer_line(RL.read_bytes(os.path.join(root, RL.REGISTER_REL)).decode(), "2026-09-18.32").encode())
            errs, _, _ = lint_errs(root)
            self.assertTrue(any("hand-written" in e for e in errs_for("RL-11", errs)), errs)

    def test_positive_rl13_rl14_rows_identical_except_permitted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            base = reconstruct_base_register(root)
            # base rows: undo the permitted changes so the base looks like B's table
            reg = RL.Register(root)
            self.assertEqual(reg.manifest["table_baseline"], {"correspondence_rows": 36, "instruments_rows": 1,
                                                              "definition": reg.manifest["table_baseline"]["definition"],
                                                              "permitted_changes": RM.PERMITTED_TABLE_CHANGES})
            basep = os.path.join(tmp, "base-REGISTER.md")
            RL.write_bytes(basep, pre_migration_rows(base))
            errs, _, notes = lint_errs(root, migration_base=basep)
            self.assertEqual(errs_for("RL-13", errs) + errs_for("RL-14", errs), [], errs)
            self.assertTrue(any(n.startswith("RL-13 36 + 1 base data rows") for n in notes), notes)

    def test_mutation_rl13_change_one_character_in_a_historical_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            basep = os.path.join(tmp, "base-REGISTER.md")
            RL.write_bytes(basep, pre_migration_rows(reconstruct_base_register(root)))
            regp = os.path.join(root, RL.REGISTER_REL)
            RL.write_bytes(regp, RL.read_bytes(regp).replace(b"| 013 | `build-harness/CORR-LEGO-PIPE-013-reconciliation.md`", b"| 013 | `build-harness/CORR-LEGO-PIPE-013-reconciliation.MD`"))
            errs, _, _ = lint_errs(root, migration_base=basep)
            self.assertTrue(any("row 013 differs" in e for e in errs_for("RL-13", errs)), errs)

    def test_mutation_rl13_unpermitted_row_added(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            basep = os.path.join(tmp, "base-REGISTER.md")
            RL.write_bytes(basep, pre_migration_rows(reconstruct_base_register(root)))
            regp = os.path.join(root, RL.REGISTER_REL)
            RL.write_bytes(regp, RL.read_bytes(regp).replace(b"| 036+ |", b"| 033-R0 | x | REVIEW | x | x | drafted here |\n| 036+ |"))
            errs, _, _ = lint_errs(root, migration_base=basep)
            self.assertTrue(any("row 033-R0 added" in e for e in errs_for("RL-13", errs)), errs)

    def test_mutation_rl13_widened_whitelist_and_row_change_together(self):
        """CW-33-I03: the manifest's permitted_changes is bound to the ratified Q-13 set. Widening
        the whitelist AND changing the row in the same tree must fail — the width is not the
        author's to declare."""
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            basep = os.path.join(tmp, "base-REGISTER.md")
            RL.write_bytes(basep, pre_migration_rows(reconstruct_base_register(root)))
            regp = os.path.join(root, RL.REGISTER_REL)
            RL.write_bytes(regp, RL.read_bytes(regp).replace(b"| 013 | `build-harness/CORR-LEGO-PIPE-013-reconciliation.md`", b"| 013 | `build-harness/CORR-LEGO-PIPE-013-reconciliation.MD`"))
            # control: unwhitelisted change is red
            errs, _, _ = lint_errs(root, migration_base=basep)
            self.assertTrue(any("row 013 differs" in e for e in errs_for("RL-13", errs)), errs)
            # mutation: widen the whitelist in the same tree — must STILL be red, now naming the widening
            edit_yaml(manifest_path(root), lambda m: m["table_baseline"]["permitted_changes"]["rows_modified"].append("013"))
            errs, _, _ = lint_errs(root, migration_base=basep)
            rl13 = errs_for("RL-13", errs)
            self.assertTrue(any("rows_modified names ['013'], which Q-13 did not ratify" in e for e in rl13), rl13)
            self.assertTrue(any("row 013 differs" in e for e in rl13), "the widened entry must not be honoured: " + str(rl13))
            # and the same for an unratified addition
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            basep = os.path.join(tmp, "base-REGISTER.md")
            RL.write_bytes(basep, pre_migration_rows(reconstruct_base_register(root)))
            regp = os.path.join(root, RL.REGISTER_REL)
            RL.write_bytes(regp, RL.read_bytes(regp).replace(b"| 036+ |", b"| 033-R0 | x | REVIEW | x | x | drafted here |\n| 036+ |"))
            edit_yaml(manifest_path(root), lambda m: m["table_baseline"]["permitted_changes"]["rows_added"].append("033-R0"))
            errs, _, _ = lint_errs(root, migration_base=basep)
            rl13 = errs_for("RL-13", errs)
            self.assertTrue(any("rows_added names ['033-R0'], which Q-13 did not ratify" in e for e in rl13), rl13)
            self.assertTrue(any("row 033-R0 added" in e for e in rl13), rl13)
            # an unknown key in permitted_changes is also refused
            edit_yaml(manifest_path(root), lambda m: m["table_baseline"]["permitted_changes"].update(rows_deleted=["029-R0"]))
            errs, _, _ = lint_errs(root, migration_base=basep)
            self.assertTrue(any("unratified keys ['rows_deleted']" in e for e in errs_for("RL-13", errs)), errs)

    def test_mutation_rl13_narrowed_whitelist_is_rejected(self):
        """H1-LEAD-02: the ratified Q-13 set is required, not merely an upper bound. (a) Remove
        032-R1 from both the table and the manifest; (b) restore 030-R0's base cell and drop it
        from the manifest; (c) next_free_row false. Each is an RL-13 error."""
        def fresh(tmp):
            root = copy_tree(tmp)
            basep = os.path.join(tmp, "base-REGISTER.md")
            RL.write_bytes(basep, pre_migration_rows(reconstruct_base_register(root)))
            return root, basep
        # (a) narrowing rows_added, table change removed too
        with tempfile.TemporaryDirectory() as tmp:
            root, basep = fresh(tmp)
            regp = os.path.join(root, RL.REGISTER_REL)
            lines = RL.read_bytes(regp).decode().split("\n")
            kept = [l for l in lines if not l.startswith("| 032-R1 |")]
            self.assertEqual(len(lines) - len(kept), 1, "fixture: exactly one 032-R1 row expected")
            RL.write_bytes(regp, "\n".join(kept).encode())
            edit_yaml(manifest_path(root), lambda m: m["table_baseline"]["permitted_changes"].update(rows_added=[]))
            errs, _, _ = lint_errs(root, migration_base=basep)
            rl13 = errs_for("RL-13", errs)
            self.assertTrue(any("rows_added omits ['032-R1'], which Q-13 ratified" in e for e in rl13), rl13)
            self.assertTrue(any("ratified addition 032-R1 is missing at HEAD" in e for e in rl13), rl13)
        # (b) restore a ratified modified row to its base text and drop it from the manifest
        with tempfile.TemporaryDirectory() as tmp:
            root, basep = fresh(tmp)
            base_rows = dict(RL.table_data_rows(RL.read_bytes(basep).decode())["correspondence"])
            regp = os.path.join(root, RL.REGISTER_REL)
            txt = RL.read_bytes(regp).decode()
            head_rows = dict(RL.table_data_rows(txt)["correspondence"])
            self.assertNotEqual(head_rows["030-R0"], base_rows["030-R0"], "fixture: 030-R0 must differ at HEAD")
            RL.write_bytes(regp, txt.replace(head_rows["030-R0"], base_rows["030-R0"], 1).encode())
            edit_yaml(manifest_path(root), lambda m: m["table_baseline"]["permitted_changes"].update(rows_modified=["031-R0"]))
            errs, _, _ = lint_errs(root, migration_base=basep)
            rl13 = errs_for("RL-13", errs)
            self.assertTrue(any("rows_modified omits ['030-R0'], which Q-13 ratified" in e for e in rl13), rl13)
            self.assertTrue(any("ratified modification 030-R0 is byte-identical to base at HEAD" in e for e in rl13), rl13)
        # (c) next_free_row narrowed to false; and the manifest-only narrowing with the table intact
        with tempfile.TemporaryDirectory() as tmp:
            root, basep = fresh(tmp)
            edit_yaml(manifest_path(root), lambda m: m["table_baseline"]["permitted_changes"].update(next_free_row=False))
            errs, _, _ = lint_errs(root, migration_base=basep)
            self.assertTrue(any("next_free_row must be exactly True" in e for e in errs_for("RL-13", errs)), errs)
        with tempfile.TemporaryDirectory() as tmp:
            root, basep = fresh(tmp)
            edit_yaml(manifest_path(root), lambda m: m["table_baseline"]["permitted_changes"].update(rows_modified=["030-R0"]))
            errs, _, _ = lint_errs(root, migration_base=basep)
            self.assertTrue(any("rows_modified omits ['031-R0']" in e for e in errs_for("RL-13", errs)), errs)
            # exact set restored → green again (control)
            edit_yaml(manifest_path(root), lambda m: m["table_baseline"]["permitted_changes"].update(rows_modified=["030-R0", "031-R0"]))
            errs, _, _ = lint_errs(root, migration_base=basep)
            self.assertEqual(errs_for("RL-13", errs), [], errs)

    def test_mutation_rl14_instruments_row_changed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            basep = os.path.join(tmp, "base-REGISTER.md")
            RL.write_bytes(basep, pre_migration_rows(reconstruct_base_register(root)))
            regp = os.path.join(root, RL.REGISTER_REL)
            RL.write_bytes(regp, RL.read_bytes(regp).replace(b"| H-01 | R1 | as-committed |", b"| H-01 | R1 | as-exported |"))
            errs, _, _ = lint_errs(root, migration_base=basep)
            self.assertTrue(errs_for("RL-14", errs), errs)

    def test_row_definition_excludes_header_and_separator(self):
        fixture = "| Number | Document | Type |\n|---|---|---|\n| 001-R0 | a | b |\n| 002+ | next | |\n\n## Instruments\n\n| Instrument | Revision |\n|---|---|\n| H-01 | R1 |\n"
        rows = RL.table_data_rows(fixture)
        self.assertEqual([k for k, _ in rows["correspondence"]], ["001-R0", "002+"])
        self.assertEqual([k for k, _ in rows["instruments"]], ["H-01"])
        reg = RL.Register(REPO)
        head = RL.table_data_rows(reconstruct_base_register(REPO).decode("utf-8"))
        self.assertEqual((len(head["correspondence"]), len(head["instruments"])), (37, 1))  # HEAD: B's 36 + the 032-R1 row
        base = RL.table_data_rows(pre_migration_rows(reconstruct_base_register(REPO)).decode("utf-8"))
        self.assertEqual((len(base["correspondence"]), len(base["instruments"])), (36, 1))  # RR-32-07: 37 data rows at B

    def test_positive_rl18_sentinel_present_and_ratchet_holds(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            prior = self._prior(tmp, root)
            errs, _, notes = lint_errs(root, prior_tree=prior)
            self.assertEqual(errs_for("RL-18", errs), [])
            self.assertTrue(any("sentinel present" in n for n in notes), notes)
            code, out = run_tool("register_lint.py", "rule18", "--repo", root)
            self.assertEqual((code, out.strip()), (0, "present"))

    def test_rl18_absent_sentinel_is_report_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            regp = os.path.join(root, RL.REGISTER_REL)
            txt = RL.read_bytes(regp).decode()
            txt = "\n".join(l for l in txt.split("\n") if not l.startswith("18. **Merge-method enforcement:**"))
            RL.write_bytes(regp, txt.encode())
            code, out = run_tool("register_lint.py", "rule18", "--repo", root)
            self.assertEqual((code, out.strip()), (0, "absent"))
            errs, _, notes = lint_errs(root)  # no prior tree: no ratchet, just report
            self.assertEqual(errs_for("RL-18", errs), [])
            self.assertTrue(any("report-only" in n for n in notes), notes)

    def test_mutation_rl18_ratchet(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            prior = self._prior(tmp, root)
            regp = os.path.join(root, RL.REGISTER_REL)
            original = RL.read_bytes(regp).decode()
            rule = next(l for l in original.split("\n") if l.startswith("18. **Merge-method enforcement:**"))
            # delete → red
            RL.write_bytes(regp, original.replace(rule + "\n", "").encode())
            errs, _, _ = lint_errs(root, prior_tree=prior)
            self.assertTrue(errs_for("RL-18", errs), errs)
            # edit one word → red
            RL.write_bytes(regp, original.replace("accepts only merge commits", "accepts merge commits").encode())
            errs, _, _ = lint_errs(root, prior_tree=prior)
            self.assertTrue(errs_for("RL-18", errs), errs)
            # delete + numbered successor → green
            RL.write_bytes(regp, original.replace(rule + "\n", "19. **Supersedes Rule 18:** merge-method enforcement withdrawn, ratified 2099-01-01.\n").encode())
            errs, _, _ = lint_errs(root, prior_tree=prior)
            self.assertEqual(errs_for("RL-18", errs), [], errs)
            # same deletion with no successor anywhere → red (already covered above; assert again explicitly)
            RL.write_bytes(regp, original.replace(rule + "\n", "").encode())
            errs, _, _ = lint_errs(root, prior_tree=prior)
            self.assertTrue(any("ratchet" in e for e in errs_for("RL-18", errs)), errs)


# ======================================================================= migration tool

class WorkflowShape(unittest.TestCase):
    """The evidence pipeline's two sequencing properties (CW-33-I06, CW-33-I02), read from the
    workflow file so a later edit that drops them fails here rather than in a red CI job."""

    def steps(self):
        wf = yaml.safe_load(RL.read_bytes(os.path.join(REPO, ".github", "workflows", "register-lint.yml")).decode("utf-8"))
        return wf["jobs"]["register-lint"]["steps"]

    def test_settings_read_runs_even_when_the_finalization_check_fails(self):
        steps = self.steps()
        settings = [st for st in steps if st.get("name", "").startswith("Settings read")]
        self.assertEqual(len(settings), 1, [st.get("name") for st in steps])
        self.assertEqual(str(settings[0].get("if")).strip(), "always()", settings[0])
        names = [st.get("name", "") for st in steps]
        self.assertLess([i for i, n in enumerate(names) if n.startswith("register_finalize --check")][0],
                        names.index(settings[0]["name"]), "the finalization check precedes the settings read; if: always() is what keeps AO-14 reachable")

    def test_every_finalizer_invocation_names_its_target(self):
        for st in self.steps():
            run = st.get("run") or ""
            for line in run.split("\n"):
                if "register_finalize.py" in line:
                    self.assertIn("--repo", line, line)


class SettingsEvaluation(unittest.TestCase):
    """AO-14's two-state verdict is computed only from validated booleans (H1-LEAD-01). The
    ordinary Actions token returns null for the three merge fields; that must read as
    UNVERIFIED, never as an enforcing success, and must not fail the step."""
    COMPLIANT = {"allow_merge_commit": True, "allow_squash_merge": False, "allow_rebase_merge": False}
    PERMISSIVE = {"allow_merge_commit": True, "allow_squash_merge": True, "allow_rebase_merge": True}
    NULLS = {"allow_merge_commit": None, "allow_squash_merge": None, "allow_rebase_merge": None}
    PROTECTION_403 = "__API_FAILURE__"

    def test_sentinel_present_compliant_is_enforcing_success(self):
        status, lines, code = RL.evaluate_settings(True, self.COMPLIANT, {"required_linear_history": False, "required_checks": []})
        self.assertEqual((status, code), ("enforcing", 0))
        self.assertTrue(any(l.startswith("OK: settings step enforcing") for l in lines), lines)
        self.assertTrue(any("reported, not evaluated" in l for l in lines), lines)

    def test_sentinel_present_permissive_or_merge_commits_off_fails(self):
        for st in (self.PERMISSIVE,
                   dict(self.COMPLIANT, allow_squash_merge=True),
                   dict(self.COMPLIANT, allow_rebase_merge=True),
                   dict(self.COMPLIANT, allow_merge_commit=False)):
            status, lines, code = RL.evaluate_settings(True, st, self.PROTECTION_403)
            self.assertEqual((status, code), ("fail", 1), st)
            self.assertTrue(any(l.startswith("::error::Rule 18 is ratified but") for l in lines), lines)
            self.assertFalse(any("enforcing" in l and l.startswith("OK") for l in lines), lines)

    def test_sentinel_absent_is_report_only_whatever_the_booleans(self):
        for st in (self.COMPLIANT, self.PERMISSIVE):
            status, lines, code = RL.evaluate_settings(False, st, self.PROTECTION_403)
            self.assertEqual((status, code), ("report-only", 0), st)
            self.assertTrue(any("report-only" in l for l in lines), lines)

    def test_null_missing_malformed_and_api_failure_are_unverified_never_enforcing(self):
        cases = {
            "null (the H1 CI log)": self.NULLS,
            "one null": dict(self.COMPLIANT, allow_squash_merge=None),
            "missing key": {"allow_merge_commit": True, "allow_rebase_merge": False},
            "empty dict": {},
            "string instead of bool": dict(self.COMPLIANT, allow_squash_merge="false"),
            "int instead of bool": dict(self.COMPLIANT, allow_rebase_merge=0),
            "malformed (list)": [True, False, False],
            "malformed (string)": "not json at all",
            "API failure marker": "__API_FAILURE__",
            "None (no read)": None,
        }
        for name, st in cases.items():
            for sentinel in (True, False):
                status, lines, code = RL.evaluate_settings(sentinel, st, self.PROTECTION_403)
                self.assertEqual((status, code), ("unverified", 0), f"{name} / sentinel={sentinel}: {lines}")
                self.assertTrue(any(RL.UNVERIFIED in l for l in lines), lines)
                self.assertTrue(any("NOT AO-14 enforcement evidence" in l for l in lines), lines)
                self.assertFalse(any(l.startswith("OK: settings step enforcing") for l in lines), f"{name}: fail-open: {lines}")
                self.assertFalse(any(l.startswith("::error::") for l in lines), f"{name}: unverified must not fail the step: {lines}")
                self.assertTrue(any("branch protection: unavailable to this token" in l for l in lines), lines)

    def test_cli_round_trip_matches_the_function(self):
        import json
        for sentinel, st, prot, want_status, want_code in (
            ("present", json.dumps(self.COMPLIANT), json.dumps({"required_linear_history": False}), "enforcing", 0),
            ("present", json.dumps(self.PERMISSIVE), "__API_FAILURE__", "fail", 1),
            ("present", json.dumps(self.NULLS), "__API_FAILURE__", "unverified", 0),
            ("absent", json.dumps(self.PERMISSIVE), "__API_FAILURE__", "report-only", 0),
            ("present", "__API_FAILURE__", "__API_FAILURE__", "unverified", 0),
            ("present", "{not json", "__API_FAILURE__", "unverified", 0),
        ):
            code, out = run_tool("register_lint.py", "settings-eval", "--sentinel", sentinel, "--settings", st, "--protection", prot)
            self.assertEqual(code, want_code, out)
            self.assertIn(f"settings-eval: {want_status}", out)
        code, out = run_tool("register_lint.py", "settings-eval", "--sentinel", "maybe", "--settings", "{}")
        self.assertEqual(code, 2, out)

    def test_workflow_uses_the_validated_evaluator_not_shell_comparison(self):
        wf = RL.read_bytes(os.path.join(REPO, ".github", "workflows", "register-lint.yml")).decode("utf-8")
        step = wf[wf.index("Settings read"):]
        self.assertIn("register_lint.py settings-eval", step)
        self.assertNotIn('[ "$squash" = "True" ]', step, "the H1 shell comparison fails open on null")
        self.assertIn("__API_FAILURE__", step)
        self.assertNotIn("secrets.", step, "no privileged repository secret is used or requested")


class MigrationTool(unittest.TestCase):
    def test_idempotent_and_reproducible_offline(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = reconstruct_base_register(REPO)
            # the committed REGISTER.md rows differ from B's (permitted changes); the manifest's
            # partition, records and anomalies must nevertheless be reproduced byte-exact
            m1 = RM.migrate(src, RL.Register(REPO).manifest["base_commit"], tmp)
            produced = os.path.join(tmp, RL.REGISTER_DIR_REL)
            for name in os.listdir(os.path.join(produced, "versions")):
                self.assertEqual(RL.read_bytes(os.path.join(produced, "versions", name)), RL.read_bytes(os.path.join(REG_DIR, "versions", name)), name)
            self.assertEqual(RL.read_bytes(os.path.join(produced, "KNOWN-ANOMALIES.yaml")), RL.read_bytes(os.path.join(REG_DIR, "KNOWN-ANOMALIES.yaml")))
            committed = RL.Register(REPO).manifest
            for k in ("line_sha256", "line_bytes", "slices", "resolutions", "seams", "preamble", "lowest_version", "version_count"):
                self.assertEqual(m1[k], committed[k], k)
            # idempotence: a second run on the migrated file is a no-op
            msg = RM.rewrite_register_in_place(tmp, src, RL.read_bytes(os.path.join(tmp, RL.REGISTER_REL)))
            self.assertIn("no-op", msg)
            snapshot = {n: RL.read_bytes(os.path.join(produced, "versions", n)) for n in os.listdir(os.path.join(produced, "versions"))}
            RM.migrate(src, committed["base_commit"], tmp)
            self.assertEqual(snapshot, {n: RL.read_bytes(os.path.join(produced, "versions", n)) for n in os.listdir(os.path.join(produced, "versions"))})

    def test_migrate_refuses_a_moved_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = copy_tree(tmp)
            regp = os.path.join(root, RL.REGISTER_REL)
            RL.write_bytes(regp, RL.read_bytes(regp).replace(b"**Register version: 2026-09-18.31** \xe2\x80\x94 one register version", b"**Register version: 2026-09-18.31** \xe2\x80\x94 something else"))
            with self.assertRaises(RuntimeError):
                RM.rewrite_register_in_place(root, reconstruct_base_register(REPO), RL.read_bytes(regp).replace(b"something else", b"one register version"))

    def test_fixed_emitter_round_trips_version_strings(self):
        doc = {"register_version": "2026-09-18.31", "previous_version": None, "n": 2026, "d": "2026-09-18"}
        out = RL.dump_yaml(doc)
        back = yaml.safe_load(out)
        self.assertEqual(back["register_version"], "2026-09-18.31")
        self.assertIsNone(back["previous_version"])
        self.assertEqual(back["d"], "2026-09-18", "dates are quoted by the emitter, never parsed back as date objects")
        self.assertEqual(RL.dump_yaml(back), out)

    def _produced_with_committed_manifest(self, tmp):
        """A fresh migrator run over the reconstructed base, with the committed (immutable)
        manifest overlaid — the offline stand-in for `--base B`, whose whole-file source fields
        only the --with-git case can recompute."""
        produced = os.path.join(tmp, "produced")
        RM.migrate(reconstruct_base_register(REPO), RL.Register(REPO).manifest["base_commit"], produced)
        shutil.copyfile(RL.Register(REPO).manifest_paths[0], manifest_path(produced))
        return produced

    def test_reproduction_accepts_forward_state_and_detects_migration_artifact_corruption(self):
        """F-08/H4: the reproduction proof is about the migration's own artifacts. Legitimate
        forward state (a finalized record, an advanced pointer, a landed allocation) is not a
        difference; corruption of anything the migration owns, or an illegitimate ledger
        movement, still is."""
        manifest = RL.Register(REPO).manifest
        with tempfile.TemporaryDirectory() as tmp:
            produced = self._produced_with_committed_manifest(tmp)
            # (a) the bootstrap tree itself: empty
            boot = bootstrap_tree(tmp, name="boot")
            self.assertEqual(RM.reproduction_diffs(produced, boot, manifest), [])
            # (b) legitimate forward state, constructed the way the finalizer would produce it
            fwd = bootstrap_tree(tmp, name="fwd")
            body = b"forward landing"
            write_record(fwd, {"register_version": "2026-09-18.32", "previous_version": "2026-09-18.31", "kind": "finalized",
                               "finalized_from_main": "b" * 40, "affected_memos": ["HANDOFF-LEGO-PIPE-032-R1"],
                               "allocations_consumed": ["032-R1"], "note_sha256": sha(body)}, body)
            regp = os.path.join(fwd, RL.REGISTER_REL)
            RL.write_bytes(regp, RF.pointer_line(RL.read_bytes(regp).decode(), "2026-09-18.32").encode())
            lp = os.path.join(fwd, RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml")
            edit_yaml(lp, lambda d: [e.update(state="landed", landed_version="2026-09-18.32") for e in d["allocations"] if e["key"] == "032-R1"])
            self.assertEqual(RM.reproduction_diffs(produced, fwd, manifest), [])
            # plus withdrawals of unlanded allocations (CDX-34-H4-01): reserved→withdrawn (034),
            # in_flight→withdrawn (033 after moving in_flight below is exercised separately)
            edit_yaml(lp, lambda d: [e.update(state="withdrawn") for e in d["allocations"] if e["key"] == "034"])
            self.assertEqual(RM.reproduction_diffs(produced, fwd, manifest), [])
            # plus a later reservation appended at/above next_free, and 033 moved reserved→in_flight
            edit_yaml(lp, lambda d: (d["allocations"].append({"key": "036-R0", "number": 36, "identity": "CORR-LEGO-PIPE-036", "type": "CORR",
                                                              "thread": "cluster", "actor": "x", "allocated_by": "James", "date": "2026-09-22",
                                                              "state": "reserved", "landed_version": None, "basis": "later"}),
                                     [e.update(state="in_flight") for e in d["allocations"] if e["key"] == "033"], d.update(next_free=37)))
            self.assertEqual(RM.reproduction_diffs(produced, fwd, manifest), [])
            # (c) negative controls — each on a fresh copy of the forward tree
            def mutated(fn):
                root = os.path.join(tmp, f"m{len(os.listdir(tmp))}")
                shutil.copytree(fwd, root)
                fn(root)
                return RM.reproduction_diffs(produced, root, manifest)
            def flip_record(root):
                edit_record(root, "2026-09-18.13", body=b"tampered")
            def seeded_field(root):
                edit_yaml(os.path.join(root, RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml"), lambda d: [e.update(allocated_by="nobody") for e in d["allocations"] if e["key"] == "031-R0"])
            def backwards(root):
                edit_yaml(os.path.join(root, RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml"), lambda d: [e.update(state="reserved", landed_version=None) for e in d["allocations"] if e["key"] == "031-R0"])
            def dangling(root):
                edit_yaml(os.path.join(root, RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml"), lambda d: [e.update(landed_version="2026-09-18.40") for e in d["allocations"] if e["key"] == "032-R1"])
            def not_named(root):
                edit_record(root, "2026-09-18.32", fn_fm=lambda fm: fm.update(allocations_consumed=[]))
            def removed(root):
                edit_yaml(os.path.join(root, RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml"), lambda d: d.update(allocations=[e for e in d["allocations"] if e["key"] != "013"]))
            def low_number(root):
                edit_yaml(os.path.join(root, RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml"), lambda d: d["allocations"].append(dict(d["allocations"][-1], key="009-X", number=9)))
            def manifest_byte(root):
                mp = manifest_path(root); RL.write_bytes(mp, RL.read_bytes(mp).replace(b"line_bytes: 39268", b"line_bytes: 39269"))
            def anomalies(root):
                ap = os.path.join(root, RL.REGISTER_DIR_REL, "KNOWN-ANOMALIES.yaml"); RL.write_bytes(ap, RL.read_bytes(ap) + b"\n# tampered\n")
            def pointer_behind(root):
                rp = os.path.join(root, RL.REGISTER_REL); RL.write_bytes(rp, RF.pointer_line(RL.read_bytes(rp).decode(), "2026-09-18.30").encode())
            def pointer_template(root):
                rp = os.path.join(root, RL.REGISTER_REL); RL.write_bytes(rp, RL.read_bytes(rp).replace(b"never claimed on a branch", b"claimed on a branch"))
            def migrated_record_deleted(root):
                os.remove(os.path.join(root, RL.REGISTER_DIR_REL, "versions", "2026-09-18.20.md"))
            def withdrawn_with_landed_version(root):
                edit_yaml(os.path.join(root, RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml"), lambda d: [e.update(state="withdrawn", landed_version="2026-09-18.32") for e in d["allocations"] if e["key"] == "035"])
            def landed_to_withdrawn(root):
                edit_yaml(os.path.join(root, RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml"), lambda d: [e.update(state="withdrawn", landed_version=None) for e in d["allocations"] if e["key"] == "031-R0"])
            def in_flight_to_withdrawn_ok_then_revived(root):
                # 033 was moved reserved→in_flight on the forward tree above; withdrawing it now
                # is the legal in_flight→withdrawn edge. Terminality of withdrawn (no revival) is
                # proved exhaustively in test_ledger_transition_graph_is_the_ratified_four_state_lifecycle.
                edit_yaml(os.path.join(root, RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml"), lambda d: [e.update(state="withdrawn", landed_version=None) for e in d["allocations"] if e["key"] == "033"])
            def stray_migrated_record(root):
                write_record(root, {"register_version": "2026-09-18.33", "previous_version": "2026-09-18.32", "kind": "migrated", "slice": "s-31", "note_sha256": sha(b"x")}, b"x")
            for name, fn, needle in (
                ("record byte", flip_record, "differs: register/versions/2026-09-18.13.md"),
                ("seeded field", seeded_field, "031-R0.allocated_by changed from seed"),
                ("backwards", backwards, "landed → reserved, which is not allowed (terminal"),
                ("dangling landed_version", dangling, "no finalized record with that version"),
                ("record does not name the key", not_named, "allocations_consumed does not name it"),
                ("seeded entry removed", removed, "seeded entry 013 is missing"),
                ("new entry below next_free", low_number, "below the seeded next_free"),
                ("manifest byte", manifest_byte, "differs: register/MIGRATION-"),
                ("anomalies", anomalies, "differs: register/KNOWN-ANOMALIES.yaml"),
                ("pointer behind", pointer_behind, "is behind the migrated version"),
                ("pointer template", pointer_template, "pointer text differs from the migrated template"),
                ("migrated record deleted", migrated_record_deleted, "missing in committed tree: register/versions/2026-09-18.20.md"),
                ("stray migrated record", stray_migrated_record, "extra in committed tree: register/versions/2026-09-18.33.md"),
                ("withdrawn with landed_version", withdrawn_with_landed_version, "withdrawn but carries landed_version"),
                ("landed → withdrawn", landed_to_withdrawn, "landed → withdrawn, which is not allowed (terminal"),
            ):
                diffs = mutated(fn)
                self.assertTrue(any(needle in d for d in diffs), f"{name}: expected a difference containing {needle!r}, got {diffs}")
            # in_flight → withdrawn is accepted on the forward tree (033 was moved to in_flight above)
            self.assertEqual(mutated(in_flight_to_withdrawn_ok_then_revived), [])

    def test_ledger_transition_graph_is_the_ratified_four_state_lifecycle(self):
        """CDX-34-H4-01: the states are reserved | in_flight | landed | withdrawn (R0 §3, the
        ledger, register_lint.LEDGER_STATES); transitions are an explicit graph, landed and
        withdrawn terminal. Asserted against the graph itself AND exhaustively against
        ledger_forward_diffs over every ordered pair."""
        self.assertEqual(RM.LEDGER_STATES, RL.LEDGER_STATES)
        self.assertEqual(set(RM.ALLOWED_TRANSITIONS), set(RM.LEDGER_STATES))
        self.assertEqual(RM.ALLOWED_TRANSITIONS, {
            "reserved": {"reserved", "in_flight", "landed", "withdrawn"},
            "in_flight": {"in_flight", "landed", "withdrawn"},
            "landed": {"landed"},
            "withdrawn": {"withdrawn"},
        })
        for terminal in ("landed", "withdrawn"):
            self.assertEqual(RM.ALLOWED_TRANSITIONS[terminal], {terminal}, f"{terminal} must be terminal")
        # exhaustive pairwise check through the comparison function, with a finalized record
        # available so that legal landings are justified
        with tempfile.TemporaryDirectory() as tmp:
            vdir = os.path.join(tmp, "versions"); os.makedirs(vdir)
            RL.write_bytes(os.path.join(vdir, "2026-09-18.32.md"), RL.record_bytes(
                {"register_version": "2026-09-18.32", "previous_version": "2026-09-18.31", "kind": "finalized",
                 "finalized_from_main": "b" * 40, "affected_memos": ["x"], "allocations_consumed": ["K"], "note_sha256": sha(b"n")}, b"n"))
            def entry(state, lv=None):
                return {"key": "K", "number": 50, "identity": "CORR-LEGO-PIPE-050", "type": "CORR", "thread": "cluster",
                        "actor": "a", "allocated_by": "James", "date": "2026-09-21", "state": state, "landed_version": lv, "basis": "t"}
            def diffs(seed_state, committed_state, lv=None, seed_lv=None):
                seed = {"schema": "s", "next_free": 51, "allocations": [entry(seed_state, seed_lv)]}
                com = {"schema": "s", "next_free": 51, "allocations": [entry(committed_state, lv)]}
                return RM.ledger_forward_diffs(seed, com, vdir)
            for src in RM.LEDGER_STATES:
                for dst in RM.LEDGER_STATES:
                    lv = "2026-09-18.32" if dst == "landed" else None
                    seed_lv = "2026-09-18.32" if src == "landed" else None
                    d = diffs(src, dst, lv=lv, seed_lv=seed_lv)
                    if dst in RM.ALLOWED_TRANSITIONS[src]:
                        self.assertEqual(d, [], f"{src} → {dst} should be accepted: {d}")
                    else:
                        self.assertTrue(any("is not allowed" in x for x in d), f"{src} → {dst} should be rejected: {d}")
            # the named cases the review asked for
            self.assertEqual(diffs("reserved", "withdrawn"), [])                                   # 1
            self.assertEqual(diffs("in_flight", "withdrawn"), [])                                  # 2
            self.assertTrue(any("withdrawn but carries landed_version" in x for x in diffs("in_flight", "withdrawn", lv="2026-09-18.32")))  # 3
            self.assertTrue(any("landed → withdrawn, which is not allowed (terminal" in x for x in diffs("landed", "withdrawn", seed_lv="2026-09-18.32")))  # 4
            for dst in ("reserved", "in_flight", "landed"):                                        # 5
                lv = "2026-09-18.32" if dst == "landed" else None
                self.assertTrue(any("withdrawn → " + dst in x and "terminal" in x for x in diffs("withdrawn", dst, lv=lv)), dst)
            # landing evidence is still required across both landing edges
            for src in ("reserved", "in_flight"):
                self.assertTrue(any("no finalized record" in x for x in diffs(src, "landed", lv="2026-09-18.99")), src)
                self.assertTrue(any("landed at" in x and "no finalized record" in x or "does not name it" in x for x in diffs(src, "landed", lv="2026-09-18.99")), src)
            # a landed record that does not name the key is still rejected
            RL.write_bytes(os.path.join(vdir, "2026-09-18.33.md"), RL.record_bytes(
                {"register_version": "2026-09-18.33", "previous_version": "2026-09-18.32", "kind": "finalized",
                 "finalized_from_main": "c" * 40, "affected_memos": ["x"], "allocations_consumed": ["OTHER"], "note_sha256": sha(b"m")}, b"m"))
            self.assertTrue(any("does not name it" in x for x in diffs("in_flight", "landed", lv="2026-09-18.33")))

    @unittest.skipUnless(WITH_GIT, "--with-git: reads the manifest's base commit from the project's .git")
    def test_reproduction_from_the_base_commit_is_an_empty_diff(self):
        base = RL.Register(REPO).manifest["base_commit"]
        self.assertEqual(sha(RL.git_bytes(REPO, "show", f"{base}:docs/correspondence/REGISTER.md")), RL.Register(REPO).manifest["source_sha256"])
        code, out = run_tool("register_migrate.py", "--base", base, "--check")
        self.assertEqual(code, 0, out)
        self.assertIn("0 differences", out)
        # negative control against a real base commit, in a temporary repository: a landed
        # forward state is accepted, then one migrated record byte flipped is a difference
        with tempfile.TemporaryDirectory() as tmp:
            T = TempRepo(tmp)
            a = T.clone("a")
            code, out = run_tool("register_migrate.py", "--repo", a, "--base", T.base, "--check")
            self.assertEqual(code, 0, out)
            T.reserve(a, "050-R0", 50); T.add_row(a, "050-R0", "x"); T.pending(a, "050.md", "CORR-LEGO-PIPE-050-R0", "050-R0", b"fwd")
            T.commit(a, "memo 050")
            self.assertEqual(T.finalize(a)[0], 0)
            code, out = run_tool("register_migrate.py", "--repo", a, "--base", T.base, "--check")
            self.assertEqual(code, 0, out + " — a legitimate finalized landing must not be a reproduction difference")
            edit_record(a, "2026-09-18.19", body=b"tampered")
            code, out = run_tool("register_migrate.py", "--repo", a, "--base", T.base, "--check")
            self.assertEqual(code, 1, out)
            self.assertIn("differs: register/versions/2026-09-18.19.md", out)


# ======================================================================= corpus differential (G-12)

class CorpusDifferential(unittest.TestCase):
    def memos(self):
        out = []
        for root, _, files in os.walk(CORR):
            if os.path.basename(root) in ("register", "versions", "pending", "attachments"):
                continue
            for f in files:
                if f.endswith(".md") and f != "REGISTER.md" and not f.startswith("HANDOFF-LEGO-PIPE-032-"):
                    out.append(os.path.join(root, f))
        return sorted(out)

    # G-12 / CW-33-I01: the register cross-check in memo_preflight.py (`key in regtxt` … first
    # line containing the key) was distorted at B by the 39 KB version line: for memos the line
    # mentioned, the WARN "NNN-Rn already listed in register (expected on re-run)" was
    # suppressed (first hit inside the version line, whose remainder never says "superseded");
    # for 011-R0/011-R1, whose rows DO say "superseded by R1/R2", the first hit was ALSO the
    # version line, whose remainder lacks the word, so the WARN fired spuriously. With the line
    # migrated the first hit is the row itself: the WARN correctly appears for 13 memos and
    # correctly disappears for 2. Both directions are asserted by exact membership; a future
    # change that removed a WARN it should not, or added one, moves a memo between these sets
    # and fails here. memo_preflight.py itself is out of scope (R0 §11) and is not changed.
    WARN = "already listed in register (expected on re-run)"
    EXPECTED_GAINED = (
        "CORR-LEGO-PIPE-016-correspondence-alignment-chatgpt.md",
        "CORR-LEGO-PIPE-017-correspondence-alignment-claude.md",
        "CORR-LEGO-PIPE-027-R0-chatgpt-design-handoff-review-debrief.md",
        "CORR-LEGO-PIPE-028-R0-debrief-design-handoff-schema-round.md",
        "CORR-LEGO-PIPE-029-R0-design-handoff-delivery-debrief.md",
        "CORR-LEGO-PIPE-030-R0-register-shape-cleanup.md",
        "CORR-LEGO-PIPE-031-R0-register-concurrency-peer-memo.md",
        "HANDOFF-LEGO-PIPE-023-R2-drafting-table-on-fixtures-and-the-program.md",
        "HANDOFF-LEGO-PIPE-024-R1-design-package-protocol.md",
        "REVIEW-LEGO-PIPE-025-R1-review-of-design-package-protocol.md",
        "REVIEW-LEGO-PIPE-026-R0-chatgpt-review-of-design-package-protocol.md",
        "build-harness/HANDOFF-LEGO-PIPE-018-spikes-S1-S7-claude-code.md",
        "build-harness/LEGO-PIPE-011-from-studio-to-stage-R2.md",
    )
    EXPECTED_LOST = (
        "build-harness/LEGO-PIPE-011-from-studio-to-stage-R0.md",
        "build-harness/LEGO-PIPE-011-from-studio-to-stage-R1.md",
    )

    def differential(self):
        memos = self.memos()
        self.assertGreaterEqual(len(memos), 27)
        with tempfile.TemporaryDirectory() as tmp:
            basep = os.path.join(tmp, "REGISTER-base.md")
            if WITH_GIT:
                RL.write_bytes(basep, RL.git_bytes(REPO, "show", f"{RL.Register(REPO).manifest['base_commit']}:docs/correspondence/REGISTER.md"))
            else:
                RL.write_bytes(basep, reconstruct_base_register(REPO))
            exit_diffs, other_diffs, gained, lost, mixed = [], [], [], [], []
            for memo in memos:
                rel = os.path.relpath(memo, CORR)
                before = run_tool("memo_preflight.py", memo, basep)
                after = run_tool("memo_preflight.py", memo, REGISTER)
                if before[0] != after[0]:
                    exit_diffs.append(f"{rel}: exit {before[0]} → {after[0]}")
                b_all, a_all = before[1].split("\n"), after[1].split("\n")
                b_warn = [l for l in b_all if self.WARN in l]
                a_warn = [l for l in a_all if self.WARN in l]
                b_rest = [l for l in b_all if self.WARN not in l]
                a_rest = [l for l in a_all if self.WARN not in l]
                if b_rest != a_rest:
                    other_diffs.append(f"{rel}\n  base: {before}\n  head: {after}")
                if a_warn and not b_warn:
                    gained.append(rel)
                elif b_warn and not a_warn:
                    lost.append(rel)
                elif b_warn != a_warn:
                    mixed.append(rel)
            return len(memos), exit_diffs, other_diffs, sorted(gained), sorted(lost), sorted(mixed)

    def test_memo_preflight_exit_codes_and_non_warn_output_identical(self):
        n, exit_diffs, other_diffs, gained, lost, mixed = self.differential()
        self.assertEqual(exit_diffs, [], "\n".join(exit_diffs))
        self.assertEqual(other_diffs, [], "\n".join(other_diffs))
        self.assertEqual(mixed, [], f"WARN text changed rather than gained/lost: {mixed}")
        print(f"\n[corpus differential] {n} memos: exit codes identical; non-WARN output identical; "
              f"'already listed' WARN gained by {len(gained)}, lost by {len(lost)} (see test_g12_gained_and_lost_sets_are_exact)")

    def test_g12_gained_and_lost_sets_are_exact(self):
        """CW-33-I01: direction and membership, not just text."""
        n, _, _, gained, lost, _ = self.differential()
        self.assertEqual(gained, sorted(self.EXPECTED_GAINED), f"gained set changed: +{sorted(set(gained) - set(self.EXPECTED_GAINED))} -{sorted(set(self.EXPECTED_GAINED) - set(gained))}")
        self.assertEqual(lost, sorted(self.EXPECTED_LOST), f"lost set changed: +{sorted(set(lost) - set(self.EXPECTED_LOST))} -{sorted(set(self.EXPECTED_LOST) - set(lost))}")
        self.assertEqual((len(gained), len(lost)), (13, 2))
        print(f"\n[G-12] gained {len(gained)}: {gained}\n[G-12] lost {len(lost)}: {lost}")

    def test_032_memos_pass_preflight_at_head(self):
        for rev in ("R0", "R1"):
            code, out = run_tool("memo_preflight.py", os.path.join(CORR, f"HANDOFF-LEGO-PIPE-032-{rev}-register-migration.md"), REGISTER)
            self.assertEqual(code, 0, out)
        self.assertEqual(sha(RL.read_bytes(os.path.join(CORR, "HANDOFF-LEGO-PIPE-032-R0-register-migration.md"))),
                         "d7980999a57231585cd0fbdcc8fe53302c7c0dc221656d3eac3e4bf59c4861ea")
        self.assertEqual(sha(RL.read_bytes(os.path.join(CORR, "HANDOFF-LEGO-PIPE-032-R1-register-migration.md"))),
                         "0ef0fe82faaa52f13dd4a73ba2c62dc4f513f06f00576aaa9a77a41e51559438")


# ======================================================================= Git tier: finalizer, rehearsal, landing facts

def _git(repo, *args, check=True, env=None):
    p = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, env=env)
    if check and p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} in {repo}: {p.stderr}")
    return p.stdout.strip()


GIT_ENV = dict(os.environ, GIT_AUTHOR_NAME="battery", GIT_AUTHOR_EMAIL="b@x", GIT_COMMITTER_NAME="battery",
               GIT_COMMITTER_EMAIL="b@x", GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1")


class TempRepo:
    """A bare origin whose main is the migrated tree, plus clones (never the project's .git)."""

    def __init__(self, tmp, push_migration=True, with_pending=False, keep_file=True):
        self.tmp = tmp
        self.origin = os.path.join(tmp, "origin.git")
        _git(tmp, "init", "--bare", "-b", "main", self.origin, env=GIT_ENV)
        self.work = self.clone("work")
        # base commit: the pre-migration register only
        base_bytes = pre_migration_rows(reconstruct_base_register(REPO))
        RL.write_bytes(os.path.join(self.work, RL.REGISTER_REL), base_bytes)
        self.commit(self.work, "base: pre-migration register")
        self.base = self.head(self.work)
        if not push_migration:
            _git(self.work, "push", "-q", "origin", "main", env=GIT_ENV)
        # migration commit: the BOOTSTRAP set (constructed, not copied from the live tree —
        # F-08/H4), its manifest re-pinned to this repository's base
        boot = bootstrap_tree(tmp, name="bootstrap-src")
        shutil.copytree(os.path.join(boot, RL.REGISTER_DIR_REL), os.path.join(self.work, RL.REGISTER_DIR_REL))
        os.makedirs(os.path.join(self.work, RL.REGISTER_DIR_REL, "pending"), exist_ok=True)
        if keep_file:
            RL.write_bytes(os.path.join(self.work, RL.REGISTER_DIR_REL, "pending", ".gitkeep"), b"")
        if with_pending:
            RL.write_bytes(os.path.join(self.work, RL.REGISTER_DIR_REL, "pending", "032-register-migration.md"), migration_note_bytes())
        shutil.copyfile(os.path.join(boot, RL.REGISTER_REL), os.path.join(self.work, RL.REGISTER_REL))
        mp = manifest_path(self.work)
        edit_yaml(mp, lambda m: m.update(base_commit=self.base, source_sha256=sha(base_bytes), source_bytes=len(base_bytes),
                                         source_lines=base_bytes.count(b"\n"), verbatim_as_of=self.base))
        os.rename(mp, os.path.join(os.path.dirname(mp), f"MIGRATION-{self.base}.yaml"))
        self.commit(self.work, "migration: register split")
        self.migration = self.head(self.work)
        if push_migration:
            _git(self.work, "push", "-q", "origin", "main", env=GIT_ENV)
        else:
            # the migration stays a branch proposal; origin/main is the unmigrated base
            _git(self.work, "checkout", "-q", "-b", "feat/migration", env=GIT_ENV)
            _git(self.work, "branch", "-q", "-f", "main", "origin/main", env=GIT_ENV)

    def clone(self, name):
        path = os.path.join(self.tmp, name)
        _git(self.tmp, "clone", "-q", self.origin, path, env=GIT_ENV)
        return path

    def commit(self, repo, msg):
        _git(repo, "add", "-A", env=GIT_ENV)
        _git(repo, "commit", "-q", "--allow-empty", "-m", msg, env=GIT_ENV)
        return self.head(repo)

    def head(self, repo):
        return _git(repo, "rev-parse", "HEAD", env=GIT_ENV)

    def pending(self, repo, name, memo, key, body):
        RL.write_bytes(os.path.join(repo, RL.REGISTER_DIR_REL, "pending", name),
                       RL.record_bytes({"affected_memos": [memo], "allocations_consumed": [key]}, body))

    def reserve(self, repo, key, number):
        edit_yaml(os.path.join(repo, RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml"), lambda d: (
            d["allocations"].append({"key": key, "number": number, "identity": f"CORR-LEGO-PIPE-{number:03d}", "type": "CORR",
                                     "thread": "cluster", "actor": "battery", "allocated_by": "James (battery)", "date": "2026-09-21",
                                     "state": "in_flight", "landed_version": None, "basis": "battery"}),
            d.update(next_free=max(d["next_free"], number + 1))))
        regp = os.path.join(repo, RL.REGISTER_REL)
        txt = RL.read_bytes(regp).decode()
        nf = RL.next_free_row_number(txt)
        if number + 1 > nf:
            txt = txt.replace(f"| {nf:03d}+ |", f"| {number + 1:03d}+ |")
        RL.write_bytes(regp, txt.encode())

    def add_row(self, repo, key, text):
        regp = os.path.join(repo, RL.REGISTER_REL)
        txt = RL.read_bytes(regp).decode()
        nf = RL.next_free_row_number(txt)
        txt = txt.replace(f"| {nf:03d}+ |", f"| {key} | `x/{key}.md` | CORR | cluster | battery | {text} |\n| {nf:03d}+ |")
        RL.write_bytes(regp, txt.encode())

    def finalize(self, repo, *args, env=None):
        return run_tool("register_finalize.py", "--repo", repo, *args, env=env or GIT_ENV)

    def lint(self, repo, *args):
        return run_tool("register_lint.py", "--repo", repo, "--git", *args)

    def merge_into_main(self, branch_repo, msg):
        """Merge a branch clone's HEAD into origin/main by merge commit (the landing)."""
        landing = self.clone("landing-" + os.path.basename(branch_repo) + str(len(os.listdir(self.tmp))))
        _git(landing, "fetch", "-q", branch_repo, "HEAD", env=GIT_ENV)
        _git(landing, "merge", "-q", "--no-ff", "-m", msg, "FETCH_HEAD", env=GIT_ENV)
        _git(landing, "push", "-q", "origin", "main", env=GIT_ENV)
        return self.head(landing)


@unittest.skipUnless(WITH_GIT, "--with-git: builds temporary repositories")
class GitTier(unittest.TestCase):
    def test_positive_rf_happy_path_and_g06_determinism(self):
        with tempfile.TemporaryDirectory() as tmp:
            T = TempRepo(tmp)
            a = T.clone("a")
            T.reserve(a, "040-R0", 40)
            T.add_row(a, "040-R0", "for review")
            T.pending(a, "040.md", "CORR-LEGO-PIPE-040-R0", "040-R0", b"note A, byte-exact \xe2\x80\x94 no trailing newline")
            T.commit(a, "memo 040")
            b = T.clone("b-twin")
            _git(b, "fetch", "-q", a, "HEAD", env=GIT_ENV); _git(b, "checkout", "-q", "FETCH_HEAD", env=GIT_ENV)
            code, out = T.finalize(a)
            self.assertEqual(code, 0, out)
            self.assertIn("finalized 2026-09-18.32", out)
            code, out = T.finalize(b)
            self.assertEqual(code, 0, out)
            for rel in (RL.REGISTER_REL, os.path.join(RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml"), os.path.join(RL.REGISTER_DIR_REL, "versions", "2026-09-18.32.md")):
                self.assertEqual(RL.read_bytes(os.path.join(a, rel)), RL.read_bytes(os.path.join(b, rel)), rel)
            self.assertFalse(os.path.exists(os.path.join(a, RL.REGISTER_DIR_REL, "pending", "040.md")))
            fm, body = RL.parse_record(RL.read_bytes(os.path.join(a, RL.REGISTER_DIR_REL, "versions", "2026-09-18.32.md")))
            self.assertEqual(fm["finalized_from_main"], T.migration)
            self.assertEqual(fm["allocations_consumed"], ["040-R0"])
            self.assertNotIn("landing_pr", fm)
            self.assertEqual(body, b"note A, byte-exact \xe2\x80\x94 no trailing newline")
            T.commit(a, "finalize 040")
            code, out = T.finalize(a, "--check")
            self.assertEqual(code, 0, out)
            self.assertIn("empty diff", out)
            # G-06 mutation: a timestamp field injected into the record → --check non-empty
            edit_record(a, "2026-09-18.32", lambda fm: fm.update(landed_at="2026-09-21T00:00:00Z"))
            code, out = T.finalize(a, "--check")
            self.assertEqual(code, 1, out)

    def test_self_hosting_first_run_against_unmigrated_main(self):
        """Q-12: the migration PR's own version comes from the first real finalizer run, against
        an origin/main that has no register/versions/ at all. Rehearsed here in a temporary
        repository — never on the implementation branch before independent review."""
        with tempfile.TemporaryDirectory() as tmp:
            T = TempRepo(tmp, push_migration=False)
            w = T.work
            self.assertEqual(_git(w, "rev-parse", "origin/main", env=GIT_ENV), T.base)
            self.assertFalse(_git(w, "ls-tree", "--name-only", "origin/main", RL.REGISTER_DIR_REL.replace(os.sep, "/") + "/", check=False, env=GIT_ENV))
            # the committed pending note consumes 032-R1, which the seeded ledger holds in_flight
            RL.write_bytes(os.path.join(w, RL.REGISTER_DIR_REL, "pending", "032-register-migration.md"), migration_note_bytes())
            T.commit(w, "pending note")
            code, out = T.finalize(w, "--check")
            self.assertEqual(code, 1, out)
            self.assertIn("RF-05", out)
            code, out = T.finalize(w)
            self.assertEqual(code, 0, out)
            self.assertIn("finalized 2026-09-18.32 (previous 2026-09-18.31)", out)
            fm, body = RL.parse_record(RL.read_bytes(os.path.join(w, RL.REGISTER_DIR_REL, "versions", "2026-09-18.32.md")))
            self.assertEqual(fm["finalized_from_main"], T.base)
            self.assertEqual(fm["allocations_consumed"], ["032-R1"])
            self.assertEqual(fm["kind"], "finalized")
            # the rehearsal reproduces the REAL landing's note digest when the live tree carries it
            live32 = RL.Register(REPO).records.get("2026-09-18.32")
            if live32 and live32[0].get("kind") == "finalized":
                self.assertEqual(fm["note_sha256"], live32[0]["note_sha256"], "temp-repo finalization of the derived note must reproduce the real .32 note_sha256")
            ledger = RL.load_yaml_file(os.path.join(w, RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml"))
            e = next(e for e in ledger["allocations"] if e["key"] == "032-R1")
            self.assertEqual((e["state"], e["landed_version"]), ("landed", "2026-09-18.32"))
            self.assertIn("**Register version: 2026-09-18.32**", RL.read_bytes(os.path.join(w, RL.REGISTER_REL)).decode())
            T.commit(w, "finalize 032")
            code, out = T.finalize(w, "--check")
            self.assertEqual(code, 0, out)
            self.assertIn("empty diff", out)
            code, out = T.lint(w)
            self.assertEqual(code, 0, out)
            self.assertIn("RL-13 36 + 1 base data rows", out)
            # land it by merge commit; the next ordinary landing (the canary) is the second run
            landing = T.merge_into_main(w, "Merge migration — landing .32")
            c = T.clone("canary")
            T.reserve(c, "070-R0", 70); T.add_row(c, "070-R0", "canary"); T.pending(c, "070.md", "CORR-LEGO-PIPE-070-R0", "070-R0", b"canary")
            T.commit(c, "canary memo")
            code, out = T.finalize(c)
            self.assertEqual(code, 0, out)
            self.assertIn("finalized 2026-09-18.33", out)
            T.commit(c, "finalize canary")
            T.merge_into_main(c, "Merge canary — landing .33")
            _git(w, "checkout", "-q", "main", env=GIT_ENV); _git(w, "pull", "-q", "--ff-only", "origin", "main", env=GIT_ENV)
            code, out = T.lint(w)
            self.assertEqual(code, 0, out)
            self.assertIn(f"2026-09-18.32.md: landed by {landing[:12]} (first parent {T.base[:12]}", out)
            self.assertIn("2026-09-18.33.md: landed by", out)
            self.assertIn("RL-13 migration already on origin/main", out)

    def test_pending_note_survives_a_merge_across_another_landing(self):
        """Found in the live rehearsal: when a landing deletes every file in pending/ and adds a
        record whose body is the note, git's directory-rename detection infers pending/ →
        versions/ and relocates a concurrent branch's new pending note into versions/ on merge.
        pending/.gitkeep keeps the directory alive; this reproduces the hazard with the real
        migration note (large enough to trip rename similarity)."""
        def scenario(keep_file):
            with tempfile.TemporaryDirectory() as tmp:
                # the merge base carries the migration's own pending note (as the real head does)
                T = TempRepo(tmp, with_pending=True, keep_file=keep_file)
                a, b = T.clone("A"), T.clone("B")
                T.reserve(a, "080-R0", 80); T.add_row(a, "080-R0", "x"); T.pending(a, "080.md", "CORR-LEGO-PIPE-080-R0", "080-R0", b"a")
                T.commit(a, "memo 080")
                T.reserve(b, "081-R0", 81); T.add_row(b, "081-R0", "x"); T.pending(b, "081.md", "CORR-LEGO-PIPE-081-R0", "081-R0", b"small")
                T.commit(b, "memo 081")
                code, out = T.finalize(a)  # consumes 032-R1 and 080-R0 together
                self.assertEqual(code, 0, out)
                keep = os.path.join(a, RL.REGISTER_DIR_REL, "pending", ".gitkeep")
                self.assertTrue(os.path.exists(keep), "the finalizer must leave the keep-file behind")
                if not keep_file:
                    os.remove(keep)  # a finalizer without the protection would empty pending/
                T.commit(a, "finalize 080")
                T.merge_into_main(a, "landing 080")
                _git(b, "fetch", "-q", "origin", env=GIT_ENV)
                subprocess.run(["git", "merge", "--no-edit", "origin/main"], cwd=b, capture_output=True, env=GIT_ENV)
                return (os.path.exists(os.path.join(b, RL.REGISTER_DIR_REL, "pending", "081.md")),
                        os.path.exists(os.path.join(b, RL.REGISTER_DIR_REL, "versions", "081.md")))
        # without the keep-file the hazard is real: git relocates B's note into versions/
        self.assertEqual(scenario(keep_file=False), (False, True), "expected git's directory-rename detection to relocate the note; the fixture no longer reproduces the hazard")
        # with it, the note stays where it was written
        self.assertEqual(scenario(keep_file=True), (True, False))

    def test_mutation_rf01_fetch_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            T = TempRepo(tmp)
            a = T.clone("a")
            shutil.rmtree(T.origin)
            code, out = T.finalize(a)
            self.assertEqual(code, 1, out)
            self.assertIn("RF-01", out)

    def test_mutation_rf05_nothing_to_finalize_and_check_before_finalization(self):
        with tempfile.TemporaryDirectory() as tmp:
            T = TempRepo(tmp)
            a = T.clone("a")
            code, out = T.finalize(a)
            self.assertEqual(code, 1, out)
            self.assertIn("RF-05", out)
            T.pending(a, "041.md", "CORR-LEGO-PIPE-041-R0", "041-R0", b"x")
            code, out = T.finalize(a, "--check")
            self.assertEqual(code, 1, out)
            self.assertIn("RF-05", out)
            self.assertIn("not finalized", out)

    def test_mutation_rf04_leftover_stale_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            T = TempRepo(tmp)
            a = T.clone("a")
            write_record(a, finalized_fm(version="2026-09-18.33", prev="2026-09-18.32", main=T.migration), b"stale")
            T.pending(a, "042.md", "CORR-LEGO-PIPE-042-R0", "042-R0", b"x")
            code, out = T.finalize(a)
            self.assertEqual(code, 1, out)
            self.assertIn("RF-04", out)
            self.assertIn("2026-09-18.33.md", out)

    def test_mutation_rf06_lint_error_reverts_every_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            T = TempRepo(tmp)
            a = T.clone("a")
            T.pending(a, "043.md", "CORR-LEGO-PIPE-043-R0", "043-not-in-ledger", b"x")
            before = {rel: RL.read_bytes(os.path.join(a, rel)) for rel in (RL.REGISTER_REL, os.path.join(RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml"))}
            code, out = T.finalize(a)
            self.assertEqual(code, 1, out)
            self.assertIn("RF-06", out)
            self.assertFalse(os.path.exists(os.path.join(a, RL.REGISTER_DIR_REL, "versions", "2026-09-18.32.md")))
            self.assertTrue(os.path.exists(os.path.join(a, RL.REGISTER_DIR_REL, "pending", "043.md")))
            for rel, data in before.items():
                self.assertEqual(RL.read_bytes(os.path.join(a, rel)), data, rel)

    def porcelain(self, repo):
        p = subprocess.run(["git", "status", "--porcelain"], cwd=repo, capture_output=True, text=True, env=GIT_ENV)
        return sorted(l for l in p.stdout.split("\n") if l.strip())  # keep the leading status columns

    def snapshot(self, repo):
        """Every file the finalizer may touch, plus the working tree's porcelain."""
        out = {}
        for rel in (RL.REGISTER_REL, os.path.join(RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml")):
            out[rel] = RL.read_bytes(os.path.join(repo, rel))
        for sub in ("versions", "pending"):
            d = os.path.join(repo, RL.REGISTER_DIR_REL, sub)
            out[sub] = {n: RL.read_bytes(os.path.join(d, n)) for n in sorted(os.listdir(d))} if os.path.isdir(d) else None
        out["porcelain"] = self.porcelain(repo)
        return out

    def test_mutation_rf07_missing_or_wrong_target(self):
        """CW-33-I02: the finalizer never infers its target. Missing --repo, a non-directory, a
        directory that is not a Git work tree, a subdirectory of one, and a work tree with no
        register all refuse with RF-07 before any fetch; every run's first line names its target."""
        with tempfile.TemporaryDirectory() as tmp:
            T = TempRepo(tmp)
            a = T.clone("a")
            T.reserve(a, "044-R0", 44); T.add_row(a, "044-R0", "x")
            T.pending(a, "044.md", "CORR-LEGO-PIPE-044-R0", "044-R0", b"x")
            T.commit(a, "memo 044")
            before = self.snapshot(a)
            # missing --repo, run from inside the target repo AND from /tmp: both refuse
            for cwd in (a, tmp):
                for extra in ((), ("--check",)):
                    code, out = run_tool("register_finalize.py", *extra, cwd=cwd, env=GIT_ENV)
                    self.assertEqual(code, 1, out)
                    self.assertEqual(out.split("\n")[0], "target: (none)", out)
                    self.assertIn("RF-07", out)
                    self.assertIn("--repo DIR is required", out)
            # wrong targets
            for bad, why in ((os.path.join(tmp, "nope"), "is not a directory"),
                             (os.path.join(tmp, "plain"), "is not inside a Git work tree"),
                             (os.path.join(a, "docs"), "is not the top level of its Git work tree"),
                             (os.path.join(tmp, "gitnoreg"), "has no docs/correspondence/REGISTER.md")):
                if why.startswith("is not inside"):
                    os.makedirs(bad)
                if why.startswith("has no"):
                    _git(tmp, "init", "-q", "-b", "main", bad, env=GIT_ENV)
                code, out = run_tool("register_finalize.py", "--repo", bad, cwd=tmp, env=GIT_ENV)
                self.assertEqual(code, 1, out)
                self.assertEqual(out.split("\n")[0], f"target: {os.path.abspath(bad)}", out)
                self.assertIn("RF-07", out)
                self.assertIn(why, out)
            # nothing was written anywhere in the real repo by any of the refusals
            self.assertEqual(self.snapshot(a), before)
            # positive: the explicit target is announced first, then the run proceeds
            code, out = T.finalize(a)
            self.assertEqual(code, 0, out)
            self.assertEqual(out.split("\n")[0], f"target: {os.path.abspath(a)}", out)

    def test_mutation_rf06_yaml_parse_failure_after_record_and_pointer_writes_rolls_back(self):
        """CDX-34-I01: the ledger is read AFTER the record and pointer are written. A parser
        failure there must enter RF-06, revert both writes, restore the pending note, and leave
        the working tree differing only by the deliberately corrupted ledger — no traceback."""
        with tempfile.TemporaryDirectory() as tmp:
            T = TempRepo(tmp)
            a = T.clone("a")
            T.reserve(a, "045-R0", 45); T.add_row(a, "045-R0", "x")
            T.pending(a, "045.md", "CORR-LEGO-PIPE-045-R0", "045-R0", b"note 045")
            T.commit(a, "memo 045")
            ledger_rel = os.path.join(RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml")
            ledger_path = os.path.join(a, ledger_rel)
            RL.write_bytes(ledger_path, b"allocations: [\n  - key: broken\n    state: {unclosed\n")  # yaml.parser.ParserError
            before = self.snapshot(a)
            self.assertEqual(before["porcelain"], [f" M {ledger_rel}"])
            code, out = T.finalize(a)
            self.assertEqual(code, 1, out)
            self.assertIn("RF-06", out)
            self.assertIn("ParserError", out)
            self.assertNotIn("Traceback", out)
            after = self.snapshot(a)
            self.assertEqual(after, before, "rollback must restore pointer, record, ledger, pending notes and the porcelain")
            self.assertFalse(os.path.exists(os.path.join(a, RL.REGISTER_DIR_REL, "versions", "2026-09-18.32.md")))
            self.assertIn(b"**Register version: 2026-09-18.31**", after[RL.REGISTER_REL])
            self.assertIn("045.md", after["pending"])
            self.assertEqual(after["porcelain"], [f" M {ledger_rel}"])

    def test_mutation_rf06_decode_and_filesystem_failures_after_first_write_roll_back(self):
        """CDX-34-I01, the other two operational classes: a ledger that is not UTF-8, and a
        ledger path that is a directory (OSError on read) — both after the first write."""
        for corrupt in (lambda p: RL.write_bytes(p, b"\xff\xfe not utf-8"),
                        lambda p: (os.remove(p), os.makedirs(p))):
            with tempfile.TemporaryDirectory() as tmp:
                T = TempRepo(tmp)
                a = T.clone("a")
                T.reserve(a, "046-R0", 46); T.add_row(a, "046-R0", "x")
                T.pending(a, "046.md", "CORR-LEGO-PIPE-046-R0", "046-R0", b"note 046")
                T.commit(a, "memo 046")
                ledger_path = os.path.join(a, RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml")
                corrupt(ledger_path)
                pointer_before = RL.read_bytes(os.path.join(a, RL.REGISTER_REL))
                code, out = T.finalize(a)
                self.assertEqual(code, 1, out)
                self.assertIn("RF-06", out)
                self.assertNotIn("Traceback", out)
                self.assertFalse(os.path.exists(os.path.join(a, RL.REGISTER_DIR_REL, "versions", "2026-09-18.32.md")))
                self.assertEqual(RL.read_bytes(os.path.join(a, RL.REGISTER_REL)), pointer_before)
                self.assertTrue(os.path.exists(os.path.join(a, RL.REGISTER_DIR_REL, "pending", "046.md")))

    def test_mutation_reserved_allocation_cannot_be_consumed(self):
        """CDX-34-I02: only in_flight is consumable. A reserved allocation named by a pending
        note refuses through RF-06 with the tree left exactly as committed."""
        with tempfile.TemporaryDirectory() as tmp:
            T = TempRepo(tmp)
            a = T.clone("a")
            T.reserve(a, "047-R0", 47); T.add_row(a, "047-R0", "x")
            edit_yaml(os.path.join(a, RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml"),
                      lambda d: [e.update(state="reserved") for e in d["allocations"] if e["key"] == "047-R0"])
            T.pending(a, "047.md", "CORR-LEGO-PIPE-047-R0", "047-R0", b"note 047")
            T.commit(a, "memo 047 reserved")
            before = self.snapshot(a)
            self.assertEqual(before["porcelain"], [])
            code, out = T.finalize(a)
            self.assertEqual(code, 1, out)
            self.assertIn("RF-06", out)
            self.assertIn("allocation 047-R0 is 'reserved', not in_flight", out)
            self.assertEqual(self.snapshot(a), before)
            # and a landed one is refused too (never re-consumed)
            edit_yaml(os.path.join(a, RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml"),
                      lambda d: [e.update(state="landed", landed_version="2026-09-18.30") for e in d["allocations"] if e["key"] == "047-R0"])
            T.commit(a, "047 landed elsewhere")
            code, out = T.finalize(a)
            self.assertEqual(code, 1, out)
            self.assertIn("is 'landed', not in_flight", out)
            self.assertEqual(self.porcelain(a), [])

    def test_positive_zero_allocation_landing_finalizes(self):
        """CW-33-I04: a revision or policy-text-only landing consumes no number (rule 8).
        `allocations_consumed: []` finalizes; the ledger is untouched byte for byte; --check is
        an empty diff; affected_memos may not be empty."""
        with tempfile.TemporaryDirectory() as tmp:
            T = TempRepo(tmp)
            a = T.clone("a")
            RL.write_bytes(os.path.join(a, RL.REGISTER_DIR_REL, "pending", "048.md"),
                           RL.record_bytes({"affected_memos": ["CORR-LEGO-PIPE-030-R1"], "allocations_consumed": []}, b"R1 of 030: revision consumes no number"))
            T.commit(a, "030-R1 revision")
            ledger_rel = os.path.join(RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml")
            ledger_before = RL.read_bytes(os.path.join(a, ledger_rel))
            code, out = T.finalize(a)
            self.assertEqual(code, 0, out)
            self.assertIn("consumed []", out)
            fm, body = RL.parse_record(RL.read_bytes(os.path.join(a, RL.REGISTER_DIR_REL, "versions", "2026-09-18.32.md")))
            self.assertEqual(fm["allocations_consumed"], [])
            self.assertEqual(fm["affected_memos"], ["CORR-LEGO-PIPE-030-R1"])
            self.assertEqual(RL.read_bytes(os.path.join(a, ledger_rel)), ledger_before)
            T.commit(a, "finalize 030-R1")
            code, out = T.finalize(a, "--check")
            self.assertEqual(code, 0, out)
            self.assertIn("empty diff", out)
            code, out = T.lint(a)
            self.assertEqual(code, 0, out)
            # the schema accepts the record the finalizer emitted
            errs = []
            check_against_schema(fm, load_schema("register-version.v1"), errs)
            self.assertEqual(errs, [], errs)
        # affected_memos: [] is still refused
        with tempfile.TemporaryDirectory() as tmp:
            T = TempRepo(tmp)
            a = T.clone("a")
            RL.write_bytes(os.path.join(a, RL.REGISTER_DIR_REL, "pending", "049.md"),
                           RL.record_bytes({"affected_memos": [], "allocations_consumed": []}, b"x"))
            code, out = T.finalize(a)
            self.assertEqual(code, 1, out)
            self.assertIn("RF-05", out)
            self.assertIn("affected_memos must be a non-empty list", out)

    def test_two_branch_rehearsal(self):
        """R0 §9: steps 1–8 — stale finalization fails at RF-02 (not RF-03), refresh assigns
        the following version without editing the first, table-tail conflict measured, RF-03 in
        both variants, negative control RL-11."""
        with tempfile.TemporaryDirectory() as tmp:
            T = TempRepo(tmp)
            a, b = T.clone("A"), T.clone("B")
            # step 1: distinct pending notes and distinct table-tail rows
            for repo, key, n in ((a, "050", 50), (b, "051", 51)):
                T.reserve(repo, f"{key}-R0", n)
                T.add_row(repo, f"{key}-R0", "for review")
                T.pending(repo, f"{key}.md", f"CORR-LEGO-PIPE-{key}-R0", f"{key}-R0", f"note {key}".encode())
                T.commit(repo, f"memo {key}")
            # step 2: finalize A → .32; record bytes; land by merge commit
            code, out = T.finalize(a)
            self.assertEqual(code, 0, out)
            T.commit(a, "finalize 050")
            rec_a = RL.read_bytes(os.path.join(a, RL.REGISTER_DIR_REL, "versions", "2026-09-18.32.md"))
            landing_a = T.merge_into_main(a, "Merge A (050) — landing .32")
            # step 3: finalize B against the stale base → RF-02, nothing written
            tree_before = _git(b, "status", "--porcelain", env=GIT_ENV)
            code, out = T.finalize(b)
            self.assertEqual(code, 1, out)
            self.assertIn("RF-02", out)
            self.assertNotIn("RF-03", out)
            self.assertEqual(_git(b, "status", "--porcelain", env=GIT_ENV), tree_before, "nothing written on refusal")
            self.assertFalse(os.path.exists(os.path.join(b, RL.REGISTER_DIR_REL, "versions", "2026-09-18.32.md")))
            # step 4: git merge origin/main into B — the table tail conflicts; record the outcome
            _git(b, "fetch", "-q", "origin", env=GIT_ENV)
            p = subprocess.run(["git", "merge", "--no-edit", "origin/main"], cwd=b, capture_output=True, text=True, env=GIT_ENV)
            auto_merged = p.returncode == 0
            if not auto_merged:
                conflicted = _git(b, "diff", "--name-only", "--diff-filter=U", env=GIT_ENV).split()
                self.rehearsal_note = f"table-tail merge: git did NOT auto-merge; conflicts in {conflicted}; resolved by keeping both rows"
                # resolve deterministically: take main's REGISTER.md and re-apply B's row + next-free; ledger: take main's and re-add B's entry
                _git(b, "checkout", "--theirs", RL.REGISTER_REL, env=GIT_ENV)
                T.add_row(b, "051-R0", "for review")
                regp = os.path.join(b, RL.REGISTER_REL)
                RL.write_bytes(regp, RL.read_bytes(regp).replace(b"| 051+ |", b"| 052+ |"))
                lp = os.path.join(b, RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml")
                if lp.replace(b + os.sep, "") in conflicted or os.path.join(RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml") in conflicted:
                    _git(b, "checkout", "--theirs", os.path.join(RL.REGISTER_DIR_REL, "ALLOCATIONS.yaml"), env=GIT_ENV)
                    T.reserve(b, "051-R0", 51)
                _git(b, "add", "-A", env=GIT_ENV)
                _git(b, "commit", "-q", "--no-edit", env=GIT_ENV)
            else:
                self.rehearsal_note = "table-tail merge: git auto-merged the adjacent rows"
            print(f"\n[rehearsal] {self.rehearsal_note}")
            # step 5: finalize B → .33; A's record byte-identical; --check empty; lint green; --git derives A's landing
            code, out = T.finalize(b)
            self.assertEqual(code, 0, out)
            self.assertIn("finalized 2026-09-18.33", out)
            self.assertEqual(RL.read_bytes(os.path.join(b, RL.REGISTER_DIR_REL, "versions", "2026-09-18.32.md")), rec_a)
            T.commit(b, "finalize 051")
            code, out = T.finalize(b, "--check")
            self.assertEqual(code, 0, out)
            code, out = T.lint(b)
            self.assertEqual(code, 0, out)
            self.assertIn(f"2026-09-18.32.md: landed by {landing_a[:12]} (first parent {T.migration[:12]}", out)
            landing_b = T.merge_into_main(b, "Merge B (051) — landing .33")
            # step 6: RF-03, correspondence variant — main advances with a version record during the pause
            c = T.clone("C")
            T.reserve(c, "052-R0", 52); T.add_row(c, "052-R0", "x"); T.pending(c, "052.md", "CORR-LEGO-PIPE-052-R0", "052-R0", b"c")
            T.commit(c, "memo 052")
            d = T.clone("D")
            T.reserve(d, "053-R0", 53); T.add_row(d, "053-R0", "x"); T.pending(d, "053.md", "CORR-LEGO-PIPE-053-R0", "053-R0", b"d")
            T.commit(d, "memo 053")
            # D lands by MERGE COMMIT (a fast-forward push of a multi-commit branch would put a
            # correspondence commit with no version record on main's first-parent line — which
            # RL-10 catches, and which is the Q-06 merge-commit setting's whole purpose)
            landing_d = T.clone("landing-D")
            hook = os.path.join(tmp, "advance-corr.sh")
            RL.write_bytes(hook, (f"#!/bin/sh\nset -e\ncd {d} && {sys.executable} {os.path.join(TOOLS, 'register_finalize.py')} --repo {d} >/dev/null && git add -A && git commit -q -m finalize-053\n"
                                  f"cd {landing_d} && git fetch -q {d} HEAD && git merge -q --no-ff -m 'Merge D (053) — landing' FETCH_HEAD && git push -q origin main\n").encode())
            os.chmod(hook, 0o755)
            env = dict(GIT_ENV, REGISTER_FINALIZE_PAUSE_CMD=hook)
            tree_before = _git(c, "status", "--porcelain", env=GIT_ENV)
            code, out = T.finalize(c, env=env)
            self.assertEqual(code, 1, out)
            self.assertIn("RF-03", out)
            self.assertEqual(_git(c, "status", "--porcelain", env=GIT_ENV), tree_before)
            self.assertFalse(os.path.exists(os.path.join(c, RL.REGISTER_DIR_REL, "versions", "2026-09-18.34.md")))
            # step 7: RF-03, non-correspondence variant — a plain code change advances main
            # (a fresh clone G, cut after D's landing, so the only intervening commit is E's)
            g = T.clone("G")
            T.reserve(g, "054-R0", 54); T.add_row(g, "054-R0", "x"); T.pending(g, "054.md", "CORR-LEGO-PIPE-054-R0", "054-R0", b"g")
            T.commit(g, "memo 054")
            e = T.clone("E")
            RL.write_bytes(os.path.join(e, "src", "unrelated.txt"), b"code change\n")
            T.commit(e, "unrelated code change")
            hook2 = os.path.join(tmp, "advance-code.sh")
            RL.write_bytes(hook2, f"#!/bin/sh\ncd {e} && git push -q origin HEAD:main\n".encode())
            os.chmod(hook2, 0o755)
            tree_before = _git(g, "status", "--porcelain", env=GIT_ENV)
            code, out = T.finalize(g, env=dict(GIT_ENV, REGISTER_FINALIZE_PAUSE_CMD=hook2))
            self.assertEqual(code, 1, out)
            self.assertIn("RF-03", out)
            self.assertNotIn("versions/2026-09-18.35.md", _git(g, "status", "--porcelain", env=GIT_ENV))
            self.assertEqual(_git(g, "status", "--porcelain", env=GIT_ENV), tree_before, "nothing written on RF-03")
            self.assertTrue(os.path.exists(os.path.join(g, RL.REGISTER_DIR_REL, "pending", "054.md")))
            # after merging main (E's code change; no register conflict) G finalizes cleanly as .35
            _git(g, "fetch", "-q", "origin", env=GIT_ENV); _git(g, "merge", "-q", "--no-edit", "origin/main", env=GIT_ENV)
            code, out = T.finalize(g)
            self.assertEqual(code, 0, out)
            self.assertIn("finalized 2026-09-18.35", out)
            # step 8: negative control — a hand-written record on a third branch → RL-11 red
            f = T.clone("F")
            write_record(f, finalized_fm(version="2026-09-18.35", prev="2026-09-18.34", main="e" * 40), b"hand")
            RL.write_bytes(os.path.join(f, RL.REGISTER_REL), RF.pointer_line(RL.read_bytes(os.path.join(f, RL.REGISTER_REL)).decode(), "2026-09-18.35").encode())
            code, out = T.lint(f)
            self.assertEqual(code, 1, out)
            self.assertIn("RL-11 ERROR", out)
            self.assertIn("stale base or hand-written", out)

    def test_positive_rl10_rl16_rl17_and_bootstrap_replay(self):
        """AO-17: the migration merge (30 migrated, 0 finalized) is invisible to G-16; the
        ordinary finalized landing after it is counted; RL-17 sees one introducing commit."""
        with tempfile.TemporaryDirectory() as tmp:
            T = TempRepo(tmp)
            code, out = T.lint(T.work)
            self.assertEqual(code, 0, out)
            self.assertIn("RL-17 all 30 migrated records introduced by one first-parent commit", out)
            self.assertIn("RL-16 baseline fixed at", out)
            a = T.clone("a")
            T.reserve(a, "060-R0", 60); T.add_row(a, "060-R0", "x"); T.pending(a, "060.md", "CORR-LEGO-PIPE-060-R0", "060-R0", b"a")
            T.commit(a, "memo 060")
            code, out = T.finalize(a)
            self.assertEqual(code, 0, out)
            T.commit(a, "finalize")
            T.merge_into_main(a, "landing 060")
            _git(T.work, "pull", "-q", "origin", "main", env=GIT_ENV)
            code, out = T.lint(T.work)
            self.assertEqual(code, 0, out)
            self.assertIn("2026-09-18.32.md: landed by", out)

    def test_mutation_rl10_landing_without_a_finalized_record_and_with_two(self):
        with tempfile.TemporaryDirectory() as tmp:
            T = TempRepo(tmp)
            a = T.clone("a")
            T.add_row(a, "061-R0", "row added without finalization")
            T.reserve(a, "061-R0", 61)
            T.commit(a, "memo 061 no finalize")
            T.merge_into_main(a, "landing without record")
            _git(T.work, "pull", "-q", "origin", "main", env=GIT_ENV)
            code, out = T.lint(T.work)
            self.assertEqual(code, 1, out)
            self.assertIn("introduces 0 finalized records", out)
            # two finalized records in one landing
            b = T.clone("b")
            for v, pv in (("2026-09-18.32", "2026-09-18.31"), ("2026-09-18.33", "2026-09-18.32")):
                write_record(b, finalized_fm(version=v, prev=pv, main=_git(b, "rev-parse", "origin/main", env=GIT_ENV)), b"x")
            RL.write_bytes(os.path.join(b, RL.REGISTER_REL), RF.pointer_line(RL.read_bytes(os.path.join(b, RL.REGISTER_REL)).decode(), "2026-09-18.33").encode())
            T.commit(b, "two records")
            T.merge_into_main(b, "landing with two records")
            _git(T.work, "pull", "-q", "origin", "main", env=GIT_ENV)
            code, out = T.lint(T.work)
            self.assertEqual(code, 1, out)
            self.assertIn("introduces 2 finalized records", out)

    def test_mutation_rl16_baseline_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            T = TempRepo(tmp)
            edit_yaml(manifest_path(T.work), lambda m: m.update(source_sha256="0" * 64))
            code, out = T.lint(T.work)
            self.assertEqual(code, 1, out)
            self.assertIn("RL-16 ERROR", out)
        with tempfile.TemporaryDirectory() as tmp:
            # an unrelated register edit between base and migration
            origin = os.path.join(tmp, "o.git"); _git(tmp, "init", "--bare", "-b", "main", origin, env=GIT_ENV)
            work = os.path.join(tmp, "w"); _git(tmp, "clone", "-q", origin, work, env=GIT_ENV)
            RL.write_bytes(os.path.join(work, RL.REGISTER_REL), reconstruct_base_register(REPO))
            _git(work, "add", "-A", env=GIT_ENV); _git(work, "commit", "-q", "-m", "base", env=GIT_ENV)
            RL.write_bytes(os.path.join(work, "docs", "correspondence", "stray.md"), b"between")
            _git(work, "add", "-A", env=GIT_ENV); _git(work, "commit", "-q", "-m", "stray correspondence edit", env=GIT_ENV)
            boot = bootstrap_tree(tmp, name="boot")
            shutil.copytree(os.path.join(boot, RL.REGISTER_DIR_REL), os.path.join(work, RL.REGISTER_DIR_REL))
            shutil.copyfile(os.path.join(boot, RL.REGISTER_REL), os.path.join(work, RL.REGISTER_REL))
            base = _git(work, "rev-parse", "HEAD~1", env=GIT_ENV)
            edit_yaml(manifest_path(work), lambda m: m.update(base_commit=base, source_sha256=sha(reconstruct_base_register(REPO))))
            _git(work, "add", "-A", env=GIT_ENV); _git(work, "commit", "-q", "-m", "migration", env=GIT_ENV)
            _git(work, "push", "-q", "origin", "main", env=GIT_ENV)
            code, out = run_tool("register_lint.py", "--repo", work, "--git")
            self.assertEqual(code, 1, out)
            self.assertIn("touch docs/correspondence/", out)

    def test_mutation_rl17_second_introduction_of_a_migrated_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            T = TempRepo(tmp)
            a = T.clone("a")
            reg = RL.Register(a)
            s = reg.slices()["s-31"]
            write_record(a, {"register_version": "2026-09-18.32", "previous_version": "2026-09-18.31", "kind": "migrated", "slice": "s-31"}, reg.records["2026-09-18.31"][1])
            RL.write_bytes(os.path.join(a, RL.REGISTER_REL), RF.pointer_line(RL.read_bytes(os.path.join(a, RL.REGISTER_REL)).decode(), "2026-09-18.32").encode())
            T.commit(a, "a later migrated record")
            code, out = T.lint(a)
            self.assertEqual(code, 1, out)
            self.assertIn("RL-17 ERROR", out)
            self.assertIn("2 different first-parent commits", out)

    def test_mutation_rl11_stale_base_half(self):
        with tempfile.TemporaryDirectory() as tmp:
            T = TempRepo(tmp)
            a = T.clone("a")
            write_record(a, finalized_fm(main="f" * 40), b"x")
            RL.write_bytes(os.path.join(a, RL.REGISTER_REL), RF.pointer_line(RL.read_bytes(os.path.join(a, RL.REGISTER_REL)).decode(), "2026-09-18.32").encode())
            code, out = T.lint(a)
            self.assertEqual(code, 1, out)
            self.assertIn("RL-11 ERROR", out)

    def test_positive_rl09_rl18_prior_tree_from_origin_main(self):
        with tempfile.TemporaryDirectory() as tmp:
            T = TempRepo(tmp)
            code, out = T.lint(T.work)
            self.assertEqual(code, 0, out)
            self.assertIn("RL-09 30 prior records byte-identical", out)
            self.assertIn("RL-18 Rule 18 merge-method sentinel present", out)
            edit_record(T.work, "2026-09-18.19", body=b"tampered")
            code, out = T.lint(T.work)
            self.assertEqual(code, 1, out)
            self.assertIn("RL-09 ERROR", out)


# ======================================================================= meta-test (AO-15)

RULE_TESTS = {
    "RL-01": ("MigrationProof.test_positive_rl01_reconstruction_and_digests", "MigrationProof.test_mutation_rl01_shift_one_boundary"),
    "RL-02": ("LedgerSetPointer.test_positive_rl02_ledger_seed_complete_and_next_free_derived", "LedgerSetPointer.test_mutation_rl02_duplicate_key"),
    "RL-03": ("LedgerSetPointer.test_positive_rl03_set_complete", "LedgerSetPointer.test_mutation_rl03_register_alone_is_not_the_register"),
    "RL-04": ("LedgerSetPointer.test_positive_rl04_pointer", "LedgerSetPointer.test_mutation_rl04_pointer_behind_and_doubled"),
    "RL-05": ("MigrationProof.test_positive_rl05_resolve_every_version_and_compare_digests", "MigrationProof.test_mutation_rl05_delete_a_record"),
    "RL-06": ("MigrationProof.test_positive_rl06_chain", "MigrationProof.test_mutation_rl06_second_chain_start"),
    "RL-07": ("Anomalies.test_positive_rl07_historical_doubled_label_and_shared_slices_green", "Anomalies.test_mutation_rl07_remove_dot6_anomaly"),
    "RL-08": ("Anomalies.test_positive_rl07_historical_doubled_label_and_shared_slices_green", "Anomalies.test_mutation_rl08_frozen_false"),
    "RL-09": ("ImmutabilityRowsRule18.test_positive_rl09_against_a_prior_tree", "ImmutabilityRowsRule18.test_mutation_rl09_edit_one_byte_and_regenerate_pointer"),
    "RL-10": ("GitTier.test_positive_rl10_rl16_rl17_and_bootstrap_replay", "GitTier.test_mutation_rl10_landing_without_a_finalized_record_and_with_two"),
    "RL-11": ("ImmutabilityRowsRule18.test_positive_rl11_shape", "ImmutabilityRowsRule18.test_mutation_rl11_hand_written_finalized_record"),
    "RL-12": ("RecordSchema.test_positive_migrated_slice", "RecordSchema.test_mutation_forbidden_key_in_a_committed_record"),
    "RL-13": ("ImmutabilityRowsRule18.test_positive_rl13_rl14_rows_identical_except_permitted", "ImmutabilityRowsRule18.test_mutation_rl13_change_one_character_in_a_historical_row"),
    "RL-14": ("ImmutabilityRowsRule18.test_positive_rl13_rl14_rows_identical_except_permitted", "ImmutabilityRowsRule18.test_mutation_rl14_instruments_row_changed"),
    "RL-16": ("GitTier.test_positive_rl10_rl16_rl17_and_bootstrap_replay", "GitTier.test_mutation_rl16_baseline_drift"),
    "RL-17": ("GitTier.test_positive_rl10_rl16_rl17_and_bootstrap_replay", "GitTier.test_mutation_rl17_second_introduction_of_a_migrated_record"),
    "RL-18": ("ImmutabilityRowsRule18.test_positive_rl18_sentinel_present_and_ratchet_holds", "ImmutabilityRowsRule18.test_mutation_rl18_ratchet"),
    "RF-01": ("GitTier.test_self_hosting_first_run_against_unmigrated_main", "GitTier.test_mutation_rf01_fetch_failure"),
    "RF-02": ("GitTier.test_positive_rf_happy_path_and_g06_determinism", "GitTier.test_two_branch_rehearsal"),
    "RF-03": ("GitTier.test_positive_rf_happy_path_and_g06_determinism", "GitTier.test_two_branch_rehearsal"),
    "RF-04": ("GitTier.test_positive_rf_happy_path_and_g06_determinism", "GitTier.test_mutation_rf04_leftover_stale_record"),
    "RF-05": ("GitTier.test_positive_rf_happy_path_and_g06_determinism", "GitTier.test_mutation_rf05_nothing_to_finalize_and_check_before_finalization"),
    "RF-06": ("GitTier.test_positive_rf_happy_path_and_g06_determinism", "GitTier.test_mutation_rf06_yaml_parse_failure_after_record_and_pointer_writes_rolls_back"),
    "RF-07": ("GitTier.test_positive_rf_happy_path_and_g06_determinism", "GitTier.test_mutation_rf07_missing_or_wrong_target"),
}
# Further mutation cases beyond the one-per-rule minimum RULE_TESTS records (H0→H1 repairs):
#   RF-06: test_mutation_rf06_lint_error_reverts_every_write, test_mutation_rf06_decode_and_filesystem_failures_after_first_write_roll_back,
#          test_mutation_reserved_allocation_cannot_be_consumed
#   RL-13: test_mutation_rl13_widened_whitelist_and_row_change_together
#   G-12:  CorpusDifferential.test_g12_gained_and_lost_sets_are_exact


class MetaTest(unittest.TestCase):
    """Every RL/RF id the two tools declare has a positive and a mutation case (AO-15)."""

    def test_every_declared_rule_has_positive_and_mutation_cases(self):
        declared = set()
        for script in ("register_lint.py", "register_finalize.py"):
            src = RL.read_bytes(os.path.join(TOOLS, script)).decode("utf-8")
            declared |= set(re.findall(r"\b(R[LF]-\d{2})\b", src))
        declared -= {"RL-15"}  # named in the docs only as the generated-view drift check Q-05 did not build
        self.assertTrue(declared >= {"RL-01", "RL-16", "RL-17", "RL-18", "RF-02", "RF-03", "RF-04"})
        missing = sorted(r for r in declared if r not in RULE_TESTS)
        self.assertEqual(missing, [], f"rules without test mapping: {missing}")
        module = sys.modules[__name__]
        for rule, (pos, mut) in RULE_TESTS.items():
            for name in (pos, mut):
                cls, meth = name.split(".")
                self.assertTrue(hasattr(getattr(module, cls), meth), f"{rule}: {name} does not exist")
            self.assertNotEqual(pos, mut, rule)
        self.assertGreaterEqual(len(declared), 24)

    def test_battery_is_not_vacuous(self):
        loader = unittest.TestLoader()
        n = loader.loadTestsFromModule(sys.modules[__name__]).countTestCases()
        self.assertGreater(n, 50)


if __name__ == "__main__":
    print(f"tests/test_register.py mode: {'--with-git' if WITH_GIT else 'offline'}")
    unittest.main(verbosity=2)
