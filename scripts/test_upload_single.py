"""
Single Video Test Runner & Dry-Run Utility.
Allows testing transcoding, SEO generation, deduplication, and live upload for a specific video.
"""

import sys
import argparse
from pathlib import Path

# Enforce UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from core.logger import logger
from core.config import config
from core.transcoder import Transcoder
from core.seo_engine import SEOEngine
from core.deduplicator import Deduplicator
from core.vault import ContentVault
from uploaders.youtube_uploader import YouTubeUploader
from uploaders.instagram_uploader import InstagramUploader
from uploaders.facebook_uploader import FacebookUploader

def main():
    parser = argparse.ArgumentParser(description="Test pipeline on a single video file.")
    parser.add_argument("--file", "-f", type=str, help="Path to video file. If omitted, takes first available from vault.")
    parser.add_argument("--slot", "-s", type=str, default="Morning", choices=["Morning", "Afternoon", "Evening"])
    parser.add_argument("--platform", "-p", type=str, default="all", choices=["all", "youtube", "instagram", "facebook"])
    parser.add_argument("--dry-run", action="store_true", help="Run transcoding & SEO without uploading to live platforms.")
    args = parser.parse_args()

    print("=" * 70)
    print(f"🚀 Running Single Test Pipeline [Slot: {args.slot} | Dry Run: {args.dry_run}]")
    print("=" * 70)

    # 1. Source Video Selection
    vault = ContentVault()
    if args.file:
        video_path = Path(args.file)
        if not video_path.exists():
            logger.error(f"Specified file does not exist: {video_path}")
            return
    else:
        all_videos = vault.get_all_available_videos()
        if not all_videos:
            logger.error("No videos found in content vault!")
            return
        video_path = all_videos[0]

    logger.info(f"🎯 Target video selected: {video_path.name}")

    # 2. Transcoding
    transcoder = Transcoder()
    try:
        transcoded_path = transcoder.transcode(video_path)
    except Exception as e:
        logger.error(f"Transcoding test failed: {e}")
        return

    # 3. SEO Metadata
    metadata = SEOEngine.generate_metadata(video_path.name, slot_name=args.slot)
    print("\n--- Generated SEO Package ---")
    print(f"Title: {metadata['title']}")
    print(f"Hashtags: {metadata['hashtags_string']}")
    print("-" * 30 + "\n")

    if args.dry_run:
        logger.info("🏁 Dry run completed successfully! No uploads performed.")
        return

    # 4. Live Platform Upload
    results = {}
    dedup = Deduplicator()
    file_hash = dedup.calculate_file_hash(video_path)

    if args.platform in ("all", "youtube"):
        yt = YouTubeUploader()
        results["youtube"] = yt.upload_short(transcoded_path, metadata)

    if args.platform in ("all", "instagram"):
        ig = InstagramUploader()
        results["instagram"] = ig.upload_reel(transcoded_path, metadata)

    if args.platform in ("all", "facebook"):
        fb = FacebookUploader()
        results["facebook"] = fb.upload_reel(transcoded_path, metadata)

    print("\n" + "=" * 70)
    print("📊 UPLOAD SUMMARY")
    print("=" * 70)
    for plat, res in results.items():
        print(f"[{plat.upper()}]: Status = {res.get('status')} | Result = {res}")

    # Deduplication recording if any upload succeeded
    if any(r.get("status") == "success" for r in results.values()):
        dedup.record_upload(
            file_name=video_path.name,
            file_hash=file_hash,
            slot_name=args.slot,
            platform_statuses=results,
            metadata=metadata
        )

if __name__ == "__main__":
    main()
