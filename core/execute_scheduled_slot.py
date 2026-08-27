"""
👑 RANI MAKEOVER — UNIFIED SCHEDULED SLOT EXECUTOR
Executes the exact scheduled content based on Alternate-Day Rules:
1. YouTube: ALWAYS 3 Video Reels/Shorts per day.
2. Instagram/FB: Alternate-day afternoon poster (with fresh text/offer), otherwise reels.
"""

import sys
import datetime
from pathlib import Path

# Enforce UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from core.smart_alternate_day_scheduler import SmartAlternateScheduler
from core.anti_repetition_dynamic_rotator import ContentRotator
from core.ultimate_master_reel_engine import UltimateRaniMasterEngine

def run_slot(slot_name: str = "afternoon"):
    print("=" * 80)
    print(f"🚀 EXECUTING SCHEDULED SLOT: {slot_name.upper()} IST")
    print("=" * 80)

    scheduler = SmartAlternateScheduler()
    plan = scheduler.get_publishing_plan(slot_name)
    rotator = ContentRotator()
    bundle = rotator.get_next_unique_bundle()

    print(f"📅 Date: {plan['date']} | Is Poster Day: {plan['is_poster_day']}")
    print(f"📺 YouTube Action: {plan['youtube']}")
    print(f"📸 Instagram/FB Action: {plan['instagram_and_facebook']}")
    print(f"✨ Content Hook: {bundle['headline']}")
    print(f"🎁 Offer: {bundle['offer'][0]} ({bundle['offer'][1]})")

    # 1. ALWAYS Render & Publish YouTube Short
    print("\n[STEP 1] Generating & Publishing YouTube Short...")
    engine = UltimateRaniMasterEngine()
    out_video = BASE_DIR / "content_vault" / f"scheduled_reel_{slot_name}.mp4"
    engine.render_master_reel_with_music(
        raw_video_path=bundle["video_path"],
        output_video_path=out_video,
        headline=bundle["headline"],
        subheadline=bundle["subheadline"],
        duration=15
    )

    # Publish to YouTube
    try:
        from uploaders.youtube_uploader import YouTubeUploader
        yt = YouTubeUploader()
        yt_meta = {
            "title": f"Rani Makeover • {bundle['headline']} ✨ #Shorts #Viral",
            "description": f"{bundle['subheadline']}\n\n📞 Call/WhatsApp: +91 9334668807\n📍 Address: Shop No. G-38, RC Plaza, Kirari Chowk, Nangloi, Delhi - 110086\n📸 Instagram: @Lovelyrani53\n#RaniMakeover #BeautySalon #Shorts",
            "tags": ["Rani Makeover", "Beauty Parlour", "Delhi Salon", "Shorts", "Trending"]
        }
        yt.upload_short(out_video, yt_meta)
    except Exception as e:
        print(f"YouTube publishing note: {e}")

    # 2. Instagram & Facebook Action
    if plan["instagram_and_facebook"] == "CANVA_LUXURY_POSTER":
        print("\n[STEP 2] Rendering & Publishing Canva Luxury Poster (Alternate-Day Afternoon)...")
        from scripts.render_master_creative_demo import render_creative
        render_creative()
        from scripts.publish_poster_to_instagram import main as pub_poster
        pub_poster()
    else:
        print("\n[STEP 2] Publishing Video Reel to Instagram Reels + Story + FB...")
        from scripts.publish_full_meta_suite import main as pub_reel
        pub_reel()

    print("\n" + "=" * 80)
    print(f"🎉 {slot_name.upper()} SCHEDULED SLOT PUBLISHED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    slot = sys.argv[1] if len(sys.argv) > 1 else "afternoon"
    run_slot(slot)
