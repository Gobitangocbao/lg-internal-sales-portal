# Motion — the lg-motion kit

Nineteen animated HTML/CSS components for slides, web pages and screen deliverables: charts that
build, processes that connect, product panels, headlines that arrive. They are picked from the
command line and pasted in, so a deck can be animated without hand-writing keyframes each time.

```bash
python3 scripts/lg_motion.py search "so sánh sell-out giữa các kênh"
python3 scripts/lg_motion.py get bars-compare
python3 scripts/lg_motion.py get kpi-row --no-base     # base CSS already on the page
python3 scripts/lg_motion.py list --family connected
python3 scripts/lg_motion.py doctor                    # is the kit still on-brand
```

**Never open `assets/lg-motion/components.json` or `gallery.html` with a file tool.** They hold
every component's code and a rendered page of all nineteen; reading either spends thousands of
tokens to find one snippet. `search` returns one-line matches, `get` returns exactly one
component ready to paste. If Python is unavailable, `CATALOG.md` is 4 KB and lists everything —
then get the id you chose.

## What is LG's here, and what is ours

This distinction is the whole reason to read this file before using the kit.

**LG's** — the palette, the type, and the three motion families. The guideline names exactly
three animations for EI Form Motion (master PDF p.103–105, summarised in `ei-form.md`):

| Family | LG's phrase | What it means here |
| --- | --- | --- |
| **adaptive** | "Adapt Flexibly" | content arrives in order and settles. The default. |
| **connected** | "Connect with Experiences" | a line, bar or path is drawn, so a relationship is shown rather than stated. |
| **fluid** | "Flow Organically" | continuous, ambient, for a state rather than an event. Used sparingly — two components only. |

Every component declares one of the three, and `doctor` rejects any other value. That keeps the
kit inside LG's motion vocabulary instead of drifting into generic web animation.

**Ours** — the components themselves, their durations, and their easing. The guideline does not
specify timing or easing curves at all (`ei-form.md`, "Not specified in source"), so the values
below are a reading of *warm, unhurried, restrained*, not a rule from LG:

```
--lgm-slow 900ms   --lgm-med 600ms   --lgm-fast 350ms
--lgm-ease cubic-bezier(.22,.61,.36,1)     /* decelerate; no overshoot, no bounce */
--lgm-step 90ms                            /* the gap between staggered items */
```

Say so when you use them. "The build order and 600 ms timing are my choice; LG's guideline names
the motion families but not the timings" is an accurate sentence to put in front of a reviewer.

**Not LG's, and not pretending to be.** `product-frame` is a plain panel, **not an EI form**. EI
forms are fixed artwork this skill does not ship, and an invented shape presented as one fails a
review exactly like a redrawn logo — see rule 2 in `SKILL.md`. The same applies to the
`ambient-dots` background: it is a mild texture, and it is not a gradient. Use it only where an
official gradient is *not* being used.

## The four rules the kit will not let you break

`scripts/lg_motion.py doctor` runs on every build and fails on any of these:

1. **A brand asset is never animated by us.** No component may reference the logo, the logotype
   or the slogan. LG has exactly one official animated mark — Digital Logo Play — and it is
   fixed artwork; animating the static logo to imitate one is prohibited
   (`digital-logo-play.md`). If a page needs an animated LG mark, use a Digital Logo Play GIF.
2. **No gradients.** The four master gradients are fixed artwork that may not be altered, and
   animating one counts as altering it. New CSS gradients may not be created either, so
   `linear-gradient` and `radial-gradient` are both refused inside the kit.
3. **Palette only.** Every colour in every component is checked against the shipped palette
   (Active Red, Heritage Red, the ink and warm-grey scale, black and white) — as a hex *and* as
   an `rgba()` triple, since a faint guide line is naturally written with an alpha and would
   otherwise walk past a hex check. An off-palette colour is a build failure, not a warning.

4. **Sample content stays generic.** Every number and label in a component is a placeholder
   marked `THAY:` — replace all of them. `doctor` fails the build if a component's sample
   content names a real product or feature (WashTower, TurboWash™, AI DD™, ThinQ, OLED…).
   The kit was written straight after a WashTower poster and its placeholders said "14 kg
   giặt" and "39 phút TurboWash™ 360": that made a WashTower demo look better than it was,
   misled anyone building for a TV, and risked somebody shipping a slide carrying a model
   name they never meant to put on it.

Plus two mechanical ones: all CSS is prefixed `.lgm-` so pasting a component into an existing
page cannot collide with it, and the base CSS must carry a `prefers-reduced-motion` guard.

## prefers-reduced-motion

The base CSS collapses every animation to 1 ms for anyone whose system asks for reduced motion,
so they get the finished state immediately rather than nothing. This is not politeness: motion
sensitivity and vestibular disorders are real, and a brand whose whole voice is warmth should
not make someone feel unwell. If you write a new component, it inherits the guard automatically
by living under `.lgm` — do not animate outside that scope.

## The nineteen

| Category | Components |
| --- | --- |
| **charts** | `bars-compare`, `line-trend`, `donut-share`, `counter-hero`, `kpi-row`, `progress-target`, `funnel-steps` |
| **product** | `spec-rows`, `feature-tiles`, `compare-two`, `product-frame` |
| **process** | `steps-flow`, `timeline-track`, `pillars-three` |
| **type** | `headline-rise`, `quote-pull`, `grid-reveal` |
| **state** | `loading-dots`, `ambient-dots` |

`search` accepts Vietnamese with or without diacritics — "kenh", "kênh", "so sanh" all match.

## Using one

`get` prints, in order: a comment naming the component, the base CSS (once per page — pass
`--no-base` for the second and later components), the component's own CSS, and its HTML. Paste
it, then replace the placeholder numbers and labels with the real ones. The markup is deliberately
plain so editing it needs no build step.

### Making a component bigger

Components are authored at 480–560 px, which is right for a web page and small for a 1920 px
slide. To enlarge one, **use `zoom`, not `transform: scale()`**:

```css
.chart{ zoom: 1.6; }          /* the layout box grows too */
.chart{ transform: scale(1.6); }   /* WRONG on a slide - see below */
```

`transform` changes what is painted and leaves the layout box alone. CSS positions with the
layout box, so `right: var(--margin)` puts the *unscaled* edge on the margin and lets the
painted edge run past it — with nothing in the stylesheet to show it. Enlarging four components
this way on one deck put ten items over the LG margin at once, and the page looked deliberate.
`zoom` scales the layout box as well, so margins, neighbours and the grid all still hold.

`verify.py` warns with `SCALED_BOX` whenever an element's own transform scales it, and names
both boxes so the difference is visible.

### Making the motion visible on a deck

**CSS animations fire once, at load, on every slide at the same time.** On a deck that means
the whole motion design plays in the first two seconds, before anyone has left slide 1, and
every slide the viewer actually arrives at is a still picture. The components work; nobody
sees them. This is the single most likely reason an animated deck looks static.

`templates/deck-16x9.html` handles it: press **F** for a real presentation — one slide filling
the screen — and each slide's animations replay as you arrive on it (`R` replays the current
one). In the stacked editing view, a slide replays when it scrolls back into sight. A deck
built by hand needs the same thing:

```js
el.getAnimations({subtree: true}).forEach(a => { a.cancel(); a.play(); });
```

`tests/run.py` checks the template still does this, because it is invisible when it breaks.

The stacked view has a second problem worth knowing about: **a slide is 1920 px wide by
definition**, so on a laptop window the file opens showing a corner of slide 1. The template
scales the stack down to fit (`zoom: var(--fit-page)`, set from the window width, never above
1). `zoom` and not `transform`, so the slides still stack correctly and the scrollbar is the
right length — and `verify.py` resets the fit to 1 before measuring, because a viewing
convenience must never change the geometry being checked.

Two things to keep in mind:

- **Motion does not survive a still export.** A PDF, a screenshot or a printed slide captures
  frame one. If the deliverable will be printed or exported, either the end state must read
  correctly on its own — most of these do, since they animate *into* a finished layout — or use
  a static build instead. A component whose whole point is the movement (`loading-dots`,
  `ambient-dots`) has no business on paper.
- **The kit is layout, not identity.** It never places a logo. Logo, slogan, margin and grid
  still come from `layout-grid.md` and `logo-and-slogan.md`, and `verify.py` still measures the
  finished page. An animated chart on a page with a mis-sized logo is a failed page.

## Adding a component

Edit `scripts/build_motion.py` — it is the source of truth — then rebuild:

```bash
python3 scripts/build_motion.py && python3 scripts/lg_motion.py doctor
```

That regenerates `components.json`, `index.json`, `CATALOG.md` and `gallery.html` together.
Editing the generated files directly puts the catalogue and the code out of step, and the next
person searching will get a description that no longer matches the code.

Render `gallery.html` in a browser and look at it before shipping a change. Two of the original
nineteen were wrong in ways no checker could see — a grid that read as a barcode, a product image
overflowing its panel — and only a human eye on the render caught them.

## Not specified in source

- Motion durations, easing curves, stagger intervals and frame rates. LG names the three
  families and their character; it gives no numbers.
- Whether these three families are intended to govern anything beyond EI forms. The guideline
  scopes them to the EI Form Motion System; applying the same vocabulary to charts and layout
  is a reasonable extension, and it is an extension.
- Any rule about animating data visualisation, charts or UI states. The guideline is silent, so
  everything in the charts and state categories is craft judgement inside LG's palette and type.
