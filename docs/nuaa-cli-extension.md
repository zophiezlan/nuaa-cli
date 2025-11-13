# NUAA CLI Extension Design (Planning)

Status: DRAFT
Target Release Window: Q1 2026 (subject to prioritization)

## Overview

Add NUAA‑specific subcommands to the Specify CLI to streamline creation of NUAA program design, evaluation, proposal, and reporting artifacts. Goal: reduce manual navigation & copy/paste; enforce consistent scaffolding, flags, and quality checks.

## Proposed Commands

| Command                | Purpose                                                            | Primary Inputs                                                | Outputs                                        | Notes                                       |
| ---------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------- | ---------------------------------------------- | ------------------------------------------- |
| `specify nuaa init`    | Scaffold NUAA kit structure into an existing repo or new project   | `--path`, `--include-ms365`, `--status`                       | Folder tree, baseline docs, placeholder README | Non‑destructive if folders exist            |
| `specify nuaa design`  | Generate program design template populated with flag defaults      | Program name, duration, target population, optional `--depth` | `program-design.md` (draft)                    | Wraps AI prompt assembly                    |
| `specify nuaa measure` | Create evaluation framework from existing design                   | Program name, period, budget                                  | `impact-framework.md`                          | Applies command flag schema                 |
| `specify nuaa propose` | Produce funding proposal skeleton referencing existing logic model | Program name, funder, amount, duration                        | `proposal.md`                                  | Inserts procurement/funder alignment blocks |
| `specify nuaa report`  | Generate periodic progress/evaluation report                       | Period, program name, stage                                   | `report.md`                                    | Pulls indicators from dictionary            |
| `specify nuaa refine`  | Suggest modifications based on measurement findings                | Program name, change summary                                  | Diff set / updated design sections             | Integrates remediation actions log          |

(Initial implementation may restrict scope to `init` + one artifact command.)

## Command Contract Examples

### `specify nuaa init`

- Inputs: `--path` (default `.`), `--include-ms365` (bool), `--status` (initial status label), `--force` (overwrite placeholders)
- Outputs: Creates `nuaa-kit/` with docs, templates, examples, scripts; returns summary table to console.
- Error Modes:
  - Path not writable → abort with message
  - Existing files conflict without `--force` → skip and list conflicts
  - Missing Python dependency (future quality scripts) → warn
- Success Criteria: All required baseline files created or confirmed present; summary lists skipped/created items.

### `specify nuaa design`

- Inputs: `PROGRAM_NAME`, flags (see schema), optional raw context file path
- Process: Validate flags against `schema.json`, assemble prompt, invoke selected AI agent (future integration), write draft file with front matter `status: draft`.
- Outputs: Draft `program-design.md`, console summary of sections generated.
- Edge Cases: Missing required fields → interactive prompt fallback; unsupported flag value → validation error.

## Flags (Shared)

Pulled from `nuaa-kit/commands/schema.json`:

- `--format` (professional | engaging | partnership)
- `--focus` (budget | evaluation | storytelling)
- `--depth` (light | standard | comprehensive)
- `--participatory` (light | standard | high)
- `--methods` (quantitative | qualitative | mixed)
- `--length` (short | full)

Validation service will read schema JSON and surface allowed values with suggestions.

## Architecture Sketch

```text
[Typer App] --> [nuaa subcommand group] --> [Handlers]
                                      \--> [Schema Validation Service]
                                      \--> [Template Renderer]
                                      \--> [AI Prompt Builder]
                                      \--> [Placeholder Linter Integration]
```

- Keep NUAA logic isolated in `src/nuaa_cli/nuaa_extension/` package (future) to avoid cluttering root.
- Late binding of AI agent logic (user may select Claude/Gemini/etc. globally)
- Ensure no circular imports with existing root `__init__.py`.

## Migration / Adoption Plan

1. Phase 0 (Current): Documentation & planning only.
2. Phase 1: Implement `specify nuaa init` (non‑destructive scaffolder) + schema validation utility.
3. Phase 2: Add `design` + `measure` commands using existing templates.
4. Phase 3: Integrate AI agent selection & prompt generation (respect AGENT_CONFIG).
5. Phase 4: Add `report` + `refine` commands (requires stable data dictionary workflows).
6. Phase 5: Add automation layer (readability scoring, stigma scan).

## Quality & Testing Strategy

- Unit tests for flag validation (allowed values, defaults).
- Snapshot tests for scaffold output (directory + file names).
- Lint tests: confirm generated markdown passes markdownlint & placeholder scripts.
- Future integration tests: simulate program lifecycle (design → measure → report → refine).

## Risks & Mitigations

| Risk                       | Impact               | Mitigation                                         |
| -------------------------- | -------------------- | -------------------------------------------------- |
| Scope creep                | Delayed release      | Phase gating, minimal MVP first                    |
| Template drift             | Inconsistent files   | Central template registry + version tags           |
| Agent variability          | Inconsistent prompts | Abstract prompt builder; use schema-driven mapping |
| Overwriting user changes   | Data loss            | Safe writes, diff preview, `--force` option        |
| Performance lag (AI calls) | Slow UX              | Async execution + caching of prompts               |

## Open Questions

- Should `init` optionally import historical versions? (Version pinning)
- Need for `--license` injection or governance metadata front matter?
- Extent of automatic indicator hydration from CSV (Phase 3+)

## Future Enhancements

- `specify nuaa audit` for accessibility + stigma scan report
- `specify nuaa diff` to compare two versions of a design or evaluation framework
- Telemetry (opt-in) for command usage to prioritise improvement

---

This document will evolve before implementation; no code integration performed yet.
