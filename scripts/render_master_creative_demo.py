"""
👑 RANI MAKEOVER — CANVA-GRADE LUXURY SALON CREATIVE POSTER DEMO
Uses Headless Chrome HTML/CSS to render 1080x1920 Pixel-Perfect Creative with:
- Official RM Monogram Logo
- Real Vector SVG Icons
- S-Curve Gold & Velvet Plum Layout
- Model Hero Photo + 2 Circular Service Insets
- 5-Star Service Cards with Gold Badges
"""

import os
import sys
import shutil
import base64
import subprocess
from pathlib import Path

# Enforce UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

def find_chrome() -> str:
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        "/usr/bin/chromium",
        "/usr/bin/google-chrome",
        shutil.which("chrome")
    ]
    for c in candidates:
        if c and Path(c).exists():
            return str(c)
    return "chrome"

def img_b64(path: Path) -> str:
    if not path.exists():
        return ""
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('utf-8')}"

def render_creative():
    print("=" * 80)
    print("🎨 RENDERING MASTER LUXURY SALON CREATIVE POSTER (1080x1920)")
    print("=" * 80)

    photo_dir = BASE_DIR / "assets" / "salon_photos"
    hero_b64 = img_b64(photo_dir / "facial_hero.jpg")
    hair_b64 = img_b64(photo_dir / "hair_wash.jpg")
    nail_b64 = img_b64(photo_dir / "nail_art.jpg")
    logo_b64 = img_b64(photo_dir / "official_rm_logo.png")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&family=Playfair+Display:ital,wght@0,600;0,700;0,900;1,600;1,700&family=Poppins:wght@400;500;600;700&display=swap');

    * {{ margin: 0; padding: 0; box-sizing: border-box; }}

    body {{
        width: 1080px;
        height: 1920px;
        background-color: #0d010b;
        color: #ffffff;
        font-family: 'Poppins', sans-serif;
        overflow: hidden;
        position: relative;
    }}

    /* HERO PHOTO & CURVES */
    .hero-box {{
        position: relative;
        width: 1080px;
        height: 820px;
        overflow: hidden;
    }}

    .hero-img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center 20%;
    }}

    .top-bar {{
        position: absolute;
        top: 0;
        left: 0;
        width: 1080px;
        height: 120px;
        background: linear-gradient(135deg, #e6007a 0%, #a0004e 100%);
        clip-path: polygon(0 0, 100% 0, 100% 65px, 60% 45px, 25% 90px, 0 35px);
        z-index: 2;
    }}

    .mid-wave-1 {{
        position: absolute;
        bottom: 0;
        left: 0;
        width: 1080px;
        height: 240px;
        background: linear-gradient(135deg, #e6007a 0%, #850040 100%);
        clip-path: polygon(0 90px, 35% 60px, 70% 120px, 100% 20px, 100% 100%, 0 100%);
        z-index: 2;
    }}

    .mid-wave-2 {{
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 1080px;
        height: 170px;
        background: #0d010b;
        clip-path: polygon(0 75px, 40% 50px, 75% 100px, 100% 30px, 100% 100%, 0 100%);
        z-index: 3;
    }}

    /* CIRCULAR INSET PHOTOS WITH GOLD BORDERS */
    .circle-1 {{
        position: absolute;
        top: 560px;
        left: 45px;
        width: 440px;
        height: 440px;
        border-radius: 50%;
        border: 8px solid #ffffff;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.7);
        overflow: hidden;
        z-index: 10;
        background: #1a0316;
    }}
    .circle-1 img {{ width: 100%; height: 100%; object-fit: cover; }}

    .circle-2 {{
        position: absolute;
        top: 480px;
        left: 320px;
        width: 320px;
        height: 320px;
        border-radius: 50%;
        border: 8px solid #ffd700;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.7);
        overflow: hidden;
        z-index: 12;
        background: #1a0316;
    }}
    .circle-2 img {{ width: 100%; height: 100%; object-fit: cover; }}

    /* RIGHT HEADER TYPOGRAPHY & OFFER CARD */
    .header-info {{
        position: absolute;
        top: 730px;
        left: 540px;
        width: 500px;
        z-index: 15;
    }}

    .brand-logo-badge {{
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 12px;
    }}

    .brand-logo-badge img {{
        width: 75px;
        height: 75px;
        border-radius: 50%;
        border: 2px solid #ffd700;
    }}

    .brand-name-tag {{
        font-family: 'Playfair Display', serif;
        font-size: 34px;
        font-weight: 900;
        color: #ffd700;
        line-height: 1.1;
    }}

    .brand-title {{
        font-family: 'Playfair Display', serif;
        font-size: 76px;
        font-weight: 900;
        line-height: 1.05;
        color: #ffffff;
    }}

    .brand-sub {{
        font-family: 'Playfair Display', serif;
        font-size: 60px;
        font-style: italic;
        font-weight: 700;
        line-height: 1.1;
        color: #ffffff;
        margin-bottom: 8px;
    }}

    .tagline {{
        font-family: 'Playfair Display', serif;
        font-size: 21px;
        font-style: italic;
        color: #d8ccd4;
        line-height: 1.35;
        margin-bottom: 16px;
    }}

    /* OFFER CARD */
    .offer-card {{
        background: linear-gradient(145deg, #2b051e, #1a0312);
        border: 2px solid #ffd700;
        border-radius: 18px;
        padding: 14px 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.6);
    }}

    .offer-tag {{
        color: #ffd700;
        font-size: 20px;
        font-weight: 800;
        font-family: 'Montserrat', sans-serif;
        margin-bottom: 4px;
    }}

    .offer-pricing {{
        display: flex;
        align-items: baseline;
        gap: 14px;
    }}

    .price-main {{
        font-family: 'Playfair Display', serif;
        font-size: 46px;
        font-weight: 900;
        color: #ffffff;
    }}

    .price-strike {{
        font-size: 24px;
        color: #a8949e;
        text-decoration: line-through;
        font-weight: 600;
    }}

    .discount-badge {{
        background: #25d366;
        color: #000000;
        font-size: 16px;
        font-weight: 900;
        padding: 3px 10px;
        border-radius: 6px;
        font-family: 'Montserrat', sans-serif;
    }}

    /* ACTION BUTTONS */
    .buttons-row {{
        position: absolute;
        top: 1220px;
        left: 60px;
        width: 960px;
        display: flex;
        justify-content: space-between;
        z-index: 15;
    }}

    .pill-btn {{
        width: 450px;
        height: 80px;
        background: linear-gradient(135deg, #e6007a 0%, #b80058 100%);
        border-radius: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Montserrat', sans-serif;
        font-size: 32px;
        font-weight: 800;
        color: #ffffff;
        box-shadow: 0 8px 25px rgba(230, 0, 122, 0.4);
    }}

    /* BOTTOM 2-COLUMN GRID */
    .bottom-grid {{
        position: absolute;
        top: 1345px;
        left: 60px;
        width: 960px;
        display: grid;
        grid-template-columns: 440px 480px;
        gap: 40px;
        z-index: 15;
    }}

    .contact-col {{
        display: flex;
        flex-direction: column;
        gap: 22px;
    }}

    .contact-row {{
        display: flex;
        align-items: center;
        gap: 16px;
    }}

    .icon-circle {{
        width: 52px;
        height: 52px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}

    .icon-circle.phone {{ background: #ffd700; color: #12020e; }}
    .icon-circle.insta {{ background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); color: #ffffff; }}
    .icon-circle.loc {{ background: #eb2f46; color: #ffffff; }}

    .contact-text-gold {{
        color: #ffd700;
        font-size: 30px;
        font-weight: 800;
        font-family: 'Montserrat', sans-serif;
    }}

    .contact-text-white {{
        font-size: 26px;
        font-weight: 700;
    }}

    .address-box {{
        font-size: 21px;
        line-height: 1.35;
        color: #e0d4dc;
        font-weight: 500;
    }}

    .brand-crown-tag {{
        margin-top: 6px;
        background: #25041a;
        border: 2px solid #ffd700;
        border-radius: 12px;
        padding: 10px 16px;
        display: flex;
        align-items: center;
        gap: 10px;
        color: #ffd700;
        font-size: 18px;
        font-weight: 800;
        font-family: 'Montserrat', sans-serif;
    }}

    /* SERVICES LIST */
    .services-col {{
        display: flex;
        flex-direction: column;
        gap: 16px;
    }}

    .service-card {{
        display: flex;
        align-items: center;
        gap: 14px;
        background: rgba(255, 255, 255, 0.06);
        padding: 11px 16px;
        border-radius: 12px;
        border: 1px solid rgba(230, 0, 122, 0.35);
    }}

    .service-num {{
        width: 36px;
        height: 36px;
        background: #e6007a;
        color: #ffffff;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Montserrat', sans-serif;
        font-size: 18px;
        font-weight: 800;
        flex-shrink: 0;
    }}

    .service-title {{
        font-family: 'Playfair Display', serif;
        font-size: 26px;
        font-weight: 700;
        color: #ffffff;
    }}
</style>
</head>
<body>

    <div class="hero-box">
        <img class="hero-img" src="{hero_b64}" alt="Salon Facial">
        <div class="top-bar"></div>
        <div class="mid-wave-1"></div>
        <div class="mid-wave-2"></div>
    </div>

    <div class="circle-1"><img src="{hair_b64}" alt="Hair Spa"></div>
    <div class="circle-2"><img src="{nail_b64}" alt="Nail Art"></div>

    <div class="header-info">
        <div class="brand-logo-badge">
            <img src="{logo_b64}" alt="RM Logo">
            <div class="brand-name-tag">RANI MAKEOVER<br><span style="font-size: 18px; color: #fff; font-weight: 500;">Festive & Bridal Studio</span></div>
        </div>

        <div class="brand-title">Beauty</div>
        <div class="brand-sub">Salon</div>
        <div class="tagline">Beauty is being comfortable in your own skin. Pamper it well.</div>

        <div class="offer-card">
            <div class="offer-tag">🎁 5-IN-1 FESTIVE SPECIAL OFFER</div>
            <div class="offer-pricing">
                <div class="price-main">ONLY ₹599/-</div>
                <div class="price-strike">₹1,999</div>
                <div class="discount-badge">70% OFF</div>
            </div>
        </div>
    </div>

    <div class="buttons-row">
        <div class="pill-btn">Book Now</div>
        <div class="pill-btn">Our Services</div>
    </div>

    <div class="bottom-grid">
        <div class="contact-col">
            <div class="contact-row">
                <div class="icon-circle phone">
                    <svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2a1 1 0 011.02-.24 11.72 11.72 0 003.68.59 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1 11.72 11.72 0 00.59 3.68 1 1 0 01-.24 1.02l-2.23 2.09z"/>
                    </svg>
                </div>
                <div class="contact-text-gold">+91 9334668807</div>
            </div>

            <div class="contact-row">
                <div class="icon-circle insta">
                    <svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                    </svg>
                </div>
                <div class="contact-text-white">@Lovelyrani53</div>
            </div>

            <div class="contact-row" style="align-items: flex-start;">
                <div class="icon-circle loc">
                    <svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                    </svg>
                </div>
                <div class="address-box">
                    <div>Shop No. G-38, RC Plaza,</div>
                    <div>Kirari Chowk, Nangloi,</div>
                    <div>Delhi - 110086</div>
                </div>
            </div>

            <div class="brand-crown-tag">
                <span>👑</span>
                <span>RANI MAKEOVER & BEAUTY LOUNGE</span>
            </div>
        </div>

        <div class="services-col">
            <div class="service-card">
                <div class="service-num">1</div>
                <div class="service-title">Radiance Glow Facial</div>
            </div>
            <div class="service-card">
                <div class="service-num">2</div>
                <div class="service-title">Professional Eyebrows</div>
            </div>
            <div class="service-card">
                <div class="service-num">3</div>
                <div class="service-title">Forehead Threading</div>
            </div>
            <div class="service-card">
                <div class="service-num">4</div>
                <div class="service-title">Upper Lips Care</div>
            </div>
            <div class="service-card">
                <div class="service-num">5</div>
                <div class="service-title">Full Arms Glow Waxing</div>
            </div>
        </div>
    </div>

</body>
</html>
"""

    temp_html = BASE_DIR / "temp" / "canva_creative_demo.html"
    temp_html.parent.mkdir(parents=True, exist_ok=True)
    temp_html.write_text(html, encoding="utf-8")

    out_png = BASE_DIR / "posters_showcase" / "RANI_MAKEOVER_MASTER_CREATIVE_DEMO.png"
    out_png.parent.mkdir(parents=True, exist_ok=True)

    chrome_exe = find_chrome()
    cmd = [
        chrome_exe,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        "--window-size=1080,1920",
        f"--screenshot={str(out_png.resolve())}",
        f"file:///{str(temp_html.resolve()).replace(chr(92), '/')}"
    ]

    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    size_mb = out_png.stat().st_size / (1024 * 1024)
    print(f"✅ Master Creative Poster Generated: {out_png.name} ({size_mb:.2f} MB)")

    # Save copy to Desktop
    desktop_copy = Path(r"C:\Users\EDITI\OneDrive\Desktop\RANI_MAKEOVER_MASTER_CREATIVE.png")
    shutil.copy2(out_png, desktop_copy)
    print(f"💻 Saved to Desktop: '{desktop_copy.name}'")

    # Upload to Google Drive
    try:
        from scripts.upload_to_gdrive_clint import get_gdrive_service, find_or_create_folder, upload_file
        service = get_gdrive_service()
        clint_id = find_or_create_folder(service, "CLINT")
        posters_id = find_or_create_folder(service, "02_DESIGN_SYSTEM_AND_PROMPTS", parent_id=clint_id)
        upload_file(service, out_png, posters_id, mime_type="image/png")
        print("☁️ Uploaded Master Creative to Google Drive 'CLINT' Folder!")
    except Exception as e:
        print(f"GDrive sync note: {e}")

    print("=" * 80)

if __name__ == "__main__":
    render_creative()
