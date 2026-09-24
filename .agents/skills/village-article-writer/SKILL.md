---
name: village-article-writer
description: >-
  Plan, draft, revise, or fact-check James's public Medium series about the LEGO
  Village Pipeline: the family Christmas village, winter train, and the design and
  agent pipeline behind them. Use for a blog post, Medium post, essay, "article N",
  village-story idea, pre-publication review, or a check for status overclaims,
  family privacy, LEGO vocabulary, or voice. Not for LEGO-PIPE memos or handoffs,
  GitHub evidence issues, READMEs, product documentation, or unrelated writing.
---

# Village Article Writer

Use this skill for public article work. It owns the procedure; the editorial docs
are reference material and must not duplicate it.

For direct invocation, supply a mode followed by an article number, title, or pasted
draft: `plan`, `packet`, `draft`, `revise`, or `fact-check`.

## Hard rules

- Preserve family privacy. James is a friend of the family, never "Dad" or a
  parental role. Refer to the boys only as EH, HH, and LH. Do not publish names,
  photos, identifying details, or verbatim family requests without explicit consent.
- Treat these as distinct states: **built and verified**, **designed or ratified**,
  **planned**, and **known broken or unresolved**. Do not use *shipped*, *launched*,
  *live*, *operational*, or *completed* unless current evidence proves that status.
- James is the sole decision authority. Keep agent origin, independent review, and
  human decisions legible; do not use collective *we* to blur them.
- The repository holds exported Claude Design artifacts, not the whole live design
  session. Family-facing journeys are not family-validated until real use supplies
  evidence. Prototype numbers are mock math until verified and independently audited.
- Read `docs/writing/medium-series-plan.md` for the canonical LEGO glossary. Keep
  *parcel* literal, and write *LEGO bricks* or *a LEGO set*, never "LEGOs."

## Select the mode before loading context

| Request signal | Mode | Deliverable |
|---|---|---|
| "Where does this idea fit?", series order, or an outline request | Plan | placement, governing question, learning event, and evidence needed next |
| "Load context", "what can we safely say?", or an article number before drafting | Context packet | compact fact/status packet for correction |
| "Draft", "write the next post", "article N", blog/Medium/essay request | Draft | article prose, preceded by a compact packet when evidence is consequential |
| Existing prose plus "rewrite", "tighten", or voice feedback | Revise | revised prose plus a note of any claim that needs rechecking |
| Pasted prose plus "check", "ready to publish?", status, privacy, or overclaim question | Fact-check | claim ledger and findings; revised wording only when requested |

If the request fits more than one mode, choose the least expansive one. A pasted
paragraph with "check" is Fact-check, not a full Draft. Ask only when the mode
would materially change the requested output.

## Load only the context the mode needs

Apply the source hierarchy in `docs/writing/style-context.md` in every mode: a
user brief controls purpose and point of view, not repository facts. Read a full
source—not a search snippet—for any claim about status, authority, chronology, or
outcome.

### Plan

Read `docs/correspondence/REGISTER.md` first for current status. Then read the
relevant sections of `docs/writing/medium-series-plan.md`: **The editorial
correction**, **The three nested learning loops**, **LEGO language and its
boundaries**, **The ten-article sequence**, and **Core evidence map**. Read only
the article-specific source needed to test a proposed claim.

### Context packet

Read the relevant article brief and the sources named for it in the evidence map.
Read `docs/correspondence/REGISTER.md` first, then `CLAUDE.md` and
`.claude/northstar.md` when authority, current scope, or delivery status matters.
Inspect current Git state for claims about a branch, pull request, or implementation.

### Draft or Revise

Read `docs/writing/medium-series-plan.md` and `docs/writing/style-context.md` in
full, then load the Context-packet sources above. Read the full operative work
order, design manifest, and article-specific evidence selected from the map.
When access permits, consult one reflective/architectural and one procedural Medium
source named in the style context. When access is unavailable, use the voice profile
and record `Voice samples consulted: none (offline)` in the packet.

### Fact-check

Read the submitted draft or passage, the relevant article brief, the register, and
the exact evidence behind each consequential claim. Use the hard rules above and
the source hierarchy; load `CLAUDE.md` or a work order only when a claim depends on
its authority or scope. Do not load the full series arc or voice profile unless the
question asks about placement or voice.

## Produce the right output

### Plan

State the proposed article slot (or explain why it should be an interlude), its
governing question, one concrete learning event, its LEGO object/action, and the
evidence that must exist before publishing. Do not turn a plan into an implementation
work order.

### Context packet

Use this compact correction surface before a consequential draft:

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
Voice samples consulted: <titles or none (offline)>
High-risk claim: <the claim most likely to mislead or become stale>
```

This is a correction surface, not an approval gate unless the user asks for one.

### Fact-check

Return a claim ledger:

| Claim | Status | Evidence | Safe wording | Finding |
|---|---|---|---|---|

If a central claim cannot be verified, stop and ask for evidence or a decision. For
a non-central claim, label it unresolved or hedge it explicitly; never invent a
source or silently upgrade its status.

### Draft or Revise

Open from a physical scene, question, or interaction. Introduce technical machinery
only because the village needs it. Find a learning event and use the recurring
structure in the series plan as a lens, not mandatory headings. End with what the
next bag or next year inherits. Extract techniques from published work; never imitate
phrases.

Unless the user asks for files, return prose in chat. When asked to create files,
write drafts to `docs/writing/articles/NN-slug.md` and the adjacent claim ledger to
`docs/writing/articles/NN-slug-notes.md`. Do not commit, push, publish, or link a
draft from a tracked index without explicit user authorization.

## Final review

Check that:

- the village, bounded context, and seasonal timetable remain visible;
- a learning loop closes or intentionally remains open;
- every consequential status claim names current evidence;
- planned work is not narrated as delivered capability;
- family privacy and consent rules hold;
- agent origin, human authority, and review independence are legible;
- the live design session is not conflated with its exported handoff;
- LEGO vocabulary is accurate and *parcel* stays literal;
- technical detail serves the governing thought rather than promotional language;
- the ending names what remains sealed or what the next year inherits.

## Reference ownership

- `docs/writing/medium-series-plan.md` owns the series arc, article briefs, LEGO
  glossary, learning loops, and evidence map.
- `docs/writing/style-context.md` owns the durable voice profile, source hierarchy,
  and published style sources.
- This file owns modes, load lists, output formats, and the final review. Do not
  copy those procedures into the reference documents.
