"""
👑 RANI MAKEOVER — 100% STANDALONE CLOUD CREDENTIALS VAULT
Ensures that GitHub Actions Linux VM NEVER fails with missing secret files.
If token files don't exist on disk, it automatically restores them from the internal Base64 vault.
"""

import os
import sys
import base64
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def ensure_cloud_credentials():
    token_pickle = BASE_DIR / "token.pickle"
    gdrive_token = BASE_DIR / "gdrive_token.pickle"
    ig_session = BASE_DIR / "instagram_session.json"

    # YouTube Token Restore
    if not token_pickle.exists() or token_pickle.stat().st_size == 0:
        # Check env or fallback
        b64_yt = os.getenv("TOKEN_PICKLE_BASE64")
        if not b64_yt:
            # Fallback from .env
            env_file = BASE_DIR / ".env"
            if env_file.exists():
                for line in env_file.read_text(encoding="utf-8").splitlines():
                    if line.startswith("YOUTUBE_TOKEN_PICKLE_B64="):
                        b64_yt = line.split("=", 1)[1].strip()
                        break
        if b64_yt:
            try:
                token_pickle.write_bytes(base64.b64decode(b64_yt))
                print("✅ YouTube token restored from cloud vault.")
            except Exception as e:
                print(f"YouTube restore note: {e}")

    # GDrive Token Restore
    if not gdrive_token.exists() or gdrive_token.stat().st_size == 0:
        b64_gd = os.getenv("GDRIVE_TOKEN_BASE64")
        if not b64_gd:
            temp_gd = BASE_DIR / "temp" / "GDRIVE_TOKEN_BASE64.txt"
            if temp_gd.exists():
                b64_gd = temp_gd.read_text(encoding="utf-8").strip()
        if b64_gd:
            try:
                gdrive_token.write_bytes(base64.b64decode(b64_gd))
                print("✅ Google Drive token restored from cloud vault.")
            except Exception as e:
                print(f"GDrive restore note: {e}")

    # Instagram Session Restore
    if not ig_session.exists() or ig_session.stat().st_size == 0:
        raw_ig = os.getenv("INSTAGRAM_SESSION")
        if not raw_ig:
            temp_ig = BASE_DIR / "temp" / "INSTAGRAM_SESSION.txt"
            if temp_ig.exists():
                raw_ig = temp_ig.read_text(encoding="utf-8").strip()
        if raw_ig:
            try:
                ig_session.write_text(raw_ig, encoding="utf-8")
                print("✅ Instagram session restored from cloud vault.")
            except Exception as e:
                print(f"Instagram restore note: {e}")

if __name__ == "__main__":
    ensure_cloud_credentials()
