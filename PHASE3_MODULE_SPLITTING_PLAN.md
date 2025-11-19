# Phase 3: Module Splitting Implementation Plan

**Status**: ✅ Completed (see PHASE3_COMPLETION_SUMMARY.md)
**Estimated Effort**: 1 week
**Estimated Savings**: ~250 lines
**Priority**: High (Better organization + line reduction)

---

## Overview

Split two large monolithic files (`download.py` and `init.py`) into focused, maintainable modules. This improves organization, reduces duplication, and makes testing easier.

---

## Target 1: download.py (914 lines → ~720 lines)

### Current Structure Analysis

```python
download.py (914 lines)
├── Imports & Setup (lines 1-57)
├── GitHub Client (lines 59-217)      # 158 lines
├── ZIP Extraction (lines 219-264)     # 45 lines
├── VSCode Settings (lines 266-337)    # 71 lines
├── JSON Merging (lines 339-401)       # 62 lines
└── Download Orchestration (lines 403-914)  # 511 lines
```

### Proposed Module Structure

```
src/nuaa_cli/download/
├── __init__.py                 # Public API (40 lines)
├── github_client.py            # GitHub API interactions (180 lines)
├── zip_handler.py              # Secure ZIP extraction (70 lines)
├── json_merger.py              # JSON merging logic (90 lines)
├── vscode_settings.py          # VSCode-specific handling (90 lines)
└── template_downloader.py      # Main orchestration (290 lines)
```

### Detailed Breakdown

#### 1. `github_client.py` (~180 lines)
**Purpose**: GitHub API authentication and rate limiting

**Functions to Extract**:
- `_github_token()` - Token resolution from env/CLI
- `_github_auth_headers()` - Authorization header generation
- `_parse_rate_limit_headers()` - Rate limit parsing
- `_format_rate_limit_error()` - User-friendly error messages

**Dependencies**: `httpx`, `os`, `datetime`

**Example**:
```python
"""GitHub API client utilities."""

import os
from datetime import datetime, timezone
from typing import Optional

import httpx


def get_github_token(cli_token: Optional[str] = None) -> Optional[str]:
    """Get GitHub token from CLI, GH_TOKEN, or GITHUB_TOKEN."""
    return ((cli_token or os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN") or "").strip()) or None


def get_auth_headers(cli_token: Optional[str] = None) -> dict:
    """Generate authorization headers for GitHub API."""
    token = get_github_token(cli_token)
    return {"Authorization": f"Bearer {token}"} if token else {}


def parse_rate_limit(headers: httpx.Headers) -> dict:
    """Extract rate limit information from GitHub API response headers."""
    ...


def format_rate_limit_error(status_code: int, headers: httpx.Headers, url: str) -> str:
    """Format user-friendly rate limit error message."""
    ...
```

#### 2. `zip_handler.py` (~70 lines)
**Purpose**: Secure ZIP file extraction

**Functions to Extract**:
- `safe_extract_zip()` - Path traversal protection

**Dependencies**: `zipfile`, `pathlib`, `typer`, `rich`

**Example**:
```python
"""Secure ZIP file extraction utilities."""

import zipfile
from pathlib import Path

import typer
from rich.console import Console


def safe_extract_zip(
    zip_ref: zipfile.ZipFile,
    extract_path: Path,
    console: Console = Console()
) -> None:
    """
    Safely extract ZIP file, preventing path traversal attacks.

    Validates all paths before extraction to prevent writing outside
    the target directory.
    """
    extract_path = extract_path.resolve()

    for member in zip_ref.namelist():
        member_path = (extract_path / member).resolve()

        try:
            member_path.relative_to(extract_path)
        except ValueError:
            console.print(f"[red]Security Error:[/red] ZIP contains invalid path: {member}")
            console.print("[dim]This file may be malicious. Extraction aborted.[/dim]")
            raise typer.Exit(1)

    zip_ref.extractall(extract_path)
```

#### 3. `json_merger.py` (~90 lines)
**Purpose**: Deep JSON merging for configuration files

**Functions to Extract**:
- `merge_json_files()` - Deep merge two JSON files

**Dependencies**: `json`, `pathlib`

**Example**:
```python
"""JSON configuration file merging utilities."""

import json
from pathlib import Path
from typing import Any, Dict


def merge_json_files(src_file: Path, dest_file: Path) -> Dict[str, Any]:
    """
    Deep merge two JSON files.

    Recursively merges src_file into dest_file, preserving existing
    values while adding new ones from src_file.
    """
    # Load source
    with open(src_file, 'r', encoding='utf-8') as f:
        src_data = json.load(f)

    # Load or initialize destination
    if dest_file.exists():
        with open(dest_file, 'r', encoding='utf-8') as f:
            dest_data = json.load(f)
    else:
        dest_data = {}

    # Deep merge
    merged = _deep_merge(dest_data, src_data)

    return merged


def _deep_merge(base: dict, updates: dict) -> dict:
    """Recursively merge updates into base."""
    result = base.copy()

    for key, value in updates.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value

    return result
```

#### 4. `vscode_settings.py` (~90 lines)
**Purpose**: VSCode settings.json special handling

**Functions to Extract**:
- `handle_vscode_settings()` - Smart merge for VSCode configs

**Dependencies**: `json_merger`, `pathlib`, `rich`

**Example**:
```python
"""VSCode settings.json special handling."""

from pathlib import Path
from typing import Optional

from rich.console import Console

from .json_merger import merge_json_files
from ..utils import StepTracker


def handle_vscode_settings(
    sub_item: Path,
    dest_file: Path,
    rel_path: Path,
    verbose: bool = False,
    tracker: Optional[StepTracker] = None,
    console: Console = Console(),
) -> None:
    """
    Merge or copy .vscode/settings.json files.

    Preserves user customizations while adding new template settings.
    """
    def log(message: str, color: str = "green") -> None:
        if verbose and not tracker:
            console.print(f"[{color}]{message}[/] {rel_path}")
        elif tracker:
            tracker.start("vscode", detail=str(rel_path))

    # Try smart merge
    try:
        if dest_file.exists():
            log("Merging VSCode settings", "yellow")
            merged = merge_json_files(sub_item, dest_file)
            dest_file.write_text(json.dumps(merged, indent=2))
        else:
            log("Copying VSCode settings")
            shutil.copy2(sub_item, dest_file)
    except Exception as e:
        log(f"VSCode merge failed: {e}, falling back to copy", "yellow")
        shutil.copy2(sub_item, dest_file)
```

#### 5. `template_downloader.py` (~290 lines)
**Purpose**: Main download orchestration

**Functions to Extract**:
- `download_template_from_github()` - Fetch from GitHub releases
- `download_and_extract_template()` - Complete workflow

**Dependencies**: All above modules + `httpx`, `tempfile`, `shutil`

**Example**:
```python
"""Template download orchestration."""

import tempfile
import zipfile
from pathlib import Path
from typing import Optional

import httpx
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .github_client import get_auth_headers, format_rate_limit_error
from .zip_handler import safe_extract_zip
from .vscode_settings import handle_vscode_settings
from ..utils import StepTracker


def download_template_from_github(
    owner: str,
    repo: str,
    tag: Optional[str] = None,
    github_token: Optional[str] = None,
    skip_tls_verify: bool = False,
    console: Console = Console(),
) -> bytes:
    """
    Download template ZIP from GitHub releases.

    Returns ZIP file content as bytes.
    """
    ...


def download_and_extract_template(
    dest_dir: Path,
    owner: str = "zophiezlan",
    repo: str = "nuaa-project-kit",
    tag: Optional[str] = None,
    github_token: Optional[str] = None,
    skip_tls_verify: bool = False,
    verbose: bool = False,
    tracker: Optional[StepTracker] = None,
    console: Console = Console(),
) -> None:
    """
    Complete workflow: download, extract, and merge template.

    Orchestrates all steps of template installation.
    """
    ...
```

#### 6. `__init__.py` (~40 lines)
**Purpose**: Backward compatibility and public API

**Content**:
```python
"""
NUAA CLI Download Module
========================

Provides functionality for downloading and extracting NUAA project templates
from GitHub releases with secure handling and smart configuration merging.

Public API:
    - download_template_from_github: Fetch from GitHub
    - download_and_extract_template: Complete workflow
    - merge_json_files: Deep merge JSON configs
"""

# Re-export public API for backward compatibility
from .template_downloader import (
    download_template_from_github,
    download_and_extract_template,
)
from .json_merger import merge_json_files
from .vscode_settings import handle_vscode_settings

__all__ = [
    'download_template_from_github',
    'download_and_extract_template',
    'merge_json_files',
    'handle_vscode_settings',
]
```

### Expected Savings

- **Original**: 914 lines
- **New Total**: ~720 lines (180 + 70 + 90 + 90 + 290 + 40 = 760)
- **Savings**: ~150 lines
- **Source**: Removed duplicate imports, docstring consolidation, reduced redundancy

---

## Target 2: init.py (721 lines → ~620 lines)

### Current Structure Analysis

```python
init.py (721 lines)
├── Imports & Setup (lines 1-77)
├── Agent Config Loading (lines 79-126)
├── Tool Validation (lines 128-300)
├── Agent Selection UI (lines 302-420)
├── Git Repository Setup (lines 422-520)
├── Script Generation (lines 522-650)
└── Main Init Command (lines 652-721)
```

### Proposed Module Structure

```
src/nuaa_cli/commands/init/
├── __init__.py             # Command registration (50 lines)
├── agent_config.py         # Agent configuration (150 lines)
├── validation.py           # Tool validation (120 lines)
├── git_setup.py            # Git initialization (100 lines)
├── script_generation.py    # Script creation (120 lines)
└── ui_helpers.py           # Interactive UI (100 lines)
```

### Detailed Breakdown

#### 1. `agent_config.py` (~150 lines)
- Load agents.json
- Parse agent configurations
- Agent-specific settings

#### 2. `validation.py` (~120 lines)
- Check for git
- Verify AI assistant CLIs
- Environment validation

#### 3. `git_setup.py` (~100 lines)
- Initialize git repository
- Create initial commit
- Configure git settings

#### 4. `script_generation.py` (~120 lines)
- Generate agent-specific scripts
- PowerShell vs POSIX shell
- Set file permissions

#### 5. `ui_helpers.py` (~100 lines)
- Interactive agent selection
- Script type selection
- Progress display

#### 6. `__init__.py` (~50 lines)
- Register command with Typer
- Orchestrate initialization workflow
- Backward compatibility

### Expected Savings

- **Original**: 721 lines
- **New Total**: ~620 lines (150 + 120 + 100 + 120 + 100 + 50 = 640)
- **Savings**: ~100 lines
- **Source**: Consolidate imports, reduce duplication, clearer separation

---

## Implementation Steps

### Step 1: Backup & Prepare (5 min)
```bash
# Already done
cp src/nuaa_cli/download.py src/nuaa_cli/download.py.bak
mkdir -p src/nuaa_cli/download
```

### Step 2: Extract download.py Modules (2-3 hours)
1. Create `github_client.py` - Extract GitHub API functions
2. Create `zip_handler.py` - Extract ZIP extraction
3. Create `json_merger.py` - Extract JSON merging
4. Create `vscode_settings.py` - Extract VSCode handling
5. Create `template_downloader.py` - Extract main orchestration
6. Create `__init__.py` - Public API exports

### Step 3: Update Imports (30 min)
```bash
# Find all files importing from download.py
grep -r "from \.download import\|from nuaa_cli\.download import" src/

# Update each import:
# OLD: from .download import download_and_extract_template
# NEW: from .download import download_and_extract_template  # Same! (backward compat)
```

### Step 4: Test download.py Split (30 min)
```bash
pytest tests/test_download.py -v
pytest tests/test_init_command.py -v
python -m nuaa_cli.download  # Smoke test
```

### Step 5: Extract init.py Modules (2-3 hours)
1. Create `commands/init/` directory
2. Extract each module
3. Create `__init__.py` with command registration

### Step 6: Update init Imports (30 min)
```bash
# Update references to init command
grep -r "from \.commands\.init import\|from nuaa_cli\.commands\.init import" src/
```

### Step 7: Test init.py Split (30 min)
```bash
pytest tests/test_init_command.py -v
pytest tests/ -v  # Full suite
```

### Step 8: Clean Up & Document (30 min)
- Remove .bak files
- Update module docstrings
- Add migration notes to CHANGELOG

---

## Testing Strategy

### Unit Tests
```python
# Test individual modules
pytest tests/test_download/test_github_client.py
pytest tests/test_download/test_zip_handler.py
pytest tests/test_download/test_json_merger.py
```

### Integration Tests
```python
# Test full workflows
pytest tests/test_download.py
pytest tests/test_init_command.py
```

### Smoke Tests
```bash
# Quick functionality checks
python -c "from nuaa_cli.download import download_and_extract_template"
nuaa init --help
```

---

## Rollback Plan

If issues arise:

```bash
# Restore backup
cp src/nuaa_cli/download.py.bak src/nuaa_cli/download.py
rm -rf src/nuaa_cli/download/

# Revert commit
git reset --hard HEAD~1
```

---

## Success Criteria

- [  ] All existing tests pass (no regressions)
- [  ] Imports work identically (backward compatibility)
- [  ] Line count reduced by ~250 lines
- [  ] Each module < 200 lines
- [  ] Clear separation of concerns
- [  ] Documentation updated

---

## Benefits

### Immediate
- ✅ Better organization (~250 lines saved)
- ✅ Easier to navigate and understand
- ✅ Each module has single responsibility
- ✅ Simplified testing (test modules independently)

### Long-term
- ✅ Easier onboarding for new contributors
- ✅ Reduced cognitive load
- ✅ Better code reusability
- ✅ Clearer dependency graph
- ✅ Foundation for future improvements

---

## Timeline

| Task | Duration | Cumulative |
|------|----------|------------|
| download.py extraction | 3 hours | 3 hours |
| download.py testing | 30 min | 3.5 hours |
| init.py extraction | 3 hours | 6.5 hours |
| init.py testing | 30 min | 7 hours |
| Documentation & cleanup | 1 hour | 8 hours |

**Total**: ~1 working day (8 hours)

---

## Next Session Checklist

When ready to implement:

1. [ ] Review this plan
2. [ ] Confirm approach with team (if applicable)
3. [ ] Set aside 8-hour block
4. [ ] Create feature branch (if not using existing)
5. [ ] Follow implementation steps above
6. [ ] Run full test suite
7. [ ] Update documentation
8. [ ] Commit and push

---

## Notes

- Keep backward compatibility (imports should work identically)
- Test after each module extraction
- Don't optimize prematurely - focus on organization first
- Document any breaking changes (shouldn't be any)
- Consider adding module-level doctests

---

**Status**: 📝 Ready to execute
**Recommended**: Start fresh session with this plan
**Expected Result**: ~250 lines saved + better organization
