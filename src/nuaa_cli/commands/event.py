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
from ..utils import validate_program_name, validate_text_field


def register(app, show_banner_fn=None, console: Console | None = None):
    console = console or Console()

    @app.command()
    def event(
        event_name: str = typer.Argument(..., help="Event name (e.g., 'Peer Forum Launch')"),
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
        """Create an event plan for workshops, forums, launches, or celebrations.

        This command generates a comprehensive event planning document for organizing
        peer-led gatherings, community forums, training workshops, program launches,
        celebrations, or advocacy events. Well-planned events strengthen community,
        build capacity, and demonstrate NUAA's commitment to accessible, inclusive,
        and culturally-safe gatherings.

        The event plan includes:
        - **Event Overview**: Purpose, objectives, and intended outcomes aligned with
          NUAA's mission and harm reduction principles
        - **Detailed Program**: Session schedule, speakers/facilitators, activities,
          and content flow with timing
        - **Logistics Coordination**: Venue selection (accessible, safe, culturally
          appropriate), equipment needs, catering (dietary requirements), transport
        - **Promotion and Registration**: Marketing strategy, communication channels,
          registration process, accessibility accommodations
        - **Event Team**: Roles and responsibilities (MC, facilitators, peer support,
          technical support, accessibility coordinator)
        - **Risk Management**: Health and safety protocols, emergency procedures,
          harm reduction supplies, safe space policies
        - **Budget**: Venue costs, catering, honorariums for peer presenters, materials,
          transport subsidies
        - **Planning Checklist**: Timeline of tasks from initial planning to post-event
          evaluation

        NUAA's event planning approach prioritizes accessibility (physical, cognitive,
        financial), cultural safety, trauma-informed practices, and meaningful peer
        participation. Events should be welcoming, non-judgmental spaces where people
        who use drugs feel valued and safe.

        Args:
            event_name: Descriptive name for the event (e.g., "Annual Peer Forum",
                "Naloxone Training Workshop", "Harm Reduction Week Launch"). Used
                throughout the event plan and promotional materials.
            event_type: Category of event (e.g., "Workshop", "Forum", "Training",
                "Launch", "Celebration", "Conference"). Customizes planning sections
                and logistics requirements.
            expected_attendance: Anticipated number of participants (e.g., "50 people",
                "100-150 attendees", "30 peer workers"). Used for venue size, catering,
                materials, and resource planning.
            feature: Optional custom feature slug to override auto-generated numbering.
                Useful for grouping related events or maintaining naming conventions.
            force: If True, overwrites existing event-plan.md file. Default is False
                to preserve planning notes, vendor contacts, and confirmed details.

        Raises:
            typer.Exit: Exits with code 1 if the event plan template is not found
                (requires 'nuaa init'), if permission is denied for file operations,
                or if other filesystem errors occur.

        Examples:
            Plan annual peer worker forum:
                $ nuaa event "Annual Peer Forum" "Forum" "80 people"

            Organize naloxone training workshop:
                $ nuaa event "Naloxone Training" "Workshop" "25 participants"

            Launch new supervised injection facility:
                $ nuaa event "SIF Community Launch" "Launch Event" "150 attendees"

            Plan Harm Reduction Week celebration with custom slug:
                $ nuaa event "Harm Reduction Week 2024" "Community Celebration" "200 people" --feature hr-week-2024
        """
        if show_banner_fn:
            show_banner_fn()

        # Validate inputs
        event_name = validate_text_field(event_name, "event_name", 200, console)
        event_type = validate_text_field(event_type, "event_type", 100, console)
        expected_attendance = validate_text_field(expected_attendance, "expected_attendance", 100, console)

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
        except FileNotFoundError:
            console.print("[red]Template not found:[/red] event-plan.md")
            console.print("[dim]Run 'nuaa init' to set up templates[/dim]")
            raise typer.Exit(1)
        except PermissionError:
            console.print("[red]Permission denied:[/red] Cannot read template or write output file")
            raise typer.Exit(1)
        except OSError as e:
            console.print(f"[red]File system error:[/red] {e}")
            raise typer.Exit(1)
