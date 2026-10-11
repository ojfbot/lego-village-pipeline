# N-01 — X-01 and W-00 are wireframes, not implementation guides

Filed 2026-10-10 at the operator's request.

## What was observed
Any state change on `Typology Identity v2` or `Workbench Frame` (open a card, hover Benny, acknowledge a chip) makes the **whole page flash**. The operator read this correctly: the app is not wired to re-render only the smallest changed portion.

## Why it happens in the wireframe
1. One design component holds all state; every `setState` re-renders the entire board tree.
2. Transitions use the document-level View Transitions API: `document.startViewTransition` snapshots the **whole document**, so even an unrelated hover re-snapshots everything.
3. Styles are inline (a streaming-preview constraint), so container queries and motion classes are emulated in JS rather than declared in CSS.

## What production must do instead (for a dedicated build session)
- Component-scoped state: each card, rail, Benny and the ledger own their state; cross-component changes flow through one shared store with selectors so only subscribers re-render.
- Element-scoped layout animation (Motion `layoutId` + `AnimatePresence`, or scoped view transitions when available); never a document-level snapshot for a local change.
- CSS Grid + Subgrid + Container Queries in stylesheets; `cqi`-based type; `@container` for the per-component size variants shown here (overview / rail / open; full / short / verb-only text).
- Carbon motion tokens as named CSS custom properties (see `package.yaml → extensions.dt.motion_tokens`); duration scales with distance.
- Reduced-motion: every move has a non-animated equivalent (already respected in the wireframes).

## What the wireframes ARE for
The behaviour, the choreography order (lift → rail → rest; exit fast, enter after), the size variants per component, the ripple grammar (connector → pulse → old→new → chip → ledger sentence), Benny's push-not-overlay rule, and the nested-subgrid specimen structure. Treat these as the spec; do not copy the code.
