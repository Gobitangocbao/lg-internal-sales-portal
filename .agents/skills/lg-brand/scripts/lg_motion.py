#!/usr/bin/env python3
"""
lg_motion.py - pick an animated component in LG's own motion language.

    python3 scripts/lg_motion.py search "so sánh sell-out giữa các kênh"
    python3 scripts/lg_motion.py get bars-compare
    python3 scripts/lg_motion.py get bars-compare --no-base   # base CSS already on the page
    python3 scripts/lg_motion.py list --family connected

The point of the search-then-get flow is token cost. `components.json` holds every component's
code and `gallery.html` is a rendered page of all of them; reading either with a file tool
spends thousands of tokens to find one snippet. Search returns a handful of one-line matches,
get returns exactly one component. Read `CATALOG.md` (4 KB) if Python is unavailable, then get
the id you chose - but never read components.json or gallery.html.

The kit is built from scripts/build_motion.py. Edit components there and rebuild; editing the
generated files directly puts the catalogue and the code out of step.

Motion here follows the three families the guideline names for EI Form Motion (p.103-105):
adaptive (arrive in order), connected (draw the relationship), fluid (continuous, sparing).
Durations and easing are not specified in the source - the values used are a reading of
"warm, unhurried, restrained", documented in references/motion.md.
"""
import argparse
import json
import os
import re
import sys
import unicodedata

# Product and feature names that must never appear in a component's sample content.
PRODUCT_NAMES = (r"WashTower", r"TurboWash", r"AI\s?DD", r"ThinQ", r"Heat\s?Pump",
                 r"Center\s?Control", r"Smart\s?Pairing", r"OLED", r"InstaView",
                 r"Styler", r"PuriCare", r"gram\b", r"WT\d{4}")

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(os.path.dirname(HERE), "assets", "lg-motion")


def load(name):
    p = os.path.join(KIT, name)
    if not os.path.isfile(p):
        sys.exit(f"{name} is missing. Run: python3 scripts/build_motion.py")
    return json.load(open(p, encoding="utf-8"))


def fold(s):
    """Strip Vietnamese diacritics so 'kenh' finds 'kênh'. People type both."""
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.replace("đ", "d")


def score(entry, terms):
    hay_fields = [(fold(entry["id"]), 6), (fold(entry["name"]), 4),
                  (fold(entry["use"]), 3), (fold(" ".join(entry["tags"])), 5),
                  (fold(entry["cat"] + " " + entry["family"]), 2)]
    total = 0
    for t in terms:
        for hay, w in hay_fields:
            if t in hay:
                total += w
                break
    return total


def cmd_search(a):
    index = load("index.json")
    terms = [fold(t) for t in re.split(r"\s+", a.query) if len(t) > 1]
    if a.family:
        index = [e for e in index if e["family"] == a.family]
    ranked = sorted(((score(e, terms), e) for e in index),
                    key=lambda p: (-p[0], p[1]["pri"], p[1]["id"]))
    hits = [(s, e) for s, e in ranked if s > 0][:a.n]
    if not hits:
        print(f"Nothing matched \"{a.query}\".\n"
              f"There are only {len(index)} components - `list` shows all of them, and "
              f"CATALOG.md is 4 KB.\n"
              f"If nothing fits, write the component yourself following references/motion.md, "
              f"then add it to scripts/build_motion.py so the next person finds it.")
        return 1
    for s, e in hits:
        print(f"{e['id']:<16} {e['family']:<10} {e['size']:<9} {e['use']}")
        print(f"{'':<16} tags: {', '.join(e['tags'][:8])}")
    print(f"\nget one with:  python3 scripts/lg_motion.py get {hits[0][1]['id']}")
    return 0


def cmd_list(a):
    index = load("index.json")
    if a.family:
        index = [e for e in index if e["family"] == a.family]
    if a.cat:
        index = [e for e in index if e["cat"] == a.cat]
    for e in sorted(index, key=lambda x: (x["cat"], x["id"])):
        print(f"{e['id']:<16} {e['cat']:<9} {e['family']:<10} {e['size']:<9} {e['use']}")
    print(f"\n{len(index)} component(s)")
    return 0


def cmd_get(a):
    store = load("components.json")
    c = store["components"].get(a.id)
    if not c:
        near = [k for k in store["components"] if fold(a.id) in fold(k)]
        sys.exit(f"No component '{a.id}'." + (f" Did you mean: {', '.join(near)}?" if near
                                              else " Run `search` or `list`."))
    print(f"<!-- lg-motion: {c['id']} ({c['family']}, {c['size']}) - {c['use']} -->")
    if not a.no_base:
        print("<style>/* lg-motion base - paste once per page */")
        print(store["base_css"])
        print("</style>")
    if c["css"]:
        print(f"<style>/* {c['id']} */")
        print(c["css"])
        print("</style>")
    print(c["html"])
    if a.id == "product-frame":
        print("<!-- note: a plain panel, NOT an EI form. EI forms are fixed artwork this "
              "skill does not ship. -->")
    return 0


def cmd_doctor(a):
    """Catch the ways this kit could quietly stop being LG."""
    store = load("components.json")
    index = load("index.json")
    problems = []

    allowed = {"#FD312E", "#A50034", "#262626", "#4A4946", "#716F6A",
               "#CBC8C2", "#E6E1D6", "#F0ECE4", "#F6F3EB", "#FFF", "#FFFFFF", "#000", "#000000"}
    for cid, c in store["components"].items():
        blob = c["css"] + c["html"]
        for hexv in set(re.findall(r"#[0-9A-Fa-f]{3,6}\b", blob)):
            if hexv.upper() not in allowed:
                problems.append(f"{cid}: off-palette colour {hexv}")
        # An rgba() with an alpha is the natural way to write a faint guide line, and it walks
        # straight past a hex check - so the same palette applies to it, on the RGB triple.
        allowed_rgb = {tuple(int(h.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
                       for h in allowed if len(h) == 7}
        for r, g, bl in set(re.findall(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", blob)):
            if (int(r), int(g), int(bl)) not in allowed_rgb:
                problems.append(f"{cid}: off-palette colour rgb({r},{g},{bl})")
        if re.search(r"LGE_Logo|LGE_2D_LG-Electronics|Slogan_(Horizontal|Stacked)", blob):
            problems.append(f"{cid}: references a brand logo or slogan asset - these are never "
                            f"animated by us; only Digital Logo Play is an official animated mark")
        if re.search(r"Gradient_0\d", blob):
            problems.append(f"{cid}: references a master gradient - they may not be altered, "
                            f"and animating one counts as altering it")
        if re.search(r"linear-gradient|radial-gradient", blob):
            problems.append(f"{cid}: builds a CSS gradient - the four masters are fixed artwork "
                            f"and new gradients may not be created")
        if not re.search(r"\.lgm-", c["css"]) and c["css"]:
            problems.append(f"{cid}: CSS is not prefixed .lgm- so it can collide when pasted")
        if c["family"] not in ("adaptive", "connected", "fluid"):
            problems.append(f"{cid}: family '{c['family']}' is not one of LG's three")
        # The kit was written straight after a WashTower poster, so its placeholders said
        # "14 kg giặt" and "TurboWash 360". That flatters a WashTower demo and misleads anyone
        # building for a TV - and the real risk is somebody shipping a slide with a model name
        # they never meant to put on it. Placeholders stay generic.
        for name in PRODUCT_NAMES:
            if re.search(name, c["html"], re.I):
                problems.append(f"{cid}: placeholder names a specific product or feature "
                                f"('{name}') - keep sample content generic so nobody ships it "
                                f"by accident")

    if "prefers-reduced-motion" not in store["base_css"]:
        problems.append("base CSS has no prefers-reduced-motion guard")
    # Half of any "high-tech" deck is dark slides. Without a dark block here every agent
    # invents its own overrides, which is how unreadable grey-on-grey got shipped once.
    if ".lg-dark .lgm" not in store["base_css"]:
        problems.append("base CSS has no dark-ground block - .lg-dark .lgm / .lgm--dark")
    dark = store["base_css"][store["base_css"].find(".lg-dark .lgm"):][:400]
    if "#716F6A" in dark and "--lgm-mute:#716F6A" in dark:
        problems.append("dark block uses Warm Gray 03 as muted text - 3.0:1 on #262626")
    ids_store, ids_index = set(store["components"]), {e["id"] for e in index}
    if ids_store != ids_index:
        problems.append(f"index and components disagree: {ids_store ^ ids_index}")

    for p in problems:
        print(f"  [x] {p}")
    print(f"\n  {len(store['components'])} components, {len(problems)} problem(s)")
    return 1 if problems else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("search", help="find a component by describing the job")
    p.add_argument("query")
    p.add_argument("-n", type=int, default=5)
    p.add_argument("--family", choices=("adaptive", "connected", "fluid"))
    p.set_defaults(fn=cmd_search)

    p = sub.add_parser("list", help="list everything")
    p.add_argument("--family", choices=("adaptive", "connected", "fluid"))
    p.add_argument("--cat")
    p.set_defaults(fn=cmd_list)

    p = sub.add_parser("get", help="print one component, ready to paste")
    p.add_argument("id")
    p.add_argument("--no-base", action="store_true",
                   help="skip the base CSS when it is already on the page")
    p.set_defaults(fn=cmd_get)

    p = sub.add_parser("doctor", help="check the kit is still on-brand and internally consistent")
    p.set_defaults(fn=cmd_doctor)

    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
