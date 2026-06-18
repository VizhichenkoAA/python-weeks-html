# Fix WSL2 + Ubuntu for Docker Desktop (run as Administrator)
#   Set-ExecutionPolicy -Scope Process Bypass -Force
#   cd "C:\Users\Admin\Desktop\Новая папка\tp-project"
#   .\scripts\fix_wsl_docker.ps1

$ErrorActionPreference = "Continue"

function Test-IsAdmin {
    $id = [Security.Principal.WindowsIdentity]::GetCurrent()
    $p = New-Object Security.Principal.WindowsPrincipal($id)
    return $p.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Fix WSL2 + Ubuntu (for Docker Desktop)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-IsAdmin)) {
    Write-Host "[ERROR] Run PowerShell AS ADMINISTRATOR." -ForegroundColor Red
    exit 1
}

Write-Host "[1/7] Enable Windows features..." -ForegroundColor Yellow
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
dism.exe /online /enable-feature /featurename:HypervisorPlatform /all /norestart 2>$null

Write-Host ""
Write-Host "[2/7] Update WSL (--web-download applies to --update, NOT --install)..." -ForegroundColor Yellow
wsl --update --web-download
if ($LASTEXITCODE -ne 0) {
    Write-Host "[WARN] wsl --update --web-download failed, trying --inbox..." -ForegroundColor Yellow
    wsl --update --inbox
}

Write-Host ""
Write-Host "[3/7] Set WSL2 as default..." -ForegroundColor Yellow
wsl --set-default-version 2

Write-Host ""
Write-Host "[4/7] Try: wsl --install -d Ubuntu ..." -ForegroundColor Yellow
wsl --install -d Ubuntu --no-launch
$ubuntuOk = $LASTEXITCODE -eq 0

if (-not $ubuntuOk) {
    Write-Host ""
    Write-Host "[5/7] Fallback: install Ubuntu via direct download (aka.ms)..." -ForegroundColor Yellow
    $dest = Join-Path $env:TEMP "Ubuntu2204.appx"
    Invoke-WebRequest -Uri "https://aka.ms/wslubuntu2204" -OutFile $dest -UseBasicParsing
    Add-AppxPackage $dest
    $ubuntuOk = $LASTEXITCODE -eq 0
} else {
    Write-Host "[5/7] Ubuntu installed via wsl --install (skip fallback)." -ForegroundColor Green
}

Write-Host ""
Write-Host "[6/7] Installed distros:" -ForegroundColor Yellow
wsl -l -v

Write-Host ""
Write-Host "[7/7] WSL status:" -ForegroundColor Yellow
wsl --status

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host " NEXT: REBOOT, then run:  wsl -d Ubuntu" -ForegroundColor Green
Write-Host " (or open 'Ubuntu' from Start menu)" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
