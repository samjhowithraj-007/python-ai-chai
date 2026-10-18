#!/usr/bin/env python3
"""Clean voice track for a cut video, rebuilt from the RAW take (fixes a "whoosh"/hiss under the voice).

Why: quiet room tone (fan, AC) in the raw is inaudible until the voice is boosted to YouTube level; time-stretching it
(the 1.05x speed-up) and the render's own audio processing turn it into a swelling "whoosh" in every pause, and a
dynamic loudnorm pumps it further. So: never ship the render's audio; build the voice from the raw instead.

Steps: high-pass 110 Hz -> afftdn noise reduction with a profile learned from the quietest 0.75 s gap in the raw
(auto-found, or --gap START END) -> soft gate between words -> the same cut as the cut-list (20 ms fades, like
apply-cut.py) -> the same speed-up. Then ONE fixed gain to the target LUFS (no dynamic loudnorm).
Output: a WAV on the flat-cut timeline (mux it under the rendered picture with -map 0:v -map 1:a).

Usage: python clean-voice.py --raw raw.mp4 --cut-list cut-list.json --out voice-clean.wav [--speed 1.05] [--lufs -15]
       [--gap 152.30 153.05]
"""
import argparse, json, os, re, subprocess
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--raw", required=True); ap.add_argument("--cut-list", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--speed", type=float, default=1.0); ap.add_argument("--lufs", type=float, default=-15.0)
ap.add_argument("--gap", type=float, nargs=2)
a = ap.parse_args()
work = os.path.dirname(os.path.abspath(a.out)); os.makedirs(work, exist_ok=True)
rel = lambda p: os.path.relpath(p).replace(os.sep, "/")       # ffmpeg filter args cannot take "C:" paths
run = lambda c: subprocess.run(c, check=True)
raw_wav, den_wav, cut_wav = (os.path.join(work, n) for n in ("_voice-raw.wav", "_voice-den.wav", "_voice-cut.wav"))
run(["ffmpeg", "-y", "-v", "error", "-i", a.raw, "-vn", "-ac", "2", "-ar", "48000", raw_wav])

if a.gap:
    g0, g1 = a.gap
else:   # quietest 0.75 s stretch in the first 5 minutes = room tone only
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-t", "300", "-i", raw_wav, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True).stdout
    x = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    w, hop = 12000, 1600
    e = [(float((x[i:i + w] ** 2).mean()), i) for i in range(16000, len(x) - w, hop)]
    g0 = min(e)[1] / 16000; g1 = g0 + 0.75
print("noise profile from %.2f-%.2f s" % (g0, g1))
cmd = os.path.join(work, "_nr-cmd.txt")
open(cmd, "w").write("%.2f afftdn sample_noise start;\n%.2f afftdn sample_noise stop;\n" % (g0, g1))
run(["ffmpeg", "-y", "-v", "error", "-i", raw_wav, "-af",
     f"highpass=f=110,asendcmd=f={rel(cmd)},afftdn=nr=28:nf=-50:tn=1:om=o,"
     "agate=threshold=0.008:ratio=6:attack=4:release=200:range=0.06", den_wav])

kept = json.load(open(a.cut_list))["kept"]; F = 0.02
parts = "".join(f"[0:a]atrim=start={k['start']:.6f}:end={k['end']:.6f},asetpts=PTS-STARTPTS,afade=t=in:d={F},"
                f"afade=t=out:st={max(0.0, k['end'] - k['start'] - F):.6f}:d={F}[a{i}];" for i, k in enumerate(kept))
tail = "".join(f"[a{i}]" for i in range(len(kept))) + f"concat=n={len(kept)}:v=0:a=1" + (f",atempo={a.speed}" if a.speed != 1 else "") + "[out]"
script = os.path.join(work, "_voice-cut.txt"); open(script, "w").write(parts + tail)
run(["ffmpeg", "-y", "-v", "error", "-i", den_wav, "-/filter_complex", script, "-map", "[out]", cut_wav])   # ffmpeg 7+: -/filter_complex

o = subprocess.run(["ffmpeg", "-i", cut_wav, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
gain = a.lufs - float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])
run(["ffmpeg", "-y", "-v", "error", "-i", cut_wav, "-af", f"volume={gain:.2f}dB,alimiter=limit=0.89", a.out])
for p in (raw_wav, den_wav, cut_wav): os.remove(p)
print("clean voice -> %s (fixed gain %+.1f dB to %.0f LUFS)" % (a.out, gain, a.lufs))
