# Writing

Editorial material for public writing about the LEGO Village Pipeline. Nothing in
this directory is a work order or project authority.

## Files

- `medium-series-plan.md` — the ten-article arc, nested learning loops, LEGO
  vocabulary, article briefs, status guardrails, and evidence map.
- `style-context.md` — James's durable voice profile, published style sources, and
  the repeatable context-loading and fact-checking pipeline.

Article drafts, claim ledgers, and publication checklists land separately. Do not
add a link here until its target is committed in the same pull request or already
exists on canonical `main`.

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

This sharing arrangement requires the checkout to preserve symlinks. If
`.claude/skills/village-article-writer` is not a symlink after checkout (for
example, on a platform or Git configuration with symlinks disabled), Claude will
not discover the shared skill; restore symlink support before relying on it.

The skill loads these editorial files first, then reads the canonical register and
article-specific project evidence. Durable style belongs here; current status stays
in the repository sources that own it.
