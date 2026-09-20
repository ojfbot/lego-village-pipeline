#!/usr/bin/env python3
"""register_finalize.py — deterministic, rerunnable, abortable, forward-only finalization of a
correspondence landing (HANDOFF-LEGO-PIPE-032-R1; R0 §5). The only writer of
register/versions/ and of REGISTER.md's version pointer (G-07).

Inputs: the branch's register/pending/*.md notes (frontmatter `affected_memos[]`,
`allocations_consumed[]`, optional `corrects`; body = the note), the fetched origin/main,
the branch head. No option changes the output; no clock, identity or environment value is
written. Two runs by two people on the same origin/main and branch head produce
byte-identical files (G-06).

Algorithm — each refusal fires at one named step (RR-32-04):
  1. `git fetch origin main`; RF-01 if the fetch fails. Capture `observed_main`, the exact
     fetched sha; every later step compares against it (RR-32-R2-02).
  2. RF-02 unless observed_main is an ancestor of HEAD — the branch must have MERGED current
     main, never rebased onto it. This is the check a stale branch fails. Remedy:
     `git merge origin/main`, rerun.
  3. Read the current version from observed_main:REGISTER.md; next = current + 1 (the date
     prefix is carried from the current version — no clock input). RF-04 if the branch
     already carries a register/versions/<v>.md not on observed_main with v != next (a leftover
     record from a run against an older base). Remedy: delete it, rerun. RF-05 if there is
     nothing to finalize (no pending notes).
  4. Re-fetch origin/main immediately before writing; RF-03 if the sha differs from
     observed_main AT ALL — an unrelated code merge included. Nothing is written.
  5. Concatenate the pending notes in filename order; write versions/<next>.md with
     kind: finalized, previous_version: current, finalized_from_main: observed_main,
     affected_memos, allocations_consumed, note_sha256. No landing_pr, no timestamp, nothing
     this run cannot itself attest to.
  6. Point REGISTER.md's version line at next; move each consumed allocation in_flight →
     landed with landed_version: next; delete the pending files.
  7. Serialise with the one fixed emitter; run register_lint; on any error revert every
     write of this run and exit non-zero.

--check reruns steps 1–4 exactly as a real run would and then recomputes, from the committed
finalized record's own inputs, what this algorithm would have produced — record bytes,
pointer line, ledger — and diffs. The reviewer's statement is "`--check` at base <sha> on
head <sha>: empty diff", valid only against the origin/main it names (RR-32-R3-07). CI runs
the same check against `git merge-base origin/main HEAD` (AO-19).

Usage: register_finalize.py [--repo DIR] [--check] [--remote NAME]
Exit: 0 · 1 refusal (RF-nn) or lint error · 2 usage/IO
Test hook (never for real use): REGISTER_FINALIZE_PAUSE_CMD is executed between step 3 and
the step-4 re-fetch so the battery can manufacture the RF-03 race.

Needs PyYAML: re-execs itself under tools/.venv (tools/setup-preflight.sh creates it).
"""
import os
import shlex
import subprocess
import sys

from register_lint import (REGISTER_DIR_REL, REGISTER_REL, Lint, Register, dump_yaml, git,
                           git_bytes, parse_record, read_bytes, record_bytes,
                           register_version_line, sha256, vnum, vprefix, write_bytes, yaml)
from register_migrate import NEW_VERSION_LINE

PENDING_REQUIRED = ("affected_memos", "allocations_consumed")


def refuse(code, msg):
    print(f"{code} REFUSED {msg}")
    return 1


def fetch_main(repo, remote):
    p = subprocess.run(["git", "fetch", "--quiet", remote, "main"], cwd=repo, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or "fetch failed")
    return git(repo, "rev-parse", f"{remote}/main").strip()


def pending_notes(repo):
    pdir = os.path.join(repo, REGISTER_DIR_REL, "pending")
    if not os.path.isdir(pdir):
        return []
    out = []
    for name in sorted(os.listdir(pdir)):
        if name.endswith(".md"):
            fm, body = parse_record(read_bytes(os.path.join(pdir, name)))
            for k in PENDING_REQUIRED:
                if not isinstance(fm.get(k), list) or not fm[k]:
                    raise ValueError(f"pending/{name}: {k} must be a non-empty list")
            out.append((name, fm, body))
    return out


def compute(current, observed_main, notes):
    """(next_version, record_frontmatter, body) — pure function of its inputs."""
    nxt = f"{vprefix(current)}.{vnum(current) + 1}"
    body = b"\n\n".join(b for _, _, b in notes)
    fm = {
        "register_version": nxt,
        "previous_version": current,
        "kind": "finalized",
        "finalized_from_main": observed_main,
        "affected_memos": sorted({m for _, f, _ in notes for m in f["affected_memos"]}),
        "allocations_consumed": sorted({a for _, f, _ in notes for a in f["allocations_consumed"]}),
        "note_sha256": sha256(body),
    }
    corrects = sorted({f["corrects"] for _, f, _ in notes if f.get("corrects")})
    if corrects:
        fm["corrects"] = corrects[0] if len(corrects) == 1 else ", ".join(corrects)
    return nxt, fm, body


def consume(ledger, consumed, nxt):
    """Move consumed allocations in_flight → landed; returns the new ledger dict."""
    keys = {e["key"] for e in ledger["allocations"]}
    missing = [k for k in consumed if k not in keys]
    if missing:
        raise ValueError(f"allocations_consumed names keys not in the ledger: {missing}")
    for e in ledger["allocations"]:
        if e["key"] in consumed:
            if e["state"] not in ("in_flight", "reserved"):
                raise ValueError(f"allocation {e['key']} is {e['state']}, not in_flight/reserved")
            e["state"] = "landed"
            e["landed_version"] = nxt
    return ledger


def pointer_line(regtxt, nxt):
    idx, _, _ = register_version_line(regtxt)
    lines = regtxt.split("\n")
    lines[idx] = NEW_VERSION_LINE.format(version=nxt)
    return "\n".join(lines)


def main(argv):
    args = list(argv)
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    remote = "origin"
    if "--repo" in args:
        i = args.index("--repo"); repo = os.path.abspath(args[i + 1]); del args[i:i + 2]
    if "--remote" in args:
        i = args.index("--remote"); remote = args[i + 1]; del args[i:i + 2]
    check = "--check" in args
    if check:
        args.remove("--check")
    if args:
        sys.stderr.write(__doc__ or "")
        return 2

    # step 1
    try:
        observed_main = fetch_main(repo, remote)
    except RuntimeError as e:
        return refuse("RF-01", f"cannot fetch {remote}/main: {e}")
    head = git(repo, "rev-parse", "HEAD").strip()
    # step 2
    if subprocess.run(["git", "merge-base", "--is-ancestor", observed_main, "HEAD"], cwd=repo).returncode != 0:
        return refuse("RF-02", f"{remote}/main {observed_main[:12]} is not an ancestor of HEAD {head[:12]} — the branch has not merged current main; run `git merge {remote}/main` (never rebase) and rerun")
    # step 3
    main_reg = git_bytes(repo, "show", f"{observed_main}:{REGISTER_REL.replace(os.sep, '/')}").decode("utf-8")
    _, _, current = register_version_line(main_reg)
    if current is None:
        return refuse("RF-01", f"{remote}/main REGISTER.md carries no version line")
    nxt = f"{vprefix(current)}.{vnum(current) + 1}"
    vdir_rel = REGISTER_DIR_REL.replace(os.sep, "/") + "/versions/"
    on_main = set(l.split("/")[-1] for l in git(repo, "ls-tree", "--name-only", observed_main, vdir_rel, check=False).split("\n") if l.strip())
    vdir = os.path.join(repo, REGISTER_DIR_REL, "versions")
    # Branch-side finalization products are `finalized` (or `bootstrap`) records only: the
    # migration's `migrated` records are the migrator's, proved by lint against the manifest —
    # on the migration branch itself origin/main has no versions/ yet (the Q-12 self-hosting case).
    branch_only = sorted(
        n for n in (os.listdir(vdir) if os.path.isdir(vdir) else [])
        if n.endswith(".md") and n not in on_main
        and parse_record(read_bytes(os.path.join(vdir, n)))[0].get("kind") != "migrated")
    stale = [n for n in branch_only if n[:-3] != nxt]
    if stale and not check:
        return refuse("RF-04", f"branch carries {stale} not on {remote}/main while next is {nxt} — leftover record(s) from a run against an older base; delete the stale record and rerun")
    try:
        notes = pending_notes(repo)
    except (ValueError, UnicodeDecodeError) as e:
        return refuse("RF-05", str(e))

    if check:
        # recompute from the committed record's own inputs and diff
        if stale:
            return refuse("RF-04", f"{stale} on this head do not name next {nxt} against {remote}/main {observed_main[:12]}")
        if not branch_only:
            return refuse("RF-05", f"no finalized record on this head beyond {remote}/main {observed_main[:12]}; {len(notes)} pending note(s) remain — not finalized")
        name = branch_only[0]
        fm, body = parse_record(read_bytes(os.path.join(vdir, name)))
        diffs = []
        if fm.get("finalized_from_main") != observed_main:
            return refuse("RF-03", f"{name} was finalized from {str(fm.get('finalized_from_main'))[:12]} but {remote}/main is {observed_main[:12]} — main moved since finalization; merge {remote}/main, delete the record, refinalize")
        merge_base = git(repo, "merge-base", f"{remote}/main", "HEAD").strip()
        if merge_base != observed_main:
            return refuse("RF-03", f"git merge-base {remote}/main HEAD = {merge_base[:12]} != {remote}/main {observed_main[:12]}")
        expected_fm = {
            "register_version": nxt, "previous_version": current, "kind": "finalized",
            "finalized_from_main": observed_main,
            "affected_memos": sorted(set(fm.get("affected_memos") or [])),
            "allocations_consumed": sorted(set(fm.get("allocations_consumed") or [])),
            "note_sha256": sha256(body),
        }
        if fm.get("corrects"):
            expected_fm["corrects"] = fm["corrects"]
        expected = record_bytes(expected_fm, body)
        if read_bytes(os.path.join(vdir, name)) != expected:
            diffs.append(f"versions/{name}: bytes differ from a deterministic re-emission (keys, order, digest or pointer fields)")
        regtxt = read_bytes(os.path.join(repo, REGISTER_REL)).decode("utf-8")
        if regtxt != pointer_line(regtxt, nxt):
            diffs.append(f"REGISTER.md version line is not the pointer to {nxt}")
        # ledger: origin/main's ledger with the consumption applied must equal the committed one
        try:
            main_ledger = yaml.safe_load(git_bytes(repo, "show", f"{observed_main}:{REGISTER_DIR_REL.replace(os.sep, '/')}/ALLOCATIONS.yaml").decode("utf-8"))
        except RuntimeError:
            main_ledger = None
        committed_ledger = read_bytes(os.path.join(repo, REGISTER_DIR_REL, "ALLOCATIONS.yaml"))
        if main_ledger is not None:
            # branch-side edits to the ledger (new reservations / in_flight entries) are legal;
            # what must hold is that every consumed key is landed at next, and the file is the
            # emitter's own output.
            branch_ledger = yaml.safe_load(committed_ledger.decode("utf-8"))
            if dump_yaml(branch_ledger).encode("utf-8") != committed_ledger:
                diffs.append("ALLOCATIONS.yaml is not the fixed emitter's serialisation")
            for e in branch_ledger["allocations"]:
                if e["key"] in expected_fm["allocations_consumed"] and (e["state"] != "landed" or e.get("landed_version") != nxt):
                    diffs.append(f"ALLOCATIONS.yaml: {e['key']} consumed by {nxt} but state {e['state']} / landed_version {e.get('landed_version')}")
        if notes:
            diffs.append(f"{len(notes)} pending note(s) still present after finalization")
        for d in diffs:
            print("  " + d)
        print(f"register_finalize --check at base {observed_main} on head {head}: {'empty diff' if not diffs else str(len(diffs)) + ' differences'} ({nxt})")
        return 1 if diffs else 0

    if not notes:
        return refuse("RF-05", "nothing to finalize: no register/pending/*.md notes on this branch")
    if branch_only:
        return refuse("RF-04", f"{branch_only} already present on the branch — finalized already; delete it to refinalize")
    nxt, fm, body = compute(current, observed_main, notes)
    # test hook — the RF-03 race is manufactured here, never in real use
    hook = os.environ.get("REGISTER_FINALIZE_PAUSE_CMD")
    if hook:
        hook_env = dict(os.environ)
        hook_env.pop("REGISTER_FINALIZE_PAUSE_CMD")  # the hook's own finalizer run must not recurse
        subprocess.run(shlex.split(hook), cwd=repo, check=False, env=hook_env)
    # step 4
    try:
        refetched = fetch_main(repo, remote)
    except RuntimeError as e:
        return refuse("RF-01", f"re-fetch failed: {e}")
    if refetched != observed_main:
        return refuse("RF-03", f"{remote}/main moved from {observed_main[:12]} to {refetched[:12]} between the ancestor check and the write — nothing written; `git merge {remote}/main` and rerun")
    # steps 5–7, with revert on error
    written, originals = [], {}

    def put(path, data):
        if path not in originals:
            originals[path] = read_bytes(path) if os.path.exists(path) else None
        write_bytes(path, data)
        written.append(path)

    def revert():
        for path, orig in originals.items():
            if orig is None:
                if os.path.exists(path):
                    os.remove(path)
            else:
                write_bytes(path, orig)
        for name, _, _ in notes:
            p = os.path.join(repo, REGISTER_DIR_REL, "pending", name)
            if p in removed:
                write_bytes(p, removed[p])

    removed = {}
    try:
        put(os.path.join(vdir, f"{nxt}.md"), record_bytes(fm, body))
        reg_path = os.path.join(repo, REGISTER_REL)
        put(reg_path, pointer_line(read_bytes(reg_path).decode("utf-8"), nxt).encode("utf-8"))
        ledger_path = os.path.join(repo, REGISTER_DIR_REL, "ALLOCATIONS.yaml")
        ledger = yaml.safe_load(read_bytes(ledger_path).decode("utf-8"))
        ledger = consume(ledger, set(fm["allocations_consumed"]), nxt)
        put(ledger_path, dump_yaml(ledger).encode("utf-8"))
        for name, _, _ in notes:
            p = os.path.join(repo, REGISTER_DIR_REL, "pending", name)
            removed[p] = read_bytes(p)
            os.remove(p)
        # pending/ must never be emptied: a landing that deletes every note while adding a
        # record with the same body makes git's directory-rename detection infer
        # pending/ → versions/ and relocate a concurrent branch's new note on merge (found in
        # the live rehearsal). The keep-file makes the directory survive.
        keep = os.path.join(repo, REGISTER_DIR_REL, "pending", ".gitkeep")
        if not os.path.exists(keep):
            put(keep, b"")
        reg = Register(repo)
        lint = Lint(reg, git_mode=True)
        lint.run()
        if lint.errs:
            for e in lint.errs:
                print("  " + e)
            raise ValueError(f"register_lint reported {len(lint.errs)} error(s); reverting this run's writes")
    except (ValueError, KeyError, RuntimeError) as e:
        revert()
        return refuse("RF-06", str(e))
    print(f"finalized {nxt} (previous {current}) from {remote}/main {observed_main} on head {head}: "
          f"{len(notes)} note(s), affected {fm['affected_memos']}, consumed {fm['allocations_consumed']}, note_sha256 {fm['note_sha256']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
