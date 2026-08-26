"""
Deduplication manager for tracking posted videos and maintaining cycle states.
Ensures zero duplicate uploads until the entire vault library has completed a cycle.
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from core.logger import logger
from core.config import config

class Deduplicator:
    def __init__(self, log_path: Optional[Path] = None):
        self.log_path = log_path or config.used_reels_log
        self._ensure_log_file()

    def _ensure_log_file(self) -> None:
        """Initializes the json log file if it does not exist."""
        if not self.log_path.parent.exists():
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            initial_data = {
                "cycle": 1,
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "history": [],
                "current_cycle_posted_files": []
            }
            self._save(initial_data)

    def _load(self) -> Dict[str, Any]:
        """Loads and returns the json tracking file."""
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading {self.log_path}: {e}. Initializing fresh state.")
            return {
                "cycle": 1,
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "history": [],
                "current_cycle_posted_files": []
            }

    def _save(self, data: Dict[str, Any]) -> None:
        """Atomically saves tracking state to disk."""
        data["last_updated"] = datetime.now(timezone.utc).isoformat()
        temp_path = self.log_path.with_suffix(".tmp")
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        temp_path.replace(self.log_path)

    @staticmethod
    def calculate_file_hash(file_path: Path) -> str:
        """Computes SHA256 checksum of a file for exact deduplication."""
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def filter_available_videos(self, all_videos: List[Path]) -> List[Path]:
        """
        Filters out videos that have already been posted in the current cycle.
        If all available videos have been posted, bumps the cycle count and resets.
        """
        data = self._load()
        current_posted = set(data.get("current_cycle_posted_files", []))
        
        # Check by filename or base identifier
        available = [v for v in all_videos if v.name not in current_posted]

        if not available and all_videos:
            logger.info("🎉 All vault videos have been posted! Rolling over to next cycle...")
            data["cycle"] = data.get("cycle", 1) + 1
            data["current_cycle_posted_files"] = []
            self._save(data)
            return all_videos

        return available

    def record_upload(
        self,
        file_name: str,
        file_hash: str,
        slot_name: str,
        platform_statuses: Dict[str, Any],
        metadata: Dict[str, Any]
    ) -> None:
        """Records a successful upload into history and current cycle list."""
        data = self._load()
        
        record = {
            "cycle": data.get("cycle", 1),
            "file_name": file_name,
            "sha256": file_hash,
            "slot": slot_name,
            "posted_at": datetime.now(timezone.utc).isoformat(),
            "platforms": platform_statuses,
            "metadata": metadata
        }

        data.setdefault("history", []).append(record)
        
        current_posted = data.setdefault("current_cycle_posted_files", [])
        if file_name not in current_posted:
            current_posted.append(file_name)

        self._save(data)
        logger.info(f"💾 Logged '{file_name}' to {self.log_path} (Cycle {data['cycle']})")
