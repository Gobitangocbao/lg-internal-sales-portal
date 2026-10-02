#!/usr/bin/env python3
"""
brand_check.py - the STATIC half of the LG brand check.

Run scripts/verify.py instead for HTML: it calls this file for the static rules and then
measures the rendered page for everything geometric. This file is the right entry point
only for a .pptx, which has no browser rendering to measure.

Scope, deliberately narrow: font-file resolution, colour, gradients, type size, and PPTX
internals. Anything about size, position or what a logo is sitting on belongs to verify.py -
having two implementations of one rule is how a size regression once survived a run that
reported success.

Original description follows.

brand_check.py - lint an LG-branded deliverable against the BI guideline.

    python3 scripts/brand_check.py <file.html|file.pptx|file.svg|directory> [--web] [--canvas WxH]

--web       judge colours against the LG.com palette (Active Red #EA1917) instead of the BI palette
--canvas    canvas size in px or mm, e.g. 1920x1080, so grid-derived checks can run

This is a linter, not a reviewer. It catches the mechanical failures - wrong hex, wrong font
family, logo geometry, missing assets. It cannot see whether the composition works. Always look at
the rendered output too.

Exit code 0 = no errors (warnings may still be present), 1 = at least one error.
"""
import argparse
import hashlib
import os
import re
import sys
import zipfile

# ---------------------------------------------------------------- palettes

BI = {
    "#FD312E": "LG Active Red", "#A50034": "LG Red (Heritage)",
    "#FFFFFF": "White", "#000000": "Black",
    "#262626": "Warm Gray 01", "#4A4946": "Warm Gray 02", "#716F6A": "Warm Gray 03",
    "#CBC8C2": "Warm Gray 04", "#E6E1D6": "Warm Gray 05", "#F0ECE4": "Warm Gray 06",
    "#F6F3EB": "Warm Gray 07",
}
WEB_EXTRA = {
    "#EA1917": "Active Red (web)", "#646464": "Mid Gray 2", "#333333": "Dark Gray 1",
    "#1A1A1A": "Dark Gray 3", "#F7B500": "Yellow Review", "#DEAD25": "Yellow Toast",
    "#287D00": "Green (Validation)", "#316D15": "Tree Green", "#076369": "Blue Green (Toast)",
}
AI_GRADIENT = {
    "#FD2F3F", "#FD2E43", "#FD297A", "#FF21D3", "#FE21D1",
    "#F914EB", "#E51DEE", "#B446FF", "#8227FF", "#B945FF", "#FF1EFF",
}
LG_FAMILIES = {
    "lg ei headline", "lg ei text",
    "lg ei text light", "lg ei text regular", "lg ei text semibold", "lg ei text bold",
}
# fonts people fall back to when LG EI fails to load
SUSPECT_FONTS = {
    "arial", "helvetica", "helvetica neue", "inter", "roboto", "open sans", "lato",
    "calibri", "segoe ui", "times new roman", "montserrat", "poppins", "noto sans",
    "system-ui", "-apple-system", "sans-serif", "lg smart", "lgsmart",
}
LOGO_HINT = re.compile(r"LGE_(2D_LG-Electronics_)?Logo|LGE_Logotype", re.I)
SLOGAN_HINT = re.compile(r"Slogan_(Horizontal|Stacked)", re.I)

# measured symbol height / PNG canvas height, per lockup
SYM_SHARE = {"compact": 0.668, "wide": 0.671}
SLOGAN_INK_SHARE = 0.669   # slogan ink height / PNG canvas height
LOGO_SYMBOL_X = 1.30       # BI p.77 - symbol height as a multiple of the margin
SLOGAN_INK_X = 0.90        # BI p.78 - visible slogan height
MIN_LOGO_PX = 16           # guideline minimum logo height (4mm / 16px)
SMALL_SIZE_PX = 60         # below this width, use the Small-Size artwork


def asset_hashes():
    """sha256 -> filename for every shipped logo/slogan/gradient asset, so we can prove a
    deliverable embeds the real artwork rather than a re-saved copy of it."""
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
    out = {}
    for sub in ("logo", "slogan", "gradients", "lg-ai"):
        d = os.path.join(root, sub)
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            p = os.path.join(d, f)
            if os.path.isfile(p):
                out[hashlib.sha256(open(p, "rb").read()).hexdigest()] = f
    return out


class Report:
    def __init__(self):
        self.rows = []

    def add(self, level, code, msg, hint=""):
        self.rows.append((level, code, msg, hint))

    def error(self, *a):
        self.add("ERROR", *a)

    def warn(self, *a):
        self.add("WARN", *a)

    def info(self, *a):
        self.add("INFO", *a)

    def dump(self, target):
        order = {"ERROR": 0, "WARN": 1, "INFO": 2}
        self.rows.sort(key=lambda r: order[r[0]])
        errs = sum(1 for r in self.rows if r[0] == "ERROR")
        warns = sum(1 for r in self.rows if r[0] == "WARN")
        print(f"\nlg-brand check - {target}")
        print("=" * 72)
        if not self.rows:
            print("  nothing flagged.")
        for level, code, msg, hint in self.rows:
            mark = {"ERROR": "x", "WARN": "!", "INFO": "i"}[level]
            print(f"  [{mark}] {code:<22} {msg}")
            if hint:
                print(f"      -> {hint}")
        print("-" * 72)
        print(f"  {errs} error(s), {warns} warning(s)")
        print("  A clean lint is not a passed review - render it and look at it.")
        return 1 if errs else 0


# ---------------------------------------------------------------- helpers

def norm_hex(h):
    h = h.upper().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return "#" + h


def allowed_palette(web):
    p = dict(BI)
    if web:
        p.update(WEB_EXTRA)
    return p


def check_colors(text, rep, web):
    # a hex inside a --custom-property declaration is a token being offered, not a colour
    # being used; what matters is whether the design references it
    text = re.sub(r"--[\w-]+\s*:\s*#[0-9A-Fa-f]{3,6}\s*;", " ", text)
    palette = allowed_palette(web)
    found = {}
    for m in re.finditer(r"#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b", text):
        h = norm_hex(m.group(0))
        found.setdefault(h, 0)
        found[h] += 1
    for h, n in sorted(found.items(), key=lambda kv: -kv[1]):
        if h in palette or h in AI_GRADIENT:
            continue
        if h == "#EA1917" and not web:
            rep.error("COLOR_WEB_RED_OFFWEB",
                      f"{h} used {n}x - that is the LG.com Active Red",
                      "Off-web output uses #FD312E. Re-run with --web if this really is for lge.com.")
        elif h == "#FD312E" and web:
            rep.warn("COLOR_BI_RED_ONWEB",
                     f"{h} used {n}x in a web context",
                     "LG.com specifies Active Red as #EA1917.")
        else:
            rep.warn("COLOR_OFF_PALETTE", f"{h} used {n}x is not in the palette",
                     "Allowed as a content accent, but check it does not evoke a competitor.")
    if not web and "--lg-active-red-web" in text:
        rep.error("COLOR_WEB_RED_OFFWEB",
                  "var(--lg-active-red-web) is referenced in non-web output",
                  "Off-web output uses --lg-active-red (#FD312E).")
    inpal = [h for h in found if h in palette]
    if inpal:
        rep.info("COLOR_OK", f"{len(inpal)} palette colour(s) found: " +
                 ", ".join(f"{h} {palette[h]}" for h in sorted(inpal)[:6]))


def check_fonts(text, rep):
    fams = set()
    for m in re.finditer(r"font-family\s*:\s*([^;}]+)", text, re.I):
        for part in m.group(1).split(","):
            f = part.strip().strip("'\"").lower()
            if f:
                fams.add(f)
    if not fams:
        rep.warn("FONT_NONE", "no font-family declared",
                 "LG EI must be stated explicitly; nothing inherits it.")
        return
    lg = fams & LG_FAMILIES
    if not lg:
        rep.error("FONT_NOT_LG", f"no LG EI family declared (found: {', '.join(sorted(fams))})",
                  'Use "LG EI Headline" for titles and "LG EI Text" for body.')
    bad = fams & SUSPECT_FONTS
    # a generic last-resort fallback is tolerable; a named substitute is not
    hard = bad - {"sans-serif", "system-ui", "-apple-system"}
    if hard:
        rep.error("FONT_SUBSTITUTE", f"non-LG font in the stack: {', '.join(sorted(hard))}",
                  "Remove it. A visible fallback means some text will ship in the wrong typeface.")
    if "lg ei text" in fams and "@font-face" not in text.lower():
        rep.error("FONT_NO_FACE", '"LG EI Text" used with no @font-face block',
                  "LG EI Text weights each declare their own family name, so the unified "
                  '"LG EI Text" family only exists if you create it with @font-face.')
    if re.search(r"font-family\s*:\s*['\"]?LG EI Text['\"]?[^;}]*;\s*[^}]*font-weight\s*:\s*(bold|[6-9]00)",
                 text, re.I) and "@font-face" not in text.lower():
        rep.error("FONT_FAUX_BOLD", "bold weight on LG EI Text without @font-face mapping",
                  "This produces faux bold or a substituted font.")
    if "@font-face" in text.lower() and "font-display" not in text.lower():
        rep.warn("FONT_NO_DISPLAY", "@font-face without font-display",
                 "Add font-display:block, or a screenshot/PDF export may capture the fallback font.")


def check_gradients(text, rep):
    # the .lg-grid-overlay helper draws the composing grid with CSS gradients and is
    # removed before export - judging it as brand artwork is a false alarm
    text = re.sub(r"\.lg-grid-overlay[^{]*\{[^}]*\}", " ", text)
    grads = re.findall(r"LGE_Electronics_Gradient_0(\d)_RGB", text)
    if len(set(grads)) > 1:
        rep.error("GRADIENT_TWO", f"more than one master gradient referenced: {sorted(set(grads))}",
                  "Never two gradients in the same piece.")
    if re.search(r"linear-gradient|radial-gradient", text, re.I) and \
       re.search(r"#(FD312E|A50034|EA1917)", text, re.I):
        rep.warn("GRADIENT_CSS", "a CSS gradient is built from brand red",
                 "The four master gradients are fixed artwork - crop and rotate only, never rebuild.")
    if re.search(r"background-clip\s*:\s*text|-webkit-background-clip\s*:\s*text", text, re.I):
        rep.error("GRADIENT_IN_TEXT", "gradient clipped to text",
                  "Gradients are never used inside text.")


def check_web_specifics(text, rep):
    for m in re.finditer(r"font-size\s*:\s*([\d.]+)px", text):
        pass
    if re.search(r"1600\s*[x×]\s*720", text):
        rep.warn("WEB_NARROW_HERO", "1600x720 hero size in use",
                 "The web guide marks Narrow (1600px) as not recommended.")


HEADLINE_SEL = re.compile(r"(h1|h2|h3|\.lg-headline|\.headline|\.title)\b", re.I)


def check_min_pt(text, rep):
    """The 18pt floor is a Headline rule. Body copy in LG EI Text is legitimately smaller -
    the business card sets it at 6.8pt - so only flag rules that style a headline."""
    for m in re.finditer(r"([^{}]+)\{([^}]*)\}", text):
        sel, body = m.group(1), m.group(2)
        if not HEADLINE_SEL.search(sel):
            continue
        for sm in re.finditer(r"font-size\s*:\s*([\d.]+)pt", body):
            v = float(sm.group(1))
            if v < 18:
                rep.warn("TYPE_UNDER_18PT",
                         f"headline rule '{sel.strip()[:40]}' sets {v}pt",
                         "LG EI Headline below 18pt is not recommended.")


# ---------------------------------------------------------------- drivers

COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
# html/body rules only style the preview chrome around the canvas, never the deliverable
CHROME_RE = re.compile(r"\b(?:html\s*,\s*body|body\s*,\s*html|html|body)\s*\{[^}]*\}")


def load_with_styles(path):
    """Read a file plus any local stylesheet it links, and drop comments and preview chrome.

    Comments matter: these templates carry long explanatory notes that mention asset
    filenames and sizes. Scanning them produces confident, wrong findings - the checker
    once reported a white logo on a light ground because a comment mentioned the white
    variant. Only what actually ships is checked.
    """
    raw = open(path, "r", encoding="utf-8", errors="replace").read()
    text = COMMENT_RE.sub(" ", raw)
    base = os.path.dirname(os.path.abspath(path))
    for href in re.findall(r'<link[^>]+href="([^"]+)"', text):
        if href.startswith(("http://", "https://", "//")):
            continue
        p2 = os.path.join(base, href)
        if os.path.isfile(p2):
            text += "\n/* linked: %s */\n" % href + \
                    COMMENT_RE.sub(" ", open(p2, encoding="utf-8", errors="replace").read())
    return text, CHROME_RE.sub(" ", text)


def check_font_urls(path, rep):
    """Verify every @font-face url() actually resolves on disk.

    This is the check that matters most. When a font URL is wrong the page still renders -
    the browser silently substitutes a system font and the result looks plausible at a
    glance, especially in a screenshot. Nothing in the markup is wrong, so every other
    static check passes. Resolving the paths is the only cheap way to catch it.

    The usual cause: lg-tokens.css writes url("../assets/fonts/...") because it lives in
    templates/. Copy it somewhere else without moving assets/ and every face 404s.
    """
    base = os.path.dirname(os.path.abspath(path))
    files = [(path, base)]
    raw = open(path, encoding="utf-8", errors="replace").read()
    for href in re.findall(r'<link[^>]+href="([^"]+)"', raw):
        if href.startswith(("http://", "https://", "//")):
            continue
        p2 = os.path.join(base, href)
        if os.path.isfile(p2):
            files.append((p2, os.path.dirname(p2)))

    seen = missing = 0
    for f, d in files:
        try:
            body = open(f, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        for block in re.findall(r"@font-face\s*\{[^}]*\}", body):
            for url in re.findall(r'url\(\s*["\']?([^"\')]+)', block):
                if url.startswith(("http", "data:")):
                    continue
                seen += 1
                if not os.path.isfile(os.path.join(d, url)):
                    missing += 1
                    rep.error("FONT_URL_MISSING",
                              f"@font-face url does not resolve: {url}",
                              f"Relative to {os.path.relpath(d) or '.'}. The page will render "
                              "in a substituted system font that looks fine in a screenshot.")
    if seen and not missing:
        rep.info("FONT_URLS_OK", f"all {seen} @font-face file(s) resolve on disk")
    elif not seen and re.search(r'font-family\s*:\s*["\']?LG EI', raw, re.I):
        rep.warn("FONT_NO_FACE_ANYWHERE", "LG EI is used but no @font-face was found",
                 "Link lg-tokens.css, or declare the faces - LG EI is not a system font.")


def check_text_file(path, rep, web, margin_px=None):
    check_font_urls(path, rep)
    text, shipped = load_with_styles(path)
    check_colors(shipped, rep, web)
    check_fonts(text, rep)
    check_gradients(text, rep)
    check_min_pt(text, rep)
    if web:
        check_web_specifics(text, rep)


def check_pptx(path, rep, web, margin_px):
    z = zipfile.ZipFile(path)
    blob = []
    for n in z.namelist():
        if n.endswith(".xml") or n.endswith(".rels"):
            blob.append(z.read(n).decode("utf-8", "replace"))
    text = "\n".join(blob)

    # theme colours + fonts
    theme = next((z.read(n).decode("utf-8", "replace")
                  for n in z.namelist() if "theme" in n and n.endswith(".xml")), "")
    if theme:
        typefaces = set(t.lower() for t in re.findall(r'<a:latin typeface="([^"]*)"', theme) if t)
        if typefaces and not any("lg ei" in t for t in typefaces):
            rep.error("PPTX_THEME_FONT",
                      f"theme fonts are {', '.join(sorted(typefaces))} - not LG EI",
                      "The bundled LG templates ship the default Office theme. Build the theme "
                      "properly with templates/build_pptx.py.")
        # Matching one magic hex only catches one Office version - the 2007 default is
        # 4F81BD, the modern one 4472C4. Judge the whole scheme against the palette instead.
        scheme = re.search(r"<a:clrScheme.*?</a:clrScheme>", theme, re.S)
        if scheme:
            allowed = set(allowed_palette(web)) | AI_GRADIENT | {"#FFFFFF", "#000000"}
            stray = sorted({norm_hex(c) for c in
                            re.findall(r'srgbClr val="([0-9A-Fa-f]{6})"', scheme.group(0))}
                           - allowed)
            if stray:
                rep.error("PPTX_THEME_OFFICE",
                          f"the theme colour scheme is not the LG palette: {', '.join(stray[:6])}",
                          "Every new shape and text box inherits these. Build the deck with "
                          "templates/build_pptx.py, which rewrites the theme part.")

    slide_xml = "\n".join(z.read(n).decode("utf-8", "replace")
                          for n in z.namelist() if n.startswith("ppt/slides/slide"))
    authored = {m.group(1) for m in re.finditer(r'<a:latin typeface="([^"]+)"', slide_xml)}
    bad = {f for f in authored if f.lower() in SUSPECT_FONTS}
    if bad:
        rep.error("PPTX_FONT_SUBSTITUTE",
                  f"non-LG typeface on authored text: {', '.join(sorted(bad))}",
                  "Set the exact LG EI family string on every run.")
    lg = {f for f in authored if "lg ei" in f.lower()}
    if lg:
        rep.info("PPTX_FONT_OK", f"LG EI families in use: {', '.join(sorted(lg))}")
    elif authored:
        rep.error("PPTX_FONT_NOT_LG", f"authored text uses {', '.join(sorted(authored))}",
                  "Every run needs an explicit LG EI family name.")
    latent = {m.group(1) for m in re.finditer(r'<a:latin typeface="([^"]+)"', text)} - authored
    stale = {f for f in latent if f.lower() in SUSPECT_FONTS}
    if stale:
        rep.warn("PPTX_LATENT_DEFAULTS",
                 f"non-LG fonts remain in latent/default styles: {', '.join(sorted(stale))}",
                 "Harmless for existing text, but a new text box inherits them. "
                 "build_pptx.py scrubs these.")

    colors = {norm_hex(c) for c in re.findall(r'srgbClr val="([0-9A-Fa-f]{6})"', text)}
    palette = set(allowed_palette(web)) | AI_GRADIENT
    off = sorted(colors - palette)
    if off:
        rep.warn("PPTX_OFF_PALETTE", f"{len(off)} off-palette colour(s): {', '.join(off[:8])}")

    media = [n for n in z.namelist() if n.startswith("ppt/media/")]
    known = asset_hashes()
    matched = {}
    unknown = 0
    for n in media:
        h = hashlib.sha256(z.read(n)).hexdigest()
        if h in known:
            matched[known[h]] = n
        else:
            unknown += 1
    logos = [f for f in matched if LOGO_HINT.search(f)]
    slogans = [f for f in matched if SLOGAN_HINT.search(f)]
    if not logos:
        rep.error("PPTX_LOGO_NOT_OFFICIAL",
                  "no embedded image is byte-identical to a shipped LG logo asset",
                  "Insert assets/logo/*.png directly. A re-exported, re-saved or "
                  "screenshotted logo is a redraw as far as the review is concerned.")
    else:
        rep.info("PPTX_LOGO_OK", f"official logo artwork found: {', '.join(sorted(logos))}")
    if slogans:
        rep.info("PPTX_SLOGAN_OK", f"official slogan artwork found: {', '.join(sorted(slogans))}")
    if len(slogans) > 1:
        rep.error("PPTX_SLOGAN_REPEATED", "more than one slogan asset embedded",
                  "The slogan appears at most once per application.")
    rep.info("PPTX_MEDIA", f"{len(media)} media file(s), {unknown} not from the LG asset pack")

    if "embeddedFont" not in text:
        rep.warn("PPTX_FONTS_NOT_EMBEDDED", "fonts are not embedded in the deck",
                 "Save with font embedding on, or LG EI substitutes on other machines.")


def parse_canvas(s):
    if not s:
        return None
    m = re.match(r"^\s*([\d.]+)\s*[x×]\s*([\d.]+)\s*$", s)
    if not m:
        print(f"could not parse --canvas {s!r}; expected e.g. 1920x1080", file=sys.stderr)
        return None
    w, h = float(m.group(1)), float(m.group(2))
    return 0.05 * min(w, h)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target")
    ap.add_argument("--web", action="store_true",
                    help="judge against the LG.com palette (Active Red #EA1917)")
    ap.add_argument("--canvas", help="canvas size, e.g. 1920x1080, to enable grid checks")
    ap.add_argument("--render", help="a rendered PNG of the same file, to check the logo's "
                                     "actual background instead of only the markup")
    args = ap.parse_args()

    margin = parse_canvas(args.canvas)
    rep = Report()

    targets = []
    if os.path.isdir(args.target):
        for root, _, files in os.walk(args.target):
            for f in files:
                if f.lower().endswith((".html", ".htm", ".css", ".svg", ".pptx")):
                    targets.append(os.path.join(root, f))
    else:
        targets = [args.target]

    if not targets:
        print("no checkable files found (html, css, svg, pptx)")
        return 0

    for t in targets:
        if t.lower().endswith(".pptx"):
            check_pptx(t, rep, args.web, margin)
        else:
            check_text_file(t, rep, args.web, margin)

    if args.render:
        wh = None
        if args.canvas:
            mm = re.match(r"^\s*([\d.]+)\s*[x\u00d7]\s*([\d.]+)\s*$", args.canvas)
            if mm:
                wh = (float(mm.group(1)), float(mm.group(2)))
        html = ""
        for t in targets:
            if t.lower().endswith((".html", ".htm")):
                html = load_with_styles(t)[0]
                break
        check_render(args.render, html, rep, wh)

    return rep.dump(args.target)


if __name__ == "__main__":
    sys.exit(main())
