# NUAA Kit Changelog

All notable changes to the NUAA adaptation of Spec Kit are documented here. This changelog tracks kit‑specific content (commands, templates, guidance) separate from the core Specify CLI (`pyproject.toml` + `CHANGELOG.md`).

Format: YYYY-MM-DD Semantic grouping (Added / Changed / Removed / Deprecated / Fixed / Security)

## [Unreleased]

### Added

- None.

### Changed

- None.

### Fixed

- None.

### Deprecated

- None.

### Removed

- None.

### Security

- None.

## 2025-11-10 Phase 3B Implementation - Brownfield Documentation & M365 Integration

### Added

- **Document Command** (`commands/document.md`) - Complete implementation (v1.0.0)

  - Comprehensive brownfield documentation command for existing programs
  - Detailed interview protocols (staff, peer workers, participants)
  - 4-phase documentation workflow (Discovery, Knowledge Capture, Documentation, Validation)
  - Gap analysis framework (documentation, operational, NUAA principles alignment)
  - Reconstructed logic model methodology
  - Strengths preservation framework
  - Implementation roadmap with phased recommendations
  - Data collection guidance for establishing baselines
  - Quality checklist (12 validation points)
  - Integration with existing NUAA-Kit workflows

- **Existing Program Analysis Template** (`templates/existing-program-analysis.md`) - Complete implementation (v1.0.0)

  - Comprehensive 9-section analysis framework
  - Program background and historical context sections
  - Current state documentation (inputs, activities, outputs, outcomes, impact)
  - Reconstructed logic model structure with Mermaid diagram
  - Detailed gap analysis across documentation, operations, and NUAA principles
  - Strengths identification and institutional knowledge capture
  - Prioritized recommendations (immediate, short-term, medium-term, long-term)
  - Implementation roadmap with timelines and owners
  - Baseline measurement guidance
  - 6 comprehensive appendices (interviews, documents, timeline, stakeholders, finances, testimonials)
  - Quality checklist (11 validation points)
  - 35,000+ words of detailed guidance

- **Microsoft 365 Integration Guide** (`microsoft365/README.md`) - Phase 1 implementation
  - Quick start manual integration methods (immediate use, no setup)
  - Word document export guidance with branding standards
  - Excel spreadsheet integration (budget calculator, impact dashboard, evaluation tracking)
  - SharePoint organization structure and version control best practices
  - Teams collaboration setup and notification workflows
  - Power Automate workflow specifications (4 planned workflows for Q2 2026)
  - Word and Excel template specifications for future automation
  - Data privacy and security guidelines
  - Troubleshooting section
  - Training and support resources
  - Detailed roadmap (Q4 2025 - Q4 2026)

### Changed

- **STATUS.md** - Updated implementation status
  - Added Existing Program Analysis Template: ✅ Implemented (2025-11-10)
  - Added Document Command Doc: ✅ Implemented (2025-11-10)
  - Microsoft 365 Integration: Planned → ⚠️ Phase 1 Complete (manual integration guidance)
  - Updated notes for M365: "Manual integration guidance implemented; automation planned Q2 2026"

### Fixed

- None.

### Deprecated

- None.

### Removed

- None.

### Security

- Added comprehensive data privacy and security guidance in Microsoft 365 integration
  - Participant-level data protection requirements
  - SharePoint security settings (sensitivity labels, access controls, encryption)
  - Excel security (sheet protection, hidden formulas, data validation)
  - Access audit requirements

## 2025-11-10 Phase 3A Implementation - High-Value Feature Completion

### Added

- **Budget Calculator Template** (`templates/budget-calculator.md`) - Complete implementation (v1.0.0)

  - Comprehensive budget structure with 6 core categories (Personnel, Peer Remuneration, Operations, Participant Support, Evaluation, Administration)
  - NUAA remuneration standards ($300/session baseline)
  - Automatic calculation formulas for Excel export
  - Sensitivity analysis scenarios (80% reduced, 120% expanded funding)
  - Budget assumptions documentation section
  - Version history tracking template
  - Quality checklist with 12 validation points
  - Export guidance for Word, Excel, SharePoint
  - Integration notes with other NUAA-Kit artifacts

- **Report Command** (`commands/report.md`) - Complete implementation (v1.0.0)

  - Multi-audience report formats (funder, community, internal)
  - Comprehensive report template structure (9 sections)
  - Data synthesis guidance from impact framework indicators
  - Equity analysis section with disaggregated data tables
  - Budget vs. actual reporting for funder accountability
  - Lessons learned and recommendations framework
  - Participant voices section with ethical representation guidelines
  - Export guidance for Word, SharePoint, community dissemination
  - Quality checklist with 13 validation points
  - Integration with program design, logic model, impact framework

- **Refine Command** (`commands/refine.md`) - Complete implementation (v1.0.0)

  - Systematic feedback integration workflows
  - Version control and change documentation guidance
  - Cross-artifact consistency checking
  - 5 detailed refinement workflows (consumer advisory, funder response, mid-program iteration, consistency check, pre-submission quality)
  - Common refinement focus areas (logic model, budget, evaluation, narrative, stakeholders)
  - Semantic versioning scheme (MAJOR.MINOR.PATCH)
  - Changelog format template
  - Placeholder lint check integration
  - Quality checklist with 11 validation points
  - Advanced refinement scenarios (conflicting feedback, mid-program pivot, scalability)

- **Command Flags Schema** (`commands/schema.json`) - Enhanced to v1.1.0
  - Added 'document' command to appliesTo enums
  - Expanded format values (funder, community, internal, all)
  - New flags: mode, preserve, check-consistency, feedback, data-source, report-type, export
  - Brownfield documentation flags: running-since, current-participants, budget-amount
  - Expanded focus values (13 total options)
  - Comprehensive usage examples for all 6 commands
  - Schema governance notes (consistency, extensibility, validation, combinations)
  - Full changelog section

### Changed

- **STATUS.md** - Updated implementation status
  - Budget Calculator Template: Planned (stub) → ✅ Implemented (2025-11-10)
  - Report Command Doc: Planned (stub) → ✅ Implemented (2025-11-10)
  - Refine Command Doc: Planned (stub) → ✅ Implemented (2025-11-10)
  - Command Flags Schema: Planned → ✅ Implemented v1.1.0 (2025-11-10)

### Fixed

- None.

### Deprecated

- None.

### Removed

- None.

### Security

- None.

## 2025-11-11 Initial Draft Baseline

### Added

- Initial glossary (`glossary.md`) covering evaluation and harm reduction terminology.
- Accessibility & Inclusive Content Guidelines (`accessibility-guidelines.md`).
- Command flags schema (`commands/schema.json`) v1.0.0.
- Placeholder lint scripts (PowerShell + Bash).
- Evaluation data dictionary and indicator CSV example.
- Stubs: `report.md`, `refine.md`, `budget-calculator.md` (PLANNED).
- Core NUAA command documents: `design.md`, `measure.md`, `propose.md`.
- Supporting templates: `program-design.md`, `logic-model.md`, `impact-framework.md`, `proposal.md`.
- `STATUS.md` tracking implemented vs planned artifacts.
- Microsoft365 scaffolding directories.

### Changed

- Normalized ordered list spacing in `commands/design.md`.
- Updated `nuaa-kit/README.md` directory tree and added pre‑submission checks section.
- Adjusted schema draft to 07 for compatibility.

### Fixed

- Initial markdown lint errors (code fence languages, blank lines around headings, tables).
- Markdown heading/list spacing issues in newly added documents.

### Deprecated / Removed / Security

- None.

## 2025-11-11 Initial Draft Baseline

### Added

- Core NUAA command documents: `design.md`, `measure.md`, `propose.md`.
- Supporting templates: `program-design.md`, `logic-model.md`, `impact-framework.md`, `proposal.md`.
- `STATUS.md` tracking implemented vs planned artifacts.
- Microsoft365 scaffolding directories.

### Changed

- Adjusted schema draft to 07 for compatibility.

### Fixed

- Initial markdown lint errors (code fence languages, blank lines around headings, tables).

### Deprecated / Removed / Security

- None.

---

Release process:

1. Update documents and run placeholder + markdown lint checks.
2. Increment [Unreleased] entries into dated section upon tagging.
3. Peer review significant content changes (glossary, evaluation frameworks) prior to release.
4. Keep entries concise; cross‑reference detailed diffs in version control as needed.
