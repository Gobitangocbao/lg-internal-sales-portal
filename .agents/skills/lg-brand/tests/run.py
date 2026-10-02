#!/usr/bin/env python3
"""
run.py - the regression suite for verify.py.

    python3 tests/run.py

Every fixture in tests/fixtures/ is a deliberately broken (or deliberately correct) LG
layout, and cases.json says which error code each one must produce. The suite exists
because this skill has twice shipped a checker that reported success on work that was
wrong; a rule that is not covered here is a rule nobody is enforcing.

Adding a rule to verify.py without adding a fixture here is how the last regression got in.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VERIFY = os.path.join(ROOT, "scripts", "verify.py")


def run_case(c, default_canvas):
    path = os.path.join(HERE, "fixtures", c["file"])
    if not os.path.isfile(path):
        return False, f"fixture missing: {c['file']}", ""
    cmd = [sys.executable, VERIFY, path, "--canvas", c.get("canvas", default_canvas)]
    if c.get("web"):
        cmd.append("--web")
    p = subprocess.run(cmd, capture_output=True, text=True)
    out = p.stdout + p.stderr
    errs = set(re.findall(r"\[x\] (\w+)", out))
    warns = set(re.findall(r"\[!\] (\w+)", out))

    want_e = set(c.get("expect", [])) if c.get("expect") != "pass" else set()
    want_w = set(c.get("expect_warn", []))
    clean_expected = c.get("expect") == "pass"

    if clean_expected:
        ok = not errs
        return ok, ("clean" if ok else f"expected clean, got {sorted(errs)}"), out

    missing_e = want_e - errs
    missing_w = want_w - warns
    ok = not missing_e and not missing_w
    caught = sorted((want_e & errs) | (want_w & warns))
    detail = "caught " + ", ".join(caught) if caught else ""
    if missing_e or missing_w:
        detail = (f"MISSED {sorted(missing_e | missing_w)}; "
                  f"errors {sorted(errs) or 'none'}, warnings {sorted(warns) or 'none'}")
    elif errs - want_e:
        detail += f" (also errored on {sorted(errs - want_e)})"
    return ok, detail, out


def check_crash_is_not_a_pass():
    """The one case that cannot be a fixture file, because the point is that there is no file.

    verify.py used to catch a render exception, print it as a line of prose, and then dump a
    report ending in "0 error(s) - geometry, fonts and assets check out". The exit code was
    right and the sentence a human reads was wrong, which is the half that ships.
    """
    p = subprocess.run([sys.executable, VERIFY, os.path.join(HERE, "no-such-page.html"),
                        "--canvas", "1080x1350"], capture_output=True, text=True)
    out = p.stdout + p.stderr
    problems = []
    if p.returncode != 2:
        problems.append(f"exit code was {p.returncode}, expected 2")
    if "VERIFY_INCOMPLETE" not in out:
        problems.append("did not report VERIFY_INCOMPLETE")
    if "THIS IS NOT A PASS" not in out:
        problems.append("did not say plainly that this is not a pass")
    if "check out" in out:
        problems.append("still printed the all-clear sentence after failing to measure")
    return problems


def check_templates_are_clean():
    """Whatever else is true, the files people start from must pass.

    templates/ is the one place in this skill that is copied rather than read, so a defect
    there is inherited by every deliverable built from it and is never noticed again.
    """
    tdir = os.path.join(ROOT, "templates")
    sizes = {"slide-16x9.html": ("1920x1080", False), "deck-16x9.html": ("1920x1080", False),
             "poster-a2.html": ("420x594mm", False),
             # banner-web.html is built to the lge.com design system, which has its own red
             # and does not expect a logo on the component - it needs --web to be judged.
             "banner-web.html": ("1920x720", True)}
    problems = []
    for name, (canvas, web) in sizes.items():
        full = os.path.join(tdir, name)
        if not os.path.isfile(full):
            problems.append(f"{name} is missing from templates/")
            continue
        cmd = [sys.executable, VERIFY, full, "--canvas", canvas] + (["--web"] if web else [])
        p = subprocess.run(cmd, capture_output=True, text=True)
        errs = set(re.findall(r"\[x\] (\w+)", p.stdout + p.stderr))
        if errs:
            problems.append(f"{name}: {sorted(errs)}")
    return problems


def check_for_print_produces_a_clean_page():
    """for_print.py exists to turn a warning into a command. If its output does not itself
    verify clean, it has moved the problem rather than solved it."""
    src = os.path.join(ROOT, "templates", "deck-16x9.html")
    out = os.path.join(ROOT, "templates", ".print-test.html")
    if not os.path.isfile(src):
        return ["templates/deck-16x9.html is missing"]
    try:
        p = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "for_print.py"),
                            src, "-o", out], capture_output=True, text=True)
        if p.returncode != 0:
            return [f"for_print.py exited {p.returncode}"]
        text = open(out, encoding="utf-8").read()
        problems = []
        # The removal comment names the motion on purpose, so look for a LOADED file,
        # not for the phrase.
        if re.search(r'src\s*=\s*"[^"]*Digital[ _]Logo[ _]Play', text):
            problems.append("the print copy still loads a Digital Logo Play file")
        v = subprocess.run([sys.executable, VERIFY, out, "--canvas", "1920x1080"],
                           capture_output=True, text=True)
        errs = set(re.findall(r"\[x\] (\w+)", v.stdout + v.stderr))
        if errs:
            problems.append(f"the print copy does not verify clean: {sorted(errs)}")
        return problems
    finally:
        if os.path.isfile(out):
            os.remove(out)


def check_every_error_code_has_a_next_step():
    """Every code the suite can produce must have a plain next step in report.py.

    A code with no next step is a dead end for the person reading the report: it names the
    rule and leaves them to work out what to change. Adding a rule without adding its line
    here is the easy omission, so it is checked rather than remembered.
    """
    import importlib.util
    spec_ = importlib.util.spec_from_file_location(
        "lgreport", os.path.join(ROOT, "scripts", "report.py"))
    mod = importlib.util.module_from_spec(spec_)
    spec_.loader.exec_module(mod)

    wanted = set()
    cases = json.load(open(os.path.join(HERE, "cases.json")))
    for c in cases["cases"]:
        if c.get("expect") != "pass":
            wanted |= set(c.get("expect", []))
        wanted |= set(c.get("expect_warn", []))
    wanted.add("VERIFY_INCOMPLETE")
    missing = sorted(wanted - set(mod.NEXT_STEP))
    return [f"report.py has no next step for: {', '.join(missing)}"] if missing else []


def check_report_renders():
    """report.py must produce a self-contained page - if the screenshots are not embedded it
    cannot be forwarded, which is the entire point of it."""
    src = os.path.join(HERE, "fixtures", "text-overlap.html")
    out = os.path.join(HERE, "fixtures", ".report-test.html")
    try:
        p = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "report.py"),
                            src, "--canvas", "1920x1080", "-o", out],
                           capture_output=True, text=True)
        if p.returncode not in (0, 1):
            return [f"report.py exited {p.returncode}: {(p.stderr or p.stdout).strip()[-140:]}"]
        if not os.path.isfile(out):
            return ["report.py wrote no file"]
        text = open(out, encoding="utf-8").read()
        problems = []
        if "data:image/png;base64," not in text:
            problems.append("the render is not embedded, so the report cannot be forwarded")
        if "OVERLAP" not in text:
            problems.append("the finding does not appear in the report")
        if 'class="mark"' not in text:
            problems.append("the finding is not drawn on the render")
        if "16 trong 38" not in text:
            problems.append("the report does not state what it cannot check")
        return problems
    finally:
        if os.path.isfile(out):
            os.remove(out)


def check_deck_replays_animations():
    """A deck template must actually present.

    The defect this guards: CSS animations run once, at load, for every slide at the same
    time. A deck full of animated components therefore plays its entire motion design in the
    first two seconds - before anyone has advanced past slide 1 - and every slide after that
    is a still picture when it is reached. The components were fine; nobody ever saw them.
    Fixing it needs a replay on entry, and a rule that is not tested is a rule that rots.
    """
    src = os.path.join(ROOT, "templates", "deck-16x9.html")
    if not os.path.isfile(src):
        return ["templates/deck-16x9.html is missing"]
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return []          # same skip as the rest of the browser lane
    problems = []
    with sync_playwright() as pw:
        b = pw.chromium.launch()

        # A slide is 1920px wide by definition. On a laptop window the file therefore opens
        # showing a corner of slide 1 unless the stacked view scales itself down - which is
        # exactly what happened the first time this deck was opened on a MacBook.
        for vw, vh in ((1280, 800), (1440, 900)):
            small = b.new_page(viewport={"width": vw, "height": vh})
            small.goto("file://" + os.path.abspath(src))
            small.wait_for_timeout(1200)
            m = small.evaluate("() => ({ slide: Math.round(document.querySelector('.lg-canvas').getBoundingClientRect().width), doc: document.documentElement.scrollWidth })")
            if m["doc"] > vw + 2 or m["slide"] > vw:
                problems.append(f"at {vw}x{vh} the deck does not fit the window "
                                f"(slide {m['slide']}px, page {m['doc']}px) - it opens "
                                f"showing part of one slide")
            small.close()

        pg = b.new_page(viewport={"width": 1440, "height": 900})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto("file://" + os.path.abspath(src))
        pg.wait_for_timeout(2200)          # let the initial pass finish
        if errs:
            problems.append(f"javascript error: {errs[0][:90]}")
        pg.keyboard.press("f")
        pg.wait_for_timeout(500)
        if not pg.evaluate("document.body.classList.contains('present')"):
            problems.append("F does not enter presentation mode")
        if pg.evaluate("document.querySelectorAll('.lg-canvas.is-live').length") != 1:
            problems.append("presentation mode does not show exactly one slide")
        fit = pg.evaluate(
            "getComputedStyle(document.documentElement).getPropertyValue('--fit').trim()")
        if not fit or float(fit or 0) <= 0:
            problems.append("the slide is not scaled to the screen (--fit unset)")
        pg.keyboard.press("ArrowRight")
        pg.wait_for_timeout(150)
        running = pg.evaluate("""() => {
            const el = document.querySelector('.lg-canvas.is-live');
            return el ? el.getAnimations({subtree:true})
                          .filter(a => a.playState === 'running').length : -1; }""")
        if running < 1:
            problems.append(f"arriving on a slide does not replay its animations "
                            f"({running} running) - the deck presents as still pictures")
        b.close()
    return problems


EXTRA = [
    ("(a page that cannot be measured)", check_crash_is_not_a_pass),
    ("(templates/ all verify clean)", check_templates_are_clean),
    ("(for_print.py output verifies)", check_for_print_produces_a_clean_page),
    ("(every code has a next step)", check_every_error_code_has_a_next_step),
    ("(report.py renders a page)", check_report_renders),
    ("(deck fits window + replays)", check_deck_replays_animations),
]


def main():
    spec = json.load(open(os.path.join(HERE, "cases.json")))
    canvas = spec["canvas"]
    results = []
    for c in spec["cases"]:
        ok, detail, out = run_case(c, canvas)
        results.append((ok, c, detail, out))
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] {c['file']:<32} {detail}")
        if not ok and "-v" in sys.argv:
            print("        " + "\n        ".join(out.splitlines()[:24]))

    extra_bad = 0
    for label, fn in EXTRA:
        problems = fn()
        if problems:
            extra_bad += 1
            print(f"  [FAIL] {label:<32} " + "; ".join(problems)[:110])
        else:
            print(f"  [PASS] {label:<32} ok")

    failed = [r for r in results if not r[0]]
    print("-" * 76)
    print(f"  {len(results) - len(failed)}/{len(results)} cases pass"
          + f"  + {len(EXTRA) - extra_bad}/{len(EXTRA)} structural checks")
    if failed:
        print("\n  Not enforced yet:")
        for _, c, detail, _ in failed:
            print(f"    - {c['file']}: {c['why']}")
    return 1 if (failed or extra_bad) else 0


if __name__ == "__main__":
    sys.exit(main())
