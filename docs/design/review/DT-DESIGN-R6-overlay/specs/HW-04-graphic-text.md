# HW-04 — Graphic text, bubbles and gradients

Source: the PLAY WELL poster, chapter captions, dashboard title and concept-door title in `sources/prototypes/House World.dc.html`; `@font-face` and `body` palette in its helmet. This is also the brief for the vector wordmark (N-04).

## 1. The technique — layered stroke type

Every display word is **three stacked copies of the same text** in one inline-block, plus a hard drop shadow on the whole stack:

| layer | position | colour | stroke | purpose |
|---|---|---|---|---|
| 1 outline | absolute, inset 0, `aria-hidden` | `--studio-yellow` fill + `-webkit-text-stroke` **.1em** yellow, `paint-order: stroke fill` | thick | the brick-yellow halo |
| 2 inline | absolute, inset 0, `aria-hidden` | `--studio-white` fill + stroke **.035em** white | thin | the ink keyline that separates halo from face |
| 3 face | relative (the readable copy) | gradient-clipped (poster) or solid ink (captions/titles) | none | the text screen readers get |
| shadow | `filter: drop-shadow(X X 0 var(--studio-red))` on the stack | studio red | — | the printed-poster offset |

Only layer 3 is read aloud. Letter-spacing is negative so the halos fuse into one shape.

## 2. The four sizes

| use | font | size | tracking / leading | shadow | stroke 1 | notes |
|---|---|---|---|---|---|---|
| **Poster** PLAY / WELL | DynaPuff 700 | `clamp(130px, 19vw, 340px)` | −.055em / .86 | 12px 12px 0 | .1em | rotated −6° about left-centre; two words stacked, second indented .1em; face is the gradient sweep (§4) |
| **Chapter caption** | DynaPuff 700 | `clamp(28px, 3vw, 44px)` | −.025em / 1.12 | 3px 3px 0 | .1em | enters with `hwCaption` (.5 s, 6 px rise); face `--studio-white` |
| **Sheet title** (dashboard h2) | DynaPuff 700 | 20px | −.025em / 1.18 | 2px 2px 0 | .09em | face `--dt-ink`; sits inside the dashed room pill |
| **Concept-door title** (h3) | DynaPuff 700 | 34px | −.025em | 3px 3px 0 | .1em | face `--dt-ink` |

Secondary display (no strokes): DynaPuff 400 for room/sheet titles in lists (14–18 px, −.015em). Everything else is Libre Franklin (body) and Azeret Mono (codes, labels, `GO`, hints — 10–11 px, .08–.12em tracking, uppercase).

## 3. Studio palette

Set on `body`, switched by `.dt-blueprint` (shared preference, N-05). These are the only colours the graphic text and bubbles use besides DT tokens.

| token | paper | blueprint | role |
|---|---|---|---|
| `--studio-bg` | #EAE8DA | #172B40 | bubble fill, text shadow halo |
| `--studio-white` | #172B40 | #FFF4D6 | bubble ink, caption face, thin keyline |
| `--studio-red` | #FF533D | #FF533D | hard drop shadow, GO, brand brick |
| `--studio-yellow` | #FFD23F | #FFD23F | thick halo |
| `--studio-glow` | #3F6A8F | #FFE17D | the gradient highlight |

Red and yellow are constant across themes (they are brick colours); bg/white invert; the glow is blueprint-blue on paper and warm highlight on blueprint.

## 4. The gradient sweep (poster face only)

```
background-image: linear-gradient(105deg, white 0%, white 42%, glow 50%, white 58%, white 100%);
background-size: 300% 100%;
background-position: P% 50%;     /* P = min(1, progress / .07) × 100 */
-webkit-background-clip: text; background-clip: text; color: transparent;
```
A 16 %-wide highlight band crosses the word once as the user begins to scroll (0 → 7 % progress), in step with the wordmark settling from scale 1.14 to 1 (0 → 8.5 %) and before it fades (7 → 12 %). No time-based animation — the sweep is scroll-driven so it is still, not looping, while the page rests.

## 5. Bubbles (pills and cards)

| element | radius | fill / ink | border | shadow |
|---|---|---|---|---|
| Ask bar, finder input, theme toggle | 999px | `--studio-bg` / `--studio-white` | 1px `color-mix(studio-white 45–55%, transparent)` | ask bar: `0 10px 30px color-mix(studio-bg 50%, transparent)` |
| Brand button | 16px | studio-bg / studio-white | transparent → 45 % white on hover | — |
| Hover card | 14px | studio-bg / studio-white | 1px 40 % white | `--dt-shadow` |
| Status pills (flying / settled) | `--dt-r-pill` | `--dt-plate` / `--dt-on-plate` | — | `--dt-shadow` |
| Room switcher pill | `--dt-r-pill` | transparent / `--dt-ink` | 1.5px **dashed** `--dt-muted` → solid ink on hover | — |
| Sheet tabs | `--dt-r-pill` | active: plate / on-plate; idle: sheet / ink | 1.5px | — |
| Finder list, switch list, dashboard | `--dt-r-card` | `--dt-sheet` | 1px `--dt-ink` | `--dt-shadow` |

Rule: **studio** colours for things that float over the house; **DT** tokens for anything that is, or belongs to, a sheet. Dashed = not real yet (talk, concept doors, room switcher's "other rooms").

Body text that sits directly over the 3D view gets a halo instead of a box: `text-shadow: 0 1px 2px var(--studio-bg), 0 0 8px var(--studio-bg)`.

## 6. Font loading

DynaPuff 400–700 vendored at `house/fonts/DynaPuff.ttf` (OFL beside it), `@font-face … font-display: block` + `<link rel=preload as=font crossorigin>`. Fallback stack `'Arial Rounded MT Bold', sans-serif`. A flash on first paint is still seen in some browsers (D-15); the vector wordmark (§7) removes it for the poster, not for captions.

## 7. Brief for the vector wordmark (N-04)

Produce `playwell.svg` reproducing §1–§2 Poster exactly: DynaPuff 700 outlines, −.055em tracking, .86 leading, two stacked words with WELL indented .1em, −6° rotation baked or applied by CSS, three paint layers (yellow .1em stroke, ink .035em stroke, face), red offset shadow as a fourth filled layer behind (not a filter). Colours must stay **CSS variables** (`currentColor` / `var(--studio-*)`) so the theme switch still works; the face must stay a separate `<g id="face">` so the gradient sweep can be applied by CSS `mask` or kept as live type. Keep `aria-hidden` on the graphic and the words in a visually-hidden element beside it. Size by width (56 % of viewport at 5 % left, top `max(17%,112px)`).
