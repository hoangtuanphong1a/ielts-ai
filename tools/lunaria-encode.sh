#!/usr/bin/env bash
# Mã hóa video Lunaria cho web.
# Dùng: tools/lunaria-encode.sh <file-goc.mp4> <pose> <look|idle|talk>
#   vd:  tools/lunaria-encode.sh ~/Downloads/seedance.mp4 stand look
# Kết quả: frontend/src/assets/lunaria/video/<pose>-<kind>.mp4 (web tự nhận)
set -euo pipefail
src="$1"; pose="$2"; kind="$3"
out="$(dirname "$0")/../frontend/src/assets/lunaria/video/${pose}-${kind}.mp4"

if [ "$kind" = "look" ]; then
  # Mọi khung hình là keyframe (-g 1): tua theo chuột tức thì, không giật
  ffmpeg -y -i "$src" -an -vf "scale=-2:min(ih\,1280)" \
    -c:v libx264 -preset slow -crf 23 -g 1 -keyint_min 1 -pix_fmt yuv420p -movflags +faststart "$out"
else
  # idle / talk: phát lặp bình thường, nén gọn
  ffmpeg -y -i "$src" -an -vf "scale=-2:min(ih\,1280)" \
    -c:v libx264 -preset slow -crf 24 -pix_fmt yuv420p -movflags +faststart "$out"
fi
echo "-> $out ($(du -h "$out" | cut -f1))"
