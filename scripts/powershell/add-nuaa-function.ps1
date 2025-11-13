param(
    [string]$Version = "",
    [switch]$Latest
)

$ErrorActionPreference = 'Stop'

# Determine target version
if ($Latest) {
    $ref = 'main'
}
elseif ([string]::IsNullOrWhiteSpace($Version)) {
    $ref = 'main'
}
else {
    if ($Version -notmatch '^v\d+\.\d+\.\d+$') {
        Write-Error "Version must look like v0.0.0 (got: $Version). Use -Latest to track main."
    }
    $ref = $Version
}

# Choose profile (all hosts for broader availability)
$profilePath = $PROFILE.CurrentUserAllHosts
$profileDir = Split-Path -Parent $profilePath
if (!(Test-Path $profileDir)) { New-Item -ItemType Directory -Path $profileDir | Out-Null }
if (!(Test-Path $profilePath)) { New-Item -ItemType File -Path $profilePath | Out-Null }

# Check uvx availability
$uvx = Get-Command uvx -ErrorAction SilentlyContinue
if (-not $uvx) {
    Write-Warning "'uvx' was not found. Install uv from https://docs.astral.sh/uv/ (Windows MSI), then re-run this script."
}

$fn = @"
function nuaa {
    param([Parameter(ValueFromRemainingArguments = $true)][object[]]$Args)
    uvx --from "git+https://github.com/zophiezlan/nuaa-cli@${ref}" nuaa @Args
}
"@

# Idempotently write the function to profile
$content = Get-Content -Raw -Path $profilePath
if ($content -notmatch 'function\s+nuaa\s*{') {
    Add-Content -Path $profilePath -Value "`n# NUAA CLI (added by add-nuaa-function.ps1 on $(Get-Date -Format o))`n$fn"
    Write-Host "Added 'nuaa' function to $profilePath"
}
else {
    # Replace existing definition
    $updated = $content -replace '(?s)function\s+nuaa\s*\{.*?\}', '# REPLACED BY add-nuaa-function.ps1`n' + $fn
    Set-Content -Path $profilePath -Value $updated
    Write-Host "Updated existing 'nuaa' function in $profilePath"
}

Write-Host "Reload your profile or open a new PowerShell session, then run: nuaa version"
