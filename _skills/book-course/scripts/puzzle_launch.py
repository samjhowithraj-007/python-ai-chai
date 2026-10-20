"""Launch + countdown ads for "Reasoning Samjho" with the public DADA code (8% off: ₹275 per edition, ₹367 both, till 30 Nov).
Same approved designs as ads.py + carousel.py (via puzzle_ads.py), words and images swapped. Never the private code.
Run: python puzzle_launch.py -> out/puzzle/launch-1..5.jpg, out/puzzle/{3days,lastday}-{post,story,wide}.jpg, out/puzzle/launch-sheet.png"""
import subprocess, sys
sys.dont_write_bytecode = True
import ads as A
import carousel as C
import puzzle_ads as PA

P, U, dada, COVER, NOT_AFF, FOOT = PA.P, PA.U, PA.dada, PA.COVER, PA.NOT_AFF, PA.FOOT
PRICE_TAG = "<s>₹299</s> ₹275 till 30 Nov"


def story_page():
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(P / "tall3.png"), "-vf", "crop=1120:1270:0:1640",
                    "-update", "1", str(P / "story.png")])


SLIDES = [
    f"""<div class="sun" style="right:-160px;top:430px;width:900px;height:900px"></div>
<div style="position:absolute;left:60px;top:70px;right:60px">
 <div class="k" style="font-size:52px">SSC · Bank · Railway · CAT · Placements</div>
 <h1 style="font-size:126px;margin-top:10px">Reasoning<br><em>Samjho</em></h1></div>
<img class="img" src="{COVER}" style="right:90px;top:430px;width:440px;transform:rotate(5deg)">
<div class="burst" style="right:20px;top:330px;transform:rotate(12deg)">OUT<br>NOW!</div>
<div class="m" style="left:40px;top:800px;width:330px;height:330px">{dada("aha")}</div>
<div class="bub l" style="left:70px;top:680px;font-size:40px">Ruko! Pehle socho!</div>
<div class="tag" style="left:60px;bottom:120px;font-size:40px">{PRICE_TAG}</div>
<div class="swipe">Swipe →</div>{FOOT}""",
    f"""<div class="sun" style="left:-200px;top:520px;width:800px;height:800px"></div>
<div style="position:absolute;left:60px;top:80px;right:60px">
 <div class="k" style="font-size:50px">Har chapter shuru hota hai…</div>
 <h1 style="font-size:96px;margin-top:6px">Dada ki<br><em>class</em> se</h1></div>
<img class="img" src="{U('story.png')}" style="left:90px;top:420px;width:560px;transform:rotate(-4deg)">
<div class="m" style="right:30px;top:860px;width:300px;height:300px">{dada("ask")}</div>
<div class="bub r" style="right:70px;top:740px;font-size:38px">Pehle kahani, phir formula</div>
<div class="foot">Concept kahani mein, shortcut baad mein</div>""",
    f"""<div class="sun" style="right:-200px;top:300px;width:800px;height:800px"></div>
<div style="position:absolute;left:60px;top:80px;right:60px">
 <h1 style="font-size:108px">Real exam style.<br><em>192 puzzles.</em></h1></div>
<img class="img" src="{U('q.png')}" style="left:70px;top:420px;width:640px;transform:rotate(-3deg)">
<div class="tag" style="right:40px;top:860px;font-size:38px;transform:rotate(4deg)">Har jawab computer<br>se check kiya ✓</div>
<div class="m" style="left:60px;top:900px;width:260px;height:260px">{dada("think")}</div>
<div class="foot">Seating · ranking · series · coding · clocks · LRDI</div>""",
    f"""<div class="sun" style="left:-160px;top:420px;width:800px;height:800px"></div>
<div style="position:absolute;left:60px;top:80px;right:60px">
 <div class="k" style="font-size:50px">Har puzzle ke saath</div>
 <h1 style="font-size:100px;margin-top:6px">Shortcut +<br><em>jaal</em> dono</h1></div>
<img class="img" src="{U('sol.png')}" style="left:70px;top:440px;width:640px;transform:rotate(2deg)">
<div class="m" style="right:40px;top:870px;width:290px;height:290px">{dada("thumbs")}</div>
<div class="bub r" style="right:80px;top:760px;font-size:38px">Toppers bhi phaste hain!</div>
<div class="foot">3 mock tests · exam-wise index · English + Hinglish</div>""",
    f"""<div class="sun" style="right:-120px;top:380px;width:820px;height:820px"></div>
<div style="position:absolute;left:60px;top:80px;width:560px">
 <div class="k" style="font-size:52px">Launch offer 🎯</div>
 <h1 style="font-size:104px;margin-top:6px">Reasoning<br>Samjho</h1>
 <ul style="font-size:32px;margin-top:30px">
  <li>192 original puzzles</li><li>SSC · Bank · Railway</li><li>CSAT · CAT · Placements</li><li>Shortcuts, traps, 3 mocks</li><li>English + Hinglish · PDF + EPUB</li></ul></div>
<img class="img" src="{COVER}" style="right:60px;top:200px;width:400px;transform:rotate(5deg)">
<div class="m" style="right:420px;top:800px;width:240px;height:240px">{dada("aha")}</div>
<div style="position:absolute;left:60px;bottom:200px"><div class="p"><s>₹299</s>₹275</div>
 <span style="font-family:D;font-size:34px;margin-left:16px">till 30 Nov · dono ₹367</span></div>
<div style="position:absolute;left:60px;bottom:120px;font-size:36px">Buy link 👉 <b style="color:#ffd166">bio + comments mein</b></div>
{FOOT}""",
]

COUNTDOWN = [("launch", "Launch offer 🎯", "<s>₹299</s> ₹275 till 30 Nov"), ("3days", "Sirf 3 din baaki! ⏳", "<s>₹299</s> ₹275 · ends 30 Nov"),
             ("lastday", "Aaj last day! ⏰", "<s>₹299</s> ₹275 · aaj 7 PM tak")]


def jpg(png):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(png), "-q:v", "2", str(png.with_suffix(".jpg"))])


if __name__ == "__main__":
    story_page()
    for i, body in enumerate(SLIDES, 1):
        src = P / f"launch-{i}.html"
        src.write_text(C.slide(i, body), encoding="utf8")
        A.shot(src.as_uri(), C.W, C.H, P / f"launch-{i}.png")
        jpg(P / f"launch-{i}.png")
    for name, kicker, price in COUNTDOWN:
        for fmt, (w, h, _, _) in A.FORMATS.items():
            page = A.html(fmt)
            if fmt == "wide":
                page = page.replace("</style>", "h1{font-size:84px} ul{margin:16px 0;font-size:24px}</style>", 1)
            for a, b in PA.TEASER:
                if a == '<div class="k">New book by Raj</div>':
                    b = f'<div class="k">{kicker}</div>'
                elif a == "<s>₹299</s>₹199 launch offer":
                    b = price
                elif a.startswith("Free preview"):
                    b = 'Buy link: <b>bio + comments mein</b><br><span style="font-size:.72em;opacity:.85">' + NOT_AFF + "</span>"
                page = page.replace(a, b, 1)
            src = P / f"{name}-{fmt}.html"
            src.write_text(page, encoding="utf8")
            A.shot(src.as_uri(), w, h, P / f"{name}-{fmt}.png")
            jpg(P / f"{name}-{fmt}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + sum([["-i", str(P / f"launch-{i}.png")] for i in range(1, 6)], []) +
                   ["-filter_complex", "".join("[%d]scale=360:-1[s%d];" % (i, i) for i in range(5)) + "".join("[s%d]" % i for i in range(5)) + "hstack=5",
                    "-update", "1", str(P / "launch-sheet.png")])
    print("ok")
