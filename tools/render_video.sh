#!/bin/bash
# Render <serie_dir>/v<n>.html to <serie_dir>/out/<name>.mp4 with <serie_dir>/tmp_mix<n>.wav
# Usage: tools/render_video.sh <serie_dir> <n> <name>
set -e; SD=$(cd $1 && pwd); N=$2; NAME=$3; F=$(mktemp -d); mkdir -p $SD/out
cd $SD && PAGE=v$N.html node render.js video $F
ffmpeg -v error -y -framerate 30 -i $F/f_%05d.jpg -i $SD/tmp_mix$N.wav -c:v libx264 -pix_fmt yuv420p -crf 18 -preset medium -c:a aac -b:a 192k -shortest -movflags +faststart $SD/out/$NAME.mp4
rm -rf $F $SD/tmp_mix$N.wav; echo "$NAME $(ffprobe -v error -show_entries format=duration -of csv=p=0 $SD/out/$NAME.mp4)"
