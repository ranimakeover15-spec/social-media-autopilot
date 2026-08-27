"""
Publish to Instagram Story with thumbnail.
"""

import os
import sys
from pathlib import Path
from instagrapi import Client

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
SESSION_FILE = BASE_DIR / "instagram_session.json"

def main():
    if not SESSION_FILE.exists():
        return

    cl = Client()
    cl.load_settings(SESSION_FILE)

    video_path = BASE_DIR / "content_vault" / "RANI_MAKEOVER_MASTER_REEL_WITH_MUSIC.mp4"
    thumb_path = BASE_DIR / "temp" / f"thumb_{video_path.stem}.jpg"

    print("Publishing Story to Instagram Profile @Lovelyrani53...")
    try:
        story = cl.video_upload_to_story(
            path=str(video_path),
            thumbnail=str(thumb_path)
        )
        print(f"INSTAGRAM STORY IS LIVE! Story ID: {story.id}")
    except Exception as e:
        print(f"Story upload error: {e}")

if __name__ == "__main__":
    main()
