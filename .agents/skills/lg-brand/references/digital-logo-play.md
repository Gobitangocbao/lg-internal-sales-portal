# Digital Logo Play

Source: `01_LG_BI_Guidelines_V5_MASTER.pdf` section 04, PDF p.33–37 (doc p.9–13), plus the
official asset folder `LG assets/09. Digital Logo`, measured directly.

The LG symbol animated: a line-drawn version of the smiling face that moves "with a warm and
witty attitude and adapts to consumers' moods and needs". Eight fixed animations, exactly as
the guideline describes them.

## The one rule that catches people

**Digital Logo Play is only available in motion and must only be used in digital environments.**
The guideline's own reason for the prohibition is worth understanding rather than memorising:
a still frame of one *"would be confused as an extension of our CI"* — because the animated mark
is a line-art variant of the symbol, a frozen frame reads as a second, unofficial logo.

Concretely, that means:

- Never on **static media** — a poster, a print ad, a spec board, a PDF leaflet, a still slide.
- Never as a **still export**, a poster frame, a thumbnail, or the first frame lifted out.
- Never with **shadows or effects**.
- Never **changed, edited, or newly created** — the eight movements are fixed artwork, like the
  logo itself. Do not retime, reverse, loop-trim, recolour, or animate the static logo yourself
  to imitate one.

It also does **not replace the master logo**. In the motion end frame the order is
*Life's Good Slogan → Digital Logo Play → LG Master Logo* (p.186), so it precedes the master
logo rather than standing in for it.

`scripts/verify.py` enforces the static-media rule: a Digital Logo Play asset on a millimetre
(print) canvas is an error, and on a digital canvas it warns if no master logo appears with it.

## The eight motions

All eight run **6.0–6.08 seconds**. Frame counts differ because the GIFs were encoded at
different rates, not because the animations differ in length.

| Motion | Feel | Reach for it when |
| --- | --- | --- |
| **Appearing** | the mark draws itself in from nothing | an opener, a first load, a reveal |
| **Nodding** | agrees, acknowledges | a confirmation, a success state |
| **Wink** | a beat of humour | a light moment, a playful CTA |
| **Amazed** | reacts with surprise | a product reveal, a "look at this" moment |
| **BobtoMusic** | bobs in rhythm | audio and entertainment contexts |
| **Bowing** | greets, thanks | a welcome, a thank-you, a close |
| **LookingAround** | scans, curious | search, discovery, browsing |
| **Spinning** | rotates continuously | a loading or processing state |

`assets/digital-logo-play/CONTACT-SHEET.png` shows first / middle / last frame of each one, so
you can pick a motion without opening eight files.

The guideline's own steer: motions should be *appropriate to the content and to how users
interact with it*. Spinning belongs on a loading state, not under a headline.

## What ships here, and what does not

**Shipped — the 16 transparent GIFs, byte-identical to the originals**, in
`assets/digital-logo-play/black/` and `white/`. One filename change: LG ships them with spaces
in the name, which some packaging tools reject, so here the spaces are underscores. The image
bytes are untouched, so a hash check against the original folder still matches. These are the practical web format: transparent,
small, and playable anywhere without a video pipeline.

| | Black | White |
| --- | --- | --- |
| Size on canvas | 1000 × 1000 px | 2000 × 2000 px |
| File size | 34–256 KB | 79–610 KB |
| Use on | light backgrounds — warm grey, white | dark backgrounds, imagery, video |

The two colours are supplied at different pixel sizes. That is how LG shipped them, not an
error here — but it means you cannot assume both are interchangeable at the same scale. Set the
display size in CSS and let the browser scale.

**Not shipped — the `.mov` masters, about 1.1 GB.** They stay in LG's asset pack, because a
skill package that size would be unusable. `assets/digital-logo-play/MANIFEST.json` lists all 35
of them by motion, variant and size, with a **pack-relative path** — relative to the root of the
asset pack, never an absolute path, because the pack sits somewhere different on every machine
and this skill gets shared.

To turn a pack-relative path into a real one on whatever machine you are on:

```bash
python3 scripts/resolve_assets.py                       # what is available here
python3 scripts/resolve_assets.py --find "09. Digital Logo/.../Nodding.mov"
```

If the pack is not on this machine, that is the normal case and not a failure: the GIFs above
cover web, social and UI work completely. Say which specific master file would be needed and
why, rather than substituting a different asset or assuming a path.

| Master set | What exists |
| --- | --- |
| **2K .mov** | complete — all 8 motions × Mono (Black, White) and Transparent (Black, White) = 32 files, 17–30 MB each |
| **6K ProRes 4444** | **incomplete** — only BobtoMusic, Nodding and Spinning, and only in Mono/Black (3 files, ~130 MB each) |

The 6K gap is worth knowing before promising a large-format or broadcast deliverable: five of
the eight motions have no 6K master in this folder at all. If one is needed, it has to come from
LG's asset portal.

If what you actually need is motion that is *not* the logo — a chart that builds, a headline
that arrives, a process that connects — that is `references/motion.md` and
`scripts/lg_motion.py`, which animate the layout around the mark and never the mark itself.

## Choosing a variant

- **Transparent** — the mark over your own background, footage or UI. This is what the GIFs are,
  and the usual choice.
- **Mono** — the mark on a solid black or white field, baked in. Useful when the delivery
  channel cannot carry an alpha channel.
- **Black** on light grounds, **White** on dark. The same contrast logic as the static logo, and
  `verify.py` samples the pixels underneath to check it.

## Placing one in a web page

Nothing in the guideline gives a size rule for Digital Logo Play, so **the 1.3X symbol rule does
not transfer to it** — it is a different asset in a different role. Size it to its context and
say that the choice was yours.

```html
<!-- transparent GIF, sized in CSS; the file is square so height = width -->
<img src="assets/digital-logo-play/black/LGE_Electronics_Digital_Logo_Play_Transparent_Black_Nodding.gif"
     width="96" height="96" alt="LG">
```

**If the page will be printed or exported, run `for_print.py` rather than remembering to swap
the mark by hand:**

```bash
python3 scripts/for_print.py deck.html          # writes deck-print.html
python3 scripts/for_print.py deck.html --check  # says what it would do
```

It decides per canvas. A slide that already carries the static logo has the animated mark
*removed* — putting a second master logo where the animated one sat would land it outside the
five permitted positions. A canvas where Digital Logo Play is the only LG mark gets the static
lockup instead, sized to the 1.3X rule rather than to the animated mark's box. Keep the original
for screen use; the print copy is only for the exported version.

Two practical notes. A GIF loops forever by default and there is no way to stop it from the
markup — if a single play is wanted, the `.mov` master in a `<video>` element is the honest
route. And a GIF's first frame is what a screenshot or a PDF export captures, which is exactly
the still-frame case the guideline prohibits: if a page will be exported to PDF or printed, use
the static logo there instead.

## Not specified in source

- Size, clear space and minimum size for Digital Logo Play.
- Which motion suits which context — the mapping in the table above is a reading of what each
  animation does, not a rule from the guideline. Say so when you use it.
- Frame rate, and whether the GIFs are intended to loop or play once.
- Whether the five missing 6K motions exist elsewhere.
