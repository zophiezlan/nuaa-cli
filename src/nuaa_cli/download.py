#!/usr/bin/env python3
"""
NUAA CLI Download Module
========================

This module provides comprehensive functionality for downloading and extracting
NUAA project templates from GitHub releases. It handles:

- Secure ZIP file extraction with path traversal protection
- GitHub API rate limiting and authentication
- VSCode settings.json merging for smooth IDE integration
- Deep JSON merging for configuration files
- Template downloading with progress tracking
- Intelligent directory structure flattening

The module ensures robust error handling for network issues, file system errors,
and malicious archive content.

Key Functions:
    - download_template_from_github: Fetch templates from GitHub releases
    - download_and_extract_template: Complete workflow for template setup
    - merge_json_files: Deep merge JSON configuration files
    - handle_vscode_settings: Special handling for VSCode settings
    - _safe_extract_zip: Secure ZIP extraction with security checks

Security Features:
    - Path traversal attack prevention in ZIP extraction
    - SSL/TLS verification with truststore
    - GitHub token support for higher rate limits
    - Comprehensive error handling and user feedback

Author: NUAA Project
License: MIT
"""

import json
import os
import shutil
import ssl
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple

import httpx
import truststore
import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from .utils import StepTracker

# Initialize SSL context with truststore for secure connections
ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)


def _github_token(cli_token: Optional[str] = None) -> Optional[str]:
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
        >>> token = _github_token("ghp_abc123")
        >>> token
        'ghp_abc123'

        >>> os.environ["GH_TOKEN"] = "ghp_xyz789"
        >>> token = _github_token()
        >>> token
        'ghp_xyz789'
    """
    return ((cli_token or os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN") or "").strip()) or None


def _github_auth_headers(cli_token: Optional[str] = None) -> dict:
    """
    Return Authorization header dict only when a non-empty token exists.

    Args:
        cli_token: Token passed via CLI argument

    Returns:
        Dictionary with Authorization header if token exists, empty dict otherwise

    Examples:
        >>> headers = _github_auth_headers("ghp_abc123")
        >>> headers
        {'Authorization': 'Bearer ghp_abc123'}

        >>> headers = _github_auth_headers(None)
        >>> headers
        {}
    """
    token = _github_token(cli_token)
    return {"Authorization": f"Bearer {token}"} if token else {}


def _parse_rate_limit_headers(headers: httpx.Headers) -> dict:
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
        >>> info = _parse_rate_limit_headers(headers)
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


def _format_rate_limit_error(status_code: int, headers: httpx.Headers, url: str) -> str:
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
        >>> error = _format_rate_limit_error(403, headers, 'https://api.github.com/repos/foo/bar')
        >>> 'Rate Limit Information' in error
        True
    """
    rate_info = _parse_rate_limit_headers(headers)

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
    lines.append("  • Consider using a GitHub token via --github-token or the GH_TOKEN/GITHUB_TOKEN")
    lines.append("    environment variable to increase rate limits.")
    lines.append("  • Authenticated requests have a limit of 5,000/hour vs 60/hour for unauthenticated.")

    return "\n".join(lines)


def _safe_extract_zip(zip_ref: zipfile.ZipFile, extract_path: Path, console: Console = Console()) -> None:
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
        ...     _safe_extract_zip(zf, Path('/tmp/safe_dir'))

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

    def deep_merge(base: dict, update: dict) -> dict:
        """Recursively merge update dict into base dict."""
        result = base.copy()
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                # Recursively merge nested dictionaries
                result[key] = deep_merge(result[key], value)
            else:
                # Add new key or replace existing value
                result[key] = value
        return result

    merged = deep_merge(existing_content, new_content)

    if verbose:
        console.print(f"[cyan]Merged JSON file:[/cyan] {existing_path.name}")

    return merged


def download_template_from_github(
    ai_assistant: str,
    download_dir: Path,
    *,
    script_type: str = "sh",
    verbose: bool = True,
    show_progress: bool = True,
    client: Optional[httpx.Client] = None,
    debug: bool = False,
    github_token: Optional[str] = None,
    console: Console = Console(),
) -> Tuple[Path, dict]:
    """
    Download NUAA template from GitHub releases.

    Fetches the latest release from the NUAA CLI repository and downloads the
    appropriate template asset based on AI assistant and script type preferences.

    Args:
        ai_assistant: AI assistant identifier (e.g., 'claude', 'copilot', 'codex')
        download_dir: Directory to download the template ZIP file to
        script_type: Script type ('sh' for POSIX shell or 'ps' for PowerShell)
        verbose: Whether to print detailed progress messages
        show_progress: Whether to show download progress bar
        client: Optional httpx.Client to reuse (creates new one if None)
        debug: Whether to print debug information on errors
        github_token: Optional GitHub token for authentication (increases rate limits)
        console: Rich console for output (defaults to new Console instance)

    Returns:
        Tuple of (zip_path, metadata) where:
        - zip_path: Path to downloaded ZIP file
        - metadata: Dict with 'filename', 'size', 'release', 'asset_url'

    Raises:
        typer.Exit: On network errors, rate limiting, or missing assets
        RuntimeError: On API errors or invalid responses

    Examples:
        >>> from pathlib import Path
        >>> zip_path, meta = download_template_from_github(
        ...     'claude',
        ...     Path('/tmp'),
        ...     script_type='sh',
        ...     verbose=True
        ... )
        >>> meta['release']
        'v1.0.0'
    """
    # NUAA templates are published as release assets in this repository
    repo_owner = "zophiezlan"
    repo_name = "nuaa-cli"
    close_client = False
    http_client = client
    if http_client is None:
        http_client = httpx.Client(verify=ssl_context)
        close_client = True

    if verbose:
        console.print("[cyan]Fetching latest release information...[/cyan]")
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    try:
        response = http_client.get(
            api_url,
            timeout=30,
            follow_redirects=True,
            headers=_github_auth_headers(github_token),
        )
        status = response.status_code
        if status != 200:
            # Format detailed error message with rate-limit info
            error_msg = _format_rate_limit_error(status, response.headers, api_url)
            if debug:
                error_msg += f"\n\n[dim]Response body (truncated 500):[/dim]\n{response.text[:500]}"
            raise RuntimeError(error_msg)
        try:
            release_data = response.json()
        except ValueError as je:
            raise RuntimeError(f"Failed to parse release JSON: {je}\nRaw (truncated 400): {response.text[:400]}")
    except httpx.TimeoutException:
        console.print("[red]Error fetching release information[/red]")
        console.print(
            Panel(
                "Request timed out connecting to GitHub API",
                title="Fetch Error",
                border_style="red",
            )
        )
        raise typer.Exit(1)
    except httpx.ConnectError:
        console.print("[red]Error fetching release information[/red]")
        console.print(
            Panel(
                "Could not connect to GitHub API. Check your internet connection.",
                title="Fetch Error",
                border_style="red",
            )
        )
        raise typer.Exit(1)
    except httpx.HTTPError as e:
        console.print("[red]Error fetching release information[/red]")
        console.print(Panel(f"HTTP error occurred: {e}", title="Fetch Error", border_style="red"))
        raise typer.Exit(1)
    except RuntimeError as e:
        console.print("[red]Error fetching release information[/red]")
        console.print(Panel(str(e), title="Fetch Error", border_style="red"))
        raise typer.Exit(1)

    assets = release_data.get("assets", [])
    # Expected asset name pattern: nuaa-template-<agent>-<script>-<version>.zip
    pattern = f"nuaa-template-{ai_assistant}-{script_type}"
    matching_assets = [asset for asset in assets if pattern in asset["name"] and asset["name"].endswith(".zip")]

    asset = matching_assets[0] if matching_assets else None

    if asset is None:
        console.print(
            f"[red]No matching release asset found[/red] for [bold]{ai_assistant}[/bold] "
            f"(expected pattern: [bold]{pattern}[/bold])"
        )
        asset_names = [a.get("name", "?") for a in assets]
        console.print(
            Panel(
                "\n".join(asset_names) or "(no assets)",
                title="Available Assets",
                border_style="yellow",
            )
        )
        raise typer.Exit(1)

    download_url = asset["browser_download_url"]
    filename = asset["name"]
    file_size = asset["size"]

    if verbose:
        console.print(f"[cyan]Found template:[/cyan] {filename}")
        console.print(f"[cyan]Size:[/cyan] {file_size:,} bytes")
        console.print(f"[cyan]Release:[/cyan] {release_data['tag_name']}")

    zip_path = download_dir / filename
    if verbose:
        console.print("[cyan]Downloading template...[/cyan]")

    try:
        with http_client.stream(
            "GET",
            download_url,
            timeout=60,
            follow_redirects=True,
            headers=_github_auth_headers(github_token),
        ) as response:
            if response.status_code != 200:
                # Handle rate-limiting on download as well
                error_msg = _format_rate_limit_error(response.status_code, response.headers, download_url)
                if debug:
                    error_msg += f"\n\n[dim]Response body (truncated 400):[/dim]\n{response.text[:400]}"
                raise RuntimeError(error_msg)
            total_size = int(response.headers.get("content-length", 0))
            with open(zip_path, "wb") as f:
                if total_size == 0:
                    for chunk in response.iter_bytes(chunk_size=8192):
                        f.write(chunk)
                else:
                    if show_progress:
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
                    else:
                        for chunk in response.iter_bytes(chunk_size=8192):
                            f.write(chunk)
        if verbose:
            console.print(f"Downloaded: {filename}")
        metadata = {
            "filename": filename,
            "size": file_size,
            "release": release_data["tag_name"],
            "asset_url": download_url,
        }
        return zip_path, metadata
    except httpx.TimeoutException:
        console.print("[red]Error downloading template[/red]")
        if zip_path.exists():
            zip_path.unlink()
        console.print(Panel("Download timed out. Please try again.", title="Download Error", border_style="red"))
        raise typer.Exit(1)
    except httpx.ConnectError:
        console.print("[red]Error downloading template[/red]")
        if zip_path.exists():
            zip_path.unlink()
        console.print(
            Panel(
                "Could not connect to GitHub. Check your internet connection.",
                title="Download Error",
                border_style="red",
            )
        )
        raise typer.Exit(1)
    except httpx.HTTPError as e:
        console.print("[red]Error downloading template[/red]")
        if zip_path.exists():
            zip_path.unlink()
        console.print(Panel(f"HTTP error: {e}", title="Download Error", border_style="red"))
        raise typer.Exit(1)
    except PermissionError:
        console.print("[red]Error downloading template[/red]")
        if zip_path.exists():
            zip_path.unlink()
        console.print(
            Panel(
                f"Permission denied writing to: {zip_path}",
                title="Download Error",
                border_style="red",
            )
        )
        raise typer.Exit(1)
    except OSError as e:
        console.print("[red]Error downloading template[/red]")
        if zip_path.exists():
            zip_path.unlink()
        console.print(Panel(f"File system error: {e}", title="Download Error", border_style="red"))
        raise typer.Exit(1)
    except RuntimeError as e:
        console.print("[red]Error downloading template[/red]")
        if zip_path.exists():
            zip_path.unlink()
        console.print(Panel(str(e), title="Download Error", border_style="red"))
        raise typer.Exit(1)
    finally:
        if close_client:
            http_client.close()


def download_and_extract_template(
    project_path: Path,
    ai_assistant: str,
    script_type: str,
    is_current_dir: bool = False,
    *,
    verbose: bool = True,
    tracker: Optional[StepTracker] = None,
    client: Optional[httpx.Client] = None,
    debug: bool = False,
    github_token: Optional[str] = None,
    console: Console = Console(),
) -> Path:
    """
    Download the latest release and extract it to create a new project.

    Complete workflow that handles:
    - Downloading template from GitHub
    - Extracting ZIP archive securely
    - Flattening nested directory structures
    - Merging with existing directories when using current directory
    - Special handling for VSCode settings
    - Progress tracking and error handling

    Args:
        project_path: Target path for the new project
        ai_assistant: AI assistant identifier (e.g., 'claude', 'copilot', 'codex')
        script_type: Script type ('sh' for POSIX shell or 'ps' for PowerShell)
        is_current_dir: Whether extracting into current directory (merge mode)
        verbose: Whether to print detailed progress messages
        tracker: Optional StepTracker for progress tracking
        client: Optional httpx.Client to reuse
        debug: Whether to print debug information on errors
        github_token: Optional GitHub token for authentication
        console: Rich console for output (defaults to new Console instance)

    Returns:
        Path to the created/updated project directory

    Raises:
        typer.Exit: On extraction errors, network issues, or file system errors

    Examples:
        >>> from pathlib import Path
        >>> project_path = download_and_extract_template(
        ...     Path('/tmp/my-project'),
        ...     'claude',
        ...     'sh',
        ...     verbose=True
        ... )
        >>> project_path.exists()
        True

    Note:
        Uses tracker if provided with expected keys:
        - fetch: Fetching release from GitHub
        - download: Downloading template ZIP
        - extract: Extracting template
        - cleanup: Removing temporary files
    """
    current_dir = Path.cwd()

    if tracker:
        tracker.start("fetch", "contacting GitHub API")
    try:
        zip_path, meta = download_template_from_github(
            ai_assistant,
            current_dir,
            script_type=script_type,
            verbose=verbose and tracker is None,
            show_progress=(tracker is None),
            client=client,
            debug=debug,
            github_token=github_token,
            console=console,
        )
        if tracker:
            tracker.complete("fetch", f"release {meta['release']} ({meta['size']:,} bytes)")
            tracker.add("download", "Download template")
            tracker.complete("download", meta["filename"])
    except (
        httpx.TimeoutException,
        httpx.ConnectError,
        httpx.HTTPError,
        RuntimeError,
        PermissionError,
        OSError,
    ) as e:
        if tracker:
            tracker.error("fetch", str(e))
        else:
            if verbose:
                console.print(f"[red]Error downloading template:[/red] {e}")
        raise

    if tracker:
        tracker.add("extract", "Extract template")
        tracker.start("extract")
    elif verbose:
        console.print("Extracting template...")

    try:
        if not is_current_dir:
            project_path.mkdir(parents=True)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_contents = zip_ref.namelist()
            if tracker:
                tracker.start("zip-list")
                tracker.complete("zip-list", f"{len(zip_contents)} entries")
            elif verbose:
                console.print(f"[cyan]ZIP contains {len(zip_contents)} items[/cyan]")

            if is_current_dir:
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    _safe_extract_zip(zip_ref, temp_path, console)

                    extracted_items = list(temp_path.iterdir())
                    if tracker:
                        tracker.start("extracted-summary")
                        tracker.complete("extracted-summary", f"temp {len(extracted_items)} items")
                    elif verbose:
                        console.print(f"[cyan]Extracted {len(extracted_items)} items to temp location[/cyan]")

                    source_dir = temp_path
                    if len(extracted_items) == 1 and extracted_items[0].is_dir():
                        source_dir = extracted_items[0]
                        if tracker:
                            tracker.add("flatten", "Flatten nested directory")
                            tracker.complete("flatten")
                        elif verbose:
                            console.print("[cyan]Found nested directory structure[/cyan]")

                    for item in source_dir.iterdir():
                        dest_path = project_path / item.name
                        if item.is_dir():
                            if dest_path.exists():
                                if verbose and not tracker:
                                    console.print(f"[yellow]Merging directory:[/yellow] {item.name}")
                                for sub_item in item.rglob("*"):
                                    if sub_item.is_file():
                                        rel_path = sub_item.relative_to(item)
                                        dest_file = dest_path / rel_path
                                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                                        # Special handling for .vscode/settings.json - merge instead of overwrite
                                        if dest_file.name == "settings.json" and dest_file.parent.name == ".vscode":
                                            handle_vscode_settings(
                                                sub_item,
                                                dest_file,
                                                rel_path,
                                                verbose,
                                                tracker,
                                                console,
                                            )
                                        else:
                                            shutil.copy2(sub_item, dest_file)
                            else:
                                shutil.copytree(item, dest_path)
                        else:
                            if dest_path.exists() and verbose and not tracker:
                                console.print(f"[yellow]Overwriting file:[/yellow] {item.name}")
                            shutil.copy2(item, dest_path)
                    if verbose and not tracker:
                        console.print("[cyan]Template files merged into current directory[/cyan]")
            else:
                _safe_extract_zip(zip_ref, project_path, console)

                extracted_items = list(project_path.iterdir())
                if tracker:
                    tracker.start("extracted-summary")
                    tracker.complete("extracted-summary", f"{len(extracted_items)} top-level items")
                elif verbose:
                    console.print(f"[cyan]Extracted {len(extracted_items)} items to {project_path}:[/cyan]")
                    for item in extracted_items:
                        console.print(f"  - {item.name} ({'dir' if item.is_dir() else 'file'})")

                if len(extracted_items) == 1 and extracted_items[0].is_dir():
                    nested_dir = extracted_items[0]
                    temp_move_dir = project_path.parent / f"{project_path.name}_temp"

                    shutil.move(str(nested_dir), str(temp_move_dir))

                    project_path.rmdir()

                    shutil.move(str(temp_move_dir), str(project_path))
                    if tracker:
                        tracker.add("flatten", "Flatten nested directory")
                        tracker.complete("flatten")
                    elif verbose:
                        console.print("[cyan]Flattened nested directory structure[/cyan]")

    except zipfile.BadZipFile:
        if tracker:
            tracker.error("extract", "Invalid or corrupted ZIP file")
        else:
            if verbose:
                console.print("[red]Error extracting template:[/red] Invalid or corrupted ZIP file")
                if debug:
                    console.print(
                        Panel(
                            "The downloaded file is not a valid ZIP archive",
                            title="Extraction Error",
                            border_style="red",
                        )
                    )

        if not is_current_dir and project_path.exists():
            shutil.rmtree(project_path)
        raise typer.Exit(1)
    except PermissionError as e:
        if tracker:
            tracker.error("extract", f"Permission denied: {e}")
        else:
            if verbose:
                console.print("[red]Error extracting template:[/red] Permission denied")
                if debug:
                    console.print(Panel(str(e), title="Extraction Error", border_style="red"))

        if not is_current_dir and project_path.exists():
            shutil.rmtree(project_path)
        raise typer.Exit(1)
    except OSError as e:
        if tracker:
            tracker.error("extract", f"File system error: {e}")
        else:
            if verbose:
                console.print(f"[red]Error extracting template:[/red] File system error: {e}")
                if debug:
                    console.print(Panel(str(e), title="Extraction Error", border_style="red"))

        if not is_current_dir and project_path.exists():
            shutil.rmtree(project_path)
        raise typer.Exit(1)
    else:
        if tracker:
            tracker.complete("extract")
    finally:
        if tracker:
            tracker.add("cleanup", "Remove temporary archive")

        if zip_path.exists():
            zip_path.unlink()
            if tracker:
                tracker.complete("cleanup")
            elif verbose:
                console.print(f"Cleaned up: {zip_path.name}")

    return project_path
