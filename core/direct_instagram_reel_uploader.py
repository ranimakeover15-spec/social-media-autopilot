"""
Direct Instagram Reel Uploader using persistent session.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from instagrapi import Client

# Enforce UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
SESSION_FILE = BASE_DIR / "instagram_session.json"

class DirectInstagramUploader:
    def __init__(self):
        self.cl = Client()
        self.cl.delay_range = [2, 5]
        self.is_configured = False
        self._load_session()

    def _load_session(self):
        if SESSION_FILE.exists():
            try:
                self.cl.load_settings(SESSION_FILE)
                self.is_configured = True
            except Exception as e:
                print(f"Error loading Instagram session: {e}")

    def upload_reel(self, video_path: Path, caption: str) -> Dict[str, Any]:
        if not self.is_configured:
            return {"status": "failed", "error": "Instagram session not found. Please run CONNECT_INSTAGRAM.bat first."}

        try:
            print(f"📸 Uploading Reel directly to Instagram: '{video_path.name}'...")
            media = self.cl.clip_upload(
                path=str(video_path),
                caption=caption
            )
            print(f"🎉 Instagram Reel Published! Media Code: {media.code}")
            return {
                "status": "success",
                "platform": "instagram",
                "media_id": media.id,
                "media_code": media.code,
                "url": f"https://www.instagram.com/reel/{media.code}/"
            }
        except Exception as e:
            print(f"❌ Instagram upload error: {e}")
            return {"status": "failed", "error": str(e)}
