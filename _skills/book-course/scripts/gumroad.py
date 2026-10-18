"""Gumroad product images: 1280x720 cover + 600x600 thumbnail for each product (English, Hinglish, Both).
Run: python gumroad.py  -> out/gumroad/{en,hi,both}-{cover,thumb}.png"""
import subprocess, sys
sys.dont_write_bytecode = True
from ads import chotu, CHROME, F, OUT as BOOKOUT, ADS

G = ADS / "gumroad"
COV = {k: (BOOKOUT / ("cover-%s.png" % k)).as_uri() for k in ("en", "hi")}
PRODUCTS = {"en": "English edition", "hi": "Hinglish edition", "both": "English + Hinglish"}

BASE = f"""@font-face{{font-family:D;src:url({F}/Baloo2-800.woff2)}}
@font-face{{font-family:H;src:url({F}/Caveat-700.woff2)}}
@font-face{{font-family:Body;src:url({F}/DMSans-400.woff2)}}
html,body{{margin:0;overflow:hidden}}
body{{background:linear-gradient(160deg,#2a1260 0%,#5b1a8f 42%,#c2185b 72%,#ff7a2f 100%);font-family:Body,sans-serif;color:#fff;position:relative}}
.sun{{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(255,214,120,.55),rgba(255,214,120,0) 70%)}}
.c{{position:absolute;border-radius:10px;box-shadow:0 26px 50px rgba(0,0,0,.45)}}
.k{{font-family:H;color:#ffd166}} h1{{font-family:D;line-height:.95;margin:0}}
.ed{{display:inline-block;background:#ffd166;color:#2a1260;font-family:D;border-radius:12px;padding:6px 18px}}
.m{{position:absolute}}"""


def covers(k):
    if k == "both":
        return (f'<img class="c" src="{COV["hi"]}" style="right:250px;top:110px;width:330px;transform:rotate(-6deg)">'
                f'<img class="c" src="{COV["en"]}" style="right:70px;top:70px;width:350px;transform:rotate(5deg)">')
    return f'<img class="c" src="{COV[k]}" style="right:90px;top:70px;width:410px;transform:rotate(4deg)">'


def cover_html(k):
    return f"""<!doctype html><meta charset="utf-8"><style>{BASE}
html,body{{width:1280px;height:720px}}</style><body><div class="sun" style="right:100px;top:-140px;width:640px;height:640px"></div>
{covers(k)}<div class="m" style="left:545px;bottom:6px;width:160px;height:160px;transform:rotate(-6deg)">{chotu("party", "")}</div>
<div style="position:absolute;left:70px;top:80px;width:560px"><div class="k" style="font-size:44px">by Raj</div>
<h1 style="font-size:100px;margin:6px 0 12px">Python<br>with Chai</h1>
<div style="font-size:30px">From Basic to Expert</div>
<div class="ed" style="font-size:36px;margin-top:22px">{PRODUCTS[k]}</div>
<div style="font-size:24px;margin-top:22px;opacity:.95;line-height:1.5">30 illustrated chapters · {'2 × ' if k == 'both' else ''}336-page PDF<br>Real code, real output · answers &amp; index</div></div></body>"""


def thumb_html(k):
    inner = (f'<img class="c" src="{COV["hi"]}" style="left:70px;top:90px;width:270px;transform:rotate(-7deg)">'
             f'<img class="c" src="{COV["en"]}" style="left:250px;top:60px;width:285px;transform:rotate(5deg)">') if k == "both" else \
        f'<img class="c" src="{COV[k]}" style="left:140px;top:40px;width:320px;transform:rotate(3deg)">'
    return f"""<!doctype html><meta charset="utf-8"><style>{BASE}
html,body{{width:600px;height:600px}}</style><body><div class="sun" style="left:60px;top:40px;width:520px;height:520px"></div>
{inner}<div class="ed" style="position:absolute;left:50%;transform:translateX(-50%);bottom:28px;font-size:30px;white-space:nowrap">{PRODUCTS[k]}</div></body>"""


def shot(html, w, h, png):
    src = png.with_suffix(".html"); src.write_text(html, encoding="utf8")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--allow-file-access-from-files", "--virtual-time-budget=6000",
                    "--hide-scrollbars", "--window-size=%d,%d" % (w, h), "--screenshot=" + str(png), src.as_uri()], capture_output=True)


if __name__ == "__main__":
    G.mkdir(exist_ok=True)
    for k in PRODUCTS:
        shot(cover_html(k), 1280, 720, G / ("%s-cover.png" % k))
        shot(thumb_html(k), 600, 600, G / ("%s-thumb.png" % k))
    sheet = [str(G / ("%s-%s.png" % (k, t))) for k in PRODUCTS for t in ("cover", "thumb")]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + sum([["-i", p] for p in sheet], []) + ["-filter_complex",
                    "".join("[%d]scale=-1:240[s%d];" % (i, i) for i in range(6)) + "".join("[s%d]" % i for i in range(6)) + "hstack=6",
                    "-update", "1", str(G / "sheet.png")])
    print("ok")
