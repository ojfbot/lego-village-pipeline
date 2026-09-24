---
title: "The Village That Learns — Medium article-series plan"
status: editorial-plan
owner: James
updated: 2026-09-24
audience: technical operators, engineering leads, product designers, and people experimenting with agentic application delivery
authority: none
---

# The Village That Learns

*Building a family LEGO Christmas village one bag — and one year — at a time.*

This is the editorial plan for a ten-article Medium series about the LEGO Village
Pipeline. It is not a project work order and does not authorize implementation.
Repository facts must be rechecked before each article is drafted.
Dated source snapshots, draft links, and claim ledgers belong with the individual
article, not in this durable series plan.

## Governing hypothesis — James's clarification, 2026-09-23

An agentic application stack could help a family grow from one LEGO set into a
planned railway display integrating new official sets, community MOCs, and its own
modifications, sustainably across years, budgets, schedules, and busy lives.
Whole-family participation requires multiple ways into the same village, with
appropriate controls, gates, and protections. The system should document decisions
as work happens, teach at the point of need, and carry learning through play into
the next build and the next season.

The stack draws inspiration from ERP and construction-management functions and
from NASA systems-engineering practices that James is incorporating into ojfbot.
These are design influences and a hypothesis to test, not claims that an ERP
product, a NASA-compliant system, or the family workflow has been delivered.

The village is simultaneously a practical setting for learning agentic application
and system design. James intends to open-source the software and share publishable
designs, documentation, and lessons so others can build their own LEGO planning
and building tools. Record that as intent until release and reuse evidence exists.

The railbed is the first bounded test. A completed railbed alone cannot establish
multi-year sustainability, whole-family usability, or reuse by other builders.
The series must report evidence for those outcomes as it arrives, including the
possibility that maintaining the stack costs more time than it saves.

James's origin account: last year's Family Christmas Tree prompted this year's
train addition and the question of growing a scene like the master builders on
YouTube create. Keep the growing world open to play: no Kragle, stories can change
the scene, and family ideas help determine what to build next. Christmas-market
language supplies places and activity—stalls, paths, arrivals, gathering—without
inventing a family memory. AI helps organize making those ideas real.

## The editorial correction

The village is the protagonist. The agents, application, schemas, tools, reviews,
and delivery infrastructure are supporting machinery.

The series is not "ten lessons from using AI coding agents." It follows one family
LEGO Christmas village through an annual cycle. The technical story appears because
the village needs to remember last year, choose a bounded addition for this year,
help a family work through ideas, make physical constraints visible, buy the right
parts before a real deadline, and preserve what actually happened for next year.

Three systems are being developed together:

1. **Agentic product discovery.** Claude Design makes sophisticated journeys
   tangible quickly enough that James can operate, challenge, and revise them.
2. **Application and schema co-design.** Using the journeys exposes missing states,
   records, evidence, authority, and lifecycle distinctions.
3. **Agentic application delivery.** Design packages, fixtures, tests, reviews,
   human rulings, exact repository states, and merge discipline carry those lessons
   into working software without mistaking a plan for a capability.

## The three nested learning loops

### The annual village loop

```text
Unpack last year's village
        ↓
Choose this year's bounded addition
        ↓
Invite ideas and work through constraints
        ↓
Measure, design, validate, and release
        ↓
Order, receive, inspect, and build
        ↓
Reconcile what actually happened
        ↓
Pack away a truthful starting point for next year
```

Last year's as-built village is this year's starting state. The intended village,
purchased village, assembled village, and village that survived storage may differ.
The application must preserve those differences rather than reconstructing a clean
story after the fact.

### The design learning loop

```text
Prototype a journey
        ↓
Operate it at useful fidelity
        ↓
Encounter an awkward or unrepresentable case
        ↓
Propose a schema or interaction change
        ↓
Seed design and application with the same village state
        ↓
Implement and test
        ↓
Feed the result and the disagreement into the next design cut
```

Claude Design is not merely an upstream supplier of screens. Its prototypes are
investigative instruments. Static wireframes would not expose what happens when a
measurement changes after approval, a family request conflicts with a physical
envelope, an AI proposal needs correction, or an order is placed outside the plan.

### The bag loop

```text
Agree the picture on the box
        ↓
Refine the booklet for one bounded slice
        ↓
Open one numbered bag
        ↓
Build on the table with validated fixtures
        ↓
Step back and look
        ↓
Return learning to design, schema, and the next booklet
        ↓
Open the next bag only when the previous slice can be explained unaided
```

A bag is not done because code merged. It is done when James can operate the slice,
describe what it does without the booklet, and state what the work taught the next
bag.

## Learning through play

The series uses the LEGO Foundation's five characteristics of learning through
play as design criteria, not as decorative branding.

| Characteristic | How it appears in the village | How it appears in delivery |
|---|---|---|
| **Joyful** | The family can see, move, name, and tell stories about a village that belongs to them | A working slice is put on the table early enough to manipulate, not admired as a plan |
| **Meaningful** | The work extends a real family tradition with a real tree, train, room, budget, and Christmas | Acceptance is tied to this year's physical outcome and order-by date |
| **Actively engaged** | People measure, place, rotate, compare, choose, build, photograph, and correct | Claude Design prototypes, fixtures, running sheets, tests, and physical checks make assumptions operable |
| **Iterative** | Each scene and each Christmas begins from the previous result | Numbered bags, weekly cuts, drift triage, step-backs, and revisions preserve feedback |
| **Socially interactive** | Family requests and stories remain visible and answerable | Designers, implementers, reviewers, and James disagree through durable artifacts with explicit authority |

Do not imply that all five have already been validated with the family. James is the
sole user until the 2026-12-25 demo. The family-facing journeys are designed and
prototyped now; actual family use is future evidence.

## LEGO language and its boundaries

Use LEGO set-building language consistently. Do not overload it until the metaphor
stops distinguishing real domain states.

| LEGO language | Meaning in this project |
|---|---|
| **Picture on the box** | The observable outcome agreed as the test of done; acceptance criteria, not aspiration alone |
| **Box** | The whole program or roadmap. It promises the model and sequence but builds nothing |
| **Instruction booklet** | The short, human-refined work order for one bag: one diagram, local vocabulary, failure modes, the slice delivered, and its picture of done |
| **Numbered bag** | One ordered, bounded, end-to-end slice. Only one is open in build |
| **Model in the booklet** | The pinned Claude Design standalone. Looked at while building; never copied as production code |
| **Bricks and pieces** | Schema types, fixtures, components, tools, tests, and evidence that can be assembled into the slice |
| **Build on the table** | Run the application against validated fixtures representing the real village as currently known |
| **Step back and look** | Compare the working slice with the box, explain it unaided, record drift, and send learning back to design |
| **Real bricks, no glue** | Introduce real data one entity at a time behind explicit gates, without making reversal impossible |
| **Parcel** | A literal shop shipment. Do not use it as a synonym for a PR, design package, or agent handoff |
| **Pack away** | Reconcile the as-built village, inventory, unfinished requests, and lessons so next year begins from truth |

LEGO is an adjective: write *LEGO bricks* and *a LEGO set*, never "LEGOs."

## The ten-article sequence

### 1. A Christmas Tree, a Train, and Room to Play

**Seasonal position:** opening the annual loop
**Primary characteristics:** meaningful · joyful · socially interactive

Open with James's actual account: the Family Christmas Tree last year, a decision
to add a train this year, then the question of building a scene that can grow each
Christmas. Keep the village open to play as it grows. Use a possible Christmas
market to show how stories can lead to things the family chooses to build.

Introduce AI through the work around that play: finding a design, checking space,
organizing parts, remembering why something changed, and returning to a parked
idea. Keep detailed architecture for later articles. Retained learning should help
the next season without making this season's scene untouchable.

**Governing question:** Can we grow a world together while keeping it a place to play?
**Application strand:** family stories, proposals, practical planning, retained learning
**Delivery strand:** test whether AI reduces the organizing burden of a growing tradition
**Status:** origin supplied by James; imagined market scenes remain possibilities.
Establish a dated claim ledger before drafting.

### 2. The Picture on This Year's Box

**Seasonal position:** choosing this year's bounded addition
**Primary characteristics:** meaningful · socially interactive

Explain the scaling hypothesis through this year's bounded test: the family tree,
the Winter Holiday Train and its assigned track, the R40 railbed, the parts gap,
and the order needed to make the physical build possible. Connect official sets,
community MOCs, and our modifications to one planned display. Explain how multiple
family and operator surfaces, proportionate controls, and a self-documenting
learning loop could keep that display manageable as it grows.

The picture on the box is not only a rendering. It is an acceptance contract: the
track fits; the right-of-way is clear; the tree remains usable; the parts list has
traceable evidence; purchasing can happen before the deadline; and the result can
be understood and extended by the family.

**Governing question:** What are we trying to learn and deliver this Christmas?
**Application strand:** one real village, bounded context, family outcomes
**Delivery strand:** vertical scope and acceptance before architecture
**Status:** establish the current program status in the article's dated claim
ledger; distinguish the box from delivered software and never describe the whole
bag program as accepted unless canonical evidence supports it.

### 3. The Booklet Is a Conversation

**Seasonal position:** experiencing the proposed journey
**Primary characteristics:** joyful · actively engaged · socially interactive

Show how Claude Design rapidly prototypes the whole journey: arranging the village,
switching between plan and 3D, placing a family scene, measuring a fact, correcting
an AI claim, seeing downstream staleness, reviewing a parts gap, releasing or
reopening a purchase, and recording something bought outside the plan.

The high fidelity is purposeful. The prototype can disagree with James and reveal
problems a wireframe or isolated schema review would not. It remains a behavior
reference, not production code and not an autonomous decision-maker.

**Governing question:** What do we discover only when the journey can be experienced?
**Application strand:** Claude Design, Family Workbench, measurement, release, requests
**Delivery strand:** design decisions and unresolved questions must survive export
**Status:** publishable as a design-method story; say plainly that the live Claude Design conversation is richer than the exported handoff

### 4. One Numbered Bag at a Time

**Seasonal position:** turning the box into ordered slices
**Primary characteristics:** iterative · actively engaged

Introduce the bag as the unit of progress: a bounded vertical slice with a booklet,
a pinned design model, acceptance criteria, validated fixtures, a working build,
and a step-back. Open bags in order. Keep one bag open in build. Do not begin the
next merely because the roadmap exists.

Use the planned sequence as the concrete example: foundations; components; the
morning hub; geometry; measurement and BOM; procurement; then real bricks.

**Governing question:** What is the smallest slice that teaches us something complete?
**Application strand:** recognizable capability in every slice
**Delivery strand:** WIP limits, booklet preconditions, design pins, weekly cuts
**Status:** distinguish the proposed program from bags actually implemented. Do
not treat the bag program or its vocabulary as settled while its source remains
under review.

### 5. The Bricks Tell Us the Schema Is Wrong

**Seasonal position:** letting behavior reshape the underlying model
**Primary characteristics:** actively engaged · iterative

Trace interaction discoveries into schema requirements:

- changed measurement → immutable revision and `supersedes`;
- family idea → durable request with origin, attached work, status, reasons, and reply;
- proposed scene → envelope before a finished model;
- AI-authored change → origin, proposal, restatement, confirmation, and invalidation;
- purchasing release → a gate record with evidence and authority;
- price display → time-bound observations and ranges;
- manual purchase → a first-class retroactive order path;
- delivered parcel → ordered, received, inspected, owned, and built are different states.

The schema enables journeys, and the journeys challenge the schema. Neither side
hands the other a finished answer.

**Governing question:** What can the family do that our current data model cannot honestly represent?
**Application strand:** family and operator journeys
**Delivery strand:** fixtures and runtime validation expose unrepresentable cases before production
**Status:** separate accepted design decisions, open schema requests, and implemented validators

### 6. Build It on the Table

**Seasonal position:** dogfooding without spending money
**Primary characteristics:** joyful · actively engaged · iterative

The Claude Design prototype and the application should show one village: the same
tree, track, parts, measurements, claims, and known collision. The shared fixture
set progresses on three axes:

- **ambiguity:** asserted facts become measured or verified;
- **fidelity:** approximate geometry, inventory, lots, and prices approach reality;
- **autonomy:** agents originate more useful changes, with restatement before save.

Define dogfooding as moving the village from guessed to known while the software
watches. Nothing needs to touch real shops, Studio, Blender, or the family yet.

**Governing question:** Did the software help us know the village better?
**Application strand:** shared fixtures, plan, 3D, measurements, BOM
**Delivery strand:** `DataSource = fixtures` and later `DataSource = real` through one validated seam
**Status:** publish after naming precisely which fixture-driven slice is running.
Do not treat the bag program or its vocabulary as settled while its source remains
under review.

### 7. Step Back and Look

**Seasonal position:** reflecting before the next bag opens
**Primary characteristics:** iterative · socially interactive

Ask whether the slice matches the box, whether James can explain it unaided, what
drifted, what should return to Claude Design, and which guarantees existed only in
prose. Weekly design cuts, drift triage, independent review, and the step-back memo
are parts of one learning mechanism rather than separate ceremonies.

Use the design-package review round as evidence: multiple defects differed in
surface form but shared one shape — a guarantee was asserted at one layer while the
mechanism beneath went unchecked. Self-verification repeatedly stopped one layer
earlier than peer review.

**Governing question:** What did this bag change about the next booklet?
**Application strand:** can the slice be understood and used?
**Delivery strand:** review, drift, enforcement, preserved disagreement
**Status:** publishable from the recorded review and debrief material, while
distinguishing those findings from the still-under-review bag program.

### 8. When the Model Does Not Match the Box

**Seasonal position:** turning a physical block into useful learning
**Primary characteristics:** meaningful · iterative · actively engaged

Center the story on the honest geometry block: the railbed appears plausible until
the shared geometry finds the inner-corner conflict with the tree base. That is not
the design process failing. It is the loop succeeding before money is spent.

Inspect the model, verify measurements, show the disagreement in plan and 3D,
choose among real alternatives, record the decision, and rerun the same checks.
Relate this to software defects without making the physical story a disposable
metaphor.

**Governing question:** Can the system make being wrong useful?
**Application strand:** one geometry, many views, deterministic fit checks
**Delivery strand:** evidence-backed correction and independent audit
**Status:** do not call Q13 resolved until the chosen physical solution passes in code

### 9. Building a Merge Train for Humans and Coding Agents

**Seasonal position:** accepting consequential learning into the durable record
**Primary characteristic:** socially interactive

Three capable agents can move quickly while still being unable to answer which
exact commit was approved or who had authority to decide. The merge train exists
because design, implementation, review, coordination, and human authority are
different roles.

The useful unit is an accepted landing transaction:

> one pinned repository state + independently scoped review + an explicit human
> decision + a merge with verifiable Git facts

Use the unsafe historical-text split as the concrete discovery: reconstruction and
digest proofs could both pass while proving the wrong representation. Durable
artifacts allow disagreement to improve the next accepted state without turning
agents into decision authorities.

**Required flow:** source verification → plan-only work order → independent reviews
on the same head → reconciliation → one human decision docket → ratified revision →
implementation → exact-head review → merge → canary.

**Status guardrail:** create a dated, source-linked claim ledger when this article
is drafted. Keep the plan free of point-in-time Git, pull-request, and register
facts. Treat the migration and its post-migration canary as separate claims, and
name neither as complete, launched, operational, or merged without current
canonical evidence.

**Required visuals:**

1. Authority boundary: James above separately labelled Codex, Claude Code, and
   Cowork lanes; arrows distinguish proposal, review, and implementation from
   James's decision authority.
2. Accepted landing transaction: pinned head through canary.
3. Delivered now versus planned next.
4. Superficial proof failure: quoted prose contains a lookalike seam; bytes and
   digests reconstruct while conceptual slices are wrong.

### 10. The Parcel Is Not the Finish Line

**Seasonal position:** returning physical truth to the next annual loop
**Primary characteristics:** all five converge

A parcel at the door is another transition, not completion:

```text
planned → released → ordered → shipped → received → inspected → allocated → built → reconciled
```

Follow substitutions, shortages, damage, unused parts, manual orders, and changes
made on the table. End by packing the village away carefully: record what was built,
return loose pieces to inventory, retain unfinished requests, preserve measurements
and corrections, photograph the final arrangement, and name what next year inherits.

**Governing question:** Did the village merely get larger, or did the family become better able to build the next part together?
**Application strand:** procurement, receiving, inspection, build, reconciliation
**Delivery strand:** the record follows reality even when reality leaves the planned path
**Status:** hold the retrospective until a real order and build supply the evidence

## Recurring structure inside every article

Use this as a lens, not a mandatory heading template when it would sound mechanical.

### The picture on the box

What we thought success would look like.

### What we built on the table

The journey, prototype, fixture, application slice, or physical artifact actually
tried.

### What moved

Which learning axis advanced: ambiguity, fidelity, autonomy, or a combination.

### What we learned when we stepped back

The disagreement, block, or discovery that changed the next bag.

### What remains sealed

What is deliberately unbuilt, unverified, or outside this year's bounded context.

## Procedure ownership

The repo-local `village-article-writer` skill owns status definitions, publication
guardrails, mode selection, evidence-loading procedure, and final review. This plan
owns the article briefs, series arc, learning loops, LEGO glossary, and evidence map.

## Core evidence map

Read the canonical register first, then select only the sources needed for the
article being written.

- Project authority and current state:
  `docs/correspondence/REGISTER.md`, `CLAUDE.md`, `.claude/northstar.md`
- Annual product and design intent:
  `docs/design/H-01-R1/brief/LEGO-PIPE-007-R2.md`
- Learning-through-play delivery program:
  `docs/correspondence/HANDOFF-LEGO-PIPE-023-R2-drafting-table-on-fixtures-and-the-program.md`
- Design-package boundary:
  `docs/correspondence/HANDOFF-LEGO-PIPE-024-R1-design-package-protocol.md`
- Family collaboration:
  `docs/design/H-01-R1/specs/F-01-family-workbench.md`
- Measurement and claim learning:
  `docs/design/H-01-R1/specs/M-01-measure-and-check.md`
- Shared geometry and physical block:
  `docs/design/H-01-R1/specs/A-01-layout-canvas.md`
- BOM and release:
  `docs/design/H-01-R1/specs/C-01-railbed.md`
- Procurement and parcels:
  `docs/design/H-01-R1/specs/P-01-procurement.md`
- Review learning:
  `docs/correspondence/CORR-LEGO-PIPE-027-R0-chatgpt-design-handoff-review-debrief.md`,
  `docs/correspondence/CORR-LEGO-PIPE-028-R0-debrief-design-handoff-schema-round.md`,
  `docs/correspondence/CORR-LEGO-PIPE-029-R0-design-handoff-delivery-debrief.md`
- Register migration and concurrency:
  `docs/correspondence/CORR-LEGO-PIPE-030-R0-register-shape-cleanup.md`,
  `docs/correspondence/CORR-LEGO-PIPE-031-R0-register-concurrency-peer-memo.md`
- Tool boundary with Studio:
  `docs/research/studio-bridge/research-bricklink-studio-agent-integration.md`

The writer workflow and durable voice profile live in
`docs/writing/style-context.md` and the repo-local
`village-article-writer` skill.
