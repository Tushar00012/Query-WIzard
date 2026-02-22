$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "[1/4] Building frontend"
Set-Location frontend
npm ci
npm run build
Set-Location ..

Write-Host "[2/4] Installing desktop Python dependencies"
python -m pip install -r requirements-desktop.txt

Write-Host "[3/4] Building Windows executable"
pyinstaller --noconfirm --onefile --windowed --name QueryWizard `
  --add-data "frontend/dist;frontend/dist" `
  --add-data "backend/mysql_schema.json;backend" `
  desktop_launcher.py

Write-Host "[4/4] Build output: dist/QueryWizard.exe"
