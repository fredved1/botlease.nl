#!/usr/bin/env python3
"""
IndexNow ping — notify Bing/Yandex/others over wijzigingen op botlease.nl.

Geen account / login nodig. Werkt via een publieke key file op de site root.
Bing deelt de IndexNow-data met andere search engines, dus dit triggert
indirect ook snellere recrawl elders.

Usage:
  python3 scripts/indexnow_ping.py                # ping alle sitemap-URLs
  python3 scripts/indexnow_ping.py URL [URL ...]  # ping specifieke URLs
"""
from __future__ import annotations
import json
import re
import sys
import urllib.request as ur
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEY = "fa7f90fa9c554aa9b26424bdba749f9c"
HOST = "botlease.nl"
SITEMAP = ROOT / "frontend" / "sitemap.xml"


def urls_from_sitemap():
    if not SITEMAP.exists():
        return []
    txt = SITEMAP.read_text()
    return re.findall(r"<loc>([^<]+)</loc>", txt)


def ping(urls):
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": f"https://{HOST}/{KEY}.txt",
        "urlList": urls,
    }
    body = json.dumps(payload).encode("utf-8")
    req = ur.Request(
        "https://api.indexnow.org/IndexNow",
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "BotLease-IndexNow/1.0"},
        method="POST",
    )
    try:
        with ur.urlopen(req, timeout=10) as resp:
            return resp.status, resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return None, str(e)


def main():
    urls = sys.argv[1:] or urls_from_sitemap()
    if not urls:
        print("❌ Geen URLs gevonden — bouw eerst sitemap (run build_news.py).")
        sys.exit(1)
    # API limiet 10.000 URLs per call — wij zitten ver onder.
    print(f"📡 IndexNow ping voor {len(urls)} URLs naar Bing/Yandex...")
    status, body = ping(urls)
    if status == 200 or status == 202:
        print(f"✅ IndexNow accepted ({status}). Bing/Yandex zullen binnen 24-48u opnieuw crawlen.")
    elif status is None:
        print(f"❌ Network/connection error: {body}")
    else:
        print(f"⚠ HTTP {status}: {body[:200]}")


if __name__ == "__main__":
    main()
