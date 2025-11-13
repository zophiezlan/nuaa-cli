# Installation Guide

## Prerequisites

- **Linux/macOS** (or Windows; PowerShell scripts now supported without WSL)
- AI coding agent: [Claude Code](https://www.anthropic.com/claude-code), [GitHub Copilot](https://code.visualstudio.com/), [Codebuddy CLI](https://www.codebuddy.ai/cli) or [Gemini CLI](https://github.com/google-gemini/gemini-cli)
- [uv](https://docs.astral.sh/uv/) for package management
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## Installation

### Initialize a New Project

The easiest way to get started is to initialize a new project:

```bash
uvx --from git+https://github.com/zophiezlan/nuaa-cli.git nuaa init <PROJECT_NAME>
```

Or initialize in the current directory:

```bash
uvx --from git+https://github.com/zophiezlan/nuaa-cli.git nuaa init .
# or use the --here flag
uvx --from git+https://github.com/zophiezlan/nuaa-cli.git nuaa init --here
```

> **Note**: The legacy `specify` command is still supported for backwards compatibility.

### One-Line Shell Function (Easy Global Access)

If you want to type `nuaa` anywhere without prefixing with `uvx`, install a lightweight shell function.

#### PowerShell (Windows)

Run:

```powershell
pwsh -File scripts/powershell/add-nuaa-function.ps1 -Version v0.2.0
```

Then restart your terminal (or run `. $PROFILE`) and test:

```powershell
nuaa version
```

To track the latest main branch instead of a fixed version:

```powershell
pwsh -File scripts/powershell/add-nuaa-function.ps1 -Latest
```

#### Bash / Zsh (macOS & Linux)

Run:

```bash
bash scripts/bash/add-nuaa-function.sh v0.2.0
```

Reload your shell:

```bash
source ~/.bashrc  # or: source ~/.zshrc
```

Test:

```bash
nuaa version
```

Follow `main` instead of a pinned version:

```bash
bash scripts/bash/add-nuaa-function.sh latest
```

> These helpers create a function that shells out to `uvx` so you always get a clean, ephemeral run of the CLI without a global install.

### Specify AI Agent

You can proactively specify your AI agent during initialization:

```bash
uvx --from git+https://github.com/zophiezlan/nuaa-cli.git nuaa init <project_name> --ai claude
uvx --from git+https://github.com/zophiezlan/nuaa-cli.git nuaa init <project_name> --ai gemini
uvx --from git+https://github.com/zophiezlan/nuaa-cli.git nuaa init <project_name> --ai copilot
uvx --from git+https://github.com/zophiezlan/nuaa-cli.git nuaa init <project_name> --ai codebuddy
```

### Specify Script Type (Shell vs PowerShell)

All automation scripts now have both Bash (`.sh`) and PowerShell (`.ps1`) variants.

Auto behavior:

- Windows default: `ps`
- Other OS default: `sh`
- Interactive mode: you'll be prompted unless you pass `--script`

Force a specific script type:

```bash
uvx --from git+https://github.com/zophiezlan/nuaa-cli.git nuaa init <project_name> --script sh
uvx --from git+https://github.com/zophiezlan/nuaa-cli.git nuaa init <project_name> --script ps
```

### Ignore Agent Tools Check

If you prefer to get the templates without checking for the right tools:

```bash
uvx --from git+https://github.com/zophiezlan/nuaa-cli.git nuaa init <project_name> --ai claude --ignore-agent-tools
```

## Verification

After initialization, you should see the following commands available in your AI agent:

- `/nuaa.design` - Create program designs
- `/nuaa.propose` - Generate funding proposals
- `/nuaa.measure` - Define impact frameworks
- `/nuaa.document` - Document existing programs
- `/nuaa.refine` - Refine and improve outputs
- `/nuaa.report` - Generate reports and presentations

The `.nuaa/scripts` directory will contain both `.sh` and `.ps1` scripts.

## Troubleshooting

### Git Credential Manager on Linux

If you're having issues with Git authentication on Linux, you can install Git Credential Manager:

```bash
#!/usr/bin/env bash
set -e
echo "Downloading Git Credential Manager v2.6.1..."
wget https://github.com/git-ecosystem/git-credential-manager/releases/download/v2.6.1/gcm-linux_amd64.2.6.1.deb
echo "Installing Git Credential Manager..."
sudo dpkg -i gcm-linux_amd64.2.6.1.deb
echo "Configuring Git to use GCM..."
git config --global credential.helper manager
echo "Cleaning up..."
rm gcm-linux_amd64.2.6.1.deb
```
