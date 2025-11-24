"""
GitHub API client for NUAA CLI.

This module provides a clean interface for interacting with the GitHub API,
including release downloads, rate limit handling, and authentication.
"""

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import httpx
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .logging_config import get_logger, log_api_call, log_error

logger = get_logger(__name__)
console = Console()


# Module-level utility functions for token and header management
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
    """
    return ((cli_token or os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN") or "").strip()) or None


def get_auth_headers(cli_token: Optional[str] = None) -> dict:
    """
    Return Authorization header dict only when a non-empty token exists.

    Args:
        cli_token: Token passed via CLI argument

    Returns:
        Dictionary with Authorization header if token exists, empty dict otherwise
    """
    token = get_github_token(cli_token)
    return {"Authorization": f"Bearer {token}"} if token else {}


def parse_rate_limit_headers(headers: httpx.Headers) -> dict:
    """
    Extract and parse GitHub rate-limit headers.

    Args:
        headers: Response headers from GitHub API request

    Returns:
        Dictionary containing parsed rate limit information
    """
    info = {}

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

    if "Retry-After" in headers:
        retry_after = headers.get("Retry-After")
        try:
            info["retry_after_seconds"] = int(retry_after)
        except ValueError:
            info["retry_after"] = retry_after

    return info


def format_rate_limit_error(status_code: int, headers: httpx.Headers, url: str) -> str:
    """
    Format a user-friendly error message with rate-limit information.

    Args:
        status_code: HTTP status code from failed request
        headers: Response headers containing rate limit information
        url: URL that was requested

    Returns:
        Formatted multi-line error message string with troubleshooting tips
    """
    rate_info = parse_rate_limit_headers(headers)

    lines = [f"GitHub API returned status {status_code} for {url}", ""]

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

    lines.append("[bold]Troubleshooting Tips:[/bold]")
    lines.append("  • Consider using a GitHub token to increase rate limits")
    lines.append("  • Set GH_TOKEN or GITHUB_TOKEN environment variable")
    lines.append("  • Authenticated requests have 5,000/hour limit vs 60/hour unauthenticated")

    return "\n".join(lines)


class GitHubRateLimitError(Exception):
    """Raised when GitHub API rate limit is exceeded."""

    pass


class GitHubClient:
    """Client for interacting with GitHub API."""

    def __init__(
        self,
        token: Optional[str] = None,
        ssl_context=None,
        debug: bool = False,
    ):
        """
        Initialize GitHub API client.

        Args:
            token: GitHub authentication token (or None for unauthenticated)
            ssl_context: SSL context for HTTPS requests
            debug: Enable debug output
        """
        self.token = token or get_github_token()
        self.ssl_context = ssl_context
        self.debug = debug
        self.base_url = "https://api.github.com"

    def _get_headers(self) -> dict:
        """Get request headers including authentication if available."""
        headers = {"Accept": "application/vnd.github+json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def get_latest_release(self, owner: str, repo: str) -> dict:
        """
        Get latest release information from GitHub repository.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            Release data dictionary

        Raises:
            GitHubRateLimitError: If rate limit exceeded
            RuntimeError: For other API errors
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/releases/latest"
        logger.info(f"Fetching latest release from {owner}/{repo}")

        with httpx.Client(verify=self.ssl_context) as client:
            try:
                response = client.get(url, headers=self._get_headers(), timeout=30, follow_redirects=True)
                log_api_call(url, "GET", response.status_code)

                if response.status_code == 403:
                    error_msg = format_rate_limit_error(response.status_code, response.headers, url)
                    logger.error(f"Rate limit exceeded: {error_msg}")
                    raise GitHubRateLimitError(error_msg)

                if response.status_code != 200:
                    error_msg = format_rate_limit_error(response.status_code, response.headers, url)
                    logger.error(f"API error: {error_msg}")
                    raise RuntimeError(error_msg)

                return response.json()

            except httpx.HTTPError as e:
                log_error(e, f"HTTP error fetching release from {url}")
                raise RuntimeError(f"Failed to fetch release: {e}")

    def download_release_asset(
        self,
        download_url: str,
        destination: Path,
        show_progress: bool = True,
    ) -> None:
        """
        Download a release asset from GitHub.

        Args:
            download_url: Asset download URL
            destination: Path to save downloaded file
            show_progress: Show progress bar

        Raises:
            RuntimeError: If download fails
        """
        logger.info(f"Downloading asset from {download_url}")

        with httpx.Client(verify=self.ssl_context) as client:
            try:
                with client.stream(
                    "GET",
                    download_url,
                    headers=self._get_headers(),
                    timeout=60,
                    follow_redirects=True,
                ) as response:
                    if response.status_code != 200:
                        error_msg = format_rate_limit_error(response.status_code, response.headers, download_url)
                        raise RuntimeError(error_msg)

                    total_size = int(response.headers.get("content-length", 0))
                    log_api_call(download_url, "GET", response.status_code)

                    with open(destination, "wb") as f:
                        if total_size == 0 or not show_progress:
                            for chunk in response.iter_bytes(chunk_size=8192):
                                f.write(chunk)
                        else:
                            with Progress(
                                SpinnerColumn(),
                                TextColumn("[progress.description]{task.description}"),
                                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                                console=console,
                            ) as progress:
                                task = progress.add_task("Downloading...", total=total_size)
                                downloaded = 0
                                for chunk in response.iter_bytes(chunk_size=8192):
                                    f.write(chunk)
                                    downloaded += len(chunk)
                                    progress.update(task, completed=downloaded)

                    logger.info(f"Downloaded {total_size:,} bytes to {destination}")

            except httpx.HTTPError as e:
                log_error(e, f"HTTP error downloading asset from {download_url}")
                if destination.exists():
                    destination.unlink()
                raise RuntimeError(f"Failed to download asset: {e}")

    def find_matching_asset(self, release_data: dict, pattern: str) -> Optional[dict]:
        """
        Find a release asset matching a pattern.

        Args:
            release_data: Release data from GitHub API
            pattern: Pattern to match in asset name

        Returns:
            Asset dict if found, None otherwise
        """
        assets = release_data.get("assets", [])
        matching = [asset for asset in assets if pattern in asset["name"] and asset["name"].endswith(".zip")]

        if matching:
            logger.debug(f"Found {len(matching)} matching assets for pattern '{pattern}'")
            return matching[0]

        logger.warning(f"No matching asset found for pattern '{pattern}'")
        return None
