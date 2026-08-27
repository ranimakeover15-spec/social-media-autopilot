"""
Configuration manager for the Social Media Autopilot.
Loads environment variables, handles base64 decoded secrets, and provides path resolutions.
"""

import os
import base64
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load .env if present
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

class AppConfig(BaseModel):
    # Timezone & Schedule
    timezone: str = Field(default_factory=lambda: os.getenv("TIMEZONE", "Asia/Kolkata"))

    # Content Vault
    vault_type: str = Field(default_factory=lambda: os.getenv("VAULT_TYPE", "local"))
    local_vault_path: Path = Field(
        default_factory=lambda: BASE_DIR / os.getenv("LOCAL_VAULT_PATH", "content_vault")
    )
    gdrive_folder_id: str = Field(default_factory=lambda: os.getenv("GDRIVE_FOLDER_ID", ""))
    gdrive_service_account_b64: str = Field(
        default_factory=lambda: os.getenv("GDRIVE_SERVICE_ACCOUNT_B64", "")
    )
    gdrive_token_pickle_b64: str = Field(
        default_factory=lambda: os.getenv("GDRIVE_TOKEN_PICKLE_B64", "")
    )

    # YouTube Shorts
    youtube_token_pickle_b64: str = Field(
        default_factory=lambda: os.getenv("YOUTUBE_TOKEN_PICKLE_B64", "")
    )
    youtube_client_secrets_b64: str = Field(
        default_factory=lambda: os.getenv("YOUTUBE_CLIENT_SECRETS_B64", "")
    )
    youtube_privacy_status: str = Field(
        default_factory=lambda: os.getenv("YOUTUBE_PRIVACY_STATUS", "public")
    )
    youtube_category_id: str = Field(
        default_factory=lambda: os.getenv("YOUTUBE_CATEGORY_ID", "22")
    )
    youtube_made_for_kids: bool = Field(
        default_factory=lambda: os.getenv("YOUTUBE_MADE_FOR_KIDS", "false").lower() == "true"
    )

    # Instagram Reels
    instagram_account_id: str = Field(
        default_factory=lambda: os.getenv("INSTAGRAM_ACCOUNT_ID", "")
    )
    instagram_access_token: str = Field(
        default_factory=lambda: os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
    )
    public_media_host_url: str = Field(
        default_factory=lambda: os.getenv("PUBLIC_MEDIA_HOST_URL", "")
    )

    # Facebook Reels
    facebook_page_id: str = Field(
        default_factory=lambda: os.getenv("FACEBOOK_PAGE_ID", "")
    )
    facebook_page_access_token: str = Field(
        default_factory=lambda: os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN", "")
    )

    # Transcoder
    target_width: int = Field(default_factory=lambda: int(os.getenv("TARGET_WIDTH", "1080")))
    target_height: int = Field(default_factory=lambda: int(os.getenv("TARGET_HEIGHT", "1920")))
    max_video_duration_sec: int = Field(
        default_factory=lambda: int(os.getenv("MAX_VIDEO_DURATION_SEC", "60"))
    )
    video_codec: str = Field(default_factory=lambda: os.getenv("VIDEO_CODEC", "libx264"))
    pixel_format: str = Field(default_factory=lambda: os.getenv("PIXEL_FORMAT", "yuv420p"))
    audio_codec: str = Field(default_factory=lambda: os.getenv("AUDIO_CODEC", "aac"))
    audio_bitrate: str = Field(default_factory=lambda: os.getenv("AUDIO_BITRATE", "192k"))
    audio_sample_rate: int = Field(
        default_factory=lambda: int(os.getenv("AUDIO_SAMPLE_RATE", "44100"))
    )
    crf: int = Field(default_factory=lambda: int(os.getenv("CRF", "20")))
    preset: str = Field(default_factory=lambda: os.getenv("PRESET", "fast"))

    # SEO Defaults
    niche_category: str = Field(default_factory=lambda: os.getenv("NICHE_CATEGORY", "motivation"))
    brand_name: str = Field(default_factory=lambda: os.getenv("BRAND_NAME", "AutoClips"))
    call_to_action: str = Field(
        default_factory=lambda: os.getenv(
            "CALL_TO_ACTION", "Follow for daily high-voltage motivation! 🚀🔥"
        )
    )

    # Internal paths
    base_dir: Path = BASE_DIR
    temp_dir: Path = BASE_DIR / "temp"
    logs_dir: Path = BASE_DIR / "logs"
    used_reels_log: Path = BASE_DIR / "logs" / "used_reels.json"

    def restore_secrets_to_files(self) -> dict:
        """Restores base64 encoded secrets to temporary runtime files if necessary."""
        restored = {}
        self.temp_dir.mkdir(parents=True, exist_ok=True)

        if self.youtube_token_pickle_b64:
            pickle_path = self.temp_dir / "token.pickle"
            try:
                pickle_path.write_bytes(base64.b64decode(self.youtube_token_pickle_b64))
                restored["youtube_token_pickle"] = str(pickle_path)
            except Exception as e:
                print(f"Failed to decode YOUTUBE_TOKEN_PICKLE_B64: {e}")

        if self.youtube_client_secrets_b64:
            secrets_path = self.temp_dir / "client_secrets.json"
            try:
                secrets_path.write_bytes(base64.b64decode(self.youtube_client_secrets_b64))
                restored["youtube_client_secrets"] = str(secrets_path)
            except Exception as e:
                print(f"Failed to decode YOUTUBE_CLIENT_SECRETS_B64: {e}")

        if self.gdrive_token_pickle_b64:
            gdrive_pickle = self.temp_dir / "gdrive_token.pickle"
            try:
                gdrive_pickle.write_bytes(base64.b64decode(self.gdrive_token_pickle_b64))
                restored["gdrive_token_pickle"] = str(gdrive_pickle)
            except Exception as e:
                print(f"Failed to decode GDRIVE_TOKEN_PICKLE_B64: {e}")

        if self.gdrive_service_account_b64:
            sa_path = self.temp_dir / "service_account.json"
            try:
                sa_path.write_bytes(base64.b64decode(self.gdrive_service_account_b64))
                restored["gdrive_service_account"] = str(sa_path)
            except Exception as e:
                print(f"Failed to decode GDRIVE_SERVICE_ACCOUNT_B64: {e}")

        return restored

# Instantiate global config
config = AppConfig()
