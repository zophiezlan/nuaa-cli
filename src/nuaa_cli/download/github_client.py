#!/usr/bin/env python3
"""
GitHub API Client Utilities
============================

This module provides utilities for interacting with GitHub's API, including:

- Token resolution from environment variables and CLI arguments
- Authorization header generation
- Rate limit header parsing and error formatting
- User-friendly error messages for rate limiting issues

Functions:
    - get_github_token: Get GitHub token from CLI, GH_TOKEN, or GITHUB_TOKEN
    - get_auth_headers: Generate authorization headers for GitHub API
    - parse_rate_limit_headers: Extract rate limit information from response headers
    - format_rate_limit_error: Format user-friendly rate limit error messages

Security Features:
    - Token sanitization and validation
    - Comprehensive rate limit information for troubleshooting
    - Clear guidance for resolving authentication issues

Author: NUAA Project
License: MIT
"""

import os
from datetime import datetime, timezone
from typing import Optional

import httpx


def get_github_token(cli_token: Optional[str] = None) -> Optional[str]:
    """
    Return sanitized GitHub token or None.

    Priority order:
    1. CLI argument token
    2. GH_TOKEN environment variable
    3. GITHUB_TOKEN environment variable

    Args:
        cli_token: Token passed via CLI argument

    Returns:
        Sanitized token string or None if no token available

    Examples:
        >>> token = get_github_token("ghp_abc123")
        >>> token
        'ghp_abc123'

        >>> os.environ["GH_TOKEN"] = "ghp_xyz789"
        >>> token = get_github_token()
        >>> token
        'ghp_xyz789'
    """
    return ((cli_token or os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN") or "").strip()) or None


def get_auth_headers(cli_token: Optional[str] = None) -> dict:
    """
    Return Authorization header dict only when a non-empty token exists.

    Args:
        cli_token: Token passed via CLI argument

    Returns:
        Dictionary with Authorization header if token exists, empty dict otherwise

    Examples:
        >>> headers = get_auth_headers("ghp_abc123")
        >>> headers
        {'Authorization': 'Bearer ghp_abc123'}

        >>> headers = get_auth_headers(None)
        >>> headers
        {}
    """
    token = get_github_token(cli_token)
    return {"Authorization": f"Bearer {token}"} if token else {}


def parse_rate_limit_headers(headers: httpx.Headers) -> dict:
    """
    Extract and parse GitHub rate-limit headers.

    Parses standard GitHub API rate limit headers and retry-after headers
    to provide useful information about API quota status.

    Args:
        headers: Response headers from GitHub API request

    Returns:
        Dictionary containing parsed rate limit information with keys:
        - limit: Total requests allowed per hour
        - remaining: Requests remaining in current window
        - reset_epoch: Unix timestamp when limit resets
        - reset_time: DateTime object for reset time (UTC)
        - reset_local: DateTime object for reset time (local timezone)
        - retry_after_seconds: Seconds to wait before retrying (if applicable)

    Examples:
        >>> headers = httpx.Headers({
        ...     'X-RateLimit-Limit': '5000',
        ...     'X-RateLimit-Remaining': '4999',
        ...     'X-RateLimit-Reset': '1234567890'
        ... })
        >>> info = parse_rate_limit_headers(headers)
        >>> info['limit']
        '5000'
    """
    info = {}

    # Standard GitHub rate-limit headers
    if "X-RateLimit-Limit" in headers:
        info["limit"] = headers.get("X-RateLimit-Limit")
    if "X-RateLimit-Remaining" in headers:
        info["remaining"] = headers.get("X-RateLimit-Remaining")
    if "X-RateLimit-Reset" in headers:
        reset_epoch = int(headers.get("X-RateLimit-Reset", "0"))
        if reset_epoch:
            reset_time = datetime.fromtimestamp(reset_epoch, tz=timezone.utc)
            info["reset_epoch"] = reset_epoch
            info["reset_time"] = reset_time
            info["reset_local"] = reset_time.astimezone()

    # Retry-After header (seconds or HTTP-date)
    if "Retry-After" in headers:
        retry_after = headers.get("Retry-After")
        try:
            info["retry_after_seconds"] = int(retry_after)
        except ValueError:
            # HTTP-date format - not implemented, just store as string
            info["retry_after"] = retry_after

    return info


def format_rate_limit_error(status_code: int, headers: httpx.Headers, url: str) -> str:
    """
    Format a user-friendly error message with rate-limit information.

    Creates a comprehensive error message including rate limit details and
    troubleshooting guidance for GitHub API rate limiting issues.

    Args:
        status_code: HTTP status code from failed request
        headers: Response headers containing rate limit information
        url: URL that was requested

    Returns:
        Formatted multi-line error message string with troubleshooting tips

    Examples:
        >>> headers = httpx.Headers({'X-RateLimit-Remaining': '0'})
        >>> error = format_rate_limit_error(403, headers, 'https://api.github.com/repos/foo/bar')
        >>> 'Rate Limit Information' in error
        True
    """
    rate_info = parse_rate_limit_headers(headers)

    lines = [f"GitHub API returned status {status_code} for {url}"]
    lines.append("")

    if rate_info:
        lines.append("[bold]Rate Limit Information:[/bold]")
        if "limit" in rate_info:
            lines.append(f"  • Rate Limit: {rate_info['limit']} requests/hour")
        if "remaining" in rate_info:
            lines.append(f"  • Remaining: {rate_info['remaining']}")
        if "reset_local" in rate_info:
            reset_str = rate_info["reset_local"].strftime("%Y-%m-%d %H:%M:%S %Z")
            lines.append(f"  • Resets at: {reset_str}")
        if "retry_after_seconds" in rate_info:
            lines.append(f"  • Retry after: {rate_info['retry_after_seconds']} seconds")
        lines.append("")

    # Add troubleshooting guidance
    lines.append("[bold]Troubleshooting Tips:[/bold]")
    lines.append("  • If you're on a shared CI or corporate environment, you may be rate-limited.")
    lines.append(
        "  • Consider using a GitHub token via --github-token or the GH_TOKEN/GITHUB_TOKEN"
    )
    lines.append("    environment variable to increase rate limits.")
    lines.append(
        "  • Authenticated requests have a limit of 5,000/hour vs 60/hour for unauthenticated."
    )

    return "\n".join(lines)
