"""transcribe-hinglish.py: word-level Hindi/Hinglish transcript with faster-whisper large-v3 (Parakeet cannot do Hindi).
Usage: python transcribe-hinglish.py <16k mono wav> <out transcript.json> [auto|hi]   (run without python -I: the package is a user-site install)
Writes [{id,text,start,end}] in Devanagari; on-screen copy is written in romanised Hinglish by hand."""
import sys, json
from faster_whisper import WhisperModel
audio, out, lang = sys.argv[1], sys.argv[2], sys.argv[3]
m = WhisperModel("large-v3", device="cpu", compute_type="int8")
import wave, numpy as np
wf = wave.open(audio); a = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float32)/32768
segs, info = m.transcribe(a, language=None if lang=="auto" else lang, word_timestamps=True, vad_filter=False, beam_size=5)
words, lines = [], []
for s in segs:
    lines.append(f"[{s.start:.2f}-{s.end:.2f}] {s.text.strip()}")
    for w in s.words:
        words.append({"text": w.word.strip(), "start": round(w.start,3), "end": round(w.end,3)})
words = [dict(id="w%d" % i, **w) for i, w in enumerate(words)]
json.dump(words, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("lang", info.language, info.language_probability)
print("\n".join(lines))
