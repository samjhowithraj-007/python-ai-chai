# 🤖 AI + Python: chai ka chatbot banao — 50-part series (5 seasons × 10)

Sequel to the 10-part python-chai Instagram series (`videos/python-chai`, `python-chai-2` … `-10`).
Same world, same look, same pipeline: 30 s, 1080×1080 square, faceless, on-screen Hinglish text, no voiceover,
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
| 20 | SEASON 2 FINALE: AI Chai Bot ready! | Sab milake: aap AI developer ho | full bot recap + Season 3 teaser |

## Season 3 — Bot ki superpowers

| # | Title (hook) | Message | Python idea |
|---|---|---|---|
| 21 | Jawab type hote dikhe | streaming = live typing | streamed response |
| 22 | AI ko saaf bolo | achha prompt = achha jawab | prompt basics: role, task, format |
| 23 | Examples do, AI seekhe | few-shot = dikhao, phir poocho | example messages |
| 24 | AI se order form bharwao | JSON = AI ka form | structured JSON output |
| 25 | JSON ko Python mein lo | `json.loads` = text se dict | parse into dict |
| 26 | Hindi, English, Hinglish | AI har bhasha samjhe | language instruction in system prompt |
| 27 | Ek se zyada tools | menu + price + stock tools | multiple tool definitions |
| 28 | AI khud tools chalaye | tool loop = jab tak kaam pura na ho | loop until no tool call |
| 29 | Chat file mein save | `json.dump` = chat ki diary | save history to file |
| 30 | Purana customer, yaad hai! | file se memory load | load history, greet by name |

## Season 4 — Bot ko app banao

| # | Title (hook) | Message | Python idea |
|---|---|---|---|
| 31 | Code ke kamre banao | modules = alag files, saaf project | split into files, `import` |
| 32 | Bot ki website 10 lines mein | Streamlit = Python se web app | `pip install streamlit`, first page |
| 33 | Asli chat screen | `st.chat_input` + `st.chat_message` | chat UI |
| 34 | Page refresh, chat gayab? | `session_state` = app ki yaad | keep history across reruns |
| 35 | Menu sidebar mein | sidebar = side ka counter | `st.sidebar`, price list |
| 36 | Menu ki photo dikhao | AI photo bhi padhe | image input (vision) |
| 37 | Dukaan ki jaankari do | knowledge = AI ki kitaab | add a text file to the prompt |
| 38 | Sahi page dhundo | search phir jawab (RAG intro) | keyword search over notes |
| 39 | Duniya ko dikhao | deploy = online, free | Streamlit Community Cloud |
| 40 | Key online bhi safe | secrets = deploy ki tijori | `st.secrets` |

## Season 5 — Chai Dukaan AI Agent

| # | Title (hook) | Message | Python idea |
|---|---|---|---|
| 41 | Telegram pe Chai Bot | bot ab phone pe | Telegram bot basics |
| 42 | Telegram + AI | phone se AI chai order | connect the AI reply function |
| 43 | Order aaya, ping! | notification = dukaandaar ko khabar | send order message to owner |
| 44 | Bot ko test karo | `assert` = bot ka exam | simple tests for reply/bill |
| 45 | Kitna kharcha hua? | tokens = AI ka meter | log usage, cost per chat |
| 46 | Sasta aur tez | sahi model, caching = bachat | model choice, prompt caching |
| 47 | AI plan banaye | agent = soche, kare, check kare | multi-step task: order → bill → time |
| 48 | Bot topic pe rahe | guardrails = dukaan ki seema | off-topic refusal in system prompt |
| 49 | Customer ki raay | feedback = bot sudharo | save ratings, review weak answers |
| 50 | GRAND FINALE: Chai Dukaan AI Agent | 50 parts: buddhu se AI agent | full recap + next learning path |

## Production checklist per part
1. Copy the previous part's folder skeleton (no renders/frames), write `BRIEF.md` + `STORYBOARD.md`.
2. Write `build-frames.py`, run it, write `index.html` (5 scenes, 0.5 s crossfades, bgm).
3. `npx --yes hyperframes@0.8.153 check` → build + render each platform variant (yt, ig).
4. Thumbnail 1080×1920 from `thumbnail/thumb.html`.
5. `CAPTION.md`: Instagram caption + hashtags, and YouTube Shorts title (#shorts), description (with the code) and tags.

## Status
- [x] Part 1 — built, 50-part roadmap, square YT + IG versions (see `../ai-chai-bot-01`)
- [ ] Parts 2–50
