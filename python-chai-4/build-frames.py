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
chips = "".join(f'<div class="{f}-pill" id="{f}-chip{i}" style="left:{90 + i * 310}px;top:560px;width:280px;height:100px;justify-content:center;'
                f'background:{NAVY};border:3px solid {FLAV[i][1]};color:{FLAV[i][1]};font-size:46px">{FLAV[i][0]}</div>' for i in range(3))
body = f"""    <div class="{f}-kick" id="{f}-kick" style="top:100px">PART 4 · SAMJHO WITH RAJ</div>
    <div class="{f}-h" id="{f}-t1" style="top:200px;font-size:110px">{words(f, "Chai ke kitne", {})}</div>
    <div class="{f}-h" id="{f}-t2" style="top:330px;font-size:140px">{words(f, "flavours?", {0: f + "-a"})}</div>
    {chips}
    <div class="{f}-h" id="{f}-sub" style="top:760px;font-size:68px"><span class="{f}-w {f}-c" style="font-family:'JetBrains Mono',monospace">list</span> <span class="{f}-w">mein</span> <span class="{f}-w">rakho!</span></div>"""
js = [f'  tl.fromTo("#{f}-kick", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, 0.05);',
      rise(f"#{f}-t1 .{f}-w", 0.2, 0.1), rise(f"#{f}-t2 .{f}-w", 0.7, 0.1)]
for i in range(3):
    js.append(f'  tl.fromTo("#{f}-chip{i}", {{ opacity: 0, scale: 0.6, y: 30 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.4, ease: "power3.out" }}, {1.4 + i * 0.25:.2f});')
js.append(rise(f"#{f}-sub .{f}-w", 2.8, 0.1))
write(f, 4, body, js)

# ---- Frame 2: make a list (7s) ----
f = "02-list"
lines = ['flavours = [',
         f'  <span class="{f}-s">"Masala"</span>,',
         f'  <span class="{f}-s">"Adrak"</span>,',
         f'  <span class="{f}-s">"Elaichi"</span> ]']
cardh, ns = card(f, lines, "left:90px;top:200px;width:900px;height:376px;font-size:44px")
slots = "".join(slot(f, i, 90 + i * 305, 630, 290, 190) for i in range(3))
body = f"""    <div class="{f}-h" id="{f}-head" style="top:84px;font-size:80px">{words(f, "list = ek dabba", {0: f + "-c"})}</div>
{cardh}
    <div id="{f}-tray" style="position:absolute;left:72px;top:612px;width:936px;height:226px;border-radius:28px;border:3px solid rgba(245,241,232,.22);box-sizing:border-box"></div>
    {slots}"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.1),
      f'  tl.fromTo("#{f}-card", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.3);',
      f'  tl.fromTo(["#{f}-tray", "#{f}-s0", "#{f}-s1", "#{f}-s2"], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, 0.5);',
      type_line(f, 0, ns[0], 1.0, 0.6)]
for i in range(3):
    t = 1.8 + i * 1.15
    js.append(type_line(f, i + 1, ns[i + 1], t, 0.6))
    js.append(f'  tl.fromTo("#{f}-c{i}", {{ opacity: 0, y: -40, scale: 0.85 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.45, ease: "power3.out" }}, {t + 0.45:.2f});')
js.append(f'  tl.fromTo("#{f}-tray", {{ borderColor: "rgba(245,241,232,.22)", boxShadow: "0 0 0 rgba(10,240,240,0)" }}, {{ borderColor: "rgba(10,240,240,.9)", boxShadow: "0 0 40px rgba(10,240,240,.45)", duration: 0.6, ease: "power2.out" }}, 5.6);')
write(f, 7, body, js)

# ---- Frame 3: index from 0 (7s) ----
f = "03-index"
SX = [90 + i * 305 for i in range(3)]
slots = "".join(slot(f, i, SX[i], 210, 290, 190) for i in range(3))
idx = "".join(index_label(f, i, SX[i] + 145, 412) for i in range(3))
lines = [f'<span class="{f}-k">print</span>(flavours[<span class="{f}-n">0</span>])',
         f'<span class="{f}-k">print</span>(flavours[<span class="{f}-n">2</span>])']
cardh, ns = card(f, lines, "left:90px;top:490px;width:900px;height:236px;font-size:44px")
body = f"""    <div class="{f}-h" id="{f}-head" style="top:84px;font-size:80px">{words(f, "Ginti 0 se shuru!", {1: f + "-a"})}</div>
    {slots}
    {idx}
    <div id="{f}-ring" style="position:absolute;left:{SX[0] - 10}px;top:200px;width:310px;height:210px;border-radius:26px;border:6px solid {CYAN};
         box-shadow:0 0 40px rgba(10,240,240,.6);box-sizing:border-box;opacity:0"></div>
{cardh}
    {outstrip(f, "o0", "Masala", 90, 762, 440)}
    {outstrip(f, "o1", "Elaichi", 550, 762, 440)}"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.1),
      f'  tl.fromTo(["#{f}-c0", "#{f}-c1", "#{f}-c2"], {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out", stagger: 0.1 }}, 0.3);',
      f'  tl.set(["#{f}-s0", "#{f}-s1", "#{f}-s2"], {{ opacity: 0 }}, 0);',
      f'  tl.fromTo(["#{f}-ix0", "#{f}-ix1", "#{f}-ix2"], {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "power3.out", stagger: 0.2 }}, 0.8);',
      f'  tl.fromTo("#{f}-card", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 1.0);',
      type_line(f, 0, ns[0], 1.5, 0.8),
      f'  tl.fromTo("#{f}-ring", {{ opacity: 0, scale: 1.15 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "power3.out" }}, 2.4);',
      f'  tl.fromTo("#{f}-o0", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }}, 2.9);',
      type_line(f, 1, ns[1], 4.0, 0.8),
      f'  tl.to("#{f}-ring", {{ x: {SX[2] - SX[0]}, duration: 0.6, ease: "power2.inOut" }}, 4.9);',
      f'  tl.fromTo("#{f}-o1", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }}, 5.5);']
write(f, 7, body, js)

# ---- Frame 4: append + len (6s) ----
f = "04-append"
SX = [70 + i * 240 for i in range(4)]
slots = "".join(slot(f, i, SX[i], 210, 220, 180) for i in range(4))
idx = "".join(index_label(f, i, SX[i] + 110, 400) for i in range(4))
lines = [f'flavours.<span class="{f}-k">append</span>(<span class="{f}-s">"Tulsi"</span>)',
         f'<span class="{f}-k">print</span>(<span class="{f}-k">len</span>(flavours))']
cardh, ns = card(f, lines, "left:90px;top:490px;width:900px;height:236px;font-size:44px")
body = f"""    <div class="{f}-h" id="{f}-head" style="top:84px;font-size:80px">{words(f, "append = naya jodo", {0: f + "-c"})}</div>
    {slots}
    {idx}
{cardh}
    {outstrip(f, "o", "4", 90, 762, 300)}"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.1),
      f'  tl.set(["#{f}-s0", "#{f}-s1", "#{f}-s2"], {{ opacity: 0 }}, 0);',
      f'  tl.fromTo(["#{f}-c0", "#{f}-c1", "#{f}-c2", "#{f}-ix0", "#{f}-ix1", "#{f}-ix2"], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, 0.3);',
      f'  tl.fromTo("#{f}-s3", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, 0.6);',
      f'  tl.fromTo("#{f}-card", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.5);',
      type_line(f, 0, ns[0], 1.0, 1.0),
      f'  tl.fromTo("#{f}-c3", {{ opacity: 0, x: 220 }}, {{ opacity: 1, x: 0, duration: 0.6, ease: "power3.out" }}, 2.2);',
      f'  tl.fromTo("#{f}-ix3", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "power3.out" }}, 2.7);',
      type_line(f, 1, ns[1], 3.2, 0.8),
      f'  tl.fromTo("#{f}-o", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }}, 4.1);',
      f'  tl.fromTo(["#{f}-ix0", "#{f}-ix1", "#{f}-ix2", "#{f}-ix3"], {{ color: "{CYAN}", scale: 1 }}, {{ color: "{AMBER}", scale: 1.25, duration: 0.25, ease: "power2.out", stagger: 0.22, immediateRender: false }}, 4.4);']
write(f, 6, body, js)

# ---- Frame 5: payoff + teaser (6s, final: quiet hold) ----
f = "05-cta"
body = f"""    <div class="{f}-h" id="{f}-l1" style="top:110px;font-size:84px">{words(f, "list = sab flavours", {0: f + "-c"})}</div>
    <div class="{f}-h" id="{f}-l2" style="top:215px;font-size:96px">{words(f, "ek jagah!", {0: f + "-a", 1: f + "-a"})}</div>
    <div id="{f}-teaser" style="position:absolute;left:90px;top:420px;width:900px;height:220px;border-radius:20px;background:{NAVY};border:2px solid rgba(10,240,240,.5);
         box-sizing:border-box;padding:34px 44px;box-shadow:0 24px 70px rgba(0,0,0,.5)">
      <div style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:30px;letter-spacing:.16em;color:rgba(245,241,232,.66)">AGLA PART 5</div>
      <div style="font-size:50px;margin-top:22px;white-space:nowrap"><span class="{f}-c" style="font-family:'JetBrains Mono',monospace">for loop</span>: har flavour try karo</div>
    </div>
    <div class="{f}-pill" id="{f}-cta" style="left:230px;top:740px;width:620px;justify-content:center;background:rgba(10,240,240,.14);border:2px solid {CYAN};color:{CREAM}">
      Follow karo <span style="color:{CYAN}">·</span> Samjho with Raj</div>"""
js = [rise(f"#{f}-l1 .{f}-w", 0.05, 0.08), rise(f"#{f}-l2 .{f}-w", 0.7, 0.1),
      f'  tl.fromTo("#{f}-teaser", {{ opacity: 0, y: 70 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 1.7);',
      f'  tl.fromTo("#{f}-cta", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }}, 3.4);']
write(f, 6, body, js)
print("wrote", sorted(os.listdir(OUT)))
