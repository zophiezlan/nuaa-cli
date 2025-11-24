"""Event planning command using factory pattern."""

import typer
from rich.console import Console

from ..command_factory import FieldConfig, TemplateCommandConfig, TemplateCommandHandler

# Configuration for the event command
CONFIG = TemplateCommandConfig(
    command_name="event",
    template_name="event-plan.md",
    output_filename="event-plan.md",
    help_text="""Create an event plan for workshops, forums, launches, or celebrations.

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
    """,
    fields=[
        FieldConfig("event_type", "Event type (e.g., 'Workshop', 'Forum')", max_length=100),
        FieldConfig(
            "expected_attendance", "Expected attendance (e.g., '50 people')", max_length=100
        ),
    ],
    primary_field_name="EVENT_NAME",
)

# Create handler
_handler = TemplateCommandHandler(CONFIG)


def register(app, show_banner_fn=None, console: Console | None = None):
    """Register the event command with the Typer app."""
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
        feature: str | None = typer.Option(
            None, help="Override feature slug (e.g., '001-custom-slug')"
        ),
        force: bool = typer.Option(False, help="Overwrite existing files if present"),
    ):
        """Create an event plan for workshops, forums, launches, or celebrations."""
        _handler.execute(
            event_name,
            event_type,
            expected_attendance,
            feature=feature,
            force=force,
            show_banner_fn=show_banner_fn,
            console=console,
        )
