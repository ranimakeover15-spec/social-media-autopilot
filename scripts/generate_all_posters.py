"""
Batch Generator for 3 Canva-Grade Luxury Agency Posters and 9:16 Video Reels:
1. Karwa Chauth Bridal & Glow Combo
2. Diwali Mega Transformation Package
3. Hydra Facial & Hair Spa Offer
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple, Dict, Any
from PIL import Image, ImageDraw, ImageFont
import subprocess

# Enforce UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent

class LuxuryPosterEngine:
    WIDTH = 1080
    HEIGHT = 1920

    def __init__(self):
        self._load_fonts()

    def _load_fonts(self):
        def try_font(font_names: List[str], size: int) -> ImageFont.FreeTypeFont:
            for name in font_names:
                try:
                    return ImageFont.truetype(name, size)
                except Exception:
                    pass
            return ImageFont.load_default()

        self.font_brand = try_font(["georgiab.ttf", "Georgia-Bold.ttf", "timesbd.ttf", "arialbd.ttf"], 38)
        self.font_sub = try_font(["arialbd.ttf", "Arial-Bold.ttf", "calibrib.ttf"], 22)
        self.font_badge = try_font(["arialbd.ttf", "Arial-Bold.ttf", "calibrib.ttf"], 32)
        self.font_price = try_font(["georgiab.ttf", "Georgia-Bold.ttf", "timesbd.ttf"], 82)
        self.font_item = try_font(["georgiab.ttf", "Georgia-Bold.ttf", "timesbd.ttf"], 32)
        self.font_desc = try_font(["arialbd.ttf", "Arial-Bold.ttf", "calibrib.ttf"], 20)
        self.font_phone = try_font(["arialbd.ttf", "Arial-Bold.ttf", "calibrib.ttf"], 44)
        self.font_addr = try_font(["arialbd.ttf", "Arial-Bold.ttf", "calibrib.ttf"], 21)

    def generate_poster(
        self,
        theme_bg: Tuple[int, int, int],
        card_bg: Tuple[int, int, int],
        accent_color: Tuple[int, int, int],
        badge_title: str,
        combo_title: str,
        price_main: str,
        price_strike: str,
        discount_text: str,
        services: List[Tuple[str, str]],
        urgency_text: str,
        urgency_bg: Tuple[int, int, int],
        output_png: Path
    ) -> Path:
        canvas = Image.new("RGB", (self.WIDTH, self.HEIGHT), theme_bg)
        draw = ImageDraw.Draw(canvas)

        # ----------------------------------------------------------------------
        # LAYER 1: BRAND HEADER (Y: 0 -> 175)
        # ----------------------------------------------------------------------
        draw.rectangle([0, 0, self.WIDTH, 175], fill=(16, 12, 22))
        draw.line([(0, 175), (self.WIDTH, 175)], fill=accent_color, width=4)

        # YouTube / Studio Official Badge
        draw.rounded_rectangle([45, 55, 105, 95], radius=10, fill=(255, 0, 0))
        draw.polygon([(65, 65), (65, 85), (88, 75)], fill=(255, 255, 255))

        draw.text((120, 48), "RANI MAKEOVER & BEAUTY LOUNGE", font=self.font_brand, fill=accent_color)
        draw.text((120, 108), "EXCLUSIVE FESTIVE BEAUTY & MAKEUP STUDIO", font=self.font_sub, fill=(255, 255, 255))

        # ----------------------------------------------------------------------
        # LAYER 2: HERO FESTIVE BADGE (Y: 195 -> 280)
        # ----------------------------------------------------------------------
        draw.rounded_rectangle([80, 195, 1000, 280], radius=40, fill=accent_color)
        # Center badge text approximately
        draw.text((115, 222), badge_title, font=self.font_badge, fill=(12, 10, 16))

        # ----------------------------------------------------------------------
        # LAYER 3: MEGA PRICE HERO CARD (Y: 300 -> 485)
        # ----------------------------------------------------------------------
        draw.rounded_rectangle([85, 300, 995, 485], radius=25, fill=card_bg, outline=accent_color, width=3)
        draw.text((125, 322), combo_title, font=self.font_sub, fill=(255, 215, 0))
        draw.text((125, 362), price_main, font=self.font_price, fill=(255, 255, 255))
        draw.text((680, 380), price_strike, font=self.font_badge, fill=(180, 150, 150))
        draw.line([(675, 400), (825, 400)], fill=(255, 40, 40), width=4)
        draw.text((685, 425), discount_text, font=self.font_sub, fill=(50, 225, 100))

        # ----------------------------------------------------------------------
        # LAYER 4: 5-STAR SERVICE CARDS (Y: 505 -> 1325)
        # ----------------------------------------------------------------------
        y_pos = 505
        for title, desc in services[:5]:
            draw.rounded_rectangle([85, y_pos, 995, y_pos + 135], radius=18, fill=card_bg, outline=accent_color, width=2)
            draw.rounded_rectangle([85, y_pos, 100, y_pos + 135], radius=4, fill=accent_color)
            draw.text((125, y_pos + 20), title, font=self.font_item, fill=(255, 215, 0))
            draw.text((125, y_pos + 78), desc, font=self.font_desc, fill=(240, 240, 240))

            # Vector Gold Circle Checkmark
            draw.ellipse([925, y_pos + 42, 970, y_pos + 87], fill=accent_color)
            draw.line([(937, y_pos + 65), (946, y_pos + 75)], fill=(12, 10, 16), width=4)
            draw.line([(946, y_pos + 75), (960, y_pos + 52)], fill=(12, 10, 16), width=4)
            y_pos += 155

        # ----------------------------------------------------------------------
        # LAYER 5: URGENCY & LIMITED SLOTS RIBBON (Y: 1335 -> 1415)
        # ----------------------------------------------------------------------
        draw.rounded_rectangle([120, 1335, 960, 1415], radius=25, fill=urgency_bg, outline=(255, 215, 0), width=2)
        draw.text((160, 1360), urgency_text, font=self.font_sub, fill=(255, 255, 255))

        # ----------------------------------------------------------------------
        # LAYER 6: CONTACT FOOTER (Y: 1445 -> 1920)
        # ----------------------------------------------------------------------
        draw.rectangle([0, 1445, self.WIDTH, self.HEIGHT], fill=(12, 10, 16))
        draw.line([(0, 1445), (self.WIDTH, 1445)], fill=accent_color, width=4)

        # Phone Handset Graphic in Accent Circle
        draw.ellipse([75, 1495, 170, 1590], fill=accent_color)
        draw.rounded_rectangle([102, 1520, 118, 1565], radius=6, fill=(12, 10, 16))
        draw.rounded_rectangle([127, 1520, 143, 1565], radius=6, fill=(12, 10, 16))
        draw.rounded_rectangle([110, 1530, 135, 1555], radius=4, fill=(12, 10, 16))

        draw.text((195, 1492), "+91 9334668807", font=self.font_phone, fill=(255, 255, 255))
        draw.text((195, 1555), "CALL / WHATSAPP FOR APPOINTMENTS", font=self.font_sub, fill=accent_color)

        # Location Pin
        draw.ellipse([75, 1630, 105, 1660], fill=(255, 40, 40))
        draw.polygon([(80, 1653), (100, 1653), (90, 1673)], fill=(255, 40, 40))
        draw.ellipse([85, 1640, 95, 1650], fill=(255, 255, 255))
        draw.text((125, 1628), "Shop No. G-38, RC Plaza, Kirari Chowk, Nangloi, Delhi - 110086", font=self.font_addr, fill=(255, 255, 255))

        # Socials
        draw.rounded_rectangle([75, 1715, 1005, 1815], radius=20, fill=card_bg, outline=accent_color, width=2)
        draw.text((120, 1748), "Instagram: @Lovelyrani53   |   YouTube: Rani Makeover", font=self.font_sub, fill=accent_color)

        output_png.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(output_png)
        return output_png

    def render_reel(self, poster_path: Path, output_video: Path, duration: int = 15):
        vf = "zoompan=z='min(zoom+0.0004,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=450:s=1080x1920:fps=30"
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(poster_path),
            "-f", "lavfi", "-i", f"sine=frequency=528:duration={duration}",
            "-filter_complex", vf,
            "-c:v", "libx264", "-t", str(duration),
            "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            str(output_video)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def main():
    print("=" * 80)
    print("🎨 GENERATING 3 CANVA-GRADE LUXURY FESTIVE POSTERS & REELS")
    print("=" * 80)

    engine = LuxuryPosterEngine()
    out_dir = BASE_DIR / "content_vault"
    posters_dir = BASE_DIR / "posters_showcase"
    out_dir.mkdir(parents=True, exist_ok=True)
    posters_dir.mkdir(parents=True, exist_ok=True)

    packages = [
        {
            "name": "01_karwa_chauth_bridal_glow",
            "badge": "✨ KARWA CHAUTH BRIDAL & GLOW COMBO ✨",
            "combo": "COMPLETE 5-IN-1 BRIDAL MOON GLOW PACKAGE",
            "price_main": "ONLY ₹999/-",
            "price_strike": "₹3,499/-",
            "discount": "(72% OFF)",
            "theme_bg": (22, 10, 18),      # Deep Royal Maroon
            "card_bg": (32, 14, 26),
            "accent": (212, 175, 55),       # Royal Gold
            "urgency_bg": (180, 20, 50),
            "urgency": "LIMITED SLOTS FOR KARWA CHAUTH • PRE-BOOKING OPEN",
            "services": [
                ("1. 24K GOLD BRIDAL FACIAL", "Instant moon glow, deep tan removal & glass skin radiance"),
                ("2. HD EYEBROW ARCH STYLING", "Festive bridal brow shaping & crystal clean forehead"),
                ("3. BRIDAL HAND POLISHING & D-TAN", "Silky soft skin with long-lasting bright festive shine"),
                ("4. HERBAL NOURISHING HAIR SPA", "Deep scalp therapy, frizz-free shine & soft glossy hair"),
                ("5. FULL FACE GLOW BLEACH & CARE", "Painless upper lips care & mirror finish clarity")
            ]
        },
        {
            "name": "02_diwali_mega_transformation",
            "badge": "🪔 DIWALI MEGA TRANSFORMATION PACKAGE 🪔",
            "combo": "FULL BODY & GLOW FESTIVE MAKEOVER",
            "price_main": "ONLY ₹1,499/-",
            "price_strike": "₹4,999/-",
            "discount": "(70% OFF)",
            "theme_bg": (14, 12, 26),      # Deep Festive Navy-Purple
            "card_bg": (24, 18, 40),
            "accent": (255, 185, 20),      # Bright Warm Gold
            "urgency_bg": (200, 30, 30),
            "urgency": "DIWALI SPECIAL SLOTS FAST FILLING • BOOK TODAY",
            "services": [
                ("1. O3+ BRIGHTENING GLOW FACIAL", "Super active glow, melanin control & bridal brightness"),
                ("2. KERATIN HAIR SPA NOURISHMENT", "Damage repair, intense moisture & silky smooth texture"),
                ("3. RICA BUTTER FULL ARMS WAXING", "100% smooth, painless waxing ready for ethnic outfits"),
                ("4. BACK & NECK ANTI-TAN POLISHING", "Crystal clean shine for festive deep-cut blouses"),
                ("5. FESTIVE PARTY GLAM LOOK", "HD touchup, brow shaping & lip hydration finish")
            ]
        },
        {
            "name": "03_hydra_facial_and_hair_spa",
            "badge": "💧 HYDRA FACIAL & LUXURY HAIR SPA OFFER 💆‍♀️",
            "combo": "7-STEP CLINICAL GLOW & HAIR REPAIR COMBO",
            "price_main": "ONLY ₹799/-",
            "price_strike": "₹2,999/-",
            "discount": "(73% OFF)",
            "theme_bg": (10, 20, 16),      # Velvet Emerald Forest
            "card_bg": (16, 32, 26),
            "accent": (50, 225, 150),      # Emerald Mint Gold
            "urgency_bg": (160, 30, 60),
            "urgency": "LIMITED WEEKEND SLOTS • ADVANCE BOOKING OPEN",
            "services": [
                ("1. 7-STEP HYDRA VACUUM FACIAL", "Deep blackhead removal, pore shrinking & oxygen water blast"),
                ("2. HYALURONIC ACID SERUM INFUSION", "Instant 72-hour moisture lock & mirror gloss glass skin"),
                ("3. L'OREAL PROFESSIONAL HAIR SPA", "Intense hair spa cream bath, scalp massage & steam therapy"),
                ("4. HAIR SPLIT-ENDS TRIMMING", "Clean bouncy look, split-end removal & shine serum finish"),
                ("5. PAINLESS THREADING & UPPER LIPS", "Gentle precision grooming & smooth makeup base prep")
            ]
        }
    ]

    for pkg in packages:
        png_path = posters_dir / f"{pkg['name']}.png"
        mp4_path = out_dir / f"{pkg['name']}.mp4"

        print(f"\n🎨 Drawing Canva-Grade Poster: {pkg['badge']}...")
        engine.generate_poster(
            theme_bg=pkg["theme_bg"],
            card_bg=pkg["card_bg"],
            accent_color=pkg["accent"],
            badge_title=pkg["badge"],
            combo_title=pkg["combo"],
            price_main=pkg["price_main"],
            price_strike=pkg["price_strike"],
            discount_text=pkg["discount"],
            services=pkg["services"],
            urgency_text=pkg["urgency"],
            urgency_bg=pkg["urgency_bg"],
            output_png=png_path
        )
        print(f"✅ Poster Saved: {png_path}")

        print(f"🎬 Rendering 9:16 Video Reel...")
        engine.render_reel(poster_path=png_path, output_video=mp4_path, duration=15)
        size_mb = mp4_path.stat().st_size / (1024 * 1024)
        print(f"✅ Video Reel Saved to Vault: {mp4_path.name} ({size_mb:.2f} MB)")

    print("\n" + "=" * 80)
    print("🎉 ALL 3 CANVA-GRADE LUXURY POSTERS & REELS GENERATED!")
    print(f"📁 Posters Showcase: {posters_dir}")
    print(f"📁 Video Vault (Auto-Pilot Ready): {out_dir}")
    print("=" * 80)

if __name__ == "__main__":
    main()
