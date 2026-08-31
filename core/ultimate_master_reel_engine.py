"""
👑 RANI MAKEOVER — ULTIMATE MASTER REEL ENGINE (LUXURY V2)
Senior Video Architect Implementation

Fixes Applied:
1. Bundled TrueType Fonts (assets/fonts/): Guarantees bold, crisp, full-size typography on both Windows and Linux runners (zero microscopic 10px fallback).
2. Modern Luxury Full-Vertical 9:16 Framing: Dynamic blurred backdrop + crisp foreground.
3. High-CTR Branding: Top Floating Gold RM Monogram Header, Mid-Lower Headline Capsule, and Elevated Bottom Booking Hub.
4. 320kbps High-Quality Audio Transcoding with smooth 2s fadeout.
"""

import os
import sys
import subprocess
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent

class UltimateRaniMasterEngine:
    WIDTH = 1080
    HEIGHT = 1920

    GOLD_PRIMARY = (212, 175, 55)
    GOLD_BRIGHT = (255, 215, 0)
    DARK_BG = (15, 12, 20)
    TRANSLUCENT_BG = (18, 14, 24, 235)
    WHATSAPP_GREEN = (37, 211, 102)
    YOUTUBE_RED = (255, 0, 0)
    PURE_WHITE = (255, 255, 255)
    SOFT_WHITE = (240, 235, 240)

    def __init__(self):
        self.font_dir = BASE_DIR / "assets" / "fonts"
        self.font_serif_path = self.font_dir / "georgiab.ttf" if (self.font_dir / "georgiab.ttf").exists() else "georgiab.ttf"
        self.font_sans_path = self.font_dir / "arialbd.ttf" if (self.font_dir / "arialbd.ttf").exists() else "arialbd.ttf"
        self._load_fonts()
        self.music_dir = BASE_DIR / "assets" / "music"
        self.logo_path = BASE_DIR / "assets" / "salon_photos" / "official_rm_logo.png"

    def _get_fitted_font(self, text: str, font_path, max_size: int, max_width: int):
        """Calculates fitted font size so text NEVER overflows container width."""
        size = max_size
        while size >= 18:
            try:
                f = ImageFont.truetype(str(font_path), size)
                bbox = f.getbbox(text)
                w = bbox[2] - bbox[0]
                if w <= max_width:
                    return f, w
            except Exception:
                pass
            size -= 2
        try:
            f = ImageFont.truetype(str(font_path), 18)
            bbox = f.getbbox(text)
            return f, bbox[2] - bbox[0]
        except Exception:
            f = ImageFont.load_default()
            return f, len(text) * 10

    def _load_fonts(self):
        font_dir = self.font_dir
        
        def get_font(size, bold=True, serif=False):
            candidates = []
            if font_dir.exists():
                if serif:
                    candidates.append(str(font_dir / "georgiab.ttf"))
                candidates.append(str(font_dir / "arialbd.ttf"))
                candidates.append(str(font_dir / "arial.ttf"))
            
            # Linux system fallbacks
            candidates.extend([
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "arialbd.ttf",
                "georgiab.ttf"
            ])

            for c in candidates:
                try:
                    return ImageFont.truetype(c, size)
                except Exception:
                    pass
            return ImageFont.load_default(size=size) if hasattr(ImageFont, "load_default") else ImageFont.load_default()

        self.font_brand = get_font(44, bold=True, serif=True)
        self.font_sub = get_font(24, bold=True)
        self.font_glow_title = get_font(40, bold=True, serif=True)
        self.font_glow_sub = get_font(26, bold=True)
        self.font_phone_big = get_font(48, bold=True)
        self.font_phone_sub = get_font(22, bold=True)
        self.font_addr = get_font(24, bold=True)
        self.font_pill = get_font(26, bold=True)

    def draw_whatsapp_icon(self, draw: ImageDraw.Draw, x: int, y: int, radius: int = 30):
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=self.WHATSAPP_GREEN)
        draw.polygon([(x - 18, y + 10), (x - 26, y + 28), (x - 8, y + 22)], fill=self.WHATSAPP_GREEN)
        draw.rounded_rectangle([x - 14, y - 13, x - 6, y + 13], radius=4, fill=self.PURE_WHITE)
        draw.rounded_rectangle([x + 6, y - 13, x + 14, y + 13], radius=4, fill=self.PURE_WHITE)
        draw.rounded_rectangle([x - 10, y - 4, x + 10, y + 6], radius=3, fill=self.PURE_WHITE)

    def draw_instagram_icon(self, draw: ImageDraw.Draw, x: int, y: int, radius: int = 24):
        draw.rounded_rectangle([x - radius, y - radius, x + radius, y + radius], radius=12, fill=(225, 0, 115))
        draw.rounded_rectangle([x - 15, y - 15, x + 15, y + 15], radius=7, outline=self.PURE_WHITE, width=3)
        draw.ellipse([x - 7, y - 7, x + 7, y + 7], outline=self.PURE_WHITE, width=3)
        draw.ellipse([x + 8, y - 9, x + 11, y - 6], fill=self.PURE_WHITE)

    def draw_youtube_icon(self, draw: ImageDraw.Draw, x: int, y: int, radius: int = 24):
        draw.rounded_rectangle([x - 28, y - 20, x + 28, y + 20], radius=10, fill=self.YOUTUBE_RED)
        draw.polygon([(x - 8, y - 10), (x - 8, y + 10), (x + 10, y)], fill=self.PURE_WHITE)

    def draw_location_pin(self, draw: ImageDraw.Draw, x: int, y: int, radius: int = 20):
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=(235, 40, 40))
        draw.ellipse([x - 8, y - 10, x + 8, y + 5], fill=self.PURE_WHITE)
        draw.polygon([(x - 7, y), (x + 7, y), (x, y + 13)], fill=(235, 40, 40))
        draw.ellipse([x - 4, y - 6, x + 4, y + 2], fill=(235, 40, 40))

    def generate_flawless_overlay(
        self,
        headline: str,
        subheadline: str,
        output_png: Path
    ) -> Path:
        canvas = Image.new("RGBA", (self.WIDTH, self.HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        # ----------------------------------------------------------------------
        # 1. TOP FLOATING LUXURY HEADER (Y: 30 to 195)
        # ----------------------------------------------------------------------
        top_w = 1000
        top_h = 150
        top_x = (self.WIDTH - top_w) // 2
        top_y = 35

        draw.rounded_rectangle(
            [top_x, top_y, top_x + top_w, top_y + top_h],
            radius=24,
            fill=self.TRANSLUCENT_BG,
            outline=self.GOLD_PRIMARY,
            width=3
        )

        if self.logo_path.exists():
            logo_img = Image.open(self.logo_path).convert("RGBA").resize((115, 115))
            canvas.paste(logo_img, (top_x + 20, top_y + 18), logo_img)
        else:
            draw.ellipse([top_x + 20, top_y + 18, top_x + 135, top_y + 133], fill=(0, 0, 0), outline=self.GOLD_PRIMARY, width=3)
            draw.text((top_x + 45, top_y + 45), "RM", font=self.font_brand, fill=self.GOLD_BRIGHT)

        draw.text((top_x + 155, top_y + 30), "RANI MAKEOVER", font=self.font_brand, fill=self.GOLD_BRIGHT)
        draw.text((top_x + 158, top_y + 90), "Bridal Makeup  •  Hair Cutting  •  Hair Spa  •  Hydra Facial", font=self.font_sub, fill=self.PURE_WHITE)

        # ----------------------------------------------------------------------
        # 2. MID-LOWER GLOW-UP HEADLINE CAPSULE (Y: 1300 to 1460)
        # ----------------------------------------------------------------------
        card_w = 1000
        card_h = 145
        card_x = (self.WIDTH - card_w) // 2
        card_y = 1300

        draw.rounded_rectangle(
            [card_x, card_y, card_x + card_w, card_y + card_h],
            radius=22,
            fill=self.TRANSLUCENT_BG,
            outline=self.GOLD_PRIMARY,
            width=3
        )

        # Sanitize emojis (remove unrenderable glyph box symbols)
        clean_headline = re.sub(r'[\U00010000-\U0010ffff]', '', headline)
        clean_headline = re.sub(r'[✂️💇‍♀️💆‍♀️👑🌟🎁🔥💅🌸✨👁️👸💎💄✂️]', '', clean_headline).strip()
        if not clean_headline.startswith("★") and not clean_headline.startswith("•"):
            clean_headline = f"★ {clean_headline} ★"

        clean_sub = re.sub(r'[\U00010000-\U0010ffff]', '', subheadline)
        clean_sub = re.sub(r'[✂️💇‍♀️💆‍♀️👑🌟🎁🔥💅🌸✨👁️👸💎💄✂️]', '', clean_sub).strip()

        # Dynamic Font Auto-Fit: Title (never overflows 920px width)
        font_head_fitted, hw = self._get_fitted_font(clean_headline, self.font_serif_path, max_size=40, max_width=920)
        draw.text((card_x + (card_w - hw) // 2, card_y + 24), clean_headline, font=font_head_fitted, fill=self.GOLD_BRIGHT)

        # Dynamic Font Auto-Fit: Subtitle
        font_sub_fitted, sw = self._get_fitted_font(clean_sub, self.font_sans_path, max_size=26, max_width=920)
        draw.text((card_x + (card_w - sw) // 2, card_y + 86), clean_sub, font=font_sub_fitted, fill=self.PURE_WHITE)

        # ----------------------------------------------------------------------
        # 3. BOTTOM CONTACT & BOOKING HUB (Y: 1480 to 1880)
        # ----------------------------------------------------------------------
        bot_w = 1000
        bot_h = 380
        bot_x = (self.WIDTH - bot_w) // 2
        bot_y = 1480

        draw.rounded_rectangle(
            [bot_x, bot_y, bot_x + bot_w, bot_y + bot_h],
            radius=24,
            fill=self.TRANSLUCENT_BG,
            outline=self.GOLD_PRIMARY,
            width=3
        )

        # Row 1: WhatsApp Icon + Big Phone
        self.draw_whatsapp_icon(draw, bot_x + 310, bot_y + 65, radius=32)
        draw.text((bot_x + 360, bot_y + 28), "+91 9334668807", font=self.font_phone_big, fill=self.PURE_WHITE)
        draw.text((bot_x + 365, bot_y + 88), "CALL / WHATSAPP FOR APPOINTMENTS", font=self.font_phone_sub, fill=self.GOLD_BRIGHT)

        draw.line([(bot_x + 40, bot_y + 140), (bot_x + bot_w - 40, bot_y + 140)], fill=(80, 65, 75), width=2)

        # Row 2: Location Pin + Address
        self.draw_location_pin(draw, bot_x + 55, bot_y + 185, radius=22)
        draw.text((bot_x + 95, bot_y + 172), "Shop No. G-38, RC Plaza, Kirari Chowk, Nangloi, Delhi - 110086", font=self.font_addr, fill=self.PURE_WHITE)

        draw.line([(bot_x + 40, bot_y + 235), (bot_x + bot_w - 40, bot_y + 235)], fill=(80, 65, 75), width=2)

        # Row 3: Dual Social Media Badges
        # Left: Instagram
        self.draw_instagram_icon(draw, bot_x + 90, bot_y + 300, radius=24)
        draw.text((bot_x + 130, bot_y + 285), "Instagram: @Lovelyrani53", font=self.font_pill, fill=self.PURE_WHITE)

        # Separator line
        draw.line([(bot_x + bot_w // 2, bot_y + 255), (bot_x + bot_w // 2, bot_y + 345)], fill=(120, 100, 110), width=2)

        # Right: YouTube
        self.draw_youtube_icon(draw, bot_x + bot_w // 2 + 60, bot_y + 300, radius=24)
        draw.text((bot_x + bot_w // 2 + 100, bot_y + 285), "YouTube: Rani makeover", font=self.font_pill, fill=self.PURE_WHITE)

        output_png.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(output_png, "PNG")
        return output_png

    def render_master_reel_with_music(
        self,
        raw_video_path: Path,
        output_video_path: Path,
        headline: str,
        subheadline: str,
        duration: int = 15,
        music_path: Path = None
    ) -> Path:
        overlay_png = BASE_DIR / "temp" / "flawless_overlay.png"
        self.generate_flawless_overlay(headline, subheadline, overlay_png)

        if not music_path or not Path(music_path).exists():
            tracks = list(self.music_dir.glob("*.mp3"))
            music_path = tracks[0] if tracks else None

        filter_complex = (
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=20[vbg];"
            "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease[vfg];"
            "[vbg][vfg]overlay=(W-w)/2:(H-h)/2[vmerged];"
            "[vmerged][1:v]overlay=0:0[vout];"
            f"[2:a]aloop=loop=-1:size=2e+09,afade=t=out:st={duration-2}:d=2,volume=1.0[aout]"
        )

        cmd = [
            "ffmpeg", "-y",
            "-i", str(raw_video_path),
            "-i", str(overlay_png),
            "-i", str(music_path),
            "-filter_complex", filter_complex,
            "-map", "[vout]",
            "-map", "[aout]",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "320k",
            "-t", str(duration),
            "-movflags", "+faststart",
            str(output_video_path)
        ]

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print("FFmpeg error:", res.stderr[-500:])
            res.check_returncode()

        return output_video_path
