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
    def engage(
        program_name: str = typer.Argument(
            ..., help="Program name (used to derive feature folder)"
        ),
        target_population: str = typer.Argument(
            ..., help="Target population description"
        ),
        duration: str = typer.Argument(..., help="Planning period (e.g., '12 months')"),
        feature: Optional[str] = typer.Option(
            None, help="Override feature slug (e.g., '001-custom-slug')"
        ),
        force: bool = typer.Option(False, help="Overwrite existing files if present"),
    ):
        """Create a stakeholder engagement plan for a NUAA program."""
        if show_banner_fn:
            show_banner_fn()

        # Determine feature directory
        if feature:
            slug = _slugify(feature)
            feature_dir, num_str, _ = _next_feature_dir(slug)
        else:
            feature_dir, num_str, slug = _next_feature_dir(program_name)

        created = datetime.now().strftime("%Y-%m-%d")
        mapping = {
            "PROGRAM_NAME": program_name,
            "TARGET_POPULATION": target_population,
            "DURATION": duration,
            "DATE": created,
            "FEATURE_ID": num_str,
            "SLUG": slug,
        }

        # stakeholder-engagement-plan.md
        try:
            template = _load_template("stakeholder-engagement-plan.md")
            filled = _apply_replacements(template, mapping)
            meta = {
                "title": f"{program_name} - Stakeholder Engagement Plan",
                "created": created,
                "feature": f"{num_str}-{slug}",
                "status": "draft",
            }
            text = _prepend_metadata(filled, meta)
            dest = feature_dir / "stakeholder-engagement-plan.md"
            write_markdown_if_needed(dest, text, force=force, console=console)

            console.print(
                Panel(
                    f"Stakeholder engagement plan created: [cyan]{dest}[/cyan]\n\n"
                    f"This plan provides:\n"
                    f"  • Stakeholder mapping and analysis\n"
                    f"  • Engagement strategies for each stakeholder group\n"
                    f"  • Communication channels and timeline\n"
                    f"  • Cultural safety considerations\n\n"
                    f"Next steps:\n"
                    f"  1. Review and customize stakeholder groups\n"
                    f"  2. Set engagement priorities and activities\n"
                    f"  3. Develop communication materials",
                    title="Engagement Plan Ready",
                    border_style="green",
                )
            )
        except Exception as e:
            console.print(
                f"[red]Failed to create stakeholder-engagement-plan.md:[/red] {e}"
            )
            raise typer.Exit(1)
