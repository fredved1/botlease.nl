#!/usr/bin/env bash
# Daily news pipeline: rebuild news pages from articles_data.py, then deploy.
set -euo pipefail
PROJ="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJ"

# Rebuild news pages
python3 scripts/build_news.py

# Sync root index.html with frontend/index.html (Vercel serves frontend/)
cp frontend/index.html index.html 2>/dev/null || true

# Git commit (don't fail if nothing changed)
if ! git diff --quiet || ! git diff --cached --quiet; then
  git add -A
  git commit -m "news: daily article + rebuild $(date +%Y-%m-%d)" --quiet || true
  git push origin master --quiet || true
fi

# Deploy
vercel --prod --yes 2>&1 | tail -5

echo "✅ deployed $(date)"
