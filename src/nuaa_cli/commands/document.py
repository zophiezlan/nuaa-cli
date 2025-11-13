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
    def document(
        program_name: str = typer.Argument(..., help="Existing program identifier/name"),
        force: bool = typer.Option(False, help="Overwrite if exists"),
    ):
        """Create an existing program analysis document."""
        if show_banner_fn:
            show_banner_fn()
        feature_dir = get_or_create_feature_dir(program_name)
        mapping = {
            "PROGRAM_NAME": program_name,
            "DATE": datetime.now().strftime("%Y-%m-%d"),
        }
        try:
            template = _load_template("existing-program-analysis.md")
            text = _prepend_metadata(
                _apply_replacements(template, mapping),
                {"title": f"{program_name} - Existing Program Analysis"},
            )
            dest = feature_dir / "existing-program-analysis.md"
            write_markdown_if_needed(dest, text, force=force, console=console)
        except Exception as e:
            console.print(f"[red]Failed to create existing-program-analysis.md:[/red] {e}")
            raise typer.Exit(1)
