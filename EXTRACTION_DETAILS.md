# Detailed Extraction Specifications with Line Numbers and Code Snippets

## Module 1: git_utils.py (Extract FIRST)

**File location**: `/home/user/nuaa-cli/src/nuaa_cli/git_utils.py` (NEW)

**Exact lines to extract from __init__.py**: 
- Lines 370-415 (run_command + is_git_repo)
- Lines 417-455 (init_git_repo)

### Complete Code to Copy:

```python
# run_command (lines 370-393)
def run_command(
    cmd: list[str],
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
) -> Optional[str]:
    """Run a shell command and optionally capture output."""
    try:
        if capture:
            result = subprocess.run(
                cmd, check=check_return, capture_output=True, text=True, shell=shell  # nosec B602
            )
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=check_return, shell=shell)  # nosec B602
            return None
    except subprocess.CalledProcessError as e:
        if check_return:
            console.print(f"[red]Error running command:[/red] {' '.join(cmd)}")
            console.print(f"[red]Exit code:[/red] {e.returncode}")
            if hasattr(e, "stderr") and e.stderr:
                console.print(f"[red]Error output:[/red] {e.stderr}")
            raise
        return None

# is_git_repo (lines 396-414)
def is_git_repo(path: Path | None = None) -> bool:
    """Check if the specified path is inside a git repository."""
    if path is None:
        path = Path.cwd()

    if not path.is_dir():
        return False

    try:
        # Use git command to check if inside a work tree
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,
            cwd=path,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

# init_git_repo (lines 417-455)
def init_git_repo(project_path: Path, quiet: bool = False) -> Tuple[bool, Optional[str]]:
    """Initialize a git repository in the specified path.

    Args:
        project_path: Path to initialize git repository in
        quiet: if True suppress console output (tracker handles status)

    Returns:
        Tuple of (success: bool, error_message: Optional[str])
    """
    original_cwd = Path.cwd()
    try:
        os.chdir(project_path)
        if not quiet:
            console.print("[cyan]Initializing git repository...[/cyan]")
        subprocess.run(["git", "init"], check=True, capture_output=True, text=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from NUAA template"],
            check=True,
            capture_output=True,
            text=True,
        )
        if not quiet:
            console.print("[green]✓[/green] Git repository initialized")
        return True, None

    except subprocess.CalledProcessError as e:
        error_msg = f"Command: {' '.join(e.cmd)}\nExit code: {e.returncode}"
        if e.stderr:
            error_msg += f"\nError: {e.stderr.strip()}"
        elif e.stdout:
            error_msg += f"\nOutput: {e.stdout.strip()}"

        if not quiet:
            console.print(f"[red]Error initializing git repository:[/red] {e}")
        return False, error_msg
    finally:
        os.chdir(original_cwd)
```

**Imports to add at top of git_utils.py**:
```python
import os
import subprocess
from pathlib import Path
from typing import Optional, Tuple

import typer
from rich.console import Console
```

**After extraction, update in __init__.py**:
- Remove lines 370-455
- Add import: `from .git_utils import run_command, is_git_repo, init_git_repo`
- NOTE: `run_command` is only used internally in git operations, consider making it private or internal only

---

## Module 2: ui.py (Extract SECOND)

**File location**: `/home/user/nuaa-cli/src/nuaa_cli/ui.py` (NEW)

**Exact lines to extract from __init__.py**: 
- Lines 221-239 (get_key)
- Lines 242-323 (select_with_arrows)

### Complete Code to Copy:

```python
# get_key (lines 221-239)
def get_key():
    """Get a single keypress in a cross-platform way using readchar."""
    key = readchar.readkey()

    if key == readchar.key.UP or key == readchar.key.CTRL_P:
        return "up"
    if key == readchar.key.DOWN or key == readchar.key.CTRL_N:
        return "down"

    if key == readchar.key.ENTER:
        return "enter"

    if key == readchar.key.ESC:
        return "escape"

    if key == readchar.key.CTRL_C:
        raise KeyboardInterrupt

    return key

# select_with_arrows (lines 242-323)
def select_with_arrows(
    options: dict, prompt_text: str = "Select an option", default_key: str | None = None
) -> str:
    """
    Interactive selection using arrow keys with Rich Live display.

    Args:
        options: Dict with keys as option keys and values as descriptions
        prompt_text: Text to show above the options
        default_key: Default option key to start with

    Returns:
        Selected option key
    """
    option_keys = list(options.keys())
    if default_key and default_key in option_keys:
        selected_index = option_keys.index(default_key)
    else:
        selected_index = 0

    selected_key = None

    def create_selection_panel():
        """Create the selection panel with current selection highlighted."""
        table = Table.grid(padding=(0, 2))
        table.add_column(style="cyan", justify="left", width=3)
        table.add_column(style="white", justify="left")

        for i, key in enumerate(option_keys):
            if i == selected_index:
                table.add_row("▶", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")
            else:
                table.add_row(" ", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")

        table.add_row("", "")
        table.add_row("", "[dim]Use ↑/↓ to navigate, Enter to select, Esc to cancel[/dim]")

        return Panel(
            table,
            title=f"[bold]{prompt_text}[/bold]",
            border_style="cyan",
            padding=(1, 2),
        )

    console.print()

    def run_selection_loop():
        nonlocal selected_key, selected_index
        with Live(
            create_selection_panel(),
            console=console,
            transient=True,
            auto_refresh=False,
        ) as live:
            while True:
                try:
                    key = get_key()
                    if key == "up":
                        selected_index = (selected_index - 1) % len(option_keys)
                    elif key == "down":
                        selected_index = (selected_index + 1) % len(option_keys)
                    elif key == "enter":
                        selected_key = option_keys[selected_index]
                        break
                    elif key == "escape":
                        console.print("\n[yellow]Selection cancelled[/yellow]")
                        raise typer.Exit(1)

                    live.update(create_selection_panel(), refresh=True)

                except KeyboardInterrupt:
                    console.print("\n[yellow]Selection cancelled[/yellow]")
                    raise typer.Exit(1)

    run_selection_loop()

    if selected_key is None:
        console.print("\n[red]Selection failed.[/red]")
        raise typer.Exit(1)

    return selected_key
```

**Imports to add at top of ui.py**:
```python
import readchar
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live

# Global console object (must be provided or created)
console = Console()
```

**After extraction, update in __init__.py**:
- Remove lines 221-323
- Add import: `from .ui import get_key, select_with_arrows`

---

## Module 3: scripts.py (Extract THIRD)

**File location**: `/home/user/nuaa-cli/src/nuaa_cli/scripts.py` (NEW)

**Exact lines to extract from __init__.py**: 
- Lines 924-973 (ensure_executable_scripts)

### Complete Code to Copy:

```python
# ensure_executable_scripts (lines 924-973)
def ensure_executable_scripts(project_path: Path, tracker: StepTracker | None = None) -> None:
    """Ensure POSIX .sh scripts under agent script folders have execute bits (no-op on Windows)."""
    if os.name == "nt":
        return  # Windows: skip silently
    # Default to a common scripts folder if present; skip quietly if not
    scripts_root = project_path / ".agents" / "scripts"
    if not scripts_root.is_dir():
        return
    failures: list[str] = []
    updated = 0
    for script in scripts_root.rglob("*.sh"):
        try:
            if script.is_symlink() or not script.is_file():
                continue
            try:
                with script.open("rb") as f:
                    if f.read(2) != b"#!":
                        continue
            except (OSError, PermissionError):
                continue
            st = script.stat()
            mode = st.st_mode
            if mode & 0o111:
                continue
            new_mode = mode
            if mode & 0o400:
                new_mode |= 0o100
            if mode & 0o040:
                new_mode |= 0o010
            if mode & 0o004:
                new_mode |= 0o001
            if not (new_mode & 0o100):
                new_mode |= 0o100
            os.chmod(script, new_mode)
            updated += 1
        except (OSError, PermissionError) as e:
            failures.append(f"{script.relative_to(scripts_root)}: {e}")
    if tracker:
        detail = f"{updated} updated" + (f", {len(failures)} failed" if failures else "")
        tracker.add("chmod", "Set script permissions recursively")
        (tracker.error if failures else tracker.complete)("chmod", detail)
    else:
        if updated:
            console.print(
                f"[cyan]Updated execute permissions on {updated} script(s) recursively[/cyan]"
            )
        if failures:
            console.print("[yellow]Some scripts could not be updated:[/yellow]")
            for failure in failures:
                console.print(f"  - {failure}")
```

**Imports to add at top of scripts.py**:
```python
import os
from pathlib import Path
from rich.console import Console
from .utils import StepTracker

# Global console object
console = Console()
```

**After extraction, update in __init__.py**:
- Remove lines 924-973
- Add import: `from .scripts import ensure_executable_scripts`

---

## Module 4: banner.py (Extract FOURTH)

**File location**: `/home/user/nuaa-cli/src/nuaa_cli/banner.py` (NEW)

**Exact lines to extract from __init__.py**: 
- Lines 209-216 (BANNER constant)
- Line 218 (TAGLINE constant)
- Lines 328-334 (BannerGroup class)
- Lines 346-358 (show_banner function)

### Complete Code to Copy:

```python
from rich.console import Console
from rich.text import Text
from rich.align import Align
from typer.core import TyperGroup

# Global console object
console = Console()

# Constants
BANNER = """
███╗   ██╗██╗   ██╗ █████╗  █████╗
████╗  ██║██║   ██║██╔══██╗██╔══██╗
██╔██╗ ██║██║   ██║███████║███████║
██║╚██╗██║██║   ██║██╔══██║██╔══██║
██║ ╚████║╚██████╔╝██║  ██║██║  ██║
╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
"""

TAGLINE = "NUAA Project - AI-Assisted Project Management for NSW Users and AIDS Association"

# Custom Typer group for banner display
class BannerGroup(TyperGroup):
    """Custom group that shows banner before help."""

    def format_help(self, ctx, formatter):
        # Show banner before help
        show_banner()
        super().format_help(ctx, formatter)

# Banner display function
def show_banner():
    """Display the ASCII art banner."""
    banner_lines = BANNER.strip().split("\n")
    colors = ["bright_blue", "blue", "cyan", "bright_cyan", "white", "bright_white"]

    styled_banner = Text()
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        styled_banner.append(line + "\n", style=color)

    console.print(Align.center(styled_banner))
    console.print(Align.center(Text(TAGLINE, style="italic bright_yellow")))
    console.print()
```

**After extraction, update in __init__.py**:
- Remove lines 209-218, 328-334, 346-358
- Add import: `from .banner import BANNER, TAGLINE, BannerGroup, show_banner`

---

## Module 5: download.py (Extract FIFTH)

**File location**: `/home/user/nuaa-cli/src/nuaa_cli/download.py` (NEW)

**Exact lines to extract from __init__.py**: 
- Lines 138-171 (_safe_extract_zip)
- Lines 458-490 (handle_vscode_settings)
- Lines 493-534 (merge_json_files)
- Lines 537-722 (download_template_from_github)
- Lines 724-921 (download_and_extract_template)

**These functions should be extracted in order**. The complete file needs:

**Imports at top**:
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
# Note: Will need console passed as parameter or globally

# Global console object
console = Console()
```

**Complete functions** (see __init__.py lines 138-171, 458-490, 493-534, 537-722, 724-921):
- Copy all 5 functions as-is from __init__.py

**After extraction, update in __init__.py**:
- Remove lines 138-171, 458-490, 493-534, 537-722, 724-921
- Add import: `from .download import download_and_extract_template, handle_vscode_settings, download_template_from_github`

---

## Module 6: commands/init.py (Extract LAST)

**File location**: `/home/user/nuaa-cli/src/nuaa_cli/commands/init.py` (NEW - or move existing)

**Exact lines to extract from __init__.py**: 
- Lines 976-1408 (entire init command)

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
import httpx
import ssl
import truststore

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

# Global console
console = Console()

# Will need these from parent:
# AGENT_CONFIG (from __init__.py lines 205)
# SCRIPT_TYPE_CHOICES (from __init__.py line 207)
# ssl_context (from __init__.py line 60)
```

**Register function signature**:
```python
def register(app: typer.Typer, agent_config: dict, script_type_choices: dict, 
             ssl_context, console: Console) -> None:
    """Register the init command with the Typer app."""
    
    @app.command()
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
    ):
        """[Full docstring from lines 1018-1041]"""
        # [Copy entire function body from lines 1043-1408]
```

**After extraction, update in __init__.py**:
- Remove lines 976-1408
- In command registration section (lines 1479-1581), replace the old init registration with:
  ```python
  try:
      from .commands.init import register as _register_init
      _register_init(app, AGENT_CONFIG, SCRIPT_TYPE_CHOICES, ssl_context, console)
  except Exception:
      # Safe fallback
      pass
  ```

---

## Files Summary - What to Extract and In What Order

| Step | File | Lines | Action | Dependencies |
|------|------|-------|--------|--------------|
| 1 | git_utils.py | 370-455 | NEW FILE - Create | None |
| 2 | ui.py | 221-323 | NEW FILE - Create | readchar, rich |
| 3 | scripts.py | 924-973 | NEW FILE - Create | utils.StepTracker |
| 4 | banner.py | 209-218, 328-334, 346-358 | NEW FILE - Create | rich, typer |
| 5 | download.py | 138-171, 458-534, 537-921 | NEW FILE - Create | httpx, github_client |
| 6 | commands/init.py | 976-1408 | NEW FILE - Create | All above + scaffold |
| 7 | __init__.py | All extracted lines | DELETE + Update | Clean up imports |

---

## Critical Notes on Passing console and Configuration

Several extracted modules need access to:
1. **console** global object - Either:
   - Pass as parameter to functions
   - Create locally in each module
   - Import from shared location

2. **AGENT_CONFIG** - Only needed by init.py, pass as parameter

3. **SCRIPT_TYPE_CHOICES** - Only needed by init.py, pass as parameter

4. **ssl_context** - Only needed by init.py (via download.py), pass as parameter

**Recommended approach**: 
- Each module creates its own `console = Console()`
- Modules like `download_and_extract_template` accept `console` as optional parameter
- init.py receives these configuration objects and passes them where needed

