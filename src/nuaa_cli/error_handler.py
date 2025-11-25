"""
Centralized Error Handling Utilities
=====================================

This module provides centralized error handling and user-friendly error display
to reduce code duplication across commands and modules.

Functions:
    - print_error: Display consistent error messages
    - handle_network_error: Handle network/HTTP errors with cleanup
    - handle_file_error: Handle file operation errors
    - display_debug_environment: Show debug environment information
"""

from pathlib import Path
from typing import Optional, List, Tuple, TYPE_CHECKING
import shutil
import sys
import typer
from rich.console import Console
from rich.panel import Panel

if TYPE_CHECKING:
    from .utils import StepTracker


def print_error(
    console: Console,
    title: str,
    message: str,
    details: Optional[str] = None,
    use_panel: bool = True,
) -> None:
    """
    Display a consistent error message.

    Args:
        console: Rich console instance
        title: Error title
        message: Error message
        details: Optional detailed error information
        use_panel: Whether to use a Panel (True) or inline format (False)
    """
    if use_panel:
        panel_content = message
        if details:
            panel_content += f"\n\n[dim]{details}[/dim]"
        console.print(Panel(panel_content, title=f"[red]{title}[/red]", border_style="red"))
    else:
        console.print(f"[red]{title}:[/red] {message}")
        if details:
            console.print(f"[dim]{details}[/dim]")


def handle_network_error(
    error: Exception,
    action: str,
    console: Console,
    cleanup_path: Optional[Path] = None,
    tracker: Optional["StepTracker"] = None,
    debug: bool = False,
    exit_code: int = 1,
) -> None:
    """
    Handle network errors with consistent formatting and cleanup.

    Args:
        error: The exception that occurred
        action: Description of what action failed (e.g., "downloading template")
        console: Rich console instance
        cleanup_path: Optional path to clean up on error
        tracker: Optional StepTracker for progress tracking
        debug: Whether to show debug information
        exit_code: Exit code to use (default: 1)

    Raises:
        typer.Exit: Always exits with the specified code
    """
    import httpx
    from .logging_config import get_logger

    logger = get_logger(__name__)
    error_type = type(error).__name__

    # Log the error
    logger.error(f"Network error during {action}: {error}")

    # Update tracker if available
    if tracker:
        tracker.error("final", f"Network error: {error}")

    # Determine error message based on exception type
    if isinstance(error, httpx.TimeoutException):
        title = "Request Timeout"
        message = f"The request timed out while {action}."
        details = "Please check your internet connection and try again."
    elif isinstance(error, httpx.ConnectError):
        title = "Connection Error"
        message = f"Could not connect to the server while {action}."
        details = "Please check your internet connection and firewall settings."
    elif isinstance(error, httpx.HTTPError):
        title = "HTTP Error"
        message = f"An HTTP error occurred while {action}."
        details = str(error)
    else:
        title = f"{error_type}"
        message = f"An error occurred while {action}."
        details = str(error)

    # Display error
    print_error(console, title, message, details)

    # Show debug info if requested
    if debug:
        console.print("\n[dim]Debug Information:[/dim]")
        console.print(f"[dim]Error Type: {error_type}[/dim]")
        console.print(f"[dim]Error Details: {error}[/dim]")
        if hasattr(error, "__traceback__"):
            import traceback

            console.print("[dim]Traceback:[/dim]")
            console.print(f"[dim]{''.join(traceback.format_tb(error.__traceback__))}[/dim]")

    # Cleanup if path provided
    if cleanup_path and cleanup_path.exists():
        try:
            if cleanup_path.is_dir():
                shutil.rmtree(cleanup_path)
            else:
                cleanup_path.unlink()
            logger.debug(f"Cleaned up: {cleanup_path}")
        except Exception as cleanup_error:
            logger.warning(f"Failed to clean up {cleanup_path}: {cleanup_error}")

    raise typer.Exit(exit_code)


def handle_file_error(
    error: Exception,
    action: str,
    file_path: Path,
    console: Console,
    debug: bool = False,
    exit_code: int = 1,
) -> None:
    """
    Handle file operation errors with consistent formatting.

    Args:
        error: The exception that occurred
        action: Description of what action failed (e.g., "reading file")
        file_path: Path to the file that caused the error
        console: Rich console instance
        debug: Whether to show debug information
        exit_code: Exit code to use (default: 1)

    Raises:
        typer.Exit: Always exits with the specified code
    """
    from .logging_config import get_logger

    logger = get_logger(__name__)
    error_type = type(error).__name__

    logger.error(f"File error during {action}: {error}")

    # Determine error message based on exception type
    if isinstance(error, FileNotFoundError):
        title = "File Not Found"
        message = f"Could not find the required file while {action}."
        details = f"Path: {file_path}"
    elif isinstance(error, PermissionError):
        title = "Permission Denied"
        message = f"Permission denied while {action}."
        details = f"Path: {file_path}\nPlease check file permissions."
    elif isinstance(error, OSError):
        title = "File System Error"
        message = f"A file system error occurred while {action}."
        details = f"Path: {file_path}\n{str(error)}"
    else:
        title = f"{error_type}"
        message = f"An error occurred while {action}."
        details = f"Path: {file_path}\n{str(error)}"

    print_error(console, title, message, details)

    if debug:
        console.print("\n[dim]Debug Information:[/dim]")
        console.print(f"[dim]Error Type: {error_type}[/dim]")
        console.print(f"[dim]Error Details: {error}[/dim]")

    raise typer.Exit(exit_code)


def display_debug_environment(
    console: Console,
    extra_info: Optional[List[Tuple[str, str]]] = None,
) -> None:
    """
    Display debug environment information in a consistent format.

    Args:
        console: Rich console instance
        extra_info: Optional list of (label, value) tuples for additional debug info
    """
    env_pairs = [
        ("Python", sys.version.split()[0]),
        ("Platform", sys.platform),
        ("CWD", str(Path.cwd())),
    ]

    if extra_info:
        env_pairs.extend(extra_info)

    label_width = max(len(k) for k, _ in env_pairs)
    env_lines = [f"{k.ljust(label_width)} → [bright_black]{v}[/bright_black]" for k, v in env_pairs]

    console.print(
        Panel(
            "\n".join(env_lines),
            title="Debug Environment",
            border_style="magenta",
        )
    )
