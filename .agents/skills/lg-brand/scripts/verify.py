#!/usr/bin/env python3
"""
verify.py - the real brand check for an HTML deliverable.

    python3 scripts/verify.py page.html --canvas 1080x1350 [--web] [--shot out.png]

Why this exists, and why it is the entry point rather than brand_check.py:

The LG grid is expressed in CSS variables and calc(). A regex over the stylesheet cannot
evaluate `calc(var(--logo-symbol-h) / .668)`, so source-level checking of geometry is
guesswork that reports success. It missed a logo placed at a third of its required size -
a defect a human caught by eye - and passed 7 of 8 deliberately broken fixtures.

So geometry is measured in a real browser, where the cascade has already resolved. Elements
are found by the ASSET they load, not by class name, so a hand-built layout is checked as
strictly as one from templates/. The static checks (colour, gradients, font URLs, PPTX)
still come from brand_check.py; this file imports them so one command covers everything.

Exit 0 = clean. Exit 1 = at least one error. Exit 2 = the page could not be verified at all,
which is a failure, not a pass - a check that cannot run must never look like a check that
passed.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

try:
    import brand_check as bc
except ImportError:
    bc = None

# Measured geometry of the shipped artwork. See references/logo-and-slogan.md.
LOCKUPS = {
    # matched against the image filename
    "compact":   {"re": r"LGE_Logo_(HeritageRed|Mono)", "sym_share": 0.668, "aspect": 2081 / 1127},
    "wide":      {"re": r"LGE_2D_LG-Electronics_Logo",  "sym_share": 0.671, "aspect": 5452 / 1130},
    "logotype":  {"re": r"LGE_Logotype",                "sym_share": None,  "aspect": 4509 / 1127},
}
# The animated mark. It is a line-art variant of the symbol, which is why a frozen frame
# reads as a second, unofficial logo - hence the prohibition on static media.
DIGITAL_LOGO_PLAY = r"Digital[ _]Logo[ _]Play"

SLOGAN_H = r"LGE_Electronics_Slogan_Horizontal"
SLOGAN_S = r"LGE_Electronics_Slogan_Stacked"
SLOGAN_INK_SHARE = 0.669
SLOGAN_ASPECT_H = 3832 / 870

LOGO_SYMBOL_X = 1.30
SLOGAN_INK_X = 0.90
TOL = 0.06          # 6% - covers rounding and sub-pixel layout, not a real size error
MIN_SYMBOL_PX = 16
MIN_SYMBOL_MM = 4.0

PERMITTED = ("upper-left", "upper-center", "upper-right", "middle-left", "bottom-left")

PROBE = r"""
(idx) => {
  const out = {elements: [], fonts: {errors: [], unresolved: []}};
  // A deck is several .lg-canvas on one page. Measuring only the first was how a five-slide
  // deck reported clean: four slides were never looked at. idx selects one; scoping the
  // element scan to that canvas keeps one slide's boxes out of another slide's report.
  const all_canvases = document.querySelectorAll('.lg-canvas');
  const canvas = all_canvases[idx] || document.body;
  const scope = all_canvases.length > 1 ? canvas : document;
  out.canvasCount = all_canvases.length;
  const cb = canvas.getBoundingClientRect();
  out.canvas = {w: cb.width, h: cb.height, x: cb.x, y: cb.y};

  out.fonts.faces = [];
  for (const f of document.fonts) {
    out.fonts.faces.push({family: f.family.replace(/^["']|["']$/g, ''),
                          weight: String(f.weight), status: f.status});
    if (f.status === 'error') out.fonts.errors.push(f.family + ' ' + f.weight);
  }

  // Does this page animate at all, and does it respect someone who asked it not to?
  // Reading the rules can throw on a cross-origin stylesheet; a page we cannot read is
  // reported as unknown rather than guessed at.
  out.motion = {keyframes: 0, reducedGuard: false, readable: true};
  const scan = (rules) => {
    for (const r of rules) {
      if (r.type === CSSRule.KEYFRAMES_RULE || r.constructor.name === 'CSSKeyframesRule')
        out.motion.keyframes++;
      if (r.media && String(r.media.mediaText).indexOf('prefers-reduced-motion') >= 0)
        out.motion.reducedGuard = true;
      if (r.cssRules) scan(r.cssRules);
    }
  };
  for (const ss of document.styleSheets) {
    try { scan(ss.cssRules); } catch (e) { out.motion.readable = false; }
  }

  const all = scope.querySelectorAll('*');
  // Paint order, roughly: an element later in document order (or with a higher z-index)
  // paints over an earlier one. That is what decides whether an overlap hides text or is
  // simply text sitting on top of its own background. Stacking contexts can complicate it;
  // this is the common case and it is stated as an approximation in the report.
  const eidOf = new WeakMap();
  for (const el of all) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) continue;
    const text = (el.childElementCount === 0 ? (el.textContent || '').trim() : '');
    const rec = {
      tag: el.tagName.toLowerCase(),
      cls: el.className && el.className.baseVal !== undefined ? el.className.baseVal : (el.className || ''),
      // A brand asset can arrive as <img src>, or as a CSS background-image. Reading only
      // the first lets a background-image logo escape measurement entirely.
      src: (el.tagName === 'IMG' ? (el.getAttribute('src') || '') : '')
           || ((cs.backgroundImage.match(/url\((?:"|')?([^"')]+)/) || [])[1] || ''),
      viaBackground: el.tagName !== 'IMG' && cs.backgroundImage !== 'none',
      // A missing file, a typo'd path or a corrupt image all render as an empty box the
      // page keeps its layout around. naturalWidth is the only honest signal.
      loaded: el.tagName !== 'IMG' ? null : (el.complete && el.naturalWidth > 0),
      x: r.x - cb.x, y: r.y - cb.y, w: r.width, h: r.height,
      transform: cs.transform,
      round: (parseFloat(cs.borderRadius) >= r.width * 0.4) || cs.borderRadius.indexOf('50%') >= 0,
      brandRed: ['rgb(253, 49, 46)', 'rgb(165, 0, 52)', 'rgb(234, 25, 23)'].indexOf(cs.backgroundColor) >= 0,
      family: cs.fontFamily, weight: cs.fontWeight, size: cs.fontSize,
      color: cs.color, bg: cs.backgroundColor,
      text: text.slice(0, 40),
      hasText: text.length > 0
    };

    // paint order and parentage, for the overlap check
    rec.eid = out.elements.length;
    let anc = el.parentElement, pe = -1;
    while (anc) { if (eidOf.has(anc)) { pe = eidOf.get(anc); break; } anc = anc.parentElement; }
    rec.parentEid = pe;
    rec.z = cs.zIndex === 'auto' ? 0 : (parseInt(cs.zIndex, 10) || 0);
    // "opaque" = something that would hide what is behind it
    const bgm = cs.backgroundColor.match(/rgba?\(([^)]+)\)/);
    const bga = bgm ? (bgm[1].split(',')[3] === undefined ? 1 : parseFloat(bgm[1].split(',')[3])) : 0;
    rec.opaque = el.tagName === 'IMG' || bga > 0.5;
    // The layout box, which is what CSS positions with. A transform changes what is painted
    // and leaves this untouched - the trap that put ten items over the margin on a 1920px slide.
    rec.layoutW = el.offsetWidth || r.width;
    rec.layoutH = el.offsetHeight || r.height;
    // An asset is animated whether the keyframes sit on it or on a wrapper around it - the
    // mark moves either way, and the wrapper is the more likely way someone does it.
    rec.anim = (cs.animationName && cs.animationName !== 'none') ? cs.animationName : '';
    rec.animAncestor = '';
    if (!rec.anim) {
      for (let p = el.parentElement; p && p !== document.documentElement; p = p.parentElement) {
        const pcs = getComputedStyle(p);
        if (pcs.animationName && pcs.animationName !== 'none') { rec.animAncestor = pcs.animationName; break; }
      }
    }
    // Not everything animates through CSS. element.animate() leaves animationName as 'none',
    // so a logo moved from JavaScript would walk straight past the check above.
    // getAnimations() sees CSS animations, transitions and the Web Animations API alike.
    try {
      if (!rec.anim && el.getAnimations && el.getAnimations().length) rec.anim = 'script-driven';
    } catch (e) {}
    rec.transitions = (parseFloat(cs.transitionDuration) > 0 &&
                       /transform|opacity|all|filter/.test(cs.transitionProperty))
                      ? cs.transitionProperty : '';
    if (text) {
      const spec = cs.fontStyle + ' ' + cs.fontWeight + ' ' + cs.fontSize + ' ' + cs.fontFamily;
      try { rec.fontOk = document.fonts.check(spec, text); } catch (e) { rec.fontOk = null; }
      // fonts.check() says "available", not "used": an unavailable family whose fallback can
      // render the glyphs still returns true. The decisive signal is whether a @font-face for
      // this family exists at all. A width probe corroborates, but only as a hint - at some
      // sizes a real face and the fallback happen to measure within a third of a pixel of
      // each other, which is how this check once raised a false alarm.
      rec.firstFamily = (cs.fontFamily.split(',')[0] || '').trim().replace(/^["']|["']$/g, '');
      const ctx = (window.__m || (window.__m = document.createElement('canvas').getContext('2d')));
      const probe = 'MWmwiIl1@#0OÔgjQ\u0111\u1EAB';   // wide/narrow/diacritic mix, amplifies difference
      const big = '200px ';
      ctx.font = big + cs.fontFamily;
      const wDeclared = ctx.measureText(probe).width;
      ctx.font = big + 'serif';
      const wSerif = ctx.measureText(probe).width;
      ctx.font = big + 'monospace';
      const wMono = ctx.measureText(probe).width;
      rec.widthHint = !(Math.abs(wDeclared - wSerif) < 0.5 || Math.abs(wDeclared - wMono) < 0.5);
    }
    out.elements.push(rec);
    eidOf.set(el, rec.eid);
  }
  return out;
}
"""


class Report:
    def __init__(self):
        self.rows = []
        self.context = ""     # "slide 2/5: " when a deck is being measured
        self.slide = 0        # which canvas the row belongs to, 0-based
        self.frames = []      # one per canvas: index, screenshot path, rendered size
        self.lockups = {}     # lockup family -> the slides it appears on, judged piece-wide
        self.broken = ""      # set when the run could not complete; never a pass

    def _add(self, lvl, code, msg, hint="", box=None):
        """box, when given, is the offending element's rect on its own canvas. It costs one
        argument at the call site and it is what lets report.py draw the finding on the
        render instead of describing it - which is the difference between a report a
        marketeer can act on and a list of error codes."""
        self.rows.append({"level": lvl, "code": code, "msg": f"{self.context}{msg}",
                          "hint": hint, "slide": self.slide, "box": box})

    def incomplete(self, reason):
        """The run did not finish. This is the one state that must never print reassurance:
        a page that could not be measured has not been checked, and the whole point of this
        file is that a check which cannot run must not look like a check that passed."""
        self.broken = reason
        self._add("ERROR", "VERIFY_INCOMPLETE", f"the page could not be measured: {reason}")

    def error(self, *a, **kw):
        self._add("ERROR", *a, **kw)

    def warn(self, *a, **kw):
        self._add("WARN", *a, **kw)

    def info(self, *a, **kw):
        self._add("INFO", *a, **kw)

    def codes(self):
        return {r["code"] for r in self.rows if r["level"] == "ERROR"}

    def dump(self, target):
        order = {"ERROR": 0, "WARN": 1, "INFO": 2}
        self.rows.sort(key=lambda r: order[r["level"]])
        errs = sum(1 for r in self.rows if r["level"] == "ERROR")
        warns = sum(1 for r in self.rows if r["level"] == "WARN")
        print(f"\nlg-brand verify - {target}")
        print("=" * 76)
        for lvl, code, msg, hint in ((r["level"], r["code"], r["msg"], r["hint"])
                                     for r in self.rows):
            print(f"  [{ {'ERROR':'x','WARN':'!','INFO':'i'}[lvl] }] {code:<24} {msg}")
            if hint:
                print(f"      -> {hint}")
        print("-" * 76)
        print(f"  {errs} error(s), {warns} warning(s)")
        if self.broken:
            print("\n  THIS IS NOT A PASS. The page was never measured, so nothing above")
            print("  says anything about whether it is on brand. Fix the reason and run again;")
            print("  do not report the work as verified.")
            return 2
        if not errs:
            print("  Geometry, fonts and assets check out. Now look at the render: this cannot")
            print("  see that a composition is weak or that a crop killed the gradient.")
        return 1 if errs else 0


def lockup_of(src):
    for name, spec in LOCKUPS.items():
        if re.search(spec["re"], src):
            return name
    return None


def parse_canvas(s):
    m = re.match(r"^\s*([\d.]+)\s*[x×]\s*([\d.]+)\s*(px|mm)?\s*$", s or "")
    if not m:
        return None
    return float(m.group(1)), float(m.group(2)), (m.group(3) or "px")


def check_page(path, canvas, rep, shot=None, web=False):
    """Render the page once, then measure every .lg-canvas on it.

    A deck is several canvases in one file. The old version screenshotted `.lg-canvas` with a
    strict locator, so any page with more than one threw - and the throw was caught upstream
    and printed as a line of prose while the summary still said "0 errors". A five-slide deck
    with two missing logos reported clean. Hence: count the canvases, measure each.
    """
    import tempfile
    from playwright.sync_api import sync_playwright

    tmpdir = tempfile.mkdtemp()
    W, H, unit = canvas
    # mm canvases are laid out at CSS-mm; render at a px viewport big enough to hold them
    px_per_unit = 1.0 if unit == "px" else 96 / 25.4
    vw, vh = int(round(W * px_per_unit)), int(round(H * px_per_unit))

    frames = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": vw, "height": vh})
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        # An <img> reports naturalWidth, but a logo set as a CSS background-image reports
        # nothing at all - the box is simply empty. The network layer sees both.
        failed = []
        pg.on("requestfailed", lambda r: failed.append(r.url))
        pg.on("response", lambda r: failed.append(r.url) if r.status >= 400 else None)
        pg.goto("file://" + os.path.abspath(path))
        pg.wait_for_timeout(2000)
        try:
            pg.evaluate("async () => { await document.fonts.ready; }")
        except Exception:
            pass
        # Page chrome - a navigation hint, a toolbar, anything the deck shows the person
        # driving it - is not part of the deliverable. Marking it data-noexport keeps it out
        # of both the measurement and the screenshots a review report is built from.
        try:
            pg.eval_on_selector_all("[data-noexport]",
                                    "els => els.forEach(e => e.style.display = 'none')")
            # A deck scales itself down to fit the window it is opened in. That is a viewing
            # convenience, not the artwork - the artwork is 1920x1080 and must be measured at
            # 1920x1080. Reset the fit so a narrow render viewport cannot shrink the geometry
            # being checked.
            pg.evaluate("() => { document.documentElement.style.setProperty('--fit-page','1');"
                        "        document.documentElement.style.setProperty('--fit','1'); }")
        except Exception:
            pass
        loc = pg.locator(".lg-canvas")
        n = max(1, loc.count())
        for i in range(n):
            data = pg.evaluate(PROBE, i)
            if shot:
                out = shot if n == 1 else f"{os.path.splitext(shot)[0]}-{i + 1}.png"
            else:
                out = os.path.join(tmpdir, f"render{i + 1}.png")
            (loc.nth(i) if loc.count() else pg).screenshot(path=out)
            frames.append((data, out))
        b.close()

    for e in errors:
        rep.warn("PAGE_ERROR", f"javascript error on the page: {e[:100]}")

    # Reported once for the page rather than once per slide: a file is missing or it is not.
    for url in dict.fromkeys(failed):
        name = os.path.basename(url.split("?")[0])
        if name.lower().endswith((".otf", ".ttf", ".woff", ".woff2")):
            continue          # fonts have their own, more specific check
        brand = (lockup_of(url) or re.search(SLOGAN_H, url) or re.search(SLOGAN_S, url)
                 or re.search(DIGITAL_LOGO_PLAY, url, re.I)
                 or re.search(r"Gradient_0\d_RGB", url))
        rep.error("LOGO_ABSENT" if brand else "ASSET_NOT_LOADED",
                  f'the {"brand asset" if brand else "file"} "{name}" failed to load',
                  "The page requested it and got nothing back. A background-image that 404s "
                  "leaves an empty box with the layout intact, so it is invisible in review.")

    if n > 1:
        rep.info("DECK", f"{n} canvases on this page - each one measured separately")

    for i, (data, out) in enumerate(frames):
        rep.context = f"slide {i + 1}/{n}: " if n > 1 else ""
        rep.slide = i
        rep.frames.append({"index": i, "shot": out,
                           "w": data["canvas"]["w"], "h": data["canvas"]["h"]})
        analyse(data, canvas, rep, out, web)
    rep.context, rep.slide = "", 0

    # Judged across the whole piece, not per canvas: the defect is that slide 2 carries a
    # different mark from slide 1, which no single-canvas rule can see.
    if len(rep.lockups) > 1:
        where = "; ".join(f"{fam} on slide(s) {', '.join(map(str, sorted(set(sl))))}"
                          for fam, sl in sorted(rep.lockups.items()))
        rep.error("LOGO_VARIANT_MIXED",
                  f"this piece uses more than one LG lockup - {where}",
                  "Pick one and keep it. The compact symbol + 'LG' and the wide symbol + "
                  "'LG Electronics' are different marks, and alternating them across a deck "
                  "reads as two brands. logo-and-slogan.md: the compact lockup is the default; "
                  "the wide one is for where the full company name is required. On dark "
                  "grounds the compact variant is LGE_Logo_HeritageRed_White_RGB.png.")

    return frames[0][0] if frames else {}


def analyse(data, canvas, rep, shot, web=False):
    """Everything measured about ONE canvas."""
    W, H, unit = canvas
    px_per_unit = 1.0 if unit == "px" else 96 / 25.4
    vw, vh = int(round(W * px_per_unit)), int(round(H * px_per_unit))
    cw, ch = data["canvas"]["w"], data["canvas"]["h"]
    if abs(cw - vw) > 2 or abs(ch - vh) > 2:
        rep.warn("CANVAS_MISMATCH",
                 f".lg-canvas rendered {cw:.0f}x{ch:.0f}, --canvas said {vw}x{vh}",
                 "Geometry is judged against the rendered box, so check which one is wrong.")
    margin = 0.05 * min(cw, ch)
    rep.info("GRID", f"canvas {cw:.0f}x{ch:.0f} -> margin {margin:.1f}, gutter {margin/2:.1f}, "
                     f"symbol h {LOGO_SYMBOL_X*margin:.1f}, slogan h {SLOGAN_INK_X*margin:.1f}")

    # ---------------- fonts ----------------
    for f in data["fonts"]["errors"]:
        rep.error("FONT_NOT_RENDERED", f"@font-face failed to load: {f}",
                  "The browser has silently substituted a system font. Check the url() paths "
                  "in the stylesheet - they are relative to the CSS file, not the HTML.")
    bad_text = [e for e in data["elements"] if e.get("hasText") and e.get("fontOk") is False]
    for e in bad_text[:5]:
        rep.error("FONT_NOT_RENDERED",
                  f"text \"{e['text']}\" cannot be rendered in {e['family']} {e['weight']}",
                  "Either the face is not loaded or it lacks these glyphs.")
    declared_families = {f["family"].lower() for f in data["fonts"].get("faces", [])}
    substituted = [e for e in data["elements"]
                   if e.get("hasText") and "lg ei" in e["family"].lower()
                   and e.get("firstFamily", "").lower() not in declared_families]
    for e in substituted[:5]:
        rep.error("FONT_NOT_RENDERED",
                  f"text \"{e['text']}\" declares {e['firstFamily']}, for which no @font-face "
                  f"exists - it renders in a substituted font",
                  "The family name is right and the face is missing - most often no "
                  "@font-face for that weight. LG EI Text ships each weight as its own "
                  "family, so every weight needs its own rule.")
    for e in [x for x in data["elements"]
              if x.get("hasText") and "lg ei" in x["family"].lower()
              and x.get("widthHint") is False and x not in substituted][:3]:
        rep.warn("FONT_MAY_BE_SUBSTITUTED",
                 f"text \"{e['text']}\" measures the same as a generic fallback",
                 "The face is declared, so this is usually a false alarm - confirm by eye "
                 "in the render before acting on it.")
    non_lg = [e for e in data["elements"]
              if e.get("hasText") and "lg ei" not in e["family"].lower()]
    for e in non_lg[:5]:
        rep.error("FONT_NOT_LG", f"text \"{e['text']}\" is set in {e['family']}",
                  "All LG type is LG EI Headline or LG EI Text.")

    # ---------------- find the brand assets by what they load ----------------
    imgs = [e for e in data["elements"] if e["src"]]

    # An <img> whose file is missing still occupies a box, still matches the filename
    # patterns below, and still gets measured - so a deck with no logo on it once came back
    # as a warning that the logo "is only 35px wide". A broken asset is an absent asset.
    for e in [x for x in imgs if x.get("loaded") is False]:
        name = os.path.basename(e["src"])
        brand = (lockup_of(e["src"]) or re.search(SLOGAN_H, e["src"])
                 or re.search(SLOGAN_S, e["src"])
                 or re.search(DIGITAL_LOGO_PLAY, e["src"], re.I)
                 or re.search(r"Gradient_0\d_RGB", e["src"]))
        if brand:
            rep.error("LOGO_ABSENT",
                      f'the brand asset "{name}" is on the page but did not load',
                      "Nothing is rendering there. Check the path, and check the file exists "
                      "in assets/ - the all-white COMPACT lockup, for one, is not in LG's pack "
                      "at all. On a dark ground that does NOT mean switching to the wide "
                      "'LG Electronics' lockup: use LGE_Logo_HeritageRed_White_RGB.png, the "
                      "compact mark with a white logotype, which S1 p.21 approves for black "
                      "and image grounds.")
        else:
            rep.error("ASSET_NOT_LOADED",
                      f'the image "{name}" did not load',
                      "A missing or mistyped path renders as an empty box that keeps its "
                      "layout, so the page looks structurally fine and ships with a hole in it.")
    imgs = [e for e in imgs if e.get("loaded") is not False]

    logos = [e for e in imgs if lockup_of(e["src"])]
    slogans = [e for e in imgs if re.search(SLOGAN_H, e["src"]) or re.search(SLOGAN_S, e["src"])]
    grads = sorted({m.group(1) for e in imgs
                    for m in [re.search(r"Gradient_0(\d)_RGB", e["src"])] if m})

    if len(grads) > 1:
        rep.error("GRADIENT_TWO", f"two master gradients in one piece: {grads}",
                  "Never two gradients at the same time.")

    # ---------------- Digital Logo Play ----------------
    dlp = [e for e in imgs if re.search(DIGITAL_LOGO_PLAY, e["src"], re.I)]
    for e in dlp:
        motion = re.split(r"[_\\/]", e["src"])[-1].rsplit(".", 1)[0]
        if unit == "mm":
            rep.error("DLP_ON_STATIC_MEDIA",
                      f"Digital Logo Play ({motion}) is placed on a print canvas",
                      "It is only available in motion and only for digital environments. A "
                      "still frame reads as a second, unofficial logo, which is the reason the "
                      "guideline gives. Use the static logo here.")
        else:
            rep.warn("DLP_EXPORT_RISK",
                     f"Digital Logo Play ({motion}) is on this page",
                     "Fine while it animates. If this page is ever exported to PDF or printed, "
                     "the still first frame becomes a prohibited use - swap in the static logo "
                     "for that version.")
        if e["transform"] and e["transform"] not in ("none", "matrix(1, 0, 0, 1, 0, 0)"):
            rep.error("DLP_TRANSFORMED",
                      f"a transform is applied to Digital Logo Play: {e['transform']}",
                      "The eight movements are fixed artwork - not to be changed or recreated.")
    if dlp and not logos:
        rep.warn("DLP_WITHOUT_MASTER_LOGO",
                 "Digital Logo Play is the only LG mark on this canvas",
                 "In the end-frame sequence it precedes the master logo rather than replacing "
                 "it. Confirm the master logo appears somewhere in the application.")

    # ---------------- is this the right lockup at all? ----------------
    # Every rule above measures whichever mark is on the page. None of them asked whether it
    # is the mark this piece should carry - so a deck that used the compact "LG" lockup on its
    # light slides and the corporate "LG Electronics" lockup on its dark ones passed clean,
    # changing brand identity halfway through. The variant was picked because a white file
    # happened to exist, not because the guideline pointed at it.
    for e in logos:
        fam = lockup_of(e["src"])
        if fam:
            rep.lockups.setdefault(fam, []).append(rep.slide + 1)
    for e in logos:
        if lockup_of(e["src"]) == "wide":
            rep.warn("LOGO_CORPORATE_LOCKUP",
                     f"the wide 'LG Electronics' lockup is used ({os.path.basename(e['src'])})",
                     "That is the corporate signature, for pieces where the full company name "
                     "is required. Product, channel and campaign work defaults to the compact "
                     "symbol + 'LG'. On a dark ground the compact variant is "
                     "LGE_Logo_HeritageRed_White_RGB.png (S1 p.21).")
        if re.search(LOCKUPS["logotype"]["re"], e["src"]):
            rep.warn("LOGO_WORDMARK_ALONE",
                     f"the 'LG Electronics' wordmark is used without the symbol "
                     f"({os.path.basename(e['src'])})",
                     "The wordmark on its own is not the master logo. Unless a layout "
                     "specifically calls for the wordmark, use a lockup that includes the "
                     "symbol.")

    # ---------------- motion applied to fixed artwork ----------------
    # LG has exactly one official animated mark, and it is Digital Logo Play. Animating the
    # logo, the logotype, the slogan or a master gradient - directly or through a wrapper -
    # creates an unofficial animated mark out of artwork that is fixed by the guideline.
    gradient_imgs = [e for e in imgs if re.search(r"Gradient_0\d_RGB", e["src"])]
    for e in logos + slogans + gradient_imgs:
        moving = e.get("anim") or e.get("animAncestor") or e.get("transitions")
        if not moving:
            continue
        what = ("the slogan" if e in slogans else
                "a master gradient" if e in gradient_imgs else "the logo")
        where = "on it" if e.get("anim") or e.get("transitions") else "on the element wrapping it"
        rep.error("BRAND_ASSET_ANIMATED",
                  f"{what} is animated ({moving}, {where})",
                  "These are fixed artwork. LG's only official animated mark is Digital Logo "
                  "Play, which ships in assets/digital-logo-play/ - animating the static logo "
                  "to imitate one is prohibited. Animate the layout around the mark instead; "
                  "scripts/lg_motion.py has components that do exactly that.")
    for e in dlp:
        moving = e.get("anim") or e.get("animAncestor")
        if moving:
            rep.error("DLP_ANIMATED",
                      f"a CSS animation ({moving}) is applied to Digital Logo Play",
                      "The eight movements are fixed artwork and must not be changed, edited "
                      "or recreated. Adding motion on top of one is editing it.")

    if data.get("motion", {}).get("keyframes") and not data["motion"]["reducedGuard"]:
        rep.warn("MOTION_NO_REDUCED_GUARD",
                 f"the page defines {data['motion']['keyframes']} @keyframes rule(s) but has no "
                 f"prefers-reduced-motion guard",
                 "Not a guideline rule - ours. Anyone who has asked their system for reduced "
                 "motion should get the finished state, not the movement. The lg-motion base "
                 "CSS carries the guard; a hand-written animation needs its own.")

    # symbol used without the logotype
    for e in imgs:
        if lockup_of(e["src"]) or re.search(DIGITAL_LOGO_PLAY, e["src"], re.I):
            continue
        if re.search(r"symbol", e["src"], re.I) and 0.8 < (e["w"] / max(e["h"], 1)) < 1.25:
            rep.error("SYMBOL_ALONE", f"a square symbol-only image is placed: {e['src']}",
                      "The symbol may appear without the logotype only on business cards, "
                      "badges, and as a website/mobile/PC icon.")

    if not logos:
        if web:
            rep.info("LOGO_ABSENT_WEB", "no logo placed",
                     "Correct inside lge.com, where the site header carries it. Anywhere "
                     "without LG site chrome needs one.")
        else:
            rep.error("LOGO_ABSENT", "no LG logo asset is placed on this canvas",
                      "The logo is artwork from assets/logo/. If you meant to use a lockup "
                      "the skill does not ship, ask rather than substituting.")

    # ---------------- logo geometry and placement ----------------
    for e in logos:
        name = lockup_of(e["src"])
        spec = LOCKUPS[name]
        if spec["sym_share"] is None:
            rep.warn("LOGOTYPE_ONLY", f"the logotype-only asset is placed: {os.path.basename(e['src'])}",
                     "Confirm this is a context where the symbol is deliberately omitted.")
            continue
        sym = e["h"] * spec["sym_share"]
        ratio = sym / margin
        if abs(ratio - LOGO_SYMBOL_X) / LOGO_SYMBOL_X > TOL:
            hint = ("The 1.3X rule measures the SYMBOL. The PNG carries clear-space padding, "
                    f"so the file must be {LOGO_SYMBOL_X*margin/spec['sym_share']:.1f}px tall "
                    f"for the symbol to be {LOGO_SYMBOL_X*margin:.1f}px.")
            if abs(e["h"] - LOGO_SYMBOL_X * margin) / (LOGO_SYMBOL_X * margin) < 0.08:
                hint = ("This is the file set to 1.3X directly, which lands the symbol at "
                        "0.87X - about a third undersized, and it looks deliberate. ") + hint
            rep.error("LOGO_SIZE",
                      f"symbol is {sym:.1f}px = {ratio:.2f}X, expected {LOGO_SYMBOL_X:.2f}X "
                      f"({LOGO_SYMBOL_X*margin:.1f}px)", hint,
                      box=[e["x"], e["y"], e["w"], e["h"]])
        else:
            rep.info("LOGO_SIZE_OK", f"symbol {sym:.1f}px = {ratio:.2f}X ({name} lockup)")

        if sym < MIN_SYMBOL_PX and unit == "px":
            rep.error("LOGO_TOO_SMALL", f"symbol {sym:.1f}px is under the 16px minimum")
        if unit == "mm" and sym / px_per_unit < MIN_SYMBOL_MM:
            rep.error("LOGO_TOO_SMALL", f"symbol {sym/px_per_unit:.1f}mm is under the 4mm minimum")
        if e["w"] < 60 and "Small-Size" not in e["src"]:
            rep.warn("LOGO_USE_SMALL_ART", f"logo is only {e['w']:.0f}px wide",
                     "Use the *_Small-Size_*.png artwork below roughly 60px.")

        if e["transform"] and e["transform"] not in ("none", "matrix(1, 0, 0, 1, 0, 0)"):
            rep.error("LOGO_TRANSFORMED", f"a transform is applied to the logo: {e['transform']}",
                      "The logo may not be rotated, skewed, stretched or squashed.")

        pos = classify_position(e, cw, ch, margin)
        if pos is None:
            rep.error("LOGO_POSITION",
                      f"logo sits at x{e['x']:.0f} y{e['y']:.0f}, which is none of the five "
                      "permitted positions",
                      "Permitted: bottom-left, middle-left, upper-left, upper-centre, "
                      "upper-right. Bottom-right in particular is not on the list.",
                      box=[e["x"], e["y"], e["w"], e["h"]])
        else:
            rep.info("LOGO_POSITION_OK", f"logo {pos}")

    # ---------------- slogan ----------------
    if len(slogans) > 1:
        rep.error("SLOGAN_REPEATED", f"{len(slogans)} slogan assets placed",
                  "The slogan appears at most once per application.")
    if slogans and not logos:
        rep.error("SLOGAN_ALONE", "slogan placed with no logo",
                  "The slogan is never used without the logo somewhere in the application.")

    for e in slogans:
        stacked = bool(re.search(SLOGAN_S, e["src"]))
        ink = e["h"] * SLOGAN_INK_SHARE
        ratio = ink / margin
        signoff = is_signoff(e, cw, ch, margin)
        if stacked and signoff:
            rep.error("SLOGAN_STACKED_SIGNOFF",
                      "the stacked slogan is used as a sign-off",
                      "Do not use the stacked slogan as a sign-off - horizontal only.")
        if signoff and abs(ratio - SLOGAN_INK_X) / SLOGAN_INK_X > TOL:
            rep.error("SLOGAN_SIZE",
                      f"slogan is {ink:.1f}px = {ratio:.2f}X, expected {SLOGAN_INK_X:.2f}X "
                      f"({SLOGAN_INK_X*margin:.1f}px)",
                      "0.9X measures the visible artwork. The file carries padding, so it must "
                      f"be {SLOGAN_INK_X*margin/SLOGAN_INK_SHARE:.1f}px tall.",
                      box=[e["x"], e["y"], e["w"], e["h"]])
        elif signoff:
            rep.info("SLOGAN_SIZE_OK", f"slogan ink {ink:.1f}px = {ratio:.2f}X (sign-off)")
        else:
            rep.info("SLOGAN_LEAD", "slogan is not in a sign-off position; treated as a lead "
                                    "message, which is sized to the grid rather than to 0.9X")

        for lg in logos:
            gap = box_gap(lg, e)
            if gap < 2 * margin:
                rep.error("LOGO_SLOGAN_ADJACENT",
                          f"logo and slogan are {gap:.0f}px apart (under 2 x margin = "
                          f"{2*margin:.0f}px)",
                          "They must sit in separate regions of the layout with real space "
                          "between them. This rule appears four times in the source.")

    # ---------------- someone drawing the symbol instead of placing it ----------------
    for e in data["elements"]:
        if e["src"] or e["hasText"]:
            continue
        square = 0.85 < (e["w"] / max(e["h"], 1)) < 1.18 and 24 <= e["h"] <= ch * 0.5
        if square and e.get("round") and e.get("brandRed"):
            rep.error("LOGO_REDRAWN",
                      f"a round element filled with brand red at x{e['x']:.0f} y{e['y']:.0f} "
                      f"({e['w']:.0f}x{e['h']:.0f})",
                      "That is the symbol being redrawn. The symbol is fixed artwork in "
                      "assets/logo/ and is never approximated with a shape, a font or an emoji.")

    # ---------------- what the logo is actually sitting on ----------------
    check_overlap(data, cw, ch, rep)
    check_scaled_boxes(data, rep)
    if shot:
        check_text_contrast(shot, data, rep)
        if logos:
            check_ground(shot, logos, cw, ch, rep)

    # ---------------- margin encroachment ----------------
    band = margin
    offenders = []
    for e in data["elements"]:
        if e["tag"] in ("html", "body"):
            continue
        if "lg-canvas" in str(e["cls"]) or "lg-layer" in str(e["cls"]):
            continue
        is_brand = bool(e["src"] and (lockup_of(e["src"])
                        or re.search(SLOGAN_H, e["src"]) or re.search(SLOGAN_S, e["src"])))
        if not (e["hasText"] or e["tag"] == "img"):
            continue
        # Imagery anchored to a canvas edge is a deliberate bleed - a cropped gradient or a
        # photograph running off the page - and the guideline shows both. Brand assets are
        # never exempt: the logo and slogan sit on the margin line, full stop.
        if not is_brand and not e["hasText"]:
            touches = (e["x"] <= 1 or e["y"] <= 1
                       or e["x"] + e["w"] >= cw - 1 or e["y"] + e["h"] >= ch - 1)
            if touches:
                continue
        inside = (e["x"] >= band - 1 and e["y"] >= band - 1
                  and e["x"] + e["w"] <= cw - band + 1
                  and e["y"] + e["h"] <= ch - band + 1)
        if not inside:
            offenders.append(e)
    for e in offenders[:6]:
        what = f'"{e["text"]}"' if e["hasText"] else os.path.basename(e["src"] or e["tag"])
        rep.error("MARGIN_ENCROACHED",
                  f"{what} crosses the {margin:.0f}px margin "
                  f"(box x{e['x']:.0f} y{e['y']:.0f} {e['w']:.0f}x{e['h']:.0f})",
                  "Leave the margin genuinely empty - a caption or page number creeping into "
                  "it undoes the grid's whole effect.", box=[e["x"], e["y"], e["w"], e["h"]])

    return data



def _related(a, b, by_eid):
    """True when one element is inside the other. A child sitting on its parent's background
    is the normal case, not a collision."""
    for x, y in ((a, b), (b, a)):
        cur = x.get("parentEid", -1)
        seen = 0
        while cur >= 0 and seen < 64:
            if cur == y["eid"]:
                return True
            cur = by_eid.get(cur, {}).get("parentEid", -1)
            seen += 1
    return False


def _paints_over(a, b):
    """Does a cover b? Later z-index wins; at the same level, later in the document wins."""
    if a["z"] != b["z"]:
        return a["z"] > b["z"]
    return a["eid"] > b["eid"]


def check_overlap(data, cw, ch, rep):
    """Text that something else lands on top of.

    Every other geometry rule here measures one element against the canvas. None of them
    compares two elements to each other, which is why a deck whose headline was covered by a
    panel of feature tiles came back with zero errors and had to be caught by eye. On a page
    built with absolute positioning - how slides are built - this is the most common defect
    there is, and it was the only one nobody was checking.
    """
    els = [e for e in data["elements"] if e["w"] > 2 and e["h"] > 2]
    by_eid = {e["eid"]: e for e in els}
    texts = [e for e in els if e["hasText"]]
    blockers = [e for e in els if e["hasText"] or e.get("opaque")]

    seen = set()
    hits = []
    for t in texts:
        for b in blockers:
            if b["eid"] == t["eid"] or not _paints_over(b, t):
                continue
            if _related(t, b, by_eid):
                continue
            ox = min(t["x"] + t["w"], b["x"] + b["w"]) - max(t["x"], b["x"])
            oy = min(t["y"] + t["h"], b["y"] + b["h"]) - max(t["y"], b["y"])
            if ox < 8 or oy < 8:
                continue
            share = (ox * oy) / max(t["w"] * t["h"], 1)
            if share < 0.10:
                continue
            key = (t["eid"], b["eid"])
            if key in seen:
                continue
            seen.add(key)
            hits.append((t, b, share))

    hits.sort(key=lambda h: -h[2])
    for t, b, share in hits[:6]:
        what = f'"{t["text"]}"'
        over = (f'"{b["text"]}"' if b["hasText"]
                else (os.path.basename(b["src"]) if b["src"] else f'a {b["tag"]} block'))
        why = "later in the document" if b["z"] == t["z"] else "z-index %d" % b["z"]
        rep.error("OVERLAP",
                  f"{what} is covered by {over} ({share * 100:.0f}% of it, {why})",
                  "Two elements are competing for the same space. On slides this usually means "
                  "a block was positioned by a guessed pixel offset - lay the slide out on the "
                  "grid instead, so the content decides where things sit.", box=[t["x"], t["y"], t["w"], t["h"]])


def check_scaled_boxes(data, rep):
    """transform: scale() paints big and lays out small.

    CSS positions with the layout box, so `right: var(--margin)` on a scaled element puts the
    UNSCALED edge at the margin and lets the painted edge run past it. On a 1920px slide, where
    every fixed-size component has to be enlarged, this put ten items over the margin at once.

    `zoom` scales the layout box as well, so it is the right tool and is not flagged - even
    though it too makes getBoundingClientRect and offsetWidth disagree. The signal is the
    element's own transform matrix, not the difference between the two boxes.
    """
    for e in data["elements"]:
        m = re.match(r"matrix\(([-\d.]+),\s*([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)", e.get("transform") or "")
        if not m:
            continue
        a, b, c, d = (float(m.group(i)) for i in (1, 2, 3, 4))
        sx = (a * a + b * b) ** 0.5
        sy = (c * c + d * d) ** 0.5
        if abs(sx - 1) < 0.01 and abs(sy - 1) < 0.01:
            continue
        label = f'"{e["text"]}"' if e["hasText"] else (os.path.basename(e["src"]) or e["tag"])
        rep.warn("SCALED_BOX",
                 f"{label} is scaled {sx:.2f}x by a transform, so it paints "
                 f"{e['w']:.0f}x{e['h']:.0f} while CSS lays it out as "
                 f"{e.get('layoutW', 0):.0f}x{e.get('layoutH', 0):.0f}",
                 "Margins and neighbours are positioned from the layout box, so the painted "
                 "edge can cross the margin with nothing in the CSS to show it. To enlarge a "
                 "fixed-size component use `zoom`, which scales the layout box too.")


def _lum(rgb):
    def ch(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def _ratio(a, b):
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


CONTRAST_HINT = ("Sampled from the render, so this accounts for gradients and panels, not just "
                 "the declared colours. The LG palette has enough range to fix it: Warm Gray 01 "
                 "or 02 on light grounds, 06 or 07 on dark. Not a guideline rule - ours.")


def check_text_contrast(shot, data, rep):
    """Is the type actually readable on what ended up behind it?

    check_ground already samples the pixels under the LOGO. Nothing sampled the pixels under
    the TEXT, so a warm-grey caption on a warm-grey panel, or a dark-slide palette invented by
    whoever built the page, passed silently. WCAG's thresholds are used because the guideline
    gives none - this is our rule, not LG's, and the report says so.
    """
    try:
        from PIL import Image
    except ImportError:
        return
    try:
        im = Image.open(shot).convert("RGB")
    except Exception:
        return
    sx, sy = im.width / max(data["canvas"]["w"], 1), im.height / max(data["canvas"]["h"], 1)

    for e in data["elements"]:
        if not e["hasText"] or e["w"] < 12 or e["h"] < 8:
            continue
        m = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?", e.get("color", ""))
        if not m:
            continue
        if m.group(4) is not None and float(m.group(4)) < 0.5:
            continue          # nearly transparent text is a design choice, not a contrast bug
        fg = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
        box = (max(0, int(e["x"] * sx)), max(0, int(e["y"] * sy)),
               min(im.width, int((e["x"] + e["w"]) * sx)), min(im.height, int((e["y"] + e["h"]) * sy)))
        if box[2] - box[0] < 4 or box[3] - box[1] < 4:
            continue
        # If the element is its own coloured box - a button, a badge, a filled cell - then
        # its background IS the ground, and sampling around it reads the page behind the
        # button instead. That put white-on-red at 1.2:1 by comparing white to white.
        own = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?", e.get("bg", "") or "")
        if own and (own.group(4) is None or float(own.group(4)) > 0.5):
            bg = (int(own.group(1)), int(own.group(2)), int(own.group(3)))
            r = _ratio(fg, bg)
            size = float(re.sub(r"[^\d.]", "", e.get("size", "16") or "16") or 16)
            heavy = e.get("weight", "400") in ("600", "700", "800", "900", "bold", "bolder")
            large = size >= 24 or (size >= 18.66 and heavy)
            need, floor = (3.0, 2.0) if large else (4.5, 3.0)
            if r < need:
                msg = (f'"{e["text"]}" reads at {r:.1f}:1 on its own background '
                       f'(needs {need:.1f}:1 at {size:.0f}px)')
                (rep.error if r < floor else rep.warn)("TEXT_CONTRAST", msg, CONTRAST_HINT,
                                                      box=[e["x"], e["y"], e["w"], e["h"]])
            continue

        # The ground behind the glyphs is best read from just OUTSIDE the text box. Sampling
        # inside it means competing with the glyphs themselves: at 96px the type covers more
        # of its own box than the background does and scores a perfect 1.0:1 against itself,
        # and at 20px the antialiased edge pixels win the count instead.
        pad = 4
        ring = (max(0, box[0] - pad), max(0, box[1] - pad),
                min(im.width, box[2] + pad), min(im.height, box[3] + pad))
        outer = im.crop(ring).quantize(colors=16).convert("RGB")
        inner_box = (box[0] - ring[0], box[1] - ring[1],
                     box[2] - ring[0], box[3] - ring[1])
        counts = {}
        for px in range(outer.width):
            for py in range(outer.height):
                if inner_box[0] <= px < inner_box[2] and inner_box[1] <= py < inner_box[3]:
                    continue
                cpx = outer.getpixel((px, py))
                counts[cpx] = counts.get(cpx, 0) + 1
        if not counts:
            continue
        bg = max(counts.items(), key=lambda kv: kv[1])[0]
        r = _ratio(fg, bg)

        size = float(re.sub(r"[^\d.]", "", e.get("size", "16") or "16") or 16)
        heavy = e.get("weight", "400") in ("600", "700", "800", "900", "bold", "bolder")
        large = size >= 24 or (size >= 18.66 and heavy)
        need, floor = (3.0, 2.0) if large else (4.5, 3.0)
        if r >= need:
            continue
        msg = (f'"{e["text"]}" reads at {r:.1f}:1 against what is behind it '
               f'(needs {need:.1f}:1 at {size:.0f}px)')
        (rep.error if r < floor else rep.warn)("TEXT_CONTRAST", msg, CONTRAST_HINT,
                                              box=[e["x"], e["y"], e["w"], e["h"]])

def check_ground(shot, logos, cw, ch, rep):
    """Sample the rendered pixels under each logo.

    Markup cannot tell you that a Heritage Red symbol landed on a red part of a gradient -
    a named prohibition - or that a white logotype ended up on a pale background. Because
    the box here is measured rather than assumed, this works on any layout, not only ones
    built from templates/.
    """
    try:
        from PIL import Image
        import numpy as np
    except ImportError:
        rep.warn("GROUND_NO_PIL", "Pillow/numpy missing - cannot check what the logo sits on")
        return
    im = Image.open(shot).convert("RGB")
    sx, sy = im.width / cw, im.height / ch
    for e in logos:
        pad = min(e["w"], e["h"]) * 0.15
        box = (max(0, int((e["x"] - pad) * sx)), max(0, int((e["y"] - pad) * sy)),
               min(im.width, int((e["x"] + e["w"] + pad) * sx)),
               min(im.height, int((e["y"] + e["h"] + pad) * sy)))
        if box[2] <= box[0] or box[3] <= box[1]:
            continue
        a = np.asarray(im.crop(box)).astype(float)
        r, g, b = a[..., 0].mean(), a[..., 1].mean(), a[..., 2].mean()
        lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
        redness = r - (g + b) / 2
        src = e["src"]
        light_mark = bool(re.search(r"Mono_White|HeritageRed_White", src))
        dark_mark = bool(re.search(r"Mono_Black|HeritageRed_Grey", src))
        red_symbol = bool(re.search(r"HeritageRed", src))
        rep.info("LOGO_GROUND", f"under the logo: luminance {lum:.0f}/255, redness {redness:+.0f}")
        if red_symbol and redness > 45 and lum > 60:
            rep.error("LOGO_RED_ON_RED",
                      f"the Heritage Red symbol is on a red ground (redness {redness:+.0f})",
                      "Logo Don't #14. Use a white lockup, or move the logo onto a dark or "
                      "neutral part of the image.")
        if light_mark and lum > 140:
            rep.error("LOGO_LOW_CONTRAST",
                      f"a white logotype on a light ground (luminance {lum:.0f})",
                      "Switch to HeritageRed+Grey or the black mono variant.")
        if dark_mark and lum < 90:
            rep.error("LOGO_LOW_CONTRAST",
                      f"a dark logotype on a dark ground (luminance {lum:.0f})",
                      "Switch to a white logotype variant.")
        # Busyness has to be measured on the ground AROUND the mark, not on a crop that
        # contains it: a white logotype on a dark slide is high-variance by construction, so
        # the old version warned on exactly the pairing the guideline recommends.
        inner = (int((e["x"]) * sx) - box[0], int((e["y"]) * sy) - box[1],
                 int((e["x"] + e["w"]) * sx) - box[0], int((e["y"] + e["h"]) * sy) - box[1])
        ring = a.copy()
        y0, y1 = max(0, inner[1]), min(ring.shape[0], inner[3])
        x0, x1 = max(0, inner[0]), min(ring.shape[1], inner[2])
        mask = np.ones(ring.shape[:2], bool)
        if y1 > y0 and x1 > x0:
            mask[y0:y1, x0:x1] = False
        if mask.sum() > 32 and ring[mask].std(axis=0).mean() > 70:
            rep.warn("LOGO_BUSY_GROUND",
                     "the ground around the logo is visually busy",
                     "The guideline prohibits placing the logo on a busy background. Move it "
                     "onto a calm area, or put the logo on a flat panel.")


def classify_position(e, cw, ch, margin):
    tol = max(4.0, margin * 0.25)
    left = abs(e["x"] - margin) <= tol
    right = abs((e["x"] + e["w"]) - (cw - margin)) <= tol
    centre = abs((e["x"] + e["w"] / 2) - cw / 2) <= tol
    top = abs(e["y"] - margin) <= tol
    middle = abs((e["y"] + e["h"] / 2) - ch / 2) <= tol
    bottom = abs((e["y"] + e["h"]) - (ch - margin)) <= tol
    if top and left:
        return "upper-left"
    if top and centre:
        return "upper-center"
    if top and right:
        return "upper-right"
    if middle and left:
        return "middle-left"
    if bottom and left:
        return "bottom-left"
    return None


def is_signoff(e, cw, ch, margin):
    """A sign-off sits in a corner. A lead message is scaled across the grid."""
    return e["w"] < cw * 0.5


def box_gap(a, b):
    dx = max(0, max(a["x"], b["x"]) - min(a["x"] + a["w"], b["x"] + b["w"]))
    dy = max(0, max(a["y"], b["y"]) - min(a["y"] + a["h"], b["y"] + b["h"]))
    return (dx ** 2 + dy ** 2) ** 0.5


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target")
    ap.add_argument("--canvas", required=True, help="e.g. 1080x1350 or 420x594mm")
    ap.add_argument("--web", action="store_true", help="LG.com component: web palette, no logo expected")
    ap.add_argument("--shot", help="write a render to this path")
    ap.add_argument("--json", help="write the measurements to this path")
    args = ap.parse_args()

    canvas = parse_canvas(args.canvas)
    if not canvas:
        print("could not parse --canvas; expected e.g. 1080x1350 or 420x594mm", file=sys.stderr)
        return 2

    rep = Report()

    # static checks first - they need no browser and catch broken paths early
    if bc:
        margin_px = 0.05 * min(canvas[0], canvas[1])
        try:
            bc.check_font_urls(args.target, rep)
            text, shipped = bc.load_with_styles(args.target)
            bc.check_colors(shipped, rep, args.web)
            bc.check_gradients(text, rep)
        except Exception as e:
            rep.warn("STATIC_CHECKS_SKIPPED", f"brand_check could not run: {e}")
    else:
        rep.warn("STATIC_CHECKS_SKIPPED", "brand_check.py not importable; colour not checked")

    try:
        data = check_page(args.target, canvas, rep, args.shot, args.web)
    except ImportError:
        print("\nverify.py needs playwright to measure the rendered page.\n"
              "  pip install playwright && playwright install chromium\n"
              "Without it the geometry rules cannot be checked at all - do not treat a run\n"
              "of brand_check.py alone as a passed check.", file=sys.stderr)
        return 2
    except Exception as e:
        # Printing the exception and then dumping the report used to end with
        # "0 error(s), 0 warning(s) - geometry, fonts and assets check out", which is
        # the single most dangerous sentence this file can produce.
        rep.incomplete(f"{type(e).__name__}: {e}")
        return rep.dump(args.target)

    if args.json:
        # Everything a report needs: what was found, where it is, and which screenshot it is
        # on. scripts/report.py turns exactly this into a page a person can forward.
        with open(args.json, "w") as f:
            json.dump({"target": os.path.abspath(args.target),
                       "canvas": args.canvas, "web": bool(args.web),
                       "frames": rep.frames, "rows": rep.rows,
                       "measurements": data}, f, indent=1)

    return rep.dump(args.target)


if __name__ == "__main__":
    sys.exit(main())
