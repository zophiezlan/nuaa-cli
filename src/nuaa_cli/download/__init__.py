#!/usr/bin/env python3
"""
NUAA CLI Download Module
========================

Provides functionality for downloading and extracting NUAA project templates
from GitHub releases with secure handling and smart configuration merging.

This module has been refactored into focused submodules:
- github_client: GitHub API authentication and rate limiting
- zip_handler: Secure ZIP file extraction
- json_merger: Deep JSON configuration merging
- vscode_settings: VSCode settings.json special handling
- template_downloader: Main download orchestration

Public API:
    - download_template_from_github: Fetch template from GitHub
    - download_and_extract_template: Complete workflow
    - merge_json_files: Deep merge JSON configs
    - handle_vscode_settings: Smart VSCode settings merge

Author: NUAA Project
License: MIT
"""

# Re-export public API for backward compatibility
from .template_downloader import (
    download_template_from_github,
    download_and_extract_template,
)
from .json_merger import merge_json_files
from .vscode_settings import handle_vscode_settings

__all__ = [
    "download_template_from_github",
    "download_and_extract_template",
    "merge_json_files",
    "handle_vscode_settings",
]
