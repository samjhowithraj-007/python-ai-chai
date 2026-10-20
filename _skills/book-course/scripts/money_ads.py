"""Ads for the money templates (Family Money Planner ₹199, Budget + EMI + Goals Tracker ₹149): the approved ads.py layout,
words + images swapped, Chotu swapped for Gullak Bhai (money mascot, with a white sticker outline on the dark background).
Every ad carries "Financial education, advice nahi" and promises no returns. No discount code (full price).
Run: python money_ads.py -> out/money/<product>-{post,story,wide}.jpg + out/money/sheet.png"""
import subprocess, sys, pathlib
sys.dont_write_bytecode = True
import ads as A
sys.path.insert(0, "C:/samjhowithraj/brand/mascots/gullak-bhai")
from gullak import gullak

M = A.ADS / "money"
TPL = pathlib.Path("C:/samjhowithraj/financial planning/money-book/templates/out")
STICKER = ".p{transform:translateY(-34px)} li:before{content:\"\\1F4B0  \"} .m svg{filter:drop-shadow(3px 0 0 #fff) drop-shadow(-3px 0 0 #fff) drop-shadow(0 3px 0 #fff) drop-shadow(0 -3px 0 #fff)}"
NOTE = '<br><span style="font-size:.75em;opacity:.85">Financial education, advice nahi · Verma family is fictional</span>'

PRODUCTS = [
    dict(slug="family-money-planner", pose="point",
         kicker="Family ke liye 🏠", title="Money<br>Planner",
         sub="Google Sheet + Excel · har rupaye ko kaam",
         items=["3 jars: essentials, yearly + fun, future", "Emergency-fund target + net worth", "Verma example + blank tab for you"],
         price="Sirf ₹199", peek="budget-emi-goals-tracker-thumb.png"),
    dict(slug="budget-emi-goals-tracker", pose="think",
         kicker="Salary kahan gayi? 🤔", title="Budget + EMI<br>Tracker",
         sub="Google Sheet + Excel · plan vs actual",
         items=["12-month budget: plan vs actual", "Up to 5 loans: EMI, interest, schedule", "8 goals + monthly saving for each"],
         price="Sirf ₹149", peek="family-money-planner-thumb.png"),
]


def jpg(png):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(png), "-q:v", "2", str(png.with_suffix(".jpg"))])


if __name__ == "__main__":
    M.mkdir(parents=True, exist_ok=True)
    for p in PRODUCTS:
        lst = "<ul>" + "".join(f"<li>{i}</li>" for i in p["items"]) + "</ul>"
        swaps = [
            ('<div class="k">New book by Raj</div>', f'<div class="k">{p["kicker"]}</div>'),
            ("Python<br>with Chai", p["title"]),
            ("From Basic to Expert · 30 illustrated chapters", p["sub"]),
            (A.LIST, lst),
            ("<s>₹299</s>₹199 launch offer", p["price"]),
            ("Free preview: <b>techsamjhoraj.com/#book</b>", "Buy link: <b>bio + comments mein</b>" + NOTE),
            ((A.OUT / "cover-en.png").as_uri(), (TPL / f"{p['slug']}-cover.png").as_uri()),
            ((A.ADS / "page.png").as_uri(), (TPL / p["peek"]).as_uri()),
            (A.chotu("party", ""), gullak(p["pose"], "")),
            ("</style>", STICKER + "</style>"),
        ]
        for fmt, (w, h, _, _) in A.FORMATS.items():
            page = A.html(fmt)
            if fmt == "wide":  # the 3-line list + note need a little more room than the book ad
                page = page.replace("</style>", "h1{font-size:84px} ul{margin:16px 0;font-size:24px}</style>", 1)
            for a, b in swaps:
                assert a in page or fmt == "wide" and a == (A.ADS / "page.png").as_uri(), (fmt, a[:40])
                page = page.replace(a, b, 1)
            src = M / f"{p['slug']}-{fmt}.html"
            src.write_text(page, encoding="utf8")
            A.shot(src.as_uri(), w, h, M / f"{p['slug']}-{fmt}.png")
            jpg(M / f"{p['slug']}-{fmt}.png")
    files = [M / f"{p['slug']}-{f}.png" for p in PRODUCTS for f in ("post", "story")]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + sum([["-i", str(f)] for f in files], []) +
                   ["-filter_complex", "".join("[%d]scale=-1:640[s%d];" % (i, i) for i in range(len(files))) +
                    "".join("[s%d]" % i for i in range(len(files))) + "hstack=%d" % len(files), "-update", "1", str(M / "sheet.png")])
    print("ok", M)
