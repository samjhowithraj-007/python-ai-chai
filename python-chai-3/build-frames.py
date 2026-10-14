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


ROSE = "#FF8FA3"


def cube(fid, i, left, top, size=110):
    return (f'<div id="{fid}-cube{i}" style="position:absolute;left:{left}px;top:{top}px;width:{size}px;height:{size}px;border-radius:18px;'
            f'background:linear-gradient(145deg,#FFFFFF 0%,#EDEAE2 60%,#D9D4C8 100%);box-shadow:inset 0 -8px 0 rgba(0,0,0,.08),0 14px 30px rgba(0,0,0,.45)"></div>')


def verdict(fid, vid, text, color, left, top, width):
    return (f'<div id="{fid}-{vid}" style="position:absolute;left:{left}px;top:{top}px;width:{width}px;padding:18px 0;border-radius:16px;text-align:center;'
            f'border:3px solid {color};background:rgba(14,17,22,.85);color:{color};font-family:\'JetBrains Mono\',monospace;font-weight:700;font-size:40px;'
            f'line-height:1.35;box-shadow:0 0 30px {color}55">{text}</div>')


def outstrip(fid, text, left, top, width):
    return (f'<div id="{fid}-out" style="position:absolute;left:{left}px;top:{top}px;width:{width}px;height:96px;border-radius:12px;background:rgba(255,176,32,.12);'
            f'border:2px solid {AMBER};font-family:\'JetBrains Mono\',monospace;font-size:46px;color:{AMBER};display:flex;align-items:center;padding-left:34px;'
            f'box-sizing:border-box">&gt; {text}</div>')


def hl(fid, left, top, width, h):
    return (f'<div id="{fid}-hl" style="position:absolute;left:{left}px;top:{top}px;width:{width}px;height:{h}px;background:rgba(10,240,240,.14);'
            f'border-left:6px solid {CYAN};opacity:0"></div>')


# ---- Frame 1: hook (4s) ----
f = "01-hook"
body = f"""    <div class="{f}-kick" id="{f}-kick" style="top:100px">PART 3 · SAMJHO WITH RAJ</div>
    <div class="{f}-h" id="{f}-q" style="top:190px;font-size:130px">{words(f, "Cheeni kitni?", {0: f + "-a", 1: f + "-a"})}</div>
{cup_svg(f, 300, "left:390px;top:470px")}
    {cube(f, 0, 485, 380, 100)}
    <div class="{f}-h" id="{f}-sub" style="top:790px;font-size:64px"><span class="{f}-w {f}-c" style="font-family:'JetBrains Mono',monospace">if-else</span> <span class="{f}-w">se</span> <span class="{f}-w">decide</span> <span class="{f}-w">karo!</span></div>"""
js = [f'  tl.fromTo("#{f}-kick", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, 0.05);',
      rise(f"#{f}-q .{f}-w", 0.2, 0.15),
      f'  tl.fromTo("#{f}-cup", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 1.3);',
      steam_js(f, 1.6),
      f'  tl.fromTo("#{f}-cube0", {{ opacity: 0, y: -260, rotation: -25 }}, {{ opacity: 1, y: 0, rotation: -8, duration: 0.7, ease: "power3.out" }}, 1.7);',
      f'  tl.to("#{f}-cube0", {{ y: -14, duration: 1.4, ease: "sine.inOut" }}, 2.4);',
      rise(f"#{f}-sub .{f}-w", 2.6, 0.08)]
write(f, 4, body, js)

# ---- Frame 2: if, True (7s) ----
f = "02-if"
LH = 46 * 1.6
lines = [f'cheeni = <span class="{f}-n">2</span>',
         f'<span class="{f}-k">if</span> cheeni &gt; <span class="{f}-n">1</span>:',
         f'    <span class="{f}-k">print</span>(<span class="{f}-s">"Meethi chai"</span>)']
cardh, ns = card(f, lines, "left:60px;top:250px;width:720px;height:340px;font-size:46px")
body = f"""    <div class="{f}-h" id="{f}-head" style="top:100px;font-size:84px">{words(f, "if = agar", {0: f + "-c"})}</div>
{cardh}
    {hl(f, 62, int(250 + 64 + 2 * LH - 6), 716, int(LH))}
    {cube(f, 0, 820, 270)}{cube(f, 1, 925, 300)}
    {verdict(f, "v", "2 &gt; 1<br>True", CYAN, 810, 450, 240)}
    {outstrip(f, "Meethi chai", 60, 640, 720)}"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.1),
      f'  tl.fromTo("#{f}-card", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.3);',
      type_line(f, 0, ns[0], 1.0, 0.5),
      f'  tl.fromTo("#{f}-cube0", {{ opacity: 0, y: -300, rotation: -30 }}, {{ opacity: 1, y: 0, rotation: -6, duration: 0.55, ease: "power3.out" }}, 1.4);',
      f'  tl.fromTo("#{f}-cube1", {{ opacity: 0, y: -300, rotation: 30 }}, {{ opacity: 1, y: 0, rotation: 8, duration: 0.55, ease: "power3.out" }}, 1.8);',
      type_line(f, 1, ns[1], 2.4, 0.7),
      f'  tl.fromTo("#{f}-v", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "power3.out" }}, 3.3);',
      type_line(f, 2, ns[2], 4.2, 0.8),
      f'  tl.fromTo("#{f}-hl", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 4.2);',
      f'  tl.fromTo("#{f}-out", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }}, 5.2);']
write(f, 7, body, js)

# ---- Frame 3: else, False (7s) ----
f = "03-else"
LH = 44 * 1.6
TOP = 300
lines = [f'<span class="{f}-k">if</span> cheeni &gt; <span class="{f}-n">1</span>:',
         f'    <span class="{f}-k">print</span>(<span class="{f}-s">"Meethi chai"</span>)',
         f'<span class="{f}-k">else</span>:',
         f'    <span class="{f}-k">print</span>(<span class="{f}-s">"Feeki chai"</span>)']
cardh, ns = card(f, lines, f"left:50px;top:{TOP}px;width:730px;height:380px;font-size:44px")
y = lambda i: int(TOP + 64 + i * LH - 5)
body = f"""    <div class="{f}-h" id="{f}-head" style="top:90px;font-size:80px">{words(f, "else = warna", {0: f + "-c"})}</div>
    <div class="{f}-pill" id="{f}-val" style="left:60px;top:200px;background:rgba(245,241,232,.08);border:2px solid rgba(245,241,232,.4);
         color:{CREAM};font-family:'JetBrains Mono',monospace;font-size:36px;height:70px">cheeni = <span style="color:{ROSE}">0</span></div>
{cardh}
    {hl(f, 52, y(0), 726, int(LH))}
    {verdict(f, "v", "0 &gt; 1<br>False", ROSE, 805, 330, 210)}
    {outstrip(f, "Feeki chai", 50, 712, 730)}"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.1),
      f'  tl.fromTo("#{f}-val", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "power3.out" }}, 0.5);',
      f'  tl.fromTo("#{f}-card", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.6);']
for i, n in enumerate(ns):
    js.append(f'  tl.set("#{f}-l{i}", {{ width: "{n}ch" }}, 0.6);')
js += [f'  tl.fromTo("#{f}-hl", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 1.3);',
       f'  tl.fromTo("#{f}-v", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "power3.out" }}, 1.8);',
       f'  tl.to("#{f}-l1", {{ opacity: 0.3, duration: 0.4 }}, 2.4);',
       f'  tl.to("#{f}-hl", {{ y: {y(2) - y(0)}, duration: 0.35, ease: "power2.inOut" }}, 3.0);',
       f'  tl.to("#{f}-hl", {{ y: {y(3) - y(0)}, duration: 0.35, ease: "power2.inOut" }}, 3.8);',
       f'  tl.fromTo("#{f}-out", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }}, 4.6);']
write(f, 7, body, js)

# ---- Frame 4: two roads (6s) ----
f = "04-fork"
NX, NY = 540, 330          # decision node centre
TX, FX, CY = 270, 810, 650  # result card centres
body = f"""    <div class="{f}-h" id="{f}-head" style="top:90px;font-size:80px">{words(f, "if-else = do raaste", {0: f + "-c", 2: f + "-a", 3: f + "-a"})}</div>
    <svg id="{f}-lines" width="1080" height="1080" viewBox="0 0 1080 1080" style="position:absolute;left:0;top:0" fill="none">
      <path id="{f}-pt" d="M{NX} {NY + 50} L{TX} {CY - 70}" stroke="{CYAN}" stroke-width="8" stroke-linecap="round" stroke-dasharray="420" stroke-dashoffset="420"/>
      <path id="{f}-pf" d="M{NX} {NY + 50} L{FX} {CY - 70}" stroke="{ROSE}" stroke-width="8" stroke-linecap="round" stroke-dasharray="420" stroke-dashoffset="420"/>
    </svg>
    <div id="{f}-node" style="position:absolute;left:{NX - 200}px;top:{NY - 55}px;width:400px;height:110px;border-radius:9999px;background:{NAVY};
         border:3px solid rgba(245,241,232,.5);display:flex;align-items:center;justify-content:center;font-family:'JetBrains Mono',monospace;font-size:44px">cheeni &gt; 1 ?</div>
    <div id="{f}-lt" style="position:absolute;left:{(NX + TX) // 2 - 150}px;top:{(NY + CY) // 2 - 40}px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:40px;color:{CYAN}">True</div>
    <div id="{f}-lf" style="position:absolute;left:{(NX + FX) // 2 + 40}px;top:{(NY + CY) // 2 - 40}px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:40px;color:{ROSE}">False</div>
    <div id="{f}-ct" style="position:absolute;left:{TX - 190}px;top:{CY - 70}px;width:380px;height:140px;border-radius:20px;background:{NAVY};border:3px solid {CYAN};
         display:flex;align-items:center;justify-content:center;font-size:54px">Meethi chai</div>
    <div id="{f}-cf" style="position:absolute;left:{FX - 190}px;top:{CY - 70}px;width:380px;height:140px;border-radius:20px;background:{NAVY};border:3px solid {ROSE};
         display:flex;align-items:center;justify-content:center;font-size:54px">Feeki chai</div>
    <div id="{f}-dot" style="position:absolute;left:{NX - 18}px;top:{NY + 32}px;width:36px;height:36px;border-radius:50%;background:{AMBER};box-shadow:0 0 30px {AMBER};opacity:0"></div>"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.08),
      f'  tl.fromTo("#{f}-node", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "power3.out" }}, 0.7);',
      f'  tl.fromTo("#{f}-pt", {{ strokeDashoffset: 420 }}, {{ strokeDashoffset: 0, duration: 0.7, ease: "power2.out" }}, 1.2);',
      f'  tl.fromTo("#{f}-pf", {{ strokeDashoffset: 420 }}, {{ strokeDashoffset: 0, duration: 0.7, ease: "power2.out" }}, 1.35);',
      f'  tl.fromTo(["#{f}-lt", "#{f}-lf"], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35, stagger: 0.15 }}, 1.8);',
      f'  tl.fromTo("#{f}-ct", {{ opacity: 0, y: 40 }}, {{ opacity: 0.55, y: 0, duration: 0.5, ease: "power3.out" }}, 2.1);',
      f'  tl.fromTo("#{f}-cf", {{ opacity: 0, y: 40 }}, {{ opacity: 0.55, y: 0, duration: 0.5, ease: "power3.out" }}, 2.3);',
      f'  tl.set("#{f}-dot", {{ opacity: 1, x: 0, y: 0 }}, 3.0);',
      f'  tl.to("#{f}-dot", {{ x: {TX - NX}, y: {CY - 70 - NY - 50}, duration: 0.8, ease: "power2.inOut" }}, 3.0);',
      f'  tl.to("#{f}-ct", {{ opacity: 1, scale: 1.06, duration: 0.3, ease: "power2.out" }}, 3.8);',
      f'  tl.set("#{f}-dot", {{ x: 0, y: 0 }}, 4.4);',
      f'  tl.to("#{f}-dot", {{ x: {FX - NX}, y: {CY - 70 - NY - 50}, duration: 0.8, ease: "power2.inOut" }}, 4.4);',
      f'  tl.to("#{f}-cf", {{ opacity: 1, scale: 1.06, duration: 0.3, ease: "power2.out" }}, 5.2);']
write(f, 6, body, js)

# ---- Frame 5: payoff + teaser (6s, final: quiet hold) ----
f = "05-cta"
body = f"""    <div class="{f}-h" id="{f}-l1" style="top:110px;font-size:84px">{words(f, "if-else =", {0: f + "-c"})}</div>
    <div class="{f}-h" id="{f}-l2" style="top:215px;font-size:92px">{words(f, "computer ka faisla", {2: f + "-a"})}</div>
    <div id="{f}-teaser" style="position:absolute;left:150px;top:420px;width:780px;height:220px;border-radius:20px;background:{NAVY};border:2px solid rgba(10,240,240,.5);
         box-sizing:border-box;padding:34px 44px;box-shadow:0 24px 70px rgba(0,0,0,.5)">
      <div style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:30px;letter-spacing:.16em;color:rgba(245,241,232,.66)">AGLA PART 4</div>
      <div style="font-size:64px;margin-top:18px"><span class="{f}-c" style="font-family:'JetBrains Mono',monospace">list</span>: chai ke flavours</div>
    </div>
    <div class="{f}-pill" id="{f}-cta" style="left:230px;top:740px;width:620px;justify-content:center;background:rgba(10,240,240,.14);border:2px solid {CYAN};color:{CREAM}">
      Follow karo <span style="color:{CYAN}">·</span> Samjho with Raj</div>"""
js = [rise(f"#{f}-l1 .{f}-w", 0.05, 0.08), rise(f"#{f}-l2 .{f}-w", 0.7, 0.1),
      f'  tl.fromTo("#{f}-teaser", {{ opacity: 0, y: 70 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 1.7);',
      f'  tl.fromTo("#{f}-cta", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }}, 3.4);']
write(f, 6, body, js)
print("wrote", sorted(os.listdir(OUT)))
