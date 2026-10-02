# LG.com web system

Source: `05_Web_Style_Guidelines_v1.3.pdf` (LG.com Global One Platform Web Style Guide v1.3, 2024)
and `04_GP1_Banner_Detailed.pdf`.

This system governs lge.com and components built to it. **Where it differs from the BI guideline,
it wins for web output** — most importantly on Active Red. For print, slides, social or events, go
back to the BI defaults.

## Palette

### Primary

| Token | HEX | RGB |
| --- | --- | --- |
| Active Red | `#EA1917` | 234, 25, 23 |
| Warm Gray | `#F0ECE4` | 240, 236, 228 |
| Black | `#000000` | 0, 0, 0 |
| White | `#FFFFFF` | 255, 255, 255 |

Note the red: `#EA1917` here, `#FD312E` in the BI guideline. See the discrepancy section in
`color.md`.

### Secondary

| Token | HEX | RGB |
| --- | --- | --- |
| Light Gray 1 | `#F6F3EB` | 246, 243, 235 |
| Light Gray 2 | `#F0ECE4` | 240, 236, 228 |
| Light Gray 3 | `#E6E1D6` | 230, 225, 214 |
| Mid Gray 1 | `#CBC8C2` | 203, 200, 194 |
| Mid Gray 2 | `#646464` | 100, 100, 100 |
| Mid Gray 3 | `#4A4946` | 74, 73, 70 |
| Dark Gray 1 | `#333333` | 51, 51, 51 |
| Dark Gray 2 | `#262626` | 38, 38, 38 |
| Dark Gray 3 | `#1A1A1A` | 26, 26, 26 |

### Etc / state

| Token | HEX | RGB | Use |
| --- | --- | --- | --- |
| Heritage Red | `#A50034` | 165, 0, 52 | promo flag and error state on warm/light grey backgrounds |
| Yellow Review | `#F7B500` | 247, 181, 0 | review stars |
| Yellow Toast | `#DEAD25` | 222, 173, 37 | warning toast |
| Green (Validation) | `#287D00` | 40, 125, 0 | valid input on white |
| Tree Green (Validation) | `#316D15` | 49, 109, 21 | valid input on warm/light grey |
| Blue Green (Toast) | `#076369` | 7, 99, 105 | information toast |

State-colour logic worth knowing: on a **white** background, success is `#287D00` and error is
Active Red `#EA1917`; on a **warm/light grey** background, success is `#316D15` and error is
Heritage Red `#A50034`. Product flags are Black; promotional flags are Active Red on white and
Heritage Red on warm grey. Error toasts use Dark Gray 2 `#262626`.

Accessibility: WCAG 2.2 AA, minimum 4.5:1 contrast. Text must not be baked into images — the guide
calls embedded text a web-accessibility violation.

## Grid

Device-specific, fixed pixels — not the BI 5% rule.

| Breakpoint | Columns | Margin | Gutter | Notes |
| --- | --- | --- | --- | --- |
| XL — 1920+ | 24 | 240 px | 24 px | full-bleed area 1920 px, content area 1440 px |
| L — 1440+ | 24 | 24 px | 24 px | |
| S — 360+ | 8 | 16 px | 10 px | full area 360 px, content area 328 px |

The grid caps at **2560 px**. At 1920, column width is 37 px and the 240 px margin splits 160 + 80.
On mobile a 2-column span is 75 px.

## Type scale

All LG.com type is LG EI. Regular is the working weight; SemiBold and Bold are not recommended for
general use.

| Style | Desktop | Mobile |
| --- | --- | --- |
| Title Large | EI Headline Semibold 80 / 80 | EI Headline Semibold 36 / 36 |
| Title Medium | EI Headline Semibold 56 / 60 | EI Headline Semibold 28 / 32 |
| Title Small | EI Headline Semibold 48 / 56 | EI Headline Semibold 24 / 28 |
| Sub Title Large | EI Text Regular 36 / 42 | EI Text Regular 24 / 28 |
| Sub Title Medium | EI Text Regular 32 / 36 | EI Text Regular 20 / 24 |
| Menu Large (GNB & Tab) | EI Text Regular 24 / 28 | — |
| Menu Default | EI Text Regular 20 / 24 | EI Text Regular 16 / 18 |
| Menu Small | EI Text Regular 16 / 18 | EI Text Regular 12 / 14 |
| Tag Large | EI Text Regular 20 / 24 | — |
| Tag Default | EI Text Regular 16 / 18 | EI Text Regular 14 / 16 |
| Tag Small | — | EI Text Regular 12 / 14 |
| CTA Large | EI Text Semibold 24 / 24 | EI Text Semibold 16 / 16 |
| Price Large | EI Text Semibold 32 / 32 | EI Text Semibold 28 / 28 |
| Price Medium | EI Text Regular 20 / 20 | EI Text Regular 20 / 20 |
| Price Small (default) | EI Text Regular 16 / 16 | EI Text Regular 12 / 12 |
| Price Small (original) | EI Text Regular 16 / 20, strikethrough | EI Text Regular 12 / 12, strikethrough |

(Sizes are px; the second number is line-height.) A few Body styles exist beyond these; the guide's
Font Guide pages 17–19 are the full table if a specific one is needed.

## Buttons

Box buttons come in three sizes and three types. Active Red is reserved for important actions —
purchase, subscription.

| Size | Height | Min box width | Text size / line-height |
| --- | --- | --- | --- |
| Small | 36 px | 80 px | 14 / 14 |
| Medium (default) | 44 px | 100 px | 16 / 16 |
| Large | 64 px | 120 px | 24 / 24 |

Types: `Outlined_Black`, `Red`, `Outlined_icon`. States: Default, Hover, Disabled.
Icon buttons: Small 36 × 36, Medium 44 × 44, Large 64 × 64.

## Layout spacing

| Situation | Desktop | Mobile |
| --- | --- | --- |
| With a title — top margin | 48 px | 24 px |
| With a title — bottom margin | 64 px | 24 px |
| No title — top and bottom | 48 px | 24 px |
| Between title and content | 20 px | 12 px |

Default alignment is justified both sides with the title on the left; left alignment when there is
only a title. Titles are always left-aligned. Centre alignment is an exception, used in the PDP
features section.

## Hero banner (ST0001) — the spec for a web banner

| Property | Value |
| --- | --- |
| Desktop / tablet image | Wide 1920 × 720, Narrow 1600 × 720, Content 1440 × 720 |
| Mobile upload | 720 × 960 (displays at 360 × 480) |
| Text width | Wide 862 px, Narrow 642 px |
| Text colour | White `#fff` or Black `#000` — set separately for desktop and mobile |
| File formats | JPG, PNG, GIF, MP4 |
| Headline | Desktop 56 px default (80 px option); mobile 36 px. Max 60 characters |
| Eyebrow | max 50 characters |
| Body copy | 16 px desktop and mobile. Max 200 characters |
| CTA | max 2. Primary = Active Red button; Secondary = outline black button |
| Alignment | horizontal left / centre / right, vertical top / middle / bottom — recommended: vertical top or bottom, horizontal left or right |
| Carousel | max 3 contents recommended, up to 8 possible |

Narrow (1600 px) is explicitly **not recommended**. Alt text is required on every content item.

Image asset requirements (BI Workshop 2025, p.108): JPG or PNG, maximum file size **5120 KB**,
and content kept within the **centre 80%** of the image, which is the safe area that will not be
cropped at other breakpoints.

## Icons

- Sizes: 48 px (desktop, anything above 36 px), 24 px, 12 px, and 64 px for category icons.
- Stroke weight: **1.5 px** default; **1.2 px** for smaller or emphasised symbols.
- Rounded style, reflecting the brand value of warmth. Two types — common icons and product icons —
  each in white or black.
- Build as SVG, keeping the icon's grid and padding area intact.
