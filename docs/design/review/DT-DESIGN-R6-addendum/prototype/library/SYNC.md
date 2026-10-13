# Component copies

The five component DCs here (GapCloser, SetRef, CrossRef, ReleaseGate, Blocker) are **copies** of `prototypes/*.dc.html`, present only so the standalone bundle of D-01 can embed them. Source of truth is `prototypes/`. Re-copy after any change (the handoff bundling step does this).

A root-level `SetRef.dc.html` copy exists for the Hub (paths rewritten `../dt/` → `dt/`). Same rule: `prototypes/` is the source.
