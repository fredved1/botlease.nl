#!/usr/bin/env python3
"""
BotLease Analytics Bot - pulls Umami stats and saves snapshot for the dashboard.

Runs on the VPS where Umami is local (no auth via tunneled internal API).
Writes seo/analytics_snapshot.json which build_seo_dashboard reads.

Cron: same wrapper as news-bot + rank-bot (weekly Friday 17:00).
Also runnable on-demand.

Usage:
  python3 scripts/analytics_bot.py [--commit]
"""
from __future__ import annotations
import argparse
import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT_FILE = ROOT / "seo" / "analytics_snapshot.json"

UMAMI_URL = os.environ.get("UMAMI_URL", "http://127.0.0.1:3001")
UMAMI_USER = os.environ.get("UMAMI_USER", "admin")
UMAMI_PASS = os.environ.get("UMAMI_PASS", "umami")
WEBSITE_ID = os.environ.get("UMAMI_WEBSITE_ID", "185bb2a6-3057-420f-9f3b-babb2776450f")

LOG_TAG = "[analytics-bot]"


def log(msg: str) -> None:
    print(f"{LOG_TAG} {datetime.now().isoformat(timespec='seconds')} {msg}", flush=True)


def umami_login() -> str:
    body = json.dumps({"username": UMAMI_USER, "password": UMAMI_PASS}).encode()
    req = urllib.request.Request(
        f"{UMAMI_URL}/api/auth/login",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())["token"]


def api_get(token: str, path: str, params: dict | None = None) -> dict | list:
    url = f"{UMAMI_URL}{path}"
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def ms(dt: datetime) -> int:
    return int(dt.timestamp() * 1000)


def collect_snapshot(token: str) -> dict:
    now = datetime.now(timezone.utc)
    starts = {
        "24h": now - timedelta(hours=24),
        "7d":  now - timedelta(days=7),
        "30d": now - timedelta(days=30),
    }
    snap = {
        "generated_at": now.isoformat(),
        "website_id": WEBSITE_ID,
        "periods": {},
    }
    for key, start in starts.items():
        # Umami v3 metrics endpoint requires `compare=prev` and uses `type=path`
        # (not `url`) for page rankings. Stats endpoint accepts plain startAt/endAt.
        params = {"startAt": ms(start), "endAt": ms(now)}
        mparams = {**params, "compare": "prev"}
        try:
            stats = api_get(token, f"/api/websites/{WEBSITE_ID}/stats", params)
            top_pages_raw = api_get(token, f"/api/websites/{WEBSITE_ID}/metrics",
                                    {**mparams, "type": "path", "limit": 15})
            top_referrers_raw = api_get(token, f"/api/websites/{WEBSITE_ID}/metrics",
                                        {**mparams, "type": "referrer", "limit": 10})
            countries_raw = api_get(token, f"/api/websites/{WEBSITE_ID}/metrics",
                                    {**mparams, "type": "country", "limit": 10})
            devices_raw = api_get(token, f"/api/websites/{WEBSITE_ID}/metrics",
                                  {**mparams, "type": "device", "limit": 5})
            os_raw = api_get(token, f"/api/websites/{WEBSITE_ID}/metrics",
                             {**mparams, "type": "os", "limit": 6})
            browsers_raw = api_get(token, f"/api/websites/{WEBSITE_ID}/metrics",
                                   {**mparams, "type": "browser", "limit": 6})
            events_raw = api_get(token, f"/api/websites/{WEBSITE_ID}/metrics",
                                 {**mparams, "type": "event", "limit": 30})
            snap["periods"][key] = {
                "stats": stats,
                "top_pages": top_pages_raw,
                "top_referrers": top_referrers_raw,
                "countries": countries_raw,
                "devices": devices_raw,
                "os": os_raw,
                "browsers": browsers_raw,
                "events": events_raw,
            }
            pv = stats.get("pageviews", 0) if isinstance(stats, dict) else 0
            visitors = stats.get("visitors", 0) if isinstance(stats, dict) else 0
            # Some Umami versions wrap in {value: X}; normalize both
            if isinstance(pv, dict): pv = pv.get("value", 0)
            if isinstance(visitors, dict): visitors = visitors.get("value", 0)
            log(f"  {key}: {pv} pageviews, {visitors} unique visitors")
        except Exception as e:
            log(f"  {key}: ERROR {str(e)[:120]}")
            snap["periods"][key] = {"error": str(e)[:200]}
        time.sleep(0.3)
    return snap


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--rebuild", action="store_true",
                        help="rebuild SEO dashboard after snapshot")
    args = parser.parse_args()

    log("start")
    try:
        token = umami_login()
        log("logged in to Umami")
    except Exception as e:
        log(f"login failed: {e}")
        return 1

    snap = collect_snapshot(token)
    SNAPSHOT_FILE.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_FILE.write_text(json.dumps(snap, indent=2, ensure_ascii=False), encoding="utf-8")
    log(f"saved {SNAPSHOT_FILE}")

    if args.rebuild or args.commit:
        log("rebuilding dashboard...")
        r = subprocess.run(["python3", "scripts/build_seo_dashboard.py"],
                           cwd=ROOT, capture_output=True, text=True)
        if r.returncode != 0:
            log(f"build failed: {r.stderr[:200]}")
        else:
            log(r.stdout.strip().split("\n")[-1])

    if args.commit:
        token_gh = os.environ.get("GH_REPO_TOKEN", "").strip()
        if not token_gh:
            log("GH_REPO_TOKEN not set - skip push")
            return 0
        subprocess.run(["git", "add", "seo/analytics_snapshot.json",
                        "frontend/admin/seo.html"], cwd=ROOT)
        diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
        if diff.returncode == 0:
            log("no changes - skip commit")
            return 0
        subprocess.run([
            "git", "-c", "user.email=bot@botlease.nl",
            "-c", "user.name=BotLease Analytics Bot",
            "commit", "-m", "analytics-bot: weekly umami snapshot"
        ], cwd=ROOT, check=True)
        import re
        remote = subprocess.run(["git", "remote", "get-url", "origin"],
                                cwd=ROOT, capture_output=True, text=True).stdout.strip()
        if remote.startswith("https://"):
            host_path = re.sub(r"^https://[^/@]*@", "", remote)[len("https://"):]
            push_url = f"https://{token_gh}@{host_path}"
        else:
            push_url = remote
        subprocess.run(["git", "push", push_url, "HEAD:master"], cwd=ROOT, check=True)
        log("pushed")

    log("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
