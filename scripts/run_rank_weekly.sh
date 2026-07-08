#!/bin/bash
# run_rank_weekly.sh — launchd entrypoint voor de BotLease rank-bot.
# Draait op Thomas' Mac (residentieel IP; vanaf de VPS/datacenter blokkeert DDG harder).
# Meet wekelijks de posities, commit seo/seo_data.json + dashboard, en pusht.
set -uo pipefail

REPO="/Users/werk/Documents/Python/botlease.nl"
PYTHON="/usr/local/bin/python3"
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export HOME="/Users/werk"

LOGDIR="$REPO/logs"; mkdir -p "$LOGDIR"
TS="$(date +%Y%m%d-%H%M%S)"; LOG="$LOGDIR/rankbot-$TS.log"

{
  echo "===== rank bot run $TS ====="
  cd "$REPO" || { echo "FATAL: cannot cd to $REPO"; exit 1; }
  "$PYTHON" scripts/rank_bot.py --commit
  echo "bot exit code: $?"
  git -C "$REPO" push origin master && echo "push: ok" || echo "WARN push failed"
} >"$LOG" 2>&1

ln -sf "$LOG" "$LOGDIR/rankbot-latest.log"
