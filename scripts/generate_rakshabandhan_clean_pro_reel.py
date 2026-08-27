"""
Clean Raksha Bandhan Master Agency Poster & Reel (Zero Photo Obstruction).
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

from core.agency_master_designer import ProAgencyDesigner

def main():
    print("=" * 80)
    print("👑 RAKSHA BANDHAN CLEAN PRO AGENCY MASTER POSTER & REEL")
    print("=" * 80)

    designer = ProAgencyDesigner()
    out_poster = BASE_DIR / "posters_showcase" / "raksha_bandhan_clean_pro_poster.png"
    out_reel = BASE_DIR / "content_vault" / "raksha_bandhan_clean_pro_reel.mp4"

    print("🎨 Rendering 100% Clean Hero Photo Layout with Real Vector Icons...")
    designer.create_agency_master_poster(
        brand_line_1="Beauty",
        brand_line_2="Salon",
        tagline="Beauty is being comfortable in your own skin. Pamper it well",
        offer_highlight="🎁 RAKSHA BANDHAN SPECIAL • 5-IN-1 COMBO ₹599",
        services=[
            "Radiance Glow Facial",
            "Professional Eyebrows",
            "Forehead Threading",
            "Upper Lips Care",
            "Full Arms Glow Waxing"
        ],
        phone="+91 9334668807",
        instagram="@Lovelyrani53",
        address_line_1="Shop G-38, RC Plaza,",
        address_line_2="Kirari Chowk, Nangloi,",
        address_line_3="Delhi - 110086",
        output_png=out_poster
    )
    print(f"✅ Clean Poster Generated: {out_poster}")

    print("🎬 Rendering 9:16 Full HD Motion Reel...")
    designer.render_reel(out_poster, out_reel, duration=15)
    print(f"✅ Video Reel Generated: {out_reel}")

    print("\n" + "=" * 80)
    print("🎉 CLEAN PRO AGENCY POSTER & REEL SUCCESSFULLY READY!")
    print("=" * 80)

if __name__ == "__main__":
    main()
