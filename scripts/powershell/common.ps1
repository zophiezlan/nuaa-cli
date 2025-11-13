#!/usr/bin/env pwsh
# Common PowerShell functions analogous to common.sh

function Get-RepoRoot {
    try {
        $result = git rev-parse --show-toplevel 2>$null
        if ($LASTEXITCODE -eq 0) {
            return $result
        }
    }
    catch {
        # Git command failed
    }
    
    # Fall back to script location for non-git repos
    return (Resolve-Path (Join-Path $PSScriptRoot "../../..")).Path
}

function Get-NuaaTemplateRoot {
    param(
        [string]$RepoRoot = (Get-RepoRoot)
    )

    $candidates = @(
        Join-Path $RepoRoot '.nuaa/templates',
        Join-Path $RepoRoot 'nuaa-kit/templates'
    )

    foreach ($candidate in $candidates) {
        if (Test-Path $candidate -PathType Container) {
            return $candidate
        }
    }

    return $null
}

function Resolve-NuaaTemplatePath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RelativePath,
        [string]$RepoRoot = (Get-RepoRoot)
    )

    $root = Get-NuaaTemplateRoot -RepoRoot $RepoRoot
    if ($root) {
        return (Join-Path $root $RelativePath)
    }

    # Fallback preserves previous behavior for callers that expect nuaa-kit paths
    $fallbackRoot = Join-Path $RepoRoot 'nuaa-kit/templates'
    return (Join-Path $fallbackRoot $RelativePath)
}

function Get-CurrentBranch {
    # First check if NUAA_FEATURE environment variable is set
    if ($env:NUAA_FEATURE) {
        return $env:NUAA_FEATURE
    }
    
    # Then check git if available
    try {
        $result = git rev-parse --abbrev-ref HEAD 2>$null
        if ($LASTEXITCODE -eq 0) {
            return $result
        }
    }
    catch {
        # Git command failed
    }
    
    # For non-git repos, try to find the latest feature directory
    $repoRoot = Get-RepoRoot
    $featuresDir = Join-Path $repoRoot "nuaa"
    
    if (Test-Path $featuresDir) {
        $latestFeature = ""
        $highest = 0
        
        Get-ChildItem -Path $featuresDir -Directory | ForEach-Object {
            if ($_.Name -match '^(\d{3})-') {
                $num = [int]$matches[1]
                if ($num -gt $highest) {
                    $highest = $num
                    $latestFeature = $_.Name
                }
            }
        }
        
        if ($latestFeature) {
            return $latestFeature
        }
    }
    
    # Final fallback
    return "main"
}

function Test-HasGit {
    try {
        git rev-parse --show-toplevel 2>$null | Out-Null
        return ($LASTEXITCODE -eq 0)
    }
    catch {
        return $false
    }
}

function Test-FeatureBranch {
    param(
        [string]$Branch,
        [bool]$HasGit = $true
    )
    
    # For non-git repos, we can't enforce branch naming but still provide output
    if (-not $HasGit) {
        Write-Warning "[nuaa] Warning: Git repository not detected; skipped branch validation"
        return $true
    }
    
    if ($Branch -notmatch '^[0-9]{3}-') {
        Write-Output "ERROR: Not on a feature branch. Current branch: $Branch"
        Write-Output "Feature branches should be named like: 001-feature-name"
        return $false
    }
    return $true
}

function Get-FeatureDir {
    param([string]$RepoRoot, [string]$Branch)
    Join-Path $RepoRoot "nuaa/$Branch"
}

function Get-FeaturePathsEnv {
    $repoRoot = Get-RepoRoot
    $currentBranch = Get-CurrentBranch
    $hasGit = Test-HasGit
    $featureDir = Get-FeatureDir -RepoRoot $repoRoot -Branch $currentBranch
    
    [PSCustomObject]@{
        REPO_ROOT        = $repoRoot
        CURRENT_BRANCH   = $currentBranch
        HAS_GIT          = $hasGit
        FEATURE_DIR      = $featureDir
        PROPOSAL         = Join-Path $featureDir 'proposal.md'
        DESIGN           = Join-Path $featureDir 'program-design.md'
        LOGIC_MODEL      = Join-Path $featureDir 'logic-model.md'
        IMPACT_FRAMEWORK = Join-Path $featureDir 'impact-framework.md'
        RESEARCH         = Join-Path $featureDir 'research.md'
        DATA_MODEL       = Join-Path $featureDir 'data-model.md'
        QUICKSTART       = Join-Path $featureDir 'quickstart.md'
        CONTRACTS_DIR    = Join-Path $featureDir 'contracts'
    }
}

function Test-FileExists {
    param([string]$Path, [string]$Description)
    if (Test-Path -Path $Path -PathType Leaf) {
        Write-Output "  ✓ $Description"
        return $true
    }
    else {
        Write-Output "  ✗ $Description"
        return $false
    }
}

function Test-DirHasFiles {
    param([string]$Path, [string]$Description)
    if ((Test-Path -Path $Path -PathType Container) -and (Get-ChildItem -Path $Path -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer } | Select-Object -First 1)) {
        Write-Output "  ✓ $Description"
        return $true
    }
    else {
        Write-Output "  ✗ $Description"
        return $false
    }
}

