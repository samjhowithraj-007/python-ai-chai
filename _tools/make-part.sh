#!/usr/bin/env bash
# One command per chai-bot part: build both platform variants, check, render, snapshot, deliver.
# Usage: bash _tools/make-part.sh ai-chai-bot-03 [snap-times]   (run from videos/)
# Usage-light by design: one tool call, quiet logs, one small contact sheet to review.
set -u
P="$1"; SNAP="${2:-3.5,10,17,23,28.5}"
NN="${P##*-}"; OUT="/c/Users/rajpr/Videos/YouTube Renders/ai-chai-bot"
HF="npx --yes hyperframes@0.8.154"
cd "$(dirname "$0")/../$P" || exit 1
mkdir -p renders "$OUT"
for PL in yt ig; do
  PYTHONUTF8=1 python build-frames.py "$PL" > build-$PL.log 2>&1 || { echo "BUILD FAIL $PL"; tail -5 build-$PL.log; exit 1; }
  if [ "$PL" = yt ]; then
    $HF check > check.log 2>&1; grep -E "✗|Check (passed|failed)" check.log | head -8
    $HF snapshot --at "$SNAP" 2>&1 | grep -i "contact" | sed 's/.*\(C:.*jpg\).*/SNAP \1/'
  fi
  $HF render --quality high --output "renders/chai-bot-$NN-$PL.mp4" > render-$PL.log 2>&1 || { echo "RENDER FAIL $PL"; tail -5 render-$PL.log; exit 1; }
  cp "renders/chai-bot-$NN-$PL.mp4" "$OUT/"
  echo "OK $PL $(ffprobe -v error -show_entries format=duration -of csv=p=0 renders/chai-bot-$NN-$PL.mp4)s"
done
echo DONE
