"""Part 3 of AI + Python: chai ka chatbot banao (dictionary). Writes compositions/frames/NN-*.html; timings in T (re-timed to the voice via timing.json).
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




# ======== AI + Python: chai ka chatbot banao — Part 1 ========

def bot_svg(fid, bid, size, style=""):
    """Chai Bot: rounded-square navy head, cyan eyes (class eye, blink by scaleY), amber antenna ball, cream smile."""
    return (f'<svg id="{fid}-{bid}" viewBox="0 0 200 200" width="{size}" height="{size}" fill="none" style="position:absolute;{style};'
            f'filter:drop-shadow(0 0 26px rgba(10,240,240,.45))">'
            f'<path d="M100 22 L100 42" stroke="{CREAM}" stroke-width="7" stroke-linecap="round"/>'
            f'<circle cx="100" cy="16" r="11" fill="{AMBER}"/>'
            f'<rect x="14" y="88" width="16" height="40" rx="6" fill="{CYAN}" opacity=".7"/>'
            f'<rect x="170" y="88" width="16" height="40" rx="6" fill="{CYAN}" opacity=".7"/>'
            f'<rect x="30" y="42" width="140" height="128" rx="36" fill="{NAVY}" stroke="{CYAN}" stroke-width="7"/>'
            f'<ellipse class="{fid}-eye" cx="74" cy="100" rx="14" ry="17" fill="{CYAN}"/>'
            f'<ellipse class="{fid}-eye" cx="126" cy="100" rx="14" ry="17" fill="{CYAN}"/>'
            f'<path d="M72 135 Q100 156 128 135" stroke="{CREAM}" stroke-width="7" stroke-linecap="round"/></svg>')


def blink(fid, bid, t):
    return [f'  tl.to("#{fid}-{bid} .{fid}-eye", {{ scaleY: 0.1, transformOrigin: "50% 50%", duration: 0.07 }}, {t:.2f});',
            f'  tl.to("#{fid}-{bid} .{fid}-eye", {{ scaleY: 1, transformOrigin: "50% 50%", duration: 0.09 }}, {t + 0.1:.2f});']


def pop(sel, t, d=0.4):
    return f'  tl.fromTo("{sel}", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: {d}, ease: "back.out(1.7)" }}, {t:.2f});'


def fade_up(sel, t, d=0.5, y=50):
    return f'  tl.fromTo("{sel}", {{ opacity: 0, y: {y} }}, {{ opacity: 1, y: 0, duration: {d}, ease: "power3.out" }}, {t:.2f});'


def bubble(fid, bid, html, side, top):
    if side == "bot":
        pos, bg, bd, col, rad = "left:110px", "rgba(10,240,240,.12)", CYAN, CREAM, "8px 28px 28px 28px"
        av = (f'<div id="{fid}-{bid}a" style="position:absolute;left:26px;top:{top + 4}px;width:64px;height:64px">'
              f'{bot_svg(fid, bid + "f", 64, "left:0;top:0")}</div>')
    else:
        pos, bg, bd, col, rad, av = "right:30px", CREAM, CREAM, INK, "28px 8px 28px 28px", ""
    return (av + f'<div id="{fid}-{bid}" style="position:absolute;{pos};top:{top}px;padding:14px 30px;border-radius:{rad};background:{bg};'
            f'border:3px solid {bd};color:{col};font-size:40px;font-weight:700;white-space:nowrap;display:flex;align-items:center;gap:14px">{html}</div>')


MONO = "font-family:'JetBrains Mono',monospace;font-variant-ligatures:none"



# ======== Part 3: 50 if-else? Nahi! Dictionary se ========
import sys, json as _json
PLATFORM = sys.argv[1] if len(sys.argv) > 1 else "yt"
BTN, BTN_BG = ("Subscribe", "#FF0000") if PLATFORM == "yt" else ("Follow", "#0095F6")
GREEN = "#7CE38B"

T = {
    "hook": dict(len=4.2, x=1.4, sub=2.4),
    "pile": dict(len=8.0, chips=[0.8, 1.6, 2.4, 3.0, 3.5, 3.9, 4.2, 4.5], count=5.0, stamp=6.2),
    "diary": dict(len=8.0, book=0.5, rows=[2.0, 3.6, 5.2]),
    "code": dict(len=10.0, term=2.2, q=[2.8, 4.6, 6.4], tip=5.6, stamp=8.4),
    "cta": dict(len=12.0, pill=0.7, web=4.5, teaser=6.5, sb=9.0, btn=9.4),
}
if os.path.exists(os.path.join(HERE, "timing.json")):
    T.update(_json.load(open(os.path.join(HERE, "timing.json")))["T"])   # re-timed to Raj's voice

# ---- Frame 1: hook ----
f = "01-hook"; t = T["hook"]
ghost = "".join(f'<div style="{MONO};font-size:30px;color:rgba(245,241,232,.55);white-space:nowrap;line-height:1.5">'
                f'<span style="color:rgba(10,240,240,.75)">elif</span> msg == "{w}": ...</div>'
                for w in ["menu", "price", "timing", "masala", "adrak", "elaichi", "tulsi", "chai", "bill", "address"])
body = f"""    {rose_style(f)}
    <div class="{f}-kick" id="{f}-kick" style="top:90px">AI + PYTHON · PART 3</div>
    <div class="{f}-h" id="{f}-t1" style="top:160px;font-size:104px">{words(f, "50 if-else?")}</div>
    <div class="{f}-h {f}-r" id="{f}-t2" style="top:275px;font-size:120px">{words(f, "Nahi!")}</div>
    <div id="{f}-ghost" style="position:absolute;left:250px;top:420px;width:580px;height:330px;overflow:hidden;border-radius:16px;
         background:rgba(24,23,21,.7);border:1px solid rgba(245,241,232,.12);padding:18px 28px;box-sizing:border-box">{ghost}</div>
    <svg id="{f}-x" width="300" height="300" viewBox="0 0 100 100" style="position:absolute;left:390px;top:435px" fill="none">
      <path d="M18 18 L82 82 M82 18 L18 82" stroke="{ROSE}" stroke-width="10" stroke-linecap="round" stroke-dasharray="91" stroke-dashoffset="91"/></svg>
    <div class="{f}-h {f}-c" id="{f}-sub" style="top:780px;font-size:76px;{MONO}">dictionary se!</div>"""
js = [f'  tl.fromTo("#{f}-kick", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, 0.05);',
      rise(f"#{f}-t1 .{f}-w", 0.2, 0.1), rise(f"#{f}-t2 .{f}-w", 0.7, 0.1),
      fade_up(f"#{f}-ghost", 0.5, 0.5, 40),
      f'  tl.fromTo("#{f}-ghost > div", {{ y: 0 }}, {{ y: -120, duration: 2.6, ease: "none" }}, 0.6);',
      f'  tl.fromTo("#{f}-x path", {{ strokeDashoffset: 91 }}, {{ strokeDashoffset: 0, duration: 0.35, ease: "power2.out" }}, {t["x"]});',
      fade_up(f"#{f}-sub", t["sub"], 0.45, 30)]
write(f, t["len"], body, js)

# ---- Frame 2: the pile of elifs ----
f = "02-pile"; t = T["pile"]
words_ = ["menu", "price", "timing", "masala", "adrak", "elaichi", "tulsi", "bill"]
chips = ""
for i, w in enumerate(words_):
    col, row = i % 2, i // 2
    kw = "if" if i == 0 else "elif"
    chips += (f'<div id="{f}-c{i}" style="position:absolute;left:{90 + col * 460}px;top:{200 + row * 108}px;width:430px;height:84px;border-radius:14px;'
              f'background:{NAVY};border:2px solid rgba(10,240,240,.45);display:flex;align-items:center;padding-left:20px;box-sizing:border-box;'
              f'{MONO};font-size:30px;white-space:pre"><span><span style="color:{CYAN}">{kw}</span> msg == <span style="color:{AMBER}">"{w}"</span></span></div>')
body = f"""    {rose_style(f)}
    <div class="{f}-h" id="{f}-head" style="top:76px;font-size:80px">{words(f, "Har sawaal = naya elif", {3: f + "-c"})}</div>
    {chips}
    <div id="{f}-count" class="{f}-r" style="position:absolute;left:90px;top:650px;font-size:64px;font-weight:700;white-space:nowrap">… 50 if-else 😵</div>
    <div id="{f}-stamp" class="{f}-r" style="position:absolute;left:120px;top:770px;padding:12px 28px;border:5px solid {ROSE};border-radius:16px;
         background:rgba(14,17,22,.92);font-size:46px;font-weight:700;white-space:nowrap;transform:rotate(-4deg)">Lamba aur messy!</div>"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.08)]
for i, tt in enumerate(t["chips"]):
    js.append(pop(f"#{f}-c{i}", tt, 0.3))
js += [fade_up(f"#{f}-count", t["count"], 0.4, 30),
       f'  tl.fromTo("#{f}-stamp", {{ opacity: 0, scale: 1.6, rotation: -4 }}, {{ opacity: 1, scale: 1, rotation: -4, duration: 0.35, ease: "power4.in" }}, {t["stamp"]});']
write(f, t["len"], body, js)

# ---- Frame 3: dictionary = the bot's diary ----
f = "03-diary"; t = T["diary"]
entries = [('"menu"', "Masala, Adrak!"), ('"price"', "Rs 20"), ('"timing"', "Subah 7 – raat 10")]
rows = "".join(f'<div id="{f}-r{i}" style="display:flex;align-items:center;gap:22px;height:96px;border-bottom:2px dashed rgba(245,241,232,.18);white-space:nowrap">'
               f'<span style="{MONO};font-size:40px;color:{CYAN};width:250px">{k}</span><span style="font-size:40px;color:{CREAM}">→</span>'
               f'<span class="{f}-a" style="font-size:44px;font-weight:700">{v}</span></div>' for i, (k, v) in enumerate(entries))
body = f"""    <div class="{f}-h" id="{f}-head" style="top:76px;font-size:78px">{words(f, "dictionary = jawab ki diary", {0: f + "-c", 3: f + "-a"})}</div>
    <div id="{f}-book" style="position:absolute;left:110px;top:210px;width:860px;height:470px;border-radius:22px;background:#1b1914;
         border:3px solid {AMBER};box-shadow:0 24px 70px rgba(0,0,0,.55);padding:34px 50px 30px 90px;box-sizing:border-box">
      <div style="position:absolute;left:46px;top:0;bottom:0;width:4px;background:rgba(255,143,163,.55)"></div>
      <div style="display:flex;gap:22px;{MONO};font-size:28px;letter-spacing:.14em;color:rgba(245,241,232,.6);margin-bottom:6px">
        <span style="width:250px">SAWAAL (key)</span><span style="width:38px"></span><span>JAWAB (value)</span></div>
      {rows}
    </div>"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.08), fade_up(f"#{f}-book", t["book"], 0.6, 60)]
for i, tt in enumerate(t["rows"]):
    js.append(f'  tl.fromTo("#{f}-r{i}", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }}, {tt:.2f});')
write(f, t["len"], body, js)

# ---- Frame 4: the code + terminal demo ----
f = "04-code"; t = T["code"]
LH = 32 * 1.6
CT = 170
lines = [f'replies = {{<span class="{f}-s">"menu"</span>: <span class="{f}-s">"Masala, Adrak!"</span>,',
         f'           <span class="{f}-s">"price"</span>: <span class="{f}-s">"Rs 20"</span>}}',
         f'msg = <span class="{f}-k">input</span>(<span class="{f}-s">"Aap: "</span>)',
         f'<span class="{f}-k">print</span>(replies.<span class="{f}-k">get</span>(msg, <span class="{f}-s">"Samjha nahi!"</span>))']
cardh, ns = card(f, lines, f"left:40px;top:{CT}px;width:1000px;height:312px;font-size:32px", fname="chai_bot.py · while True ke andar")
y = lambda i: int(CT + 64 + i * LH - 4)
row = lambda rid, txt, col: f'<div id="{f}-{rid}" style="font-size:36px;line-height:1.4;color:{col}">{txt}</div>'
demo = [("menu", "Masala, Adrak!"), ("price", "Rs 20"), ("kaise ho?", "Samjha nahi!")]
inner = "".join(row(f"q{k}", f'Aap: {typed(f, f"u{k}", q, CYAN)}', CREAM) + row(f"o{k}", f"Bot: {a}", ROSE if k == 2 else AMBER)
                for k, (q, a) in enumerate(demo))
body = f"""    <div class="{f}-h" id="{f}-head" style="top:66px;font-size:80px">{words(f, "Code chhota, jawab zyada", {1: f + "-c", 3: f + "-a"})}</div>
{cardh}
    <div id="{f}-hl" style="position:absolute;left:42px;top:{y(3)}px;width:996px;height:{int(LH)}px;background:rgba(10,240,240,.14);border-left:6px solid {CYAN};opacity:0"></div>
    {terminal(f, inner, 40, 500, 1000, 380)}
    <div id="{f}-tip" style="position:absolute;left:560px;top:560px;width:440px;padding:14px 22px;border-radius:14px;background:rgba(10,240,240,.1);
         border:2px solid {CYAN};box-sizing:border-box;font-size:30px;line-height:1.35"><span style="{MONO};color:{CYAN}">.get(msg, ...)</span><br>na mile toh "Samjha nahi!"</div>
    <div id="{f}-stamp" style="position:absolute;left:560px;top:690px;padding:12px 26px;border:5px solid {GREEN};border-radius:16px;color:{GREEN};
         background:rgba(14,17,22,.92);font-size:40px;font-weight:700;white-space:nowrap;transform:rotate(-5deg)">Naya sawaal = 1 line!</div>"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.08), fade_up(f"#{f}-card", 0.2, 0.6, 60)]
for i in range(4):
    js.append(type_line(f, i, ns[i], 0.4 + i * 0.3, 0.4))
js += [fade_up(f"#{f}-term", t["term"], 0.5), f'  tl.fromTo("#{f}-hl", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, {t["term"] + 0.3:.2f});']
for k, ((q, a), t0) in enumerate(zip(demo, t["q"])):
    js.append(f'  tl.fromTo("#{f}-q{k}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15 }}, {t0:.2f});')
    js += type_user(f, f"u{k}", len(q), t0 + 0.3, 0.45)
    js.append(f'  tl.fromTo("#{f}-o{k}", {{ opacity: 0, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }}, {t0 + 1.15:.2f});')
js += [fade_up(f"#{f}-tip", t["tip"], 0.45, 20),
       f'  tl.fromTo("#{f}-stamp", {{ opacity: 0, scale: 1.6, rotation: -5 }}, {{ opacity: 1, scale: 1, rotation: -5, duration: 0.35, ease: "power4.in" }}, {t["stamp"]});']
write(f, t["len"], body, js)

# ---- Frame 5: payoff + Part 4 teaser + website + channel bar ----
f = "05-cta"; t = T["cta"]
body = f"""    <div class="{f}-h" id="{f}-l1" style="top:90px;font-size:80px">{words(f, "dictionary = bot ki diary", {0: f + "-c", 3: f + "-a"})}</div>
    <div id="{f}-pill" style="position:absolute;left:50%;transform:translateX(-50%);top:215px;padding:12px 30px;border-radius:9999px;border:3px solid {GREEN};
         color:{GREEN};{MONO};font-weight:700;font-size:34px;white-space:nowrap">✓ PART 3 / 20</div>
    <div id="{f}-teaser" style="position:absolute;left:90px;top:330px;width:900px;height:200px;border-radius:20px;background:{NAVY};border:2px solid rgba(10,240,240,.5);
         box-sizing:border-box;padding:30px 44px;box-shadow:0 24px 70px rgba(0,0,0,.5)">
      <div style="{MONO};font-weight:700;font-size:30px;letter-spacing:.16em;color:rgba(245,241,232,.66)">AGLA PART 4</div>
      <div style="font-size:52px;margin-top:20px;white-space:nowrap">"MENU" ya "menu"? <span class="{f}-c" style="{MONO}">.lower()</span></div>
    </div>
    <div id="{f}-web" style="position:absolute;left:0;right:0;top:600px;text-align:center;font-size:40px;font-weight:700;white-space:nowrap">
      Free notes + code: <span class="{f}-c" style="{MONO}">samjhowithraj.online</span></div>
    <div id="{f}-sb" style="position:absolute;left:40px;top:745px;height:132px;padding:0 22px 0 18px;border-radius:9999px;
         background:rgba(255,255,255,.08);border:3px solid rgba(255,255,255,.22);box-shadow:0 24px 80px rgba(0,0,0,.5);
         display:flex;align-items:center;gap:22px;white-space:nowrap;box-sizing:border-box">
      <div style="width:100px;height:100px;border-radius:50%;overflow:hidden;background:#111;flex:none"><img src="assets/img/raj-mark.png" alt="" style="width:100px;height:100px;display:block"></div>
      <div><div style="font-size:42px;font-weight:700;line-height:1.05">Samjho with Raj</div>
        <div style="font-size:23px;font-weight:400;color:rgba(245,241,232,.85)">AI + Python series · har hafte naya part</div></div>
      <div id="{f}-btn" style="margin-left:10px;background:{BTN_BG};color:#fff;font-weight:700;font-size:32px;padding:16px 30px;border-radius:9999px">{BTN}</div>
    </div>"""
js = [rise(f"#{f}-l1 .{f}-w", 0.05, 0.08),
      f'  tl.fromTo("#{f}-pill", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {t["pill"]});',
      fade_up(f"#{f}-web", t["web"], 0.5, 30), fade_up(f"#{f}-teaser", t["teaser"], 0.6, 70),
      f'  tl.fromTo("#{f}-sb", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, {t["sb"]});',
      f'  tl.fromTo("#{f}-btn", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.22, yoyo: true, repeat: 5, ease: "power1.inOut" }}, {t["btn"]});']
write(f, t["len"], body, js)
print("wrote", sorted(os.listdir(OUT)))
