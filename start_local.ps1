Write-Host "IDEPocket Quick Start..." -ForegroundColor Cyan

if (-not (Test-Path "Backend\.env")) {
    Write-Host ".env file not found. Copying .env.example..." -ForegroundColor Yellow
    Copy-Item "Backend\.env.example" "Backend\.env"
    Write-Host "Please configure your API keys in Backend\.env and restart the script." -ForegroundColor Red
    exit 1
}

Write-Host "Installing dependencies..." -ForegroundColor Cyan
pip install -e ./shared
pip install -r Backend\requirements.txt
pip install -r Terminal_Agent\requirements.txt

Write-Host "Starting Backend in background..." -ForegroundColor Cyan
Start-Process -FilePath "python" -ArgumentList "Backend\main.py" -WindowStyle Minimized

Write-Host "Starting Terminal Agent..." -ForegroundColor Cyan
python Terminal_Agent\main.py
