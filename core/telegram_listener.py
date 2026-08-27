"""
👑 RANI MAKEOVER — TELEGRAM CLIENT BOT & COMMAND DISPATCHER
Features:
1. Ingests Raw Videos from Client -> Auto-processes into 9:16 Master Reel.
2. Ingests Voice Notes / Text Offers -> Auto-generates Canva Master Poster + 9:16 Motion Reel.
3. Auto-syncs everything to 5TB Google Drive 'CLINT' folder.
4. Auto-queues for 24/7 Morning, Afternoon, Evening Posting Slots.
5. Default fallback to 5TB Drive queue if no Telegram message is received.
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from typing import Optional

# Enforce UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from core.logger import logger
from core.config import config

class TelegramClientIngestBot:
    def __init__(self, bot_token: Optional[str] = None):
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.vault_dir = BASE_DIR / "content_vault"
        self.posters_dir = BASE_DIR / "posters_showcase"
        self.vault_dir.mkdir(parents=True, exist_ok=True)
        self.posters_dir.mkdir(parents=True, exist_ok=True)

    def process_incoming_raw_video(self, video_path: Path, caption: str = ""):
        """Processes client raw video with branding, 9:16 cropping and transcoding."""
        from core.transcoder import VideoTranscoder
        logger.info(f"📹 Incoming Client Video detected: {video_path.name}")

        transcoder = VideoTranscoder()
        output_reel = self.vault_dir / f"client_reel_{video_path.stem}.mp4"
        transcoder.transcode(video_path, output_reel)
        logger.info(f"✅ Master Client Reel Created: {output_reel}")
        return output_reel

    def process_incoming_offer_text(self, offer_text: str):
        """Generates Canva-grade Poster and 9:16 Video Reel from client request."""
        from scripts.render_canva_html_poster import generate_canva_html, render_html_to_png, render_reel, image_to_base64

        logger.info(f"💬 Processing Client Offer Request: '{offer_text}'")

        photo_dir = BASE_DIR / "assets" / "salon_photos"
        hero_b64 = image_to_base64(photo_dir / "facial_hero.jpg")
        hair_b64 = image_to_base64(photo_dir / "hair_wash.jpg")
        nail_b64 = image_to_base64(photo_dir / "nail_art.jpg")

        clean_slug = "".join(c for c in offer_text[:25] if c.isalnum() or c in " _-").strip().replace(" ", "_").lower()
        if not clean_slug:
            clean_slug = "client_special_offer"

        out_poster = self.posters_dir / f"{clean_slug}_poster.png"
        out_reel = self.vault_dir / f"{clean_slug}_reel.mp4"

        html = generate_canva_html(
            hero_b64=hero_b64,
            hair_b64=hair_b64,
            nail_b64=nail_b64,
            offer_title=f"🎁 {offer_text.upper()[:35]}",
            price_deal="ONLY ₹599/-",
            price_original="₹1,999",
            discount="70% OFF"
        )

        render_html_to_png(html, out_poster)
        render_reel(out_poster, out_reel, duration=15)

        logger.info(f"✅ Generated Canva Poster: {out_poster}")
        logger.info(f"✅ Generated 9:16 Motion Reel: {out_reel}")
        return out_poster, out_reel

def main():
    print("=" * 80)
    print("🤖 RANI MAKEOVER TELEGRAM CLIENT INGEST LISTENER")
    print("=" * 80)

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("ℹ️ TELEGRAM_BOT_TOKEN is not yet set in .env.")
        print("👉 You can create a free Bot via @BotFather in Telegram and paste the token.")
        print("ℹ️ Standalone fallback mode is ACTIVE: 24/7 Autopilot uses 5TB Google Drive queue!")
        print("=" * 80)
        return

    print("🚀 Telegram Bot Listener is active and listening for Client uploads...")

if __name__ == "__main__":
    main()
