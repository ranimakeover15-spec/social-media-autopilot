import urllib.request
import json
import sys

# Enforce UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

token = "8997636217:AAGnU3XP9GgmiS60zitBnxe_4vy99n-F-ug"
url = f"https://api.telegram.org/bot{token}/getUpdates"

req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        results = data.get("result", [])
        print("=" * 60)
        print(f"📥 TELEGRAM BOT INBOX STATUS: {len(results)} Update(s)")
        print("=" * 60)
        if not results:
            print("ℹ️ Render Cloud is actively polling and consuming messages immediately!")
            print("👉 Send a message now on Telegram (@RaniMakeover_reel_bot) to test!")
        for idx, u in enumerate(results, 1):
            msg = u.get("message", {})
            sender = msg.get("from", {}).get("first_name", "Unknown")
            username = msg.get("from", {}).get("username", "None")
            text = msg.get("text", "")
            has_video = "video" in msg or ("document" in msg and msg.get("document", {}).get("mime_type", "").startswith("video/"))
            has_voice = "voice" in msg or "audio" in msg
            media_type = "VIDEO" if has_video else ("VOICE" if has_voice else "TEXT")
            print(f"{idx}. From: {sender} (@{username}) | Type: [{media_type}] | Content: '{text}'")
        print("=" * 60)
except Exception as e:
    print(f"Inbox read error (expected if Render long-polling is active): {e}")
