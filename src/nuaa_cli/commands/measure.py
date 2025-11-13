from datetime import datetime

import typer
from rich.console import Console

from ..scaffold import (
    get_or_create_feature_dir,
    _load_template,
    _apply_replacements,
    _prepend_metadata,
    write_markdown_if_needed,
)


def register(app, show_banner_fn=None, console: Console | None = None):
    console = console or Console()

    @app.command()
    def measure(
        program_name: str = typer.Argument(..., help="Program name (existing)"),
        evaluation_period: str = typer.Argument(..., help="Evaluation period"),
        budget: str = typer.Argument(..., help="Evaluation budget (e.g., $7000)"),
        force: bool = typer.Option(False, help="Overwrite if exists"),
    ):
        """Create or update the impact framework document from the template."""
        if show_banner_fn:
            show_banner_fn()
        feature_dir = get_or_create_feature_dir(program_name)
        mapping = {
            "PROGRAM_NAME": program_name,
            "EVALUATION_PERIOD": evaluation_period,
            "BUDGET": budget,
            "DATE": datetime.now().strftime("%Y-%m-%d"),
        }
        try:
            template = _load_template("impact-framework.md")
            text = _prepend_metadata(
                _apply_replacements(template, mapping),
                {"title": f"{program_name} - Impact Framework"},
            )
            dest = feature_dir / "impact-framework.md"
            write_markdown_if_needed(dest, text, force=force, console=console)
        except Exception as e:
            console.print(f"[red]Failed to create impact-framework.md:[/red] {e}")
            raise typer.Exit(1)
