"""
Banner display for NUAA CLI.

This module provides the ASCII art banner and display functions
for the NUAA Project Kit CLI interface.
"""

import typer
from rich.align import Align
from rich.console import Console
from rich.text import Text
from typer.core import TyperGroup


BANNER = """
███╗   ██╗██╗   ██╗ █████╗  █████╗
████╗  ██║██║   ██║██╔══██╗██╔══██╗
██╔██╗ ██║██║   ██║███████║███████║
██║╚██╗██║██║   ██║██╔══██║██╔══██║
██║ ╚████║╚██████╔╝██║  ██║██║  ██║
╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
"""

TAGLINE = "NUAA Project - AI-Assisted Project Management for NSW Users and AIDS Association"


def show_banner(console: Console | None = None) -> None:
    """
    Display the ASCII art banner with gradient colors.

    The banner is displayed with alternating colors (blue → cyan → white gradient)
    and centered on the screen, followed by the NUAA tagline.

    Args:
        console: Optional Rich console for output (creates new one if not provided)

    Example:
        >>> show_banner()
        ███╗   ██╗██╗   ██╗ █████╗  █████╗
        ...
        NUAA Project - AI-Assisted Project Management...
    """
    _console = console or Console()

    banner_lines = BANNER.strip().split("\n")
    colors = ["bright_blue", "blue", "cyan", "bright_cyan", "white", "bright_white"]

    styled_banner = Text()
    for i, line in enumerate(banner_lines):
        color = colors[i % len(colors)]
        styled_banner.append(line + "\n", style=color)

    _console.print(Align.center(styled_banner))
    _console.print(Align.center(Text(TAGLINE, style="italic bright_yellow")))
    _console.print()


class BannerGroup(TyperGroup):
    """
    Custom Typer group that shows banner before help.

    This class extends the default TyperGroup to automatically display
    the NUAA banner when the help text is formatted.

    Example:
        >>> app = typer.Typer(cls=BannerGroup)
    """

    def format_help(self, ctx: typer.Context, formatter: typer.core.HelpFormatter) -> None:
        """
        Format help text with banner prepended.

        Args:
            ctx: Typer context
            formatter: Help text formatter
        """
        # Show banner before help
        show_banner()
        super().format_help(ctx, formatter)
