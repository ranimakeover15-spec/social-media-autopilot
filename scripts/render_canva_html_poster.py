"""
Canva-Grade Pixel-Perfect Luxury Salon HTML/CSS Renderer.
Cross-Platform (Windows & Linux Cloud) Headless Chrome/Chromium.
"""

import os
import sys
import shutil
import base64
import subprocess
from pathlib import Path

# Enforce UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent

def find_chrome_executable() -> str:
    """Finds Chrome, Chromium, or Edge across Windows and Linux."""
    candidates = [
        # Windows
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        # Linux / Docker
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        shutil.which("chromium"),
        shutil.which("google-chrome"),
        shutil.which("chrome")
    ]
    for c in candidates:
        if c and Path(c).exists():
            return str(c)
    return "chrome"

def image_to_base64(path: Path) -> str:
    if not path.exists():
        return ""
    mime = "image/jpeg" if path.suffix.lower() in [".jpg", ".jpeg"] else "image/png"
    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"

def generate_canva_html(
    hero_b64: str,
    hair_b64: str,
    nail_b64: str,
    brand_title: str = "Beauty",
    brand_sub: str = "Salon",
    tagline: str = "Beauty is being comfortable in your own skin. Pamper it well.",
    offer_title: str = "🎁 RAKSHA BANDHAN 5-IN-1 SPECIAL",
    price_deal: str = "ONLY ₹599/-",
    price_original: str = "₹1,999",
    discount: str = "70% OFF",
    phone: str = "+91 9334668807",
    instagram: str = "@Lovelyrani53",
    address_l1: str = "Shop No. G-38, RC Plaza,",
    address_l2: str = "Kirari Chowk, Nangloi,",
    address_l3: str = "Delhi - 110086",
    services: list = None
) -> str:
    if services is None:
        services = [
            "Radiance Glow Facial",
            "Professional Eyebrows",
            "Forehead Threading",
            "Upper Lips Care",
            "Full Arms Glow Waxing"
        ]

    service_items_html = ""
    for idx, s in enumerate(services, 1):
        service_items_html += f"""
        <div class="service-row">
            <div class="service-num">{idx}</div>
            <div class="service-name">{s}</div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&family=Playfair+Display:ital,wght@0,600;0,700;0,900;1,600;1,700&family=Poppins:wght@400;500;600;700&display=swap');

    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}

    body {{
        width: 1080px;
        height: 1920px;
        background-color: #12020e;
        color: #ffffff;
        font-family: 'Poppins', sans-serif;
        overflow: hidden;
        position: relative;
    }}

    /* TOP HERO SECTION */
    .hero-container {{
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

    /* ORGANIC S-CURVES */
    .top-wave {{
        position: absolute;
        top: 0;
        left: 0;
        width: 1080px;
        height: 120px;
        background: linear-gradient(135deg, #e6007a 0%, #b80058 100%);
        clip-path: polygon(0 0, 100% 0, 100% 70px, 65% 50px, 30% 95px, 0 40px);
        z-index: 2;
    }}

    .mid-wave-1 {{
        position: absolute;
        bottom: 0;
        left: 0;
        width: 1080px;
        height: 240px;
        background: linear-gradient(135deg, #e6007a 0%, #a0004e 100%);
        clip-path: polygon(0 90px, 35% 60px, 70% 120px, 100% 20px, 100% 100%, 0 100%);
        z-index: 2;
    }}

    .mid-wave-2 {{
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 1080px;
        height: 170px;
        background: #12020e;
        clip-path: polygon(0 75px, 40% 50px, 75% 100px, 100% 30px, 100% 100%, 0 100%);
        z-index: 3;
    }}

    /* CIRCULAR INSET PHOTOS */
    .circle-inset-1 {{
        position: absolute;
        top: 560px;
        left: 40px;
        width: 440px;
        height: 440px;
        border-radius: 50%;
        border: 8px solid #ffffff;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
        overflow: hidden;
        z-index: 10;
        background: #20051a;
    }}

    .circle-inset-1 img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}

    .circle-inset-2 {{
        position: absolute;
        top: 480px;
        left: 310px;
        width: 320px;
        height: 320px;
        border-radius: 50%;
        border: 8px solid #ffffff;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);
        overflow: hidden;
        z-index: 12;
        background: #20051a;
    }}

    .circle-inset-2 img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
    }}

    /* RIGHT SIDE HEADER TYPOGRAPHY */
    .header-info {{
        position: absolute;
        top: 760px;
        left: 540px;
        width: 500px;
        z-index: 15;
    }}

    .brand-title {{
        font-family: 'Playfair Display', serif;
        font-size: 82px;
        font-weight: 900;
        line-height: 1.05;
        color: #ffffff;
        text-shadow: 0 4px 15px rgba(0, 0, 0, 0.8);
    }}

    .brand-sub {{
        font-family: 'Playfair Display', serif;
        font-size: 68px;
        font-style: italic;
        font-weight: 700;
        line-height: 1.1;
        color: #ffffff;
        margin-bottom: 12px;
        text-shadow: 0 4px 15px rgba(0, 0, 0, 0.8);
    }}

    .tagline {{
        font-family: 'Playfair Display', serif;
        font-size: 24px;
        font-style: italic;
        color: #d8ccd4;
        line-height: 1.35;
        margin-bottom: 20px;
    }}

    /* FESTIVE OFFER CARD (FLEXBOX AUTO-SCALED) */
    .offer-card {{
        background: linear-gradient(145deg, #2b051e, #1a0312);
        border: 2px solid #ffd700;
        border-radius: 18px;
        padding: 14px 20px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
    }}

    .offer-tag {{
        color: #ffd700;
        font-size: 20px;
        font-weight: 800;
        font-family: 'Montserrat', sans-serif;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }}

    .offer-pricing-row {{
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
        padding: 3px 8px;
        border-radius: 6px;
        font-family: 'Montserrat', sans-serif;
    }}

    /* ACTION BUTTONS ROW */
    .buttons-row {{
        position: absolute;
        top: 1230px;
        left: 60px;
        width: 960px;
        display: flex;
        justify-content: space-between;
        z-index: 15;
    }}

    .pill-btn {{
        width: 440px;
        height: 85px;
        background: linear-gradient(135deg, #e6007a 0%, #b80058 100%);
        border-radius: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Montserrat', sans-serif;
        font-size: 34px;
        font-weight: 800;
        color: #ffffff;
        box-shadow: 0 8px 25px rgba(230, 0, 122, 0.4);
    }}

    /* BOTTOM 2-COLUMN GRID */
    .bottom-grid {{
        position: absolute;
        top: 1360px;
        left: 60px;
        width: 960px;
        display: grid;
        grid-template-columns: 440px 480px;
        gap: 40px;
        z-index: 15;
    }}

    /* LEFT CONTACT COLUMN */
    .contact-col {{
        display: flex;
        flex-direction: column;
        gap: 24px;
    }}

    .contact-row {{
        display: flex;
        align-items: center;
        gap: 18px;
    }}

    .icon-circle {{
        width: 54px;
        height: 54px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}

    .icon-circle.phone {{
        background: #ffd700;
        color: #12020e;
    }}

    .icon-circle.insta {{
        background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
        color: #ffffff;
    }}

    .icon-circle.loc {{
        background: #eb2f46;
        color: #ffffff;
    }}

    .contact-text {{
        font-size: 28px;
        font-weight: 700;
    }}

    .contact-text.gold {{
        color: #ffd700;
        font-size: 30px;
        font-family: 'Montserrat', sans-serif;
    }}

    .address-box {{
        font-size: 21px;
        line-height: 1.4;
        color: #e0d4dc;
        font-weight: 500;
    }}

    .brand-badge {{
        margin-top: 10px;
        background: #25041a;
        border: 2px solid #d4af37;
        border-radius: 12px;
        padding: 12px 18px;
        display: flex;
        align-items: center;
        gap: 10px;
        color: #ffd700;
        font-size: 19px;
        font-weight: 800;
        font-family: 'Montserrat', sans-serif;
    }}

    /* RIGHT SERVICES COLUMN */
    .services-col {{
        display: flex;
        flex-direction: column;
        gap: 18px;
    }}

    .service-row {{
        display: flex;
        align-items: center;
        gap: 16px;
        background: rgba(255, 255, 255, 0.05);
        padding: 12px 18px;
        border-radius: 14px;
        border: 1px solid rgba(230, 0, 122, 0.3);
    }}

    .service-num {{
        width: 38px;
        height: 38px;
        background: #e6007a;
        color: #ffffff;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Montserrat', sans-serif;
        font-size: 20px;
        font-weight: 800;
        flex-shrink: 0;
    }}

    .service-name {{
        font-family: 'Playfair Display', serif;
        font-size: 28px;
        font-weight: 700;
        color: #ffffff;
    }}
</style>
</head>
<body>

    <!-- TOP HERO IMAGE & WAVES -->
    <div class="hero-container">
        <img class="hero-img" src="{hero_b64}" alt="Salon Facial">
        <div class="top-wave"></div>
        <div class="mid-wave-1"></div>
        <div class="mid-wave-2"></div>
    </div>

    <!-- CIRCULAR INSET PHOTOS -->
    <div class="circle-inset-1">
        <img src="{hair_b64}" alt="Hair Spa">
    </div>
    <div class="circle-inset-2">
        <img src="{nail_b64}" alt="Nail Art">
    </div>

    <!-- RIGHT TOP BRANDING & OFFER CARD -->
    <div class="header-info">
        <div class="brand-title">{brand_title}</div>
        <div class="brand-sub">{brand_sub}</div>
        <div class="tagline">{tagline}</div>

        <div class="offer-card">
            <div class="offer-tag">{offer_title}</div>
            <div class="offer-pricing-row">
                <div class="price-main">{price_deal}</div>
                <div class="price-strike">{price_original}</div>
                <div class="discount-badge">{discount}</div>
            </div>
        </div>
    </div>

    <!-- ACTION BUTTONS ROW -->
    <div class="buttons-row">
        <div class="pill-btn">Book Now</div>
        <div class="pill-btn">Our Service</div>
    </div>

    <!-- BOTTOM 2-COLUMN GRID -->
    <div class="bottom-grid">
        <!-- LEFT: CONTACT & LOCATION -->
        <div class="contact-col">
            <div class="contact-row">
                <div class="icon-circle phone">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M6.62 10.79a15.053 15.053 0 006.59 6.59l2.2-2.2a1 1 0 011.02-.24 11.72 11.72 0 003.68.59 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1 11.72 11.72 0 00.59 3.68 1 1 0 01-.24 1.02l-2.23 2.09z"/>
                    </svg>
                </div>
                <div class="contact-text gold">{phone}</div>
            </div>

            <div class="contact-row">
                <div class="icon-circle insta">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                    </svg>
                </div>
                <div class="contact-text">{instagram}</div>
            </div>

            <div class="contact-row" style="align-items: flex-start;">
                <div class="icon-circle loc">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                    </svg>
                </div>
                <div class="address-box">
                    <div>{address_l1}</div>
                    <div>{address_l2}</div>
                    <div>{address_l3}</div>
                </div>
            </div>

            <div class="brand-badge">
                <span>👑</span>
                <span>RANI MAKEOVER & LOUNGE</span>
            </div>
        </div>

        <!-- RIGHT: 5-STAR SERVICES -->
        <div class="services-col">
            {service_items_html}
        </div>
    </div>

</body>
</html>
"""
    return html

def render_html_to_png(html_content: str, output_png_path: Path) -> Path:
    temp_html = BASE_DIR / "temp" / "canva_poster.html"
    temp_html.parent.mkdir(parents=True, exist_ok=True)
    temp_html.write_text(html_content, encoding="utf-8")

    chrome_path = find_chrome_executable()

    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        f"--window-size=1080,1920",
        f"--screenshot={str(output_png_path.resolve())}",
        f"file:///{str(temp_html.resolve()).replace(chr(92), '/')}"
    ]

    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output_png_path

def render_reel(poster_path: Path, output_mp4: Path, duration: int = 15):
    vf = "zoompan=z='min(zoom+0.0004,1.06)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=450:s=1080x1920:fps=30"
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(poster_path),
        "-f", "lavfi", "-i", f"sine=frequency=432:duration={duration}",
        "-filter_complex", vf,
        "-c:v", "libx264", "-t", str(duration),
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        str(output_mp4)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output_mp4
