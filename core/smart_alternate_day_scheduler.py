"""
👑 RANI MAKEOVER — SMART ALTERNATE-DAY CONTENT SCHEDULER
Rules:
1. YouTube Shorts: ALWAYS 3 Video Reels/Shorts Every Single Day (09:00 AM, 02:00 PM, 07:00 PM IST).
2. Instagram & Facebook:
   - Day 1: 09:00 AM (Reel), 02:00 PM (Reel), 07:00 PM (Reel)
   - Day 2: 09:00 AM (Reel), 02:00 PM (🎨 CANVA LUXURY POSTER with New Text/Offer), 07:00 PM (Reel)
   - Repeats alternately!
"""

import os
import sys
import json
import datetime
from pathlib import Path
from typing import Dict, Any

# Enforce UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
SCHEDULE_TRACKER_FILE = BASE_DIR / "content_vault" / "schedule_tracker.json"

class SmartAlternateScheduler:
    def __init__(self):
        self._load_tracker()

    def _load_tracker(self):
        if SCHEDULE_TRACKER_FILE.exists():
            try:
                self.tracker = json.loads(SCHEDULE_TRACKER_FILE.read_text(encoding="utf-8"))
            except Exception:
                self.tracker = {"day_count": 1, "last_poster_date": ""}
        else:
            self.tracker = {"day_count": 1, "last_poster_date": ""}

    def _save_tracker(self):
        SCHEDULE_TRACKER_FILE.parent.mkdir(parents=True, exist_ok=True)
        SCHEDULE_TRACKER_FILE.write_text(json.dumps(self.tracker, indent=2), encoding="utf-8")

    def get_publishing_plan(self, slot_name: str = "afternoon") -> Dict[str, Any]:
        """
        slot_name: 'morning' (09:00 AM), 'afternoon' (02:00 PM), or 'evening' (07:00 PM)
        Returns the exact publishing plan for YouTube and Instagram/FB.
        """
        today_str = datetime.date.today().isoformat()
        day_of_year = datetime.date.today().timetuple().tm_yday

        # Check if today is a Poster Day (Alternate Days: day_of_year % 2 == 0)
        is_poster_day = (day_of_year % 2 == 0)

        # YouTube ALWAYS gets Video Reel
        yt_plan = "VIDEO_REEL"

        # Instagram / FB logic:
        # Only on Poster Days during Afternoon (02:00 PM), post a Poster.
        # Otherwise post Video Reel.
        if is_poster_day and slot_name.lower() == "afternoon":
            insta_plan = "CANVA_LUXURY_POSTER"
            self.tracker["last_poster_date"] = today_str
            self._save_tracker()
        else:
            insta_plan = "VIDEO_REEL"

        return {
            "date": today_str,
            "slot": slot_name.lower(),
            "is_poster_day": is_poster_day,
            "youtube": yt_plan,
            "instagram_and_facebook": insta_plan
        }

if __name__ == "__main__":
    scheduler = SmartAlternateScheduler()
    print("=" * 80)
    print("👑 RANI MAKEOVER: ALTERNATE-DAY PUBLISHING SCHEDULE MATRIX")
    print("=" * 80)

    for slot in ["morning", "afternoon", "evening"]:
        plan = scheduler.get_publishing_plan(slot)
        print(f"⏰ Slot: {slot.upper():<10} | YouTube: {plan['youtube']:<12} | Insta/FB: {plan['instagram_and_facebook']}")

    print("=" * 80)
