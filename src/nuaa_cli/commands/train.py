from datetime import datetime
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from ..scaffold import (
    _next_feature_dir,
    _slugify,
    _load_template,
    _apply_replacements,
    _prepend_metadata,
    write_markdown_if_needed,
)


def register(app, show_banner_fn=None, console: Console | None = None):
    console = console or Console()

    @app.command()
    def train(
        training_name: str = typer.Argument(
            ..., help="Training program name (e.g., 'Peer Worker Training')"
        ),
        target_audience: str = typer.Argument(
            ..., help="Target audience (e.g., 'Peer Workers', 'Volunteers')"
        ),
        duration: str = typer.Argument(
            ..., help="Training duration (e.g., '2 days', '8 weeks')"
        ),
        feature: Optional[str] = typer.Option(
            None, help="Override feature slug (e.g., '001-custom-slug')"
        ),
        force: bool = typer.Option(False, help="Overwrite existing files if present"),
    ):
        """Create a training curriculum for peer workers, volunteers, or staff."""
        if show_banner_fn:
            show_banner_fn()

        # Determine feature directory
        if feature:
            slug = _slugify(feature)
            feature_dir, num_str, _ = _next_feature_dir(slug)
        else:
            feature_dir, num_str, slug = _next_feature_dir(training_name)

        created = datetime.now().strftime("%Y-%m-%d")
        mapping = {
            "TRAINING_NAME": training_name,
            "TARGET_AUDIENCE": target_audience,
            "DURATION": duration,
            "DATE": created,
            "FEATURE_ID": num_str,
            "SLUG": slug,
        }

        # training-curriculum.md
        try:
            template = _load_template("training-curriculum.md")
            filled = _apply_replacements(template, mapping)
            meta = {
                "title": f"{training_name} - Training Curriculum",
                "created": created,
                "feature": f"{num_str}-{slug}",
                "status": "draft",
                "audience": target_audience,
            }
            text = _prepend_metadata(filled, meta)
            dest = feature_dir / "training-curriculum.md"
            write_markdown_if_needed(dest, text, force=force, console=console)

            console.print(
                Panel(
                    f"Training curriculum created: [cyan]{dest}[/cyan]\n\n"
                    f"This curriculum includes:\n"
                    f"  • Training overview and learning objectives\n"
                    f"  • Detailed training schedule\n"
                    f"  • 8+ training modules with activities\n"
                    f"  • Facilitation guidance and tips\n"
                    f"  • Training materials list\n"
                    f"  • Participant support and assessment\n\n"
                    f"Next steps:\n"
                    f"  1. Customize modules for {target_audience}\n"
                    f"  2. Develop activities and handouts\n"
                    f"  3. Schedule and promote training",
                    title="Training Curriculum Ready",
                    border_style="green",
                )
            )
        except Exception as e:
            console.print(f"[red]Failed to create training-curriculum.md:[/red] {e}")
            raise typer.Exit(1)
