# TP Project - install required tools via winget
# Run in PowerShell AS ADMINISTRATOR:
#   Set-ExecutionPolicy -Scope Process Bypass -Force
#   .\scripts\install_tools.ps1

$ErrorActionPreference = "Stop"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " TP Project - Tool installer (Miniconda + Docker Desktop)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

function Test-Command($name) {
    return [bool](Get-Command $name -ErrorAction SilentlyContinue)
}

Write-Host "[check] git:        $(if (Test-Command git) { git --version } else { 'NOT FOUND' })"
Write-Host "[check] python:     $(if (Test-Command python) { python --version } else { 'NOT FOUND' })"
Write-Host "[check] conda:      $(if (Test-Command conda) { conda --version } else { 'NOT FOUND' })"
Write-Host "[check] docker:     $(if (Test-Command docker) { docker --version } else { 'NOT FOUND' })"
Write-Host ""

$winget = Get-Command winget -ErrorAction SilentlyContinue
if (-not $winget) {
    Write-Host "[ERROR] winget not found. Install App Installer from Microsoft Store." -ForegroundColor Red
    exit 1
}

if (-not (Test-Command conda)) {
    Write-Host "[install] Miniconda3 (required for week 1 setup_env.bat)..." -ForegroundColor Yellow
    winget install Anaconda.Miniconda3 --source winget --accept-package-agreements --accept-source-agreements
    Write-Host "[info] After install: CLOSE and REOPEN terminal, then run: conda --version" -ForegroundColor Green
} else {
    Write-Host "[skip] conda already installed" -ForegroundColor Green
}

if (-not (Test-Command docker)) {
    Write-Host "[install] Docker Desktop (required for weeks 10-12)..." -ForegroundColor Yellow
    Write-Host "[info] Docker may require reboot and WSL2 enable." -ForegroundColor Yellow
    winget install Docker.DockerDesktop --source winget --accept-package-agreements --accept-source-agreements
} else {
    Write-Host "[skip] docker already installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "Manual downloads (if winget fails):" -ForegroundColor Cyan
Write-Host "  Miniconda: https://docs.conda.io/en/latest/miniconda.html"
Write-Host "  Docker:    https://www.docker.com/products/docker-desktop/"
Write-Host ""
Write-Host "After reboot, verify:" -ForegroundColor Cyan
Write-Host "  conda --version"
Write-Host "  docker compose version"
