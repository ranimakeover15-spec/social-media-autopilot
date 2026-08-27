"""
👑 RANI MAKEOVER — 24/7 TELEGRAM ASSET INGESTION BOT & CLOUD AUTOPILOT DAEMON
Runs 24/7 on Render.com Cloud.
Features:
1. Lightweight HTTP Health Check Server for Render Web Services.
2. 24/7 Background Scheduler Thread for 09:00 AM, 02:00 PM, 07:00 PM IST.
3. Priority 1 Ingestion of Raw Videos & Offers sent on Telegram.
4. Auto-Publishing to YouTube Shorts, Instagram Reels & Story, and Facebook.
5. Instant Live Link Telegram Dispatch.
"""

import os
import sys
import time
import json
import datetime
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
from core.telegram_priority_unified_pipeline import TelegramPriorityPipeline

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8997636217:AAGnU3XP9GgmiS60zitBnxe_4vy99n-F-ug")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ------------------------------------------------------------------------------
# 1. LIGHTWEIGHT HTTP HEALTH CHECK SERVER FOR RENDER.COM CLOUD
# ------------------------------------------------------------------------------
class HealthCheckHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Rani Makeover 24/7 Telegram Cloud Bot & Autopilot is Live and Healthy! OK\n")

    def log_message(self, format, *args):
        pass

def start_health_check_server():
    port = int(os.getenv("PORT", "10000"))
    try:
        with socketserver.TCPServer(("0.0.0.0", port), HealthCheckHandler) as httpd:
            logger.info(f"🌐 Cloud Health Check Server running on port {port}...")
            httpd.serve_forever()
    except Exception as e:
        logger.warning(f"Health server note: {e}")

# ------------------------------------------------------------------------------
# 2. 24/7 BACKGROUND CLOUD SCHEDULER THREAD (IST 09:00 AM, 02:00 PM, 07:00 PM)
# ------------------------------------------------------------------------------
def background_cloud_scheduler():
    logger.info("⏰ 24/7 Cloud Background Scheduler Thread Started...")
    last_triggered_minute = ""

    while True:
        try:
            # Calculate current IST Time (UTC + 5:30)
            now_utc = datetime.datetime.now(datetime.timezone.utc)
            ist_offset = datetime.timedelta(hours=5, minutes=30)
            now_ist = now_utc + ist_offset

            current_time_str = now_ist.strftime("%H:%M")
            current_date_str = now_ist.strftime("%Y-%m-%d")
            time_key = f"{current_date_str}_{current_time_str}"

            # Slots: 09:00 AM, 14:00 (02:00 PM), 19:00 (07:00 PM) IST
            if time_key != last_triggered_minute:
                if current_time_str == "09:00":
                    logger.info("🌅 [09:00 AM IST TRIGGER] Executing Morning Scheduled Slot...")
                    last_triggered_minute = time_key
                    pipeline = TelegramPriorityPipeline()
                    pipeline.execute_pipeline("morning")

                elif current_time_str == "14:00":
                    logger.info("☀️ [02:00 PM IST TRIGGER] Executing Afternoon Scheduled Slot...")
                    last_triggered_minute = time_key
                    pipeline = TelegramPriorityPipeline()
                    pipeline.execute_pipeline("afternoon")

                elif current_time_str == "19:00":
                    logger.info("🌆 [07:00 PM IST TRIGGER] Executing Evening Scheduled Slot...")
                    last_triggered_minute = time_key
                    pipeline = TelegramPriorityPipeline()
                    pipeline.execute_pipeline("evening")

            time.sleep(25)  # Check every 25 seconds
        except Exception as e:
            logger.error(f"Scheduler loop note: {e}")
            time.sleep(30)

# ------------------------------------------------------------------------------
# 3. TELEGRAM API HELPERS
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

def send_message(chat_id: int, text: str, parse_mode: str = "HTML") -> dict:
    return api_call("sendMessage", {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode
    })

# ------------------------------------------------------------------------------
# 4. TELEGRAM INTERACTIVE HANDLERS
# ------------------------------------------------------------------------------
def handle_text_offer(chat_id: int, text: str):
    send_message(chat_id, "⏳ <b>Processing your request...</b>\nBranding with Official RM Logo & Publishing across all channels!")
    pipeline = TelegramPriorityPipeline()
    pipeline.execute_pipeline("afternoon")

def handle_video_upload(chat_id: int, file_id: str, file_name: str, caption: str = ""):
    send_message(chat_id, f"📥 <b>Raw Video Received!</b>\nApplying Master 9:16 Branding, Music & Auto-Publishing...")
    pipeline = TelegramPriorityPipeline()
    pipeline.execute_pipeline("afternoon")

def run_bot():
    print("=" * 80)
    print("🤖 RANI MAKEOVER 24/7 TELEGRAM & AUTOPILOT DAEMON IS RUNNING...")
    print(f"👉 Bot: @RaniMakeover_reel_bot")
    print("=" * 80)

    # 1. Start HTTP Health Server in background thread for Render.com
    t_health = threading.Thread(target=start_health_check_server, daemon=True)
    t_health.start()

    # 2. Start Background 24/7 Scheduler Thread for 09:00 AM, 02:00 PM, 07:00 PM IST
    t_sched = threading.Thread(target=background_cloud_scheduler, daemon=True)
    t_sched.start()

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

                    if "text" in msg:
                        text = msg["text"].strip()
                        if text == "/start":
                            send_message(chat_id, "👑 <b>Namaste & Welcome to Rani Makeover & Beauty Lounge Autopilot!</b>\n\n👉 <b>Aap yahan:</b>\n1️⃣ <b>Raw Video bhejiye:</b> Master 9:16 Reel bankar YouTube & Insta par post ho jayegi.\n2️⃣ <b>Festive Offer likhiye:</b> Turant Canva Poster & Reel publish ho jayenge!\n\n🚀 <b>Schedule:</b> 09:00 AM, 02:00 PM, 07:00 PM IST par auto-publish hota hai.")
                        elif text == "/publish_now":
                            send_message(chat_id, "🚀 <b>Triggering Instant Publication...</b>")
                            pipeline = TelegramPriorityPipeline()
                            pipeline.execute_pipeline("afternoon")
                        else:
                            handle_text_offer(chat_id, text)

                    elif "video" in msg:
                        v = msg["video"]
                        handle_video_upload(chat_id, v["file_id"], v.get("file_name", "video.mp4"), msg.get("caption", ""))

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
