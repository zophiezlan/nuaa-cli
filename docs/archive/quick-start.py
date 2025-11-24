#!/usr/bin/env python3
"""
NUAA Quick Start - One-Click Setup for Non-Technical Users

This script automatically sets up and launches the NUAA WebUI with zero configuration.
Perfect for users with no technical experience.

Usage:
    python quick-start.py

    OR double-click this file (on most systems)
"""

import os
import sys
import subprocess
import platform
import webbrowser
import time
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output"""

    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    END = "\033[0m"
    BOLD = "\033[1m"


def clear_screen():
    """Clear the terminal screen"""
    os.system("cls" if platform.system() == "Windows" else "clear")


def print_banner():
    """Print welcome banner"""
    print(
        f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        {Colors.BOLD}NUAA Quick Start - WebUI Setup{Colors.END}{Colors.CYAN}                  ║
║                                                              ║
║        No technical skills needed!                           ║
║        This will take about 60 seconds...                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}
"""
    )


def print_step(step_num, total_steps, message):
    """Print a progress step"""
    print(f"\n{Colors.BLUE}[{step_num}/{total_steps}]{Colors.END} {message}...", end="", flush=True)


def print_success(message="Done!"):
    """Print success message"""
    print(f" {Colors.GREEN}✓ {message}{Colors.END}")


def print_error(message):
    """Print error message"""
    print(f" {Colors.RED}✗ {message}{Colors.END}")


def print_warning(message):
    """Print warning message"""
    print(f"\n{Colors.YELLOW}⚠ {message}{Colors.END}")


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        return False, f"{version.major}.{version.minor}"
    return True, f"{version.major}.{version.minor}"


def check_dependency(package_name):
    """Check if a Python package is installed"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False


def install_dependencies():
    """Install required dependencies"""
    required_packages = ["flask", "werkzeug"]
    missing_packages = [pkg for pkg in required_packages if not check_dependency(pkg)]

    if not missing_packages:
        return True, []

    try:
        # Try to install missing packages
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet", "--user"] + missing_packages,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True, missing_packages
    except subprocess.CalledProcessError:
        return False, missing_packages


def find_webui_path():
    """Find the WebUI directory"""
    current_dir = Path(__file__).parent
    possible_paths = [
        current_dir / "interfaces" / "web-simple",
        current_dir / "web-simple",
        current_dir / ".." / "interfaces" / "web-simple",
    ]

    for path in possible_paths:
        if path.exists() and (path / "app.py").exists():
            return path.resolve()

    return None


def get_local_ip():
    """Get local IP address for sharing"""
    try:
        import socket

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"


def create_desktop_shortcut(webui_path):
    """Create a desktop shortcut for easy access"""
    system = platform.system()
    desktop = Path.home() / "Desktop"

    if not desktop.exists():
        return False

    try:
        if system == "Windows":
            # Create batch file
            shortcut_path = desktop / "NUAA WebUI.bat"
            with open(shortcut_path, "w") as f:
                f.write("@echo off\n")
                f.write(f'cd /d "{webui_path}"\n')
                f.write('start "" "http://localhost:5000"\n')
                f.write("python app.py\n")
                f.write("pause\n")
            return True

        elif system == "Darwin":  # macOS
            # Create shell script
            shortcut_path = desktop / "NUAA WebUI.command"
            with open(shortcut_path, "w") as f:
                f.write("#!/bin/bash\n")
                f.write(f'cd "{webui_path}"\n')
                f.write('open "http://localhost:5000"\n')
                f.write("python3 app.py\n")
            os.chmod(shortcut_path, 0o755)
            return True

        elif system == "Linux":
            # Create desktop file
            shortcut_path = desktop / "NUAA-WebUI.desktop"
            with open(shortcut_path, "w") as f:
                f.write("[Desktop Entry]\n")
                f.write("Version=1.0\n")
                f.write("Type=Application\n")
                f.write("Name=NUAA WebUI\n")
                f.write("Comment=NUAA Harm Reduction WebUI\n")
                f.write(f"Exec=python3 {webui_path}/app.py\n")
                f.write(f"Path={webui_path}\n")
                f.write("Terminal=false\n")
                f.write("Categories=Office;Utility;\n")
            os.chmod(shortcut_path, 0o755)
            return True

    except Exception:
        return False

    return False


def start_webui(webui_path):
    """Start the WebUI server"""
    try:
        # Change to WebUI directory
        os.chdir(webui_path)

        # Start the server
        env = os.environ.copy()
        env["FLASK_APP"] = "app.py"
        env["FLASK_ENV"] = "development"

        process = subprocess.Popen(
            [sys.executable, "app.py"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Wait a moment for server to start
        time.sleep(2)

        # Check if process is still running
        if process.poll() is not None:
            # Process died, get error
            _, stderr = process.communicate()
            return False, process, stderr

        return True, process, None

    except Exception as e:
        return False, None, str(e)


def main():
    """Main setup flow"""
    clear_screen()
    print_banner()

    total_steps = 6

    # Step 1: Check Python version
    print_step(1, total_steps, "Checking Python version")
    compatible, version = check_python_version()
    if not compatible:
        print_error(f"Python {version} is too old")
        print(f"\n{Colors.RED}Sorry! NUAA requires Python 3.8 or newer.{Colors.END}")
        print(f"You have Python {version}")
        print("\nPlease download Python from: https://www.python.org/downloads/")
        input("\nPress Enter to exit...")
        sys.exit(1)
    print_success(f"Python {version}")

    # Step 2: Check/Install dependencies
    print_step(2, total_steps, "Checking dependencies")
    success, packages = install_dependencies()
    if not success:
        print_error("Failed to install dependencies")
        print(
            f"\n{Colors.RED}Could not install required packages: {', '.join(packages)}{Colors.END}"
        )
        print("\nPlease try running:")
        print(f"  pip install {' '.join(packages)}")
        input("\nPress Enter to exit...")
        sys.exit(1)
    if packages:
        print_success(f"Installed {', '.join(packages)}")
    else:
        print_success("All installed")

    # Step 3: Find WebUI
    print_step(3, total_steps, "Locating WebUI")
    webui_path = find_webui_path()
    if not webui_path:
        print_error("WebUI not found")
        print(f"\n{Colors.RED}Could not find the WebUI directory.{Colors.END}")
        print("\nPlease make sure you're running this from the NUAA project directory.")
        input("\nPress Enter to exit...")
        sys.exit(1)
    print_success(f"Found at {webui_path}")

    # Step 4: Create desktop shortcut
    print_step(4, total_steps, "Creating desktop shortcut")
    if create_desktop_shortcut(webui_path):
        print_success("Shortcut created")
    else:
        print_warning("Could not create shortcut (not critical)")

    # Step 5: Start server
    print_step(5, total_steps, "Starting WebUI server")
    success, process, error = start_webui(webui_path)
    if not success:
        print_error("Failed to start")
        print(f"\n{Colors.RED}Could not start the server:{Colors.END}")
        print(f"{error}")
        input("\nPress Enter to exit...")
        sys.exit(1)
    print_success("Server running")

    # Step 6: Open browser
    print_step(6, total_steps, "Opening browser")
    time.sleep(1)
    try:
        webbrowser.open("http://localhost:5000")
        print_success("Browser opened")
    except Exception:
        print_warning("Could not open browser automatically")

    # Success message
    local_ip = get_local_ip()

    print(
        f"""
{Colors.GREEN}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        {Colors.BOLD}SUCCESS! NUAA WebUI is now running!{Colors.END}{Colors.GREEN}                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.BOLD}Your WebUI is accessible at:{Colors.END}

  {Colors.CYAN}On this computer:{Colors.END}
    http://localhost:5000

  {Colors.CYAN}From other devices on your network:{Colors.END}
    http://{local_ip}:5000

{Colors.BOLD}What to do next:{Colors.END}

  1. Your browser should open automatically
  2. Bookmark the page for easy access
  3. Share the network URL with your team

{Colors.BOLD}To stop the server:{Colors.END}

  Press Ctrl+C in this window

{Colors.BOLD}To start again later:{Colors.END}

  - Double-click the "NUAA WebUI" shortcut on your desktop
  - OR run this script again: python quick-start.py

{Colors.YELLOW}═══════════════════════════════════════════════════════════════{Colors.END}

Server is running... (Press Ctrl+C to stop)
"""
    )

    try:
        # Keep the script running and show server output
        for line in process.stdout:
            if line.strip():
                print(f"  {Colors.CYAN}[Server]{Colors.END} {line.strip()}")
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Stopping server...{Colors.END}")
        process.terminate()
        process.wait()
        print(f"{Colors.GREEN}Server stopped. Goodbye!{Colors.END}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Setup cancelled.{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n{Colors.RED}An unexpected error occurred:{Colors.END}")
        print(f"{e}")
        input("\nPress Enter to exit...")
        sys.exit(1)
