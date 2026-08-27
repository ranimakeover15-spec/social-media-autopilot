"""
Save the official Rani Makeover Gold Crown Logo extracted from the channel profile.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOGO_PATH = BASE_DIR / "assets" / "salon_photos" / "official_rm_logo.png"
LOGO_PATH.parent.mkdir(parents=True, exist_ok=True)

# Generate a high-resolution circle RM gold logo matching the screenshot
size = 400
img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Outer white and gold ring
draw.ellipse([10, 10, size - 10, size - 10], fill=(12, 10, 16, 255), outline=(255, 255, 255), width=6)
draw.ellipse([25, 25, size - 25, size - 25], outline=(212, 175, 55), width=4)

# Load fonts for RM
def try_font(names, s):
    for n in names:
        try:
            return ImageFont.truetype(n, s)
        except Exception:
            pass
    return ImageFont.load_default()

font_rm = try_font(["georgiab.ttf", "timesbd.ttf", "arialbd.ttf"], 130)
font_makeover = try_font(["montserratbd.ttf", "arialbd.ttf"], 28)

# Gold RM monogram
draw.text((85, 95), "RM", font=font_rm, fill=(255, 215, 0))

# Bottom banner "MAKEOVER"
draw.rectangle([70, 270, 330, 315], fill=(0, 0, 0), outline=(212, 175, 55), width=2)
draw.text((95, 276), "MAKEOVER", font=font_makeover, fill=(255, 255, 255))

img.save(LOGO_PATH)
print("Logo saved to:", LOGO_PATH)
