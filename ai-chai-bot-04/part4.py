
# ======== Part 4: "MENU" ya "menu"? .lower() + .strip() ========
import sys, json as _json
PLATFORM = sys.argv[1] if len(sys.argv) > 1 else "yt"
BTN, BTN_BG = ("Subscribe", "#FF0000") if PLATFORM == "yt" else ("Follow", "#0095F6")
GREEN = "#7CE38B"

T = {
    "hook": dict(len=4.2, b=[0.9, 1.3, 1.7], no=2.2, sub=3.0),
    "prob": dict(len=8.0, chips=[0.8, 1.8, 2.6, 3.4], count=4.6, stamp=6.0),
    "idea": dict(len=8.0, rows=[1.0, 2.6, 4.8], lab=[1.6, 3.2, 5.4]),
    "code": dict(len=10.0, term=2.2, q=[2.8, 4.6, 6.4], tip=5.6, stamp=8.4),
    "cta": dict(len=12.0, pill=0.7, web=4.5, teaser=6.5, sb=9.0, btn=9.4),
}
if os.path.exists(os.path.join(HERE, "timing.json")):
    T.update(_json.load(open(os.path.join(HERE, "timing.json")))["T"])   # re-timed to Raj's voice

SP = '<span style="color:rgba(255,143,163,.9)">·</span>'   # a visible space dot


# ---- Frame 1: hook ----
f = "01-hook"; t = T["hook"]
asks = ["MENU", "Menu", f"{SP}menu{SP}"]
bubs = "".join(f'<div id="{f}-b{i}" style="position:absolute;right:{90 + i * 40}px;top:{400 + i * 110}px;padding:14px 30px;border-radius:26px 26px 6px 26px;'
               f'background:{CREAM};color:{INK};{MONO};font-size:40px;font-weight:700;white-space:pre">{a}</div>' for i, a in enumerate(asks))
body = f"""    {rose_style(f)}
    <div class="{f}-kick" id="{f}-kick" style="top:90px">AI + PYTHON · PART 4</div>
    <div class="{f}-h" id="{f}-t1" style="top:160px;font-size:100px">{words(f, '"MENU" ya "menu"?')}</div>
    {bubs}
    <div id="{f}-no" class="{f}-r" style="position:absolute;left:90px;top:520px;padding:14px 30px;border-radius:26px 26px 26px 6px;background:{NAVY};
         border:3px solid {ROSE};font-size:44px;font-weight:700;white-space:nowrap">Bot: Samjha nahi! 😵</div>
    <div class="{f}-h {f}-c" id="{f}-sub" style="top:770px;left:60px;right:auto;text-align:left;font-size:70px;{MONO}">.lower() se!</div>"""
js = [f'  tl.fromTo("#{f}-kick", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, 0.05);',
      rise(f"#{f}-t1 .{f}-w", 0.2, 0.1)]
js += [pop(f"#{f}-b{i}", tt, 0.3) for i, tt in enumerate(t["b"])]
js += [pop(f"#{f}-no", t["no"], 0.35), fade_up(f"#{f}-sub", t["sub"], 0.45, 30)]
write(f, t["len"], body, js)

# ---- Frame 2: the problem: Python sees four different words ----
f = "02-problem"; t = T["prob"]
cases = [("menu", True), ("MENU", False), ("Menu", False), (f"{SP}menu{SP}", False)]
chips = ""
for i, (w, ok) in enumerate(cases):
    col = GREEN if ok else ROSE
    mark = "✓ match" if ok else "✗ alag"
    chips += (f'<div id="{f}-c{i}" style="position:absolute;left:150px;top:{200 + i * 104}px;width:780px;height:84px;border-radius:14px;background:{NAVY};'
              f'border:2px solid {col};display:flex;align-items:center;justify-content:space-between;padding:0 28px;box-sizing:border-box;white-space:pre">'
              f'<span style="{MONO};font-size:38px">msg == <span style="color:{AMBER}">"{w}"</span></span>'
              f'<span style="font-size:34px;font-weight:700;color:{col}">{mark}</span></div>')
body = f"""    {rose_style(f)}
    <div class="{f}-h" id="{f}-head" style="top:76px;font-size:78px">{words(f, "Python ke liye sab alag!", {4: f + "-r"})}</div>
    {chips}
    <div id="{f}-count" style="position:absolute;left:150px;top:640px;font-size:56px;font-weight:700;white-space:nowrap">Insaan ke liye ek hi sawaal 🤷</div>
    <div id="{f}-stamp" class="{f}-r" style="position:absolute;left:180px;top:760px;padding:12px 28px;border:5px solid {ROSE};border-radius:16px;
         background:rgba(14,17,22,.92);font-size:44px;font-weight:700;white-space:nowrap;transform:rotate(-4deg)">Capital ya space = Samjha nahi!</div>"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.08)]
js += [pop(f"#{f}-c{i}", tt, 0.3) for i, tt in enumerate(t["chips"])]
js += [fade_up(f"#{f}-count", t["count"], 0.4, 30),
       f'  tl.fromTo("#{f}-stamp", {{ opacity: 0, scale: 1.6, rotation: -4 }}, {{ opacity: 1, scale: 1, rotation: -4, duration: 0.35, ease: "power4.in" }}, {t["stamp"]});']
write(f, t["len"], body, js)

# ---- Frame 3: the cleaning step ----
f = "03-clean"; t = T["idea"]
rows_ = [('"MENU"', ".lower()"), ('"Menu"', ".lower()"), (f'"{SP}{SP}menu{SP}{SP}"', ".strip()")]
rows = "".join(f'<div id="{f}-r{i}" style="position:absolute;left:70px;top:{230 + i * 150}px;width:940px;height:120px;display:flex;align-items:center;gap:24px;white-space:pre">'
               f'<span style="{MONO};font-size:44px;color:{AMBER};width:330px;text-align:right">{a}</span>'
               f'<span id="{f}-m{i}" style="{MONO};font-size:38px;color:{INK};background:{CYAN};padding:10px 22px;border-radius:14px;font-weight:700">{m}</span>'
               f'<span style="font-size:44px;color:{CREAM}">→</span>'
               f'<span style="{MONO};font-size:44px;color:{GREEN};font-weight:700">"menu" ✓</span></div>' for i, (a, m) in enumerate(rows_))
body = f"""    <div class="{f}-h" id="{f}-head" style="top:76px;font-size:76px">{words(f, "Pehle saaf karo, phir dhundo", {1: f + "-c", 4: f + "-a"})}</div>
    {rows}
    <div id="{f}-lab" style="position:absolute;left:0;right:0;top:700px;text-align:center;font-size:40px;line-height:1.5;white-space:nowrap">
      <span style="{MONO};color:{CYAN}">.lower()</span> = sab chhota &nbsp;·&nbsp; <span style="{MONO};color:{CYAN}">.strip()</span> = extra space hatao</div>"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.08)]
for i, tt in enumerate(t["rows"]):
    js.append(f'  tl.fromTo("#{f}-r{i}", {{ opacity: 0, x: -40 }}, {{ opacity: 1, x: 0, duration: 0.45, ease: "power3.out" }}, {tt:.2f});')
    js.append(pop(f"#{f}-m{i}", t["lab"][i], 0.3))
js.append(fade_up(f"#{f}-lab", t["rows"][2] + 1.4, 0.45, 20))
write(f, t["len"], body, js)

# ---- Frame 4: the code + terminal demo ----
f = "04-code"; t = T["code"]
LH = 32 * 1.6
CT = 170
lines = [f'replies = {{<span class="{f}-s">"menu"</span>: <span class="{f}-s">"Masala, Adrak!"</span>,',
         f'           <span class="{f}-s">"price"</span>: <span class="{f}-s">"Rs 20"</span>}}',
         f'msg = <span class="{f}-k">input</span>(<span class="{f}-s">"Aap: "</span>).<span class="{f}-k">lower</span>().<span class="{f}-k">strip</span>()',
         f'<span class="{f}-k">print</span>(replies.<span class="{f}-k">get</span>(msg, <span class="{f}-s">"Samjha nahi!"</span>))']
cardh, ns = card(f, lines, f"left:40px;top:{CT}px;width:1000px;height:312px;font-size:32px", fname="chai_bot.py · while True ke andar")
y = lambda i: int(CT + 64 + i * LH - 4)
row = lambda rid, txt, col: f'<div id="{f}-{rid}" style="font-size:36px;line-height:1.4;color:{col};white-space:pre">{txt}</div>'
demo = [("MENU", "Masala, Adrak!"), ("  Price ", "Rs 20"), ("Menu", "Masala, Adrak!")]
inner = "".join(row(f"q{k}", f'Aap: {typed(f, f"u{k}", q, CYAN)}', CREAM) + row(f"o{k}", f"Bot: {a}", AMBER)
                for k, (q, a) in enumerate(demo))
body = f"""    <div class="{f}-h" id="{f}-head" style="top:66px;font-size:80px">{words(f, "Ek line, sab theek", {1: f + "-c", 3: f + "-a"})}</div>
{cardh}
    <div id="{f}-hl" style="position:absolute;left:42px;top:{y(2)}px;width:996px;height:{int(LH)}px;background:rgba(10,240,240,.14);border-left:6px solid {CYAN};opacity:0"></div>
    {terminal(f, inner, 40, 500, 1000, 380)}
    <div id="{f}-tip" style="position:absolute;left:560px;top:545px;width:440px;padding:12px 20px;border-radius:14px;background:rgba(10,240,240,.1);
         border:2px solid {CYAN};box-sizing:border-box;font-size:30px;line-height:1.35"><span style="{MONO};color:{CYAN}">.lower().strip()</span><br>chain karo, ek saath!</div>
    <div id="{f}-stamp" style="position:absolute;left:560px;top:655px;padding:10px 24px;border:5px solid {GREEN};border-radius:16px;color:{GREEN};
         background:rgba(14,17,22,.92);font-size:40px;font-weight:700;white-space:nowrap;transform:rotate(-5deg)">Ab bot samajhdaar!</div>"""
js = [rise(f"#{f}-head .{f}-w", 0.05, 0.08), fade_up(f"#{f}-card", 0.2, 0.6, 60)]
for i in range(4):
    js.append(type_line(f, i, ns[i], 0.4 + i * 0.3, 0.4))
js += [fade_up(f"#{f}-term", t["term"], 0.5), f'  tl.fromTo("#{f}-hl", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, {t["term"] + 0.3:.2f});']
for k, ((q, a), t0) in enumerate(zip(demo, t["q"])):
    js.append(f'  tl.fromTo("#{f}-q{k}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15 }}, {t0:.2f});')
    js += type_user(f, f"u{k}", len(q), t0 + 0.3, 0.45)
    js.append(f'  tl.fromTo("#{f}-o{k}", {{ opacity: 0, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }}, {t0 + 1.15:.2f});')
js += [fade_up(f"#{f}-tip", t["tip"], 0.45, 20),
       f'  tl.fromTo("#{f}-stamp", {{ opacity: 0, scale: 1.6, rotation: -5 }}, {{ opacity: 1, scale: 1, rotation: -5, duration: 0.35, ease: "power4.in" }}, {t["stamp"]});']
write(f, t["len"], body, js)

# ---- Frame 5: payoff + Part 5 teaser + website + channel bar ----
f = "05-cta"; t = T["cta"]
body = f"""    <div class="{f}-h" id="{f}-l1" style="top:90px;font-size:76px"><span class="{f}-w {f}-c" style="{MONO}">.lower()</span> <span class="{f}-w">= bot ke kaan</span> <span class="{f}-w {f}-a">saaf!</span></div>
    <div id="{f}-pill" style="position:absolute;left:50%;transform:translateX(-50%);top:200px;padding:10px 28px;border-radius:9999px;border:3px solid {GREEN};
         color:{GREEN};{MONO};font-weight:700;font-size:34px;white-space:nowrap">✓ PART 4 / 50</div>
    <div id="{f}-teaser" style="position:absolute;left:90px;top:290px;width:900px;height:180px;border-radius:20px;background:{NAVY};border:2px solid rgba(10,240,240,.5);
         box-sizing:border-box;padding:24px 44px;box-shadow:0 24px 70px rgba(0,0,0,.5)">
      <div style="{MONO};font-weight:700;font-size:30px;letter-spacing:.16em;color:rgba(245,241,232,.66)">AGLA PART 5</div>
      <div style="font-size:50px;margin-top:20px;white-space:nowrap">Poora sentence samjho: <span class="{f}-c" style="{MONO}">in</span></div>
    </div>
    <div id="{f}-web" style="position:absolute;left:0;right:0;top:500px;text-align:center;font-size:40px;font-weight:700;white-space:nowrap">
      Free notes + code: <span class="{f}-c" style="{MONO}">samjhowithraj.online</span></div>
    <div id="{f}-sb" style="position:absolute;left:40px;top:575px;height:132px;padding:0 22px 0 18px;border-radius:9999px;
         background:rgba(255,255,255,.08);border:3px solid rgba(255,255,255,.22);box-shadow:0 24px 80px rgba(0,0,0,.5);
         display:flex;align-items:center;gap:22px;white-space:nowrap;box-sizing:border-box">
      <div style="width:100px;height:100px;border-radius:50%;overflow:hidden;background:#111;flex:none"><img src="assets/img/raj-mark.png" alt="" style="width:100px;height:100px;display:block"></div>
      <div><div style="font-size:42px;font-weight:700;line-height:1.05">Samjho with Raj</div>
        <div style="font-size:23px;font-weight:400;color:rgba(245,241,232,.85)">AI + Python series · har hafte naya part</div></div>
      <div id="{f}-btn" style="margin-left:10px;background:{BTN_BG};color:#fff;font-weight:700;font-size:32px;padding:16px 30px;border-radius:9999px">{BTN}</div>
    </div>"""
js = [rise(f"#{f}-l1 .{f}-w", 0.05, 0.08),
      f'  tl.fromTo("#{f}-pill", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {t["pill"]});',
      fade_up(f"#{f}-web", t["web"], 0.5, 30), fade_up(f"#{f}-teaser", t["teaser"], 0.6, 70),
      f'  tl.fromTo("#{f}-sb", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }}, {t["sb"]});',
      f'  tl.fromTo("#{f}-btn", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.22, yoyo: true, repeat: 5, ease: "power1.inOut" }}, {t["btn"]});']
write(f, t["len"], body, js)
print("wrote", sorted(os.listdir(OUT)))
