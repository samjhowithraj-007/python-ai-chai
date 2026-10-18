#!/usr/bin/env python3
"""Python Chai Part 18 (faceless) on the APPROVED Money Plan Short frame (financial planning/videos/ep01/build-short.py,
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
MK_W = 395
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

IMP = '<span class="cyan">from</span> datetime <span class="cyan">import</span> datetime'
NOTE = '<span style="font-family:DM Sans,sans-serif;font-size:28px;font-weight:700;color:rgba(255,255,255,.55)">(aapka time alag hoga)</span>'

# ---- S1 hook: is the shop open?
a, b = S["s1"], nxt["s1"]
scene("sA", a, b, '<div class="hook">Dukaan <b class="mag">khuli</b> hai?</div>'
      '<div id="a-clk" class="h" style="left:340px;top:420px;width:400px;height:400px;border-radius:50%;border:12px solid #F5F1E8;'
      'display:flex;align-items:center;justify-content:center;box-shadow:0 0 60px rgba(255,185,4,.35)">'
      '<span class="amber" style="font-size:120px;font-weight:700">9:30</span></div>'
      '<div id="a-q" class="h chip2" style="left:240px;top:880px">Python ko <span class="mag">time</span> kaise pata?</div>')
js.append("tl.fromTo('#a-clk',{opacity:0,scale:.6,rotation:-30},{opacity:1,scale:1,rotation:0,duration:.6,ease:'back.out(1.6)'},%.2f);" % (a + .3))
rise("#a-q", a + 2.2)

# ---- S2 datetime = Python's clock
a, b = S["s2"], nxt["s2"]
tools = "".join('<span style="display:inline-block;margin:10px 10px 0 0;padding:10px 20px;border-radius:14px;background:rgba(10,240,240,.14);'
                'border:2px solid rgba(10,240,240,.5);%s;font-size:36px">%s</span>' % (MONO, t) for t in ("now()", "strftime()", ".hour"))
scene("sB", a, b, '<div class="hook">datetime = <b class="cyan">Python ki ghadi</b></div>'
      '<div id="b-box" class="card h" style="left:90px;top:420px;width:900px;padding:36px 46px">'
      '<div style="font-size:30px;letter-spacing:.12em;color:rgba(255,255,255,.66);font-weight:700">PYTHON KI GHADI</div>'
      '<div style="%s;font-size:64px;margin-top:14px" class="amber">datetime</div><div id="b-tools">%s</div></div>'
      '<div id="b-imp" class="h" style="left:90px;top:840px;width:900px;text-align:center;%s;font-size:44px">%s</div>' % (MONO, tools, MONO, IMP))
rise("#b-box", a + .4)
js.append("tl.fromTo('#b-tools span',{opacity:0,scale:.8},{opacity:1,scale:1,duration:.3,stagger:.2,ease:'back.out(1.8)'},%.2f);" % (a + 1.2))
rise("#b-imp", a + 2.6); typeon("#b-imp", a + 2.8, .9, 29)

# ---- S3 the code: now()
a, b = S["s3"], nxt["s3"]
scene("sC", a, b, '<div class="hook">Abhi ka <b class="cyan">time</b></div>' + CODEBOX % ("c-code",
      '<div style="font-size:38px"><div id="c-l0">' + IMP + '</div>'
      '<div id="c-l1">now = datetime.<span id="c-n" class="cyan">now</span>()</div>'
      '<div id="c-l2"><span class="cyan">print</span>(now)</div></div>')
      + '<div id="c-term" class="h" style="left:60px;top:700px;width:960px;padding:24px 40px;border-radius:24px;background:#0b0d10;'
        'box-shadow:0 0 0 3px rgba(255,255,255,.14);' + MONO + ';font-size:42px"><div class="amber">2026-10-18 09:30:12.345678</div>' + NOTE + '</div>')
rise("#c-code", a + .3)
for i, t0 in enumerate((a + .6, a + 1.4, a + 2.0)):
    typeon("#c-l%d" % i, t0, .7 if i == 0 else .5)
glow("#c-n", a + 2.6, "10,240,240"); rise("#c-term", a + 3.2)

# ---- S4 strftime: a neat time
a, b = S["s4"], nxt["s4"]
def row(rid, top, code, res):
    return ('<div id="%s" class="card h" style="left:90px;top:%dpx;width:900px;padding:26px 36px">'
            '<div style="%s;font-size:38px">%s</div><div style="%s;font-size:44px;margin-top:10px">&#8594; <span class="amber">%s</span></div></div>') % (rid, top, MONO, code, MONO, res)
scene("sD", a, b, '<div class="hook">Sundar time: <b class="cyan">strftime</b></div>'
      + row("d-0", 410, 'now.<span class="cyan">strftime</span>(<span class="amber">"%H:%M"</span>)', "09:30")
      + row("d-1", 650, 'now.<span class="cyan">strftime</span>(<span class="amber">"%d-%m-%Y"</span>)', "18-10-2026")
      + '<div id="d-chip" class="h chip2" style="left:200px;top:900px">%H ghanta &#183; %M minute &#183; %d din</div>')
rise("#d-0", a + .5); rise("#d-1", a + 2.6); rise("#d-chip", a + 4.6)

# ---- S5 open or closed?
a, b = S["s5"], nxt["s5"]
scene("sE", a, b, '<div class="hook">Khuli ya <b class="mag">band?</b></div>' + CODEBOX % ("e-code",
      '<div style="font-size:38px"><div id="e-l0"><span class="cyan">if</span> 8 &lt;= now.<span id="e-h" class="cyan">hour</span> &lt; 22:</div>'
      '<div id="e-l1">&#160;&#160;&#160;&#160;<span class="cyan">print</span>(<span class="amber">"Dukaan khuli hai!"</span>)</div>'
      '<div id="e-l2"><span class="cyan">else</span>:</div>'
      '<div id="e-l3">&#160;&#160;&#160;&#160;<span class="cyan">print</span>(<span class="amber">"Kal aana!"</span>)</div></div>')
      + '<div id="e-term" class="h" style="left:60px;top:760px;width:960px;padding:24px 40px;border-radius:24px;background:#0b0d10;'
        'box-shadow:0 0 0 3px rgba(255,255,255,.14);' + MONO + ';font-size:44px"><div class="amber">Dukaan khuli hai!</div>' + NOTE + '</div>')
rise("#e-code", a + .3)
for i, t0 in enumerate((a + .6, a + 1.3, a + 1.9, a + 2.3)):
    typeon("#e-l%d" % i, t0, .5)
glow("#e-h", a + 2.9, "10,240,240"); rise("#e-term", a + 3.4)

# ---- S6 payoff + Part 19 teaser
a, b = S["s6"], nxt["s6"]
scene("sF", a, b, '<div class="hook">datetime =<br><b class="cyan">time ka hisaab</b></div>'
      '<div id="f-t" class="card h" style="left:90px;top:560px;width:900px;padding:34px 44px">'
      '<div style="' + MONO + ';font-size:30px;letter-spacing:.16em;color:rgba(255,255,255,.66);font-weight:700">AGLA PART 19</div>'
      '<div style="font-size:54px;font-weight:700;margin-top:16px">Dukaan ek object: <span class="cyan" style="' + MONO + '">class</span></div></div>')
rise("#f-t", a + .8)

# ---- S7 website glimpse: the REAL lesson page (captured from techsamjhoraj.com/#python-18)
a, b = S["s7"], nxt["s7"]
scene("sG", a, b, '<div class="hook">Free notes + <b class="cyan">code</b></div>'
      '<div id="g-win" class="webwin h" style="left:60px;top:400px;height:760px"><div class="wbar"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i>'
      '<i style="background:#28c840"></i><span class="wurl">techsamjhoraj.com/#python-18</span></div>'
      '<div id="g-pg" style="position:absolute;left:0;top:64px;width:960px;transform-origin:0 0">'
      '<img src="img/site.png" style="width:1660px;height:auto;margin-left:-540px">'
      '<div id="g-mk" class="mk" style="left:24px;top:214px;width:%dpx;height:48px"></div></div></div>' % MK_W)
rise("#g-win", a + .2)
js.append("tl.fromTo('#g-mk',{scaleX:0},{scaleX:1,duration:.5,ease:'power2.out'},%.2f);" % (a + .8))
js.append("tl.fromTo('#g-pg',{scale:1},{scale:1.05,duration:%.2f,ease:'none'},%.2f);" % (b - a - .2, a + .2))
js.append("tl.fromTo('#g-pg',{y:0},{y:-1030,duration:1.6,ease:'power2.inOut'},%.2f);" % (a + 1.8))

# captions (one line each) and POINT cards (left of the prop box)
CAPS = [("Python ko time pata hai?", "s1", {2: "mag"}), ("datetime = Python ki ghadi", "s2", {0: "cyan"}),
        ("now() = abhi ka time", "s3", {0: "cyan"}), ("strftime = sundar format", "s4", {0: "cyan"}),
        ("hour se dukaan ka faisla", "s5", {0: "amber"}), ("Part 19: dukaan ek object", "s6", {0: "amber", 1: "amber"}),
        ("Free notes: techsamjhoraj.com", "s7", {2: "cyan"})]
for i, (txt, k, em) in enumerate(CAPS):
    cap("c%d" % i, txt, em, S[k] + .5, nxt[k])
P = [("<b>datetime</b> = ghadi", S["s2"] + 3.0, nxt["s2"]), ("<b>now()</b> = abhi", S["s3"] + 3.0, nxt["s3"]),
     ("<b>%H:%M</b> = 09:30", S["s4"] + 2.0, nxt["s4"]), ("<b>now.hour</b> = ghanta", S["s5"] + 2.0, S["s5"] + 4.2),
     ("<b>8 &lt;= hour &lt; 22</b>", S["s5"] + 4.2, nxt["s5"])]
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
html.append('<div id="sH" class="clip endc" data-start="%.2f" data-duration="3.24" data-track-index="8"><div class="endt">Python <b class="cyan">Chai</b><br>Part 18 &#10003;</div>'
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
        'background:#F5F1E8;color:#1b1a17;%s;font-size:34px;font-weight:700">datetime</span></div>'
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
<div id="tag"><span>PYTHON CHAI · <b class="cyan">Part 18</b></span></div>
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
