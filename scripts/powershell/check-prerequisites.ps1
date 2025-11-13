#!/usr/bin/env pwsh

# Consolidated prerequisite checking script (PowerShell)
#
# This script provides unified prerequisite checking for the NUAA project kit.
# It replaces the functionality previously spread across multiple scripts.
#
# Usage: ./check-prerequisites.ps1 [OPTIONS]
#
# OPTIONS:
#   -Json               Output in JSON format
#   -RequireTasks       Require tasks.md to exist (for implementation phase)
#   -IncludeTasks       Include tasks.md in AVAILABLE_DOCS list
#   -PathsOnly          Only output path variables (no validation)
#   -Help, -h           Show help message

[CmdletBinding()]
param(
    [switch]$Json,
    [switch]$RequireDesign,
    [switch]$IncludeProposal,
    [switch]$PathsOnly,
    [switch]$Help
)

$ErrorActionPreference = 'Stop'

# Show help if requested
if ($Help) {
    Write-Output @"
Usage: check-prerequisites.ps1 [OPTIONS]

Consolidated prerequisite checking for the NUAA project kit.

OPTIONS:
  -Json               Output in JSON format
  -RequireDesign      Require program-design.md to exist
  -IncludeProposal    Include proposal.md in AVAILABLE_DOCS list
  -PathsOnly          Only output path variables (no prerequisite validation)
  -Help, -h           Show this help message

EXAMPLES:
  # Check design prerequisites (proposal.md required)
  .\check-prerequisites.ps1 -Json
  
  # Check implementation prerequisites (proposal.md + program-design.md required)
  .\check-prerequisites.ps1 -Json -RequireDesign -IncludeProposal
  
  # Get feature paths only (no validation)
  .\check-prerequisites.ps1 -PathsOnly

"@
    exit 0
}

# Source common functions
. "$PSScriptRoot/common.ps1"

# Get feature paths and validate branch
$paths = Get-FeaturePathsEnv

if (-not (Test-FeatureBranch -Branch $paths.CURRENT_BRANCH -HasGit:$paths.HAS_GIT)) { 
    exit 1 
}

# If paths-only mode, output paths and exit (support combined -Json -PathsOnly)
if ($PathsOnly) {
    if ($Json) {
        [PSCustomObject]@{
            REPO_ROOT        = $paths.REPO_ROOT
            BRANCH           = $paths.CURRENT_BRANCH
            FEATURE_DIR      = $paths.FEATURE_DIR
            PROPOSAL         = $paths.PROPOSAL
            DESIGN           = $paths.DESIGN
            LOGIC_MODEL      = $paths.LOGIC_MODEL
            IMPACT_FRAMEWORK = $paths.IMPACT_FRAMEWORK
        } | ConvertTo-Json -Compress
    }
    else {
        Write-Output "REPO_ROOT: $($paths.REPO_ROOT)"
        Write-Output "BRANCH: $($paths.CURRENT_BRANCH)"
        Write-Output "FEATURE_DIR: $($paths.FEATURE_DIR)"
        Write-Output "PROPOSAL: $($paths.PROPOSAL)"
        Write-Output "DESIGN: $($paths.DESIGN)"
        Write-Output "LOGIC_MODEL: $($paths.LOGIC_MODEL)"
        Write-Output "IMPACT_FRAMEWORK: $($paths.IMPACT_FRAMEWORK)"
    }
    exit 0
}

# Validate required directories and files
if (-not (Test-Path $paths.FEATURE_DIR -PathType Container)) {
    Write-Output "ERROR: Feature directory not found: $($paths.FEATURE_DIR)"
    Write-Output "Run 'nuaa propose' first to create the feature structure."
    exit 1
}

if (-not (Test-Path $paths.PROPOSAL -PathType Leaf)) {
    Write-Output "ERROR: proposal.md not found in $($paths.FEATURE_DIR)"
    Write-Output "Run 'nuaa propose' first to create the proposal."
    exit 1
}

# Check for program-design.md if required
if ($RequireDesign -and -not (Test-Path $paths.DESIGN -PathType Leaf)) {
    Write-Output "ERROR: program-design.md not found in $($paths.FEATURE_DIR)"
    Write-Output "Run 'nuaa design' first to create the program design."
    exit 1
}

# Build list of available documents
$docs = @()

# Always check these optional docs
if (Test-Path $paths.RESEARCH) { $docs += 'research.md' }
if (Test-Path $paths.DATA_MODEL) { $docs += 'data-model.md' }

# Check contracts directory (only if it exists and has files)
if ((Test-Path $paths.CONTRACTS_DIR) -and (Get-ChildItem -Path $paths.CONTRACTS_DIR -ErrorAction SilentlyContinue | Select-Object -First 1)) { 
    $docs += 'contracts/' 
}

if (Test-Path $paths.QUICKSTART) { $docs += 'quickstart.md' }

# Include proposal.md if requested and it exists
if ($IncludeProposal -and (Test-Path $paths.PROPOSAL)) { 
    $docs += 'proposal.md' 
}

# Output results
if ($Json) {
    # JSON output
    [PSCustomObject]@{ 
        FEATURE_DIR    = $paths.FEATURE_DIR
        AVAILABLE_DOCS = $docs 
    } | ConvertTo-Json -Compress
}
else {
    # Text output
    Write-Output "FEATURE_DIR:$($paths.FEATURE_DIR)"
    Write-Output "AVAILABLE_DOCS:"
    
    # Show status of each potential document
    Test-FileExists -Path $paths.RESEARCH -Description 'research.md' | Out-Null
    Test-FileExists -Path $paths.DATA_MODEL -Description 'data-model.md' | Out-Null
    Test-DirHasFiles -Path $paths.CONTRACTS_DIR -Description 'contracts/' | Out-Null
    Test-FileExists -Path $paths.QUICKSTART -Description 'quickstart.md' | Out-Null
    
    if ($IncludeProposal) {
        Test-FileExists -Path $paths.PROPOSAL -Description 'proposal.md' | Out-Null
    }
}
