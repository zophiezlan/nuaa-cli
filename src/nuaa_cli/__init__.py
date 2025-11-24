#!/usr/bin/env python3
# flake8: noqa
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer",
#     "rich",
#     "platformdirs",
#     "readchar",
#     "httpx",
# ]
# ///
"""
NUAA CLI - AI-Assisted Project Management for NGOs

Usage:
    uvx --from git+https://github.com/zophiezlan/nuaa-cli.git nuaa init <project-name>
    uvx --from git+https://github.com/zophiezlan/nuaa-cli.git nuaa init .
    uvx --from git+https://github.com/zophiezlan/nuaa-cli.git nuaa init --here

Or install globally (via package name):
    uv tool install --from . nuaa-cli
    nuaa init <project-name>
    nuaa init .
    nuaa init --here

Legacy alias: the "specify" command still works for backwards compatibility.
"""

import os
import subprocess
import sys
import zipfile
import tempfile
import shutil
import shlex
import json
from pathlib import Path
from typing import Optional, Tuple
import re
from datetime import datetime, timezone

import typer
import httpx
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.live import Live
from rich.align import Align
from rich.table import Table
from rich.tree import Tree
from typer.core import TyperGroup

# For cross-platform keyboard input
import readchar
import ssl
import truststore

ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
from .utils import StepTracker, check_tool

# Import from new modularized components
from .banner import BannerGroup, show_banner
from .ui import get_key, select_with_arrows
from .git_utils import run_command, is_git_repo, init_git_repo
from .scripts import ensure_executable_scripts
from .download import (
    download_template_from_github,
    download_and_extract_template,
    handle_vscode_settings,
    merge_json_files,
)


from .scaffold import (
    _slugify,
    _find_templates_root,
    _ensure_nuaa_root,
    _next_feature_dir,
    _find_feature_dir_by_program,
    _load_template,
    _apply_replacements,
    _prepend_metadata,
    _write_markdown,
    _stamp,
)


def _load_agent_config() -> dict:
    """Load agent configuration from the agents.json file."""
    try:
        config_path = Path(__file__).parent / "agents.json"
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        console.print(f"[red]Error loading agent configuration from agents.json:[/red] {e}")
        # Provide a more helpful error message if the file is missing in a packaged context
        if isinstance(e, FileNotFoundError):
            console.print("[yellow]This might happen if the file was not included in the package.[/yellow]")
        raise typer.Exit(1)


# Agent configuration is now loaded from agents.json
AGENT_CONFIG = _load_agent_config()

SCRIPT_TYPE_CHOICES = {"sh": "POSIX Shell (bash/zsh)", "ps": "PowerShell"}


console = Console()

app = typer.Typer(
    name="nuaa",
    help="NUAA Project Kit - AI-assisted NGO program management (built on Spec-Driven Development)",
    add_completion=False,
    invoke_without_command=True,
    cls=BannerGroup,
)


@app.callback()
def callback(ctx: typer.Context):
    """Show banner when no subcommand is provided."""
    if ctx.invoked_subcommand is None and "--help" not in sys.argv and "-h" not in sys.argv:
        show_banner()
        console.print(Align.center("[dim]Run 'nuaa --help' for usage information[/dim]"))
        console.print()


## init command now registered from commands/init.py


@app.command()
def check():
    """Check that all required tools are installed."""
    show_banner()
    console.print("[bold]Checking for installed tools...[/bold]\n")

    tracker = StepTracker("Check Available Tools")

    tracker.add("git", "Git version control")
    git_ok = check_tool("git", tracker=tracker)

    cli_agent_results: dict[str, bool] = {}
    has_ide_agent = False
    for agent_key, agent_config in AGENT_CONFIG.items():
        agent_name = agent_config["name"]
        requires_cli = agent_config["requires_cli"]

        tracker.add(agent_key, agent_name)

        if requires_cli:
            cli_agent_results[agent_key] = check_tool(agent_key, tracker=tracker)
        else:
            # IDE-based agent - skip CLI check and mark as optional
            tracker.skip(agent_key, "IDE-based, no CLI check")
            has_ide_agent = True

    # Check VS Code variants (not in agent config)
    tracker.add("code", "Visual Studio Code")
    code_ok = check_tool("code", tracker=tracker)

    tracker.add("code-insiders", "Visual Studio Code Insiders")
    code_insiders_ok = check_tool("code-insiders", tracker=tracker)

    console.print(tracker.render())

    console.print("\n[bold green]NUAA CLI is ready to use![/bold green]")

    if not git_ok:
        console.print("[dim]Tip: Install git for repository management[/dim]")

    if not any(cli_agent_results.values()):
        if has_ide_agent:
            console.print(
                "[dim]Tip: Install a CLI-based AI assistant if you need standalone workflows; IDE assistants are already supported.[/dim]"
            )
        else:
            console.print("[dim]Tip: Install an AI assistant for the best experience[/dim]")


## design command now registered from commands/design.py


## propose command now registered from commands/propose.py


## measure command now registered from commands/measure.py


## document command now registered from commands/document.py


## report command now registered from commands/report.py


## refine command now registered from commands/refine.py


# Register externalized commands
try:
    from .commands.init import register as _register_init

    _register_init(app, show_banner, console)
except Exception:
    # Safe fallback: ignore registration failure; command suite still usable
    pass

try:
    from .commands.version import register as _register_version

    _register_version(app)
except Exception:
    # Safe fallback: ignore registration failure; command suite still usable
    pass

try:
    from .commands.check import register as _register_check

    _register_check(app, AGENT_CONFIG, show_banner, console)
except Exception:
    # Safe fallback: ignore registration failure; command suite still usable
    pass

try:
    from .commands.design import register as _register_design

    _register_design(app, show_banner, console)
except Exception:
    # Safe fallback: ignore registration failure; command suite still usable
    pass

try:
    from .commands.propose import register as _register_propose

    _register_propose(app, show_banner, console)
except Exception:
    # Safe fallback: ignore registration failure; command suite still usable
    pass

try:
    from .commands.measure import register as _register_measure

    _register_measure(app, show_banner, console)
except Exception:
    # Safe fallback: ignore registration failure; command suite still usable
    pass

try:
    from .commands.document import register as _register_document

    _register_document(app, show_banner, console)
except Exception:
    # Safe fallback: ignore registration failure; command suite still usable
    pass

try:
    from .commands.report import register as _register_report

    _register_report(app, show_banner, console)
except Exception:
    # Safe fallback: ignore registration failure; command suite still usable
    pass

try:
    from .commands.refine import register as _register_refine

    _register_refine(app, show_banner, console)
except Exception:
    # Safe fallback: ignore registration failure; command suite still usable
    pass

try:
    from .commands.engage import register as _register_engage

    _register_engage(app, show_banner, console)
except Exception:
    # Safe fallback: ignore registration failure; command suite still usable
    pass

try:
    from .commands.partner import register as _register_partner

    _register_partner(app, show_banner, console)
except Exception:
    # Safe fallback: ignore registration failure; command suite still usable
    pass

try:
    from .commands.train import register as _register_train

    _register_train(app, show_banner, console)
except Exception:
    # Safe fallback: ignore registration failure; command suite still usable
    pass

try:
    from .commands.event import register as _register_event

    _register_event(app, show_banner, console)
except Exception:
    # Safe fallback: ignore registration failure; command suite still usable
    pass

try:
    from .commands.risk import register as _register_risk

    _register_risk(app, show_banner, console)
except Exception:
    # Safe fallback: ignore registration failure; command suite still usable
    pass

try:
    from .commands.webui import register as _register_webui

    _register_webui(app, show_banner, console)
except Exception:
    # Safe fallback: ignore registration failure; command suite still usable
    pass


def main():
    app()


if __name__ == "__main__":
    main()
