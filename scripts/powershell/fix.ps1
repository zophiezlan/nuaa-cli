# Quick fix script - Auto-formats code and fixes common issues
# Usage: .\scripts\powershell\fix.ps1

$ErrorActionPreference = "Continue"

Write-Host "🔧 NUAA CLI Auto-Fix Script" -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor Cyan
Write-Host ""

# Change to repo root
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent (Split-Path -Parent $scriptPath)
Set-Location $repoRoot

Write-Host "🎨 Step 1/3: Auto-formatting with black..." -ForegroundColor Yellow
black src/nuaa_cli tests scripts/python
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Black formatting complete!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Black had some issues" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "🔍 Step 2/3: Auto-fixing with ruff..." -ForegroundColor Yellow
ruff check --fix src/nuaa_cli tests scripts/python
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Ruff fixes complete!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Ruff had some issues (this is usually okay)" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "🔒 Step 3/3: Security scan..." -ForegroundColor Yellow
bandit -r src/nuaa_cli -f screen
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Security scan complete!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Security scan had some findings" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "✨ All fixes applied!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  • Review changes: git diff"
Write-Host "  • Run tests: pytest"
Write-Host "  • Commit changes: git add . && git commit -m 'fix: Apply auto-formatting and fixes'"
