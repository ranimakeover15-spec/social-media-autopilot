"""
Facebook Reels Uploader.
Uses Facebook Graph API v19.0 / v20.0 Pages Video Reels 3-phase upload protocol:
Phase 1: Initialize (upload_phase=start)
Phase 2: Transfer binary chunk (POST rupload stream)
Phase 3: Finalize & Publish (upload_phase=finish, video_state=PUBLISHED)
"""

import os
import requests
from pathlib import Path
from typing import Dict, Any, Optional

from core.logger import logger
from core.config import config

GRAPH_API_VERSION = "v19.0"
GRAPH_BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

class FacebookUploader:
    def __init__(self):
        self.page_id = config.facebook_page_id
        self.page_access_token = config.facebook_page_access_token
        self.is_configured = bool(self.page_id and self.page_access_token)

        if not self.is_configured:
            logger.warning("⚠️ Facebook credentials (FACEBOOK_PAGE_ID or FACEBOOK_PAGE_ACCESS_TOKEN) not set.")
        else:
            logger.info("✅ Facebook Graph API Reels client configured.")

    def upload_reel(
        self,
        video_path: Path,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Uploads video to Facebook Page Reels using the official 3-phase protocol.
        """
        if not self.is_configured:
            logger.error("Facebook client not configured. Skipping upload.")
            return {"status": "skipped", "error": "Not configured"}

        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        description = metadata.get("facebook", {}).get("description", metadata.get("hashtags_string", ""))
        logger.info(f"📘 Starting Facebook Reel upload ({video_path.name})...")

        try:
            # Phase 1: Initialize
            start_url = f"{GRAPH_BASE_URL}/{self.page_id}/video_reels"
            start_payload = {
                "upload_phase": "start",
                "access_token": self.page_access_token
            }

            start_res = requests.post(start_url, data=start_payload, timeout=30)
            start_data = start_res.json()

            if "video_id" not in start_data or "upload_url" not in start_data:
                logger.error(f"❌ Facebook Reel start phase failed: {start_data}")
                return {"status": "failed", "error": start_data}

            video_id = start_data["video_id"]
            upload_url = start_data["upload_url"]
            file_size = video_path.stat().st_size

            # Phase 2: Binary Transfer
            logger.info(f"⏳ Transferring binary ({file_size / (1024*1024):.2f} MB) to Facebook Reels...")
            headers = {
                "Authorization": f"OAuth {self.page_access_token}",
                "offset": "0",
                "file_size": str(file_size),
                "Content-Type": "application/octet-stream"
            }

            with open(video_path, "rb") as vf:
                transfer_res = requests.post(upload_url, headers=headers, data=vf, timeout=120)

            if transfer_res.status_code not in (200, 201):
                logger.error(f"❌ Facebook Reel binary transfer failed ({transfer_res.status_code}): {transfer_res.text}")
                return {"status": "failed", "error": transfer_res.text}

            # Phase 3: Finalize & Publish
            logger.info("⏳ Finalizing and publishing Facebook Reel...")
            finish_payload = {
                "upload_phase": "finish",
                "access_token": self.page_access_token,
                "video_id": video_id,
                "video_state": "PUBLISHED",
                "description": description
            }

            finish_res = requests.post(start_url, data=finish_payload, timeout=30)
            finish_data = finish_res.json()

            if not finish_data.get("success", False):
                logger.error(f"❌ Facebook Reel finish phase failed: {finish_data}")
                return {"status": "failed", "error": finish_data}

            logger.info(f"🎉 Facebook Reel published successfully! Video ID: {video_id}")
            return {
                "status": "success",
                "platform": "facebook",
                "video_id": video_id,
                "url": f"https://www.facebook.com/reel/{video_id}"
            }

        except Exception as e:
            logger.error(f"❌ Facebook upload error: {e}")
            return {"status": "failed", "error": str(e)}
