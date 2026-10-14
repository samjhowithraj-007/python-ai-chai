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


# ---- Frame 1: hook (4s) ----
f = "01-hook"
body = f"""    <div class="{f}-kick" id="{f}-kick" style="top:100px">PART 8 · SAMJHO WITH RAJ</div>
    <div class="{f}-h" id="{f}-t1" style="top:180px;font-size:104px">{words(f, "Customer se", {})}</div>
    <div class="{f}-h" id="{f}-t2" style="top:295px;font-size:140px">{words(f, "pucho!", {0: f + "-a"})}</div>
    <div id="{f}-bub" style="position:absolute;left:190px;top:480px;width:700px;height:170px">
      <div style="position:absolute;inset:0;border-radius:40px;background:{CREAM};display:flex;align-items:center;justify-content:center;
           color:{INK};font-size:66px;box-shadow:0 24px 60px rgba(0,0,0,.5)">Kitne cup chahiye?</div>
      <svg width="80" height="60" viewBox="0 0 80 60" style="position:absolute;left:110px;top:160px"><path d="M0 0 L80 0 L10 60 Z" fill="{CREAM}"/></svg>
    </div>
    <div class="{f}-h" id="{f}-sub" style="top:770px;font-size:76px"><span class="{f}-w {f}-c" style="font-family:'JetBrains Mono',monospace">input()</span> <span class="{f}-w">se!</span></div>"""
js = [f'  tl.fromTo("#{f}-kick", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, 0.05);',
      rise(f"#{f}-t1 .{f}-w", 0.2, 0.1), rise(f"#{f}-t2 .{f}-w", 0.6, 0.1),
      f'  tl.fromTo("#{f}-bub", {{ opacity: 0, scale: 0.6, y: 40 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.5, ease: "power3.out" }}, 1.4);',
      rise(f"#{f}-sub .{f}-w", 2.8, 0.12)]
write(f, 4, body, js)

# ---- Frame 2: input() (7s) ----
f = "02-input"
lines = [f'naam = <span class="{f}-k">input</span>(<span class="{f}-s">"Naam? "</span>)',
         f'<span class="{f}-k">print</span>(<span class="{f}-s">"Namaste"</span>, naam)']
cardh, ns = card(f, lines, "left:60px;top:200px;width:960px;height:222px;font-size:40px")
inner = (f'<div id="{f}-q" style="font-size:50px;line-height:1.6;color:{CREAM}">Naam? {typed(f, "u", "Raj", CYAN)}</div>'
         f'<div id="{f}-o" style="font-size:50px;line-height:1.6;color:{AMBER}">Namaste Raj</div>')
body = f"""    <div class="{f}-h" id="{f}-head" style="top:80px;font-size:76px">{words(f, "input = user se pucho", {0: f + "-c", 4: f + "-a"})}</div>
{cardh}
    {terminal(f, inner, 60, 470, 960, 290)}
    <div class="{f}-h" id="{f}-lab" style="top:790px;font-size:44px;color:rgba(245,241,232,.75)">program <span class="{f}-a">rukta</span> hai, aapka jawab leta hai</div>"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.08),
      f'  tl.fromTo("#{f}-card", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.25);',
      type_line(f, 0, ns[0], 0.5, 0.6), type_line(f, 1, ns[1], 1.0, 0.6),
      f'  tl.fromTo("#{f}-term", {{ opacity: 0, y: 50 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, 1.6);',
      f'  tl.fromTo("#{f}-q", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 2.0);']
js += type_user(f, "u", 3, 2.9, 0.6)
js += [f'  tl.fromTo("#{f}-o", {{ opacity: 0, x: -24 }}, {{ opacity: 1, x: 0, duration: 0.4, ease: "power3.out" }}, 4.4);',
       f'  tl.fromTo("#{f}-lab", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power2.out" }}, 5.2);']
write(f, 7, body, js)

# ---- Frame 3: int(input()) (7s) ----
f = "03-int"
lines = [f'cups = <span class="{f}-k">int</span>(<span class="{f}-k">input</span>(<span class="{f}-s">"Kitne cup? "</span>))',
         f'bill = cups * <span class="{f}-n">20</span>',
         f'<span class="{f}-k">print</span>(<span class="{f}-s">"Bill:"</span>, bill)']
cardh, ns = card(f, lines, "left:60px;top:190px;width:960px;height:276px;font-size:38px")
inner = (f'<div id="{f}-q" style="font-size:50px;line-height:1.6;color:{CREAM}">Kitne cup? {typed(f, "u", "3", CYAN)}</div>'
         f'<div id="{f}-o" style="font-size:50px;line-height:1.6;color:{AMBER}">Bill: 60</div>')
arrow = (f'<svg width="70" height="30" viewBox="0 0 70 30"><path d="M4 15 L60 15 M46 4 L62 15 L46 26" stroke="{CREAM}" stroke-width="4" '
         f'fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')
body = f"""    <div class="{f}-h" id="{f}-head" style="top:76px;font-size:76px">{words(f, "int() = number banao", {0: f + "-c"})}</div>
{cardh}
    {terminal(f, inner, 60, 500, 600, 250)}
    <div id="{f}-chip" style="position:absolute;left:690px;top:560px;width:330px;height:130px;border-radius:20px;background:{NAVY};border:3px solid {CYAN};
         display:flex;align-items:center;justify-content:center;gap:18px;font-family:'JetBrains Mono',monospace;font-size:52px">
      <span style="color:{AMBER}">"3"</span>{arrow}<span style="color:{CYAN}">3</span></div>
    <div class="{f}-h" id="{f}-lab" style="top:790px;font-size:44px;color:rgba(245,241,232,.75)">text <span class="{f}-c">→</span> number</div>"""
body = body.replace(f'text <span class="{f}-c">→</span> number', f'input text deta hai, <span class="{f}-c">int()</span> number banata hai')
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.08),
      f'  tl.fromTo("#{f}-card", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.25)']
js[-1] += ";"
for i in range(3):
    js.append(type_line(f, i, ns[i], 0.5 + i * 0.4, 0.5))
js += [f'  tl.fromTo("#{f}-term", {{ opacity: 0, y: 50 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, 1.8);',
       f'  tl.fromTo("#{f}-q", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 2.2);']
js += type_user(f, "u", 1, 3.0, 0.2)
js += [f'  tl.fromTo("#{f}-chip", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "power3.out" }}, 3.6);',
       f'  tl.fromTo("#{f}-o", {{ opacity: 0, x: -24 }}, {{ opacity: 1, x: 0, duration: 0.4, ease: "power3.out" }}, 4.5);',
       f'  tl.fromTo("#{f}-lab", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power2.out" }}, 5.2);']
write(f, 7, body, js)

# ---- Frame 4: why int() (6s) ----
f = "04-why"
body = f"""    <div class="{f}-h" id="{f}-head" style="top:84px;font-size:84px">{words(f, "int() kyun?", {0: f + "-c"})}</div>
    <div id="{f}-L" style="position:absolute;left:40px;top:230px;width:490px;height:420px;border-radius:18px;background:{NAVY};border:3px solid rgba(255,143,163,.7);
         box-sizing:border-box;padding:40px 36px;font-family:'JetBrains Mono',monospace">
      <div style="font-size:54px;color:{CREAM}"><span style="color:{AMBER}">"3"</span> * 20</div>
      <div id="{f}-bad" style="margin-top:30px;font-size:40px;line-height:1.3;color:{ROSE};word-break:break-all">33333333333333333333</div>
    </div>
    <div id="{f}-oops" style="position:absolute;left:230px;top:520px;padding:14px 30px;border-radius:14px;border:5px solid {ROSE};color:{ROSE};
         font-size:58px;font-weight:700;background:rgba(14,17,22,.85)">Oops!</div>
    <div id="{f}-R" style="position:absolute;left:550px;top:230px;width:490px;height:420px;border-radius:18px;background:{NAVY};border:3px solid {CYAN};
         box-sizing:border-box;padding:40px 36px;font-family:'JetBrains Mono',monospace;box-shadow:0 0 50px rgba(10,240,240,.35)">
      <div style="font-size:54px;color:{CREAM}"><span style="color:{CYAN}">3</span> * 20</div>
      <div id="{f}-good" style="margin-top:40px;display:flex;align-items:center;gap:26px"><span style="font-size:150px;font-weight:700;color:{AMBER}">60</span>{CHECK}</div>
    </div>
    <div class="{f}-h" id="{f}-n1" style="top:680px;left:40px;right:auto;width:490px;font-size:44px;color:{ROSE}">bina int()</div>
    <div class="{f}-h {f}-c" id="{f}-n2" style="top:680px;left:550px;right:auto;width:490px;font-size:44px">int() ke saath</div>"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.1),
      f'  tl.fromTo("#{f}-L", {{ opacity: 0, y: 50 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, 0.4);',
      f'  tl.fromTo("#{f}-n1", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, 0.7);',
      f'  tl.fromTo("#{f}-bad", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.8, ease: "steps(20)" }}, 1.2);',
      f'  tl.fromTo("#{f}-oops", {{ opacity: 0, scale: 1.8, rotation: -20 }}, {{ opacity: 1, scale: 1, rotation: -8, duration: 0.35, ease: "power3.out" }}, 2.1);',
      f'  tl.fromTo("#{f}-R", {{ opacity: 0, y: 50 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, 2.8);',
      f'  tl.fromTo("#{f}-n2", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, 3.1);',
      f'  tl.fromTo("#{f}-good", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "power3.out" }}, 3.5);']
write(f, 6, body, js)

# ---- Frame 5: payoff + teaser (6s, final: quiet hold) ----
f = "05-cta"
body = f"""    <div class="{f}-h" id="{f}-l1" style="top:110px;font-size:84px">{words(f, "input = program se", {0: f + "-c"})}</div>
    <div class="{f}-h" id="{f}-l2" style="top:215px;font-size:96px">{words(f, "baat karo!", {0: f + "-a", 1: f + "-a"})}</div>
    <div id="{f}-teaser" style="position:absolute;left:90px;top:420px;width:900px;height:220px;border-radius:20px;background:{NAVY};border:2px solid rgba(10,240,240,.5);
         box-sizing:border-box;padding:34px 44px;box-shadow:0 24px 70px rgba(0,0,0,.5)">
      <div style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:30px;letter-spacing:.16em;color:rgba(245,241,232,.66)">AGLA PART 9</div>
      <div style="font-size:42px;margin-top:24px;white-space:nowrap"><span class="{f}-c" style="font-family:'JetBrains Mono',monospace">try-except</span>: galat input? No problem!</div>
    </div>
    <div class="{f}-pill" id="{f}-cta" style="left:230px;top:740px;width:620px;justify-content:center;background:rgba(10,240,240,.14);border:2px solid {CYAN};color:{CREAM}">
      Follow karo <span style="color:{CYAN}">·</span> Samjho with Raj</div>"""
js = [rise(f"#{f}-l1 .{f}-w", 0.05, 0.08), rise(f"#{f}-l2 .{f}-w", 0.7, 0.1),
      f'  tl.fromTo("#{f}-teaser", {{ opacity: 0, y: 70 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 1.7);',
      f'  tl.fromTo("#{f}-cta", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }}, 3.4);']
write(f, 6, body, js)
print("wrote", sorted(os.listdir(OUT)))
