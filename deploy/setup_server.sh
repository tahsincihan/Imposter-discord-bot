#!/usr/bin/env bash
# Runs on the Oracle VM (Ubuntu), inside the bot's folder. push_to_server.sh calls it for you.
# Installs Python packages, then installs and (re)starts the bot as a background service.
set -euo pipefail
APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$APP_DIR"

if [ ! -f .env ]; then
  echo "Missing $APP_DIR/.env (needs DISCORD_BOT)." >&2
  exit 1
fi

if [ ! -d .venv ]; then
  if ! command -v python3 >/dev/null || ! python3 -m venv --help >/dev/null 2>&1; then
    echo "First run: installing Python..."
    sudo apt-get update -y
    sudo apt-get install -y python3 python3-venv python3-pip
  fi
  python3 -m venv .venv || { sudo apt-get install -y python3-venv && python3 -m venv .venv; }
  .venv/bin/pip install -q --upgrade pip
fi
.venv/bin/pip install -q -r deploy/requirements-server.txt

sed -e "s|__USER__|$(whoami)|" -e "s|__DIR__|$APP_DIR|g" deploy/imposter.service \
  | sudo tee /etc/systemd/system/imposter.service >/dev/null
sudo systemctl daemon-reload
sudo systemctl enable imposter >/dev/null 2>&1
sudo systemctl restart imposter

sleep 8
sudo journalctl -u imposter -n 15 --no-pager
if systemctl is-active --quiet imposter; then
  echo "✅ Imposter bot is running on the server."
else
  echo "❌ Imposter bot didn't start. Logs are above." >&2
  exit 1
fi
