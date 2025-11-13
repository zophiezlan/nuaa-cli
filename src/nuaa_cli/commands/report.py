from datetime import datetime

import typer
from rich.console import Console

from ..scaffold import (
    get_or_create_feature_dir,
    write_markdown_if_needed,
)


def register(app, show_banner_fn=None, console: Console | None = None):
    console = console or Console()

    @app.command()
    def report(
        program_name: str = typer.Argument(..., help="Program name (existing)"),
        report_type: str = typer.Option(
            "final",
            "--type",
            help="Report type: progress|mid-program|final|quarterly|annual",
        ),
        force: bool = typer.Option(False, help="Overwrite if exists"),
    ):
        """Generate a simple report scaffold referencing program artifacts."""
        if show_banner_fn:
            show_banner_fn()
        feature_dir = get_or_create_feature_dir(program_name)
        created = datetime.now().strftime("%Y-%m-%d")
        lines = [
            f"# {program_name} - {report_type.title()} Report",
            "",
            f"Generated: {created}",
            "",
            "This is a scaffold report. Populate the sections based on your "
            "impact framework and collected data.",
            "",
            "## Overview",
            "",
            "## Key Findings",
            "",
            "## Progress Against Logic Model",
            "",
            "## Equity Analysis",
            "",
            "## Budget vs Actuals",
            "",
            "## Lessons Learned and Recommendations",
            "",
        ]
        content = "\n".join(lines) + "\n"
        dest = feature_dir / "report.md"
        write_markdown_if_needed(dest, content, force=force, console=console)
