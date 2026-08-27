"""
Google Drive 5TB Vault Integration & Lister.
Directly uses existing authorized token from cosmic_matrix_bot without browser login.
"""

import os
import sys
import pickle
import base64
from pathlib import Path
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Enforce UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent

def get_gdrive_service():
    """Loads and auto-refreshes Google Drive OAuth credentials."""
    token_candidates = [
        Path(r"D:\WORKING\AUTOPILOT_BOTS\cosmic_matrix_bot\gdrive_token.pickle"),
        BASE_DIR / "gdrive_token.pickle"
    ]
    token_path = next((p for p in token_candidates if p.exists()), None)

    if not token_path:
        raise FileNotFoundError("gdrive_token.pickle not found!")

    with open(token_path, "rb") as f:
        creds = pickle.load(f)

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(token_path, "wb") as f:
            pickle.dump(creds, f)

    return build("drive", "v3", credentials=creds), token_path

def main():
    print("=" * 75)
    print("☁️ 5TB GOOGLE DRIVE VAULT CONNECTION TEST")
    print("=" * 75)

    service, token_path = get_gdrive_service()
    print(f"✅ Google Drive Authorized Token: {token_path}")

    # Query items
    results = service.files().list(
        pageSize=15,
        fields="files(id, name, mimeType, size)",
        q="trashed = false"
    ).execute()

    items = results.get("files", [])
    print(f"\n📁 Total Items Found in 5TB Drive: {len(items)}")
    print("-" * 75)
    for i, item in enumerate(items, 1):
        size_mb = int(item.get("size", 0)) / (1024 * 1024) if item.get("size") else 0
        mime = item.get("mimeType", "")
        kind = "FOLDER" if "folder" in mime else "FILE"
        print(f"{i:2d}. [{kind:6s}] {item['name'][:45]:<45} | Size: {size_mb:6.2f} MB | ID: {item['id']}")

    print("-" * 75)

    # Export Base64 for GitHub Secrets
    with open(token_path, "rb") as f:
        gdrive_b64 = base64.b64encode(f.read()).decode("utf-8")

    print("\n📋 GITHUB REPOSITORY SECRET FOR 24/7 GDRIVE CLOUD ACCESS:")
    print("=" * 75)
    print("Secret Name: GDRIVE_TOKEN_PICKLE_B64")
    print(f"Value Length: {len(gdrive_b64)} characters")
    print("=" * 75)

if __name__ == "__main__":
    main()
