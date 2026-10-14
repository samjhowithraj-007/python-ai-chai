"""Writes compositions/frames/NN-*.html (one <template> sub-composition each) from the storyboard's shot sequences.
Shared look from frame.md's channel override: ink ground + stove glow + faint grid, cream text, cyan keywords,
amber chai, DM Sans 700 labels, JetBrains Mono code cards. Typing = a monospace line revealed by width in ch
with a steps() ease (one tween per line, seek-safe)."""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "compositions", "frames")
os.makedirs(OUT, exist_ok=True)

INK, CREAM, CYAN, AMBER, NAVY = "#0E1116", "#F5F1E8", "#0AF0F0", "#FFB020", "#181715"


def css(fid):
    p = fid
    return f"""
<style>
  @font-face {{ font-family:"DM Sans"; font-weight:400; src:url("assets/fonts/DMSans-400.woff2") format("woff2"); }}
  @font-face {{ font-family:"DM Sans"; font-weight:700; src:url("assets/fonts/DMSans-700.woff2") format("woff2"); }}
  @font-face {{ font-family:"JetBrains Mono"; font-weight:400; src:url("assets/fonts/JetBrainsMono-400.woff2") format("woff2"); }}
  @font-face {{ font-family:"JetBrains Mono"; font-weight:700; src:url("assets/fonts/JetBrainsMono-700.woff2") format("woff2"); }}
  #root {{ position:absolute; inset:0; width:1080px; height:1080px; overflow:hidden; color:{CREAM};
          font-family:"DM Sans", ui-sans-serif, system-ui, sans-serif; }}
  .{p}-bg {{ position:absolute; inset:0; background:
      radial-gradient(70% 45% at 50% 108%, rgba(255,176,32,.30), rgba(255,176,32,0) 70%),
      radial-gradient(60% 50% at 15% 0%, rgba(10,240,240,.10), rgba(10,240,240,0) 70%), {INK}; }}
  .{p}-grid {{ position:absolute; inset:0; opacity:.18; background-image:
      linear-gradient(rgba(245,241,232,.10) 1px, transparent 1px), linear-gradient(90deg, rgba(245,241,232,.10) 1px, transparent 1px);
      background-size:72px 72px; }}
  .{p}-stage {{ position:absolute; inset:0; transform-origin:50% 40%; }}
  .{p}-h {{ position:absolute; left:0; right:0; text-align:center; font-weight:700; letter-spacing:-.02em; line-height:1.05; }}
  .{p}-c {{ color:{CYAN}; text-shadow:0 0 24px rgba(10,240,240,.45); }}
  .{p}-a {{ color:{AMBER}; text-shadow:0 0 24px rgba(255,176,32,.35); }}
  .{p}-w {{ display:inline-block; }}
  .{p}-card {{ position:absolute; background:{NAVY}; border:1px solid rgba(245,241,232,.14); border-radius:12px;
      box-shadow:0 24px 70px rgba(0,0,0,.45); padding:64px 40px 30px; box-sizing:border-box;
      font-family:"JetBrains Mono", ui-monospace, monospace; }}
  .{p}-dots {{ position:absolute; left:22px; top:22px; display:flex; gap:9px; }}
  .{p}-dots i {{ width:13px; height:13px; border-radius:50%; background:rgba(245,241,232,.22); display:block; }}
  .{p}-file {{ position:absolute; right:24px; top:16px; font-size:22px; color:rgba(245,241,232,.66); }}
  .{p}-ln {{ display:block; white-space:pre; overflow:hidden; width:0ch; line-height:1.6; }}
  .{p}-k {{ color:{CYAN}; }} .{p}-s {{ color:{AMBER}; }} .{p}-n {{ color:#FF8FA3; }} .{p}-f {{ color:#B8F5A0; }}
  .{p}-kick {{ position:absolute; left:0; right:0; text-align:center; font-family:"JetBrains Mono", monospace;
      font-weight:700; font-size:26px; letter-spacing:.18em; color:rgba(245,241,232,.62); }}
  .{p}-pill {{ position:absolute; display:flex; align-items:center; gap:14px; padding:0 30px; height:76px; border-radius:9999px;
      font-weight:700; font-size:34px; box-sizing:border-box; }}
</style>"""


def shell(fid, dur, body, js):
    return f"""<template>
{css(fid)}
<div id="root" data-composition-id="{fid}" data-width="1080" data-height="1080">
  <div class="clip {fid}-bg" id="{fid}-bg" data-start="0" data-duration="{dur}" data-track-index="0"><div class="{fid}-grid"></div></div>
  <div class="clip {fid}-stage" id="{fid}-stage" data-start="0" data-duration="{dur}" data-track-index="1">
{body}
  </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script>
(function () {{
  const tl = gsap.timeline({{ paused: true }});
  const q = (s) => document.querySelector(s);
  tl.fromTo("#{fid}-stage", {{ scale: 1.0 }}, {{ scale: 1.04, duration: {dur}, ease: "none" }}, 0);
{js}
  window.__timelines = window.__timelines || {{}};
  window.__timelines["{fid}"] = tl;
}})();
</script>
</template>
"""


def words(fid, text, cls_map=None):
    """Hero line as word spans (rise in staggered). cls_map: {word_index: class}."""
    out = []
    for i, w in enumerate(text.split(" ")):
        c = (" " + cls_map[i]) if cls_map and i in cls_map else ""
        out.append(f'<span class="{fid}-w{c}">{w}</span>')
    return " ".join(out)


def rise(sel, t, stagger=0.06):
    return (f'  tl.fromTo("{sel}", {{ opacity: 0, y: 34 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out", '
            f'stagger: {stagger} }}, {t:.2f});')


def code_line(fid, i, html):
    n = len(re.sub(r"<[^>]+>", "", html).replace("&quot;", '"').replace("&lt;", "<").replace("&gt;", ">"))
    return f'<span class="{fid}-ln" id="{fid}-l{i}" data-n="{n}">{html}</span>', n


def type_line(fid, i, n, t, dur):
    return (f'  tl.fromTo("#{fid}-l{i}", {{ width: "0ch" }}, {{ width: "{n}ch", duration: {dur:.2f}, '
            f'ease: "steps({n})" }}, {t:.2f});')


def card(fid, lines, style, fname="chai.py"):
    spans, ns = [], []
    for i, h in enumerate(lines):
        s, n = code_line(fid, i, h); spans.append(s); ns.append(n)
    html = (f'    <div class="{fid}-card" id="{fid}-card" style="{style}"><div class="{fid}-dots"><i></i><i></i><i></i></div>'
            f'<div class="{fid}-file">{fname}</div>' + "".join(spans) + "</div>")
    return html, ns


def cup_svg(fid, w, extra_style=""):
    # line-art chai glass: body, handle, saucer, chai fill, three steam curls (drawn by dash offset)
    return f"""    <svg id="{fid}-cup" viewBox="0 0 300 300" width="{w}" height="{w}" style="position:absolute;{extra_style}" fill="none">
      <path id="{fid}-fill" d="M78 150 L222 150 L210 252 Q208 262 198 262 L102 262 Q92 262 90 252 Z" fill="{AMBER}" opacity=".85"/>
      <path d="M70 128 L230 128 L212 254 Q209 270 194 270 L106 270 Q91 270 88 254 Z" stroke="{CREAM}" stroke-width="7" stroke-linejoin="round"/>
      <path d="M228 160 Q268 160 266 196 Q264 228 220 230" stroke="{CREAM}" stroke-width="7" stroke-linecap="round"/>
      <path d="M40 284 L260 284" stroke="{CREAM}" stroke-width="7" stroke-linecap="round" opacity=".7"/>
      <path class="{fid}-steam" d="M115 108 Q100 88 115 68 Q130 48 115 28" stroke="{CREAM}" stroke-width="6" stroke-linecap="round" opacity=".75" stroke-dasharray="100" stroke-dashoffset="100"/>
      <path class="{fid}-steam" d="M150 108 Q135 88 150 68 Q165 48 150 28" stroke="{CREAM}" stroke-width="6" stroke-linecap="round" opacity=".75" stroke-dasharray="100" stroke-dashoffset="100"/>
      <path class="{fid}-steam" d="M185 108 Q170 88 185 68 Q200 48 185 28" stroke="{CREAM}" stroke-width="6" stroke-linecap="round" opacity=".75" stroke-dasharray="100" stroke-dashoffset="100"/>
    </svg>"""


def steam_js(fid, t):
    return (f'  tl.fromTo("#{fid}-cup .{fid}-steam", {{ strokeDashoffset: 100 }}, {{ strokeDashoffset: 0, duration: 1.1, '
            f'ease: "power2.out", stagger: 0.18 }}, {t:.2f});')


def write(fid, dur, body, js):
    # element ids/classes get an "f" prefix (an id starting with a digit is an invalid CSS/GSAP selector);
    # the composition id and timeline key stay the bare frame id
    html = shell(fid, dur, body, "\n".join(js)).replace(fid + "-", "f" + fid + "-")
    open(os.path.join(OUT, fid + ".html"), "w", encoding="utf-8").write(html)


FLAV = [("Masala", "#C8782A"), ("Adrak", "#E8C26A"), ("Elaichi", "#8CCB7E"), ("Tulsi", "#5FB37A")]


def mini_cup(tint, size):
    return (f'<svg viewBox="0 0 300 300" width="{size}" height="{size}" fill="none">'
            f'<path d="M78 150 L222 150 L210 252 Q208 262 198 262 L102 262 Q92 262 90 252 Z" fill="{tint}"/>'
            f'<path d="M70 128 L230 128 L212 254 Q209 270 194 270 L106 270 Q91 270 88 254 Z" stroke="{CREAM}" stroke-width="12" stroke-linejoin="round"/>'
            f'<path d="M228 160 Q268 160 266 196 Q264 228 220 230" stroke="{CREAM}" stroke-width="12" stroke-linecap="round"/></svg>')


def slot(fid, i, left, top, w, h, filled=True):
    name, tint = FLAV[i]
    return (f'<div id="{fid}-s{i}" style="position:absolute;left:{left}px;top:{top}px;width:{w}px;height:{h}px;border-radius:20px;'
            f'border:3px dashed rgba(245,241,232,.35);box-sizing:border-box"></div>'
            f'<div id="{fid}-c{i}" style="position:absolute;left:{left}px;top:{top}px;width:{w}px;height:{h}px;border-radius:20px;background:{NAVY};'
            f'border:3px solid {tint};box-sizing:border-box;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px">'
            f'{mini_cup(tint, int(h * 0.5))}<div style="font-size:{int(h * 0.2)}px;color:{CREAM}">{name}</div></div>')


def index_label(fid, i, cx, top):
    return (f'<div id="{fid}-ix{i}" style="position:absolute;left:{cx - 40}px;top:{top}px;width:80px;text-align:center;font-family:\'JetBrains Mono\',monospace;'
            f'font-weight:700;font-size:44px;color:{CYAN}">{i}</div>')


def outstrip(fid, oid, text, left, top, width):
    return (f'<div id="{fid}-{oid}" style="position:absolute;left:{left}px;top:{top}px;width:{width}px;height:96px;border-radius:12px;background:rgba(255,176,32,.12);'
            f'border:2px solid {AMBER};font-family:\'JetBrains Mono\',monospace;font-size:46px;color:{AMBER};display:flex;align-items:center;padding-left:30px;'
            f'box-sizing:border-box">&gt; {text}</div>')


ROSE = "#FF8FA3"
CHECK = (f'<svg width="30" height="30" viewBox="0 0 30 30" style="flex:none"><circle cx="15" cy="15" r="14" fill="{CYAN}"/>'
         f'<path d="M8 15.5 L13 20.5 L22 10" stroke="{INK}" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def tag(fid, i, text):
    return (f'<div id="{fid}-tag{i}" style="display:inline-flex;align-items:center;gap:12px;height:70px;padding:0 28px;border-radius:9999px;'
            f'border:3px solid rgba(245,241,232,.35);background:rgba(14,17,22,.6);font-family:\'JetBrains Mono\',monospace;font-size:32px;color:{CREAM}">'
            f'<span id="{fid}-tk{i}" style="display:inline-flex;opacity:0">{CHECK}</span>{text}</div>')


def tags_row(fid, texts, top):
    return (f'<div style="position:absolute;left:0;right:0;top:{top}px;display:flex;justify-content:center;gap:22px">'
            + "".join(tag(fid, i, t) for i, t in enumerate(texts)) + '</div>')


def tag_js(fid, i, t):
    return [f'  tl.fromTo("#{fid}-tag{i}", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }}, {t:.2f});',
            f'  tl.fromTo("#{fid}-tk{i}", {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "power3.out" }}, {t + 0.35:.2f});',
            f'  tl.fromTo("#{fid}-tag{i}", {{ borderColor: "rgba(245,241,232,.35)" }}, {{ borderColor: "rgba(10,240,240,.9)", duration: 0.3, immediateRender: false }}, {t + 0.35:.2f});']


def stack(fid, sid, values, style):
    spans = "".join(f'<span id="{fid}-{sid}{k}" style="position:absolute;left:0;right:0;text-align:center;opacity:{1 if k == 0 else 0}">{v}</span>'
                    for k, v in enumerate(values))
    return f'<div style="position:absolute;{style}">{spans}</div>'


# ---- Frame 1: hook (4s) ----
f = "01-hook"
chips = ["function", "if-else", "list", "for loop", "dictionary"]
row1 = "".join(f'<div id="{f}-ch{i}" style="display:inline-flex;align-items:center;height:84px;padding:0 34px;border-radius:9999px;background:rgba(10,240,240,.12);'
               f'border:3px solid {CYAN};color:{CYAN};font-family:\'JetBrains Mono\',monospace;font-size:40px">{c}</div>' for i, c in enumerate(chips))
body = f"""    <div class="{f}-kick" id="{f}-kick" style="top:100px">PART 7 · FINALE · SAMJHO WITH RAJ</div>
    <div class="{f}-h" id="{f}-t1" style="top:180px;font-size:100px">{words(f, "Chai ka", {})}</div>
    <div class="{f}-h" id="{f}-t2" style="top:290px;font-size:170px">{words(f, "BILL banao!", {0: f + "-a"})}</div>
    <div style="position:absolute;left:80px;width:920px;top:540px;display:flex;flex-wrap:wrap;justify-content:center;gap:24px">{row1}</div>
    <div class="{f}-h" id="{f}-sub" style="top:790px;font-size:56px;color:rgba(245,241,232,.85)">Sab kuch <span class="{f}-a">ek saath!</span></div>"""
js = [f'  tl.fromTo("#{f}-kick", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, 0.05);',
      rise(f"#{f}-t1 .{f}-w", 0.2, 0.1), rise(f"#{f}-t2 .{f}-w", 0.5, 0.15)]
for i in range(5):
    js.append(f'  tl.fromTo("#{f}-ch{i}", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "power3.out" }}, {1.4 + i * 0.3:.2f});')
js.append(f'  tl.fromTo("#{f}-sub", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, 3.0);')
write(f, 4, body, js)

# ---- Frame 2: order (6s) ----
f = "02-order"
lines = [f'menu = {{<span class="{f}-k">"Masala"</span>: <span class="{f}-s">20</span>, <span class="{f}-k">"Adrak"</span>: <span class="{f}-s">15</span>}}',
         f'order = [<span class="{f}-k">"Masala"</span>, <span class="{f}-k">"Adrak"</span>, <span class="{f}-k">"Masala"</span>]']
cardh, ns = card(f, lines, "left:50px;top:210px;width:980px;height:203px;font-size:34px")
ORD = ["Masala", "Adrak", "Masala"]
cups = "".join(f'<div id="{f}-cup{i}" style="position:absolute;left:{190 + i * 260}px;top:450px;width:180px;text-align:center">'
               f'{mini_cup(dict(FLAV)[n], 150)}<div style="font-size:40px;color:{CREAM}">{n}</div></div>' for i, n in enumerate(ORD))
body = f"""    <div class="{f}-h" id="{f}-head" style="top:84px;font-size:84px">{words(f, "Order lo!", {0: f + "-a"})}</div>
{cardh}
    {cups}
    {tags_row(f, ["dictionary", "list"], 770)}"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.1),
      f'  tl.fromTo("#{f}-card", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.3);',
      type_line(f, 0, ns[0], 1.0, 1.0), type_line(f, 1, ns[1], 2.2, 1.0)]
for i in range(3):
    js.append(f'  tl.fromTo("#{f}-cup{i}", {{ opacity: 0, y: 40, scale: 0.8 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.4, ease: "power3.out" }}, {3.4 + i * 0.35:.2f});')
js += tag_js(f, 0, 4.4) + tag_js(f, 1, 4.8)
write(f, 6, body, js)

# ---- Frame 3: loop total (8s) ----
f = "03-total"
lines = [f'<span class="{f}-k">def</span> <span class="{f}-f">bill</span>(order):',
         f'    total = <span class="{f}-n">0</span>',
         f'    <span class="{f}-k">for</span> item <span class="{f}-k">in</span> order:',
         f'        total += menu[item]']
cardh, ns = card(f, lines, "left:40px;top:180px;width:670px;height:300px;font-size:32px")
CX = [170 + i * 280 for i in range(3)]
cups = "".join(f'<div id="{f}-cup{i}" style="position:absolute;left:{CX[i]}px;top:540px;width:180px;text-align:center">'
               f'{mini_cup(dict(FLAV)[n], 120)}<div style="font-size:36px;color:{CREAM}">{n}</div></div>' for i, n in enumerate(ORD))
plus = "".join(f'<div id="{f}-plus{i}" style="position:absolute;left:{CX[i]}px;width:180px;top:520px;text-align:center;font-family:\'JetBrains Mono\',monospace;'
               f'font-weight:700;font-size:44px;color:{AMBER};opacity:0">+{PR}</div>' for i, PR in enumerate([20, 15, 20]))
body = f"""    <div class="{f}-h" id="{f}-head" style="top:70px;font-size:80px">{words(f, "Loop se total", {2: f + "-a"})}</div>
{cardh}
    <div id="{f}-panel" style="position:absolute;left:740px;top:180px;width:300px;height:300px;border-radius:14px;background:{NAVY};
         border:2px solid rgba(255,176,32,.5);box-sizing:border-box">
      <div style="position:absolute;left:0;right:0;top:30px;text-align:center;font-family:'JetBrains Mono',monospace;font-size:32px;color:rgba(245,241,232,.7)">total</div>
      {stack(f, "t", [0, 20, 35, 55], f"left:0;right:0;top:90px;height:170px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:130px;color:{AMBER};line-height:170px")}
    </div>
    <div id="{f}-ring" style="position:absolute;left:{CX[0] - 10}px;top:525px;width:200px;height:200px;border-radius:26px;border:6px solid {CYAN};
         box-shadow:0 0 40px rgba(10,240,240,.6);box-sizing:border-box;opacity:0"></div>
    {cups}
    {plus}
    {tags_row(f, ["function", "for loop"], 790)}"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.1),
      f'  tl.fromTo("#{f}-card", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.2);',
      f'  tl.fromTo("#{f}-panel", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.35);',
      f'  tl.fromTo(["#{f}-cup0", "#{f}-cup1", "#{f}-cup2"], {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power3.out", stagger: 0.1 }}, 0.5);']
for i in range(4):
    js.append(type_line(f, i, ns[i], 0.6 + i * 0.3, 0.4))
for i in range(3):
    t = 2.0 + i * 1.4
    if i == 0:
        js.append(f'  tl.fromTo("#{f}-ring", {{ opacity: 0, scale: 1.15 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "power3.out" }}, {t:.2f});')
    else:
        js.append(f'  tl.to("#{f}-ring", {{ x: {CX[i] - CX[0]}, duration: 0.45, ease: "power2.inOut" }}, {t - 0.2:.2f});')
    js.append(f'  tl.fromTo("#{f}-plus{i}", {{ opacity: 0, y: 0 }}, {{ opacity: 1, y: -60, duration: 0.5, ease: "power2.out" }}, {t + 0.25:.2f});')
    js.append(f'  tl.to("#{f}-plus{i}", {{ opacity: 0, duration: 0.3 }}, {t + 0.9:.2f});')
    js.append(f'  tl.set("#{f}-t{i}", {{ opacity: 0 }}, {t + 0.5:.2f});')
    js.append(f'  tl.set("#{f}-t{i + 1}", {{ opacity: 1 }}, {t + 0.5:.2f});')
    js.append(f'  tl.fromTo("#{f}-l3", {{ textShadow: "0 0 0 rgba(10,240,240,0)" }}, {{ textShadow: "0 0 24px rgba(10,240,240,.95)", duration: 0.25, immediateRender: false }}, {t + 0.3:.2f});')
    js.append(f'  tl.to("#{f}-l3", {{ textShadow: "0 0 0 rgba(10,240,240,0)", duration: 0.35 }}, {t + 0.7:.2f});')
js += tag_js(f, 0, 6.3) + tag_js(f, 1, 6.7)
write(f, 8, body, js)

# ---- Frame 4: discount (7s) ----
f = "04-discount"
lines = [f'    <span class="{f}-k">if</span> total &gt; <span class="{f}-n">50</span>:',
         f'        total -= <span class="{f}-n">5</span>',
         f'    <span class="{f}-k">return</span> total']
cardh, ns = card(f, lines, "left:60px;top:180px;width:960px;height:286px;font-size:40px")
body = f"""    <div class="{f}-h" id="{f}-head" style="top:70px;font-size:80px">{words(f, "if-else: discount!", {0: f + "-c", 1: f + "-a"})}</div>
{cardh}
    <div id="{f}-big" style="position:absolute;left:300px;top:500px;width:400px;height:240px">
      <div style="position:absolute;left:0;right:0;top:0;text-align:center;font-family:'JetBrains Mono',monospace;font-size:40px;color:rgba(245,241,232,.75)">total</div>
      {stack(f, "b", [55, 50], f"left:0;right:0;top:50px;height:180px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:160px;color:{AMBER};line-height:180px")}
    </div>
    <div id="{f}-v" style="position:absolute;left:740px;top:540px;width:250px;padding:18px 0;border-radius:16px;text-align:center;border:3px solid {CYAN};
         background:rgba(14,17,22,.85);color:{CYAN};font-family:'JetBrains Mono',monospace;font-weight:700;font-size:38px;line-height:1.35">55 &gt; 50<br>True</div>
    <div id="{f}-stamp" style="position:absolute;left:110px;top:540px;width:170px;height:170px;border-radius:50%;border:6px solid {ROSE};color:{ROSE};
         display:flex;align-items:center;justify-content:center;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:64px;background:rgba(255,143,163,.10)">-5</div>
    {tags_row(f, ["if-else"], 790)}"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.1),
      f'  tl.fromTo("#{f}-card", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.3);']
for i in range(3):
    js.append(type_line(f, i, ns[i], 1.0 + i * 0.6, 0.5))
js += [f'  tl.fromTo("#{f}-big", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "power3.out" }}, 1.6);',
       f'  tl.fromTo("#{f}-v", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "power3.out" }}, 2.6);',
       f'  tl.fromTo("#{f}-stamp", {{ opacity: 0, scale: 1.8, rotation: -30 }}, {{ opacity: 1, scale: 1, rotation: -12, duration: 0.35, ease: "power3.out" }}, 3.6);',
       f'  tl.set("#{f}-b0", {{ opacity: 0 }}, 4.1);',
       f'  tl.set("#{f}-b1", {{ opacity: 1 }}, 4.1);',
       f'  tl.fromTo("#{f}-big", {{ scale: 1.12 }}, {{ scale: 1, duration: 0.4, ease: "power2.out", immediateRender: false }}, 4.1);']
js += tag_js(f, 0, 5.0)
write(f, 7, body, js)

# ---- Frame 5: receipt + finale (5s, final: quiet hold) ----
f = "05-receipt"
PAPER = "#F5F1E8"
rec_rows = [("Masala x2", "Rs 40"), ("Adrak x1", "Rs 15"), ("Discount", "-Rs 5")]
rr = "".join(f'<div id="{f}-rr{i}" style="display:flex;justify-content:space-between;height:58px;font-size:36px">'
             f'<span>{a}</span><span style="color:{"#C2185B" if b.startswith("-") else INK}">{b}</span></div>' for i, (a, b) in enumerate(rec_rows))
body = f"""    <div id="{f}-rec" style="position:absolute;left:250px;top:80px;width:580px;background:{PAPER};color:{INK};border-radius:10px;padding:36px 48px 30px;
         box-sizing:border-box;font-family:'JetBrains Mono',monospace;box-shadow:0 30px 80px rgba(0,0,0,.6)">
      <div style="text-align:center;font-weight:700;font-size:38px;letter-spacing:.2em;margin-bottom:22px">CHAI BILL</div>
      {rr}
      <div style="border-top:3px dashed rgba(14,17,22,.4);margin:14px 0 18px"></div>
      <div id="{f}-tot" style="display:flex;justify-content:space-between;font-weight:700;font-size:52px"><span>TOTAL</span><span style="color:#B86E00">Rs 50</span></div>
    </div>
    <div class="{f}-h" id="{f}-f1" style="top:580px;font-size:72px">{words(f, "Ab aap", {})}</div>
    <div class="{f}-h" id="{f}-f2" style="top:665px;font-size:92px">{words(f, "Python coder ho!", {0: f + "-c", 1: f + "-c"})}</div>
    <div class="{f}-pill" id="{f}-cta" style="left:230px;top:800px;width:620px;justify-content:center;background:rgba(10,240,240,.14);border:2px solid {CYAN};color:{CREAM}">
      Follow karo <span style="color:{CYAN}">·</span> Samjho with Raj</div>"""
js = [f'  tl.fromTo("#{f}-rec", {{ opacity: 0, y: 80 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.05);']
for i in range(3):
    js.append(f'  tl.fromTo("#{f}-rr{i}", {{ opacity: 0, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "power2.out" }}, {0.5 + i * 0.25:.2f});')
js += [f'  tl.fromTo("#{f}-tot", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "power3.out" }}, 1.3);',
       rise(f"#{f}-f1 .{f}-w", 1.7, 0.08), rise(f"#{f}-f2 .{f}-w", 2.0, 0.1),
       f'  tl.fromTo("#{f}-cta", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }}, 3.2);']
write(f, 5, body, js)
print("wrote", sorted(os.listdir(OUT)))
