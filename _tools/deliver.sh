#!/usr/bin/env bash
# Copy finished files into a delivery folder WITHOUT losing older versions (same rule as money-plan-01):
# if a file of the same name is already there and differs, it is kept as <name>-vN.<ext> (next free N) first.
# Usage: bash _tools/deliver.sh "<dest-folder>" file1 [file2 ...]
# Example: bash _tools/deliver.sh "/c/Users/rajpr/Videos/YouTube Renders/ai-chai-bot-04" renders/chai-bot-04-yt.mp4 CAPTION.md
set -u
DEST="$1"; shift
mkdir -p "$DEST"
for SRC in "$@"; do
  [ -f "$SRC" ] || { echo "MISSING $SRC"; continue; }
  NAME="$(basename "$SRC")"; T="$DEST/$NAME"
  if [ -f "$T" ]; then
    if cmp -s "$SRC" "$T"; then echo "SAME $NAME"; continue; fi
    BASE="${NAME%.*}"; EXT="${NAME##*.}"; N=1
    while [ -e "$DEST/$BASE-v$N.$EXT" ]; do N=$((N + 1)); done
    mv "$T" "$DEST/$BASE-v$N.$EXT" && echo "ARCHIVED $NAME -> $BASE-v$N.$EXT"
  fi
  cp "$SRC" "$T" && echo "DELIVERED $NAME"
done
