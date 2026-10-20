"""Pre-launch ads for "Reasoning Samjho: Puzzle se Selection tak" (Dimaag Dada): the approved ads.py + carousel.py
designs, words and images swapped, Chotu swapped for Dimaag Dada. No buy link and no price (listing not live yet).
Never promise a selection or a rank; every ad carries the "original puzzles, not affiliated" line.
Run: python puzzle_ads.py [A|B|C] -> out/puzzle/teaser-{post,story,wide}.jpg, out/puzzle/jaal-1..5.jpg, out/puzzle/sheet.png
(cover A, Raj's pick)."""
import subprocess, sys, pathlib, importlib.util
sys.dont_write_bytecode = True
import ads as A
import carousel as C

BOOK = pathlib.Path("C:/samjhowithraj/vlog1/videos/exam-puzzle-book")
_s = importlib.util.spec_from_file_location("dada_book_mascot", BOOK / "mascot.py")
_m = importlib.util.module_from_spec(_s); _s.loader.exec_module(_m)
dada = lambda pose: _m.dada(pose, "")

P = A.ADS / "puzzle"
LETTER = (sys.argv[1] if len(sys.argv) > 1 else "A").upper()
COVER = (BOOK / "out" / "covers" / f"cover-{LETTER}-en.png").as_uri()
U = lambda f: (P / f).as_uri()
NOT_AFF = "Original puzzles · exam names belong to their bodies · not affiliated"


def pages():
    tall = P / "tall3.png"
    if not tall.exists():
        A.shot((BOOK / "out" / "notes" / "puzzles-3-en.html").as_uri(), 560, 8000, tall, 2)
    for name, crop in [("q.png", "1120:750:0:6340"), ("sol.png", "1120:600:0:7100")]:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tall), "-vf", "crop=" + crop, "-update", "1", str(P / name)])


LIST = "<ul><li>SSC · Bank · Railway · CSAT · CAT · Placements</li><li>Har jawab computer se check kiya hua</li><li>Shortcuts, traps + 3 mock tests</li></ul>"
TEASER = [
    ('<div class="k">New book by Raj</div>', '<div class="k">Competitive exam ki taiyari? 🎯</div>'),
    ("Python<br>with Chai", "Reasoning<br>Samjho"),
    ("From Basic to Expert · 30 illustrated chapters", "Puzzle se Selection tak · 192 original puzzles"),
    (A.LIST, LIST),
    ("<s>₹299</s>₹199 launch offer", "<s>₹299</s> ₹275 till 30 Nov"),
    ("Free preview: <b>techsamjhoraj.com/#book</b>",
     'Free Chapter 1: <b>techsamjhoraj.com/#puzzles</b><br><span style="font-size:.72em;opacity:.85">' + NOT_AFF + "</span>"),
    ((A.OUT / "cover-en.png").as_uri(), COVER),
    ((A.ADS / "page.png").as_uri(), U("q.png")),
    (A.chotu("party", ""), dada("aha")),
    ("</style>", ".p{transform:translateY(-30px)}</style>"),
]

FOOT = f'<div class="foot" style="font-size:20px;bottom:18px;opacity:.7">{NOT_AFF}</div>'
JAAL = [
    f"""<div class="sun" style="right:-160px;top:430px;width:900px;height:900px"></div>
<div style="position:absolute;left:60px;top:70px;right:60px">
 <div class="k" style="font-size:52px">90% log yahan galti karte hain 😬</div>
 <h1 style="font-size:132px;margin-top:10px">Jaal<br><em>pakdo!</em></h1></div>
<img class="img" src="{U('q.png')}" style="left:70px;top:470px;width:640px;transform:rotate(-3deg)">
<div class="burst" style="right:40px;top:330px;transform:rotate(12deg)">SSC<br>FAVE</div>
<div class="m" style="right:30px;top:820px;width:320px;height:320px">{dada("think")}</div>
<div class="bub r" style="right:90px;top:700px;font-size:40px">Answer kya hoga?</div>
<div class="tag" style="left:60px;bottom:120px;font-size:38px">Comment karo: a, b, c ya d?</div>
<div class="swipe">Swipe →</div>{FOOT}""",
    f"""<div class="sun" style="left:-200px;top:520px;width:800px;height:800px"></div>
<div style="position:absolute;left:60px;top:120px;right:60px">
 <div class="k" style="font-size:54px">Dimaag Dada ka rule</div>
 <h1 style="font-size:124px;margin-top:10px">Ruko!<br><em>Pehle socho,</em><br>phir likho.</h1></div>
<div class="m" style="right:60px;top:760px;width:380px;height:380px">{dada("timer")}</div>
<div class="bub l" style="left:70px;top:860px;font-size:42px">5 second… dhyaan se padho!</div>
<div class="foot">Answer agli slide mein →</div>""",
    f"""<div class="sun" style="right:-200px;top:300px;width:800px;height:800px"></div>
<div style="position:absolute;left:60px;top:80px;right:60px">
 <div class="k" style="font-size:52px">Sabse common galti</div>
 <h1 style="font-size:150px;margin-top:6px">23? <em>Jaal hai!</em></h1></div>
<div class="tag" style="left:60px;top:470px;font-size:46px;line-height:1.25;transform:rotate(-2deg)">9 + 14 = 23 …<br>par Tara do baar<br>gini gayi! ❌</div>
<div class="m" style="right:50px;top:800px;width:340px;height:340px">{dada("ask")}</div>
<div class="bub r" style="right:90px;top:690px;font-size:38px">Toppers bhi phas jaate hain!</div>
<div class="foot">Left se 8, right se 13, aur Tara khud</div>""",
    f"""<div class="sun" style="left:-160px;top:420px;width:800px;height:800px"></div>
<div style="position:absolute;left:60px;top:80px;right:60px">
 <div class="k" style="font-size:50px">Order &amp; Ranking · Puzzle 3.1</div>
 <h1 style="font-size:110px;margin-top:6px">Dada ka<br><em>shortcut</em></h1></div>
<img class="img" src="{U('sol.png')}" style="left:70px;top:450px;width:640px;transform:rotate(2deg)">
<div class="tag" style="right:40px;top:860px;font-size:50px;transform:rotate(4deg)">L + R − 1 = 22 ✓</div>
<div class="m" style="right:420px;top:930px;width:260px;height:260px">{dada("thumbs")}</div>
<div class="foot">Har jawab computer se check kiya hua</div>""",
    f"""<div class="sun" style="right:-120px;top:380px;width:820px;height:820px"></div>
<div style="position:absolute;left:60px;top:80px;width:560px">
 <div class="k" style="font-size:52px">Ab available hai 📘</div>
 <h1 style="font-size:104px;margin-top:6px">Reasoning<br>Samjho</h1>
 <ul style="font-size:32px;margin-top:30px">
  <li>192 original puzzles</li><li>SSC · Bank · Railway</li><li>CSAT · CAT · Placements</li><li>Shortcuts, traps, 3 mocks</li><li>English + Hinglish</li></ul></div>
<img class="img" src="{COVER}" style="right:60px;top:200px;width:400px;transform:rotate(5deg)">
<div class="m" style="right:420px;top:800px;width:240px;height:240px">{dada("aha")}</div>
<div style="position:absolute;left:60px;bottom:200px"><div class="p"><s>₹299</s>₹275</div><span style="font-family:D;font-size:34px;margin-left:16px">till 30 Nov · dono ₹367</span></div>
<div style="position:absolute;left:60px;bottom:120px;font-size:36px">Buy link 👉 <b style="color:#ffd166">bio + comments mein</b></div>
{FOOT}""",
]


def jpg(png):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(png), "-q:v", "2", str(png.with_suffix(".jpg"))])


if __name__ == "__main__":
    P.mkdir(parents=True, exist_ok=True)
    pages()
    for fmt, (w, h, _, _) in A.FORMATS.items():
        page = A.html(fmt)
        if fmt == "wide":  # list + not-affiliated line need a little more room than the book ad
            page = page.replace("</style>", "h1{font-size:84px} ul{margin:16px 0;font-size:24px}</style>", 1)
        for a, b in TEASER:
            page = page.replace(a, b, 1)
        src = P / f"teaser-{fmt}.html"
        src.write_text(page, encoding="utf8")
        A.shot(src.as_uri(), w, h, P / f"teaser-{fmt}.png")
        jpg(P / f"teaser-{fmt}.png")
    for i, body in enumerate(JAAL, 1):
        src = P / f"jaal-{i}.html"
        src.write_text(C.slide(i, body), encoding="utf8")
        A.shot(src.as_uri(), C.W, C.H, P / f"jaal-{i}.png")
        jpg(P / f"jaal-{i}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + sum([["-i", str(P / f"jaal-{i}.png")] for i in range(1, 6)], []) +
                   ["-filter_complex", "".join("[%d]scale=360:-1[s%d];" % (i, i) for i in range(5)) + "".join("[s%d]" % i for i in range(5)) + "hstack=5",
                    "-update", "1", str(P / "sheet.png")])
    print("ok", P, "cover", LETTER)
