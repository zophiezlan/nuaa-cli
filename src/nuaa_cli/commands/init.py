"""
NUAA CLI Init Command Module
=============================

This module provides the 'init' command for initializing new NUAA Project Kit workspaces
from the latest template. It orchestrates the complete project setup workflow including:

- Tool validation (git, AI assistant CLIs)
- Interactive selection of AI assistant and script type
- Template download from GitHub releases
- Secure ZIP extraction with path traversal protection
- Git repository initialization
- Script permission management
- Configuration file merging

The init command is the primary entry point for creating new NUAA projects, setting up
the complete directory structure, agent-specific command folders, and initial configuration
files needed for AI-assisted NGO program management.

Architecture:
    This module follows the standard NUAA command pattern with a `register()` function
    that registers the command with the Typer app, accepting optional banner and console
    parameters for consistent UI across all commands.

Key Features:
    - Multi-AI assistant support (Claude, Copilot, Gemini, Cursor, etc.)
    - Cross-platform script generation (PowerShell/POSIX shell)
    - Current directory initialization with merge support
    - GitHub API rate limiting handling
    - Comprehensive error handling and user feedback
    - SSL/TLS verification with truststore
    - Step-by-step progress tracking

Security:
    - ZIP path traversal attack prevention
    - SSL/TLS verification (optional skip with --skip-tls)
    - GitHub token authentication support
    - File permission validation

Usage Examples:
    $ nuaa init my-project
    $ nuaa init my-project --ai claude
    $ nuaa init . --ai copilot
    $ nuaa init --here --force
    $ nuaa init my-project --no-git --ignore-agent-tools

Author: NUAA Project
License: MIT
"""

import json
import os
import shlex
import shutil
import ssl
import sys
import zipfile
from pathlib import Path
from typing import Optional

import httpx
import truststore
import typer
from rich.console import Console
from rich.live import Live
from rich.panel import Panel

# Import from parent modules
from ..download import download_and_extract_template
from ..git_utils import init_git_repo, is_git_repo
from ..scripts import ensure_executable_scripts
from ..ui import select_with_arrows
from ..utils import StepTracker, check_tool
from ..error_handler import display_debug_environment, handle_network_error

# SSL context for secure connections
ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)


def _load_agent_config() -> dict:
    """
    Load agent configuration from the agents.json file.

    Returns:
        Dictionary containing agent configurations with keys as agent identifiers
        and values as configuration dictionaries containing name, folder, format,
        cli_tool, description, requires_cli, and install_url.

    Raises:
        typer.Exit: If agents.json file is not found or contains invalid JSON.

    Example:
        >>> config = _load_agent_config()
        >>> config['claude']['name']
        'Claude Code'
    """
    try:
        config_path = Path(__file__).parent.parent / "agents.json"
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as e:
        console = Console()
        console.print(f"[red]Error loading agent configuration from agents.json:[/red] {e}")
        console.print(
            "[yellow]This might happen if the file was not included in the package.[/yellow]"
        )
        raise typer.Exit(1)
    except json.JSONDecodeError as e:
        console = Console()
        console.print(f"[red]Error parsing agent configuration from agents.json:[/red] {e}")
        raise typer.Exit(1)


# Agent configuration loaded from agents.json
AGENT_CONFIG = _load_agent_config()

# Script type choices for template generation
SCRIPT_TYPE_CHOICES = {"sh": "POSIX Shell (bash/zsh)", "ps": "PowerShell"}


def register(app, show_banner_fn=None, console: Optional[Console] = None):
    """
    Register the init command with the Typer application.

    This function follows the standard NUAA command registration pattern,
    allowing the init command to be dynamically registered with optional
    banner display and console customization.

    Args:
        app: Typer application instance to register the command with
        show_banner_fn: Optional callable to display the NUAA banner before
            command execution. Should accept no arguments.
        console: Optional Rich Console instance for output. If None, a new
            Console will be created.

    Example:
        >>> from typer import Typer
        >>> app = Typer()
        >>> register(app, show_banner_fn=show_banner)
    """
    console = console or Console()

    @app.command()
    def init(
        project_name: Optional[str] = typer.Argument(
            None,
            help="Name for your new project directory (optional if using --here, or use '.' for current directory)",
        ),
        ai_assistant: Optional[str] = typer.Option(
            None,
            "--ai",
            help=f"AI assistant to use: {', '.join(AGENT_CONFIG.keys())}",
        ),
        script_type: Optional[str] = typer.Option(
            None, "--script", help="Script type to use: sh or ps"
        ),
        ignore_agent_tools: bool = typer.Option(
            False,
            "--ignore-agent-tools",
            help="Skip checks for AI agent tools like Claude Code",
        ),
        no_git: bool = typer.Option(False, "--no-git", help="Skip git repository initialization"),
        here: bool = typer.Option(
            False,
            "--here",
            help="Initialize project in the current directory instead of creating a new one",
        ),
        force: bool = typer.Option(
            False,
            "--force",
            help="Force merge/overwrite when using --here (skip confirmation)",
        ),
        skip_tls: bool = typer.Option(
            False, "--skip-tls", help="Skip SSL/TLS verification (not recommended)"
        ),
        debug: bool = typer.Option(
            False,
            "--debug",
            help="Show verbose diagnostic output for network and extraction failures",
        ),
        github_token: Optional[str] = typer.Option(
            None,
            "--github-token",
            help="GitHub token to use for API requests (or set GH_TOKEN or GITHUB_TOKEN environment variable)",
        ),
    ):
        """
        Initialize a new NUAA Project Kit workspace from the latest template.

        This command orchestrates the complete setup of a new NUAA project workspace,
        providing an opinionated structure for AI-assisted NGO program management. It
        handles everything from tool validation to template extraction and git
        initialization, creating a production-ready environment in minutes.

        The initialization workflow includes:
            1. Tool validation - Checks for required tools (git is optional)
            2. AI assistant selection - Interactive or command-line selection
            3. Script type selection - Choose between POSIX shell or PowerShell
            4. Template download - Fetches latest release from GitHub
            5. Secure extraction - ZIP extraction with security validation
            6. Git initialization - Creates fresh repository (optional)
            7. Configuration setup - Prepares agent-specific folders and settings

        The command supports two initialization modes:
            - New directory: Creates a new project folder with the specified name
            - Current directory: Initializes in current directory with merge support

        When initializing in the current directory (--here or '.'), the command can
        merge template files with existing content. This is useful for adding NUAA
        capabilities to existing projects, but requires confirmation unless --force
        is used.

        Args:
            project_name: Name for the new project directory. Can be:
                - A project name: Creates new directory with this name
                - '.': Initializes in current directory (same as --here)
                - None: Must use --here flag for current directory
            ai_assistant: AI assistant identifier to use for the project. Must be one
                of the keys in AGENT_CONFIG (claude, copilot, gemini, cursor, codex,
                qwen, opencode, windsurf, kilocode, auggie, roo, codebuddy, q, amp).
                If not provided, an interactive selection menu will be displayed.
            script_type: Script type for agent commands and utilities:
                - 'sh': POSIX shell scripts (bash/zsh) for Unix-like systems
                - 'ps': PowerShell scripts for Windows
                If not provided, defaults to 'ps' on Windows and 'sh' elsewhere,
                with interactive confirmation if stdin is a TTY.
            ignore_agent_tools: If True, skips validation that required AI agent
                CLI tools are installed. Useful for setting up projects on systems
                where the agent will be installed later, or for IDE-only agents.
            no_git: If True, skips git repository initialization entirely. Use this
                if you want to add git manually later, or if the directory is already
                in a git repository.
            here: If True, initializes the project in the current directory instead
                of creating a new subdirectory. Template files will be merged with
                existing content. Mutually exclusive with providing a project_name.
            force: If True, skips confirmation prompt when initializing in a non-empty
                current directory. Use with caution as it may overwrite existing files.
            skip_tls: If True, disables SSL/TLS verification for HTTPS requests.
                Not recommended except for troubleshooting network issues or working
                behind corporate proxies that intercept SSL.
            debug: If True, displays verbose diagnostic information including Python
                version, platform, and current working directory when errors occur.
                Useful for troubleshooting network or filesystem issues.
            github_token: GitHub personal access token for API requests. Increases
                rate limit from 60/hour (anonymous) to 5,000/hour (authenticated).
                Can also be set via GH_TOKEN or GITHUB_TOKEN environment variables.

        Raises:
            typer.Exit: Exits with code 1 in the following scenarios:
                - Both project_name and --here flag are specified
                - Neither project_name nor --here flag is specified
                - Invalid AI assistant name provided
                - Invalid script type provided
                - Required AI agent CLI tool not found (unless --ignore-agent-tools)
                - Target directory already exists (when creating new directory)
                - User cancels confirmation prompt (when initializing in non-empty directory)
                - Network errors during template download
                - File system errors during extraction
                - ZIP file corruption or security issues
                - Git initialization fails (warning only, does not stop initialization)

        Examples:
            Create a new project with interactive assistant selection:
                $ nuaa init my-harm-reduction-project

            Create project with Claude Code and default script type:
                $ nuaa init peer-support-network --ai claude

            Create project with GitHub Copilot and PowerShell scripts:
                $ nuaa init naloxone-program --ai copilot --script ps

            Initialize in current directory with confirmation:
                $ nuaa init .
                $ nuaa init --here

            Force initialize in non-empty current directory:
                $ nuaa init --here --force

            Create project without git, using Cursor IDE:
                $ nuaa init community-engagement --ai cursor-agent --no-git

            Create project skipping agent tool validation:
                $ nuaa init training-program --ai gemini --ignore-agent-tools

            Initialize with debug output and custom GitHub token:
                $ nuaa init my-project --debug --github-token ghp_xxxxxxxxxxxx

            Initialize behind corporate proxy (skip TLS verification):
                $ nuaa init my-project --skip-tls

        Notes:
            - Template is downloaded from the latest GitHub release of zophiezlan/nuaa-cli
            - Git initialization is automatic unless --no-git is specified or git is not installed
            - Agent folder (e.g., .claude/commands/) may contain credentials - add to .gitignore
            - Some AI assistants require CLI installation (checked unless --ignore-agent-tools)
            - VSCode settings.json is intelligently merged if it already exists
            - Script files are made executable on Unix-like systems (no-op on Windows)
            - Codex assistant requires CODEX_HOME environment variable to be set

        See Also:
            - nuaa check: Verify all required tools are installed
            - nuaa design: Create program designs after initialization
            - nuaa --help: View all available commands
        """
        if show_banner_fn:
            show_banner_fn()

        # Handle '.' shorthand for current directory
        if project_name == ".":
            here = True
            project_name = None  # Clear project_name to use existing validation logic

        # Validate project name and --here flag are mutually exclusive
        if here and project_name:
            console.print("[red]Error:[/red] Cannot specify both project name and --here flag")
            raise typer.Exit(1)

        # Ensure either project name or --here is provided
        if not here and not project_name:
            console.print(
                "[red]Error:[/red] Must specify either a project name, use '.' for current directory, or use --here flag"
            )
            raise typer.Exit(1)

        # Determine project path and handle current directory initialization
        if here:
            project_name = Path.cwd().name
            project_path = Path.cwd()

            # Check if current directory is not empty and handle confirmation
            existing_items = list(project_path.iterdir())
            if existing_items:
                console.print(
                    f"[yellow]Warning:[/yellow] Current directory is not empty ({len(existing_items)} items)"
                )
                console.print(
                    "[yellow]Template files will be merged with existing content and may overwrite existing files[/yellow]"
                )
                if force:
                    console.print(
                        "[cyan]--force supplied: skipping confirmation and proceeding with merge[/cyan]"
                    )
                else:
                    response = typer.confirm("Do you want to continue?")
                    if not response:
                        console.print("[yellow]Operation cancelled[/yellow]")
                        raise typer.Exit(0)
        else:
            assert project_name is not None  # for type checkers
            project_path = Path(project_name).resolve()

            # Ensure target directory doesn't already exist
            if project_path.exists():
                error_panel = Panel(
                    f"Directory '[cyan]{project_name}[/cyan]' already exists\n"
                    "Please choose a different project name or remove the existing directory.",
                    title="[red]Directory Conflict[/red]",
                    border_style="red",
                    padding=(1, 2),
                )
                console.print()
                console.print(error_panel)
                raise typer.Exit(1)

        # Display project setup information
        current_dir = Path.cwd()
        setup_lines = [
            "[cyan]Specify Project Setup[/cyan]",
            "",
            f"{'Project':<15} [green]{project_path.name}[/green]",
            f"{'Working Path':<15} [dim]{current_dir}[/dim]",
        ]

        if not here:
            setup_lines.append(f"{'Target Path':<15} [dim]{project_path}[/dim]")

        console.print(Panel("\n".join(setup_lines), border_style="cyan", padding=(1, 2)))

        # Check git availability
        should_init_git = False
        if not no_git:
            should_init_git = check_tool("git")
            if not should_init_git:
                console.print(
                    "[yellow]Git not found - will skip repository initialization[/yellow]"
                )

        # AI assistant selection (interactive or from command line)
        if ai_assistant:
            if ai_assistant not in AGENT_CONFIG:
                console.print(
                    f"[red]Error:[/red] Invalid AI assistant '{ai_assistant}'. "
                    f"Choose from: {', '.join(AGENT_CONFIG.keys())}"
                )
                raise typer.Exit(1)
            selected_ai = ai_assistant
        else:
            # Create options dict for selection (agent_key: display_name)
            ai_choices = {key: config["name"] for key, config in AGENT_CONFIG.items()}
            selected_ai = select_with_arrows(ai_choices, "Choose your AI assistant:", "copilot")

        # Validate required AI agent tools are installed
        if not ignore_agent_tools:
            agent_config = AGENT_CONFIG.get(selected_ai)
            if agent_config and agent_config["requires_cli"]:
                install_url = agent_config["install_url"]
                if not check_tool(selected_ai):
                    error_panel = Panel(
                        f"[cyan]{selected_ai}[/cyan] not found\n"
                        f"Install from: [cyan]{install_url}[/cyan]\n"
                        f"{agent_config['name']} is required to continue with this project type.\n\n"
                        "Tip: Use [cyan]--ignore-agent-tools[/cyan] to skip this check",
                        title="[red]Agent Detection Error[/red]",
                        border_style="red",
                        padding=(1, 2),
                    )
                    console.print()
                    console.print(error_panel)
                    raise typer.Exit(1)

        # Script type selection (interactive or from command line)
        if script_type:
            if script_type not in SCRIPT_TYPE_CHOICES:
                console.print(
                    f"[red]Error:[/red] Invalid script type '{script_type}'. "
                    f"Choose from: {', '.join(SCRIPT_TYPE_CHOICES.keys())}"
                )
                raise typer.Exit(1)
            selected_script = script_type
        else:
            # Default based on operating system
            default_script = "ps" if os.name == "nt" else "sh"

            # Interactive selection if stdin is a TTY
            if sys.stdin.isatty():
                selected_script = select_with_arrows(
                    SCRIPT_TYPE_CHOICES,
                    "Choose script type (or press Enter)",
                    default_script,
                )
            else:
                selected_script = default_script

        console.print(f"[cyan]Selected AI assistant:[/cyan] {selected_ai}")
        console.print(f"[cyan]Selected script type:[/cyan] {selected_script}")

        # Initialize step tracker for progress display
        tracker = StepTracker("Initialize NUAA Project")

        # Set tracker active flag (for other modules that check this)
        sys._specify_tracker_active = True  # type: ignore[attr-defined]

        # Add all steps to tracker
        tracker.add("precheck", "Check required tools")
        tracker.complete("precheck", "ok")
        tracker.add("ai-select", "Select AI assistant")
        tracker.complete("ai-select", f"{selected_ai}")
        tracker.add("script-select", "Select script type")
        tracker.complete("script-select", selected_script)

        for key, label in [
            ("fetch", "Fetch latest release"),
            ("download", "Download template"),
            ("extract", "Extract template"),
            ("zip-list", "Archive contents"),
            ("extracted-summary", "Extraction summary"),
            ("chmod", "Ensure scripts executable"),
            ("cleanup", "Cleanup"),
            ("git", "Initialize git repository"),
            ("final", "Finalize"),
        ]:
            tracker.add(key, label)

        # Track git error message outside Live context so it persists
        git_error_message = None

        # Execute main initialization workflow with live progress display
        with Live(tracker.render(), console=console, refresh_per_second=8, transient=True) as live:
            tracker.attach_refresh(lambda: live.update(tracker.render()))

            try:
                # Configure SSL verification
                verify = not skip_tls
                local_ssl_context = ssl_context if verify else False

                # Download and extract template
                with httpx.Client(verify=local_ssl_context) as local_client:
                    download_and_extract_template(
                        project_path,
                        selected_ai,
                        selected_script,
                        here,
                        verbose=False,
                        tracker=tracker,
                        client=local_client,
                        debug=debug,
                        github_token=github_token,
                    )

                # Ensure shell scripts are executable
                ensure_executable_scripts(project_path, tracker=tracker)

                # Initialize git repository if requested
                if not no_git:
                    tracker.start("git")
                    if is_git_repo(project_path):
                        tracker.complete("git", "existing repo detected")
                    elif should_init_git:
                        success, error_msg = init_git_repo(project_path, quiet=True)
                        if success:
                            tracker.complete("git", "initialized")
                        else:
                            tracker.error("git", "init failed")
                            git_error_message = error_msg
                    else:
                        tracker.skip("git", "git not available")
                else:
                    tracker.skip("git", "--no-git flag")

                tracker.complete("final", "project ready")

            except (httpx.TimeoutException, httpx.ConnectError, httpx.HTTPError) as e:
                if debug:
                    display_debug_environment(console)
                cleanup_path = project_path if not here else None
                handle_network_error(e, "initialization", console, cleanup_path, tracker, debug)

            except (zipfile.BadZipFile, PermissionError, OSError) as e:
                tracker.error("final", f"File system error: {e}")
                console.print(
                    Panel(
                        f"File system error during initialization: {e}",
                        title="Failure",
                        border_style="red",
                    )
                )
                if debug:
                    display_debug_environment(console)
                # Clean up partial directory if not current directory
                if not here and project_path.exists():
                    shutil.rmtree(project_path)
                raise typer.Exit(1)

            except RuntimeError as e:
                tracker.error("final", str(e))
                console.print(
                    Panel(f"Initialization failed: {e}", title="Failure", border_style="red")
                )
                if debug:
                    display_debug_environment(console)
                # Clean up partial directory if not current directory
                if not here and project_path.exists():
                    shutil.rmtree(project_path)
                raise typer.Exit(1)

        # Display final tracker state
        console.print(tracker.render())
        console.print("\n[bold green]NUAA project workspace ready.[/bold green]")

        # Show git error details if initialization failed
        if git_error_message:
            console.print()
            git_error_panel = Panel(
                f"[yellow]Warning:[/yellow] Git repository initialization failed\n\n"
                f"{git_error_message}\n\n"
                f"[dim]You can initialize git manually later with:[/dim]\n"
                f"[cyan]cd {project_path if not here else '.'}[/cyan]\n"
                f"[cyan]git init[/cyan]\n"
                f"[cyan]git add .[/cyan]\n"
                f'[cyan]git commit -m "Initial commit"[/cyan]',
                title="[red]Git Initialization Failed[/red]",
                border_style="red",
                padding=(1, 2),
            )
            console.print(git_error_panel)

        # Display agent folder security notice
        agent_config = AGENT_CONFIG.get(selected_ai)
        if agent_config:
            agent_folder = agent_config["folder"]
            security_notice = Panel(
                f"Some agents may store credentials, auth tokens, or other identifying and private artifacts in the agent folder within your project.\n"
                f"Consider adding [cyan]{agent_folder}[/cyan] (or parts of it) to [cyan].gitignore[/cyan] to prevent accidental credential leakage.",
                title="[yellow]Agent Folder Security[/yellow]",
                border_style="yellow",
                padding=(1, 2),
            )
            console.print()
            console.print(security_notice)

        # Build next steps instructions
        steps_lines = []
        if not here:
            steps_lines.append(f"1. Go to the project folder: [cyan]cd {project_name}[/cyan]")
            step_num = 2
        else:
            steps_lines.append("1. You're already in the project directory!")
            step_num = 2

        # Add Codex-specific setup step if needed
        if selected_ai == "codex":
            codex_path = project_path / ".codex"
            quoted_path = shlex.quote(str(codex_path))
            if os.name == "nt":  # Windows
                cmd = f"setx CODEX_HOME {quoted_path}"
            else:  # Unix-like systems
                cmd = f"export CODEX_HOME={quoted_path}"

            steps_lines.append(
                f"{step_num}. Set [cyan]CODEX_HOME[/cyan] environment variable before running Codex: [cyan]{cmd}[/cyan]"
            )
            step_num += 1

        steps_lines.append(f"{step_num}. Start using slash commands with your AI agent:")

        steps_lines.append("   [bold]Core Program Commands:[/bold]")
        steps_lines.append("   • [cyan]/nuaa.design[/] - Create program designs with logic models")
        steps_lines.append("   • [cyan]/nuaa.propose[/] - Generate funding proposals")
        steps_lines.append("   • [cyan]/nuaa.measure[/] - Define impact measurement frameworks")
        steps_lines.append("   • [cyan]/nuaa.document[/] - Document existing programs")
        steps_lines.append("")
        steps_lines.append("   [bold]Planning & Management:[/bold]")
        steps_lines.append("   • [cyan]/nuaa.engage[/] - Create stakeholder engagement plans")
        steps_lines.append("   • [cyan]/nuaa.partner[/] - Generate partnership agreements (MOUs)")
        steps_lines.append("   • [cyan]/nuaa.risk[/] - Build comprehensive risk registers")
        steps_lines.append("")
        steps_lines.append("   [bold]Events & Training:[/bold]")
        steps_lines.append("   • [cyan]/nuaa.event[/] - Plan workshops, forums, and events")
        steps_lines.append("   • [cyan]/nuaa.train[/] - Design training curricula for peer workers")
        steps_lines.append("")
        steps_lines.append("   [bold]Refinement:[/bold]")
        steps_lines.append("   • [cyan]/nuaa.refine[/] - Refine and improve outputs")
        steps_lines.append("   • [cyan]/nuaa.report[/] - Generate reports and presentations")

        steps_panel = Panel(
            "\n".join(steps_lines),
            title="Next Steps",
            border_style="cyan",
            padding=(1, 2),
        )
        console.print()
        console.print(steps_panel)

        # Display template suite information
        enhancement_lines = [
            "You now have access to [bold]19 comprehensive templates[/bold] covering:",
            "",
            "✓ Program Design (design, logic models, impact frameworks)",
            "✓ Funding & Proposals (proposals, budgets)",
            "✓ Stakeholder Management (engagement plans, partnerships, community strategy)",
            "✓ Planning & Operations (risk registers, communication plans, monitoring)",
            "✓ Events & Training (event planning, training curricula)",
            "✓ Ethics & HR (ethics applications, job descriptions, volunteer programs)",
            "",
            "Run [cyan]nuaa --help[/cyan] to see all available commands.",
        ]
        enhancements_panel = Panel(
            "\n".join(enhancement_lines),
            title="Template Suite Available",
            border_style="cyan",
            padding=(1, 2),
        )
        console.print()
        console.print(enhancements_panel)
