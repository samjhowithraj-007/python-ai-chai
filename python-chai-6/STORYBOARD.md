---
format: 1080x1080
duration: 30s
message: "dictionary = naam se dhundo"
arc: Hook → Make the dict (menu fills) → Lookup by key → Add + update → Payoff/teaser
audience: complete beginners who watched Parts 1–5
mode: autonomous
music: host
---

## Video direction

Same world as Parts 1–5 (ink ground, amber stove glow, grid, navy JetBrains Mono cards, cyan keywords, amber values,
flavour tints Masala #C8782A / Adrak #E8C26A / Elaichi #8CCB7E / Tulsi #5FB37A). New for Part 6: a chai menu card
(navy, cream hairline, "CHAI MENU" kicker) whose rows are name … Rs price with a dotted leader; keys glow cyan,
prices amber. Prices are written "Rs 20" (the shipped fonts have no rupee glyph). DM Sans 700 ≥ 72px labels,
code ≥ 40px, max 4 code lines, nothing below y=896. Silent film.

## Frame 1 — Hook

- scene: "PART 6"; "Masala chai kitne ki?"; "dictionary batayegi!" with a small menu card
- duration: 4s
- poster: 3.5s
- transition_in: cut
- status: animated
- voiceover: "Part 6: masala chai kitne ki? Dictionary batayegi!"
- src: compositions/frames/01-hook.html
- blueprint: compose
- focal: the question "kitne ki?" in amber
- roles: kicker; a tilted mini menu card; answer line with "dictionary" cyan mono

Scene 1 (0.0–1.4s): kicker; question rises word by word.
→ Scene 2 (1.4–2.6s): mini menu card drops in tilted.
→ Scene 3 (2.6–4.0s): "dictionary batayegi!" rises.

## Frame 2 — Make the dict

- scene: menu = {...} types; menu card rows fill in sync; key/value chips
- duration: 8s
- poster: 7.5s
- transition_in: crossfade
- status: animated
- voiceover: "dictionary mein key aur value: naam aur daam. Masala 20, adrak 15, elaichi 25."
- src: compositions/frames/02-dict.html
- blueprint: compose
- focal: code card: menu = { / "Masala": 20, / "Adrak": 15, / "Elaichi": 25 }
- roles: header "key : value" (key cyan, value amber); menu card right; chips "key = naam" (cyan) and "value = daam" (amber)

Scene 1 (0.0–1.0s): header; code card and empty menu card enter.
→ Scene 2 (1.0–5.4s): first line types; each entry line types and its menu row fills.
→ Scene 3 (5.4–8.0s): the two chips pop under the cards.

## Frame 3 — Lookup by key

- scene: menu["Masala"] → 20; menu["Elaichi"] → 25; the read row lights up
- duration: 7s
- poster: 6.5s
- transition_in: crossfade
- status: animated
- voiceover: "Key do, value lo. menu Masala: 20. menu Elaichi: 25."
- src: compositions/frames/03-lookup.html
- blueprint: compose
- focal: the menu card with a cyan highlight that lands on the looked-up row
- roles: header "Key do, value lo!" (Key cyan, value amber); code card with two print lines; two output strips

Scene 1 (0.0–1.0s): header; menu card and code card enter.
→ Scene 2 (1.0–3.6s): print(menu["Masala"]) types; Masala row lights; output "> 20".
→ Scene 3 (3.6–7.0s): print(menu["Elaichi"]) types; highlight moves to Elaichi; output "> 25".

## Frame 4 — Add + update

- scene: menu["Tulsi"] = 30 adds a row; menu["Adrak"] = 18 flips the price
- duration: 6s
- poster: 5.5s
- transition_in: crossfade
- status: animated
- voiceover: "Naya item? menu Tulsi barabar 30. Daam badla? Adrak ab 18."
- src: compositions/frames/04-update.html
- blueprint: compose
- focal: the menu card: Tulsi row slides in; Adrak price flips 15 → 18
- roles: header "Add bhi, update bhi!" (Add, update cyan); code card with the two assignment lines

Scene 1 (0.0–1.0s): header; menu card (3 rows) and code card enter.
→ Scene 2 (1.0–3.0s): line 1 types; Tulsi row slides in.
→ Scene 3 (3.0–6.0s): line 2 types; Adrak's price flips 15 → 18 with an amber flash.

## Frame 5 — Payoff + teaser

- scene: "dictionary = naam se dhundo"; Part 7 teaser; follow pill
- duration: 5s
- poster: 4.5s
- transition_in: crossfade
- status: animated
- voiceover: "dictionary: naam se dhundo. Part 7: mini project, chai ka bill. Follow karo."
- src: compositions/frames/05-cta.html
- blueprint: compose
- focal: payoff line, "naam se dhundo" amber
- roles: teaser card "AGLA PART 7 / Mini project: chai ka bill" (bill cyan); follow pill

Scene 1 (0.0–1.4s): payoff lines rise.
→ Scene 2 (1.4–3.0s): teaser card slides up.
→ Scene 3 (3.0–5.0s): follow pill grows in; quiet hold.
