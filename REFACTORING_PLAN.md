# Detailed Refactoring Plan for /home/user/nuaa-cli/src/nuaa_cli/__init__.py

## Current State Analysis

The `__init__.py` file is **1,590 lines** and contains multiple logical concerns:
- HTTP/GitHub API utilities (lines 64-136)
- ZIP download and extraction (lines 138-722)
- JSON file merging (lines 458-534)
- Banner display (lines 209-358)
- Interactive UI components (lines 221-323)
- Git repository operations (lines 396-455)
- Init command implementation (lines 976-1408)
- Command registration and app setup (lines 325-368, 1478-1589)

**Good News**: Many modules have already been extracted (`github_client.py`, individual commands), but the main `__init__.py` still contains several logical sections that should be modularized.

---

## Module Extraction Plan

### Phase 1: Extract HTTP Utilities (Consolidate with Existing github_client.py)

**Status**: Partially exists in `github_client.py` - RECOMMEND CONSOLIDATION

**Current Duplicates in __init__.py**:
- Lines 64-66: `_github_token()`
- Lines 69-72: `_github_auth_headers()`
- Lines 75-101: `_parse_rate_limit_headers()`
- Lines 104-135: `_format_rate_limit_error()`

**Recommendation**:
These functions already exist as methods in `github_client.py` (lines 52-131). The ones in `__init__.py` are standalone functions while `github_client.py` has them as class methods.

**Action**: Add standalone helper functions to `github_client.py` that delegate to the class, OR migrate all code to use the `GitHubClient` class directly.

---

### Phase 2: Extract ZIP/Download Operations → **download.py**

**Extract to**: `/home/user/nuaa-cli/src/nuaa_cli/download.py`

**Functions to extract** (Lines 138-722):
1. `_safe_extract_zip()` - lines 138-171
2. `download_template_from_github()` - lines 537-722
3. `download_and_extract_template()` - lines 724-921
4. `handle_vscode_settings()` - lines 458-490
5. `merge_json_files()` - lines 493-534

**Imports needed**:
```python
import os
import zipfile
import tempfile
import shutil
import json
from pathlib import Path
from typing import Optional, Tuple

import typer
import httpx
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

from .utils import StepTracker
from .github_client import GitHubClient  # For HTTP operations
```

**Dependencies**:
- `rich` (for console output and progress bars)
- `httpx` (for HTTP requests)
- `typer` (for exit handling)
- Internal: `utils.StepTracker`, `github_client.GitHubClient`
- External console object

**Function signatures**:
```python
def _safe_extract_zip(
    zip_ref: zipfile.ZipFile,
    extract_path: Path,
    console: Console
) -> None: ...

def download_template_from_github(
    ai_assistant: str,
    download_dir: Path,
    *,
    script_type: str = "sh",
    verbose: bool = True,
    show_progress: bool = True,
    client: httpx.Client | None = None,
    debug: bool = False,
    github_token: str | None = None,
) -> Tuple[Path, dict]: ...

def download_and_extract_template(
    project_path: Path,
    ai_assistant: str,
    script_type: str,
    is_current_dir: bool = False,
    *,
    verbose: bool = True,
    tracker: StepTracker | None = None,
    client: httpx.Client | None = None,
    debug: bool = False,
    github_token: str | None = None,
) -> Path: ...

def handle_vscode_settings(
    sub_item,
    dest_file,
    rel_path,
    verbose=False,
    tracker=None
) -> None: ...

def merge_json_files(
    existing_path: Path,
    new_content: dict,
    verbose: bool = False
) -> dict: ...
```

**Extraction order**: Extract this FIRST (Phase 2) - others may depend on it.

---

### Phase 3: Extract Git Operations → **git_utils.py**

**Extract to**: `/home/user/nuaa-cli/src/nuaa_cli/git_utils.py`

**Functions to extract** (Lines 370-455):
1. `run_command()` - lines 370-393
2. `is_git_repo()` - lines 396-414
3. `init_git_repo()` - lines 417-455

**Imports needed**:
```python
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple

import typer
from rich.console import Console
```

**Dependencies**:
- `subprocess` (system commands)
- `pathlib.Path`
- `typer` (exit handling)
- `rich.console.Console` (for output)

**Function signatures**:
```python
def run_command(
    cmd: list[str],
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
) -> Optional[str]: ...

def is_git_repo(path: Path | None = None) -> bool: ...

def init_git_repo(
    project_path: Path,
    quiet: bool = False
) -> Tuple[bool, Optional[str]]: ...
```

**Extraction order**: Extract SECOND (Phase 3) - independent module.

---

### Phase 4: Extract Script Permission Management → **scripts.py**

**Extract to**: `/home/user/nuaa-cli/src/nuaa_cli/scripts.py`

**Function to extract** (Lines 924-973):
1. `ensure_executable_scripts()` - lines 924-973

**Imports needed**:
```python
import os
from pathlib import Path
from rich.console import Console
from .utils import StepTracker
```

**Dependencies**:
- `os` (chmod operations)
- `pathlib`
- `rich.console.Console`
- Internal: `utils.StepTracker`

**Function signature**:
```python
def ensure_executable_scripts(
    project_path: Path,
    tracker: StepTracker | None = None
) -> None: ...
```

**Extraction order**: Extract THIRD (Phase 4) - independent module, used by init.

---

### Phase 5: Extract UI/Interactive Components → **ui.py**

**Extract to**: `/home/user/nuaa-cli/src/nuaa_cli/ui.py`

**Functions to extract** (Lines 221-323):
1. `get_key()` - lines 221-239
2. `select_with_arrows()` - lines 242-323

**Imports needed**:
```python
import sys
import readchar

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.live import Live
from rich.align import Align

import typer
```

**Dependencies**:
- `readchar` (keyboard input)
- `rich` (terminal UI)
- `typer` (exit handling)
- External: `console` object (Rich Console)

**Function signatures**:
```python
def get_key() -> str: ...

def select_with_arrows(
    options: dict,
    prompt_text: str = "Select an option",
    default_key: str | None = None
) -> str: ...
```

**Extraction order**: Extract FOURTH (Phase 5) - independent, used by init.

---

### Phase 6: Extract Banner Display → **banner.py**

**Extract to**: `/home/user/nuaa-cli/src/nuaa_cli/banner.py`

**Items to extract** (Lines 209-358):
1. `BANNER` constant - lines 209-216
2. `TAGLINE` constant - line 218
3. `BannerGroup` class - lines 328-334
4. `show_banner()` function - lines 346-358

**Imports needed**:
```python
from rich.console import Console
from rich.text import Text
from rich.align import Align
from typer.core import TyperGroup
```

**Dependencies**:
- `rich` (terminal output)
- `typer` (CLI framework)
- External: `console` object (Rich Console)

**Class/Function signatures**:
```python
BANNER = """..."""
TAGLINE = "..."

class BannerGroup(TyperGroup):
    def format_help(self, ctx, formatter): ...

def show_banner() -> None: ...
```

**Extraction order**: Extract FIFTH (Phase 6) - independent, used by init and check.

---

### Phase 7: Extract Init Command → **init_cmd.py**

**Extract to**: `/home/user/nuaa-cli/src/nuaa_cli/commands/init.py` (move from __init__.py)

**Function to extract** (Lines 976-1408):
1. `init()` command function - lines 976-1408

**Imports needed**:
```python
import os
import sys
import shlex
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from ..utils import StepTracker, check_tool
from ..download import download_and_extract_template
from ..scripts import ensure_executable_scripts
from ..git_utils import is_git_repo, init_git_repo
from ..ui import select_with_arrows
from ..banner import show_banner
from ..scaffold import (
    _slugify,
    _find_templates_root,
    _ensure_nuaa_root,
    _next_feature_dir,
    _find_feature_dir_by_program,
    _load_template,
    _apply_replacements,
    _prepend_metadata,
    _write_markdown,
    _stamp,
)

import httpx
import ssl
import truststore
```

**Dependencies**:
- `download.py` (download_and_extract_template)
- `scripts.py` (ensure_executable_scripts)
- `git_utils.py` (is_git_repo, init_git_repo)
- `ui.py` (select_with_arrows)
- `banner.py` (show_banner)
- `utils.py` (StepTracker, check_tool)
- `scaffold.py` (template imports)
- `AGENT_CONFIG` and `SCRIPT_TYPE_CHOICES` from parent module
- External: `console`, `app` (Typer app instance)

**Function signature**:
```python
def init(
    project_name: str | None = typer.Argument(...),
    ai_assistant: str | None = typer.Option(...),
    script_type: str | None = typer.Option(...),
    ignore_agent_tools: bool = typer.Option(...),
    no_git: bool = typer.Option(...),
    here: bool = typer.Option(...),
    force: bool = typer.Option(...),
    skip_tls: bool = typer.Option(...),
    debug: bool = typer.Option(...),
    github_token: str | None = typer.Option(...),
) -> None: ...

def register(app: typer.Typer, agent_config: dict, console: Console) -> None: ...
```

**Extraction order**: Extract LAST (Phase 7) - depends on many other modules.

---

## What Should Remain in __init__.py

After extraction, `__init__.py` should contain only:

**Lines to keep**:
1. Module docstring - lines 13-28
2. Imports (clean up after extraction) - lines 30-61
3. Global configuration - lines 188-205 (`AGENT_CONFIG`, `_load_agent_config()`)
4. Constants - lines 207 (`SCRIPT_TYPE_CHOICES`)
5. App initialization - lines 325-343 (app creation, but BannerGroup moves to banner.py)
6. Callback - lines 361-367 (but show_banner moves to banner.py)
7. Check command - lines 1411-1457
8. Command registration - lines 1479-1581
9. Main entry point - lines 1584-1589

**Lines to remove**: All extracted functions/classes

**New imports in __init__.py**:
```python
import os
import json
import sys
from pathlib import Path

import typer
from rich.console import Console
from typer.core import TyperGroup
import ssl
import truststore

from .utils import check_tool
from .banner import show_banner, BannerGroup
from .scaffold import _ensure_nuaa_root
```

**Key configuration**:
- `AGENT_CONFIG` (lines 188-205)
- `SCRIPT_TYPE_CHOICES` (line 207)
- Global `console` object (line 325)
- SSL context (line 60)

---

## Dependency Graph

```
http_utils (→ consolidate with github_client.py)
    ↓ used by ↓
download.py
    ↓ used by ↓
init_cmd.py (commands/init.py)
    ↓ uses ↓
git_utils.py
scripts.py
ui.py
banner.py
scaffold.py (already extracted)
utils.py (already extracted)

Standalone modules:
- git_utils.py (only uses subprocess, Path, typer)
- scripts.py (only uses os, Path, utils.StepTracker)
- ui.py (only uses readchar, rich, typer)
- banner.py (only uses rich, typer)
```

---

## Extraction Order (Correct Dependency Order)

**CRITICAL**: Extract in this order to avoid circular imports:

1. **git_utils.py** (Phase 3) - no internal dependencies
2. **ui.py** (Phase 5) - no internal dependencies
3. **scripts.py** (Phase 4) - depends on utils.py (already exists)
4. **banner.py** (Phase 6) - no internal dependencies
5. **download.py** (Phase 2) - depends on github_client.py, utils.StepTracker
6. **commands/init.py** (Phase 7) - depends on everything above
7. **Consolidate HTTP utilities** (Phase 1) - refactor github_client.py
8. **Cleanup __init__.py** - remove extracted code, update imports

---

## File Size Impact Analysis

**Current __init__.py**: 1,590 lines (59.7 KB)

**After extraction**:
- `__init__.py`: ~250-300 lines (app setup, config, check command, registration)
- `git_utils.py`: ~80 lines
- `ui.py`: ~110 lines
- `scripts.py`: ~65 lines
- `banner.py`: ~80 lines
- `download.py`: ~380 lines
- `commands/init.py`: ~450 lines

**Total**: ~1,415 lines (distributed across files, easier to maintain)

---

## Testing Considerations

After extraction, test these in order:

1. Test each extracted module independently
2. Test imports don't have circular dependencies
3. Test init command still works completely
4. Test check command
5. Test banner display
6. Integration tests for full init workflow

---

## Summary Table

| Module | Lines | Functions | Dependencies | Priority |
|--------|-------|-----------|--------------|----------|
| git_utils.py | 80 | 3 | subprocess, typer | High |
| ui.py | 110 | 2 | readchar, rich, typer | High |
| scripts.py | 65 | 1 | os, utils.StepTracker | High |
| banner.py | 80 | 1 class + 1 func + 2 const | rich, typer | Medium |
| download.py | 380 | 5 | httpx, zipfile, utils, github_client | Critical |
| commands/init.py | 450 | 1 main + 1 register | All above | Final |
| github_client.py | Consolidate | Add helper functions | Existing module | Medium |
| __init__.py | 250-300 | Remaining CLI framework | All modules | Final |
