"""
Build gdrive_map.json containing all 22 beauty salon raw videos from Google Drive 'CLINT' folder.
"""

import os
import sys
import json
import pickle
from pathlib import Path
from googleapiclient.discovery import build

BASE_DIR = Path(__file__).resolve().parent.parent

def build_map():
    with open(BASE_DIR / "gdrive_token.pickle", "rb") as f:
        creds = pickle.load(f)

    drive = build("drive", "v3", credentials=creds)

    # Search for CLINT folder
    res = drive.files().list(q="name='CLINT' and mimeType='application/vnd.google-apps.folder' and trashed=false", fields="files(id, name)").execute()
    clint_id = res.get("files", [{}])[0].get("id")
    print(f"CLINT Folder ID: {clint_id}")

    # Search for all videos in CLINT
    query = f"'{clint_id}' in parents and trashed=false"
    res = drive.files().list(q=query, fields="files(id, name, mimeType)").execute()

    files_list = []
    # Also search subfolders
    subfolders = [f for f in res.get("files", []) if f["mimeType"] == "application/vnd.google-apps.folder"]
    for sf in subfolders:
        sub_query = f"'{sf['id']}' in parents and trashed=false"
        sub_res = drive.files().list(q=sub_query, fields="files(id, name, mimeType, size)").execute()
        for f in sub_res.get("files", []):
            if "mp4" in f["name"].lower() or f["mimeType"] == "video/mp4":
                files_list.append({"id": f["id"], "name": f["name"], "size": f.get("size", 0)})

    print(f"Found {len(files_list)} raw videos in Google Drive!")

    map_path = BASE_DIR / "gdrive_map.json"
    map_data = {
        "clint_folder_id": clint_id,
        "total_clips": len(files_list),
        "clips": files_list
    }
    map_path.write_text(json.dumps(map_data, indent=2), encoding="utf-8")
    print(f"Saved gdrive_map.json to {map_path}")

if __name__ == "__main__":
    build_map()
