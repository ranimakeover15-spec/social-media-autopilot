"""
Log in to Instagram directly using authenticated browser sessionid.
"""

import os
import sys
import json
import urllib.parse
from pathlib import Path
from instagrapi import Client

# Enforce UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
SESSION_FILE = BASE_DIR / "instagram_session.json"

RAW_SESSIONID = "37979168548%3AZTbx4QIsZzMcur%3A20%3AAYhIE78CGoSypO0E68s1_EXMapLGVx7ND_68kwnydQ"
USER_ID = "37979168548"
CSRF_TOKEN = "CfpwZ9laJYrKh3aXKiligGkBI1D0h4CJ"

def main():
    print("=" * 80)
    print("📸 CONNECTING TO INSTAGRAM VIA ACTIVE BROWSER SESSION")
    print("=" * 80)

    sessionid = urllib.parse.unquote(RAW_SESSIONID)

    cl = Client()
    cl.delay_range = [1, 3]

    print(f"⏳ Authenticating with Session ID for User ID: {USER_ID}...")
    try:
        cl.login_by_sessionid(sessionid)
        cl.dump_settings(SESSION_FILE)

        user_info = cl.user_info_by_username("Lovelyrani53")
        print("\n" + "=" * 80)
        print("🎉 INSTAGRAM ACCOUNT SUCCESSFULLY CONNECTED!")
        print(f"👤 Username: @{user_info.username}")
        print(f"👑 Full Name: {user_info.full_name}")
        print(f"📊 Followers: {user_info.follower_count} | Posts: {user_info.media_count}")
        print(f"💾 Permanent Session Saved to: {SESSION_FILE}")
        print("🚀 Instagram Reels 24/7 Auto-Posting is now 100% LIVE!")
        print("=" * 80)
    except Exception as e:
        print(f"❌ Connection error: {e}")
        # Try injecting full cookies dict
        try:
            settings = {
                "authorization_data": {
                    "ds_user_id": USER_ID,
                    "sessionid": sessionid
                },
                "cookies": {
                    "sessionid": sessionid,
                    "ds_user_id": USER_ID,
                    "csrftoken": CSRF_TOKEN
                }
            }
            cl.set_settings(settings)
            cl.dump_settings(SESSION_FILE)
            user_info = cl.user_info_by_username("Lovelyrani53")
            print("\n🎉 INSTAGRAM CONNECTED VIA EXTENDED COOKIES!")
            print(f"👤 Username: @{user_info.username}")
        except Exception as e2:
            print(f"Extended error: {e2}")

if __name__ == "__main__":
    main()
