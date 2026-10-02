# Logo and Slogan

## What ships, and what each variant is for

All files in `assets/logo/` are RGB PNG with transparency.

**One filename change from the original asset pack:** LG names the wide lockup files
`LGE_2D+LG-Electronics_...`. The `+` is rejected by some archive and packaging tools, so inside
this skill they are `LGE_2D_LG-Electronics_...`. The image bytes are untouched — only the name
differs, so a hash check against the original pack still matches. The CMYK set lives in the original asset
pack under `04_logo/cmyk/` — use those for print separations.

| File (in `assets/logo/`) | Contents | Canvas | Aspect (canvas) |
| --- | --- | --- | --- |
| `LGE_2D_LG-Electronics_Logo_HeritageRed_Grey_RGB.png` | symbol + "LG Electronics" | 5452 × 1130 | 4.825 : 1 |
| `LGE_2D_LG-Electronics_Logo_HeritageRed_White_RGB.png` | as above, white logotype | 5452 × 1130 | 4.825 : 1 |
| `LGE_2D_LG-Electronics_Logo_Mono_Black_RGB.png` | all black | 5452 × 1130 | 4.825 : 1 |
| `LGE_2D_LG-Electronics_Logo_Mono_White_RGB.png` | all white | 5452 × 1130 | 4.825 : 1 |
| `LGE_2D_LG-Electronics_Logo_Mono_*_Small-Size_RGB.png` | small-size optimised | 165 × 34 | 4.853 : 1 |
| `LGE_Logo_HeritageRed_Grey_RGB.png` | symbol + "LG" | 2081 × 1127 | 1.847 : 1 |
| `LGE_Logo_HeritageRed_White_RGB.png` | symbol + "LG", white | 2081 × 1127 | 1.847 : 1 |
| `LGE_Logo_Mono_Black_RGB.png` | symbol + "LG", black | 2079 × 1127 | 1.845 : 1 |
| `LGE_Logo_Mono_Black_Small-Size_RGB.png` | small-size optimised | 63 × 34 | 1.853 : 1 |
| `LGE_Logotype_Black/Grey/White_RGB.png` | "LG Electronics" wordmark only | 4509 × 1127 | 4.001 : 1 |

### Two gaps worth knowing before you pick a variant

**There is no all-white mono version of the compact `LGE_Logo` (symbol + "LG") lockup** — not in
RGB, not in CMYK. The all-white mono exists only for the longer `2D+LG-Electronics` lockup. So on
a dark or image background where you want the compact mark, use
`LGE_Logo_HeritageRed_White_RGB.png` (red symbol, white logotype), which BI p.21 approves for black
and image grounds. The one all-white symbol in the pack, `04_logo/cmyk/Logo LG_Mono_Full white.png`
(1080 × 1080), is the symbol alone — subject to the symbol-alone restriction.

**Minimum size is rarely the binding constraint — check it anyway on small formats.** With the
symbol at 1.3X, a canvas needs a short edge of about 62 mm before the symbol drops under the
4 mm floor, or 246 px before it drops under 16 px. So A5 and above, and any social format, clear
it comfortably. Small collateral — a business card, an email signature — does not, which is why
those have their own specified sizes in `print-and-collateral.md`.

The **Small-Size** files are separately drawn for small reproduction, with strokes thickened so the
mark survives. Use them wherever the logo lands under roughly 60 px wide — not the full-size file
scaled down, which goes muddy.

**Default choice:** `LGE_Logo_HeritageRed_Grey_RGB.png` (symbol + "LG") for most layouts;
the `2D+LG-Electronics` lockup where the full company name is required.

### Pick one lockup and keep it — the mistake this skill made

The compact symbol + "LG" and the wide symbol + "LG Electronics" are **different marks**, not
two sizes of one mark. Product, channel and campaign work uses the compact one. The wide
corporate signature is for pieces that require the full company name.

A deck built with this skill used the compact lockup on its light slides and the wide one on
its dark slides, and passed every check: right size, permitted position, good contrast on each
slide taken alone. The brand simply changed identity halfway through the deck. The reason was
not a design decision — it was that the missing all-white compact file made the wide white file
the one that *existed*, and a hint in `verify.py` recommended it.

**On a dark or image ground the compact lockup is `LGE_Logo_HeritageRed_White_RGB.png`** — the
Heritage Red symbol with a white logotype, which S1 p.21 approves for black and image
backgrounds. The absent all-white compact mono file is never a reason to switch lockup family.

`verify.py` now checks this across the whole piece: `LOGO_VARIANT_MIXED` is an error when a
deliverable carries more than one lockup, `LOGO_CORPORATE_LOCKUP` warns when the wide signature
is used, and `LOGO_WORDMARK_ALONE` warns when the "LG Electronics" wordmark appears without the
symbol.

### The symbol mark alone

The symbol may appear **without the logotype only** on business cards and badges, and as an icon on
websites, mobile apps and PC. Anywhere else, the symbol alone is a prohibited use — the guideline
states it directly in two places.

### The logotype colour

The "LG Electronics" logotype is only ever **LG Gray (C0 M0 Y0 K70)**, Black, or White.
`#4A4946` (Warm Gray 02 / Pantone Cool Gray 11 C) is the value the collateral pages give for LG Gray
in Pantone terms; the CMYK build C0 M0 Y0 K70 is what the logo section specifies. Use the supplied
Grey artwork rather than recolouring, and this question does not arise.

### The retired 3D logo

The 3D logo is discontinued — 2D only. The old logo-plus-slogan combination lockup is also retired.

### Korean-market logo

A Korean version exists that must include the company name. Korea only; not relevant to Vietnam
or other markets.

## Clear space and minimum size

**Source values (BI master PDF p.19–20, repeated in BI Workshop 2025 p.19–20):**

- Horizontal logo: clear space is **0.15X of the symbol size**.
- Vertical logo: clear space is **15% of the logo size**.
- Minimum size, both: the logo must be at least **4 mm / 16 px tall**.
- No other element may sit inside the clear space.

**Measured from the asset files, which matters in practice:** the shipped PNGs already carry
transparent padding on every side. In `LGE_2D_LG-Electronics_Logo_HeritageRed_Grey_RGB.png` the
symbol is exactly 758 × 758 px inside a 5452 × 1130 canvas, with 188 px padding left, 187 right,
186 top and bottom — that is **0.248 × the symbol size**, comfortably above the 0.15X minimum. The
same ratio holds in the other lockups.

The useful consequence: **place the PNG at its full canvas and treat the canvas edge as the clear
space boundary.** Nothing else touches the canvas rectangle. Doing that satisfies the rule with
margin to spare, and removes any need to compute clear space by hand. If you crop the padding off
for any reason, you must then add ≥ 0.15 × symbol height of space back manually.

Geometry worth keeping to hand: **symbol height ÷ canvas height = 0.671**. So if a spec asks for a
symbol of height *S*, place the PNG at canvas height *S ÷ 0.671*.

Minimum size in canvas terms: the 16 px / 4 mm floor refers to the *logo*, so with the padding
included a canvas height of at least ~24 px keeps the mark itself above 16 px.

## Colour variation on backgrounds

The logo may sit on white, black, Active Red, LG Red, Warm Gray, or an image — with the variant
chosen for contrast. Approved pairings from the source:

| Background | Logo variant |
| --- | --- |
| White or light warm grey | Heritage Red symbol + Grey logotype |
| LG Active Red | white logotype variant, or full white mono |
| LG Red (Heritage) | white logotype variant, or full white mono |
| Black | Heritage Red + White, or full white mono |
| Warm Gray (dark end) | white mono |
| Photography / gradient | Heritage Red + White, or full white mono — whichever holds contrast |

Two named failures: **never on a busy background**, and **never a red symbol on a red background**.

## Size and placement on a layout

From the grid section (PDF p.77), with the margin *X* computed as in `layout-grid.md`:

- **Symbol height = 1.30 X.** The page states "The Logo is 1.3X the size of our margins"; the
  diagram beside it resolves what is being measured. A 220 dpi render of that diagram gives:
  the left column marked **X** is 76 px wide, the band labelled **1X** is 78 px tall, the band
  labelled **1.3X** is 101 px tall (= 1.33X), and the red symbol sitting in that band is
  **100 px tall**. The bands measure height, and the symbol fills the 1.3X band.
  The same page's placement artboard confirms it independently: artboard 774 × 324 px, logo
  inset 16 px from the edge (= 5% of the 324 px short edge, so X = 16), symbol height 19–20 px
  = 1.2–1.3X. If 1.3X were the lockup's *width*, the whole logo would be 20.8 px wide there —
  but the symbol alone measures 20 px wide, leaving nothing for the logotype. Width is ruled out.
- **Place the file by height, not width.** Because the PNGs carry clear-space padding, a file
  set to 1.3X puts the symbol at only 0.87X — about a third undersized. Divide by the symbol's
  share of the canvas: **file height = 1.30 X / 0.668 = 1.95 X** for the compact `LGE_Logo_*`
  lockup, or **/ 0.671 = 1.94 X** for the wide one. Let the width follow from the aspect ratio;
  that way either lockup lands correctly without a second calculation.
- **Five permitted positions:** bottom-left, middle-left, upper-left, upper-centre, upper-right.
  Nothing else. Bottom-right in particular is not on the list.
- The logo aligns to the margin, so its canvas edge sits on the margin line.

Note on the bundled PPTX templates: their logo pictures are ~0.71 in wide on a 13.33 × 7.5 in
slide. Under the corrected reading the guideline calls for a file height of 1.95 × 0.375 in =
0.73 in, which for the compact lockup is ~1.35 in wide — so the templates are *smaller* than the
guideline, not larger. Follow the guideline; the grid section is the authority on sizing.

### Format-specific overrides

These replace the 1.3X rule in their own contexts — see `layout-grid.md` for the full set.

- **Video / social end frames:** 16:9 — symbol height = 3X of a 25-row grid, or 12% of frame height,
  centred. 1:1 and 9:16 — symbol width = 6X of a 20-unit grid, or 30% of frame width, centred.
- **Top-left corner logo in video (optional):** symbol height = 1/20 of frame height (or 5% of it),
  positioned with a margin of 1.5 × logo width from the left and 1 × logo height from the top.
- **OOH:** taking the height of the whitespace band as 1X, logo height is at least 2.5X. Logo goes
  top-left; slogan, if used, bottom-left.

## The Slogan — "Life's Good"

Files in `assets/slogan/`, all RGB PNG:

| File | Canvas | Aspect |
| --- | --- | --- |
| `LGE_Electronics_Slogan_Horizontal_Mono_ActiveRed_RGB.png` | 3832 × 870 | 4.405 : 1 |
| `LGE_Electronics_Slogan_Horizontal_Mono_Black_RGB.png` | 3832 × 870 | 4.405 : 1 |
| `LGE_Electronics_Slogan_Horizontal_Mono_White_RGB.png` | 3832 × 869 | 4.409 : 1 |
| `LGE_Electronics_Slogan_Stacked_Mono_ActiveRed_RGB.png` | 2171 × 1507 | 1.441 : 1 |
| `LGE_Electronics_Slogan_Stacked_Mono_Black_RGB.png` | 2171 × 1507 | 1.441 : 1 |
| `LGE_Electronics_Slogan_Stacked_Mono_White_RGB.png` | 2171 × 1507 | 1.441 : 1 |

The slogan is drawn in a **custom typeface built only for it**. That typeface is not available for
any other text, and the slogan is never set from a font — it is always this artwork. The four
supplied colours (Active Red, White, Black — and Warm Gray / gradient backgrounds behind them) are
the only permitted colours; a gradient background behind the slogan is allowed, a gradient *fill*
inside it is not.

Measured padding: ink sits inside a 144 px transparent border on all sides of each file. As with the
logo, place at full canvas and the clear space is handled — the stated rule is *keep an area the
size of the period in the slogan around the asset*.

### Roles

The slogan is used **either** as a lead message **or** as a sign-off, never both in one piece, and
**never without the logo somewhere in the application**.

- **Sign-off:** visible slogan height = **0.90 X** (0.9 × the grid margin). Measured the same way
  as the logo: on p.78 the X column is 77 px, the 1X band is 78 px, and the band labelled 0.90X
  is 70.5 px = 0.92X, hugging the artwork. The file carries padding (ink is 0.669 of canvas
  height), so **place the file at 0.90 X / 0.669 = 1.35 X tall**. Horizontal version only — the
  stacked slogan is explicitly not for sign-off. It can sit on the same vertical axis as the logo,
  or in the opposite corner.
- **Lead message:** the slogan is scaled to align with the left and right edges of the full grid.
  If horizontally centred, place it vertically centred or at the bottom. Images may sit in front of,
  behind, or in the middle of the slogan to create a sense of space — sized so the slogan still
  reads easily.

### The separation rule

**Do not place the LG logo and the slogan next to each other.** They go in different regions of the
layout with real space between them — logo top-left and slogan bottom-left is the canonical pairing.
This appears four times across the logo, slogan and grid sections, which is a good indication of how
often it is got wrong.

### Video and event sizing

- 16:9 — height of the slogan's "L" = 2–4X on a 20-row grid, i.e. 10–20% of frame height, centred.
- 1:1 — slogan width = 8–14X on a 20-column grid, i.e. 40–70% of frame width, centred.
- 9:16 — slogan width = 14X, i.e. 70% of frame width, centred.
- End frame order, recommended: slogan over footage, then logo. On a plain white or black
  background instead of footage, the same order applies.
- All videos: master logo on screen for **at least 1 second**. Videos over 30 seconds: at least
  0.5 s for the slogan plus 1 s for the master logo. The master logo is optional for videos of
  6 seconds or less. No jingle. No CTA in the end frame.
