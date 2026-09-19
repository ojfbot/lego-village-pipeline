#!/usr/bin/env python3
"""Acceptance battery for the design-package contract (HANDOFF-LEGO-PIPE-024-R1).

One command, from a clean checkout:

    python3 tests/test_design_package.py

Every case here is an enforcement claim the protocol makes. The PR #13 review round
found five defects that the *described* battery would have caught while it lived only
in a scratchpad — so it lives here now, runnable by a reviewer the way both reviews
were actually conducted. Fixtures are built from the committed package at run time;
nothing large is duplicated into the repository.

Needs PyYAML: re-execs itself under tools/.venv (tools/setup-preflight.sh creates it).
"""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(REPO, "tools")
sys.path.insert(0, TOOLS)

from schema_lint import check_against_schema, load_schema, require_yaml  # noqa: E402

yaml = require_yaml()

REGISTER = os.path.join(REPO, "docs", "correspondence", "REGISTER.md")
R1 = os.path.join(REPO, "docs", "design", "H-01-R1")
OVERLAY_R1 = os.path.join(REPO, "docs", "design", "manifests", "H-01-R1.overlay.yaml")

# Ground truths of record. R1_DIGEST is cited by the instruments table and the overlay;
# the .9 register note is the source of the drift counts.
R1_DIGEST = "b5664a2ad0ed7b7c7f093f4a1b369b32095799f73ade2af074b882e8038b9a1d"
R1_FILES, R1_BYTES = 98, 13058284
EMPTY_SHA = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def run(script, *args):
    p = subprocess.run([sys.executable, os.path.join(TOOLS, script), *args],
                       capture_output=True, text=True, cwd=REPO)
    return p.returncode, p.stdout + p.stderr


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def write_yaml(path, doc):
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(doc, f, sort_keys=False, allow_unicode=True)


class SchemaInterpreter(unittest.TestCase):
    """The shared interpreter must actually interpret — nulls and nested values included."""

    def setUp(self):
        self.schema = load_schema("design-package.v1")

    def test_all_required_keys_null_is_rejected(self):
        # Regression: null-skipping made "required" mean only "the key exists".
        doc = {k: None for k in self.schema["required"]}
        errs = []
        check_against_schema(doc, self.schema, errs)
        self.assertTrue(errs, "an all-null document must not validate")
        self.assertTrue(any("mock_math" in e for e in errs),
                        f"mock_math must be a required BOOLEAN, not merely present: {errs}")

    def test_null_allowed_only_where_declared(self):
        imp = load_schema("design-package-import.v1")
        errs = []
        check_against_schema({"archive_sha256": None, "package_path": None}, imp, errs)
        self.assertEqual([e for e in errs if "archive_sha256" in e or "package_path" in e], [],
                         "fields declaring null must accept it")

    def test_nested_supersedes_values_are_validated(self):
        # Regression: nested key presence was checked, nested values were not.
        errs = []
        check_against_schema(
            {"supersedes": {"design_package": "H-01", "revision": "not-a-revision",
                            "tree_sha256": "banana"}},
            self.schema, errs)
        self.assertTrue(any("supersedes.revision" in e for e in errs), errs)
        self.assertTrue(any("supersedes.tree_sha256" in e for e in errs), errs)

    def test_answers_items_are_validated(self):
        errs = []
        check_against_schema({"answers": ["not-a-memo-ref"]}, self.schema, errs)
        self.assertTrue(any("answers[0]" in e for e in errs), errs)

    def test_valid_supersedes_passes(self):
        errs = []
        check_against_schema(
            {"supersedes": {"design_package": "H-01", "revision": "R1", "tree_sha256": R1_DIGEST}},
            self.schema, errs)
        self.assertEqual([e for e in errs if "supersedes" in e], [])

    def test_required_nested_records_are_not_hollow(self):
        # Regression: required structured records declared field NAMES but no types,
        # so an all-null decisions/fixtures/known_defects/sheets entry validated.
        cases = [
            ({"decisions": {"ledger": None, "last_id": None, "count": None}}, "decisions"),
            ({"fixtures": {"set": None, "sha256": None}}, "fixtures"),
            ({"known_defects": [{"id": None, "rule_id": None, "paths": None,
                                 "expected_failure": None, "evidence": None,
                                 "status": None}]}, "known_defects"),
            ({"sheets": [{"id": None, "title": None}]}, "sheets"),
        ]
        for doc, key in cases:
            errs = []
            check_against_schema(doc, self.schema, errs)
            self.assertTrue([e for e in errs if e.startswith(key)],
                            f"{key} accepted an all-null record")

    def test_malformed_nested_values_are_rejected(self):
        errs = []
        check_against_schema({"decisions": {"ledger": "decisions.md", "last_id": "nope",
                                            "count": "three"}}, self.schema, errs)
        self.assertTrue(any("last_id" in e for e in errs), errs)
        self.assertTrue(any("count" in e for e in errs), errs)

    def test_overlay_reconstruction_is_not_hollow(self):
        errs = []
        check_against_schema({"reconstruction": {"authored_by": None, "date": None,
                                                 "sources": None}},
                             load_schema("design-package-overlay.v1"), errs)
        self.assertTrue([e for e in errs if e.startswith("reconstruction")], errs)

    def test_bool_is_not_an_integer(self):
        errs = []
        check_against_schema({"bytes": True}, load_schema("design-package-import.v1"), errs)
        self.assertTrue(any("bytes" in e for e in errs), "a flag is not a byte count")


class TreeDigest(unittest.TestCase):
    """The digest is normative or it is nothing: two importers must not disagree."""

    def test_reference_digest_of_the_committed_package(self):
        code, out = run("design_pkg.py", "digest", R1)
        self.assertEqual(code, 0, out)
        self.assertIn(R1_DIGEST, out)
        self.assertIn(f"file_count: {R1_FILES}", out)
        self.assertIn(f"bytes: {R1_BYTES}", out)

    def test_directory_symlink_is_an_error_not_an_empty_tree(self):
        # Regression: os.walk leaves symlinked dirs in dirnames, so a whole package
        # could hide behind one link and digest identically to an empty directory.
        with tempfile.TemporaryDirectory() as tmp:
            real = os.path.join(tmp, "real")
            os.makedirs(real)
            with open(os.path.join(real, "f.txt"), "w") as f:
                f.write("hi")
            pkg = os.path.join(tmp, "pkg")
            os.makedirs(pkg)
            os.symlink(real, os.path.join(pkg, "linked"))
            code, out = run("design_pkg.py", "digest", pkg)
            self.assertEqual(code, 1, out)
            self.assertIn("directory symlink", out)
            self.assertNotIn(EMPTY_SHA, out)

    def test_file_symlink_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "real.txt"), "w") as f:
                f.write("hi")
            os.symlink(os.path.join(tmp, "real.txt"), os.path.join(tmp, "link.txt"))
            code, out = run("design_pkg.py", "digest", tmp)
            self.assertEqual(code, 1, out)
            self.assertIn("symlink in tree", out)


class PinResolution(unittest.TestCase):
    """Acceptance outcome 1: a pin resolves to one row, or it fails loudly."""

    def _pin_file(self, tmp, pin_yaml):
        p = os.path.join(tmp, "booklet.md")
        open(p, "w", encoding="utf-8").write(f"---\ndesign_pin: {pin_yaml}\n---\n\nbody\n")
        return p

    def test_qualified_pin_resolves(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = self._pin_file(tmp, "{design_package: H-01, revision: R1, cut_state: as-committed}")
            code, out = run("design_pkg.py", "pin", f, REGISTER)
            self.assertEqual(code, 0, out)
            self.assertIn(R1_DIGEST, out)

    def test_bare_pin_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = self._pin_file(tmp, "H-01 R1")
            code, out = run("design_pkg.py", "pin", f, REGISTER)
            self.assertEqual(code, 1, out)
            self.assertIn("bare", out)

    def test_pin_without_cut_state_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = self._pin_file(tmp, "{design_package: H-01, revision: R1}")
            code, out = run("design_pkg.py", "pin", f, REGISTER)
            self.assertEqual(code, 1, out)
            self.assertIn("cut_state", out)

    def test_pin_to_an_unregistered_cut_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = self._pin_file(tmp, "{design_package: H-01, revision: R9, cut_state: as-exported}")
            code, out = run("design_pkg.py", "pin", f, REGISTER)
            self.assertEqual(code, 1, out)
            self.assertIn("no instruments row", out)

    # A pin must resolve to bytes; a cut that never landed must not resolve at all.
    REJECTED_ROW = ("\n| Instrument | Revision | Cut state | Governing brief | Path | "
                    "tree_sha256 | Archive digest | Imported at | Pinned by | Status |\n"
                    "|---|---|---|---|---|---|---|---|---|---|\n"
                    "| DT-DESIGN | R9 | as-exported | 014-R0 |  |  | none | .27 | — | rejected |\n")

    def _register_with(self, tmp, extra):
        p = os.path.join(tmp, "REGISTER.md")
        with open(REGISTER, encoding="utf-8") as f:
            base = f.read()
        with open(p, "w", encoding="utf-8") as f:
            f.write(base + extra)
        return p

    def test_rejected_cut_does_not_resolve_as_a_pin(self):
        with tempfile.TemporaryDirectory() as tmp:
            reg = self._register_with(tmp, self.REJECTED_ROW)
            f = self._pin_file(tmp, "{design_package: DT-DESIGN, revision: R9, cut_state: as-exported}")
            code, out = run("design_pkg.py", "pin", f, reg)
            self.assertEqual(code, 1, out)
            self.assertIn("landed no bytes", out)

    def test_row_without_a_valid_digest_does_not_resolve(self):
        row = self.REJECTED_ROW.replace("| rejected |", "| current |")
        with tempfile.TemporaryDirectory() as tmp:
            reg = self._register_with(tmp, row)
            f = self._pin_file(tmp, "{design_package: DT-DESIGN, revision: R9, cut_state: as-exported}")
            code, out = run("design_pkg.py", "pin", f, reg)
            self.assertEqual(code, 1, out)
            self.assertIn("no Path", out)

    def test_superseded_row_with_real_bytes_stays_addressable(self):
        row = ("\n| Instrument | Revision | Cut state | Governing brief | Path | tree_sha256 "
               "| Archive digest | Imported at | Pinned by | Status |\n"
               "|---|---|---|---|---|---|---|---|---|---|\n"
               f"| H-01 | R0 | as-exported | 007-R2 | `docs/design/H-01-R0` | `{'5d'*32}` "
               "| none | .27 | — | superseded |\n")
        with tempfile.TemporaryDirectory() as tmp:
            reg = self._register_with(tmp, row)
            f = self._pin_file(tmp, "{design_package: H-01, revision: R0, cut_state: as-exported}")
            code, out = run("design_pkg.py", "pin", f, reg)
            self.assertEqual(code, 0, out)
            self.assertIn("superseded", out)


class HistoricalCuts(unittest.TestCase):
    """The committed package and its overlay: the ground truth of record."""

    def test_committed_r1_passes_with_its_overlay(self):
        code, out = run("package_preflight.py", R1, REGISTER, "--overlay", OVERLAY_R1)
        self.assertEqual(code, 0, out)

    def test_reference_path_counts(self):
        _, out = run("package_preflight.py", R1, REGISTER, "--overlay", OVERLAY_R1)
        for fragment in ("'as-written': 5", "'stripped': 86", "'design_source': 11",
                         "'unresolved': 0", "'escape': 0"):
            self.assertIn(fragment, out, out.splitlines()[0])

    def test_runtime_defects_are_declared_never_verified(self):
        _, out = run("package_preflight.py", R1, REGISTER, "--overlay", OVERLAY_R1)
        for d in ("D-1", "D-3", "D-5", "D-6"):
            self.assertTrue(any(d in ln and "[declared]" in ln for ln in out.splitlines()),
                            f"{d} must be reported as declared, not verified")

    def test_cut_key_matches_its_instruments_row(self):
        _, out = run("package_preflight.py", R1, REGISTER, "--overlay", OVERLAY_R1)
        self.assertIn("matches its instruments row", out)


class CutKeyEnforcement(unittest.TestCase):
    """The cut-key ruling is enforced by exactly one check — it must not be bypassable."""

    def _overlay(self, tmp, **changes):
        doc = load_yaml(OVERLAY_R1)
        doc.update(changes)
        p = os.path.join(tmp, "o.yaml")
        write_yaml(p, doc)
        return p

    def test_wrong_digest_for_a_registered_cut_key_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            o = self._overlay(tmp, tree_sha256="de" + "ad" * 31)
            code, out = run("package_preflight.py", R1, REGISTER, "--overlay", o)
            self.assertEqual(code, 1, out)
            self.assertIn("two trees may not share one cut key", out)

    def test_unknown_cut_state_does_not_silence_the_digest_check(self):
        # Regression: a typo minted a new identity AND disabled the check protecting it.
        with tempfile.TemporaryDirectory() as tmp:
            o = self._overlay(tmp, cut_state="as_committed", tree_sha256="de" + "ad" * 31)
            code, out = run("package_preflight.py", R1, REGISTER, "--overlay", o)
            self.assertEqual(code, 1, out)
            self.assertIn("not in the register's declared list", out)
            self.assertIn("invented identity", out)

    def test_a_declared_state_awaiting_its_row_warns_but_passes(self):
        # A cut's instruments row is written at landing, after this check passes.
        with tempfile.TemporaryDirectory() as tmp:
            o = self._overlay(tmp, revision="R7")
            code, out = run("package_preflight.py", R1, REGISTER, "--overlay", o)
            self.assertEqual(code, 0, out)
            self.assertIn("went unchecked", out)
            self.assertIn("add the row in the landing PR", out)


class ImportRecords(unittest.TestCase):
    BASE = {
        "import_schema": "design-package-import/v1",
        "design_package": "H-01", "revision": "R1", "cut_state": "as-committed",
        "package_path": "docs/design/H-01-R1", "tree_sha256": R1_DIGEST,
        "archive_sha256": None, "archive_digest_status": "unavailable",
        "bytes": R1_BYTES, "file_count": R1_FILES, "disposition": "imported",
        "imported_at_register_version": "2026-09-18.26", "import_date": "2026-09-19",
        "imported_by": "Claude Code",
    }

    def _record(self, tmp, **changes):
        doc = dict(self.BASE)
        doc.update(changes)
        p = os.path.join(tmp, "r.import.yaml")
        write_yaml(p, doc)
        return p

    def test_matching_digest_verifies(self):
        with tempfile.TemporaryDirectory() as tmp:
            rec = self._record(tmp)
            code, out = run("package_preflight.py", R1, REGISTER,
                            "--overlay", OVERLAY_R1, "--import-record", rec)
            self.assertEqual(code, 0, out)
            self.assertIn("tree_sha256 verified", out)

    def test_digest_mismatch_is_never_waivable(self):
        with tempfile.TemporaryDirectory() as tmp:
            rec = self._record(tmp, tree_sha256="11" * 32)
            code, out = run("package_preflight.py", R1, REGISTER,
                            "--overlay", OVERLAY_R1, "--import-record", rec)
            self.assertEqual(code, 1, out)
            self.assertIn("never designer-waivable", out)

    def test_rejected_record_may_carry_no_bytes(self):
        errs = []
        doc = dict(self.BASE, disposition="rejected", package_path=None,
                   tree_sha256=None, bytes=None, file_count=None)
        check_against_schema(doc, load_schema("design-package-import.v1"), errs)
        self.assertEqual(errs, [], "a bounced Friday must still be recordable")

    def test_a_waiver_without_authority_grants_nothing(self):
        # A record with a defect_id and no authority is not a waiver (PR #13 re-review).
        with tempfile.TemporaryDirectory() as tmp:
            rec = self._record(tmp, waivers=[{"defect_id": "D-4", "authorized_by": None,
                                              "date": None, "memo": None, "disposition": None}])
            code, out = run("package_preflight.py", R1, REGISTER,
                            "--overlay", OVERLAY_R1, "--import-record", rec)
            self.assertEqual(code, 1, out)
            self.assertIn("grants nothing", out)
            self.assertIn("authorized_by", out)

    def test_a_valid_waiver_is_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            rec = self._record(tmp, waivers=[{
                "defect_id": "D-4", "authorized_by": "James",
                "date": "2026-09-19", "memo": "HANDOFF-LEGO-PIPE-024-R1",
                "disposition": "imported with the defect recorded"}])
            code, out = run("package_preflight.py", R1, REGISTER,
                            "--overlay", OVERLAY_R1, "--import-record", rec)
            self.assertEqual(code, 0, out)

    def test_imported_record_may_not_carry_null_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            rec = self._record(tmp, package_path=None)
            code, out = run("package_preflight.py", R1, REGISTER,
                            "--overlay", OVERLAY_R1, "--import-record", rec)
            self.assertEqual(code, 1, out)
            self.assertIn("disposition is 'imported'", out)


class DesignerCut(unittest.TestCase):
    """The end-to-end R2 rehearsal: what Claude Design will actually export."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.pkg = os.path.join(cls.tmp, "DT-DESIGN-R2")
        shutil.copytree(R1, cls.pkg, symlinks=False)
        import json
        idx_path = os.path.join(cls.pkg, "index.json")
        with open(idx_path, encoding="utf-8") as f:
            idx = json.load(f)

        def strip(x):
            return x[len("handoff/"):] if isinstance(x, str) and x.startswith("handoff/") else x

        idx["path_base"] = "."
        idx["tokens"] = strip(idx["tokens"])
        idx["brief"] = [strip(b) for b in idx["brief"]]
        idx["ledgers"] = {k: strip(v) for k, v in idx["ledgers"].items()}
        for s in idx["sheets"]:
            for k in ("spec", "standalone"):
                if s.get(k):
                    s[k] = strip(s[k])
            s["screenshots"] = [strip(x) for x in s.get("screenshots") or []]
        for st in idx["state_screenshots"]:
            st["file"] = strip(st["file"])
        if (idx.get("review_round") or {}).get("brief"):
            idx["review_round"]["brief"] = strip(idx["review_round"]["brief"])
        with open(idx_path, "w", encoding="utf-8") as f:
            json.dump(idx, f, indent=2)

        # A real designer cut PREPENDS its new decision: the ledger is newest-first.
        led = os.path.join(cls.pkg, "decisions.md")
        text = open(led, encoding="utf-8").read()
        row = ("| DEC-037 | 2026-09-25 09:00 | **index.json is package-internal navigation; "
               "DEC-028's single-source-of-status claim is retired.** | index.json | accepted "
               "| R2 | DEC-028 (authority claim) |\n")
        open(led, "w", encoding="utf-8").write(text.replace("| DEC-036 |", row + "| DEC-036 |", 1))
        cls.ledger_original = text

        cls.manifest = {
            "manifest_schema": "design-package/v1",
            "design_package": "DT-DESIGN", "revision": "R2", "cut_state": "as-exported",
            "cut": "2026-09-25", "manifest_origin": "designer", "path_base": ".",
            "governing_brief": "HANDOFF-LEGO-PIPE-014-R0", "answers": [],
            "supersedes": {"design_package": "H-01", "revision": "R1", "tree_sha256": R1_DIGEST},
            "maturity": "prototype", "tier_coverage": "tier-1", "mock_math": True,
            "index": "index.json",
            "sheets": [{"id": s["id"], "title": s["title"]} for s in idx["sheets"]],
            "decisions": {"ledger": "decisions.md", "last_id": "DEC-037", "count": 37},
            "fixtures": {"set": "village-fixtures-f5", "sha256": "00" * 32},
            "known_defects": [], "debts": [], "authoring_kit_version": "1.0",
        }
        cls._write_manifest()

    @classmethod
    def _write_manifest(cls, **changes):
        doc = dict(cls.manifest)
        doc.update(changes)
        write_yaml(os.path.join(cls.pkg, "package.yaml"), doc)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def tearDown(self):
        self._write_manifest()
        open(os.path.join(self.pkg, "decisions.md"), "w", encoding="utf-8").write(
            self.ledger_original.replace(
                "| DEC-036 |",
                "| DEC-037 | 2026-09-25 09:00 | **index.json is package-internal navigation; "
                "DEC-028's single-source-of-status claim is retired.** | index.json | accepted "
                "| R2 | DEC-028 (authority claim) |\n| DEC-036 |", 1))

    def test_happy_path(self):
        code, out = run("package_preflight.py", self.pkg, REGISTER, "--previous", R1)
        self.assertEqual(code, 0, out)
        self.assertIn("DEC-037", out)

    def test_sheet_id_as_package_name_is_rejected(self):
        self._write_manifest(design_package="A-01")
        code, out = run("package_preflight.py", self.pkg, REGISTER)
        self.assertEqual(code, 1, out)
        self.assertIn("not a sheet id", out)

    def test_designer_manifest_may_not_declare_a_prefix_strip(self):
        self._write_manifest(path_prefix_strip="handoff/")
        code, out = run("package_preflight.py", self.pkg, REGISTER)
        self.assertEqual(code, 1, out)
        self.assertIn("reconstruction-only", out)

    def test_superseded_governing_brief_is_rejected(self):
        self._write_manifest(governing_brief="HANDOFF-LEGO-PIPE-023-R1")
        code, out = run("package_preflight.py", self.pkg, REGISTER)
        self.assertEqual(code, 1, out)
        self.assertIn("superseded", out)

    def test_package_root_escape_is_an_error(self):
        import json
        idx_path = os.path.join(self.pkg, "index.json")
        original = open(idx_path, encoding="utf-8").read()
        try:
            idx = json.loads(original)
            idx["tokens"] = "../../../etc/hosts"
            open(idx_path, "w", encoding="utf-8").write(json.dumps(idx))
            code, out = run("package_preflight.py", self.pkg, REGISTER)
            self.assertEqual(code, 1, out)
            self.assertIn("escapes the package root", out)
        finally:
            open(idx_path, "w", encoding="utf-8").write(original)

    def test_editing_a_prior_decision_is_a_breach(self):
        led = os.path.join(self.pkg, "decisions.md")
        text = open(led, encoding="utf-8").read()
        open(led, "w", encoding="utf-8").write(text.replace("| DEC-030 | 2026-09-17 17:55 | **A-01",
                                                            "| DEC-030 | 2026-09-17 17:55 | **EDITED A-01"))
        code, out = run("package_preflight.py", self.pkg, REGISTER, "--previous", R1)
        self.assertEqual(code, 1, out)
        self.assertIn("DEC-030 changed beyond", out)

    def test_deleting_a_prior_decision_is_a_breach(self):
        led = os.path.join(self.pkg, "decisions.md")
        kept = [ln for ln in open(led, encoding="utf-8").read().splitlines(True)
                if not ln.startswith("| DEC-033 ")]
        open(led, "w", encoding="utf-8").write("".join(kept))
        code, out = run("package_preflight.py", self.pkg, REGISTER, "--previous", R1)
        self.assertEqual(code, 1, out)
        self.assertIn("DEC-033 removed", out)

    def test_permitted_status_transition_is_accepted(self):
        # A prior row MAY gain a supersession reference naming a new, higher id.
        led = os.path.join(self.pkg, "decisions.md")
        text = open(led, encoding="utf-8").read()
        old = "| DEC-028 | 2026-09-17 16:20 |"
        line = next(ln for ln in text.splitlines() if ln.startswith(old))
        cells = line.split("|")
        cells[5] = " superseded by DEC-037 "
        open(led, "w", encoding="utf-8").write(text.replace(line, "|".join(cells)))
        code, out = run("package_preflight.py", self.pkg, REGISTER, "--previous", R1)
        self.assertEqual(code, 0, out)
        self.assertIn("permitted transition", out)

    def test_missing_manifest_is_recorded_not_imported(self):
        os.rename(os.path.join(self.pkg, "package.yaml"), os.path.join(self.tmp, "held.yaml"))
        try:
            code, out = run("package_preflight.py", self.pkg, REGISTER)
            self.assertEqual(code, 1, out)
            self.assertIn("recorded, not imported", out)
            self.assertIn("previous pin does not move", out)
        finally:
            os.rename(os.path.join(self.tmp, "held.yaml"), os.path.join(self.pkg, "package.yaml"))


class DriftGroundTruth(unittest.TestCase):
    """Register note .9 is the answer key: the tool must reproduce it exactly."""

    def test_ledger_gate_fails_on_a_removed_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            new = os.path.join(tmp, "H-01-R1-edited")
            shutil.copytree(R1, new, symlinks=False)
            led = os.path.join(new, "decisions.md")
            kept = [ln for ln in open(led, encoding="utf-8").read().splitlines(True)
                    if not ln.startswith("| DEC-033 ")]
            open(led, "w", encoding="utf-8").write("".join(kept))
            code, out = run("package_drift.py", R1, new)
            self.assertEqual(code, 1, out)
            self.assertIn("BREACH", out)
            self.assertIn("Ledger gate: FAIL", out)

    def test_unchanged_trees_report_no_delta(self):
        code, out = run("package_drift.py", R1, R1)
        self.assertEqual(code, 0, out)
        self.assertIn("**0 changed · 0 added · 0 removed**", out)
        self.assertIn("Ledger gate: PASS", out)

    def test_drift_claims_file_level_evidence_not_semantic(self):
        out = run("package_drift.py", R1, R1)[1]
        self.assertIn("file-level change evidence", out)
        self.assertIn("unavailable", out)


def corpus_memos():
    """Every memo in docs/correspondence/, including frozen and expected-to-fail material."""
    root = os.path.join(REPO, "docs", "correspondence")
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d != "attachments")
        for name in sorted(filenames):
            if not name.endswith(".md"):
                continue
            if name in ("REGISTER.md",) or name.startswith(("ROUTING", "ARCHITECTURE")):
                continue
            out.append(os.path.join(dirpath, name))
    return sorted(out)


class MemoCorpusRegression(unittest.TestCase):
    """The shared interpreter also validates correspondence — it must not regress.

    The claim of record is that extracting the interpreter and correcting null handling
    changed NOTHING for the corpus. That is asserted here as a differential against a
    frozen copy of the pre-extraction validator (tests/fixtures/), over every memo —
    frozen and expected-to-fail material included — comparing exit code and output line
    by line. A claim in a memo is not evidence; this is.
    """

    OPERATIVE = [
        "HANDOFF-LEGO-PIPE-024-R1-design-package-protocol.md",
        "HANDOFF-LEGO-PIPE-023-R2-drafting-table-on-fixtures-and-the-program.md",
        "REVIEW-LEGO-PIPE-025-R1-review-of-design-package-protocol.md",
        "REVIEW-LEGO-PIPE-026-R0-chatgpt-review-of-design-package-protocol.md",
        "CORR-LEGO-PIPE-022-R0-chatgpt-reconciliation.md",
        "HANDOFF-LEGO-PIPE-019-R0-initial-handover-claude-code.md",
    ]

    def test_the_corpus_is_not_empty(self):
        self.assertGreaterEqual(len(corpus_memos()), 20, "corpus enumeration is broken")

    def test_operative_memos_still_pass(self):
        for name in self.OPERATIVE:
            path = os.path.join(REPO, "docs", "correspondence", name)
            code, out = run("memo_preflight.py", path, REGISTER)
            self.assertEqual(code, 0, f"{name}: {out}")

    def test_full_corpus_output_is_identical_to_the_pre_extraction_validator(self):
        # The frozen fixture resolves tools/.venv and tools/schemas/ relative to itself,
        # so it is staged inside tools/ for the run and removed afterwards. Both
        # validators therefore read the same schema files, not a frozen copy of them.
        fixture = os.path.join(REPO, "tests", "fixtures", "memo_preflight_pre_extraction.py")
        staged = os.path.join(TOOLS, "_pre_extraction_check.py")
        shutil.copyfile(fixture, staged)
        try:
            differences = []
            for memo in corpus_memos():
                before = run("_pre_extraction_check.py", memo, REGISTER)
                after = run("memo_preflight.py", memo, REGISTER)
                before_out = before[1].replace("_pre_extraction_check.py", "memo_preflight.py")
                if (before[0], before_out) != after:
                    differences.append(
                        f"{os.path.relpath(memo, REPO)}\n"
                        f"  before: exit={before[0]}\n{before_out}\n"
                        f"  after:  exit={after[0]}\n{after[1]}")
            self.assertEqual(differences, [], "\n\n".join(differences))
        finally:
            os.remove(staged)

    def test_authoring_kit_schema_mirror_has_not_drifted(self):
        # The kit Claude Design authors against must not diverge from canonical.
        # The hand-copied mirror drifted within one commit; it is generated now.
        code, out = run("design_pkg.py", "kit-mirror")
        self.assertEqual(code, 0, out)

    def test_frozen_v1_validator_is_untouched(self):
        p = subprocess.run(["git", "diff", "--quiet", "origin/main", "--", "tools/preflight.py"],
                           cwd=REPO, capture_output=True)
        self.assertEqual(p.returncode, 0, "tools/preflight.py is frozen — register rows cite it")


if __name__ == "__main__":
    unittest.main(verbosity=2)
