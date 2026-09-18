# Correspondence and research — the collaboration schema between agents

**Status:** reference, as-built · **Describes the system at register `2026-09-18.18`** (§1a added at `.19`) · **Author:** Claude (Cowork), correspondence steward · **Date:** 2026-09-18
**Chart:** `attachments/ARCHITECTURE-correspondence-and-research.html` (lifecycle, transfer graph, identity anatomy, register row) — open in any browser.
**Relation to the record:** this document *describes*; it decides nothing. The decisions live in CORR-013 (register instituted), CORR-016-R1 / CORR-017-R2 (merged rules and v2 schema), CORR-021 (failure taxonomy, invariants, checklist, ratification), CORR-022 (ratification with amendments, PR-only contribution), register rules 1–17, and HANDOFF-023 §4–6 (program layer). Where this document and those disagree, they win and this document has a defect — open it as a register note.

---

## 0. Why this exists, and how to read it

Six parties — James, Claude (Cowork), Claude Code, Claude Design, ChatGPT, and GitHub as the record — cannot convene. They can only leave each other documents. Over two days (17–18 Sep 2026) the way they leave documents grew from "attach the memo" into a system with identity rules, a lifecycle, a schema with a validator, a transfer discipline, a single register under git, a PR-based contribution path, and a ratification procedure. It grew by failing eight times and writing each failure down.

This document is the one place that says what the whole system *is* — for a new session of any agent, for James six months from now, and for the tooling (validator, CLI, CI) that has to implement it. It is written to teach: each section states the mechanism, then the reason, then where it is implemented, then what is still missing.

Read §1 (the two classes) and §3 (the lifecycle) first. §11 (the worked example) is 023's own life, which exercised most of the system in one afternoon.

---

## 1. Two classes of document — and two more that pass through

| Class | What it is | Identity | Registered as | Mutability | Cited as |
|---|---|---|---|---|---|
| **Correspondence** | A *speech act* between agents: a work order, a review, a reply, a decision, a report | `PREFIX-LEGO-PIPE-nnn` + `R<n>` (rule 5) | A **row** in `REGISTER.md` | Repairable while unissued; frozen once issued; corrected only by revision or supersession (invariant 3) | prefix + number + revision, e.g. `HANDOFF-LEGO-PIPE-011-R2` |
| **Research** | A *knowledge document*: a brief, a strategy, an architecture sketch, a source survey. It informs decisions; it does not make them | Path + content sha256; internal R-amendment blocks (`## R1 amendments` appended, never rewritten) | A **version note** in the register's version line, never a row (`.12` precedent) | Amended by appended blocks; superseded by a new document or by an ADR derived from it | path, with `[verified]` / `[unverified]` on every claim inside |
| **Design package** (passes through — **black box today, see §1a**) | A cut of the design session's whole `handoff/` tree — sheets, specs, ledgers, standalones. Prototype fidelity throughout; every number MOCK MATH | **Borrowed:** the executing brief's row + a package label that is really a sheet ID (`H-01`) + the zip sha256. No manifest field carries revision, executes, or cut date | Not its own row: a note on the `HANDOFF-014` row and a version note on import (`.9`) | **Verbatim, never edited** under `docs/design/H-01-R<n>/`; only `decisions.md` grows (append-only) | revision + DEC-ids inside it |
| **Attachment** (passes through) | A chart, a data file, a script that travels with a memo | Named in the memo's `attachments:` frontmatter; identity is the memo's | Mentioned on the memo's row | Frozen with the memo | the memo, then the attachment path |

**The rule that separates the first two:** a correspondence document *asks or tells someone to do something* and therefore needs a number that never moves, a status, and an audit trail; a research document *says what is known* and therefore needs a hash and a verification convention. When a research document's conclusions become binding they do so by being carried into a memo or an ADR (`docs/architecture/`, with a pointer back) — the research file itself never acquires authority.

### 1a. The design package, dissected — a black box with borrowed identity

This is the least resolved component in the schema, and the one the 023 program leans on hardest (pin · cut · drift). Stated plainly so nobody builds on an assumption.

**What it is in the source.** A zip exported from the Claude Design session. Inside, one folder `handoff/`: `README.md` (how to read it), `index.json` (the manifest — sheets ↔ journeys ↔ components, ledger paths, decision ids, schema-request ids, state captures, known defects), `decisions.md` (DEC-001…035, dated, `supersedes`, status), `schema-requests.md`, `seam.md`, `open-questions.md`, `responsive.md`, `repo-structure.md`, `specs/` (one page per sheet + `ANNOUNCEMENTS.md`), `standalone/` (offline HTML of every sheet — the behaviour reference, whose code is never copied), `dt/` (tokens + runtime helpers + contrast checker), `a11y/` (tree baselines), `screenshots/` (+ `STATES.md`), `brief/` (copies of 007-R2 and RESEARCH-01), `check-manifest.mjs`, its own `CLAUDE.md`, `REVIEW-R1.md`, `ADDENDUM-A1-right-now.md`. **It carries no `lego-pipe-memo` frontmatter.** The preflight cannot read it; nothing in it states a revision, what brief it executes, or when it was cut, as a field.

**What it is in the schema.** Not a speech act; a deliverable that *executes* one (014-R0). Register rule 5 says `HANDOFF-` covers "work orders and design packages", but no package has ever had a `HANDOFF-` row of its own. Its identity today is assembled from three places: the executing brief's row ("executed by Claude Design as H-01 R1, zip sha256 `e898a64a…`"), the version note that imported it (`.9`: LATEST superset `e5b4857c…`, 10,013,923 bytes, 98 files, operator ruling on the R1-plus-addendum cut), and a label — **`H-01`** — which is the **sheet ID of the package's own Handoff sheet**, so the package is named after one of its members. Three meanings of "handoff" collide: the memo prefix, the export folder, the record sheet.

**Fidelity state (what the box contains, honestly).** Ten sheets at *prototype* fidelity: Hub, D-01, A-01, B-01, C-01, P-01, F-01, J-01, H-01, M-01, plus D-00 (direction). Tier 1 of 014 applied (WP0–WP4); Tiers 2–3 not started. Accessibility retrofit is Tier-1-scoped (A-01, C-01, P-01 have `role=main`; five sheets have no `<h1>`). Responsive: intent only (Q7). Every number is MOCK MATH. Six package-integrity defects are known first-day facts (019 §4.2 D-1…D-6: contrast fails its own check; drift checker crashes; A-01 loads Three.js from a CDN; `path_base` names unshipped folders; thin landmarks; a `file://` fetch). Two debts owed by Claude Design (G-1 journey hierarchy, G-2 per-sheet acceptance criteria). One operator item on the critical path (Q13). The design session's `prototypes/` sources are **not** in the package — only the built standalones are.

**Roadmap role (023 §5).** The package is the thing a dive *pins*; a new cut is the only way design reaches build; the drift checker diffs cuts; the `decisions.md` ledger is the shared truth between design and build. Two cuts are scheduled (R2 on 3 Oct, R3 on 17 Oct). None of that works reliably while the package's identity is borrowed and its manifest is free text: a drift report needs `revision` and `supersedes` as fields, a pin needs a hash it can cite, and a register row needs an identity that isn't a sheet ID.

**Export → import, as practised (019 §1.4, `.9`).** (1) Claude Design exports the zip; James downloads it. (2) James attaches it to Cowork or places it where Claude Code can read it; sha256 computed. (3) Claude Code commits the whole `handoff/` tree verbatim to `docs/design/H-01-R<n>/`, `standalone/` and `dt/` together (relative loads), records the sha256 and byte count in the register version note and on the executing brief's row, diffs `decisions.md` against the previous revision to confirm append-only. (4) Cowork writes a readiness verdict (019 §4) — package-level review, not prototype QA. (5) Build pins it by name in the next briefing.

**Proposal to resolve (not a decision — for James, then Claude Design at cut R2):**

1. **A manifest with fields**, `package.yaml` at the archive root, beside `index.json`: `design_package: <name, not a sheet id>` · `revision: R2` · `executes: HANDOFF-LEGO-PIPE-014-R0` (or the change request it answers) · `cut: 2026-10-03` · `supersedes: R1` · `sheets: [...]` with fidelity per sheet (`prototype · tier-1 · tier-2 …`) · `decisions: DEC-001…DEC-0nn` · `known_defects: [...]` · `debts: [...]`. The importer records `sha256` and `bytes` beside it. The drift checker reads this, not free text.
2. **A second register table for instruments** — proposed in 017 §1.2 (S-08), never landed. Design package cuts get rows there (name · revision · executes · sha256 · imported at version · pinned by dives); correspondence keeps the first table. Research documents could join later.
3. **Rename the package label** so it stops colliding with the H-01 sheet: `LVP-DESIGN R2`, or whatever James prefers — the name is register data.
4. **Fix `path_base`** to name the shipped root, and ship the drift checker against it (Dive 1, D-2).

Until 1–3 land, the schema should say what is true: *a design package is identified by the executing brief's row plus a zip hash, and its revision label is informal.*

**Threads** partition correspondence by subject and are register data, not a validator enum (rule 16): `design`, `build-harness`, `correspondence-governance`, `cluster`; `app-stack` proposed by 023. Research is filed by *component* (`build-harness/`, `mils-integrator/`, `studio-bridge/`), which is not the same partition — a component's research may feed several threads.

---

## 2. Identity — what a number is, and what it is not

Anatomy: `HANDOFF-LEGO-PIPE-023-R1`

| Part | Meaning | Rule |
|---|---|---|
| `HANDOFF-` | Type prefix: `HANDOFF-` (work orders, design packages), `CORR-` (reconciliation, replies, reports), `REVIEW-` (independent reviews). Two documents may share a number if their prefixes differ | 4, 5 |
| `LEGO-PIPE-` | The register's namespace: one monotonic sequence across every thread and every provider | 13 |
| `023` | The number. **James allocates** (or delegates one allocation); an agent never infers a free number from a mirror. Recorded as *reserved* before drafting. Never reused, never moved once the memo has reached an agent. Consumed by reservations and abandoned drafts alike | 1, 2, 3 |
| `R1` | The revision. Same speech act, same author, recipients, authority, purpose and scope — corrected or extended. Consumes no number. A reply, a review, a decision, a new authorization, changed recipients, changed authority or materially changed scope needs a **new number** | 6, 7, 8 |

Three things identity is **not**:

- **Not the filename** (rule 15, F-06). Mirrors rename files; the row carries canonical path, aliases, and the sha256 as transferred. `LEGO-PIPE-012-R0-Review-of-…md` and `REVIEW-LEGO-PIPE-012-…md` are one document, proven by hash (X-07).
- **Not the frontmatter's own claim.** 015's file still says `document_id: CORR-LEGO-PIPE-011`; the register says 015. The file is byte-frozen; the register supplies the canonical form (X-01, X-02). `issued_as` records the number a file *was issued under* when that differs; it is provenance, not a second identifier.
- **Not repaired when it collides.** 009 (CORR vs HANDOFF-009-R1), 010 (design vs build-harness), 011/015: both rows stay; disambiguate by prefix, then by thread. "Mis-numbered" was withdrawn as a word (`.6`).

**Transfer identity** is separate from document identity: it is the sha256 of the bytes that moved (invariant 2). A document without a stated hash has not been transferred, only *received*.

---

## 3. Lifecycle — the states a memo passes through

```
                 James allocates                    preflight passes · frozen · row · verifiable transfer
   draft ───────► reserved ───────► for_review ────────────────────────────────────► issued
                                    for_reconciliation                                  │
     ▲                                     │                                            ├──► accepted
     │  repair the SAME revision           │  repair the SAME revision                  ├──► accepted_work_order
     └─────────────────────────────────────┘  (unissued: rule 12, invariant 3)          ├──► closed
                                                                                        ├──► withdrawn
   received ── (arrived without hash / by paste / reconstructed) ── row says so ──►    └──► superseded  ── by a NEW number or a NEW revision;
   never becomes issued until the sender's bytes arrive with a hash (F-01, X-08)             both rows record it; the old number stays valid (rule 10)
```

**Issuance** (rule 9) is the gate everything hinges on. Five conditions, all required: operator authorization or delegated authority; a frozen revision; a passing preflight; a row in the canonical register; a verifiable transfer. Creating, pasting or mentioning a draft does not issue it. A memo that is *on disk* is not thereby *dispatched* (018's row: "file possession is not dispatch").

**Repair** has two shapes and the state decides which (rule 12): unissued → fix the same revision in place, record it in the change log (016 §3.8 precedent; 023-R1 did this at `.17`); issued → a new revision, or a superseding memo under a new number. Nothing that has reached an agent is edited in place.

**Work-order capacity** is a further gate on top of *issued*: a memo acts as a work order only if it is issued, passes the *operative* validator, and carries authorization state. 018 is issued-in-content, ratified-in-schema, and still non-operative because no v2-aware validator has passed it (rule 14, X-04).

**Status enums.** v1 (operative validator): `draft · for_review · for_reconciliation · accepted · accepted_work_order · superseded`. v2 (ratified): adds `reserved · issued · closed · withdrawn`. The register row's status text is prose and may say more than the enum ("for review — number proposed; James confirms").

---

## 4. Schema — v1 operative, v2 ratified, one validator that knows only v1

| | `lego-pipe-memo/v1` | `lego-pipe-memo/v2` |
|---|---|---|
| Standing | **Operative**: the committed `tools/preflight.py` validates it | **Ratified** 2026-09-18 (`.13`, CORR-022) with two amendments; governs new memos; **no v2 work order acts until a v2-aware validator passes it** (rule 14) |
| Required keys | `correspondence_schema · memo · revision · status · memo_type · title · date · from · to · thread · cluster · repos · tags · argument · parts · provenance` | fifteen: as v1 minus `cluster/repos/tags/parts` (optional / conditional), plus `authority · register`; `parts` required for handoff and work_order; `findings` required when the memo raises or disposes findings |
| `memo_type` | `handoff · review_response · decision · work_order · findings · review` | adds `correspondence · addendum` |
| `from` / `to` | string or mapping / list of strings, mapping, or list of mappings | mapping / list of `{actor, role, provider}` only |
| `argument` | should begin "In which" (warning) | must begin "In which" |
| Finding IDs | body pattern `[RNC]-\d{1,2}` must be declared in `findings:` — **also matches sheet IDs** `C-01` (F-05), so a memo without `findings:` may mention sheets freely and a memo with it must declare them | reserved namespace `(R|N|X|S|Q|K)-\d{2}`: `R-` review finding · `N-` new finding · `X-` registered disagreement · `S-` process finding · `Q-` open question · `K-` settled constraint · `OD-`/`D-` operator decision. Letters `A C F H J P` are **sheet** prefixes and invalid for findings. 021's `F-01…F-08` are frozen legacy aliases for `S-15…S-22` (X-05) |
| Retired in v2 | — | `document_id · document_type · version · finding_ids · trailer block · to as string` |
| Migration | Legacy files stay byte-frozen with `schema: legacy` on the row; transition memos (`.13`: 016-R1, 022; `.15`–`.17`: 023) authored v1 so they can pass; 011-R3, 014-R1 convert on revision | v2 from birth once the validator dispatches on `correspondence_schema` |

**Why two schemas coexist.** Ratification is a decision James makes; validator capability is code Claude Code writes (011-R2 scope item 2: a versioned JSON Schema + CLI replacing `preflight.py`). Separating them (X-04) is what lets the protocol advance without a single memo pretending the tooling exists.

---

## 5. Transfer — how bytes move between venues, and what counts

| Channel | Counts as transfer? | Record on the row |
|---|---|---|
| **File attachment** with its sha256 stated by the sender, verified by the receiver | Yes (rule 11) | `sha256` as transferred; receiver preflight result |
| **Repository-native**: repo + canonical path + commit SHA + content sha256, for a recipient with repository access | Yes — equivalent to attachment (022 amendment 2) | same, plus commit |
| **Paste** into a chat | **Never** (F-01). Content may be complete; it has no hash. Record *received*, keep the reconstruction with a receipt note itemising what was restored; moves to *issued* only when the sender's file arrives | `received, not issued`; reconstruction sha256 |
| **Mention** ("I've drafted 024…") | Not a transfer, not an issuance (rule 9) | nothing |

**Who can reach the repository directly:** Claude Code (commit, push, PR, merge only when operator-authorized by relay); ChatGPT (branch, commit, draft PR — never `main`, never self-merge; rule 17, 022 §4); Claude (Cowork) (commit on a branch through the linked Mac; **cannot push** — no credentials in its VM; James pushes and opens the PR); James (everything, and the only merge to `main`). **Who reads a mirror:** Claude Design and ChatGPT read the register and memos as copies; every copy states the version it copied (invariant 5). The chart's transfer graph draws this.

**Receiver duties on every transfer:** preflight against the operative schema; verify the hash if one was stated; record the received hash; refuse to act on a failure. The register's own rows show the discipline working: 018 "rejected by v1 on `schema id` + `status issued` exactly as its row records"; 009 and 009-R1 "crash the v1 reference script" — recorded, not hidden.

---

## 6. The register — one file, under git, that is the authority

`docs/correspondence/REGISTER.md` on canonical `main` of `ojfbot/lego-village-pipeline`. Authority transferred to it at commit `5446e6e` (`.6`); before that the claude.ai project copy held it by convention. It governs the whole play-well cluster, both repos, and may move to a repo of its own only by a recorded authority transfer that never re-keys anything.

**What it contains, top to bottom:**

1. **Authority line** — names itself and its home.
2. **Version line** — `2026-09-18.17`, bumped on **every** edit and by **every** commit that touches `docs/correspondence/` (a rule in `CLAUDE.md`). The version note is a running log: what landed at this version, hashes, deviations, research landings, in-place repairs. Superseded versions are listed with why each is stale.
3. **Rules in force** — currently seventeen (§1–5 above paraphrase them; the register's wording wins).
4. **The table** — one row per correspondence identity: number · canonical path · type · thread · author · status prose (which carries: sha256 as transferred, aliases, preflight result, collision notes, supersession, `issued_as`, dispatch state, what it lands or waits on). `023+ / 024+ next free` closes the table.
5. **Resolved** — the 010 collision narrative.
6. **Notes** — schema status, validator status, open defects (the finding-ID/sheet-ID shadowing), current contribution path.

**Mirrors** (the claude.ai project's `correspondence/`, ChatGPT's project, any attachment in circulation) are read-only copies refreshed by copy. James's standing instruction: the project is a mirror, never a home.

**Concurrency** is solved by PR-flow (`.14`): every change to `main`, register deltas included, lands by pull request; James merges; Claude Code may self-merge only content the operator authorized by relay. Server-side branch protection on `main` (PR required, admins included), `main-guard.yml` turning red on any bypass, and `.githooks/pre-push` per clone. A contributing steward puts its memo **and** its register delta in one PR (X-06) so the row and the file land atomically. "No concurrent register editing" forbids competing direct writes, not competing PRs.

**Register maintainer** is a role (Claude Code: `implementing_agent_and_register_maintainer`); stewards propose deltas, the maintainer or James applies them. In practice, at `.15`–`.17`, Cowork wrote its own rows on a branch — permitted because the branch is a proposal until merged.

---

## 7. Actors — the roles the protocol names, and their venues

| Actor | Protocol role (as written in frontmatter) | Venue | Reaches the register how |
|---|---|---|---|
| James (`@ojfbot`, `@jfo` in design) | `operator_and_final_authority` — decision owner, dispatch authority, number allocator, merger, ratifier | Mac terminal; every chat; Claude Design | Directly; the only merge to `main` |
| Claude (Cowork) | `correspondence_steward` / `coordinating_reviewer_and_handoff_author` | Cowork sessions on the LEGO Village project, linked to the Mac | Branch commits through the linked folder; push and PR by James |
| Claude Code | `implementing_agent_and_register_maintainer` | The repo, CI, its own sessions | Commit, push, PR; landing commits for migrations; self-merge only by relayed authorization |
| ChatGPT | `peer_correspondence_steward` / `independent_reviewer` (widened by 023-R1 to design + architecture proposals) | Its own project; GitHub connection | Branch + draft PR only (rule 17) |
| Claude Design | `design_agent` | The design session and its project | Never directly: emits a package cut, imported verbatim by Claude Code (019 §1.4) |

**Named stewards and the ratification procedure** (021 §D as amended by 022): a protocol change is *proposed* in a `CORR-` memo carrying the full contract; each steward *returns* confirmation or an `X-nn` disagreement with remedy (silence is not assent); the *operator ratifies* and the register records it and the version; until then the prior contract is operative and anything written in the new one is a draft; during migration the validator accepts both and the register says which is operative. This is how v2 went from proposed (016/017) to ratified (022) in a day without the agents ever being in the same room.

---

## 8. Research documents — how knowledge enters and stays honest

Five documents live under `docs/research/<component>/`, migrated verbatim from the claude.ai project at `.12` with sha256s in the landing commit. Conventions they already follow, now stated as the rule:

- **No memo identity, no row.** Their register record is the version note that landed them. They are cited by path.
- **Every claim carries `[verified]` or `[unverified]`** — verified means read from the primary source in that session; unverified means prior knowledge or secondary. The claim, not the document, carries the tag.
- **Amendment by appended block.** `storage-architecture-asset-versioning.md` carries its R1 amendments as a second heading; the 011-R2 convention — amendments win over earlier text, earlier text is not rewritten.
- **Sources are declared** with date compiled and the primary pages read; licensing is a first-class column where the research is about data sources.
- **Derived authority goes elsewhere.** When research settles into a decision, an ADR is written under `docs/architecture/` with a pointer back; the research file is not promoted in place. Registered memos with ADR content (009-R1, 010 build-harness) *stay at their registered paths* (`.11` placement decision); derived ADRs point to them.
- **Concatenations are recorded, not silently split.** Three of the five files each hold two documents; the version note says so and the operator rules on splitting.

**What research is not:** RESEARCH-01 (nomenclature) is *inside* the design package (`brief/RESEARCH-01-nomenclature.md`) because the design session commissioned it; it is a research document by kind and a package member by location. Q1 and the schema-naming freeze depend on it.

**Gap:** there is no research index. Five files are findable by `ls`; fifty will not be. A `docs/research/INDEX.md` mirroring the register's shape — path, component, date compiled, status (research · pre-ADR · superseded by ADR-nnnn), sha256, which memos cite it — is the obvious next artifact and is not yet authorized by anyone.

---

## 9. The session checklist — what every agent runs

From 021 §C, amended by 022. Six steps; none optional; this is the part of the system that lives in behaviour rather than in files.

**Open.** (1) Read the register from the authority; state its version in your first message; if you can only reach a mirror, say which and treat every number as provisional. (2) Before acting on any memo: preflight against the operative schema; verify the stated hash. A memo that fails may be read by a human and may not act.

**Work.** (3) Author in the *operative* schema; state the register version read in the frontmatter (`register_version_read`); declare every finding ID you cite. (4) Transfer by attachment with sha256 — or repository-native for a recipient with repo access. Paste is not transfer.

**Close.** (5) Land it in the authority repo, committed by an agent that can commit; verify afterwards — path, byte count, hash — and report all three. (6) Propose the register delta you need in the same PR; do not race another agent on `main`.

---

## 10. Implementation surface — what exists, what is planned

| Piece | Status | Where |
|---|---|---|
| Register | live, `.17` | `docs/correspondence/REGISTER.md` |
| v1 reference validator | live; checks: frontmatter present, no tabs, no duplicate top-level keys, required keys and types, schema id pinned, status and memo_type enums, "In which" (warn), finding IDs used ⊆ declared, `in_reply_to` and `supersedes` targets present in register, "already listed" warning. **Crashes** on pre-v1 files (009, 009-R1) — input to its replacement | `tools/preflight.py` (needs PyYAML; system python on the Mac lacks it) |
| v2-aware validator: versioned JSON Schema + CLI dispatching on `correspondence_schema`, reserved finding namespace, v2 enums | **live at `.20`** — `memo_preflight.py` + `schemas/lego-pipe-memo.{v1,v2}.schema.json`; 018's validator gate met (register row wins on operative status) | `tools/` |
| PR-flow enforcement | live: branch protection on `main`; `main-guard.yml`; `.githooks/pre-push` (activate per clone: `git config core.hooksPath .githooks`) | `.github/workflows/`, `.githooks/` |
| Commit convention | memo-shaped commit messages ending in the session's attribution lines; every correspondence commit names the register version it produces | `CLAUDE.md` |
| Attachments folder | new at `.15`: charts and files that travel with a memo, named `<memo-id>-<slug>.<ext>`, declared in the memo's `attachments:` | `docs/correspondence/attachments/` |
| Proposals folders | proposed by 023-R1 §4.1 for ChatGPT's design and architecture proposals | `docs/design/proposals/`, `docs/architecture/proposals/` |
| Program board | proposed by 023-R1 §6.4 | `docs/program/` |
| Research index | gap (§8) | — |
| Cowork landing skill | `lego-pipe-land-memo` — draft, preflight, register bump, branch commit on the Mac; James pushes and opens the PR with `--head` | Cowork skill |

---

## 11. Worked example — the life of 023, which exercised most of this in one afternoon

1. **Read at the wrong version.** Cowork read the register at `.12` on `main` and drafted as **022**. James's current branch held `.14`, where 022 had gone to ChatGPT's reconciliation and v2 had been ratified. Lesson: read the register **on the branch the operator is on**, not just `main` (checklist step 1, sharpened). Renumbered to **023** before any transfer — permitted, because the draft had reached no agent (rule 3).
2. **Authored v1 under the migration.** v2 governs new memos, but the validator is v1-only; 023 was authored v1 like the `.13` transition memos, with a note that it re-issues as v2 before acting as a work order (rule 14).
3. **Landed by branch, not push.** Committed on `correspondence/023-…` through the linked Mac; the Cowork VM has no GitHub credentials, so James pushed and opened the PR (F-08: say which channel cannot do what).
4. **Register bumps `.15`, `.16`, `.17`** — one per commit touching correspondence, each note saying what landed.
5. **R0 → R1 by revision, not new number.** Same author, recipients (widened — arguably a rule-7 trigger; recorded in the change log for James to rule), authority, purpose; R0's row marked *superseded by R1*, its number and citations intact (rules 6, 10).
6. **Repaired in place while unissued.** ChatGPT's authority widened at `.17` as an in-place edit of R1 with a change-log line (rule 12, 016 §3.8 precedent) — because R1 had not been issued to anyone.
7. **Attachment convention born.** The chart travels under `attachments/`, declared in frontmatter, published in parallel as an artifact for phone viewing; the repo copy is canonical.
8. **Reland.** James opened `corr/023-reland-to-main` rebasing R0 onto the merged `.14`; R1's commits sit on the older branch pending a cherry-pick — an ordinary PR-flow reconciliation, resolved by the operator, not by force-push (022 §4.6).

Everything above is verifiable in `git log` and the register's version notes. That is the point of the system.

---

## 12. Open items this document surfaces (not decisions — a list for James)

- v2-aware validator (011-R2 item 2) — gates 018 and every v2 memo.
- 008 has no file anywhere (F-07); the row says so.
- Research index (§8).
- `register_version_read` is a v2 key; v1 transition memos carry it informally — decide whether the v1 validator should warn when it is absent.
- Thread `app-stack` — proposed by 023, needs a register ruling (rule 16).
- Whether widening recipients at R1 (023) is a rule-7 new-number trigger — ruling wanted so the precedent is clean.
- `docs/correspondence/attachments/` — ratify the naming convention or move attachments beside their memos.
- **Design package identity (§1a):** manifest with fields, an instruments table (017 §1.2 S-08), a package name that is not a sheet ID — needed before cut R2 for the pin / drift loop to be trustworthy.

— Claude (Cowork), correspondence steward · register version read `2026-09-18.18` · decisions by James (`@ojfbot`)
