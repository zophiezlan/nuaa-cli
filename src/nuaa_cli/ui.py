"""
Interactive UI utilities for NUAA CLI.

This module provides functions for interactive command-line interfaces
including keyboard input handling and arrow-key selection menus.
"""

import readchar
import typer
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table


def get_key() -> str:
    """
    Get a single keypress in a cross-platform way using readchar.

    Normalizes arrow keys, Enter, Escape, and Ctrl combinations
    to standardized string values.

    Returns:
        Normalized key string:
        - "up": Up arrow or Ctrl+P
        - "down": Down arrow or Ctrl+N
        - "enter": Enter key
        - "escape": Escape key
        - Other keys: returned as-is

    Raises:
        KeyboardInterrupt: When Ctrl+C is pressed

    Example:
        >>> key = get_key()
        >>> if key == "enter":
        ...     print("Enter pressed!")
    """
    key = readchar.readkey()

    if key == readchar.key.UP or key == readchar.key.CTRL_P:
        return "up"
    if key == readchar.key.DOWN or key == readchar.key.CTRL_N:
        return "down"

    if key == readchar.key.ENTER:
        return "enter"

    if key == readchar.key.ESC:
        return "escape"

    if key == readchar.key.CTRL_C:
        raise KeyboardInterrupt

    return key


def select_with_arrows(
    options: dict,
    prompt_text: str = "Select an option",
    default_key: str | None = None,
    console: Console | None = None,
) -> str:
    """
    Interactive selection using arrow keys with Rich Live display.

    Displays a menu of options that can be navigated with arrow keys
    and selected with Enter. Supports Esc to cancel.

    Args:
        options: Dict with keys as option keys and values as descriptions.
                 Example: {"claude": "Claude by Anthropic", "copilot": "GitHub Copilot"}
        prompt_text: Text to show above the options (default: "Select an option")
        default_key: Default option key to start with (default: first option)
        console: Optional Rich console for output

    Returns:
        Selected option key (one of the keys from options dict)

    Raises:
        typer.Exit: When user cancels (Esc) or selection fails

    Controls:
        - ↑/↓ or Ctrl+P/Ctrl+N: Navigate options
        - Enter: Select current option
        - Esc or Ctrl+C: Cancel selection

    Example:
        >>> agents = {"claude": "Claude by Anthropic", "copilot": "GitHub Copilot"}
        >>> selected = select_with_arrows(agents, "Choose an AI agent")
        >>> print(f"You selected: {selected}")
    """
    _console = console or Console()
    option_keys = list(options.keys())

    if default_key and default_key in option_keys:
        selected_index = option_keys.index(default_key)
    else:
        selected_index = 0

    selected_key = None

    def create_selection_panel():
        """Create the selection panel with current selection highlighted."""
        table = Table.grid(padding=(0, 2))
        table.add_column(style="cyan", justify="left", width=3)
        table.add_column(style="white", justify="left")

        for i, key in enumerate(option_keys):
            if i == selected_index:
                table.add_row("▶", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")
            else:
                table.add_row(" ", f"[cyan]{key}[/cyan] [dim]({options[key]})[/dim]")

        table.add_row("", "")
        table.add_row("", "[dim]Use ↑/↓ to navigate, Enter to select, Esc to cancel[/dim]")

        return Panel(
            table,
            title=f"[bold]{prompt_text}[/bold]",
            border_style="cyan",
            padding=(1, 2),
        )

    _console.print()

    def run_selection_loop():
        nonlocal selected_key, selected_index
        with Live(
            create_selection_panel(),
            console=_console,
            transient=True,
            auto_refresh=False,
        ) as live:
            while True:
                try:
                    key = get_key()
                    if key == "up":
                        selected_index = (selected_index - 1) % len(option_keys)
                    elif key == "down":
                        selected_index = (selected_index + 1) % len(option_keys)
                    elif key == "enter":
                        selected_key = option_keys[selected_index]
                        break
                    elif key == "escape":
                        _console.print("\n[yellow]Selection cancelled[/yellow]")
                        raise typer.Exit(1)

                    live.update(create_selection_panel(), refresh=True)

                except KeyboardInterrupt:
                    _console.print("\n[yellow]Selection cancelled[/yellow]")
                    raise typer.Exit(1)

    run_selection_loop()

    if selected_key is None:
        _console.print("\n[red]Selection failed.[/red]")
        raise typer.Exit(1)

    return selected_key
