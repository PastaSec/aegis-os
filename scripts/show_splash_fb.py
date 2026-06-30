from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets/boot/aegis-boot-320x240.png"
FB = Path("/dev/fb1")

img = Image.open(IMG).convert("RGB").resize((320, 240))

buf = bytearray()
for r, g, b in img.getdata():
    rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
    buf += rgb565.to_bytes(2, "little")

FB.write_bytes(buf)
