"""
Script utilities for NUAA CLI.

This module provides utilities for managing script files in NUAA projects,
including setting executable permissions on shell scripts.
"""

import os
from pathlib import Path

from rich.console import Console

from .utils import StepTracker


def ensure_executable_scripts(
    project_path: Path, tracker: StepTracker | None = None, console: Console | None = None
) -> None:
    """
    Ensure POSIX .sh scripts under agent script folders have execute bits.

    On Windows, this function does nothing (no-op). On POSIX systems (Linux, macOS),
    it recursively finds all .sh scripts with shebang (#!) lines and sets execute
    permissions appropriately based on read permissions.

    Args:
        project_path: Path to the project root directory
        tracker: Optional StepTracker for progress tracking
        console: Optional Rich console for output

    Permissions logic:
        - If user can read (0o400), add user execute (0o100)
        - If group can read (0o040), add group execute (0o010)
        - If other can read (0o004), add other execute (0o001)
        - Always ensures at least user execute (0o100) is set

    Example:
        >>> ensure_executable_scripts(Path("my-project"))
        Updated execute permissions on 5 script(s) recursively

    Note:
        - Only processes files with .sh extension
        - Only processes files starting with shebang (#!)
        - Skips symlinks
        - Silently skips if .agents/scripts directory doesn't exist
    """
    if os.name == "nt":
        return  # Windows: skip silently

    _console = console or Console()

    # Default to a common scripts folder if present; skip quietly if not
    scripts_root = project_path / ".agents" / "scripts"
    if not scripts_root.is_dir():
        return

    failures: list[str] = []
    updated = 0

    for script in scripts_root.rglob("*.sh"):
        try:
            # Skip symlinks and non-files
            if script.is_symlink() or not script.is_file():
                continue

            # Only process files with shebang
            try:
                with script.open("rb") as f:
                    if f.read(2) != b"#!":
                        continue
            except (OSError, PermissionError):
                continue

            # Check current permissions
            st = script.stat()
            mode = st.st_mode

            # Skip if already executable
            if mode & 0o111:
                continue

            # Calculate new mode based on read permissions
            new_mode = mode
            if mode & 0o400:  # User read
                new_mode |= 0o100  # Add user execute
            if mode & 0o040:  # Group read
                new_mode |= 0o010  # Add group execute
            if mode & 0o004:  # Other read
                new_mode |= 0o001  # Add other execute

            # Ensure at least user execute is set
            if not (new_mode & 0o100):
                new_mode |= 0o100

            # Apply new permissions
            os.chmod(script, new_mode)
            updated += 1

        except (OSError, PermissionError) as e:
            failures.append(f"{script.relative_to(scripts_root)}: {e}")

    # Report results
    if tracker:
        detail = f"{updated} updated" + (f", {len(failures)} failed" if failures else "")
        tracker.add("chmod", "Set script permissions recursively")
        (tracker.error if failures else tracker.complete)("chmod", detail)
    else:
        if updated:
            _console.print(
                f"[cyan]Updated execute permissions on {updated} script(s) recursively[/cyan]"
            )
        if failures:
            _console.print("[yellow]Some scripts could not be updated:[/yellow]")
            for failure in failures:
                _console.print(f"  - {failure}")
