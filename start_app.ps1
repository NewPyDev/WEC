# Django Ecommerce Inventory Manager - PowerShell Launcher
# This script starts the Django app without requiring a virtual environment

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "    Django Ecommerce Inventory Manager" -ForegroundColor Cyan  
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting Django development server..." -ForegroundColor Green
Write-Host ""
Write-Host "App will be available at: http://localhost:8000" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Change to script directory
Set-Location -Path $PSScriptRoot

# Check if manage.py exists
if (-not (Test-Path "manage.py")) {
    Write-Host "ERROR: manage.py not found in current directory!" -ForegroundColor Red
    Write-Host "Make sure this script is in your Django project folder." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Python is available
try {
    $pythonVersion = python --version
    Write-Host "Found Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python not found! Please install Python first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Run Django development server
try {
    python manage.py runserver 0.0.0.0:8000
} catch {
    Write-Host "Error starting Django server!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

Write-Host ""
Write-Host "Server stopped." -ForegroundColor Yellow
Read-Host "Press Enter to exit"
