#!/usr/bin/env python3
# refresh_claude_token.py — best-effort local refresh of ~/.claude/.credentials.json
#
# Mints a fresh accessToken from the stored refreshToken via Claude Code's public
# OAuth token endpoint, then writes the file back atomically. Never prints secrets.
#
# Why: the news bot authenticates with the Claude Code OAuth accessToken, which is
# short-lived. Claude Code keeps it fresh only while it is running, so an unattended
# launchd run can hit an expired token and silently publish nothing. This script
# refreshes it first. It is BEST-EFFORT: Anthropic may restrict third-party refresh,
# in which case it exits non-zero and the wrapper surfaces a loud failure.
#
# Exit codes: 0 = token fresh or successfully refreshed; 2 = refresh needed but failed.
# Usage: python3 scripts/refresh_claude_token.py [--force]
import json
import os
import sys
import time
import tempfile
import urllib.request
import urllib.error

CREDS = os.environ.get("CLAUDE_CREDS_PATH", os.path.expanduser("~/.claude/.credentials.json"))
TOKEN_URL = "https://console.anthropic.com/v1/oauth/token"
CLIENT_ID = "9d1c250a-e61b-44d9-88ed-5944d1962f5e"  # public Claude Code PKCE client
SKEW_MS = 10 * 60 * 1000  # refresh if within 10 min of expiry
FORCE = "--force" in sys.argv[1:]


def die(msg, code):
    sys.stderr.write(f"[refresh] {msg}\n")
    sys.exit(code)


try:
    with open(CREDS, "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    die(f"cannot read creds at {CREDS}: {e}", 2)

oauth = data.get("claudeAiOauth") or {}
refresh_token = oauth.get("refreshToken")
expires_at = oauth.get("expiresAt", 0)  # epoch MILLISECONDS
if not refresh_token:
    die("no refreshToken in creds — cannot refresh (re-login with Claude Code)", 2)

now_ms = int(time.time() * 1000)
if not FORCE and expires_at - now_ms > SKEW_MS:
    mins = (expires_at - now_ms) // 60000
    sys.stderr.write(f"[refresh] token still valid ~{mins} min; skipping\n")
    sys.exit(0)

body = json.dumps({
    "grant_type": "refresh_token",
    "refresh_token": refresh_token,
    "client_id": CLIENT_ID,
}).encode("utf-8")
req = urllib.request.Request(
    TOKEN_URL, data=body, method="POST",
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "anthropic-beta": "oauth-2025-04-20",
        "User-Agent": "claude-cli/oauth",
    },
)
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        resp = json.loads(r.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    detail = e.read().decode("utf-8", "replace")[:300]
    die(f"refresh HTTP {e.code}: {detail}", 2)
except Exception as e:
    die(f"refresh request failed: {e}", 2)

new_access = resp.get("access_token")
if not new_access:
    die("refresh response missing access_token", 2)
# refreshToken rotates — keep the new one if returned, else reuse the old one
new_refresh = resp.get("refresh_token") or refresh_token
expires_in = int(resp.get("expires_in", 0))
new_expires_at = int(time.time() * 1000) + expires_in * 1000

oauth["accessToken"] = new_access
oauth["refreshToken"] = new_refresh
oauth["expiresAt"] = new_expires_at
data["claudeAiOauth"] = oauth

# atomic write, 0600
d = os.path.dirname(CREDS) or "."
fd, tmp = tempfile.mkstemp(dir=d, prefix=".credentials.", suffix=".tmp")
try:
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(data, f)
        f.flush()
        os.fsync(f.fileno())
    os.chmod(tmp, 0o600)
    os.replace(tmp, CREDS)
except Exception as e:
    try:
        os.unlink(tmp)
    except OSError:
        pass
    die(f"atomic write failed: {e}", 2)

sys.stderr.write("[refresh] token refreshed OK\n")
sys.exit(0)
