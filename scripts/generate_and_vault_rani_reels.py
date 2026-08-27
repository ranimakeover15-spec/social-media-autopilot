"""
Generate Master Agency Reels for Rani Makeover and store them in content_vault.
"""

import sys
from pathlib import Path

# Enforce UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from core.logger import logger
from core.video_creator import RaniMakeoverVideoCreator

def main():
    print("=" * 80)
    print("👑 RANI MAKEOVER — 10/10 MASTER AGENCY REEL GENERATOR")
    print("=" * 80)

    creator = RaniMakeoverVideoCreator()
    vault_dir = BASE_DIR / "content_vault"
    vault_dir.mkdir(parents=True, exist_ok=True)

    temp_poster = BASE_DIR / "temp" / "rani_makeover_poster.png"
    output_video = vault_dir / "rani_makeover_festive_offer_599.mp4"

    # 1. Render High-Resolution Poster
    logger.info("🎨 Rendering 1080x1920 Luxury Agency Poster...")
    creator.render_poster_image(output_image_path=temp_poster)
    logger.info(f"✅ Poster Generated: {temp_poster}")

    # 2. Check for optional music file
    music_candidates = [
        Path(r"D:\CLINT\RANI_MAKEOVER\assets\music\viral_luxury_fashion_beat.mp3"),
        BASE_DIR / "assets" / "music" / "viral_luxury_fashion_beat.mp3"
    ]
    music_file = next((m for m in music_candidates if m.exists()), None)

    # 3. Render 1080x1920 9:16 Video Reel with Ken Burns Zoom motion
    logger.info("🎬 Rendering Full HD 9:16 Reel with Ken Burns Motion Effect...")
    creator.render_reel_video(
        poster_path=temp_poster,
        output_video_path=output_video,
        music_path=music_file,
        duration=20
    )

    size_mb = output_video.stat().st_size / (1024 * 1024)
    logger.info(f"🎉 MASTER REEL SUCCESSFULLY CREATED AND SAVED TO VAULT!")
    logger.info(f"📁 Video Location: {output_video} ({size_mb:.2f} MB)")
    print("\n" + "=" * 80)
    print("🚀 Video is ready in 'content_vault' and will be auto-uploaded by the 24/7 Pipeline!")
    print("=" * 80)

if __name__ == "__main__":
    main()
