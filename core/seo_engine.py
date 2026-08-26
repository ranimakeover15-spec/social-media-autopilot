"""
Algorithmic SEO Engine for multi-platform viral short-form video optimization.
Generates high-CTR English titles with emojis, 15+ relevant search hashtags,
and platform-tailored descriptions for YouTube Shorts, Instagram Reels, and Facebook Reels.
"""

import re
import random
from typing import Dict, List, Any
from core.config import config
from core.logger import logger

class SEOEngine:
    # High-CTR Viral Hook Templates
    HOOK_TEMPLATES = [
        "This Will Change How You Think Forever 🧠⚡",
        "Stop Scrolling If You Want Real Growth 📈🚀",
        "The 1% Rule Nobody Talks About 🤫💡",
        "Never Make This Critical Mistake ⚠️🛑",
        "How Winners Actually Win Every Day 🏆🔥",
        "The Brutal Truth You Need To Hear Today 💥🎯",
        "Master This Mindset Shift Right Now ⏳✨",
        "What 99% Of People Learn Too Late in Life 🗝️📖",
        "Unleash Your True Potential Today 💪💥",
        "Your Daily Dose of Unstoppable Focus 🚀⚡",
        "Secret Habit of Highly Successful People 🌟🔑",
        "Turn Pain Into Power: Watch Till The End ⏳🔥",
        "Don't Give Up! Your Time Is Coming 🌅💫",
        "The Best Advice You'll Hear All Week 💯👂",
        "Discipline Over Motivation Every Single Day ⚔️🛡️"
    ]

    # Slot-Specific Framing
    SLOT_FRAMES = {
        "Morning": ["Morning Kickstart ☀️", "Start Your Day Strong 💪", "Early Grind Focus 🌅"],
        "Afternoon": ["Midday Power Boost ⚡", "Afternoon Energy Reset 🔋", "Stay Focused Midday 🎯"],
        "Evening": ["Evening Reflection 🌙", "End Your Day Like A Champion 🏆", "Night Mindset Fuel 🌌"]
    }

    # 15+ Algorithmic Hashtag Pools per Niche
    NICHE_TAGS = {
        "motivation": [
            "#motivation", "#motivationalquotes", "#mindset", "#success", "#discipline",
            "#grind", "#inspiration", "#focus", "#selfimprovement", "#growth",
            "#positivevibes", "#dailygrind", "#nevergiveup", "#ambition", "#hustle",
            "#goals", "#winner", "#mindsetmatters", "#successmindset", "#consistency"
        ],
        "tech": [
            "#tech", "#technology", "#ai", "#innovation", "#future",
            "#coding", "#programming", "#developer", "#artificialintelligence", "#software",
            "#gadgets", "#techtrends", "#productivity", "#technews", "#engineering",
            "#automation", "#cloud", "#cybersecurity", "#techlife", "#futuretech"
        ],
        "finance": [
            "#finance", "#money", "#investing", "#wealth", "#financialfreedom",
            "#stockmarket", "#crypto", "#passiveincome", "#business", "#entrepreneur",
            "#moneytips", "#savingmoney", "#investment", "#realestate", "#cashflow",
            "#personalfinance", "#millionairemindset", "#smartmoney", "#trading", "#sidehustle"
        ],
        "fitness": [
            "#fitness", "#workout", "#gym", "#fitnessmotivation", "#bodybuilding",
            "#health", "#training", "#fitfam", "#gymmotivation", "#cardio",
            "#gains", "#fitlife", "#nutrition", "#weightloss", "#strength",
            "#exercise", "#lifestyle", "#muscle", "#healthyhabits", "#consistency"
        ]
    }

    # Universal Discovery Tags
    UNIVERSAL_SHORT_TAGS = [
        "#viral", "#trending", "#foryou", "#shorts", "#reels", "#fyp", "#explore"
    ]

    @classmethod
    def clean_filename(cls, filename: str) -> str:
        """Extracts human-readable words from file stems."""
        clean = re.sub(r"[_\-\d\.]+", " ", filename).strip()
        words = [w.capitalize() for w in clean.split() if len(w) > 1 and w.lower() not in ["transcoded", "video", "output", "clip", "reel"]]
        if words:
            return " ".join(words)
        return ""

    @classmethod
    def generate_metadata(
        cls,
        filename: str,
        slot_name: str = "Morning",
        niche: str = None
    ) -> Dict[str, Any]:
        """
        Generates unified SEO package customized for each social platform.
        """
        selected_niche = (niche or config.niche_category).lower()
        tag_pool = cls.NICHE_TAGS.get(selected_niche, cls.NICHE_TAGS["motivation"])
        
        # Select 15-18 distinct tags
        chosen_tags = list(dict.fromkeys(random.sample(tag_pool, min(14, len(tag_pool))) + cls.UNIVERSAL_SHORT_TAGS))
        
        # Build Title
        file_hint = cls.clean_filename(filename)
        hook = random.choice(cls.HOOK_TEMPLATES)
        slot_options = cls.SLOT_FRAMES.get(slot_name, cls.SLOT_FRAMES["Morning"])
        slot_tag = random.choice(slot_options)

        if file_hint and len(file_hint) > 3:
            base_title = f"{file_hint} - {hook}"
        else:
            base_title = f"{slot_tag} | {hook}"

        # Ensure title fits YouTube Shorts limit (100 chars)
        if len(base_title) > 85:
            base_title = base_title[:82] + "..."

        yt_title = f"{base_title} #Shorts"
        ig_title = base_title
        fb_title = base_title

        # Hashtag strings
        hashtags_str = " ".join(chosen_tags)
        clean_raw_tags = [t.replace("#", "") for t in chosen_tags]

        # 1. YouTube Description
        yt_description = (
            f"{base_title}\n\n"
            f"⚡ {config.call_to_action}\n\n"
            f"🔔 Subscribe to {config.brand_name} for daily high-impact Shorts!\n\n"
            f"🎯 Focus on discipline, daily consistency, and relentless growth.\n\n"
            f"#Shorts #YouTubeShorts {hashtags_str}"
        )

        # 2. Instagram Caption
        ig_caption = (
            f"{base_title}\n\n"
            f"{config.call_to_action}\n"
            f"Save this for later & share with someone who needs this today! 📌💬\n\n"
            f"----\n"
            f"{hashtags_str}"
        )

        # 3. Facebook Reels Description
        fb_description = (
            f"{base_title}\n\n"
            f"👉 Drop a '100%' in the comments if you agree! 🔥\n"
            f"{config.call_to_action}\n\n"
            f"{hashtags_str}"
        )

        metadata = {
            "title": base_title,
            "slot": slot_name,
            "niche": selected_niche,
            "tags": clean_raw_tags,
            "hashtags_string": hashtags_str,
            "youtube": {
                "title": yt_title,
                "description": yt_description,
                "tags": clean_raw_tags[:20],
                "category_id": config.youtube_category_id,
                "privacy_status": config.youtube_privacy_status
            },
            "instagram": {
                "caption": ig_caption
            },
            "facebook": {
                "description": fb_description
            }
        }

        logger.info(f"✨ SEO Metadata Generated: '{yt_title}' ({len(chosen_tags)} tags)")
        return metadata
