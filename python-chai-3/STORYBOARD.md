---
format: 1080x1080
duration: 30s
message: "if-else se computer decide karta hai"
arc: Hook → if (True) → else (False) → Two roads → Payoff/teaser
audience: complete beginners who watched Parts 1–2
mode: autonomous
music: host
---

## Video direction

Same world as Parts 1–2: ink #0E1116 ground, amber stove glow, faint 72px grid, navy JetBrains Mono code cards,
cyan for Python keywords and the concept word, amber for chai/output. New for Part 3: white sugar cubes (rounded
squares with a soft sheen) that drop to show the value of `cheeni`, a True/False verdict chip (cyan True, rose False
#FF8FA3), and a branch highlight that lands on the line that runs. DM Sans 700 ≥ 72px for labels, code ≥ 44px,
max 4 code lines, nothing below y=896. Silent film: visible text is the copy.

## Frame 1 — Hook

- scene: "PART 3"; "Cheeni kitni?" big; "if-else se decide karo!"
- duration: 4s
- poster: 3.5s
- transition_in: cut
- status: animated
- voiceover: "Part 3: cheeni kitni? if-else se decide karo!"
- src: compositions/frames/01-hook.html
- blueprint: compose
- focal: "Cheeni kitni?" in amber at 130px with a cup and a sugar cube hovering over it
- roles: kicker "PART 3 · SAMJHO WITH RAJ"; sub line with "if-else" in cyan mono

Scene 1 (0.0–1.4s): kicker fades; "Cheeni kitni?" rises word by word.
→ Scene 2 (1.4–2.6s): cup rises; a sugar cube drops toward it and stops just above (hovering = the question).
→ Scene 3 (2.6–4.0s): "if-else se decide karo!" rises.

## Frame 2 — if: True

- scene: cheeni = 2, two cubes drop; if cheeni > 1 is True; prints Meethi chai
- duration: 7s
- poster: 6.5s
- transition_in: crossfade
- status: animated
- voiceover: "Cheeni do hai. Kya do, ek se zyada hai? Haan! Toh meethi chai."
- src: compositions/frames/02-if.html
- blueprint: compose
- focal: code card: cheeni = 2 / if cheeni > 1: / print("Meethi chai")
- roles: header "if = agar" (if cyan); two sugar cubes right of the card; verdict chip "2 > 1 → True" (cyan); output strip "> Meethi chai"

Scene 1 (0.0–1.0s): header rises; card enters.
→ Scene 2 (1.0–2.4s): "cheeni = 2" types; two cubes drop one after another.
→ Scene 3 (2.4–4.2s): "if cheeni > 1:" types; verdict chip "2 > 1 = True" pops in cyan.
→ Scene 4 (4.2–7.0s): print line types with a cyan branch highlight; output strip "> Meethi chai" slides in.

## Frame 3 — else: False

- scene: cheeni = 0; condition False; the else branch runs; prints Feeki chai
- duration: 7s
- poster: 6.5s
- transition_in: crossfade
- status: animated
- voiceover: "Ab cheeni zero. Condition false. Toh else chalega: feeki chai."
- src: compositions/frames/03-else.html
- blueprint: compose
- focal: code card: if cheeni > 1: / print("Meethi chai") / else: / print("Feeki chai")
- roles: header "else = warna" (else cyan); a value chip "cheeni = 0" above the card; verdict chip "0 > 1 = False" (rose); output strip "> Feeki chai"

Scene 1 (0.0–1.2s): header rises; value chip "cheeni = 0" pops; card enters with all four lines.
→ Scene 2 (1.2–3.0s): highlight lands on the if line; verdict chip "0 > 1 = False" pops in rose; the "Meethi" line dims.
→ Scene 3 (3.0–4.6s): highlight jumps to else:, then to the Feeki print line.
→ Scene 4 (4.6–7.0s): output strip "> Feeki chai" slides in.

## Frame 4 — Two roads

- scene: A fork: "cheeni > 1 ?" splits into True → Meethi chai and False → Feeki chai; a dot travels a path
- duration: 6s
- poster: 5.5s
- transition_in: crossfade
- status: animated
- voiceover: "if-else matlab do raaste. Condition decide karti hai kaunsa raasta."
- src: compositions/frames/04-fork.html
- blueprint: compose
- focal: the fork diagram: decision node at top, two branches down to two result cards
- roles: header "if-else = do raaste" (do raaste amber); branch labels True (cyan) / False (rose); result cards "Meethi chai" / "Feeki chai"

Scene 1 (0.0–1.2s): header rises; the decision node "cheeni > 1 ?" pops.
→ Scene 2 (1.2–3.0s): both branches draw down; their labels and result cards land.
→ Scene 3 (3.0–6.0s): a glowing dot travels down the True branch and lights Meethi; then a second dot travels the False branch and lights Feeki.

## Frame 5 — Payoff + teaser

- scene: "if-else = computer ka faisla"; Part 4 teaser; follow pill
- duration: 6s
- poster: 5.5s
- transition_in: crossfade
- status: animated
- voiceover: "if-else: computer ka faisla. Part 4: list, chai ke flavours. Follow karo."
- src: compositions/frames/05-cta.html
- blueprint: compose
- focal: the payoff line, "faisla" amber
- roles: teaser card "AGLA PART 4 / list: chai ke flavours" (list cyan); follow pill

Scene 1 (0.0–1.6s): payoff lines rise.
→ Scene 2 (1.6–3.4s): teaser card slides up.
→ Scene 3 (3.4–6.0s): follow pill grows in; quiet hold.
