#!/usr/bin/env python3
"""Python Chai Part 11 (faceless) on the APPROVED Money Plan Short frame (financial planning/videos/ep01/build-short.py,
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
S = dict(s1=0.0, s2=5.0, s3=12.0, s4=19.0, s5=28.5, s6=35.0)
END = 41.0; DUR = round(END + 3.24, 2)
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

BILL = ('<div class="paper" id="%s" style="left:60px;top:400px"><div class="phead">CHAI BILL</div>'
        '<div class="prow" style="grid-template-columns:2fr 1fr"><span>Masala x2</span><span>Rs 40</span></div>'
        '<div class="prow" style="grid-template-columns:2fr 1fr"><span>Adrak x1</span><span>Rs 15</span></div>'
        '<div class="prow" style="grid-template-columns:2fr 1fr"><span>Discount</span><span style="color:#b0263a">-Rs 5</span></div>'
        '<div class="prow" style="grid-template-columns:2fr 1fr;border:0;font-size:56px"><span>TOTAL</span><span class="amber">Rs 50</span></div>%s</div>')

# ---- S1 hook: the bill vanishes
a, b = S["s1"], nxt["s1"]
scene("sA", a, b, '<div class="hook">Bill <b class="mag">gayab?</b></div>' + BILL % ("a-bill", '<div class="pmask" id="a-mask" style="transform:scaleX(0)"></div>')
      + '<div id="a-q" class="h big" style="left:0;right:0;top:640px;text-align:center;font-size:220px;color:#CD00EE">?</div>')
rise("#a-bill", a + .3)
js.append("tl.fromTo('#a-mask',{scaleX:0},{scaleX:1,duration:.7,ease:'power2.inOut'},%.2f);" % (a + 2.4))
js.append("tl.fromTo('#a-q',{opacity:0,scale:.6},{opacity:1,scale:1,duration:.4,ease:'back.out(2)'},%.2f);" % (a + 3.2))

# ---- S2 variable = kacchi yaad
a, b = S["s2"], nxt["s2"]
scene("sB", a, b, '<div class="hook">Variable = <b class="amber">kacchi</b> yaad</div>'
      '<div id="b-card" class="card h" style="left:90px;top:420px;width:900px;padding:40px 50px">'
      '<div style="font-size:30px;color:rgba(255,255,255,.7);letter-spacing:.08em">RAM (computer ki kacchi yaad)</div>'
      '<div id="b-v" style="%s;font-size:72px;margin-top:18px">total = <span class="amber">50</span></div></div>'
      '<div id="b-x" class="h pillx" style="left:270px;top:760px">Program band &#215;</div>'
      '<div id="b-gone" class="h" style="left:90px;top:900px;width:900px;text-align:center;%s;font-size:64px;color:rgba(255,255,255,.7)">total = <span style="color:#E0242E">???</span></div>' % (MONO, MONO))
rise("#b-card", a + .4); rise("#b-x", a + 2.4)
js.append("tl.to('#b-v',{opacity:.15,filter:'blur(6px)',duration:.6},%.2f);" % (a + 3.0))
rise("#b-gone", a + 3.6)

# ---- S3 file = pakki yaad (the register book)
a, b = S["s3"], nxt["s3"]
lines = "".join('<div style="height:62px;border-bottom:3px solid rgba(27,26,23,.18)"></div>' for _ in range(4))
scene("sC", a, b, '<div class="hook">File = <b class="cyan">pakki</b> yaad</div>'
      '<div id="c-book" class="paper h" style="left:160px;top:400px;width:760px;transform:rotate(-2deg)">'
      '<div style="display:flex;justify-content:space-between;align-items:center"><span class="phead">bill.txt</span>'
      '<span style="font-size:30px;color:rgba(27,26,23,.6)">dukaan ka register</span></div>%s'
      '<div id="c-w" style="position:absolute;left:46px;top:150px;%s;font-size:46px;color:#1b1a17">Total: Rs 50</div></div>'
      '<div id="c-chip" class="h chip2" style="left:170px;top:930px">Band karo, phir bhi <span class="cyan">rehti hai</span></div>' % (lines, MONO))
rise("#c-book", a + .4)
js.append("tl.fromTo('#c-w',{clipPath:'inset(0 100%% 0 0)'},{clipPath:'inset(0 0%% 0 0)',duration:.9,ease:'steps(12)'},%.2f);" % (a + 1.6))
rise("#c-chip", a + 3.2)

# ---- S4 the code
a, b = S["s4"], nxt["s4"]
code = ('<div id="d-code" class="h" style="left:60px;top:400px;width:960px;padding:34px 40px;border-radius:24px;background:#181715;'
        'box-shadow:0 0 0 3px rgba(255,255,255,.14),0 30px 90px rgba(0,0,0,.6);%s;font-size:44px;line-height:1.6">'
        '<div id="d-l0"><span class="cyan">with</span> <span class="cyan">open</span>(<span class="amber">"bill.txt"</span>, <span id="d-w" class="amber">"w"</span>) <span class="cyan">as</span> f:</div>'
        '<div id="d-l1">&#160;&#160;&#160;&#160;f.<span class="cyan">write</span>(<span class="amber">"Total: Rs 50"</span>)</div></div>') % MONO
scene("sD", a, b, '<div class="hook">2 line ka <b class="cyan">code</b></div>' + code
      + '<div id="d-file" class="h" style="left:300px;top:720px;width:480px;padding:30px;border-radius:24px;background:#F5F1E8;color:#1b1a17;text-align:center;box-shadow:0 30px 80px rgba(0,0,0,.55)">'
        '<div style="font-size:34px;font-weight:700">&#128196; bill.txt</div><div style="%s;font-size:42px;margin-top:12px">Total: Rs 50</div></div>' % MONO)
rise("#d-code", a + .3)
for i, t0 in enumerate((a + .7, a + 1.5)):
    js.append("tl.fromTo('#d-l%d',{clipPath:'inset(0 100%% 0 0)'},{clipPath:'inset(0 0%% 0 0)',duration:.8,ease:'steps(20)'},%.2f);" % (i, t0))
js.append("tl.fromTo('#d-w',{backgroundColor:'rgba(255,185,4,0)'},{backgroundColor:'rgba(255,185,4,.35)',duration:.3},%.2f);" % (a + 3.0))
js.append("tl.fromTo('#d-file',{opacity:0,y:40,scale:.9},{opacity:1,y:0,scale:1,duration:.5,ease:'back.out(1.6)'},%.2f);" % (a + 5.2))

# ---- S5 proof: the folder still has it
a, b = S["s5"], nxt["s5"]
scene("sE", a, b, '<div class="hook">Kal bhi <b class="cyan">milega!</b></div>'
      '<div id="e-win" class="webwin h" style="left:60px;top:400px;height:520px"><div class="wbar"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i>'
      '<i style="background:#28c840"></i><span class="wurl">C:\\chai-dukaan\\</span></div>'
      '<div style="position:absolute;left:50px;top:110px;right:50px;font-size:40px;line-height:2.1">'
      '<div style="color:rgba(255,255,255,.55)">&#128193; recipes</div><div id="e-row" style="border-radius:12px;padding:0 16px;margin-left:-16px">&#128196; <b>bill.txt</b> '
      '<span style="font-size:28px;color:rgba(255,255,255,.55)">· kal raat 10:05</span></div><div style="color:rgba(255,255,255,.55)">&#128196; menu.txt</div></div></div>'
      '<div id="e-open" class="paper h" style="left:200px;top:820px;width:680px;padding:28px 36px"><div style="%s;font-size:46px;text-align:center">Total: <span class="amber">Rs 50</span></div></div>' % MONO)
rise("#e-win", a + .3)
js.append("tl.fromTo('#e-row',{backgroundColor:'rgba(10,240,240,0)'},{backgroundColor:'rgba(10,240,240,.22)',duration:.3},%.2f);" % (a + 1.6))
js.append("tl.fromTo('#e-open',{opacity:0,scale:.85},{opacity:1,scale:1,duration:.45,ease:'back.out(1.6)'},%.2f);" % (a + 2.6))

# ---- S6 payoff + Part 12 teaser + website
a, b = S["s6"], nxt["s6"]
scene("sF", a, b, '<div class="hook">Variable bhoole,<br><b class="cyan">file yaad rakhe</b></div>'
      '<div id="f-t" class="card h" style="left:90px;top:520px;width:900px;padding:34px 44px">'
      '<div style="%s;font-size:30px;letter-spacing:.16em;color:rgba(255,255,255,.66);font-weight:700">AGLA PART 12</div>'
      '<div style="font-size:54px;font-weight:700;margin-top:16px">File padho: <span class="cyan">bill wapas lo</span></div></div>'
      '<div id="f-w" class="h" style="left:0;right:0;top:820px;text-align:center;font-size:42px;font-weight:700">Free notes + code: <span class="cyan">techsamjhoraj.com</span></div>' % MONO)
rise("#f-t", a + .8); rise("#f-w", a + 2.0)

# captions (one line each) and POINT cards (left of the prop box)
CAPS = [("Dukaan band… bill gayab!", "s1", {2: "mag"}), ("Program band, variable khatam", "s2", {3: "mag"}),
        ("File = dukaan ka register", "s3", {0: "cyan"}), ("open, with, write: bas!", "s4", {0: "cyan", 1: "cyan", 2: "cyan"}),
        ("Program band, bill safe!", "s5", {3: "cyan"}), ("Part 12: bill wapas padho", "s6", {0: "amber", 1: "amber"})]
for i, (txt, k, em) in enumerate(CAPS):
    cap("c%d" % i, txt, em, S[k] + .5, nxt[k])
P = [("Variable = <b>kacchi</b> yaad", S["s2"] + 1.0, nxt["s2"]), ("File = <b>pakki</b> yaad", S["s3"] + 1.0, nxt["s3"]),
     ('<b>"w"</b> = likhne ke liye', S["s4"] + 2.8, S["s4"] + 5.6), ("<b>with</b> = file khud band", S["s4"] + 5.6, nxt["s4"]),
     ("Band karo, <b>bill safe</b>", S["s5"] + 1.0, nxt["s5"])]
for n, (txt, ta, tb) in enumerate(P, 1):
    pt("p%d" % n, n, txt, ta, tb)
_cta = ("Python Chai playlist &#8593;<small>Part 1 se shuru karo</small>" if PLAT == "yt" else "Python Chai series<small>Samjho with Raj · Part 1 se shuru karo</small>")
html.append('<div id="p6" class="clip cta" data-start="%.2f" data-duration="%.2f" data-track-index="9"%s>%s</div>'
            % (S["s6"] + 1.0, END - S["s6"] - 1.0, "" if PLAT == "yt" else ' style="background:#0095F6"', _cta))
js.append("tl.fromTo('#p6',{opacity:0,scale:.9},{opacity:1,scale:1,duration:.35,ease:'back.out(1.6)'},%.2f);" % (S["s6"] + 1.1))
js.append("tl.fromTo('#p6',{scale:1},{scale:1.05,duration:.3,yoyo:true,repeat:3,ease:'power1.inOut'},%.2f);" % (S["s6"] + 2.2))

# ---- ending (Money Plan end card)
btn = '<span class="btn red">Subscribe</span>' if PLAT == "yt" else '<span class="btn blue">Follow</span>'
who = ('<span class="ico">&#9654;</span><div><div class="endk">YouTube</div><div class="endh">@SamjhowithRaj</div></div>' if PLAT == "yt" else
       '<span class="ico ig">&#9673;</span><div><div class="endk">Instagram · Facebook · X</div><div class="endh">@samjhowithraj</div></div>')
html.append('<div id="sH" class="clip endc" data-start="%.2f" data-duration="3.24" data-track-index="8"><div class="endt">Python <b class="cyan">Chai</b><br>Part 11 &#10003;</div>'
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
        'background:#F5F1E8;color:#1b1a17;%s;font-size:34px;font-weight:700">bill.txt</span></div>'
        '<div style="position:absolute;left:0;right:0;top:430px;text-align:center;font-size:26px;font-weight:700;letter-spacing:.12em;color:rgba(255,255,255,.7)">PYTHON CHAI</div>') % MONO
js.append("tl.fromTo('#cam .stm',{y:0,opacity:.2},{y:-18,opacity:.8,duration:1.4,ease:'sine.inOut',stagger:.25,yoyo:true,repeat:13},.4);")
js.append("tl.fromTo('#prop-tag',{rotation:0},{rotation:-4,duration:.5,yoyo:true,repeat:1,ease:'power1.inOut'},%.2f);" % (S["s4"] + 5.2))

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
<div id="tag"><span>PYTHON CHAI · <b class="cyan">Part 11</b></span></div>
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
