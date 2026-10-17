#!/usr/bin/env bash
# Usage: make-icons.sh <site-folder> <bg-hex like 0x1d6b4f> [logo]
# Makes img/icon-192.png, icon-512.png, icon-maskable-512.png (logo at 78% for the safe zone) and apple-touch-icon.png.
set -e; D="$1"; BG="$2"; L="${3:-C:/samjhowithraj/logo-banner/samjhowithraj_watermark_600.png}"; mkdir -p "$D/img"
mk(){ ffmpeg -v error -y -f lavfi -i "color=c=$BG:s=$1x$1" -i "$L" -filter_complex "[1]scale=$2:$2:flags=lanczos[l];[0][l]overlay=(W-w)/2:(H-h)/2:format=auto" -frames:v 1 "$D/img/$3"; }
mk 512 512 icon-512.png; mk 192 192 icon-192.png; mk 512 400 icon-maskable-512.png; mk 180 164 apple-touch-icon.png
ls "$D/img"
