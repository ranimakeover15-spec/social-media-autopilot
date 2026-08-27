"""
👑 RANI MAKEOVER — DIRECT 1-CLICK INSTAGRAM LINKER (CLEAN VISIBLE INPUT)
Logs in directly to Instagram (@Lovelyrani53) and generates permanent instagram_session.json
"""

import os
import sys
import json
from pathlib import Path
from instagrapi import Client

# Enforce UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
SESSION_FILE = BASE_DIR / "instagram_session.json"

def main():
    print("=" * 80)
    print("📸 RANI MAKEOVER — DIRECT INSTAGRAM ACCOUNT LINKER")
    print("=" * 80)
    print("👉 Connects directly to Instagram (@Lovelyrani53) without Facebook.\n")

    cl = Client()
    cl.delay_range = [2, 5]

    # Check existing session
    if SESSION_FILE.exists():
        try:
            print(f"🔍 Found existing session, verifying...")
            cl.load_settings(SESSION_FILE)
            user_info = cl.user_info_by_username("Lovelyrani53")
            print(f"✅ Instagram already connected as: @{user_info.username} ({user_info.full_name})")
            return
        except Exception as e:
            print(f"Session expired or needs fresh login: {e}\n")

    username = input("Enter Instagram Username [default: Lovelyrani53]: ").strip()
    if not username:
        username = "Lovelyrani53"

    # Use clean standard input so user can see what they type
    password = input(f"Enter Instagram Password for @{username}: ").strip()

    print(f"\n⏳ Logging in directly to Instagram as @{username}...")
    try:
        cl.login(username, password)
        cl.dump_settings(SESSION_FILE)
        print("\n" + "=" * 80)
        print(f"🎉 INSTAGRAM @{username} CONNECTED SUCCESSFULLY!")
        print(f"💾 Permanent session saved to: {SESSION_FILE}")
        print("🚀 Auto-posting for Instagram Reels is now 100% READY!")
        print("=" * 80)
    except Exception as e:
        print(f"\n❌ Login note: {e}")
        # Check if 2FA or checkpoint code is needed
        if "two_factor_required" in str(e).lower() or "challenge" in str(e).lower() or "checkpoint" in str(e).lower():
            code = input("\nEnter the 6-digit Security Code sent to your phone/SMS: ").strip()
            try:
                cl.login(username, password, verification_code=code)
                cl.dump_settings(SESSION_FILE)
                print("\n🎉 INSTAGRAM 2FA VERIFIED & CONNECTED SUCCESSFULLY!")
            except Exception as e2:
                print(f"❌ 2FA verification error: {e2}")

if __name__ == "__main__":
    main()
