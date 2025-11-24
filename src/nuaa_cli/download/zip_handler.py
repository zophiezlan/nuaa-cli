#!/usr/bin/env python3
"""
Secure ZIP File Extraction Utilities
=====================================

This module provides secure ZIP file extraction with protection against
path traversal attacks and other malicious archive content.

Functions:
    - safe_extract_zip: Safely extract ZIP file contents with security validation

Security Features:
    - Path traversal attack prevention
    - Validates all paths before extraction
    - Aborts on detection of malicious paths
    - Clear error messages for security issues

Author: NUAA Project
License: MIT
"""

import zipfile
from pathlib import Path

import typer
from rich.console import Console


def safe_extract_zip(zip_ref: zipfile.ZipFile, extract_path: Path, console: Console = Console()) -> None:
    """
    Safely extract ZIP file contents, preventing path traversal attacks.

    Validates all paths in the ZIP archive before extraction to ensure no
    malicious paths attempt to write outside the target directory. This prevents
    security vulnerabilities from specially crafted ZIP files.

    Args:
        zip_ref: Open ZipFile object to extract
        extract_path: Target directory for extraction
        console: Rich console for error output (defaults to new Console instance)

    Raises:
        ValueError: If ZIP contains malicious paths attempting traversal
        typer.Exit: If validation fails (exits with code 1)

    Examples:
        >>> import zipfile
        >>> from pathlib import Path
        >>> # Safe extraction
        >>> with zipfile.ZipFile('template.zip', 'r') as zf:
        ...     safe_extract_zip(zf, Path('/tmp/safe_dir'))

        >>> # Malicious ZIP with path traversal attempt would raise ValueError
    """
    extract_path = extract_path.resolve()

    for member in zip_ref.namelist():
        # Get the target path
        member_path = (extract_path / member).resolve()

        # Ensure the resolved path is within the intended extract directory
        try:
            member_path.relative_to(extract_path)
        except ValueError:
            # Path traversal detected
            console.print(f"[red]Security Error:[/red] ZIP file contains invalid path: {member}")
            console.print("[dim]This file may be malicious. Extraction aborted.[/dim]")
            raise typer.Exit(1)

    # All paths validated, safe to extract
    zip_ref.extractall(extract_path)
