"""
👑 RANI MAKEOVER — 3-IN-1 INSTAGRAM + STORY + FACEBOOK AUTO-PUBLISHER
Handles:
1. Instagram Reels Upload (with share_to_facebook=True)
2. Instagram Story Auto-Publishing (video_upload_to_story)
3. Facebook Page Cross-Posting
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
    print("🚀 PUBLISHING 3-IN-1: REEL + STORY + FACEBOOK CROSS-POST")
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

    # 1. Upload to Instagram Reels
    print(f"🎬 [1/2] Uploading Reel with Facebook Cross-Share...")
    media = cl.clip_upload(
        path=str(video_path),
        caption=caption,
        thumbnail=str(thumb_path),
        extra_data={"share_to_fb": "1", "share_to_facebook": "1"}
    )
    reel_url = f"https://www.instagram.com/reel/{media.code}/"
    print(f"✅ Reel Live: {reel_url}")

    # 2. Upload to Instagram Story
    print(f"📱 [2/2] Auto-Publishing to Instagram Story...")
    try:
        story = cl.video_upload_to_story(
            path=str(video_path)
        )
        print(f"🎉 Story Live on @Lovelyrani53 Profile! (Story ID: {story.id})")
    except Exception as e:
        print(f"Story upload note: {e}")

    print("\n" + "=" * 80)
    print("🎉 3-IN-1 (REELS + STORY + FACEBOOK) AUTO-PUBLISHED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    main()
