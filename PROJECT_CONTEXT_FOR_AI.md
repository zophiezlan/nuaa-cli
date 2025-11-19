# NUAA CLI Project Context & User Assumptions

## Critical Understanding: Two Distinct Audiences

### 1. Tool Developers (Minority - ~3 people)

**Location**: Working in the `nuaa-cli` repository (this repo)
**What they do**: Develop, test, and maintain the CLI tool itself
**Setup**: Clone repo → `pip install -e .[dev]` → develop/test
**Tools needed**: Full dev environment (ruff, black, pytest, mypy, pre-commit, etc.)
**Focus**: Source code quality, CI/CD, releases, linting the CLI codebase

### 2. End Users (Majority - hundreds/thousands)

**Location**: Their own project repositories
**What they do**: Use NUAA CLI for AI-assisted project management
**Setup**: `uvx --from git+https://github.com/zophiezlan/nuaa-cli.git nuaa init .`
**Tools needed**: Just the CLI tool itself, no dev dependencies
**Focus**: Their project work, using the WebUI and NUAA workflows

---

## Key Project Architecture Points

### Installation Method for End Users

```bash
# Users DON'T clone the nuaa-cli repo
# They run this in THEIR project:
uvx --from git+https://github.com/zophiezlan/nuaa-cli.git nuaa init .
```

This:

- Installs NUAA CLI into their project
- Creates `.nuaa/` directory with templates, scripts, memory
- Sets up agent-specific files (`.github/agents/`, `.claude/commands/`, etc.)
- Does NOT copy all the development files from nuaa-cli repo
- Does NOT require dev dependencies

### Primary User Interface: WebUI

**Most users will interact via the WebUI, NOT VS Code**

**Important implications:**

- Documentation should prioritize WebUI workflows
- Instructions should be WebUI-first, CLI-second
- VS Code tasks/setup are for DEVELOPERS of the tool, not end users
- End users don't need to know about linting, pre-commit hooks, etc.

### What Users Get After `nuaa init .`

```
their-project/
├── .nuaa/
│   ├── memory/          # Project constitution, context
│   ├── scripts/         # Bash or PowerShell scripts for NUAA workflows
│   └── templates/       # Document templates
├── .github/agents/      # (if using Copilot)
├── .claude/commands/    # (if using Claude)
├── .gemini/commands/    # (if using Gemini)
└── [their existing project files]
```

**They do NOT get:**

- pyproject.toml
- tests/
- src/nuaa_cli/
- .github/workflows/
- Development tooling
- This README

---

## Auto-Fix & Linting Architecture

### Purpose: FOR TOOL DEVELOPERS ONLY

The auto-fix workflows, pre-commit hooks, and linting setup are for maintaining the **CLI tool's source code**, NOT for end user projects.

### Current Implementation

- **Location**: `.github/workflows/` (CI/CD for the CLI tool itself)
- **Triggers**: Push/PR to nuaa-cli repo
- **What it fixes**: Python code in `src/nuaa_cli/`, test files, development scripts
- **Reusable action**: `.github/actions/auto-fix-lint/action.yml`

### Coverage

| Workflow                  | Purpose                 | Auto-fix         |
| ------------------------- | ----------------------- | ---------------- |
| CI (`ci.yml`)             | Test the CLI tool       | ✅ Before tests  |
| Release (`release.yml`)   | Create release packages | ✅ Before verify |
| E2E (`e2e.yml`)           | Smoke test CLI commands | ✅ Before tests  |
| Auto-fix (`auto-fix.yml`) | Fix PRs automatically   | ✅ Commits fixes |

### What This Means for Users

**End users don't see or care about any of this.** They just run `nuaa init .` and use the tool. The auto-fix infrastructure ensures that when developers push updates to the CLI, those updates are properly tested and formatted.

---

## Documentation & Instructions Priorities

### ❌ Wrong Focus (Current Problem)

- Too much emphasis on cloning the repo
- Instructions assume people are working IN the nuaa-cli repo
- Developer workflows mixed with user workflows
- VS Code tasks presented as primary interface

### ✅ Correct Focus (Should Be)

1. **WebUI First**: Most documentation should focus on web interface
2. **Init-Based**: All user docs should start with `nuaa init .`
3. **Agent Agnostic**: Support all AI agents equally (Claude, Copilot, Gemini, etc.)
4. **Non-Technical Friendly**: Many users may not be comfortable with CLI/terminal
5. **Project Context**: Users work in THEIR projects, not the nuaa-cli repo

### Documentation Structure Should Be

```
📚 User Documentation (95% of docs)
├── Getting Started
│   ├── Install via uvx + init
│   ├── Using the WebUI
│   ├── Choosing your AI agent
│   └── Your first workflow
├── WebUI Guide
│   ├── Design workflow
│   ├── Propose workflow
│   ├── Measure workflow
│   └── Report workflow
├── AI Agent Setup
│   ├── GitHub Copilot setup
│   ├── Claude setup
│   ├── Gemini setup
│   └── Other agents...
└── Troubleshooting

🔧 Developer Documentation (5% of docs)
├── Contributing
├── Development setup
├── Running tests
├── Creating releases
└── Architecture
```

---

## Common Anti-Patterns to Avoid

### ❌ Don't Say

- "Clone the nuaa-cli repository"
- "Run the auto-fix task in VS Code"
- "Install dev dependencies"
- "Set up pre-commit hooks"
- "Run pytest to test your project"

### ✅ Do Say

- "Run `nuaa init .` in your project directory"
- "Open the WebUI to start your workflow"
- "Choose your AI assistant (Copilot/Claude/Gemini)"
- "Use the NUAA commands in your AI chat"
- "Access your project memory in `.nuaa/memory/`"

---

## File Distribution

### These Files Are For CLI Development (Stay in nuaa-cli repo)

- `.github/workflows/` - CI/CD for the tool
- `.github/actions/` - Reusable workflow actions
- `tests/` - Unit tests for the CLI
- `src/nuaa_cli/` - CLI source code
- `pyproject.toml` - CLI package definition
- `.pre-commit-config.yaml` - Dev linting setup
- `.vscode/tasks.json` - Developer tasks
- `scripts/python/` - Development scripts
- `benchmarks/`, `mutation_testing/` - Dev tools

### These Files Go To User Projects (via `nuaa init`)

- `.nuaa/memory/` - Project constitution & context
- `.nuaa/scripts/` - Workflow scripts (bash/ps1)
- `.nuaa/templates/` - Document templates
- Agent-specific files (`.github/agents/`, `.claude/commands/`, etc.)
- `QUICKSTART.md` - User-facing quick start guide

### These Files Are Context/Reference (Don't go anywhere)

- `nuaa-kit/` - Template source files
- `docs/` - Documentation source
- `interfaces/` - WebUI, email bridge, Teams bot
- `README.md` - Project README (for GitHub, not users)
- `AGENTS.md`, `ROADMAP.md`, etc. - Project documentation

---

## WebUI Considerations

### Current State

The WebUI is in `interfaces/web-simple/` and provides a simplified interface for running NUAA workflows without needing terminal access.

### What This Means for Instructions

- Most users will access NUAA through the WebUI
- Instructions should show WebUI screenshots/workflows
- Terminal commands are secondary (for advanced users)
- Mobile field workers and email-only users may ONLY use WebUI/email bridge
- Accessibility features are critical (keyboard navigation, screen readers)

### Integration with `nuaa init`

After running `nuaa init .`, users should be able to:

1. Start the WebUI with a simple command
2. Access all NUAA workflows through browser
3. Not need to touch configuration files
4. Not need to understand the underlying structure

---

## AI Assessment Questions

When evaluating the project, consider:

1. **User Journey**: Does the documentation follow "install via uvx → init → use WebUI" path?
2. **Separation of Concerns**: Are developer tasks clearly separated from user tasks?
3. **Accessibility**: Can non-technical users (email-only, mobile workers) use the system?
4. **Agent Equality**: Are all AI agents treated as first-class citizens?
5. **Minimal Overhead**: Does `nuaa init` add only what's needed, not the whole dev environment?
6. **WebUI Priority**: Is the web interface positioned as the primary interface?
7. **Clear Context**: Is it obvious whether content is for tool developers or end users?

---

## Summary

**The nuaa-cli repo** = Tool development environment
**User projects** = Where the tool is used (via `nuaa init`)
**Primary interface** = WebUI (not VS Code, not terminal)
**Primary users** = Non-developers using AI for project management
**Primary workflow** = Init → WebUI → AI commands → Document generation

Everything else (linting, testing, CI/CD, VS Code tasks) is infrastructure for maintaining the tool itself, invisible to end users.
