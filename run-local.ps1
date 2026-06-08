# Run BottleCRM locally without Docker (SQLite, no Redis required)
$ErrorActionPreference = "Stop"

$env:DJANGO_SETTINGS_MODULE = "crm.local_settings"

Write-Host "Starting backend on http://localhost:8001 ..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; `$env:DJANGO_SETTINGS_MODULE='crm.local_settings'; python manage.py runserver 0.0.0.0:8001"

Start-Sleep -Seconds 2

Write-Host "Starting frontend on http://localhost:5173 ..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm run dev -- --host 0.0.0.0 --port 5173"

Write-Host ""
Write-Host "Login: http://localhost:5173/login"
Write-Host "  Email:    admin@localhost"
Write-Host "  Password: admin"
Write-Host ""
Write-Host "API docs: http://localhost:8001/swagger-ui/"
