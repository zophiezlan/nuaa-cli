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
- [♿ Accessibility & Inclusion](#-accessibility--inclusion)
- [⚡ Get Started](#-get-started)
- [🎯 Core Features](#-core-features)
- [📋 Quick Start Guide](#-quick-start-guide)
- [🔧 Prerequisites](#-prerequisites)
- [📖 Learn More](#-learn-more)
- [🔒 Security](#-security)
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

## ♿ Accessibility & Inclusion

**NUAA CLI is designed for everyone.** We've built comprehensive accessibility features to ensure wide adoption across our diverse workplace.

### 🌍 Multi-Language Support

Available in 6 languages to serve our diverse communities:

- **English (Australia)** - en_AU
- **Vietnamese** - vi_VN
- **Thai** - th_TH
- **Arabic** - ar (with RTL support)
- **Simplified Chinese** - zh_CN
- **Spanish** - es

Set your language:
```bash
export LANGUAGE=vi_VN  # Vietnamese
nuaa --help
```

[Learn more about translations](TRANSLATION_GUIDE.md) | [Contribute translations](TRANSLATION_GUIDE.md#how-to-contribute-translations)

### 👁️ Visual Accessibility Modes

Multiple display modes for different vision needs:

```bash
# High contrast mode (enhanced visibility)
export NUAA_HIGH_CONTRAST=1

# No color mode (for color blindness)
export NO_COLOR=1

# Dyslexia-friendly mode (extra spacing, shorter lines)
export NUAA_DYSLEXIA_FRIENDLY=1
```

### 🎤 Screen Reader Support

Fully optimized for NVDA, JAWS, VoiceOver, and Orca:

```bash
export NUAA_SCREEN_READER=1
nuaa --help
```

Features:
- No visual-only indicators
- Clear status announcements
- Structured navigation hints
- No spinners or animations in screen reader mode

[Screen Reader Guide](docs/accessibility/KEYBOARD_SHORTCUTS.md#screen-reader-compatibility)

### ⌨️ Full Keyboard Accessibility

Every feature works with keyboard only - no mouse required.

**Essential shortcuts:**
- `↑↓` or `j/k` - Navigate menus
- `Enter` - Select
- `Esc` or `Ctrl+C` - Cancel
- `?` - Context help

[Complete Keyboard Guide](docs/accessibility/KEYBOARD_SHORTCUTS.md)

### 🧠 Cognitive Accessibility

Simple mode for clearer, step-by-step guidance:

```bash
export NUAA_SIMPLE_MODE=1
nuaa onboard  # Interactive onboarding wizard
```

Features:
- One question at a time
- Clear progress indicators (Step X of Y)
- Plain language (Grade 8-10 reading level)
- No time pressure on interactions

### 🌏 Cultural Safety

Built-in cultural safety features:
- Person-first, non-stigmatizing language
- Harm reduction philosophy
- Gender-inclusive language (they/them pronouns)
- Aboriginal and Torres Strait Islander cultural protocols
- LGBTIQ+ inclusion
- Trauma-informed design

[Cultural Safety Framework](CULTURAL_SAFETY_FRAMEWORK.md)

### 🎯 Automated Accessibility Testing

We automatically check for:
- Readability (plain language standards)
- Stigmatizing language detection
- Alt text for images
- Heading hierarchy
- Color-only meaning

Run tests yourself:
```bash
./scripts/accessibility/run_accessibility_tests.sh
```

### 📚 Accessibility Resources

- [Complete Accessibility Plan](ACCESSIBILITY_ENHANCEMENT_PLAN.md)
- [Keyboard Shortcuts Guide](docs/accessibility/KEYBOARD_SHORTCUTS.md)
- [Cultural Safety Framework](CULTURAL_SAFETY_FRAMEWORK.md)
- [Translation Guide](TRANSLATION_GUIDE.md)
- [Accessibility Guidelines](nuaa-kit/accessibility-guidelines.md)

**Need accessibility support?** Open an issue with the `accessibility` label.

---

## ⚡ Get Started

### Quick Installation for Your Project

NUAA CLI is installed directly into **your project** (not cloned as a repository). Most users will interact with it through the **WebUI** - no command line experience needed!

**Step 1: Install NUAA CLI in your project**

```bash
# Run this in your project directory
uvx --from git+https://github.com/zophiezlan/nuaa-cli.git nuaa init .
```

This command will:
- Install NUAA CLI tools into your project
- Create `.nuaa/` directory with templates and scripts
- Set up your chosen AI assistant integration (Claude, Copilot, Gemini, etc.)
- Initialize a git repository (optional)

**Step 2: Start the WebUI (Recommended for most users)**

```bash
# After init completes, start the web interface
python .nuaa/scripts/start_webui.py
# Or if you prefer: uvx --from git+https://github.com/zophiezlan/nuaa-cli.git nuaa webui
```

Then open your browser to `http://localhost:5000` and start creating program designs, proposals, and impact frameworks through an easy-to-use web interface!

**Step 3 (Alternative): Use AI Assistant Commands**

If you prefer working with AI assistants directly, use the slash commands:

```bash
/nuaa.design Design a peer-led workshop series on stigma reduction in healthcare settings
```

### System Requirements

- **Linux/macOS/Windows**
- [Supported AI coding agent](#-supported-ai-agents) (Claude Code, GitHub Copilot, etc.)
- [uv](https://docs.astral.sh/uv/) for package management
- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

### 📦 Getting Started (Step-by-Step for Beginners)

**Don't have command line experience? No problem!** NUAA CLI comes with a web interface that requires no technical knowledge.

#### Step 1: Install NUAA CLI in Your Project

1. **Open your terminal** (or Command Prompt on Windows, or Terminal app on Mac)

2. **Navigate to your project folder**:
   ```bash
   cd /path/to/your-project-folder
   # Or create a new folder: mkdir my-nuaa-project && cd my-nuaa-project
   ```

3. **Run the installation command**:
   ```bash
   uvx --from git+https://github.com/zophiezlan/nuaa-cli.git nuaa init .
   ```

4. **Follow the prompts**:
   - Choose your AI assistant (Claude, Copilot, Gemini, etc.) - or skip if unsure
   - Choose script type (just press Enter for default)

5. **Wait for installation** - This downloads templates and sets up your project (takes about 30 seconds)

#### Step 2: Start Using NUAA

You have two options:

**Option A: WebUI (Recommended for most users - No coding required!)**

```bash
# Start the web interface
python .nuaa/scripts/start_webui.py
```

Then open your browser to: `http://localhost:5000`

You'll see a simple, user-friendly interface where you can:
- Click to create program designs
- Fill in forms to generate proposals
- Export documents to Word/Excel

**Option B: AI Assistant Commands (For those comfortable with AI tools)**

If you're using an AI assistant like Claude Code or GitHub Copilot, you can use slash commands:

```bash
/nuaa.design Create a peer-led naloxone distribution program
/nuaa.propose Generate funding proposal for the program
/nuaa.measure Define impact measurement framework
```

#### Common Questions

<details>
<summary><b>❓ What if I don't have Python installed?</b></summary>

You'll need Python 3.11 or newer. Download it from [python.org/downloads](https://www.python.org/downloads/)

Check your version:
```bash
python --version
```

</details>

<details>
<summary><b>❓ What if I don't have uvx installed?</b></summary>

uvx comes with Python 3.11+. If you get "command not found", install it:

```bash
pip install uvx
```

</details>

<details>
<summary><b>❓ Can I use this on my phone or tablet?</b></summary>

Yes! Once the WebUI is running, you can access it from any device on the same network. Your team member will give you the URL (it looks like `http://192.168.1.x:5000`).

</details>

<details>
<summary><b>❓ Do I need to install an AI assistant?</b></summary>

Not if you're using the WebUI! The WebUI works standalone. AI assistants are only needed if you want to use the slash commands method.

</details>

#### Next Steps

- 🌐 **For WebUI users**: Open the interface and click around - it's intuitive!
- 🤖 **For AI assistant users**: Try your first `/nuaa.design` command
- 📖 **Need more help?**: Check out the [WebUI Guide](./interfaces/web-simple/README.md)
- 💬 **Got questions?**: Open a [GitHub Issue](https://github.com/zophiezlan/nuaa-cli/issues)

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

## 📋 Workflows & Use Cases

### Your First Week with NUAA

After running `nuaa init .` in your project, you'll have everything you need to start creating professional program designs, proposals, and impact frameworks.

#### Week 1: WebUI Basics (Recommended for Most Users)

**Day 1-2: Get Familiar**
1. Start the WebUI: `python .nuaa/scripts/start_webui.py`
2. Open browser to `http://localhost:5000`
3. Explore the interface - click through the different sections
4. Try creating a simple program design using the guided form

**Day 3-4: Create Your First Program Design**
1. Click "Program Design" in the WebUI
2. Fill in the form with your program details:
   - Program name: "Peer Naloxone Distribution"
   - Target population: "People at risk of opioid overdose"
   - Duration: "12 months"
3. Review the generated logic model
4. Export to Word for review with your team

**Day 5: Generate a Funding Proposal**
1. Click "Funding Proposal" in the WebUI
2. Select your program design as the basis
3. Add funder details (e.g., "NSW Health", "$50,000", "12 months")
4. Customize the proposal for your funder's requirements
5. Export to Word and add attachments

#### Week 2-3: Advanced Features

**Impact Measurement**
- Use the "Impact Framework" section to define evaluation indicators
- Export evaluation plan to Excel for tracking

**Team Collaboration**
- Share the WebUI URL with team members on your network
- Multiple people can work on different programs simultaneously
- Export and share documents via email or SharePoint

#### Week 4+: Ongoing Use

**Regular Workflows**
- Weekly: Document outreach sessions and program activities
- Monthly: Update program designs based on learnings
- Quarterly: Generate progress reports for funders
- Annually: Conduct program evaluations

**For Advanced Users: AI Assistant Commands**

If you're comfortable with AI assistants, you can use slash commands for faster workflows:

```bash
/nuaa.design Create program design for Peer Naloxone Distribution targeting people at risk of opioid overdose over 12 months
/nuaa.propose Generate NSW Health funding proposal for $50,000 over 12 months
/nuaa.measure Define impact framework for 12-month evaluation with $7,000 budget
/nuaa.document Document existing Outreach & Needle Exchange program
/nuaa.report Create final report for Peer Naloxone Distribution program
```

All outputs are saved in your project's `.nuaa/outputs/` directory with organized folders for each program.

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

## 🔒 Security

NUAA CLI implements multiple layers of security to protect your projects and data.

### Input Validation

All command inputs are validated to prevent security issues:

- **Program names and text fields** are sanitized to prevent path traversal attacks
- **Length limits** are enforced to prevent buffer issues
- **Empty values** are rejected with clear error messages
- **Special characters** are filtered to ensure filesystem safety

### File Operations

Template and file operations are protected:

- **ZIP extraction** validates all paths to prevent path traversal attacks
- **File permissions** are checked before reading or writing
- **Temporary files** are securely created and cleaned up
- **Directory operations** use safe path resolution

### Network Security

GitHub API interactions use industry-standard security:

- **HTTPS/TLS** connections with certificate validation via `truststore`
- **Rate limiting** is respected to prevent API abuse
- **Timeouts** prevent hanging connections
- **Authentication tokens** are read from environment variables (never hardcoded)

### Environment Variables

Sensitive configuration is managed through environment variables:

```bash
# GitHub authentication (optional, for higher rate limits)
export GH_TOKEN=your_token_here
export GITHUB_TOKEN=your_token_here

# See .env.example for complete list of supported variables
```

**Important:** Never commit your `.env` file or expose your GitHub tokens in logs or screenshots.

### Logging & Data Privacy

Log files are stored securely:

- **Platform-specific directories:**
  - Linux: `~/.local/state/nuaa-cli/nuaa-cli.log`
  - macOS: `~/Library/Logs/nuaa-cli/nuaa-cli.log`
  - Windows: `%LOCALAPPDATA%\nuaa-cli\Logs\nuaa-cli.log`
- **Sensitive data** is not logged (tokens are masked in debug output)
- **File permissions** are set to user-only access
- **Log rotation** can be configured via `LOG_FILE` environment variable

### Reporting Security Issues

If you discover a security vulnerability, please:

1. **Do NOT** open a public issue
2. Email the maintainers directly (see [Maintainers](#-maintainers) section)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if you have one)

We take security seriously and will respond promptly to verified reports.

## 🔧 For Developers: Contributing to NUAA CLI

**Note**: This section is for people developing the NUAA CLI tool itself. If you're an end user wanting to use NUAA for your projects, you can skip this section!

If you want to contribute to NUAA CLI development, see [CONTRIBUTING.md](./CONTRIBUTING.md) for:

- Setting up your development environment
- Running tests and linters
- Code quality automation
- CI/CD workflows
- Creating pull requests

### Quick Developer Commands

```bash
# Clone the repository (for developers only!)
git clone https://github.com/zophiezlan/nuaa-cli.git
cd nuaa-cli

# Install with development dependencies
make install-dev

# Run all quality checks
make check

# Auto-fix code style issues
make fix
```

For complete development documentation, see [CONTRIBUTING.md](./CONTRIBUTING.md).

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
