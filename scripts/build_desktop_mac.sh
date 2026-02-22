#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

echo "[1/4] Building frontend"
cd frontend
npm ci
npm run build
cd ..

echo "[2/4] Installing desktop Python dependencies"
python3 -m pip install -r requirements-desktop.txt

echo "[3/4] Building macOS app"
pyinstaller --noconfirm --onefile --windowed --name QueryWizard \
  --add-data "frontend/dist:frontend/dist" \
  --add-data "backend/mysql_schema.json:backend" \
  desktop_launcher.py

echo "[4/4] Build output: dist/QueryWizard"
