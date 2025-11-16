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
    def event(
        event_name: str = typer.Argument(
            ..., help="Event name (e.g., 'Peer Forum Launch')"
        ),
        event_type: str = typer.Argument(
            ..., help="Event type (e.g., 'Workshop', 'Forum', 'Training')"
        ),
        expected_attendance: str = typer.Argument(
            ..., help="Expected attendance (e.g., '50 people')"
        ),
        feature: Optional[str] = typer.Option(
            None, help="Override feature slug (e.g., '001-custom-slug')"
        ),
        force: bool = typer.Option(False, help="Overwrite existing files if present"),
    ):
        """Create an event plan for workshops, forums, launches, or celebrations."""
        if show_banner_fn:
            show_banner_fn()

        # Determine feature directory
        if feature:
            slug = _slugify(feature)
            feature_dir, num_str, _ = _next_feature_dir(slug)
        else:
            feature_dir, num_str, slug = _next_feature_dir(event_name)

        created = datetime.now().strftime("%Y-%m-%d")
        mapping = {
            "EVENT_NAME": event_name,
            "EVENT_TYPE": event_type,
            "EXPECTED_ATTENDANCE": expected_attendance,
            "DATE": created,
            "FEATURE_ID": num_str,
            "SLUG": slug,
        }

        # event-plan.md
        try:
            template = _load_template("event-plan.md")
            filled = _apply_replacements(template, mapping)
            meta = {
                "title": f"{event_name} - Event Plan",
                "created": created,
                "feature": f"{num_str}-{slug}",
                "status": "planning",
                "event_type": event_type,
            }
            text = _prepend_metadata(filled, meta)
            dest = feature_dir / "event-plan.md"
            write_markdown_if_needed(dest, text, force=force, console=console)

            console.print(
                Panel(
                    f"Event plan created: [cyan]{dest}[/cyan]\n\n"
                    f"This plan includes:\n"
                    f"  • Event overview and objectives\n"
                    f"  • Detailed event program and schedule\n"
                    f"  • Logistics (venue, equipment, catering)\n"
                    f"  • Promotion and registration strategy\n"
                    f"  • Event team roles and responsibilities\n"
                    f"  • Risk management and contingencies\n"
                    f"  • Comprehensive planning checklist\n\n"
                    f"Next steps:\n"
                    f"  1. Finalize event program and speakers\n"
                    f"  2. Book venue and arrange catering\n"
                    f"  3. Create promotional materials\n"
                    f"  4. Open registration",
                    title="Event Plan Ready",
                    border_style="green",
                )
            )
        except Exception as e:
            console.print(f"[red]Failed to create event-plan.md:[/red] {e}")
            raise typer.Exit(1)
