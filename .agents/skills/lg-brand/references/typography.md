# Typography

LG uses one type system, **LG EI** (Emotionally Intelligent), in two families. All nine files ship
in `assets/fonts/` as OTF. There is no licensed web-font CDN — embed the OTFs.

- **LG EI Headline** — key messages, titles, anything that needs to carry the brand voice.
- **LG EI Text** — body copy, UI, long-form, small sizes.

The predecessor **LG Smart font is retired**. The guideline states plainly that it is not used;
LG EI Text is its replacement. If you find LG Smart in an existing file, that file is out of date.

## The family-naming trap — read before writing any font-family string

The two families are built differently, and this breaks naive CSS and PowerPoint usage. Values
below were read out of each font's `name` table:

| File | family name (`nameID 1`) | style | usWeightClass |
| --- | --- | --- | --- |
| LGEIHeadline-Thin.otf | `LG EI Headline` | Thin | 100 |
| LGEIHeadline-Light.otf | `LG EI Headline` | Light | 300 |
| LGEIHeadline-Regular.otf | `LG EI Headline` | Regular | 400 |
| LGEIHeadline-Semibold.otf | `LG EI Headline` | Semibold | 600 |
| LGEIHeadline-Bold.otf | `LG EI Headline` | Bold | 700 |
| LGEIText-Light.otf | `LG EI Text Light` | Regular | 300 |
| LGEIText-Regular.otf | `LG EI Text Regular` | Regular | 400 |
| LGEIText-SemiBold.otf | `LG EI Text SemiBold` | Regular | 600 |
| LGEIText-Bold.otf | `LG EI Text Bold` | Regular | 700 |

**Headline** is a proper five-style family — `font-family: "LG EI Headline"` plus `font-weight`
works as expected.

**Text is four separate one-style families.** Each weight declares itself as its own family with
style "Regular". So `font-family:"LG EI Text"; font-weight:700` resolves to nothing — there is no
family by that name, and a browser or PowerPoint will silently substitute a system font. This is
the single most common way an otherwise-correct LG layout ends up in Arial.

**In CSS**, unify them yourself with four `@font-face` rules pointing at one family name:

```css
@font-face{font-family:"LG EI Headline";src:url("../assets/fonts/LGEIHeadline-Regular.otf");font-weight:400;font-style:normal;font-display:block}
@font-face{font-family:"LG EI Headline";src:url("../assets/fonts/LGEIHeadline-Semibold.otf");font-weight:600;font-style:normal;font-display:block}
@font-face{font-family:"LG EI Headline";src:url("../assets/fonts/LGEIHeadline-Bold.otf");font-weight:700;font-style:normal;font-display:block}
@font-face{font-family:"LG EI Headline";src:url("../assets/fonts/LGEIHeadline-Light.otf");font-weight:300;font-style:normal;font-display:block}
@font-face{font-family:"LG EI Headline";src:url("../assets/fonts/LGEIHeadline-Thin.otf");font-weight:100;font-style:normal;font-display:block}

@font-face{font-family:"LG EI Text";src:url("../assets/fonts/LGEIText-Light.otf");font-weight:300;font-style:normal;font-display:block}
@font-face{font-family:"LG EI Text";src:url("../assets/fonts/LGEIText-Regular.otf");font-weight:400;font-style:normal;font-display:block}
@font-face{font-family:"LG EI Text";src:url("../assets/fonts/LGEIText-SemiBold.otf");font-weight:600;font-style:normal;font-display:block}
@font-face{font-family:"LG EI Text";src:url("../assets/fonts/LGEIText-Bold.otf");font-weight:700;font-style:normal;font-display:block}
```

`font-display:block` matters: without it the first paint uses a fallback font, and a screenshot or
PDF export taken at that moment silently ships the wrong typeface.

**In PowerPoint / Word / Illustrator**, there is no unification — write the exact family string
(`LG EI Text SemiBold`, not `LG EI Text` + bold) and leave the bold/italic buttons off. Turning on
faux-bold over an already-bold family produces a smeared synthetic weight that a brand reviewer
will spot.

Install the fonts on the machine before building a PPTX, and embed them in the file
(PowerPoint → Save As → Tools → Save Options → Embed fonts) or the deck will re-substitute on
someone else's laptop.

## Size and weight rules

- **LG EI Headline below 18 pt is not recommended** — legibility falls off. This is the only hard
  size floor in the source.
- For marketing materials there are **no prescribed weight rules** — thickness is a design choice.
- **Exception:** when type sits close to the "Life's Good" slogan, use **Regular**. A heavy weight
  next to the slogan competes with it.
- For special events, campaigns or seasonal work, additional fonts may be combined with LG EI —
  but avoid fonts stylistically similar to LG EI, which read as a bad copy rather than a contrast.

### lge.com convention

Titles use **EI Headline SemiBold**, body uses **EI Text Regular**. The web guide adds that on
LG.com, Regular is the working weight and SemiBold/Bold are *not* recommended for general use.
Full type scale in `web-system.md`.

### Observed usage pattern (source example page, PDF p.66)

LG SIGNATURE and LG Shop contexts use EI Headline Light / Regular; social and LGE.com use
EI Headline SemiBold. Read this as a tone signal — lighter for premium and considered, semibold
for busy digital surfaces — not as a rule.

## Vietnamese and other languages

The guideline's stated position: for languages that do not use the Roman alphabet, local
subsidiaries render the local language in the font most similar to LG EI, and are responsible for
licensing it.

**For Vietnamese this clause does not apply.** Every one of the nine shipped fonts was checked
against the full set of Vietnamese precomposed letters and diacritics — `ăâđêôơư` and all
tone-marked vowels — and **all 74 characters are present in all nine fonts**, with no substitution
needed. LG EI Text carries roughly 14,283 mapped codepoints; LG EI Headline roughly 544 (Latin,
Vietnamese and punctuation — enough for headlines, not for CJK).

So Vietnamese-language LG material uses LG EI directly. Do not substitute a lookalike, and do not
mix a second font in for the diacritics — that produces visibly inconsistent accents.

Practical note for Vietnamese headlines: stacked tone marks make ascenders taller than Latin text,
so tight line-heights that look fine in English can collide. Give Vietnamese headline copy a little
more leading rather than shrinking the type below the 18 pt floor.

## Capitalisation (LG.com convention, useful more broadly)

- **Titles** — first letter capitalised, the rest lowercase. "Product category", not "Product Category".
- **Body** — sentence case; capitalise the first letter only.
- **Prepositions, articles and conjunctions** — always lowercase.
- **Brand and product names** keep their own casing. "LG", never "Lg" or "lg".
- **Quotations** — capitalise only the first letter after the opening quote: "Life's good".
