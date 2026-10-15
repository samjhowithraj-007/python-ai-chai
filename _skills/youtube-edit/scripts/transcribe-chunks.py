"""transcribe-chunks.py: Hinglish transcript of a long raw take, fast and with live progress.
Splits the 16 kHz mono WAV at pauses (20 ms RMS > 0.006, gaps < 0.6 s merged, chunks <= 12 s), transcribes each chunk
with faster-whisper (beam 1, no cross-chunk context, so no skipped windows or hallucination loops) and writes
[{start,end,text}] plus a <out>.log that grows line by line (tail it to watch progress).
Usage: python transcribe-chunks.py <16k mono wav> <out.json> [large-v3|medium]   (run without python -I)
A 3-minute take takes ~20 min on this laptop's CPU with large-v3; medium is ~2x faster and good enough to pick takes."""
import sys, json, wave, numpy as np
from faster_whisper import WhisperModel
wf = wave.open(sys.argv[1]); a = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float32)/32768; sr=16000
hop=320; n=len(a)//hop; r=np.array([np.sqrt((a[i*hop:(i+1)*hop]**2).mean()) for i in range(n)])
sp=r>0.006; segs=[]; i=0
while i<n:
    if sp[i]:
        j=i
        while j<n and sp[j]: j+=1
        segs.append([i*0.02,j*0.02]); i=j
    else: i+=1
ch=[]
for s in segs:
    if ch and s[0]-ch[-1][1]<0.6 and s[1]-ch[-1][0]<12: ch[-1][1]=s[1]
    else: ch.append(list(s))
ch=[c for c in ch if c[1]-c[0]>0.25]
m = WhisperModel(sys.argv[3], device="cpu", compute_type="int8")
out=[]; log=open(sys.argv[2]+".log","w",encoding="utf-8")
for k,(s0,s1) in enumerate(ch):
    seg=a[int(max(0,s0-0.15)*sr):int((s1+0.15)*sr)]
    res,_=m.transcribe(seg, language="hi", beam_size=1, condition_on_previous_text=False, vad_filter=False)
    t=" ".join(x.text.strip() for x in res)
    out.append({"start":round(s0,2),"end":round(s1,2),"text":t})
    log.write(f"[{s0:6.2f}-{s1:6.2f}] {t}\n"); log.flush()
json.dump(out,open(sys.argv[2],"w",encoding="utf-8"),ensure_ascii=False,indent=0)
