#!/usr/bin/env python3
"""
Template Download Orchestration
================================

This module provides the main download orchestration functionality for
downloading and extracting NUAA project templates from GitHub releases.

Functions:
    - download_template_from_github: Fetch templates from GitHub releases
    - download_and_extract_template: Complete workflow for template setup

Features:
    - GitHub release fetching
    - Secure ZIP extraction
    - Directory flattening
    - Merge with existing directories
    - VSCode settings handling
    - Progress tracking

Author: NUAA Project
License: MIT
"""

import shutil
import ssl
import tempfile
import zipfile
from pathlib import Path
from typing import Optional, Tuple

import httpx
import truststore
import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..github_client import get_auth_headers, format_rate_limit_error
from ..error_handler import print_error, display_debug_environment
from .vscode_settings import handle_vscode_settings
from .zip_handler import safe_extract_zip
from ..utils import StepTracker

# Initialize SSL context with truststore for secure connections
ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)


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
            headers=get_auth_headers(github_token),
        )
        status = response.status_code
        if status != 200:
            # Format detailed error message with rate-limit info
            error_msg = format_rate_limit_error(status, response.headers, api_url)
            if debug:
                error_msg += f"\n\n[dim]Response body (truncated 500):[/dim]\n{response.text[:500]}"
            raise RuntimeError(error_msg)
        try:
            release_data = response.json()
        except ValueError as je:
            raise RuntimeError(
                f"Failed to parse release JSON: {je}\nRaw (truncated 400): {response.text[:400]}"
            )
    except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPError) as e:
        error_type = type(e).__name__
        if isinstance(e, httpx.TimeoutException):
            title, message = "Fetch Error", "Request timed out connecting to GitHub API"
        elif isinstance(e, httpx.ConnectError):
            title, message = (
                "Fetch Error",
                "Could not connect to GitHub API. Check your internet connection.",
            )
        else:
            title, message = "Fetch Error", f"HTTP error occurred: {e}"
        print_error(console, title, message)
        if debug:
            display_debug_environment(console)
        raise typer.Exit(1)
    except RuntimeError as e:
        print_error(console, "Fetch Error", str(e))
        if debug:
            display_debug_environment(console)
        raise typer.Exit(1)

    assets = release_data.get("assets", [])
    # Expected asset name pattern: nuaa-template-<agent>-<script>-<version>.zip
    pattern = f"nuaa-template-{ai_assistant}-{script_type}"
    matching_assets = [
        asset for asset in assets if pattern in asset["name"] and asset["name"].endswith(".zip")
    ]

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
            headers=get_auth_headers(github_token),
        ) as response:
            if response.status_code != 200:
                # Handle rate-limiting on download as well
                error_msg = format_rate_limit_error(
                    response.status_code, response.headers, download_url
                )
                if debug:
                    error_msg += (
                        f"\n\n[dim]Response body (truncated 400):[/dim]\n{response.text[:400]}"
                    )
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
    except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPError) as e:
        if zip_path.exists():
            zip_path.unlink()
        if isinstance(e, httpx.TimeoutException):
            title, message = "Download Error", "Download timed out. Please try again."
        elif isinstance(e, httpx.ConnectError):
            title, message = (
                "Download Error",
                "Could not connect to GitHub. Check your internet connection.",
            )
        else:
            title, message = "Download Error", f"HTTP error: {e}"
        print_error(console, title, message)
        if debug:
            display_debug_environment(console)
        raise typer.Exit(1)
    except (PermissionError, OSError) as e:
        if zip_path.exists():
            zip_path.unlink()
        if isinstance(e, PermissionError):
            title, message = "Download Error", f"Permission denied writing to: {zip_path}"
        else:
            title, message = "Download Error", f"File system error: {e}"
        print_error(console, title, message)
        if debug:
            display_debug_environment(console)
        raise typer.Exit(1)
    except RuntimeError as e:
        if zip_path.exists():
            zip_path.unlink()
        print_error(console, "Download Error", str(e))
        if debug:
            display_debug_environment(console)
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
                    safe_extract_zip(zip_ref, temp_path, console)

                    extracted_items = list(temp_path.iterdir())
                    if tracker:
                        tracker.start("extracted-summary")
                        tracker.complete("extracted-summary", f"temp {len(extracted_items)} items")
                    elif verbose:
                        console.print(
                            f"[cyan]Extracted {len(extracted_items)} items to temp location[/cyan]"
                        )

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
                                    console.print(
                                        f"[yellow]Merging directory:[/yellow] {item.name}"
                                    )
                                for sub_item in item.rglob("*"):
                                    if sub_item.is_file():
                                        rel_path = sub_item.relative_to(item)
                                        dest_file = dest_path / rel_path
                                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                                        # Special handling for .vscode/settings.json - merge instead of overwrite
                                        if (
                                            dest_file.name == "settings.json"
                                            and dest_file.parent.name == ".vscode"
                                        ):
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
                safe_extract_zip(zip_ref, project_path, console)

                extracted_items = list(project_path.iterdir())
                if tracker:
                    tracker.start("extracted-summary")
                    tracker.complete("extracted-summary", f"{len(extracted_items)} top-level items")
                elif verbose:
                    console.print(
                        f"[cyan]Extracted {len(extracted_items)} items to {project_path}:[/cyan]"
                    )
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
        error_msg = "Invalid or corrupted ZIP file"
        if tracker:
            tracker.error("extract", error_msg)
        else:
            print_error(
                console,
                "Extraction Error",
                error_msg,
                "The downloaded file is not a valid ZIP archive" if debug else None,
            )
        if not is_current_dir and project_path.exists():
            shutil.rmtree(project_path)
        if debug:
            display_debug_environment(console)
        raise typer.Exit(1)
    except (PermissionError, OSError) as e:
        if isinstance(e, PermissionError):
            error_msg = f"Permission denied: {e}"
        else:
            error_msg = f"File system error: {e}"

        if tracker:
            tracker.error("extract", error_msg)
        else:
            print_error(console, "Extraction Error", error_msg)

        if not is_current_dir and project_path.exists():
            shutil.rmtree(project_path)
        if debug:
            display_debug_environment(console)
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
