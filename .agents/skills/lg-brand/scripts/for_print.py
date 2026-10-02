#!/usr/bin/env python3
"""
for_print.py - make an export-safe copy of a page that uses Digital Logo Play.

    python3 scripts/for_print.py deck.html            # writes deck-print.html
    python3 scripts/for_print.py deck.html -o out.html
    python3 scripts/for_print.py deck.html --check     # report only, change nothing

Why this exists:

Digital Logo Play is **only available in motion and only for digital environments**
(BI Guidelines V5.2, S1 p.33, p.37). The guideline's own reason is worth keeping in mind: the
animated mark is a line-art variant of the symbol, so a frozen frame *"would be confused as an
extension of our CI"*.

A GIF's first frame is exactly what a PDF export, a screenshot or a print captures. So a deck
that is correct on screen becomes a prohibited use the moment somebody prints it - and channel
decks at LG are printed and sent to dealers as a matter of routine.

`verify.py` warns about this with DLP_EXPORT_RISK. A warning that says "swap in the static logo
for that version" and leaves the work to a marketeer is a warning most people will skip, which
is why this file exists: it does the swap.

What it does, decided per canvas, because the right answer depends on the slide:

  - a slide that ALREADY carries the static logo has the animated mark **removed**. Replacing
    it there would put two master logos on one canvas, the second one sitting wherever the
    animated mark happened to be - which is not one of the five permitted positions.
  - a canvas where Digital Logo Play is the ONLY LG mark gets the static lockup instead,
    sized to the 1.3X rule rather than to the animated mark's box, since the static logo has
    a size rule the animated one does not.
  - either way a comment is left in the HTML saying what changed, so the diff is auditable.
  - nothing else on the page is touched.

Then verify the result - it is a different page now:

    python3 scripts/verify.py deck-print.html --canvas 1920x1080
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)

DLP = re.compile(r"Digital[ _]Logo[ _]Play", re.I)
IMG = re.compile(r"<img\b[^>]*>", re.I)
SRC = re.compile(r'src\s*=\s*"([^"]+)"', re.I)

# The compact lockup both times, because Digital Logo Play is the symbol alone and the compact
# lockup is the closest static equivalent that is still a permitted mark. There is no all-white
# COMPACT lockup in LG's pack - but the fix for a dark ground is NOT the corporate
# "LG Electronics" mark: S1 p.21 approves the compact Heritage Red symbol + white logotype on
# black and image grounds, and switching lockup families mid-piece is its own defect.
REPLACEMENT = {
    "black": ("assets/logo/LGE_Logo_Mono_Black_RGB.png", "compact mono black", "--logo-h"),
    "white": ("assets/logo/LGE_Logo_HeritageRed_White_RGB.png",
              "compact, Heritage Red symbol + white logotype - approved for black and image "
              "grounds (S1 p.21); there is no all-white compact mono file",
              "--logo-h"),
}


def relative_to(page_path, asset_rel):
    """The replacement path has to be written relative to the page, not to the skill."""
    target = os.path.join(SKILL, asset_rel)
    return os.path.relpath(target, os.path.dirname(os.path.abspath(page_path))).replace(os.sep, "/")


STATIC_LOGO = re.compile(r"LGE_Logo_|LGE_2D_LG-Electronics_Logo|LGE_Logotype")
CANVAS_SPLIT = re.compile(r'(?=<div[^>]*class="[^"]*lg-canvas)', re.I)


def swap(html, page_path):
    """Per canvas, because the right transformation depends on what else is on that slide.

    A slide that already carries the static logo does NOT want a second one: replacing the
    animated mark there would put two master logos on one canvas, and the second would land
    wherever the animated one happened to sit - which is not one of the five permitted
    positions. On those slides the animated mark is simply removed; the slide keeps its logo.

    A canvas where Digital Logo Play is the ONLY LG mark does need a replacement, and it is
    placed at the correct 1.3X size rather than at whatever size the animated mark used,
    since the static logo has a size rule the animated one does not.
    """
    swaps, removals = [], []
    out_parts = []

    for part in CANVAS_SPLIT.split(html):
        has_static = bool(STATIC_LOGO.search(part))

        def one(m):
            tag = m.group(0)
            src_m = SRC.search(tag)
            if not src_m or not DLP.search(src_m.group(1)):
                return tag
            old_src = src_m.group(1)
            motion = re.split(r"[_\\/]", old_src)[-1].rsplit(".", 1)[0]
            if has_static:
                removals.append(motion)
                return (f"<!-- for_print.py: Digital Logo Play ({motion}) removed - this slide "
                        f"already carries the static LG logo, and a second master logo placed "
                        f"where the animated mark sat would not be a permitted position. -->")
            variant = "white" if re.search(r"_White_", old_src) else "black"
            rel, why, hvar = REPLACEMENT[variant]
            new_src = relative_to(page_path, rel)
            swaps.append((motion, variant, os.path.basename(rel), why))
            tag = tag[:src_m.start(1)] + new_src + tag[src_m.end(1):]
            tag = re.sub(r'\s(width|height)\s*=\s*"[^"]*"', "", tag)
            size = f"height:var({hvar});width:auto;"
            if re.search(r'style\s*=\s*"', tag):
                tag = re.sub(r'(style\s*=\s*")', r"\1" + size, tag, count=1)
            else:
                tag = tag[:-1].rstrip() + f' style="{size}">'
            return (f"<!-- for_print.py: Digital Logo Play ({motion}) -> "
                    f"{os.path.basename(rel)}, resized to the 1.3X rule -->\n" + tag)

        out_parts.append(IMG.sub(one, part))

    return "".join(out_parts), swaps, removals


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page")
    ap.add_argument("-o", "--out", help="default: <page>-print.html next to the original")
    ap.add_argument("--check", action="store_true", help="report what would change, write nothing")
    a = ap.parse_args()

    if not os.path.isfile(a.page):
        sys.exit(f"no such file: {a.page}")
    html = open(a.page, encoding="utf-8").read()
    out, swaps, removals = swap(html, a.page)

    if not swaps and not removals:
        print(f"{a.page} has no Digital Logo Play on it - nothing to swap.\n"
              f"It is already safe to export or print, as far as this rule goes.")
        return 0

    print(f"Digital Logo Play on {os.path.basename(a.page)}:")
    for motion in removals:
        print(f"  {motion:<14} removed        (slide already carries the static logo)")
    for motion, variant, newfile, why in swaps:
        print(f"  {motion:<14} ({variant})  ->  {newfile}")
        if "no all-white" in why:
            print(f"                 note: {why}")

    if a.check:
        print("\n--check: nothing written.")
        return 1

    dest = a.out or (os.path.splitext(a.page)[0] + "-print.html")
    open(dest, "w", encoding="utf-8").write(out)
    print(f"\nwritten: {dest}")
    print("Keep the original for screen use - it is correct there, and Digital Logo Play is\n"
          "the better mark in a digital environment. This copy is only for the printed or\n"
          "exported version.\n")
    print("Now verify it, because the static logo has a size rule the animated one does not:\n"
          f"  python3 scripts/verify.py {dest} --canvas WxH")
    return 0


if __name__ == "__main__":
    sys.exit(main())
