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


# ---- Frame 1: hook (4s) ----
f = "01-hook"
inner = f'<div id="{f}-q" style="font-size:52px;color:{CREAM}">Kitne cup? {typed(f, "u", "teen", ROSE)}</div>'
body = f"""    {rose_style(f)}
    <div class="{f}-kick" id="{f}-kick" style="top:100px">PART 9 · SAMJHO WITH RAJ</div>
    <div class="{f}-h" id="{f}-t1" style="top:180px;font-size:110px">{words(f, "Galat", {})}</div>
    <div class="{f}-h" id="{f}-t2" style="top:295px;font-size:140px">{words(f, "input?", {0: f + "-a"})}</div>
    {terminal(f, inner, 190, 490, 700, 190)}
    <div class="{f}-h" id="{f}-sub" style="top:760px;font-size:66px"><span class="{f}-w {f}-c" style="font-family:'JetBrains Mono',monospace">try-except</span> <span class="{f}-w">bachayega!</span></div>"""
js = [f'  tl.fromTo("#{f}-kick", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, 0.05);',
      rise(f"#{f}-t1 .{f}-w", 0.2, 0.1), rise(f"#{f}-t2 .{f}-w", 0.5, 0.1),
      f'  tl.fromTo("#{f}-term", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, 1.2);']
js += type_user(f, "u", 4, 1.9, 0.6)
js.append(rise(f"#{f}-sub .{f}-w", 2.8, 0.12))
write(f, 4, body, js)

# ---- Frame 2: crash (7s) ----
f = "02-crash"
lines = [f'cups = <span class="{f}-k">int</span>(<span class="{f}-k">input</span>(<span class="{f}-s">"Kitne cup? "</span>))']
cardh, ns = card(f, lines, "left:60px;top:200px;width:960px;height:155px;font-size:38px")
inner = (f'<div id="{f}-q" style="font-size:46px;line-height:1.5;color:{CREAM}">Kitne cup? {typed(f, "u", "teen", ROSE)}</div>'
         f'<div id="{f}-e0" style="font-size:36px;line-height:1.5;color:{ROSE};margin-top:10px">ValueError: invalid literal</div>'
         f'<div id="{f}-e1" style="font-size:36px;line-height:1.5;color:{ROSE}">for int(): \'teen\'</div>')
body = f"""    {rose_style(f)}
    <div class="{f}-h" id="{f}-head" style="top:80px;font-size:84px">{words(f, "Bina try: crash!", {2: f + "-r"})}</div>
{cardh}
    {terminal(f, inner, 60, 400, 960, 330)}
    <div id="{f}-stamp" style="position:absolute;left:620px;top:640px;padding:16px 40px;border-radius:16px;border:6px solid {ROSE};color:{ROSE};
         font-size:80px;font-weight:700;letter-spacing:.04em;background:rgba(14,17,22,.9)">CRASH!</div>"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.1),
      f'  tl.fromTo("#{f}-card", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.25);',
      type_line(f, 0, ns[0], 0.5, 0.8),
      f'  tl.fromTo("#{f}-term", {{ opacity: 0, y: 50 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, 1.2);',
      f'  tl.fromTo("#{f}-q", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 1.6);']
js += type_user(f, "u", 4, 2.3, 0.7)
js += [f'  tl.fromTo("#{f}-e0", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15 }}, 3.5);',
       f'  tl.fromTo("#{f}-e1", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15 }}, 3.7);']
for k, dx in enumerate([-18, 16, -12, 8, 0]):
    js.append(f'  tl.to("#{f}-term", {{ x: {dx}, duration: 0.06, ease: "none" }}, {3.9 + k * 0.06:.2f});')
js.append(f'  tl.fromTo("#{f}-stamp", {{ opacity: 0, scale: 1.8, rotation: -20 }}, {{ opacity: 1, scale: 1, rotation: -8, duration: 0.35, ease: "power3.out" }}, 4.3);')
write(f, 7, body, js)

# ---- Frame 3: try-except (8s) ----
f = "03-try"
LH = 34 * 1.6
CT = 190
lines = [f'<span class="{f}-k">try</span>:',
         f'    cups = <span class="{f}-k">int</span>(<span class="{f}-k">input</span>(<span class="{f}-s">"Kitne cup? "</span>))',
         f'<span class="{f}-k">except</span> ValueError:',
         f'    <span class="{f}-k">print</span>(<span class="{f}-s">"Number likho!"</span>)']
cardh, ns = card(f, lines, f"left:40px;top:{CT}px;width:1000px;height:312px;font-size:34px")
y = lambda i: int(CT + 64 + i * LH - 4)
inner = (f'<div id="{f}-q" style="font-size:44px;line-height:1.5;color:{CREAM}">Kitne cup? {typed(f, "u", "teen", ROSE)}</div>'
         f'<div id="{f}-o" style="font-size:46px;line-height:1.5;color:{AMBER}">Number likho!</div>')
body = f"""    <div class="{f}-h" id="{f}-head" style="top:76px;font-size:78px">{words(f, "try-except = safety net", {0: f + "-c"})}</div>
{cardh}
    <div id="{f}-hl" style="position:absolute;left:42px;top:{y(1)}px;width:996px;height:{int(LH)}px;background:rgba(10,240,240,.14);border-left:6px solid {CYAN};opacity:0"></div>
    {terminal(f, inner, 40, 540, 720, 230)}
    <div id="{f}-shield" style="position:absolute;left:810px;top:540px;width:220px;text-align:center">{SHIELD}</div>"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.08),
      f'  tl.fromTo("#{f}-card", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.2);']
for i in range(4):
    js.append(type_line(f, i, ns[i], 0.4 + i * 0.3, 0.4))
js += [f'  tl.fromTo("#{f}-hl", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 1.8);',
       f'  tl.fromTo("#{f}-term", {{ opacity: 0, y: 50 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, 2.0);',
       f'  tl.fromTo("#{f}-q", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 2.3);']
js += type_user(f, "u", 4, 2.9, 0.6)
js += [f'  tl.fromTo("#{f}-hl", {{ backgroundColor: "rgba(10,240,240,.14)", borderLeftColor: "{CYAN}" }}, {{ backgroundColor: "rgba(255,143,163,.25)", borderLeftColor: "{ROSE}", duration: 0.2, immediateRender: false }}, 4.0);',
       f'  tl.to("#{f}-hl", {{ y: {y(2) - y(1)}, backgroundColor: "rgba(10,240,240,.14)", borderLeftColor: "{CYAN}", duration: 0.35, ease: "power2.inOut" }}, 4.5);',
       f'  tl.fromTo("#{f}-shield", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "power3.out" }}, 4.6);',
       f'  tl.to("#{f}-hl", {{ y: {y(3) - y(1)}, duration: 0.3, ease: "power2.inOut" }}, 5.3);',
       f'  tl.fromTo("#{f}-o", {{ opacity: 0, x: -24 }}, {{ opacity: 1, x: 0, duration: 0.4, ease: "power3.out" }}, 5.8);']
write(f, 8, body, js)

# ---- Frame 4: two paths (5s) ----
f = "04-paths"
NX, NY = 540, 300
LX, RX, CY = 280, 800, 640
body = f"""    {rose_style(f)}
    <div class="{f}-h" id="{f}-head" style="top:80px;font-size:76px">{words(f, "Error? except sambhalega", {0: f + "-r", 1: f + "-c"})}</div>
    <svg width="1080" height="1080" viewBox="0 0 1080 1080" style="position:absolute;left:0;top:0" fill="none">
      <path id="{f}-pl" d="M{NX} {NY + 50} L{LX} {CY - 80}" stroke="{CYAN}" stroke-width="8" stroke-linecap="round" stroke-dasharray="420" stroke-dashoffset="420"/>
      <path id="{f}-pr" d="M{NX} {NY + 50} L{RX} {CY - 80}" stroke="{ROSE}" stroke-width="8" stroke-linecap="round" stroke-dasharray="420" stroke-dashoffset="420"/>
    </svg>
    <div id="{f}-node" style="position:absolute;left:{NX - 140}px;top:{NY - 50}px;width:280px;height:100px;border-radius:9999px;background:{NAVY};
         border:3px solid rgba(245,241,232,.5);display:flex;align-items:center;justify-content:center;font-family:'JetBrains Mono',monospace;font-size:52px;color:{CYAN}">try</div>
    <div id="{f}-ll" style="position:absolute;left:{(NX + LX) // 2 - 140}px;top:{(NY + CY) // 2 - 50}px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:42px;color:{CYAN}">OK</div>
    <div id="{f}-lr" style="position:absolute;left:{(NX + RX) // 2 + 40}px;top:{(NY + CY) // 2 - 50}px;font-family:'JetBrains Mono',monospace;font-weight:700;font-size:42px;color:{ROSE}">Error</div>
    <div id="{f}-cl" style="position:absolute;left:{LX - 200}px;top:{CY - 80}px;width:400px;height:170px;border-radius:20px;background:{NAVY};border:3px solid {CYAN};
         display:flex;align-items:center;justify-content:center;font-size:54px;text-align:center">chalta raho</div>
    <div id="{f}-cr" style="position:absolute;left:{RX - 200}px;top:{CY - 80}px;width:400px;height:170px;border-radius:20px;background:{NAVY};border:3px solid {AMBER};
         display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:46px;text-align:center">
      <span style="font-family:'JetBrains Mono',monospace;color:{AMBER};font-size:40px">except:</span>pyaar se samjhao</div>
    <div id="{f}-dot" style="position:absolute;left:{NX - 18}px;top:{NY + 32}px;width:36px;height:36px;border-radius:50%;background:{AMBER};box-shadow:0 0 30px {AMBER};opacity:0"></div>"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.1),
      f'  tl.fromTo("#{f}-node", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "power3.out" }}, 0.5);',
      f'  tl.fromTo("#{f}-pl", {{ strokeDashoffset: 420 }}, {{ strokeDashoffset: 0, duration: 0.6, ease: "power2.out" }}, 1.0);',
      f'  tl.fromTo("#{f}-pr", {{ strokeDashoffset: 420 }}, {{ strokeDashoffset: 0, duration: 0.6, ease: "power2.out" }}, 1.1);',
      f'  tl.fromTo(["#{f}-ll", "#{f}-lr"], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, stagger: 0.12 }}, 1.5);',
      f'  tl.fromTo("#{f}-cl", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, 1.7);',
      f'  tl.fromTo("#{f}-cr", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power3.out" }}, 1.9);',
      f'  tl.set("#{f}-dot", {{ opacity: 1, x: 0, y: 0 }}, 2.4);',
      f'  tl.to("#{f}-dot", {{ x: {LX - NX}, y: {CY - 80 - NY - 50}, duration: 0.7, ease: "power2.inOut" }}, 2.4);',
      f'  tl.set("#{f}-dot", {{ x: 0, y: 0 }}, 3.4);',
      f'  tl.to("#{f}-dot", {{ x: {RX - NX}, y: {CY - 80 - NY - 50}, duration: 0.7, ease: "power2.inOut" }}, 3.4);',
      f'  tl.fromTo("#{f}-cr", {{ boxShadow: "0 0 0 rgba(255,176,32,0)" }}, {{ boxShadow: "0 0 50px rgba(255,176,32,.6)", duration: 0.4, immediateRender: false }}, 4.1);']
write(f, 5, body, js)

# ---- Frame 5: payoff + teaser (6s, final: quiet hold) ----
f = "05-cta"
body = f"""    <div class="{f}-h" id="{f}-l1" style="top:110px;font-size:80px">{words(f, "try-except = crash nahi,", {0: f + "-c"})}</div>
    <div class="{f}-h" id="{f}-l2" style="top:215px;font-size:110px">{words(f, "samjhao!", {0: f + "-a"})}</div>
    <div id="{f}-teaser" style="position:absolute;left:90px;top:420px;width:900px;height:220px;border-radius:20px;background:{NAVY};border:2px solid rgba(10,240,240,.5);
         box-sizing:border-box;padding:34px 44px;box-shadow:0 24px 70px rgba(0,0,0,.5)">
      <div style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:30px;letter-spacing:.16em;color:rgba(245,241,232,.66)">AGLA PART 10</div>
      <div style="font-size:48px;margin-top:22px;white-space:nowrap"><span class="{f}-c" style="font-family:'JetBrains Mono',monospace">while True</span>: dukaan khuli rakho</div>
    </div>
    <div class="{f}-pill" id="{f}-cta" style="left:230px;top:740px;width:620px;justify-content:center;background:rgba(10,240,240,.14);border:2px solid {CYAN};color:{CREAM}">
      Follow karo <span style="color:{CYAN}">·</span> Samjho with Raj</div>"""
js = [rise(f"#{f}-l1 .{f}-w", 0.05, 0.08), rise(f"#{f}-l2 .{f}-w", 0.7, 0.1),
      f'  tl.fromTo("#{f}-teaser", {{ opacity: 0, y: 70 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 1.7);',
      f'  tl.fromTo("#{f}-cta", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }}, 3.4);']
write(f, 6, body, js)
print("wrote", sorted(os.listdir(OUT)))
