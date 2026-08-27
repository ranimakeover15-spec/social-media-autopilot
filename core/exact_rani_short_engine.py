"""
👑 RANI MAKEOVER — EXACT YOUTUBE SHORT TEMPLATE MASTER ENGINE
Replicates 100% of https://youtube.com/shorts/LsJvYUAE0B4 layout:
1. Top Header Bar (Solid Black/Velvet Plum with Gold Line):
   - Left: Official Red YouTube Badge
   - Title: RANI MAKEOVER & BEAUTY LOUNGE (Gold Bold)
   - Subtitle: EXCLUSIVE FESTIVE BEAUTY & MAKEUP STUDIO (White)
2. Center: Raw Salon Video (Padded/Centered with blurred or clean background)
3. Lower Mid-Card:
   - ⭐ 100% FLAWLESS HD GLOW-UP ⭐ (Gold Border, Purple/Dark Gradient)
   - Luxury Salon Experience • Mirror Shine & Glass Skin
4. Bottom Contact Card:
   - Big Green WhatsApp/Call Icon: +91 9334668807 (CALL / WHATSAPP FOR APPOINTMENTS)
   - Red Map Pin: Shop No. G-38, RC Plaza, Kirari Chowk, Nangloi, Delhi - 110086
   - Dual Capsule Pill at bottom:
     - Left: 📷 Instagram: @Lovelyrani53
     - Right: ▶ YouTube: Rani Makeover
"""

import os
import sys
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Enforce UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent

class ExactRaniShortEngine:
    WIDTH = 1080
    HEIGHT = 1920

    # Colors
    ROYAL_GOLD = (255, 215, 0)
    DARK_BG = (14, 2, 12)
    PURPLE_CARD_BG = (28, 4, 24)
    BORDER_GOLD = (212, 175, 55)
    WHATSAPP_GREEN = (37, 211, 102)
    YOUTUBE_RED = (255, 0, 0)
    INSTA_PINK = (225, 0, 115)
    PURE_WHITE = (255, 255, 255)
    SOFT_GRAY = (220, 210, 215)

    def __init__(self):
        self._load_fonts()

    def _load_fonts(self):
        def try_font(names, size):
            for n in names:
                try:
                    return ImageFont.truetype(n, size)
                except Exception:
                    pass
            return ImageFont.load_default()

        self.font_brand_title = try_font(["georgiab.ttf", "arialbd.ttf"], 36)
        self.font_brand_sub = try_font(["arialbd.ttf", "Arial-Bold.ttf"], 20)
        self.font_offer_title = try_font(["georgiab.ttf", "Georgia-Bold.ttf", "arialbd.ttf"], 34)
        self.font_offer_sub = try_font(["arialbd.ttf", "Arial-Bold.ttf"], 22)
        self.font_phone_big = try_font(["arialbd.ttf", "Arial-Bold.ttf"], 42)
        self.font_phone_sub = try_font(["arialbd.ttf", "Arial-Bold.ttf"], 18)
        self.font_addr = try_font(["arialbd.ttf", "Arial-Bold.ttf"], 22)
        self.font_pill = try_font(["arialbd.ttf", "Arial-Bold.ttf"], 22)

    # --------------------------------------------------------------------------
    # VECTOR ICONS
    # --------------------------------------------------------------------------
    def draw_yt_badge(self, draw: ImageDraw.Draw, x: int, y: int):
        draw.ellipse([x - 30, y - 30, x + 30, y + 30], outline=self.ROYAL_GOLD, width=2)
        draw.rounded_rectangle([x - 22, y - 16, x + 22, y + 16], radius=6, fill=self.YOUTUBE_RED)
        draw.polygon([(x - 6, y - 8), (x - 6, y + 8), (x + 8, y)], fill=self.PURE_WHITE)

    def draw_whatsapp_icon(self, draw: ImageDraw.Draw, x: int, y: int, radius: int = 26):
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=self.WHATSAPP_GREEN)
        # Speech bubble tail
        draw.polygon([(x - 14, y + 8), (x - 22, y + 24), (x - 4, y + 18)], fill=self.WHATSAPP_GREEN)
        # White telephone inside
        draw.rounded_rectangle([x - 11, y - 10, x - 5, y + 10], radius=3, fill=self.PURE_WHITE)
        draw.rounded_rectangle([x + 5, y - 10, x + 11, y + 10], radius=3, fill=self.PURE_WHITE)
        draw.rounded_rectangle([x - 8, y - 3, x + 8, y + 5], radius=2, fill=self.PURE_WHITE)

    def draw_loc_pin(self, draw: ImageDraw.Draw, x: int, y: int, radius: int = 16):
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=(235, 45, 65))
        draw.ellipse([x - 6, y - 8, x + 6, y + 4], fill=self.PURE_WHITE)
        draw.polygon([(x - 5, y), (x + 5, y), (x, y + 9)], fill=self.PURE_WHITE)
        draw.ellipse([x - 2, y - 4, x + 2, y], fill=(235, 45, 65))

    def generate_exact_template_overlay(
        self,
        headline: str,
        subheadline: str,
        output_png: Path
    ) -> Path:
        canvas = Image.new("RGBA", (self.WIDTH, self.HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        # ----------------------------------------------------------------------
        # 1. TOP HEADER BAR (Y: 0 to 175)
        # ----------------------------------------------------------------------
        draw.rectangle([0, 0, self.WIDTH, 170], fill=(14, 2, 12, 255))
        draw.line([(0, 170), (self.WIDTH, 170)], fill=self.ROYAL_GOLD, width=4)

        # YouTube Circular Badge (Left)
        self.draw_yt_badge(draw, 75, 85)

        # Brand Title & Subtitle
        draw.text((130, 52), "RANI MAKEOVER & BEAUTY LOUNGE", font=self.font_brand_title, fill=self.ROYAL_GOLD)
        draw.text((132, 104), "EXCLUSIVE FESTIVE BEAUTY & MAKEUP STUDIO", font=self.font_brand_sub, fill=self.PURE_WHITE)

        # ----------------------------------------------------------------------
        # 2. LOWER-MIDDLE OFFER/GLOW-UP CARD (Y: 1250 to 1400)
        # ----------------------------------------------------------------------
        card_w = 980
        card_h = 145
        card_x = (self.WIDTH - card_w) // 2
        card_y = 1255

        draw.rounded_rectangle(
            [card_x, card_y, card_x + card_w, card_y + card_h],
            radius=18,
            fill=(26, 3, 22, 255),
            outline=self.BORDER_GOLD,
            width=3
        )

        # Star + Headline + Star
        head_text = f"★   {headline}   ★"
        bbox_head = self.font_offer_title.getbbox(head_text)
        hw = bbox_head[2] - bbox_head[0]
        draw.text((card_x + (card_w - hw) // 2, card_y + 24), head_text, font=self.font_offer_title, fill=self.ROYAL_GOLD)

        # Subtitle
        bbox_sub = self.font_offer_sub.getbbox(subheadline)
        sw = bbox_sub[2] - bbox_sub[0]
        draw.text((card_x + (card_w - sw) // 2, card_y + 84), subheadline, font=self.font_offer_sub, fill=self.PURE_WHITE)

        # ----------------------------------------------------------------------
        # 3. BOTTOM CONTACT & BOOKING SECTION (Y: 1440 to 1920)
        # ----------------------------------------------------------------------
        draw.rectangle([0, 1440, self.WIDTH, self.HEIGHT], fill=(12, 1, 10, 255))
        draw.line([(0, 1440), (self.WIDTH, 1440)], fill=self.ROYAL_GOLD, width=4)

        # Row 1: WhatsApp Icon + Number + Subtitle (Y: 1475 to 1570)
        self.draw_whatsapp_icon(draw, 340, 1515, radius=26)
        draw.text((385, 1485), "+91 9334668807", font=self.font_phone_big, fill=self.PURE_WHITE)
        draw.text((390, 1540), "CALL / WHATSAPP FOR APPOINTMENTS", font=self.font_phone_sub, fill=self.ROYAL_GOLD)

        # Row 2: Location Pin + Full Address (Y: 1610 to 1660)
        self.draw_loc_pin(draw, 65, 1640, radius=16)
        draw.text((95, 1626), "Shop No. G-38, RC Plaza, Kirari Chowk, Nangloi, Delhi - 110086", font=self.font_addr, fill=self.PURE_WHITE)

        # Row 3: Dual Social Media Capsules (Y: 1710 to 1830)
        pill_w = 980
        pill_h = 90
        pill_x = (self.WIDTH - pill_w) // 2
        pill_y = 1715

        draw.rounded_rectangle(
            [pill_x, pill_y, pill_x + pill_w, pill_y + pill_h],
            radius=16,
            fill=(22, 2, 18, 255),
            outline=self.BORDER_GOLD,
            width=2
        )

        # Divider between Insta and YouTube
        draw.line([(self.WIDTH // 2, pill_y + 12), (self.WIDTH // 2, pill_y + pill_h - 12)], fill=(120, 100, 110), width=2)

        # Left: Instagram Capsule
        draw.rectangle([pill_x + 55, pill_y + 26, pill_x + 95, pill_y + 66], outline=self.PURE_WHITE, width=2)
        draw.ellipse([pill_x + 67, pill_y + 38, pill_x + 83, pill_y + 54], outline=self.PURE_WHITE, width=2)
        draw.text((pill_x + 115, pill_y + 30), "Instagram: @Lovelyrani53", font=self.font_pill, fill=self.PURE_WHITE)

        # Right: YouTube Capsule
        draw.rounded_rectangle([self.WIDTH // 2 + 55, pill_y + 26, self.WIDTH // 2 + 105, pill_y + 64], radius=6, fill=self.YOUTUBE_RED)
        draw.polygon([(self.WIDTH // 2 + 73, pill_y + 34), (self.WIDTH // 2 + 73, pill_y + 56), (self.WIDTH // 2 + 91, pill_y + 45)], fill=self.PURE_WHITE)
        draw.text((self.WIDTH // 2 + 125, pill_y + 30), "YouTube: Rani Makeover", font=self.font_pill, fill=self.PURE_WHITE)

        output_png.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(output_png)
        return output_png

    def render_exact_short_video(
        self,
        raw_video_path: Path,
        output_video_path: Path,
        headline: str = "100% FLAWLESS HD GLOW-UP",
        subheadline: str = "Luxury Salon Experience • Mirror Shine & Glass Skin",
        duration: int = 15
    ) -> Path:
        temp_overlay = BASE_DIR / "temp" / "exact_template_overlay.png"
        self.generate_exact_template_overlay(
            headline=headline,
            subheadline=subheadline,
            output_png=temp_overlay
        )

        # FFmpeg:
        # Scale/pad raw video perfectly in the center display area (Y: 170 to 1255)
        # Background: Rich blurred video backdrop
        # Overlay: The Exact Template Graphic
        vf = (
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=20[vbg];"
            "[0:v]scale=1080:1085:force_original_aspect_ratio=decrease[vfg];"
            "[vbg][vfg]overlay=(W-w)/2:170[vmerged];"
            "[vmerged][1:v]overlay=0:0[vout]"
        )

        cmd = [
            "ffmpeg", "-y",
            "-i", str(raw_video_path),
            "-i", str(temp_overlay),
            "-filter_complex", vf,
            "-map", "[vout]",
            "-map", "0:a?",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", str(duration),
            "-movflags", "+faststart",
            str(output_video_path)
        ]

        output_video_path.parent.mkdir(parents=True, exist_ok=True)
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print("FFmpeg error:", res.stderr.decode("utf-8", errors="replace")[-500:])
            res.check_returncode()

        return output_video_path

def main():
    print("=" * 80)
    print("👑 RANI MAKEOVER — 100% EXACT YOUTUBE SHORT REFERENCE RENDER")
    print("=" * 80)

    engine = ExactRaniShortEngine()
    vault = BASE_DIR / "content_vault"

    raw_video = vault / "viral_beauty_21_38_Stunning Rashmika Mandannas bridal Makeup_LwvBQhjHNso.mp4"
    if not raw_video.exists():
        raw_video = next(vault.glob("viral_beauty_*.mp4"))

    output_video = vault / "rani_makeover_exact_reference_short.mp4"

    print(f"🎬 Processing Raw Footage with EXACT REFERENCE TEMPLATE...")
    engine.render_exact_short_video(
        raw_video_path=raw_video,
        output_video_path=output_video,
        headline="100% FLAWLESS HD GLOW-UP",
        subheadline="Luxury Salon Experience • Mirror Shine & Glass Skin",
        duration=15
    )

    size_mb = output_video.stat().st_size / (1024 * 1024)
    print(f"✅ Exact Reference Short Generated: {output_video.name} ({size_mb:.2f} MB)")

    # Upload to Google Drive
    try:
        from scripts.upload_to_gdrive_clint import get_gdrive_service, find_or_create_folder, upload_file
        service = get_gdrive_service()
        clint_id = find_or_create_folder(service, "CLINT")
        vid_id = find_or_create_folder(service, "01_RANI_MAKEOVER_VIDEOS", parent_id=clint_id)
        upload_file(service, output_video, vid_id, mime_type="video/mp4")
        print("☁️ Uploaded to Google Drive 'CLINT' Folder!")
    except Exception as e:
        print(f"GDrive note: {e}")

    print("=" * 80)

if __name__ == "__main__":
    main()
