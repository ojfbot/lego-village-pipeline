---
correspondence_schema: lego-pipe-memo/v2
memo: CORR-LEGO-PIPE-038
revision: R0
status: for_review
memo_type: findings
title: "BrickBench, read whole — agentic brick design has a floor a simulator can hold and a ceiling only taste can raise"
date: 2026-10-13
thread: cluster
tags: [research, brickbench, brickagent, bricknet, brickgpt, agents, validator, stability, fitment, inventory, design-quality, cost, operator-notes]
from:
  actor: Claude (claude.ai, Lego Village Pipeline project)
  role: research_intake_on_operator_request
to:
  - actor: James
    role: operator_and_final_authority
argument: >
  In which a paper posted five days ago is read whole rather than through a summary; eleven
  general coding agents are found to out-build the purpose-made brick models, but only while a
  validator stands beside them; the validator is found to buy soundness and nothing else, the
  design gap to a human set remaining wide; an earlier research report is corrected on two
  numbers; two Blender precedents are put on the shelf, one confirmed and one awaiting a source; and the consequences are laid
  out for the operator alone, for brick_bench, brickcore and the inventory rooms, with nothing
  decided and the order gate left untouched.
provenance:
  source_artifacts:
    - {name: "arXiv 2610.12452v1 — Kulits, Xu, Jones, Schmid, Wu, 'BrickBench: Evaluating Agentic Brick Design', submitted 2026-10-08", role: "primary source, read section by section from https://arxiv.org/html/2610.12452v1 (Sections 1–7, Tables 1, 2 and A1, Appendix C)"}
    - {name: "http://www.brickben.ch", role: "the paper's stated release location; NOT read — the fetch permission timed out, so nothing here rests on it"}
    - {name: "YouTube KPYpZEr5c6E — 'This LEGO Animation Hack in BLENDER Changed My Life | Trevor Carlee' (The VFX Process)", role: "operator-supplied 2026-10-13; confirms Carlee as a Blender-native LEGO precedent (oEmbed metadata read; video not transcribed)"}
    - {name: "YouTube a0PYJRo4NVE — 'How to Build a Big 3D LEGO City (without blowing up your computer) | Blender Tutorial' (TiNKLe, @TiNKLeFilms)", role: "operator-supplied 2026-10-13; city-scale Blender performance precedent (oEmbed metadata read; video not transcribed)"}
    - {name: "reddit r/lego thread 1vntuwu — 'Been building a digital LEGO city for the past 2…' (attributed to crazytakeharu)", role: "operator-supplied lead; NOT read — the site is blocked to this session, and no other source for the handle was found"}
    - {name: "Claude Advanced Research report, claude.ai, 2026-10-13 ('Play-Well Research Extension: Blender LEGO Craft, Procedural Snow and Terrain, and Instructions-to-Build Groups')", role: "the secondary summary this memo corrects in §3; not committed"}
    - {name: "Dia research seeds, 2026-10-13 (not committed; hashes only)", role: "operator's starting briefs — Digital LEGO in Blender sha256 b3b5ecd47eb1d35e107c5117d638d6f15d93950538c8e62b8d513247f8d4a876; Procedural Generation for the Village Pipeline sha256 71e7e2da3485f8e1d6c9f4cff20a2b64562e10229b949261c6dea4dee138dd4f; From Instructions to Buildable Groups sha256 e21f00f347aab1234af6f2d55dc1e8f3da3bb51f6c80813aaf7dfedec101d49e"}
    - {name: "docs/correspondence/CORR-LEGO-PIPE-036-R0-lego-software-ecosystem-research.md", role: "prior intake that named BrickNet the reference generator; this memo updates that framing"}
  method: >
    The paper was read directly from arXiv's HTML rendering, section by section, after the
    Advanced Research report's account of it proved partly wrong. Every number in §2 is
    transcribed from the paper's tables; nothing was re-run. The repository was read only to
    place the findings against existing decisions (brickcore verdicts, brick_bench as the
    agentic venue, the inventory prototypes, the ORDER-BY gate).
authority:
  decision_owner: James
register:
  number: "038"
  allocated_by: "James, 2026-10-13 — 'Take the next available registration' (claude.ai Lego Village Pipeline session). 037 is allocated to HANDOFF-LEGO-PIPE-037 (House World, James 2026-10-11) on the unlanded branch feat/house-world-design-brief, so the next available number is 038"
register_version_read: 2026-09-18.33
findings:
  - {id: N-01, summary: "General coding agents inside a validator environment subsume the task-specific brick models: top agents reach validity 1.00 and VQA ~0.95; BrickNet-14B scores validity 0.26, BrickGPT VQA 0.024 (Model setting)"}
  - {id: N-02, summary: "The environment buys physical validity and nothing else: removing BrickAgent drops GPT-6 Astra's validity 1.00 → 0.40 while its VQA (0.954 → 0.940) and ELO (1297 → 1309) hold"}
  - {id: N-03, summary: "The gap to human design is wide and open: raters picked the human build in 323 of 360 comparisons; no agent passed for human more than one time in five"}
  - {id: N-04, summary: "BrickBench's stability test is a rigid-body proxy with no stud clutch; anything that depends on clutch must come back from brickcore as unknown(coverage), not valid"}
  - {id: N-05, summary: "The Alt-Build setting (design only from set 10698's 783 pieces) is the same problem as the inventory rooms — design from what we have"}
  - {id: N-06, summary: "A VLM pairwise design judge was validated against 102 human raters (Kendall tau 0.89); the pattern transfers to judging snow/roof variants if calibrated to the operator's own picks"}
  - {id: N-07, summary: "A full design run costs roughly $0.31–$18.80 per assembly at list price (Claude Opus 5.5: $6.33 average) — squarely in the restricted token-intensive subset for family play"}
  - {id: N-08, summary: "The release surface (tool API, language, licence) is undocumented in the paper; brickben.ch was not read — adoption claims wait on it"}
  - {id: N-09, summary: "Two Blender LEGO precedents join the shelf: Trevor Carlee (confirmed, VFX Process interview) for shot-scale craft, and a Studio-modelled, Blender-rendered digital LEGO city attributed to crazytakeharu (unverified) for village-scale craft; TiNKLe's big-city performance tutorial bears on R6-NEXT-RENDER"}
  - {id: Q-01, summary: "Can you supply crazytakeharu's channel or a video link, so the city precedent can be studied from the source?"}
  - {id: Q-02, summary: "Approve a read of brickben.ch to establish what is actually released and under what licence?"}
  - {id: Q-03, summary: "After ORDER-BY, should brickcore adopt BrickBench's validity definition as its floor check set, extended with MILS checks and clutch-unknown?"}
  - {id: Q-04, summary: "After ORDER-BY, should a small inventory-constrained winter-village prompt set become brick_bench's regression benchmark?"}
parts:
  "0": "Orientation"
  "1": "The paper, read whole"
  "2": "What it found"
  "3": "What the earlier report got wrong"
  "4": "What it means for play-well"
  "5": "What it does not decide"
  "6": "Questions"
---

# BrickBench, read whole

*For James alone. Nobody else is a recipient; no agent is asked to act on this.*

## §0 Orientation

This afternoon three research seeds from Dia went through an Advanced Research pass. Its report recommended keeping play-well's present shape — agents mutate the scene in Blender, deterministic `brickcore` checks gate the result — and leaned that recommendation on a paper posted on 8 October 2026: **BrickBench: Evaluating Agentic Brick Design** (Kulits, Xu, Jones, Schmid, Wu; arXiv 2610.12452). Kulits is the BrickNet author, so this is the same group that built the generator CORR-036 named as the reference.

You distrusted the report — rightly, as §3 shows — and asked for the paper itself. This memo is that reading. Think of it as opening the box and checking the bags against the inventory sheet rather than trusting the picture on the lid.

The short version: **a validator turns a capable coding agent into a reliable builder, but it does not turn it into a good designer.** That is the floor/ceiling split play-well already assumes — `brickcore` holds the floor; known-goods, precedent and your judgment have to raise the ceiling.

## §1 The paper, read whole

**The task.** Text prompt in, LDraw assembly out. Every part instance gets a part type, a colour and a 6D pose, chosen from the full LDraw library as BrickNet supports it — 14,441 part types.

**Three settings, 100 prompts each, ten per topic category** (categories follow the BrickLink Designer Program; prompts were LLM-drafted and hand-checked):

- **Model** — at most 400 parts, full library.
- **Set** — 400 to 4,000 parts, full library.
- **Alt-Build** — only the 783 pieces (104 part types) of retail set 10698.

**BrickAgent, the environment.** The LDraw library, BrickNet's typed-connector system, and tools to search parts, place them *by position or by connector*, mirror and measure, define and combine subassemblies, render from any viewpoint, and validate. The validator "interpretably reports each failure with the parts involved." Agents ran through their vendors' own harnesses — Claude Code for the Opus models, Codex CLI for the rest — with a budget of 300 turns per prompt.

**What "valid" means.**

- *Connected:* a compatible pair of BrickNet connectors (stud, hinge, axle, ball, fixed — each with subtype, polarity and frame) aligned "up to tolerance". The tolerance is not given numerically.
- *Collision-free:* no two parts overlap "by more than a tolerance". Also not given numerically.
- *Stable:* each connected component simulated as a rigid body of uniform density in PyBullet, high friction, no restitution; it fails if any point moves more than 3 LDU (three quarters of a stud's height). Stud holding force and axle play are **not** modelled.
- *Valid* = meets the setting's part requirement, collision-free, stable.

**How well it matches the prompt (VQA).** Each prompt becomes a graph of yes/no questions; Gemma 4 31B answers them from eight rendered views; the score is the fraction answered yes.

**How well it is designed (ELO).** A vision-language judge compares two assemblies on four views each, in both orders, and is asked which is "better designed by the standard of an official set". Results are fitted Bradley–Terry style. A Prolific study — 102 raters, 4,080 judgments — agreed with the judge on 34 of 36 agent pairs (Kendall τ = 0.89).

## §2 What it found

Averaged across the three settings:

| System | Valid | VQA | ELO | $ / assembly |
|---|---|---|---|---|
| GPT-6 Astra | 1.00 | 0.954 | 1297 ± 22 | 4.06 |
| GPT-6.1 Sol | 1.00 | 0.945 | 1293 ± 23 | 0.87 |
| Claude Opus 5.5 | 0.99 | 0.923 | 1249 ± 23 | 6.33 |
| Claude Opus 5 | 1.00 | 0.908 | 1101 ± 17 | 16.47 |
| GPT-5.6 Luna | 1.00 | 0.792 | 898 ± 16 | 0.75 |
| GLM 5.3 Flash | 0.92 | 0.590 | 752 ± 23 | 0.54 |

The two purpose-made models were scored in the Model setting only: **BrickNet-14B** valid 0.26, VQA 0.180, ELO 731, $0.0006; **BrickGPT** valid 1.00, VQA 0.024, ELO 338, $0.04. BrickGPT is always sound because its eight-brick grid can hardly be otherwise; it almost never builds what was asked.

**The one ablation** removes the whole BrickAgent environment — the agent keeps its harness, container and task but gets only the LDraw library and a primer on the file format:

| | Valid | Colliding pairs | Components | VQA | ELO |
|---|---|---|---|---|---|
| Astra, with BrickAgent | 1.00 | 0.00 | 2.21 | 0.954 | 1297 |
| Astra, without | 0.40 | 7.19 | 6.12 | 0.940 | 1309 |
| Luna, with BrickAgent | 1.00 | 0.00 | 4.60 | 0.792 | 898 |
| Luna, without | < 0.01 | 155.51 | 83.00 | 0.813 | 960 |

There is no finer ablation — validator, rendering and subassemblies were not removed one at a time.

**Against people.** Five raters made 360 human-versus-agent judgments and picked the human build in 323 (about 90%). Astra passed for human in 4 of its 21 pairs; no agent did better than one in five.

**Where it fails.** Of 137 invalid assemblies, 44 were never delivered; the rest failed on stability (41), collisions (31) and the part requirement (21). Set is the hardest setting for validity. Colour questions are satisfied ≥ 91% of the time; texture only 49–83%.

The authors' own summary: *"The domain gives the task a floor that a simulator can verify and an open ceiling on design quality."*

## §3 What the earlier report got wrong

Recorded, not repaired — the report stands as it was delivered; these are the corrections.

1. **BrickNet's 26%** is its *validity* in the Model setting — part requirement, collisions and stability together — not "collision-free on 26% of prompts".
2. **It missed the most useful result.** It read the ablation as "outputs collapse without the validator". The fuller reading is §2's second table: without the environment, soundness collapses *but prompt match and design rating do not fall* (Astra's ELO is nominally higher without it). The environment is a floor, not a designer.
3. **The creators.** The report's account of Trevor Carlee stands: he is a real Blender-native LEGO creator, and the VFX Process interview you supplied ("This LEGO Animation Hack in BLENDER Changed My Life") confirms him. He is a good data point for shot-scale craft (build only what the camera sees, Python for the repetitive work). The city builder you were actually thinking of is a different person, attributed to **crazytakeharu** (sometimes "Takeharu"). That is a reddit thread about two-plus years spent building a whole digital LEGO city, modelled in BrickLink Studio and rendered in Blender. I could not open the thread or find any other source for the handle, so he is **unverified** (N-09, Q-01). One correction to the note that came with it: the "How to Build a Big 3D LEGO City" video is by **TiNKLe** (@TiNKLeFilms), not crazytakeharu.

## §4 What it means for play-well

**The floor is `brickcore`'s job, and BrickBench hands it a ready baseline (N-01, N-02).** BrickNet connectors, collision, rigid-body 3 LDU — an externally used, published definition of "sound" to start the check set from, with MILS profile checks layered on top. It keeps the existing verdict shape: every check still returns `valid | invalid | unknown(coverage)`.

**Clutch is a declared blind spot (N-04).** The paper says it plainly: an assembly that balances passes "even when a physical one might sag", so the test is "necessary but not sufficient". Snow overhangs, cantilevered eaves, long plate spans on a railbed — the things a winter village is made of — lean on clutch. Until play-well has a connection-strength model, those come back `unknown(coverage)`, never `valid`.

**`brick_bench`'s tool surface should look like BrickAgent's (N-02).** Place by connector, compose subassemblies, render any view, and a validator that names the parts at fault. That surface is what moved agents from 0.40 to 1.00. Caveat (N-08): the paper describes these tools only at the level of a sentence each — no signatures, no language, no licence — so this is a pattern to copy, not yet a library to adopt.

**The ceiling is where known-goods earn their keep (N-03, N-06).** No tool closes a 90% human-preference gap; curated precedent and your eye have to. The paper's pairwise judge, validated against people, is a pattern worth borrowing: calibrate a judge on *your* choices between snow-on-roof or terrain variants, and it becomes the acceptance gate for the procedural levers in the mils-integrator direction.

**Alt-Build is the inventory rooms' problem (N-05).** "Design only from the 783 pieces of one set" is "design from what we have" — the What We Have / Documenting the Boxes / One Set prototypes. A small benchmark of winter-village prompts restricted to parts you actually own would be a fair, cheap regression test for `brick_bench`, and it borrows a setting someone else has already shown to be measurable.

**Cost places full design in the restricted subset (N-07).** At list price a complete design run costs between about $0.31 and $18.80 per assembly (Opus 5.5 averages $6.33). That fits the standing rule that ordinary play runs for long stretches on minimal tokens and only a small, named set of token-intensive actions is restricted: "design me a whole building" belongs in that set; "move this tree two studs left" does not.

**Precedent, not just papers (N-09).** If confirmed, the crazytakeharu city is the closest public match to play-well's own split: Studio as the modelling surface, Blender as the render venue, at village scale, sustained for years. It is worth studying for how a city is cut into modules and how part counts are kept renderable. TiNKLe's "without blowing up your computer" tutorial is direct input to R6-NEXT-RENDER's instancing-versus-batching measurement. Carlee is the shot-scale counterpart. None of the three videos has been transcribed for this memo.

**Claude Opus 5.5 was benchmarked through Claude Code** — the same harness this cluster already runs — and placed third overall (valid 0.99, ELO 1249), behind two GPT-6 models and ahead of Opus 5. That is a fact about the paper's runs, not a recommendation to switch anything.

## §5 What it does not decide

- **Nothing touches the 2026-10-21 ORDER-BY gate.** The BOM stays Studio-authored and reconciled as already planned; none of this is on the critical path to buying parts.
- It does not adopt BrickAgent, BrickNet or any code — the release terms are unread (N-08).
- It does not amend any ADR, the BuildDoc, or the verdict vocabulary.
- It does not make the earlier report's build plan a work order; that plan stays an unratified suggestion.
- It does not verify the crazytakeharu precedent; that waits on a source (Q-01).
- Every BrickBench number is a five-day-old preprint's, unreviewed, and its model names are the authors' reporting.

## §6 Questions

- **Q-01** — Can you supply crazytakeharu's channel or a video link? The only lead is a reddit thread this session cannot open. With a source, the city precedent can be studied properly rather than guessed at.
- **Q-02** — Approve a read of brickben.ch, so the next note can say what is actually released (tools, environment, licence) instead of what the paper says will be?
- **Q-03** — After ORDER-BY: should `brickcore` adopt BrickBench's validity definition as its floor check set, extended with the MILS checks and a clutch-dependent `unknown(coverage)`?
- **Q-04** — After ORDER-BY: should a small inventory-constrained winter-village prompt set become `brick_bench`'s regression benchmark, in the Alt-Build style?

*Source: Kulits, Xu, Jones, Schmid, Wu. "BrickBench: Evaluating Agentic Brick Design." arXiv:2610.12452v1, 8 Oct 2026. https://arxiv.org/abs/2610.12452*
