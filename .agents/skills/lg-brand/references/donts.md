# The prohibition list

Consolidated from the four Don'ts pages in the source. Use it two ways: as a pre-flight check
before declaring a piece finished, and as the checklist when the task is "review this design".

## Logo (BI master PDF p.23 — 14 named failures)

1. Don't recolour the logo.
2. Don't change the relationship between the symbol mark and the logotype.
3. Don't rotate, stretch, squash or crop the logo.
4. Don't use the logo smaller than specified (4 mm / 16 px minimum height).
5. Don't use shadows or effects.
6. Don't obscure the logo.
7. Don't use the previous 3D slogan combination.
8. Don't create your own logos.
9. Don't apply perspective to the logo.
10. Don't use the symbol mark without the logotype (except business cards, badges, and website /
    mobile / PC icons).
11. Don't use the logo inside a sentence.
12. Don't use the wrong ratio between the symbol and the logotype.
13. Don't use a logo colour that is hard to read on a bright background.
14. Don't use a red symbol on a red background.

Plus, from the clear-space and colour pages: don't place the logo on a busy background, and don't
let any element enter the clear space.

## Slogan (BI master PDF p.81 — 8 named failures)

1. Don't crop or obstruct the legibility of the slogan.
2. Don't add effects — including outlines and transparencies.
3. Don't use the logo together with the slogan.
4. Don't rotate or skew the slogan.
5. Don't position the slogan randomly — follow the layout system.
6. Don't use the slogan more than once in one application.
7. Don't use the slogan as a font. Its typeface exists only for this asset.
8. Don't let images cover the slogan in a way that makes it hard to see.

Plus: the slogan is never used without the logo somewhere in the application, and never as both a
lead message and a sign-off in the same piece. The stacked slogan is never used as a sign-off.

## Gradients (BI master PDF p.58 — 10 named failures)

1. Don't alter existing gradients or create new ones — use the supplied assets.
2. Don't use gradients outside their intended usage, such as inside text.
3. Don't use two gradients at the same time.
4. Don't crop a gradient so far that it stops looking like a gradient.
5. Don't use arbitrarily changed gradients.
6. Don't use gradients inside shapes.
7. Don't use gradients on surfaces that cannot express them — vehicles are named.
8. Don't use meaningless gradients that disregard the brand's values and messaging.
9. Don't use gradients on images that are too small.
10. Don't combine too many colour gradients.

## Colour (BI master PDF p.47 — 6 named failures)

1. Don't use colours that evoke a competitor's brand image.
2. Don't use colours that directly evoke a competitor's products.
3. Don't use excessive red where it isn't relevant to the content.
4. Don't use extreme display settings that misrepresent Active Red.
5. Don't use colour combinations that don't align with the content.
6. Don't use too many colour combinations in a single piece.

## Typography

- Don't use the retired LG Smart font.
- Don't set LG EI Headline below 18 pt.
- Don't combine LG EI with a font that looks similar to it.
- Don't apply faux bold or faux italic to an LG EI Text weight — pick the correct family instead.
- Don't substitute a lookalike font for Vietnamese; LG EI covers it fully.

## Web (LG.com)

- Don't embed text inside images — the web guide treats this as an accessibility violation.
- Don't use SemiBold or Bold as the general working weight on LG.com; Regular is.
- Don't use the 1600 px "Narrow" hero size; the guide marks it as not recommended.
- Don't ship a text/background pair below 4.5:1 contrast.

## Failure modes this skill sees most often

Not from the source — these are the practical ways an otherwise-good LG piece goes wrong:

- **Font silently substituted.** LG EI Text weights each declare their own family name, so a
  `font-weight: bold` on `"LG EI Text"` resolves to nothing and the browser uses a system font. The
  output looks fine at a glance and is wrong throughout.
- **Logo and slogan placed together** because they read as a natural pairing. They aren't one.
- **Margin encroachment.** A page number, a caption or a footnote drifting into the 5% margin
  breaks the grid's whole effect.
- **Wrong red.** `#EA1917` used off-web, or `#FD312E` used on lge.com.
- **Logo redrawn** as a circle plus letters, or fetched from a web search instead of the supplied
  asset — usually visible in the letterform weights and the smile curve.
- **Small logo scaled down from the full-size file** instead of using the Small-Size artwork, which
  goes muddy below about 60 px.
