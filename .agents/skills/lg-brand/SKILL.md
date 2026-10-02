---
name: lg-brand
description: LG Electronics brand identity (BI Guidelines V5.2, Aug 2024): the real logo, slogan, gradient and LG EI font files, source-cited colour, typography, grid, photography, voice and co-branding rules, a browser verifier that measures the finished page, and animated components in LG's own motion families. Use whenever producing or checking ANY LG-branded output — slides, PPTX decks, posters, leaflets, POP and spec boards, web and social banners, key visuals, OOH, business cards, co-marketing artwork, or the copy on them — and whenever the user mentions LG, LGE, LG Electronics, Life's Good, LG AI, ThinQ, "brand guideline", "nhận diện LG", "đúng brand", or asks whether a design is on-brand. Use it too for LG motion work: an animated chart or slide, a building headline, a loading state, "motion", "hoạt hình". And before answering any question about LG brand colours, the LG EI typeface, logo clear space or minimum size, so the answer comes from the measured guideline rather than memory.
---

# LG Electronics Brand Identity

This skill turns LG's official brand assets into work that passes an LG brand-team review.
Every number in it was read out of the source files listed in `references/sources.md`, most of
them measured off the guideline's own diagrams. Nothing is invented. Where a source is silent,
the reference file says **"Not specified in source"** — that is a gap to ask about, never a
licence to guess a plausible value.

## Bắt đầu ở đây — nếu bạn không rành kỹ thuật

Nói bằng tiếng Việt, như nói với đồng nghiệp. Ba câu này là đủ để bắt đầu:

- *"Làm cho tôi bộ 5 slide 16:9 về WashTower WT1410NHEG, có dashboard thông số."*
- *"Cái poster này đã đúng brand LG chưa?"* (kèm file)
- *"Màu đỏ LG là mã gì? Logo phải to bao nhiêu trên slide?"*

Không cần nhớ tên file hay câu lệnh nào. Agent sẽ tự làm bốn việc, và **nên nói cho bạn biết
nó đã làm**:

1. **Lấy số từ nguồn, không đoán.** Thông số sản phẩm lấy từ lg.com/vn hoặc từ tài liệu bạn
   đưa. Số nào chưa xác nhận được thì ghi thẳng **"chưa xác định"** lên bản thiết kế — để bạn
   biết mà đi hỏi, thay vì phát hiện lúc đã in.
2. **Dựng từ template có sẵn** trong `templates/`, đã đúng lưới, đúng cỡ logo, đúng phông.
3. **Đo lại bản đã render** bằng `scripts/verify.py` — không phải đọc code, mà mở trình duyệt
   và đo thật.
4. **Xuất một bản báo cáo bạn gửi được cho Brand Management:**

```bash
python3 scripts/report.py bai-cua-ban.html --canvas 1920x1080
```

Ra một file HTML duy nhất: ảnh từng slide, lỗi khoanh đỏ ngay trên ảnh, mỗi lỗi kèm một câu
*phải làm gì tiếp*, và một mục nói rõ phần nào máy kiểm được và phần nào vẫn cần mắt người.

**Một điều nên nhớ:** báo cáo sạch **không phải** là đã được duyệt brand. 16 trong 38 điều cấm
của guideline kiểm được bằng máy; 22 điều còn lại — ảnh có ấm không, bố cục có xứng không,
câu chữ có đúng giọng LG không — vẫn cần người nhìn. Báo cáo nói điều đó ở mọi lần chạy.

## Before you share anything from this skill

The source documents are stamped **"Internal Use only"** on nearly every page, and the
Exhibition Playbook is marked **"Confidential and Proprietary"**. The bundled LG EI fonts are
licensed to LG Electronics. So: use this inside LGE, and do not pass the skill package, the
fonts, or extracts from the guidelines to anyone outside the company. The sample images in the
guidelines carry their own instruction — *do not change, edit, recreate, or use images
externally* — which is why no photography ships here.

## Two tiers of asset, and why it matters when this skill is shared

**Tier 1 — shipped inside the skill.** Fonts, the RGB logo set, the slogan, the four gradients,
the LG AI vectors, and the Digital Logo Play GIFs. These work on any laptop the skill is
installed on, and they cover slides, posters, banners, social and web work end to end.

**Tier 2 — LG's asset pack, optional and local.** The `.mov` motion masters (~1.1 GB), the CMYK
logo set for print separation, the full-resolution gradients, the source PDFs, the original
PPTX files. Too large or too situational to bundle.

Tier 2 lives in a different place on every machine, so **nothing in this skill records an
absolute path to it**. Manifests store paths relative to the pack root and
`scripts/resolve_assets.py` finds the root here and now — from `LG_BRAND_ASSETS`, from
`assets/local-pack.json`, or by looking in the usual places.

```bash
python3 scripts/resolve_assets.py     # what is available on this machine
```

When the pack is absent — which it will be for most people you share this with — that is a
normal state, not an error. Use the shipped assets, and if a task genuinely needs a Tier 2 file,
name the file and say it is not on this machine. Do not guess a path, and do not quietly
substitute a different asset for it.

## Non-negotiables

Six rules cause most brand-review rejections. Everything else is craft.

1. **Use the shipped asset files, never a redraw.** The LG symbol, logotype, "Life's Good"
   slogan and the four gradients are fixed artwork in `assets/`. They are never re-typed,
   re-traced, re-coloured, re-proportioned, or approximated with an emoji, a circle plus
   letters, a CSS gradient, or a font — **and never animated**, since LG has exactly one
   official animated mark and it is Digital Logo Play. The one exception is the LG AI symbol,
   which ships as SVG and may be inlined as-is.
2. **When the asset you need is not here, say so — do not approximate it.** EI form shapes,
   the EI Form Motion templates, and illustration characters and gestures are fixed artwork
   this skill does not ship. An invented EI form fails a review exactly like a redrawn logo,
   and is harder to spot. Ask for the file, or design without it — none of them is mandatory.
   Check `assets/` first, though: Digital Logo Play was on this list until its files arrived,
   and the list is a snapshot rather than a permanent state.
3. **Type is LG EI only.** `assets/fonts/` holds all nine weights. Embed or install them — do
   not fall back to Arial, Helvetica, Inter or Roboto and call it close enough. The families
   are named unusually; read `references/typography.md` before writing any font-family string.
4. **One lockup per piece, and the compact one by default.** Symbol + "LG" is the mark for
   product, channel and campaign work. Symbol + "LG Electronics" is the corporate signature,
   for pieces that require the full company name — and mixing the two across a deck reads as
   two brands. On dark or image grounds the compact variant is
   `LGE_Logo_HeritageRed_White_RGB.png`; the missing all-white compact file is never a reason
   to switch to the corporate mark.
5. **Never place the Logo and the Slogan next to each other.** They are separate assets in
   separate roles in the same layout — logo top-left, slogan bottom-left, for example. This one
   surprises people and appears four times in the source.
6. **Every measurement derives from the margin.** Margin = 5% of the canvas's *shortest* edge;
   symbol height, slogan height and spacing are all multiples of it. Compute it first, before
   placing anything. Note that 1.3X and 0.9X measure the **visible mark**, not the PNG — the
   files carry clear-space padding, and `templates/lg-tokens.css` does the division for you.

## Which identity system

LG runs two systems. Mixing them wrongly is a rejection.

**LG Electronics core BI** — the default. Corporate, product, channel, retail, event and
internal communication. Red symbol + "LG" or "LG Electronics" logotype, LG EI type, warm-grey
palette, the four gradients, "Life's Good".

**LG AI** — only when the subject is genuinely LG's AI offering. Two modes: the AI logo *with*
the LG logo when talking about LG AI broadly at brand or hero level; the AI logo *without* it
when locked to a product, platform or feature name to flag AI technology inside it.

A deck about a washing machine that happens to have an AI mode is core BI with an AI feature
badge — not an LG AI-system deck. When unsure, use core BI; it is the safer default, and adding
an AI symbol later is cheap. Details in `references/lg-ai.md` — note that its clear space,
minimum size and type scale are not specified in the source, so that file is thinner than the
core system by necessity, not by omission.

## Routing — what to read for the task in front of you

Read the two in **Always**, then only the row that matches. Nothing here needs the whole set.

| The user asks for | Read | Verify with |
| --- | --- | --- |
| *Always, whatever the task* | `color.md`, `typography.md` | — |
| One slide, or a PPTX | `layout-grid.md`, `logo-and-slogan.md` | `verify.py` on HTML, `brand_check.py` on the .pptx |
| **A deck** — several slides in one HTML file | `layout-grid.md`, `logo-and-slogan.md`; start from `templates/deck-16x9.html` | `verify.py` on the whole file — it measures every slide and labels findings `slide n/N` |
| **A dashboard**, a numbers slide, a report of figures | `layout-grid.md`, then `motion.md` for the chart components | `verify.py --canvas WxH` |
| A poster, key visual, campaign image | `layout-grid.md`, `logo-and-slogan.md`, `photography.md`, `ei-form.md` | `verify.py --canvas WxHmm` |
| A social post or banner outside lge.com | `layout-grid.md`, `logo-and-slogan.md`, `photography.md` | `verify.py --canvas WxH` |
| Anything on lge.com or built to its design system | `web-system.md` **instead of** `layout-grid.md` | `verify.py --canvas WxH --web` |
| OOH, exhibition, booth, POP, spec board | `layout-grid.md`, `print-and-collateral.md` | by hand — these are physical |
| Business card, letterhead, envelope, email signature | `print-and-collateral.md` | by hand — sizes are specified there directly |
| Anything with a partner or dealer logo, co-marketing | `co-branding.md` **first** — it may not be allowed at all | by hand, then Brand Management sign-off |
| The words: headline, eyebrow, body, campaign line | `voice.md` | by eye against its worked examples |
| Video, end frame, social video | `layout-grid.md` (per-format grids), `logo-and-slogan.md` | by hand |
| An animated logo, a loading state, an app or web motion moment | `digital-logo-play.md` — the eight official motions ship here as GIFs | `verify.py` (it errors if one lands on a print canvas) |
| An animated chart, a building slide, a motion moment that is **not** the logo | `motion.md`, then `python3 scripts/lg_motion.py search "<the job>"` | `lg_motion.py doctor`, then `verify.py` on the finished page |
| Illustration, characters, Finger Heart | `illustration.md` | — |
| "Is this on-brand?" / fix an existing design | `donts.md`, plus the row above matching what it is | `verify.py` if it is HTML |
| A question about a specific value | `sources.md` — it maps every number to its file and page | — |

Two habits worth keeping whatever the row: name the values you used and where they came from,
and say which parts you verified mechanically and which you judged by eye.

## Workflow

**1. Decide which system you are in — they do not mix.**

| | LG Electronics BI | LG.com web |
| --- | --- | --- |
| Applies to | slides, print, POSM, social, OOH, events, internal | lge.com pages and components built to its design system |
| Grid | margin = 5% of the shortest edge, 9 × 9 | 24 / 8 columns, fixed margins 240 / 24 / 16 px |
| Active Red | `#FD312E` | `#EA1917` |
| Type | free within LG EI, Headline ≥ 18 pt | the fixed lge.com scale |
| Verify with | `verify.py --canvas WxH` | `verify.py --canvas WxH --web` |

A piece that is genuinely both — a web banner that will also be printed — is a question for
the user, not something to average. Everything below is the BI system; `web-system.md` is
self-contained for the other one.

**2. Establish the canvas and the margin.** Ask for, or infer, exact output dimensions. Then:

```
margin        = 0.05 × min(width, height)
gutter        = margin / 2
logo symbol height       = 1.30 × margin     # the SYMBOL's height, measured off the diagram
slogan height (sign-off) = 0.90 × margin     # the visible artwork height

# the shipped PNGs include clear-space padding, so size the file up to compensate:
logo file height   = 1.30 × margin / 0.668   ( = 1.95 × margin )
slogan file height = 0.90 × margin / 0.669   ( = 1.35 × margin )
```

Columns and rows: 9 × 9 (or a multiple of 3). Full derivation and the exceptions for video,
social and OOH formats are in `references/layout-grid.md`.

**3. Open the references the routing table sent you to.** Only those.

**4. Build it.**

**Motion on a deck needs a replay.** CSS animations fire once, at load, for every slide at
once — so an animated deck plays its whole build before anyone leaves slide 1, and every slide
after that is a still picture on arrival. The deck template replays a slide's animations as you
enter it; a hand-built deck must do the same. `references/motion.md` has the three lines.

**Dark slides**: put `.lg-dark` on the `.lg-canvas`. It re-roles the same LG palette to
measured pairings — do not write your own dark colours. On `#262626`, Warm Gray 03 is 3.0:1
and Heritage Red is 1.9:1, so neither is used there; the tokens pick 04, 05 and 07 instead.

Start from `templates/` rather than an empty file — the templates already have the grid maths,
the `@font-face` block with the right family names, and the logo placed correctly, which is where
hand-built attempts usually go wrong.

- `templates/slide-16x9.html`, `templates/poster-a2.html`, `templates/banner-web.html` — self-contained
  HTML with a print/export path. Best control, and `brand_check.py` can inspect them.
- `templates/build_pptx.py` — writes a PPTX with a proper LG theme (colours and fonts in the theme
  part) and grid-correct logo placement, for decks the team will edit in PowerPoint.

The bundled PPTX files that ship with LG's asset pack carry the *default Office theme* — Calibri
and Office blue — with brand appearance pasted on top as images. Do not treat them as a source of
truth for colour or type; `build_pptx.py` exists because of this.

A note on why the padding correction matters: 1.3X and 0.9X describe the *visible* mark, but
the asset files carry transparent clear space around it. Setting the file to 1.3X makes the
logo about a third smaller than the guideline asks — small enough to look deliberate and pass
an inexpert eye, which is exactly why it is worth getting right. `lg-tokens.css` does the
division for you.

**5. Verify before reporting done.**

```bash
python3 scripts/verify.py <page.html> --canvas 1080x1350 [--web] [--shot out.png]
python3 scripts/brand_check.py <deck.pptx>          # .pptx has no rendering to measure
```

**A multi-slide deck is one file with several `.lg-canvas`, and that is handled.** Every canvas
is measured on its own and every finding is labelled `slide n/N`, so a deck fails on the slide
that is wrong rather than passing because slide 1 happened to be right.

**Read the exit code, not only the last line.** `0` clean, `1` at least one error, and `2`
**the page could not be measured at all** — a missing file, a render that threw. Exit 2 prints
`VERIFY_INCOMPLETE` and says in words that it is not a pass. Never report work as verified on a
run that ended in 2: nothing was measured, so nothing is known.

`verify.py` renders the page in a browser and measures what actually came out. That matters
more than it sounds: the grid is written in CSS variables and `calc()`, so reading the
stylesheet cannot tell you how big the logo ended up. An earlier source-reading checker
reported success on a logo placed at a third of its required size, and passed seven of eight
deliberately broken test pages. Measuring the rendered DOM closes that.

It finds elements by the **asset they load**, not by class name, so a layout you hand-built is
checked exactly as strictly as one started from `templates/`. An `<img>` whose file did not load
is an **error**, not a cosmetic warning — a broken path renders as an empty box that keeps its
layout, so the page looks structurally fine with a hole in it. When the broken image is a brand
mark, that is `LOGO_ABSENT`.

What it enforces: symbol height 1.3X and slogan 0.9X against the *measured* margin; the five
permitted logo positions; minimum size; transforms on the logo; the logo–slogan separation;
the slogan used once, never without the logo, never stacked as a sign-off; the symbol never
alone; nothing crossing the margin; two gradients in one piece; gradients inside text; text
that renders in a substituted font; off-palette colour; and — by sampling the pixels under the
logo — a red symbol on a red ground and a low-contrast lockup. Across the whole piece it also
checks that only **one** lockup is used, since a deck alternating the compact and corporate
marks passes every per-slide rule while changing brand identity between slides. It compares elements against
**each other**, so text covered by a panel or by other text is `OVERLAP`; it samples the pixels
under **text** as well as under the logo, so an on-palette but unreadable pairing such as Warm
Gray 04 on Warm Gray 07 (1.5:1) is `TEXT_CONTRAST`; and it warns with `SCALED_BOX` when an
element's own `transform: scale()` makes the painted box outgrow the layout box CSS positions
with — the trap that puts an enlarged component over the margin. On animated pages it also
catches motion applied to fixed artwork — the logo, the slogan, a master gradient or a Digital
Logo Play file — whether the keyframes sit on the asset, on a wrapper around it, or come from
`element.animate()` in script.

**A clean run is not a passed brand review.** 16 of the 38 numbered prohibitions can be
checked mechanically. The other 22 are judgement: whether a crop killed the gradient, whether
the photography feels warm rather than clinical, whether the composition earns its space. Look
at the render, and say plainly which parts you verified and which you judged.

`tests/run.py` and `tests/run_static.py` are the regression suite behind all of this — 53
fixtures, each a deliberately
broken layout with the error it must produce. If you add a rule, add a fixture; a rule with no
fixture is a rule nobody is enforcing, which is how the size regression survived.

## When something isn't in the guideline

The source genuinely does not cover everything — slide-internal type scales for a channel deck,
chart colours, table styling, icon choices for a business presentation. In those cases: stay
inside the palette, keep LG EI, respect the grid, and tell the user plainly which choice was
yours rather than LG's. An honest "the guideline is silent on chart colours; I used Warm Gray
02–05 with Active Red for the highlight series" is far more useful to someone facing a brand
review than a confident invention.

## References

- `color.md` — the full palette with HEX, RGB, CMYK and Pantone per swatch, gradients, and the Active Red discrepancy between print and web
- `typography.md` — the LG EI families, the family-naming trap that silently substitutes fonts, size rules, full Vietnamese coverage
- `logo-and-slogan.md` — variants, clear space, minimum size, the five positions, and the measured asset geometry behind the 1.3X and 0.9X rules
- `layout-grid.md` — grid construction, worked margins per canvas, and the per-format grids for video, social and OOH
- `photography.md` — the six principles, the three product categories, and every named don't
- `ei-form.md` — EI Form and EI Lens: states, containment, the 25 px blur scale, background treatment, motion
- `voice.md` — the three writing principles, headline rules, and LG's own published examples
- `co-branding.md` — partner and dealer lockups, the 0.5X / 0.65X spacing, and when co-branding is not permitted at all
- `web-system.md` — the lge.com palette, type scale, grid, buttons and spacing (self-contained; replaces the BI grid)
- `lg-ai.md` — the LG AI identity, when it applies, and what the source does not specify
- `print-and-collateral.md` — print colour behaviour, exhibition and POP, stationery, business card, email signature
- `digital-logo-play.md` — the eight motions, which to reach for, what ships as GIF vs what stays as a 1.1 GB master, and why a still frame is prohibited
- `motion.md` — the lg-motion kit: LG's three motion families, what in it is LG's and what is ours, and the three rules the kit enforces on itself
- `illustration.md` — characters, gestures, and the policy for assets this skill does not ship
- `donts.md` — the consolidated prohibition list, for designing and for reviewing
- `sources.md` — **every number in this skill, with its file and page**, the corrections made along the way, and the honest list of what is still uncovered

## Tools

- `scripts/verify.py` — renders and measures an HTML deliverable. The main check.
- `scripts/brand_check.py` — static checks only; the right entry point for a .pptx.
- `scripts/lg_motion.py` — 19 animated components in LG's own motion language. `search` by describing the job, `get` one to paste, `doctor` to check the kit is still on-brand. Never read `components.json` or `gallery.html` with a file tool — that is what `search` is for.
- `scripts/build_motion.py` — the source of truth behind the kit; edit components here and rebuild.
- `scripts/resolve_assets.py` — reports what is available on this machine and locates the optional asset pack without hardcoding a path.
- `templates/lg-tokens.css` — the palette, the font faces, and the grid maths as CSS variables.
- `templates/deck-16x9.html` — a multi-slide 16:9 deck: grid layout inside the margins, light and dark slides, an lg-motion component already placed on every slide, pager, and a real presentation mode (**F** = one slide filling the screen, animations replaying as you arrive on each). Start here for anything with more than one slide.
- `templates/slide-16x9.html`, `poster-a2.html`, `banner-web.html` — starting points that are already correct.
- `scripts/report.py` — runs the check and writes a self-contained HTML review: every slide as it rendered, findings boxed on the render, a next step per finding, and a written statement of what is machine-checked and what is not. This is the output to give a person.
- `scripts/for_print.py` — makes the export-safe copy of a page that uses Digital Logo Play: removes the animated mark where the slide already has a logo, swaps it for the correctly sized static lockup where it does not.
- `templates/build_pptx.py` — builds a deck with a real LG theme, which the bundled LG .pptx files do not have.
- `tests/run_portability.py` — proves the package carries no machine-specific paths, no broken asset references, and nothing the installer will refuse (filename characters, the 1024-character description cap), so it survives being shared.
- `tests/run.py`, `tests/run_static.py` — 53 fixtures covering every mechanically checkable rule. Add a fixture whenever you add a rule.
- `tests/run_motion.py` — the lg-motion lane: the kit is on-brand, the catalogue matches the code, search still finds things, and all 19 components pass the real verifier on a real page.
