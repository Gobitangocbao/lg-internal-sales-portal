# Sources

Every numeric value in this skill, traced to the file it came from. If a value you need is not
listed here, it was not found in the source — say "not specified in the guideline" rather than
supplying a plausible number.

## Source documents

| # | File | Version / date | Pages |
| --- | --- | --- | --- |
| S1 | `01_guidelines/01_LG_BI_Guidelines_V5_MASTER.pdf` | Brand Communication Guidelines **V5.2, August 2024** | 234 |
| S2 | `01_guidelines/02_BI_Workshop_2025.pdf` | BI Workshop 2025 (incl. LG AI Playbook v01 2024) | 167 |
| S3 | `01_guidelines/03_Digital_Promotion_Guideline.pdf` | Digital Promotion Guideline | 98 — image-only, no extractable text |
| S4 | `01_guidelines/04_GP1_Banner_Detailed.pdf` | GP1 Banner / ST0001 Hero component | 6 |
| S5 | `01_guidelines/05_Web_Style_Guidelines_v1.3.pdf` | LG.com Global One Platform Web Style Guide **v1.3, 2024** | 96 |
| S6 | `01_guidelines/06_Exhibition_Playbook_v1.1.pdf` | Exhibition Playbook **V1, 2024** | 62 |
| S7 | `02_color/LGE_Core Brand Assets_Color_Palette_RGB.ase` | Adobe swatch exchange, 13 swatches | — |
| S8 | `02_color/LGE_Core Brand Assets_Color_Palette_CMYK.ase` | Adobe swatch exchange, 13 swatches | — |
| S9 | `03_fonts/*.otf` | 9 OTF files — `name` and `OS/2` tables read directly | — |
| S10 | `04_logo/`, `05_gradients/`, `06_slogan/`, `07_lg_ai/` | Asset files — pixel and vector geometry measured directly | — |
| S11 | `08_ppt_templates/*.pptx` | 3 PowerPoint templates — OOXML read directly | — |
| S12 | `09. Digital Logo/` | Digital Logo Play: 16 GIFs + 35 .mov masters, ~1.1 GB — measured directly | — |

S1 page numbers below are **PDF page numbers**, which is what a page-render tool needs. Note that
S1 is two documents concatenated: Part 1 (Brand Identity) is PDF p.1–24 with matching printed page
numbers; Part 2 (Visual Identity) starts at PDF p.25 and restarts its printed numbering at 1, so
PDF p.40 carries the printed number 16.

## Section map for S1 (PDF pages)

| Section | PDF pages |
| --- | --- |
| 01 Brand Identity | 8–13 |
| 02 Logo | 15–23 |
| 03 Design Philosophy | 28–33 |
| 04 Digital Logo Play | 34–37 |
| 05 Color | 38–47 |
| 06 Gradients | 48–58 |
| 07 Typography | 59–67 |
| 08 Slogan (incl. Grid) | 68–81 |
| 09 Design System | 82–109 |
| 10 Illustration | 110–122 |
| 11 Voice | 123–132 |
| 12 Photography | 133–152 |
| 13 Video | 153–189 |
| 14 Other (OOH, stationery, e-mail) | 190–203 |
| 15–16 Digital / Social Guidelines | 204–end |

## Value ledger

### Colour

| Value | Source |
| --- | --- |
| All 11 core + supporting swatches: HEX, RGB, CMYK, Pantone | **S1 p.40** (swatch page, read visually) |
| Same RGB values, independently confirmed | **S7** (ASE binary parse) |
| Same CMYK values, independently confirmed | **S8** (ASE binary parse) |
| Active Red print build C0 M97 Y95 K0; sRGB basis; paper test list | **S1 p.41** |
| Colour "Things to Avoid" (6 items) | **S1 p.47** |
| Web Active Red `#EA1917` and full web palette | **S5 p.10, p.11, p.14, p.66** |
| WCAG 2.2 AA, 4.5:1 minimum, cleared pairings | **S5 p.9, p.10** |
| Active Red PMS 2034 C in an exhibition context | **S6 p.44** |

### Typography

| Value | Source |
| --- | --- |
| Family names, style names, usWeightClass, unitsPerEm 1000 | **S9** (OTF `name` + `OS/2` tables) |
| Vietnamese coverage — 74/74 characters present in all 9 fonts; ~14,283 codepoints in Text, ~544 in Headline | **S9** (OTF `cmap` table) |
| Headline for key messages, Text for body; LG Smart retired | **S1 p.61, p.62, p.63** |
| 18 pt minimum for Headline; no weight regulation for marketing | **S1 p.64** |
| Regular recommended near the slogan | **S1 p.65** |
| lge.com: Headline SemiBold titles, Text Regular body | **S1 p.66** |
| Local-language substitution clause | **S1 p.67** |
| Full LG.com type scale (sizes + line-heights) | **S5 p.17, p.18, p.19** |
| Regular preferred on LG.com; SemiBold/Bold not recommended | **S5 p.16** |
| Capitalisation rules | **S5 p.16** |

### Logo

| Value | Source |
| --- | --- |
| Clear space 0.15X of symbol size (horizontal); 15% of logo size (vertical); minimum 4 mm / 16 px | **S1 p.19, p.20**; repeated **S2 p.19, p.20** |
| Clear-space diagram proportions (15% / 17.5% / 65% / 17.5% / 15%) | **S1 p.19** (page render) |
| Measured: symbol 758 × 758 px, canvas 5452 × 1130, padding 188/187/186/186 = 0.248 × symbol; symbol/canvas height = 0.671 | **S10** (alpha-channel measurement) |
| All logo file canvas dimensions and aspect ratios | **S10** |
| Logotype colour LG Gray C0 M0 Y0 K70 / Black / White | **S1 p.18** |
| Symbol-alone exceptions (business card, badge, web/mobile/PC icon) | **S1 p.17** |
| Colour variations by background | **S1 p.21** |
| 2D only; 3D retired; logo+slogan lockup retired | **S1 p.15** |
| Company-name notation rules | **S1 p.22** |
| Logo Don'ts (14 items) | **S1 p.23** |
| Logo **symbol height** = 1.3X of margin; five placements | **S1 p.77** (text + 220 dpi page render, measured: X column 76 px, 1X band 78 px, 1.3X band 101 px, symbol 100 px; placement artboard 774 × 324 px, 16 px inset, symbol 19–20 px) |
| Logo file height = 1.3X / 0.668 = 1.95X (compact), / 0.671 = 1.94X (wide) | derived from **S1 p.77** + **S10** padding measurement |
| Video logo sizing: 16:9 25-row / 3X / 12%; 1:1 and 9:16 20-unit / 6X / 30% | **S1 p.177, p.178, p.179** |
| Top-left video logo: X = height/20 or 5%; margins 1.5X wide, 1X tall | **S1 p.188** |
| OOH logo ≥ 2.5X of whitespace height; white logo outdoors | **S1 p.196, p.197, p.198** |

### Slogan

| Value | Source |
| --- | --- |
| Clear space = size of the period in the slogan; four versions | **S1 p.72** |
| Colourways: Active Red, White, Black, on Warm Gray or gradient | **S1 p.71** |
| Lead message vs sign-off; never both; never without the logo | **S1 p.72, p.73** |
| Sign-off **visible** height 0.9X; file height = 0.9X / 0.669 = 1.35X; placement rules; stacked not for sign-off | **S1 p.78** (220 dpi render measured: X column 77 px, 1X band 78 px, 0.90X band 70.5 px) |
| Lead message aligns to full grid width; centred → vertically centred or bottom | **S1 p.79** |
| Sense-of-space image placement | **S1 p.80** |
| Slogan Don'ts (8 items) | **S1 p.81** |
| Video slogan sizing: 16:9 "L" 2–4X / 10–20%; 1:1 8–14X / 40–70%; 9:16 14X / 70% | **S1 p.181, p.182, p.183** |
| End-frame timings: 1 s logo; >30 s → 0.5 s slogan + 1 s logo; ≤6 s logo optional; no jingle, no CTA | **S1 p.176** |
| End-frame order A/B/C | **S1 p.185** |
| Slogan file canvas dimensions, 144 px padding | **S10** |

### Grid and layout

| Value | Source |
| --- | --- |
| Margin 5% of shortest edge; 9 columns; 9 rows; multiples of 3; gutter = half the margin | **S1 p.76** (text + page render) |
| Grid intent — "tight margins, restricting font sizes" | **S1 p.75** |
| Web grid: XL 24 col / 240 px margin / 24 px gutter; L 24 / 24 / 24; S 8 / 16 / 10; cap 2560 px; column 37 px, 2-col mobile 75 px | **S5 p.5, p.7** |
| Web layout spacing 48 / 64 / 48 / 20 / 12 px | **S5 p.50** |
| Web button sizes and text sizes | **S5 p.24, p.27** |
| Icon sizes and 1.5 / 1.2 px strokes | **S5 p.88, p.90, p.91** |
| Blur level 25 px for EI Form backgrounds | **S2 p.62** |
| Image spec: JPG/PNG, ≤ 5120 KB, content in centre 80% | **S2 p.108** |

### Gradients

| Value | Source |
| --- | --- |
| Four masters, Warm → Innovative; cannot be modified or created | **S1 p.49, p.50** |
| Five crop formats and their intended media; ≥ 2 colours visible | **S1 p.51–54** |
| Compose → crop → finish layout | **S1 p.55** |
| Usage contexts (hero moments, packaging, web/social); Gradient 04 for innovation | **S1 p.56** |
| Gradient Don'ts (10 items) | **S1 p.58** |
| Master files 2000 × 2000 px | **S10** |

### Hero banner / web components

| Value | Source |
| --- | --- |
| 1920 × 720 / 1600 × 720 / 1440 × 720; mobile 720 × 960 upload, 360 × 480 display | **S4** |
| Text width 862 / 642 px; headline 56 px default, 80 px option, mobile 36 px; body 16 px | **S4** |
| Character limits: eyebrow 50, headline 60, body 200; max 2 CTAs; carousel 3 recommended / 8 max | **S4** |
| CTA primary Active Red, secondary outlined black | **S4** |

### Print and collateral

| Value | Source |
| --- | --- |
| Business card 90 × 50 mm, paper, UV ink, type sizes 10.2 / 6.8 pt | **S1 p.199** |
| Business card back — 8 graphic options, epoxy | **S1 p.200** |
| Digital business card 596 × 1073 px @ 300 dpi | **S1 p.201** |
| Letter A4 / US Letter; envelope L/M/S sizes; address 8–9 pt; LG Gray K 70% | **S1 p.202** |
| E-mail signature: logo 14 px, slogan 17 px, type 10 / 8 / 6 pt, Pantone values | **S1 p.203** |
| Pre-screening and pre-testing process; GMG consultation for joint branding | **S1 p.176, p.189** |

### Exhibition

| Value | Source |
| --- | --- |
| Logo signage seen first, at the top of every space | **S6 p.18** |
| Warm / Bold / Simple; avoid too many colours | **S6 p.35** |
| Inform wall: highlight title H 160 mm on a 3,000 mm wall | **S6 p.41** |
| Island displays sit lower than wall graphics | **S6 p.42** |
| Spec board: PMS 2034 C; product name H 6 mm / EI Headline 27 pt; model H 3.5 mm / EI Text 14 pt | **S6 p.44** |
| Eye level 1,550 mm | **S6 p.46** |
| Lounge minimums: entrance 1,000 mm, passage 700 mm, hallway 1,000 mm; warm white wall | **S6 p.54** |

### Design System — EI Form and EI Lens

| Value | Source |
| --- | --- |
| Must be used with the content; not applicable broadly; not mandatory | **S1 p.83, p.87, p.93** |
| Core vs connected state; core shapes never combined | **S1 p.86** |
| Cropping must keep the image recognisable | **S1 p.86, p.100** |
| Choose the form to suit the product's shape | **S1 p.87** |
| Background: solid complementary colour, or the same image enlarged and blurred; with two or more forms use the emphasised form's image; a different image is not allowed | **S1 p.97** |
| Blur scale 5 / 15 / **25** / 60 / 80 px with the verdict for each | **S1 p.96** |
| Build sequence compose → set background → blur (+ nudge a couple of px) → finish layout | **S1 p.95** |
| Three layouts: Basic, Core EI Form, Connected EI Form | **S1 p.94** |
| Six as-is/to-be corrections incl. no gradients inside forms, same shooting angle, one form per image | **S1 p.99–101** |
| EI Lens role, character (Intelligent / Respectful), and its two uses | **S1 p.89, p.90, p.91** |
| Containment rule and its exception | **S1 p.98** |
| Three motions (Adaptive / Connected / Fluid), their layouts and character | **S1 p.103, p.104, p.105** |
| After Effects production notes: forms only, Stroke Width + Offset Paths, Adjustment Layer | **S1 p.106** |
| Eight AE template files, per-motion guidance | **S1 p.107, p.108** |

### Photography

| Value | Source |
| --- | --- |
| Six common principles | **S1 p.133** |
| Lifestyle principles | **S1 p.136** |
| Lifestyle: 4 avoids + 6 don'ts | **S1 p.137** |
| Three product categories | **S1 p.139** |
| Product Isolated principles (long focal length, red thread, warm backgrounds, people + product) | **S1 p.141, p.142** |
| Product Isolated: 6 don'ts | **S1 p.143** |
| Product Abstract principles | **S1 p.145, p.146** |
| Product Abstract: 5 don'ts | **S1 p.147** |
| Product Close-ups principles (natural light, shallow depth of field, close crops, real environment) | **S1 p.149, p.150** |
| Product Close-ups: 5 don'ts | **S1 p.151** |

### Voice

| Value | Source |
| --- | --- |
| Principle 1 "with a smile", try-to / try-not-to, 11-year-old test | **S1 p.123** |
| Message examples (XBOOM360, Objet Posé, InstaView Range) | **S1 p.124** |
| Principle 2 "with insight", SEO + life benefits formula, ESG must | **S1 p.125** |
| Message examples (UltraGear, gram, 6 Motion DD) | **S1 p.126** |
| Principle 3 "with design": headline 5–8 words, sentence case, no trailing full stop | **S1 p.127** |
| Before/after correction, generic + title case critique | **S1 p.128** |
| Full application examples | **S1 p.129, p.130** |

### Illustration and Digital Logo Play

| Value | Source |
| --- | --- |
| Illustration role; LG Fashionista and LG Gamer characters | **S1 p.110, p.111** |
| Finger Heart / Hand Heart as symbolic brand elements | **S1 p.112** |
| Illustration usage and 2 don'ts | **S1 p.113, p.114** |
| Digital Logo Play: eight forms, do not change or create new | **S1 p.34** |
| Only available in motion, digital environments only | **S1 p.33** |
| Usage examples on mobile app and website | **S1 p.35, p.36** |
| Don'ts incl. never on static media, no shadows or effects | **S1 p.37** |
| Motion end frame order and five colours, 3 aspect ratios | **S1 p.186, p.187** |
| The eight motion names, durations, frame counts, pixel sizes and file sizes | **S12** (measured from the files) |
| 2K master set complete (32 files); **6K set incomplete** — 3 of 8 motions, Mono/Black only | **S12** (folder scan) |

### Motion (the lg-motion kit)

| Value | Source |
| --- | --- |
| The three motion families — Adaptive "Adapt Flexibly", Connected "Connect with Experiences", Fluid "Flow Organically" — and their character | **S1 p.103–105** |
| Per-motion layout guidance, and that the system is composed solely of EI forms | **S1 p.105, p.106** |
| EI Form Motion is digital and video only | **S1 p.103** |
| Durations, easing curves, stagger intervals, frame rates | **not specified in source** — the kit's 350/600/900 ms and `cubic-bezier(.22,.61,.36,1)` are this skill's reading of "warm, unhurried, restrained", flagged as such in `motion.md` |
| The nineteen components themselves | **this skill** — layout devices built from the LG palette and LG EI type. Not LG artwork, and `product-frame` is explicitly not an EI form |

### LG AI

| Value | Source |
| --- | --- |
| Affectionate Intelligence vision, two pillars | **S2 p.152** |
| LG AI / Affectionate Intelligence / AI symbol / FURON definitions; Vietnamese name | **S2 p.153** |
| Per-division AI application status (HE / IT / H&A / ThinQ) | **S2 p.154** |
| With-LG vs without-LG application rule | **S2 p.156** |
| Four communication levels (Hero / Event / Listing / Hero product features) | **S2 p.157** |
| Symbol application contexts; five motions | **S2 p.155, p.158** |
| Symbol gradient `#FD312E` → `#FD2F3F`; wordmark spectrum stops | **S10** (SVG source) |
| All LG AI SVG viewBox dimensions and aspect ratios | **S10** |

## Known gaps — "not specified in source"

Listed so they are visible rather than quietly filled in:

- Whether the 5% margin applies to the shortest edge on all four sides, or only left/right.
- LG AI clear space, minimum size, type scale, named palette roles, and motion timings.
- Motion timing of any kind: EI Form Motion durations, easing, stagger and frame rate.
  The guideline names the three families and their character and gives no numbers, so
  every value in the lg-motion kit is this skill's judgement inside LG's vocabulary.
- Any rule for animating charts, data visualisation or UI states. The three families are
  scoped to EI forms; extending the same vocabulary to layout is a reasonable extension
  and is labelled as one in `motion.md`.
- Text-safe-area and secondary-element-area dimensions on the digital business card.
- Slide-internal type scale for presentations (the web scale in `web-system.md` is for web).
- Chart, table and data-visualisation styling of any kind.
- No all-white mono version of the compact symbol+"LG" lockup exists in the asset pack (measured
  against the full file listing, S10).
- The *Brand Usage Guidelines* and the co-branding review checklist referenced by S1 p.225–228
  are separate documents, not in the asset pack, so the "mandatory conditions" for a joint
  marketing lockup cannot be verified from what is available here.
- EI form shapes, the eight EI Form Motion After Effects templates, illustration characters and
  gestures, and the eight Digital Logo Play files are all referenced by the guideline as
  downloads and are **not in this skill's assets/**. See `illustration.md` for the policy on
  what to do instead. Digital Logo Play is no longer on this list — its official assets arrived
  and are covered by `digital-logo-play.md`.
- Section 13 Video (S1 p.153–175) is covered only for end frames, logo/slogan sizing and the
  top-left logo. Tone & manner, production, and the colour treatment / LUT pages are not sourced.
- Sections 15–18 (Digital, Social, ESG, Package Design) are link pages in S1; the actual
  guidelines are separate documents not in the asset pack.
- **S3, the Digital Promotion Guideline, is a 98-page image-only PDF** with no extractable text.
  Nothing in this skill is drawn from it. If a digital-promotion question comes up that the other
  sources don't answer, that document needs to be read page by page as images.

## Corrections made to this skill

Recorded so the reasoning is auditable rather than silently overwritten.

- **Logo and slogan sizing, corrected.** An earlier version of this skill read "The Logo is 1.3X
  the size of our margins" (S1 p.77) as the lockup's *width*, and applied 1.3X and 0.9X to the
  PNG *files*. Both were wrong. Measuring the diagrams at 220 dpi shows the labelled bands
  measure height and hug the visible mark: the 1.3X band is 101 px against a 76 px margin column
  and contains a 100 px symbol; on p.78 the 0.90X band is 70.5 px against a 77 px column. Because
  the files carry clear-space padding, the placed file must be divided by the mark's share of the
  canvas. Under the wrong reading a logo came out roughly a third the intended size — which looks
  deliberate rather than broken, so it survived a full brand-check pass and was only caught when a
  reviewer said it "seems small". `brand_check.py` now flags this case by name.
- **The checker was rebuilt, not patched.** The original `brand_check.py` matched regexes
  against CSS source, but the grid is written in `calc()` and custom properties, so it could
  never evaluate the geometry it claimed to check. Its size rule was dead code. A suite of
  deliberately broken pages showed 7 of 8 passing clean, including the undersized logo above.
  `scripts/verify.py` replaced it: it renders the page and measures the DOM, finds brand assets
  by the file they load rather than by class name, and samples the pixels under the logo.
  `brand_check.py` was cut back to the static rules only, so no rule has two implementations.
  `tests/` now holds 53 fixtures — every mechanically checkable rule has one, and a rule without
  a fixture is treated as unenforced.
- **Coverage was 22% of the master guideline and is now 58%.** The additions are the sections
  that channel and marketing work actually needs: Design System (EI Form / EI Lens),
  Photography, Voice, Illustration and Digital Logo Play, and Brand Management / co-branding.
- **Motion was added as a kit, with the brand rules enforced by the build.** `scripts/lg_motion.py`
  ships nineteen animated components in LG's own three motion families, and
  `lg_motion.py doctor` fails the build on an off-palette colour, a CSS gradient, an unprefixed
  class, or any reference to the logo, the logotype, the slogan or a master gradient — because
  LG has exactly one official animated mark and animating the static logo to imitate it is
  prohibited. `verify.py` enforces the same rule on the finished page (`BRAND_ASSET_ANIMATED`,
  `DLP_ANIMATED`), and `tests/run_motion.py` puts all nineteen through the real verifier on a
  real page rather than trusting a frozen fixture. Two components were wrong in ways no checker
  could see — a grid that rendered as a barcode, a product image overflowing its panel — and
  were caught only by rendering the gallery and looking at it.
- **Two install-time failures are now tested, not remembered.** The package was twice refused
  by the installer for reasons invisible while working on it: a `+` in six logo filenames
  ("Zip file contains path with invalid characters"), and a `description` that grew past the
  1024-character cap one clause at a time. `tests/run_portability.py` checks both.
- **The checker was caught lying a third time, and the failure mode was closed at the source.**
  A roleplay run — a marketeer asking for a 5-slide WashTower deck — put `verify.py` on a page
  with five `.lg-canvas`. Playwright's strict locator threw, the exception was caught upstream,
  printed as a line of prose, and the report still ended with *"0 error(s), 0 warning(s) —
  geometry, fonts and assets check out"*. The deck had ten margin breaches and two slides with
  no logo at all. Three things changed: a run that cannot measure the page now prints
  **VERIFY_INCOMPLETE** and says in words that it is not a pass (exit 2); several canvases on
  one page are **deck mode**, each measured separately and labelled `slide n/N`; and an `<img>`
  that did not load is an **error** — `LOGO_ABSENT` for a brand mark, `ASSET_NOT_LOADED`
  otherwise — because the missing all-white compact lockup had been reported as a warning that
  the logo "is only 35px wide". The one case that cannot be a fixture file, a page that cannot
  be opened at all, is checked directly in `tests/run.py`. A fourth followed from auditing
  the fix: an `<img>` reports `naturalWidth`, but a logo set as a CSS `background-image`
  reports nothing when its path is wrong, so failed network requests are now watched too.
- **The checker learned to compare elements with each other.** Every geometry rule until now
  measured one element against the canvas, so a headline covered by a panel of feature tiles
  produced zero errors and had to be caught by eye. `OVERLAP` now flags text that something
  painting after it lands on — using document order and z-index to tell "covered" from the
  normal case of text sitting on its own background, so a headline over a full-bleed gradient
  stays clean (there is a fixture for exactly that false positive). `TEXT_CONTRAST` samples the
  ring of pixels around each text box, not only under the logo: Warm Gray 04 on Warm Gray 07 is
  1.5:1, both on-palette, which is why an eyeball checking the palette passes it. Thresholds
  are WCAG's because the guideline gives none, and the report says so. `SCALED_BOX` warns when
  an element's own `transform: scale()` makes the painted box outgrow the layout box CSS
  positions with — `zoom` scales both and is not flagged; `references/motion.md` now says which
  to use. Running these on the deck that had passed produced 32 errors on the draft and, on the
  supposedly finished version, three real contrast failures its author had noticed and not
  fixed.
- **The deck got a template, and dark slides got measured colours.** "A slide, a deck, a
  PPTX" was one routing row with a single-slide template behind it, so every agent invented
  its own deck scaffold — and its own dark-slide palette, which is how Warm Gray 04 on Warm
  Gray 07 (1.5:1) shipped while looking perfectly on-brand. `templates/deck-16x9.html` now
  carries the grid, the pager, keyboard navigation and present mode; `.lg-dark` in
  `lg-tokens.css` re-roles the palette from measured ratios (see the table in `color.md`), and
  `lg_motion.py doctor` fails the kit if the dark block is missing or uses Warm Gray 03 as
  muted text. `scripts/for_print.py` turns the Digital Logo Play export warning into a command.
  Two false positives surfaced while testing this and were fixed: `LOGO_BUSY_GROUND` measured
  variance over a crop that *contained* the logo, so a white logotype on a dark slide — the
  pairing the guideline recommends — always read as "busy"; and `TEXT_CONTRAST` sampled around
  a button instead of using the button's own fill, scoring white-on-red at 1.2:1. `tests/run.py`
  now also verifies every file in `templates/` and the output of `for_print.py`, because a
  defect in a file people copy is inherited by everything built from it.
- **The skill got a front door, and the kit lost its bias.** Everything in it addressed an
  agent; a marketeer got error codes in a terminal and had nothing to send to Brand
  Management. `SKILL.md` now opens with three sentences a real person would say, and
  `scripts/report.py` writes one self-contained HTML review — every slide as it rendered, each
  finding boxed on the slide it belongs to, a plain next step per finding, and a written
  statement that a clean run is not a passed brand review (16 of 38 prohibitions are
  mechanical; the other 22 are named on the page). `tests/run.py` checks that every code the
  suite can produce has a next step, so adding a rule without adding its line fails. Separately,
  the motion kit's placeholders had been written straight after a WashTower poster — "14 kg
  giặt", "39 phút TurboWash™ 360" — which flattered a WashTower demo, misled anyone building
  for another category, and risked shipping a model name nobody meant to include; they are now
  generic `THAY:` markers and `doctor` fails on any real product or feature name. Page chrome
  marked `data-noexport` is hidden before measuring, so a navigation hint no longer lands in a
  review screenshot.
- **An animated deck that nobody could see animate.** The WashTower deck carried five
  lg-motion components and looked completely static. The cause was not the kit: CSS animations
  fire once, at load, on every slide simultaneously, so the entire motion design played in the
  first two seconds while the viewer was still on slide 1. `templates/deck-16x9.html` now has
  a real presentation mode — F for one slide filling the screen, arrow keys, R to replay — and
  replays each slide's animations on arrival (and on scroll-back in the stacked view). It also
  ships a component on every slide instead of empty placeholders, which is what a deck template
  is for. `tests/run.py` drives the template in a browser and fails if arriving on a slide
  leaves nothing running. Separately, two kit components put Warm Gray 03 captions on a Warm
  Gray 06 panel — 4.3:1, under the floor — now Warm Gray 02 at 7.6:1, correct on dark too.
- **The deck opened wider than the screen.** A slide is 1920 px by definition, so opening the
  file on a laptop showed a corner of slide 1 — presentation mode fitted the screen, the
  default view did not, and the default view is what everyone sees first. The stacked view now
  scales to the window with `zoom: var(--fit-page)` (never above 1, so a full-width window is
  untouched), and `verify.py` resets that variable before measuring so a viewing convenience
  cannot shrink the geometry under test. `tests/run.py` opens the template at 1280x800 and
  1440x900 and fails if the page overflows.
- **A deck that changed brand identity halfway through, and the hint that caused it.** The
  WashTower deck used the compact symbol + "LG" lockup on its light slides and the corporate
  symbol + "LG Electronics" lockup on its dark ones. Every per-slide rule passed — right size,
  permitted position, good contrast — because no rule had ever asked whether the mark on the
  page was the *right mark for the piece*. A reviewer caught it by eye.
  The root cause is worth recording precisely: `logo-and-slogan.md` already said the compact
  lockup is the default and that S1 p.21 approves `LGE_Logo_HeritageRed_White_RGB.png` (Heritage
  Red symbol + white logotype) on black grounds. But when the earlier fix for a missing white
  file was written, its hint said "use the wide LGE_2D_LG-Electronics_Logo_Mono_White_RGB.png on
  dark grounds" — answering *which file exists* instead of *which mark belongs here* — and that
  wrong sentence propagated into `verify.py`, `for_print.py`, the deck template and the deck.
  Three checks now exist: **LOGO_VARIANT_MIXED** (error, judged across the whole piece rather
  than per canvas, since that is the only level at which the defect is visible),
  **LOGO_CORPORATE_LOCKUP** and **LOGO_WORDMARK_ALONE** (warnings). The hint is corrected in all
  four places, and the lockup rule is now non-negotiable #4 in `SKILL.md`.
- A previously recorded conflict — "1.3X puts the wide lockup's symbol under the 4 mm minimum" —
  **was an artefact of that misreading and has been withdrawn.** With the symbol at 1.3X, the 4 mm
  floor only binds below roughly a 62 mm short edge.
- **The WashTower product photo showed its studio white background as a visible rectangle** on
  the deck's warm-grey panel — not unified with it, and (per `photography.md`, Product Isolated
  Don't 6) shipped with no ground shadow at all. A first pass keyed out "any pixel near pure
  white," which is what Don't 6 warns against in a different form: the appliance's own cream
  front panel is nearly as light as the background, and the whole thing came back as one
  connected blob — the crop ate into the product. Fixed with a border-seeded flood fill in
  floating/gradient-tolerant mode (each pixel compared to its already-filled neighbour, not to
  absolute white), which follows the background's lighting gradient and stops at the product's
  real edge regardless of how light that edge is; confirmed by the background reducing to exactly
  one connected component both times, but only the second pass left the cream panel at full
  opacity. A soft, blurred contact shadow was then added under the feet (the source crop ran to
  its canvas edge with no room for one, so the canvas was padded first) to satisfy Don't 6 rather
  than leave a shadowless cut-out. Technique recorded in `photography.md`, "Using a supplied
  product image."

## Known conflicts between sources

| Topic | Conflict | Rule adopted |
| --- | --- | --- |
| Active Red | S1/S7/S8 say `#FD312E`; S5 says `#EA1917` in four places | `#EA1917` for LG.com and its design system, `#FD312E` everywhere else |
| Logo clear space | S1 states 0.15X of symbol; the shipped PNGs (S10) carry 0.248X | Use the asset's own canvas — it satisfies the stated minimum with room to spare |
| Logo size on slides | S1 p.77 gives 1.3 × margin (0.49 in on a 13.33 × 7.5 in slide); the S11 templates place a 0.71 in logo | Follow S1; the templates are not authoritative |
| PPTX theme | S11 templates carry the default Office theme — Calibri, `#4472C4` — with brand appearance pasted on as images | Build a real LG theme; `templates/build_pptx.py` does this |
