#!/usr/bin/env python3
"""
BotLease News Bot — RSS → Dutch article pipeline.

Pulls humanoid-robot relevant news from RSS feeds, dedupes against past runs,
calls OpenRouter LLM to rewrite as Dutch BotLease article with proper structure,
appends to articles_data.py, rebuilds site, optionally commits + pushes to GitHub
(Vercel auto-deploys on push).

Run modes:
  python3 scripts/news_bot.py --dry-run     # show what would be generated
  python3 scripts/news_bot.py --max=3       # max 3 new articles per run
  python3 scripts/news_bot.py --commit      # also git commit + push

LLM auth (in order):
  1. Claude OAuth token at $CLAUDE_CREDS_PATH (uses the Claude Max subscription, Opus). Primary.
  2. OPENROUTER_API_KEY (sk-or-v1-...) → anthropic/claude-opus-4.7. Real fallback when (1)
     is absent OR fails (outage / expired token).

Env vars:
  CLAUDE_CREDS_PATH     path to Claude Code credentials (default ~/.claude on this Mac via the wrapper)
  CLAUDE_REFRESH_SCRIPT optional script to refresh an expired OAuth token in-process
  OPENROUTER_API_KEY    fallback LLM auth
  GH_REPO_TOKEN         only when --commit, for the token-based git push

Scheduling: weekly via launchd on this Mac — see scripts/run_news_weekly.sh +
  ~/Library/LaunchAgents/nl.botlease.newsbot.plist (installed 2026-06-02).
  The wrapper refreshes the OAuth token, runs --commit --max=2, and turns the
  bot's silent "0 articles" exit into a loud failure. GitHub Actions + OpenRouter
  is the documented machine-independent backstop.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta, date as date_cls
from pathlib import Path
from html import unescape

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
SEEN_FILE = SCRIPTS / "news_seen.json"
ARTICLES_FILE = SCRIPTS / "articles_data.py"
LOG_TAG = "[news-bot]"

# ---------------------------------------------------------------- config

# RSS feeds — humanoid-relevant. (name, url, default_category, source_country)
FEEDS = [
    # --- verified working (kept) ---
    ("The Robot Report",           "https://www.therobotreport.com/feed/",                      "Industrie",      "US"),
    ("IEEE Spectrum Robotics",     "https://spectrum.ieee.org/feeds/topic/robotics.rss",        "R&D",            "US"),
    ("Tweakers",                   "https://feeds.feedburner.com/tweakers/mixed",               "Markt",          "NL"),
    ("Robohub",                    "https://robohub.org/feed/",                                 "R&D",            "EU"),

    # --- replacements for dead feeds (verified 2026-06-02 with feedparser) ---
    # Apptronik & Agility removed their own RSS (sites are now Webflow / no feed path).
    # Company coverage preserved via The Robot Report tag feeds (reliable WordPress RSS).
    ("Apptronik (via TRR)",        "https://www.therobotreport.com/tag/apptronik/feed/",        "Bedrijfsnieuws", "US"),  # was apptronik.com/news?format=rss (dead 301->404)
    ("Agility Robotics (via TRR)", "https://www.therobotreport.com/tag/agility-robotics/feed/", "Bedrijfsnieuws", "US"),  # was agilityrobotics.com/news/rss.xml (dead 301->404)
    ("TRR Humanoids",              "https://www.therobotreport.com/category/humanoids/feed/",   "Industrie",      "US"),  # replaces Computable (404)
    ("TechCrunch Robotics",        "https://techcrunch.com/tag/robotics/feed/",                 "Markt",          "US"),  # replaces FD Tech (returned HTML, not RSS)
    ("TRR Humanoid Robots",        "https://www.therobotreport.com/tag/humanoid-robots/feed/",  "R&D",            "US"),  # extra humanoid stream

    # --- self-feed, intentionally filtered out in code ---
    ("BotLease intern (skip)",     "https://botlease.nl/rss.xml",                               "Marktstand",     "NL"),  # self — filtered out
]

# Drop candidates older than this before scoring/publishing, so the bot never
# publishes months-old archive items as fresh "news". Tuned for a weekly cadence.
MAX_AGE_DAYS = 21

# Strict humanoid-relevant patterns. Each requires an unambiguous signal
# to avoid false positives like "Apollo space mission" or "Figure (skating)".
KEYWORDS = [
    # explicit humanoid mentions
    r"\bhumanoid\b",
    r"\bhumano[iï]de\b",
    r"\bbipedal robot\b",
    r"\bbipedal humanoid\b",
    # manufacturer + product combos (disambiguated)
    r"\bApptronik\b",
    r"\bApollo robot\b",
    r"\bApollo humanoid\b",
    r"\bFigure 0?[123]\b",
    r"\bFigure AI\b",
    r"\b1X Technologies\b",
    r"\b1X NEO\b",
    r"\bUnitree\b",
    r"\bNEURA Robotics\b",
    r"\b4NE-?1\b",
    r"\bAgility Robotics\b",
    r"\bDigit robot\b",
    r"\bAtlas (robot|humanoid)\b",
    r"\bBoston Dynamics\b",
    r"\bUBTECH\b",
    r"\bWalker S[12]\b",
    r"\bEngineAI\b",
    r"\bSanctuary AI\b",
    r"\bPhoenix robot\b",
    r"\bPollen Robotics\b",
    r"\bReachy\b",
    # concepts directly tied to humanoid robotica
    r"\bVLA model\b",
    r"\bembodied AI\b",
    r"\bdexterous manipulation\b",
    r"\brobot lease\b",
    r"\brobot leasen\b",
]
KEYWORD_RE = re.compile("|".join(KEYWORDS), re.IGNORECASE)

# Block any post containing these — purely consumer/social robots, not relevant
BLOCK_PATTERNS = re.compile(
    r"\b(toy robot|robot lawn ?mower|robot vacuum|roomba|robotic vacuum|robotic mower)\b",
    re.IGNORECASE,
)

SLUG_BAD_RE = re.compile(r"[^a-z0-9]+")
SOURCE_URL_HASH = lambda u: hashlib.sha256(u.encode("utf-8")).hexdigest()[:16]


# Load BotLease's target SEO keywords from seo/seo_data.json so the news-bot
# scores candidates by topical relevance + weaves these terms into output.
SEO_KEYWORDS_FILE = Path(__file__).resolve().parent.parent / "seo" / "seo_data.json"


def load_seo_targets() -> list[dict]:
    try:
        data = json.loads(SEO_KEYWORDS_FILE.read_text(encoding="utf-8"))
        return data.get("target_keywords", [])
    except Exception:
        return []


def seo_score(title: str, summary: str, targets: list[dict]) -> tuple[int, list[str]]:
    """Score how well a candidate aligns with our SEO target keywords.
    Returns (score, matched_keyword_ids). Title hits count double.
    A match requires at least one DISCRIMINATING token (brand/sector/city),
    not just generic 'robot' or 'humanoid'."""
    title_l = title.lower()
    summary_l = summary.lower()

    # Tokens too generic to count alone — every humanoid article has them
    GENERIC = {"robot", "robots", "humanoid", "humanoids", "humanoide",
               "humanoïde", "nederland", "leasen", "lease", "huren",
               "kopen", "prijs", "het", "een", "voor", "the", "and", "for", "with"}

    score = 0
    matched = []
    weight = {"P0": 6, "P1": 3, "P2": 1}
    for kw in targets:
        terms = re.findall(r"[a-z0-9-]+", kw["kw"].lower())
        # Discriminating = not in GENERIC and length >= 3
        discriminating = [t for t in terms if t not in GENERIC and len(t) >= 3]
        if not discriminating:
            continue
        title_hits = sum(1 for t in discriminating if t in title_l)
        summary_hits = sum(1 for t in discriminating if t in summary_l)
        # Need at least one discriminating hit
        if title_hits == 0 and summary_hits == 0:
            continue
        kw_score = weight.get(kw.get("priority", "P2"), 1)
        # Title hit = double weight, summary hit = base. Multi-token bonus.
        total_hits = title_hits * 2 + summary_hits
        score += kw_score * total_hits
        matched.append(kw["id"])
    return score, matched

# LLM auth — preferred path is Claude Code OAuth (uses user's Claude Max subscription).
# Falls back to OpenRouter if OAuth not available.
CLAUDE_CREDS_PATH = os.environ.get(
    "CLAUDE_CREDS_PATH", "/root/.claude/.credentials.json"
)
CLAUDE_REFRESH_SCRIPT = os.environ.get(
    "CLAUDE_REFRESH_SCRIPT", "/root/refresh-anthropic-token.sh"
)
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_BETA_HEADER = "oauth-2025-04-20"
# Best-quality news writing → Opus only. (Note: "Opus 4.6" doesn't exist as an ID;
# the latest Opus in the Claude 4.x family is 4.7. We use that.)
CLAUDE_MODEL_PRIMARY = "claude-opus-4-7"
CLAUDE_MODEL_FALLBACK = "claude-opus-4-7"  # no downgrade — user wants Opus only

# PRIMARY route: the `claude` CLI (Claude Code subscription). Same mechanism the
# draft-bot uses — it manages its own OAuth + token refresh, so it never silently
# falls through to a billed API. User rule: news must ALWAYS run via the subscription.
CLAUDE_BIN = os.environ.get("CLAUDE_BIN", "/usr/local/bin/claude")
CLAUDE_CLI_MODEL = os.environ.get("NEWS_CLI_MODEL", "opus")

# OpenRouter as backup if OAuth not available
OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY", "").strip()
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL_PRIMARY = "google/gemini-2.5-flash"
OPENROUTER_MODEL_FALLBACK = "anthropic/claude-haiku-4.5"


# ---------------------------------------------------------------- utils

def log(msg: str) -> None:
    print(f"{LOG_TAG} {datetime.now().isoformat(timespec='seconds')} {msg}", flush=True)


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[áàäâ]", "a", s)
    s = re.sub(r"[éèëê]", "e", s)
    s = re.sub(r"[íìïî]", "i", s)
    s = re.sub(r"[óòöô]", "o", s)
    s = re.sub(r"[úùüû]", "u", s)
    s = SLUG_BAD_RE.sub("-", s).strip("-")
    return s[:80]


def _date_ordinal(s: str) -> int:
    """Proleptic-Gregorian ordinal for an ISO date string; 0 if unparseable.
    Used in sort keys so one bad date can never crash the whole run."""
    try:
        return date_cls.fromisoformat(s[:10]).toordinal()
    except Exception:
        return 0


def _norm_title_fp(title: str) -> str:
    """Fingerprint a title for content-level dedup (same story from two feeds)."""
    norm = re.sub(r"[^a-z0-9]", "", (title or "").lower())
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()[:16]


def _atomic_write(path: Path, text: str) -> None:
    """Write text via temp-file + os.replace so a crash never leaves a half-written file."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def load_seen() -> dict:
    if not SEEN_FILE.exists():
        return {}
    try:
        return json.loads(SEEN_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        log(f"WARN: could not parse {SEEN_FILE}: {e} — starting fresh")
        return {}


def save_seen(seen: dict) -> None:
    _atomic_write(SEEN_FILE, json.dumps(seen, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------- RSS

def fetch_feeds(feeds):
    """Yield (entry, feed_meta) for every entry across all feeds."""
    import feedparser
    for name, url, default_cat, country in feeds:
        if "botlease.nl" in url:
            continue  # skip self
        log(f"feed: {name} ({url})")
        try:
            f = feedparser.parse(url, request_headers={"User-Agent": "BotLeaseNewsBot/1.0 (+https://botlease.nl)"})
        except Exception as e:
            log(f"  ERROR fetching {name}: {e}")
            continue
        if f.bozo and not f.entries:
            log(f"  WARN {name}: bozo + no entries")
            continue
        log(f"  → {len(f.entries)} entries")
        for entry in f.entries:
            yield entry, {"name": name, "url": url, "default_category": default_cat, "country": country}


def _clean_image_url(u: str) -> str:
    """Return u only if it is a usable absolute http(s) image URL.
    Protocol-relative //... is upgraded to https:; relative/non-http is rejected."""
    u = (u or "").strip()
    if not u:
        return ""
    if u.startswith("//"):
        u = "https:" + u
    return u if u.startswith(("http://", "https://")) else ""


def extract_image(entry) -> str:
    """Extract a hero image URL from a feedparser entry (validated absolute http(s) only)."""
    # 1. media_content / media_thumbnail
    for key in ("media_content", "media_thumbnail"):
        items = entry.get(key)
        if items:
            for it in items:
                u = _clean_image_url(it.get("url", ""))
                if u:
                    return u
    # 2. links with image rel
    for lnk in entry.get("links", []):
        if "image" in lnk.get("type", ""):
            u = _clean_image_url(lnk.get("href", ""))
            if u:
                return u
    # 3. enclosures
    for enc in entry.get("enclosures", []):
        if "image" in enc.get("type", ""):
            u = _clean_image_url(enc.get("href", ""))
            if u:
                return u
    # 4. parse <img src=> from summary/content
    html = entry.get("summary", "") or ""
    for c in entry.get("content", []):
        html += c.get("value", "")
    m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', html)
    if m:
        return _clean_image_url(unescape(m.group(1)))
    return ""


def is_relevant(title: str, summary: str) -> bool:
    body = f"{title}\n{summary}"
    if BLOCK_PATTERNS.search(body):
        return False
    return bool(KEYWORD_RE.search(body))


def normalize_entry(entry, feed_meta) -> dict | None:
    """Return normalized entry-dict or None if irrelevant."""
    title = (entry.get("title") or "").strip()
    summary_raw = (entry.get("summary") or "").strip()
    # Strip HTML tags from summary for keyword matching
    summary = re.sub(r"<[^>]+>", " ", summary_raw)
    summary = re.sub(r"\s+", " ", summary).strip()
    link = (entry.get("link") or "").strip()
    if not title or not link:
        return None
    if not is_relevant(title, summary):
        return None

    # Date. Validate month/day ranges (malformed feeds can yield tm_mon=0) and
    # do NOT fall back to "today" for undated items — that would let archive
    # entries masquerade as fresh news. Undated → sentinel old date so the
    # recency filter in main() drops them.
    pub_iso = None
    for k in ("published_parsed", "updated_parsed"):
        t = entry.get(k)
        if t and 1 <= t.tm_mon <= 12 and 1 <= t.tm_mday <= 31:
            pub_iso = f"{t.tm_year:04d}-{t.tm_mon:02d}-{t.tm_mday:02d}"
            break
    if not pub_iso:
        pub_iso = "1970-01-01"  # undated → treated as stale

    return {
        "title": title,
        "summary": summary[:1500],
        "url": link,
        "image": extract_image(entry),
        "published": pub_iso,
        "source_name": feed_meta["name"],
        "default_category": feed_meta["default_category"],
        "url_hash": SOURCE_URL_HASH(link),
    }


# ---------------------------------------------------------------- LLM

def _read_claude_token() -> str | None:
    try:
        d = json.loads(Path(CLAUDE_CREDS_PATH).read_text(encoding="utf-8"))
        return d.get("claudeAiOauth", {}).get("accessToken")
    except Exception:
        return None


def _refresh_claude_token() -> None:
    if not Path(CLAUDE_REFRESH_SCRIPT).exists():
        return
    try:
        subprocess.run(["bash", CLAUDE_REFRESH_SCRIPT], capture_output=True, timeout=30)
    except Exception as e:
        log(f"  refresh script failed: {e}")


def call_claude_cli(system: str, user: str) -> str:
    """Write via the `claude` CLI = the Claude Code subscription. No API billing,
    self-refreshing auth. This is the primary route (user rule). The CLI is itself
    Claude Code, so journalism instructions go in the prompt, not a system field."""
    prompt = f"{system}\n\n=== BRON ===\n{user}"
    r = subprocess.run(
        [CLAUDE_BIN, "-p", prompt, "--model", CLAUDE_CLI_MODEL],
        capture_output=True, text=True, timeout=300,
        env={**os.environ, "HOME": os.environ.get("HOME", "/root")},
    )
    raw = (r.stdout or "").strip()
    if not raw:
        raise RuntimeError(f"claude CLI empty output ({(r.stderr or '')[:160]})")
    return raw


def call_claude_oauth(model: str, system: str, user: str, max_tokens: int = 4000) -> str:
    """Call Anthropic API using Claude Code OAuth token (uses Claude Max subscription).

    NB: Claude Code OAuth restricts custom system prompts on Opus — must use the
    exact identity string only. Journalism instructions are folded into the user
    message instead. (Sonnet allows custom prompts, but user prefers Opus.)
    """
    import urllib.request
    token = _read_claude_token()
    if not token:
        raise RuntimeError(f"no Claude OAuth token at {CLAUDE_CREDS_PATH}")

    cc_system = "You are Claude Code, Anthropic's official CLI for Claude."
    user_with_instructions = f"{system}\n\n---\n\n{user}"

    body_dict = {
        "model": model,
        "max_tokens": max_tokens,
        "system": cc_system,
        "messages": [{"role": "user", "content": user_with_instructions}],
    }
    body = json.dumps(body_dict).encode("utf-8")

    def _do_call(tok: str) -> tuple[int, str]:
        req = urllib.request.Request(
            ANTHROPIC_API_URL,
            data=body,
            headers={
                "Authorization": f"Bearer {tok}",
                "anthropic-version": "2023-06-01",
                "anthropic-beta": ANTHROPIC_BETA_HEADER,
                "content-type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return 200, r.read().decode("utf-8")
        except urllib.request.HTTPError as e:
            return e.code, e.read().decode("utf-8", errors="replace")

    status, raw = _do_call(token)
    # 401 → token expired, refresh + retry once
    if status == 401:
        log("  oauth 401 — refreshing token")
        _refresh_claude_token()
        token = _read_claude_token()
        if not token:
            raise RuntimeError("token refresh failed: no token after refresh")
        status, raw = _do_call(token)

    # 429 → rate-limited (Claude Max 5h window shared with user's interactive sessions).
    # Back off and retry up to 3 times with exponential delay.
    backoff = 30
    for _ in range(3):
        if status != 429:
            break
        log(f"  oauth 429 — backing off {backoff}s")
        time.sleep(backoff)
        status, raw = _do_call(token)
        backoff *= 2

    if status != 200:
        raise RuntimeError(f"Anthropic API {status}: {raw[:300]}")

    data = json.loads(raw)
    content = data.get("content", [])
    if not content:
        raise RuntimeError(f"empty content in response: {data}")
    # Anthropic returns content as list of {type:text, text:...}
    return content[0].get("text", "")


def call_openrouter(model: str, system: str, user: str, max_tokens: int = 4000) -> str:
    import urllib.request
    if not OPENROUTER_KEY:
        raise RuntimeError("OPENROUTER_API_KEY not set")
    body = json.dumps({
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "temperature": 0.4,
        "max_tokens": max_tokens,
    }).encode("utf-8")
    req = urllib.request.Request(
        OPENROUTER_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://botlease.nl",
            "X-Title": "BotLease News Bot",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read().decode("utf-8")
    except Exception as e:
        raise RuntimeError(f"OpenRouter call failed for {model}: {e}")
    data = json.loads(raw)
    if "choices" not in data:
        raise RuntimeError(f"OpenRouter returned no choices: {data}")
    return data["choices"][0]["message"]["content"]


REWRITE_SYSTEM = """Je bent een Nederlandse tech-journalist voor BotLease.nl, een Nederlandse lease-bemiddelaar voor humanoïde robots.
Je schrijft hoogwaardige, feitelijke Nederlandse nieuwsartikelen over humanoïde robotica, ~600-900 woorden.

REGELS:
- Schrijf ALTIJD in correct, professioneel Nederlands. Geen Engelse zinnen, geen anglicismen waar dat onnodig is.
- GEEN em-dashes (-) of en-dashes (-). Gebruik een gewone dash (-) met spaties, of een dubbele punt, of begin een nieuwe zin. Dit is een harde regel.
- GEEN "smart quotes" (' ' " "). Alleen rechte quotes (' ").
- Wees feitelijk en concreet. Gebruik cijfers waar de bron ze geeft. Verzin nooit specs of namen.
- Bouw context op vanuit Nederlandse/Europese hoek (compliance, EU AI-Act, NL-markt) waar relevant.
- Geef NIET het gevoel van een persbericht. Beoordeel kritisch: wat betekent dit voor een Europese/Nederlandse werkgever?
- NOOIT clickbait. NOOIT "experts zeggen" zonder bron. NOOIT speculeren over koersen of overnames.
- Sluit af met een bondige NL-impact-paragraaf van 2-3 zinnen.

FORMAT — geef EXACT geldige JSON terug, niets anders:
{
  "title": "string - Nederlandse titel, MAX 55 CHARS (harde limiet voor Google SERP-weergave). Geen titel-case. Voor SEO: zet het belangrijkste keyword voorin.",
  "subtitle": "string — 1 zin samenvatting, max 180 chars",
  "tldr": "string — DE KERN in 1-2 strakke zinnen (max 250 chars). Geen aanloopzin, direct het belangrijkste feit + waarom het ertoe doet.",
  "category": "een van: Industrie, Markt, R&D, Regelgeving, Bedrijfsnieuws, Pilots",
  "tags": ["lijst", "van", "max", "5", "tags"],
  "intro": "string — eerste paragraaf, 2-3 zinnen, zet de feiten neer (mag uitgebreider zijn dan tldr)",
  "body_sections": [
    {"h": "Tussenkopje", "p": "HTML-veilige paragraaf met <b> en <a> waar nodig"},
    {"h": "Tussenkopje 2", "p": "Paragraaf 2 — minimaal 4 secties totaal"}
  ],
  "reading_time": 5,
  "nl_angle": "string — afsluit-paragraaf 2-3 zinnen over NL/EU-impact"
}"""

REWRITE_USER_TEMPLATE = """Bron-artikel:
TITEL: {title}
BRON: {source_name}
LINK: {url}
DATUM: {published}

INHOUD (samenvatting):
{summary}

SEO-FOCUS (verwerk deze termen NATUURLIJK in titel, intro en H2's waar relevant — niet forceren als de context niet past):
{seo_focus}

INTERNE LINKS — bouw er minstens 2-3 in waar relevant (markdown link-syntax in HTML <a>-tags):
- /robots — catalogus 15 modellen
- /gids/humanoide-robot-leasen — pijler-gids
- /gids/ai-act-machineverordening — EU AI-Act / Machineverordening gids
- /kosten — prijsstelling
- /vergelijken/lease-vs-koop — beslis-pagina
- /sectoren/3pl-fulfillment — 3PL sector-pagina
- /sectoren/productie-assemblage — productie sector-pagina
- /robots/unitree-g1, /robots/neura-4ne1-gen3, /robots/apptronik-apollo, etc. — model-pagina's (alleen linken als het model in artikel genoemd wordt)

Schrijf hier een Nederlandstalig BotLease-artikel van. Geef EXACT JSON terug volgens het schema."""


def llm_rewrite(item: dict) -> dict | None:
    # Build SEO-focus block: take matched keywords + few high-priority ones to hint at
    targets = load_seo_targets()
    matched_ids = set(item.get("seo_matched", []))
    matched_kws = [t for t in targets if t["id"] in matched_ids]
    extra_p0 = [t for t in targets if t.get("priority") == "P0" and t["id"] not in matched_ids][:2]
    focus_lines = []
    for t in matched_kws[:5]:
        focus_lines.append(f"- \"{t['kw']}\"  ({t.get('priority','P?')}, doel-pagina: {t.get('target_page','/')})")
    for t in extra_p0:
        focus_lines.append(f"- \"{t['kw']}\"  ({t.get('priority','P0')}, optioneel als context past)")
    seo_focus = "\n".join(focus_lines) if focus_lines else "(geen sterke matches — focus op algemene humanoid/lease termen)"

    user_prompt = REWRITE_USER_TEMPLATE.format(
        title=item["title"], source_name=item["source_name"],
        url=item["url"], published=item["published"], summary=item["summary"],
        seo_focus=seo_focus,
    )

    # Build a list of (label, fn) callables to try in order.
    attempts = []
    # PRIMARY: the `claude` CLI = Claude Code subscription. Self-refreshing auth,
    # no API billing. User rule: news must always run via the subscription.
    if Path(CLAUDE_BIN).exists():
        attempts.append((f"claude-cli:{CLAUDE_CLI_MODEL}",
                         lambda: call_claude_cli(REWRITE_SYSTEM, user_prompt)))
    # Fallback A: Opus via Claude OAuth API (same subscription, raw token path).
    if Path(CLAUDE_CREDS_PATH).exists():
        attempts.append((f"claude-oauth:{CLAUDE_MODEL_PRIMARY}",
                         lambda: call_claude_oauth(CLAUDE_MODEL_PRIMARY, REWRITE_SYSTEM, user_prompt, max_tokens=8000)))
    # Real fallback: OpenRouter (still Opus). Runs whenever a key is set and the
    # Claude attempt is absent OR fails — so a Claude outage / expired token no
    # longer silently yields zero articles.
    if OPENROUTER_KEY:
        attempts.append(("openrouter:anthropic/claude-opus-4.7",
                         lambda: call_openrouter("anthropic/claude-opus-4.7", REWRITE_SYSTEM, user_prompt, max_tokens=8000)))

    if not attempts:
        log("  no LLM auth available (no Claude OAuth creds, no OPENROUTER_API_KEY)")
        return None

    for label, fn in attempts:
        try:
            log(f"  llm: {label}")
            raw = fn()
            raw = raw.strip()
            if raw.startswith("```"):
                raw = re.sub(r"^```(json)?", "", raw).rstrip("`").strip()
            data = json.loads(raw)
            for k in ("title", "subtitle", "category", "intro", "body_sections", "nl_angle"):
                if k not in data:
                    raise ValueError(f"missing field: {k}")
            # body_sections must be a non-empty list of dict sections (models
            # sometimes return a list of strings) — coerce/validate, don't crash.
            if not isinstance(data.get("body_sections"), list):
                raise ValueError("body_sections is not a list")
            data["body_sections"] = [s for s in data["body_sections"] if isinstance(s, dict)]
            if not data["body_sections"]:
                raise ValueError("body_sections has no valid dict sections")
            log(f"  ✓ generated via {label}")
            return data
        except Exception as e:
            log(f"  llm failed ({label}): {str(e)[:160]}")
            continue
    return None


def editorial_gate(rewrite: dict, item: dict) -> tuple[bool, str]:
    """Redactionele kwaliteitspoort: weiger dunne single-source rehash vóór publicatie
    (anti scaled-content). FAIL-OPEN: bij interne fout publiceren we (return True)."""
    try:
        secs = [s for s in rewrite.get("body_sections", []) if isinstance(s, dict)]
        paras = [p for p in (str(s.get("p", "") or "").strip() for s in secs) if p]
        body_chars = sum(len(p) for p in paras)
        nl = str(rewrite.get("nl_angle", "") or "").strip()
        intro = str(rewrite.get("intro", "") or "").strip()
        title = str(rewrite.get("title", "") or "")
        if len(title) > 80:
            return False, f"titel te lang ({len(title)} tekens, max 80)"
        if len(paras) < 3:
            return False, f"te weinig alinea's ({len(paras)})"
        if body_chars < 800:
            return False, f"body te dun ({body_chars} tekens)"
        if len(nl) < 100:
            return False, f"NL-duiding te dun ({len(nl)} tekens)"
        if len(intro) < 80:
            return False, f"intro te dun ({len(intro)} tekens)"
        return True, "ok"
    except Exception as e:
        return True, f"gate-fout, fail-open ({str(e)[:60]})"


# ---------------------------------------------------------------- article writer

def article_to_python(item: dict, rewrite: dict) -> str:
    """Render a Python dict literal for articles_data.ARTICLES.append()."""
    slug = slugify(rewrite["title"])
    if not slug:
        slug = f"news-{item['url_hash']}"
    # Body tuples: [("h2", h), ("p", p), ...]
    body_lines = []
    for sec in rewrite["body_sections"]:
        if not isinstance(sec, dict):
            continue
        h = str(sec.get("h", "") or "").strip()
        p = str(sec.get("p", "") or "").strip()
        if h:
            body_lines.append(f'            ("h2", {repr(h)}),')
        if p:
            body_lines.append(f'            ("p", {repr(p)}),')
    body_lines.append(f'            ("h2", "Wat betekent dit voor Nederland?"),')
    body_lines.append(f'            ("p", {repr(rewrite["nl_angle"])}),')

    tags = rewrite.get("tags") or []
    tags_repr = ", ".join(repr(t) for t in tags[:6])

    try:
        reading_time = int(rewrite.get("reading_time", 5))
    except (ValueError, TypeError):
        reading_time = 5

    return f"""    {{
        "slug": {repr(slug)},
        "title": {repr(rewrite["title"])},
        "subtitle": {repr(rewrite["subtitle"])},
        "category": {repr(rewrite["category"])},
        "date": {repr(date_cls.today().isoformat())},
        "reading_time": {reading_time},
        "author": "Thomas Vedder",
        "source_name": {repr(item["source_name"])},
        "source_url": {repr(item["url"])},
        "hero_image_url": {repr(item.get("image", ""))},
        "hero_image_alt": {repr(rewrite["title"][:120])},
        "tags": [{tags_repr}],
        "tldr": {repr(rewrite.get("tldr", ""))},
        "intro": {repr(rewrite["intro"])},
        "body": [
{chr(10).join(body_lines)}
        ],
        "sources": [
            ({repr(item["source_name"])}, {repr(item["url"])}),
        ],
    }},
"""


def append_to_articles(article_py: str) -> bool:
    import ast
    text = ARTICLES_FILE.read_text(encoding="utf-8")
    # Insert before the last `]\n` of `ARTICLES = [`
    # Strategy: find the LAST occurrence of "\n]" that closes ARTICLES.
    idx = text.rfind("\n]")
    if idx == -1:
        log("ERROR: could not find end of ARTICLES list")
        return False
    new_text = text[:idx] + "\n" + article_py + text[idx + 1:]
    # Never write a file we can't parse — a corrupt articles_data.py would break
    # every later import, the site build, and all future bot runs.
    try:
        ast.parse(new_text)
    except SyntaxError as e:
        log(f"ERROR: refusing to write — new articles_data.py would be invalid Python: {e}")
        return False
    _atomic_write(ARTICLES_FILE, new_text)
    return True


# ---------------------------------------------------------------- git

def run(cmd: list[str], cwd: Path | None = None) -> str:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"cmd failed: {' '.join(cmd)}\nSTDOUT: {r.stdout}\nSTDERR: {r.stderr}")
    return r.stdout.strip()



def update_main_sitemap(slugs: list) -> None:
    """Voegt nieuwe nieuws-URLs toe aan frontend/sitemap.xml (merge — raakt
    bestaande entries niet aan; build_news schrijft deze sitemap bewust niet)."""
    sm = ROOT / "frontend" / "sitemap.xml"
    try:
        xml = sm.read_text(encoding="utf-8")
        today = date_cls.today().isoformat()
        new = ""
        for slug in slugs:
            loc = f"https://botlease.nl/nieuws/{slug}"
            if loc in xml:
                continue
            new += (f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod>"
                    f"<changefreq>monthly</changefreq><priority>0.7</priority></url>\n")
        if new:
            xml = xml.replace("</urlset>", new + "</urlset>")
            _atomic_write(sm, xml)
            log(f"sitemap.xml: +{new.count('<url>')} nieuws-URLs")
    except Exception as e:
        log(f"WARN sitemap.xml update faalde: {str(e)[:120]}")


def git_commit_and_push(slugs: list[str]) -> None:
    token = os.environ.get("GH_REPO_TOKEN", "").strip()
    titles = ", ".join(slugs)
    msg = f"news-bot: auto-publish — {titles}"
    # Stage BOTH the source data AND the rebuilt site output, so a single commit
    # actually deploys the new pages. (Historically only the two source files were
    # staged, so the generated HTML was never committed and never went live.)
    # Explicit paths — never `git add -A` — so unrelated working-tree changes are
    # left untouched. Only stage paths that actually exist.
    paths = [
        "scripts/articles_data.py",
        "scripts/news_seen.json",
        "frontend/nieuws",                # per-article HTML + nieuws/index.html
        "frontend/data/articles.json",
        "frontend/rss.xml",
        "frontend/sitemap-news.xml",
        "frontend/sitemap.xml",
    ]
    existing = [p for p in paths if (ROOT / p).exists()]
    run(["git", "add", *existing], cwd=ROOT)
    # commit only if there is staged change
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
    if diff.returncode == 0:
        log("no changes staged — skip commit")
        return
    run(["git", "-c", "user.email=bot@botlease.nl", "-c", "user.name=BotLease News Bot",
         "commit", "-m", msg], cwd=ROOT)
    # Push. SSH remote → use the configured key (no token needed). HTTPS remote →
    # inject GH_REPO_TOKEN (stripping any existing creds so we don't get TOKEN@TOKEN@host).
    try:
        remote = run(["git", "remote", "get-url", "origin"], cwd=ROOT)
        if remote.startswith("https://"):
            if not token:
                log("https remote but GH_REPO_TOKEN not set — commit is LOCAL, push manually")
                return
            m = re.match(r"https://(?:[^/@]*@)?(.+)$", remote)
            push_url = f"https://{token}@{m.group(1)}" if m else remote
        else:
            push_url = remote  # ssh/git@ — pushes via the user's SSH key
        run(["git", "push", push_url, "HEAD:master"], cwd=ROOT)
        log(f"pushed: {msg}")
    except Exception as e:
        log(f"WARN push failed — commit is local, fix + push manually: {str(e)[:200]}")
        return
    # Notify IndexNow (Bing/Yandex) of the freshly published pages.
    try:
        urls = [f"https://botlease.nl/nieuws/{s}" for s in slugs]
        run(["python3", "scripts/indexnow_ping.py", *urls], cwd=ROOT)
        log(f"indexnow: pinged {len(urls)} url(s)")
    except Exception as e:
        log(f"WARN indexnow ping failed: {str(e)[:160]}")


# ---------------------------------------------------------------- main

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max", type=int, default=2)
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--rebuild", action="store_true",
                        help="also run build_news.py after appending")
    args = parser.parse_args()

    log(f"start — max={args.max}, dry_run={args.dry_run}, commit={args.commit}")
    seen = load_seen()
    log(f"loaded {len(seen)} seen URLs")

    # 1. Collect + score candidates from all feeds
    targets = load_seo_targets()
    log(f"loaded {len(targets)} SEO target keywords for scoring")
    cutoff = (date_cls.today() - timedelta(days=MAX_AGE_DAYS)).toordinal()
    # Title fingerprints already published — block the same story arriving via a
    # second feed (different URL, so url_hash alone wouldn't catch it).
    seen_title_fps = {_norm_title_fp(v.get("title", "")) for v in seen.values()}
    candidates: list[dict] = []
    n_stale = n_dup_url = n_dup_title = 0
    for entry, feed_meta in fetch_feeds(FEEDS):
        norm = normalize_entry(entry, feed_meta)
        if not norm:
            continue
        if norm["url_hash"] in seen:
            n_dup_url += 1
            continue
        # Recency: never publish months-old archive items as fresh news.
        if _date_ordinal(norm["published"]) < cutoff:
            n_stale += 1
            continue
        # Content dedup vs already-published titles.
        tfp = _norm_title_fp(norm["title"])
        if tfp in seen_title_fps:
            n_dup_title += 1
            continue
        norm["title_fp"] = tfp
        score, matched = seo_score(norm["title"], norm["summary"], targets)
        norm["seo_score"] = score
        norm["seo_matched"] = matched
        candidates.append(norm)
    # Sort: highest SEO score first, then newest within same score. Safe date key —
    # a single unparseable date can never crash the whole run.
    candidates.sort(key=lambda x: (-x["seo_score"], -_date_ordinal(x["published"])))
    log(f"found {len(candidates)} fresh unseen candidates "
        f"(filtered: {n_stale} stale, {n_dup_url} seen-url, {n_dup_title} dup-title; "
        f"top SEO-score: {candidates[0]['seo_score'] if candidates else 0})")
    if not candidates:
        log("nothing to do.")
        return 0

    # 2. Pick top N — also dedup by title fingerprint within this batch.
    to_process = []
    picked_fps: set[str] = set()
    for c in candidates:
        if c["title_fp"] in picked_fps:
            continue
        picked_fps.add(c["title_fp"])
        to_process.append(c)
        if len(to_process) >= args.max:
            break
    if args.dry_run:
        for c in to_process:
            log(f"DRY: {c['published']}  seo_score={c['seo_score']}  {c['source_name']}")
            log(f"     {c['title']}")
            log(f"     matched_kw: {c['seo_matched'] or '(none)'}")
            log(f"     img: {c['image'] or '(none)'}")
        return 0

    # 3. LLM rewrite + append. Each item is isolated: one bad item logs + skips,
    #    it never aborts the whole run. seen.json is persisted right after each
    #    successful append so a mid-run crash can't desync it from articles_data.py.
    published_slugs = []
    for item in to_process:
        log(f"processing: {item['title'][:80]}")
        try:
            rewrite = llm_rewrite(item)
            if not rewrite:
                log("  skip — llm failed")
                continue
            ok_edit, reason = editorial_gate(rewrite, item)
            if not ok_edit:
                log(f"  skip — redactie-poort: {reason}")
                continue
            slug = slugify(rewrite["title"])
            article_py = article_to_python(item, rewrite)
            ok = append_to_articles(article_py)
            if not ok:
                continue
            seen[item["url_hash"]] = {
                "date": item["published"],
                "slug": slug,
                "title": rewrite["title"],
                "source": item["source_name"],
            }
            save_seen(seen)
            published_slugs.append(slug)
            log(f"  ✅ added: {slug}")
        except Exception as e:
            log(f"  skip — error: {str(e)[:200]}")
            continue
        time.sleep(1)  # be polite to APIs

    log(f"seen.json has {len(seen)} entries")

    if not published_slugs:
        log("no articles published this run.")
        return 0

    update_main_sitemap(published_slugs)

    # 4. Optionally rebuild
    if args.rebuild or args.commit:
        log("rebuilding...")
        run(["python3", "scripts/build_news.py"], cwd=ROOT)

    # 5. Optionally commit + push
    if args.commit:
        git_commit_and_push(published_slugs)

    log(f"done — {len(published_slugs)} articles published")
    return 0


if __name__ == "__main__":
    sys.exit(main())
