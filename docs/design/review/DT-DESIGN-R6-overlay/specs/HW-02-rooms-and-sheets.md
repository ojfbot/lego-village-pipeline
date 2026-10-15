# HW-02 — Rooms as kinds of work: the block → room → sheet map

Source: `rooms[]` and `pages[]` in `sources/prototypes/House World.dc.html`. Answers 037 §2–3 ("how many pages does a room hold") and reframes R0's one-block-one-door map.

## 1. Principle

A **room** is one kind of work a person does at the table. A **sheet** is a page that lives in a room. The house teaches the shape of the work before any page opens: point at a room and you read what happens there and which pages it holds; fly in and the pages are tabs across the top. Nothing in the map is evidence — room names and kinds are wayfinding, not records.

Rules
- Every sheet lives in exactly one room. Every room has ≥ 1 sheet and ≥ 1 block.
- Activating a room opens its **first** sheet unless a specific sheet was asked for (finder row, ask bar hit).
- A room's **first block** is where the camera lands. `lobby: true` overrides the landing with the lobby pose (R1 only — P-R5-1).
- Sheets without a file are **concept doors**: they open a labelled page that says there is no page yet. They exist so the route can be tested; they are never a record.
- Once a sheet has been opened in this visit it **stays mounted** (hidden, not unmounted) so drafts survive tab and room switches (P-R5-2).

## 2. The map

| room | title | kind of work | what happens here | blocks | sheets |
|---|---|---|---|---|---|
| R1 | The drafting table (lobby) | WORK MANAGEMENT | What is next today, and what each thing waits on | 1, 13 | HUB, T-01 |
| R2 | The layout room | DESIGN & PLANNING | Where the sections go and whether they fit | 2, 15, 18 | A-01, F-01, W-00 |
| R3 | The measuring room | VERIFICATION | Checking sizes against the instructions and the build | 3, 4, 5 | M-01, V-01, V-02 |
| R4 | The decision room | REVIEW & APPROVAL | Questions the AI could not settle, and approvals | 6, 7 | B-01, C-01 |
| R5 | The buying room | PROCUREMENT & RECEIVING | Shops, prices, and parcels arriving | 9, 14 | P-01, R-01 |
| R6 | The store room | INVENTORY | What we have, where it is, and what is inside each box | 10, 11, 12 | I-01, I-02, I-03 |
| R7 | The map room | PROGRAMME & HANDOFF | How the sheets connect, and what gets handed over | 16, 17, 19, 20, 21 | J-01, H-01 |
| R8 | The ideas room | RESEARCH | Open research — not records yet | 22 | F5, F6, F7, F8 |

Block 8 is unassigned (D-17). Blocks are R0's `Block_N` indices from `house-metadata.json` and must survive the GLB swap unchanged.

## 3. The sheets

| code | title | verb | plain-words detail | opens |
|---|---|---|---|---|
| HUB | The drafting table | See today | The three things next, and what each is waiting on. | `Hub.dc.html` |
| T-01 | The queue | See today | See waiting work and the reason each item is waiting. | Prototype T |
| A-01 | Layout canvas | Arrange | Place sections and see whether the train circle fits. | Prototype A |
| F-01 | Family workbench | Arrange | Use the village tools together at the table. | `F-01 Workbench Junior.dc.html` |
| W-00 | Workbench frame | Study | Explore the optional rails, ledger, and change ripple. *(Wireframe study)* | `Workbench Frame.dc.html` |
| M-01 | Measure and check | Confirm | Record the measurements that later checks depend on. | Prototype M |
| V-01 | Reading the instructions | Look up | Find measurements already stated in the build instructions. | Prototype V |
| V-02 | Replaying the build | Arrange | Derive fit from the way a section is built. | Prototype V2 |
| B-01 | When the AI isn't sure | Answer | See the question, the evidence, and the answer that becomes the record. | Prototype B |
| C-01 | The railbed parts list | Approve | Review the parts and their basis before a purchase decision. | Prototype C |
| P-01 | Buying the gap | Buy | See shop options and price ranges after the list is released. | Prototype P |
| R-01 | Bringing things in | Confirm | Review receipts and parcels before anything counts as in the house. | Prototype R |
| I-01 | What we have | Look up | Separate what is owned, built, and free to use. | Prototype I |
| I-02 | Documenting the boxes | Confirm | Record what is actually inside each box. | Prototype I2 |
| I-03 | One set | Look closely | See the evidence and open work for one set. | Prototype I3 |
| J-01 | The thirteen journeys | Find your way | See how the sheets and decisions connect. | `J-01 Journey Map.dc.html` |
| H-01 | The handoff | Hand over | See what was settled and what agents may use next. | `H-01 Handoff.dc.html` |
| F5 | Your model, your story | Tell | The builder gives the model its meaning. Brick facts stay separate. | concept door · issue 38 |
| F6 | Compare ideas | Compare | See each proposal before discussing a shared version. | concept door · issue 39 |
| F7 | What if | Explore | Test a change against a real village constraint. | concept door · issue 40 |
| F8 | How agents work | Learn | Build, check, decide, and retain the evidence. | concept door · issue 41 |

Each row carries a **verb** (what you come here to do) and a **detail** sentence in plain words; both are what the finder, hover card and tabs show — never the kind-of-work label alone (operator principle).

## 4. Where the map shows up

**Finder** (header combobox, 44 px pill). Literal, case-folded match across *sheet code · title · verb · detail · room title · room kind · room what*. Rows show `code · title · in <room>`. ↑↓ moves the active row and highlights the room's blocks without moving the camera; the active row **expands inline** with the detail, `OPENS THE REAL SHEET · <verb> · <KIND>` (or `CONCEPT DOOR · …`) and `PREVIEW ONLY · ↵ FLIES THERE`. ↵ flies to the sheet's room with that sheet selected. Esc closes; focus never leaves the input. Count is announced politely. Footer hint: `↑↓ look · ↵ fly · esc close`.

**Hover card** (HW-01 §3). `R-code · title · KIND` / what / `n sheets: title · title` / `CLICK TO FLY IN`.

**Dashboard header.** `← BACK TO THE HOUSE` · a dashed pill holding `R-code · Room title ▾ other rooms` (the room switcher) · a `tablist` of the room's sheets (`code title`, active = plate fill) · the KIND label at the far right in mono.

**Switch room** (listbox under the pill). Lead sentence: *Each room is one kind of work. Pick one and its first sheet opens; Back to the house lands you outside that room.* Rows: code · title · what · *you are here* or *n sheets*. Picking re-uses an already-open sheet of that room if one exists, else the first; focus moves to the title; camera is re-landed on Back (HW-01 §5).

**No-WebGL list.** The same map as cards: code · KIND / title / one button per sheet.

## 5. Changing the map

Edit `rooms[]` and `pages[]` only. A sheet code must appear in exactly one room's `sheets`; a room's `blocks` must exist in the metadata. New sheets need `file` (relative to `prototypes/`) or `status` (concept). No other place in the source knows the map.
