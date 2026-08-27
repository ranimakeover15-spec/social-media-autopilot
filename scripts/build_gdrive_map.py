"""
👑 RANI MAKEOVER — STRICT RAW-ONLY GDRIVE MAP GENERATOR
Strict Rule:
Only pure unbranded raw footage (from '04_VIRAL_BEAUTY_REELS_VAULT' or named 'viral_beauty_*.mp4')
is allowed. All previously branded/rendered videos are STRICTLY EXCLUDED.
"""

import os
import sys
import json
import pickle
from pathlib import Path
from googleapiclient.discovery import build

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent

EXCLUDED_BRANDED_KEYWORDS = [
    "branded", "master", "demo_", "scheduled_", "live_publish_", 
    "auto_reel_", "perfect_", "raksha_bandhan", "rani_makeover_",
    "final_reel", "output", "client_reel", "exact_reference"
]

def is_pure_raw_footage(filename: str) -> bool:
    name_lower = filename.lower()
    for kw in EXCLUDED_BRANDED_KEYWORDS:
        if kw in name_lower:
            return False
    return name_lower.endswith(".mp4") and ("viral_beauty_" in name_lower or "raw" in name_lower)

def build_strict_raw_map():
    with open(BASE_DIR / "gdrive_token.pickle", "rb") as f:
        creds = pickle.load(f)

    drive = build("drive", "v3", credentials=creds)

    # 1. Search for CLINT folder
    res = drive.files().list(q="name='CLINT' and mimeType='application/vnd.google-apps.folder' and trashed=false", fields="files(id, name)").execute()
    clint_id = res.get("files", [{}])[0].get("id")
    print(f"CLINT Folder ID: {clint_id}")

    # 2. Search for 04_VIRAL_BEAUTY_REELS_VAULT inside CLINT
    q_vault = f"'{clint_id}' in parents and name='04_VIRAL_BEAUTY_REELS_VAULT' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    vault_res = drive.files().list(q=q_vault, fields="files(id, name)").execute()
    vault_folders = vault_res.get("files", [])

    raw_clips = []

    if vault_folders:
        vault_id = vault_folders[0]["id"]
        print(f"Found Pure Raw Vault: '04_VIRAL_BEAUTY_REELS_VAULT' (ID: {vault_id})")
        q_files = f"'{vault_id}' in parents and trashed=false"
        files_res = drive.files().list(q=q_files, fields="files(id, name, size, mimeType)").execute()
        for f in files_res.get("files", []):
            if is_pure_raw_footage(f["name"]):
                raw_clips.append({"id": f["id"], "name": f["name"], "size": f.get("size", 0)})

    # Also search general CLINT folder with strict filter
    q_all = f"'{clint_id}' in parents and trashed=false"
    all_res = drive.files().list(q=q_all, fields="files(id, name, size, mimeType)").execute()
    for f in all_res.get("files", []):
        if is_pure_raw_footage(f["name"]) and f["id"] not in [c["id"] for c in raw_clips]:
            raw_clips.append({"id": f["id"], "name": f["name"], "size": f.get("size", 0)})

    print(f"Found {len(raw_clips)} PURE RAW UNBRANDED videos in Google Drive (0% Branded Files).")

    map_path = BASE_DIR / "gdrive_map.json"
    map_data = {
        "clint_folder_id": clint_id,
        "total_clips": len(raw_clips),
        "clips": raw_clips
    }
    map_path.write_text(json.dumps(map_data, indent=2), encoding="utf-8")
    print(f"Saved strict gdrive_map.json to {map_path}")

if __name__ == "__main__":
    build_strict_raw_map()
