"""Archive Tech Explainer 01 into one timestamped zip (Money Plan layout) + CONTENTS.txt, then verify it.
Keeps what can't be rebuilt; leaves out render scratch (renders/, public/, short*/public, snaps*, review/, reel/, sample60/).
Usage: python archive-part.py   -> C:\\Users\\rajpr\\Videos\\_archive-staging\\tech-explainer-01-<stamp>.zip
"""
import os, zipfile, datetime, hashlib

P = r"C:\samjhowithraj\vlog1\videos\tech-explainer-01"
R = r"C:\Users\rajpr\Videos\YouTube Renders\tech-explainer-01"
OUT = r"C:\Users\rajpr\Videos\_archive-staging"
stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
os.makedirs(OUT, exist_ok=True)
zpath = os.path.join(OUT, f"tech-explainer-01-{stamp}.zip")

groups = [
    ("1-raw-recordings", [os.path.join(P, "raw")]),
    ("2-ai-clips", [os.path.join(P, "broll")]),
    ("3-assets-pexels-rohan", [os.path.join(P, "assets"), os.path.join(P, "thumbnail")]),
    ("4-animations-src", [os.path.join(P, "anim")]),
    ("5-source-captures", [os.path.join(P, "sources")]),
    ("6-final-posted", [R]),
]
SKIP_DIRS = {"old", "node_modules", ".hyperframes", "snaps", "public", "renders", "_parts"}
SKIP_EXT = {".wav"}
files = []
for top, roots in groups:
    for root in roots:
        for d, dirs, fs in os.walk(root):
            dirs[:] = [x for x in dirs if x not in SKIP_DIRS and not x.startswith("snaps")]
            for f in fs:
                src = os.path.join(d, f)
                if os.path.splitext(f)[1].lower() in SKIP_EXT and top != "1-raw-recordings":
                    continue
                files.append((src, os.path.join(top, os.path.basename(root), os.path.relpath(src, root))))
# project code + notes (small text files at the top level and in short/, shortB/)
for d in (P, os.path.join(P, "short"), os.path.join(P, "shortB")):
    for f in os.listdir(d):
        src = os.path.join(d, f)
        if os.path.isfile(src) and os.path.splitext(f)[1].lower() in {".py", ".sh", ".md", ".json", ".css", ".txt", ".log"}:
            files.append((src, os.path.join("7-project-code", os.path.relpath(src, P))))

STORE = {".mp4", ".mov", ".m4a", ".mp3", ".jpg", ".jpeg", ".png", ".webm", ".zip", ".woff2"}
lines = []
with zipfile.ZipFile(zpath, "w", allowZip64=True) as z:
    for src, arc in files:
        ext = os.path.splitext(src)[1].lower()
        z.write(src, arc, compress_type=zipfile.ZIP_STORED if ext in STORE else zipfile.ZIP_DEFLATED)
        lines.append(f"{arc}\t{os.path.getsize(src)}")
head = ("Tech Explainer 01 archive (" + datetime.date.today().isoformat() + "). AI se naukri jayegi ya milegi?\n"
        "Published: YouTube https://youtu.be/LvB_jh7vtmk · Short https://youtube.com/shorts/YjdYGu3qXTc\n"
        "Instagram https://www.instagram.com/samjhowithraj/reel/Deo5kC_ydNb/ · Facebook reel https://www.facebook.com/reel/1398172522306717/\n"
        "X https://x.com/samjhowithraj/status/2111829007557689656 · Playlist: AI Explained in Hindi 🤖\n"
        "Rebuild: 7-project-code (handcut.py → apply_chunked.py → build.py → finish2.sh → clean-audio.py → finish-final.sh; Short: build-mpshort.py A → finish-shortA.sh).\n"
        "Skill copy: samjhowithraj-007/python-ai-chai (videos/_skills/youtube-edit).\n\n")
open(os.path.join(OUT, "CONTENTS.txt"), "w", encoding="utf-8").write(head + "\n".join(lines) + "\n")

# verify: every member readable with a matching CRC, and the count matches
with zipfile.ZipFile(zpath) as z:
    bad = z.testzip()
    n = len(z.infolist())
total = sum(os.path.getsize(s) for s, _ in files)
print(f"zip {zpath}\nfiles {n} (expected {len(files)}), bad member: {bad}\nsource {total/1e9:.2f} GB, zip {os.path.getsize(zpath)/1e9:.2f} GB")
