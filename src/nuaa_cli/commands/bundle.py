#!/usr/bin/env python3
"""
Bundle Command - Package Agent Configurations
==============================================

Creates distributable packages of NUAA agent configurations, templates,
and metadata. Useful for sharing agent bundles, creating marketplace
artifacts, or versioning agent setups.

Example:
    $ nuaa bundle my-agent-pack --output ./dist
    $ nuaa bundle custom-templates --include-mcp
"""

import json
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn


def register(app, show_banner_fn=None, console: Console | None = None):
    """Register the bundle command with the Typer app."""
    console = console or Console()

    @app.command()
    def bundle(
        name: str = typer.Argument(..., help="Bundle name"),
        output: str = typer.Option("./dist", "--output", "-o", help="Output directory for bundle"),
        include_mcp: bool = typer.Option(False, "--include-mcp", help="Include MCP configuration"),
        include_templates: bool = typer.Option(
            True, "--include-templates", help="Include project templates"
        ),
        include_a2a: bool = typer.Option(
            True, "--include-a2a", help="Include Agent-to-Agent configuration"
        ),
        agent: Optional[str] = typer.Option(
            None, "--agent", "-a", help="Specific agent to bundle (e.g., 'claude', 'copilot')"
        ),
        version: str = typer.Option("1.0.0", "--version", "-v", help="Bundle version"),
        description: Optional[str] = typer.Option(
            None, "--description", "-d", help="Bundle description"
        ),
        author: Optional[str] = typer.Option(None, "--author", help="Bundle author name"),
        license: str = typer.Option("MIT", "--license", help="Bundle license"),
        marketplace: bool = typer.Option(
            False, "--marketplace", help="Prepare bundle for marketplace distribution"
        ),
        dependencies: Optional[str] = typer.Option(
            None, "--dependencies", help="Additional dependencies (comma-separated)"
        ),
    ):
        """
        Package agent configurations and templates into a distributable bundle.

        Creates a ZIP archive containing:
        - Agent command files (.claude/, .github/agents/, etc.)
        - Templates (if --include-templates)
        - MCP configuration (if --include-mcp)
        - A2A configuration (if --include-a2a)
        - Manifest with metadata

        The bundle can be shared with others, uploaded to marketplaces,
        or used for version control of agent setups.

        Args:
            name: Bundle name (will be used for filename)
            output: Output directory (default: ./dist)
            include_mcp: Include MCP registry configuration
            include_templates: Include NUAA templates
            include_a2a: Include Agent-to-Agent configuration
            agent: Specific agent to bundle (if None, bundles all)
            version: Bundle version string
            description: Optional bundle description
            author: Bundle author name
            license: Bundle license (default: MIT)
            marketplace: Prepare bundle for marketplace distribution
            dependencies: Additional dependencies (comma-separated)

        Examples:
            Create a basic bundle:
                $ nuaa bundle my-agent-pack

            Bundle only Claude Code configuration:
                $ nuaa bundle claude-only --agent claude

            Create bundle with MCP support:
                $ nuaa bundle mcp-enabled --include-mcp

            Bundle for distribution:
                $ nuaa bundle nuaa-complete --version 2.0.0 --description "Complete NUAA setup" --author "Your Name"
        """
        if show_banner_fn:
            show_banner_fn()

        console.print(f"[bold]Creating bundle:[/bold] {name}")
        console.print()

        # Validate inputs
        output_dir = Path(output)
        output_dir.mkdir(parents=True, exist_ok=True)

        bundle_filename = f"{name}-{version}.zip"
        bundle_path = output_dir / bundle_filename

        # Check if bundle already exists
        if bundle_path.exists():
            overwrite = typer.confirm(
                f"Bundle '{bundle_filename}' already exists. Overwrite?",
                default=False,
            )
            if not overwrite:
                console.print("[yellow]Bundle creation cancelled.[/yellow]")
                raise typer.Exit(0)

        # Create temporary working directory
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            work_dir = Path(tmpdir) / name

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:
                # Task 1: Collect agent files
                task1 = progress.add_task("Collecting agent files...", total=None)
                _collect_agent_files(work_dir, agent, console)
                progress.update(task1, completed=True)

                # Task 2: Collect templates
                if include_templates:
                    task2 = progress.add_task("Including templates...", total=None)
                    _collect_templates(work_dir, console)
                    progress.update(task2, completed=True)

                # Task 3: Include MCP config
                if include_mcp:
                    task3 = progress.add_task("Including MCP configuration...", total=None)
                    _create_mcp_config(work_dir, console)
                    progress.update(task3, completed=True)

                # Task 3.5: Include A2A config
                if include_a2a:
                    task3_5 = progress.add_task("Including A2A configuration...", total=None)
                    _create_a2a_config(work_dir, console)
                    progress.update(task3_5, completed=True)

                # Task 4: Create manifest
                task4 = progress.add_task("Creating manifest...", total=None)
                _create_manifest(
                    work_dir,
                    name,
                    version,
                    description,
                    agent,
                    include_mcp,
                    include_a2a,
                    author,
                    license,
                    marketplace,
                    dependencies,
                    console,
                )
                progress.update(task4, completed=True)

                # Task 5: Package bundle
                task5 = progress.add_task("Packaging bundle...", total=None)
                _create_zip(work_dir, bundle_path, console)
                progress.update(task5, completed=True)

        # Success message
        console.print()
        console.print(
            Panel(
                f"Bundle created successfully!\n\n"
                f"[cyan]Location:[/cyan] {bundle_path}\n"
                f"[cyan]Size:[/cyan] {_format_size(bundle_path.stat().st_size)}\n"
                f"[cyan]Version:[/cyan] {version}",
                title="✅ Bundle Ready",
                border_style="green",
            )
        )
        console.print()
        console.print("[dim]Share this bundle with others or upload to a marketplace.[/dim]")


def _collect_agent_files(work_dir: Path, agent: Optional[str], console: Console) -> None:
    """Collect agent command files from the project."""
    # Load agent config
    import json
    from pathlib import Path as _Path

    agents_json_path = _Path(__file__).parent.parent / "agents.json"
    with open(agents_json_path, "r") as f:
        AGENT_CONFIG = json.load(f)

    agents_to_collect = [agent] if agent else list(AGENT_CONFIG.keys())

    for agent_name in agents_to_collect:
        if agent_name not in AGENT_CONFIG:
            console.print(f"[yellow]Warning:[/yellow] Unknown agent '{agent_name}', skipping")
            continue

        agent_config = AGENT_CONFIG[agent_name]
        agent_folder = Path(agent_config["folder"])

        if agent_folder.exists():
            dest = work_dir / agent_folder
            shutil.copytree(agent_folder, dest, dirs_exist_ok=True)
            console.print(f"  [green]✓[/green] Collected {agent_name} files")
        else:
            console.print(f"  [dim]- {agent_name} not found, skipping[/dim]")


def _collect_templates(work_dir: Path, console: Console) -> None:
    """Collect NUAA templates."""
    templates_src = Path("nuaa-kit/templates")
    if templates_src.exists():
        dest = work_dir / "nuaa-kit" / "templates"
        shutil.copytree(templates_src, dest, dirs_exist_ok=True)
        console.print("  [green]✓[/green] Included templates")
    else:
        console.print("  [yellow]Warning:[/yellow] Templates not found")


def _create_mcp_config(work_dir: Path, console: Console) -> None:
    """Create MCP configuration file."""
    mcp_config = {
        "version": "1.0",
        "protocol": "mcp",
        "tools": [],
        "servers": [],
    }

    mcp_file = work_dir / "mcp.json"
    mcp_file.write_text(json.dumps(mcp_config, indent=2))
    console.print("  [green]✓[/green] Created MCP configuration")


def _create_a2a_config(work_dir: Path, console: Console) -> None:
    """Create A2A coordinator configuration file."""
    a2a_config = {
        "version": "1.0",
        "protocol": "a2a",
        "agents": [],
        "coordinator": {"max_history": 100, "timeout": 30},
        "capabilities": [],
    }

    a2a_file = work_dir / "a2a.json"
    a2a_file.write_text(json.dumps(a2a_config, indent=2))
    console.print("  [green]✓[/green] Created A2A configuration")


def _create_manifest(
    work_dir: Path,
    name: str,
    version: str,
    description: Optional[str],
    agent: Optional[str],
    include_mcp: bool,
    include_a2a: bool,
    author: Optional[str],
    license: str,
    marketplace: bool,
    dependencies: Optional[str],
    console: Console,
) -> None:
    """Create bundle manifest file with enhanced metadata."""
    manifest: dict[str, Any] = {
        "name": name,
        "version": version,
        "description": description or f"{name} agent bundle",
        "created": datetime.now().isoformat(),
        "agents": [agent] if agent else "all",
        "includes_mcp": include_mcp,
        "includes_a2a": include_a2a,
        "includes_templates": True,
        "nuaa_cli_version": "0.4.0",
        "author": author,
        "license": license,
    }

    # Add dependencies
    if dependencies:
        manifest["dependencies"] = [dep.strip() for dep in dependencies.split(",")]
    else:
        manifest["dependencies"] = []

    # Add marketplace metadata if requested
    if marketplace:
        manifest["marketplace"] = {
            "category": "agent-bundles",
            "tags": ["nuaa", "harm-reduction", "agent-kit"],
            "compatible_with": ["nuaa-cli>=0.4.0"],
            "support_url": None,
            "homepage": None,
            "repository": None,
        }

    manifest_file = work_dir / "manifest.json"
    manifest_file.write_text(json.dumps(manifest, indent=2))
    console.print("  [green]✓[/green] Created manifest")


def _create_zip(source_dir: Path, output_path: Path, console: Console) -> None:
    """Create ZIP archive of the bundle."""
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in source_dir.rglob("*"):
            if file.is_file():
                arcname = file.relative_to(source_dir)
                zipf.write(file, arcname)
    console.print("  [green]✓[/green] Created archive")


def _format_size(bytes: int) -> str:
    """Format file size in human-readable format."""
    size = float(bytes)
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"
