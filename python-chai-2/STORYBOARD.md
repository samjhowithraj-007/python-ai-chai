---
format: 1080x1080
duration: 30s
message: "Function ek baar likho, kabhi bhi RUN karo"
arc: Hook → Recap → Run → Return → Payoff/teaser
audience: complete beginners who watched Part 1
mode: autonomous
music: host
---

## Video direction

Same world as Part 1: ink #0E1116 ground, amber stove glow low, faint 72px grid, navy code cards in JetBrains Mono,
cyan for Python keywords and the concept word, amber for chai and output. New element for Part 2: a terminal panel
(darker #0A0C10, green ">>>" prompt) whose output lines print one by one, and an amber "▶ RUN" button that gets
pressed. DM Sans 700 labels ≥ 72px, code ≥ 44px, max 4 code lines, nothing below y=896. Silent film: the visible
text is the copy.

## Frame 1 — Hook

- scene: "PART 2" kicker; "chai_banao() ko RUN karte hain!" with a RUN button pressed
- duration: 4s
- poster: 3.5s
- transition_in: cut
- status: animated
- voiceover: "Part 2: chai_banao() ko run karte hain!"
- src: compositions/frames/01-hook.html
- blueprint: compose
- focal: the amber "▶ RUN" button (big pill) under the title
- roles: kicker "PART 2 · SAMJHO WITH RAJ"; title line 1 "chai_banao()" (mono, cyan), line 2 "ko RUN karte hain!" (RUN amber)

Scene 1 (0.0–1.2s): kicker fades; "chai_banao()" types in large mono.
→ Scene 2 (1.2–2.4s): "ko RUN karte hain!" rises word by word.
→ Scene 3 (2.4–4.0s): RUN button pops in, a cursor arrow slides to it and presses (scale .92 → 1), a glow ring expands.

## Frame 2 — Recap: the function

- scene: The function types in: def chai_banao() with three print steps
- duration: 6s
- poster: 5.5s
- transition_in: crossfade
- status: animated
- voiceover: "Pehle function likha: chai_banao, teen steps ke saath."
- src: compositions/frames/02-recap.html
- blueprint: compose
- focal: code card: def chai_banao(): / print("Paani ubla") / print("Patti daali") / print("Doodh daala")
- roles: header "Pehle: Function likho" (Function cyan)

Scene 1 (0.0–1.0s): header rises; card enters.
→ Scene 2 (1.0–4.6s): the def line types, then the three print lines, one after another.
→ Scene 3 (4.6–6.0s): a cyan bracket draws down the left edge of the indented block, label "andar ke steps".

## Frame 3 — Run it

- scene: chai_banao() runs in a terminal; three output lines print while the cup fills in three steps
- duration: 7s
- poster: 6.5s
- transition_in: crossfade
- status: animated
- voiceover: "Ab call karo: chai_banao(). Har step print hota hai, aur chai banti jaati hai."
- src: compositions/frames/03-run.html
- blueprint: compose
- focal: terminal panel with ">>> chai_banao()" then the three output lines
- roles: header "Ab RUN karo" (RUN amber); line-art cup on the right that fills in three steps, one per output line

Scene 1 (0.0–1.2s): header rises; terminal panel and empty cup enter.
→ Scene 2 (1.2–2.2s): ">>> chai_banao()" types.
→ Scene 3 (2.4–6.0s): each output line prints (Paani ubla / Patti daali / Doodh daala) 1.1s apart; the cup fill rises one third each time; steam draws after the last.

## Frame 4 — Return value

- scene: cup = chai_banao() and print(cup) output "Chai ready!"; return explained
- duration: 7s
- poster: 6.5s
- transition_in: crossfade
- status: animated
- voiceover: "return se function jawab deta hai: cup mein aa gayi chai!"
- src: compositions/frames/04-return.html
- blueprint: compose
- focal: code card: return "Chai ready!" highlighted, then cup = chai_banao() / print(cup) and an output strip "Chai ready!"
- roles: header "return = function ka jawab" (return cyan, jawab amber)

Scene 1 (0.0–1.0s): header rises; card enters with `def chai_banao():` and `    return "Chai ready!"` (return glows cyan).
→ Scene 2 (1.0–3.4s): `cup = chai_banao()` then `print(cup)` type in.
→ Scene 3 (3.6–7.0s): an amber arrow travels from the return line to `cup`; output strip "> Chai ready!" slides in under the card.

## Frame 5 — Payoff + teaser

- scene: "Ek baar likho, kabhi bhi RUN karo"; Part 3 teaser; follow pill
- duration: 6s
- poster: 5.5s
- transition_in: crossfade
- status: animated
- voiceover: "Function: ek baar likho, kabhi bhi run karo. Part 3: if-else, cheeni kitni? Follow karo."
- src: compositions/frames/05-cta.html
- blueprint: compose
- focal: the two-line payoff, "RUN" amber
- roles: teaser card "PART 3 → if-else: cheeni kitni?" (if-else cyan); pill "Follow karo · Samjho with Raj"

Scene 1 (0.0–1.6s): payoff lines rise.
→ Scene 2 (1.6–3.4s): teaser card slides up with a small "?" bounce-free pulse.
→ Scene 3 (3.4–6.0s): follow pill grows in; quiet hold.
