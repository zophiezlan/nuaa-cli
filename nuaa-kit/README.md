# NUAA Kit - AI-Assisted Project Management for NUAA

## Overview

NUAA Kit is a specialized adaptation of Spec-Driven Development methodology designed specifically for NSW Users and AIDS Association. It transforms program design, proposal writing, and impact measurement into systematic, AI-assisted workflows integrated with Microsoft 365.

## Quick Start (Deploy in Weeks)

### Phase 1: Core Setup (Week 1)

1. Install dependencies
2. Configure Microsoft 365 integration
3. Import NUAA-specific templates
4. Train staff on first command: `/nuaa.design`

### Phase 2: Initial Use (Week 2-3)

- Create first program design using logic model generator
- Generate proposal for upcoming funding opportunity
- Test impact measurement framework

### Phase 3: Iteration (Week 4+)

- Refine based on staff feedback
- Expand to additional commands
- Full Microsoft 365 automation deployment

## Core Features

### 1. **Program Design & Logic Models**

- `/nuaa.design` - Generate comprehensive program designs
- Automatic logic model creation (Inputs → Activities → Outputs → Outcomes → Impact)
- Stakeholder journey mapping
- Risk assessment integration
- Built-in NUAA principles and ethics

### 2. **Proposal & Grant Writing**

- `/nuaa.propose` - Generate funding proposals
- Automatic budget table generation
- Methodology breakdown from program design
- Timeline chart creation
- NUAA capability statement integration
- Export to Word with professional formatting

### 3. **Impact Measurement & Evaluation**

- `/nuaa.measure` - Define impact frameworks
- Indicator development (process, output, outcome, impact)
- Evaluation planning
- Data collection template generation
- Export to Excel for tracking

## Output Formatting (Context-Aware)

### Professional (External)

- Formal language for government, funders
- Full technical detail
- Policy-ready formatting
- Word document export with NUAA branding

### Professional/Peer (Internal)

- Clear, direct language for NUAA staff
- Balance of detail and accessibility
- SharePoint integration
- Teams collaboration features

### Peer-Friendly (Community)

- Plain language
- Visual emphasis (infographics, diagrams)
- Accessible formats
- Community consultation materials

## Microsoft 365 Integration

### Word

- Branded proposal templates
- Auto-generated sections
- Track changes workflow
- Co-authoring support

### Excel

- Budget calculators
- Impact tracking dashboards
- Logic model visualizations
- Indicator monitoring sheets

### SharePoint

- Centralized template library
- Version control
- Staff collaboration workspace
- Document approval workflows

### Teams

- Command access via Teams bot (future)
- Notification for reviews
- Collaboration channels
- File sharing integration

### Power Automate

- Auto-save to SharePoint
- Approval workflows
- Email notifications
- Calendar integration for timelines

## Directory Structure

Below tree reflects current state. Items marked (planned) are placeholders for upcoming work and may have stub or empty directories only.

```text
nuaa-kit/
├── README.md                      # This file
├── QUICKSTART.md                  # Staff training guide
├── STATUS.md                      # Implemented vs planned artifact matrix
├── templates/                     # Core templates
│   ├── program-design.md
│   ├── proposal.md
│   ├── logic-model.md
│   ├── impact-framework.md
│   └── budget-calculator.md       # (planned stub)
├── commands/                      # NUAA command docs
│   ├── design.md                  # /nuaa.design
│   ├── propose.md                 # /nuaa.propose
│   ├── measure.md                 # /nuaa.measure
│   ├── report.md                  # (planned) /nuaa.report
│   └── refine.md                  # (planned) /nuaa.refine
├── microsoft365/                  # (planned) M365 integration scaffolding
│   ├── README.md                  # Overview & roadmap
│   ├── word-templates/            # (planned)
│   ├── excel-dashboards/          # (planned)
│   └── powerautomate-flows/       # (planned)
└── examples/                      # (planned) Real NUAA examples library
    └── README.md                  # Placeholder roadmap
```

For actual historical NUAA examples see top-level `NUAA-examples/` outside of this kit.

## First Command to Try: `/nuaa.design`

**Purpose**: Design a new program with full logic model, stakeholder journeys, and impact framework.

**Usage**:

```bash
/nuaa.design Design a peer-led workshop series on stigma reduction in healthcare settings, \
    targeting 50 people who use drugs in Western Sydney, with 6 monthly sessions over 12 months.
```

**Output**: Complete program design document including:

- Program overview and rationale
- Stakeholder journey maps
- Logic model (inputs, activities, outputs, outcomes, impact)
- Risk assessment
- Preliminary budget estimate
- Impact measurement framework
- Export to Word for review

## NUAA-Specific Principles Built-In

Every command and template incorporates:

- **Peer-led approach** - Lived experience at center
- **Harm reduction philosophy** - Non-judgmental, evidence-based
- **Consumer remuneration** - Fair payment for contributions ($300/session standard)
- **Cultural safety** - Respectful of diverse communities
- **Transparency** - Open processes and decision-making
- **Impact focus** - Outcomes over outputs
- **Ethical practice** - Do no harm, informed consent

## Next Steps

1. Review `QUICKSTART.md` for staff training
2. Try first command: `/nuaa.design`
3. Customize templates for specific NUAA needs
4. Set up Microsoft 365 integration
5. Provide feedback for iteration

## Pre-Submission Checks (Placeholder Linter)

Before marking any NUAA document `status: final` in its front matter, run one of the placeholder linter scripts to ensure no raw placeholder tokens like `[Amount]` or `[Name]` remain:

```pwsh
pwsh scripts/powershell/check-placeholders.ps1 -Path nuaa-kit
```

```bash
./scripts/bash/check-placeholders.sh nuaa-kit
```

Both scripts exit non-zero if unresolved bracketed placeholders are detected in files whose front matter contains `status: final`.

## Documentation

### Getting Started

- **[QUICKSTART.md](QUICKSTART.md)** - Week-by-week onboarding guide for new users
- **[STATUS.md](STATUS.md)** - Current implementation status of all features

### Methodology Guides

- **[docs/workflow-diagram.md](docs/workflow-diagram.md)** - Visual guide to the complete program lifecycle
- **[docs/evolution-guide.md](docs/evolution-guide.md)** - How to maintain and update program designs over time
- **[docs/multi-agent-setup.md](docs/multi-agent-setup.md)** - Using multiple AI agents in one project
- **[docs/update-guide.md](docs/update-guide.md)** - How to update NUAA-Kit itself

### Technical References

- **[accessibility-guidelines.md](accessibility-guidelines.md)** - Making outputs accessible to all
- **[evaluation-data-dictionary.md](evaluation-data-dictionary.md)** - Standard indicators and measures
- **[glossary.md](glossary.md)** - NUAA-specific terminology

### Review & Analysis

- **[REVIEW-FINDINGS.md](REVIEW-FINDINGS.md)** - Comprehensive review and analysis findings

## Support

Contact: [NUAA IT/Project Lead]
Documentation: `/nuaa-kit/docs/`
Training: [Schedule sessions with staff]

---

**Built for NUAA by NUAA principles** 🌱
