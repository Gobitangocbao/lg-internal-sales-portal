#!/usr/bin/env python3
"""
resolve_assets.py - find the optional LG asset pack on *this* machine.

    python3 scripts/resolve_assets.py                 # report what is available
    python3 scripts/resolve_assets.py --find "09. Digital Logo/.../Nodding.mov"
    python3 scripts/resolve_assets.py --json          # machine-readable

Why this exists:

Almost everything the skill needs ships inside it and works anywhere. A few things are too
large to bundle - the Digital Logo Play .mov masters are about 1.1 GB, the CMYK logo set and
the full-resolution gradients are print-only, and the source PDFs are reference material. Those
live in LG's asset pack, which sits in a different place on every person's laptop.

An earlier version of the manifest recorded one person's absolute paths. That works on exactly
one machine: share the skill and every path is wrong, the agent reading it has no way to know
that, and the package quietly leaks that person's username and folder layout. So paths are now
recorded relative to the pack root, and the root is discovered here at run time.

Order of resolution, first hit wins:

  1. the LG_BRAND_ASSETS environment variable
  2. assets/local-pack.json next to this skill  (copy local-pack.example.json and edit it)
  3. a search of the usual places for a folder that looks like the pack

Nothing here fails the task. If the pack is absent, that is a normal state on most machines -
report it plainly, use the shipped assets, and tell the user which specific file would need the
pack. Guessing a path, or pretending a master file was used, is the failure mode to avoid.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)

# A folder is the pack if it holds these. Two of three is enough - people reorganise, and
# some copies of the pack are partial.
SIGNATURE = ("03_fonts", "04_logo", "01_guidelines", "09. Digital Logo",
             "02_color", "05_gradients", "06_slogan", "07_lg_ai")
MIN_HITS = 2

SEARCH_DEPTH = 4
CANDIDATE_ROOTS = [
    # Claude's desktop workspace mounts the folders you connected under ~/mnt, so that is
    # where the pack usually appears when a skill runs inside Claude - not at the path you
    # would type in Finder. Both are searched.
    "~/mnt", "~", "~/Documents", "~/Desktop", "~/Downloads", "~/Dropbox",
    "~/OneDrive", "~/Library/CloudStorage", "/Volumes", "/mnt", "/media",
]


def looks_like_pack(path):
    try:
        names = set(os.listdir(path))
    except OSError:
        return 0
    return sum(1 for s in SIGNATURE if s in names)


def from_env():
    p = os.environ.get("LG_BRAND_ASSETS")
    if p and os.path.isdir(os.path.expanduser(p)):
        return os.path.expanduser(p), "LG_BRAND_ASSETS"
    return None, None


def from_config():
    """pack_root may be a single path or a list. A list is useful because the same person
    reaches the same folder by two paths - the one they see in Finder, and the ~/mnt/... one
    Claude's workspace mounts it at - and only one of them exists in any given run."""
    cfg = os.path.join(SKILL, "assets", "local-pack.json")
    if not os.path.isfile(cfg):
        return None, None
    try:
        roots = json.load(open(cfg, encoding="utf-8")).get("pack_root", "")
    except (ValueError, OSError):
        return None, None
    for p in ([roots] if isinstance(roots, str) else list(roots)):
        p = os.path.expanduser(p)
        if os.path.isdir(p):
            return p, "assets/local-pack.json"
    return None, None


def by_search(verbose=False):
    """Walk a few likely places, shallowly. Deliberately bounded: a full disk scan on
    someone's laptop is not a reasonable thing for a brand skill to do."""
    seen = set()
    for root in CANDIDATE_ROOTS:
        root = os.path.expanduser(root)
        if not os.path.isdir(root):
            continue
        base_depth = root.rstrip(os.sep).count(os.sep)
        for dirpath, dirnames, _ in os.walk(root):
            if dirpath.count(os.sep) - base_depth >= SEARCH_DEPTH:
                dirnames[:] = []
                continue
            dirnames[:] = [d for d in dirnames
                           if not d.startswith(".") and d not in
                           ("node_modules", "Library", "Applications", "System")]
            real = os.path.realpath(dirpath)
            if real in seen:
                continue
            seen.add(real)
            if looks_like_pack(dirpath) >= MIN_HITS:
                return dirpath, "search"
    return None, None


def resolve(search=True, verbose=False):
    for fn in (from_env, from_config):
        p, how = fn()
        if p:
            return p, how
    if search:
        return by_search(verbose)
    return None, None


def status(pack):
    """What can be done right now, stated in terms of the work rather than the filesystem."""
    shipped = {
        "fonts": "assets/fonts",
        "logo (RGB)": "assets/logo",
        "slogan": "assets/slogan",
        "gradients (1400px)": "assets/gradients",
        "LG AI (SVG)": "assets/lg-ai",
        "Digital Logo Play (GIF)": "assets/digital-logo-play",
    }
    out = {"pack_root": pack, "shipped": {}, "needs_pack": {}}
    for k, v in shipped.items():
        d = os.path.join(SKILL, v)
        n = sum(len(f) for _, _, f in os.walk(d)) if os.path.isdir(d) else 0
        out["shipped"][k] = {"path": v, "files": n, "available": n > 0}
    out["needs_pack"] = {
        "Digital Logo Play .mov masters": "09. Digital Logo/",
        "CMYK logo set for print separation": "04_logo/cmyk/",
        "Full-resolution 2000px gradients": "05_gradients/",
        "The source guideline PDFs": "01_guidelines/",
        "The original PPTX templates": "08_ppt_templates/",
    }
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--find", help="a pack-relative path from a manifest; prints the absolute "
                                   "path if the pack is present")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-search", action="store_true", help="only env var and config file")
    args = ap.parse_args()

    pack, how = resolve(search=not args.no_search)
    st = status(pack)

    if args.json:
        st["resolved_by"] = how
        if args.find and pack:
            cand = os.path.join(pack, args.find)
            st["find"] = {"query": args.find, "path": cand if os.path.isfile(cand) else None}
        print(json.dumps(st, indent=1))
        return 0 if pack else 1

    if args.find:
        if not pack:
            print(f"The asset pack is not on this machine, so '{args.find}' cannot be resolved.\n"
                  f"Use the shipped equivalent if there is one, and tell the user this specific\n"
                  f"file needs the pack. See the setup note below.\n")
        else:
            cand = os.path.join(pack, args.find)
            if os.path.isfile(cand):
                print(cand)
                return 0
            print(f"The pack is at {pack} but '{args.find}' is not in it.\n"
                  f"Copies of the pack differ - say which file is missing rather than "
                  f"substituting another.\n")

    print("lg-brand assets")
    print("=" * 72)
    print("\nShipped with the skill - these work on any machine:")
    for k, v in st["shipped"].items():
        mark = "ok " if v["available"] else "MISSING"
        print(f"  [{mark}] {k:<28} {v['files']:>3} files   {v['path']}")

    print(f"\nOptional asset pack: {'found at ' + pack if pack else 'not found on this machine'}"
          + (f"  (via {how})" if pack else ""))
    for k, v in st["needs_pack"].items():
        if pack:
            ok = os.path.isdir(os.path.join(pack, v.rstrip("/")))
            print(f"  [{'ok ' if ok else '-- '}] {k:<42} {v}")
        else:
            print(f"  [--] {k:<42} {v}")

    if not pack:
        print("""
This is a normal state, not an error. The shipped assets above cover slides, posters,
banners, social and web work end to end. Only the items in the second list need the pack.

If this machine does have the pack, point the skill at it once, either way:

    export LG_BRAND_ASSETS="/path/to/LG assets"

or copy assets/local-pack.example.json to assets/local-pack.json and set "pack_root" - it
accepts a list, which is handy because Claude's workspace mounts a connected folder under
~/mnt/... rather than at the path you see in Finder.

If it does not: use the shipped assets, and when a task genuinely needs a master file, say
which file and why rather than substituting a different one.""")
    return 0 if pack else 1


if __name__ == "__main__":
    sys.exit(main())
