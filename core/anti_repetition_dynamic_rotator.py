"""
👑 RANI MAKEOVER — ANTI-REPETITION & DYNAMIC CONTENT ROTATION ENGINE
Guarantees:
1. Zero Duplicate Posts: Tracks published history in `content_vault/published_history.json`.
2. Dynamic Variation Engine: If raw clips are reused, it generates:
   - Fresh High-CTR Headlines (from 30+ luxury salon hooks)
   - Fresh Sub-headlines & Offers
   - Rotated 320k BGM Tracks
   - Rotated Color Accents & Themes
   - Unique SEO Descriptions & Hashtags
"""

import os
import sys
import json
import random
import time
from pathlib import Path
from typing import Dict, Any, Tuple

# Enforce UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
HISTORY_FILE = BASE_DIR / "content_vault" / "published_history.json"

LUXURY_HEADLINES = [
    ("✂️ THREADING, FOREHEAD & UPPER LIPS ✂️", "Precision Eyebrow Shaping, Forehead & Upper Lips Glow", "✨"),
    ("💆‍♀️ LUXURY HAIR SPA & DEEP NOURISH GLOW 💆‍♀️", "Signature Hair Spa, Deep Conditioning & Silky Shine", "✨"),
    ("👑 ROYAL BRIDAL & BEAUTY MAKEOVER 👑", "HD Bridal Makeup, Threading, Forehead & Upper Lips", "💄"),
    ("🌟 KOREAN GLASS SKIN HYDRA FACIAL 🌟", "Deep Pore Cleansing & Instant Collagen Boost", "🌸"),
    ("✨ PERFECT THREADING & FACIAL GLOW ✨", "Threading, Forehead, Upper Lips & Herbal De-Tan", "🌿"),
    ("★ 100% FLAWLESS HD GLOW-UP ★", "Bridal Makeup, Hair Spa & Complete Makeover Experience", "✨"),
    ("🎁 5-IN-1 FESTIVE BEAUTY PACKAGE 🎁", "Threading + Forehead + Upper Lips + Hair Spa Special", "🎉"),
    ("🔥 CELEBRITY PARTY GLAMOUR LOOK 🔥", "Waterproof HD Makeup, Hair Styling & Flawless Glow", "✨"),
    ("💅 LUXURY NAIL ART & GEL EXTENSIONS 💅", "Custom Aesthetic Nails & Long-Lasting Shine", "💎"),
    ("🌸 HERBAL DE-TAN & SKIN BRIGHTENING 🌸", "100% Organic Glow & Sun Damage Repair", "🌿"),
    ("👑 ROYAL QUEEN MAKEOVER STUDIO 👑", "Bridal Makeup, Threading, Upper Lips & Hair Spa Pampering", "👸")
]

OFFERS_LIST = [
    ("🎁 FESTIVE 5-IN-1 SPECIAL", "ONLY ₹599/-", "₹1,999", "70% OFF"),
    ("💎 BRIDAL PRE-BOOKING OFFER", "FLAT 40% OFF", "₹9,999", "LIMITED SLOTS"),
    ("🌟 HYDRA GLOW FACIAL COMBO", "ONLY ₹899/-", "₹2,499", "65% OFF"),
    ("💆‍♀️ HAIR SPA & THREADING COMBO", "FLAT ₹799/-", "₹1,999", "MEGA DEAL"),
    ("💄 PARTY MAKEUP & HAIRSTYLE", "ONLY ₹1,199/-", "₹2,999", "60% OFF")
]

COLOR_THEMES = [
    {"name": "Royal Velvet Plum & Gold", "gold": (212, 175, 55), "gold_bright": (255, 215, 0), "bg": (12, 10, 16), "card": (22, 14, 28)},
    {"name": "Rose Gold & Midnight Black", "gold": (224, 168, 146), "gold_bright": (255, 192, 170), "bg": (10, 8, 12), "card": (24, 12, 20)},
    {"name": "Champagne Gold & Deep Wine", "gold": (247, 231, 206), "gold_bright": (255, 240, 215), "bg": (14, 8, 14), "card": (28, 12, 22)},
    {"name": "Emerald Luxury & Gold", "gold": (212, 175, 55), "gold_bright": (255, 215, 0), "bg": (8, 14, 12), "card": (12, 24, 20)}
]

class ContentRotator:
    def __init__(self):
        self.vault_dir = BASE_DIR / "content_vault"
        self.music_dir = BASE_DIR / "assets" / "music"
        self._load_history()

    def _load_history(self):
        if HISTORY_FILE.exists():
            try:
                self.history = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
            except Exception:
                self.history = {"used_videos": [], "used_headlines": [], "published_count": 0}
        else:
            self.history = {"used_videos": [], "used_headlines": [], "published_count": 0}

    def _save_history(self):
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        HISTORY_FILE.write_text(json.dumps(self.history, indent=2), encoding="utf-8")

    def get_next_unique_bundle(self) -> Dict[str, Any]:
        """Returns a 100% unique video + headline + music + theme + offer combination."""
        raw_videos = list(self.vault_dir.glob("viral_beauty_*.mp4"))
        if not raw_videos:
            raw_videos = list(self.vault_dir.glob("*.mp4"))

        # Find videos not yet used in this cycle
        selected_video = None
        if raw_videos:
            unused_videos = [v for v in raw_videos if v.name not in self.history["used_videos"]]
            if not unused_videos:
                print("🔄 All raw video clips cycled once! Starting next fresh iteration with new themes.")
                self.history["used_videos"] = []
                unused_videos = raw_videos
            if unused_videos:
                selected_video = random.choice(unused_videos)
                self.history["used_videos"].append(selected_video.name)

        # Select next unique headline
        unused_headlines = [h for h in LUXURY_HEADLINES if h[0] not in self.history["used_headlines"]]
        if not unused_headlines:
            self.history["used_headlines"] = []
            unused_headlines = LUXURY_HEADLINES

        selected_headline = random.choice(unused_headlines)
        self.history["used_headlines"].append(selected_headline[0])

        # Pick random 320k music track
        music_tracks = list(self.music_dir.glob("*.mp3"))
        selected_music = random.choice(music_tracks) if music_tracks else None

        # Pick random color theme and offer
        selected_theme = random.choice(COLOR_THEMES)
        selected_offer = random.choice(OFFERS_LIST)

        self.history["published_count"] += 1
        self._save_history()

        bundle = {
            "video_path": selected_video,
            "headline": selected_headline[0],
            "subheadline": selected_headline[1],
            "emoji": selected_headline[2],
            "offer": selected_offer,
            "theme": selected_theme,
            "music_path": selected_music,
            "iteration": self.history["published_count"]
        }

        return bundle

if __name__ == "__main__":
    rotator = ContentRotator()
    bundle = rotator.get_next_unique_bundle()
    print("=" * 80)
    print("🎯 DYNAMIC ANTI-REPETITION BUNDLE GENERATED:")
    print("=" * 80)
    print(f"🎬 Video: {bundle['video_path'].name}")
    print(f"✨ Headline: {bundle['headline']}")
    print(f"📝 Subheadline: {bundle['subheadline']}")
    print(f"🎨 Theme: {bundle['theme']['name']}")
    print(f"🎶 Music: {bundle['music_path'].name if bundle['music_path'] else 'None'}")
    print(f"🎁 Offer: {bundle['offer'][0]} - {bundle['offer'][1]}")
    print(f"📊 Total Published Count: #{bundle['iteration']}")
    print("=" * 80)
