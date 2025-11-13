# NUAA CLI Commands

Status: ✅ IMPLEMENTED (v0.3.0+)

## Overview

The NUAA CLI provides first-class subcommands for NUAA program design, evaluation, proposal, and reporting workflows. All commands create structured Markdown artifacts using the templates in `nuaa-kit/templates/` with automatic feature directory scaffolding, slug generation, and metadata stamping.

## Implemented Commands

| Command         | Purpose                                           | Primary Inputs                          | Outputs                        | Status         |
| --------------- | ------------------------------------------------- | --------------------------------------- | ------------------------------ | -------------- |
| `nuaa design`   | Generate program design template with logic model | Program name, target, duration          | `program-design.md`, etc.      | ✅ Implemented |
| `nuaa propose`  | Create funding proposal from template             | Program name, funder, amount, duration  | `proposal.md`                  | ✅ Implemented |
| `nuaa measure`  | Define or update evaluation framework             | Program name, period, budget            | `impact-framework.md`          | ✅ Implemented |
| `nuaa document` | Document existing programs (brownfield)           | Program name                            | `existing-program-analysis.md` | ✅ Implemented |
| `nuaa report`   | Generate report scaffold                          | Program name, `--type` (progress/final) | `report.md`                    | ✅ Implemented |
| `nuaa refine`   | Record refinement in program changelog            | Program name, `--note`                  | Appends to `CHANGELOG.md`      | ✅ Implemented |

## Implementation Details

### Feature Directory Scaffolding

All commands use automatic feature numbering:

- `nuaa/001-program-slug/`
- `nuaa/002-another-program/`
- etc.

Slugs are automatically generated from program names using snake_case conversion.

### Command Examples

```bash
# Create a comprehensive program design
nuaa design "Peer Naloxone Distribution" "people at risk of opioid overdose" "12 months"

# Generate a funding proposal
nuaa propose "Peer Naloxone Distribution" "NSW Health" "$50000" "12 months"

# Define evaluation framework
nuaa measure "Peer Naloxone Distribution" "12 months" "$7000"

# Document existing program
nuaa document "Outreach & Needle Exchange"

# Create progress report
nuaa report "Peer Naloxone Distribution" --type progress

# Record a refinement
nuaa refine "Peer Naloxone Distribution" --note "Updated budget after pilot feedback"
```

## Flags (Shared)

Pulled from `nuaa-kit/commands/schema.json`:

- `--format` (professional | engaging | partnership)
- `--focus` (budget | evaluation | storytelling)
- `--depth` (light | standard | comprehensive)
- `--participatory` (light | standard | high)
- `--methods` (quantitative | qualitative | mixed)
- `--length` (short | full)

Validation service will read schema JSON and surface allowed values with suggestions.

## Architecture

The NUAA CLI uses modular command registration with shared utilities:

```text
src/nuaa_cli/
├── __init__.py           # Main Typer app, AGENT_CONFIG
├── commands/
│   ├── design.py         # nuaa design
│   ├── propose.py        # nuaa propose
│   ├── measure.py        # nuaa measure
│   ├── document.py       # nuaa document
│   ├── report.py         # nuaa report
│   └── refine.py         # nuaa refine
├── utils.py              # StepTracker, check_tool
└── scaffold.py           # Template & file helpers
```

Key helpers:

- `get_or_create_feature_dir()` - Auto-numbering and slug generation
- `write_markdown_if_needed()` - Safe writes with force flag
- Template discovery from multiple search paths
- YAML frontmatter prepending

## Testing

Comprehensive test coverage implemented:

- `tests/test_cli_basic.py` - Command scaffolding tests
- `tests/test_scaffold_helpers.py` - Feature directory and write logic tests
- `tests/test_version.py` - Network-mocked version command tests
- `scripts/python/e2e_smoke_test.py` - End-to-end workflow validation

CI runs lint (Ruff), type checks (mypy), unit tests (pytest), and E2E tests across Windows and Ubuntu.

## Roadmap

Planned improvements:

- Direct AI agent invocation for richer validation
- Enhanced flag validation from schema.json
- Readability scoring integration
- Automated stigma language scanning
- Version pinning for templates
- Automatic indicator hydration from evaluation data dictionary
- `nuaa audit` for accessibility and stigma scan reporting
- `nuaa diff` to compare versions of design or evaluation frameworks
- Telemetry (opt-in) for command usage analytics
