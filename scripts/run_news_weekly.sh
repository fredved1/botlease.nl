#!/bin/bash
# run_news_weekly.sh — launchd entrypoint for the BotLease news bot.
#
# End-to-end weekly run: refresh OAuth token -> generate+commit+push articles ->
# DEPLOY the committed origin/master to Vercel (push alone does NOT auto-deploy
# on this project). Robust against silent failures: inspects the log and exits
# NON-ZERO on the failure cases (auth dead / push failed / deploy failed).
set -uo pipefail

REPO="/Users/werk/Documents/Python/botlease.nl"
PYTHON="/usr/local/bin/python3"
# launchd has a minimal PATH; include npm-global (vercel), homebrew, system.
export PATH="$HOME/.npm-global/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export HOME="/Users/werk"
export CLAUDE_CREDS_PATH="$HOME/.claude/.credentials.json"
export CLAUDE_REFRESH_SCRIPT="$REPO/scripts/refresh_token_wrapper.sh"  # bot's own 401-path can self-heal
# Optional OpenRouter fallback (only used when the creds file is ABSENT):
# export OPENROUTER_API_KEY="sk-or-v1-..."

MAX_ARTICLES="${1:-3}"   # default 3 per weekly run; override: run_news_weekly.sh 4

LOGDIR="$REPO/logs"
mkdir -p "$LOGDIR"
TS="$(date +%Y%m%d-%H%M%S)"
LOG="$LOGDIR/newsbot-$TS.log"

{
  echo "===== news bot run $TS (max=$MAX_ARTICLES) ====="
  echo "whoami=$(whoami) python=$PYTHON vercel=$(command -v vercel || echo MISSING)"

  # 1) Best-effort local token refresh before the run.
  if "$PYTHON" "$REPO/scripts/refresh_claude_token.py"; then
    echo "refresh: ok / not needed"
  else
    echo "refresh: FAILED (continuing — run will detect if auth is dead)"
  fi

  # 2) Generate + commit + push.
  cd "$REPO" || { echo "FATAL: cannot cd to $REPO"; exit 1; }
  "$PYTHON" scripts/news_bot.py --commit --max="$MAX_ARTICLES"
  echo "bot exit code: $?"
} >"$LOG" 2>&1

# 3) Deploy — ONLY if the bot published AND pushed. Deploy the committed
#    origin/master from a clean worktree, NEVER the (possibly dirty) working tree.
if grep -qE "done — [0-9]+ articles published" "$LOG" && ! grep -q "WARN push failed" "$LOG"; then
  {
    echo "=== deploy origin/master to Vercel ==="
    git -C "$REPO" fetch origin -q
    DWT="$REPO/.deploy-worktree"
    rm -rf "$DWT"; git -C "$REPO" worktree prune
    if git -C "$REPO" worktree add --detach "$DWT" origin/master >/dev/null 2>&1; then
      cp -r "$REPO/.vercel" "$DWT/.vercel" 2>/dev/null
      ( cd "$DWT" && vercel --prod --yes )
      git -C "$REPO" worktree remove "$DWT" --force
    else
      echo "WARN deploy worktree add failed"
    fi
  } >>"$LOG" 2>&1
fi

# 4) Loud result detection (the bot exits 0 even on a silent no-op).
if grep -q "WARN push failed" "$LOG"; then
  STATUS=1; echo "RESULT: FAILURE — articles generated but git push failed (check SSH key / network)." >>"$LOG"
elif grep -qE "done — [0-9]+ articles published" "$LOG"; then
  if grep -q "Aliased: https://botlease.nl" "$LOG"; then
    STATUS=0; echo "RESULT: SUCCESS — articles published + deployed live." >>"$LOG"
  else
    STATUS=1; echo "RESULT: PARTIAL — articles pushed to origin but Vercel deploy did not confirm. Deploy manually: cd $REPO && vercel --prod --yes (from a clean checkout)." >>"$LOG"
  fi
elif grep -q "nothing to do." "$LOG"; then
  STATUS=0; echo "RESULT: OK (no fresh candidates this week)." >>"$LOG"
elif grep -q "no articles published this run" "$LOG"; then
  STATUS=1; echo "RESULT: FAILURE — candidates existed but 0 published (likely expired/blocked OAuth token). Fix: $PYTHON $REPO/scripts/refresh_claude_token.py --force (or open Claude Code), then re-run." >>"$LOG"
else
  STATUS=1; echo "RESULT: FAILURE — unexpected (bot may have crashed). See log above." >>"$LOG"
fi

ln -sf "$LOG" "$LOGDIR/newsbot-latest.log"
exit $STATUS
