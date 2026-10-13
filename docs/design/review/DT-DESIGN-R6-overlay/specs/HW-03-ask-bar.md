# HW-03 — The ask bar: agent input in plain words

Source: `#hw-ask-wrap` and `onAsk` / `onTalk` in `sources/prototypes/House World.dc.html`. Replaces the R5 "PLAY WELL bubble" link. Governed by the operator principle: AI conversation arrives as plain language (tap / type / talk), never as an unexplained status grid; AI origin is permanently visible.

## 1. What it is

A single pill under the wordmark that says what it is for before you use it:

> **Describe what you want to build or change…** · 🎙 (dashed) · **GO**
> *One day you will type or talk here and the table drafts the change. Today it finds the right room for what you describe.*

The hint sentence is the honesty line (N-06). It is always visible while the bar sits under the wordmark, and reappears whenever the bar has something to say.

## 2. Placement and life

| state | where | hint |
|---|---|---|
| tour, progress < 10 %, poster present | under the wordmark: `top = max(17%,112px) + clamp(300px,40vw,700px)`, left 5 %, width min(560px, 80vw) | shown |
| tour ≥ 10 %, poster gone, settled, held, or tour off | docked bottom-left, `bottom 132px` (above the chapter caption) | hidden unless there is a note |
| flying or a sheet open | opacity 0, pointer-events none | — |

Moves with a 500 ms ease on top/bottom; 300 ms on opacity. The hover card dodges it (HW-01 §3).

## 3. What it does today (routing, not drafting)

1. Trim the text. Empty → nothing.
2. Case-fold and look for the text as a **substring** of each sheet's *title · verb · detail · room title · room kind · room what* (HW-02 §3) — same fields as the finder, minus the code.
3. **A hit** → note *That sounds like <room> — flying there. The finder above can narrow it down.* and start a room flight (HW-01 §4) to the first hit's room with that sheet selected.
4. **No hit** → note *Nothing matched exactly. The finder above has every sheet by room.*, copy the words into the finder, open its list, focus it.

It never fabricates an answer, never shows a spinner, never says "thinking". Known limit: literal matching (D-18).

## 4. Talk

The microphone is a dashed-outline button titled *Talk instead of typing (coming later)*; pressing it sets the note *Talking is not wired up yet. For now, type what you want and press Go.* Dashed = not yet real, the same convention as concept doors (HW-02 §1). It must not record.

## 5. Accessibility

`<form>` submit on Enter; visually-hidden `<label for="hw-ask">`; talk button has `aria-label`; notes are rendered in the bar and echoed through the page's polite live region via the flight announcement. 40 px controls inside a 52 px pill; mono `GO` on studio red; text 15 px Libre Franklin in studio-white on studio-bg.

## 6. What the future agent inherits

- The place: same pill, same position rule, same honesty line (rewritten when drafting is real).
- The contract: input → **a destination plus a sentence** that says why. When drafting exists, the sentence must say what the table *proposes* and where the proposal will appear (which room, which sheet), and the proposal must carry the AI-origin marker from the evidence axes before anything becomes a record.
- Talk reuses the same input; the dashed outline becomes solid when it is live.
