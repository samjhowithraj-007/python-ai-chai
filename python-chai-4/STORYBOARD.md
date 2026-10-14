---
format: 1080x1080
duration: 30s
message: "list = sab flavours ek jagah"
arc: Hook → Make a list → Index from 0 → append + len → Payoff/teaser
audience: complete beginners who watched Parts 1–3
mode: autonomous
music: host
---

## Video direction

Same world as Parts 1–3: ink #0E1116 ground, amber stove glow, faint 72px grid, navy JetBrains Mono code cards, cyan
for Python keywords and the concept word, amber for chai/output. New for Part 4: a tray of rounded slots (the list),
each holding a small line-art chai cup tinted by flavour (Masala #C8782A, Adrak #E8C26A, Elaichi #8CCB7E,
Tulsi #5FB37A) with its name, and cyan index numbers 0 1 2 3 under the slots. DM Sans 700 ≥ 72px labels, code ≥ 40px,
max 4 code lines, nothing below y=896. Silent film: visible text is the copy.

## Frame 1 — Hook

- scene: "PART 4"; "Chai ke kitne flavours?"; three flavour chips pop; "list mein rakho!"
- duration: 4s
- poster: 3.5s
- transition_in: cut
- status: animated
- voiceover: "Part 4: chai ke kitne flavours? Sab list mein rakho!"
- src: compositions/frames/01-hook.html
- blueprint: compose
- focal: "Chai ke kitne flavours?" with flavours in amber
- roles: kicker; three flavour chips (Masala / Adrak / Elaichi) in their tints; sub line with "list" cyan mono

Scene 1 (0.0–1.4s): kicker; title rises word by word.
→ Scene 2 (1.4–2.8s): three chips pop in, 0.25s apart.
→ Scene 3 (2.8–4.0s): "list mein rakho!" rises.

## Frame 2 — Make a list

- scene: flavours = [...] types in four lines; three tray slots fill with flavour cups
- duration: 7s
- poster: 6.5s
- transition_in: crossfade
- status: animated
- voiceover: "list matlab ek dabba, jismein kai cheezein. Masala, adrak, elaichi."
- src: compositions/frames/02-list.html
- blueprint: compose
- focal: code card: flavours = [ / "Masala", / "Adrak", / "Elaichi" ]
- roles: header "list = ek dabba" (list cyan); tray of 3 slots under the card, each filling as its line types

Scene 1 (0.0–1.0s): header rises; card and empty dashed tray enter.
→ Scene 2 (1.0–5.4s): line 1 types; then each flavour line types and its slot fills with a tinted cup + name.
→ Scene 3 (5.4–7.0s): the tray outline glows cyan once (one box, many things).

## Frame 3 — Index from 0

- scene: slots with index numbers 0 1 2; flavours[0] → Masala, flavours[2] → Elaichi
- duration: 7s
- poster: 6.5s
- transition_in: crossfade
- status: animated
- voiceover: "Ginti zero se shuru hoti hai. flavours zero matlab masala, flavours do matlab elaichi."
- src: compositions/frames/03-index.html
- blueprint: compose
- focal: the index numbers 0 1 2 under the slots, a cyan ring that lands on the slot being read
- roles: header "Ginti 0 se shuru!" (0 amber); code card print(flavours[0]) / print(flavours[2]); two output strips

Scene 1 (0.0–1.4s): header rises; tray with three filled slots; index numbers pop 0, 1, 2.
→ Scene 2 (1.4–4.0s): print(flavours[0]) types; ring lands on slot 0; output "> Masala".
→ Scene 3 (4.0–7.0s): print(flavours[2]) types; ring moves to slot 2; output "> Elaichi".

## Frame 4 — append + len

- scene: flavours.append("Tulsi") slides a 4th cup into the tray; len(flavours) → 4
- duration: 6s
- poster: 5.5s
- transition_in: crossfade
- status: animated
- voiceover: "append se naya flavour jodo: tulsi. Aur len batata hai kitne: chaar."
- src: compositions/frames/04-append.html
- blueprint: compose
- focal: the Tulsi slot sliding in from the right as the 4th item, index 3
- roles: header "append = naya jodo" (append cyan); code card flavours.append("Tulsi") / print(len(flavours)); output "> 4"

Scene 1 (0.0–1.0s): header rises; tray with 3 slots shifted left, card enters.
→ Scene 2 (1.0–3.2s): append line types; the Tulsi slot slides in at index 3.
→ Scene 3 (3.2–6.0s): len line types; output strip "> 4" lands; index numbers 0–3 glow in sequence (counting).

## Frame 5 — Payoff + teaser

- scene: "list = sab flavours ek jagah"; Part 5 teaser; follow pill
- duration: 6s
- poster: 5.5s
- transition_in: crossfade
- status: animated
- voiceover: "list: sab flavours ek jagah. Part 5: for loop, har flavour try karo. Follow karo."
- src: compositions/frames/05-cta.html
- blueprint: compose
- focal: payoff line, "ek jagah" amber
- roles: teaser card "AGLA PART 5 / for loop: har flavour try karo" (for loop cyan); follow pill

Scene 1 (0.0–1.6s): payoff lines rise.
→ Scene 2 (1.6–3.4s): teaser card slides up.
→ Scene 3 (3.4–6.0s): follow pill grows in; quiet hold.
