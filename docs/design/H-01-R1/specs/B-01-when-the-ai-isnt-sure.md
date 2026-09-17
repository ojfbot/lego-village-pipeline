# B-01 — When the AI isn’t sure

**File:** `prototypes/Prototype B - When the AI Isnt Sure.dc.html` · **Journeys:** J1 J2 (reuse for J12) · **Status at handoff:** built
Behaviour reference is the live prototype; its code is not to be copied. All numbers are mock pending real math + audit.

## Purpose
The AI reads a builder's page (bl-741807), hits an ambiguous phrase ("for 4 tracks"), shows its work, and asks the operator — tap, type, or talk. The answer becomes the record; it never asks twice.

## Behaviour
- **The design in question**: listing card with rights status and a listing-visibility control (listing may be shown to family; the downloaded file stays operator-only until rights pass).
- **The conversation**: the AI states what it read, what it guessed (◇ AI GUESS), the options it sees (tap), a free-text field (type) and a mic (talk). On answer it restates what it heard before saving; the field gets ■ CONFIRMED or ▲ CORRECTED.
- **Paper trail** (plain-language five rows): WHO WROTE IT · HOW · HOW SURE · WHO DECIDED · STATUS; full chain behind disclosure.
- **Files & links**: browser download → drop → hash; immutable artifact; acquisition trail.

## States
unanswered · answered (confirmed/corrected) · on hold · listing visible/hidden to family · file present/absent.

## Copy rules
Terse AI. Never verbose explanation in the UI. Question first, evidence behind disclosure.
