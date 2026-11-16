"""Tell Bing (and other IndexNow engines) about every page in the sitemap.

Run after the site is live on its domain:  python3 indexnow.py
"""
import json, re, urllib.request
from build import SITE, INDEXNOW_KEY, OUT

urls = re.findall(r"<loc>([^<]+)</loc>", (OUT / "sitemap.xml").read_text())
host = SITE["domain"].split("//", 1)[1]
body = json.dumps({"host": host, "key": INDEXNOW_KEY, "keyLocation": f"{SITE['domain']}/{INDEXNOW_KEY}.txt",
                   "urlList": urls[:10000]}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print("IndexNow:", r.status, f"({len(urls)} URLs)")
