#!/usr/bin/env pwsh
# Setup implementation plan for a feature

[CmdletBinding()]
param(
    [switch]$Json,
    [switch]$Help
)

$ErrorActionPreference = 'Stop'

# Show help if requested
if ($Help) {
    Write-Output "Usage: ./setup-plan.ps1 [-Json] [-Help]"
    Write-Output "  -Json     Output results in JSON format"
    Write-Output "  -Help     Show this help message"
    exit 0
}

# Load common functions
. "$PSScriptRoot/common.ps1"

# Get all paths and variables from common functions
$paths = Get-FeaturePathsEnv

# Check if we're on a proper feature branch (only for git repos)
if (-not (Test-FeatureBranch -Branch $paths.CURRENT_BRANCH -HasGit $paths.HAS_GIT)) { 
    exit 1 
}

# Ensure the feature directory exists
New-Item -ItemType Directory -Path $paths.FEATURE_DIR -Force | Out-Null

# Copy design template if it exists, otherwise note it or create empty file
$template = Resolve-NuaaTemplatePath -RelativePath 'program-design.md' -RepoRoot $paths.REPO_ROOT
if (Test-Path $template) { 
    Copy-Item $template $paths.DESIGN -Force
    Write-Output "Copied program design template to $($paths.DESIGN)"
}
else {
    Write-Warning "Program design template not found at $template"
    # Create a basic design file if template doesn't exist
    New-Item -ItemType File -Path $paths.DESIGN -Force | Out-Null
}

# Output results
if ($Json) {
    $result = [PSCustomObject]@{ 
        FEATURE_SPEC = $paths.PROPOSAL
        DESIGN       = $paths.DESIGN
        FEATURE_DIR  = $paths.FEATURE_DIR
        BRANCH       = $paths.CURRENT_BRANCH
        HAS_GIT      = $paths.HAS_GIT
    }
    $result | ConvertTo-Json -Compress
}
else {
    Write-Output "PROPOSAL: $($paths.PROPOSAL)"
    Write-Output "DESIGN: $($paths.DESIGN)"
    Write-Output "FEATURE_DIR: $($paths.FEATURE_DIR)"
    Write-Output "BRANCH: $($paths.CURRENT_BRANCH)"
    Write-Output "HAS_GIT: $($paths.HAS_GIT)"
}
