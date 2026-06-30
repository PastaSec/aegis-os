from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
logo_path = ROOT / "assets/logo/aegis-os-logo-primary.png"
out_path = ROOT / "assets/boot/aegis-boot-320x240.png"

canvas = Image.new("RGB", (320, 240), "black")
logo = Image.open(logo_path).convert("RGB")
logo.thumbnail((210, 210))

x = (320 - logo.width) // 2
y = 4
canvas.paste(logo, (x, y))

draw = ImageDraw.Draw(canvas)
text = "AEGIS OS v0.3.0-alpha"
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
except Exception:
    font = None

bbox = draw.textbbox((0, 0), text, font=font)
tw = bbox[2] - bbox[0]
draw.text(((320 - tw) // 2, 218), text, fill=(240, 232, 210), font=font)

canvas.save(out_path)
print(out_path)
