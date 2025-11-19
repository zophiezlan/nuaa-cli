# NUAA CLI for Qwen Code

This package provides NUAA (NSW Users & AIDS Association) command templates for Alibaba's Qwen Code CLI.

## About NUAA

NUAA is a peer-led harm reduction organization with 30+ years of experience supporting people who use drugs in NSW, Australia. This CLI toolkit helps staff, peer workers, and community members design evidence-based, culturally safe programs.

## Installation

1. Install Qwen Code CLI following the [official documentation](https://help.aliyun.com/document_detail/2601612.html)
2. Extract this package to your project directory
3. The NUAA commands will be available in `.qwen/commands/`

## Available Commands

All commands are available as TOML files in `.qwen/commands/`:

- `nuaa.design` - Create comprehensive program designs with logic models
- `nuaa.propose` - Generate funding proposals
- `nuaa.measure` - Define impact measurement frameworks
- `nuaa.engage` - Create stakeholder engagement plans
- `nuaa.document` - Generate program documentation
- `nuaa.train` - Design training curricula
- `nuaa.risk` - Create risk registers
- `nuaa.report` - Generate progress reports
- `nuaa.refine` - Refine existing documentation
- `nuaa.partner` - Create partnership agreements
- `nuaa.event` - Plan events and activities

## Usage

Each command follows this pattern:

```bash
qwen nuaa.<command> [arguments]
```

For example:

```bash
qwen nuaa.design "Peer Naloxone Program" "People at risk of opioid overdose" "12 months"
```

## Templates and Scripts

This package includes:

- **Templates** (`.nuaa/templates/`): Pre-built document templates for proposals, risk registers, logic models, etc.
- **Scripts** (`.nuaa/scripts/bash/` or `.nuaa/scripts/powershell/`): Helper scripts for creating new features and managing documentation
- **Memory** (`.nuaa/memory/`): NUAA's constitution and organizational context

## NUAA Principles

All commands are designed around NUAA's core values:

- **Peer Leadership**: Centering lived experience in design and delivery
- **Harm Reduction**: Non-judgmental, evidence-based approaches
- **Cultural Safety**: Trauma-informed, LGBTIQ+ inclusive, culturally responsive
- **Consumer Participation**: Meaningful engagement with appropriate remuneration
- **Anti-Stigma**: Rights-based, empowerment-focused framing

## Support

For questions about NUAA CLI or to report issues, contact the NUAA program team or visit: https://github.com/zophiezlan/nuaa-cli

## License

This package is provided for use by NUAA staff, partners, and community members in support of harm reduction work.
