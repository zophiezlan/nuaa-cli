"""Stakeholder engagement plan command using factory pattern."""

import typer
from rich.console import Console

from ..command_factory import FieldConfig, TemplateCommandConfig, TemplateCommandHandler

# Configuration for the engage command
CONFIG = TemplateCommandConfig(
    command_name="engage",
    template_name="stakeholder-engagement-plan.md",
    output_filename="stakeholder-engagement-plan.md",
    help_text="""Create a stakeholder engagement plan for a NUAA program.

    This command generates a comprehensive stakeholder engagement plan that maps
    all relevant stakeholders and defines strategies for meaningful, culturally-safe
    engagement throughout the program lifecycle. Strong stakeholder relationships
    are essential for program success, sustainability, and systemic advocacy.

    The stakeholder engagement plan includes:
    - **Stakeholder Mapping**: Identification and analysis of all stakeholder groups
      including PWUD communities, government agencies, health services, peer
      organizations, funders, and allies
    - **Engagement Strategies**: Tailored approaches for each stakeholder group
      recognizing power dynamics, cultural needs, and relationship history
    - **Communication Channels**: Preferred methods (face-to-face, email, peer networks,
      social media) respecting accessibility and privacy needs
    - **Engagement Timeline**: Frequency and timing of engagement activities aligned
      with program milestones
    - **Cultural Safety Considerations**: Protocols for trauma-informed, non-judgmental,
      and culturally-responsive engagement
    - **Feedback Mechanisms**: How stakeholder input will be collected, valued, and
      integrated into program refinement

    NUAA's stakeholder engagement approach centers the voices of people who use drugs
    as primary stakeholders, not afterthoughts. The template ensures peer participation
    is meaningful, compensated, and valued as expert consultation.

    Args:
        program_name: Name of the program or initiative requiring stakeholder engagement
            (e.g., "Supervised Injection Facility", "Drug Law Reform Campaign").
            Used to create a feature directory and populate the template.
        target_population: Primary stakeholder group or program beneficiaries (e.g.,
            "PWUD in inner Sydney", "Young people who inject drugs"). Helps identify
            related stakeholder networks and community connections.
        duration: Planning timeframe for engagement activities (e.g., "12 months",
            "2-year pilot", "ongoing advocacy campaign"). Should align with program
            duration and key engagement milestones.
        feature: Optional custom feature slug to override auto-generated numbering.
            Useful for maintaining consistent naming across related initiatives.
        force: If True, overwrites existing stakeholder-engagement-plan.md file.
            Default is False to preserve existing relationship mapping and notes.

    Raises:
        typer.Exit: Exits with code 1 if the stakeholder engagement template is not
            found (requires 'nuaa init'), if permission is denied for file operations,
            or if other filesystem errors occur.

    Examples:
        Create engagement plan for new peer support initiative:
            $ nuaa engage "Peer Support Network" "PWUD in Western Sydney" "12 months"

        Plan stakeholder engagement for advocacy campaign:
            $ nuaa engage "Drug Law Reform" "NSW PWUD community" "2 years"

        Develop engagement strategy for culturally-specific program:
            $ nuaa engage "Aboriginal Harm Reduction" "Aboriginal and Torres Strait Islander PWUD" "ongoing" --feature aboriginal-engagement

        Map stakeholders for service expansion:
            $ nuaa engage "Needle Exchange Network" "PWUD across regional NSW" "18 months"
    """,
    fields=[
        FieldConfig("target_population", "Target population description", max_length=500),
        FieldConfig("duration", "Planning period (e.g., '12 months')", max_length=100),
    ],
)

# Create handler
_handler = TemplateCommandHandler(CONFIG)


def register(app, show_banner_fn=None, console: Console | None = None):
    """Register the engage command with the Typer app."""
    console = console or Console()

    @app.command()
    def engage(
        program_name: str = typer.Argument(..., help="Program name (used to derive feature folder)"),
        target_population: str = typer.Argument(..., help="Target population description"),
        duration: str = typer.Argument(..., help="Planning period (e.g., '12 months')"),
        feature: str | None = typer.Option(None, help="Override feature slug (e.g., '001-custom-slug')"),
        force: bool = typer.Option(False, help="Overwrite existing files if present"),
    ):
        """Create a stakeholder engagement plan for a NUAA program."""
        _handler.execute(
            program_name,
            target_population,
            duration,
            feature=feature,
            force=force,
            show_banner_fn=show_banner_fn,
            console=console,
        )
