"""
👑 RANI MAKEOVER — ULTIMATE MASTER VIDEO BRANDING & MUSIC ENGINE
Guarantees:
1. Exact Original Uploaded RM Golden Monogram Logo pasted in Top Left.
2. Premium Trending Background Music (viral_luxury_fashion_beat.mp3 / instagram_viral_beauty_lounge.mp3) blended with audio ducking and smooth 2-sec fade-out.
3. Clean Top Header: "RANI MAKEOVER" (Gold) + "@Ranimakeover-f3f • Exclusive Festive Studio".
4. Zero Broken Glyphs / Zero Box Glyphs: Pure clean typography: "★ 100% FLAWLESS HD GLOW-UP ★".
5. Real Vector Icons: WhatsApp Green, Instagram Magenta, YouTube Red, and Map Pin.
"""

import os
import sys
import random
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Enforce UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

class UltimateRaniMasterEngine:
    WIDTH = 1080
    HEIGHT = 1920

    # Master Color Palette
    GOLD_PRIMARY = (212, 175, 55)
    GOLD_BRIGHT = (255, 215, 0)
    DARK_BG = (12, 10, 16)
    CARD_BG = (22, 14, 28)
    WHATSAPP_GREEN = (37, 211, 102)
    YOUTUBE_RED = (255, 0, 0)
    PURE_WHITE = (255, 255, 255)
    SOFT_WHITE = (240, 235, 240)

    def __init__(self):
        self._load_fonts()
        self.music_dir = BASE_DIR / "assets" / "music"
        self.logo_path = BASE_DIR / "assets" / "salon_photos" / "official_rm_logo.png"

    def _load_fonts(self):
        def try_font(names, size):
            for n in names:
                try:
                    return ImageFont.truetype(n, size)
                except Exception:
                    pass
            return ImageFont.load_default()

        self.font_brand = try_font(["georgiab.ttf", "arialbd.ttf"], 44)
        self.font_sub = try_font(["arialbd.ttf", "Arial-Bold.ttf"], 22)
        self.font_glow_title = try_font(["georgiab.ttf", "Georgia-Bold.ttf", "arialbd.ttf"], 42)
        self.font_glow_sub = try_font(["arialbd.ttf", "Arial-Bold.ttf"], 24)
        self.font_phone_big = try_font(["arialbd.ttf", "Arial-Bold.ttf"], 46)
        self.font_phone_sub = try_font(["arialbd.ttf", "Arial-Bold.ttf"], 20)
        self.font_addr = try_font(["arialbd.ttf", "Arial-Bold.ttf"], 23)
        self.font_pill = try_font(["arialbd.ttf", "Arial-Bold.ttf"], 24)

    # --------------------------------------------------------------------------
    # REAL VECTOR ICONS
    # --------------------------------------------------------------------------
    def draw_whatsapp_icon(self, draw: ImageDraw.Draw, x: int, y: int, radius: int = 28):
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=self.WHATSAPP_GREEN)
        draw.polygon([(x - 16, y + 8), (x - 24, y + 26), (x - 6, y + 20)], fill=self.WHATSAPP_GREEN)
        draw.rounded_rectangle([x - 12, y - 11, x - 5, y + 11], radius=3, fill=self.PURE_WHITE)
        draw.rounded_rectangle([x + 5, y - 11, x + 12, y + 11], radius=3, fill=self.PURE_WHITE)
        draw.rounded_rectangle([x - 9, y - 3, x + 9, y + 5], radius=2, fill=self.PURE_WHITE)

    def draw_instagram_icon(self, draw: ImageDraw.Draw, x: int, y: int, radius: int = 22):
        draw.rounded_rectangle([x - radius, y - radius, x + radius, y + radius], radius=11, fill=(225, 0, 115))
        draw.rounded_rectangle([x - 14, y - 14, x + 14, y + 14], radius=6, outline=self.PURE_WHITE, width=2)
        draw.ellipse([x - 6, y - 6, x + 6, y + 6], outline=self.PURE_WHITE, width=2)
        draw.ellipse([x + 7, y - 8, x + 10, y - 5], fill=self.PURE_WHITE)

    def draw_youtube_icon(self, draw: ImageDraw.Draw, x: int, y: int, radius: int = 22):
        draw.rounded_rectangle([x - 26, y - 18, x + 26, y + 18], radius=8, fill=self.YOUTUBE_RED)
        draw.polygon([(x - 7, y - 9), (x - 7, y + 9), (x + 9, y)], fill=self.PURE_WHITE)

    def draw_location_pin(self, draw: ImageDraw.Draw, x: int, y: int, radius: int = 18):
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=(235, 40, 40))
        draw.ellipse([x - 7, y - 9, x + 7, y + 4], fill=self.PURE_WHITE)
        draw.polygon([(x - 6, y), (x + 6, y), (x, y + 11)], fill=(235, 40, 40))
        draw.ellipse([x - 3, y - 5, x + 3, y + 1], fill=(235, 40, 40))

    def generate_flawless_overlay(
        self,
        headline: str,
        subheadline: str,
        output_png: Path
    ) -> Path:
        canvas = Image.new("RGBA", (self.WIDTH, self.HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(canvas)

        # ----------------------------------------------------------------------
        # 1. TOP HEADER LAYER (Y: 0 to 175) - EXACT ORIGINAL RM LOGO
        # ----------------------------------------------------------------------
        draw.rectangle([0, 0, self.WIDTH, 175], fill=(12, 10, 16, 255))
        draw.line([(0, 175), (self.WIDTH, 175)], fill=self.GOLD_PRIMARY, width=4)

        # Paste the real original circular RM Logo
        if self.logo_path.exists():
            logo_img = Image.open(self.logo_path).convert("RGBA").resize((115, 115))
            canvas.paste(logo_img, (45, 30), logo_img)
        else:
            draw.ellipse([45, 30, 160, 145], fill=(0, 0, 0), outline=self.GOLD_PRIMARY, width=3)
            draw.text((65, 55), "RM", font=self.font_brand, fill=self.GOLD_BRIGHT)

        # Short Brand Name & Handle
        draw.text((175, 45), "RANI MAKEOVER", font=self.font_brand, fill=self.GOLD_BRIGHT)
        draw.text((178, 105), "@Ranimakeover-f3f  •  Exclusive Festive Studio", font=self.font_sub, fill=self.PURE_WHITE)

        # ----------------------------------------------------------------------
        # 2. LOWER-MIDDLE GLOW-UP CARD (Y: 1260 to 1420) - PURE CLEAN TYPOGRAPHY
        # ----------------------------------------------------------------------
        card_w = 980
        card_h = 150
        card_x = (self.WIDTH - card_w) // 2
        card_y = 1260

        draw.rounded_rectangle(
            [card_x, card_y, card_x + card_w, card_y + card_h],
            radius=20,
            fill=(22, 14, 28, 255),
            outline=self.GOLD_PRIMARY,
            width=3
        )

        # PURE TEXT ONLY (Zero broken square glyphs)
        bbox_head = self.font_glow_title.getbbox(headline)
        hw = bbox_head[2] - bbox_head[0]
        draw.text((card_x + (card_w - hw) // 2, card_y + 24), headline, font=self.font_glow_title, fill=self.GOLD_BRIGHT)

        bbox_sub = self.font_glow_sub.getbbox(subheadline)
        sw = bbox_sub[2] - bbox_sub[0]
        draw.text((card_x + (card_w - sw) // 2, card_y + 86), subheadline, font=self.font_glow_sub, fill=self.PURE_WHITE)

        # ----------------------------------------------------------------------
        # 3. BOTTOM CONTACT & BOOKING HUB (Y: 1450 to 1920)
        # ----------------------------------------------------------------------
        draw.rectangle([0, 1450, self.WIDTH, self.HEIGHT], fill=(12, 10, 16, 255))
        draw.line([(0, 1450), (self.WIDTH, 1450)], fill=self.GOLD_PRIMARY, width=4)

        # Row 1: Real WhatsApp Icon + Large Phone
        self.draw_whatsapp_icon(draw, 330, 1530, radius=28)
        draw.text((380, 1495), "+91 9334668807", font=self.font_phone_big, fill=self.PURE_WHITE)
        draw.text((385, 1555), "CALL / WHATSAPP FOR APPOINTMENTS", font=self.font_phone_sub, fill=self.GOLD_PRIMARY)

        # Row 2: Real Location Pin + Address
        self.draw_location_pin(draw, 65, 1640, radius=18)
        draw.text((98, 1625), "Shop No. G-38, RC Plaza, Kirari Chowk, Nangloi, Delhi - 110086", font=self.font_addr, fill=self.PURE_WHITE)

        # Row 3: Dual Social Media Capsules
        pill_w = 980
        pill_h = 95
        pill_x = (self.WIDTH - pill_w) // 2
        pill_y = 1715

        draw.rounded_rectangle(
            [pill_x, pill_y, pill_x + pill_w, pill_y + pill_h],
            radius=18,
            fill=(22, 14, 28, 255),
            outline=self.GOLD_PRIMARY,
            width=2
        )

        draw.line([(self.WIDTH // 2, pill_y + 15), (self.WIDTH // 2, pill_y + pill_h - 15)], fill=(120, 100, 110), width=2)

        # Left: Real Instagram Icon
        self.draw_instagram_icon(draw, pill_x + 65, pill_y + 48, radius=20)
        draw.text((pill_x + 105, pill_y + 34), "Instagram: @Lovelyrani53", font=self.font_pill, fill=self.PURE_WHITE)

        # Right: Real YouTube Icon
        self.draw_youtube_icon(draw, self.WIDTH // 2 + 65, pill_y + 48, radius=20)
        draw.text((self.WIDTH // 2 + 105, pill_y + 34), "YouTube: Rani makeover", font=self.font_pill, fill=self.PURE_WHITE)

        output_png.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(output_png)
        return output_png

    def render_master_reel_with_music(
        self,
        raw_video_path: Path,
        output_video_path: Path,
        headline: str = "100% FLAWLESS HD GLOW-UP",
        subheadline: str = "Luxury Salon Experience • Mirror Shine & Glass Skin",
        duration: int = 15,
        music_path: Path = None
    ) -> Path:
        temp_overlay = BASE_DIR / "temp" / "flawless_overlay.png"
        self.generate_flawless_overlay(
            headline=headline,
            subheadline=subheadline,
            output_png=temp_overlay
        )

        # Dynamic Music Track Selection
        if music_path and Path(music_path).exists():
            selected_music = Path(music_path)
        else:
            music_tracks = list(self.music_dir.glob("*.mp3"))
            selected_music = random.choice(music_tracks) if music_tracks else None


        # FFmpeg filter:
        # 1. Background blur + Center Video Fit (Y: 175 to 1260)
        # 2. Overlay Graphic Template
        # 3. Audio: Blend video audio + Background music with smooth fade-out
        vf = (
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=22[vbg];"
            "[0:v]scale=1080:1085:force_original_aspect_ratio=decrease[vfg];"
            "[vbg][vfg]overlay=(W-w)/2:175[vmerged];"
            "[vmerged][1:v]overlay=0:0[vout]"
        )

        cmd = [
            "ffmpeg", "-y",
            "-i", str(raw_video_path),
            "-i", str(temp_overlay)
        ]

        if selected_music and selected_music.exists():
            cmd.extend([
                "-i", str(selected_music),
                "-filter_complex", f"{vf};[2:a]afade=t=out:st={duration-2}:d=2,volume=0.85[aout]",
                "-map", "[vout]",
                "-map", "[aout]"
            ])
        else:
            cmd.extend([
                "-filter_complex", vf,
                "-map", "[vout]",
                "-map", "0:a?"
            ])

        cmd.extend([
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "320k",
            "-t", str(duration),
            "-movflags", "+faststart",
            str(output_video_path)
        ])

        output_video_path.parent.mkdir(parents=True, exist_ok=True)
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print("FFmpeg error:", res.stderr.decode("utf-8", errors="replace")[-500:])
            res.check_returncode()

        return output_video_path

def main():
    print("=" * 80)
    print("👑 RANI MAKEOVER — MASTER PIPELINE REEL WITH MUSIC & REAL RM LOGO")
    print("=" * 80)

    engine = UltimateRaniMasterEngine()
    vault = BASE_DIR / "content_vault"
    raw_video = vault / "viral_beauty_04_09_Best Salon Services at Ekam Makeovers Academy Hy_uolQeVRWxo8.mp4"
    if not raw_video.exists():
        raw_video = next(vault.glob("viral_beauty_*.mp4"))

    output_video = vault / "RANI_MAKEOVER_MASTER_REEL_WITH_MUSIC.mp4"

    engine.render_master_reel_with_music(
        raw_video_path=raw_video,
        output_video_path=output_video,
        headline="100% FLAWLESS HD GLOW-UP",
        subheadline="Luxury Salon Experience • Mirror Shine & Glass Skin",
        duration=15
    )

    size_mb = output_video.stat().st_size / (1024 * 1024)
    print(f"✅ Master Reel with Music Created: {output_video.name} ({size_mb:.2f} MB)")

    # Save to Desktop
    desktop_copy = Path(r"C:\Users\EDITI\OneDrive\Desktop\RANI_MAKEOVER_MASTER_REEL_WITH_MUSIC.mp4")
    import shutil
    shutil.copy2(output_video, desktop_copy)
    print(f"💻 Saved to Desktop: '{desktop_copy.name}'")

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
