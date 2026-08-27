import urllib.request
import re
import json

url = "https://www.youtube.com/watch?v=LsJvYUAE0B4"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
try:
    html = urllib.request.urlopen(req).read().decode("utf-8")
    for m in re.finditer(r'"videoDetails":\s*({.*?})\s*,\s*"playerConfig"', html):
        details = json.loads(m.group(1))
        print("VIDEO TITLE:", details.get("title"))
        print("CHANNEL:", details.get("author"))
        print("SHORT DESCRIPTION:", details.get("shortDescription")[:200])
        break
except Exception as e:
    print("Error:", e)
