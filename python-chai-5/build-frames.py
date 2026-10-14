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



# ---- Frame 1: hook (4s) ----
f = "01-hook"
body = f"""    <div class="{f}-kick" id="{f}-kick" style="top:100px">PART 5 · SAMJHO WITH RAJ</div>
    <div class="{f}-h" id="{f}-t1" style="top:180px;font-size:104px">{words(f, "Har flavour", {1: f + "-a"})}</div>
    <div class="{f}-h" id="{f}-t2" style="top:292px;font-size:104px">{words(f, "try karna hai?", {})}</div>
    <svg id="{f}-loop" width="440" height="440" viewBox="0 0 440 440" style="position:absolute;left:320px;top:430px" fill="none">
      <path id="{f}-arc" d="M220 30 A190 190 0 1 1 55 125" stroke="{CYAN}" stroke-width="12" stroke-linecap="round" stroke-dasharray="1100" stroke-dashoffset="1100"
            style="filter:drop-shadow(0 0 14px rgba(10,240,240,.7))"/>
      <path id="{f}-tip" d="M20 105 L58 128 L82 88" stroke="{CYAN}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" opacity="0"/>
    </svg>
    <div class="{f}-h {f}-c" id="{f}-fl" style="top:600px;font-size:62px;font-family:'JetBrains Mono',monospace">for loop</div>
    <div class="{f}-h" id="{f}-kr" style="top:690px;font-size:58px">karega!</div>"""
js = [f'  tl.fromTo("#{f}-kick", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, 0.05);',
      rise(f"#{f}-t1 .{f}-w", 0.2, 0.1), rise(f"#{f}-t2 .{f}-w", 0.6, 0.1),
      f'  tl.fromTo("#{f}-arc", {{ strokeDashoffset: 1100 }}, {{ strokeDashoffset: 0, duration: 1.2, ease: "power2.inOut" }}, 1.4);',
      f'  tl.fromTo("#{f}-tip", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 2.5);',
      f'  tl.fromTo("#{f}-loop", {{ rotation: 0 }}, {{ rotation: 30, duration: 2.6, ease: "none", transformOrigin: "50% 50%" }}, 1.4);',
      f'  tl.fromTo("#{f}-fl", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "power3.out" }}, 1.9);',
      f'  tl.fromTo("#{f}-kr", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, 2.4);']
write(f, 4, body, js)

# ---- Frame 2: the loop (8s) ----
f = "02-loop"
SX = [70 + i * 240 for i in range(4)]
slots = "".join(slot(f, i, SX[i], 190, 220, 170) for i in range(4))
lines = [f'<span class="{f}-k">for</span> f <span class="{f}-k">in</span> flavours:',
         f'    <span class="{f}-k">print</span>(f + <span class="{f}-s">" chai"</span>)']
cardh, ns = card(f, lines, "left:90px;top:420px;width:900px;height:241px;font-size:46px")
vals = "".join(f'<span id="{f}-v{i}" style="position:absolute;left:150px;top:0;line-height:84px;color:{FLAV[i][1]};opacity:0">"{FLAV[i][0]}"</span>' for i in range(4))
body = f"""    <div class="{f}-h" id="{f}-head" style="top:76px;font-size:76px">{words(f, "for = har ek ke liye", {0: f + "-c"})}</div>
    {slots}
    <div id="{f}-ring" style="position:absolute;left:{SX[0] - 10}px;top:180px;width:240px;height:190px;border-radius:26px;border:6px solid {CYAN};
         box-shadow:0 0 40px rgba(10,240,240,.6);box-sizing:border-box;opacity:0"></div>
{cardh}
    <div id="{f}-chip" style="position:absolute;left:290px;top:700px;width:500px;height:84px;border-radius:9999px;background:rgba(10,240,240,.10);
         border:3px solid {CYAN};font-family:'JetBrains Mono',monospace;font-size:44px;box-sizing:border-box">
      <span style="position:absolute;left:44px;top:0;line-height:78px;color:{CREAM}">f =</span>{vals}</div>"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.07),
      f'  tl.set(["#{f}-s0", "#{f}-s1", "#{f}-s2", "#{f}-s3"], {{ opacity: 0 }}, 0);',
      f'  tl.fromTo(["#{f}-c0", "#{f}-c1", "#{f}-c2", "#{f}-c3"], {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out", stagger: 0.08 }}, 0.2);',
      f'  tl.fromTo("#{f}-card", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.35);',
      type_line(f, 0, ns[0], 0.6, 0.6), type_line(f, 1, ns[1], 1.0, 0.6),
      f'  tl.fromTo("#{f}-chip", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "power3.out" }}, 1.4);']
for i in range(4):
    t = 1.6 + i * 1.3
    if i == 0:
        js.append(f'  tl.fromTo("#{f}-ring", {{ opacity: 0, scale: 1.15 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "power3.out" }}, {t:.2f});')
    else:
        js.append(f'  tl.to("#{f}-ring", {{ x: {SX[i] - SX[0]}, duration: 0.45, ease: "power2.inOut" }}, {t - 0.2:.2f});')
        js.append(f'  tl.set("#{f}-v{i - 1}", {{ opacity: 0 }}, {t:.2f});')
    js.append(f'  tl.set("#{f}-v{i}", {{ opacity: 1 }}, {t:.2f});')
    js.append(f'  tl.fromTo("#{f}-l1", {{ textShadow: "0 0 0 rgba(10,240,240,0)" }}, {{ textShadow: "0 0 26px rgba(10,240,240,.95)", duration: 0.3, ease: "power2.out", immediateRender: false }}, {t + 0.3:.2f});')
    js.append(f'  tl.to("#{f}-l1", {{ textShadow: "0 0 0 rgba(10,240,240,0)", duration: 0.4, ease: "power2.in" }}, {t + 0.7:.2f});')
write(f, 8, body, js)

# ---- Frame 3: output (7s) ----
f = "03-output"
rows = "".join(f'<div id="{f}-r{i}" style="display:flex;align-items:center;gap:22px;height:92px">{mini_cup(FLAV[i][1], 70)}'
               f'<span style="font-size:50px;color:{FLAV[i][1]}">{FLAV[i][0]} chai</span></div>' for i in range(4))
body = f"""    <div class="{f}-h" id="{f}-head" style="top:84px;font-size:84px">{words(f, "Output", {0: f + "-a"})}</div>
    <div id="{f}-term" style="position:absolute;left:140px;top:210px;width:800px;height:480px;background:#0A0C10;border:1px solid rgba(245,241,232,.16);
         border-radius:14px;padding:66px 50px 20px;box-sizing:border-box;font-family:'JetBrains Mono',monospace;box-shadow:0 24px 70px rgba(0,0,0,.5)">
      <div class="{f}-dots"><i></i><i></i><i></i></div><div class="{f}-file">terminal</div>
      {rows}
    </div>
    <div id="{f}-badge" style="position:absolute;left:300px;top:740px;width:480px;height:100px;border-radius:22px;background:{AMBER};color:{INK};
         display:flex;align-items:center;justify-content:center;font-size:58px;font-weight:700;box-shadow:0 18px 50px rgba(255,176,32,.45)">4 baar chala!</div>"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.1),
      f'  tl.fromTo("#{f}-term", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.3);']
for i in range(4):
    js.append(f'  tl.fromTo("#{f}-r{i}", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.4, ease: "power3.out" }}, {1.0 + i * 1.0:.2f});')
js.append(f'  tl.fromTo("#{f}-badge", {{ opacity: 0, scale: 1.4, rotation: -3 }}, {{ opacity: 1, scale: 1, rotation: -3, duration: 0.4, ease: "power3.out" }}, 5.2);')
write(f, 7, body, js)

# ---- Frame 4: why a loop (5s) ----
f = "04-why"
left_lines = [f'<span class="{f}-k">print</span>(<span class="{f}-s">"Masala chai"</span>)',
              f'<span class="{f}-k">print</span>(<span class="{f}-s">"Adrak chai"</span>)',
              f'<span class="{f}-k">print</span>(<span class="{f}-s">"Elaichi chai"</span>)',
              f'<span class="{f}-k">print</span>(<span class="{f}-s">"Tulsi chai"</span>)']
cardA, nA = card(f, left_lines, "left:40px;top:250px;width:490px;height:330px;font-size:28px", fname="bina loop")
right_lines = [f'<span class="{f}-k">for</span> f <span class="{f}-k">in</span> flavours:',
               f'    <span class="{f}-k">print</span>(f+<span class="{f}-s">" chai"</span>)']
cardB, nB = card(f, right_lines, "left:550px;top:250px;width:490px;height:330px;font-size:30px", fname="loop ke saath")
cardB = cardB.replace(f'id="{f}-card"', f'id="{f}-card2"').replace(f'id="{f}-l', f'id="{f}-m')
body = f"""    <div class="{f}-h" id="{f}-head" style="top:84px;font-size:84px">{words(f, "Loop = kam code", {2: f + "-a", 3: f + "-a"})}</div>
{cardA}
{cardB}
    <div class="{f}-h" id="{f}-n1" style="top:600px;left:40px;right:auto;width:490px;font-size:46px;color:rgba(245,241,232,.6)">4 lines</div>
    <div class="{f}-h {f}-c" id="{f}-n2" style="top:600px;left:550px;right:auto;width:490px;font-size:46px">2 lines</div>
    <div class="{f}-h" id="{f}-cap" style="top:760px;font-size:56px">100 flavours? Phir bhi <span class="{f}-a">2 lines!</span></div>"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.08),
      f'  tl.fromTo("#{f}-card", {{ opacity: 0, y: 50 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, 0.3);']
for i, n in enumerate(nA):
    js.append(f'  tl.set("#{f}-l{i}", {{ width: "{n}ch" }}, 0.3);')
js += [f'  tl.fromTo("#{f}-n1", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, 0.8);',
       f'  tl.fromTo("#{f}-card2", {{ opacity: 0, y: 50 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, 1.2);']
for i, n in enumerate(nB):
    js.append(f'  tl.set("#{f}-m{i}", {{ width: "{n}ch" }}, 1.2);')
js += [f'  tl.fromTo("#{f}-card2", {{ boxShadow: "0 0 0 rgba(10,240,240,0)", borderColor: "rgba(245,241,232,.14)" }}, {{ boxShadow: "0 0 50px rgba(10,240,240,.5)", borderColor: "rgba(10,240,240,.9)", duration: 0.5, immediateRender: false }}, 1.8);',
       f'  tl.to("#{f}-card", {{ opacity: 0.45, duration: 0.5 }}, 1.8);',
       f'  tl.fromTo("#{f}-n2", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, 1.9);',
       f'  tl.fromTo("#{f}-cap", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, 2.8);']
write(f, 5, body, js)

# ---- Frame 5: payoff + teaser (6s, final: quiet hold) ----
f = "05-cta"
body = f"""    <div class="{f}-h" id="{f}-l1" style="top:110px;font-size:84px">{words(f, "for loop = har item,", {0: f + "-c", 1: f + "-c"})}</div>
    <div class="{f}-h" id="{f}-l2" style="top:215px;font-size:96px">{words(f, "ek-ek karke!", {0: f + "-a", 1: f + "-a"})}</div>
    <div id="{f}-teaser" style="position:absolute;left:90px;top:420px;width:900px;height:220px;border-radius:20px;background:{NAVY};border:2px solid rgba(10,240,240,.5);
         box-sizing:border-box;padding:34px 44px;box-shadow:0 24px 70px rgba(0,0,0,.5)">
      <div style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:30px;letter-spacing:.16em;color:rgba(245,241,232,.66)">AGLA PART 6</div>
      <div style="font-size:50px;margin-top:22px;white-space:nowrap"><span class="{f}-c" style="font-family:'JetBrains Mono',monospace">dictionary</span>: chai ka menu card</div>
    </div>
    <div class="{f}-pill" id="{f}-cta" style="left:230px;top:740px;width:620px;justify-content:center;background:rgba(10,240,240,.14);border:2px solid {CYAN};color:{CREAM}">
      Follow karo <span style="color:{CYAN}">·</span> Samjho with Raj</div>"""
js = [rise(f"#{f}-l1 .{f}-w", 0.05, 0.08), rise(f"#{f}-l2 .{f}-w", 0.7, 0.1),
      f'  tl.fromTo("#{f}-teaser", {{ opacity: 0, y: 70 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 1.7);',
      f'  tl.fromTo("#{f}-cta", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }}, 3.4);']
write(f, 6, body, js)
print("wrote", sorted(os.listdir(OUT)))
