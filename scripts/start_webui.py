#!/usr/bin/env python3
"""
NUAA WebUI Launcher
===================

Starts the NUAA Simple Web Interface for teams who prefer web-based workflows.

This script:
1. Locates the NUAA CLI installation
2. Checks for Flask dependencies
3. Starts the web interface on localhost:5000
4. Opens the browser automatically

Usage:
    python .nuaa/scripts/start_webui.py

    Or from the CLI:
    nuaa webui
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path


def find_nuaa_cli_path():
    """
    Find the NUAA CLI installation path.

    Tries multiple strategies:
    1. Check if running from within a project (has .nuaa directory)
    2. Check site-packages for installed nuaa-cli
    3. Check if running from the nuaa-cli git repository
    """
    # Strategy 1: Running from within a NUAA project
    current_dir = Path.cwd()
    if (current_dir / ".nuaa").exists():
        # Try to find nuaa-cli in site-packages
        try:
            import nuaa_cli
            return Path(nuaa_cli.__file__).parent.parent.parent
        except ImportError:
            pass

    # Strategy 2: Look for the interfaces/web-simple directory relative to script
    script_dir = Path(__file__).parent
    # If running from .nuaa/scripts, go up to find the installation
    possible_paths = [
        script_dir.parent.parent / "interfaces" / "web-simple",  # From .nuaa/scripts
        script_dir.parent / "interfaces" / "web-simple",  # From scripts/
    ]

    for path in possible_paths:
        if path.exists() and (path / "app.py").exists():
            return path.parent.parent

    # Strategy 3: Check if nuaa-cli is installed
    try:
        import nuaa_cli
        cli_path = Path(nuaa_cli.__file__).parent.parent.parent
        webui_path = cli_path / "interfaces" / "web-simple"
        if webui_path.exists():
            return cli_path
    except ImportError:
        pass

    return None


def check_dependencies():
    """Check if Flask and required dependencies are installed."""
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


def install_dependencies(packages):
    """Install missing dependencies."""
    print(f"\nInstalling required dependencies: {', '.join(packages)}")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet"] + packages
        )
        return True
    except subprocess.CalledProcessError:
        return False


def start_webui(webui_path):
    """Start the WebUI server."""
    print(f"\nStarting NUAA WebUI from: {webui_path}")
    print("Server will be available at: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    print("=" * 60)

    # Change to the WebUI directory
    os.chdir(webui_path)

    # Give the server a moment to start before opening browser
    def open_browser():
        time.sleep(2)
        webbrowser.open("http://localhost:5000")

    # Start browser opener in background
    import threading
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    # Start the Flask app
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n\nShutting down NUAA WebUI. Goodbye!")


def main():
    """Main entry point."""
    print("NUAA WebUI Launcher")
    print("=" * 60)

    # Find NUAA CLI installation
    print("\n[1/4] Locating NUAA WebUI...")
    nuaa_path = find_nuaa_cli_path()

    if nuaa_path is None:
        print("\n❌ ERROR: Could not locate NUAA WebUI installation.")
        print("\nPlease ensure you:")
        print("  1. Have run 'nuaa init' in a project directory, OR")
        print("  2. Are running this from a NUAA project directory, OR")
        print("  3. Have nuaa-cli installed")
        print("\nFor installation help, visit:")
        print("  https://github.com/zophiezlan/nuaa-cli")
        sys.exit(1)

    webui_path = nuaa_path / "interfaces" / "web-simple"
    if not webui_path.exists() or not (webui_path / "app.py").exists():
        print(f"\n❌ ERROR: WebUI not found at expected location: {webui_path}")
        print("\nThe WebUI might not be included in your installation.")
        print("Please reinstall or update nuaa-cli.")
        sys.exit(1)

    print(f"✓ Found WebUI at: {webui_path}")

    # Check dependencies
    print("\n[2/4] Checking dependencies...")
    missing = check_dependencies()

    if missing:
        print(f"⚠ Missing packages: {', '.join(missing)}")
        print("\n[3/4] Installing dependencies...")
        if not install_dependencies(missing):
            print("\n❌ ERROR: Failed to install dependencies.")
            print("\nPlease install manually:")
            print(f"  pip install {' '.join(missing)}")
            sys.exit(1)
        print("✓ Dependencies installed")
    else:
        print("✓ All dependencies satisfied")

    # Start the server
    print("\n[4/4] Starting WebUI server...")
    start_webui(webui_path)


if __name__ == "__main__":
    main()
