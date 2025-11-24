"""Partnership agreement (MOU) command using factory pattern."""

import typer
from rich.console import Console

from ..command_factory import FieldConfig, TemplateCommandConfig, TemplateCommandHandler

# Configuration for the partner command
CONFIG = TemplateCommandConfig(
    command_name="partner",
    template_name="partnership-agreement.md",
    output_filename="partnership-agreement.md",
    help_text="""Create a partnership agreement (MOU) template for a NUAA collaboration.

    This command generates a comprehensive Memorandum of Understanding (MOU) template
    that formalizes partnerships with health services, community organizations,
    government agencies, or other harm reduction groups. Strong partnership agreements
    clarify expectations, protect organizational interests, and establish foundations
    for effective collaboration.

    The partnership agreement template includes:
    - **Purpose and Scope**: Shared objectives and boundaries of the partnership
    - **Roles and Responsibilities**: Clear delineation of what each partner contributes
      and delivers, preventing duplication and gaps
    - **Governance Structure**: Decision-making processes, meeting schedules, and
      dispute resolution mechanisms
    - **Information Sharing Protocols**: How participant data and confidential information
      will be handled, respecting privacy and consent requirements
    - **Financial Arrangements**: Cost-sharing, resource contributions, or funding flows
      between partners
    - **Cultural Safety and Values Alignment**: Commitment to harm reduction principles,
      peer-led approaches, and non-judgmental service delivery
    - **Review and Exit Provisions**: How the partnership will be evaluated and
      conditions for modification or termination

    NUAA's MOU template emphasizes equitable partnerships where peer-led organizations
    have equal voice despite potential power imbalances. It includes language protecting
    NUAA's independence, advocacy role, and commitment to centering lived experience.
    """,
    fields=[
        FieldConfig("partner_org", "Partner organization name", max_length=300),
        FieldConfig("duration", "Agreement duration (e.g., '2 years')", max_length=100),
    ],
)

# Create handler
_handler = TemplateCommandHandler(CONFIG)


def register(app, show_banner_fn=None, console: Console | None = None):
    """Register the partner command with the Typer app."""
    console = console or Console()

    @app.command()
    def partner(
        program_name: str = typer.Argument(..., help="Program or partnership name"),
        partner_org: str = typer.Argument(..., help="Partner organization name"),
        duration: str = typer.Argument(..., help="Agreement duration (e.g., '2 years')"),
        feature: str | None = typer.Option(
            None, help="Override feature slug (e.g., '001-custom-slug')"
        ),
        force: bool = typer.Option(False, help="Overwrite existing files if present"),
    ):
        """Create a partnership agreement (MOU) template for a NUAA collaboration."""
        _handler.execute(
            program_name,
            partner_org,
            duration,
            feature=feature,
            force=force,
            show_banner_fn=show_banner_fn,
            console=console,
        )
