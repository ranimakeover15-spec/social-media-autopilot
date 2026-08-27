"""
👑 RANI MAKEOVER — 100% STANDARDIZED AI VIDEO EDITING & DESIGN SYSTEM
Generates 10/10 Agency-Quality Master Reels with exact geometric hierarchy,
vector graphics, typography, Ken Burns zoom motion, and luxury background beat.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional, List, Tuple
from PIL import Image, ImageDraw, ImageFont

# Enforce UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent

class RaniMakeoverVideoCreator:
    WIDTH = 1080
    HEIGHT = 1920

    # Color Palette
    BG_BLACK = (12, 10, 16)         # #0C0A10
    HEADER_BLACK = (16, 12, 22)     # #100C16
    CARD_BG = (18, 14, 26)          # #120E1A
    HERO_CARD_BG = (22, 16, 32)     # #161020
    ROYAL_GOLD = (212, 175, 55)     # #D4AF37
    BRIGHT_GOLD = (255, 215, 0)     # #FFD700
    CRIMSON_RED = (180, 20, 40)     # #B41428
    PURE_WHITE = (255, 255, 255)    # #FFFFFF
    SOFT_WHITE = (240, 240, 240)    # #F0F0F0
    EMERALD_GREEN = (50, 225, 100)  # #32E164
    STRIKE_GREY = (180, 150, 150)   # #B49696

    def __init__(self):
        self._load_fonts()

    def _load_fonts(self):
        """Loads Georgia Bold and Arial Bold with graceful system font fallbacks."""
        def try_font(font_names: List[str], size: int) -> ImageFont.FreeTypeFont:
            for name in font_names:
                try:
                    return ImageFont.truetype(name, size)
                except Exception:
                    pass
            return ImageFont.load_default()

        self.font_header = try_font(["georgiab.ttf", "Georgia-Bold.ttf", "timesbd.ttf", "arialbd.ttf"], 40)
        self.font_sub = try_font(["arialbd.ttf", "Arial-Bold.ttf", "calibrib.ttf", "DejaVuSans-Bold.ttf"], 22)
        self.font_badge = try_font(["arialbd.ttf", "Arial-Bold.ttf", "calibrib.ttf", "DejaVuSans-Bold.ttf"], 34)
        self.font_price = try_font(["georgiab.ttf", "Georgia-Bold.ttf", "timesbd.ttf", "arialbd.ttf"], 86)
        self.font_item = try_font(["georgiab.ttf", "Georgia-Bold.ttf", "timesbd.ttf", "arialbd.ttf"], 33)
        self.font_desc = try_font(["arialbd.ttf", "Arial-Bold.ttf", "calibrib.ttf", "DejaVuSans-Bold.ttf"], 20)
        self.font_phone = try_font(["arialbd.ttf", "Arial-Bold.ttf", "calibrib.ttf", "DejaVuSans-Bold.ttf"], 46)
        self.font_addr = try_font(["arialbd.ttf", "Arial-Bold.ttf", "calibrib.ttf", "DejaVuSans-Bold.ttf"], 21)

    def render_poster_image(
        self,
        offer_title: str = "RAKSHA BANDHAN MEGA SPECIAL OFFER",
        combo_name: str = "COMPLETE 5-IN-1 BEAUTY FESTIVE COMBO",
        price_text: str = "ONLY ₹599/-",
        original_price: str = "₹1,999/-",
        discount_text: str = "(70% OFF)",
        services_list: Optional[List[Tuple[str, str]]] = None,
        output_image_path: Optional[Path] = None
    ) -> Path:
        """Draws the master 1080x1920 luxury agency poster graphic."""
        canvas = Image.new("RGB", (self.WIDTH, self.HEIGHT), self.BG_BLACK)
        draw = ImageDraw.Draw(canvas)

        if services_list is None:
            services_list = [
                ("1. RADIANCE GLOW FACIAL", "Deep skin cleansing, instant tan removal & mirror gloss shine"),
                ("2. PROFESSIONAL EYEBROW SHAPING", "Perfect arched brow styling tailored for festive looks"),
                ("3. FOREHEAD THREADING", "Smooth flawless finish & crystal clean forehead"),
                ("4. UPPER LIPS CARE", "Ultra-clean, gentle & smooth finish"),
                ("5. FULL ARMS GLOW WAXING", "100% smooth, silky & bright skin ready for festivities")
            ]

        # ----------------------------------------------------------------------
        # LAYER 1: TOP BRAND HEADER (Y: 0 -> 175)
        # ----------------------------------------------------------------------
        draw.rectangle([0, 0, self.WIDTH, 175], fill=self.HEADER_BLACK)
        draw.line([(0, 175), (self.WIDTH, 175)], fill=self.ROYAL_GOLD, width=4)

        # YouTube Official Vector Badge
        draw.rounded_rectangle([45, 55, 105, 95], radius=10, fill=(255, 0, 0))
        draw.polygon([(65, 65), (65, 85), (88, 75)], fill=self.PURE_WHITE)

        draw.text((120, 48), "RANI MAKEOVER & BEAUTY LOUNGE", font=self.font_header, fill=self.ROYAL_GOLD)
        draw.text((120, 108), "EXCLUSIVE FESTIVE BEAUTY & MAKEUP STUDIO", font=self.font_sub, fill=self.PURE_WHITE)

        # ----------------------------------------------------------------------
        # LAYER 2: FESTIVE / PROMO HERO BADGE (Y: 195 -> 280)
        # ----------------------------------------------------------------------
        draw.rounded_rectangle([100, 195, 980, 280], radius=40, fill=self.ROYAL_GOLD)
        draw.text((150, 220), offer_title, font=self.font_badge, fill=self.BG_BLACK)

        # ----------------------------------------------------------------------
        # LAYER 3: MEGA PRICE HERO CARD (Y: 300 -> 485)
        # ----------------------------------------------------------------------
        draw.rounded_rectangle([85, 300, 995, 485], radius=25, fill=self.HERO_CARD_BG, outline=self.ROYAL_GOLD, width=3)
        draw.text((125, 322), combo_name, font=self.font_sub, fill=self.BRIGHT_GOLD)
        draw.text((125, 362), price_text, font=self.font_price, fill=self.PURE_WHITE)
        draw.text((680, 380), original_price, font=self.font_badge, fill=self.STRIKE_GREY)
        draw.line([(675, 400), (825, 400)], fill=(255, 40, 40), width=4)
        draw.text((685, 425), discount_text, font=self.font_sub, fill=self.EMERALD_GREEN)

        # ----------------------------------------------------------------------
        # LAYER 4: 5-STAR SERVICE CARDS (Y: 505 -> 1325)
        # ----------------------------------------------------------------------
        y_pos = 505
        for title, desc in services_list:
            draw.rounded_rectangle([85, y_pos, 995, y_pos + 135], radius=18, fill=self.CARD_BG, outline=self.ROYAL_GOLD, width=2)
            draw.rounded_rectangle([85, y_pos, 100, y_pos + 135], radius=4, fill=self.ROYAL_GOLD)
            draw.text((125, y_pos + 20), title, font=self.font_item, fill=self.BRIGHT_GOLD)
            draw.text((125, y_pos + 78), desc, font=self.font_desc, fill=self.SOFT_WHITE)

            # Vector Gold Circle Checkmark
            draw.ellipse([925, y_pos + 42, 970, y_pos + 87], fill=self.ROYAL_GOLD)
            draw.line([(937, y_pos + 65), (946, y_pos + 75)], fill=self.BG_BLACK, width=4)
            draw.line([(946, y_pos + 75), (960, y_pos + 52)], fill=self.BG_BLACK, width=4)
            y_pos += 155

        # ----------------------------------------------------------------------
        # LAYER 5: URGENCY & LIMITED SLOTS RIBBON (Y: 1335 -> 1415)
        # ----------------------------------------------------------------------
        draw.rounded_rectangle([150, 1335, 930, 1415], radius=25, fill=self.CRIMSON_RED, outline=self.BRIGHT_GOLD, width=2)
        draw.text((215, 1360), "LIMITED SLOTS ONLY • ADVANCE BOOKING OPEN", font=self.font_sub, fill=self.PURE_WHITE)

        # ----------------------------------------------------------------------
        # LAYER 6: PERMANENT BOTTOM CONTACT FOOTER (Y: 1445 -> 1920)
        # ----------------------------------------------------------------------
        draw.rectangle([0, 1445, self.WIDTH, self.HEIGHT], fill=self.BG_BLACK)
        draw.line([(0, 1445), (self.WIDTH, 1445)], fill=self.ROYAL_GOLD, width=4)

        # Real Phone Handset Graphic in Gold Circle
        draw.ellipse([75, 1495, 170, 1590], fill=self.ROYAL_GOLD)
        draw.rounded_rectangle([102, 1520, 118, 1565], radius=6, fill=self.BG_BLACK)
        draw.rounded_rectangle([127, 1520, 143, 1565], radius=6, fill=self.BG_BLACK)
        draw.rounded_rectangle([110, 1530, 135, 1555], radius=4, fill=self.BG_BLACK)

        draw.text((195, 1492), "+91 9334668807", font=self.font_phone, fill=self.PURE_WHITE)
        draw.text((195, 1555), "CALL / WHATSAPP FOR APPOINTMENTS", font=self.font_sub, fill=self.ROYAL_GOLD)

        # Location Pin Vector & Address
        draw.ellipse([75, 1630, 105, 1660], fill=(255, 40, 40))
        draw.polygon([(80, 1653), (100, 1653), (90, 1673)], fill=(255, 40, 40))
        draw.ellipse([85, 1640, 95, 1650], fill=self.PURE_WHITE)
        draw.text((125, 1628), "Shop No. G-38, RC Plaza, Kirari Chowk, Nangloi, Delhi - 110086", font=self.font_addr, fill=self.PURE_WHITE)

        # Social Handles Bar
        draw.rounded_rectangle([75, 1715, 1005, 1815], radius=20, fill=self.HERO_CARD_BG, outline=self.ROYAL_GOLD, width=2)
        draw.text((120, 1748), "Instagram: @Lovelyrani53   |   YouTube: Rani Makeover", font=self.font_sub, fill=self.ROYAL_GOLD)

        # Save Image
        if output_image_path is None:
            temp_dir = BASE_DIR / "temp"
            temp_dir.mkdir(parents=True, exist_ok=True)
            output_image_path = temp_dir / "poster_rani_makeover.png"

        canvas.save(output_image_path)
        return output_image_path

    def render_reel_video(
        self,
        poster_path: Path,
        output_video_path: Path,
        music_path: Optional[Path] = None,
        duration: int = 20
    ) -> Path:
        """
        Renders complete 1080x1920 9:16 Video Reel with Ken Burns subtle zoom effect
        and smooth audio fade out.
        """
        # Ken Burns Smooth Zoom Filter
        vf_motion = "zoompan=z='min(zoom+0.0004,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=600:s=1080x1920:fps=30"

        # Check for audio file
        has_audio = music_path and music_path.exists()

        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", str(poster_path)
        ]

        if has_audio:
            fade_start = max(1, duration - 2)
            cmd.extend([
                "-i", str(music_path),
                "-filter_complex", vf_motion,
                "-af", f"afade=t=out:st={fade_start}:d=2",
                "-c:a", "aac",
                "-b:a", "192k",
                "-ar", "44100"
            ])
        else:
            # Generate synthetic luxury synth chime tone if no audio file provided
            cmd.extend([
                "-f", "lavfi",
                "-i", f"sine=frequency=440:duration={duration}",
                "-filter_complex", vf_motion,
                "-c:a", "aac",
                "-b:a", "192k"
            ])

        cmd.extend([
            "-c:v", "libx264",
            "-t", str(duration),
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            str(output_video_path)
        ])

        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if process.returncode != 0:
            raise RuntimeError(f"FFmpeg Reel Render Error: {process.stderr[-500:]}")

        return output_video_path

# Global instance
rani_creator = RaniMakeoverVideoCreator()
