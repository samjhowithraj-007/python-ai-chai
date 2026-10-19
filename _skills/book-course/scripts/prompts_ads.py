"""Ads for the "50 AI Prompts for Jobs + Study" PDF (₹149): same approved designs as ads.py + carousel.py, words and images swapped.
Run: python prompts_ads.py -> out/prompts/ad-{post,story,wide}.jpg, out/prompts/slide-1..5.jpg, out/prompts/sheet.png
Uses 2 sample page shots only (prompt 1 + contents), never the full PDF. No buy URL baked in (link goes in the caption)."""
import subprocess, sys, pathlib
sys.dont_write_bytecode = True
import ads as A
import carousel as C

P = A.ADS / "prompts"
SRC = pathlib.Path("C:/samjhowithraj/vlog1/videos/ai-prompts-pdf/out")
COVER = (SRC / "cover-en.png").as_uri()
U = lambda f: (P / f).as_uri()
CH = lambda pose: C.chotu(pose, "")


def pages():
    tall = P / "tall.png"
    if not tall.exists():
        A.shot((SRC / "50-ai-prompts-en.html").as_uri(), 560, 6000, tall, 2)
    for name, crop in [("p1.png", "1120:1180:0:9530"), ("reply.png", "1120:820:0:9840"), ("toc.png", "1120:1000:0:6420")]:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tall), "-vf", "crop=" + crop, "-update", "1", str(P / name)])


LIST = "<ul><li>Resume, interview, study, coding, office</li><li>Har prompt ka real AI reply</li><li>English &amp; Hinglish editions</li></ul>"

SINGLE = [
    ("New book by Raj", "New PDF by Raj"),
    ("Python<br>with Chai", "50 AI<br>Prompts"),
    ("From Basic to Expert · 30 illustrated chapters", "for Jobs + Study · copy, paste, done"),
    (A.LIST, LIST),
    ("<s>₹299</s>₹199 launch offer", "Sirf ₹149"),
    ("Free preview: <b>techsamjhoraj.com/#book</b>", "Buy link: <b>bio + comments mein</b>"),
    ((A.OUT / "cover-en.png").as_uri(), COVER),
    ((A.ADS / "page.png").as_uri(), U("p1.png")),
]

SLIDES = [
    f"""<div class="sun" style="right:-160px;top:430px;width:900px;height:900px"></div>
<div style="position:absolute;left:60px;top:70px;right:60px">
 <div class="k" style="font-size:50px">ChatGPT / Claude se job kaise milegi? 🤔</div>
 <h1 style="font-size:132px;margin-top:10px">50 ready<br><em>AI prompts</em></h1></div>
<img class="img" src="{COVER}" style="right:90px;top:470px;width:470px;transform:rotate(5deg)">
<div class="burst" style="right:20px;top:300px;transform:rotate(12deg)">NEW<br>PDF</div>
<div class="m" style="left:40px;top:830px;width:330px;height:330px;transform:rotate(-6deg)">{CH("party")}</div>
<div class="bub l" style="left:70px;top:705px;font-size:40px">Copy, paste, done!</div>
<div class="tag" style="left:60px;bottom:120px;font-size:40px">₹149 · EN + Hinglish</div>
<div class="swipe">Swipe →</div>""",
    f"""<div class="sun" style="left:-200px;top:520px;width:800px;height:800px"></div>
<div style="position:absolute;left:60px;top:80px;right:60px">
 <div class="k" style="font-size:50px">Prompt #1 · Resume</div>
 <h1 style="font-size:96px;margin-top:6px">Duties ko<br><em>achievements</em> banao</h1></div>
<img class="img" src="{U('p1.png')}" style="left:90px;top:430px;width:600px;transform:rotate(-4deg)">
<div class="m" style="right:40px;top:860px;width:300px;height:300px;transform:rotate(6deg)">{CH("read")}</div>
<div class="bub r" style="right:70px;top:740px;font-size:38px">[Brackets] badlo, paste karo!</div>
<div class="foot">Har prompt: copy karo, apni details daalo, AI ko do</div>""",
    f"""<div class="sun" style="right:-200px;top:300px;width:800px;height:800px"></div>
<div style="position:absolute;left:60px;top:80px;right:60px">
 <h1 style="font-size:100px">Har prompt ka<br><em>asli AI jawab</em></h1></div>
<img class="img" src="{U('reply.png')}" style="left:80px;top:420px;width:620px;transform:rotate(-3deg)">
<div class="tag" style="right:50px;top:640px;font-size:38px;transform:rotate(4deg)">Real AI reply,<br>andar hi ✓</div>
<div class="m" style="right:60px;top:880px;width:290px;height:290px">{CH("cool")}</div>
<div class="foot">Pehle dekho jawab kaisa aata hai, phir khud try karo</div>""",
    f"""<div class="sun" style="left:-160px;top:420px;width:800px;height:800px"></div>
<div style="position:absolute;left:60px;top:80px;right:60px">
 <div class="k" style="font-size:50px">Job + Study + Office</div>
 <h1 style="font-size:100px;margin-top:6px">50 prompts,<br><em>5 sections</em></h1></div>
<img class="img" src="{U('toc.png')}" style="left:90px;top:440px;width:560px;transform:rotate(3deg)">
<div class="m" style="right:50px;top:860px;width:300px;height:300px;transform:rotate(-4deg)">{CH("wave")}</div>
<div class="bub r" style="right:60px;top:740px;font-size:38px">Interview kal hai? ✓</div>
<div class="foot">Resume · Interview · Study · Coding · Office</div>""",
    f"""<div class="sun" style="right:-120px;top:380px;width:820px;height:820px"></div>
<div style="position:absolute;left:60px;top:80px;width:560px">
 <div class="k" style="font-size:52px">New PDF by Raj</div>
 <h1 style="font-size:104px;margin-top:6px">50 AI<br>Prompts</h1>
 <ul style="font-size:34px;margin-top:30px">
  <li>Jobs + Study + Office</li><li>Har prompt ka real AI reply</li><li>English + Hinglish</li><li>ChatGPT, Claude, Gemini</li></ul></div>
<img class="img" src="{COVER}" style="right:60px;top:200px;width:400px;transform:rotate(5deg)">
<div class="m" style="right:430px;top:790px;width:240px;height:240px;transform:rotate(-6deg)">{CH("wave")}</div>
<div style="position:absolute;left:60px;bottom:200px"><div class="p">₹149</div>
 <span style="font-family:D;font-size:36px;margin-left:16px">PDF · EN + Hinglish</span></div>
<div style="position:absolute;left:60px;bottom:120px;font-size:38px">Buy link 👉 <b style="color:#ffd166">bio + comments mein</b></div>
<div class="foot" style="bottom:56px">🔖 Save karo · job dhoondh rahe dost ko bhejo</div>""",
]


def jpg(png):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(png), "-q:v", "2", str(png.with_suffix(".jpg"))])


if __name__ == "__main__":
    P.mkdir(parents=True, exist_ok=True)
    pages()
    for fmt, (w, h, _, _) in A.FORMATS.items():
        page = A.html(fmt)
        for a, b in SINGLE:
            page = page.replace(a, b)
        src = P / f"ad-{fmt}.html"
        src.write_text(page, encoding="utf8")
        A.shot(src.as_uri(), w, h, P / f"ad-{fmt}.png")
        jpg(P / f"ad-{fmt}.png")
    for i, body in enumerate(SLIDES, 1):
        src = P / f"slide-{i}.html"
        src.write_text(C.slide(i, body), encoding="utf8")
        A.shot(src.as_uri(), C.W, C.H, P / f"slide-{i}.png")
        jpg(P / f"slide-{i}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + sum([["-i", str(P / f"slide-{i}.png")] for i in range(1, 6)], []) +
                   ["-filter_complex", "".join("[%d]scale=360:-1[s%d];" % (i, i) for i in range(5)) + "".join("[s%d]" % i for i in range(5)) + "hstack=5",
                    "-update", "1", str(P / "sheet.png")])
    print("ok", P)
