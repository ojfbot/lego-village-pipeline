---
type: northstar
slug: l1-lego-village-pipeline
tier: L1
app: lego-village-pipeline
ladders_up_to: l2-ojfbot
status: active
properties:
  - id: P1
    name: "The procurement spine is trusted with real money"
    target: "Geometry → BOM → release gate → order capture runs end-to-end on the railbed build; the 2026-10-21 ORDER-BY gate passes on software-produced artifacts (or a retroactive order is captured with honest provenance)."
    current: 0
    verification: "A released BOM + procurement plan James actually ordered against, with the ReleaseGate record and revalidation stamps in the repo; Q13 fit resolution verified by the six checks running in code."
    ladders_up_to: "ns:l2-ojfbot#P1"
  - id: P2
    name: "Decisions and provenance are captured and scale"
    target: "The correspondence register, decision ledger (DEC-*), ADRs, and per-order provenance survive every session; the 2026-12-25 demo can show the record, not just the artifact."
    current: 10
    verification: "Register version history in git; every memo preflight-passes; each order (live or retroactive) traceable to its release record and basis rows."
    ladders_up_to: "ns:l2-ojfbot#P2"
  - id: P3
    name: "Family-facing surfaces teach frictionlessly"
    target: "Post-demo: the family (EH/HH/LH + partner) uses the workbench surfaces on play branches without instruction; every UI passes the accessibility-tree contract and the teacher principle."
    current: 0
    verification: "A recorded family session per surface; a11y-tree snapshots green in CI; zero jargon-first labels on family sheets."
    ladders_up_to: "ns:l2-ojfbot#P1"
---

# Northstar — lego-village-pipeline (L1)

> NUMERIC CURRENTS/TARGETS ARE PROPOSALS (operator to calibrate). Registered at cluster
> founding (HANDOFF-LEGO-PIPE-019, 2026-09-17). Cluster: **play-well** — the cluster tier is
> designed-not-built fleet-wide, so this L1 ladders to l2-ojfbot directly (cluster-golf
> precedent); the play-well grouping lives in registry comments until the cluster tier ships.

**Vision.** A digital twin for a multi-year family LEGO Christmas village that plans and
delivers physical builds: designs become validated components, components aggregate into BOMs,
BOMs become purchasing artifacts, and what gets built is reconciled back — with every decision
and provenance chain on the record. The 2026-12-25 demo proves "software planned and delivered a
physical thing, and the method scales when the family picks it up."

## P1 — The procurement spine is trusted with real money

The critical line to the 2026-10-21 ORDER-BY gate: Q13 railbed geometry verified in code by
2026-10-14, then BOM → release gate → order capture dogfooded on the real Winter Holiday Train
railbed order. BOM correctness outranks procurement optimisation.

## P2 — Decisions and provenance are captured and scale

The record outranks the automation. The correspondence system (register + preflight), the design
package's DEC ledger, and per-order provenance are the demo's actual product. Current 10%
reflects the founded correspondence system.

## P3 — Family-facing surfaces teach frictionlessly

Deferred until after the demo (family arrives 2026-12-25+). Every UI is a frictionless teacher;
the accessibility tree is the agent-facing contract.
