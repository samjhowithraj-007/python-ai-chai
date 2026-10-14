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
      font-family:"JetBrains Mono", ui-monospace, monospace; font-variant-ligatures:none; }}
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
TERMBG = "#0A0C10"
CHECK = (f'<svg width="56" height="56" viewBox="0 0 30 30" style="flex:none"><circle cx="15" cy="15" r="14" fill="{CYAN}"/>'
         f'<path d="M8 15.5 L13 20.5 L22 10" stroke="{INK}" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def terminal(fid, inner, left, top, width, height):
    return (f'<div id="{fid}-term" style="position:absolute;left:{left}px;top:{top}px;width:{width}px;height:{height}px;background:{TERMBG};'
            f'border:1px solid rgba(245,241,232,.16);border-radius:14px;padding:70px 44px 24px;box-sizing:border-box;font-family:\'JetBrains Mono\',monospace;'
            f'box-shadow:0 24px 70px rgba(0,0,0,.5)"><div class="{fid}-dots"><i></i><i></i><i></i></div><div class="{fid}-file">terminal</div>{inner}</div>')


def typed(fid, uid, text, color):
    """User's typed answer: a monospace span revealed by width, plus a block caret after it."""
    return (f'<span id="{fid}-{uid}" style="display:inline-block;vertical-align:top;white-space:pre;overflow:hidden;width:0ch;color:{color}">{text}</span>'
            f'<span id="{fid}-{uid}c" style="display:inline-block;width:.6em;height:1.1em;vertical-align:-.15em;background:{CYAN};opacity:0"></span>')


def type_user(fid, uid, n, t, dur):
    return [f'  tl.fromTo("#{fid}-{uid}c", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.05 }}, {t - 0.3:.2f});',
            f'  tl.fromTo("#{fid}-{uid}", {{ width: "0ch" }}, {{ width: "{n}ch", duration: {dur:.2f}, ease: "steps({n})" }}, {t:.2f});',
            f'  tl.to("#{fid}-{uid}c", {{ opacity: 0, duration: 0.05 }}, {t + dur + 0.3:.2f});']


SHIELD = (f'<svg width="190" height="220" viewBox="0 0 100 116" fill="none" style="filter:drop-shadow(0 0 22px rgba(10,240,240,.6))">'
          f'<path d="M50 4 L92 20 L92 56 Q92 92 50 112 Q8 92 8 56 L8 20 Z" fill="rgba(10,240,240,.14)" stroke="{CYAN}" stroke-width="6" stroke-linejoin="round"/>'
          f'<path d="M30 58 L44 72 L72 42" stroke="{CYAN}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def rose_style(fid):
    return f'<style>.{fid}-r {{ color:{ROSE}; text-shadow:0 0 24px rgba(255,143,163,.45); }}</style>'


def sign(fid, left, top, w, h, big=110):
    return (f'<div id="{fid}-sign" style="position:absolute;left:{left}px;top:{top}px;width:{w}px;height:{h}px;border-radius:22px;background:#0A0C10;'
            f'border:4px solid {CYAN};box-shadow:0 0 40px rgba(10,240,240,.45), inset 0 0 30px rgba(10,240,240,.15);box-sizing:border-box">'
            f'<div style="position:absolute;left:0;right:0;top:{int(h * .16)}px;text-align:center;font-family:\'JetBrains Mono\',monospace;font-weight:700;'
            f'font-size:{int(big * .3)}px;letter-spacing:.18em;color:rgba(245,241,232,.75)">CHAI DUKAAN</div>'
            f'<div id="{fid}-open" style="position:absolute;left:0;right:0;top:{int(h * .38)}px;text-align:center;font-size:{big}px;color:{CYAN};'
            f'text-shadow:0 0 30px rgba(10,240,240,.9)">KHULA</div>'
            f'<div id="{fid}-shut" style="position:absolute;left:0;right:0;top:{int(h * .38)}px;text-align:center;font-size:{big}px;color:{ROSE};'
            f'text-shadow:0 0 30px rgba(255,143,163,.9);opacity:0">BAND</div></div>')


def shut_js(fid, t):
    return [f'  tl.set("#{fid}-open", {{ opacity: 0 }}, {t:.2f});',
            f'  tl.set("#{fid}-shut", {{ opacity: 1 }}, {t:.2f});',
            f'  tl.fromTo("#{fid}-sign", {{ borderColor: "{CYAN}", boxShadow: "0 0 40px rgba(10,240,240,.45)" }}, '
            f'{{ borderColor: "{ROSE}", boxShadow: "0 0 40px rgba(255,143,163,.5)", duration: 0.25, immediateRender: false }}, {t:.2f});']


# ---- Frame 1: hook (4s) ----
f = "01-hook"
body = f"""    <div class="{f}-kick" id="{f}-kick" style="top:100px">PART 10 · SAMJHO WITH RAJ</div>
    <div class="{f}-h" id="{f}-t1" style="top:180px;font-size:100px">{words(f, "Dukaan band", {1: f + "-a"})}</div>
    <div class="{f}-h" id="{f}-t2" style="top:290px;font-size:100px">{words(f, "mat karo!", {0: f + "-a", 1: f + "-a"})}</div>
    {sign(f, 240, 450, 600, 260, big=120)}
    <div class="{f}-h {f}-c" id="{f}-sub" style="top:770px;font-size:80px;font-family:'JetBrains Mono',monospace">while True!</div>"""
js = [f'  tl.fromTo("#{f}-kick", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, 0.05),'.rstrip(",") + ";",
      rise(f"#{f}-t1 .{f}-w", 0.2, 0.1), rise(f"#{f}-t2 .{f}-w", 0.55, 0.1),
      f'  tl.fromTo("#{f}-sign", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.08 }}, 1.4);',
      f'  tl.to("#{f}-sign", {{ opacity: 0.2, duration: 0.06 }}, 1.55);',
      f'  tl.to("#{f}-sign", {{ opacity: 1, duration: 0.06 }}, 1.68);',
      f'  tl.to("#{f}-sign", {{ opacity: 0.35, duration: 0.05 }}, 1.85);',
      f'  tl.to("#{f}-sign", {{ opacity: 1, duration: 0.1 }}, 1.95);',
      f'  tl.fromTo("#{f}-sub", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, 2.8);']
write(f, 4, body, js)

# ---- Frame 2: while True serves orders (8s) ----
f = "02-loop"
LH = 32 * 1.6
CT = 180
lines = [f'<span class="{f}-k">while True</span>:',
         f'    order = <span class="{f}-k">input</span>(<span class="{f}-s">"Order? "</span>)',
         f'    <span class="{f}-k">print</span>(order, <span class="{f}-s">"ready!"</span>)']
cardh, ns = card(f, lines, f"left:40px;top:{CT}px;width:680px;height:248px;font-size:32px")
y = lambda i: int(CT + 64 + i * LH - 4)
row = lambda rid, txt, col: f'<div id="{f}-{rid}" style="font-size:38px;line-height:1.45;color:{col}">{txt}</div>'
inner = (row("q1", f'Order? {typed(f, "u1", "Masala", CYAN)}', CREAM) + row("o1", "Masala ready!", AMBER)
         + row("q2", f'Order? {typed(f, "u2", "Adrak", CYAN)}', CREAM) + row("o2", "Adrak ready!", AMBER)
         + row("q3", f'Order? <span id="{f}-c3" style="display:inline-block;width:.6em;height:1.1em;vertical-align:-.15em;background:{CYAN};opacity:0"></span>', CREAM))
body = f"""    <div class="{f}-h" id="{f}-head" style="top:76px;font-size:76px">{words(f, "while True = hamesha chalo", {0: f + "-c", 1: f + "-c"})}</div>
{cardh}
    <div id="{f}-hl" style="position:absolute;left:42px;top:{y(1)}px;width:676px;height:{int(LH)}px;background:rgba(10,240,240,.14);border-left:6px solid {CYAN};opacity:0"></div>
    {sign(f, 750, CT, 290, 248, big=72)}
    {terminal(f, inner, 40, 460, 1000, 400)}"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.08),
      f'  tl.fromTo("#{f}-card", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.2);',
      f'  tl.fromTo("#{f}-sign", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, 0.4);']
for i in range(3):
    js.append(type_line(f, i, ns[i], 0.4 + i * 0.3, 0.4))
js += [f'  tl.fromTo("#{f}-term", {{ opacity: 0, y: 50 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, 1.4);',
       f'  tl.fromTo("#{f}-hl", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, 1.7);']
for k, (name, t0) in enumerate([("Masala", 1.8), ("Adrak", 4.6)]):
    q, u, o = f"q{k + 1}", f"u{k + 1}", f"o{k + 1}"
    if k:
        js.append(f'  tl.to("#{f}-hl", {{ y: 0, duration: 0.3, ease: "power2.inOut" }}, {t0 - 0.2:.2f});')
    js.append(f'  tl.fromTo("#{f}-{q}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15 }}, {t0:.2f});')
    js += type_user(f, u, len(name), t0 + 0.6, 0.6)
    js.append(f'  tl.to("#{f}-hl", {{ y: {y(2) - y(1)}, duration: 0.3, ease: "power2.inOut" }}, {t0 + 1.6:.2f});')
    js.append(f'  tl.fromTo("#{f}-{o}", {{ opacity: 0, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }}, {t0 + 1.9:.2f});')
js += [f'  tl.to("#{f}-hl", {{ y: 0, duration: 0.3, ease: "power2.inOut" }}, 7.0);',
       f'  tl.fromTo("#{f}-q3", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15 }}, 7.2);',
       f'  tl.fromTo("#{f}-c3", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.05 }}, 7.4);']
write(f, 8, body, js)

# ---- Frame 3: break (7s) ----
f = "03-break"
CT = 180
lines = [f'<span class="{f}-k">while True</span>:',
         f'    order = <span class="{f}-k">input</span>(<span class="{f}-s">"Order? "</span>)',
         f'    <span class="{f}-k">if</span> order == <span class="{f}-s">"band"</span>:',
         f'        <span class="{f}-k">break</span>']
cardh, ns = card(f, lines, f"left:40px;top:{CT}px;width:680px;height:312px;font-size:32px")
y = lambda i: int(CT + 64 + i * LH - 4)
inner = (f'<div id="{f}-q" style="font-size:44px;line-height:1.5;color:{CREAM}">Order? {typed(f, "u", "band", ROSE)}</div>'
         f'<div id="{f}-o" style="font-size:44px;line-height:1.5;color:{CREAM}">Dukaan band! Kal milte hain.</div>')
body = f"""    <div class="{f}-h" id="{f}-head" style="top:76px;font-size:80px">{words(f, "break = bahar niklo", {0: f + "-c"})}</div>
{cardh}
    <div id="{f}-hl" style="position:absolute;left:42px;top:{y(1)}px;width:676px;height:{int(LH)}px;background:rgba(10,240,240,.14);border-left:6px solid {CYAN};opacity:0"></div>
    {sign(f, 750, CT, 290, 312, big=80)}
    {terminal(f, inner, 40, 530, 1000, 250)}"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.1),
      f'  tl.fromTo("#{f}-card", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.2);',
      f'  tl.fromTo("#{f}-sign", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, 0.4);']
for i in range(4):
    js.append(type_line(f, i, ns[i], 0.4 + i * 0.25, 0.35))
js += [f'  tl.fromTo("#{f}-hl", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, 1.6);',
       f'  tl.fromTo("#{f}-term", {{ opacity: 0, y: 50 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, 1.6);',
       f'  tl.fromTo("#{f}-q", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15 }}, 2.0);']
js += type_user(f, "u", 4, 2.5, 0.5)
js += [f'  tl.to("#{f}-hl", {{ y: {y(2) - y(1)}, duration: 0.3, ease: "power2.inOut" }}, 3.3);',
       f'  tl.to("#{f}-hl", {{ y: {y(3) - y(1)}, backgroundColor: "rgba(255,143,163,.22)", borderLeftColor: "{ROSE}", duration: 0.3, ease: "power2.inOut" }}, 4.0);']
js += shut_js(f, 4.5)
js.append(f'  tl.fromTo("#{f}-o", {{ opacity: 0, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.4, ease: "power3.out" }}, 5.0);')
write(f, 7, body, js)

# ---- Frame 4: loop circle (5s) ----
f = "04-circle"
CX, CY, R = 520, 570, 220
nodes = [("Order lo", CX, CY - R), ("Chai do", CX + 190, CY + 110), ("Agla customer", CX - 190, CY + 110)]
node_html = "".join(f'<div id="{f}-n{i}" style="position:absolute;left:{x - 140}px;top:{y0 - 38}px;width:280px;height:76px;border-radius:9999px;background:{NAVY};'
                    f'border:3px solid rgba(245,241,232,.45);display:flex;align-items:center;justify-content:center;font-size:36px">{t}</div>'
                    for i, (t, x, y0) in enumerate(nodes))
EX0, EY0 = CX + 156, CY - 156     # circle point at -45 degrees
EX1, EY1 = 900, 300
body = f"""    {rose_style(f)}
    <div class="{f}-h" id="{f}-head" style="top:76px;font-size:76px">{words(f, "Gol gol, jab tak break!", {4: f + "-r"})}</div>
    <svg width="1080" height="1080" viewBox="0 0 1080 1080" style="position:absolute;left:0;top:0" fill="none">
      <circle id="{f}-ring" cx="{CX}" cy="{CY}" r="{R}" stroke="{CYAN}" stroke-width="8" stroke-dasharray="1383" stroke-dashoffset="1383" transform="rotate(-90 {CX} {CY})"/>
      <path id="{f}-exit" d="M{EX0} {EY0} L{EX1 - 70} {EY1 + 40}" stroke="{ROSE}" stroke-width="8" stroke-linecap="round" stroke-dasharray="14 12" opacity="0"/>
    </svg>
    {node_html}
    <div id="{f}-rotor" style="position:absolute;left:{CX}px;top:{CY}px;width:0;height:0">
      <div id="{f}-dot" style="position:absolute;left:-18px;top:{-R - 18}px;width:36px;height:36px;border-radius:50%;background:{AMBER};box-shadow:0 0 30px {AMBER};opacity:0"></div>
    </div>
    <div id="{f}-out" style="position:absolute;left:{EX1 - 150}px;top:{EY1 - 110}px;width:260px;height:90px;border-radius:9999px;border:3px solid {ROSE};
         background:rgba(255,143,163,.12);color:{ROSE};display:flex;align-items:center;justify-content:center;font-family:'JetBrains Mono',monospace;font-size:36px">break: bahar</div>
    <div id="{f}-dot2" style="position:absolute;left:{EX0 - 18}px;top:{EY0 - 18}px;width:36px;height:36px;border-radius:50%;background:{ROSE};box-shadow:0 0 30px {ROSE};opacity:0"></div>"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.08),
      f'  tl.fromTo("#{f}-ring", {{ strokeDashoffset: 1383 }}, {{ strokeDashoffset: 0, duration: 0.8, ease: "power2.inOut" }}, 0.3);']
for i in range(3):
    js.append(f'  tl.fromTo("#{f}-n{i}", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "power3.out" }}, {0.5 + i * 0.15:.2f});')
js += [f'  tl.set("#{f}-dot", {{ opacity: 1 }}, 1.0);',
       f'  tl.fromTo("#{f}-rotor", {{ rotation: 0 }}, {{ rotation: 765, duration: 2.6, ease: "none" }}, 1.0);',
       f'  tl.set("#{f}-dot", {{ opacity: 0 }}, 3.6);',
       f'  tl.fromTo("#{f}-exit", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 3.5);',
       f'  tl.fromTo("#{f}-out", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "power3.out" }}, 3.5);',
       f'  tl.set("#{f}-dot2", {{ opacity: 1 }}, 3.6);',
       f'  tl.to("#{f}-dot2", {{ x: {EX1 - 70 - EX0}, y: {EY1 + 40 - EY0}, duration: 0.6, ease: "power2.in" }}, 3.6);',
       f'  tl.to("#{f}-dot2", {{ opacity: 0, duration: 0.2 }}, 4.2);']
write(f, 5, body, js)

# ---- Frame 5: payoff + teaser (6s, final: quiet hold) ----
f = "05-cta"
body = f"""    <div class="{f}-h" id="{f}-l1" style="top:110px;font-size:80px">{words(f, "while True = chalta raho", {0: f + "-c", 1: f + "-c", 3: f + "-a", 4: f + "-a"})}</div>
    <div class="{f}-h" id="{f}-l2" style="top:215px;font-size:80px">{words(f, "break = ruk jao", {0: f + "-c", 2: f + "-a", 3: f + "-a"})}</div>
    <div id="{f}-teaser" style="position:absolute;left:90px;top:420px;width:900px;height:220px;border-radius:20px;background:{NAVY};border:2px solid rgba(10,240,240,.5);
         box-sizing:border-box;padding:34px 44px;box-shadow:0 24px 70px rgba(0,0,0,.5)">
      <div style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:30px;letter-spacing:.16em;color:rgba(245,241,232,.66)">AGLA PART 11</div>
      <div style="font-size:54px;margin-top:22px;white-space:nowrap"><span class="{f}-c" style="font-family:'JetBrains Mono',monospace">file</span>: bill save karo</div>
    </div>
    <div class="{f}-pill" id="{f}-cta" style="left:230px;top:740px;width:620px;justify-content:center;background:rgba(10,240,240,.14);border:2px solid {CYAN};color:{CREAM}">
      Follow karo <span style="color:{CYAN}">·</span> Samjho with Raj</div>"""
js = [rise(f"#{f}-l1 .{f}-w", 0.05, 0.08), rise(f"#{f}-l2 .{f}-w", 0.8, 0.1),
      f'  tl.fromTo("#{f}-teaser", {{ opacity: 0, y: 70 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 1.7);',
      f'  tl.fromTo("#{f}-cta", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }}, 3.4);']
write(f, 6, body, js)
print("wrote", sorted(os.listdir(OUT)))
