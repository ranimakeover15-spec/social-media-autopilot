"""
YouTube Shorts Uploader.
Uses YouTube Data API v3 with OAuth 2.0 token auto-refresh and resumable upload protocol.
"""

import os
import pickle
import time
import base64
from pathlib import Path
from typing import Dict, Any, Optional
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from core.logger import logger
from core.config import config

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube"
]

class YouTubeUploader:
    def __init__(self):
        self.service = None
        self._authenticate()

    def _authenticate(self) -> None:
        """Authenticates using stored pickle token or base64 environment secret."""
        creds = None
        restored = config.restore_secrets_to_files()

        # Check local pickle first, then restored pickle
        local_pickle = config.base_dir / "token.pickle"
        pickle_path = local_pickle if local_pickle.exists() else restored.get("youtube_token_pickle")

        if pickle_path and os.path.exists(pickle_path):
            try:
                with open(pickle_path, "rb") as token_file:
                    creds = pickle.load(token_file)
            except Exception as e:
                logger.warning(f"Failed to load credentials from {pickle_path}: {e}")

        # Refresh token if expired
        if creds and creds.expired and creds.refresh_token:
            try:
                logger.info("🔄 Refreshing expired YouTube OAuth token...")
                creds.refresh(Request())
                # Save refreshed token
                if local_pickle.exists() or not pickle_path:
                    with open(local_pickle, "wb") as token_file:
                        pickle.dump(creds, token_file)
                elif pickle_path:
                    with open(pickle_path, "wb") as token_file:
                        pickle.dump(creds, token_file)
                logger.info("✅ YouTube OAuth token refreshed successfully.")
            except Exception as e:
                logger.error(f"❌ Failed to refresh YouTube OAuth token: {e}")
                creds = None

        if not creds or not creds.valid:
            logger.warning("⚠️ No valid YouTube credentials found. Run 'python scripts/generate_youtube_token.py' locally.")
            self.service = None
            return

        self.service = build("youtube", "v3", credentials=creds)
        logger.info("✅ YouTube Data API v3 client initialized.")

    def upload_short(
        self,
        video_path: Path,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Uploads video to YouTube Shorts using resumable upload protocol.
        """
        if not self.service:
            logger.error("YouTube service is not authenticated. Skipping YouTube upload.")
            return {"status": "skipped", "error": "Unauthenticated"}

        if not video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

        yt_meta = metadata.get("youtube", {})
        title = yt_meta.get("title", f"{metadata.get('title', 'Video')} #Shorts")
        description = yt_meta.get("description", metadata.get("hashtags_string", ""))
        tags = yt_meta.get("tags", metadata.get("tags", []))
        category_id = str(yt_meta.get("category_id", config.youtube_category_id))
        privacy_status = yt_meta.get("privacy_status", config.youtube_privacy_status)

        body = {
            "snippet": {
                "title": title[:100], # YouTube title character limit
                "description": description[:5000],
                "tags": tags,
                "categoryId": category_id
            },
            "status": {
                "privacyStatus": privacy_status,
                "selfDeclaredMadeForKids": config.youtube_made_for_kids
            }
        }

        logger.info(f"📤 Uploading to YouTube Shorts: '{title}' [{privacy_status}]...")

        media = MediaFileUpload(
            str(video_path),
            mimetype="video/mp4",
            resumable=True,
            chunksize=1024 * 1024 * 5 # 5MB chunks
        )

        request = self.service.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )

        response = None
        retry = 0
        max_retries = 5

        while response is None:
            try:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    logger.info(f"⏳ YouTube upload progress: {progress}%")
            except Exception as e:
                retry += 1
                if retry > max_retries:
                    logger.error(f"❌ YouTube upload failed after {max_retries} attempts: {e}")
                    return {"status": "failed", "error": str(e)}
                sleep_sec = 2 ** retry
                logger.warning(f"⚠️ YouTube upload error ({e}). Retrying in {sleep_sec}s...")
                time.sleep(sleep_sec)

        video_id = response.get("id")
        video_url = f"https://youtube.com/shorts/{video_id}"
        logger.info(f"🎉 YouTube Short published successfully! URL: {video_url}")

        return {
            "status": "success",
            "platform": "youtube",
            "video_id": video_id,
            "url": video_url,
            "privacy": privacy_status
        }
