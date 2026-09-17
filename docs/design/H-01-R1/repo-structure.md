# Proposed fresh repo (for Claude Code)

> **UNADJUDICATED (K-4 · DEC-019).** The `apps/planner` / `apps/family` split and where the ledger lives are operator decisions James has not made. Claude Code may inspect the Frame fleet, run bounded spikes and submit alternatives with consequences; nothing below may be settled by scaffolding.

Monorepo, TypeScript, React, Three.js (fixed constraints). Frame is a dependency, not in this repo.

```
lego-village/
  packages/
    schema/          # THE contract. Entities from schema-requests.md land here as proposals → reviewed by @jfo.
    tokens/          # dt/tokens.css verbatim + a generated TS map; Frame alias layer lives here.
    ui/              # domain components (see index.json → components): RequestCard, BasisChip, StanceChip,
                     # OptionStateRow, PartPopover, PlantingRow, ChangePulse, DecisionLogEntry, EnvelopeBadge, StickerTile,
                     # ApprovalGate, EvidenceChips, SegmentedLine, StatusLine, ActionLog (15 total — matches index.json)
    geometry/        # canonical integer LDU for X/Y/Z (014 §7.1); studs/plates/bricks display-only; R40 math; envelope + fit checks (deterministic, tested); ONE representation read by 2D canvas and 3D viewer
    evidence/        # five-axis evidence model, chips, decision records, action log
    procurement/     # shop-combination search (exhaustive small-n, then heuristic), ranges, VendorProfile
    story/           # story graph: scenes, stickers, labels, requests → J11
  apps/
    planner/         # operator sheets: A-01 (split into viewer + canvas), B-01, C-01, P-01, J-01, Hub, H-01
    family/          # F-01 Family Workbench (same packages, tablet density, role-filtered)
  cli/               # deterministic libraries exposed as commands (BOM, fit, procurement plan) — audit surface
  docs/
    handoff/         # this folder, copied verbatim at import; decisions.md is append-only
    research/        # RESEARCH-01 and its glossary when it lands
  audits/            # independent agent audits of every "MOCK MATH" replaced by real math
```

## Working rules for the repo
- `docs/handoff/decisions.md` is append-only; a build that contradicts an entry needs a new entry first.
- Every screen imports tokens only via `packages/tokens`; no hex, no font names in app code.
- Every number shown carries its evidence chip (◇ AI GUESS · ■ MACHINE-CHECKED · ■ CONFIRMED · ▲ CORRECTED · ○ ON HOLD).
- Mocked AI calls become one client with the "restate before save" rule enforced in code.
- Naming of scale words waits for RESEARCH-01; use neutral internal names (`Item`, `Unit`) with a TODO tag until then.
