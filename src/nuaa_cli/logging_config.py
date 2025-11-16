"""
Logging configuration for NUAA CLI.

This module provides structured logging capabilities for the CLI,
with support for different verbosity levels and file logging.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

# Default log format
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
VERBOSE_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"


def setup_logging(
    verbose: bool = False,
    debug: bool = False,
    log_file: Optional[Path] = None,
    quiet: bool = False,
) -> logging.Logger:
    """
    Configure structured logging for NUAA CLI.

    Args:
        verbose: Enable verbose output (INFO level)
        debug: Enable debug output (DEBUG level)
        log_file: Optional path to log file. If None, uses nuaa-cli.log in current directory
        quiet: Suppress console output (only log to file)

    Returns:
        Configured logger instance

    Example:
        >>> logger = setup_logging(verbose=True)
        >>> logger.info("Starting NUAA CLI")
    """
    # Determine log level
    if debug:
        level = logging.DEBUG
        log_format = VERBOSE_FORMAT
    elif verbose:
        level = logging.INFO
        log_format = DEFAULT_FORMAT
    else:
        level = logging.WARNING
        log_format = DEFAULT_FORMAT

    # Create logger
    logger = logging.getLogger("nuaa_cli")
    logger.setLevel(level)

    # Clear any existing handlers
    logger.handlers.clear()

    # Console handler (unless quiet mode)
    if not quiet:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_formatter = logging.Formatter(log_format)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    # File handler
    if log_file is None:
        log_file = Path.cwd() / "nuaa-cli.log"

    try:
        file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)  # Always log DEBUG to file
        file_formatter = logging.Formatter(VERBOSE_FORMAT)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except (OSError, PermissionError) as e:
        # If we can't create log file, continue without it
        if not quiet:
            print(f"Warning: Could not create log file {log_file}: {e}", file=sys.stderr)

    # Prevent propagation to root logger
    logger.propagate = False

    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance for a specific module.

    Args:
        name: Logger name (usually __name__ of the calling module)

    Returns:
        Logger instance

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.debug("Debug message")
    """
    if name is None:
        return logging.getLogger("nuaa_cli")
    return logging.getLogger(f"nuaa_cli.{name}")


def log_command_execution(command: str, args: dict) -> None:
    """
    Log command execution for audit trail.

    Args:
        command: Command name (e.g., 'design', 'propose')
        args: Command arguments as dictionary

    Example:
        >>> log_command_execution('design', {'program_name': 'Test Program'})
    """
    logger = get_logger("commands")
    logger.info(f"Executing command: {command}")
    logger.debug(f"Command arguments: {args}")


def log_api_call(url: str, method: str = "GET", status_code: Optional[int] = None) -> None:
    """
    Log API call for debugging and monitoring.

    Args:
        url: API endpoint URL
        method: HTTP method (GET, POST, etc.)
        status_code: Optional HTTP status code from response

    Example:
        >>> log_api_call('https://api.github.com/repos/...', 'GET', 200)
    """
    logger = get_logger("api")
    if status_code:
        logger.debug(f"{method} {url} - Status: {status_code}")
    else:
        logger.debug(f"{method} {url}")


def log_error(error: Exception, context: Optional[str] = None) -> None:
    """
    Log error with context for debugging.

    Args:
        error: Exception that occurred
        context: Optional context string describing what was happening

    Example:
        >>> try:
        ...     risky_operation()
        ... except Exception as e:
        ...     log_error(e, "Failed to download template")
    """
    logger = get_logger("errors")
    if context:
        logger.error(f"{context}: {error}", exc_info=True)
    else:
        logger.error(f"Error: {error}", exc_info=True)
