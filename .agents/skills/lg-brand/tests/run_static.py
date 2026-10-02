#!/usr/bin/env python3
"""Static-only lane: the checks that run without a browser, plus PPTX.

verify.py needs playwright. brand_check.py does not, and it is the only check available for
a .pptx. This lane keeps those rules covered so they cannot rot unnoticed.
"""
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
BC = os.path.join(ROOT, "scripts", "brand_check.py")
CASES = [
    ("fixtures/font-path-broken.html", [], ["FONT_URL_MISSING"], "a wrong @font-face path resolves to nothing"),
    ("fixtures/arial-fallback.html",   [], ["FONT_SUBSTITUTE"],  "a named non-LG font in the stack"),
    ("pptx/good.pptx",                 [], [],                   "a deck built by build_pptx.py must be clean"),
    ("pptx/bad.pptx", [], ["PPTX_THEME_FONT","PPTX_THEME_OFFICE","PPTX_FONT_SUBSTITUTE","PPTX_LOGO_NOT_OFFICIAL"],
     "default Office theme, Calibri runs, and a re-saved logo instead of the shipped bytes"),
]
def main():
    bad = 0
    for path, args, want, why in CASES:
        full = os.path.join(HERE, path)
        # A missing file, or a crash, must never read as "clean" - that is how a test suite
        # starts lying to you.
        if not os.path.isfile(full):
            print(f"  [FAIL] {path:<30} fixture missing"); bad += 1; continue
        p = subprocess.run([sys.executable, BC, full] + args, capture_output=True, text=True)
        if p.returncode not in (0, 1):
            print(f"  [FAIL] {path:<30} checker crashed (exit {p.returncode})")
            print("        " + (p.stderr.strip().splitlines() or [""])[-1]); bad += 1; continue
        got = set(re.findall(r"\[x\] (\w+)", p.stdout + p.stderr))
        missing = set(want) - got
        ok = (not missing) if want else (not got)
        print(f"  [{'PASS' if ok else 'FAIL'}] {path:<30} "
              + ("clean" if not want else f"caught {sorted(set(want)&got)}"
                 + (f" MISSED {sorted(missing)}" if missing else "")))
        if not ok:
            bad += 1
            print(f"        {why}")
    print("-"*76); print(f"  {len(CASES)-bad}/{len(CASES)} static cases pass")
    return 1 if bad else 0
if __name__ == "__main__":
    sys.exit(main())
