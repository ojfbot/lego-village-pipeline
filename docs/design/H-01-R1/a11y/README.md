# Accessibility-tree snapshots

One file per sheet, captured from the prototype with `dt/a11y-tree.js` (a small walker: roles, names, heading levels, `aria-*` states; generic wrappers flattened). Curly-brace values are templates for live text; `repeat` marks rows collapsed to one exemplar.

Use: build the sheet, run the same walker (or an axe/Playwright a11y-tree dump mapped to this shape), diff. **Additions are fine; a missing node, a renamed control, or a lost state is a regression.**

| Sheet | File | Notes |
|---|---|---|
| A-01 | `A-01.tree.json` | Plan is `role=application` with two `group` sections; the 3D canvas is `role=img` whose name carries the verdict and every blocking check. |
| C-01 | `C-01.tree.json` | Source and part rows are `<details>/<summary>` with full-sentence `aria-label`s; the ReleaseGate mounts into `#gate` after approval (its own tree is in `ReleaseGate.dc.html`). |
| P-01 | `P-01.tree.json` | Captured in the default *not released* state — most controls are disabled by design. |

Announcement sentences live in `../specs/ANNOUNCEMENTS.md`.
