"""
Check live publication status on YouTube & Instagram.
"""

import sys
import pickle
from pathlib import Path
from googleapiclient.discovery import build
from instagrapi import Client

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent

def check():
    print("=" * 80)
    print("🔍 CHECKING LIVE PUBLICATIONS ON YOUTUBE & INSTAGRAM")
    print("=" * 80)

    # 1. YouTube Check
    with open(BASE_DIR / "token.pickle", "rb") as f:
        creds = pickle.load(f)
    yt = build("youtube", "v3", credentials=creds)
    ch_res = yt.channels().list(part="contentDetails", mine=True).execute()
    uploads_list_id = ch_res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    playlist_items = yt.playlistItems().list(part="snippet,status", playlistId=uploads_list_id, maxResults=5).execute()
    print("\n📺 RECENT YOUTUBE UPLOADS:")
    for item in playlist_items.get("items", []):
        snip = item["snippet"]
        vid_id = snip["resourceId"]["videoId"]
        pub_at = snip["publishedAt"]
        title = snip["title"]
        print(f"  • [{pub_at}] {title}")
        print(f"    👉 https://youtube.com/shorts/{vid_id}")

    # 2. Instagram Check
    print("\n📸 RECENT INSTAGRAM POSTS & REELS (@Lovelyrani53):")
    try:
        session_file = BASE_DIR / "instagram_session.json"
        cl = Client()
        cl.load_settings(session_file)
        user_id = cl.user_id_from_username("Lovelyrani53")
        medias = cl.user_medias(user_id, amount=5)
        for m in medias:
            print(f"  • [{m.taken_at}] Media Type: {m.media_type} | Code: {m.code}")
            print(f"    👉 https://www.instagram.com/p/{m.code}/ (or /reel/{m.code}/)")
            print(f"    Caption: {m.caption_text[:60]}...")
    except Exception as e:
        print(f"Instagram check note: {e}")

    print("\n" + "=" * 80)

if __name__ == "__main__":
    check()
