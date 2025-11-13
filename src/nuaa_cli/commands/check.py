from typing import Dict
from rich.console import Console

from ..utils import StepTracker, check_tool


def register(
    app,
    agent_config: Dict,
    show_banner_fn=None,
    console: Console | None = None,
):
    console = console or Console()

    @app.command()
    def check():
        """Check that all required tools are installed."""
        if show_banner_fn:
            show_banner_fn()
        console.print("[bold]Checking for installed tools...[/bold]\n")

        tracker = StepTracker("Check Available Tools")

        tracker.add("git", "Git version control")
        git_ok = check_tool("git", tracker=tracker)

        cli_agent_results: dict[str, bool] = {}
        has_ide_agent = False
        for agent_key, cfg in agent_config.items():
            agent_name = cfg["name"]
            requires_cli = cfg["requires_cli"]

            tracker.add(agent_key, agent_name)

            if requires_cli:
                cli_agent_results[agent_key] = check_tool(agent_key, tracker=tracker)
            else:
                tracker.skip(agent_key, "IDE-based, no CLI check")
                has_ide_agent = True

        tracker.add("code", "Visual Studio Code")
        check_tool("code", tracker=tracker)

        tracker.add("code-insiders", "Visual Studio Code Insiders")
        check_tool("code-insiders", tracker=tracker)

        console.print(tracker.render())

        console.print("\n[bold green]NUAA CLI is ready to use![/bold green]")

        if not git_ok:
            console.print("[dim]Tip: Install git for repository management[/dim]")

        if not any(cli_agent_results.values()):
            if has_ide_agent:
                console.print(
                    "[dim]Tip: Install a CLI-based AI assistant if you need "
                    "standalone workflows; IDE assistants are already "
                    "supported.[/dim]"
                )
            else:
                console.print("[dim]Tip: Install an AI assistant for the best experience[/dim]")
