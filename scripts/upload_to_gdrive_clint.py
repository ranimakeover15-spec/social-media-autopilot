"""
Create 'CLINT' folder in 5TB Google Drive and upload all client assets and data.
"""

import os
import sys
import pickle
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

# Enforce UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent

def get_gdrive_service():
    token_candidates = [
        BASE_DIR / "gdrive_token.pickle",
        Path(r"D:\WORKING\AUTOPILOT_BOTS\cosmic_matrix_bot\gdrive_token.pickle")
    ]
    token_file = next((p for p in token_candidates if p.exists()), None)
    if not token_file:
        raise FileNotFoundError("gdrive_token.pickle not found!")

    with open(token_file, "rb") as f:
        creds = pickle.load(f)

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(token_file, "wb") as f:
            pickle.dump(creds, f)

    return build("drive", "v3", credentials=creds)

def find_or_create_folder(service, folder_name: str, parent_id: str = None) -> str:
    """Finds existing folder or creates a new one in Google Drive."""
    query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    if parent_id:
        query += f" and '{parent_id}' in parents"

    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])

    if files:
        folder_id = files[0]["id"]
        print(f"📁 Existing Folder Found: '{folder_name}' (ID: {folder_id})")
        return folder_id

    # Create new folder
    metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder"
    }
    if parent_id:
        metadata["parents"] = [parent_id]

    folder = service.files().create(body=metadata, fields="id").execute()
    folder_id = folder.get("id")
    print(f"✨ New Folder Created in Google Drive: '{folder_name}' (ID: {folder_id})")
    return folder_id

def upload_file(service, local_path: Path, parent_folder_id: str, mime_type: str = None):
    """Uploads a local file into a specific Google Drive folder."""
    if not local_path.exists():
        print(f"⚠️ File not found to upload: {local_path}")
        return None

    # Check if already uploaded
    query = f"name = '{local_path.name}' and '{parent_folder_id}' in parents and trashed = false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])

    if files:
        print(f"ℹ️ File already exists in GDrive: '{local_path.name}' (ID: {files[0]['id']})")
        return files[0]["id"]

    print(f"⬆️ Uploading to GDrive: '{local_path.name}' ({local_path.stat().st_size / (1024*1024):.2f} MB)...")

    file_metadata = {
        "name": local_path.name,
        "parents": [parent_folder_id]
    }

    media = MediaFileUpload(str(local_path), mimetype=mime_type or "application/octet-stream", resumable=True)
    uploaded = service.files().create(body=file_metadata, media_body=media, fields="id, webViewLink").execute()
    file_id = uploaded.get("id")
    print(f"✅ Successfully Uploaded: '{local_path.name}' (ID: {file_id})")
    return file_id

def main():
    print("=" * 80)
    print("☁️ GOOGLE DRIVE 'CLINT' FOLDER CREATION & DATA SYNC")
    print("=" * 80)

    service = get_gdrive_service()

    # 1. Create root 'CLINT' folder
    clint_folder_id = find_or_create_folder(service, "CLINT")

    # 2. Create subfolders
    videos_folder_id = find_or_create_folder(service, "01_RANI_MAKEOVER_VIDEOS", parent_id=clint_folder_id)
    prompts_folder_id = find_or_create_folder(service, "02_DESIGN_SYSTEM_AND_PROMPTS", parent_id=clint_folder_id)
    scripts_folder_id = find_or_create_folder(service, "03_AUTOPILOT_SYSTEM_BACKUP", parent_id=clint_folder_id)

    # 3. Upload Videos
    vault_dir = BASE_DIR / "content_vault"
    for v in vault_dir.glob("*.mp4"):
        upload_file(service, v, videos_folder_id, mime_type="video/mp4")

    # 4. Upload Posters
    temp_dir = BASE_DIR / "temp"
    for img in temp_dir.glob("*.png"):
        upload_file(service, img, videos_folder_id, mime_type="image/png")

    # 5. Upload Master Prompts & Docs
    desktop_prompt = Path(r"C:\Users\EDITI\OneDrive\Desktop\MASTER_AI_AGENT_PROMPT_FOR_REELS.md")
    if desktop_prompt.exists():
        upload_file(service, desktop_prompt, prompts_folder_id, mime_type="text/markdown")

    readme = BASE_DIR / "README.md"
    if readme.exists():
        upload_file(service, readme, prompts_folder_id, mime_type="text/markdown")

    # 6. Upload Core Automation Scripts
    core_files = [
        BASE_DIR / "unified_master_autopilot.py",
        BASE_DIR / "core" / "video_creator.py",
        BASE_DIR / "core" / "seo_engine.py",
        BASE_DIR / "core" / "transcoder.py",
        BASE_DIR / "core" / "vault.py",
        BASE_DIR / "requirements.txt"
    ]
    for cf in core_files:
        if cf.exists():
            upload_file(service, cf, scripts_folder_id, mime_type="text/plain")

    print("\n" + "=" * 80)
    print("🎉 ALL CLIENT DATA & VIDEOS SUCCESSFULLY SAVED TO 'CLINT' FOLDER ON GOOGLE DRIVE!")
    print(f"📁 Main 'CLINT' Folder ID: {clint_folder_id}")
    print(f"🔗 Google Drive URL: https://drive.google.com/drive/folders/{clint_folder_id}")
    print("=" * 80)

if __name__ == "__main__":
    main()
