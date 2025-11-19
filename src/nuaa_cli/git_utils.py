"""
Git repository utilities for NUAA CLI.

This module provides helper functions for git operations including
repository initialization, checking git status, and running git commands.
"""

import os
import subprocess
from pathlib import Path
from typing import Optional, Tuple

from rich.console import Console


def run_command(
    cmd: list[str],
    check_return: bool = True,
    capture: bool = False,
    shell: bool = False,
    console: Console | None = None,
) -> Optional[str]:
    """
    Run a shell command and optionally capture output.

    Args:
        cmd: Command and arguments as a list
        check_return: Whether to check return code and raise on failure
        capture: Whether to capture and return stdout
        shell: Whether to run as shell command (use with caution)
        console: Optional Rich console for error output

    Returns:
        Captured stdout if capture=True, otherwise None

    Raises:
        subprocess.CalledProcessError: If command fails and check_return=True

    Example:
        >>> run_command(["git", "init"])
        >>> output = run_command(["git", "status"], capture=True)
    """
    _console = console or Console()

    try:
        if capture:
            result = subprocess.run(
                cmd, check=check_return, capture_output=True, text=True, shell=shell
            )  # nosec B602
            return result.stdout.strip()
        else:
            subprocess.run(cmd, check=check_return, shell=shell)  # nosec B602
            return None
    except subprocess.CalledProcessError as e:
        if check_return:
            _console.print(f"[red]Error running command:[/red] {' '.join(cmd)}")
            _console.print(f"[red]Exit code:[/red] {e.returncode}")
            if hasattr(e, "stderr") and e.stderr:
                _console.print(f"[red]Error output:[/red] {e.stderr}")
            raise
        return None


def is_git_repo(path: Path | None = None) -> bool:
    """
    Check if the specified path is inside a git repository.

    Args:
        path: Path to check (defaults to current working directory)

    Returns:
        True if path is inside a git repository, False otherwise

    Example:
        >>> if is_git_repo():
        ...     print("Already in a git repo")
    """
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


def init_git_repo(
    project_path: Path, quiet: bool = False, console: Console | None = None
) -> Tuple[bool, Optional[str]]:
    """
    Initialize a git repository in the specified path.

    Creates an initial commit with all files in the directory.

    Args:
        project_path: Path to initialize git repository in
        quiet: If True, suppress console output (for use with tracker)
        console: Optional Rich console for output

    Returns:
        Tuple of (success: bool, error_message: Optional[str])
        - success: True if repository initialized successfully
        - error_message: Error details if failed, None if successful

    Example:
        >>> success, error = init_git_repo(Path("my-project"))
        >>> if success:
        ...     print("Git repo created!")
    """
    _console = console or Console()
    original_cwd = Path.cwd()

    try:
        os.chdir(project_path)
        if not quiet:
            _console.print("[cyan]Initializing git repository...[/cyan]")

        subprocess.run(["git", "init"], check=True, capture_output=True, text=True)
        subprocess.run(["git", "add", "."], check=True, capture_output=True, text=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from NUAA template"],
            check=True,
            capture_output=True,
            text=True,
        )

        if not quiet:
            _console.print("[green]✓[/green] Git repository initialized")
        return True, None

    except subprocess.CalledProcessError as e:
        error_msg = f"Command: {' '.join(e.cmd)}\nExit code: {e.returncode}"
        if e.stderr:
            error_msg += f"\nError: {e.stderr.strip()}"
        elif e.stdout:
            error_msg += f"\nOutput: {e.stdout.strip()}"

        if not quiet:
            _console.print(f"[red]Error initializing git repository:[/red] {e}")
        return False, error_msg
    finally:
        os.chdir(original_cwd)
