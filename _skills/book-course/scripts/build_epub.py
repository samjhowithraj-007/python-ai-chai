"""Reflowable EPUB 3 of "Python with Chai" (English + Hinglish) for e-readers (Kindle via Send-to-Kindle, Kobo, Apple Books, Google Play Books).
Built from the finished book HTML in python-chai-book/out (READ ONLY), so text, code and real outputs match the PDF exactly.
Run: python build_epub.py   -> out/python-with-chai-{en,hi}.epub   (this folder is git-ignored: paid content)
Dropped for e-readers: the contents pages (the reader's own TOC replaces them), the index (page numbers don't exist in
reflowable text; readers have search), page footers and the per-page Chotu bubbles. Kept: everything else."""
import re, zipfile, uuid, datetime, pathlib, subprocess, html, glob, os, sys
from xml.dom import minidom

BOOK = pathlib.Path("C:/samjhowithraj/vlog1/videos/python-chai-book")
HERE = pathlib.Path(__file__).parent.resolve()
OUT = HERE / "out"
CHROME = glob.glob(os.path.expanduser("~/.cache/hyperframes/chrome/chrome-headless-shell/*/chrome-headless-shell-win64/chrome-headless-shell.exe"))[0]
FONTS = {"DMSans-400.woff2": "Body", "DMSans-700.woff2": "Body", "Caveat-700.woff2": "Hand", "JetBrainsMono-400.woff2": "Mono"}
META = {
    "en": dict(title="Python with Chai: From Basic to Expert", lang="en", ed="English edition",
               answers="Answers", front="Start here", about="About the author", ch="Chapter"),
    "hi": dict(title="Python with Chai: Basic se Expert tak", lang="hi-Latn", ed="Hinglish edition",
               answers="Answers", front="Shuru karein", about="Author ke baare mein", ch="Chapter"),
}
LEVEL = {"basic": "Basic", "inter": "Intermediate", "expert": "Expert"}

CSS = """@font-face{font-family:"Body";src:url(fonts/DMSans-400.woff2)}
@font-face{font-family:"Body";font-weight:bold;src:url(fonts/DMSans-700.woff2)}
@font-face{font-family:"Hand";src:url(fonts/Caveat-700.woff2)}
@font-face{font-family:"Mono";src:url(fonts/JetBrainsMono-400.woff2)}
body{font-family:"Body",sans-serif;line-height:1.5;margin:0 4%}
h1,h2{font-family:"Hand",cursive;color:#b8322a;line-height:1.1;margin:1.2em 0 .4em}
h1{font-size:2.2em} h2{font-size:1.7em} h3{color:#22356b;margin:1em 0 .3em} h4{margin:.9em 0 .3em;color:#22356b}
.pn{display:block;font-size:.75em;letter-spacing:.06em;text-transform:uppercase;color:#b8322a;margin-top:1.6em}
.chapter-open{text-align:center;page-break-before:always}
.chapter-open img{width:30%;max-width:9em;margin:.5em auto}
.big{font-family:"Hand",cursive;font-size:1.4em;color:#22356b}
.bubble{font-style:italic;margin:.3em 0 1em}
.chapter-open ul{text-align:left;display:inline-block;margin:0 auto}
.lvl{display:inline-block;border:1px solid #2b2a33;border-radius:1em;padding:0 .8em;font-family:"Hand",cursive;background:#ffe9a8}
.page{page-break-before:always}
pre{font-family:"Mono",monospace;font-size:.82em;white-space:pre-wrap;word-wrap:break-word;margin:.2em 0;line-height:1.4}
.card,.outc{border:1px solid #2b2a33;border-radius:.4em;padding:.5em .7em;margin:.6em 0;page-break-inside:avoid}
.card{background:#fffdf6} .outc{background:#1f2230;color:#e8f3d8}
.tab{display:inline-block;font-family:"Mono",monospace;font-size:.7em;background:#ffd166;color:#2b2a33;padding:0 .5em;border-radius:.3em;margin-bottom:.3em}
.outc .tab{background:#7ad6a0}
b.kw{color:#7b2fbf;font-weight:bold} i.st{color:#2e7d32;font-style:normal} i.cm{color:#8a8a8a} .num{color:#c2185b}
.explain,.whatif,.tip,.sticky,.idea,.next,.chal,.cheat,.labels,.walk-wrap{border-radius:.4em;padding:.5em .7em;margin:.7em 0}
.explain{border:1px dashed #5b7fd1;background:#eef3ff}
.whatif{border:1px dashed #2e9b5a;background:#eefaf1}
.tip,.sticky{background:#fff3b0;border-left:4px solid #e0a800}
.cheat{background:#f3ecff;border:1px solid #7b2fbf}
.chal,.next{background:#fff0e6;border:1px solid #ff7a2f}
.errline{font-family:"Mono",monospace;font-size:.78em;color:#b8322a;margin:.2em 0 .5em}
.x{color:#b8322a;font-weight:bold} .ok{color:#2e7d32;font-weight:bold}
.mist{border-top:1px solid #ddd;padding-top:.3em}
table.walk{border-collapse:collapse;width:100%;font-size:.9em} table.walk td{border-bottom:1px solid #ddd;padding:.3em;vertical-align:top}
table.walk code{font-family:"Mono",monospace;font-size:.9em}
code{font-family:"Mono",monospace;font-size:.9em;background:#fff3c4;padding:0 .15em}
.story{font-size:1.05em}
ul,ol{padding-left:1.3em} li{margin:.2em 0}
.ansblock{page-break-inside:auto} .ans h4{color:#b8322a}
.front{text-align:left} .titlep{text-align:center} .titlep img,.front img{width:25%;max-width:7em;border-radius:50%}
.cover{text-align:center;margin:0;padding:0} .cover img{max-width:100%;max-height:100%}"""


def pages(lang):
    s = (BOOK / "out" / ("python-with-chai-%s-full.html" % lang)).read_text(encoding="utf8")
    return [(c.strip(), h) for c, h in re.findall(r'<section class="page([^"]*)"[^>]*>(.*?)</section>', s, re.S)]


def inner(h):
    """The page's readable content: drop the mascot bubble/SVG and footer, unwrap .content."""
    h = re.split(r'<div class="say">|<svg class="chotu|<div class="foot">', h)[0]
    h = re.sub(r'^\s*<div class="content[^"]*">', "", h)
    h = re.sub(r"</div>\s*$", "", h)
    return h


def xhtml_fix(h):
    h = re.sub(r"<svg.*?</svg>", "", h, flags=re.S)                      # inline SVG art: not all readers cope
    h = re.sub(r'<img [^>]*src="[^"]*raj-mark\.png"[^>]*>', '<img src="img/raj-mark.png" alt="Raj"/>', h)
    h = re.sub(r"<(br|hr)\s*>", r"<\1/>", h)
    h = h.replace("&nbsp;", "&#160;")
    h = re.sub(r"&(?!#?\w+;)", "&amp;", h)
    h = re.sub(r"<(?![A-Za-z/!?])", "&lt;", h)                          # text like <__main__.Cup object> (HTML shows it as text)
    h = re.sub(r' style="[^"]*"', "", h)                                    # print layout styles
    return h


def doc(title, body, lang):
    return ('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" '
            'xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="%s" lang="%s"><head><meta charset="utf-8"/><title>%s</title>'
            '<link rel="stylesheet" type="text/css" href="style.css"/></head><body>%s</body></html>') % (lang, lang, html.escape(title), body)


def chapter_meta(first_page_html):
    t = re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", first_page_html)).strip()
    m = re.match(r"(Basic|Intermediate|Expert) Chapter (\d+) (.*?) ", t)
    return m


def build(lang, chotu_png):
    M = META[lang]; P = pages(lang)
    assert len(P) == 336, len(P)
    files = []  # (id, filename, title, xhtml)
    # cover + front matter (title, copyright, how to use)
    files.append(("cover", "cover.xhtml", "Cover", doc("Cover", '<div class="cover"><img src="img/cover.jpg" alt="%s"/></div>' % M["title"], M["lang"])))
    front = "".join('<div class="page">%s</div>' % xhtml_fix(inner(P[i][1])) for i in (1, 2, 3))
    files.append(("front", "front.xhtml", M["front"], doc(M["front"], front, M["lang"])))
    # 30 chapters, 10 pages each (pages 6..305)
    for n in range(1, 31):
        ps = P[6 + (n - 1) * 10: 6 + n * 10]
        first = xhtml_fix(inner(ps[0][1]))
        title = re.search(r"<h1[^>]*>(.*?)</h1>", first, re.S)
        ttl = re.sub("<[^>]+>", "", title.group(1)).strip() if title else "%s %d" % (M["ch"], n)
        body = ('<div class="chapter-open"><img src="img/chotu.png" alt=""/>%s</div>' % first) + "".join(
            '<div class="page">%s</div>' % xhtml_fix(inner(h)) for _, h in ps[1:])
        files.append(("ch%02d" % n, "ch%02d.xhtml" % n, "%d. %s" % (n, html.unescape(ttl)), doc(ttl, body, M["lang"])))
    # answers (306..327), about the author (334)
    ans = "".join('<div class="page">%s</div>' % xhtml_fix(inner(P[i][1])) for i in range(306, 328))
    files.append(("answers", "answers.xhtml", M["answers"], doc(M["answers"], ans, M["lang"])))
    files.append(("about", "about.xhtml", M["about"], doc(M["about"], xhtml_fix(inner(P[334][1])), M["lang"])))
    for _, fn, _, x in files:  # every page must be well-formed XML
        minidom.parseString(x.encode("utf8"))

    nav = doc("Contents", '<nav epub:type="toc" id="toc"><h1>Contents</h1><ol>%s</ol></nav>' % "".join(
        '<li><a href="%s">%s</a></li>' % (fn, html.escape(t)) for i, fn, t, _ in files if i != "cover"), M["lang"])
    minidom.parseString(nav.encode("utf8"))
    uid = "urn:uuid:%s" % uuid.uuid5(uuid.NAMESPACE_URL, "techsamjhoraj.com/book/python-with-chai/" + lang)
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    imgs = {"img/cover.jpg": "image/jpeg", "img/chotu.png": "image/png", "img/raj-mark.png": "image/png"}
    manifest = ['<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
                '<item id="css" href="style.css" media-type="text/css"/>',
                '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>']
    manifest += ['<item id="%s" href="%s" media-type="application/xhtml+xml"/>' % (i, fn) for i, fn, _, _ in files]
    manifest += ['<item id="img%d" href="%s" media-type="%s"%s/>' % (k, p, t, ' properties="cover-image"' if "cover" in p else "")
                 for k, (p, t) in enumerate(imgs.items())]
    manifest += ['<item id="font%d" href="fonts/%s" media-type="font/woff2"/>' % (k, f) for k, f in enumerate(FONTS)]
    opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="{M['lang']}">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bookid">{uid}</dc:identifier><dc:title>{html.escape(M['title'])}</dc:title>
<dc:creator>Raj</dc:creator><dc:publisher>Tech Samjho Raj</dc:publisher><dc:language>{M['lang']}</dc:language>
<dc:rights>© 2026 Raj (Tech Samjho Raj). All rights reserved.</dc:rights>
<dc:description>{M['ed']}: 30 illustrated chapters from print() to asyncio. Every output really run.</dc:description>
<meta property="dcterms:modified">{now}</meta><meta name="cover" content="img0"/>
</metadata>
<manifest>{''.join(manifest)}</manifest>
<spine toc="ncx">{''.join('<itemref idref="%s"/>' % i for i, _, _, _ in files[:1])}<itemref idref="nav"/>{''.join('<itemref idref="%s"/>' % i for i, _, _, _ in files[1:])}</spine>
<guide><reference type="cover" title="Cover" href="cover.xhtml"/></guide>
</package>"""
    ncx = ('<?xml version="1.0" encoding="utf-8"?><ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1"><head>'
           '<meta name="dtb:uid" content="%s"/></head><docTitle><text>%s</text></docTitle><navMap>%s</navMap></ncx>') % (
        uid, html.escape(M["title"]), "".join('<navPoint id="n%d" playOrder="%d"><navLabel><text>%s</text></navLabel><content src="%s"/></navPoint>'
                                              % (k, k + 1, html.escape(t), fn) for k, (_, fn, t, _) in enumerate(files)))
    minidom.parseString(opf.encode("utf8")); minidom.parseString(ncx.encode("utf8"))

    # cover image (JPEG, 1600px tall)
    cover = OUT / ("cover-%s.jpg" % lang)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(BOOK / "out" / ("cover-%s.png" % lang)), "-vf", "scale=-2:1600", "-q:v", "3", str(cover)], check=True)
    path = OUT / ("python-with-chai-%s.epub" % lang)
    with zipfile.ZipFile(path, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", compress_type=zipfile.ZIP_STORED)  # must be first + uncompressed
        z.writestr("META-INF/container.xml", '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
                   '<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>', zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/content.opf", opf, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/toc.ncx", ncx, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", CSS, zipfile.ZIP_DEFLATED)
        for _, fn, _, x in files:
            z.writestr("OEBPS/" + fn, x, zipfile.ZIP_DEFLATED)
        z.write(cover, "OEBPS/img/cover.jpg"); z.write(chotu_png, "OEBPS/img/chotu.png")
        z.write(BOOK / "img" / "raj-mark.png", "OEBPS/img/raj-mark.png")
        for f in FONTS:
            z.write(BOOK / "fonts" / f, "OEBPS/fonts/" + f)
    return path, len(files)


def chotu_png():
    sys.path.insert(0, str(BOOK)); sys.dont_write_bytecode = True
    from mascot import chotu
    h = OUT / "chotu.html"
    h.write_text('<!doctype html><style>html,body{margin:0;background:transparent}svg{width:400px;height:400px}</style>' + chotu("wave", ""), encoding="utf8")
    png = OUT / "chotu.png"
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars", "--default-background-color=00000000",
                    "--window-size=400,400", "--screenshot=" + str(png), h.as_uri()], capture_output=True)
    return png


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    c = chotu_png()
    for lang in ("en", "hi"):
        p, n = build(lang, c)
        print(lang, p.name, "%.1f MB" % (p.stat().st_size / 1e6), n, "files")
