"""
Unified Master Autopilot Runner.
24/7 autonomous coordinator that:
1. Detects current IST slot (Morning 09:00 AM, Afternoon 02:00 PM, Evening 07:00 PM).
2. Restores cloud environment secrets if running in GitHub Actions.
3. Ingests next unposted video from vault with deduplication check.
4. Transcodes to high-compatibility 1080x1920 9:16 vertical video (+faststart, AAC, H.264).
5. Generates high-CTR platform-tailored SEO metadata.
6. Publishes across YouTube Shorts, Instagram Reels, and Facebook Reels.
7. Logs state to logs/used_reels.json and cleans temporary artifacts.
"""

import sys
import os
import argparse
import pytz
from datetime import datetime
from pathlib import Path

# Enforce UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from core.logger import logger
from core.config import config
from core.vault import ContentVault
from core.deduplicator import Deduplicator
from core.transcoder import Transcoder
from core.seo_engine import SEOEngine
from uploaders.youtube_uploader import YouTubeUploader
from uploaders.instagram_uploader import InstagramUploader
from uploaders.facebook_uploader import FacebookUploader

def get_current_ist_slot() -> str:
    """Calculates active scheduled slot according to Indian Standard Time (IST)."""
    tz = pytz.timezone(config.timezone)
    now_ist = datetime.now(tz)
    hour = now_ist.hour

    if 7 <= hour < 12:
        slot = "Morning"
    elif 12 <= hour < 17:
        slot = "Afternoon"
    else:
        slot = "Evening"

    logger.info(f"🕒 Current Time ({config.timezone}): {now_ist.strftime('%Y-%m-%d %I:%M:%S %p')} -> Slot: {slot}")
    return slot

def run_pipeline(slot_override: str = None, dry_run: bool = False) -> int:
    """Executes the master autopilot pipeline."""
    print("=" * 80)
    print("🚀 24/7 AUTONOMOUS SOCIAL MEDIA PIPELINE - MASTER RUNNER")
    print("=" * 80)

    # 1. Slot Determination
    slot = slot_override or get_current_ist_slot()
    logger.info(f"📍 Active Execution Slot: [{slot}]")

    # 2. Restore cloud secrets
    restored_secrets = config.restore_secrets_to_files()
    if restored_secrets:
        logger.info(f"🔐 Decoded {len(restored_secrets)} cloud secret(s) to runtime.")

    # 3. Vault & Deduplication
    vault = ContentVault()
    dedup = Deduplicator()

    all_videos = vault.get_all_available_videos()
    if not all_videos:
        logger.warning("⚠️ No video files found in the content vault! Please add videos to 'content_vault' or Google Drive.")
        return 0

    available_videos = dedup.filter_available_videos(all_videos)
    if not available_videos:
        logger.warning("⚠️ No available videos after deduplication check.")
        return 0

    selected_video = available_videos[0]
    logger.info(f"🎬 Selected Video for Slot [{slot}]: '{selected_video.name}' (Remaining in cycle: {len(available_videos) - 1})")

    file_hash = dedup.calculate_file_hash(selected_video)

    # 4. Transcoding
    transcoder = Transcoder()
    try:
        transcoded_video = transcoder.transcode(selected_video)
    except Exception as e:
        logger.error(f"❌ Transcoding step aborted: {e}")
        return 1

    # 5. SEO Generation
    seo_metadata = SEOEngine.generate_metadata(
        filename=selected_video.name,
        slot_name=slot
    )

    if dry_run:
        logger.info("🧪 DRY RUN enabled. Video transcoded and SEO generated. Skipping uploads.")
        return 0

    # 6. Multi-Platform Uploads
    results = {}

    # (A) YouTube Shorts
    try:
        yt_uploader = YouTubeUploader()
        results["youtube"] = yt_uploader.upload_short(transcoded_video, seo_metadata)
    except Exception as e:
        logger.error(f"❌ YouTube upload exception: {e}")
        results["youtube"] = {"status": "failed", "error": str(e)}

    # (B) Instagram Reels
    try:
        ig_uploader = InstagramUploader()
        results["instagram"] = ig_uploader.upload_reel(transcoded_video, seo_metadata)
    except Exception as e:
        logger.error(f"❌ Instagram upload exception: {e}")
        results["instagram"] = {"status": "failed", "error": str(e)}

    # (C) Facebook Reels
    try:
        fb_uploader = FacebookUploader()
        results["facebook"] = fb_uploader.upload_reel(transcoded_video, seo_metadata)
    except Exception as e:
        logger.error(f"❌ Facebook upload exception: {e}")
        results["facebook"] = {"status": "failed", "error": str(e)}

    # 7. Summary & Deduplication Logging
    logger.info("=" * 80)
    logger.info("📊 MULTI-PLATFORM DISTRIBUTION REPORT:")
    logger.info("=" * 80)

    any_success = False
    for platform, status in results.items():
        st = status.get("status", "unknown")
        if st == "success":
            any_success = True
            logger.info(f"✅ {platform.upper()}: SUCCESS -> {status.get('url') or status.get('media_id')}")
        elif st == "skipped":
            logger.info(f"⏭️ {platform.upper()}: SKIPPED ({status.get('error')})")
        else:
            logger.error(f"❌ {platform.upper()}: FAILED ({status.get('error')})")

    if any_success:
        dedup.record_upload(
            file_name=selected_video.name,
            file_hash=file_hash,
            slot_name=slot,
            platform_statuses=results,
            metadata=seo_metadata
        )
        logger.info(f"🎉 Successfully completed distribution for slot [{slot}]!")
    else:
        logger.warning("⚠️ No platforms succeeded or all were skipped.")

    # 8. Temporary Artifact Cleanup
    try:
        if transcoded_video.exists() and "temp" in str(transcoded_video):
            transcoded_video.unlink()
            logger.info(f"🧹 Cleaned up temporary transcode file: {transcoded_video.name}")
    except Exception as e:
        logger.debug(f"Cleanup note: {e}")

    return 0

def main():
    parser = argparse.ArgumentParser(description="24/7 Autonomous Social Media Master Runner.")
    parser.add_argument("--slot", "-s", type=str, choices=["Morning", "Afternoon", "Evening"], help="Force specific slot name.")
    parser.add_argument("--dry-run", action="store_true", help="Execute without uploading to live social media APIs.")
    args = parser.parse_args()

    exit_code = run_pipeline(slot_override=args.slot, dry_run=args.dry_run)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
