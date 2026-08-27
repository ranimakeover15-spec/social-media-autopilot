"""
👑 RANI MAKEOVER — 24/7 TELEGRAM ASSET INGESTION BOT & CLOUD DAEMON
Includes lightweight HTTP Health-Check Server on $PORT for Render.com Web Services.
"""

import os
import sys
import time
import json
import threading
import http.server
import socketserver
import urllib.request
import urllib.parse
from pathlib import Path

# Enforce UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from core.logger import logger
from scripts.render_canva_html_poster import generate_canva_html, render_html_to_png, render_reel, image_to_base64

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8997636217:AAGnU3XP9GgmiS60zitBnxe_4vy99n-F-ug")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ------------------------------------------------------------------------------
# LIGHTWEIGHT HTTP HEALTH CHECK SERVER FOR RENDER.COM CLOUD
# ------------------------------------------------------------------------------
class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Rani Makeover 24/7 Telegram Cloud Bot is Live and Healthy! OK\n")

    def log_message(self, format, *args):
        pass  # Suppress health check access logs

def start_health_check_server():
    port = int(os.getenv("PORT", "10000"))
    try:
        with socketserver.TCPServer(("0.0.0.0", port), HealthCheckHandler) as httpd:
            logger.info(f"🌐 Cloud Health Check Server running on port {port}...")
            httpd.serve_forever()
    except Exception as e:
        logger.warning(f"Health server note: {e}")

# ------------------------------------------------------------------------------
# TELEGRAM API HELPERS
# ------------------------------------------------------------------------------
def api_call(method: str, params: dict = None, data: bytes = None, headers: dict = None) -> dict:
    url = f"{API_URL}/{method}"
    if params and not data:
        url += "?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers=headers or {"User-Agent": "Mozilla/5.0"})
    else:
        req = urllib.request.Request(url, data=data, headers=headers or {"User-Agent": "Mozilla/5.0"})

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        logger.error(f"Telegram API Error ({method}): {e}")
        return {"ok": False, "error": str(e)}

def send_message(chat_id: int, text: str, parse_mode: str = "Markdown") -> dict:
    return api_call("sendMessage", {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    })

def send_photo(chat_id: int, photo_path: Path, caption: str = ""):
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = bytearray()

    def add_field(name, val):
        body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{val}\r\n".encode("utf-8"))

    add_field("chat_id", str(chat_id))
    if caption:
        add_field("caption", caption)

    filename = photo_path.name
    body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"photo\"; filename=\"{filename}\"\r\nContent-Type: image/png\r\n\r\n".encode("utf-8"))
    body.extend(photo_path.read_bytes())
    body.extend(f"\r\n--{boundary}--\r\n".encode("utf-8"))

    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "User-Agent": "Mozilla/5.0"
    }
    return api_call("sendPhoto", data=bytes(body), headers=headers)

def send_video(chat_id: int, video_path: Path, caption: str = ""):
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = bytearray()

    def add_field(name, val):
        body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{val}\r\n".encode("utf-8"))

    add_field("chat_id", str(chat_id))
    if caption:
        add_field("caption", caption)

    filename = video_path.name
    body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"video\"; filename=\"{filename}\"\r\nContent-Type: video/mp4\r\n\r\n".encode("utf-8"))
    body.extend(video_path.read_bytes())
    body.extend(f"\r\n--{boundary}--\r\n".encode("utf-8"))

    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "User-Agent": "Mozilla/5.0"
    }
    return api_call("sendVideo", data=bytes(body), headers=headers)

def download_file(file_id: str, dest_path: Path) -> Path:
    res = api_call("getFile", {"file_id": file_id})
    if not res.get("ok"):
        raise Exception(f"Failed to get file info: {res}")
    file_path = res["result"]["file_path"]
    download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(download_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp, open(dest_path, "wb") as f:
        f.write(resp.read())
    return dest_path

def handle_text_offer(chat_id: int, text: str):
    send_message(chat_id, "🎨 *Aapka Request Mil Gaya Hai!* 10/10 Canva-Grade Poster aur 9:16 Video Reel banna shuru ho gaya hai...")

    photo_dir = BASE_DIR / "assets" / "salon_photos"
    hero_b64 = image_to_base64(photo_dir / "facial_hero.jpg")
    hair_b64 = image_to_base64(photo_dir / "hair_wash.jpg")
    nail_b64 = image_to_base64(photo_dir / "nail_art.jpg")

    clean_name = "".join(c for c in text[:20] if c.isalnum() or c in " _-").strip().replace(" ", "_").lower()
    if not clean_name:
        clean_name = f"offer_{int(time.time())}"

    out_poster = BASE_DIR / "posters_showcase" / f"{clean_name}_poster.png"
    out_reel = BASE_DIR / "content_vault" / f"{clean_name}_reel.mp4"

    html = generate_canva_html(
        hero_b64=hero_b64,
        hair_b64=hair_b64,
        nail_b64=nail_b64,
        offer_title=f"🎁 {text.upper()[:35]}",
        price_deal="ONLY ₹599/-",
        price_original="₹1,999",
        discount="70% OFF"
    )

    render_html_to_png(html, out_poster)
    render_reel(out_poster, out_reel, duration=15)

    # Sync to GDrive
    try:
        from scripts.upload_to_gdrive_clint import main as sync_gdrive
        sync_gdrive()
    except Exception as e:
        logger.warning(f"GDrive Sync warning: {e}")

    # Send preview back to client
    send_photo(chat_id, out_poster, caption=f"✅ *Luxury Graphic Poster Ready!*\n🎁 Offer: {text}\n📍 Saved to Google Drive CLINT Vault & 24/7 Autopilot!")
    send_video(chat_id, out_reel, caption=f"🎬 *9:16 Full HD Motion Reel Ready!*\n🚀 Ready for YouTube Shorts & Instagram Reels!")

def handle_video_upload(chat_id: int, file_id: str, file_name: str, caption: str = ""):
    send_message(chat_id, f"📹 *Raw Video Receive Ho Gaya:* `{file_name}`\nTranscoding and adding Rani Makeover branding...")

    raw_path = BASE_DIR / "temp" / f"raw_{int(time.time())}_{file_name}"
    download_file(file_id, raw_path)

    from core.transcoder import VideoTranscoder
    out_reel = BASE_DIR / "content_vault" / f"client_reel_{raw_path.stem}.mp4"
    transcoder = VideoTranscoder()
    transcoder.transcode(raw_path, out_reel)

    # Sync to GDrive
    try:
        from scripts.upload_to_gdrive_clint import main as sync_gdrive
        sync_gdrive()
    except Exception:
        pass

    send_video(chat_id, out_reel, caption=f"🎉 *Aapka Master 9:16 Video Reel Taiyar Hai!*\n📁 Location: content_vault & Google Drive\n🚀 Scheduled for 24/7 Auto-Publishing!")

def run_bot():
    print("=" * 80)
    print("🤖 RANI MAKEOVER TELEGRAM BOT DAEMON IS RUNNING...")
    print(f"👉 Bot: @RaniMakeover_reel_bot")
    print("=" * 80)

    # Start HTTP Health Server in background thread for Render.com
    t = threading.Thread(target=start_health_check_server, daemon=True)
    t.start()

    offset = 0
    while True:
        try:
            updates = api_call("getUpdates", {"offset": offset, "timeout": 20})
            if updates.get("ok"):
                for u in updates.get("result", []):
                    offset = u["update_id"] + 1
                    msg = u.get("message", {})
                    chat_id = msg.get("chat", {}).get("id")
                    if not chat_id:
                        continue

                    # 1. Text command / offer
                    if "text" in msg:
                        text = msg["text"].strip()
                        if text == "/start":
                            send_message(chat_id, "👑 *Namaste & Welcome to Rani Makeover & Beauty Lounge Bot!*\n\n👉 Aap yahan:\n1️⃣ *Raw Video bhejiye:* Hum use 9:16 Master Reel bana denge.\n2️⃣ *Festive Offer / Topic likhiye ya Voice Note bhejiye:* Hum turant 10/10 Canva Poster aur Video Reel bana denge!\n\n🚀 *Sabhi content 24/7 Google Drive aur Social Media Autopilot me sync hota hai.*")
                        else:
                            handle_text_offer(chat_id, text)

                    # 2. Video file
                    elif "video" in msg:
                        v = msg["video"]
                        handle_video_upload(chat_id, v["file_id"], v.get("file_name", "video.mp4"), msg.get("caption", ""))

                    # 3. Document (video)
                    elif "document" in msg:
                        d = msg["document"]
                        if d.get("mime_type", "").startswith("video/"):
                            handle_video_upload(chat_id, d["file_id"], d.get("file_name", "doc_video.mp4"), msg.get("caption", ""))

            time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping bot...")
            break
        except Exception as e:
            logger.error(f"Polling loop error: {e}")
            time.sleep(3)

if __name__ == "__main__":
    run_bot()
