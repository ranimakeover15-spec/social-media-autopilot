"""
Ultra-High Readability & Big Bold Typography Edition.
Modern Agency Salon Theme Generator:
- Massive, crisp, high-contrast typography
- Crystal-clear bold fonts for Beauty Salon / Rani Makeover
- Giant readable phone number & contact pill
- Prominent service list with bullet points & drop shadows
"""

import os
import sys
import math
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import subprocess

# Enforce UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent

class UltraClearDesignEngine:
    WIDTH = 1080
    HEIGHT = 1920

    # Colors
    MAGENTA_ACCENT = (225, 0, 120)     # #E10078 Bright Vivid Magenta
    MAGENTA_DARK = (160, 0, 80)        # #A00050
    WINE_PURPLE = (45, 4, 32)          # #2D0420 Deep Contrast Plum
    BG_DARK_PLUM = (18, 3, 15)         # #12030F Ultra-Dark Velvet Plum
    PURE_WHITE = (255, 255, 255)
    BRIGHT_GOLD = (255, 215, 0)        # #FFD700
    SOFT_WHITE = (245, 245, 245)
    LIGHT_GREY = (220, 210, 215)

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

        # Massive & Bold typography for crystal clear mobile reading
        self.font_brand_huge = try_font(["georgiab.ttf", "Georgia-Bold.ttf", "timesbd.ttf"], 96)
        self.font_brand_sub = try_font(["georgiai.ttf", "Georgia-Italic.ttf", "timesi.ttf"], 80)
        self.font_tagline = try_font(["georgiab.ttf", "Georgia-Bold.ttf", "arialbd.ttf"], 28)
        self.font_pill = try_font(["arialbd.ttf", "Arial-Bold.ttf", "calibrib.ttf"], 42)
        self.font_service_item = try_font(["georgiab.ttf", "Georgia-Bold.ttf", "arialbd.ttf"], 40)
        self.font_contact_big = try_font(["arialbd.ttf", "Arial-Bold.ttf"], 36)
        self.font_addr = try_font(["arialbd.ttf", "Arial-Bold.ttf"], 26)

    def render_ultra_clear_poster(
        self,
        brand_line_1: str = "Beauty",
        brand_line_2: str = "Salon",
        tagline: str = "Beauty is being comfortable in your own skin. Pamper it well.",
        services: list = None,
        phone: str = "+91 9334668807",
        instagram: str = "@Lovelyrani53",
        address: str = "Shop G-38, RC Plaza, Kirari, Delhi",
        output_png: Path = None
    ) -> Path:
        if services is None:
            services = [
                "• Make up & Bridal",
                "• Face treatment",
                "• Hair treatment",
                "• Skincare service"
            ]

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

            # 10px White outer ring
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

        # 6. RIGHT SIDE: GIANT ULTRA-BOLD "Beauty Salon" TYPOGRAPHY
        # Subtle dark text shadow for razor-sharp clarity
        shadow_offset = 3
        draw.text((580 + shadow_offset, 900 + shadow_offset), brand_line_1, font=self.font_brand_huge, fill=(0, 0, 0))
        draw.text((580, 900), brand_line_1, font=self.font_brand_huge, fill=self.PURE_WHITE)

        draw.text((580 + shadow_offset, 1005 + shadow_offset), brand_line_2, font=self.font_brand_sub, fill=(0, 0, 0))
        draw.text((580, 1005), brand_line_2, font=self.font_brand_sub, fill=self.PURE_WHITE)

        # Tagline - High contrast bright text
        draw.text((550, 1140), tagline[:36], font=self.font_tagline, fill=self.LIGHT_GREY)
        draw.text((550, 1175), tagline[36:72], font=self.font_tagline, fill=self.LIGHT_GREY)

        # 7. MAGENTA PILL BUTTON 1: "Book Now" (Bottom Left)
        pill_left = [75, 1370, 450, 1465]
        draw.rounded_rectangle(pill_left, radius=45, fill=self.MAGENTA_ACCENT)
        # Centered bold text
        draw.text((135, 1392), "Book Now", font=self.font_pill, fill=self.PURE_WHITE)

        # 8. MAGENTA PILL BUTTON 2: "Our Service" (Bottom Right)
        pill_right = [610, 1370, 1015, 1465]
        draw.rounded_rectangle(pill_right, radius=45, fill=self.MAGENTA_ACCENT)
        draw.text((660, 1392), "Our Service", font=self.font_pill, fill=self.PURE_WHITE)

        # 9. SERVICES LIST (RIGHT COLUMN - BIG BOLD CRISP TEXT)
        y_srv = 1505
        for s in services:
            # Dark text shadow for extreme pop
            draw.text((640 + 2, y_srv + 2), s, font=self.font_service_item, fill=(0, 0, 0))
            draw.text((640, y_srv), s, font=self.font_service_item, fill=self.PURE_WHITE)
            y_srv += 72

        # 10. CONTACT INFO (LEFT COLUMN - HUGE READABLE TEXT)
        # Giant Hotline
        draw.text((75 + 2, 1510 + 2), f"📞 {phone}", font=self.font_contact_big, fill=(0, 0, 0))
        draw.text((75, 1510), f"📞 {phone}", font=self.font_contact_big, fill=self.BRIGHT_GOLD)

        # Instagram
        draw.text((75 + 2, 1575 + 2), f"📷 {instagram}", font=self.font_contact_big, fill=(0, 0, 0))
        draw.text((75, 1575), f"📷 {instagram}", font=self.font_contact_big, fill=self.PURE_WHITE)

        # Address
        draw.text((75, 1640), "📍 Shop No. G-38, RC Plaza,", font=self.font_addr, fill=self.LIGHT_GREY)
        draw.text((75, 1675), "   Kirari Chowk, Nangloi,", font=self.font_addr, fill=self.LIGHT_GREY)
        draw.text((75, 1710), "   Delhi - 110086", font=self.font_addr, fill=self.LIGHT_GREY)

        # Convert back to RGB
        final_canvas = Image.new("RGB", (self.WIDTH, self.HEIGHT), (18, 3, 15))
        final_canvas.paste(canvas, (0, 0), mask=canvas.split()[3])

        if output_png is None:
            output_png = BASE_DIR / "posters_showcase" / "rani_makeover_ultra_clear_poster.png"

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
    print("🎨 RENDERING ULTRA-CLEAR BIG BOLD TYPOGRAPHY POSTER & REEL")
    print("=" * 80)

    engine = UltraClearDesignEngine()
    out_dir = BASE_DIR / "posters_showcase"
    vault_dir = BASE_DIR / "content_vault"

    poster_path = out_dir / "rani_makeover_ultra_clear_poster.png"
    reel_path = vault_dir / "rani_makeover_ultra_clear_reel.mp4"

    engine.render_ultra_clear_poster(
        brand_line_1="Beauty",
        brand_line_2="Salon",
        tagline="Beauty is being comfortable in your own skin. Pamper it well",
        services=[
            "Make up",
            "Face treatment",
            "Hair treatment",
            "Skincare service"
        ],
        phone="+91 9334668807",
        instagram="@Lovelyrani53",
        output_png=poster_path
    )
    print(f"✅ Ultra-Clear Poster Generated: {poster_path}")

    print("🎬 Rendering 9:16 Full HD Motion Reel...")
    engine.render_reel(poster_path, reel_path, duration=15)
    print(f"✅ 9:16 Video Reel Generated: {reel_path}")

    print("\n" + "=" * 80)
    print("🎉 ULTRA-CLEAR THEME COMPLETE!")
    print("=" * 80)

if __name__ == "__main__":
    main()
