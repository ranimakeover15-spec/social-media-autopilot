"""
Export Base64 encoded strings of tokens for GitHub Secrets.
"""

import sys
import base64
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent

def export_secrets():
    yt_token = BASE_DIR / "token.pickle"
    gd_token = BASE_DIR / "gdrive_token.pickle"
    ig_session = BASE_DIR / "instagram_session.json"

    print("=" * 80)
    print("GITHUB SECRETS BASE64 STRINGS GENERATED:")
    print("=" * 80)

    if yt_token.exists():
        b64_yt = base64.b64encode(yt_token.read_bytes()).decode("utf-8")
        print("\n--- TOKEN_PICKLE_BASE64 ---")
        print(b64_yt[:60] + "..." + b64_yt[-60:])
        (BASE_DIR / "temp" / "TOKEN_PICKLE_BASE64.txt").write_text(b64_yt, encoding="utf-8")

    if gd_token.exists():
        b64_gd = base64.b64encode(gd_token.read_bytes()).decode("utf-8")
        print("\n--- GDRIVE_TOKEN_BASE64 ---")
        print(b64_gd[:60] + "..." + b64_gd[-60:])
        (BASE_DIR / "temp" / "GDRIVE_TOKEN_BASE64.txt").write_text(b64_gd, encoding="utf-8")

    if ig_session.exists():
        raw_ig = ig_session.read_text(encoding="utf-8")
        print("\n--- INSTAGRAM_SESSION ---")
        print(raw_ig[:60] + "..." + raw_ig[-60:])
        (BASE_DIR / "temp" / "INSTAGRAM_SESSION.txt").write_text(raw_ig, encoding="utf-8")

    print("\n" + "=" * 80)
    print("All Base64 secrets saved to temp/ folder!")
    print("=" * 80)

if __name__ == "__main__":
    export_secrets()
