<div align="center">
   <h1>🌱 NUAA Project Kit</h1>
   <h3><em>AI-Assisted Project Management for NSW Users and AIDS Association</em></h3>

   <p>
      <a href="https://github.com/zophiezlan/nuaa-cli/actions/workflows/ci.yml">
         <img alt="CI" src="https://github.com/zophiezlan/nuaa-cli/actions/workflows/ci.yml/badge.svg" />
      </a>
      <a href="https://github.com/zophiezlan/nuaa-cli/actions/workflows/e2e.yml">
         <img alt="E2E" src="https://github.com/zophiezlan/nuaa-cli/actions/workflows/e2e.yml/badge.svg" />
      </a>
      <a href="https://github.com/zophiezlan/nuaa-cli/actions/workflows/release.yml">
         <img alt="Release" src="https://github.com/zophiezlan/nuaa-cli/actions/workflows/release.yml/badge.svg" />
      </a>
   </p>
</div>

<p align="center">
    <strong>An open source project transforming program design, proposal writing, and impact measurement into systematic, AI-assisted workflows for NUAA.</strong>
</p>

---

## Table of Contents

- [🤔 What is NUAA Project Kit?](#-what-is-nuaa-project-kit)
- [⚡ Get Started](#-get-started)
- [🎯 Core Features](#-core-features)
- [📋 Quick Start Guide](#-quick-start-guide)
- [🔧 Prerequisites](#-prerequisites)
- [📖 Learn More](#-learn-more)
- [👥 Maintainers](#-maintainers)
- [💬 Support](#-support)
- [📄 License](#-license)

## 🤔 What is NUAA Project Kit?

NUAA Project Kit is a specialized adaptation of Spec-Driven Development methodology designed specifically for **NSW Users and AIDS Association (NUAA)**. It transforms program design, proposal writing, and impact measurement into systematic, AI-assisted workflows integrated with Microsoft 365.

### Key Benefits

- **Program Design Made Easy**: Generate comprehensive program designs with logic models, stakeholder journeys, and risk assessments
- **Faster Proposal Writing**: Automatically create funding proposals with budget tables, methodologies, and timelines
- **Better Impact Measurement**: Define clear evaluation frameworks with indicators and data collection templates
- **Built-in NUAA Principles**: Every output incorporates peer-led approaches, harm reduction philosophy, and ethical practices

## ⚡ Get Started

### Quick Installation

NUAA Project Kit is available in the `/nuaa-kit` directory of this repository. To start using it:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/zophiezlan/nuaa-cli.git
   cd nuaa-cli/nuaa-kit
   ```

2. **Review the Quick Start Guide:**

   ```bash
   cat QUICKSTART.md
   ```

3. **Try your first command:**
   Launch your AI assistant in the `nuaa-kit` directory and use:

   ```bash
   /nuaa.design Design a peer-led workshop series on stigma reduction in healthcare settings
   ```

### System Requirements

- **Linux/macOS/Windows**
- [Supported AI coding agent](#-supported-ai-agents) (Claude Code, GitHub Copilot, etc.)
- [uv](https://docs.astral.sh/uv/) for package management
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## 🎯 Core Features

### 1. Program Design & Logic Models (`/nuaa.design`)

Generate comprehensive program designs with:

- Automatic logic model creation (Inputs → Activities → Outputs → Outcomes → Impact)
- Stakeholder journey mapping
- Risk assessment integration
- Built-in NUAA principles and ethics

### 2. Proposal & Grant Writing (`/nuaa.propose`)

Create professional funding proposals with:

- Automatic budget table generation
- Methodology breakdown from program design
- Timeline chart creation
- NUAA capability statement integration
- Export to Word with professional formatting

### 3. Impact Measurement & Evaluation (`/nuaa.measure`)

Define clear impact frameworks with:

- Indicator development (process, output, outcome, impact)
- Evaluation planning
- Data collection template generation
- Export to Excel for tracking

## 📋 Quick Start Guide

### Deploy in Weeks

### Use the NUAA CLI Workflows

Once you have this repository checked out, you can add the `nuaa` function to your PowerShell profile (Windows) so commands are easy to run:

```powershell
pwsh -File scripts/powershell/add-nuaa-function.ps1 -Version v0.3.0
```

Open a new PowerShell window and try:

```powershell
nuaa version

# Create a new feature (scaffolds program design, logic model, impact framework)
nuaa design "Peer Naloxone Distribution" "people at risk of opioid overdose" "12 months"

# Generate a proposal linked to that design
nuaa propose "Peer Naloxone Distribution" "NSW Health" "$50000" "12 months"

# Define or refresh the impact framework
nuaa measure "Peer Naloxone Distribution" "12 months" "$7000"

# Brownfield documentation for an existing program
nuaa document "Outreach & Needle Exchange"

# Report scaffold
nuaa report "Peer Naloxone Distribution" --type final

# Record a refinement in the feature changelog
nuaa refine "Peer Naloxone Distribution" --note "Updated budget and indicators after pilot"
```

Outputs are created under `nuaa/NNN-<slug>/` using the templates in `nuaa-kit/templates/`.

#### Phase 1: Core Setup (Week 1)

1. Install dependencies
2. Configure Microsoft 365 integration
3. Import NUAA-specific templates
4. Train staff on first command: `/nuaa.design`

#### Phase 2: Initial Use (Week 2-3)

- Create first program design using logic model generator
- Generate proposal for upcoming funding opportunity
- Test impact measurement framework

#### Phase 3: Iteration (Week 4+)

- Refine based on staff feedback
- Expand to additional commands
- Full Microsoft 365 automation deployment

## 🤖 Supported AI Agents

NUAA Project Kit works with all major AI coding assistants:

<!-- SUPPORTED_AGENTS_START -->

| Agent | Website | Support |
|---|---|---|
| [Claude Code](https://docs.anthropic.com/claude/docs/code-interpreter-and-cli-tool) | Official | Full |
| [Gemini CLI](https://github.com/google/generative-ai-docs/blob/main/site/en/tutorials/gemini/cli.md) | Official | Full |
| GitHub Copilot | Official | Full |
| [Cursor](https://cursor.sh/docs/cli) | Official | Full |
| [Qwen Code](https://help.aliyun.com/document_detail/2601612.html) | Official | Full |
| [opencode](https://www.opencode.com/docs/cli) | Official | Full |
| [Codex CLI](https://www.npmjs.com/package/@openai/codex-cli) | Official | Full |
| Windsurf | Official | Full |
| Kilo Code | Official | Full |
| [Auggie CLI](https://github.com/cpbuildtools/dev-docs/blob/main/auggie/README.md) | Official | Full |
| Roo Code | Official | Full |
| [CodeBuddy CLI](https://www.npmjs.com/package/codebuddy-cli) | Official | Full |
| [Amazon Q Developer CLI](https://docs.aws.amazon.com/amazonq/latest/aws-builder-use-ug/cli-install.html) | Official | Full |
| [Amp](https://docs.amp.computer/cli/overview) | Official | Full |

<!-- SUPPORTED_AGENTS_END -->

For a complete list of supported agents, see the [NUAA Project Kit README](./nuaa-kit/README.md).

## 🔧 Prerequisites

### Required

- **Linux/macOS/Windows** operating system
- **[Git](https://git-scm.com/downloads)** for version control
- **[Python 3.11+](https://www.python.org/downloads/)** for CLI tools
- **[uv](https://docs.astral.sh/uv/)** for package management
- **AI coding agent** (see supported list above)

### Optional

- **Microsoft 365** for full integration features (Word, Excel, SharePoint)
- **Microsoft Teams** for collaboration features
- **Power Automate** for workflow automation

## 📖 Learn More

### NUAA Project Kit Documentation

- **[NUAA Project Kit README](./nuaa-kit/README.md)** - Complete guide to NUAA Project Kit features
- **[Quick Start Guide](./nuaa-kit/QUICKSTART.md)** - Week-by-week onboarding for staff
- **[Status & Roadmap](./nuaa-kit/STATUS.md)** - Current implementation status
- **[Workflow Diagram](./nuaa-kit/docs/workflow-diagram.md)** - Visual guide to program lifecycle
- **[Evolution Guide](./nuaa-kit/docs/evolution-guide.md)** - Maintaining program designs over time
- **[Transition History](./docs/history/spec-driven.md)** - Documents the transition from the original Spec-Kit.

### NUAA Examples

- **[NUAA Examples](./NUAA-examples/)** - Real NUAA program documents and examples
- Strategic plans, constitutions, and reporting examples

### Technical References

- **[Accessibility Guidelines](./nuaa-kit/accessibility-guidelines.md)** - Making outputs accessible
- **[Evaluation Data Dictionary](./nuaa-kit/evaluation-data-dictionary.md)** - Standard indicators
- **[Glossary](./nuaa-kit/glossary.md)** - NUAA-specific terminology

## 🧪 Automation & quality checks

This repo bakes in a few guardrails to keep things tidy and in sync:

- Single source of truth for supported agents in `src/nuaa_cli/agents.json`
- Supported Agents tables in this README and `AGENTS.md` are auto-generated from the manifest
- Parity check ensures bash and PowerShell scripts cover all agents listed in the manifest
- CI runs lint, type checks, unit tests, coverage, security scans, and E2E tests across Windows and Ubuntu
- **Auto-formatters and linters** fix issues automatically before you commit

### 🔧 Quick Fix Commands

Before committing, auto-fix all code style issues:

```bash
# Using Make (recommended)
make fix          # Auto-format and fix all issues
make check        # Run all checks (lint, test, security)
make ci           # Run full CI suite locally

# Or use the scripts directly
./scripts/bash/fix.sh              # Linux/Mac
.\scripts\powershell\fix.ps1       # Windows

# Individual tools
make format       # Just formatting
make test-cov     # Tests with coverage
make security     # Security scan
```

### 📋 Available Make Commands

Run `make help` to see all available commands:

- `make install-dev` - Install with development dependencies
- `make format` - Auto-format code with black and ruff
- `make lint` - Check code style
- `make test` - Run tests
- `make test-cov` - Run tests with coverage report
- `make security` - Run security scan
- `make check` - Run all checks
- `make fix` - Auto-fix all issues
- `make ci` - Run full CI suite locally
- `make clean` - Clean generated files

### 🔍 Manual Commands

If you prefer running commands individually:

- Update docs from manifest: `python scripts/python/update_agents_docs.py`
- Verify script parity: `python scripts/python/verify_agent_script_parity.py`
- Run tests: `pytest`
- Format code: `black . && ruff check --fix .`
- Security scan: `bandit -r src/nuaa_cli`

## 🌟 NUAA-Specific Principles

Every command and template incorporates:

- **Peer-led approach** - Lived experience at center
- **Harm reduction philosophy** - Non-judgmental, evidence-based
- **Consumer remuneration** - Fair payment for contributions ($300/session standard)
- **Cultural safety** - Respectful of diverse communities
- **Transparency** - Open processes and decision-making
- **Impact focus** - Outcomes over outputs
- **Ethical practice** - Do no harm, informed consent

## 🔍 Troubleshooting

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

## 👥 Maintainers

- Den Delimarsky ([@localden](https://github.com/localden))
- John Lam ([@jflam](https://github.com/jflam))

## 💬 Support

For support, please open a [GitHub issue](https://github.com/zophiezlan/nuaa-cli/issues/new). We welcome bug reports, feature requests, and questions about using NUAA Project Kit.

## 🙏 Acknowledgements

This project is heavily influenced by and based on the work and research of [John Lam](https://github.com/jflam) and the Spec-Driven Development methodology.

## 📄 License

This project is licensed under the terms of the MIT open source license. Please refer to the [LICENSE](./LICENSE) file for the full terms.

---

**Built for NUAA by NUAA principles** 🌱
