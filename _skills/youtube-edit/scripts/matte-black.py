"""matte-black.py: alpha matte for a clip whose background was removed to pure black (CapCut Remove BG + black).
Usage: ffmpeg -i flat.mp4 -vf "crop=1080:1080:X:0,scale=720:720" -f rawvideo -pix_fmt rgb24 - | python matte-black.py 720 720 16 |
  ffmpeg -f rawvideo -pix_fmt rgba -s 720x720 -r 30 -i - -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 0 -crf 30 -cpu-used 4 -row-mt 1 -auto-alt-ref 0 face-cut.webm
~2.5 min for 40 s (vs ~45 min for AI remove-background on CPU). A plain colour key fails: it also keys dark hair and pupils.
Black-background matte: background = near-black pixels reachable in a straight line from the left, right or top
edge before hitting anything brighter. Raj's blue glow surrounds him, so dark hair/eyes inside it stay opaque.
Reads raw RGB frames from stdin (W x H), writes RGBA frames to stdout."""
import sys, numpy as np
W, H, T = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
inp, out = sys.stdin.buffer, sys.stdout.buffer
n = W * H * 3
while True:
    b = inp.read(n)
    if len(b) < n: break
    f = np.frombuffer(b, np.uint8).reshape(H, W, 3)
    lit = f.max(axis=2) >= T
    bg = (np.cumsum(lit, 1) == 0) | (np.cumsum(lit[:, ::-1], 1)[:, ::-1] == 0) | (np.cumsum(lit, 0) == 0)
    a = (~bg).astype(np.float32)
    # 1-px soft edge
    a = (a + np.roll(a, 1, 0) + np.roll(a, -1, 0) + np.roll(a, 1, 1) + np.roll(a, -1, 1)) / 5
    out.write(np.dstack([f, (a * 255).astype(np.uint8)]).tobytes())
