#!/usr/bin/env python3
"""
run_portability.py - can this skill be handed to someone else?

    python3 tests/run_portability.py

A skill is a package that gets shared. Anything in it that only makes sense on the machine it
was built on becomes a broken instruction the moment somebody else installs it - and worse, one
the reading agent has no way to recognise as broken. It will follow a path to a folder that does
not exist and improvise from there.

This happened here: a manifest of Digital Logo Play masters was written with 35 absolute paths
into one person's home directory. It worked perfectly for that person, and would have failed
silently for everyone else, while also publishing their username and folder layout to anyone
they shared the file with.

So the rule is checked rather than remembered. Adding assets is exactly when it gets forgotten.

The same lane also checks the installer's own limits - filename characters and the 1024-character
description cap - because both have already refused this package once, and neither is visible
until the moment somebody clicks Save.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

TEXT_EXT = (".md", ".json", ".py", ".css", ".html", ".txt")
SKIP_DIRS = {"tests", "__pycache__", ".git"}

# Paths that only exist on one machine. The example config is exempt: it is a template whose
# whole purpose is to show a placeholder path, and it is never read unless copied.
EXEMPT = {"assets/local-pack.example.json"}

PATTERNS = [
    (r"/Users/[A-Za-z0-9._-]+", "a macOS home directory"),
    (r"/home/(?!claude\b)[A-Za-z0-9._-]+", "a Linux home directory"),
    (r"[A-Za-z]:\\\\Users\\\\", "a Windows home directory"),
    (r"/Volumes/[A-Za-z0-9 ._-]+", "a mounted volume name"),
    (r"/sessions/[a-z0-9-]+", "a session-specific sandbox path"),
]


def walk_text_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            if f.endswith(TEXT_EXT):
                full = os.path.join(dirpath, f)
                yield os.path.relpath(full, ROOT), full


def check_hardcoded_paths():
    findings = []
    for rel, full in walk_text_files():
        if rel in EXEMPT:
            continue
        try:
            text = open(full, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        for pat, what in PATTERNS:
            for m in re.finditer(pat, text):
                line = text[:m.start()].count("\n") + 1
                findings.append((rel, line, what, m.group(0)[:60]))
    return findings


def check_shipped_assets_resolve():
    """Every asset path a reference or manifest points at must exist inside the package."""
    findings = []
    man = os.path.join(ROOT, "assets", "digital-logo-play", "MANIFEST.json")
    if os.path.isfile(man):
        m = json.load(open(man, encoding="utf-8"))
        for mo in m.get("motions", []):
            for g in mo.get("gif", {}).values():
                if not os.path.isfile(os.path.join(ROOT, g["path"])):
                    findings.append(("MANIFEST.json", g["path"], "shipped GIF not in package"))
            for key in ("master_2k", "master_6k"):
                for d in mo.get(key, []):
                    if "device_path" in d or os.path.isabs(d.get("pack_relative_path", "")):
                        findings.append(("MANIFEST.json", d.get("pack_relative_path", "?"),
                                         "master path is absolute, not pack-relative"))
    for rel, full in walk_text_files():
        if not rel.endswith((".html", ".css")) or rel.startswith("tests"):
            continue
        base = os.path.dirname(full)
        text = open(full, encoding="utf-8", errors="replace").read()
        # Commented-out examples are documentation, not references. Scanning them was the
        # same mistake that once made the brand checker report a white logo on a light
        # ground because a comment happened to mention the white variant.
        text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
        text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
        for ref in re.findall(r'(?:src|href)="([^"]+)"', text) + \
                   re.findall(r'url\(["\']?([^"\')]+)', text):
            if ref.startswith(("http", "data:", "#")):
                continue
            if not os.path.isfile(os.path.join(base, ref)):
                findings.append((rel, ref, "referenced file does not exist in the package"))
    return findings


def check_package_installs():
    """The installer's own limits, checked here instead of at the moment someone clicks Save.

    Both of these have already bitten this package once each, and neither is visible while
    you work - the skill runs perfectly from a folder and then refuses to install:

      "Zip file contains path with invalid characters"     - a '+' in six logo filenames
      "field 'description' in SKILL.md must be at most      - a description grown one
       1024 characters"                                       clause at a time
    """
    problems = []
    sk = os.path.join(ROOT, "SKILL.md")
    text = open(sk, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return ["SKILL.md has no YAML frontmatter"]
    fields = dict(re.findall(r"^(name|description): (.*)$", m.group(1), re.M))
    if "name" not in fields or "description" not in fields:
        problems.append("SKILL.md frontmatter needs both name and description")
    if len(fields.get("description", "")) > 1024:
        problems.append(f"description is {len(fields['description'])} characters; "
                        f"the installer rejects anything over 1024")
    if not re.fullmatch(r"[a-z0-9-]{1,64}", fields.get("name", "")):
        problems.append(f"name '{fields.get('name')}' should be lowercase, hyphenated, <= 64 chars")

    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in ("__pycache__", ".git")]
        for f in dirnames + filenames:
            if any(c in f for c in "+ \t") or any(ord(c) < 32 for c in f):
                rel = os.path.relpath(os.path.join(dirpath, f), ROOT)
                problems.append(f"'{rel}' has a character the zip packer rejects "
                                f"(space or '+') - rename it, do not re-encode the file")
    return problems


def check_resolver_degrades():
    """With no pack, the resolver must explain itself rather than crash or stay silent."""
    env = dict(os.environ)
    env.pop("LG_BRAND_ASSETS", None)
    p = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "resolve_assets.py"),
                        "--no-search"], capture_output=True, text=True, env=env)
    out = p.stdout + p.stderr
    problems = []
    if p.returncode not in (0, 1):
        problems.append(f"resolver exited {p.returncode}")
    if "not found on this machine" not in out and "found at" not in out:
        problems.append("resolver does not state whether the pack was found")
    if "not found on this machine" in out and "normal state" not in out:
        problems.append("a missing pack is not explained as a normal state")
    if "LG_BRAND_ASSETS" not in out:
        problems.append("resolver does not say how to point at a pack")
    return problems


def main():
    bad = 0

    hard = check_hardcoded_paths()
    if hard:
        bad += 1
        print(f"  [FAIL] no machine-specific paths        {len(hard)} found")
        for rel, line, what, snippet in hard[:8]:
            print(f"         {rel}:{line}  {what}: {snippet}")
        if len(hard) > 8:
            print(f"         ... and {len(hard) - 8} more")
    else:
        print("  [PASS] no machine-specific paths        package is portable")

    broken = check_shipped_assets_resolve()
    if broken:
        bad += 1
        print(f"  [FAIL] asset references resolve         {len(broken)} broken")
        for a, b, c in broken[:8]:
            print(f"         {a}: {b}  ({c})")
    else:
        print("  [PASS] asset references resolve         every referenced file is present")

    inst = check_package_installs()
    if inst:
        bad += 1
        print(f"  [FAIL] package installs                 {len(inst)} problem(s)")
        for i in inst[:8]:
            print(f"         {i}")
    else:
        print("  [PASS] package installs                 frontmatter and filenames are legal")

    deg = check_resolver_degrades()
    if deg:
        bad += 1
        print("  [FAIL] resolver degrades gracefully")
        for d in deg:
            print(f"         {d}")
    else:
        print("  [PASS] resolver degrades gracefully     a missing pack is explained, not fatal")

    print("-" * 76)
    print(f"  {4 - bad}/4 portability checks pass")
    if bad:
        print("\n  A skill that only works on the machine that built it is not shareable.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
