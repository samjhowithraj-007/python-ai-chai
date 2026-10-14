---
format: 1080x1080
duration: 30s
message: "input = program se baat karo"
arc: Hook → input() → int(input()) → Why int → Payoff/teaser
audience: complete beginners who watched Parts 1–7
mode: autonomous
music: host
---

## Video direction

Same world as Parts 1–7 (ink ground, amber stove glow, grid, navy JetBrains Mono cards, cyan keywords, amber
output). New for Part 8: a terminal where the PROGRAM's prompt prints in cream and the USER's typed answer appears in
cyan with a blinking-free block caret (the conversation between program and person), and a speech bubble for the
hook. Rose #FF8FA3 for the "Oops" wrong result. DM Sans 700 ≥ 72px labels, code ≥ 36px, max 4 code lines, nothing
below y=896. Silent film.

## Frame 1 — Hook

- scene: "PART 8"; "Customer se pucho!"; speech bubble "Kitne cup chahiye?"; "input() se!"
- duration: 4s
- poster: 3.5s
- transition_in: cut
- status: animated
- voiceover: "Part 8: customer se pucho! input se."
- src: compositions/frames/01-hook.html
- blueprint: compose
- focal: speech bubble with the question
- roles: kicker; title with "pucho" amber; answer line "input()" cyan mono

Scene 1 (0.0–1.4s): kicker; title rises.
→ Scene 2 (1.4–2.8s): speech bubble pops with its tail.
→ Scene 3 (2.8–4.0s): "input() se!" rises.

## Frame 2 — input()

- scene: naam = input("Naam? "); terminal asks, user types Raj, prints Namaste Raj
- duration: 7s
- poster: 6.5s
- transition_in: crossfade
- status: animated
- voiceover: "input program ko rokta hai aur user se poochta hai. Naam? Raj. Namaste Raj!"
- src: compositions/frames/02-input.html
- blueprint: compose
- focal: the terminal conversation
- roles: header "input = user se pucho" (input cyan); code card (2 lines); terminal (prompt, typed answer, output)

Scene 1 (0.0–1.0s): header; code card types both lines.
→ Scene 2 (1.6–4.4s): terminal appears; "Naam? " prints; "Raj" types in cyan with a caret.
→ Scene 3 (4.4–7.0s): "Namaste Raj" prints in amber.

## Frame 3 — int(input())

- scene: cups = int(input(...)); user types 3; Bill: 60; chip "3" → 3
- duration: 7s
- poster: 6.5s
- transition_in: crossfade
- status: animated
- voiceover: "Number chahiye toh int lagao. Kitne cup? 3. Bill: 60."
- src: compositions/frames/03-int.html
- blueprint: compose
- focal: the terminal: "Kitne cup? 3" then "Bill: 60"
- roles: header "int() = number banao" (int() cyan); code card (3 lines); terminal; chip '"3" → 3'

Scene 1 (0.0–1.6s): header; code card types three lines.
→ Scene 2 (1.8–4.4s): terminal: prompt prints, "3" types in cyan; chip '"3" → 3' pops.
→ Scene 3 (4.4–7.0s): "Bill: 60" prints in amber.

## Frame 4 — Why int()

- scene: "3" * 20 → 333… (Oops!) vs 3 * 20 → 60 ✓
- duration: 6s
- poster: 5.5s
- transition_in: crossfade
- status: animated
- voiceover: "int na lagaya toh? Teen, bees baar likh dega! int ke saath: 60."
- src: compositions/frames/04-why.html
- blueprint: compose
- focal: the two result cards side by side
- roles: header "int() kyun?"; left card rose: "3" * 20 → 3333… + "Oops!"; right card cyan: 3 * 20 → 60 + check

Scene 1 (0.0–1.2s): header; left card with the string expression.
→ Scene 2 (1.2–2.8s): the 3333… result spills across; "Oops!" stamp.
→ Scene 3 (2.8–6.0s): right card: 3 * 20 → 60 with a cyan check.

## Frame 5 — Payoff + teaser

- scene: "input = program se baat karo"; Part 9 teaser; follow pill
- duration: 6s
- poster: 5.5s
- transition_in: crossfade
- status: animated
- voiceover: "input: program se baat karo. Part 9: try-except, galat input? No problem. Follow karo."
- src: compositions/frames/05-cta.html
- blueprint: compose
- focal: payoff line, "baat karo" amber
- roles: teaser card "AGLA PART 9 / try-except: galat input? No problem!"; follow pill

Scene 1 (0.0–1.6s): payoff lines rise.
→ Scene 2 (1.6–3.4s): teaser card slides up.
→ Scene 3 (3.4–6.0s): follow pill grows in; quiet hold.
