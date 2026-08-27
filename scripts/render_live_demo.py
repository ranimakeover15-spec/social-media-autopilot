"""
Quick Demo Script for Master Salon Video Processor.
"""

import sys
from pathlib import Path

# Enforce UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from core.master_salon_video_processor import MasterSalonVideoProcessor

def main():
    print("=" * 80)
    print("🎬 CREATING LIVE DEMO 2: ROYAL BRIDAL TRANSFORMATION REEL")
    print("=" * 80)

    processor = MasterSalonVideoProcessor()
    vault = BASE_DIR / "content_vault"
    raw_video = vault / "viral_beauty_21_38_Stunning Rashmika Mandannas bridal Makeup_LwvBQhjHNso.mp4"
    if not raw_video.exists():
        raw_video = next(vault.glob("viral_beauty_*.mp4"))

    demo_output = vault / "demo_royal_bridal_reel.mp4"

    print(f"🎬 Processing Raw Footage: '{raw_video.name}'...")
    metadata = processor.produce_master_salon_reel(
        raw_video_path=raw_video,
        output_video_path=demo_output,
        headline="✨ Royal Bridal Transformation ✨",
        subheadline="Signature HD Bridal Glam & Glass Skin Glow",
        duration=15
    )

    print("\n" + "=" * 80)
    print("🎉 DEMO VIDEO REEL READY!")
    print(f"📁 Video Location: {demo_output} ({metadata['size_mb']} MB)")
    print(f"📝 Title: {metadata['title']}")
    print("=" * 80)

    # Sync to Google Drive
    try:
        from scripts.upload_to_gdrive_clint import get_gdrive_service, find_or_create_folder, upload_file
        service = get_gdrive_service()
        clint_id = find_or_create_folder(service, "CLINT")
        vid_id = find_or_create_folder(service, "01_RANI_MAKEOVER_VIDEOS", parent_id=clint_id)
        upload_file(service, demo_output, vid_id, mime_type="video/mp4")
        print("☁️ Demo Reel Synced to Google Drive 'CLINT' Folder!")
    except Exception as e:
        print(f"GDrive note: {e}")

if __name__ == "__main__":
    main()
