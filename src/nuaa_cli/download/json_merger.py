#!/usr/bin/env python3
"""
JSON Configuration File Merging Utilities
==========================================

This module provides utilities for deep merging JSON configuration files,
preserving existing values while adding new ones.

Functions:
    - merge_json_files: Deep merge two JSON files
    - _deep_merge: Internal recursive merge function

Merge Behavior:
    - New keys are added
    - Existing keys are preserved unless overwritten by new content
    - Nested dictionaries are merged recursively
    - Lists and other values are replaced (not merged)

Author: NUAA Project
License: MIT
"""

import json
from pathlib import Path

from rich.console import Console


def merge_json_files(
    existing_path: Path,
    new_content: dict,
    verbose: bool = False,
    console: Console = Console(),
) -> dict:
    """
    Merge new JSON content into existing JSON file.

    Performs a deep merge where:
    - New keys are added
    - Existing keys are preserved unless overwritten by new content
    - Nested dictionaries are merged recursively
    - Lists and other values are replaced (not merged)

    Args:
        existing_path: Path to existing JSON file
        new_content: New JSON content to merge in
        verbose: Whether to print merge details
        console: Rich console for output (defaults to new Console instance)

    Returns:
        Merged JSON content as dict

    Examples:
        >>> from pathlib import Path
        >>> existing = Path('config.json')
        >>> new_data = {'new_key': 'value', 'nested': {'key': 'value'}}
        >>> merged = merge_json_files(existing, new_data)
        >>> 'new_key' in merged
        True

        >>> # Deep merge example
        >>> existing_content = {'a': 1, 'b': {'c': 2}}
        >>> new_content = {'b': {'d': 3}, 'e': 4}
        >>> # Result: {'a': 1, 'b': {'c': 2, 'd': 3}, 'e': 4}
    """
    try:
        with open(existing_path, "r", encoding="utf-8") as f:
            existing_content = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is invalid, just use new content
        return new_content

    def _deep_merge(base: dict, update: dict) -> dict:
        """Recursively merge update dict into base dict."""
        result = base.copy()
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                # Recursively merge nested dictionaries
                result[key] = _deep_merge(result[key], value)
            else:
                # Add new key or replace existing value
                result[key] = value
        return result

    merged = _deep_merge(existing_content, new_content)

    if verbose:
        console.print(f"[cyan]Merged JSON file:[/cyan] {existing_path.name}")

    return merged
