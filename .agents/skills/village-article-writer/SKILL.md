---
name: village-article-writer
description: Plan, draft, fact-check, or revise Medium-style articles about the LEGO Village Pipeline using James's voice, the annual family-village learning loop, LEGO set-building language, and current repository evidence. Use for this article series; do not use for correspondence memos, product documentation, or generic technical writing.
---

# Village Article Writer

Write from the village outward. The family tradition and its annual learning loop
are the story; the application, Claude Design, schemas, agents, tooling, and delivery
infrastructure enter because the village needs them.

## Load context before writing

Read these two editorial references completely:

1. `docs/writing/medium-series-plan.md`
2. `docs/writing/style-context.md`

Then establish current project state from canonical sources:

1. `docs/correspondence/REGISTER.md` — read first; it is the index and authority.
2. `CLAUDE.md` and `.claude/northstar.md`.
3. The operative work order, design manifest, and article-specific sources named in
   the series plan.
4. Current Git head and working-tree status.

Read the full files selected for the article. Do not rely on search snippets for a
claim that affects status, authority, chronology, or outcome.

When the current user supplies a brief, it controls purpose, audience, length, and
point of view. It does not override canonical repository facts unless the user is
explicitly supplying newer external evidence; label that evidence and its status.

## Choose the mode

- **Plan:** place the idea in the ten-article arc or explain why it should be an
  interlude or later-season article.
- **Context packet:** load sources and report the factual/status basis without
  drafting prose.
- **Draft:** produce the requested article after the context packet is sound.
- **Revise:** preserve the article's claims while improving structure, voice, or
  fidelity to the series.
- **Fact-check:** test claims and status language against canonical evidence; do not
  silently rewrite disputed facts.

## Produce a context packet

Before a full draft, state:

```markdown
Article: <number and working title>
Seasonal position: <where it sits in the annual loop>
Governing question: <one question>
Learning event: <the concrete scene where understanding changed>
Primary sources loaded: <short list>
Built and verified: <facts>
Designed or ratified: <facts>
Planned: <facts>
Known broken or unresolved: <facts>
Voice samples consulted: <titles, if available>
High-risk claim: <the claim most likely to mislead or become stale>
```

This is a correction surface, not an approval gate unless the user asks for one.
If the user asks directly for a draft and the sources are sufficient, keep the
packet compact and continue.

## Find the learning loop

Every article needs a change in understanding, not merely a chronology.

Identify:

1. **Picture on the box:** what success was expected to look like.
2. **Build on the table:** what was actually prototyped, implemented, reviewed, or
   built.
3. **What moved:** ambiguity, fidelity, autonomy, or a combination.
4. **Step-back:** the discrepancy or discovery that changed the next bag.
5. **What remains sealed:** work deliberately unbuilt, unverified, or outside this
   year's bounded context.

Use these as editorial questions. They need not appear as literal headings.

## Draft in James's voice

- Open with a physical scene, interaction, confusion, or question.
- State one governing thought early.
- Use first-person singular for James's experience and first-person plural only for
  genuinely shared work.
- Name mechanisms precisely after explaining why they matter.
- Treat metaphor as a testable model, not decoration.
- Be candid about failed assumptions, incomplete work, and coordination cost.
- Distinguish design fidelity from implemented capability.
- Return to the village, family, calendar, or next Christmas at the end.

Do not imitate phrases from published posts. Use the style sources to recover
rhythm, stance, and explanatory technique.

## Preserve the LEGO language

Use the meanings in the series plan:

- box = whole program;
- picture on the box = observable acceptance;
- booklet = one bag's human-refined work order;
- numbered bag = bounded vertical slice;
- model in the booklet = pinned Claude Design standalone;
- build on the table = running slice on validated fixtures;
- step back = reflection and returned learning;
- real bricks, no glue = gated real-data introduction;
- parcel = literal purchased-part shipment;
- pack away = as-built reconciliation for next year.

Never use *parcel* for a PR, design package, or handoff. Write *LEGO bricks* or
*a LEGO set*, never "LEGOs."

## Keep evidence and authority honest

Use these status classes explicitly in working notes and clearly in prose:

- built and verified;
- designed or ratified;
- planned;
- known broken or unresolved.

Do not use *shipped*, *launched*, *live*, *operational*, or *completed* unless the
current evidence supports that exact claim.

James is the sole decision authority. Agents may design, propose, implement,
review, reconcile, or report. Do not blur those roles with collective *we*.

The repository contains exported Claude Design artifacts, not the entire live
design session. Family-facing designs are not family-validated until real family
use supplies that evidence. Prototype numbers remain mock math until verified in
implementation and independently audited.

For public writing, preserve family privacy. James is a friend of the family, never
"Dad" or a parental role. Refer to the boys only as EH, HH, and LH; do not publish
their names, photos, or identifying details. Do not reproduce a family member's
request verbatim without their explicit consent.

## Final review

Check that:

- the village remains the protagonist;
- the bounded context and seasonal timetable are visible;
- the article demonstrates at least one learning-through-play characteristic
  through events rather than labels alone;
- the learning loop closes or intentionally remains open;
- current facts cite or name their evidence;
- planned work is not narrated in the past tense as capability;
- agent origin, human authority, and review independence remain legible;
- family relationships, identifiers, images, and quoted requests respect the
  public-writing privacy rule;
- technical detail supports the governing thought;
- the ending names what the next bag or next year inherits;
- the tone is reflective and technically grounded, not promotional.

## Boundaries

This skill writes or edits editorial artifacts only when requested. It does not
modify correspondence, register state, design packages, schemas, code, or project
policy. Drafts do not become work orders merely because they cite the repository.
