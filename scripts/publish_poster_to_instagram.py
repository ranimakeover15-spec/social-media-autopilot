"""
Publish Master Creative Poster directly to Instagram Feed & Story (@Lovelyrani53).
"""

import sys
from pathlib import Path
from instagrapi import Client

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
SESSION_FILE = BASE_DIR / "instagram_session.json"
POSTER_PATH = BASE_DIR / "posters_showcase" / "RANI_MAKEOVER_MASTER_CREATIVE_DEMO.png"

def main():
    print("=" * 80)
    print("🚀 PUBLISHING MASTER POSTER LIVE TO INSTAGRAM (@Lovelyrani53)")
    print("=" * 80)

    if not SESSION_FILE.exists():
        print("❌ instagram_session.json not found!")
        return

    cl = Client()
    cl.load_settings(SESSION_FILE)

    caption = (
        "👑 5-IN-1 FESTIVE BEAUTY SPECIAL • ONLY ₹599/- 👑\n\n"
        "✨ Complete Luxury Salon Transformation:\n"
        "1️⃣ Radiance Glow Facial\n"
        "2️⃣ Professional Eyebrows Threading\n"
        "3️⃣ Forehead Threading\n"
        "4️⃣ Upper Lips Care\n"
        "5️⃣ Full Arms Glow Waxing\n\n"
        "🔥 Huge 70% Discount (Original Price ₹1,999 ➔ Now ₹599)\n"
        "📞 Call / WhatsApp for Bookings: +91 9334668807\n"
        "📍 Address: Shop No. G-38, RC Plaza, Kirari Chowk, Nangloi, Delhi - 110086\n"
        "▶ YouTube: Rani makeover\n\n"
        "#RaniMakeover #BeautyParlour #DelhiSalon #FestiveOffer #HydraFacial #SalonOffer #Nangloi #SkinCare #MakeupStudio #DelhiBeautyParlour"
    )

    # 1. Upload Photo to Instagram Feed
    print(f"📸 [1/2] Publishing Photo to Instagram Feed...")
    media = cl.photo_upload(
        path=str(POSTER_PATH),
        caption=caption,
        extra_data={"share_to_fb": "1", "share_to_facebook": "1"}
    )
    post_url = f"https://www.instagram.com/p/{media.code}/"
    print(f"🎉 Instagram Post Live: {post_url}")

    # 2. Upload Photo to Instagram Story
    print(f"📱 [2/2] Publishing Photo to Instagram Story...")
    try:
        story = cl.photo_upload_to_story(
            path=str(POSTER_PATH)
        )
        print(f"🎉 Instagram Story is Live! (Story ID: {story.id})")
    except Exception as e:
        print(f"Story upload error: {e}")

    print("\n" + "=" * 80)
    print("🎉 MASTER POSTER LIVE ON INSTAGRAM FEED & STORY!")
    print(f"🔗 View Post: {post_url}")
    print("=" * 80)

if __name__ == "__main__":
    main()
