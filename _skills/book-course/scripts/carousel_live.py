"""'Now available' version of the 5-slide carousel (same design as carousel.py, launch-live wording).
Run: python carousel_live.py -> out/live-1..5.jpg + out/live-sheet.png"""
import subprocess, sys
sys.dont_write_bytecode = True
import carousel as C

SWAPS = [
    ("NEW<br>BOOK", "OUT<br>NOW!"),
    ("₹299</s> ₹199 launch", "₹299</s> ₹199 till 15 Nov"),
    ('<div class="k" style="font-size:52px">New book by Raj</div>', '<div class="k" style="font-size:52px">Ab available hai! ☕</div>'),
    ('<span style="font-family:D;font-size:36px;margin-left:16px">launch offer</span>',
     '<span style="font-family:D;font-size:36px;margin-left:16px">launch offer · till 15 Nov</span>'),
    ("Free preview 👉 <b", "Buy + free preview 👉 <b"),
]

if __name__ == "__main__":
    for i, body in enumerate(C.SLIDES, 1):
        for a, b in SWAPS:
            body = body.replace(a, b)
        h = C.ADS / ("live-%d.html" % i)
        h.write_text(C.slide(i, body), encoding="utf8")
        png = C.ADS / ("live-%d.png" % i)
        subprocess.run([C.CHROME, "--headless", "--disable-gpu", "--allow-file-access-from-files", "--virtual-time-budget=6000",
                        "--hide-scrollbars", "--window-size=%d,%d" % (C.W, C.H), "--screenshot=" + str(png), h.as_uri()], capture_output=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(png), "-q:v", "2", str(png.with_suffix(".jpg"))])
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + sum([["-i", str(C.ADS / ("live-%d.png" % i))] for i in range(1, 6)], []) +
                   ["-filter_complex", "".join("[%d]scale=360:-1[s%d];" % (i, i) for i in range(5)) + "".join("[s%d]" % i for i in range(5)) + "hstack=5",
                    "-update", "1", str(C.ADS / "live-sheet.png")])
    print("ok")
