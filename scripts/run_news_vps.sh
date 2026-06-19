#!/usr/bin/env bash
# run_news_vps.sh — canonieke wekelijkse nieuws-runner op de VPS (185.107.90.42).
#
# Waarom op de VPS i.p.v. de Mac: de Mac-launchd-route is door macOS-rechten (TCC)
# geblokkeerd, dus draaide nieuws nooit onbeheerd. De VPS staat altijd aan en kan
# schrijven via de `claude` CLI (Claude Code-abonnement, self-refreshing auth).
#
# End-to-end: git pull -> genereer+commit+push via abonnement -> DEPLOY naar Vercel
# (push alleen deployt NIET op dit project) -> luide foutdetectie (exit != 0 bij
# stille mislukking). Wordt aangeroepen door botlease-news.service (timer: vr 17:00).
#
# Deploy vereist VERCEL_TOKEN in .env. Zonder token: artikelen gaan wel naar GitHub,
# maar de deploy wordt overgeslagen met een duidelijke melding (geen stille no-op).
set -uo pipefail

REPO="/root/botlease-news"
PYTHON="$(command -v python3)"
export HOME="/root"
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

cd "$REPO" || { echo "FATAL: kan niet naar $REPO"; exit 1; }

# Secrets + config (GH_REPO_TOKEN voor push, VERCEL_TOKEN voor deploy, OpenRouter als vangnet)
set -a; [ -f .env ] && . ./.env; set +a

MAX_ARTICLES="${1:-1}"   # 1 vers artikel per week (SEO-strategie: gestaag, geen dump)

LOGDIR="$REPO/logs"; mkdir -p "$LOGDIR"
TS="$(date +%Y%m%d-%H%M%S)"
LOG="$LOGDIR/newsbot-$TS.log"

{
  echo "===== news run $TS (max=$MAX_ARTICLES) ====="
  echo "whoami=$(whoami) python=$PYTHON claude=$(command -v claude || echo MISSING) vercel=$(command -v vercel || echo MISSING)"

  # 1) Sync met origin. De tree hoort schoon te zijn (de bot commit zijn eigen
  #    state); zo niet, dan stash zodat de rebase niet vastloopt.
  git stash -q 2>/dev/null || true
  git pull --rebase --quiet || echo "WARN: git pull faalde"

  # 2) Genereer + bouw + commit + push. Schrijft primair via de claude CLI
  #    (abonnement). --rebuild zodat de HTML mee gecommit wordt en live kan.
  "$PYTHON" scripts/news_bot.py --commit --rebuild --max="$MAX_ARTICLES"
  echo "news-bot exit: $?"

  # 3) Bijrol-bots (rankings + analytics). Niet kritiek; falen mag de run niet stoppen.
  [ -f scripts/rank_bot.py ]      && "$PYTHON" scripts/rank_bot.py --commit      2>&1 | tail -3 || true
  [ -f scripts/analytics_bot.py ] && "$PYTHON" scripts/analytics_bot.py --commit 2>&1 | tail -3 || true
} >"$LOG" 2>&1

# 4) Deploy — alleen als er daadwerkelijk iets gepubliceerd EN gepusht is.
if grep -qE "done — [0-9]+ articles published" "$LOG" && ! grep -q "WARN push failed" "$LOG"; then
  {
    if [ -n "${VERCEL_TOKEN:-}" ]; then
      echo "=== deploy origin/master naar Vercel ==="
      # .vercel-link herstellen als een her-clone 'm wegvaagde (buiten git bewaard).
      [ -f .vercel/project.json ] || { mkdir -p .vercel; cp /root/botlease-vercel-project.json .vercel/project.json 2>/dev/null; }
      git fetch origin -q
      DWT="$REPO/.deploy-worktree"
      rm -rf "$DWT"; git worktree prune
      if git worktree add --detach "$DWT" origin/master >/dev/null 2>&1; then
        cp -r .vercel "$DWT/.vercel" 2>/dev/null
        ( cd "$DWT" && vercel --prod --yes --token "$VERCEL_TOKEN" )
        git worktree remove "$DWT" --force
      else
        echo "WARN deploy worktree add faalde"
      fi
    else
      echo "DEPLOY OVERGESLAGEN: geen VERCEL_TOKEN in .env. Artikel staat wel op GitHub."
      echo "  Fix (eenmalig): voeg VERCEL_TOKEN=... toe aan $REPO/.env (token via vercel.com/account/tokens)."
    fi
  } >>"$LOG" 2>&1
fi

# 5) Luide resultaatdetectie (de bot exit 0 ook bij een stille no-op).
if grep -q "WARN push failed" "$LOG"; then
  STATUS=1; echo "RESULT: FAILURE — artikel gegenereerd maar git push faalde." >>"$LOG"
elif grep -qE "done — [0-9]+ articles published" "$LOG"; then
  if grep -q "Aliased: https://botlease.nl" "$LOG"; then
    STATUS=0; echo "RESULT: SUCCESS — gepubliceerd + live gedeployed." >>"$LOG"
  elif [ -z "${VERCEL_TOKEN:-}" ]; then
    STATUS=0; echo "RESULT: OK — gepusht naar GitHub. Deploy wacht op VERCEL_TOKEN (zie log)." >>"$LOG"
  else
    STATUS=1; echo "RESULT: PARTIAL — gepusht maar Vercel-deploy niet bevestigd. Handmatig: vercel --prod --yes --token \$VERCEL_TOKEN." >>"$LOG"
  fi
elif grep -qiE "no .*candidates|nothing to do" "$LOG"; then
  STATUS=0; echo "RESULT: OK (geen verse kandidaten deze week)." >>"$LOG"
else
  STATUS=1; echo "RESULT: FAILURE — 0 gepubliceerd (mogelijk LLM-auth dood). Check log." >>"$LOG"
fi

ln -sf "$LOG" "$LOGDIR/newsbot-latest.log"
tail -3 "$LOG"
exit $STATUS
