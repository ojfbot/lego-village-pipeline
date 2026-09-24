---
title: "James's article-writing context"
status: maintained-editorial-reference
owner: James
updated: 2026-09-24
---

# Article-writing context

This file captures durable writing preferences and a repeatable context-loading
method for the LEGO Village Pipeline article series. It describes voice and method;
it is not evidence for current project status.

## Source hierarchy

When sources disagree, use this order:

1. The current user brief controls the article's purpose, audience, length, and
   point of view.
2. Canonical repository state controls project facts and implementation status.
3. `docs/writing/medium-series-plan.md` controls the series arc, LEGO language,
   recurring learning loops, and placement of the article within the ten-part set.
4. This file controls durable voice and editorial preferences.
5. Published Medium articles provide examples of rhythm and technique. They are
   never a source for current repository facts.

Do not let an old article, an unmerged branch, a design prototype, or a confident
handoff sentence overrule canonical `main`.

A brief may supply newer external evidence, but label its source and status before
using it. A requested claim is not evidence and does not override canonical facts.

## What the writer can and cannot see

The repository contains exported design packages: prototypes, specifications,
screenshots, decisions, accessibility artifacts, schema requests, manifests, and
review records. It does not contain the whole live Claude Design experience:
conversation, discarded alternatives, rapid comparisons, and tacit reasoning may
be absent unless James exported them.

State this boundary when it matters. Do not reverse-engineer a tidy design process
from the surviving handoff bundle.

## Durable voice profile

### Stance

- Curious, technically serious, and willing to show uncertainty.
- Reflective rather than promotional. The article may advance a hypothesis without
  pretending the hypothesis was obvious at the beginning.
- Warm and human, with concrete affection for the physical subject.
- Candid about failure, incomplete implementation, and the cost of coordination.
- Interested in metaphors when they explain an object model or operating behavior,
  not as surface decoration.
- Skeptical of easy claims about autonomy, speed, and replacement.

### Point of view

- Default to first-person singular when describing James's curiosity, choices, or
  experience: "I wanted to know..."
- Use first-person plural for genuinely collective work or a shared reader journey:
  "We can now compare..."
- Do not use *we* to blur who decided, implemented, reviewed, or merged.
- Agents may propose, implement, review, reconcile, or report. They do not possess
  project authority.

### Typical movement

1. Open with a physical scene, a moment of confusion, or a question that occurred
   during the work.
2. State the governing thought early enough that the reader knows why the scene
   matters.
3. Introduce the model or mechanism through concrete project objects.
4. Define technical terms once, in plain language.
5. Show the point where the initial model failed or became incomplete.
6. Separate implemented behavior from design, plan, and anticipation.
7. Return to the physical village or modest practical takeaway.

This is a common shape, not a mandatory template.

### Sentence and section style

- Mix compact declarative sentences with longer sentences that accumulate related
  detail.
- Use exact nouns: *measurement*, *request*, *gate*, *revision*, *parcel*, *commit*.
- Prefer meaningful section titles over generic headings such as "Overview" or
  "Benefits."
- Use lists when the list is itself the model; otherwise prefer connected prose.
- Let one memorable sentence carry the thesis. Do not manufacture quotable lines
  in every section.
- Explain enough mechanics that a technical reader can test the argument without
  turning a reflective article into a specification.

### Characteristic moves observed in published work

- A personal entry point becomes an architectural question.
- A metaphor is tested against the real system rather than assumed to fit.
- The object model is named explicitly after the reader understands the stakes.
- Implementation status receives its own honest treatment.
- The author admits where confidence exceeds evidence.
- Technical structures are connected to maintenance, memory, and governance.

## Things to resist

- "AI is changing everything" openings.
- Vendor boosterism or a product-announcement voice.
- Treating agent output as equivalent to accepted work.
- Describing design fidelity as deployed functionality.
- Generic claims that humans remain "in the loop" without naming their authority.
- Corporate abstractions when a tree, train, measurement, part, parcel, or family
  request can carry the explanation.
- A sequence of slogans unsupported by mechanisms.
- Excessive self-congratulation or praise of the process.
- Smoothing over disagreement to make the delivery story look efficient.
- Calling family-facing design validated before the family has used it.

## Series-specific preferences

- The village remains the protagonist; technology enters in service of its annual
  journey.
- Use the three nested loops: annual village, design learning, and numbered bag.
- Apply the five learning-through-play characteristics through events and choices,
  not repeated branding.
- Preserve the project's exact LEGO set-building vocabulary. In particular,
  *parcel* remains a physical procurement object.
- Use the annual timetable as narrative pressure. Christmas is the visible date;
  geometry and order-by gates are the operative deadlines.
- Keep this year's bounded context visible. Do not imply that speculative general
  infrastructure must be completed before the railbed can be delivered.
- Treat the Claude Design prototype as an investigative model in the booklet:
  viewed, operated, and challenged, but never copied as production code.
- End with what was learned and what remains sealed, not a grand claim about the
  future of software engineering.

## Published style sources

Use the smallest relevant sample. Inspect the source directly when current access
is available; otherwise use the profile above.

### Recent reflective and architectural voice

- **No Laws, Only Agreements**
  https://medium.com/@ojfbot/no-laws-only-agreements-a2beda2872b5
  Useful for: opening from personal curiosity, testing a literary metaphor against
  a technical system, layered conceptual sections, candid hypothesis language.

- **Events Are the Source of Truth. Labels Are the Cache.**
  https://medium.com/@ojfbot/events-are-the-source-of-truth-labels-are-the-cache-8068a72254bd
  Useful for: explicit object models, precise role boundaries, provenance as
  material, and a clear implemented-versus-spec distinction.

### Earlier procedural and encouraging voice

- **Build a Blender Add-on Ready to Scale**
  https://medium.com/@ojfbot/build-a-blender-add-on-ready-to-scale-8c285f9f0a5
  Useful for: approachable technical sequencing, explaining why structure helps
  learning, acknowledging self-doubt without making it the subject, and ending with
  a concrete working result.

- **Rapidly Spawn Printable Meshes via Blender Python**
  https://medium.com/@ojfbot/rapidly-spawn-printable-meshes-via-blender-python-9ff5c3af6379
  Useful for: practical build progression and connecting automation to a physical
  artifact.

- **Configure Blender for 3D Printing via Python**
  https://medium.com/@ojfbot/configure-blender-for-3d-printing-via-python-ecf729e4099b
  Useful for: playful subheads, documenting a learning process, and making repetitive
  tooling work feel consequential.

Profile: https://medium.com/@ojfbot

## Repeatable context-loading pipeline

### 1. Locate the article in the series

Read `docs/writing/medium-series-plan.md` and record:

- article number and working title;
- position in the annual loop;
- LEGO object or action carrying the article;
- primary learning-through-play characteristics;
- governing question;
- facts that must be true before publication;
- claims that must remain designed, planned, or unresolved.

If the requested article does not fit the series, say why before forcing it into a
slot. A useful article may be an interlude or a later-season piece.

### 2. Load durable voice context

Read this file completely. Then inspect two published articles:

- one recent reflective/architectural article;
- one procedural article if the requested piece explains a build or tool.

Extract techniques, not phrases. Do not imitate distinctive sentences or reuse the
same metaphor merely because it worked before.

### 3. Establish canonical project state

Read, in order:

1. `docs/correspondence/REGISTER.md`;
2. `CLAUDE.md`;
3. `.claude/northstar.md`;
4. the operative work order and relevant design-package manifest;
5. article-specific specifications, reviews, and research named in the series plan.

Also inspect the current Git head and working-tree status. Treat untracked files,
draft PRs, pasted prompts, and live design sessions as separate evidence with their
own status.

For time-sensitive GitHub or Medium facts, verify against the live source when the
user requests current accuracy or when the claim may have changed.

### 4. Build a fact/status ledger before prose

For every consequential claim, record:

| Claim | Status | Evidence | Safe wording |
|---|---|---|---|
| Example: the design journey includes a release gate | designed | pinned design spec | "The prototype models..." |
| Example: a capability named only in a work order | planned unless canonical evidence proves otherwise | work order + tree | "The ratified plan calls for..." |

Use the states from the series plan: built and verified; designed or ratified;
planned; known broken or unresolved.

### 5. Find the learning event

Identify the smallest concrete scene in which the team's understanding changed.
Examples include a fit check returning BLOCK, a prototype revealing a missing
lifecycle state, a reviewer finding proof of the wrong representation, or a parcel
showing that ordered did not mean owned.

The article needs a change in understanding, not merely a chronology of activity.

### 6. Draft from the village outward

Start with the village, family, table, calendar, prototype interaction, or physical
constraint. Introduce schemas, agents, tools, and Git only when the scene requires
them.

Maintain one governing thought. Technical detail should either explain the learning
event, establish credibility, or make the takeaway reusable.

### 7. Run the status and voice review

Before delivery, verify:

- Every claim of implementation or completion is supported by current evidence.
- The article distinguishes the live design experience from the exported bundle.
- James's authority and each agent's role remain legible.
- Family participation is not described as observed when it is only designed.
- The LEGO vocabulary is consistent and *parcel* remains literal.
- At least one learning loop closes or intentionally remains open.
- The ending returns to the village and names what remains sealed.
- The prose sounds like a reflective builder, not a vendor or governance manual.

## Context packet to report before drafting

The writer should provide a compact packet for James to correct:

```markdown
Article: <number and working title>
Seasonal position: <where we are in the yearly loop>
Governing question: <one question>
Learning event: <the scene where understanding changed>
Primary sources loaded: <short list>
Built and verified: <facts>
Designed or ratified: <facts>
Planned: <facts>
Known broken or unresolved: <facts>
Voice samples consulted: <titles>
High-risk claim: <the claim most likely to become false or misleading>
```

This packet is a context check, not a request for approval unless the brief requires
James to make a decision.

## Maintaining this file

Update the profile only when repeated evidence shows a durable preference. Do not
turn one requested article format into a permanent rule. Add a published source
when it contributes a distinct mode or technique; do not build an exhaustive archive
of every post.

Current project facts do not belong here. Update the canonical repository and the
article's fact ledger instead.
