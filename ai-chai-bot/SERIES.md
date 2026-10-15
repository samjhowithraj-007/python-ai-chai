# 🤖 AI + Python: chai ka chatbot banao — 20-part series (2 seasons × 10)

Sequel to the 10-part python-chai Instagram series (`videos/python-chai`, `python-chai-2` … `-10`).
Same world, same look, same pipeline: 1080×1080 square, Raj on camera bottom-right (CapCut black background + matte-black.py), his Hinglish voice, low lo-fi bed,
low lo-fi bed, built with `build-frames.py` → HyperFrames render. Projects live in `videos/ai-chai-bot-NN/`.

**Story:** the chai dukaan gets a chatbot, "Chai Bot". It starts buddhu (same reply to everything), learns rules
(S1), gets a real AI brain via the Claude API (S2), gains superpowers like memory files and multiple tools (S3),
becomes a real app people can open (S4), and ends as a full chai-dukaan AI agent (S5). Each part adds one Python idea and keeps every earlier one.

**Audience:** people who watched Parts 1–10 (variables, functions, if-else, list, for, dict, input, try-except,
while True/break). No other coding background assumed.

**Fixed rules for every part**
- ≤ 4 code lines on screen, code ≥ 32 px, DM Sans 700 labels ≥ 72 px, nothing below y = 896.
- Ink ground + amber stove glow + grid, navy code card, cyan keywords, amber output, rose for errors/stop.
- New recurring prop: the **chat window** (customer bubbles right/cream, Chai Bot bubbles left/cyan with a bot face).
- 5 frames: Hook (4 s) → idea (6–8 s) → code + terminal/chat demo (7–8 s) → visual metaphor (5–6 s) → payoff + next-part teaser + channel bar (6 s).
- End card channel bar (same as the Agentic AI series): round raj-mark logo + "Samjho with Raj" + tagline + pulsing button.
- End card also shows "Free notes + code: samjhowithraj.online" above the channel bar; thumbnail footer and both captions carry the site link
  (Instagram: "link in bio"; YouTube description: https://www.samjhowithraj.online/#chatbot-N).
  `python build-frames.py yt` → red Subscribe, `python build-frames.py ig` → blue Follow; render both as `renders/chai-bot-NN-yt.mp4` / `-ig.mp4`. Format stays square 1080×1080 like the python-chai series.
- Parts 13–50 show real API / library code; check the `claude-api` skill for current SDK syntax and model IDs before building them.

## Season 1 — Buddhu bot se smart bot (rules, no AI)

| # | Title (hook) | Message | Python idea |
|---|---|---|---|
| 1 | Chai ka chatbot banao! | Chatbot = suno + jawab do + chalte raho | `input` + `print` + `while True` = a bot |
| 2 | Bot ko jawab sikhao | if-else = bot ka dimaag | `if msg == "menu"` replies |
| 3 | 50 if-else? Nahi! | dictionary = jawab ki diary | `replies = {"menu": ..., "price": ...}` + `.get()` |
| 4 | "MENU" ya "menu"? | `.lower()` = sab ek jaisa | `.lower()`, `.strip()` |
| 5 | Poora sentence samjho | `in` = word dhundo | `if "masala" in msg` |
| 6 | Har baar same jawab? Boring! | `random.choice` = naya jawab | `import random` |
| 7 | Bot aapka naam yaad rakhe | variable = bot ki yaad | `naam = input(...)`, f-string greeting |
| 8 | Order cart mein daalo | list `.append` = cart | cart list |
| 9 | Bill bot banayega | dict price + `sum` = total | prices dict, loop total |
| 10 | Code ko saaf karo | `def reply(msg)` = bot ka brain alag | functions + `return` |

## Season 2 — Bot ko AI ka dimaag do (Claude API)

| # | Title (hook) | Message | Python idea |
|---|---|---|---|
| 11 | Rules fail ho gaye! | Rules ki limit — "ek garam wali dena" | why we need AI (no new code) |
| 12 | API kya hai? | API = waiter: order le jaao, jawab le aao | request → response metaphor |
| 13 | Secret key chhupao | API key = ghar ki chaabi, kabhi share nahi | `pip install anthropic`, env var key |
| 14 | Pehli AI baat! | 4 lines mein AI se baat | first `messages.create` call |
| 15 | Bot ko personality do | system prompt = bot ka character | `system="Tum chai wale bhaiya ho"` |
| 16 | AI bhool jaata hai! | messages list = AI ki yaaddasht | chat history list |
| 17 | AI chat loop | while True + API = asli chatbot | loop + history + `break` |
| 18 | AI ko menu do | tools = AI tumhara function chalaye | tool use: `get_price()` |
| 19 | Paisa aur galti bachao | max_tokens + try-except = safe bot | limits, error handling |
| 20 | SERIES FINALE: AI Chai Bot ready! | Sab milake: aap AI developer ho | full bot recap |

Seasons 3–5 (Parts 21–50) are parked; revisit after Part 20.

## Production checklist per part
1. Copy the previous part's folder skeleton (no renders/frames), write `BRIEF.md` + `STORYBOARD.md`.
2. Write `build-frames.py`, run it, write `index.html` (5 scenes, 0.5 s crossfades, bgm).
3. `npx --yes hyperframes@0.8.153 check` → build + render each platform variant (yt, ig).
4. Thumbnail 1080×1920 from `thumbnail/thumb.html`.
5. `CAPTION.md`: Instagram caption + hashtags, Facebook caption (Instagram video, clickable site link, 3–5 hashtags), and YouTube Shorts title (#shorts), description (with the code) and tags.
6. Commit and push the part to github.com/samjhowithraj-007/python-ai-chai (repo root is `videos/`).
7. Update the website (github.com/samjhowithraj-007/samjhowithrajwebsite, local `C:\samjhowithraj\samjhowithrajwebsite`):
   copy `renders/chai-bot-NN-yt.mp4` to `media/chatbot-N.mp4`, add a poster `media/chatbot-N.jpg`, turn the matching
   "coming soon" lesson in `index.html` (COURSES list) into a full lesson with notes, code, output, practice and takeaway (all website text in English; code stays as in the video),
   then commit and push. www.samjhowithraj.online updates by itself.

## Status
- [x] Part 1 — built, 50-part roadmap, square YT + IG versions (see `../ai-chai-bot-01`)
- [x] Part 2 — if-else, face-cam, live on YouTube (shorts/jWicQhnSwek), Instagram, Facebook (reel/2071250410195088) + Story
- [ ] Part 3 — dictionary: scenes built; faceless draft rejected, waiting for Raj's recording (face-cam like Part 2)
- [ ] Parts 4–20 (face-cam, same format as Part 2)
