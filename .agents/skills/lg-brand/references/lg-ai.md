# LG AI identity

Source: `02_BI_Workshop_2025.pdf` section VI "AI Guidelines" (p.150–159, marked *LG AI Playbook
Version 01 – 2024*) and the vector assets in `assets/lg-ai/`.

This is a younger system than the core BI, and the source is correspondingly thinner — several
pages are marked WIP or TBD. Where a number is absent below, it is absent from the guideline; say
so rather than filling the gap.

## The idea

**Affectionate Intelligence** is LG's vision for AI: warm and full of life, with intelligent
innovation behind it. The two halves matter equally — an LG AI piece that reads as cold
technology has missed the point, and so has one that reads as warm but empty.

The system's own framing:

- **LG AI** — the name. LG Affectionate Intelligence, the AI value LG Electronics delivers.
- **Affectionate Intelligence** — the vision; how LG AI should feel across the product ecosystem.
- **AI symbol** — how LG AI looks while it is engaging with the customer. Static and motion forms.
- **FURON** — the name of the intelligence software behind LG AI. A reason-to-believe / modifier,
  expressed separately, only for products with FURON technology embedded.

Vietnamese naming used in the source: **Trí tuệ Nhân tạo Thấu cảm LG**.

## When to use it — the decision that matters

The AI logo has two application modes, and picking the wrong one is the main failure here.

**With the LG logo** — when talking about LG AI broadly, at a hero or brand level, connecting LG
Electronics' products and services to Affectionate Intelligence. lge.com brand pages, events,
campaigns about LG's AI vision.

**Without the LG logo** — when combined with a product, platform or feature name to flag the AI
technology inside it. Product level, platform level, feature / core-tech / USP level.

Four communication levels are named in the playbook:

| Level | Treatment |
| --- | --- |
| Hero | LG AI is the hero message |
| Event | LG AI leads, describing AI technologies |
| Listing product features | AI box in-line before the product feature |
| Hero product features | AI box featured in iconography |

Existing per-division practice recorded in the source: HE uses AI combined with the product name;
IT places the symbol next to the feature category; H&A uses its own AI symbol on core-tech pages
(AIDD / AI DUAL Inverter); ThinQ combines AI with the core-tech or feature name.

**Default when in doubt: use core BI, not the AI system.** A product that has an AI feature is
still a core-BI piece with an AI badge on the feature. The AI system is for when LG AI itself is
the subject.

## Colour

Read directly out of the SVG source files, so these are exact.

**AI symbol** — a two-stop linear gradient:

| Stop | HEX |
| --- | --- |
| 0 | `#FD312E` (LG Active Red) |
| 1 | `#FD2F3F` |

The symbol's gradient starts on LG Active Red, which is what ties the AI system back to the core
brand.

**Affectionate Intelligence wordmark, FURON wordmark and the Powered-by-FURON lockups** use a wider
red → magenta → violet spectrum:

`#FD312E` · `#FD2E43` · `#FD297A` · `#FF21D3` · `#FE21D1` · `#F914EB` · `#E51DEE` · `#B446FF` · `#8227FF`

Two further stops appear in the combined Symbol + Affectionate Intelligence artwork: `#B945FF` and
`#FF1EFF`.

These are the artwork's own gradient stops. **Do not rebuild the gradient from them** — use the
supplied SVG. They are listed so you can pick a matching accent for adjacent UI or a background,
and so a brand check can recognise them as legitimate.

**Not specified in source:** a named LG AI palette with roles (primary / secondary / background),
LG AI type scale, LG AI clear-space and minimum-size values, and the motion specifications for the
five symbol motions. The playbook shows the motions exist but does not give timings.

## Assets

All in `assets/lg-ai/` as SVG — vector, so they scale cleanly and are the best-quality assets in
this whole pack. PNG equivalents are in the original asset pack at `07_lg_ai/png/`.

Each of the following comes in `Colour`, `Mono_Black` and `Mono_White`:

| Asset | SVG viewBox | Aspect |
| --- | --- | --- |
| `LG_AI_Logo` | 1391.72 × 772.54 | 1.80 : 1 |
| `LG_AI_Symbol` | 1920 × 1920 | 1 : 1 |
| `LG_AI_Affectionate_Intelligence_Wordmark` | 2013.91 × 346.07 | 5.82 : 1 |
| `LG_AI_Symbol_Affectionate_Intelligence` | 2122.96 × 798.33 | 2.66 : 1 |
| `LG_AI_Symbol_Affectionate_Intelligence_Horizontal` | 2222.27 × 346.07 | 6.42 : 1 |
| `LG_AI_Furon_Wordmark` | 846.69 × 300.53 | 2.82 : 1 |
| `LG_AI_Powered_by_Furon` | 1734.22 × 1017.46 | 1.70 : 1 |
| `LG_AI_Powered_by_Furon_Horizontal` | 1444.51 × 300.53 | 4.81 : 1 |

Choose Mono_White on dark or busy backgrounds, Mono_Black on light ones, Colour where the
background is calm enough for the gradient to read — the same contrast logic as the core logo.

**The one redraw exception in this skill:** because these are SVG, inlining the SVG markup into an
HTML page is fine and preferred — it keeps the artwork vector and lets it inherit `currentColor`
for the mono versions. Inlining the file's own markup is not a redraw. Hand-authoring a new path,
or approximating the symbol with CSS shapes, is.

## Symbol application contexts

From the playbook, the symbol appears:

- **On product (gradient)** — the animated gradient plays an active role in product lighting.
- **Product UI** — on all products, for notifications and interactions with the AI agent.
- **Hero moments (3D)** — the animated 3D symbol for expressive hero moments.
- **TVC / video / digital** — motion creates recognition across key messaging.

Five motions exist and are used separately; the source shows them combined only as a sample.
Timings and easing are **not specified in source**.

## Combining with core BI

When LG AI material also carries the LG logo, the core BI rules still apply in full — grid, margin,
logo size and placement, the logo/slogan separation rule, LG EI typography. The AI system adds
assets; it does not replace the layout system.
