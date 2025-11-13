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
    def propose(
        program_name: str = typer.Argument(..., help="Program name (existing or new)"),
        funder: str = typer.Argument(..., help="Funder name"),
        amount: str = typer.Argument(..., help="Amount requested, e.g., $50000"),
        duration: str = typer.Argument(..., help="Duration e.g., '12 months'"),
        force: bool = typer.Option(False, help="Overwrite if proposal.md exists"),
    ):
        """Create a funding proposal from the template, linked to design."""
        if show_banner_fn:
            show_banner_fn()
        feature_dir = get_or_create_feature_dir(program_name)
        created = datetime.now().strftime("%Y-%m-%d")
        mapping = {
            "PROGRAM_NAME": program_name,
            "FUNDER": funder,
            "AMOUNT": amount,
            "DURATION": duration,
            "DATE": created,
        }
        try:
            template = _load_template("proposal.md")
            filled = _apply_replacements(template, mapping)
            meta = {
                "title": f"{program_name} - Proposal",
                "funder": funder,
                "amount": amount,
                "created": created,
            }
            text = _prepend_metadata(filled, meta)
            dest = feature_dir / "proposal.md"
            write_markdown_if_needed(dest, text, force=force, console=console)
        except Exception as e:
            console.print(f"[red]Failed to create proposal.md:[/red] {e}")
            raise typer.Exit(1)
