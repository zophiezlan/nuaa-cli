#!/usr/bin/env pwsh
#requires -Version 7.0

<#
.SYNOPSIS
    Build NUAA template release archives for each supported AI assistant and script type.

.DESCRIPTION
    create-release-packages.ps1 (workflow-local)
    Build NUAA template release archives for each supported AI assistant and script type.

.PARAMETER Version
    Version string with leading 'v' (e.g., v0.2.0)

.PARAMETER Agents
    Comma or space separated subset of agents to build (default: all)
    Valid agents: claude, gemini, copilot, cursor-agent, qwen, opencode, windsurf, codex, kilocode, auggie, roo, codebuddy, amp, q

.PARAMETER Scripts
    Comma or space separated subset of script types to build (default: both)
    Valid scripts: sh, ps

.EXAMPLE
    .\create-release-packages.ps1 -Version v0.2.0

.EXAMPLE
    .\create-release-packages.ps1 -Version v0.2.0 -Agents claude,copilot -Scripts sh

.EXAMPLE
    .\create-release-packages.ps1 -Version v0.2.0 -Agents claude -Scripts ps
#>

param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Version,

    [Parameter(Mandatory = $false)]
    [string]$Agents = "",

    [Parameter(Mandatory = $false)]
    [string]$Scripts = ""
)

$ErrorActionPreference = "Stop"

# Validate version format
if ($Version -notmatch '^v\d+\.\d+\.\d+$') {
    Write-Error "Version must look like v0.0.0"
    exit 1
}

Write-Host "Building release packages for $Version"
$script:NEW_VERSION = $Version

# Create and use .genreleases directory for all build artifacts
$GenReleasesDir = ".genreleases"
if (Test-Path $GenReleasesDir) {
    Remove-Item -Path $GenReleasesDir -Recurse -Force -ErrorAction SilentlyContinue
}
New-Item -ItemType Directory -Path $GenReleasesDir -Force | Out-Null

function ConvertTo-NuaaPath {
    param([string]$Content)

    $Content = $Content -replace '(/?)memory/', '.nuaa/memory/'
    $Content = $Content -replace '(/?)scripts/', '.nuaa/scripts/'
    $Content = $Content -replace '(/?)templates/', '.nuaa/templates/'
    return $Content
}

function New-CommandFile {
    param(
        [string]$Agent,
        [string]$Extension,
        [string]$ArgFormat,
        [string]$OutputDir,
        [string]$ScriptVariant
    )

    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null

    $templates = Get-ChildItem -Path "nuaa-kit/commands/*.md" -File -ErrorAction SilentlyContinue

    foreach ($template in $templates) {
        $name = [System.IO.Path]::GetFileNameWithoutExtension($template.Name)

        # Read file content and normalize line endings
        $fileContent = (Get-Content -Path $template.FullName -Raw) -replace "`r`n", "`n"

        # Extract description from YAML frontmatter
        $description = ""
        if ($fileContent -match '(?m)^description:\s*(.+)$') {
            $description = $matches[1]
        }

        # Extract script command from YAML frontmatter
        $scriptCommand = ""
        if ($fileContent -match "(?m)^\s*${ScriptVariant}:\s*(.+)$") {
            $scriptCommand = $matches[1]
        }

        if ([string]::IsNullOrEmpty($scriptCommand)) {
            Write-Warning "No script command found for $ScriptVariant in $($template.Name)"
            $scriptCommand = "(Missing script command for $ScriptVariant)"
        }

        # Extract agent_script command from YAML frontmatter if present
        $agentScriptCommand = ""
        if ($fileContent -match "(?ms)agent_scripts:.*?^\s*${ScriptVariant}:\s*(.+?)$") {
            $agentScriptCommand = $matches[1].Trim()
        }

        # Replace {SCRIPT} placeholder with the script command
        $body = $fileContent -replace '\{SCRIPT\}', $scriptCommand

        # Replace {AGENT_SCRIPT} placeholder with the agent script command if found
        if (-not [string]::IsNullOrEmpty($agentScriptCommand)) {
            $body = $body -replace '\{AGENT_SCRIPT\}', $agentScriptCommand
        }

        # Remove the scripts: and agent_scripts: sections from frontmatter
        $lines = $body -split "`n"
        $outputLines = @()
        $inFrontmatter = $false
        $skipScripts = $false
        $dashCount = 0

        foreach ($line in $lines) {
            if ($line -match '^---$') {
                $outputLines += $line
                $dashCount++
                if ($dashCount -eq 1) {
                    $inFrontmatter = $true
                }
                else {
                    $inFrontmatter = $false
                }
                continue
            }

            if ($inFrontmatter) {
                if ($line -match '^(scripts|agent_scripts):$') {
                    $skipScripts = $true
                    continue
                }
                if ($line -match '^[a-zA-Z].*:' -and $skipScripts) {
                    $skipScripts = $false
                }
                if ($skipScripts -and $line -match '^\s+') {
                    continue
                }
            }

            $outputLines += $line
        }

        $body = $outputLines -join "`n"

        # Apply other substitutions
        $body = $body -replace '\{ARGS\}', $ArgFormat
        $body = $body -replace '__AGENT__', $Agent
        $body = ConvertTo-NuaaPath -Content $body

        # Generate output file based on extension
        $outputFile = Join-Path $OutputDir "nuaa.$name.$Extension"

        switch ($Extension) {
            'toml' {
                $body = $body -replace '\\', '\\'
                $output = "description = `"$description`"`n`nprompt = `"`"`"`n$body`n`"`"`""
                Set-Content -Path $outputFile -Value $output -NoNewline
            }
            'md' {
                Set-Content -Path $outputFile -Value $body -NoNewline
            }
            'agent.md' {
                Set-Content -Path $outputFile -Value $body -NoNewline
            }
        }
    }
}

function New-CopilotPrompt {
    param(
        [string]$AgentsDir,
        [string]$PromptsDir
    )

    New-Item -ItemType Directory -Path $PromptsDir -Force | Out-Null

    $agentFiles = Get-ChildItem -Path "$AgentsDir/nuaa.*.agent.md" -File -ErrorAction SilentlyContinue

    foreach ($agentFile in $agentFiles) {
        $basename = $agentFile.Name -replace '\.agent\.md$', ''
        $promptFile = Join-Path $PromptsDir "$basename.prompt.md"

        $agentContent = Get-Content -Path $agentFile.FullName -Raw
        $frontMatterLines = @(
            '---',
            "agent: $basename",
            "version: $NEW_VERSION",
            "generated_from: .github/agents/$basename.agent.md",
            '---',
            ''
        )

        $promptContent = ($frontMatterLines -join [Environment]::NewLine) + $agentContent
        Set-Content -Path $promptFile -Value $promptContent -Encoding utf8
    }
}

function New-ReleaseVariant {
    param(
        [string]$Agent,
        [string]$Script
    )

    $baseDir = Join-Path $GenReleasesDir "sdd-${Agent}-package-${Script}"
    Write-Host "Building $Agent ($Script) package..."
    New-Item -ItemType Directory -Path $baseDir -Force | Out-Null

    # Copy base structure but filter scripts by variant
    $nuaaDir = Join-Path $baseDir ".nuaa"
    New-Item -ItemType Directory -Path $nuaaDir -Force | Out-Null

    # Copy memory directory
    if (Test-Path "memory") {
        Copy-Item -Path "memory" -Destination $nuaaDir -Recurse -Force
        Write-Host "Copied memory -> .nuaa"
    }

    # Only copy the relevant script variant directory
    if (Test-Path "scripts") {
        $scriptsDestDir = Join-Path $nuaaDir "scripts"
        New-Item -ItemType Directory -Path $scriptsDestDir -Force | Out-Null

        switch ($Script) {
            'sh' {
                if (Test-Path "scripts/bash") {
                    Copy-Item -Path "scripts/bash" -Destination $scriptsDestDir -Recurse -Force
                    Write-Host "Copied scripts/bash -> .nuaa/scripts"
                }
            }
            'ps' {
                if (Test-Path "scripts/powershell") {
                    Copy-Item -Path "scripts/powershell" -Destination $scriptsDestDir -Recurse -Force
                    Write-Host "Copied scripts/powershell -> .nuaa/scripts"
                }
            }
        }

        # Copy any script files that aren't in variant-specific directories
        Get-ChildItem -Path "scripts" -File -ErrorAction SilentlyContinue | ForEach-Object {
            Copy-Item -Path $_.FullName -Destination $scriptsDestDir -Force
        }
    }

    # Copy nuaa-kit templates (excluding vscode-settings.json)
    if (Test-Path "nuaa-kit/templates") {
        $templatesDestDir = Join-Path $nuaaDir "templates"
        New-Item -ItemType Directory -Path $templatesDestDir -Force | Out-Null

        Get-ChildItem -Path "nuaa-kit/templates" -File | Where-Object {
            $_.Name -ne 'vscode-settings.json'
        } | ForEach-Object {
            Copy-Item -Path $_.FullName -Destination $templatesDestDir -Force
        }
        Write-Host "Copied nuaa-kit/templates -> .nuaa/templates"
    }

    # Generate agent-specific command files
    $agentData = $AgentsData.($Agent)
    $agentFormat = $agentData.format
    $argPlaceholder = if ($agentFormat -eq 'TOML') { '{{args}}' } else { '$ARGUMENTS' }
    $outputDir = Join-Path $baseDir $agentData.folder
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null

    New-CommandFile -Agent $Agent -Extension $agentFormat.ToLower() -ArgFormat $argPlaceholder -OutputDir $outputDir -ScriptVariant $Script

    # Special handling for certain agents
    if ($Agent -eq 'copilot') {
        $promptsDir = Join-Path $baseDir ".github/prompts"
        New-CopilotPrompt -AgentsDir $outputDir -PromptsDir $promptsDir

        $vscodeDir = Join-Path $baseDir ".vscode"
        New-Item -ItemType Directory -Path $vscodeDir -Force | Out-Null
        if (Test-Path "templates/vscode-settings.json") {
            Copy-Item -Path "templates/vscode-settings.json" -Destination (Join-Path $vscodeDir "settings.json")
        }
    }
    elseif ($Agent -eq 'gemini' -and (Test-Path "agent_templates/gemini/GEMINI.md")) {
        Copy-Item -Path "agent_templates/gemini/GEMINI.md" -Destination (Join-Path $baseDir "GEMINI.md")
    }
    elseif ($Agent -eq 'qwen' -and (Test-Path "agent_templates/qwen/QWEN.md")) {
        Copy-Item -Path "agent_templates/qwen/QWEN.md" -Destination (Join-Path $baseDir "QWEN.md")
    }

    # Create zip archive
    $zipFile = Join-Path $GenReleasesDir "nuaa-template-${Agent}-${Script}-${Version}.zip"
    Compress-Archive -Path "$baseDir/*" -DestinationPath $zipFile -Force
    Write-Host "Created $zipFile"
}

# --- Agent and script variant selection ---
$AgentsJsonPath = "src/nuaa_cli/agents.json"
if (-not (Test-Path $AgentsJsonPath)) {
    Write-Error "Agent configuration file not found at $AgentsJsonPath"
    exit 1
}

$AgentsData = Get-Content -Path $AgentsJsonPath | ConvertFrom-Json
$AllAgents = $AgentsData.PSObject.Properties.Name
$AllScripts = @('sh', 'ps')

function Convert-ToNormalizedList {
    param([string]$InputString)

    if ([string]::IsNullOrEmpty($InputString)) {
        return @()
    }

    # Split by comma or space and remove duplicates while preserving order
    $items = $InputString -split '[,\s]+' | Where-Object { $_ } | Select-Object -Unique
    return $items
}

function Test-ValidSubset {
    param(
        [string]$Type,
        [string[]]$Allowed,
        [string[]]$Items
    )

    $ok = $true
    foreach ($item in $Items) {
        if ($item -notin $Allowed) {
            Write-Error "Unknown $Type '$item' (allowed: $($Allowed -join ', '))"
            $ok = $false
        }
    }
    return $ok
}

# Determine agent list
if (-not [string]::IsNullOrEmpty($Agents)) {
    $AgentList = Convert-ToNormalizedList -InputString $Agents
    if (-not (Test-ValidSubset -Type 'agent' -Allowed $AllAgents -Items $AgentList)) {
        exit 1
    }
}
else {
    $AgentList = $AllAgents
}

# Determine script list
if (-not [string]::IsNullOrEmpty($Scripts)) {
    $ScriptList = Convert-ToNormalizedList -InputString $Scripts
    if (-not (Test-ValidSubset -Type 'script' -Allowed $AllScripts -Items $ScriptList)) {
        exit 1
    }
}
else {
    $ScriptList = $AllScripts
}

Write-Host "Agents: $($AgentList -join ', ')"
Write-Host "Scripts: $($ScriptList -join ', ')"

# Build all variants
foreach ($agent in $AgentList) {
    foreach ($script in $ScriptList) {
        New-ReleaseVariant -Agent $agent -Script $script
    }
}

Write-Host "`nArchives in ${GenReleasesDir}:"
Get-ChildItem -Path $GenReleasesDir -Filter "nuaa-template-*-${Version}.zip" | ForEach-Object {
    Write-Host "  $($_.Name)"
}
