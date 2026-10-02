# Photography and renders

Source: `01_LG_BI_Guidelines_V5_MASTER.pdf` section 12, PDF p.133–152 (doc p.19–38).

Most posters, key visuals and social posts are 80% photograph. The grid and the logo can be
perfect and the piece will still fail a brand review if the image is cold, staged or cluttered
— those are the named failures below, and they are the ones that actually get flagged.

## The six principles, common to all LG photography (p.133)

| Principle | What it means in the source's words |
| --- | --- |
| **Authenticity** | conveys real, relatable moments — how life's not perfect, but Life's Good |
| **Positive and joyful** | shows how we've designed experiences and products that make people feel good |
| **Warmth** | through natural, calm lighting, or conveying a human touch to our tech |
| **Breathing space** | helps us focus clearly on the subject |
| **Celebrate diversity** | of people, personalities, needs, spaces — our designs are for all |
| **Attention to detail** | both lifestyle and product photos composed with attention to detail, for a high level of craft |

"Breathing space" is the one that connects photography to the grid: an image with no quiet area
leaves nowhere for the headline, and the layout system depends on that space existing.

## Lifestyle photography

**Principles (p.136)**

- **Capture authentic moments** — a real glimpse of day-to-day life, relatable everyday
  scenarios enriched by LGE, so the viewer can empathise with the positive emotions shown.
- **Natural and calm light** — soft, natural, across a range of people, environments and
  contexts.
- **Using depth to create warmth** — deep focus creating a sense of depth. The guideline notes
  this also helps with text placement, which makes it a layout decision as much as a photographic
  one.

**Avoid (p.137)**

1. Unnatural product placement and staged scenes.
2. Cold, monotone, lifeless luxury — luxury can still feel warm.
3. Over-cluttering; create a clear focal point.
4. Shots from behind people.

**Don'ts (p.137)**

1. Don't use cold, staged and cliché imagery.
2. Don't use cold homes with harsh lighting.
3. Don't use people with a negative look or feeling.
4. Don't show overly aspirational lifestyles.
5. Don't use somber imagery.
6. Don't use busy, dirty or cluttered imagery — always ensure there's space for messaging.

## Product photography — three categories (p.139)

The guideline splits product imagery into **Product Isolated**, **Product Abstract** and
**Product Close-ups**, each with its own principles and prohibitions. Pick the category
deliberately: it determines what the shot is allowed to do.

### Product Isolated

The product in its clearest, most precise form — a clear, functional role across the system.

**Principles (p.142)**

- **Clear and precise** — shot with a **long focal length** for a clean, precise feel.
- **A red thread** — should feel uniquely LG through the brand assets.
- **Warm backgrounds** — warm and real, stepping away from cold and clinical.
- **People + product** — we make products for people; add warmth where possible.

**Don'ts (p.143)**

1. Don't comp products with people — **only shoot or render a product in its natural intended
   context**.
2. Don't use different angles or perspectives in one image comp.
3. Don't comp 2D images into 3D scenes or spaces.
4. Don't comp products onto abstract backgrounds or images.
5. Don't render products in lifeless, empty or unnatural spaces.
6. Don't comp products without natural shadows on solid backgrounds.

Number 6 matters for the common case of a cut-out product on a flat brand colour: the cut-out
needs a natural shadow, or it reads as pasted on.

### Product Abstract

Elevates the narrative — communicating abstract concepts such as sound, and building a
connected LG world through lighting, colour, material and form.

**Principles (p.146)**: elevate product features with a clear narrative; set in a natural
environment that feels warm and real; a red thread through core brand assets — colour,
materials, lighting, forms; connect products and people.

**Don'ts (p.147)**

1. Don't use images or renders that feel cold and lifeless.
2. Don't overlay 'breakdown' graphics on top of images.
3. Don't add 2D products and graphics onto an image — only rendered or shot images.
4. Don't use 'illustrative' spaces that have no brand connection.
5. Don't overlay complex graphics on 2D product comps.

### Product Close-ups

Craft, attention to detail and quality, shown through close shots.

**Principles (p.150)**

- **Natural lighting and shadows** — warm natural light with cast shadows, grounding the image
  in reality.
- **Depth of field** — a shallow depth of field draws the viewer in and focuses on the detail.
- **Close crops** — capture materials, craft and detail.
- **In a real environment** — a place people can relate to their daily lives.

Note the deliberate contrast with Product Isolated: close-ups want a *shallow* depth of field,
isolated shots want a *long focal length* and precision. They are different jobs.

**Don'ts (p.151)**

1. Don't shoot close-ups in cold, sterile environments.
2. Don't focus on complex or unappealing details.
3. Don't place products in or against graphics that are not part of the brand.
4. Don't overlay unnatural hands or cutouts onto photography or renders.
5. Don't use wide-angle lenses or short focal lengths that distort images or give an unnatural
   perspective.

## Using a supplied product image

Most channel work starts from an official product shot rather than a new photograph. The rules
still apply, and two of them bite in practice:

- **Don't comp it into a scene it was not shot for.** A studio cut-out dropped onto a lifestyle
  photograph breaks Product Isolated Don'ts 1, 3 and 4 at once.
- **Give a cut-out its shadow.** On a solid or gradient ground, a product with no natural shadow
  is Don't 6.

If a cut-out on a flat warm-grey field is all the source material allows, that is a legitimate
and honest outcome — say that the composition was constrained by the available image rather
than inventing an environment for it.

**Cutting the studio background out, without eating the product.** Most official product shots
ship on a flat white field, and a global "make white pixels transparent" pass will bleed into
any white or cream plastic on the product itself (WashTower's own front panel measured this way
once — see the correction below). Key the background out with a border-seeded flood fill in
floating/gradient-tolerant mode (each new pixel compared to its already-filled *neighbour*, not
to an absolute white target) so the cut follows the background's own lighting gradient and stops
the instant it meets the product's edge, regardless of how light that edge is. Then check: does
the connected background region form exactly one component? More than one usually means the
tolerance ate into the product.

**Then give it the shadow Don't 6 asks for.** A studio cut-out with no shadow reads as pasted on
however clean the crop is. A soft, blurred, low-opacity ellipse under the base — a few percent
of the image height, wide and flat, not a hard circle — is enough; it is a compositing
convention for placing a real product photo on a solid ground, not an invented environment, so
it does not conflict with "don't add unnatural elements." Leave room for it: if the source crop
runs to the very edge of its canvas, pad the canvas before drawing the shadow rather than
overlapping it onto the product.

## Image technical requirements

From the BI Workshop 2025 deck, p.108:

- Saved as **JPG or PNG**
- Maximum file size **5120 KB**
- Content in the **centre 80%** of the image — the safe area that will not be cropped at other
  breakpoints

The LG.com guide adds that **text must never be embedded in an image**; it treats that as a web
accessibility violation. See `web-system.md`.

## Assets

**No photography ships with this skill.** The images in the guideline are sample images and the
PDF states plainly, on nearly every page: *"Do not change, edit, recreate, or use images
externally."*

So imagery has to come from the user — an official product shot, a licensed library image, or a
commissioned photograph. Do not extract images from the guideline PDFs to use in a deliverable,
and do not generate a synthetic "LG-style" lifestyle photograph to stand in for one. If a piece
needs an image nobody has, say so and design the layout around the gap.
