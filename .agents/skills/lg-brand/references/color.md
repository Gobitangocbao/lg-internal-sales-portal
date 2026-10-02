# Colour

Two independently verified sources agree exactly: the swatch page of the BI master guideline
(`01_LG_BI_Guidelines_V5_MASTER.pdf`, PDF p.40 / doc p.16) and the Adobe swatch exchange files
`LGE_Core Brand Assets_Color_Palette_RGB.ase` and `..._CMYK.ase`. Every RGB value below was parsed
byte-for-byte out of the ASE files and then confirmed against the printed swatch page. Pantone and
CMYK come from the swatch page.

## Core palette

| Name | HEX | RGB | CMYK | Pantone |
| --- | --- | --- | --- | --- |
| LG Active Red | `#FD312E` | 253, 49, 46 | C0 M97 Y95 K0 | 2034 C |
| LG Red (Heritage Red) | `#A50034` | 165, 0, 52 | C0 M100 Y62 K22 | 207 C |
| White | `#FFFFFF` | 255, 255, 255 | C0 M0 Y0 K0 | — |
| Black | `#000000` | 0, 0, 0 | C76 M68 Y60 K82 | Black 3 C |
| Warm Gray *(core swatch)* | `#F6F3EB` | 246, 243, 235 | C4 M5 Y7 K0 | 9080 C |

The core "Warm Gray" swatch and "Warm Gray 07" in the supporting ramp are the same colour — this is
confirmed in both ASE files, not an error in transcription.

## Supporting palette — warm grey ramp

Dark to light. This ramp does the quiet work: backgrounds, panels, body text, dividers.

| Name | HEX | RGB | CMYK | Pantone |
| --- | --- | --- | --- | --- |
| Warm Gray 01 | `#262626` | 38, 38, 38 | C69 M61 Y56 K65 | Black 2 C |
| Warm Gray 02 | `#4A4946` | 74, 73, 70 | C61 M54 Y53 K51 | Cool Gray 11 C |
| Warm Gray 03 | `#716F6A` | 113, 111, 106 | C48 M41 Y42 K23 | Cool Gray 9 C |
| Warm Gray 04 | `#CBC8C2` | 203, 200, 194 | C23 M20 Y22 K2 | Cool Gray 3 C |
| Warm Gray 05 | `#E6E1D6` | 230, 225, 214 | C10 M10 Y13 K0 | Cool Gray 2 C |
| Warm Gray 06 | `#F0ECE4` | 240, 236, 228 | C5 M7 Y9 K0 | Cool Gray 1 C |
| Warm Gray 07 | `#F6F3EB` | 246, 243, 235 | C4 M5 Y7 K0 | 9080 C |

Two further greys appear only in the web system and are legitimate there but not in the BI palette:
`#646464` (Mid Gray 2) and `#333333` / `#1A1A1A` (Dark Gray 1 / 3). See `web-system.md`.

## The Active Red discrepancy — read this before picking a red

The BI master guideline and the LG.com Web Style Guide give **different hex values for Active Red**:

| Source | Active Red |
| --- | --- |
| BI Guidelines V5.2 p.40 + both ASE files | `#FD312E` |
| LG.com Web Style Guide v1.3, p.10, p.11, p.14, p.66 | `#EA1917` |

This is not a transcription error — `#EA1917` appears four separate times in the web guide with its
RGB spelled out (R234 G25 B23). Both documents are official and current.

**The rule that follows from it:** if the output is an LG.com web property or a component built to
the LG.com design system, use `#EA1917`. For everything else — print, slides, social, OOH, events,
retail, internal — use `#FD312E`. If a piece is genuinely both (a web banner that will also be
printed), say so and let the user choose; do not silently average them or pick the prettier one.

## Using the palette

Red carries the brand; the warm greys carry everything else. The source describes the greys as
adding "warmth to our communication" and being applicable to all content — which is why an LG
layout reads warm rather than clinical, and why plain `#FFFFFF` or a cool grey background usually
looks subtly off-brand even when nothing is technically wrong.

Heritage Red (`#A50034`) is the historic brand red and the symbol colour. Active Red (`#FD312E`) is
the newer, brighter accent introduced in V5 for vibrancy. Both are current; they are not
interchangeable within one composition — pick the one that suits the tone and stay with it.

Accent colours outside the palette **are** allowed when content needs them, with one explicit
constraint from the source: avoid colours that evoke competitors or competitors' products.

### Things to avoid (source: BI master PDF p.47)

1. Colours that evoke a competitor's brand image.
2. Colours that directly evoke a competitor's products.
3. Excessive Red where it is not relevant to the content.
4. Extreme display settings that misrepresent Active Red.
5. Colour combinations that do not align with the content.
6. Too many colour combinations in a single piece.

## Gradients

Four fixed master gradients ship in `assets/gradients/` (`LGE_Electronics_Gradient_01..04_RGB.jpg`).
The masters are square, supplied at 2000 × 2000 px; the copies bundled here are 1400 × 1400 px for
file size — use the originals in the asset pack for large-format print.

They run 01 → 04 in feel, from **Warm** to **Innovative**. Gradient 04 is specifically cited as
suited to emphasising innovation in a product context.

Rules from the source (PDF p.50–58):

- **They cannot be modified or new ones created.** Crop and rotate only.
- Crop so that **at least two colours remain visible**, otherwise the gradient stops reading as one.
- Choose one of five crop shapes to suit the medium: Extreme Portrait (tall web banners), Portrait
  (mobile, 6-sheet, common print), Square (social), Landscape (digital, video, 48-sheet), Extreme
  Landscape (very wide stage/event formats).
- **Never two gradients in the same piece.**
- Never inside text, never inside shapes, never on small images, never on surfaces that cannot
  express a gradient (vehicle wraps are called out by name).
- Use them where richness and depth matter — hero brand moments, large event screens, packaging,
  web banners and social — in place of a flat colour, not on top of one.

## Accessibility

The LG.com guide commits to WCAG 2.2 AA and requires a contrast ratio of at least **4.5:1** between
text and background. Combinations the guide explicitly clears at AA: Heritage Red, Mid Gray 01,
Light Gray 01–03 and White against black; black and white against the light greys; white on
Heritage Red. `#646464` on white is called out as failing (1.28:1 in the source's own annotation).

Active Red on white is close to the line — check any red text with a contrast tool rather than
assuming. Red is safest as a fill with white text on it, or as an accent, not as body copy.

## Measured contrast — which pairings actually read

The guideline gives no contrast guidance, so these were measured with `verify.py`'s own maths
(WCAG). They are why `lg-tokens.css` assigns the semantic roles it does, and why `verify.py`
flags `TEXT_CONTRAST`.

| On Warm Gray 07 `#F6F3EB` (the light ground) | | On Warm Gray 01 `#262626` (the dark ground) | |
| --- | --- | --- | --- |
| Warm Gray 01 | **13.7:1** | Warm Gray 07 | **13.7:1** |
| Warm Gray 02 | **8.1:1** | Warm Gray 05 | **11.6:1** |
| Warm Gray 03 | **4.5:1** — the floor for small text | Warm Gray 04 | **9.1:1** |
| Warm Gray 04 | **1.5:1** — rules only, never text | Warm Gray 03 | **3.0:1** — large text only |
| Active Red | **3.3:1** — large text and marks, not body | Active Red | **4.1:1** — large text and marks |
| Heritage Red | **7.1:1** | Heritage Red | **1.9:1** — do not use on dark |

Two more worth knowing: on a Warm Gray 06 panel, Warm Gray 03 drops to **4.3:1**, so captions
*inside* a panel need Warm Gray 02. And white on the LG.com web red `#EA1917` is **4.5:1** —
LG's own button passes, just; white on Active Red `#FD312E` is **3.7:1** and is large-text only.

The trap this closes: **Warm Gray 04 on Warm Gray 07 is 1.5:1**. Both are LG colours, the
pairing looks entirely on-brand, and it is unreadable. It shipped once.
