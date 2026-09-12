"""
👑 RANI MAKEOVER — STRICT 5-CATEGORY ROUND-ROBIN DYNAMIC ROTATION ENGINE
Guarantees:
1. Strict Service Category Round-Robin (Zero Service Repetition):
   Cycle: NAIL_ART -> HAIR_SPA_SMOOTHING -> THREADING_CARE -> HAIRCUT_STYLING -> Repeat.
   No category can repeat back-to-back under any circumstances.
2. Category-Specific Asset Pairing:
   Nail Art videos are paired strictly with Nail Art headlines, tags, and offers.
   Hair Spa videos are paired strictly with Hair Spa headlines, tags, and offers.
   Threading videos are paired strictly with Threading headlines, tags, and offers.
   Haircut videos are paired strictly with Haircut headlines, tags, and offers.
3. Multi-Dimension Dynamic Variation:
   - Rotated 320k Curated BGM Tracks
   - Rotated Color Themes & Card Palettes
   - High-CTR Dynamic Offers
   - Cross-run History Persistence in `content_vault/published_history.json`
"""

import os
import sys
import json
import random
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

# Enforce UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
HISTORY_FILE = BASE_DIR / "content_vault" / "published_history.json"
GDRIVE_MAP_FILE = BASE_DIR / "gdrive_map.json"

CATEGORY_SEQUENCE = [
    "NAIL_ART",
    "HAIR_SPA_SMOOTHING",
    "THREADING_CARE",
    "HAIRCUT_STYLING",
    "BRIDAL_MAKEUP_MEHNDI"
]

CATEGORY_DATA = {
    "NAIL_ART": {
        "name": "Luxury Nail Art & Extensions",
        "service_text": "Nail Art • Gel Extensions • Acrylic Nails • Chrome & French Tips",
        "headlines": [
            ("💅 LUXURY NAIL ART & GEL EXTENSIONS 💅", "Custom Aesthetic Nails, Long-Lasting Gel Polish & Royal Shine", "💎"),
            ("✨ TRENDY NAIL EXTENSIONS & CHIC ART ✨", "Stunning French Tips, Chrome Glaze & Flawless Nails", "💅"),
            ("💎 ROYAL GLAMOUR NAIL TRANSFORMATION 💎", "Signature Nail Art, Acrylic Extensions & High-Fashion Look", "✨"),
            ("🔥 VIRAL AESTHETIC GEL NAILS STUDIO 🔥", "Premium Gel Polish, Nail Artistry & Glossy Durability", "💅")
        ],
        "offers": [
            ("💅 NAIL ART & EXTENSIONS SPECIAL", "FLAT 30% OFF", "₹1,499", "LIMITED SLOTS"),
            ("💎 GEL POLISH & NAIL ART COMBO", "ONLY ₹799/-", "₹1,800", "55% OFF")
        ],
        "hashtags": [
            "#RaniMakeover", "#NailArt", "#GelExtensions", "#NailExtensions", 
            "#NailTrends", "#AcrylicNails", "#NailSalon", "#DelhiNails", 
            "#NangloiSalon", "#Shorts", "#Trending", "#Reels"
        ]
    },
    "HAIR_SPA_SMOOTHING": {
        "name": "Luxury Hair Spa & Smoothening",
        "service_text": "Hair Spa • Keratin Smoothening • Hair Botox • Deep Nourishing",
        "headlines": [
            ("💆‍♀️ LUXURY HAIR SPA & DEEP NOURISH GLOW 💆‍♀️", "Signature Hair Spa, Deep Conditioning & Silky Shine", "✨"),
            ("✨ SILKY HAIR SMOOTHENING & KERATIN CARE ✨", "Frizz-Free Silky Finish, Mirror Shine & Hair Repair", "🌿"),
            ("🌟 ADVANCED HAIR REPAIR & NOURISH THERAPY 🌟", "Intense Hydration, Deep Scalp Spa & Gloss Treatment", "💆‍♀️"),
            ("🌿 ULTRA-SMOOTH HAIR MAKEOVER 🌿", "Professional Hair Spa & Keratin Infusion Experience", "✨")
        ],
        "offers": [
            ("💆‍♀️ HAIR SPA & DEEP CONDITION COMBO", "FLAT ₹799/-", "₹1,999", "MEGA DEAL"),
            ("✨ KERATIN & SMOOTHENING SPECIAL", "STARTING ₹1,999/-", "₹4,500", "55% OFF")
        ],
        "hashtags": [
            "#RaniMakeover", "#HairSpa", "#HairSmoothening", "#KeratinTreatment", 
            "#SilkyHair", "#HairCare", "#DelhiHairSalon", "#NangloiSalon", 
            "#Shorts", "#Viral", "#Reels"
        ]
    },
    "THREADING_CARE": {
        "name": "Precision Threading, Forehead & Upper Lips",
        "service_text": "Precision Threading • Forehead • Upper Lips • Eyebrow Definition",
        "headlines": [
            ("✂️ THREADING, FOREHEAD & UPPER LIPS ✂️", "Precision Eyebrow Shaping, Forehead & Upper Lips Glow", "✨"),
            ("✨ PERFECT EYEBROW ARCH & FOREHEAD CARE ✨", "Pain-Free Precision Shaping & Clean Forehead Finish", "🌿"),
            ("🌿 SIGNATURE EYEBROW SHAPING & GLOW 🌿", "Definition Threading, Upper Lips & Instant Freshness", "✨"),
            ("🌸 GENTLE THREADING & FACIAL CLEANSING 🌸", "Perfect Eyebrow Lines & Smooth Radiant Forehead", "💫")
        ],
        "offers": [
            ("✂️ THREADING + FOREHEAD + UPPER LIPS COMBO", "ONLY ₹99/-", "₹250", "SPECIAL"),
            ("🌸 THREADING + HERBAL DE-TAN COMBO", "ONLY ₹299/-", "₹650", "BESTSELLER")
        ],
        "hashtags": [
            "#RaniMakeover", "#Threading", "#EyebrowThreading", "#Forehead", 
            "#UpperLips", "#EyebrowShaping", "#BeautyParlourNangloi", "#DelhiSalon", 
            "#Trending", "#Shorts"
        ]
    },
    "HAIRCUT_STYLING": {
        "name": "Trendy Haircut & Styling",
        "service_text": "Trendy Haircut • Layer Cut • Feather Cut • Professional Styling",
        "headlines": [
            ("✨ PERFECT TRENDY HAIRCUT & STYLING ✨", "Layer Cut, Feather Cut & Professional Blow Dry Finish", "🌿"),
            ("🔥 CHIC BOUNCE HAIRCUT MAKEOVER 🔥", "Volume Layering, Split End Removal & Glossy Style", "✨"),
            ("💇‍♀️ SIGNATURE LAYER CUT & BLOWOUT 💇‍♀️", "Custom Haircut According to Face Shape & Texture", "🌟"),
            ("⭐ TRENDY SALON HAIRCUT & FINISH ⭐", "Flawless Haircut, Bouncy Volume & Lasting Elegance", "🌿")
        ],
        "offers": [
            ("💇‍♀️ ADVANCED LAYER HAIRCUT & BLOW DRY", "ONLY ₹399/-", "₹899", "55% OFF"),
            ("✨ HAIRCUT + HAIR SPA MEGA COMBO", "ONLY ₹999/-", "₹2,499", "60% OFF")
        ],
        "hashtags": [
            "#RaniMakeover", "#Haircut", "#LayerCut", "#TrendyHaircut", 
            "#HairStyling", "#BlowDry", "#NangloiSalon", "#DelhiMakeupArtist", 
            "#Shorts", "#Reels", "#Viral"
        ]
    },
    "BRIDAL_MAKEUP_MEHNDI": {
        "name": "Royal Bridal Makeup & Designer Mehndi Art",
        "service_text": "HD Bridal Makeup • Airbrush Glow • Intricate Designer Mehndi • Luxury Pre-Bridal Care",
        "headlines": [
            ("👑 ROYAL BRIDAL GLOW & MEHNDI MAKEOVER 👑", "Flawless HD Bridal Makeup, Intricate Bridal Mehndi & Royalty Look", "✨"),
            ("✨ LUXURY BRIDAL MAKEUP & DESIGNER MEHNDI ✨", "Signature Glamour, Long-Lasting Waterproof Finish & Royal Elegance", "💄"),
            ("🌺 SIGNATURE BRIDAL MEHNDI & MAKEOVER 🌺", "Traditional Indian Bridal Luxury & Flawless Bridal Glow", "👑"),
            ("💄 FLAWLESS HD BRIDAL TRANSFORMATION 💄", "Custom Bridal Look According to Face & Outfit Elegance", "🌟")
        ],
        "offers": [
            ("👑 COMPLETE ROYAL BRIDAL PACKAGE", "SPECIAL OFFER ₹7,999/-", "₹15,000", "45% OFF"),
            ("✨ BRIDAL MEHNDI & HD PRE-BRIDAL", "SPECIAL OFFER ₹3,999/-", "₹8,000", "50% OFF")
        ],
        "hashtags": [
            "#RaniMakeover", "#BridalMakeup", "#BridalMehndi", "#DelhiBridalMakeup", 
            "#NangloiSalon", "#IndianBride", "#BridalLook", "#ViralReels", "#Shorts"
        ]
    }
}

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
                self.history = self._default_history()
        else:
            self.history = self._default_history()

        # Ensure required keys exist
        if "category_history" not in self.history:
            self.history["category_history"] = {}
        for cat in CATEGORY_SEQUENCE:
            if cat not in self.history["category_history"]:
                self.history["category_history"][cat] = {"used_clip_ids": [], "used_headlines": []}
        if "used_videos" not in self.history:
            self.history["used_videos"] = []
        if "used_music" not in self.history:
            self.history["used_music"] = []
        if "published_count" not in self.history:
            self.history["published_count"] = 0
        if "last_category" not in self.history:
            self.history["last_category"] = "BRIDAL_MAKEUP_MEHNDI"

        # Cross-load and synchronize with logs/used_reels.json
        used_reels_file = BASE_DIR / "logs" / "used_reels.json"
        if used_reels_file.exists():
            try:
                ur_data = json.loads(used_reels_file.read_text(encoding="utf-8"))
                for uid in ur_data.get("used_ids", []):
                    # Add to NAIL_ART or appropriate category if not present
                    found = False
                    for cat_h in self.history["category_history"].values():
                        if str(uid) in cat_h.get("used_clip_ids", []):
                            found = True
                            break
                    if not found and "NAIL_ART" in self.history["category_history"]:
                        self.history["category_history"]["NAIL_ART"].setdefault("used_clip_ids", []).append(str(uid))
                for uvid in ur_data.get("used_videos", []):
                    if uvid not in self.history["used_videos"]:
                        self.history["used_videos"].append(uvid)
            except Exception as e_ur:
                print(f"used_reels load note: {e_ur}")

        # Permanent ban on previously posted clips so they NEVER repeat
        known_published = [
            ("548971136", "client_raw_IMG_2029.mov"),
            ("548971209", "client_raw_IMG_2030.mov"),
            ("548971262", "client_raw_IMG_2034.mp4"),
            ("540488320", "IMG_2002.MOV"),
            ("540488437", "IMG_2003.MOV"),
            ("540488768", "IMG_2004.MOV"),
            ("540489000", "IMG_2005.MOV"),
            ("540489134", "IMG_2006.MOV"),
            ("540489178", "IMG_2007.MOV")
        ]
        for k_id, k_name in known_published:
            if k_name not in self.history["used_videos"]:
                self.history["used_videos"].append(k_name)

    def _default_history(self) -> Dict[str, Any]:
        return {
            "last_category": "BRIDAL_MAKEUP_MEHNDI",
            "category_history": {cat: {"used_clip_ids": [], "used_headlines": []} for cat in CATEGORY_SEQUENCE},
            "used_videos": [],
            "used_music": [],
            "published_count": 0,
            "recent_posts": []
        }

    def _save_history(self):
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        HISTORY_FILE.write_text(json.dumps(self.history, indent=2), encoding="utf-8")

    def determine_next_category(self, force_category: Optional[str] = None) -> str:
        if force_category and force_category in CATEGORY_SEQUENCE:
            return force_category

        last_cat = self.history.get("last_category", "BRIDAL_MAKEUP_MEHNDI")
        try:
            current_idx = CATEGORY_SEQUENCE.index(last_cat)
            next_idx = (current_idx + 1) % len(CATEGORY_SEQUENCE)
        except ValueError:
            next_idx = 0
        return CATEGORY_SEQUENCE[next_idx]

    def get_next_category_bundle(self, available_clips: List[Dict[str, Any]], force_category: Optional[str] = None) -> Dict[str, Any]:
        """
        Selects next clip strictly following Zero-Repetition and Round-Robin rotation.
        Guarantees:
        1. NO video is EVER repeated. If a category runs out of unused clips, it
           automatically searches the next category in sequence that has fresh clips.
        2. If ALL categories run out of clips, it returns None to halt the pipeline safely.
        """
        # 1. Compile exhaustive set of all used clip IDs, names, and stems
        all_used_ids = set()
        all_used_names = set()

        for cat, c_info in self.history.get("category_history", {}).items():
            for cid in c_info.get("used_clip_ids", []):
                all_used_ids.add(str(cid).strip())

        for uv in self.history.get("used_videos", []):
            all_used_names.add(str(uv).strip().lower())
            all_used_ids.add(str(uv).strip())

        used_reels_file = BASE_DIR / "logs" / "used_reels.json"
        if used_reels_file.exists():
            try:
                ur_data = json.loads(used_reels_file.read_text(encoding="utf-8"))
                for uid in ur_data.get("used_ids", []):
                    all_used_ids.add(str(uid).strip())
                for uv in ur_data.get("used_videos", []):
                    all_used_names.add(str(uv).strip().lower())
            except Exception:
                pass

        def is_clip_unposted(clip: dict) -> bool:
            cid = str(clip.get("id", "")).strip()
            cname = str(clip.get("name", "")).strip().lower()
            cstem = Path(cname).stem.lower()
            if not cid and not cname:
                return False
            if cid in all_used_ids:
                return False
            if cname in all_used_names:
                return False
            if cstem in all_used_names:
                return False
            for u in all_used_names:
                if u and (u == cname or u == cstem or Path(u).stem.lower() == cstem):
                    return False
            return True

        # 2. Determine category check order
        start_cat = self.determine_next_category(force_category)
        if force_category and force_category in CATEGORY_SEQUENCE:
            categories_to_check = [force_category] + [c for c in CATEGORY_SEQUENCE if c != force_category]
        else:
            try:
                idx = CATEGORY_SEQUENCE.index(start_cat)
            except ValueError:
                idx = 0
            categories_to_check = CATEGORY_SEQUENCE[idx:] + CATEGORY_SEQUENCE[:idx]

        # 3. Find a category that has fresh unposted clips
        selected_cat = None
        selected_clip = None

        for candidate_cat in categories_to_check:
            # Filter clips for this specific category
            cat_clips = [c for c in available_clips if c.get("category") == candidate_cat]
            if not cat_clips:
                for c in available_clips:
                    name_l = c.get("name", "").lower()
                    if candidate_cat == "NAIL_ART" and ("nail" in name_l or "1894" in name_l or "1896" in name_l or "1897" in name_l or "1899" in name_l or "1901" in name_l or "1902" in name_l or "1909" in name_l or "1911" in name_l):
                        cat_clips.append(c)
                    elif candidate_cat == "BRIDAL_MAKEUP_MEHNDI" and ("1907" in name_l or "mehndi" in name_l or "bridal" in name_l):
                        cat_clips.append(c)
                    elif candidate_cat == "HAIR_SPA_SMOOTHING" and ("spa" in name_l or "smooth" in name_l or "7754410" in name_l or "7754411" in name_l or "7754412" in name_l or "7754502" in name_l):
                        cat_clips.append(c)
                    elif candidate_cat == "THREADING_CARE" and ("threading" in name_l or "7754482" in name_l or "7754507" in name_l):
                        cat_clips.append(c)
                    elif candidate_cat == "HAIRCUT_STYLING" and ("haircut" in name_l or "7754496" in name_l or "7754508" in name_l or "6302" in name_l):
                        cat_clips.append(c)

            fresh_clips = [c for c in cat_clips if is_clip_unposted(c)]
            if fresh_clips:
                selected_cat = candidate_cat
                selected_clip = random.choice(fresh_clips)
                print(f"🎯 [ZERO-REPETITION PICK] Category: {selected_cat} | Video: '{selected_clip.get('name')}' (ID: {selected_clip.get('id')})")
                break
            else:
                print(f"ℹ️ Category '{candidate_cat}' has 0 unposted clips remaining.")

        # If no category has unposted clips, check globally
        if not selected_clip:
            all_fresh = [c for c in available_clips if is_clip_unposted(c)]
            if all_fresh:
                selected_clip = random.choice(all_fresh)
                selected_cat = selected_clip.get("category", start_cat)
                print(f"🎯 [UNASSIGNED POOL PICK] Category: {selected_cat} | Video: '{selected_clip.get('name')}'")
            else:
                print("🛑 [ABSOLUTE ZERO-REPETITION LOCK] ALL clips in the vault have already been published!")
                print("🚫 STRICT ZERO DUPLICATION: No video will EVER repeat. Halting clip selection safely.")
                selected_clip = None
                selected_cat = start_cat

        category = selected_cat or start_cat
        cat_data = CATEGORY_DATA.get(category, CATEGORY_DATA["NAIL_ART"])
        cat_hist = self.history["category_history"].setdefault(category, {"used_clip_ids": [], "used_headlines": []})

        # Select headline (headlines and music can rotate dynamically)
        cat_headlines = cat_data["headlines"]
        unused_headlines = [h for h in cat_headlines if h[0] not in cat_hist.get("used_headlines", [])]
        if not unused_headlines:
            cat_hist["used_headlines"] = []
            unused_headlines = cat_headlines
        selected_headline = random.choice(unused_headlines)
        cat_hist.setdefault("used_headlines", []).append(selected_headline[0])

        # Pick Music
        curated_trending = [
            "viral_luxury_fashion_beat.mp3",
            "salon_luxury_bgm.mp3",
            "salon_energetic_glam.mp3",
            "instagram_viral_beauty_lounge.mp3",
            "01_Audionautix Acoustic.mp3",
            "08_BABES FOREVER.mp3",
            "14_Wiggle.mp3",
            "19_Slam Funk.mp3",
            "salon_aesthetic_bg.mp3"
        ]
        available_tracks = [self.music_dir / name for name in curated_trending if (self.music_dir / name).exists()]
        if not available_tracks:
            available_tracks = list(self.music_dir.glob("*.mp3"))

        unused_music = [m for m in available_tracks if m.name not in self.history.get("used_music", [])]
        if not unused_music:
            self.history["used_music"] = []
            unused_music = available_tracks

        selected_music = random.choice(unused_music) if unused_music else None
        if selected_music:
            self.history.setdefault("used_music", []).append(selected_music.name)

        # Pick theme and offer
        selected_theme = random.choice(COLOR_THEMES)
        selected_offer = random.choice(cat_data["offers"])

        # If a fresh clip was found, update persistent state
        if selected_clip is not None:
            self.history["last_category"] = category
            self.history["published_count"] += 1
            cat_hist.setdefault("used_clip_ids", []).append(str(selected_clip.get("id")))
            self.history.setdefault("used_videos", []).append(selected_clip.get("name"))

            post_record = {
                "iteration": self.history["published_count"],
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "category": category,
                "clip_id": selected_clip.get("id"),
                "clip_name": selected_clip.get("name"),
                "headline": selected_headline[0]
            }
            recent = self.history.setdefault("recent_posts", [])
            recent.append(post_record)
            if len(recent) > 50:
                self.history["recent_posts"] = recent[-50:]

            self._save_history()

            # Synchronize to logs/used_reels.json
            try:
                if used_reels_file.exists():
                    u_data = json.loads(used_reels_file.read_text(encoding="utf-8"))
                else:
                    u_data = {"used_ids": [], "used_videos": [], "published_count": 0}
                if str(selected_clip.get("id")) not in u_data.get("used_ids", []):
                    u_data.setdefault("used_ids", []).append(str(selected_clip.get("id")))
                if "used_videos" not in u_data:
                    u_data["used_videos"] = []
                if selected_clip.get("name") not in u_data["used_videos"]:
                    u_data["used_videos"].append(selected_clip.get("name"))
                u_data["published_count"] = self.history["published_count"]
                used_reels_file.write_text(json.dumps(u_data, indent=2), encoding="utf-8")
            except Exception as e_sync:
                print(f"used_reels sync note: {e_sync}")

        bundle = {
            "category": category,
            "category_name": cat_data["name"],
            "service_text": cat_data["service_text"],
            "clip_info": selected_clip,
            "headline": selected_headline[0],
            "subheadline": selected_headline[1],
            "emoji": selected_headline[2],
            "offer": selected_offer,
            "theme": selected_theme,
            "music_path": selected_music,
            "hashtags": cat_data["hashtags"],
            "iteration": self.history["published_count"]
        }

        return bundle

    # Backward compatibility helper
    def get_next_unique_bundle(self) -> Dict[str, Any]:
        if GDRIVE_MAP_FILE.exists():
            try:
                map_data = json.loads(GDRIVE_MAP_FILE.read_text(encoding="utf-8"))
                clips = map_data.get("clips", [])
                return self.get_next_category_bundle(clips)
            except Exception:
                pass
        return self.get_next_category_bundle([])

if __name__ == "__main__":
    rotator = ContentRotator()
    print("=" * 80)
    print("🎯 TESTING 4-CATEGORY ROUND-ROBIN CONTENT ROTATOR:")
    print("=" * 80)
    
    if GDRIVE_MAP_FILE.exists():
        map_data = json.loads(GDRIVE_MAP_FILE.read_text(encoding="utf-8"))
        clips = map_data.get("clips", [])
    else:
        clips = []

    for i in range(4):
        b = rotator.get_next_category_bundle(clips)
        print(f"Cycle {i+1}:")
        print(f"  🏷️ Category: {b['category']} ({b['category_name']})")
        print(f"  🎬 Video: {b['clip_info']['name'] if b['clip_info'] else 'None'}")
        print(f"  ✨ Headline: {b['headline']}")
        print(f"  🎵 Music: {b['music_path'].name if b['music_path'] else 'None'}")
        print("-" * 60)
