import urllib.request
import re
import sys

# Enforce UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

url = "https://www.youtube.com/shorts/LsJvYUAE0B4"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode("utf-8")
        title_match = re.search(r"<title>(.*?)</title>", html)
        if title_match:
            print("TITLE:", title_match.group(1))

        # Search for channel name or description
        og_desc = re.search(r'<meta property="og:description" content="(.*?)"', html)
        if og_desc:
            print("OG DESC:", og_desc.group(1))

        og_title = re.search(r'<meta property="og:title" content="(.*?)"', html)
        if og_title:
            print("OG TITLE:", og_title.group(1))
except Exception as e:
    print("Error:", e)
