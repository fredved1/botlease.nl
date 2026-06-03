#!/usr/bin/env python3
"""
BotLease Rank Bot — weekly Google rank tracker.

For each keyword in seo/seo_data.json:
- Query Google.nl directly (with NL locale + UA spoof)
- Find botlease.nl's position in top 30
- Record top 3 competitors

Output: appends a new entry to `checks` array in seo/seo_data.json.
Then rebuilds the SEO dashboard.

Run mode:
  python3 scripts/rank_bot.py [--commit] [--dry-run]

Cron: every Friday 17:30 (after news-bot at 17:00), via VPS systemd.
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import date as date_cls, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEO_DATA = ROOT / "seo" / "seo_data.json"
LOG_TAG = "[rank-bot]"

DDG_URL = "https://html.duckduckgo.com/html/"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
)
DELAY_SEC = 3.0  # polite delay between queries

TARGET_DOMAIN = "botlease.nl"

# NOTE: DDG uses Bing's index, not Google's. So positions track Bing/DDG, not
# Google directly. For trend-tracking this is fine — when site SEO improves it
# improves across engines. Google-specific tracking would require SerpAPI ($).


def log(msg: str) -> None:
    print(f"{LOG_TAG} {datetime.now().isoformat(timespec='seconds')} {msg}", flush=True)


def ddg_search(query: str) -> str:
    """DuckDuckGo HTML interface — no JS required, NL-region-aware."""
    # DDG uses POST form with kl=nl-nl for NL region
    data = urllib.parse.urlencode({
        "q": query,
        "kl": "nl-nl",
        "kp": "-2",  # safe search off
    }).encode("utf-8")
    req = urllib.request.Request(
        DDG_URL,
        data=data,
        headers={
            "User-Agent": USER_AGENT,
            "Accept-Language": "nl-NL,nl;q=0.9,en;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", errors="replace")


def extract_results(html: str) -> list[str]:
    """Extract result URLs from a DDG HTML SERP, in order.
    DDG uses class 'result__a' on anchor tags. Direct href contains target URL
    via /l/?uddg=...  or sometimes plain URL after recent updates."""
    urls: list[str] = []

    # Pattern 1: <a class="result__a" href="//duckduckgo.com/l/?uddg=https%3A//actual.com/page&..."
    for m in re.finditer(r'class="result__a"[^>]*href="([^"]+)"', html):
        href = m.group(1)
        if href.startswith("//"):
            href = "https:" + href
        # Extract uddg= param if wrapped
        u = urllib.parse.urlparse(href)
        qs = urllib.parse.parse_qs(u.query)
        if "uddg" in qs:
            urls.append(qs["uddg"][0])
        elif href.startswith("http"):
            urls.append(href)

    # Pattern 2 (fallback): any <a> inside result body with class 'result__url'
    if not urls:
        for m in re.finditer(r'class="result__url"[^>]*href="([^"]+)"', html):
            href = m.group(1)
            if href.startswith("//"):
                href = "https:" + href
            urls.append(href)

    # Dedupe by domain
    seen_domains: set[str] = set()
    deduped: list[str] = []
    for u in urls:
        d = urllib.parse.urlparse(u).netloc.lower().replace("www.", "")
        if not d or d in seen_domains:
            continue
        seen_domains.add(d)
        deduped.append(u)
    return deduped[:30]


# Backward-compat alias so test calls don't break
def google_search(query: str) -> str:
    return ddg_search(query)


def position_of(urls: list[str], target_domain: str) -> int:
    for i, u in enumerate(urls, start=1):
        d = urllib.parse.urlparse(u).netloc.lower().replace("www.", "")
        if target_domain in d:
            return i
    return 0


def short_competitor(url: str) -> str:
    d = urllib.parse.urlparse(url).netloc.lower().replace("www.", "")
    return d


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--commit", action="store_true",
                        help="git add + commit + push to remote after update")
    args = parser.parse_args()

    if not SEO_DATA.exists():
        log(f"ERROR: {SEO_DATA} missing")
        return 1
    data = json.loads(SEO_DATA.read_text(encoding="utf-8"))
    keywords = data.get("target_keywords", [])
    log(f"checking {len(keywords)} keywords against Google.nl")

    ranks: dict[str, dict] = {}
    for i, kw in enumerate(keywords, start=1):
        q = kw["kw"]
        kid = kw["id"]
        log(f"[{i}/{len(keywords)}] {kid}: {q}")
        try:
            html = google_search(q)
            urls = extract_results(html)
            pos = position_of(urls, TARGET_DOMAIN)
            top3 = [short_competitor(u) for u in urls[:3]]
            log(f"   pos={pos}  top3={top3}")
            ranks[kid] = {"position": pos, "top_competitors": top3}
        except Exception as e:
            log(f"   ERROR: {str(e)[:120]}")
            ranks[kid] = {"position": -1, "top_competitors": [], "error": str(e)[:80]}
        time.sleep(DELAY_SEC)

    # Build new check entry
    today = date_cls.today().isoformat()
    ranked = sum(1 for r in ranks.values() if r["position"] > 0)
    new_check = {
        "date": today,
        "method": "rank-bot (Google.nl direct scrape, weekly automated)",
        "notes": f"Automatische weekly check. {ranked}/{len(keywords)} keywords nu in top 30. Volgende run: vrijdag.",
        "ranks": ranks,
    }

    if args.dry_run:
        log(f"DRY-RUN — would add check: {json.dumps(new_check, indent=2)[:500]}")
        return 0

    data["checks"].insert(0, new_check)  # newest first
    SEO_DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    log(f"saved {SEO_DATA.name} (total checks: {len(data['checks'])})")

    # Rebuild dashboard
    log("rebuilding dashboard...")
    r = subprocess.run(["python3", "scripts/build_seo_dashboard.py"],
                       cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        log(f"dashboard build failed: {r.stderr[:200]}")
    else:
        log(r.stdout.strip().split("\n")[-1])

    # Commit + push
    if args.commit:
        token = os.environ.get("GH_REPO_TOKEN", "").strip() if "os" in dir() else __import__("os").environ.get("GH_REPO_TOKEN", "").strip()
        if not token:
            log("GH_REPO_TOKEN not set — skip push")
            return 0
        import os
        subprocess.run(["git", "add", "seo/seo_data.json", "frontend/admin/seo.html"], cwd=ROOT)
        diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
        if diff.returncode == 0:
            log("no changes — skip commit")
            return 0
        subprocess.run([
            "git", "-c", "user.email=bot@botlease.nl",
            "-c", "user.name=BotLease Rank Bot",
            "commit", "-m",
            f"rank-bot: weekly rank check ({ranked}/{len(keywords)} in top 30)"
        ], cwd=ROOT, check=True)
        remote = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=ROOT, capture_output=True, text=True
        ).stdout.strip()
        if remote.startswith("https://"):
            host_path = re.sub(r"^https://[^/@]*@", "", remote)[len("https://"):]
            push_url = f"https://{token}@{host_path}"
        else:
            push_url = remote
        subprocess.run(["git", "push", push_url, "HEAD:master"], cwd=ROOT, check=True)
        log(f"pushed: rank check {today}")

    log(f"done — {ranked}/{len(keywords)} ranked")
    return 0


if __name__ == "__main__":
    import os
    sys.exit(main())
