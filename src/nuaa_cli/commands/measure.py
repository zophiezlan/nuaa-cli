"""Impact measurement framework command using factory pattern."""

import typer
from rich.console import Console

from ..command_factory import FieldConfig, TemplateCommandConfig, TemplateCommandHandler

# Configuration for the measure command
CONFIG = TemplateCommandConfig(
    command_name="measure",
    template_name="impact-framework.md",
    output_filename="impact-framework.md",
    help_text="""Create or update the impact framework document from the template.

    This command generates or refreshes a comprehensive impact measurement framework
    that operationalizes the program's logic model into concrete data collection and
    evaluation activities. The framework is essential for demonstrating program
    effectiveness to funders, partners, and the community.

    The impact framework document includes:
    - Key Performance Indicators (KPIs) aligned with harm reduction outcomes
    - Data collection methods that respect participant privacy and autonomy
    - Evaluation timeline with baseline, interim, and final assessment points
    - Equity and cultural safety considerations in measurement
    - Participatory evaluation approaches centering peer input
    - Budget allocation for evaluation activities and external evaluators

    NUAA's framework templates emphasize outcome measurement that matters to people
    who use drugs, not just process metrics. This includes quality-of-life indicators,
    harm reduction behavior change, reduced stigma, and increased access to services.

    This command is typically used after program design to detail the measurement
    strategy, or during program implementation to update evaluation approaches based
    on emerging insights.

    Args:
        program_name: Name of existing program (must match a feature directory created
            with 'nuaa design'). The impact framework will be created/updated in this
            program's feature folder.
        evaluation_period: Timeframe for evaluation activities (e.g., "6 months",
            "ongoing with quarterly reviews", "baseline + 12-month follow-up").
            Should align with program duration and funder reporting requirements.
        budget: Dedicated funding for evaluation activities, including data collection,
            analysis, and external evaluator fees (e.g., "$7000", "$25k", "10% of total").
            Helps ensure adequate resources for robust impact measurement.
        force: If True, overwrites existing impact-framework.md file. Default is False
            to preserve customizations and collected baseline data.

    Raises:
        typer.Exit: Exits with code 1 if the impact framework template is not found
            (requires 'nuaa init'), if permission is denied for file operations, or if
            other filesystem errors occur.

    Examples:
        Set up impact measurement for a new peer support program:
            $ nuaa measure "Peer Support Network" "12 months with quarterly reviews" "$15000"

        Define evaluation for an overdose prevention pilot:
            $ nuaa measure "Naloxone Distribution" "6-month pilot evaluation" "$8000"

        Update framework for ongoing program with annual assessment:
            $ nuaa measure "Needle Exchange" "annual evaluation cycle" "$12000" --force

        Establish measurement for culturally-specific initiative:
            $ nuaa measure "Aboriginal Peer Program" "2 years with 6-month milestones" "$30000"
    """,
    fields=[
        FieldConfig("evaluation_period", "Evaluation period/timeframe", max_length=100),
        FieldConfig("budget", "Evaluation budget (e.g., $7000)", max_length=100),
    ],
    metadata_generator=lambda prog, m: {
        "title": f"{prog} - Impact Framework",
    },
)

# Create handler instance
_handler = TemplateCommandHandler(CONFIG)


def register(app, show_banner_fn=None, console: Console | None = None):
    """Register the measure command with the Typer app."""
    console = console or Console()

    @app.command()
    def measure(
        program_name: str = typer.Argument(..., help="Program name (existing)"),
        evaluation_period: str = typer.Argument(..., help="Evaluation period"),
        budget: str = typer.Argument(..., help="Evaluation budget (e.g., $7000)"),
        force: bool = typer.Option(False, help="Overwrite if exists"),
    ):
        """Create or update the impact framework document from the template."""
        _handler.execute(
            program_name,
            evaluation_period,
            budget,
            force=force,
            show_banner_fn=show_banner_fn,
            console=console,
        )
