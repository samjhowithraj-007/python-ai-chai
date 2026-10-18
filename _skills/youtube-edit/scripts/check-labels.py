"""Re-transcribe a FINAL flat cut with the medium model and flag any spoken labels.
Usage: python check-labels.py <flat.mp4> [more.mp4 ...]
"""
import subprocess, sys, re, numpy as np
from faster_whisper import WhisperModel

BAD = re.compile(r"सीन|सिन|scene|सीजं|कट|cut|take|टेक|again|अगेन|शूट|shoot|कैमरा|camera|नंबर|नम्बर|number|hook|हुक", re.I)
m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=6)
for path in sys.argv[1:]:
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
    a = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    print("=====", path, "%.1f s" % (len(a) / 16000))
    for s0 in np.arange(0, len(a) / 16000, 27.0):
        r, _ = m.transcribe(a[int(s0 * 16000):int((s0 + 28) * 16000)], language="hi", beam_size=5, condition_on_previous_text=False)
        for seg in r:
            t = seg.text.strip()
            if s0 > 0 and seg.start < 1.0: continue  # overlap already printed
            print("%6.1f-%6.1f  %s%s" % (s0 + seg.start, s0 + seg.end, t, "   <<< LABEL?" if BAD.search(t) else ""))
