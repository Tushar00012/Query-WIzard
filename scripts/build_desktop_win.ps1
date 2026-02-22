$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "[1/5] Building frontend"
Set-Location frontend
npm ci
npm run build
Set-Location ..

Write-Host "[2/5] Installing desktop Python dependencies"
python -m pip install -r requirements-desktop.txt

Write-Host "[3/5] Building Windows executable"
pyinstaller --noconfirm --onefile --windowed --name QueryWizard `
  --add-data "frontend/dist;frontend/dist" `
  --add-data "backend/mysql_schema.json;backend" `
  desktop_launcher.py

Write-Host "[4/5] Building Windows installer (Inno Setup)"
$iscc = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if (Test-Path $iscc) {
  & $iscc "installer/windows/QueryWizard.iss"
  Write-Host "Installer output: dist/installer/QueryWizard-Setup.exe"
} else {
  Write-Host "Inno Setup not found at '$iscc'. Install Inno Setup 6 to build installer."
}

Write-Host "[5/5] Build output: dist/QueryWizard.exe"
