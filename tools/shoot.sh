#!/bin/bash
# usage: shoot_v2.sh name url [mobile|desktop] [height]
# Mobile uses a 390px iframe harness (headless Chrome cannot go below ~500px windows). Needs `python3 -m http.server 8765` in the site dir and _h.html there.
C="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT=${SHOTS_OUT:-/Users/viet.vk/Projects/VietVk/ChessCoach/iOS/.orchestra/shots/WEB-SITE-V2}
n=$1; u=$2; mode=$3; h=${4:-900}
if [ "$mode" = mobile ]; then
  "$C" --headless=new --disable-gpu --hide-scrollbars --force-prefers-reduced-motion --virtual-time-budget=9000 --window-size=500,$h --screenshot="$OUT/$n.png" "http://localhost:8765/_h.html?w=390&h=$h&u=$u" >/dev/null 2>&1
  python3 -c "
from PIL import Image
p='$OUT/$n.png'; im=Image.open(p); im.crop((0,0,390,im.height)).save(p)"
else
  "$C" --headless=new --disable-gpu --hide-scrollbars --force-prefers-reduced-motion --virtual-time-budget=9000 --window-size=1500,$h --screenshot="$OUT/$n.png" "http://localhost:8765/_h.html?w=1440&h=$h&u=$u" >/dev/null 2>&1
  python3 -c "
from PIL import Image
p='$OUT/$n.png'; im=Image.open(p); im.crop((0,0,1440,im.height)).save(p)"
fi
