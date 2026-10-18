#!/usr/bin/env bash
# One command per chai-bot part: build both platform variants, check, render, snapshot, deliver.
# Usage: bash _tools/make-part.sh ai-chai-bot-03 [snap-times]   (run from videos/)
# Usage-light by design: one tool call, quiet logs, one small contact sheet to review.
set -u
P="$1"; SNAP="${2:-3.5,10,17,23,28.5}"
NN="${P##*-}"; OUT="/c/Users/rajpr/Videos/YouTube Renders/$P"   # one folder per part; old versions kept as -vN
HF="npx --yes hyperframes@0.8.154"
cd "$(dirname "$0")/../$P" || exit 1
mkdir -p renders/old
for PL in yt ig; do
  PYTHONUTF8=1 python build-frames.py "$PL" > build-$PL.log 2>&1 || { echo "BUILD FAIL $PL"; tail -5 build-$PL.log; exit 1; }
  if [ "$PL" = yt ]; then
    $HF check > check.log 2>&1; grep -E "✗|Check (passed|failed)" check.log | head -8
    $HF snapshot --at "$SNAP" 2>&1 | grep -i "contact" | sed 's/.*\(C:.*jpg\).*/SNAP \1/'
  fi
  R="renders/chai-bot-$NN-$PL.mp4"; if [ -f "$R" ]; then N=1; while [ -e "renders/old/chai-bot-$NN-$PL-v$N.mp4" ]; do N=$((N+1)); done; mv "$R" "renders/old/chai-bot-$NN-$PL-v$N.mp4"; fi
  $HF render --quality high --output "renders/chai-bot-$NN-$PL.mp4" > render-$PL.log 2>&1 || { echo "RENDER FAIL $PL"; tail -5 render-$PL.log; exit 1; }
  bash ../_tools/deliver.sh "$OUT" "renders/chai-bot-$NN-$PL.mp4" | grep -v "^SAME"
  echo "OK $PL $(ffprobe -v error -show_entries format=duration -of csv=p=0 renders/chai-bot-$NN-$PL.mp4)s"
done
[ -f thumbnail/thumbnail-1080x1920.png ] && bash ../_tools/deliver.sh "$OUT" thumbnail/thumbnail-1080x1920.png | grep -v "^SAME"
[ -f CAPTION.md ] && bash ../_tools/deliver.sh "$OUT" CAPTION.md | grep -v "^SAME"
echo DONE
