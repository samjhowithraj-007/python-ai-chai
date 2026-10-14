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


# ---- Frame 1: hook (5s) ----
f = "01-hook"
body = f"""    <div class="{f}-kick" id="{f}-kick" style="top:64px">SAMJHO WITH RAJ</div>
    <div class="{f}-h" id="{f}-q" style="top:140px;font-size:84px">{words(f, "Chai bana sakte ho?", {0: f + "-a"})}</div>
    <div class="{f}-h" id="{f}-ans" style="top:252px;font-size:104px">{words(f, "Toh Python bhi!", {1: f + "-c"})}</div>
{cup_svg(f, 400, "left:340px;top:440px")}"""
js = [f'  tl.fromTo("#{f}-kick", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, 0.1);',
      f'  tl.fromTo("#{f}-cup", {{ opacity: 0, y: 80, scale: 0.92 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.8, ease: "power3.out" }}, 0.15);',
      steam_js(f, 0.7),
      rise(f"#{f}-q .{f}-w", 1.6, 0.09),
      rise(f"#{f}-ans .{f}-w", 3.0, 0.12)]
write(f, 5, body, js)

# ---- Frame 2: ingredients = variables (7s) ----
f = "02-variables"
lines = [f'<span class="{f}-k">paani</span> = <span class="{f}-s">"1 cup"</span>',
         f'<span class="{f}-k">doodh</span> = <span class="{f}-s">"1/2 cup"</span>',
         f'<span class="{f}-k">chai_patti</span> = <span class="{f}-n">2</span>',
         f'<span class="{f}-k">cheeni</span> = <span class="{f}-n">1</span>']
cardh, ns = card(f, lines, "left:110px;top:330px;width:860px;height:420px;font-size:50px")
chips = ["Paani", "Doodh", "Patti", "Cheeni"]
chip_html = "".join(f'<div class="{f}-pill" id="{f}-chip{i}" style="left:{70 + i * 240}px;top:216px;width:220px;justify-content:center;'
                    f'background:rgba(255,176,32,.14);border:2px solid rgba(255,176,32,.6);color:{AMBER}">{c}</div>'
                    for i, c in enumerate(chips))
body = f"""    <div class="{f}-h" id="{f}-head" style="top:92px;font-size:76px">{words(f, "Ingredients = Variables", {2: f + "-c"})}</div>
    {chip_html}
{cardh}"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.08),
      f'  tl.fromTo("#{f}-card", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.4);']
for i, n in enumerate(ns):
    t = 1.0 + i * 1.15
    js.append(f'  tl.fromTo("#{f}-chip{i}", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }}, {t:.2f});')
    js.append(type_line(f, i, n, t, 0.8))
js.append(f'  tl.fromTo("#{f}-card .{f}-k", {{ textShadow: "0 0 0 rgba(10,240,240,0)" }}, {{ textShadow: "0 0 22px rgba(10,240,240,.9)", duration: 0.35, stagger: 0.25, ease: "power2.out" }}, 5.7);')
write(f, 7, body, js)

# ---- Frame 3: recipe = function (6s) ----
f = "03-function"
lines = [f'<span class="{f}-k">def</span> <span class="{f}-f">chai_banao</span>():',
         '    paani_ubaalo()', '    patti_daalo()', '    doodh_daalo()']
cardh, ns = card(f, lines, "left:110px;top:236px;width:860px;height:420px;font-size:50px")
pills = "".join(f'<div class="{f}-pill" id="{f}-p{i}" style="left:{88 + i * 312}px;top:700px;width:280px;justify-content:center;'
                f'background:rgba(255,176,32,.16);border:2px solid {AMBER};color:{AMBER};font-family:\'JetBrains Mono\',monospace;font-size:28px">chai_banao()</div>'
                for i in range(3))
body = f"""    <div class="{f}-h" id="{f}-head" style="top:92px;font-size:80px">{words(f, "Recipe = Function", {2: f + "-c"})}</div>
{cardh}
    {pills}
    <div class="{f}-h" id="{f}-sub" style="top:806px;font-size:40px;color:rgba(245,241,232,.75)">Ek baar likho, <span class="{f}-a">baar baar banao</span></div>"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.08),
      f'  tl.fromTo("#{f}-card", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.35);',
      type_line(f, 0, ns[0], 1.0, 0.75)]
for i in range(1, 4):
    js.append(type_line(f, i, ns[i], 1.0 + 0.85 * i, 0.6))
for i in range(3):
    js.append(f'  tl.fromTo("#{f}-p{i}", {{ opacity: 0, scale: 1.4 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "power3.out" }}, {3.8 + i * 0.5:.2f});')
js.append(f'  tl.fromTo("#{f}-sub", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power2.out" }}, 5.2);')
write(f, 6, body, js)

# ---- Frame 4: while loop (7s) ----
f = "04-loop"
lines = [f'<span class="{f}-k">while not</span> ubaal:',
         '    garam_karo()',
         f'<span class="{f}-k">print</span>(<span class="{f}-s">"Chai ready!"</span>)']
cardh, ns = card(f, lines, "left:70px;top:300px;width:780px;height:340px;font-size:46px")
steps = "".join(f'<div id="{f}-heat{i}" style="position:absolute;left:0;right:0;bottom:{i * 25}%;height:25%;'
                f'background:{["#FFD36B", "#FFB020", "#FF8A1F", "#FF5A1F"][i]};opacity:0"></div>' for i in range(4))
bubbles = "".join(f'<div id="{f}-b{i}" style="position:absolute;left:{896 + i * 22}px;top:276px;width:{16 + i * 4}px;height:{16 + i * 4}px;'
                  f'border-radius:50%;border:3px solid {CREAM};opacity:0"></div>' for i in range(3))
body = f"""    <div class="{f}-h" id="{f}-hin" style="top:84px;font-size:52px">{words(f, "Jab tak ubaal na aaye...", {2: f + "-a"})}</div>
    <div class="{f}-h" id="{f}-head" style="top:156px;font-size:96px">{words(f, "= while loop", {1: f + "-c", 2: f + "-c"})}</div>
{cardh}
    <div id="{f}-hl" style="position:absolute;left:72px;top:364px;width:776px;height:74px;background:rgba(10,240,240,.14);border-left:6px solid {CYAN};opacity:0"></div>
    <div id="{f}-bar" style="position:absolute;left:890px;top:310px;width:96px;height:330px;border-radius:48px;border:4px solid rgba(245,241,232,.5);overflow:hidden;box-sizing:border-box">{steps}</div>
    {bubbles}
    <div id="{f}-out" style="position:absolute;left:70px;top:672px;width:780px;height:96px;border-radius:12px;background:rgba(255,176,32,.12);border:2px solid {AMBER};
         font-family:'JetBrains Mono',monospace;font-size:46px;color:{AMBER};display:flex;align-items:center;padding-left:34px;box-sizing:border-box">&gt; Chai ready!</div>"""
js = [rise(f"#{f}-hin .{f}-w", 0.05, 0.07), rise(f"#{f}-head .{f}-w", 0.45, 0.09),
      f'  tl.fromTo("#{f}-card", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.5);',
      f'  tl.fromTo("#{f}-bar", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, 0.8);']
for i, n in enumerate(ns):
    js.append(f'  tl.set("#{f}-l{i}", {{ width: "{n}ch" }}, 0.5);')
# the loop: highlight jumps line1 -> line2, four passes, each pass heats one step
js.append(f'  tl.set("#{f}-hl", {{ opacity: 1, y: 0 }}, 1.2);')
for k in range(4):
    t = 1.2 + k * 0.85
    js.append(f'  tl.set("#{f}-hl", {{ y: 0 }}, {t:.2f});')
    js.append(f'  tl.set("#{f}-hl", {{ y: 74 }}, {t + 0.42:.2f});')
    js.append(f'  tl.fromTo("#{f}-heat{k}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power2.out" }}, {t + 0.42:.2f});')
js.append(f'  tl.set("#{f}-hl", {{ y: 148 }}, 4.6);')
js.append(f'  tl.fromTo("#{f}-out", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }}, 4.8);')
for i in range(3):
    js.append(f'  tl.fromTo("#{f}-b{i}", {{ opacity: 0, y: 30 }}, {{ opacity: 0.9, y: {-40 - i * 18}, duration: 0.9, ease: "power1.out" }}, {4.7 + i * 0.25:.2f});')
write(f, 7, body, js)

# ---- Frame 5: payoff + CTA (5s, final frame: quiet hold) ----
f = "05-cta"
body = f"""    <div class="{f}-h" id="{f}-l1" style="top:128px;font-size:76px">{words(f, "Agar chai bana sakte ho,", {1: f + "-a"})}</div>
    <div class="{f}-h" id="{f}-l2" style="top:230px;font-size:92px">{words(f, "Python seekh sakte ho.", {0: f + "-c"})}</div>
{cup_svg(f, 300, "left:390px;top:400px")}
    <div class="{f}-pill" id="{f}-cta" style="left:230px;top:770px;width:620px;justify-content:center;background:rgba(10,240,240,.14);border:2px solid {CYAN};color:{CREAM}">
      Follow karo <span style="color:{CYAN}">·</span> Samjho with Raj</div>"""
js = [rise(f"#{f}-l1 .{f}-w", 0.05, 0.08), rise(f"#{f}-l2 .{f}-w", 0.9, 0.1),
      f'  tl.fromTo("#{f}-cup", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.7, ease: "power3.out" }}, 1.8);',
      steam_js(f, 2.2),
      f'  tl.fromTo("#{f}-cta", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }}, 3.2);']
write(f, 5, body, js)
print("wrote", sorted(os.listdir(OUT)))
