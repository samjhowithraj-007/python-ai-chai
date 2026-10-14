---
format: 1080x1080
duration: 30s
message: "try-except = crash nahi, samjhao"
arc: Hook → Crash without try → try-except catches it → Two paths → Payoff/teaser
audience: complete beginners who watched Parts 1–8
mode: autonomous
music: host
---

## Video direction

Same world as Parts 1–8 (ink ground, amber stove glow, grid, navy JetBrains Mono cards, cyan keywords, amber output,
terminal with cream prompt and cyan typed answer). New for Part 9: rose #FF8FA3 for errors (ValueError text, a
CRASH! stamp, a short horizontal shake of the terminal), and a cyan shield glyph for the safety net that catches it.
DM Sans 700 ≥ 72px labels, code ≥ 34px, max 4 code lines, nothing below y=896. Silent film.

## Frame 1 — Hook

- scene: "PART 9"; "Galat input?"; mini terminal "Kitne cup? teen"; "try-except bachayega!"
- duration: 4s
- poster: 3.5s
- transition_in: cut
- status: animated
- voiceover: "Part 9: galat input? try-except bachayega!"
- src: compositions/frames/01-hook.html
- blueprint: compose
- focal: the mini terminal with "teen" typed in rose
- roles: kicker; title "Galat input?" (input amber); sub line with "try-except" cyan mono

Scene 1 (0.0–1.2s): kicker; title rises.
→ Scene 2 (1.2–2.8s): mini terminal appears; "teen" types in rose.
→ Scene 3 (2.8–4.0s): "try-except bachayega!" rises.

## Frame 2 — Crash

- scene: int(input()) gets "teen"; ValueError prints; terminal shakes; CRASH! stamp
- duration: 7s
- poster: 6.5s
- transition_in: crossfade
- status: animated
- voiceover: "Customer ne likha teen. int ko number chahiye tha. Program crash!"
- src: compositions/frames/02-crash.html
- blueprint: compose
- focal: the terminal error and the CRASH! stamp
- roles: header "Bina try: crash!" (crash rose); code card (1 line); terminal (prompt, "teen", ValueError lines)

Scene 1 (0.0–1.0s): header; code line types.
→ Scene 2 (1.2–3.4s): terminal: prompt, "teen" types.
→ Scene 3 (3.4–7.0s): ValueError lines print in rose; terminal shakes; CRASH! stamp lands.

## Frame 3 — try-except

- scene: try / except ValueError code; highlight runs try, jumps to except; terminal prints "Number likho!"; shield
- duration: 8s
- poster: 7.5s
- transition_in: crossfade
- status: animated
- voiceover: "try mein koshish karo. Error aaya? except pakad lega aur pyaar se bolega: number likho!"
- src: compositions/frames/03-try.html
- blueprint: compose
- focal: the line highlight jumping from the try line to the except branch
- roles: header "try-except = safety net" (try-except cyan); 4-line code card; terminal; shield glyph

Scene 1 (0.0–1.6s): header; code card types its four lines.
→ Scene 2 (1.8–4.0s): highlight on try line; terminal: "Kitne cup? teen".
→ Scene 3 (4.0–8.0s): rose flash on the try line; highlight jumps to except, then the print line; shield pops; terminal prints "Number likho!" in amber.

## Frame 4 — Two paths

- scene: try box splits: OK → "chalta raho" (cyan), Error → except → "pyaar se samjhao" (amber)
- duration: 5s
- poster: 4.5s
- transition_in: crossfade
- status: animated
- voiceover: "Sab theek? Chalta raho. Error? except sambhalega."
- src: compositions/frames/04-paths.html
- blueprint: compose
- focal: the two-path diagram with a dot travelling each path
- roles: header "Error? except sambhalega"; top node "try"; branch labels OK (cyan) / Error (rose); result cards

Scene 1 (0.0–1.0s): header; try node pops.
→ Scene 2 (1.0–2.4s): both branches draw; result cards land.
→ Scene 3 (2.4–5.0s): dot travels the OK path, then the Error path.

## Frame 5 — Payoff + teaser

- scene: "try-except = crash nahi, samjhao!"; Part 10 teaser; follow pill
- duration: 6s
- poster: 5.5s
- transition_in: crossfade
- status: animated
- voiceover: "try-except: crash nahi, samjhao. Part 10: while True, dukaan khuli rakho. Follow karo."
- src: compositions/frames/05-cta.html
- blueprint: compose
- focal: payoff line, "samjhao" amber
- roles: teaser card "AGLA PART 10 / while True: dukaan khuli rakho"; follow pill

Scene 1 (0.0–1.6s): payoff lines rise.
→ Scene 2 (1.6–3.4s): teaser card slides up.
→ Scene 3 (3.4–6.0s): follow pill grows in; quiet hold.
