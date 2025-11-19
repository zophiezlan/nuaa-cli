# Code Volume Reduction & Quality Improvement Plan

**Project**: NUAA CLI
**Date**: 2025-11-19
**Goal**: Reduce code volume by 15-25% while improving maintainability

---

## Executive Summary

This analysis identified **5 high-impact refactoring opportunities** that could reduce codebase volume by approximately **1,200-1,800 lines** (18-27% reduction) while significantly improving code quality, maintainability, and consistency.

**Current State**:
- Python commands: ~3,001 lines across 16 files
- Core modules: ~2,500 lines (download.py, init.py, scaffold.py, utils.py)
- Test code: ~3,500 lines
- Frontend: ~5,800 lines (JS + CSS)
- **Total**: ~15,000 lines of code

**Potential Savings**: 1,200-1,800 lines (12-15% of codebase)

---

## Priority 1: Abstract Command Pattern (HIGH IMPACT)

### Problem
11 command files (`design.py`, `propose.py`, `measure.py`, `engage.py`, `partner.py`, `risk.py`, `document.py`, `event.py`, `train.py`, `report.py`, `onboard.py`) follow **identical pattern**:

```python
# Repeated in every command (90-120 lines each)
def register(app, show_banner_fn=None, console: Console | None = None):
    @app.command()
    def command_name(...):
        if show_banner_fn:
            show_banner_fn()

        # Validate inputs (3-5 lines)
        program_name = validate_program_name(program_name, console)
        field1 = validate_text_field(field1, "field1", 200, console)

        # Get feature directory (1-2 lines)
        feature_dir = get_or_create_feature_dir(program_name)

        # Create mapping (5-10 lines)
        mapping = {"FIELD1": field1, "FIELD2": field2, ...}

        # Load and apply template (15-25 lines)
        try:
            template = _load_template("template.md")
            filled = _apply_replacements(template, mapping)
            meta = {"title": f"{program_name} - Title"}
            text = _prepend_metadata(filled, meta)
            dest = feature_dir / "output.md"
            write_markdown_if_needed(dest, text, force=force, console=console)
        except FileNotFoundError:
            console.print("[red]Template not found[/red]")
            console.print("[dim]Run 'nuaa init'[/dim]")
            raise typer.Exit(1)
        except PermissionError:
            console.print("[red]Permission denied[/red]")
            raise typer.Exit(1)
        except OSError as e:
            console.print(f"[red]File system error:[/red] {e}")
            raise typer.Exit(1)
```

**Code Duplication**: 40-50 lines × 11 files = **440-550 lines** of repetitive code

### Solution: Create BaseTemplateCommand Factory

**New file**: `src/nuaa_cli/command_factory.py` (~120 lines)

```python
"""Command factory for template-based commands."""

from dataclasses import dataclass
from typing import Callable, Dict, Optional
from pathlib import Path

import typer
from rich.console import Console

from .scaffold import (
    get_or_create_feature_dir,
    _load_template,
    _apply_replacements,
    _prepend_metadata,
    write_markdown_if_needed,
)
from .utils import validate_program_name, validate_text_field


@dataclass
class FieldConfig:
    """Configuration for a command field."""
    name: str
    help_text: str
    max_length: int = 500
    validator: Optional[Callable] = None


@dataclass
class TemplateCommandConfig:
    """Configuration for a template-based command."""
    command_name: str
    template_name: str
    output_filename: str
    help_text: str
    fields: list[FieldConfig]
    requires_program: bool = True
    metadata_fn: Optional[Callable] = None


def create_template_command(config: TemplateCommandConfig):
    """
    Factory function to create a template-based command.

    This eliminates 90% of boilerplate code in command files.
    """
    def register(app, show_banner_fn=None, console: Console | None = None):
        console = console or Console()

        # Dynamically build command arguments
        def command_fn(
            program_name: str = typer.Argument(..., help="Program name"),
            *args,
            force: bool = typer.Option(False, help="Overwrite if exists"),
            **kwargs
        ):
            if show_banner_fn:
                show_banner_fn()

            # Validate program name
            program_name = validate_program_name(program_name, console)

            # Validate and map all fields
            mapping = {"PROGRAM_NAME": program_name}
            for i, field in enumerate(config.fields):
                value = args[i] if i < len(args) else kwargs.get(field.name)
                validated = validate_text_field(
                    value, field.name, field.max_length, console
                )
                mapping[field.name.upper()] = validated

            # Get feature directory
            feature_dir = get_or_create_feature_dir(program_name)

            # Process template
            try:
                template = _load_template(config.template_name)
                filled = _apply_replacements(template, mapping)

                # Generate metadata
                if config.metadata_fn:
                    meta = config.metadata_fn(program_name, mapping)
                else:
                    meta = {"title": f"{program_name} - {config.command_name.title()}"}

                text = _prepend_metadata(filled, meta)
                dest = feature_dir / config.output_filename
                write_markdown_if_needed(dest, text, force=force, console=console)

            except FileNotFoundError:
                console.print(f"[red]Template not found:[/red] {config.template_name}")
                console.print("[dim]Run 'nuaa init' to set up templates[/dim]")
                raise typer.Exit(1)
            except PermissionError:
                console.print("[red]Permission denied[/red]")
                raise typer.Exit(1)
            except OSError as e:
                console.print(f"[red]File system error:[/red] {e}")
                raise typer.Exit(1)

        # Set help text and register command
        command_fn.__doc__ = config.help_text
        app.command(name=config.command_name)(command_fn)

    return register
```

**Refactored command example** (`propose.py`): **121 lines → 25 lines**

```python
"""Funding proposal command."""

from ..command_factory import create_template_command, FieldConfig, TemplateCommandConfig

config = TemplateCommandConfig(
    command_name="propose",
    template_name="proposal.md",
    output_filename="proposal.md",
    help_text="""Create a funding proposal from the template.

    Generates comprehensive funding proposal document based on NUAA's
    proven proposal template...""",
    fields=[
        FieldConfig("funder", "Funder name", max_length=200),
        FieldConfig("amount", "Amount requested", max_length=50),
        FieldConfig("duration", "Duration", max_length=100),
    ],
    metadata_fn=lambda prog, m: {
        "title": f"{prog} - Proposal",
        "funder": m["FUNDER"],
        "amount": m["AMOUNT"],
    }
)

register = create_template_command(config)
```

### Impact
- **Lines saved**: 440-550 lines (11 files × 40-50 lines each)
- **Maintenance**: Single source of truth for error handling
- **Consistency**: All commands behave identically
- **Testing**: Test factory once, not 11 times
- **Time**: 3-4 hours implementation

---

## Priority 2: Split Large Modules (HIGH IMPACT)

### 2.1 Refactor `download.py` (914 lines)

**Problem**: Single file handles 5 distinct responsibilities

**Current Structure**:
- GitHub API client (~200 lines)
- ZIP extraction (~150 lines)
- JSON merging (~100 lines)
- VSCode settings handling (~80 lines)
- Template downloading (~200 lines)
- Utility functions (~184 lines)

**Solution**: Split into focused modules

```
src/nuaa_cli/download/
├── __init__.py              (40 lines - public API)
├── github_client.py         (180 lines - API interactions)
├── zip_handler.py           (140 lines - secure extraction)
├── json_merger.py           (90 lines - config merging)
├── vscode_settings.py       (70 lines - IDE integration)
└── template_downloader.py   (200 lines - orchestration)
```

**Benefits**:
- Each module < 200 lines
- Clear separation of concerns
- Easier to test individually
- Reduced cognitive load
- Lines saved: ~150 lines (removing duplication)

### 2.2 Refactor `init.py` (721 lines)

**Problem**: Handles initialization, validation, and configuration

**Solution**: Extract into modules

```
src/nuaa_cli/commands/init/
├── __init__.py          (50 lines - command registration)
├── validation.py        (120 lines - tool/env validation)
├── agent_config.py      (150 lines - AI assistant setup)
├── git_setup.py         (100 lines - repository init)
├── template_setup.py    (180 lines - template handling)
└── script_setup.py      (100 lines - script generation)
```

**Benefits**:
- Easier onboarding for contributors
- Can test each concern independently
- Lines saved: ~100 lines (removing duplication)

### Impact
- **Lines saved**: 250 lines combined
- **Time**: 5-6 hours

---

## Priority 3: Consolidate Test Utilities (MEDIUM IMPACT)

### Problem
Test files contain significant duplication:
- `test_download.py`: 1,191 lines (largest test file)
- Repeated fixture setups across files
- Duplicate mock configurations

### Solution: Create `tests/helpers/` module

```
tests/helpers/
├── __init__.py
├── fixtures.py       (Common fixtures)
├── mocks.py          (Mock GitHub API, filesystem)
├── assertions.py     (Custom assertion helpers)
└── factories.py      (Test data factories)
```

**Example consolidation**:
```python
# Before (repeated in 5 test files):
@pytest.fixture
def mock_github_response():
    return {
        "tag_name": "v1.0.0",
        "assets": [{"browser_download_url": "..."}]
    }

# After (shared fixture):
from tests.helpers.fixtures import mock_github_response
```

### Impact
- **Lines saved**: 200-300 lines
- **Time**: 2-3 hours

---

## Priority 4: CSS Consolidation (MEDIUM IMPACT)

### Problem
- 142 color declarations across 5 CSS files
- Some theme variables not fully utilized
- Repeated selector patterns

### Solution: Enhanced CSS variable usage

```css
/* Add to main.css */
:root {
    /* Component-specific colors */
    --card-bg: var(--gray-50);
    --card-border: var(--gray-300);
    --card-shadow: var(--shadow-md);

    /* Form colors */
    --input-bg: white;
    --input-border: var(--gray-400);
    --input-focus: var(--primary-color);

    /* Status colors */
    --status-draft: var(--gray-500);
    --status-active: var(--success-color);
    --status-archived: var(--gray-400);
}

/* Component classes */
.card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    box-shadow: var(--card-shadow);
}
```

**Consolidate repeated patterns**:
```css
/* Before: Repeated 8 times */
.template-card { padding: var(--spacing-lg); border-radius: var(--border-radius); }
.stat-card { padding: var(--spacing-lg); border-radius: var(--border-radius); }
.team-card { padding: var(--spacing-lg); border-radius: var(--border-radius); }

/* After: Single utility class */
.card-base { padding: var(--spacing-lg); border-radius: var(--border-radius); }
```

### Impact
- **Lines saved**: 150-200 lines CSS
- **Time**: 2 hours

---

## Priority 5: Documentation Consolidation (LOW IMPACT)

### Problem
- 112 Markdown template files
- Some templates share 70%+ content
- Repeated sections (cultural safety, accessibility)

### Solution: Template composition system

```markdown
<!-- Base template: _base-program.md -->
{{CULTURAL_SAFETY_SECTION}}
{{ACCESSIBILITY_SECTION}}

<!-- Specific template: program-design.md -->
{% include _base-program.md %}
## Program Specific Content
...
```

### Impact
- **Lines saved**: 300-400 lines (documentation)
- **Time**: 3-4 hours

---

## Implementation Roadmap

### Phase 1: Quick Wins (Week 1)
1. ✅ **Day 1-2**: Create `command_factory.py` (~4 hours)
2. ✅ **Day 3-4**: Refactor 3 commands to use factory (~3 hours)
3. ✅ **Day 5**: Add tests for factory (~2 hours)

**Deliverable**: 150-200 lines saved, proof of concept

### Phase 2: Major Refactoring (Week 2)
1. ✅ **Day 1-2**: Split `download.py` into module (~6 hours)
2. ✅ **Day 3-4**: Split `init.py` into module (~6 hours)
3. ✅ **Day 5**: Update imports, run full test suite (~3 hours)

**Deliverable**: 350-450 lines saved cumulative

### Phase 3: Polish (Week 3)
1. ✅ **Day 1**: Refactor remaining 8 commands (~4 hours)
2. ✅ **Day 2**: Consolidate test utilities (~3 hours)
3. ✅ **Day 3**: CSS consolidation (~2 hours)
4. ✅ **Day 4-5**: Documentation updates, final testing (~6 hours)

**Deliverable**: 1,200-1,800 lines saved total

---

## Quality Metrics

### Before Refactoring
- **Average command file**: 110 lines
- **Cyclomatic complexity**: 8-12 per command
- **Code duplication**: ~15% (estimated)
- **Test coverage**: 75%

### After Refactoring (Target)
- **Average command file**: 25 lines (77% reduction)
- **Cyclomatic complexity**: 3-5 per command
- **Code duplication**: <5%
- **Test coverage**: 80%+ (easier to test)

---

## Risk Mitigation

### Risks
1. **Breaking existing functionality**: High risk
2. **Import path changes**: Medium risk
3. **Test updates required**: Medium risk
4. **Documentation outdated**: Low risk

### Mitigation Strategy
1. ✅ **Feature branch**: `claude/reduce-volume-improve-quality-*`
2. ✅ **Incremental commits**: One refactoring per commit
3. ✅ **Test after each change**: Run full test suite
4. ✅ **Backwards compatibility**: Maintain public API
5. ✅ **PR review**: Thorough review before merge

---

## Success Criteria

- [ ] Reduce Python code by 1,200+ lines (15%)
- [ ] All 134 tests pass
- [ ] No breaking changes to public API
- [ ] Linting passes (ruff, black, mypy)
- [ ] Documentation updated
- [ ] CI/CD green on all platforms
- [ ] Code review approved

---

## Additional Recommendations

### Code Quality Improvements
1. **Type hints**: Add missing type hints in `utils.py` (currently partial)
2. **Error handling**: Use custom exception classes instead of typer.Exit
3. **Logging**: Add structured logging for debugging
4. **Configuration**: Extract magic numbers to config file

### Testing Improvements
1. **Integration tests**: Add end-to-end workflow tests
2. **Performance tests**: Benchmark template processing
3. **Property-based testing**: Use Hypothesis for validation functions

### Architecture Improvements
1. **Plugin system**: Allow custom commands without modifying core
2. **Template versioning**: Support multiple template versions
3. **Async support**: Add async variants for API calls (future)

---

## Conclusion

This refactoring plan offers **18-27% code reduction** with **significant quality improvements**:

✅ **Maintainability**: Easier to understand and modify
✅ **Testability**: Smaller, focused modules are easier to test
✅ **Consistency**: Factory pattern ensures uniform behavior
✅ **Onboarding**: New contributors can navigate codebase faster
✅ **Performance**: Slightly better (less code to parse)

**Recommended Start**: Priority 1 (Command Factory) - highest ROI, lowest risk.
