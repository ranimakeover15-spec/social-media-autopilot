import urllib.request
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

oembed_url = 'https://www.youtube.com/oembed?url=https://www.youtube.com/shorts/LsJvYUAE0B4&format=json'
req = urllib.request.Request(oembed_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print('TITLE:', data.get('title'))
        print('AUTHOR:', data.get('author_name'))
        print('THUMBNAIL:', data.get('thumbnail_url'))

        # Download thumbnail to inspect visual layout
        thumb_url = data.get('thumbnail_url')
        if thumb_url:
            thumb_path = 'temp/ref_thumbnail.jpg'
            with urllib.request.urlopen(thumb_url) as tr, open(thumb_path, 'wb') as f:
                f.write(tr.read())
            print('Downloaded thumbnail to:', thumb_path)
except Exception as e:
    print('OEmbed error:', e)
