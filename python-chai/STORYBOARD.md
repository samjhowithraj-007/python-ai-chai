---
format: 1080x1080
duration: 30s
message: "Agar chai bana sakte ho, Python seekh sakte ho"
arc: Hook → Variables → Function → Loop → Payoff/CTA
audience: complete beginners who have never coded
mode: autonomous
music: host
---

## Video direction

One warm, dark kitchen-meets-code world. The ground is ink #0E1116 with a soft amber glow low in the frame (the stove)
and a faint 72px grid. Every frame pairs one chai object (cup, kettle, flame) drawn in simple line art on the left/top
with a JetBrains Mono code card (navy #181715, 8px radius, hairline cream@14%) that types in line by line. Cyan #0AF0F0
marks Python keywords and the concept word; amber #FFB020 marks chai and the payoff. DM Sans 700 for labels, ≥72px.
Motion is calm and confident: power2/power3 outs, 0.4–0.6s entrances, one camera push per frame (scale 1.00→1.04).
Silent film (no narration): every frame's visible text IS the copy, short and Hinglish. Nothing below y=896.

## Frame 1 — Hook

- scene: A chai cup steams; "Chai bana sakte ho?" then "Toh Python bhi!" lands in cyan
- duration: 5s
- poster: 4s
- transition_in: cut
- status: animated
- voiceover: "Chai bana sakte ho? Toh Python bhi seekh sakte ho."
- src: compositions/frames/01-hook.html
- blueprint: compose
- focal: a large line-art chai cup (amber) with three steam curls rising
- roles: question line (cream, DM Sans 700 84px), answer line ("Toh Python bhi!" with Python in cyan), small kicker "SAMJHO WITH RAJ"

Scene 1 (0.0–1.6s): kicker fades in top; the cup rises into the centre-lower area (y 420–800) and steam curls draw upward.
→ Scene 2 (1.6–3.0s): "Chai bana sakte ho?" rises word by word at top (y ~170).
→ Scene 3 (3.0–5.0s): "Toh Python bhi!" rises under it (y ~280), "Python" cyan with a glow; slow push 1.00→1.04 under all.

## Frame 2 — Ingredients = Variables

- scene: Ingredients drop in as Python variables typing into a code card
- duration: 7s
- poster: 6.5s
- transition_in: crossfade
- status: animated
- voiceover: "Ingredients hain variables: paani, doodh, chai patti, cheeni."
- src: compositions/frames/02-variables.html
- blueprint: compose
- focal: code card with 4 lines (paani = "1 cup" / doodh = "1/2 cup" / chai_patti = 2 / cheeni = 1)
- roles: header "Ingredients = Variables" (Variables cyan), 4 small ingredient chips on the left that pop in one per code line

Scene 1 (0.0–1.0s): header rises at top (y ~120). Code card slides up into place (x 300–1010, y 260–700).
→ Scene 2 (1.0–5.6s): each line types in over ~0.8s, 1.15s apart; as each line starts, its ingredient chip (icon + word) pops on the left column.
→ Scene 3 (5.6–7.0s): variable names glow cyan once in sequence; slow push.

## Frame 3 — Recipe = Function

- scene: The four steps wrap inside def chai_banao(): and the call runs
- duration: 6s
- poster: 5.5s
- transition_in: crossfade
- status: animated
- voiceover: "Recipe hai function. Ek baar likho, baar baar banao."
- src: compositions/frames/03-function.html
- blueprint: compose
- focal: code card: def chai_banao(): / paani_ubaalo() / patti_daalo() / doodh_daalo()
- roles: header "Recipe = Function" (Function cyan); a pill "chai_banao()" that stamps in 3 times = "baar baar"

Scene 1 (0.0–1.0s): header rises; code card enters.
→ Scene 2 (1.0–3.6s): "def chai_banao():" types (def cyan), then the three indented steps type in.
→ Scene 3 (3.6–6.0s): three amber "chai_banao()" pills stamp in below the card one by one (0.5s apart), each with a tiny cup glyph.

## Frame 4 — Jab tak ubaal na aaye = while loop

- scene: A kettle heats, a temperature bar loops up while the loop code highlights, then "Chai ready!" prints
- duration: 7s
- poster: 6.5s
- transition_in: crossfade
- status: animated
- voiceover: "Jab tak ubaal na aaye, garam karo. Yahi hai while loop."
- src: compositions/frames/04-loop.html
- blueprint: compose
- focal: code card: while not ubaal: / garam_karo() / print("Chai ready!")
- roles: header "while loop" in cyan with the Hinglish "Jab tak ubaal na aaye" above it; a vertical heat bar beside the card filling in 4 steps; an output strip "> Chai ready!" in amber

Scene 1 (0.0–1.2s): Hinglish line + header rise; code card enters with the three lines present.
→ Scene 2 (1.2–4.6s): the loop runs: a cyan highlight bar jumps between line 1 and line 2 four times, each time the heat bar fills one step (amber → hotter).
→ Scene 3 (4.6–7.0s): highlight moves to the print line; the output strip "> Chai ready!" slides in under the card; bubbles pop over the heat bar.

## Frame 5 — Payoff + CTA

- scene: The message lands with the cup full; follow CTA
- duration: 5s
- poster: 4.5s
- transition_in: crossfade
- status: animated
- voiceover: "Agar chai bana sakte ho, Python seekh sakte ho. Follow karo, Samjho with Raj."
- src: compositions/frames/05-cta.html
- blueprint: compose
- focal: the message in two lines, "Python seekh sakte ho" in amber
- roles: full chai cup glyph, a cyan pill "Follow karo · Samjho with Raj"

Scene 1 (0.0–1.8s): "Agar chai bana sakte ho," rises; then "Python seekh sakte ho." with Python in cyan and the rest amber.
→ Scene 2 (1.8–3.2s): cup glyph settles beside/below with steam.
→ Scene 3 (3.2–5.0s): CTA pill grows in; final frame settles (quiet hold).
