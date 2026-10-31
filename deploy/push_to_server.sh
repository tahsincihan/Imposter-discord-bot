#!/usr/bin/env bash
# Run on your Mac: copies the Imposter bot to the Oracle VM and (re)starts it there.
# Usage: deploy/push_to_server.sh ubuntu@<vm-ip> [path/to/ssh-key]
# Run it again any time you change the code.
set -euo pipefail
HOST="${1:?Usage: deploy/push_to_server.sh ubuntu@<vm-ip> [path/to/ssh-key]}"
KEY="${2:-}"
REMOTE_DIR="imposter"

SSH="ssh -o StrictHostKeyChecking=accept-new"
[ -n "$KEY" ] && SSH="$SSH -i $KEY"
cd "$(dirname "$0")/.."

# Code and .env (the bot keeps no saved data).
rsync -az --delete -e "$SSH" \
  --exclude .git --exclude .venv --exclude __pycache__ --exclude .claude --exclude '*.log' --exclude .DS_Store \
  ./ "$HOST:$REMOTE_DIR/"

$SSH "$HOST" "bash $REMOTE_DIR/deploy/setup_server.sh"
