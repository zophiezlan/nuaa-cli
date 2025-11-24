"""Program design command using factory pattern."""

import typer
from rich.console import Console

from ..command_factory import FieldConfig, TemplateCommandConfig, TemplateCommandHandler

# Configuration for the design command
CONFIG = TemplateCommandConfig(
    command_name="design",
    template_name="program-design.md",
    output_filename="program-design.md",
    help_text="""Create a new NUAA program design with logic model and framework.

    This command initializes a comprehensive program design package for harm reduction
    initiatives. It creates a feature-numbered directory containing three foundational
    documents that guide the entire program lifecycle:

    - **program-design.md**: Core program architecture including goals, target population,
      cultural safety considerations, and implementation approach
    - **logic-model.md**: Theory of change mapping inputs, activities, outputs, and
      intended outcomes following evidence-based harm reduction principles
    - **impact-framework.md**: Measurement strategy defining KPIs, data collection methods,
      and evaluation approach aligned with NUAA's equity-focused values

    The command automatically generates a sequential feature ID (e.g., 001-, 002-) based
    on existing programs, or you can specify a custom feature slug. All documents are
    pre-populated with NUAA-specific templates emphasizing peer-led approaches, cultural
    safety, and trauma-informed practices.

    This is typically the first command in the NUAA program workflow, establishing the
    foundation for subsequent funding proposals, stakeholder engagement, and impact
    measurement activities.

    Args:
        program_name: Name of the harm reduction program or initiative (e.g.,
            "Peer Support Network", "Safe Consumption Spaces"). Used to derive the
            feature folder name and populate all template documents.
        target_population: Description of primary beneficiaries (e.g.,
            "People who use drugs in Western Sydney", "LGBTIQ+ PWUD aged 18-30").
            Should reflect NUAA's person-centered language principles.
        duration: Intended program duration (e.g., "6 months", "2 years", "ongoing").
            Used for planning timelines and evaluation schedules.
        here: If True (default), creates the feature under ./nuaa in the current project.
            Set to False for alternative locations.
        feature: Optional custom feature slug to override auto-generated numbering.
            Can be full format "001-custom-slug" or just "custom-slug" (number will
            be auto-assigned). Useful for maintaining specific naming conventions.
        force: If True, overwrites existing files in the feature directory. Default
            is False to prevent accidental data loss.

    Raises:
        typer.Exit: Exits with code 1 if template files are not found (requires 'nuaa init'),
            if permission is denied for file operations, or if other filesystem errors occur.

    Examples:
        Create a new peer support program design:
            $ nuaa design "Peer Support Network" "PWUD in Western Sydney" "12 months"

        Design a culturally-specific program with custom feature slug:
            $ nuaa design "Aboriginal Peer Program" "Aboriginal and Torres Strait Islander PWUD" "2 years" --feature aboriginal-peer-support

        Create a harm reduction initiative for young people:
            $ nuaa design "Youth Engagement Program" "Young PWUD aged 16-25" "6 months"

        Overwrite an existing design (use with caution):
            $ nuaa design "Naloxone Distribution" "PWUD in Sydney CBD" "ongoing" --force
    """,
    fields=[
        FieldConfig("target_population", "Target population description", max_length=500),
        FieldConfig("duration", "Program duration (e.g., '6 months')", max_length=100),
    ],
    additional_outputs=[
        ("logic-model.md", "logic-model.md"),
        ("impact-framework.md", "impact-framework.md"),
    ],
    create_changelog=True,
)

# Create handler
_handler = TemplateCommandHandler(CONFIG)


def register(app, show_banner_fn=None, console: Console | None = None):
    """Register the design command with the Typer app."""
    console = console or Console()

    @app.command()
    def design(
        program_name: str = typer.Argument(
            ..., help="Program name (used to derive feature folder)"
        ),
        target_population: str = typer.Argument(..., help="Target population description"),
        duration: str = typer.Argument(..., help="Program duration (e.g., '6 months')"),
        here: bool = typer.Option(True, help="Create under ./nuaa (current project)"),
        feature: str | None = typer.Option(
            None, help="Override feature slug (e.g., '001-custom-slug')"
        ),
        force: bool = typer.Option(False, help="Overwrite existing files if present"),
    ):
        """Create a new NUAA program design with logic model and framework."""
        _handler.execute(
            program_name,
            target_population,
            duration,
            feature=feature,
            force=force,
            show_banner_fn=show_banner_fn,
            console=console,
        )
