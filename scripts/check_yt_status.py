"""
Inspect YouTube Video Status and Privacy for 3nmYvdZ_4-Q.
"""

import sys
import pickle
from googleapiclient.discovery import build

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def check_video():
    with open("token.pickle", "rb") as f:
        creds = pickle.load(f)
    yt = build("youtube", "v3", credentials=creds)

    res = yt.videos().list(part="snippet,status,contentDetails", id="3nmYvdZ_4-Q").execute()
    items = res.get("items", [])
    if items:
        v = items[0]
        print(f"Video ID: {v['id']}")
        print(f"Title: {v['snippet']['title']}")
        print(f"Privacy Status: {v['status']['privacyStatus']}")
        print(f"Upload Status: {v['status']['uploadStatus']}")
        print(f"Embeddable: {v['status'].get('embeddable')}")
        print(f"Made For Kids: {v['status'].get('madeForKids')}")
        print(f"Direct URL: https://www.youtube.com/watch?v={v['id']}")
        print(f"Shorts URL: https://youtube.com/shorts/{v['id']}")
    else:
        print("Video ID not found in API!")

    print("\n--- ALL RECENT VIDEOS ON CHANNEL ---")
    ch_res = yt.channels().list(part="contentDetails", mine=True).execute()
    uploads_id = ch_res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    pl_res = yt.playlistItems().list(part="snippet,status", playlistId=uploads_id, maxResults=10).execute()
    for item in pl_res.get("items", []):
        vid_id = item["snippet"]["resourceId"]["videoId"]
        title = item["snippet"]["title"]
        privacy = item["status"]["privacyStatus"]
        pub = item["snippet"]["publishedAt"]
        print(f"• [{pub}] [{privacy}] {title}")
        print(f"  Watch: https://www.youtube.com/watch?v={vid_id}")
        print(f"  Shorts: https://youtube.com/shorts/{vid_id}")

if __name__ == "__main__":
    check_video()
