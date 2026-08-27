"""
Publish Live Reel directly to Instagram (@Lovelyrani53) with pre-generated FFmpeg thumbnail.
"""

import os
import sys
import subprocess
from pathlib import Path
from instagrapi import Client

# Enforce UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
SESSION_FILE = BASE_DIR / "instagram_session.json"

def generate_thumbnail(video_path: Path, thumb_path: Path) -> Path:
    cmd = [
        "ffmpeg", "-y",
        "-ss", "00:00:01",
        "-i", str(video_path),
        "-vframes", "1",
        "-q:v", "2",
        str(thumb_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return thumb_path

def main():
    print("=" * 80)
    print("🚀 PUBLISHING MASTER REEL LIVE TO INSTAGRAM (@Lovelyrani53)")
    print("=" * 80)

    if not SESSION_FILE.exists():
        print("❌ instagram_session.json not found!")
        return

    cl = Client()
    cl.load_settings(SESSION_FILE)

    video_path = BASE_DIR / "content_vault" / "RANI_MAKEOVER_MASTER_REEL_WITH_MUSIC.mp4"
    if not video_path.exists():
        video_path = BASE_DIR / "content_vault" / "RANI_MAKEOVER_PERFECT_MASTER_SHORT.mp4"

    thumb_path = BASE_DIR / "temp" / f"thumb_{video_path.stem}.jpg"
    thumb_path.parent.mkdir(parents=True, exist_ok=True)
    generate_thumbnail(video_path, thumb_path)

    caption = (
        "✨ 100% FLAWLESS HD GLOW-UP & BRIDAL GLAMOUR ✨\n\n"
        "Experience luxury salon care, glowing skin facials, and signature bridal makeover at Rani Makeover & Beauty Lounge Nangloi Delhi.\n\n"
        "👑 Limited Festive & Wedding Slots Open!\n"
        "📞 Call / WhatsApp for Bookings: +91 9334668807\n"
        "📍 Address: Shop No. G-38, RC Plaza, Kirari Chowk, Nangloi, Delhi - 110086\n"
        "▶ YouTube: Rani makeover\n\n"
        "#RaniMakeover #BeautyParlour #DelhiSalon #HydraFacial #BridalMakeup #Nangloi #SkinCare #TrendingReels #ExplorePage #ViralReels"
    )

    print(f"🎬 Uploading Reel Video: '{video_path.name}' ({video_path.stat().st_size / (1024*1024):.2f} MB)...")
    print(f"🖼️ Generated Thumbnail: '{thumb_path.name}'")
    print("⏳ Streaming to Instagram Reels...")

    media = cl.clip_upload(
        path=str(video_path),
        caption=caption,
        thumbnail=str(thumb_path)
    )

    reel_url = f"https://www.instagram.com/reel/{media.code}/"

    print("\n" + "=" * 80)
    print("🎉 INSTAGRAM REEL PUBLISHED LIVE SUCCESSFULLY!")
    print(f"🔗 Reel URL: {reel_url}")
    print(f"🆔 Media ID: {media.id} | Code: {media.code}")
    print("=" * 80)

if __name__ == "__main__":
    main()
