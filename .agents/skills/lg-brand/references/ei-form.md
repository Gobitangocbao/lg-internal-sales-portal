# EI Design System — EI Form and EI Lens

Source: `01_LG_BI_Guidelines_V5_MASTER.pdf` section 09, PDF p.83–108 (doc p.59–84).

This is LG's signature creative device, and the part of the system that makes a layout look
like LG rather than like a competent grid with a red logo on it. If a key visual, campaign
image or product hero feels correct but generic, this is usually what is missing.

**Read the constraint first:** the EI design system must always be used *with the content*,
and cannot be broadly applied to all marketing outputs. It is also **not mandatory** — the
guideline says so three separate times. A clean cropped product image with no EI form is an
approved outcome. Reach for EI forms when they earn their place, not as decoration.

## EI Forms

Shapes inspired by LG's own products — rounded, soft-edged containers that imagery is cropped
into.

**Two states, and they behave differently:**

| | Core state | Connected state |
| --- | --- | --- |
| Look | simple shapes, rounded edges, warm softness | multiple shapes joined |
| Combining | **used alone, never combined with one another** | may be used alone or in combination |
| Best for | print, static, a single clear subject | digital, where shapes connect and respond through motion |

Getting this backwards — combining core-state shapes — is the most likely mistake, because
combining looks richer and nothing on the page stops you.

**Choosing a form:** select the EI form that suits the *shape of the product*. A tall product
like a refrigerator takes a tall form. The form follows the subject; the subject is not
squeezed to fit the form.

### Containment

Products or images should generally be **entirely contained** within the form. A part may
extend outside it when the product's characteristics justify it and the overall design still
holds together — but that is an exception you should be able to explain, not a default.

When cropping with EI forms, **the image inside must stay recognisable.** Avoid excessive
cropping — p.100 makes this a worked example: if the crop no longer reads as the thing it
shows, the form has beaten the content.

### Background treatment (p.97)

This is the rule that produces the signature look, and it is precise:

- Use a **solid colour that complements the image**, or
- Use **the same image that sits inside the EI form**, enlarged and blurred, to heighten the
  sense of space.
- With **two or more forms**, the background comes from **the highest-priority form's image** —
  the one being emphasised.
- **Using a different image as the blurred background is not allowed.** Stated as a "thing not
  to do", not a preference.

### Level of blur (p.96)

The guideline gives a calibrated scale, which is unusually concrete:

| Blur | Verdict |
| --- | --- |
| 5 px | not blurred enough — looks like a mistake, adds no depth, distracting next to other assets |
| 15 px | still short |
| **25 px** | **correct** — adds depth, keeps a clear visual link with the image, not overwhelming |
| 60 px | past it |
| 80 px | too blurred — reads as a vector gradient, colours muddy |

25 px works for most high-resolution imagery, but every image differs and the level needs
adjusting to keep the look consistent. Treat 25 px as the starting point, then judge by eye.

### Build sequence (p.95)

1. **Compose** — pick the EI forms layout, pick the images (product + person), compose, crop
   the imagery into the forms.
2. **Set background** — scale up the image of the person.
3. **Blur** — apply Gaussian blur and crop into the layout. Apply the *same* blurred image to
   the smaller shape, then nudge it a couple of pixels left or right so it does not blend
   invisibly into the background.
4. **Finish the layout** — add the other brand assets following the grid and sizing system.

That nudge in step 3 is the kind of detail that separates a real execution from an imitation.

### Three layouts (p.94)

| Layout | Use it for |
| --- | --- |
| **Basic** | delivering content with confidence — tidy, structured, global. Product launches, campaign visuals, event graphics. |
| **Core EI Form** | the most basic and functional layout. Highlighting specific product details and features, or when the design should be straightforward and concise. |
| **Connected EI Form** | flexible and active use of forms. Boldly displaying various images, and indicating connections or groupings. |

### Worked corrections (p.99–101)

The guideline shows six as-is / to-be pairs. The rules they encode:

- **No gradients inside EI forms**, or any use that deviates from their intended purpose.
- Using several products at once: choose images **photographed from the same angle**.
- Resize images so products are appropriately showcased; include the relevant product images.
- When cropping a form, the intended image must still read clearly.
- **One EI form per image** is recommended — including lifestyle images and individual products.
- Use forms to *highlight* the subject. Avoid excessive design that detracts from the very
  image you are trying to emphasise.

## EI Lens

The EI lens makes the system feel intelligent and warm. Its stated jobs:

- create warmth through depth
- turn image viewing into a life-like experience
- unify images with a distinctive look
- convey image, tone and lifestyle emotionally
- bring focus to designs and content
- adapt to the customer's needs and interests

Its two characters, in the guideline's own words: **Intelligent** — "always moving and
adapting, anticipating your needs"; **Respectful** — "knows when to fit neatly around you vs
stand out and catch your attention."

**Where it is used:** to emphasise specific parts of a product, and to deliver important
information clearly. Concretely — product detail emphasis when you need attention on a
feature's detail or functionality, and message emphasis when introducing a feature or drawing
attention to a message.

It can be paired with both core and connected EI forms.

## EI Form Motion

For digital and video only. Three animations:

| Motion | Character | Layout use |
| --- | --- | --- |
| **Adaptive** — "Adapt Flexibly" | forms adapt to the user's movement, from refined interfaces to dynamic presentation | the basic layout: convey a story clearly, or transition to something new |
| **Connected** — "Connect with Experiences" | forms connect product attributes to user experience | multiple forms interacting and connecting |
| **Fluid** — "Flow Organically" | forms flow among content, communicating while moving | multiple forms interacting, emphasising flexibility through more dynamic expression |

Production notes from p.106, for whoever builds it in After Effects:

- The EI Form Motion System is composed **solely of EI forms** — this is what allows uniform
  movement without animating individual paths.
- Use **Stroke Width and Offset Paths** to connect forms at uniform intervals, keeping outlines
  and distances consistent regardless of size or scale.
- Where form contours overlap, apply an **Adjustment Layer** for smooth curved edges, adjusting
  Blur, Exposure and Levels to the size and scale of each form.

`references/motion.md` and `scripts/lg_motion.py` borrow these three family names — and only
the names and their character, since the guideline gives no timings — for animating *layout*:
charts, headlines, process steps. That is an extension of LG's vocabulary beyond EI forms, not a
rule from the source, and the kit says so. The EI Form Motion System itself still needs the
After Effects templates, which this skill does not ship.

Per-motion guidance: Adaptive — enhance engagement with simple design. Connected — make the
motion's purpose and the flow of information easy to understand. Fluid — prioritise the brand
colour palette to reinforce recognition.

## Assets — and what to do about the ones that are missing

**The EI form shapes themselves are not in this skill's `assets/`, and neither are the eight
After Effects templates.** The guideline links to them for download inside LG's own systems.

So: an EI form must not be approximated with a rounded rectangle, a `border-radius`, an SVG
path drawn from the illustrations in the PDF, or anything else invented to look close. That
would break the skill's first rule as surely as redrawing the logo.

When a task needs EI forms:

1. Ask whether the shapes are available — they ship in LG's own asset portal, and a designer on
   the channel or marketing team will have them.
2. If they are not available, **say so and build without them.** A clean cropped product image
   with no EI form is explicitly approved by the guideline, so this is a real option and not a
   compromise you need to apologise for.
3. Never present an invented shape as an EI form.

**Not specified in source:** the geometry of the individual EI form shapes (radii, proportions,
how many exist), the exact Gaussian blur parameters beyond the 25 px guide value, and motion
timings or easing curves.
