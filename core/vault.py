"""
Content Vault Ingest Manager.
Discovers and retrieves video files from local directory or 5TB Google Drive Cloud Vault.
Directly uses authorized OAuth token without requiring browser login.
"""

import os
import io
import pickle
import base64
from pathlib import Path
from typing import List, Optional
from core.logger import logger
from core.config import config

SUPPORTED_EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v"}

class ContentVault:
    def __init__(self):
        self.vault_type = config.vault_type.lower()
        self.local_path = config.local_vault_path
        self._ensure_local_vault()

    def _ensure_local_vault(self) -> None:
        """Creates local content vault if missing."""
        if not self.local_path.exists():
            self.local_path.mkdir(parents=True, exist_ok=True)

    def scan_local_videos(self) -> List[Path]:
        """Scans the local vault directory for video files."""
        if not self.local_path.exists():
            return []
        
        videos = [
            p for p in self.local_path.iterdir()
            if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
        ]
        videos.sort(key=lambda x: x.name)
        logger.info(f"📂 Local Content Vault scanned: {len(videos)} video(s) found in '{self.local_path}'.")
        return videos

    def _get_gdrive_service(self):
        """Builds and auto-refreshes Google Drive Service using existing authorized token."""
        from googleapiclient.discovery import build
        from google.auth.transport.requests import Request

        token_candidates = [
            Path(r"D:\WORKING\AUTOPILOT_BOTS\cosmic_matrix_bot\gdrive_token.pickle"),
            config.base_dir / "gdrive_token.pickle"
        ]

        # Check restored cloud token first
        restored = config.restore_secrets_to_files()
        if "gdrive_token_pickle" in restored:
            token_candidates.insert(0, Path(restored["gdrive_token_pickle"]))

        token_file = next((p for p in token_candidates if p.exists()), None)
        if not token_file:
            return None

        with open(token_file, "rb") as f:
            creds = pickle.load(f)

        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(token_file, "wb") as f:
                pickle.dump(creds, f)

        return build("drive", "v3", credentials=creds)

    def download_from_gdrive(self, max_files: int = 20) -> List[Path]:
        """
        Fetches pending videos from 5TB Google Drive without browser login.
        """
        try:
            from googleapiclient.http import MediaIoBaseDownload

            service = self._get_gdrive_service()
            if not service:
                logger.warning("Google Drive token not found. Falling back to local vault.")
                return self.scan_local_videos()

            logger.info("☁️ Querying 5TB Google Drive Cloud Vault for video files...")

            # Query video files in Drive
            query = "trashed = false and (mimeType contains 'video/' or name contains '.mp4' or name contains '.mov')"
            if config.gdrive_folder_id:
                query += f" and '{config.gdrive_folder_id}' in parents"

            results = service.files().list(
                q=query,
                pageSize=max_files,
                fields="files(id, name, mimeType, size)",
                orderBy="name"
            ).execute()

            items = results.get("files", [])
            logger.info(f"☁️ 5TB Drive: {len(items)} video file(s) available in queue.")

            downloaded_paths = []
            for item in items:
                file_id = item["id"]
                file_name = item["name"]
                if not any(file_name.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                    file_name += ".mp4"

                dest_file = self.local_path / file_name
                if not dest_file.exists():
                    logger.info(f"⬇️ Downloading: '{file_name}' ({int(item.get('size', 0))/(1024*1024):.2f} MB)...")
                    request = service.files().get_media(fileId=file_id)
                    with open(dest_file, "wb") as fh:
                        downloader = MediaIoBaseDownload(fh, request, chunksize=1024*1024*5)
                        done = False
                        while not done:
                            status, done = downloader.next_chunk()
                    logger.info(f"✅ Download complete: {file_name}")

                downloaded_paths.append(dest_file)

            return downloaded_paths if downloaded_paths else self.scan_local_videos()

        except Exception as e:
            logger.error(f"⚠️ Google Drive download error: {e}. Defaulting to local vault.")
            return self.scan_local_videos()

    def get_all_available_videos(self) -> List[Path]:
        """Unified discovery method."""
        if self.vault_type == "gdrive":
            return self.download_from_gdrive()
        local = self.scan_local_videos()
        if not local:
            # Auto-fallback to Drive if local vault is empty
            return self.download_from_gdrive()
        return local
