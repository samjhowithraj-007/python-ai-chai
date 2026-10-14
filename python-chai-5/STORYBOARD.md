---
format: 1080x1080
duration: 30s
message: "for loop = har item, ek-ek karke"
arc: Hook → The loop visits each item → Output → Why a loop → Payoff/teaser
audience: complete beginners who watched Parts 1–4
mode: autonomous
music: host
---

## Video direction

Same world as Parts 1–4 (ink ground, amber stove glow, grid, navy JetBrains Mono cards, cyan keywords, amber output)
and Part 4's tray of flavour slots (Masala #C8782A, Adrak #E8C26A, Elaichi #8CCB7E, Tulsi #5FB37A). New for Part 5:
a cyan ring that walks the tray one slot per iteration, a variable chip `f = "…"` whose value swaps each round, and a
circular loop arrow motif. DM Sans 700 ≥ 72px labels, code ≥ 40px, max 4 code lines, nothing below y=896. Silent film.

## Frame 1 — Hook

- scene: "PART 5"; "Har flavour try karna hai?"; "for loop karega!"
- duration: 4s
- poster: 3.5s
- transition_in: cut
- status: animated
- voiceover: "Part 5: har flavour try karna hai? for loop karega!"
- src: compositions/frames/01-hook.html
- blueprint: compose
- focal: a circular loop arrow (cyan) spinning once around "for loop"
- roles: kicker; question line; answer line with "for loop" cyan mono

Scene 1 (0.0–1.4s): kicker; question rises word by word.
→ Scene 2 (1.4–4.0s): loop arrow draws a full circle; "for loop karega!" rises inside it.

## Frame 2 — The loop

- scene: for f in flavours: / print(f + " chai"); a ring walks four slots; chip shows f's current value
- duration: 8s
- poster: 7.5s
- transition_in: crossfade
- status: animated
- voiceover: "for f in flavours: har flavour ek-ek karke f mein aata hai."
- src: compositions/frames/02-loop.html
- blueprint: compose
- focal: the cyan ring stepping across the four tray slots, one per iteration
- roles: header "for = har ek ke liye" (for cyan); tray of 4 slots; code card (2 lines); chip f = "…"

Scene 1 (0.0–1.4s): header rises; tray and code card enter; both code lines type.
→ Scene 2 (1.6–7.2s): four iterations, 1.3s apart: the ring lands on slot i, the chip shows f = "<flavour>", the print line pulses.
→ Scene 3 (7.2–8.0s): ring settles on the last slot.

## Frame 3 — Output

- scene: terminal prints four lines, one per flavour, in its tint; badge "4 baar chala!"
- duration: 7s
- poster: 6.5s
- transition_in: crossfade
- status: animated
- voiceover: "Output: masala chai, adrak chai, elaichi chai, tulsi chai. Loop chaar baar chala."
- src: compositions/frames/03-output.html
- blueprint: compose
- focal: terminal panel with the four printed lines
- roles: header "Output" with a small cup; a mini cup beside each printed line; badge "4 baar chala!"

Scene 1 (0.0–1.0s): header rises; terminal enters.
→ Scene 2 (1.0–5.2s): each line prints with its mini cup, 1.0s apart.
→ Scene 3 (5.2–7.0s): badge "4 baar chala!" stamps in (amber).

## Frame 4 — Why a loop

- scene: Bina loop (4 print lines) vs Loop ke saath (2 lines)
- duration: 5s
- poster: 4.5s
- transition_in: crossfade
- status: animated
- voiceover: "Bina loop chaar lines, loop ke saath sirf do. Aur 100 flavours ho toh bhi do!"
- src: compositions/frames/04-why.html
- blueprint: compose
- focal: two side-by-side code cards; the loop card glows cyan
- roles: header "Loop = kam code" (kam code amber); left card dimmed "Bina loop"; right card "Loop ke saath"; caption "100 flavours? Phir bhi 2 lines!"

Scene 1 (0.0–1.2s): header rises; left card with 4 print lines enters.
→ Scene 2 (1.2–2.8s): right card with the 2-line loop enters and glows; left card dims.
→ Scene 3 (2.8–5.0s): caption "100 flavours? Phir bhi 2 lines!" rises.

## Frame 5 — Payoff + teaser

- scene: "for loop = har item, ek-ek karke"; Part 6 teaser; follow pill
- duration: 6s
- poster: 5.5s
- transition_in: crossfade
- status: animated
- voiceover: "for loop: har item, ek-ek karke. Part 6: dictionary, chai ka menu card. Follow karo."
- src: compositions/frames/05-cta.html
- blueprint: compose
- focal: payoff line, "ek-ek karke" amber
- roles: teaser card "AGLA PART 6 / dictionary: chai ka menu card"; follow pill

Scene 1 (0.0–1.6s): payoff lines rise.
→ Scene 2 (1.6–3.4s): teaser card slides up.
→ Scene 3 (3.4–6.0s): follow pill grows in; quiet hold.
