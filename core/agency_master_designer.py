"""
👑 RANI MAKEOVER — 100% STANDARDIZED PRO AGENCY DESIGN ENGINE
Strict Rules:
1. Zero photo obstruction: Hero photo is 100% clean, un-cluttered with zero floating rectangles over model.
2. Organic flowing curved waves matching top agency salon templates.
3. 2 Floating circular insets with thick white borders.
4. Elegant Serif typography ("Rani Makeover" / "Beauty Lounge").
5. Real vector icons for Phone, Instagram, and Location.
6. Balanced 2-column layout for Contact and Services.
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont, ImageOps
import subprocess

# Enforce UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent

class ProAgencyDesigner:
    WIDTH = 1080
    HEIGHT = 1920

    # Color Palette (Matching Luxury Salon Reference)
    MAGENTA_PRIMARY = (216, 0, 115)     # #D80073
    MAGENTA_DEEP = (160, 0, 80)         # #A00050
    PLUM_DARK = (45, 4, 32)             # #2D0420
    BG_VELVET = (20, 4, 16)             # #140410 Deep Velvet Black-Plum
    GOLD_ACCENT = (255, 215, 0)         # #FFD700
    PURE_WHITE = (255, 255, 255)
    SOFT_WHITE = (245, 245, 245)
    MUTED_TEXT = (210, 200, 205)

    def __init__(self):
        self._load_fonts()

    def _load_fonts(self):
        def try_font(font_names, size):
            for name in font_names:
                try:
                    return ImageFont.truetype(name, size)
                except Exception:
                    pass
            return ImageFont.load_default()

        self.font_brand_title = try_font(["georgiab.ttf", "Georgia-Bold.ttf", "timesbd.ttf"], 90)
        self.font_brand_sub = try_font(["georgiai.ttf", "Georgia-Italic.ttf", "timesi.ttf"], 75)
        self.font_tagline = try_font(["georgiai.ttf", "Georgia-Italic.ttf", "arial.ttf"], 26)
        self.font_badge = try_font(["arialbd.ttf", "Arial-Bold.ttf"], 28)
        self.font_pill = try_font(["arialbd.ttf", "Arial-Bold.ttf"], 38)
        self.font_service_item = try_font(["georgia.ttf", "Georgia.ttf", "arialbd.ttf"], 36)
        self.font_contact_bold = try_font(["arialbd.ttf", "Arial-Bold.ttf"], 34)
        self.font_addr = try_font(["arial.ttf", "Arial.ttf"], 23)

    # --------------------------------------------------------------------------
    # REAL VECTOR ICONS (Precision Geometric Rendering)
    # --------------------------------------------------------------------------
    def draw_phone_icon(self, draw: ImageDraw.Draw, x: int, y: int, radius: int = 22):
        """Telephone handset vector."""
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=self.GOLD_ACCENT)
        draw.rounded_rectangle([x - 10, y - 9, x - 4, y + 9], radius=3, fill=(20, 4, 16))
        draw.rounded_rectangle([x + 4, y - 9, x + 10, y + 9], radius=3, fill=(20, 4, 16))
        draw.rounded_rectangle([x - 7, y - 3, x + 7, y + 5], radius=2, fill=(20, 4, 16))

    def draw_instagram_icon(self, draw: ImageDraw.Draw, x: int, y: int, radius: int = 22):
        """Official Instagram vector."""
        draw.rounded_rectangle([x - radius, y - radius, x + radius, y + radius], radius=11, fill=self.MAGENTA_PRIMARY)
        draw.rounded_rectangle([x - 14, y - 14, x + 14, y + 14], radius=6, outline=self.PURE_WHITE, width=3)
        draw.ellipse([x - 6, y - 6, x + 6, y + 6], outline=self.PURE_WHITE, width=3)
        draw.ellipse([x + 7, y - 8, x + 10, y - 5], fill=self.PURE_WHITE)

    def draw_location_icon(self, draw: ImageDraw.Draw, x: int, y: int, radius: int = 22):
        """Location Pin vector."""
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=(235, 45, 65))
        draw.ellipse([x - 9, y - 12, x + 9, y + 6], fill=self.PURE_WHITE)
        draw.polygon([(x - 7, y + 1), (x + 7, y + 1), (x, y + 13)], fill=self.PURE_WHITE)
        draw.ellipse([x - 4, y - 6, x + 4, y + 1], fill=(235, 45, 65))

    def create_agency_master_poster(
        self,
        brand_line_1: str = "Rani Makeover",
        brand_line_2: str = "Beauty Lounge",
        tagline: str = "Beauty is being comfortable in your own skin. Pamper it well.",
        offer_highlight: Optional[str] = "Festive Special Offer • Up to 70% OFF",
        services: Optional[List[str]] = None,
        phone: str = "+91 9334668807",
        instagram: str = "@Lovelyrani53",
        address_line_1: str = "Shop No. G-38, RC Plaza,",
        address_line_2: str = "Kirari Chowk, Nangloi,",
        address_line_3: str = "Delhi - 110086",
        output_png: Optional[Path] = None
    ) -> Path:
        if services is None:
            services = [
                "Make up & Bridal",
                "Hydra Face Treatment",
                "Keratin Hair Spa",
                "Luxury Skincare",
                "Full Body Glow Waxing"
            ]

        # 1. Base Canvas
        canvas = Image.new("RGBA", (self.WIDTH, self.HEIGHT), self.BG_VELVET + (255,))
        draw = ImageDraw.Draw(canvas)

        photo_dir = BASE_DIR / "assets" / "salon_photos"
        hero_img_path = photo_dir / "facial_hero.jpg"
        hair_img_path = photo_dir / "hair_wash.jpg"
        nail_img_path = photo_dir / "nail_art.jpg"

        # ----------------------------------------------------------------------
        # 2. TOP HERO PHOTO (100% Clean, NO floating boxes on face)
        # ----------------------------------------------------------------------
        if hero_img_path.exists():
            hero_img = Image.open(hero_img_path).convert("RGBA")
            hero_img = ImageOps.fit(hero_img, (self.WIDTH, 900), method=Image.Resampling.LANCZOS)
            canvas.paste(hero_img, (0, 0))

        # ----------------------------------------------------------------------
        # 3. ORGANIC FLUID WAVE FRAMING (Reference S-Curves)
        # ----------------------------------------------------------------------
        overlay = Image.new("RGBA", (self.WIDTH, self.HEIGHT), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)

        # Top Accent Header Curve (Zero obstruction to face)
        odraw.polygon([
            (0, 0), (self.WIDTH, 0), (self.WIDTH, 120),
            (700, 80), (350, 140), (0, 50)
        ], fill=self.MAGENTA_PRIMARY + (240,))

        # Middle Flowing Wave Layers
        odraw.polygon([
            (0, 710), (360, 670), (740, 770), (self.WIDTH, 620),
            (self.WIDTH, 1020), (600, 930), (0, 1060)
        ], fill=self.MAGENTA_PRIMARY + (245,))

        odraw.polygon([
            (0, 780), (440, 750), (820, 830), (self.WIDTH, 700),
            (self.WIDTH, self.HEIGHT), (0, self.HEIGHT)
        ], fill=self.BG_VELVET + (255,))

        canvas = Image.alpha_composite(canvas, overlay)
        draw = ImageDraw.Draw(canvas)

        # ----------------------------------------------------------------------
        # 4. CIRCULAR INSET 1: Hair Wash (Left - Diameter 470px + 10px White Border)
        # ----------------------------------------------------------------------
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

        # ----------------------------------------------------------------------
        # 5. CIRCULAR INSET 2: Nail Art (Center Overlapping - Diameter 350px + 10px Border)
        # ----------------------------------------------------------------------
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

        # ----------------------------------------------------------------------
        # 6. RIGHT SIDE: LUXURY BRAND TITLE & TAGLINE
        # ----------------------------------------------------------------------
        shadow = 3
        draw.text((580 + shadow, 890 + shadow), brand_line_1, font=self.font_brand_title, fill=(0, 0, 0))
        draw.text((580, 890), brand_line_1, font=self.font_brand_title, fill=self.PURE_WHITE)

        draw.text((580 + shadow, 985 + shadow), brand_line_2, font=self.font_brand_sub, fill=(0, 0, 0))
        draw.text((580, 985), brand_line_2, font=self.font_brand_sub, fill=self.PURE_WHITE)

        # Elegant Tagline
        draw.text((560, 1115), tagline[:38], font=self.font_tagline, fill=self.MUTED_TEXT)
        draw.text((560, 1148), tagline[38:76], font=self.font_tagline, fill=self.MUTED_TEXT)

        # Optional Offer Badge (Nestled neatly in typography area, NEVER on face)
        if offer_highlight:
            draw.rounded_rectangle([560, 1200, 1020, 1260], radius=15, fill=self.PLUM_DARK, outline=self.GOLD_ACCENT, width=2)
            draw.text((585, 1215), offer_highlight, font=self.font_badge, fill=self.GOLD_ACCENT)

        # ----------------------------------------------------------------------
        # 7. MAGENTA PILL BUTTONS ("Book Now" & "Our Service")
        # ----------------------------------------------------------------------
        # Button 1 (Left)
        draw.rounded_rectangle([75, 1370, 440, 1465], radius=45, fill=self.MAGENTA_PRIMARY)
        draw.text((135, 1394), "Book Now", font=self.font_pill, fill=self.PURE_WHITE)

        # Button 2 (Right)
        draw.rounded_rectangle([610, 1370, 1015, 1465], radius=45, fill=self.MAGENTA_PRIMARY)
        draw.text((660, 1394), "Our Service", font=self.font_pill, fill=self.PURE_WHITE)

        # ----------------------------------------------------------------------
        # 8. SERVICES LIST (Right Column - Clean, Professional Typography)
        # ----------------------------------------------------------------------
        y_srv = 1500
        for s in services:
            draw.text((630 + 2, y_srv + 2), s, font=self.font_service_item, fill=(0, 0, 0))
            draw.text((630, y_srv), s, font=self.font_service_item, fill=self.SOFT_WHITE)
            y_srv += 66

        # ----------------------------------------------------------------------
        # 9. CONTACT INFORMATION WITH REAL VECTOR ICONS (Left Column)
        # ----------------------------------------------------------------------
        # A) Phone Icon & Helpline
        self.draw_phone_icon(draw, 105, 1525, radius=22)
        draw.text((145 + 2, 1508 + 2), phone, font=self.font_contact_bold, fill=(0, 0, 0))
        draw.text((145, 1508), phone, font=self.font_contact_bold, fill=self.GOLD_ACCENT)

        # B) Instagram Icon & Handle
        self.draw_instagram_icon(draw, 105, 1590, radius=22)
        draw.text((145 + 2, 1572 + 2), instagram, font=self.font_contact_bold, fill=(0, 0, 0))
        draw.text((145, 1572), instagram, font=self.font_contact_bold, fill=self.PURE_WHITE)

        # C) Location Icon & Address
        self.draw_location_icon(draw, 105, 1670, radius=22)
        draw.text((145, 1635), address_line_1, font=self.font_addr, fill=self.PURE_WHITE)
        draw.text((145, 1668), address_line_2, font=self.font_addr, fill=self.MUTED_TEXT)
        draw.text((145, 1701), address_line_3, font=self.font_addr, fill=self.MUTED_TEXT)

        # Convert to RGB
        final_canvas = Image.new("RGB", (self.WIDTH, self.HEIGHT), (20, 4, 16))
        final_canvas.paste(canvas, (0, 0), mask=canvas.split()[3])

        if output_png is None:
            output_png = BASE_DIR / "posters_showcase" / "pro_agency_master_poster.png"

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

# Global designer instance
pro_designer = ProAgencyDesigner()
