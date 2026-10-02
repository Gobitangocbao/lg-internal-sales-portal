#!/usr/bin/env python3
"""
report.py - turn a verify run into a page a person can read and forward.

    python3 scripts/report.py deck.html --canvas 1920x1080
    python3 scripts/report.py poster.html --canvas 420x594mm -o review.html
    python3 scripts/report.py banner.html --canvas 1920x720 --web

It runs verify.py for you and writes ONE self-contained HTML file: every slide as it actually
rendered, each finding drawn on the slide it belongs to, and a plain statement of what was
checked by machine and what still needs a human eye.

Why this exists:

Everything else in this skill talks to an agent. A marketeer gets `[x] MARGIN_ENCROACHED` in a
terminal they are not looking at, and has nothing to send to Brand Management except a sentence
in a chat window. That is the gap this closes: the output is a file, it shows the work, and it
is honest about its own limits in writing rather than in a docstring nobody opens.

The report never says "approved". 16 of the guideline's 38 numbered prohibitions can be checked
mechanically; the other 22 are judgement. The page says which is which, every time.
"""
import argparse
import base64
import html
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
VERIFY = os.path.join(HERE, "verify.py")

# What a person should DO about each code. verify.py's own hints explain the rule; these are
# the one-line next step, in the order someone would actually work through them.
NEXT_STEP = {
    "VERIFY_INCOMPLETE": "The page could not be opened or rendered. Fix that first — nothing below was measured.",
    "LOGO_ABSENT": "Place the LG logo, or fix the path — the file it points at did not load.",
    "ASSET_NOT_LOADED": "Fix the image path. The box is there; the picture is not.",
    "LOGO_SIZE": "Set the logo height from the margin: symbol = 1.30 × margin. lg-tokens.css does the maths.",
    "SLOGAN_SIZE": "Set the slogan to 0.90 × margin of visible artwork — the file carries padding.",
    "LOGO_POSITION": "Move the logo to one of the five permitted positions. Bottom-right is not one of them.",
    "LOGO_TOO_SMALL": "Enlarge it, or use the Small-Size artwork LG ships for tiny placements.",
    "LOGO_TRANSFORMED": "Remove the rotate/skew/stretch. The lockup is fixed artwork.",
    "LOGO_SLOGAN_ADJACENT": "Separate them — logo and slogan are never side by side.",
    "SLOGAN_STACKED_SIGNOFF": "Use the horizontal slogan for a sign-off.",
    "SYMBOL_ALONE": "Add the logotype. The symbol stands alone only on cards, badges and app icons.",
    "MARGIN_ENCROACHED": "Pull it back inside the margin. The margin stays empty.",
    "OVERLAP": "Two things are on top of each other. Lay the slide out on the grid instead of by pixel offsets.",
    "TEXT_CONTRAST": "Change the text colour — see the measured table in references/color.md.",
    "FONT_NOT_RENDERED": "The LG EI font did not load. Check the @font-face paths.",
    "FONT_NOT_LG": "Set the text in LG EI Headline or LG EI Text.",
    "COLOR_OFF_PALETTE": "Replace it with a palette colour.",
    "COLOR_WEB_RED_OFFWEB": "Off lge.com the Active Red is #FD312E, not the web red.",
    "GRADIENT_TWO": "Keep one master gradient per piece.",
    "GRADIENT_IN_TEXT": "Gradients do not go inside type.",
    "LOGO_RED_ON_RED": "Move the logo, or switch to the white lockup.",
    "LOGO_LOW_CONTRAST": "Switch lockup variant — dark mark on light ground, white on dark.",
    "DLP_ON_STATIC_MEDIA": "Digital Logo Play is motion-only. Use the static logo here.",
    "DLP_TRANSFORMED": "Remove the transform — the eight movements are fixed artwork.",
    "DLP_ANIMATED": "Remove the CSS animation. Adding motion on top of it is editing it.",
    "BRAND_ASSET_ANIMATED": "Animate the layout around the mark, never the mark. scripts/lg_motion.py has components for that.",
    "LOGO_REDRAWN": "Use the shipped logo file instead of a drawn approximation.",
    "PAGE_ERROR": "A script on the page failed. Worth fixing before trusting the render.",
    "DLP_EXPORT_RISK": "Fine on screen. Before printing or exporting to PDF, run scripts/for_print.py.",
    "SCALED_BOX": "Enlarge with `zoom`, not `transform: scale()` — see references/motion.md.",
    "MOTION_NO_REDUCED_GUARD": "Add a prefers-reduced-motion block, or paste the lg-motion base CSS.",
    "LOGO_BUSY_GROUND": "Move the logo somewhere calmer, or put it on a flat panel.",
    "CANVAS_MISMATCH": "The page rendered at a different size than --canvas said. Check which is right.",
    "LOGO_USE_SMALL_ART": "Below about 60px, use the Small-Size artwork LG ships.",
    "FONT_MAY_BE_SUBSTITUTED": "Usually a false alarm — confirm by looking at the render.",
    "FONT_URL_MISSING": "A @font-face path does not resolve on disk. Paths are relative to the CSS file.",
    "LOGO_VARIANT_MIXED": "Chọn một lockup và giữ nguyên cả bộ — mặc định là symbol + \"LG\" (compact).",
    "LOGO_CORPORATE_LOCKUP": "Bài sản phẩm/kênh dùng lockup compact symbol + \"LG\"; lockup \"LG Electronics\" dành cho nơi cần đủ tên công ty.",
    "LOGO_WORDMARK_ALONE": "Dùng lockup có cả symbol — chữ \"LG Electronics\" đứng một mình không phải logo chính.",
    "SLOGAN_ALONE": "Place the LG logo too — the slogan never appears without it.",
    "SLOGAN_REPEATED": "Use the slogan once per piece.",
    "DLP_WITHOUT_MASTER_LOGO": "Digital Logo Play precedes the master logo, it does not replace it — check the master logo appears somewhere.",
}

# The 22 the machine cannot judge, in the words a reviewer would use. Printed on every report,
# because a clean run is the most misread output this skill produces.
BY_EYE = [
    "Ảnh có ấm và có hơi người không, hay lạnh như ảnh kỹ thuật",
    "Cắt cúp có làm hỏng cái đẹp của gradient không",
    "Bố cục có xứng với khoảng trống nó chiếm không",
    "Tiêu đề có nói đúng một ý, và nói bằng giọng của LG không",
    "Sản phẩm có được thể hiện trung thực và ở trạng thái đẹp nhất không",
    "Hình EI form là EI form thật, hay chỉ là một hình trông giống",
    "Bài này thuộc hệ nào — core BI hay LG AI",
    "Co-branding với đối tác ở đây có được phép không",
]

CSS = """
*{box-sizing:border-box}
body{margin:0;background:#F6F3EB;color:#4A4946;
  font-family:"LG EI Text",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-size:15px;line-height:1.55}
.page{max-width:1100px;margin:0 auto;padding:44px 24px 90px}
h1,h2,h3{font-family:"LG EI Headline",sans-serif;color:#262626;margin:0;font-weight:600}
h1{font-size:34px;line-height:1.15}
h2{font-size:21px;margin:0 0 14px}
h3{font-size:16px}
.head{border-bottom:3px solid #262626;padding-bottom:26px;margin-bottom:34px}
.file{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px;color:#716F6A;margin-top:10px;word-break:break-all}
.verdict{display:inline-block;margin-top:20px;padding:9px 16px;font-weight:600;font-size:15px}
.v-clean{background:#E6E1D6;color:#262626}
.v-fail{background:#FD312E;color:#fff}
.v-broken{background:#262626;color:#F6F3EB}
.tally{display:flex;gap:26px;margin-top:22px;font-size:14px;color:#716F6A}
.tally b{display:block;font-family:"LG EI Headline",sans-serif;font-size:28px;color:#262626;line-height:1.1}
.slide{margin:38px 0 0;border-top:1px solid #CBC8C2;padding-top:26px}
.shotwrap{position:relative;display:block;line-height:0;background:#fff;border:1px solid #CBC8C2}
.shotwrap img{width:100%;height:auto;display:block}
.mark{position:absolute;border:3px solid #FD312E;box-shadow:0 0 0 2px rgba(255,255,255,.7) inset}
.mark span{position:absolute;top:-2px;left:-3px;transform:translateY(-100%);
  background:#FD312E;color:#fff;font-size:11px;font-weight:700;padding:2px 6px;white-space:nowrap;
  font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
.rows{list-style:none;padding:0;margin:18px 0 0;display:flex;flex-direction:column;gap:10px}
.row{display:grid;grid-template-columns:26px 1fr;gap:12px;padding:12px 14px;background:#fff;
  border-left:4px solid #CBC8C2}
.row--err{border-left-color:#FD312E}
.row--warn{border-left-color:#716F6A}
.n{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px;color:#716F6A;text-align:right}
.row b{color:#262626}
.code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11px;color:#716F6A;
  letter-spacing:.04em;display:block;margin-bottom:3px}
.do{display:block;margin-top:7px;color:#262626}
.do::before{content:"→ ";color:#FD312E;font-weight:700}
.why{display:block;margin-top:5px;font-size:13.5px;color:#716F6A}
.limits{margin-top:52px;padding:26px;background:#EFEBE2;border-left:4px solid #262626}
.limits ul{margin:12px 0 0;padding-left:20px}
.limits li{margin:5px 0}
.foot{margin-top:34px;font-size:13px;color:#716F6A}
@media print{body{background:#fff}.page{padding:0}.slide{page-break-inside:avoid}}
"""


def data_uri(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def build(result, target):
    rows = [r for r in result["rows"] if r["level"] != "INFO"]
    errs = [r for r in rows if r["level"] == "ERROR"]
    warns = [r for r in rows if r["level"] == "WARN"]
    broken = any(r["code"] == "VERIFY_INCOMPLETE" for r in errs)
    frames = result["frames"]
    name = os.path.basename(target)

    if broken:
        verdict = ("v-broken", "Không kết luận được — trang chưa hề được đo")
    elif errs:
        verdict = ("v-fail", f"{len(errs)} lỗi phải sửa trước khi phát hành")
    else:
        verdict = ("v-clean", "Không có lỗi máy kiểm được — phần còn lại cần mắt người")

    out = [f"""<!doctype html><html lang="vi"><head><meta charset="utf-8">
<title>LG brand check — {html.escape(name)}</title>
<link rel="stylesheet" href="{html.escape(os.path.relpath(os.path.join(SKILL, 'templates', 'lg-tokens.css'), os.path.dirname(os.path.abspath(target))).replace(os.sep, '/'))}">
<style>{CSS}</style></head><body><div class="page">
<div class="head">
  <h1>Kiểm nhận diện LG</h1>
  <div class="file">{html.escape(target)} · khung {html.escape(result['canvas'])}{' · hệ LG.com' if result.get('web') else ''}</div>
  <div class="verdict {verdict[0]}">{verdict[1]}</div>
  <div class="tally">
    <div><b>{len(frames)}</b>trang / slide đã đo</div>
    <div><b>{len(errs)}</b>lỗi</div>
    <div><b>{len(warns)}</b>cảnh báo</div>
  </div>
</div>"""]

    for fr in frames:
        fr_rows = [r for r in rows if r["slide"] == fr["index"]]
        label = f"Slide {fr['index'] + 1} / {len(frames)}" if len(frames) > 1 else "Trang"
        out.append(f'<div class="slide"><h2>{label}</h2><div class="shotwrap">')
        if os.path.isfile(fr["shot"]):
            out.append(f'<img src="{data_uri(fr["shot"])}" alt="">')
        marks = 0
        for r in fr_rows:
            if not r["box"]:
                continue
            marks += 1
            x, y, w, h = r["box"]
            out.append(
                f'<div class="mark" style="left:{x / fr["w"] * 100:.3f}%;top:{y / fr["h"] * 100:.3f}%;'
                f'width:{w / fr["w"] * 100:.3f}%;height:{h / fr["h"] * 100:.3f}%">'
                f'<span>{marks}</span></div>')
        out.append("</div>")

        if not fr_rows:
            out.append('<ul class="rows"><li class="row"><div class="n">—</div><div>'
                       'Không có phát hiện nào trên trang này.</div></li></ul>')
        else:
            out.append('<ul class="rows">')
            n = 0
            for r in fr_rows:
                cls = "row--err" if r["level"] == "ERROR" else "row--warn"
                num = ""
                if r["box"]:
                    n += 1
                    num = str(n)
                msg = html.escape(r["msg"].split(": ", 1)[-1] if r["msg"].startswith("slide ") else r["msg"])
                step = NEXT_STEP.get(r["code"], "")
                out.append(
                    f'<li class="row {cls}"><div class="n">{num}</div><div>'
                    f'<span class="code">{r["code"]}</span><b>{msg}</b>'
                    + (f'<span class="do">{html.escape(step)}</span>' if step else "")
                    + (f'<span class="why">{html.escape(r["hint"])}</span>' if r["hint"] else "")
                    + "</div></li>")
            out.append("</ul>")
        out.append("</div>")

    out.append('<div class="limits"><h3>Máy kiểm được gì, và không kiểm được gì</h3>'
               '<p style="margin-top:10px">Bản này đo hình học, tài sản thương hiệu, phông chữ, '
               'màu và độ tương phản trên trang đã render. <b>Một bản sạch không phải là một lần '
               'duyệt brand.</b> 16 trong 38 điều cấm được đánh số của guideline kiểm được bằng '
               'máy; 22 điều còn lại cần người nhìn:</p><ul>')
    for item in BY_EYE:
        out.append(f"<li>{html.escape(item)}</li>")
    out.append('</ul><p style="margin-top:12px">Những mục đó cần một người xem bản render ở trên '
               'và trả lời. Chưa ai trả lời thì chưa xong.</p></div>')

    out.append('<p class="foot">Tạo bằng <code>scripts/report.py</code> của skill lg-brand '
               '(LG BI Guidelines V5.2, 08/2024). Mọi con số đều truy được nguồn trong '
               '<code>references/sources.md</code>.</p>')
    out.append("</div></body></html>")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page")
    ap.add_argument("--canvas", required=True, help="e.g. 1920x1080 or 420x594mm")
    ap.add_argument("--web", action="store_true", help="LG.com design system")
    ap.add_argument("-o", "--out", help="default: <page>-report.html next to the page")
    a = ap.parse_args()

    if not os.path.isfile(a.page):
        sys.exit(f"no such file: {a.page}")

    tmp = tempfile.mkdtemp()
    jpath = os.path.join(tmp, "result.json")
    cmd = [sys.executable, VERIFY, a.page, "--canvas", a.canvas,
           "--json", jpath, "--shot", os.path.join(tmp, "shot.png")]
    if a.web:
        cmd.append("--web")
    p = subprocess.run(cmd, capture_output=True, text=True)
    print(p.stdout, end="")

    if not os.path.isfile(jpath):
        # verify.py could not even get far enough to write a result. Say so; do not write a
        # report that looks like a review of a page nobody measured.
        sys.stderr.write("\nverify.py produced no result, so there is nothing to report on.\n"
                         "Its output is above - fix that first.\n")
        return 2

    result = json.load(open(jpath, encoding="utf-8"))
    dest = a.out or (os.path.splitext(a.page)[0] + "-report.html")
    open(dest, "w", encoding="utf-8").write(build(result, os.path.abspath(a.page)))
    print(f"\nreport: {dest}")
    print("Open it in a browser. It is one self-contained file - the screenshots are embedded,\n"
          "so it can be sent to Brand Management as-is.")
    return 1 if any(r["level"] == "ERROR" for r in result["rows"]) else 0


if __name__ == "__main__":
    sys.exit(main())
