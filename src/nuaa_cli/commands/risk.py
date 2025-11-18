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
    def risk(
        program_name: str = typer.Argument(
            ..., help="Program name (used to derive feature folder)"
        ),
        duration: str = typer.Argument(..., help="Program duration (e.g., '12 months')"),
        feature: Optional[str] = typer.Option(
            None, help="Override feature slug (e.g., '001-custom-slug')"
        ),
        force: bool = typer.Option(False, help="Overwrite existing files if present"),
    ):
        """Create a risk register for proactive risk management."""
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
            "DURATION": duration,
            "DATE": created,
            "FEATURE_ID": num_str,
            "SLUG": slug,
        }

        # risk-register.md
        try:
            template = _load_template("risk-register.md")
            filled = _apply_replacements(template, mapping)
            meta = {
                "title": f"{program_name} - Risk Register",
                "created": created,
                "feature": f"{num_str}-{slug}",
                "status": "active",
            }
            text = _prepend_metadata(filled, meta)
            dest = feature_dir / "risk-register.md"
            write_markdown_if_needed(dest, text, force=force, console=console)

            console.print(
                Panel(
                    f"Risk register created: [cyan]{dest}[/cyan]\n\n"
                    f"This register includes:\n"
                    f"  • Risk assessment framework (likelihood × impact)\n"
                    f"  • 8 risk categories with examples:\n"
                    f"    - Program delivery risks\n"
                    f"    - Stakeholder & partnership risks\n"
                    f"    - Financial & resource risks\n"
                    f"    - Staffing & HR risks\n"
                    f"    - Health & safety risks\n"
                    f"    - Ethical & legal risks\n"
                    f"    - Reputational risks\n"
                    f"    - Cultural safety risks\n"
                    f"  • Risk summary dashboard\n"
                    f"  • Review and incident reporting processes\n\n"
                    f"Next steps:\n"
                    f"  1. Review and customize risk examples\n"
                    f"  2. Add program-specific risks\n"
                    f"  3. Schedule monthly risk reviews",
                    title="Risk Register Ready",
                    border_style="green",
                )
            )
        except Exception as e:
            console.print(f"[red]Failed to create risk-register.md:[/red] {e}")
            raise typer.Exit(1)
