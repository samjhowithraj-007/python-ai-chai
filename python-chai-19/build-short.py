#!/usr/bin/env python3
"""Python Chai Part 19 (faceless) on the APPROVED Money Plan Short frame (financial planning/videos/ep01/build-short.py,
CSS via tech-explainer-01/mpshort.css): tag pill, hook line, floating panel, one-line captions, POINT cards bottom-left,
and in Raj's cam slot (bottom-right) an animated chai + bill.txt prop instead of a face. No voice: lo-fi bed only.
Usage: python build-short.py yt|ig   -> public/index.html
"""
import os, sys, shutil, subprocess
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(HERE)
PLAT = sys.argv[1] if len(sys.argv) > 1 else "yt"
PUB = os.path.join(HERE, "public"); os.makedirs(os.path.join(PUB, "fonts"), exist_ok=True); os.makedirs(os.path.join(PUB, "assets"), exist_ok=True)
E = lambda s: escape(s, quote=False)
html, js = [], []
MONO = "font-family:'JetBrains Mono',monospace;font-variant-ligatures:none"

# scene windows (seconds); the last scene runs to END, then the Money Plan end card (3.24 s)
S = dict(s1=0.0, s2=5.0, s3=12.0, s4=19.0, s5=28.5, s6=35.0, s7=40.0)
MK_W = 385
END = 44.0; DUR = round(END + 3.24, 2)
order = list(S); nxt = {k: (S[order[i + 1]] if i + 1 < len(order) else END) for i, k in enumerate(order)}

def scene(sid, a, b, inner):
    html.append('<div id="%s" class="clip scene" data-start="%.2f" data-duration="%.2f" data-track-index="%d">%s</div>' % (sid, a, b - a, 1 + len(html) % 2, inner))
    js.append("tl.fromTo('#%s',{opacity:0},{opacity:1,duration:.3},%.2f);" % (sid, a))
    js.append("tl.to('#%s',{opacity:0,duration:.3},%.2f);" % (sid, b - .3))

def cap(cid, text, em, a, b):
    words = "".join('<span class="w%s">%s</span>' % (" " + em[i] if i in em else "", E(w)) for i, w in enumerate(text.split()))
    html.append('<div id="%s" class="clip cap" data-start="%.2f" data-duration="%.2f" data-track-index="6">%s</div>' % (cid, a, b - a, words))
    js.append("tl.fromTo('#%s .w',{opacity:0,y:20},{opacity:1,y:0,duration:.35,ease:'power2.out',stagger:.05},%.2f);" % (cid, a))
    js.append("tl.to('#%s',{opacity:0,duration:.25},%.2f);" % (cid, b - .25))

def pt(pid, n, text, a, b):
    html.append('<div id="%s" class="clip pt" data-start="%.2f" data-duration="%.2f" data-track-index="9"><div class="pn">POINT %d / 5</div><div class="px">%s</div></div>' % (pid, a, b - a, n, text))
    js.append("tl.fromTo('#%s',{opacity:0,x:-30},{opacity:1,x:0,duration:.35,ease:'power2.out'},%.2f);" % (pid, a + .1))
    js.append("tl.to('#%s',{opacity:0,duration:.25},%.2f);" % (pid, b - .25))

def rise(sel, t): js.append("rise('%s',%.2f);" % (sel, t))

CODEBOX = ('<div id="%s" class="h" style="left:60px;top:400px;width:960px;padding:34px 40px;border-radius:24px;background:#181715;'
           'box-shadow:0 0 0 3px rgba(255,255,255,.14),0 30px 90px rgba(0,0,0,.6);' + MONO + ';font-size:42px;line-height:1.6">%s</div>')
PAPER = ('<div id="%s" class="h" style="left:%dpx;top:%dpx;width:%dpx;padding:30px 34px;border-radius:22px;background:#F5F1E8;color:#1b1a17;'
         'box-shadow:0 30px 80px rgba(0,0,0,.55)"><div style="font-size:32px;font-weight:700;margin-bottom:14px">%s</div>'
         '<div style="' + MONO + ';font-size:%dpx;line-height:1.6">%s</div></div>')

def typeon(sel, t, d=.8, n=20):
    js.append("tl.fromTo('%s',{clipPath:'inset(0 100%% 0 0)'},{clipPath:'inset(0 0%% 0 0)',duration:%.2f,ease:'steps(%d)'},%.2f);" % (sel, d, n, t))

def glow(sel, t, rgba="255,185,4"):
    js.append("tl.fromTo('%s',{backgroundColor:'rgba(%s,0)'},{backgroundColor:'rgba(%s,.35)',duration:.3},%.2f);" % (sel, rgba, rgba, t))

IND = '&#160;&#160;&#160;&#160;'
CLS = '<span class="cyan">class</span> <span class="amber">ChaiDukaan</span>:'

def shop(sid, left, name, cups):
    return ('<div id="%s" class="h" style="left:%dpx;top:720px;width:400px;padding:26px 30px;border-radius:22px;background:#F5F1E8;color:#1b1a17;'
            'box-shadow:0 24px 70px rgba(0,0,0,.5)"><div style="font-size:30px;font-weight:700;color:rgba(27,26,23,.55)">OBJECT</div>'
            '<div style="font-size:48px;font-weight:700">%s</div><div style="' + MONO + ';font-size:32px;margin-top:6px">cups = %s</div></div>') % (sid, left, name, cups)

# ---- S1 hook: two shops, double the variables
a, b = S["s1"], nxt["s1"]
vars_ = "".join('<div id="a-l%d">dukaan%d_%s = <span class="amber">%s</span></div>' % (i, i // 2 + 1, k, v)
                for i, (k, v) in enumerate((("naam", '"Raju"'), ("cups", "0"), ("naam", '"Pappu"'), ("cups", "0"))))
scene("sA", a, b, '<div class="hook">Do dukaan, <b class="mag">double code?</b></div>' + CODEBOX % ("a-code",
      vars_ + '<div id="a-dots" style="color:rgba(255,255,255,.5)">&#8230; dukaan3, dukaan4 &#8230;</div>')
      + '<div id="a-x" class="h pillx" style="left:220px;top:860px">10 dukaan = 20 variable &#215;</div>')
rise("#a-code", a + .2)
for i in range(4):
    js.append("tl.fromTo('#a-l%d',{opacity:0,x:-20},{opacity:1,x:0,duration:.25},%.2f);" % (i, a + .5 + i * .35))
js.append("tl.fromTo('#a-dots',{opacity:0},{opacity:1,duration:.3},%.2f);" % (a + 2.0))
rise("#a-x", a + 2.8)

# ---- S2 class = the shop's blueprint, objects = real shops
a, b = S["s2"], nxt["s2"]
scene("sB", a, b, '<div class="hook">class = <b class="cyan">dukaan ka naksha</b></div>'
      '<div id="b-plan" class="h" style="left:140px;top:420px;width:800px;padding:30px 40px;border-radius:22px;border:4px dashed #0AF0F0;'
      'background:rgba(10,240,240,.08);text-align:center"><div style="font-size:28px;font-weight:700;letter-spacing:.12em;color:rgba(255,255,255,.66)">NAKSHA</div>'
      '<div style="' + MONO + ';font-size:50px;margin-top:8px">' + CLS + '</div>'
      '<div style="' + MONO + ';font-size:32px;margin-top:8px;color:rgba(255,255,255,.75)">naam &#183; cups &#183; bechna()</div></div>'
      + shop("b-o1", 100, "Raju", "0") + shop("b-o2", 580, "Pappu", "0"))
rise("#b-plan", a + .4)
js.append("tl.fromTo('#b-o1',{opacity:0,y:-60,scale:.7},{opacity:1,y:0,scale:1,duration:.5,ease:'back.out(1.6)'},%.2f);" % (a + 2.0))
js.append("tl.fromTo('#b-o2',{opacity:0,y:-60,scale:.7},{opacity:1,y:0,scale:1,duration:.5,ease:'back.out(1.6)'},%.2f);" % (a + 2.6))

# ---- S3 __init__ and self
a, b = S["s3"], nxt["s3"]
scene("sC", a, b, '<div class="hook">Nayi dukaan <b class="cyan">setup</b></div>' + CODEBOX % ("c-code",
      '<div style="font-size:38px"><div id="c-l0">' + CLS + '</div>'
      '<div id="c-l1">' + IND + '<span class="cyan">def</span> <span id="c-i" class="cyan">__init__</span>(<span id="c-s" class="mag">self</span>, naam):</div>'
      '<div id="c-l2">' + IND + IND + 'self.naam = naam</div>'
      '<div id="c-l3">' + IND + IND + 'self.cups = <span class="amber">0</span></div></div>')
      + '<div id="c-chip" class="h chip2" style="left:170px;top:760px"><span class="mag">self</span> = "yeh wali dukaan"</div>')
rise("#c-code", a + .3)
for i, t0 in enumerate((a + .6, a + 1.2, a + 1.9, a + 2.4)):
    typeon("#c-l%d" % i, t0, .6)
glow("#c-i", a + 3.1, "10,240,240"); glow("#c-s", a + 3.6, "205,0,238"); rise("#c-chip", a + 3.9)

# ---- S4 a method: selling chai
a, b = S["s4"], nxt["s4"]
scene("sD", a, b, '<div class="hook">Method = <b class="amber">dukaan ka kaam</b></div>' + CODEBOX % ("d-code",
      '<div style="font-size:38px"><div id="d-l0">' + IND + '<span class="cyan">def</span> <span id="d-m" class="amber">bechna</span>(self):</div>'
      '<div id="d-l1">' + IND + IND + 'self.cups += <span class="amber">1</span></div>'
      '<div id="d-l2">' + IND + IND + '<span class="cyan">print</span>(self.naam, self.cups)</div></div>')
      + '<div id="d-chip" class="h chip2" style="left:150px;top:720px">Class ke andar <span class="cyan">def</span> = method</div>')
rise("#d-code", a + .3)
for i, t0 in enumerate((a + .7, a + 1.4, a + 2.0)):
    typeon("#d-l%d" % i, t0, .6)
glow("#d-m", a + 2.9); rise("#d-chip", a + 3.6)

# ---- S5 two objects, separate counts
a, b = S["s5"], nxt["s5"]
scene("sE", a, b, '<div class="hook">Har dukaan ka <b class="cyan">apna hisaab</b></div>' + CODEBOX % ("e-code",
      '<div style="font-size:36px"><div id="e-l0">raju = ChaiDukaan(<span class="amber">"Raju"</span>)</div>'
      '<div id="e-l1">pappu = ChaiDukaan(<span class="amber">"Pappu"</span>)</div>'
      '<div id="e-l2">raju.<span class="amber">bechna</span>(); raju.<span class="amber">bechna</span>()</div>'
      '<div id="e-l3">pappu.<span class="amber">bechna</span>()</div></div>')
      + '<div id="e-term" class="h" style="left:60px;top:720px;width:960px;padding:24px 40px;border-radius:24px;background:#0b0d10;'
        'box-shadow:0 0 0 3px rgba(255,255,255,.14);' + MONO + ';font-size:42px;line-height:1.5">'
        '<div class="amber">Raju 1</div><div class="amber">Raju 2</div><div style="color:#0AF0F0">Pappu 1</div></div>')
rise("#e-code", a + .3)
for i, t0 in enumerate((a + .6, a + 1.1, a + 1.6, a + 2.2)):
    typeon("#e-l%d" % i, t0, .5)
rise("#e-term", a + 2.8)
js.append("tl.fromTo('#e-term div',{opacity:0},{opacity:1,duration:.2,stagger:.5},%.2f);" % (a + 3.0))

# ---- S6 payoff + Part 20 teaser (finale)
a, b = S["s6"], nxt["s6"]
scene("sF", a, b, '<div class="hook">class = naksha,<br><b class="cyan">object = dukaan</b></div>'
      '<div id="f-t" class="card h" style="left:90px;top:560px;width:900px;padding:34px 44px">'
      '<div style="' + MONO + ';font-size:30px;letter-spacing:.16em;color:rgba(255,255,255,.66);font-weight:700">AGLA PART 20 &#183; FINALE</div>'
      '<div style="font-size:54px;font-weight:700;margin-top:16px">Python aa gayi! Ab <span class="cyan">AI ki baari</span></div></div>')
rise("#f-t", a + .8)

# ---- S7 website glimpse: the REAL lesson page (captured from techsamjhoraj.com/#python-19)
a, b = S["s7"], nxt["s7"]
scene("sG", a, b, '<div class="hook">Free notes + <b class="cyan">code</b></div>'
      '<div id="g-win" class="webwin h" style="left:60px;top:400px;height:760px"><div class="wbar"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i>'
      '<i style="background:#28c840"></i><span class="wurl">techsamjhoraj.com/#python-19</span></div>'
      '<div id="g-pg" style="position:absolute;left:0;top:64px;width:960px;transform-origin:0 0">'
      '<img src="img/site.png" style="width:1660px;height:auto;margin-left:-540px">'
      '<div id="g-mk" class="mk" style="left:24px;top:214px;width:%dpx;height:48px"></div></div></div>' % MK_W)
rise("#g-win", a + .2)
js.append("tl.fromTo('#g-mk',{scaleX:0},{scaleX:1,duration:.5,ease:'power2.out'},%.2f);" % (a + .8))
js.append("tl.fromTo('#g-pg',{scale:1},{scale:1.05,duration:%.2f,ease:'none'},%.2f);" % (b - a - .2, a + .2))
js.append("tl.fromTo('#g-pg',{y:0},{y:-1030,duration:1.6,ease:'power2.inOut'},%.2f);" % (a + 1.8))

# captions (one line each) and POINT cards (left of the prop box)
CAPS = [("Har dukaan ke 2 variable?", "s1", {4: "mag"}), ("class = dukaan ka naksha", "s2", {0: "cyan"}),
        ("__init__ = nayi dukaan setup", "s3", {0: "cyan"}), ("Method = dukaan ka kaam", "s4", {0: "amber"}),
        ("Har object ka apna hisaab", "s5", {1: "cyan"}), ("Part 20: ab AI ki baari!", "s6", {0: "amber", 1: "amber"}),
        ("Free notes: techsamjhoraj.com", "s7", {2: "cyan"})]
for i, (txt, k, em) in enumerate(CAPS):
    cap("c%d" % i, txt, em, S[k] + .5, nxt[k])
P = [("<b>class</b> = naksha", S["s2"] + 3.0, nxt["s2"]), ("<b>self</b> = yeh dukaan", S["s3"] + 3.0, nxt["s3"]),
     ("<b>def</b> = method", S["s4"] + 3.0, nxt["s4"]), ("<b>object</b> = asli dukaan", S["s5"] + 2.0, S["s5"] + 4.2),
     ("Apne apne <b>cups</b>", S["s5"] + 4.2, nxt["s5"])]
for n, (txt, ta, tb) in enumerate(P, 1):
    pt("p%d" % n, n, txt, ta, tb)
_cta = ("Python Chai playlist &#8593;<small>Part 1 se shuru karo</small>" if PLAT == "yt" else "Python Chai series<small>Samjho with Raj · Part 1 se shuru karo</small>")
html.append('<div id="p6" class="clip cta" data-start="%.2f" data-duration="%.2f" data-track-index="9"%s>%s</div>'
            % (S["s6"] + 1.0, nxt["s6"] - S["s6"] - 1.0, "" if PLAT == "yt" else ' style="background:#0095F6"', _cta))
js.append("tl.fromTo('#p6',{opacity:0,scale:.9},{opacity:1,scale:1,duration:.35,ease:'back.out(1.6)'},%.2f);" % (S["s6"] + 1.1))
js.append("tl.fromTo('#p6',{scale:1},{scale:1.05,duration:.3,yoyo:true,repeat:3,ease:'power1.inOut'},%.2f);" % (S["s6"] + 2.2))

# ---- ending (Money Plan end card)
btn = '<span class="btn red">Subscribe</span>' if PLAT == "yt" else '<span class="btn blue">Follow</span>'
who = ('<span class="ico">&#9654;</span><div><div class="endk">YouTube</div><div class="endh">@SamjhowithRaj</div></div>' if PLAT == "yt" else
       '<span class="ico ig">&#9673;</span><div><div class="endk">Instagram · Facebook · X</div><div class="endh">@samjhowithraj</div></div>')
html.append('<div id="sH" class="clip endc" data-start="%.2f" data-duration="3.24" data-track-index="8"><div class="endt">Python <b class="cyan">Chai</b><br>Part 19 &#10003;</div>'
            '<div id="h-b" class="endb">%s%s</div><div class="endw">Free notes: <b>techsamjhoraj.com</b></div></div>' % (END, who, btn))
js += ["tl.fromTo('#sH',{opacity:0},{opacity:1,duration:.35},%.2f);" % END, "rise('#h-b',%.2f);" % (END + .35),
       "tl.fromTo('#h-b .btn',{scale:1},{scale:1.1,duration:.22,yoyo:true,repeat:5,ease:'power1.inOut'},%.2f);" % (END + .85)]

# ---- the prop in Raj's cam slot: a steaming chai glass + a bill.txt tag (faceless series)
PROP = ('<svg viewBox="0 0 300 300" width="300" height="300" style="position:absolute;left:92px;top:40px" fill="none">'
        '<path d="M78 150 L222 150 L210 252 Q208 262 198 262 L102 262 Q92 262 90 252 Z" fill="#FFB904"/>'
        '<path d="M70 128 L230 128 L212 254 Q209 270 194 270 L106 270 Q91 270 88 254 Z" stroke="#F5F1E8" stroke-width="8" stroke-linejoin="round"/>'
        '<path d="M228 160 Q268 160 266 196 Q264 228 220 230" stroke="#F5F1E8" stroke-width="8" stroke-linecap="round"/>'
        '<path class="stm" d="M115 108 Q100 88 115 68 Q130 48 115 28" stroke="#F5F1E8" stroke-width="7" stroke-linecap="round" opacity=".75"/>'
        '<path class="stm" d="M150 108 Q135 88 150 68 Q165 48 150 28" stroke="#F5F1E8" stroke-width="7" stroke-linecap="round" opacity=".75"/>'
        '<path class="stm" d="M185 108 Q170 88 185 68 Q200 48 185 28" stroke="#F5F1E8" stroke-width="7" stroke-linecap="round" opacity=".75"/></svg>'
        '<div style="position:absolute;left:0;right:0;top:350px;text-align:center"><span id="prop-tag" style="display:inline-block;padding:12px 26px;border-radius:16px;'
        'background:#F5F1E8;color:#1b1a17;%s;font-size:34px;font-weight:700">class</span></div>'
        '<div style="position:absolute;left:0;right:0;top:430px;text-align:center;font-size:26px;font-weight:700;letter-spacing:.12em;color:rgba(255,255,255,.7)">PYTHON CHAI</div>') % MONO
js.append("tl.fromTo('#cam .stm',{y:0,opacity:.2},{y:-18,opacity:.8,duration:1.4,ease:'sine.inOut',stagger:.25,yoyo:true,repeat:29},.4);")
js.append("tl.fromTo('#prop-tag',{rotation:0},{rotation:-4,duration:.5,yoyo:true,repeat:1,ease:'power1.inOut'},%.2f);" % (S["s5"] + 3.8))

# ---- assets: fonts, music bed, project files
for fn in ("DMSans-400.woff2", "DMSans-500.woff2", "DMSans-700.woff2", "JetBrainsMono-400.woff2", "JetBrainsMono-700.woff2"):
    shutil.copy(os.path.join(V, "python-chai-10", "assets", "fonts", fn), os.path.join(PUB, "fonts", fn))
BED = os.path.join(PUB, "assets", "bed.mp3")
if not os.path.exists(BED):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "60", "-i", os.path.join(V, "_shared", "music", "all-of-the-things.mp3"), "-t", str(DUR),
                    "-af", "afade=t=in:d=0.8,afade=t=out:st=%.2f:d=2.5,volume=-6dB" % (DUR - 2.5), "-c:a", "libmp3lame", "-b:a", "192k", BED], check=True)
for k2 in ("hyperframes.json", "package.json"):
    shutil.copy(os.path.join(V, "tech-explainer-01", "anim", "safar", k2), os.path.join(PUB, k2))

CSS = open(os.path.join(V, "tech-explainer-01", "mpshort.css"), encoding="utf8").read()
CSS += ('\n@font-face{font-family:"JetBrains Mono";src:url(fonts/JetBrainsMono-400.woff2) format("woff2");font-weight:400}'
        '\n@font-face{font-family:"JetBrains Mono";src:url(fonts/JetBrainsMono-700.woff2) format("woff2");font-weight:700}'
        '\n#cam{background:#0e1116}')
page = '''<!doctype html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js" integrity="sha384-sG0Hv1tP1lZCk9KQmrIbY/XNwi+OY84GQqhMscbnsoBFqAz8KNCil1kvfL3Hbbk2" crossorigin="anonymous"></script>
<style>%s</style></head><body>
<div id="stage" data-composition-id="short" data-start="0" data-duration="%.2f" data-fps="30" data-width="1080" data-height="1920">
<div id="tag"><span>PYTHON CHAI · <b class="cyan">Part 19</b></span></div>
%s
<div id="cam" class="clip" data-start="0" data-duration="%.2f" data-track-index="3">%s</div>
<div id="foot">Faceless series · <b>Hinglish + code</b></div>
<audio id="bed" src="assets/bed.mp3" data-start="0" data-duration="%.2f" data-track-index="10" data-volume="0.9"></audio>
</div>
<script>
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({ paused: true });
function rise(s,t){ tl.fromTo(s,{opacity:0,y:26},{opacity:1,y:0,duration:.4,ease:'power2.out'},t); }
tl.fromTo('#cam',{opacity:0,y:40},{opacity:1,y:0,duration:.4,ease:'power2.out'},.1);
tl.to('#cam',{opacity:0,duration:.3},%.2f);
tl.to('#foot',{opacity:0,duration:.3},%.2f);
%s
tl.to({}, { duration: %.2f }, 0);
window.__timelines["short"] = tl;
</script></body></html>''' % (CSS, DUR, "\n".join(html), END, PROP, DUR, END - .2, END - .2, "\n".join(js), DUR)
open(os.path.join(PUB, "index.html"), "w", encoding="utf-8").write(page)
print("built", PLAT, "dur %.2f" % DUR)
