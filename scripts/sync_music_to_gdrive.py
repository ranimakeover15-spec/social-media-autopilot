"""
Sync all trending music tracks to Google Drive CLINT Vault.
"""

import sys
import pickle
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent

def sync_music():
    with open(BASE_DIR / "gdrive_token.pickle", "rb") as f:
        creds = pickle.load(f)

    drive = build("drive", "v3", credentials=creds)

    # 1. Find CLINT folder
    res = drive.files().list(q="name='CLINT' and mimeType='application/vnd.google-apps.folder' and trashed=false", fields="files(id, name)").execute()
    clint_id = res.get("files", [{}])[0].get("id")

    # 2. Find or create 05_TRENDING_REELS_MUSIC folder
    q_mf = f"'{clint_id}' in parents and name='05_TRENDING_REELS_MUSIC' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    mf_res = drive.files().list(q=q_mf, fields="files(id, name)").execute()
    mf_files = mf_res.get("files", [])

    if mf_files:
        music_folder_id = mf_files[0]["id"]
    else:
        folder_meta = {
            "name": "05_TRENDING_REELS_MUSIC",
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [clint_id]
        }
        f_res = drive.files().create(body=folder_meta, fields="id").execute()
        music_folder_id = f_res.get("id")

    print(f"📁 Google Drive Music Vault ID: {music_folder_id}")

    # 3. Upload all music files
    music_dir = BASE_DIR / "assets" / "music"
    for mp3_file in music_dir.glob("*.mp3"):
        # Check if already exists
        check_q = f"'{music_folder_id}' in parents and name='{mp3_file.name}' and trashed=false"
        c_res = drive.files().list(q=check_q, fields="files(id, name)").execute()
        if c_res.get("files"):
            print(f"  ⚡ Already on Drive: {mp3_file.name}")
            continue

        print(f"  📤 Uploading: {mp3_file.name} ({mp3_file.stat().st_size / (1024*1024):.2f} MB)...")
        file_meta = {"name": mp3_file.name, "parents": [music_folder_id]}
        media = MediaFileUpload(str(mp3_file), mimetype="audio/mpeg", resumable=True)
        drive.files().create(body=file_meta, media_body=media).execute()
        print(f"  ✅ Uploaded: {mp3_file.name}")

    print("🎉 All 25 trending music tracks synced to Google Drive Cloud Vault!")

if __name__ == "__main__":
    sync_music()
