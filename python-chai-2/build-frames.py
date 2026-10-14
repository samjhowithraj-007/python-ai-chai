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


TERM = "#0A0C10"


def run_btn(fid, left, top):
    return (f'    <div class="{fid}-pill" id="{fid}-run" style="left:{left}px;top:{top}px;height:120px;padding:0 56px;gap:22px;'
            f'background:{AMBER};color:{INK};font-size:64px;box-shadow:0 18px 50px rgba(255,176,32,.45)">'
            f'<svg width="46" height="52" viewBox="0 0 46 52"><path d="M4 4 L42 26 L4 48 Z" fill="{INK}"/></svg>RUN</div>'
            f'<div id="{fid}-ring" style="position:absolute;left:{left - 20}px;top:{top - 20}px;width:400px;height:160px;border-radius:9999px;'
            f'border:4px solid {AMBER};opacity:0"></div>')


# ---- Frame 1: hook (4s) ----
f = "01-hook"
body = f"""    <div class="{f}-kick" id="{f}-kick" style="top:110px">PART 2 · SAMJHO WITH RAJ</div>
    <div class="{f}-h" style="top:220px;font-size:100px;font-family:'JetBrains Mono',monospace;font-weight:700">
      <span class="{f}-ln {f}-c" id="{f}-l0" style="display:inline-block;vertical-align:top">chai_banao()</span></div>
    <div class="{f}-h" id="{f}-t2" style="top:370px;font-size:96px">{words(f, "ko RUN karte hain!", {1: f + "-a"})}</div>
{run_btn(f, 360, 620)}
    <svg id="{f}-cur" width="90" height="110" viewBox="0 0 90 110" style="position:absolute;left:0;top:0">
      <path d="M8 6 L8 86 L28 68 L42 100 L58 93 L44 62 L72 62 Z" fill="{CREAM}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/></svg>"""
js = [f'  tl.fromTo("#{f}-kick", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, 0.05);',
      type_line(f, 0, 12, 0.3, 0.8),
      rise(f"#{f}-t2 .{f}-w", 1.2, 0.1),
      f'  tl.fromTo("#{f}-run", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "power3.out" }}, 2.3);',
      f'  tl.fromTo("#{f}-cur", {{ x: 900, y: 1000, opacity: 0 }}, {{ x: 640, y: 690, opacity: 1, duration: 0.7, ease: "power3.out" }}, 2.5);',
      f'  tl.to("#{f}-run", {{ scale: 0.92, duration: 0.1, ease: "power2.in" }}, 3.2);',
      f'  tl.to("#{f}-run", {{ scale: 1.0, duration: 0.25, ease: "power2.out" }}, 3.3);',
      f'  tl.fromTo("#{f}-ring", {{ opacity: 0.9, scale: 1 }}, {{ opacity: 0, scale: 1.25, duration: 0.6, ease: "power2.out" }}, 3.3);']
write(f, 4, body, js)

# ---- Frame 2: recap (6s) ----
f = "02-recap"
lines = [f'<span class="{f}-k">def</span> <span class="{f}-f">chai_banao</span>():',
         f'    <span class="{f}-k">print</span>(<span class="{f}-s">"Paani ubla"</span>)',
         f'    <span class="{f}-k">print</span>(<span class="{f}-s">"Patti daali"</span>)',
         f'    <span class="{f}-k">print</span>(<span class="{f}-s">"Doodh daala"</span>)']
cardh, ns = card(f, lines, "left:90px;top:260px;width:900px;height:430px;font-size:48px")
body = f"""    <div class="{f}-h" id="{f}-head" style="top:100px;font-size:80px">{words(f, "Pehle: Function likho", {1: f + "-c"})}</div>
{cardh}
    <div id="{f}-brk" style="position:absolute;left:150px;top:410px;width:8px;height:240px;background:{CYAN};border-radius:4px;transform-origin:50% 0%;box-shadow:0 0 18px rgba(10,240,240,.7)"></div>
    <div class="{f}-h" id="{f}-lab" style="top:740px;font-size:50px;color:rgba(245,241,232,.85)">andar ke <span class="{f}-c">steps</span></div>"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.08),
      f'  tl.fromTo("#{f}-card", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.35);',
      type_line(f, 0, ns[0], 1.0, 0.7)]
for i in range(1, 4):
    js.append(type_line(f, i, ns[i], 1.0 + 0.95 * i, 0.75))
js += [f'  tl.fromTo("#{f}-brk", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.6, ease: "power2.out" }}, 4.7);',
       f'  tl.fromTo("#{f}-lab", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power2.out" }}, 5.0);']
write(f, 6, body, js)

# ---- Frame 3: run it (7s) ----
f = "03-run"
outs = ["Paani ubla", "Patti daali", "Doodh daala"]
out_html = "".join(f'<div id="{f}-o{i}" style="font-size:44px;line-height:1.6;color:{AMBER}">{o}</div>' for i, o in enumerate(outs))
body = f"""    <div class="{f}-h" id="{f}-head" style="top:100px;font-size:84px">{words(f, "Ab RUN karo", {1: f + "-a"})}</div>
    <div id="{f}-term" style="position:absolute;left:70px;top:260px;width:620px;height:460px;background:{TERM};border:1px solid rgba(245,241,232,.16);
         border-radius:14px;padding:70px 40px 30px;box-sizing:border-box;font-family:'JetBrains Mono',monospace;box-shadow:0 24px 70px rgba(0,0,0,.5)">
      <div class="{f}-dots"><i></i><i></i><i></i></div><div class="{f}-file">terminal</div>
      <span class="{f}-ln" id="{f}-l0" style="font-size:46px"><span style="color:#7CF29A">&gt;&gt;&gt;</span> <span class="{f}-f">chai_banao</span>()</span>
      {out_html}
    </div>
{cup_svg(f, 300, "left:730px;top:340px")}"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.1),
      f'  tl.fromTo("#{f}-term", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.3);',
      f'  tl.fromTo("#{f}-cup", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.5);',
      f'  tl.set("#{f}-fill", {{ scaleY: 0, transformOrigin: "50% 100%" }}, 0);',
      type_line(f, 0, 16, 1.2, 0.9)]
for i in range(3):
    t = 2.4 + i * 1.1
    js.append(f'  tl.fromTo("#{f}-o{i}", {{ opacity: 0, x: -24 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power2.out" }}, {t:.2f});')
    js.append(f'  tl.to("#{f}-fill", {{ scaleY: {(i + 1) / 3:.3f}, duration: 0.6, ease: "power2.out" }}, {t:.2f});')
js.append(steam_js(f, 5.6))
write(f, 7, body, js)

# ---- Frame 4: return value (7s) ----
f = "04-return"
lines = [f'<span class="{f}-k">def</span> <span class="{f}-f">chai_banao</span>():',
         f'    <span class="{f}-k">return</span> <span class="{f}-s">"Chai ready!"</span>',
         f'cup = <span class="{f}-f">chai_banao</span>()',
         f'<span class="{f}-k">print</span>(cup)']
cardh, ns = card(f, lines, "left:90px;top:250px;width:900px;height:430px;font-size:48px")
body = f"""    <div class="{f}-h" id="{f}-head" style="top:100px;font-size:74px">{words(f, "return = function ka jawab", {0: f + "-c", 4: f + "-a"})}</div>
{cardh}
    <svg id="{f}-arrow" width="120" height="200" viewBox="0 0 120 200" style="position:absolute;left:870px;top:390px" fill="none">
      <path id="{f}-shaft" d="M10 10 Q110 60 70 150" stroke="{AMBER}" stroke-width="8" stroke-linecap="round" stroke-dasharray="200" stroke-dashoffset="200"/>
      <path id="{f}-tip" d="M48 136 L70 160 L90 130" stroke="{AMBER}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" opacity="0"/></svg>
    <div id="{f}-out" style="position:absolute;left:90px;top:712px;width:900px;height:100px;border-radius:12px;background:rgba(255,176,32,.12);border:2px solid {AMBER};
         font-family:'JetBrains Mono',monospace;font-size:50px;color:{AMBER};display:flex;align-items:center;padding-left:36px;box-sizing:border-box">&gt; Chai ready!</div>"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.08),
      f'  tl.fromTo("#{f}-card", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 0.3);',
      f'  tl.set("#{f}-l0", {{ width: "{ns[0]}ch" }}, 0.3);',
      f'  tl.set("#{f}-l1", {{ width: "{ns[1]}ch" }}, 0.3);',
      f'  tl.fromTo("#{f}-l1 .{f}-k", {{ textShadow: "0 0 0 rgba(10,240,240,0)" }}, {{ textShadow: "0 0 26px rgba(10,240,240,1)", duration: 0.5, ease: "power2.out" }}, 0.9);',
      type_line(f, 2, ns[2], 1.2, 0.8), type_line(f, 3, ns[3], 2.4, 0.6),
      f'  tl.fromTo("#{f}-shaft", {{ strokeDashoffset: 200 }}, {{ strokeDashoffset: 0, duration: 0.6, ease: "power2.inOut" }}, 3.6);',
      f'  tl.fromTo("#{f}-tip", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, 4.1);',
      f'  tl.fromTo("#{f}-out", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "power3.out" }}, 4.6);']
write(f, 7, body, js)

# ---- Frame 5: payoff + teaser (6s, final: quiet hold) ----
f = "05-cta"
body = f"""    <div class="{f}-h" id="{f}-l1" style="top:110px;font-size:80px">{words(f, "Ek baar likho,", {})}</div>
    <div class="{f}-h" id="{f}-l2" style="top:215px;font-size:92px">{words(f, "kabhi bhi RUN karo", {2: f + "-a"})}</div>
    <div id="{f}-teaser" style="position:absolute;left:150px;top:420px;width:780px;height:220px;border-radius:20px;background:{NAVY};border:2px solid rgba(10,240,240,.5);
         box-sizing:border-box;padding:34px 44px;box-shadow:0 24px 70px rgba(0,0,0,.5)">
      <div style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:30px;letter-spacing:.16em;color:rgba(245,241,232,.66)">AGLA PART 3</div>
      <div style="font-size:64px;margin-top:18px"><span class="{f}-c" style="font-family:'JetBrains Mono',monospace">if-else</span>: cheeni kitni?</div>
    </div>
    <div class="{f}-pill" id="{f}-cta" style="left:230px;top:740px;width:620px;justify-content:center;background:rgba(10,240,240,.14);border:2px solid {CYAN};color:{CREAM}">
      Follow karo <span style="color:{CYAN}">·</span> Samjho with Raj</div>"""
js = [rise(f"#{f}-l1 .{f}-w", 0.05, 0.08), rise(f"#{f}-l2 .{f}-w", 0.7, 0.1),
      f'  tl.fromTo("#{f}-teaser", {{ opacity: 0, y: 70 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out" }}, 1.7);',
      f'  tl.fromTo("#{f}-cta", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "power3.out" }}, 3.4);']
write(f, 6, body, js)
print("wrote", sorted(os.listdir(OUT)))
