#!/usr/bin/env bash
set -euo pipefail

cd /home/ianlwterry/cyberdeck/aegis-os
/usr/bin/con2fbmap 1 1 2>/dev/null || true
/usr/bin/setfont /usr/share/consolefonts/Lat7-Terminus12x6.psf.gz 2>/dev/null || true

clear
python scripts/clear_fb.py 2>/tmp/aegis-clear.log || true
python scripts/show_splash_fb.py 2>/tmp/aegis-splash.log || true
sleep 4

python scripts/clear_fb.py 2>/tmp/aegis-clear.log || true
printf '\033c'
clear

echo "================================"
echo "            AEGIS OS"
echo "        v0.1.0-alpha"
echo "================================"
echo
echo "Loading Knowledge..."
sleep 1
echo "Loading Field Journal..."
sleep 1
echo "Loading Inventory..."
sleep 1
echo "Checking Hardware..."
sleep 1
echo
echo "Mission Status: READY"
sleep 3

python scripts/clear_fb.py 2>/tmp/aegis-clear.log || true
printf '\033c'
clear

exec /home/ianlwterry/cyberdeck/aegis-os/.venv/bin/aegis