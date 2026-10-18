"""Book launch ads (lives outside python-chai-book; only READS the book's outputs): wide banner (website ad panel, X, YouTube), 4:5 feed post (Instagram/Facebook/YouTube community), 9:16 story.
Run: python ads.py   -> book-ads/out/book-ad-{wide,post,story}.jpg
Needs out/cover-en.png (python book.py) and grabs a real inside page from out/notes/python-12-en.html."""
import subprocess, pathlib, sys, glob, os
sys.dont_write_bytecode = True  # don't drop __pycache__ into the book folder
BOOK = pathlib.Path("C:/samjhowithraj/vlog1/videos/python-chai-book")
sys.path.insert(0, str(BOOK))
from mascot import chotu
CHROME = glob.glob(os.path.expanduser("~/.cache/hyperframes/chrome/chrome-headless-shell/*/chrome-headless-shell-win64/chrome-headless-shell.exe"))[0]

HERE = pathlib.Path(__file__).parent.resolve()
F = (BOOK / "fonts").as_uri()
OUT = BOOK / "out"          # read-only: cover-en.png, notes/python-12-en.html
ADS = HERE / "out"

BASE = f"""@font-face{{font-family:D;src:url({F}/Baloo2-800.woff2)}}
@font-face{{font-family:H;src:url({F}/Caveat-700.woff2)}}
@font-face{{font-family:Body;src:url({F}/DMSans-400.woff2)}}
html,body{{margin:0;overflow:hidden}}
body{{background:linear-gradient(160deg,#2a1260 0%,#5b1a8f 42%,#c2185b 72%,#ff7a2f 100%);font-family:Body,"Segoe UI",Arial,sans-serif;color:#fff;position:relative}}
.sun{{position:absolute;border-radius:50%;background:radial-gradient(circle,rgba(255,214,120,.55),rgba(255,214,120,0) 70%)}}
.cov,.pg{{position:absolute;border-radius:12px;box-shadow:0 30px 60px rgba(0,0,0,.45)}}
.pg{{border-radius:6px}}
.m{{position:absolute}}
.k{{font-family:H;color:#ffd166}}
h1{{font-family:D;line-height:.95;margin:6px 0 10px}}
ul{{list-style:none;padding:0}}
li:before{{content:"\\2615  "}}
.p{{display:inline-block;background:#ffd166;color:#2a1260;border-radius:16px;padding:12px 26px;font-family:D}}
.p s{{opacity:.6;margin-right:12px}}
.u{{position:absolute;opacity:.9}}
.u b{{color:#ffd166}}"""

LIST = "<ul><li>English &amp; Hinglish editions</li><li>120+ examples, all outputs really run</li><li>Mistakes, practice, answers &amp; cheat sheets</li></ul>"

FORMATS = {
    "wide": (1280, 720, """
.sun{right:120px;top:-140px;width:620px;height:620px}
.cov{right:110px;top:70px;width:410px;transform:rotate(4deg)}
.m{right:545px;bottom:14px;width:170px;height:170px;transform:rotate(-6deg)}
.t{position:absolute;left:70px;top:70px;width:640px}
.k{font-size:46px} h1{font-size:96px} .s{font-size:30px;opacity:.95}
ul{margin:26px 0;font-size:26px;line-height:1.55} .p{position:absolute;left:70px;bottom:96px;font-size:40px} .p s{font-size:28px}
.u{left:70px;bottom:40px;font-size:24px}""", False),
    "post": (1080, 1350, """
.sun{right:-120px;top:420px;width:760px;height:760px}
.t{position:absolute;left:70px;top:60px;right:70px}
.k{font-size:54px} h1{font-size:118px} .s{font-size:34px;opacity:.95}
.pg{left:70px;top:560px;width:390px;transform:rotate(-5deg)}
.cov{right:80px;top:500px;width:470px;transform:rotate(4deg)}
.m{left:20px;top:930px;width:170px;height:170px;transform:rotate(-8deg)}
ul{display:none}
.pg{top:540px}
.p{position:absolute;left:70px;bottom:120px;font-size:44px} .p s{font-size:30px}
.u{left:70px;bottom:56px;font-size:30px}""", True),
    "story": (1080, 1920, """
.sun{right:-160px;top:760px;width:900px;height:900px}
.t{position:absolute;left:80px;top:170px;right:80px}
.k{font-size:64px} h1{font-size:140px} .s{font-size:40px;opacity:.95}
ul{margin:34px 0 0;font-size:36px;line-height:1.6}
.pg{left:80px;top:850px;width:420px;transform:rotate(-5deg)}
.cov{right:80px;top:800px;width:480px;transform:rotate(4deg)}
.m{left:20px;top:1330px;width:200px;height:200px;transform:rotate(-8deg)}
.p{position:absolute;left:80px;bottom:290px;font-size:56px} .p s{font-size:38px}
.u{left:80px;bottom:215px;font-size:36px}""", True),
}


def html(name):
    w, h, css, peek = FORMATS[name]
    page = '<img class="pg" src="%s">' % (ADS / "page.png").as_uri() if peek else ""
    return f"""<!doctype html><meta charset="utf-8"><style>{BASE}
html,body{{width:{w}px;height:{h}px}}{css}</style><body><div class="sun"></div>
{page}<img class="cov" src="{(OUT / 'cover-en.png').as_uri()}">
<div class="m">{chotu("party", "")}</div>
<div class="t"><div class="k">New book by Raj</div><h1>Python<br>with Chai</h1>
<div class="s">From Basic to Expert · 30 illustrated chapters</div>{LIST}</div>
<div class="p"><s>₹299</s>₹199 launch offer</div>
<div class="u">Free preview: <b>techsamjhoraj.com/#book</b></div></body>"""


def shot(url, w, h, png, scale=1):
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--allow-file-access-from-files", "--virtual-time-budget=6000",
                    "--hide-scrollbars", "--force-device-scale-factor=%s" % scale, "--window-size=%d,%d" % (w, h),
                    "--screenshot=" + str(png), url], capture_output=True)


if __name__ == "__main__":
    ADS.mkdir(exist_ok=True)
    # a real inside page (Chapter 12, page 5: Example 1) for the "peek inside" look
    tall = ADS / "pages.png"
    shot((OUT / "notes" / "python-12-en.html").as_uri(), 560, 4000, tall, 2)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tall), "-vf", "crop=1120:1588:0:6350", "-update", "1", str(ADS / "page.png")])
    for name, (w, h, _, _) in FORMATS.items():
        src = ADS / ("ad-%s.html" % name)
        src.write_text(html(name), encoding="utf8")
        png = ADS / ("book-ad-%s.png" % name)
        shot(src.as_uri(), w, h, png)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(png), "-q:v", "2", str(png.with_suffix(".jpg"))])
    print("ok", ADS)
