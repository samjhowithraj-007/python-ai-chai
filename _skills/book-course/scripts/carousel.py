"""5-slide Instagram/Facebook/LinkedIn carousel for the book (1080x1350 each).
Run: python carousel.py  -> out/carousel-1..5.jpg   (needs out/p12-2.png, p12-5.png, p11-9.png; see README in CAPTIONS.md)"""
import subprocess, pathlib, sys
sys.dont_write_bytecode = True
from ads import chotu, CHROME, F, OUT as BOOKOUT, ADS

W, H = 1080, 1350
U = lambda p: (ADS / p).as_uri()
COVER = (BOOKOUT / "cover-en.png").as_uri()

CSS = f"""@font-face{{font-family:D;src:url({F}/Baloo2-800.woff2)}}
@font-face{{font-family:H;src:url({F}/Caveat-700.woff2)}}
@font-face{{font-family:Body;src:url({F}/DMSans-400.woff2)}}
@font-face{{font-family:Hand;src:url({F}/PatrickHand.woff2)}}
html,body{{margin:0;width:{W}px;height:{H}px;overflow:hidden}}
body{{background:linear-gradient(160deg,#2a1260 0%,#5b1a8f 42%,#c2185b 72%,#ff7a2f 100%);font-family:Body,sans-serif;color:#fff;position:relative}}
.sun{{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(255,214,120,.55),rgba(255,214,120,0) 70%)}}
.n{{position:absolute;right:56px;top:50px;font-family:D;font-size:30px;background:rgba(255,255,255,.16);padding:4px 18px;border-radius:30px}}
.k{{font-family:H;color:#ffd166}}
h1{{font-family:D;line-height:.98;margin:0}}
h1 em{{font-style:normal;color:#ffd166}}
.img{{position:absolute;box-shadow:0 30px 60px rgba(0,0,0,.45);border-radius:10px}}
.m{{position:absolute}}
.bub{{position:absolute;background:#fff;color:#2a1260;font-family:Hand;border-radius:26px;padding:14px 26px;box-shadow:0 10px 24px rgba(0,0,0,.25)}}
.bub:after{{content:"";position:absolute;bottom:-16px;width:0;height:0;border:16px solid transparent;border-top-color:#fff;border-bottom:0}}
.bub.l:after{{left:46px}} .bub.r:after{{right:46px}}
.burst{{position:absolute;width:210px;height:210px;display:flex;align-items:center;justify-content:center;text-align:center;font-family:D;font-size:40px;line-height:1;color:#2a1260;background:#ffd166;
  clip-path:polygon(50% 0,61% 12%,77% 6%,80% 22%,96% 25%,90% 40%,100% 50%,90% 60%,96% 75%,80% 78%,77% 94%,61% 88%,50% 100%,39% 88%,23% 94%,20% 78%,4% 75%,10% 60%,0 50%,10% 40%,4% 25%,20% 22%,23% 6%,39% 12%)}}
.tag{{position:absolute;background:#ffd166;color:#2a1260;font-family:D;border-radius:14px;padding:10px 22px}}
.swipe{{position:absolute;right:56px;bottom:46px;font-family:D;font-size:34px;opacity:.95}}
.foot{{position:absolute;left:60px;bottom:50px;font-size:26px;opacity:.85}}
.p{{display:inline-block;background:#ffd166;color:#2a1260;border-radius:18px;padding:14px 30px;font-family:D;font-size:64px}}
.p s{{font-size:40px;opacity:.6;margin-right:14px}}
ul{{list-style:none;padding:0;margin:0}} li{{margin:.25em 0}} li:before{{content:"\\2615  "}}"""

C = lambda pose, cls="": chotu(pose, cls)


def slide(i, body):
    return f'<!doctype html><meta charset="utf-8"><style>{CSS}</style><body><div class="n">{i}/5</div>{body}</body>'


SLIDES = [
    # 1. hook
    f"""<div class="sun" style="right:-160px;top:430px;width:900px;height:900px"></div>
<div style="position:absolute;left:60px;top:70px;right:60px">
 <div class="k" style="font-size:52px">Python boring lagta hai? 😴</div>
 <h1 style="font-size:132px;margin-top:10px">Ab seekho<br><em>chai ke saath</em></h1></div>
<img class="img" src="{COVER}" style="right:90px;top:470px;width:470px;transform:rotate(5deg)">
<div class="burst" style="right:30px;top:400px;transform:rotate(12deg)">NEW<br>BOOK</div>
<div class="m" style="left:40px;top:830px;width:330px;height:330px;transform:rotate(-6deg)">{C("party")}</div>
<div class="bub l" style="left:70px;top:705px;font-size:40px">Ek cup, ek chapter!</div>
<div class="tag" style="left:60px;bottom:120px;font-size:40px"><s style="opacity:.6">₹299</s> ₹199 launch</div>
<div class="swipe">Swipe →</div>""",
    # 2. story
    f"""<div class="sun" style="left:-200px;top:520px;width:800px;height:800px"></div>
<div style="position:absolute;left:60px;top:80px;right:60px">
 <div class="k" style="font-size:50px">Har chapter shuru hota hai…</div>
 <h1 style="font-size:96px;margin-top:6px">ek <em>chai-shop</em><br>kahani se</h1></div>
<img class="img" src="{U('p12-2.png')}" style="left:110px;top:430px;width:560px;transform:rotate(-4deg)">
<div class="m" style="right:40px;top:860px;width:300px;height:300px;transform:rotate(6deg)">{C("read")}</div>
<div class="bub r" style="right:70px;top:740px;font-size:38px">Raju ki dukaan yaad hai?</div>
<div class="foot">Concept pehle kahani mein, code baad mein</div>""",
    # 3. real code
    f"""<div class="sun" style="right:-200px;top:300px;width:800px;height:800px"></div>
<div style="position:absolute;left:60px;top:80px;right:60px">
 <h1 style="font-size:108px">Real code.<br><em>Real output.</em></h1></div>
<img class="img" src="{U('p12-5.png')}" style="left:90px;top:390px;width:580px;transform:rotate(-3deg)">
<div class="tag" style="right:50px;top:610px;font-size:38px;transform:rotate(4deg)">Har output sach<br>mein run kiya ✓</div>
<div class="m" style="right:60px;top:880px;width:290px;height:290px">{C("cool")}</div>
<div class="foot">120+ examples · copy, run, samjho</div>""",
    # 4. mistakes
    f"""<div class="sun" style="left:-160px;top:420px;width:800px;height:800px"></div>
<div style="position:absolute;left:60px;top:80px;right:60px">
 <div class="k" style="font-size:50px">Error se darr lagta hai?</div>
 <h1 style="font-size:100px;margin-top:6px">Galtiyan bhi<br><em>sikhati hain</em></h1></div>
<img class="img" src="{U('p11-9.png')}" style="left:90px;top:440px;width:560px;transform:rotate(3deg)">
<div class="m" style="right:50px;top:860px;width:300px;height:300px;transform:rotate(-4deg)">{C("oops")}</div>
<div class="bub r" style="right:60px;top:740px;font-size:38px">Oops! Real error ✓</div>
<div class="foot">Har chapter: 3 mistakes · practice · answers</div>""",
    # 5. CTA
    f"""<div class="sun" style="right:-120px;top:380px;width:820px;height:820px"></div>
<div style="position:absolute;left:60px;top:80px;width:560px">
 <div class="k" style="font-size:52px">New book by Raj</div>
 <h1 style="font-size:104px;margin-top:6px">Python<br>with Chai</h1>
 <ul style="font-size:34px;margin-top:30px">
  <li>30 chapters · 300+ pages</li><li>Basic → Expert</li><li>English + Hinglish</li><li>Cheat sheet har chapter</li></ul></div>
<img class="img" src="{COVER}" style="right:60px;top:200px;width:400px;transform:rotate(5deg)">
<div class="m" style="right:430px;top:790px;width:240px;height:240px;transform:rotate(-6deg)">{C("wave")}</div>
<div style="position:absolute;left:60px;bottom:200px"><div class="p"><s>₹299</s>₹199</div>
 <span style="font-family:D;font-size:36px;margin-left:16px">launch offer</span></div>
<div style="position:absolute;left:60px;bottom:120px;font-size:38px">Free preview 👉 <b style="color:#ffd166">techsamjhoraj.com/#book</b></div>
<div class="foot" style="bottom:56px">🔖 Save karo · Python seekhne wale dost ko bhejo</div>""",
]

if __name__ == "__main__":
    for i, body in enumerate(SLIDES, 1):
        h = ADS / ("carousel-%d.html" % i)
        h.write_text(slide(i, body), encoding="utf8")
        png = ADS / ("carousel-%d.png" % i)
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--allow-file-access-from-files", "--virtual-time-budget=6000",
                        "--hide-scrollbars", "--window-size=%d,%d" % (W, H), "--screenshot=" + str(png), h.as_uri()], capture_output=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(png), "-q:v", "2", str(png.with_suffix(".jpg"))])
    # contact sheet for a quick review
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + sum([["-i", str(ADS / ("carousel-%d.png" % i))] for i in range(1, 6)], []) +
                   ["-filter_complex", "".join("[%d]scale=360:-1[s%d];" % (i, i) for i in range(5)) + "".join("[s%d]" % i for i in range(5)) + "hstack=5",
                    "-update", "1", str(ADS / "carousel-sheet.png")])
    print("ok")
