"""
Helper script to authenticate YouTube Data API v3 locally once,
generate token.pickle, and output Base64-encoded secrets for GitHub Actions.
Guaranteed 100% Chrome Launch via PowerShell Start-Process.
"""

import os
import sys
import base64
import pickle
import subprocess
import threading
import time
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

# Enforce UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube"
]

BASE_DIR = Path(__file__).resolve().parent.parent

def find_client_secrets() -> Path:
    """Finds client_secrets.json in project dir or current dir."""
    target = BASE_DIR / "client_secrets.json"
    if target.exists():
        return target
    cwd_target = Path.cwd() / "client_secrets.json"
    if cwd_target.exists():
        return cwd_target
    return None

def force_launch_chrome(url: str):
    """Launches Google Chrome explicitly via Windows PowerShell Start-Process."""
    time.sleep(1) # Wait for local server to be listening
    print("\n🚀 Launching Google Chrome directly...")
    try:
        # PowerShell Start-Process chrome
        ps_cmd = f"Start-Process chrome -ArgumentList '{url}'"
        subprocess.Popen(["powershell", "-NoProfile", "-Command", ps_cmd])
    except Exception as e:
        print(f"Direct Chrome launch error: {e}")

def main():
    print("=" * 75)
    print("🔑 YouTube OAuth 2.0 Token Generator (Chrome Guaranteed)")
    print("=" * 75)

    client_secrets_path = find_client_secrets()

    if not client_secrets_path or not client_secrets_path.exists():
        print(f"\n❌ Error: 'client_secrets.json' nahi mila: {BASE_DIR}")
        return

    print(f"\n📂 Client Secrets: {client_secrets_path.name}")

    try:
        # Create flow
        flow = InstalledAppFlow.from_client_secrets_file(
            str(client_secrets_path),
            SCOPES,
            redirect_uri="http://localhost:8080/"
        )

        auth_url, _ = flow.authorization_url(
            access_type="offline",
            prompt="consent"
        )

        print("\n" + "=" * 75)
        print("🔗 GOOGLE CHROME LOGIN LINK (AGAR CHROME AUTO NA KHULE TO YE PASTE KAREIN):")
        print("=" * 75)
        print(auth_url)
        print("=" * 75 + "\n")

        # Launch Chrome via PowerShell in background thread
        threading.Thread(target=force_launch_chrome, args=(auth_url,), daemon=True).start()

        # Listen on localhost:8080 without letting Python trigger Edge
        # We manually fetch the redirect code without library state collision
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        import urllib.parse

        auth_code = None

        class QuietWSGIRequestHandler(WSGIRequestHandler):
            def log_message(self, format, *args):
                pass # suppress request noise

        def wsgi_app(environ, start_response):
            nonlocal auth_code
            query = urllib.parse.parse_qs(environ.get("QUERY_STRING", ""))
            if "code" in query:
                auth_code = query["code"][0]
                start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
                return [b"""
                <html>
                <body style="font-family: Arial; text-align: center; padding-top: 50px; background: #121212; color: #fff;">
                    <h1 style="color: #4CAF50;">&#10004; Login Successful!</h1>
                    <p style="font-size: 18px;">YouTube Authentication complete ho gaya hai. Aap is tab ko band kar sakte hain.</p>
                </body>
                </html>
                """]
            start_response("400 Bad Request", [("Content-Type", "text/plain")])
            return [b"Authentication error"]

        httpd = make_server("localhost", 8080, wsgi_app, handler_class=QuietWSGIRequestHandler)
        print("⏳ Chrome me login complete hone ka intezar kiya ja raha hai...")

        while auth_code is None:
            httpd.handle_request()

        print("✅ Auth code successfully receive ho gaya! Token generate kiya ja raha hai...")
        flow.fetch_token(code=auth_code)
        creds = flow.credentials

    except Exception as e:
        print(f"\n❌ Login Error: {e}")
        return

    pickle_path = BASE_DIR / "token.pickle"
    with open(pickle_path, "wb") as token_file:
        pickle.dump(creds, token_file)

    print(f"\n✅ Token successfully save ho gaya: {pickle_path}")

    # Base64 encodings for GitHub Actions Secrets
    with open(pickle_path, "rb") as f:
        token_b64 = base64.b64encode(f.read()).decode("utf-8")

    with open(client_secrets_path, "rb") as f:
        secrets_b64 = base64.b64encode(f.read()).decode("utf-8")

    # Write to text file for easy copy-pasting
    logs_dir = BASE_DIR / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    secrets_txt_path = logs_dir / "YOUTUBE_SECRETS_FOR_GITHUB.txt"

    file_content = f"""======================================================================
📋 GITHUB REPOSITORY SECRETS (YOUTUBE DATA API)
======================================================================

Secret Name 1:
YOUTUBE_TOKEN_PICKLE_B64

Value (Copy everything below):
{token_b64}


======================================================================
Secret Name 2:
YOUTUBE_CLIENT_SECRETS_B64

Value (Copy everything below):
{secrets_b64}
======================================================================
"""
    secrets_txt_path.write_text(file_content, encoding="utf-8")

    print("\n" + "=" * 75)
    print("📋 IN 2 SECRETS KO GITHUB REPOSITORY SECRETS MEN ADD KAREIN:")
    print("=" * 75)
    print(f"📁 Ye secrets Notepad me bhi save ho gaye hain:\n   👉 {secrets_txt_path}")
    print("=" * 75)
    print("\n1. Secret Name: YOUTUBE_TOKEN_PICKLE_B64")
    print("-" * 60)
    print(token_b64)
    print("-" * 60)

    print("\n2. Secret Name: YOUTUBE_CLIENT_SECRETS_B64")
    print("-" * 60)
    print(secrets_b64)
    print("-" * 60)
    print("\n🎉 Done! Dono secrets ready hain.")

if __name__ == "__main__":
    main()
