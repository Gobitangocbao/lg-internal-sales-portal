# Grid and layout

LG's grid is deliberately tight. The source describes the intent as "the intelligent use of space,
tight margins and restricting font sizes" — the discipline is what makes a layout read as LG rather
than as generic corporate.

## Construction (BI master PDF p.76)

Everything derives from one number.

```
X (margin) = 0.05 × min(canvas_width, canvas_height)     # 5% of the SHORTEST edge
gutter     = X / 2                                        # always half the margin
columns    = 9        (or any multiple of 3 — 3, 6, 9, 12, 18 …)
rows       = 9        (or any multiple of 3)

logo symbol height = 1.30 X       # the visible symbol, not the file, not the width
slogan height      = 0.90 X       # the visible artwork, sign-off role

# the PNGs carry clear-space padding, so the placed file is larger than the mark:
logo file height   = 1.30 X / 0.668 = 1.95 X
slogan file height = 0.90 X / 0.669 = 1.35 X
```

The margin comes off the shortest edge, so on a wide canvas the left/right margins are the same
physical size as top/bottom — the frame stays even instead of getting pinched vertically.

Worked examples:

| Canvas | Shortest edge | X (margin) | Gutter | Symbol h (1.3X) | Logo file h (1.95X) | Slogan h (0.9X) | Slogan file h (1.35X) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1920 × 1080 (16:9 slide) | 1080 | 54 px | 27 px | 70.2 px | 105.1 px | 48.6 px | 72.6 px |
| 13.333 × 7.5 in (PPT wide) | 7.5 in | 0.375 in | 0.188 in | 0.488 in | 0.730 in | 0.338 in | 0.504 in |
| A2 poster 420 × 594 mm | 420 mm | 21 mm | 10.5 mm | 27.3 mm | 40.9 mm | 18.9 mm | 28.3 mm |
| A4 210 × 297 mm | 210 mm | 10.5 mm | 5.25 mm | 13.65 mm | 20.4 mm | 9.45 mm | 14.1 mm |
| 1080 × 1080 (social) | 1080 | 54 px | 27 px | 70.2 px | 105.1 px | 48.6 px | 72.6 px |
| 1080 × 1350 (social portrait) | 1080 | 54 px | 27 px | 70.2 px | 105.1 px | 48.6 px | 72.6 px |
| 1080 × 1920 (story) | 1080 | 54 px | 27 px | 70.2 px | 105.1 px | 48.6 px | 72.6 px |
| 1920 × 480 (web banner) | 480 | 24 px | 12 px | 31.2 px | 46.7 px | 21.6 px | 32.3 px |

The file heights assume the compact `LGE_Logo_*` lockup (symbol = 0.668 of canvas height) and
the horizontal slogan (ink = 0.669 of canvas height). For the wide `LGE_2D_LG-Electronics_*`
lockup the symbol is 0.671 of canvas height, so the file height is 1.94X and the width follows
its own 4.825:1 canvas aspect. Sizing by height and letting width follow is the reliable way to
place either lockup.

Column width falls out of the rest: `col = (W − 2X − 8×gutter) / 9` for a 9-column grid.

**Not specified in source:** whether the top/bottom margin is also 5% of the shortest edge or of the
height. The construction diagram shows a uniform frame, and the 5% figure is stated once for
"margins" without qualification, so a uniform margin on all four sides is the reading this skill
uses. Flag it if a piece is unusually elongated and the difference would be visible.

## Logo and slogan placement

Covered in detail in `logo-and-slogan.md`. In summary: symbol height 1.3X, sitting on the margin line,
in one of five positions (bottom-left, middle-left, upper-left, upper-centre, upper-right); slogan
sign-off 0.9X high, positioned relative to the logo but never adjacent to it.

## Format-specific grids

Some formats replace the 9 × 9 / 5% system entirely. Use these where they apply.

### Video and social end frames — logo

| Format | Grid | Logo size | Position |
| --- | --- | --- | --- |
| 16:9 TV / digital / social | 25 rows, X = height/25 | symbol height = 3X = 12% of height | centred both axes |
| 1:1 social | 20 units, X = width/20 | symbol width = 6X = 30% of width | centred both axes |
| 9:16 social | 20 units, X = width/20 | symbol width = 6X = 30% of width | centred both axes |

### Video and social end frames — slogan

| Format | Grid | Slogan size | Position |
| --- | --- | --- | --- |
| 16:9 | 20 rows, X = height/20 | height of the "L" = 2–4X = 10–20% of height | centred both axes |
| 1:1 | 20 cols, X = width/20 | width = 8–14X = 40–70% of width | centred both axes |
| 9:16 | 20 cols, X = width/20 | width = 14X = 70% of width | centred both axes |

### Optional top-left logo in video

Not mandatory. If used: X = height / 20 (or 5% of height); symbol height = X; margin from the
top-left corner = 1.5 × logo width horizontally and 1 × logo height vertically. No rule on how long
it stays on screen.

### OOH

Priority order for elements: **Logo → Image → Headline → Product name → Slogan.** Logo, image and
headline are required; product name and slogan are optional. Logo top-left, slogan bottom-left.
Logo height at least 2.5X where 1X is the height of the whitespace band. Outdoors with no
background wall, white logo is the general recommendation. Advertising messages must meet minimum
size standards for the viewing distance — that requirement does not apply to the logo or product
names. When a product name is shown, the letters "LG" are removed from it, since the logo already
says LG.

### lge.com and web components

The web has its own 24-column / 8-column system with fixed pixel margins — it does **not** use the
5% rule. See `web-system.md`.

## Composition

The source's own build sequence for a gradient-led layout is: **compose → crop → finish layout** —
choose the gradient for the tone you want, crop it so it keeps red and points of interest, then add
the brand assets on top. For the EI Form design system the sequence is compose → set background →
blur → finish layout, with a note that **25 px of blur** works for most high-resolution imagery
though it needs adjusting per image (BI Workshop 2025, p.62).

Two habits that keep layouts on-brand:

- **Leave the margin genuinely empty.** The tight margin only reads as confident if nothing creeps
  into it. A caption or page number pushed into the margin undoes the whole system.
- **Restrict the number of type sizes.** The source names "restricting font sizes" as part of the
  grid's character. Three sizes in a poster is usually plenty; five looks unresolved.
