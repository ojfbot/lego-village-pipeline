# Writing

Editorial material for public writing about the LEGO Village Pipeline. Nothing in
this directory is a work order or project authority.

## Files

- `delivery-checklist.md` — article readiness, evidence needed next, and the publication checklist.
- `articles/01-a-christmas-tree-a-train-and-room-to-play.md` — origin-story draft, ready for author review.
- `articles/01-a-christmas-tree-a-train-and-room-to-play-notes.md` — author-supplied facts, research, and editorial notes for article 1.
- `articles/02-the-picture-on-this-years-box.md` — article 2 draft; readability rewrite deferred while article 1 proceeds.
- `articles/02-the-picture-on-this-years-box-notes.md` — source snapshot, claim ledger, and editorial decisions for article 2.
- `medium-series-plan.md` — the ten-article arc, nested learning loops, LEGO
  vocabulary, article briefs, status guardrails, and evidence map.
- `style-context.md` — James's durable voice profile, published style sources, and
  the repeatable context-loading and fact-checking pipeline.

## Shared writing skill

The canonical skill is:

```text
.agents/skills/village-article-writer/
```

Codex can invoke it as `$village-article-writer`. Claude sees the same files at:

```text
.claude/skills/village-article-writer/
```

and can invoke `/village-article-writer`. The Claude path is a relative symlink to
the canonical skill so the two agents cannot silently develop different writing
instructions.

The skill loads these editorial files first, then reads the canonical register and
article-specific project evidence. Durable style belongs here; current status stays
in the repository sources that own it.
