"""
Instagram Reels Uploader.
Uses official Meta Instagram Graph API v19.0 / v20.0 with container lifecycle management:
1. Initialize container (upload_type=resumable)
2. Stream binary payload directly to Graph API / rupload_igvideo
3. Poll container processing status until FINISHED
4. Publish media via media_publish endpoint
"""

import os
import time
import requests
from pathlib import Path
from typing import Dict, Any, Optional

from core.logger import logger
from core.config import config

GRAPH_API_VERSION = "v19.0"
GRAPH_BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

class InstagramUploader:
    def __init__(self):
        self.account_id = config.instagram_account_id
        self.access_token = config.instagram_access_token
        self.is_configured = bool(self.account_id and self.access_token)

        if not self.is_configured:
            logger.warning("⚠️ Instagram credentials (INSTAGRAM_ACCOUNT_ID or INSTAGRAM_ACCESS_TOKEN) not set.")
        else:
            logger.info("✅ Instagram Graph API client configured.")

    def upload_reel(
        self,
        video_path: Path,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Uploads video to Instagram Reels via direct resumable upload or public URL.
        """
        if not self.is_configured:
            logger.error("Instagram client not configured. Skipping upload.")
            return {"status": "skipped", "error": "Not configured"}

        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        caption = metadata.get("instagram", {}).get("caption", metadata.get("hashtags_string", ""))
        logger.info(f"📸 Starting Instagram Reel upload ({video_path.name})...")

        try:
            # Step 1: Initialize Container
            init_url = f"{GRAPH_BASE_URL}/{self.account_id}/media"
            init_params = {
                "media_type": "REELS",
                "caption": caption,
                "access_token": self.access_token,
                "upload_type": "resumable"
            }

            init_res = requests.post(init_url, data=init_params, timeout=30)
            init_data = init_res.json()

            if "id" not in init_data:
                logger.error(f"❌ Failed to initialize Instagram Reel container: {init_data}")
                return {"status": "failed", "error": init_data}

            container_id = init_data["id"]
            upload_url = init_data.get("uri")

            # Step 2: Upload Video Binary
            file_size = video_path.stat().st_size
            logger.info(f"⏳ Uploading binary stream ({file_size / (1024*1024):.2f} MB) to Instagram...")

            headers = {
                "Authorization": f"OAuth {self.access_token}",
                "offset": "0",
                "file_size": str(file_size),
                "Content-Type": "application/octet-stream"
            }

            with open(video_path, "rb") as vf:
                upload_res = requests.post(upload_url, headers=headers, data=vf, timeout=120)

            if upload_res.status_code not in (200, 201):
                logger.error(f"❌ Binary upload to Instagram failed ({upload_res.status_code}): {upload_res.text}")
                return {"status": "failed", "error": upload_res.text}

            # Step 3: Poll Container Processing Status
            logger.info(f"⏳ Polling Instagram container {container_id} status...")
            status_url = f"{GRAPH_BASE_URL}/{container_id}"
            status_params = {
                "fields": "status_code,status",
                "access_token": self.access_token
            }

            max_polls = 30
            poll_interval = 5
            ready = False

            for attempt in range(max_polls):
                time.sleep(poll_interval)
                s_res = requests.get(status_url, params=status_params, timeout=15)
                s_data = s_res.json()
                status_code = s_data.get("status_code", "").upper()

                logger.info(f"⏳ Container status (attempt {attempt + 1}/{max_polls}): {status_code}")

                if status_code == "FINISHED":
                    ready = True
                    break
                elif status_code in ("ERROR", "EXPIRED"):
                    logger.error(f"❌ Instagram processing failed with status {status_code}: {s_data}")
                    return {"status": "failed", "error": s_data}

            if not ready:
                return {"status": "failed", "error": "Container processing timeout"}

            # Step 4: Publish Reel
            publish_url = f"{GRAPH_BASE_URL}/{self.account_id}/media_publish"
            publish_params = {
                "creation_id": container_id,
                "access_token": self.access_token
            }

            pub_res = requests.post(publish_url, data=publish_params, timeout=30)
            pub_data = pub_res.json()

            if "id" not in pub_data:
                logger.error(f"❌ Instagram Reel publish failed: {pub_data}")
                return {"status": "failed", "error": pub_data}

            media_id = pub_data["id"]
            logger.info(f"🎉 Instagram Reel published successfully! Media ID: {media_id}")

            return {
                "status": "success",
                "platform": "instagram",
                "media_id": media_id,
                "container_id": container_id
            }

        except Exception as e:
            logger.error(f"❌ Instagram upload error: {e}")
            return {"status": "failed", "error": str(e)}
