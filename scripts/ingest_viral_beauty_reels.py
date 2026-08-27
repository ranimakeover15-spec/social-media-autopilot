"""
Ingest 22 Viral Beauty & Salon HD Reels from D:\Viral_Reels_HD\... into:
1. Local content_vault (for immediate autopilot scheduling)
2. Google Drive 'CLINT' Folder (04_VIRAL_BEAUTY_REELS_VAULT) for 24/7 Cloud Autopilot!
"""

import os
import sys
import shutil
from pathlib import Path

# Enforce UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

SOURCE_DIR = Path(r"D:\Viral_Reels_HD\Beauty_Parlour_Salon_Special\50_Viral_Reels_HD")
VAULT_DIR = BASE_DIR / "content_vault"

def main():
    print("=" * 80)
    print("🎬 INGESTING 22 VIRAL BEAUTY & SALON HD REELS INTO VAULT")
    print("=" * 80)

    if not SOURCE_DIR.exists():
        print(f"⚠️ Source directory not found: {SOURCE_DIR}")
        return

    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    video_files = list(SOURCE_DIR.glob("*.mp4"))

    print(f"📂 Total Videos Found: {len(video_files)}")
    print("-" * 80)

    for idx, vf in enumerate(video_files, 1):
        clean_name = f"viral_beauty_{idx:02d}_{vf.name}"
        # Sanitize filename
        clean_name = "".join(c for c in clean_name if c.isalnum() or c in " ._-").replace("  ", " ")
        dest_path = VAULT_DIR / clean_name

        if not dest_path.exists():
            shutil.copy2(vf, dest_path)
            size_mb = dest_path.stat().st_size / (1024 * 1024)
            print(f"{idx:2d}. ✅ Ingested to Vault: '{dest_path.name[:45]}' ({size_mb:.2f} MB)")
        else:
            print(f"{idx:2d}. ℹ️ Already in Vault: '{dest_path.name[:45]}'")

    print("-" * 80)
    print(f"🎉 Successfully ingested {len(video_files)} HD Beauty Reels into content_vault!")

    # Upload to Google Drive 'CLINT' folder
    try:
        print("\n☁️ Syncing Viral Reels to Google Drive 'CLINT' Vault...")
        from scripts.upload_to_gdrive_clint import get_gdrive_service, find_or_create_folder, upload_file

        service = get_gdrive_service()
        clint_id = find_or_create_folder(service, "CLINT")
        viral_vault_id = find_or_create_folder(service, "04_VIRAL_BEAUTY_REELS_VAULT", parent_id=clint_id)

        for vf in VAULT_DIR.glob("viral_beauty_*.mp4"):
            upload_file(service, vf, viral_vault_id, mime_type="video/mp4")

        print("=" * 80)
        print("🎉 ALL 22 VIRAL BEAUTY REELS SUCCESSFULLY UPLOADED TO GOOGLE DRIVE CLOUD!")
        print("=" * 80)
    except Exception as e:
        print(f"GDrive cloud upload note: {e}")

if __name__ == "__main__":
    main()
