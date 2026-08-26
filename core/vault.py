"""
Content Vault Ingest Manager.
Discovers and retrieves video files from local directory or Google Drive Cloud Vault.
"""

import os
import io
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
            # Create a sample placeholder note
            readme = self.local_path / "README_VAULT.txt"
            if not readme.exists():
                readme.write_text(
                    "Place your raw/source short video files (.mp4, .mov, etc.) here.\n"
                    "The autopilot will transcode, optimize, and upload them sequentially.\n",
                    encoding="utf-8"
                )

    def scan_local_videos(self) -> List[Path]:
        """Scans the local vault directory for video files."""
        if not self.local_path.exists():
            return []
        
        videos = [
            p for p in self.local_path.iterdir()
            if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
        ]
        # Sort by name or creation time for deterministic order
        videos.sort(key=lambda x: x.name)
        logger.info(f"📂 Local Content Vault scanned: {len(videos)} video(s) found in '{self.local_path}'.")
        return videos

    def download_from_gdrive(self) -> List[Path]:
        """
        Downloads pending videos from Google Drive folder if configured.
        Requires google-api-python-client and Service Account credentials.
        """
        if not config.gdrive_folder_id:
            logger.warning("Google Drive folder ID not configured (GDRIVE_FOLDER_ID). Fallback to local.")
            return self.scan_local_videos()

        try:
            from googleapiclient.discovery import build
            from googleapiclient.http import MediaIoBaseDownload
            from google.oauth2 import service_account
            import json

            restored = config.restore_secrets_to_files()
            sa_file = restored.get("gdrive_service_account")

            if not sa_file or not os.path.exists(sa_file):
                logger.warning("No Service Account JSON found for Google Drive. Reading local vault instead.")
                return self.scan_local_videos()

            creds = service_account.Credentials.from_service_account_file(
                sa_file, scopes=["https://www.googleapis.com/auth/drive.readonly"]
            )
            service = build("drive", "v3", credentials=creds)

            # Query video files in folder
            query = f"'{config.gdrive_folder_id}' in parents and trashed = false"
            results = service.files().list(
                q=query,
                pageSize=50,
                fields="files(id, name, mimeType, size)"
            ).execute()
            items = results.get("files", [])

            downloaded_paths = []
            for item in items:
                file_id = item["id"]
                file_name = item["name"]
                if Path(file_name).suffix.lower() not in SUPPORTED_EXTENSIONS:
                    continue

                dest_file = self.local_path / file_name
                if not dest_file.exists():
                    logger.info(f"☁️ Downloading from GDrive: {file_name}...")
                    request = service.files().get_media(fileId=file_id)
                    with open(dest_file, "wb") as fh:
                        downloader = MediaIoBaseDownload(fh, request)
                        done = False
                        while not done:
                            status, done = downloader.next_chunk()
                    logger.info(f"✅ Downloaded: {file_name}")
                downloaded_paths.append(dest_file)

            return downloaded_paths

        except Exception as e:
            logger.error(f"⚠️ Google Drive download error: {e}. Defaulting to local vault.")
            return self.scan_local_videos()

    def get_all_available_videos(self) -> List[Path]:
        """Unified method to fetch all available vault videos."""
        if self.vault_type == "gdrive":
            return self.download_from_gdrive()
        return self.scan_local_videos()
