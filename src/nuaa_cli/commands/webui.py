"""
NUAA CLI WebUI Command Module
==============================

This module provides the 'webui' command for starting the NUAA Simple Web Interface.

The webui command launches a Flask-based web interface on localhost:5000, providing
an accessible, browser-based alternative to the command-line interface.

Features:
    - Automatic dependency checking and installation
    - Browser auto-launch
    - Support for custom host and port
    - Cross-platform compatibility

Usage Examples:
    $ nuaa webui                    # Start on localhost:5000
    $ nuaa webui --port 8000        # Start on custom port
    $ nuaa webui --host 0.0.0.0     # Listen on all interfaces

Author: NUAA Project
License: MIT
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel


def _find_webui_path() -> Optional[Path]:
    """
    Find the NUAA WebUI installation path.

    Searches multiple locations:
    1. Within the installed nuaa_cli package (interfaces/web-simple)
    2. Relative to the current working directory
    3. Within a NUAA project (.nuaa directory exists)

    Returns:
        Path to the web-simple directory if found, None otherwise
    """
    # Strategy 1: Check if running from installed package
    try:
        import nuaa_cli
        cli_path = Path(nuaa_cli.__file__).parent.parent
        webui_path = cli_path / "interfaces" / "web-simple"
        if webui_path.exists() and (webui_path / "app.py").exists():
            return webui_path
    except (ImportError, AttributeError):
        pass

    # Strategy 2: Check relative to current directory
    current_dir = Path.cwd()
    possible_paths = [
        current_dir / "interfaces" / "web-simple",
        current_dir / ".." / "interfaces" / "web-simple",
        current_dir.parent / "interfaces" / "web-simple",
    ]

    for path in possible_paths:
        if path.exists() and (path / "app.py").exists():
            return path.resolve()

    return None


def _check_dependencies() -> list[str]:
    """
    Check if Flask and required dependencies are installed.

    Returns:
        List of missing package names
    """
    missing = []

    try:
        import flask
    except ImportError:
        missing.append("flask")

    try:
        import werkzeug
    except ImportError:
        missing.append("werkzeug")

    return missing


def _install_dependencies(packages: list[str], console: Console) -> bool:
    """
    Install missing dependencies using pip.

    Args:
        packages: List of package names to install
        console: Rich console for output

    Returns:
        True if installation succeeded, False otherwise
    """
    console.print(f"\n[yellow]Installing required dependencies: {', '.join(packages)}[/yellow]")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet"] + packages,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        console.print("[green]✓ Dependencies installed successfully[/green]")
        return True
    except subprocess.CalledProcessError:
        return False


def _webui_command(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host to bind to"),
    port: int = typer.Option(5000, "--port", "-p", help="Port to bind to"),
    no_browser: bool = typer.Option(False, "--no-browser", help="Don't open browser automatically"),
    console: Console = None,
) -> None:
    """
    Start the NUAA Simple Web Interface.

    The WebUI provides a browser-based interface for teams who prefer
    graphical workflows over command-line tools.

    Examples:
        nuaa webui
        nuaa webui --port 8080
        nuaa webui --host 0.0.0.0 --no-browser
    """
    if console is None:
        console = Console()

    console.print(
        Panel.fit(
            "[bold cyan]NUAA WebUI Launcher[/bold cyan]\n"
            "[dim]Starting the Simple Web Interface...[/dim]",
            border_style="cyan",
        )
    )

    # Find WebUI installation
    console.print("\n[1/3] Locating NUAA WebUI...")
    webui_path = _find_webui_path()

    if webui_path is None:
        console.print("\n[red]❌ ERROR: Could not locate NUAA WebUI installation.[/red]")
        console.print("\n[yellow]Please ensure you have nuaa-cli properly installed.[/yellow]")
        console.print("\nFor installation help, visit:")
        console.print("  [blue]https://github.com/zophiezlan/nuaa-cli[/blue]")
        raise typer.Exit(1)

    console.print(f"[green]✓ Found WebUI at:[/green] [dim]{webui_path}[/dim]")

    # Check dependencies
    console.print("\n[2/3] Checking dependencies...")
    missing = _check_dependencies()

    if missing:
        console.print(f"[yellow]⚠ Missing packages: {', '.join(missing)}[/yellow]")
        if not _install_dependencies(missing, console):
            console.print("\n[red]❌ ERROR: Failed to install dependencies.[/red]")
            console.print("\n[yellow]Please install manually:[/yellow]")
            console.print(f"  pip install {' '.join(missing)}")
            raise typer.Exit(1)
    else:
        console.print("[green]✓ All dependencies satisfied[/green]")

    # Start the server
    console.print("\n[3/3] Starting WebUI server...")
    url = f"http://{host if host != '0.0.0.0' else 'localhost'}:{port}"
    console.print(f"\n[bold green]✓ Server starting on:[/bold green] [cyan]{url}[/cyan]")
    console.print("\n[dim]Press Ctrl+C to stop the server[/dim]\n")
    console.print("=" * 60)

    # Open browser after a delay
    if not no_browser:

        def open_browser():
            time.sleep(2)
            webbrowser.open(url)

        import threading

        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()

    # Change to WebUI directory and start Flask
    original_dir = os.getcwd()
    try:
        os.chdir(webui_path)

        # Set Flask environment variables
        env = os.environ.copy()
        env["FLASK_APP"] = "app.py"
        env["FLASK_RUN_HOST"] = host
        env["FLASK_RUN_PORT"] = str(port)

        # Start the Flask app
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Shutting down NUAA WebUI. Goodbye![/yellow]")
    finally:
        os.chdir(original_dir)


def register(app: typer.Typer, show_banner=None, console: Console = None) -> None:
    """
    Register the webui command with the Typer app.

    Args:
        app: The Typer application to register with
        show_banner: Optional banner display function (unused for this command)
        console: Optional Rich console for output
    """

    @app.command()
    def webui(
        host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host to bind to"),
        port: int = typer.Option(5000, "--port", "-p", help="Port to bind to"),
        no_browser: bool = typer.Option(False, "--no-browser", help="Don't open browser automatically"),
    ):
        """Start the NUAA Simple Web Interface."""
        _webui_command(host, port, no_browser, console or Console())
