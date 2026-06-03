#!/bin/bash
# Tiny shim so the news bot's in-process 401-retry path (CLAUDE_REFRESH_SCRIPT)
# can also force-refresh the OAuth token mid-run.
exec /usr/local/bin/python3 "$(cd "$(dirname "$0")" && pwd)/refresh_claude_token.py" --force
