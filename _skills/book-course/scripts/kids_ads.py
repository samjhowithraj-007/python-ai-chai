"""Children's Day (14 Nov) ads for the free Samjho Squad sampler, aimed at parents: the approved ads.py + carousel.py
designs, words and images swapped. Mascots: Dabba, Tara, Jugnu, Tikki, Kauri only (never Chotu or Gullak Bhai).
Books are out Dec 2026: no buy link, no code. Link = the sites' free sampler card. Money page carries "Financial education, not advice".
Run: python kids_ads.py -> out/kids/sampler-{post,story,wide}.jpg, out/kids/squad-1..5.jpg, out/kids/sheet.png"""
import subprocess, sys, pathlib, importlib.util
sys.dont_write_bytecode = True
import ads as A
import carousel as C

KIDS = pathlib.Path("C:/samjhowithraj/kids-books")
_s = importlib.util.spec_from_file_location("kids_mascots", KIDS / "mascots" / "kids_mascots.py")
K = importlib.util.module_from_spec(_s); _s.loader.exec_module(K)
P = A.ADS / "kids"
U = lambda f: (P / f).as_uri()
M = lambda name, expr="happy": getattr(K, name)(expr, "")
FOOT = '<div class="foot" style="font-size:20px;bottom:18px;opacity:.75">Books out Dec 2026 · free sampler for Children\'s Day</div>'


def pages():
    # shoot the rebuilt sampler (final covers) fresh each run: 794 px square pages stacked; 0 cover, 1 squad, 2 loops, 4 Tara AI, 8 three jars
    tall = P / "tall.png"
    A.shot((KIDS / "sampler" / "sampler-en.html").as_uri(), 794, 11116, tall, 1)
    for i in (0, 1, 2, 4, 8):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tall),
                        "-vf", f"crop=794:794:0:{i * 794}", "-update", "1", str(P / f"page{i}.png")])


LIST = "<ul><li>Python, AI, money + science comics</li><li>Ages 9–18 · English + Hinglish</li><li>5 free comic spreads (PDF)</li></ul>"
SINGLE = [
    ('<div class="k">New book by Raj</div>', '<div class="k">Children\'s Day gift 🎁</div>'),
    ("Python<br>with Chai", "Samjho<br>Squad"),
    ("From Basic to Expert · 30 illustrated chapters", "Paisa, AI + coding: ab comics mein!"),
    (A.LIST, LIST),
    ("<s>₹299</s>₹199 launch offer", "Free sampler"),
    ("Free preview: <b>techsamjhoraj.com/#book</b>", 'Download: <b>link bio + comments mein</b><br><span style="font-size:.72em;opacity:.85">Books out Dec 2026</span>'),
    ((A.OUT / "cover-en.png").as_uri(), U("page0.png")),
    ((A.ADS / "page.png").as_uri(), U("page1.png")),
    (A.chotu("party", ""), M("dabba")),
    ("</style>", ".p{transform:translateY(-30px)}</style>"),
]

SLIDES = [
    f"""<div class="sun" style="right:-160px;top:430px;width:900px;height:900px"></div>
<div style="position:absolute;left:60px;top:70px;right:60px">
 <div class="k" style="font-size:48px">School nahi sikhata: paisa, AI, coding 🤷</div>
 <h1 style="font-size:128px;margin-top:10px">Comics se<br><em>seekhenge!</em></h1></div>
<img class="img" src="{U('page0.png')}" style="right:80px;top:460px;width:500px;transform:rotate(4deg)">
<div class="burst" style="right:20px;top:380px;transform:rotate(12deg)">FREE<br>SAMPLER</div>
<div class="m" style="left:40px;top:820px;width:330px;height:330px">{M("dabba")}</div>
<div class="bub l" style="left:70px;top:700px;font-size:40px">Hi! Main Dabba!</div>
<div class="tag" style="left:60px;bottom:120px;font-size:38px">Ages 9–18 · EN + Hinglish</div>
<div class="swipe">Swipe →</div>{FOOT}""",
    f"""<div class="sun" style="left:-200px;top:520px;width:800px;height:800px"></div>
<div style="position:absolute;left:60px;top:80px;right:60px">
 <div class="k" style="font-size:50px">Coding, comic mein 💻</div>
 <h1 style="font-size:100px;margin-top:6px">Dabba ke saath<br><em>loops</em></h1></div>
<img class="img" src="{U('page2.png')}" style="left:90px;top:420px;width:600px;transform:rotate(-3deg)">
<div class="m" style="right:40px;top:870px;width:290px;height:290px">{M("dabba")}</div>
<div class="foot">Real Python · har code sach mein run kiya</div>""",
    f"""<div class="sun" style="right:-200px;top:300px;width:800px;height:800px"></div>
<div style="position:absolute;left:60px;top:80px;right:60px">
 <div class="k" style="font-size:50px">AI kaise sochta hai? 🤖</div>
 <h1 style="font-size:100px;margin-top:6px">Tara ke saath<br><em>AI</em></h1></div>
<img class="img" src="{U('page4.png')}" style="left:90px;top:420px;width:600px;transform:rotate(3deg)">
<div class="m" style="right:40px;top:870px;width:290px;height:290px">{M("tara")}</div>
<div class="foot">Machine learning, bina darr ke</div>""",
    f"""<div class="sun" style="left:-160px;top:420px;width:800px;height:800px"></div>
<div style="position:absolute;left:60px;top:80px;right:60px">
 <div class="k" style="font-size:50px">Pocket money ka pehla lesson 🪙</div>
 <h1 style="font-size:100px;margin-top:6px">Kauri ke saath<br><em>3 jars</em></h1></div>
<img class="img" src="{U('page8.png')}" style="left:90px;top:420px;width:600px;transform:rotate(-2deg)">
<div class="m" style="right:40px;top:870px;width:290px;height:290px">{M("kauri")}</div>
<div class="foot">Spend · Save · Share · Financial education, not advice</div>""",
    f"""<div class="sun" style="right:-120px;top:380px;width:820px;height:820px"></div>
<div style="position:absolute;left:60px;top:80px;width:560px">
 <div class="k" style="font-size:52px">Children's Day gift 🎁</div>
 <h1 style="font-size:104px;margin-top:6px">Samjho<br>Squad</h1>
 <ul style="font-size:32px;margin-top:30px">
  <li>5 free comic spreads</li><li>Python · AI · Money · Science</li><li>Ages 9–18</li><li>English + Hinglish</li></ul></div>
<img class="img" src="{U('page1.png')}" style="right:60px;top:220px;width:420px;transform:rotate(5deg)">
<div class="m" style="right:420px;top:790px;width:240px;height:240px">{M("tikki")}</div>
<div style="position:absolute;left:60px;bottom:200px"><div class="p">FREE</div>
 <span style="font-family:D;font-size:36px;margin-left:16px">sampler PDF</span></div>
<div style="position:absolute;left:60px;bottom:120px;font-size:36px">Download 👉 <b style="color:#ffd166">link bio + comments mein</b></div>
{FOOT}""",
]


def jpg(png):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(png), "-q:v", "2", str(png.with_suffix(".jpg"))])


if __name__ == "__main__":
    P.mkdir(parents=True, exist_ok=True)
    pages()
    for fmt, (w, h, _, _) in A.FORMATS.items():
        page = A.html(fmt)
        if fmt == "wide":
            page = page.replace("</style>", "h1{font-size:84px} ul{margin:16px 0;font-size:24px} .s{font-size:24px}</style>", 1)
        for a, b in SINGLE:
            page = page.replace(a, b, 1)
        src = P / f"sampler-{fmt}.html"
        src.write_text(page, encoding="utf8")
        A.shot(src.as_uri(), w, h, P / f"sampler-{fmt}.png")
        jpg(P / f"sampler-{fmt}.png")
    for i, body in enumerate(SLIDES, 1):
        src = P / f"squad-{i}.html"
        src.write_text(C.slide(i, body), encoding="utf8")
        A.shot(src.as_uri(), C.W, C.H, P / f"squad-{i}.png")
        jpg(P / f"squad-{i}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + sum([["-i", str(P / f"squad-{i}.png")] for i in range(1, 6)], []) +
                   ["-filter_complex", "".join("[%d]scale=360:-1[s%d];" % (i, i) for i in range(5)) + "".join("[s%d]" % i for i in range(5)) + "hstack=5",
                    "-update", "1", str(P / "sheet.png")])
    print("ok", P)
