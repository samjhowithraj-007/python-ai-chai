"""Python with Chai ad set, 21 Oct - 15 Nov 2026 (same approved designs as ads.py + carousel.py; only the words change).
Run: python adset_nov.py -> out/set/<ad>-{post,story,wide}.jpg, out/set/peek-1..5.jpg, out/set/sheet-*.png
Uses out/page.png from ads.py (already there)."""
import subprocess, sys, pathlib
sys.dont_write_bytecode = True
import ads as A
import carousel as C

SET = A.ADS / "set"

# single ads (ads.py layout): (name, kicker, price line, link line)
SINGLES = [
    ("now",      "Ab available hai! ☕",   "₹199 till 15 Nov",       "Buy + free preview: <b>techsamjhoraj.com/#book</b>"),
    ("diwali",   "Diwali gift idea 🪔",    "₹199 till 15 Nov",       "Khud ko gift karo: <b>techsamjhoraj.com/#book</b>"),
    ("3days",    "Sirf 3 din baaki! ⏳",   "₹199 · ends 15 Nov",     "Buy now: <b>techsamjhoraj.com/#book</b>"),
    ("lastday",  "Aaj last day! ⏰",       "₹199 sirf aaj",          "Buy now: <b>techsamjhoraj.com/#book</b>"),
]

# chapter-peek carousel (carousel.py slides 1-5, words swapped)
PEEK = [
    ("Python boring lagta hai? 😴", "Book ke andar kya hai? 👀"),
    ("Ab seekho<br><em>chai ke saath</em>", "Ek chapter<br><em>andar se dekho</em>"),
    ("NEW<br>BOOK", "PEEK<br>INSIDE"),
    ("Ek cup, ek chapter!", "Swipe karke dekho!"),
    ("₹299</s> ₹199 launch", "₹299</s> ₹199 till 15 Nov"),
    ('<div class="k" style="font-size:52px">New book by Raj</div>', '<div class="k" style="font-size:52px">Pasand aaya? ☕</div>'),
    ('<span style="font-family:D;font-size:36px;margin-left:16px">launch offer</span>',
     '<span style="font-family:D;font-size:36px;margin-left:16px">launch offer · till 15 Nov</span>'),
    ("Free preview 👉 <b", "Buy + free preview 👉 <b"),
]


def jpg(png):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(png), "-q:v", "2", str(png.with_suffix(".jpg"))])


def sheet(pngs, out, w=360):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + sum([["-i", str(p)] for p in pngs], []) +
                   ["-filter_complex", "".join("[%d]scale=%d:-1[s%d];" % (i, w, i) for i in range(len(pngs))) +
                    "".join("[s%d]" % i for i in range(len(pngs))) + "hstack=%d" % len(pngs), "-update", "1", str(out)])


if __name__ == "__main__":
    SET.mkdir(parents=True, exist_ok=True)
    for name, kicker, price, link in SINGLES:
        for fmt, (w, h, _, _) in A.FORMATS.items():
            page = (A.html(fmt)
                    .replace('<div class="k">New book by Raj</div>', f'<div class="k">{kicker}</div>')
                    .replace("₹199 launch offer", price)
                    .replace("Free preview: <b>techsamjhoraj.com/#book</b>", link))
            src = SET / f"{name}-{fmt}.html"
            src.write_text(page, encoding="utf8")
            png = SET / f"{name}-{fmt}.png"
            A.shot(src.as_uri(), w, h, png)
            jpg(png)
    for i, body in enumerate(C.SLIDES, 1):
        for a, b in PEEK:
            body = body.replace(a, b)
        src = SET / f"peek-{i}.html"
        src.write_text(C.slide(i, body), encoding="utf8")
        png = SET / f"peek-{i}.png"
        A.shot(src.as_uri(), C.W, C.H, png)
        jpg(png)
    sheet([SET / f"peek-{i}.png" for i in range(1, 6)], SET / "sheet-peek.png")
    sheet([SET / f"{n}-post.png" for n, *_ in SINGLES], SET / "sheet-posts.png")
    sheet([SET / f"{n}-story.png" for n, *_ in SINGLES], SET / "sheet-stories.png", 270)
    print("ok", SET)
