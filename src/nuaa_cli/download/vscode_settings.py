#!/usr/bin/env python3
"""
VSCode Settings.json Special Handling
======================================

This module provides special handling for VSCode settings.json files,
merging new settings with existing ones rather than overwriting.

Functions:
    - handle_vscode_settings: Smart merge for VSCode configs

Features:
    - Preserves user customizations
    - Adds new template settings
    - Graceful fallback to copy on errors
    - Comprehensive error handling

Author: NUAA Project
License: MIT
"""

import json
import shutil
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
    Handle merging or copying of .vscode/settings.json files.

    Special handling for VSCode settings to merge new settings with existing
    ones rather than overwriting. This preserves user customizations while
    adding new template settings.

    Args:
        sub_item: Source settings.json file path
        dest_file: Destination settings.json file path
        rel_path: Relative path for logging purposes
        verbose: Whether to print detailed progress messages
        tracker: Optional StepTracker for progress tracking
        console: Rich console for output (defaults to new Console instance)

    Raises:
        None: All exceptions are caught and handled gracefully with fallback to copy

    Examples:
        >>> from pathlib import Path
        >>> handle_vscode_settings(
        ...     Path('template/.vscode/settings.json'),
        ...     Path('project/.vscode/settings.json'),
        ...     Path('.vscode/settings.json'),
        ...     verbose=True
        ... )
    """

    def log(message: str, color: str = "green") -> None:
        if verbose and not tracker:
            console.print(f"[{color}]{message}[/] {rel_path}")

    try:
        with open(sub_item, "r", encoding="utf-8") as f:
            new_settings = json.load(f)

        if dest_file.exists():
            merged = merge_json_files(dest_file, new_settings, verbose=verbose and not tracker, console=console)
            with open(dest_file, "w", encoding="utf-8") as f:
                json.dump(merged, f, indent=4)
                f.write("\n")
            log("Merged:", "green")
        else:
            shutil.copy2(sub_item, dest_file)
            log("Copied (no existing settings.json):", "blue")

    except FileNotFoundError as e:
        log(f"Warning: Settings file not found, copying source instead: {e}", "yellow")
        shutil.copy2(sub_item, dest_file)
    except PermissionError as e:
        log(
            f"Warning: Permission denied accessing settings file, copying instead: {e}",
            "yellow",
        )
        shutil.copy2(sub_item, dest_file)
    except json.JSONDecodeError as e:
        log(f"Warning: Invalid JSON in settings file, copying source instead: {e}", "yellow")
        shutil.copy2(sub_item, dest_file)
    except OSError as e:
        log(f"Warning: File system error, copying instead: {e}", "yellow")
        shutil.copy2(sub_item, dest_file)
