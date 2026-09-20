# CLAUDE.md — lego-village-pipeline

Digital twin + build harness for a multi-year LEGO Christmas village (play-well cluster).
The software turns designs into validated components, aggregates parts, subtracts inventory,
produces purchasing artifacts, and reconciles what was built. James (`@ojfbot`) is operator and
sole decision authority; sole user until the 2026-12-25 demo. Hard gate: **2026-10-21 ORDER-BY**
(BOM trusted enough to spend money against). BOM correctness outranks procurement optimisation;
the record outranks the automation — a retroactively-entered order with honest provenance is a
supported case, never a workaround.

## The correspondence system governs this repo

`docs/correspondence/REGISTER.md` is the index and authority. Read it first. Rules: **attach,
never paste** · filename is not identity · numbers never move once cited · collisions are
recorded, not repaired · numbers are allocated by the operator. Every memo passes
`tools/memo_preflight.py <memo> docs/correspondence/REGISTER.md` (version-dispatching; run
`tools/setup-preflight.sh` once per clone) before it can act as a work order. The v1
reference `tools/preflight.py` is frozen — cited by register rows, never edited.
**One register version per accepted landing (PR merge to `main`), assigned only at finalization against protected
`main` — never claimed on a branch, never bumped by hand (HANDOFF-LEGO-PIPE-032-R1, Q-02/Q-03).** A landing that touches
`docs/correspondence/` adds a note under `docs/correspondence/register/pending/`; its author runs
`tools/register_finalize.py` as the branch's last commit, the other steward reruns `tools/register_finalize.py --check`
to an empty diff, and `tools/register_lint.py --git` must exit 0 (the `register-lint` check on every such PR). The
register is the enumerated set rooted at `REGISTER.md` (`register/ALLOCATIONS.yaml`, `register/KNOWN-ANOMALIES.yaml`,
`register/MIGRATION-*.yaml`, `register/versions/`); history reads newest first via `tools/register_lint.py render`.

Current work order: `HANDOFF-LEGO-PIPE-019` (founding) executing `LEGO-PIPE-011-R2` (build
harness, Parts B–D; ADR amendments at the end of Parts C/D win over earlier text) and the design
package `docs/design/H-01-R1/` (build Tier 1 from it; defects D-1…D-6 are known first-day facts).
Design packages are governed by the design-package protocol (HANDOFF-LEGO-PIPE-024-R1): identity
is the cut key `{design_package, revision, cut_state}` in the register's instruments table; read
`docs/design/README.md` before touching anything under `docs/design/`.
Nothing beyond the authorised scope in 019 §6 — no production package boundaries before S1/S2/S7
report, no workflow UI before the schema gate, no Frame topology by scaffolding.

## Standing rules (019 §8, condensed — the memo is canonical)

- **Every UI is a frictionless teacher.** Plain words first; controls explain consequences; AI
  questions arrive as conversation. Where rigor conflicts with this on a family-facing surface,
  the teacher wins and the rigor moves operator-side.
- **Evidence axes stay separate** — origin · method · verification · authority · workflow. AI
  origin is permanently visible; the AI restates what it changed before save, announced via live
  region.
- **The accessibility tree is the agent-facing contract.** One `<h1>`, landmarks, `lang`,
  `<title>`, accessible names, live regions on derived/async changes, keyboard operation. A11y
  snapshot regression fails the build — treat it as a broken API.
- **Requests are first-class and never deleted.** Basis on every part row. Prices are ranges.
  Gates are stamps for the record, quiet modals for the act. Purchase stays outside the app.
- **People.** James is a friend of the family — never "Dad", never a parental role. The boys are
  EH, HH, LH. Kid-facing copy says "James" sparingly and never talks down.
- **All numbers in prototypes are MOCK MATH.** Design-package prototype code is a behaviour
  reference, never copied. `docs/design/H-01-R1/standalone/` is committed verbatim — never edit.
- **Vocabulary is under review** (RESEARCH-01): neutral `Item`/`Unit`/`Section` with TODO tags.
- Design direction: "Drafting Table" (paper/blueprint dual theme); tokens from the design
  package's `dt/tokens.css` are the single source of truth. Organic design system was scrapped.

## Fleet conventions

**Never push to `main` — PR-flow is in force (register v2026-09-18.14).** Every change,
correspondence landings included, lands branch → PR → merge. Branch names:
`corr/<memo-or-register-version>` for correspondence landings, `feat/…`/`fix/…` otherwise.
Merge authority: James merges; Claude Code and Codex (ChatGPT desktop agent) may self-merge
**only** PRs whose content James authorized by relay (file landings, instructed register
bumps) — never code, schema, or policy (Codex lane granted by register v2026-09-18.21). Operator relays authorize *content*; the PR is where the *commit* gets its review.
Enforcement: server-side branch protection on `main` + `main-guard.yml` (red X on bypass) +
per-clone hook — run `git config core.hooksPath .githooks` after cloning.

pnpm only, never npm. Vertical slices. Grill before non-trivial work. Log plan deviations to
`implementation-notes.md` `## Deviations`. Sibling content repo: `ojfbot/play-well-library`
(canonical content; branch flow `play/<user>` → `staging` → `main`). Northstar:
`.claude/northstar.md` (l1-lego-village-pipeline → l2-ojfbot).
