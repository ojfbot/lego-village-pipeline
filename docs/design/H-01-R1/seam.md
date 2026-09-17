# Frame seam — assumptions and questions (not a contract)

Frame is the host: stitching, routing, shared context, navigation shell, fleet conventions. It does **not** provide the visual language. The Drafting Table token file (`dt/tokens.css`) is the project's single source of truth; Frame aliases map onto it.

## Assumptions we designed against
1. Frame exposes theme mode (light/dark) and density; we map them to `body.dt-blueprint` and to nothing (density is baked into the sheets) — an alias layer, not new tokens.
2. Frame owns top-level navigation; each sheet renders inside a content slot and keeps its own in-sheet header (title · meta · ← HUB / theme toggle) until Frame provides breadcrumbs.
3. Frame provides identity/actors: `@jfo` (operator), `@boys` (family), `AI`. Sheets show tag states ◇ needed from · ■ did · ○ waiting on.
4. Frame provides routing between sheets by stable id (A-01, B-01, C-01, P-01, F-01, J-01, D-01, Hub, H-01). Cross-links in prototypes are relative file paths; replace with Frame routes.
5. Frame provides the storage/API boundary; sheets are pure UI over `packages/schema` entities plus the requests above.
6. Speech input (F-01, B-01 talk) uses the browser Web Speech API in prototypes; Frame may substitute its own capture.
7. Claude calls (B-01 interpretation, A-01 ASK, P-01 ask box, F-01 wand) are mocked with keyword parsers; in production they go through one Frame-mediated client with the current plan/evidence in context, and the AI **restates what it changed before anything is saved**.

## Questions for the Frame team
- Which Frame tokens exist for theme/density and how are they exposed (CSS vars? data-attrs?)
- Does Frame own the decision log, or do sheets post entries to it? (Hub decision log assumes a shared ledger with blast-radius links.)
- Where does the family posture live: same app with role-gated sheets, or a separate surface? F-01 assumes same tokens, same request card, role filtering (private listings never rendered to family).
- File attachments (Studio .io, photos, downloaded designs under rights review): Frame storage with operator-only visibility until rights pass?
- Offline/tablet: is a PWA shell provided?
