#!/usr/bin/env python3
"""Live Python on techsamjhoraj.com: announcement Reel/Short (faceless) on the APPROVED Money Plan Short frame,
copied from python-chai-book-launch/build-short.py (CSS via tech-explainer-01/mpshort.css); content only changed.
The middle is a REAL screen recording of the live site (record.mjs -> public/assets/demo.mp4).
Usage: python build-short.py yt|ig   -> public/index.html
"""
import os, sys, shutil, subprocess
from html import escape
sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(V, "python-chai-book"))
from mascot import chotu
PLAT = sys.argv[1] if len(sys.argv) > 1 else "yt"
PUB = os.path.join(HERE, "public"); os.makedirs(os.path.join(PUB, "fonts"), exist_ok=True); os.makedirs(os.path.join(PUB, "assets"), exist_ok=True)
E = lambda s: escape(s, quote=False)
html, js = [], []
MONO = "font-family:'JetBrains Mono',monospace;font-variant-ligatures:none"

DEMO_LEN = 27.4                      # public/assets/demo.mp4 (recording from the "lesson" mark)
S = dict(s1=0.0, s2=4.5, s3=4.5 + DEMO_LEN, s4=4.5 + DEMO_LEN + 5.5, s5=4.5 + DEMO_LEN + 12.5)
END = S["s5"] + 4.5; DUR = round(END + 3.24, 2)
order = list(S); nxt = {k: (S[order[i + 1]] if i + 1 < len(order) else END) for i, k in enumerate(order)}
D = lambda t: S["s2"] + t - 1.16     # demo mark (seconds in rec/marks.json) -> Short time
MK_W = 470

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

# ---- S1 hook
a, b = S["s1"], nxt["s1"]
scene("sA", a, b, '<div class="hook">Python install nahi hai?</div>'
      '<div id="a-sub" class="h" style="left:60px;right:60px;top:340px;text-align:center;font-size:84px;font-weight:700">Koi baat <span class="amber">nahi!</span></div>'
      '<div id="a-run" class="h" style="left:240px;top:560px;width:600px;padding:40px 0;border-radius:36px;background:#7fd1b9;color:#10231c;text-align:center;font-size:96px;font-weight:700;box-shadow:0 0 90px rgba(127,209,185,.45)">&#9654; Run</div>'
      '<div id="a-chip" class="h chip2" style="left:150px;top:900px">Website pe hi <span class="cyan">Python chalao</span></div>')
rise("#a-sub", a + .9)
js.append("tl.fromTo('#a-run',{opacity:0,scale:.5},{opacity:1,scale:1,duration:.6,ease:'back.out(1.8)'},%.2f);" % (a + 1.5))
js.append("tl.fromTo('#a-run',{scale:1},{scale:.92,duration:.15,yoyo:true,repeat:1,ease:'power1.inOut'},%.2f);" % (a + 2.6))
rise("#a-chip", a + 2.9)

# ---- S2 the REAL live demo (screen recording of techsamjhoraj.com)
a, b = S["s2"], nxt["s2"]
VW, VH = 720, 837
scene("sB", a, b, '<div class="hook" style="top:225px">LIVE <b class="cyan">demo</b> &#128064;</div>'
      '<div id="b-win" class="webwin" style="left:%dpx;top:330px;width:%dpx;height:%dpx"><div class="wbar"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i>'
      '<i style="background:#28c840"></i><span class="wurl">techsamjhoraj.com</span></div></div>' % ((1080 - VW) // 2, VW, VH + 64))
html.append('<video id="demo" class="clip" src="assets/demo.mp4" muted playsinline data-start="%.2f" data-duration="%.2f" data-media-start="0" data-track-index="4" '
            'style="position:absolute;left:%dpx;top:394px;width:%dpx;height:%dpx;z-index:4;border-radius:0 0 22px 22px"></video>' % (a, DEMO_LEN, (1080 - VW) // 2, VW, VH))
js.append("tl.fromTo('#demo',{opacity:0},{opacity:1,duration:.3},%.2f);" % a)
js.append("tl.to('#demo',{opacity:0,duration:.3},%.2f);" % (b - .3))

# ---- S3 selling points
a, b = S["s3"], nxt["s3"]
TICKS = (("Free, no install", "sirf browser chahiye"), ("Phone pe bhi", "Android, iPhone, laptop"), ("Har free lesson pe &#9654; Run", "Python, AI chatbot + Playground"), ("Book ke examples bhi", "local Python nahi? Yahin chalao"), ("Aage: AI, LLM, Agentic", "wo courses bhi yahin chalenge"))
scene("sC", a, b, '<div class="hook">Padho <b class="amber">aur</b> chalao</div>'
      '<div id="c-l" style="left:110px;top:360px;width:860px;display:flex;flex-direction:column;gap:16px">'
      + "".join('<div class="card" style="padding:18px 30px;opacity:0"><div style="font-size:54px;font-weight:700"><span class="cyan">&#10003;</span> %s</div>'
                '<div style="font-size:32px;color:rgba(255,255,255,.7);margin-left:52px">%s</div></div>' % t for t in TICKS) + '</div>')
js.append("tl.fromTo('#c-l .card',{opacity:0,x:-60},{opacity:1,x:0,duration:.45,stagger:.4,ease:'power3.out'},%.2f);" % (a + .4))

# ---- S4 Diwali: email sign-up -> extra 10% code for the book (code itself stays private)
a, b = S["s4"], nxt["s4"]
scene("sD", a, b, '<div class="hook">&#129684; Diwali <b class="amber">special</b></div>'
      '<div id="d-box" class="card h" style="left:90px;top:380px;width:900px;padding:34px 40px">'
      '<div style="font-size:42px;font-weight:700">Website pe <span class="cyan">email do</span></div>'
      '<div style="display:flex;gap:14px;margin-top:22px"><div style="flex:1;padding:20px 24px;border-radius:14px;background:rgba(255,255,255,.08);border:2px solid rgba(255,255,255,.25);font-size:36px;color:rgba(255,255,255,.75)"><span id="d-type">aap@email.com</span></div>'
      '<div id="d-btn" style="padding:20px 30px;border-radius:14px;background:#F5F1E8;color:#1b1a17;font-size:36px;font-weight:700">Notify me</div></div></div>'
      '<div id="d-gift" class="h" style="left:90px;top:720px;width:900px;padding:36px 40px;border-radius:30px;background:#FFD166;color:#2a1260;text-align:center">'
      '<div style="font-size:46px;font-weight:700">&#127873; Extra <span style="font-size:84px">10% off</span></div>'
      '<div style="font-size:36px;font-weight:700;margin-top:6px">Python with Chai book pe</div>'
      '<div style="font-size:30px;margin-top:10px">Private Diwali code, sirf email pe &#128233;</div></div>')
rise("#d-box", a + .3)
js.append("tl.fromTo('#d-type',{clipPath:'inset(0 100%% 0 0)'},{clipPath:'inset(0 0%% 0 0)',duration:.9,ease:'steps(13)'},%.2f);" % (a + .8))
js.append("tl.fromTo('#d-btn',{scale:1},{scale:.9,duration:.12,yoyo:true,repeat:1},%.2f);" % (a + 2.0))
js.append("tl.fromTo('#d-gift',{opacity:0,scale:.6,rotation:-4},{opacity:1,scale:1,rotation:0,duration:.55,ease:'back.out(1.8)'},%.2f);" % (a + 2.5))

# ---- S5 website glimpse: the REAL Playground page
a, b = S["s5"], nxt["s5"]
scene("sE", a, b, '<div class="hook">Abhi try karo &#128071;</div>'
      '<div id="e-win" class="webwin h" style="left:60px;top:380px;height:820px"><div class="wbar"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i>'
      '<i style="background:#28c840"></i><span class="wurl">techsamjhoraj.com/#playground</span></div>'
      '<div id="e-pg" style="position:absolute;left:0;top:64px;width:960px;transform-origin:0 0">'
      '<img src="img/site.png" style="width:1500px;height:auto;margin-left:-110px">'
      '<div id="e-mk" class="mk" style="left:128px;top:236px;width:%dpx;height:52px"></div></div></div>' % MK_W)
rise("#e-win", a + .2)
js.append("tl.fromTo('#e-mk',{scaleX:0},{scaleX:1,duration:.5,ease:'power2.out'},%.2f);" % (a + .9))
js.append("tl.fromTo('#e-pg',{scale:1},{scale:1.05,duration:%.2f,ease:'none'},%.2f);" % (b - a - .2, a + .2))

# captions (one line each), synced to the recording's marks
CAPS = [("Code padho, wahin chalao!", S["s1"] + .5, S["s2"], {3: "cyan"}),
        ("Lesson kholo", D(1.16) + .2, D(3.0), {1: "cyan"}),
        ("Run dabao: Python load", D(3.0), D(6.0), {1: "cyan"}),
        ("Output turant!", D(6.0), D(9.6), {1: "amber"}),
        ("Code badlo: 20 se 25", D(9.6), D(12.7), {4: "amber"}),
        ("Phir Run: Bill 75!", D(12.7), D(15.0), {2: "amber", 3: "amber"}),
        ("Playground: apna code", D(15.0), D(19.0), {0: "cyan"}),
        ("Loop kabhi khatam nahi?", D(19.0), D(23.2), {1: "mag", 2: "mag"}),
        ("Stop! Page hang nahi", D(23.2), S["s3"], {0: "cyan"}),
        ("AI, LLM, Agentic bhi yahin!", S["s3"] + .5, S["s4"], {0: "cyan", 1: "cyan", 2: "cyan"}),
        ("Email do, Diwali code pao", S["s4"] + .5, S["s5"], {3: "amber", 4: "amber"}),
        ("techsamjhoraj.com/#playground", S["s5"] + .5, END, {0: "cyan"})]
for i, (txt, ta, tb, em) in enumerate(CAPS):
    cap("c%d" % i, txt, em, ta, tb)
P = [("<b>Lesson</b> pe &#9654; Run", D(3.0) + .3, D(9.6)), ("<b>Code</b> edit karo", D(9.6) + .3, D(15.0)),
     ("<b>Playground</b>: apna code", D(15.0) + .3, D(19.0)), ("<b>Stop</b>: kabhi hang nahi", D(19.0) + .3, S["s3"]),
     ("<b>Free</b> · no install", S["s3"] + 1.0, S["s4"])]
for n, (txt, ta, tb) in enumerate(P, 1):
    pt("p%d" % n, n, txt, ta, tb)
_cta = ("Notify me &#8595;<small>techsamjhoraj.com</small>" if PLAT == "yt" else "Notify me<small>link in bio · techsamjhoraj.com</small>")
html.append('<div id="p6" class="clip cta" data-start="%.2f" data-duration="%.2f" data-track-index="9"%s>%s</div>'
            % (S["s4"] + .5, END - S["s4"] - .5, "" if PLAT == "yt" else ' style="background:#0095F6"', _cta))
js.append("tl.fromTo('#p6',{opacity:0,scale:.9},{opacity:1,scale:1,duration:.35,ease:'back.out(1.6)'},%.2f);" % (S["s4"] + .6))
js.append("tl.fromTo('#p6',{scale:1},{scale:1.05,duration:.3,yoyo:true,repeat:5,ease:'power1.inOut'},%.2f);" % (S["s4"] + 2.6))

# ---- ending (Money Plan end card)
btn = '<span class="btn red">Subscribe</span>' if PLAT == "yt" else '<span class="btn blue">Follow</span>'
who = ('<span class="ico">&#9654;</span><div><div class="endk">YouTube</div><div class="endh">@SamjhowithRaj</div></div>' if PLAT == "yt" else
       '<span class="ico ig">&#9673;</span><div><div class="endk">Instagram · Facebook · X</div><div class="endh">@samjhowithraj</div></div>')
html.append('<div id="sZ" class="clip endc" data-start="%.2f" data-duration="3.24" data-track-index="8"><div class="endt">Python <b class="cyan">live</b><br>&#9654; website pe</div>'
            '<div id="z-b" class="endb">%s%s</div><div class="endw">Try: <b>techsamjhoraj.com/#playground</b></div>'
            '<div style="font-size:36px;color:rgba(255,255,255,.7)">&#129684; Email do, Diwali code pao</div></div>' % (END, who, btn))
js += ["tl.fromTo('#sZ',{opacity:0},{opacity:1,duration:.35},%.2f);" % END, "rise('#z-b',%.2f);" % (END + .35),
       "tl.fromTo('#z-b .btn',{scale:1},{scale:1.1,duration:.22,yoyo:true,repeat:5,ease:'power1.inOut'},%.2f);" % (END + .85)]

# ---- the prop in Raj's cam slot: Chotu cheering + a Run tag
PROP = ('<div id="chotu" style="position:absolute;left:92px;top:30px;width:300px;height:300px">%s</div>'
        '<div style="position:absolute;left:0;right:0;top:350px;text-align:center"><span id="prop-tag" style="display:inline-block;padding:12px 26px;border-radius:16px;'
        'background:#7fd1b9;color:#10231c;%s;font-size:34px;font-weight:700">&#9654; RUN</span></div>'
        '<div style="position:absolute;left:0;right:0;top:430px;text-align:center;font-size:26px;font-weight:700;letter-spacing:.12em;color:rgba(255,255,255,.7)">LIVE PYTHON</div>'
        ) % (chotu("party", "").replace("<svg ", '<svg width="300" height="300" ', 1), MONO)
js.append("tl.fromTo('#chotu',{y:0,rotation:-3},{y:-14,rotation:3,duration:1.2,ease:'sine.inOut',yoyo:true,repeat:%d},.4);" % int(DUR / 1.2))
js.append("tl.fromTo('#prop-tag',{rotation:0},{rotation:-4,duration:.5,yoyo:true,repeat:1,ease:'power1.inOut'},%.2f);" % (D(3.0)))

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
<div id="tag"><span>NEW · <b class="cyan">Live Python</b> on the site</span></div>
%s
<div id="cam" class="clip" data-start="0" data-duration="%.2f" data-track-index="3">%s</div>
<div id="foot">techsamjhoraj.com · <b>Tech Samjho Raj</b></div>
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
