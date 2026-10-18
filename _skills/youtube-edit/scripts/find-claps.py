"""List clap-like bursts inside the kept ranges of the long take (raw seconds).
A clap: a sudden broadband burst (>= 14 dB above the previous 60 ms), mostly high-frequency energy, gone within ~80 ms.
Each hit also shows whether a transcribed word overlaps it (claps usually sit between words).
Usage: python find-claps.py [cut-list.json]
"""
import json, sys, wave, numpy as np

cl = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "cut-list.json"))["kept"]
w = wave.open("audio-raw.wav"); sr = w.getframerate()
a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
words = [(x[1], x[2]) for d in json.load(open("line-times.json")) for x in d["words"]]
hop = int(sr * 0.01)
hits = []
for k in cl:
    s0, s1 = int(k["start"] * sr), int(k["end"] * sr)
    seg = a[s0:s1]
    n = len(seg) // hop
    if n < 20:
        continue
    fr = seg[:n * hop].reshape(n, hop)
    en = 10 * np.log10((fr ** 2).mean(1) + 1e-10)
    hf = 10 * np.log10((np.diff(fr, axis=1) ** 2).mean(1) + 1e-10)      # first difference ~ high-pass
    for i in range(6, n - 8):
        prev = en[i - 6:i].mean()
        if en[i] - prev < 14 or en[i] < -32:
            continue
        if hf[i] - en[i] < -6:            # not treble-heavy enough (voiced speech is bass-heavy)
            continue
        if en[i + 8] > en[i] - 12:        # did not die within 80 ms
            continue
        t = (s0 + i * hop) / sr
        if hits and t - hits[-1][0] < 0.3:
            continue
        inword = any(ws - 0.02 <= t <= we + 0.02 for ws, we in words)
        hits.append((t, round(en[i] - prev, 1), round(en[i], 1), inword))
for t, jump, lev, inword in hits:
    print("%8.2f  jump %5.1f dB  level %6.1f dB  %s" % (t, jump, lev, "in a word" if inword else "BETWEEN WORDS"))
print(len(hits), "candidates")
