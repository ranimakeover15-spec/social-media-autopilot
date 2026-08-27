"""
Publish 10:00 AM Slot YouTube Short to 'Rani makeover' Official Channel.
"""

import os
import sys
import pickle
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Enforce UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent

def main():
    print("=" * 80)
    print("🚀 PUBLISHING 10:00 AM MASTER SHORT TO 'Rani makeover' YOUTUBE CHANNEL")
    print("=" * 80)

    token_path = BASE_DIR / "token.pickle"
    if not token_path.exists():
        print("❌ token.pickle not found!")
        return

    with open(token_path, "rb") as f:
        creds = pickle.load(f)

    youtube = build("youtube", "v3", credentials=creds)

    video_path = BASE_DIR / "content_vault" / "RANI_MAKEOVER_MASTER_REEL_WITH_MUSIC.mp4"
    if not video_path.exists():
        video_path = BASE_DIR / "content_vault" / "RANI_MAKEOVER_PERFECT_MASTER_SHORT.mp4"

    title = "Rani Makeover • 100% Flawless HD Glow-Up & Bridal Glamour ✨ #Shorts #Viral"
    description = (
        "Experience luxury salon treatments, radiant skin facials & signature HD bridal makeover at Rani Makeover & Beauty Lounge.\n\n"
        "✨ Complete 5-in-1 Festive & Bridal Packages Open!\n"
        "📞 Call / WhatsApp for Appointments: +91 9334668807\n"
        "📍 Address: Shop No. G-38, RC Plaza, Kirari Chowk, Nangloi, Delhi - 110086\n"
        "📸 Follow Instagram: @Lovelyrani53\n"
        "▶ Subscribe: Rani makeover\n\n"
        "#RaniMakeover #BeautyParlour #DelhiSalon #HydraFacial #BridalMakeup #Nangloi #SkinCare #Shorts #Viral"
    )
    tags = ["Rani Makeover", "Delhi Salon", "Beauty Parlour", "Hydra Facial", "Hair Spa", "Bridal Makeup", "Nangloi", "Shorts", "Trending Reels"]

    body = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags,
            "categoryId": "26"  # Howto & Style
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    print(f"🎬 Uploading Video File: '{video_path.name}' ({video_path.stat().st_size / (1024*1024):.2f} MB)...")
    print(f"📝 Video Title: {title}")
    print("⏳ Streaming to YouTube Data API v3...")

    media = MediaFileUpload(str(video_path), mimetype="video/mp4", resumable=True, chunksize=1024*1024*5)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"📊 Upload Progress: {int(status.progress() * 100)}%...")

    video_id = response.get("id")
    video_url = f"https://www.youtube.com/shorts/{video_id}"

    print("\n" + "=" * 80)
    print("🎉 YOUTUBE SHORT PUBLISHED LIVE SUCCESSFULLY!")
    print(f"🔗 Video URL: {video_url}")
    print(f"🆔 Video ID: {video_id}")
    print("=" * 80)

if __name__ == "__main__":
    main()
