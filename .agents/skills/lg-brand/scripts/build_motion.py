#!/usr/bin/env python3
"""
build_motion.py - source of truth for the LG motion kit.

Every component lives here as data. Running this emits the store that lg_motion.py serves:

    assets/lg-motion/components.json   all the code
    assets/lg-motion/index.json        metadata, machine-readable
    assets/lg-motion/CATALOG.md        one line per component, for reading
    assets/lg-motion/gallery.html      built page, for human eyes only

Keeping the definitions in one Python file rather than hand-editing four generated files is
what stops the catalogue drifting away from the code. Add a component here, run this, done.

    python3 scripts/build_motion.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
OUT = os.path.join(SKILL, "assets", "lg-motion")

# ---------------------------------------------------------------- shared CSS

# One block, emitted once per page. Everything is prefixed .lgm- so a component can be pasted
# beside anything else without a collision.
#
# The palette is LG's, from references/color.md. The timings are NOT in the guideline - it
# specifies the three motion families and their character but no durations or curves. These
# values are a reading of "warm, unhurried, restrained": a plain ease-out with no overshoot,
# because a bounce would read as playful in a way LG's system is not.
BASE = """
.lgm{
  --lgm-red:#FD312E; --lgm-heritage:#A50034;
  --lgm-ink:#262626; --lgm-body:#4A4946; --lgm-mute:#716F6A;
  --lgm-line:#CBC8C2; --lgm-panel:#E6E1D6; --lgm-panel-2:#F0ECE4; --lgm-bg:#F6F3EB;
  --lgm-slow:900ms; --lgm-med:600ms; --lgm-fast:350ms;
  --lgm-ease:cubic-bezier(.22,.61,.36,1);
  --lgm-step:90ms;
  font-family:"LG EI Text",sans-serif; color:var(--lgm-body);
  -webkit-font-smoothing:antialiased;
}
.lgm h1,.lgm h2,.lgm h3,.lgm .lgm-h{font-family:"LG EI Headline",sans-serif;font-weight:600;color:var(--lgm-ink);margin:0}
.lgm *{box-sizing:border-box}

/* Adaptive - the default arrival. Content rises a little and settles. Used for anything that
   simply needs to appear in order. */
@keyframes lgm-rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
@keyframes lgm-fade{from{opacity:0}to{opacity:1}}
/* Connected - a line drawing between things, so a relationship is shown rather than stated. */
@keyframes lgm-draw{from{stroke-dashoffset:var(--len,400)}to{stroke-dashoffset:0}}
@keyframes lgm-growx{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes lgm-growy{from{transform:scaleY(0)}to{transform:scaleY(1)}}
/* Fluid - continuous, ambient, for a state rather than an event. Use sparingly. */
@keyframes lgm-drift{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
@keyframes lgm-pulse{0%,100%{opacity:.35}50%{opacity:1}}
@keyframes lgm-spin{to{transform:rotate(360deg)}}

.lgm-rise{animation:lgm-rise var(--lgm-med) var(--lgm-ease) both}
.lgm-fade{animation:lgm-fade var(--lgm-med) var(--lgm-ease) both}

/* Dark ground. Put .lg-dark on the slide (or .lgm--dark on the component) and the kit
   re-roles the same LG palette. Measured on #262626: Warm Gray 07 is 13.7:1, 05 is 11.6:1,
   04 is 9.1:1 - and Warm Gray 03, which reads as the obvious "muted" choice, is only 3.0:1
   and is not used here. Heritage Red is 1.9:1 on dark and has no place on it at all. */
.lg-dark .lgm,.lgm--dark{
  --lgm-ink:#F6F3EB; --lgm-body:#E6E1D6; --lgm-mute:#CBC8C2;
  --lgm-line:#716F6A; --lgm-panel:#4A4946; --lgm-panel-2:#4A4946; --lgm-bg:#262626;
  --lgm-heritage:#FD312E;   /* Heritage Red is unreadable here; the accent stays Active Red */
}

/* Anyone who has asked their system to reduce motion gets the finished state immediately.
   This is not decoration - vestibular disorders are real, and a brand that talks about warmth
   should not make someone feel ill. */
@media (prefers-reduced-motion: reduce){
  .lgm *,.lgm *::before,.lgm *::after{
    animation-duration:1ms !important; animation-delay:0ms !important;
    animation-iteration-count:1 !important; transition-duration:1ms !important;
  }
}
"""

# ---------------------------------------------------------------- components

C = []


def comp(cid, cat, name, family, size, use, tags, html, css="", pri=1):
    C.append(dict(id=cid, cat=cat, name=name, family=family, size=size,
                  use=use, tags=tags, html=html.strip(), css=css.strip(), pri=pri))


# ---- charts -----------------------------------------------------

comp("bars-compare", "charts", "Cột so sánh kênh", "adaptive", "480x260",
     "So sánh sell-out hoặc doanh số giữa các kênh, có thứ hạng rõ ràng",
     ["cột", "bar", "so sánh", "compare", "kênh", "channel", "sell-out", "doanh số", "ranking"],
     """
<div class="lgm lgm-bars">
  <div class="lgm-h">Sell-out theo kênh</div>
  <div class="lgm-bars-plot">
    <div class="lgm-bar" style="--v:82%;--i:0"><span class="lgm-bar-f"></span><b>82</b><i>MT</i></div>
    <div class="lgm-bar" style="--v:64%;--i:1"><span class="lgm-bar-f"></span><b>64</b><i>GT</i></div>
    <div class="lgm-bar lgm-bar--hi" style="--v:97%;--i:2"><span class="lgm-bar-f"></span><b>97</b><i>Online</i></div>
    <div class="lgm-bar" style="--v:41%;--i:3"><span class="lgm-bar-f"></span><b>41</b><i>B2B</i></div>
  </div>
</div>""",
     """
.lgm-bars{width:480px;padding:20px 22px;background:var(--lgm-bg)}
.lgm-bars .lgm-h{font-size:19px;margin-bottom:18px}
.lgm-bars-plot{display:flex;gap:14px;align-items:flex-end;height:170px}
.lgm-bar{flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;height:100%}
.lgm-bar-f{width:100%;height:var(--v);background:var(--lgm-line);border-radius:3px 3px 0 0;
  transform-origin:bottom;animation:lgm-growy var(--lgm-slow) var(--lgm-ease) both;
  animation-delay:calc(var(--i) * var(--lgm-step))}
.lgm-bar--hi .lgm-bar-f{background:var(--lgm-red)}
.lgm-bar b{font-family:"LG EI Headline";font-size:18px;color:var(--lgm-ink);order:-1;margin-bottom:6px;
  animation:lgm-fade var(--lgm-med) var(--lgm-ease) both;animation-delay:calc(var(--i) * var(--lgm-step) + 300ms)}
.lgm-bar i{font-style:normal;font-size:13px;color:var(--lgm-mute);margin-top:8px}""")

comp("line-trend", "charts", "Đường xu hướng", "connected", "480x240",
     "Xu hướng theo thời gian — sell-out, thị phần, coverage qua các tháng",
     ["đường", "line", "xu hướng", "trend", "thời gian", "tháng", "tăng trưởng", "growth"],
     """
<div class="lgm lgm-trend">
  <div class="lgm-h">Thị phần 6 tháng</div>
  <svg viewBox="0 0 420 150" class="lgm-trend-svg">
    <line x1="0" y1="120" x2="420" y2="120" stroke="#CBC8C2" stroke-width="1"/>
    <path class="lgm-trend-p" d="M10 106 L92 96 L174 82 L256 74 L338 48 L410 30"
          fill="none" stroke="#FD312E" stroke-width="3" stroke-linecap="round"
          stroke-linejoin="round" style="--len:460"/>
    <g class="lgm-trend-dots">
      <circle cx="10" cy="106" r="4"/><circle cx="92" cy="96" r="4"/><circle cx="174" cy="82" r="4"/>
      <circle cx="256" cy="74" r="4"/><circle cx="338" cy="48" r="4"/><circle cx="410" cy="30" r="5"/>
    </g>
  </svg>
  <div class="lgm-trend-x"><span>T1</span><span>T2</span><span>T3</span><span>T4</span><span>T5</span><span>T6</span></div>
</div>""",
     """
.lgm-trend{width:480px;padding:20px 22px;background:var(--lgm-bg)}
.lgm-trend .lgm-h{font-size:19px;margin-bottom:14px}
.lgm-trend-svg{width:100%;height:150px;display:block}
.lgm-trend-p{stroke-dasharray:var(--len);animation:lgm-draw 1400ms var(--lgm-ease) both}
.lgm-trend-dots circle{fill:var(--lgm-red);opacity:0;animation:lgm-fade 300ms var(--lgm-ease) both}
.lgm-trend-dots circle:nth-child(1){animation-delay:200ms}
.lgm-trend-dots circle:nth-child(2){animation-delay:420ms}
.lgm-trend-dots circle:nth-child(3){animation-delay:640ms}
.lgm-trend-dots circle:nth-child(4){animation-delay:860ms}
.lgm-trend-dots circle:nth-child(5){animation-delay:1080ms}
.lgm-trend-dots circle:nth-child(6){animation-delay:1300ms}
.lgm-trend-x{display:flex;justify-content:space-between;font-size:13px;color:var(--lgm-mute);margin-top:6px}""")

comp("donut-share", "charts", "Vòng tỷ lệ", "connected", "260x250",
     "Một tỷ lệ duy nhất — thị phần, độ phủ, tiến độ so với mục tiêu",
     ["donut", "vòng", "tròn", "tỷ lệ", "phần trăm", "share", "thị phần", "coverage", "độ phủ"],
     """
<div class="lgm lgm-donut">
  <svg viewBox="0 0 120 120">
    <circle cx="60" cy="60" r="50" fill="none" stroke="#E6E1D6" stroke-width="12"/>
    <circle class="lgm-donut-v" cx="60" cy="60" r="50" fill="none" stroke="#FD312E" stroke-width="12"
            stroke-linecap="round" style="--len:314;--pct:.62" transform="rotate(-90 60 60)"/>
  </svg>
  <div class="lgm-donut-c"><b>62<span>%</span></b><i>độ phủ IND</i></div>
</div>""",
     """
.lgm-donut{width:260px;padding:16px;background:var(--lgm-bg);position:relative;display:grid;place-items:center}
.lgm-donut svg{width:200px;height:200px;display:block}
.lgm-donut-v{stroke-dasharray:314;stroke-dashoffset:calc(314 - 314 * var(--pct));
  animation:lgm-donut-in 1200ms var(--lgm-ease) both}
@keyframes lgm-donut-in{from{stroke-dashoffset:314}}
.lgm-donut-c{position:absolute;text-align:center;animation:lgm-fade var(--lgm-med) var(--lgm-ease) 600ms both}
.lgm-donut-c b{display:block;font-family:"LG EI Headline";font-size:44px;color:var(--lgm-ink);line-height:1}
.lgm-donut-c b span{font-size:22px}
.lgm-donut-c i{font-style:normal;font-size:13px;color:var(--lgm-mute)}""")

comp("counter-hero", "charts", "Một con số lớn", "adaptive", "420x200",
     "Slide chỉ có một con số cần đóng đinh — dùng khi con số tự nó là thông điệp",
     ["số lớn", "counter", "hero", "thống kê", "stat", "một con số", "kpi"],
     """
<div class="lgm lgm-counter">
  <span class="lgm-counter-rule"></span>
  <b>00<i>đơn vị</i></b>
  <p>THAY: một câu ngắn giải thích con số này là gì</p>
</div>""",
     """
.lgm-counter{width:420px;padding:26px 24px;background:var(--lgm-bg)}
.lgm-counter-rule{display:block;width:64px;height:5px;background:var(--lgm-red);margin-bottom:18px;
  transform-origin:left;animation:lgm-growx var(--lgm-med) var(--lgm-ease) both}
.lgm-counter b{display:block;font-family:"LG EI Headline";font-weight:600;font-size:76px;line-height:1;
  color:var(--lgm-ink);animation:lgm-rise var(--lgm-slow) var(--lgm-ease) 150ms both}
.lgm-counter b i{font-style:normal;font-family:"LG EI Text";font-size:26px;color:var(--lgm-mute);margin-left:10px}
.lgm-counter p{margin:12px 0 0;font-size:17px;color:var(--lgm-body);
  animation:lgm-rise var(--lgm-med) var(--lgm-ease) 400ms both}""")

comp("kpi-row", "charts", "Hàng ba chỉ số", "adaptive", "560x150",
     "Ba con số cạnh nhau ở đầu một slide tổng quan hoặc dashboard",
     ["kpi", "chỉ số", "ba số", "dashboard", "tổng quan", "metric", "tile"],
     """
<div class="lgm lgm-kpis">
  <div class="lgm-kpi" style="--i:0"><b>14<span>kg</span></b><i>giặt</i></div>
  <div class="lgm-kpi" style="--i:1"><b>10<span>kg</span></b><i>sấy</i></div>
  <div class="lgm-kpi lgm-kpi--hi" style="--i:2"><b>60<span>cm</span></b><i>chiều rộng</i></div>
</div>""",
     """
.lgm-kpis{width:560px;display:flex;gap:14px}
.lgm-kpi{flex:1;padding:18px;background:var(--lgm-panel-2);border-top:3px solid var(--lgm-line);
  animation:lgm-rise var(--lgm-med) var(--lgm-ease) both;animation-delay:calc(var(--i) * var(--lgm-step))}
.lgm-kpi--hi{border-top-color:var(--lgm-red)}
.lgm-kpi b{display:block;font-family:"LG EI Headline";font-size:38px;line-height:1;color:var(--lgm-ink)}
.lgm-kpi b span{font-size:18px;color:var(--lgm-body);margin-left:4px}
.lgm-kpi i{font-style:normal;font-size:13px;color:var(--lgm-body);display:block;margin-top:8px}""")

comp("progress-target", "charts", "Thanh tiến độ vs mục tiêu", "connected", "460x130",
     "Đạt bao nhiêu phần trăm kế hoạch — có mốc mục tiêu nhìn thấy được",
     ["tiến độ", "progress", "mục tiêu", "target", "kế hoạch", "plan", "đạt", "achievement"],
     """
<div class="lgm lgm-prog">
  <div class="lgm-prog-top"><span>Sell-out Q3</span><b>108%</b></div>
  <div class="lgm-prog-track"><span class="lgm-prog-fill" style="--v:108%"></span><i class="lgm-prog-mark"></i></div>
  <div class="lgm-prog-foot">mốc kế hoạch 100%</div>
</div>""",
     """
.lgm-prog{width:460px;padding:20px 22px;background:var(--lgm-bg)}
.lgm-prog-top{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:12px}
.lgm-prog-top span{font-size:15px;color:var(--lgm-body)}
.lgm-prog-top b{font-family:"LG EI Headline";font-size:26px;color:var(--lgm-ink)}
.lgm-prog-track{position:relative;height:14px;background:var(--lgm-panel);border-radius:7px;overflow:hidden}
.lgm-prog-fill{position:absolute;inset:0;width:min(var(--v),100%);background:var(--lgm-red);border-radius:7px;
  transform-origin:left;animation:lgm-growx 1100ms var(--lgm-ease) both}
.lgm-prog-mark{position:absolute;left:92.6%;top:-4px;width:2px;height:22px;background:var(--lgm-ink);
  animation:lgm-fade var(--lgm-fast) var(--lgm-ease) 900ms both}
.lgm-prog-foot{font-size:12px;color:var(--lgm-mute);margin-top:10px}""")

comp("funnel-steps", "charts", "Phễu các bước", "connected", "420x260",
     "Khách rơi ở bước nào — hành trình mua, phễu chuyển đổi",
     ["phễu", "funnel", "chuyển đổi", "conversion", "hành trình", "journey", "rơi", "drop"],
     """
<div class="lgm lgm-funnel">
  <div class="lgm-fn" style="--w:100%;--i:0"><span></span><em>Ghé cửa hàng</em><b>1.000</b></div>
  <div class="lgm-fn" style="--w:74%;--i:1"><span></span><em>Xem sản phẩm</em><b>740</b></div>
  <div class="lgm-fn" style="--w:41%;--i:2"><span></span><em>Hỏi tư vấn</em><b>410</b></div>
  <div class="lgm-fn lgm-fn--hi" style="--w:19%;--i:3"><span></span><em>Mua</em><b>190</b></div>
</div>""",
     """
.lgm-funnel{width:420px;padding:18px 20px;background:var(--lgm-bg);display:flex;flex-direction:column;gap:10px}
.lgm-fn{position:relative;display:flex;align-items:center;gap:12px;height:46px}
.lgm-fn span{position:absolute;left:0;top:0;bottom:0;width:var(--w);background:var(--lgm-panel);border-radius:4px;
  transform-origin:left;animation:lgm-growx var(--lgm-med) var(--lgm-ease) both;
  animation-delay:calc(var(--i) * 140ms)}
.lgm-fn--hi span{background:var(--lgm-red)}
.lgm-fn em,.lgm-fn b{position:relative;font-style:normal}
.lgm-fn em{font-size:14px;color:var(--lgm-body);padding-left:14px}
.lgm-fn--hi em,.lgm-fn--hi b{color:#fff}
.lgm-fn b{margin-left:auto;padding-right:12px;font-family:"LG EI Headline";font-size:17px;color:var(--lgm-ink)}""")

# ---- product and feature ----------------------------------------

comp("spec-rows", "product", "Bảng thông số cuộn ra", "adaptive", "480x230",
     "Ba đến năm dòng thông số sản phẩm, xuất hiện lần lượt",
     ["thông số", "spec", "sản phẩm", "product", "bảng", "table", "tính năng", "feature"],
     """
<div class="lgm lgm-specs">
  <div class="lgm-spec" style="--i:0"><b>00 <span>đơn vị</span></b><p>THAY: thông số thứ nhất</p></div>
  <div class="lgm-spec" style="--i:1"><b>00 <span>đơn vị</span></b><p>THAY: thông số thứ hai</p></div>
  <div class="lgm-spec" style="--i:2"><b>00 <span>đơn vị</span></b><p>THAY: thông số thứ ba</p></div>
</div>""",
     """
.lgm-specs{width:480px;padding:6px 0;background:var(--lgm-bg);border-top:2px solid var(--lgm-line)}
.lgm-spec{display:flex;align-items:baseline;gap:16px;padding:15px 4px;border-bottom:1px solid var(--lgm-line);
  animation:lgm-rise var(--lgm-med) var(--lgm-ease) both;animation-delay:calc(var(--i) * var(--lgm-step))}
.lgm-spec b{font-family:"LG EI Headline";font-size:24px;color:var(--lgm-ink);min-width:132px}
.lgm-spec b span{font-family:"LG EI Text";font-weight:400;font-size:15px;color:var(--lgm-mute)}
.lgm-spec p{margin:0;font-size:15px;color:var(--lgm-body)}""")

comp("feature-tiles", "product", "Lưới tính năng", "adaptive", "560x230",
     "Bốn tính năng ngang hàng nhau, không cái nào quan trọng hơn",
     ["tính năng", "feature", "lưới", "grid", "tile", "bốn ô", "usp"],
     """
<div class="lgm lgm-tiles">
  <div class="lgm-tile" style="--i:0"><i></i><b>THAY: tên tính năng</b><p>Một dòng mô tả</p></div>
  <div class="lgm-tile" style="--i:1"><i></i><b>THAY: tên tính năng</b><p>Một dòng mô tả</p></div>
  <div class="lgm-tile" style="--i:2"><i></i><b>THAY: tên tính năng</b><p>Một dòng mô tả</p></div>
  <div class="lgm-tile" style="--i:3"><i></i><b>THAY: tên tính năng</b><p>Một dòng mô tả</p></div>
</div>""",
     """
.lgm-tiles{width:560px;display:grid;grid-template-columns:1fr 1fr;gap:12px}
.lgm-tile{padding:16px 18px;background:var(--lgm-panel-2);
  animation:lgm-rise var(--lgm-med) var(--lgm-ease) both;animation-delay:calc(var(--i) * var(--lgm-step))}
.lgm-tile i{display:block;width:26px;height:3px;background:var(--lgm-red);margin-bottom:12px;
  transform-origin:left;animation:lgm-growx var(--lgm-fast) var(--lgm-ease) both;
  animation-delay:calc(var(--i) * var(--lgm-step) + 250ms)}
.lgm-tile b{display:block;font-family:"LG EI Headline";font-size:18px;color:var(--lgm-ink)}
.lgm-tile p{margin:6px 0 0;font-size:14px;color:var(--lgm-body)}   /* not --lgm-mute: 4.3:1 on a panel */""")

comp("compare-two", "product", "So sánh hai bên", "connected", "520x210",
     "Cách cũ so với cách LG — đặt cạnh nhau, bên phải là bên thắng",
     ["so sánh", "compare", "trước sau", "before after", "cũ mới", "vs", "đối chiếu"],
     """
<div class="lgm lgm-cmp">
  <div class="lgm-cmp-s" style="--i:0"><em>THAY: cách cũ</em><b>00</b><p>một dòng bất lợi</p></div>
  <div class="lgm-cmp-arrow"></div>
  <div class="lgm-cmp-s lgm-cmp-s--hi" style="--i:1"><em>THAY: cách của LG</em><b>00</b><p>một dòng lợi thế</p></div>
</div>""",
     """
.lgm-cmp{width:520px;display:flex;align-items:stretch;gap:0;background:var(--lgm-bg)}
.lgm-cmp-s{flex:1;padding:20px;background:var(--lgm-panel-2);
  animation:lgm-rise var(--lgm-med) var(--lgm-ease) both;animation-delay:calc(var(--i) * 220ms)}
.lgm-cmp-s--hi{background:var(--lgm-ink)}
.lgm-cmp-s em{font-style:normal;font-size:13px;color:var(--lgm-body);display:block}
.lgm-cmp-s--hi em{color:var(--lgm-line)}
.lgm-cmp-s b{display:block;font-family:"LG EI Headline";font-size:40px;line-height:1.1;color:var(--lgm-ink);margin:8px 0 6px}
.lgm-cmp-s--hi b{color:var(--lgm-red)}
.lgm-cmp-s p{margin:0;font-size:14px;color:var(--lgm-body)}
.lgm-cmp-s--hi p{color:var(--lgm-panel)}
.lgm-cmp-arrow{width:34px;align-self:center;height:2px;background:var(--lgm-line);transform-origin:left;
  animation:lgm-growx var(--lgm-fast) var(--lgm-ease) 260ms both}""")

comp("product-frame", "product", "Khung sản phẩm", "adaptive", "300x340",
     "Đặt ảnh sản phẩm cắt nền vào một tấm nền phẳng cho nó chỗ đứng",
     ["sản phẩm", "product", "khung", "frame", "nền", "panel", "ảnh", "cutout"],
     """
<div class="lgm lgm-frame">
  <div class="lgm-frame-p"></div>
  <!-- REPLACE src with the cut-out product image. The placeholder below is an inline
       Warm Gray 06 (%23E6E1D6) block so the snippet renders on its own and never points at
       a file that does not exist. -->
  <img class="lgm-frame-i" alt=""
       src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='240'%3E%3Crect width='180' height='240' rx='6' fill='%23E6E1D6'/%3E%3C/svg%3E">
</div>""",
     """
/* NOT an EI form. EI forms are fixed artwork this skill does not ship - see references/
   ei-form.md. This is a plain panel; never label it, or present it, as an EI form. */
.lgm-frame{width:300px;height:340px;position:relative;overflow:hidden;
  display:flex;align-items:flex-end;justify-content:center;padding:18px}
.lgm-frame-p{position:absolute;inset:0;background:var(--lgm-panel-2);
  transform-origin:bottom;animation:lgm-growy var(--lgm-slow) var(--lgm-ease) both}
.lgm-frame-i{position:relative;max-height:100%;max-width:100%;width:auto;height:auto;object-fit:contain;
  animation:lgm-rise var(--lgm-slow) var(--lgm-ease) 250ms both}""")

# ---- process and narrative --------------------------------------

comp("steps-flow", "process", "Chuỗi bước nối nhau", "connected", "560x140",
     "Một quy trình ba đến bốn bước, nhấn mạnh chúng nối tiếp nhau",
     ["bước", "step", "quy trình", "process", "flow", "chuỗi", "tuần tự", "roadmap"],
     """
<div class="lgm lgm-steps">
  <div class="lgm-step" style="--i:0"><span>01</span><b>Giặt</b></div>
  <div class="lgm-link" style="--i:0"></div>
  <div class="lgm-step" style="--i:1"><span>02</span><b>Chuyển</b></div>
  <div class="lgm-link" style="--i:1"></div>
  <div class="lgm-step lgm-step--hi" style="--i:2"><span>03</span><b>Sấy</b></div>
</div>""",
     """
.lgm-steps{width:560px;display:flex;align-items:center}
.lgm-step{flex:0 0 auto;padding:16px 20px;background:var(--lgm-panel-2);min-width:118px;
  animation:lgm-rise var(--lgm-med) var(--lgm-ease) both;animation-delay:calc(var(--i) * 260ms)}
.lgm-step--hi{background:var(--lgm-red)}
.lgm-step span{font-size:12px;color:var(--lgm-mute);letter-spacing:.1em}
.lgm-step--hi span{color:#fff;opacity:.8}
.lgm-step b{display:block;font-family:"LG EI Headline";font-size:20px;color:var(--lgm-ink);margin-top:6px}
.lgm-step--hi b{color:#fff}
.lgm-link{flex:1;height:2px;background:var(--lgm-line);transform-origin:left;
  animation:lgm-growx var(--lgm-fast) var(--lgm-ease) both;animation-delay:calc(var(--i) * 260ms + 180ms)}""")

comp("timeline-track", "process", "Trục thời gian", "connected", "560x160",
     "Lộ trình theo mốc thời gian — quý, tháng, giai đoạn triển khai",
     ["timeline", "trục", "thời gian", "lộ trình", "roadmap", "quý", "mốc", "milestone"],
     """
<div class="lgm lgm-tl">
  <div class="lgm-tl-line"></div>
  <div class="lgm-tl-pts">
    <div class="lgm-tl-p" style="--i:0"><i></i><b>Q1</b><p>Ra mắt</p></div>
    <div class="lgm-tl-p" style="--i:1"><i></i><b>Q2</b><p>Mở rộng MT</p></div>
    <div class="lgm-tl-p lgm-tl-p--hi" style="--i:2"><i></i><b>Q3</b><p>Phủ GT</p></div>
    <div class="lgm-tl-p" style="--i:3"><i></i><b>Q4</b><p>Tổng kết</p></div>
  </div>
</div>""",
     """
.lgm-tl{width:560px;padding:18px 8px;position:relative}
.lgm-tl-line{position:absolute;left:8px;right:8px;top:34px;height:2px;background:var(--lgm-line);
  transform-origin:left;animation:lgm-growx 1000ms var(--lgm-ease) both}
.lgm-tl-pts{display:flex;justify-content:space-between;position:relative}
.lgm-tl-p{flex:1;text-align:center;animation:lgm-fade var(--lgm-med) var(--lgm-ease) both;
  animation-delay:calc(var(--i) * 200ms + 300ms)}
.lgm-tl-p i{display:block;width:12px;height:12px;border-radius:50%;background:var(--lgm-line);margin:11px auto 14px}
.lgm-tl-p--hi i{background:var(--lgm-red);width:16px;height:16px;margin-top:9px}
.lgm-tl-p b{font-family:"LG EI Headline";font-size:17px;color:var(--lgm-ink)}
.lgm-tl-p p{margin:4px 0 0;font-size:13px;color:var(--lgm-mute)}""")

comp("pillars-three", "process", "Ba trụ cột", "adaptive", "540x200",
     "Ba ý ngang hàng làm xương sống cho một thông điệp",
     ["trụ cột", "pillar", "ba ý", "three", "giá trị", "value", "cột"],
     """
<div class="lgm lgm-pil">
  <div class="lgm-pil-c" style="--i:0"><span></span><b>Uncompromising</b><p>Chất lượng không thoả hiệp</p></div>
  <div class="lgm-pil-c" style="--i:1"><span></span><b>Human-centered</b><p>Đổi mới lấy con người làm gốc</p></div>
  <div class="lgm-pil-c" style="--i:2"><span></span><b>Warmth</b><p>Ấm áp tạo nên nụ cười</p></div>
</div>""",
     """
.lgm-pil{width:540px;display:flex;gap:16px}
.lgm-pil-c{flex:1;animation:lgm-rise var(--lgm-med) var(--lgm-ease) both;animation-delay:calc(var(--i) * 130ms)}
.lgm-pil-c span{display:block;height:4px;background:var(--lgm-red);margin-bottom:14px;transform-origin:left;
  animation:lgm-growx var(--lgm-med) var(--lgm-ease) both;animation-delay:calc(var(--i) * 130ms + 200ms)}
.lgm-pil-c b{display:block;font-family:"LG EI Headline";font-size:19px;color:var(--lgm-ink)}
.lgm-pil-c p{margin:8px 0 0;font-size:14px;color:var(--lgm-body);line-height:1.5}""")

# ---- type and structure -----------------------------------------

comp("headline-rise", "type", "Tiêu đề hiện lên", "adaptive", "560x200",
     "Mở đầu một slide hoặc một trang — eyebrow, gạch đỏ, tiêu đề, câu đỡ",
     ["tiêu đề", "headline", "mở đầu", "opener", "title", "eyebrow", "chữ"],
     """
<div class="lgm lgm-hl">
  <span class="lgm-hl-rule"></span>
  <p class="lgm-hl-eb">THAY: dòng định danh</p>
  <h2 class="lgm-h">THAY: tiêu đề,<br>ngắn và <em>cụ thể</em>.</h2>
  <p class="lgm-hl-sub">THAY: một câu đỡ.</p>
</div>""",
     """
.lgm-hl{width:560px}
.lgm-hl-rule{display:block;width:84px;height:5px;background:var(--lgm-red);transform-origin:left;
  animation:lgm-growx var(--lgm-med) var(--lgm-ease) both}
.lgm-hl-eb{margin:16px 0 10px;font-family:"LG EI Text";font-weight:600;font-size:14px;letter-spacing:.06em;
  text-transform:uppercase;color:var(--lgm-red);animation:lgm-rise var(--lgm-med) var(--lgm-ease) 150ms both}
.lgm-hl h2{font-size:46px;line-height:1.1;animation:lgm-rise var(--lgm-slow) var(--lgm-ease) 260ms both}
.lgm-hl h2 em{font-style:normal;color:var(--lgm-heritage)}
.lgm-hl-sub{margin:14px 0 0;font-size:17px;color:var(--lgm-body);
  animation:lgm-rise var(--lgm-med) var(--lgm-ease) 460ms both}""")

comp("quote-pull", "type", "Trích dẫn", "adaptive", "480x180",
     "Một câu của khách hàng hoặc lãnh đạo, tách ra khỏi phần còn lại",
     ["trích dẫn", "quote", "câu nói", "testimonial", "khách hàng", "phát biểu"],
     """
<div class="lgm lgm-quote">
  <span class="lgm-quote-bar"></span>
  <blockquote>Một tháp thay cho hai máy, và cái bảng điều khiển vừa tầm tay là thứ khách nhớ nhất.</blockquote>
  <cite>Quản lý cửa hàng, kênh MT</cite>
</div>""",
     """
.lgm-quote{width:480px;padding-left:22px;position:relative}
.lgm-quote-bar{position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--lgm-red);transform-origin:top;
  animation:lgm-growy var(--lgm-med) var(--lgm-ease) both}
.lgm-quote blockquote{margin:0;font-family:"LG EI Headline";font-weight:400;font-size:24px;line-height:1.45;
  color:var(--lgm-ink);animation:lgm-rise var(--lgm-slow) var(--lgm-ease) 180ms both}
.lgm-quote cite{display:block;margin-top:14px;font-style:normal;font-size:14px;color:var(--lgm-mute);
  animation:lgm-fade var(--lgm-med) var(--lgm-ease) 500ms both}""")

comp("grid-reveal", "type", "Lưới 9×9 hiện ra", "connected", "480x270",
     "Giải thích hệ lưới LG cho người xem, hoặc làm nền cấu trúc cho một slide mở",
     ["lưới", "grid", "hệ thống", "system", "margin", "cấu trúc", "structure", "9x9"],
     """
<div class="lgm lgm-grid">
  <div class="lgm-grid-cols"><i style="--i:0"></i><i style="--i:1"></i><i style="--i:2"></i><i style="--i:3"></i>
    <i style="--i:4"></i><i style="--i:5"></i><i style="--i:6"></i><i style="--i:7"></i><i style="--i:8"></i></div>
  <div class="lgm-grid-rows"><u style="--i:0"></u><u style="--i:1"></u><u style="--i:2"></u><u style="--i:3"></u>
    <u style="--i:4"></u><u style="--i:5"></u><u style="--i:6"></u><u style="--i:7"></u><u style="--i:8"></u></div>
  <div class="lgm-grid-m"></div>
  <div class="lgm-grid-t">margin 5% &middot; 9 &times; 9 &middot; gutter &frac12; margin</div>
</div>""",
     """
/* The margin is 5% of the shortest edge: 13.5px on a 270px-tall canvas. Gutter is half of
   that. Drawn faintly, because the point is to show the structure, not to decorate with it. */
.lgm-grid{width:480px;height:270px;position:relative;background:var(--lgm-bg);overflow:hidden}
.lgm-grid-m{position:absolute;inset:13.5px;outline:1px dashed rgba(253,49,46,.75);
  animation:lgm-fade var(--lgm-med) var(--lgm-ease) 700ms both}
.lgm-grid-cols,.lgm-grid-rows{position:absolute;inset:13.5px;display:flex}
.lgm-grid-cols{gap:6.75px}
.lgm-grid-rows{flex-direction:column;gap:6.75px}
.lgm-grid-cols i{flex:1;background:rgba(38,38,38,.05);transform-origin:top;
  animation:lgm-growy var(--lgm-fast) var(--lgm-ease) both;animation-delay:calc(var(--i) * 55ms)}
.lgm-grid-rows u{flex:1;border-top:1px solid rgba(38,38,38,.09);transform-origin:left;
  animation:lgm-growx var(--lgm-fast) var(--lgm-ease) both;animation-delay:calc(var(--i) * 55ms + 300ms)}
.lgm-grid-t{position:absolute;left:13.5px;bottom:-2px;font-size:11px;color:var(--lgm-mute);
  letter-spacing:.04em;animation:lgm-fade var(--lgm-med) var(--lgm-ease) 900ms both}""")

comp("loading-dots", "state", "Ba chấm chờ", "fluid", "120x40",
     "Trạng thái đang xử lý trong một giao diện — dùng rất tiết chế",
     ["loading", "chờ", "đang xử lý", "spinner", "state", "trạng thái", "chấm"],
     """
<div class="lgm lgm-dots"><i></i><i></i><i></i></div>""",
     """
.lgm-dots{width:120px;height:40px;display:flex;align-items:center;justify-content:center;gap:9px}
.lgm-dots i{width:10px;height:10px;border-radius:50%;background:var(--lgm-red);
  animation:lgm-pulse 1400ms var(--lgm-ease) infinite}
.lgm-dots i:nth-child(2){animation-delay:180ms}
.lgm-dots i:nth-child(3){animation-delay:360ms}""")

comp("ambient-dots", "state", "Nền chấm trôi", "fluid", "480x270",
     "Nền tĩnh cần một chút sống — chỉ dùng khi KHÔNG dùng gradient chính thức",
     ["nền", "background", "ambient", "trôi", "drift", "sống động", "backdrop"],
     """
<div class="lgm lgm-amb">
  <i style="--x:12%;--y:22%;--d:0s"></i><i style="--x:74%;--y:16%;--d:.9s"></i>
  <i style="--x:38%;--y:68%;--d:.4s"></i><i style="--x:86%;--y:74%;--d:1.3s"></i>
  <i style="--x:58%;--y:44%;--d:.7s"></i>
</div>""",
     """
/* Deliberately NOT a gradient. LG's four master gradients are fixed artwork that may not be
   altered or recreated, and animating one counts as altering it. This is flat palette tone
   only, and it never goes where a brand gradient belongs. */
.lgm-amb{width:480px;height:270px;position:relative;background:var(--lgm-bg);overflow:hidden}
.lgm-amb i{position:absolute;left:var(--x);top:var(--y);width:44px;height:44px;border-radius:50%;
  background:var(--lgm-panel);animation:lgm-drift 5s ease-in-out infinite;animation-delay:var(--d)}""")

# ---------------------------------------------------------------- emit


def build():
    os.makedirs(OUT, exist_ok=True)
    ids = [c["id"] for c in C]
    assert len(ids) == len(set(ids)), "duplicate component id"

    store = {"base_css": BASE.strip(), "components": {c["id"]: c for c in C}}
    json.dump(store, open(f"{OUT}/components.json", "w"), ensure_ascii=False, indent=1)

    index = [{k: c[k] for k in ("id", "cat", "name", "family", "size", "use", "tags", "pri")}
             for c in C]
    json.dump(index, open(f"{OUT}/index.json", "w"), ensure_ascii=False, indent=1)

    cats = {}
    for c in C:
        cats.setdefault(c["cat"], []).append(c)
    titles = {"charts": "Biểu đồ", "product": "Sản phẩm & tính năng",
              "process": "Quy trình & tường thuật", "type": "Chữ & cấu trúc",
              "state": "Trạng thái & nền"}
    lines = [f"# LG Motion Kit — bảng tra cứu\n",
             f"{len(C)} component, chia theo ba họ chuyển động của LG: "
             f"**adaptive** (xuất hiện có thứ tự), **connected** (vẽ quan hệ), "
             f"**fluid** (liên tục, dùng tiết chế).\n",
             "Chọn ở đây rồi `python3 scripts/lg_motion.py get <id>`. "
             "Nhanh hơn: `lg_motion.py search \"<việc cần làm>\"`.\n"]
    for cat, items in cats.items():
        lines.append(f"\n## {titles.get(cat, cat)}\n")
        lines.append("| id | họ | khổ | dùng khi | từ khoá |")
        lines.append("|---|---|---|---|---|")
        for c in sorted(items, key=lambda x: x["id"]):
            lines.append(f"| `{c['id']}` | {c['family']} | {c['size']} | {c['use']} | "
                         f"{', '.join(c['tags'][:6])} |")
    open(f"{OUT}/CATALOG.md", "w", encoding="utf-8").write("\n".join(lines) + "\n")

    # gallery for human eyes; never read this with a file tool
    g = ['<!doctype html><html lang="vi"><head><meta charset="utf-8">',
         '<title>LG Motion Kit</title>',
         '<link rel="stylesheet" href="../../templates/lg-tokens.css">',
         f'<style>{BASE}',
         'body{background:#F6F3EB;padding:40px;font-family:"LG EI Text",sans-serif}',
         'h1{font-family:"LG EI Headline";font-size:32px;color:#262626}',
         '.wrap{display:flex;flex-wrap:wrap;gap:28px;margin-top:24px}',
         '.card{background:#fff;padding:18px;border:1px solid #E6E1D6}',
         '.card h3{font-family:"LG EI Text";font-size:13px;color:#716F6A;margin:0 0 12px;font-weight:600}',
         "\n".join(c["css"] for c in C),
         '</style></head><body>',
         '<h1>LG Motion Kit</h1>',
         f'<p style="color:#4A4946">{len(C)} component · palette và chữ theo BI Guidelines V5.2 · '
         'ba họ chuyển động Adaptive / Connected / Fluid</p>',
         '<div class="wrap">']
    for c in C:
        g.append(f'<div class="card"><h3>{c["id"]} · {c["family"]}</h3>{c["html"]}</div>')
    g.append('</div></body></html>')
    open(f"{OUT}/gallery.html", "w", encoding="utf-8").write("\n".join(g))

    print(f"built {len(C)} components -> {os.path.relpath(OUT, SKILL)}")
    for f in ("components.json", "index.json", "CATALOG.md", "gallery.html"):
        print(f"  {f:<18} {os.path.getsize(f'{OUT}/{f}')//1024:>4} KB")


if __name__ == "__main__":
    build()
