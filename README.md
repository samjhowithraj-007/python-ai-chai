# Python + AI Chai — Samjho with Raj

Hinglish Instagram / YouTube Shorts series that teach Python through making chai.

- `python-chai`, `python-chai-2` … `python-chai-10` — Python basics series (10 parts)
- `ai-chai-bot/SERIES.md` — plan for the 50-part "AI + Python: chai ka chatbot banao" series
- `ai-chai-bot-NN` — one folder per part
- `_shared` — music and sound effects

Each part is a HyperFrames project: `python build-frames.py [yt|ig]` writes the frames,
`npx --yes hyperframes@0.8.153 render` renders `renders/*.mp4`. Post text is in `CAPTION.md`.

## Skill backup
`_skills/youtube-edit/` is a copy of the Claude Code skill that edits and publishes these videos (installed at
`~/.claude/skills/youtube-edit`). Updated and pushed every time the skill changes. To restore it on a new machine,
copy the folder back to `~/.claude/skills/youtube-edit`.
