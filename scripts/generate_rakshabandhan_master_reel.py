"""
Raksha Bandhan Luxury Agency Poster & Reel Generator.
Features:
- Real vector graphic icons for Phone, Instagram, Location Pin, and Crown
- Ultra-clear bold typography with 3D drop-shadows
- Modern flowing wave frame with salon hero photo & circular insets
- Mega Raksha Bandhan Offer & Pricing
"""

import os
import sys
import math
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import subprocess

# Enforce UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent

class RakshaBandhanAgencyEngine:
    WIDTH = 1080
    HEIGHT = 1920

    # Color Palette
    MAGENTA_ACCENT = (225, 0, 115)     # #E10073 Vivid Magenta
    DEEP_WINE = (50, 4, 35)            # #320423
    BG_DARK_PLUM = (18, 2, 14)         # #12020E Luxury Dark Velvet
    GOLD_ACCENT = (255, 215, 0)        # #FFD700
    ROYAL_GOLD = (212, 175, 55)        # #D4AF37
    PURE_WHITE = (255, 255, 255)
    SOFT_WHITE = (245, 245, 245)
    LIGHT_GREY = (220, 210, 215)

    def __init__(self):
        self._load_fonts()
        self._ensure_photos()

    def _load_fonts(self):
        def try_font(font_names, size):
            for name in font_names:
                try:
                    return ImageFont.truetype(name, size)
                except Exception:
                    pass
            return ImageFont.load_default()

        self.font_brand_huge = try_font(["georgiab.ttf", "Georgia-Bold.ttf", "timesbd.ttf"], 88)
        self.font_brand_sub = try_font(["georgiai.ttf", "Georgia-Italic.ttf", "timesi.ttf"], 72)
        self.font_badge_offer = try_font(["arialbd.ttf", "Arial-Bold.ttf", "calibrib.ttf"], 36)
        self.font_price_hero = try_font(["georgiab.ttf", "Georgia-Bold.ttf", "timesbd.ttf"], 68)
        self.font_pill = try_font(["arialbd.ttf", "Arial-Bold.ttf", "calibrib.ttf"], 42)
        self.font_service_item = try_font(["georgiab.ttf", "Georgia-Bold.ttf", "arialbd.ttf"], 38)
        self.font_contact_bold = try_font(["arialbd.ttf", "Arial-Bold.ttf"], 36)
        self.font_addr = try_font(["arialbd.ttf", "Arial-Bold.ttf"], 25)

    def _ensure_photos(self):
        photo_dir = BASE_DIR / "assets" / "salon_photos"
        photo_dir.mkdir(parents=True, exist_ok=True)
        images = {
            "facial_hero.jpg": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=1600&auto=format&fit=crop&q=85",
            "hair_wash.jpg": "https://images.unsplash.com/photo-1560066984-138dadb4c035?w=800&auto=format&fit=crop&q=85",
            "nail_art.jpg": "https://images.unsplash.com/photo-1632345031435-8727f6897d53?w=800&auto=format&fit=crop&q=85"
        }
        for name, url in images.items():
            dest = photo_dir / name
            if not dest.exists():
                try:
                    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(req, timeout=15) as resp, open(dest, "wb") as f:
                        f.write(resp.read())
                except Exception:
                    pass

    # --------------------------------------------------------------------------
    # REAL VECTOR ICON DRAWING FUNCTIONS
    # --------------------------------------------------------------------------
    def draw_phone_icon(self, draw: ImageDraw.Draw, x: int, y: int, radius: int = 24):
        """Draws a real luxury telephone handset vector icon inside a circle."""
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=self.GOLD_ACCENT)
        # Vector Phone receiver shape in dark contrast
        # Left ear, right ear, and connecting handle
        draw.rounded_rectangle([x - 12, y - 10, x - 5, y + 10], radius=3, fill=(18, 2, 14))
        draw.rounded_rectangle([x + 5, y - 10, x + 12, y + 10], radius=3, fill=(18, 2, 14))
        draw.rounded_rectangle([x - 8, y - 4, x + 8, y + 6], radius=2, fill=(18, 2, 14))

    def draw_instagram_icon(self, draw: ImageDraw.Draw, x: int, y: int, radius: int = 24):
        """Draws a real official Instagram camera gradient vector icon."""
        # Gradient magenta-gold outer rounded square
        draw.rounded_rectangle([x - radius, y - radius, x + radius, y + radius], radius=12, fill=self.MAGENTA_ACCENT)
        # Inner white camera border
        draw.rounded_rectangle([x - 15, y - 15, x + 15, y + 15], radius=7, outline=self.PURE_WHITE, width=3)
        # Center lens circle
        draw.ellipse([x - 7, y - 7, x + 7, y + 7], outline=self.PURE_WHITE, width=3)
        # Flash dot
        draw.ellipse([x + 8, y - 9, x + 11, y - 6], fill=self.PURE_WHITE)

    def draw_location_icon(self, draw: ImageDraw.Draw, x: int, y: int, radius: int = 24):
        """Draws a real Location Pin vector icon."""
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=(240, 40, 60))
        # White Pin head
        draw.ellipse([x - 10, y - 13, x + 10, y + 7], fill=self.PURE_WHITE)
        # Pin bottom triangle
        draw.polygon([(x - 8, y + 2), (x + 8, y + 2), (x, y + 14)], fill=self.PURE_WHITE)
        # Inner hole
        draw.ellipse([x - 4, y - 7, x + 4, y + 1], fill=(240, 40, 60))

    def draw_crown_badge(self, draw: ImageDraw.Draw, x: int, y: int, size: int = 40):
        """Draws a real Royal Crown vector icon for brand title."""
        draw.polygon([
            (x, y + size), (x + size, y + size),
            (x + size, y + 12), (x + size * 0.75, y + 22),
            (x + size * 0.5, y + 5), (x + size * 0.25, y + 22),
            (x, y + 12)
        ], fill=self.GOLD_ACCENT)
        # Jewels on crown peaks
        draw.ellipse([x - 2, y + 8, x + 4, y + 14], fill=self.PURE_WHITE)
        draw.ellipse([x + size * 0.5 - 3, y + 1, x + size * 0.5 + 3, y + 7], fill=self.PURE_WHITE)
        draw.ellipse([x + size - 4, y + 8, x + size + 2, y + 14], fill=self.PURE_WHITE)

    def render_rakshabandhan_poster(
        self,
        output_png: Path = None
    ) -> Path:
        # 1. Base Canvas
        canvas = Image.new("RGBA", (self.WIDTH, self.HEIGHT), self.BG_DARK_PLUM + (255,))
        draw = ImageDraw.Draw(canvas)

        photo_dir = BASE_DIR / "assets" / "salon_photos"
        hero_img_path = photo_dir / "facial_hero.jpg"
        hair_img_path = photo_dir / "hair_wash.jpg"
        nail_img_path = photo_dir / "nail_art.jpg"

        # 2. Hero Image on top (1080x920)
        if hero_img_path.exists():
            hero_img = Image.open(hero_img_path).convert("RGBA")
            hero_img = ImageOps.fit(hero_img, (self.WIDTH, 920), method=Image.Resampling.LANCZOS)
            canvas.paste(hero_img, (0, 0))

        # 3. Organic Fluid Waves with Rich Magenta Accents
        overlay = Image.new("RGBA", (self.WIDTH, self.HEIGHT), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)

        # Top decorative wave
        odraw.polygon([
            (0, 0), (self.WIDTH, 0), (self.WIDTH, 130),
            (750, 90), (400, 150), (0, 60)
        ], fill=self.MAGENTA_ACCENT + (240,))

        # Middle flowing wave layers
        odraw.polygon([
            (0, 710), (360, 670), (720, 770), (self.WIDTH, 610),
            (self.WIDTH, 1020), (600, 930), (0, 1060)
        ], fill=self.MAGENTA_ACCENT + (245,))

        odraw.polygon([
            (0, 780), (440, 750), (820, 830), (self.WIDTH, 700),
            (self.WIDTH, self.HEIGHT), (0, self.HEIGHT)
        ], fill=self.BG_DARK_PLUM + (255,))

        canvas = Image.alpha_composite(canvas, overlay)
        draw = ImageDraw.Draw(canvas)

        # 4. Circular Inset 1: Hair Wash (Diameter 460px with thick 10px white border)
        circle_1_pos = (25, 660)
        circle_1_size = 470
        if hair_img_path.exists():
            hair_img = Image.open(hair_img_path).convert("RGB")
            hair_img = ImageOps.fit(hair_img, (circle_1_size, circle_1_size), method=Image.Resampling.LANCZOS)

            mask = Image.new("L", (circle_1_size, circle_1_size), 0)
            mdraw = ImageDraw.Draw(mask)
            mdraw.ellipse((0, 0, circle_1_size, circle_1_size), fill=255)

            draw.ellipse(
                [circle_1_pos[0] - 10, circle_1_pos[1] - 10, circle_1_pos[0] + circle_1_size + 10, circle_1_pos[1] + circle_1_size + 10],
                fill=self.PURE_WHITE
            )
            canvas.paste(hair_img, circle_1_pos, mask=mask)

        # 5. Circular Inset 2: Nail Art (Diameter 340px with thick 10px white border)
        circle_2_pos = (310, 560)
        circle_2_size = 350
        if nail_img_path.exists():
            nail_img = Image.open(nail_img_path).convert("RGB")
            nail_img = ImageOps.fit(nail_img, (circle_2_size, circle_2_size), method=Image.Resampling.LANCZOS)

            mask2 = Image.new("L", (circle_2_size, circle_2_size), 0)
            mdraw2 = ImageDraw.Draw(mask2)
            mdraw2.ellipse((0, 0, circle_2_size, circle_2_size), fill=255)

            draw.ellipse(
                [circle_2_pos[0] - 10, circle_2_pos[1] - 10, circle_2_pos[0] + circle_2_size + 10, circle_2_pos[1] + circle_2_size + 10],
                fill=self.PURE_WHITE
            )
            canvas.paste(nail_img, circle_2_pos, mask=mask2)

        # 6. Top Hero Ribbon: RAKSHA BANDHAN MEGA SPECIAL
        draw.rounded_rectangle([75, 45, 1005, 125], radius=25, fill=self.GOLD_ACCENT)
        self.draw_crown_badge(draw, 105, 62, size=35)
        draw.text((155, 62), "RAKSHA BANDHAN SPECIAL OFFER", font=self.font_badge_offer, fill=(18, 2, 14))

        # 7. RIGHT SIDE: GIANT ULTRA-BOLD "Rani Makeover & Beauty Lounge"
        shadow = 3
        draw.text((580 + shadow, 875 + shadow), "Rani", font=self.font_brand_huge, fill=(0, 0, 0))
        draw.text((580, 875), "Rani", font=self.font_brand_huge, fill=self.PURE_WHITE)

        draw.text((580 + shadow, 970 + shadow), "Makeover", font=self.font_brand_huge, fill=(0, 0, 0))
        draw.text((580, 970), "Makeover", font=self.font_brand_huge, fill=self.PURE_WHITE)

        # Hero Price Callout Badge
        draw.rounded_rectangle([560, 1090, 1030, 1220], radius=20, fill=(40, 8, 30), outline=self.GOLD_ACCENT, width=3)
        draw.text((585, 1105), "COMPLETE 5-IN-1 FESTIVE COMBO", font=self.font_addr, fill=self.GOLD_ACCENT)
        draw.text((585, 1140), "ONLY ₹599/-", font=self.font_price_hero, fill=self.PURE_WHITE)
        draw.text((885, 1152), "₹1,999", font=self.font_badge_offer, fill=(180, 150, 150))
        draw.line([(880, 1172), (990, 1172)], fill=(255, 40, 40), width=4)

        # 8. MAGENTA PILL BUTTON 1: "Book Now" (Bottom Left)
        pill_left = [75, 1370, 450, 1465]
        draw.rounded_rectangle(pill_left, radius=45, fill=self.MAGENTA_ACCENT)
        draw.text((135, 1392), "Book Now", font=self.font_pill, fill=self.PURE_WHITE)

        # 9. MAGENTA PILL BUTTON 2: "Our Service" (Bottom Right)
        pill_right = [610, 1370, 1015, 1465]
        draw.rounded_rectangle(pill_right, radius=45, fill=self.MAGENTA_ACCENT)
        draw.text((660, 1392), "Our Service", font=self.font_pill, fill=self.PURE_WHITE)

        # 10. SERVICES LIST (RIGHT COLUMN - 5 RAKSHA BANDHAN SERVICES WITH GOLD BULLETS)
        services = [
            "1. Radiance Glow Facial",
            "2. Professional Eyebrows",
            "3. Forehead Threading",
            "4. Upper Lips Care",
            "5. Full Arms Glow Waxing"
        ]
        y_srv = 1495
        for s in services:
            draw.text((630 + 2, y_srv + 2), s, font=self.font_service_item, fill=(0, 0, 0))
            draw.text((630, y_srv), s, font=self.font_service_item, fill=self.PURE_WHITE)
            y_srv += 64

        # 11. CONTACT INFO (LEFT COLUMN - WITH REAL VECTOR ICONS)
        # A) Phone Icon & Number
        self.draw_phone_icon(draw, 105, 1528, radius=24)
        draw.text((145 + 2, 1510 + 2), "+91 9334668807", font=self.font_contact_bold, fill=(0, 0, 0))
        draw.text((145, 1510), "+91 9334668807", font=self.font_contact_bold, fill=self.GOLD_ACCENT)

        # B) Instagram Icon & Handle
        self.draw_instagram_icon(draw, 105, 1593, radius=24)
        draw.text((145 + 2, 1575 + 2), "@Lovelyrani53", font=self.font_contact_bold, fill=(0, 0, 0))
        draw.text((145, 1575), "@Lovelyrani53", font=self.font_contact_bold, fill=self.PURE_WHITE)

        # C) Location Pin Icon & Full Address
        self.draw_location_icon(draw, 105, 1675, radius=24)
        draw.text((145, 1640), "Shop G-38, RC Plaza,", font=self.font_addr, fill=self.PURE_WHITE)
        draw.text((145, 1675), "Kirari Chowk, Nangloi,", font=self.font_addr, fill=self.LIGHT_GREY)
        draw.text((145, 1710), "Delhi - 110086", font=self.font_addr, fill=self.LIGHT_GREY)

        # Convert back to RGB
        final_canvas = Image.new("RGB", (self.WIDTH, self.HEIGHT), (18, 2, 14))
        final_canvas.paste(canvas, (0, 0), mask=canvas.split()[3])

        if output_png is None:
            output_png = BASE_DIR / "posters_showcase" / "raksha_bandhan_master_agency_poster.png"

        output_png.parent.mkdir(parents=True, exist_ok=True)
        final_canvas.save(output_png, quality=98)
        return output_png

    def render_reel(self, poster_path: Path, output_mp4: Path, duration: int = 15):
        vf = "zoompan=z='min(zoom+0.0004,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=450:s=1080x1920:fps=30"
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(poster_path),
            "-f", "lavfi", "-i", f"sine=frequency=432:duration={duration}",
            "-filter_complex", vf,
            "-c:v", "libx264", "-t", str(duration),
            "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            str(output_mp4)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return output_mp4

def main():
    print("=" * 80)
    print("👑 RAKSHA BANDHAN MASTER AGENCY POSTER & REEL (REAL ICONS)")
    print("=" * 80)

    engine = RakshaBandhanAgencyEngine()
    out_dir = BASE_DIR / "posters_showcase"
    vault_dir = BASE_DIR / "content_vault"

    poster_path = out_dir / "raksha_bandhan_master_agency_poster.png"
    reel_path = vault_dir / "raksha_bandhan_master_agency_reel.mp4"

    print("🎨 Rendering Raksha Bandhan Poster with REAL Vector Icons...")
    engine.render_rakshabandhan_poster(output_png=poster_path)
    print(f"✅ Poster Generated: {poster_path}")

    print("🎬 Rendering 9:16 Full HD Motion Reel...")
    engine.render_reel(poster_path, reel_path, duration=15)
    print(f"✅ 9:16 Video Reel Generated: {reel_path}")

    print("\n" + "=" * 80)
    print("🎉 RAKSHA BANDHAN MASTER THEME SUCCESSFULLY CREATED!")
    print("=" * 80)

if __name__ == "__main__":
    main()
