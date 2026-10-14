"""Part 1 of AI + Python: chai ka chatbot banao. Writes compositions/frames/NN-*.html (one <template> sub-composition each) from the storyboard's shot sequences.
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


MONO = "font-family:'JetBrains Mono',monospace"

# ---- Frame 1: hook (4s) ----
f = "01-hook"
body = f"""    <div class="{f}-kick" id="{f}-kick" style="top:90px">AI + PYTHON · PART 1</div>
    <div class="{f}-h" id="{f}-t1" style="top:160px;font-size:104px">{words(f, "Chai ka")}</div>
    <div class="{f}-h" id="{f}-t2" style="top:275px;font-size:104px">{words(f, "chatbot banao!", {0: f + "-a"})}</div>
    {bot_svg(f, "bot", 330, "left:375px;top:420px")}
    <div class="{f}-h {f}-c" id="{f}-sub" style="top:780px;font-size:76px;{MONO}">Chai Bot</div>"""
js = [f'  tl.fromTo("#{f}-kick", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, 0.05);',
      rise(f"#{f}-t1 .{f}-w", 0.2, 0.1), rise(f"#{f}-t2 .{f}-w", 0.5, 0.1),
      f'  tl.fromTo("#{f}-bot", {{ opacity: 0, scale: 0.4, rotation: -12 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.7, ease: "back.out(1.8)", transformOrigin: "50% 50%" }}, 1.2);']
js += blink(f, "bot", 2.3) + blink(f, "bot", 3.4)
js.append(fade_up(f"#{f}-sub", 2.6, 0.45, 30))
write(f, 4, body, js)

# ---- Frame 2: chatbot kya hai? (7s) ----
f = "02-chat"
dots = "".join(f'<i class="{f}-dot" style="display:block;width:16px;height:16px;border-radius:50%;background:{CYAN}"></i>' for _ in range(3))
inner = (bubble(f, "m1", "Bhaiya, menu?", "cust", 110)
         + bubble(f, "ty", dots, "bot", 210)
         + bubble(f, "m2", "Masala, Adrak, Elaichi!", "bot", 210)
         + bubble(f, "m3", "Ek masala chai", "cust", 320)
         + bubble(f, "m4", f"Chai ready! {mini_cup(AMBER, 52)}", "bot", 420))
body = f"""    <div class="{f}-h" id="{f}-head" style="top:66px;font-size:80px">{words(f, "Chatbot kya hai?", {0: f + "-c"})}</div>
    <div id="{f}-win" style="position:absolute;left:90px;top:180px;width:900px;height:690px;border-radius:24px;background:#0A0C10;
         border:1px solid rgba(245,241,232,.16);box-shadow:0 24px 70px rgba(0,0,0,.5);overflow:hidden">
      <div style="position:absolute;left:0;right:0;top:0;height:76px;background:{NAVY};border-bottom:1px solid rgba(245,241,232,.12)"></div>
      {bot_svg(f, "hb", 52, "left:24px;top:12px")}
      <div style="position:absolute;left:92px;top:18px;font-size:34px;font-weight:700">Chai Bot <span style="color:#7CE38B;font-size:26px">● online</span></div>
      <div style="position:absolute;left:0;right:0;top:0;height:690px">{inner}</div>
      <div class="{f}-h {f}-a" id="{f}-cap" style="top:580px;font-size:46px">Program jo aapse baat kare</div>
    </div>"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.08), fade_up(f"#{f}-win", 0.25, 0.6, 60),
      f'  tl.fromTo("#{f}-m1", {{ opacity: 0, x: 40 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }}, 0.9);',
      f'  tl.fromTo("#{f}-tya", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 1.4);',
      f'  tl.fromTo("#{f}-ty", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 1.4);',
      f'  tl.fromTo("#{f}-ty .{f}-dot", {{ y: 0 }}, {{ y: -10, duration: 0.18, ease: "sine.inOut", stagger: 0.12 }}, 1.55);',
      f'  tl.to("#{f}-ty .{f}-dot", {{ y: 0, duration: 0.18, ease: "sine.inOut", stagger: 0.12 }}, 1.75);',
      f'  tl.set("#{f}-ty", {{ opacity: 0 }}, 2.2);',
      f'  tl.fromTo("#{f}-m2a", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.01 }}, 2.2);',
      f'  tl.set("#{f}-tya", {{ opacity: 0 }}, 2.21);',
      f'  tl.fromTo("#{f}-m2", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }}, 2.2);',
      f'  tl.fromTo("#{f}-m3", {{ opacity: 0, x: 40 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }}, 3.2);',
      f'  tl.fromTo("#{f}-m4a", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 4.1);',
      f'  tl.fromTo("#{f}-m4", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }}, 4.1);',
      fade_up(f"#{f}-cap", 5.0, 0.5, 30)]
js += blink(f, "hb", 3.0)
write(f, 7, body, js)

# ---- Frame 3: bas 3 cheezein (5s) ----
f = "03-three"
rows = [("input()", "suno"), ("print()", "jawab do"), ("while True", "chalte raho")]
rh = ""
for i, (code, word) in enumerate(rows):
    top = 250 + i * 165
    rh += (f'<div id="{f}-r{i}" style="position:absolute;left:90px;top:{top}px;width:900px;height:130px">'
           f'<div style="position:absolute;left:0;top:0;width:420px;height:130px;border-radius:18px;background:{NAVY};border:3px solid {CYAN};'
           f'display:flex;align-items:center;justify-content:center;{MONO};font-size:54px;color:{CYAN}">{code}</div>'
           f'<svg width="90" height="40" viewBox="0 0 90 40" style="position:absolute;left:440px;top:45px" fill="none">'
           f'<path d="M4 20 L74 20 M58 6 L78 20 L58 34" stroke="{CREAM}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
           f'<div class="{f}-a" style="position:absolute;left:550px;top:0;height:130px;display:flex;align-items:center;font-size:72px;font-weight:700;white-space:nowrap">{word}</div></div>')
body = f"""    <div class="{f}-h" id="{f}-head" style="top:90px;font-size:88px">{words(f, "Bas 3 cheezein!", {1: f + "-a"})}</div>
    {rh}
    <div class="{f}-h" id="{f}-foot" style="top:770px;font-size:46px;color:rgba(245,241,232,.8)">Sab aap Part 1–10 mein seekh chuke ho!</div>"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.1)]
for i in range(3):
    js.append(f'  tl.fromTo("#{f}-r{i}", {{ opacity: 0, x: -60 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }}, {0.6 + i * 0.7:.2f});')
js.append(fade_up(f"#{f}-foot", 3.0, 0.5, 30))
write(f, 5, body, js)

# ---- Frame 4: pehla chai bot (8s) ----
f = "04-code"
LH = 32 * 1.6
CT = 170
lines = [f'<span class="{f}-k">while True</span>:',
         f'    msg = <span class="{f}-k">input</span>(<span class="{f}-s">"Aap: "</span>)',
         f'    <span class="{f}-k">if</span> msg == <span class="{f}-s">"bye"</span>: <span class="{f}-k">break</span>',
         f'    <span class="{f}-k">print</span>(<span class="{f}-s">"Bot: Chai ready!"</span>)']
cardh, ns = card(f, lines, f"left:40px;top:{CT}px;width:720px;height:312px;font-size:32px", fname="chai_bot.py")
y = lambda i: int(CT + 64 + i * LH - 4)
row = lambda rid, txt, col: f'<div id="{f}-{rid}" style="font-size:38px;line-height:1.45;color:{col}">{txt}</div>'
inner = (row("q1", f'Aap: {typed(f, "u1", "menu", CYAN)}', CREAM) + row("o1", "Bot: Chai ready!", AMBER)
         + row("q2", f'Aap: {typed(f, "u2", "kaise ho?", CYAN)}', CREAM) + row("o2", "Bot: Chai ready!", AMBER))
body = f"""    {rose_style(f)}
    <div class="{f}-h" id="{f}-head" style="top:66px;font-size:80px">{words(f, "Pehla Chai Bot", {2: f + "-c"})}</div>
{cardh}
    <div id="{f}-hl" style="position:absolute;left:42px;top:{y(1)}px;width:716px;height:{int(LH)}px;background:rgba(10,240,240,.14);border-left:6px solid {CYAN};opacity:0"></div>
    {bot_svg(f, "bot", 230, "left:800px;top:190px")}
    <div id="{f}-v1" style="position:absolute;left:790px;top:430px;width:250px;text-align:center;{MONO};font-size:30px;color:rgba(245,241,232,.7)">version 1</div>
    {terminal(f, inner, 40, 510, 1000, 370)}
    <div id="{f}-stamp" class="{f}-r" style="position:absolute;left:330px;top:640px;padding:18px 34px;border:5px solid {ROSE};border-radius:16px;
         background:rgba(14,17,22,.92);font-size:56px;font-weight:700;white-space:nowrap;transform:rotate(-6deg)">Abhi bot buddhu hai!</div>"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.08),
      fade_up(f"#{f}-card", 0.2, 0.6, 60), pop(f"#{f}-bot", 0.4, 0.5),
      f'  tl.fromTo("#{f}-v1", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, 0.7);']
for i in range(4):
    js.append(type_line(f, i, ns[i], 0.4 + i * 0.25, 0.35))
js += [fade_up(f"#{f}-term", 1.6, 0.5), f'  tl.fromTo("#{f}-hl", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, 1.8);']
for k, (txt, t0) in enumerate([("menu", 2.0), ("kaise ho?", 3.9)]):
    q, u, o = f"q{k + 1}", f"u{k + 1}", f"o{k + 1}"
    if k:
        js.append(f'  tl.to("#{f}-hl", {{ y: 0, duration: 0.3, ease: "power2.inOut" }}, {t0 - 0.2:.2f});')
    js.append(f'  tl.fromTo("#{f}-{q}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15 }}, {t0:.2f});')
    js += type_user(f, u, len(txt), t0 + 0.4, 0.5)
    js.append(f'  tl.to("#{f}-hl", {{ y: {y(3) - y(1)}, duration: 0.3, ease: "power2.inOut" }}, {t0 + 1.2:.2f});')
    js.append(f'  tl.fromTo("#{f}-{o}", {{ opacity: 0, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }}, {t0 + 1.4:.2f});')
js += [f'  tl.fromTo("#{f}-stamp", {{ opacity: 0, scale: 1.6, rotation: -6 }}, {{ opacity: 1, scale: 1, rotation: -6, duration: 0.35, ease: "power4.in" }}, 6.0);',
       f'  tl.to("#{f}-bot", {{ rotation: -10, duration: 0.25, ease: "power2.out", transformOrigin: "50% 50%" }}, 6.3);',
       f'  tl.to("#{f}-bot", {{ rotation: 0, duration: 0.4, ease: "back.out(2)", transformOrigin: "50% 50%" }}, 6.55);']
js += blink(f, "bot", 1.2) + blink(f, "bot", 6.2)
write(f, 8, body, js)

import sys
PLATFORM = sys.argv[1] if len(sys.argv) > 1 else "yt"
BTN, BTN_BG = ("Subscribe", "#FF0000") if PLATFORM == "yt" else ("Follow", "#0095F6")

# ---- Frame 5: roadmap + teaser (6s, final: quiet hold) ----
f = "05-cta"
stops = [("Smart bot", "Part 1–10", ROSE, 120), ("AI bot", "Part 11–20", AMBER, 330), ("Super bot", "Part 21–30", "#B8F5A0", 540),
         ("App bot", "Part 31–40", "#C9A7FF", 750), ("AI Agent", "Part 41–50", CYAN, 960)]
sh = ""
for i, (name, part, col, cx) in enumerate(stops):
    sh += (f'<div id="{f}-s{i}" style="position:absolute;left:{cx - 105}px;top:250px;width:210px;text-align:center">'
           f'<div style="margin:0 auto;width:56px;height:56px;border-radius:50%;background:#0A0C10;border:6px solid {col};box-sizing:border-box;box-shadow:0 0 26px {col}"></div>'
           f'<div style="margin-top:16px;font-size:38px;font-weight:700;color:{col};white-space:nowrap">{name}</div>'
           f'<div style="{MONO};font-size:25px;color:rgba(245,241,232,.7);white-space:nowrap">{part}</div></div>')
body = f"""    <div class="{f}-h" id="{f}-head" style="top:90px;font-size:84px">{words(f, "50 parts ka safar", {0: f + "-a", 1: f + "-a"})}</div>
    <svg width="1080" height="1080" viewBox="0 0 1080 1080" style="position:absolute;left:0;top:0" fill="none">
      <path id="{f}-path" d="M120 278 L960 278" stroke="rgba(245,241,232,.35)" stroke-width="6" stroke-dasharray="840" stroke-dashoffset="840"/>
    </svg>
    {sh}
    <div id="{f}-dot" style="position:absolute;left:102px;top:260px;width:36px;height:36px;border-radius:50%;background:{AMBER};box-shadow:0 0 30px {AMBER};opacity:0"></div>
    <div id="{f}-teaser" style="position:absolute;left:90px;top:500px;width:900px;height:200px;border-radius:20px;background:{NAVY};border:2px solid rgba(10,240,240,.5);
         box-sizing:border-box;padding:30px 44px;box-shadow:0 24px 70px rgba(0,0,0,.5)">
      <div style="{MONO};font-weight:700;font-size:30px;letter-spacing:.16em;color:rgba(245,241,232,.66)">AGLA PART 2</div>
      <div style="font-size:54px;margin-top:20px;white-space:nowrap"><span class="{f}-c" style="{MONO}">if-else</span>: bot ko jawab sikhao</div>
    </div>
    <div id="{f}-sb" style="position:absolute;left:50%;transform:translateX(-50%);top:745px;height:132px;padding:0 22px 0 18px;border-radius:9999px;
         background:rgba(255,255,255,.08);border:3px solid rgba(255,255,255,.22);box-shadow:0 24px 80px rgba(0,0,0,.5);
         display:flex;align-items:center;gap:22px;white-space:nowrap;box-sizing:border-box">
      <div style="width:100px;height:100px;border-radius:50%;overflow:hidden;background:#111;flex:none"><img src="assets/img/raj-mark.png" alt="" style="width:100px;height:100px;display:block"></div>
      <div><div style="font-size:42px;font-weight:700;line-height:1.05">Samjho with Raj</div>
        <div style="font-size:23px;font-weight:400;color:rgba(245,241,232,.85)">AI + Python series · har hafte naya part</div></div>
      <div id="{f}-btn" style="margin-left:10px;background:{BTN_BG};color:#fff;font-weight:700;font-size:32px;padding:16px 30px;border-radius:9999px">{BTN}</div>
    </div>"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.08),
      f'  tl.fromTo("#{f}-path", {{ strokeDashoffset: 840 }}, {{ strokeDashoffset: 0, duration: 1.6, ease: "none" }}, 0.4);']
for i in range(5):
    js.append(pop(f"#{f}-s{i}", 0.4 + i * 0.4, 0.4))
js += [f'  tl.set("#{f}-dot", {{ opacity: 1 }}, 0.4);',
       f'  tl.to("#{f}-dot", {{ x: 840, duration: 1.6, ease: "none" }}, 0.4);',
       f'  tl.to("#{f}-dot", {{ backgroundColor: "{CYAN}", boxShadow: "0 0 40px {CYAN}", duration: 0.3 }}, 1.8);',
       fade_up(f"#{f}-teaser", 2.0, 0.6, 70),
       f'  tl.fromTo("#{f}-sb", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, 3.0);',
       f'  tl.fromTo("#{f}-btn", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.22, yoyo: true, repeat: 5, ease: "power1.inOut" }}, 3.6);']
write(f, 6, body, js)
print("wrote", sorted(os.listdir(OUT)))
