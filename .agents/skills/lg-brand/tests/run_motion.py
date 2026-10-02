#!/usr/bin/env python3
"""
run_motion.py - the lane for the lg-motion kit.

    python3 tests/run_motion.py

verify.py measures a finished page. This lane checks the thing that produces the pieces of
that page: the nineteen animated components and the CLI an agent uses to find one.

Three failure modes it exists to catch, all of which are quiet:

  - the kit drifts off-brand, one plausible-looking hex at a time
  - the generated catalogue and the code fall out of step, so search describes a component
    that no longer works that way
  - search stops finding things, and the agent writes its own animation instead - which is
    how a kit built to keep motion consistent ends up doing the opposite
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
KIT = os.path.join(ROOT, "assets", "lg-motion")
CLI = os.path.join(ROOT, "scripts", "lg_motion.py")
BUILD = os.path.join(ROOT, "scripts", "build_motion.py")

# What someone actually types, in the two spellings Vietnamese arrives in. If a phrase this
# ordinary returns nothing, the kit is unreachable no matter how good the components are.
QUERIES = [
    ("so sánh doanh số giữa các kênh", "bars-compare"),
    ("so sanh doanh so giua cac kenh", "bars-compare"),
    ("xu hướng thị phần theo tháng", "line-trend"),
    ("một con số lớn cho slide mở đầu", "counter-hero"),
    ("quy trình các bước triển khai", "steps-flow"),
    ("thông số sản phẩm", "spec-rows"),
    ("timeline lộ trình theo quý", "timeline-track"),
    ("loading state", "loading-dots"),
]


def run(*args):
    return subprocess.run([sys.executable, CLI] + list(args), capture_output=True, text=True)


def digest():
    h = hashlib.sha256()
    for name in sorted(("components.json", "index.json", "CATALOG.md", "gallery.html")):
        p = os.path.join(KIT, name)
        h.update(open(p, "rb").read() if os.path.isfile(p) else b"")
    return h.hexdigest()


def check_doctor():
    p = run("doctor")
    if p.returncode == 0:
        return []
    return [l.strip() for l in (p.stdout + p.stderr).splitlines() if "[x]" in l] or \
           [f"doctor exited {p.returncode}"]


def check_build_in_step():
    """The generated files must be what build_motion.py produces right now. Editing
    components.json by hand is easy, tempting, and leaves the catalogue lying."""
    before = digest()
    p = subprocess.run([sys.executable, BUILD], capture_output=True, text=True)
    if p.returncode != 0:
        return [f"build_motion.py failed: {(p.stderr or p.stdout).strip()[-160:]}"]
    if digest() != before:
        return ["the generated kit differs from what build_motion.py produces - someone edited "
                "components.json, index.json, CATALOG.md or gallery.html directly"]
    return []


def check_every_component_gets():
    store = json.load(open(os.path.join(KIT, "components.json"), encoding="utf-8"))
    bad = []
    for cid in store["components"]:
        p = run("get", cid, "--no-base")
        if p.returncode != 0 or "<" not in p.stdout:
            bad.append(f"get {cid} produced nothing usable")
    return bad


def check_catalog_matches():
    store = json.load(open(os.path.join(KIT, "components.json"), encoding="utf-8"))
    cat = open(os.path.join(KIT, "CATALOG.md"), encoding="utf-8").read()
    missing = [c for c in store["components"] if c not in cat]
    return [f"CATALOG.md does not list: {', '.join(missing)}"] if missing else []


def check_search_finds():
    bad = []
    for q, want in QUERIES:
        p = run("search", q, "-n", "5")
        if p.returncode != 0:
            bad.append(f"\"{q}\" -> nothing at all")
        elif want not in p.stdout:
            top = (p.stdout.splitlines() or ["?"])[0].split()[0]
            bad.append(f"\"{q}\" -> expected {want} in the results, got {top} and others")
    return bad


def check_kit_size():
    """search/get exist because the store is too big to read. If it ever got small enough to
    read directly, this guidance would be wrong - and if it grows past a few hundred KB, a
    stray Read of it becomes expensive enough to matter."""
    n = os.path.getsize(os.path.join(KIT, "components.json"))
    return [f"components.json is {n/1024:.0f} KB - past 300 KB, revisit the CLI guidance"] \
        if n > 300 * 1024 else []


def check_components_pass_verify():
    """Every component, all nineteen, pasted onto one correct LG page and put through the
    real verifier. The static fixture in cases.json covers two of them and freezes their code
    at the moment it was written; this one is generated from the kit as it stands right now,
    so a component that starts breaking the brand rules cannot pass unnoticed."""
    store = json.load(open(os.path.join(KIT, "components.json"), encoding="utf-8"))
    css = "\n".join(c["css"] for c in store["components"].values() if c["css"])
    # Laid out in flow, not at guessed pixel offsets. The first version of this harness
    # stacked all nineteen at 62px intervals, so components 130-340px tall sat on top of one
    # another - and verify.py's new overlap rule failed the kit for the harness's mistake.
    blocks = "\n".join(f'<div class="slot">{c["html"]}</div>'
                       for c in store["components"].values())
    page = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8">
<link rel="stylesheet" href="../../templates/lg-tokens.css">
<style>:root{{--canvas-w:1400px;--canvas-h:7200px}}
{store['base_css']}
{css}
.rail{{position:absolute;left:var(--margin);right:var(--margin);
  top:calc(var(--margin)*3);display:flex;flex-direction:column;gap:60px;align-items:flex-start}}
.slot{{position:relative}}
</style></head><body>
<div class="lg-canvas" style="background:var(--lg-warm-gray-07)"><div class="lg-layer">
<img class="lg-logo lg-logo--upper-left" src="../../assets/logo/LGE_Logo_HeritageRed_Grey_RGB.png" alt="LG">
<div class="rail">
{blocks}
</div>
</div></div></body></html>"""
    tmp = os.path.join(HERE, "fixtures", ".motion-all.html")
    try:
        open(tmp, "w", encoding="utf-8").write(page)
        p = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "verify.py"),
                            tmp, "--canvas", "1400x7200"], capture_output=True, text=True)
        if p.returncode not in (0, 1):
            return [f"verify.py crashed (exit {p.returncode}): "
                    f"{(p.stderr or p.stdout).strip()[-160:]}"]
        return [l.strip() for l in (p.stdout + p.stderr).splitlines() if "[x]" in l]
    finally:
        if os.path.isfile(tmp):
            os.remove(tmp)


CHECKS = [
    ("kit is on-brand (doctor)", check_doctor),
    ("all 19 pass the real verifier on a page", check_components_pass_verify),
    ("generated files in step with build_motion.py", check_build_in_step),
    ("every component can be fetched", check_every_component_gets),
    ("CATALOG.md lists every component", check_catalog_matches),
    ("search finds the right component", check_search_finds),
    ("store stays small enough to justify the CLI", check_kit_size),
]


def main():
    bad = 0
    for label, fn in CHECKS:
        problems = fn()
        if problems:
            bad += 1
            print(f"  [FAIL] {label:<46} {len(problems)} problem(s)")
            for p in problems[:6]:
                print(f"         {p}")
        else:
            print(f"  [PASS] {label}")
    print("-" * 76)
    print(f"  {len(CHECKS) - bad}/{len(CHECKS)} motion checks pass")
    if bad:
        print("\n  Fix components in scripts/build_motion.py, then rebuild - never by editing\n"
              "  the generated files, which is what half of these checks are watching for.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
