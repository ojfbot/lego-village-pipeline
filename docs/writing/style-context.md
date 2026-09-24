---
title: "James's article-writing context"
status: maintained-editorial-reference
owner: James
updated: 2026-09-24
---

# Article-writing context

This file captures durable writing preferences and source hierarchy for the LEGO
Village Pipeline article series. It is not evidence for current project status.

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

## Procedure ownership

The repo-local `village-article-writer` skill owns mode selection, context load
lists, the context packet, fact-check ledger, output locations, and final review.
This file remains a durable reference for voice and source hierarchy; do not copy
procedure back here.

## Maintaining this file

Update the profile only when repeated evidence shows a durable preference. Do not
turn one requested article format into a permanent rule. Add a published source
when it contributes a distinct mode or technique; do not build an exhaustive archive
of every post.

Current project facts do not belong here. Update the canonical repository and the
article's fact ledger instead.
