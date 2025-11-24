"""Risk register command using factory pattern."""

import typer
from rich.console import Console

from ..command_factory import FieldConfig, TemplateCommandConfig, TemplateCommandHandler

# Configuration for the risk command
CONFIG = TemplateCommandConfig(
    command_name="risk",
    template_name="risk-register.md",
    output_filename="risk-register.md",
    help_text="""Create a risk register for proactive risk management.

    This command generates a comprehensive risk register that identifies, assesses,
    and documents strategies for managing potential risks to program delivery, staff
    safety, participant wellbeing, and organizational reputation. Proactive risk
    management is essential for ethical service delivery and funder accountability.

    The risk register includes:
    - **Risk Assessment Framework**: Structured approach to evaluate likelihood and
      impact using a standardized matrix (Low/Medium/High/Critical)
    - **Eight Risk Categories**: Pre-populated with harm reduction-specific examples:
      * Program Delivery Risks: Capacity, service quality, participant engagement
      * Stakeholder & Partnership Risks: Relationship management, community trust
      * Financial & Resource Risks: Funding sustainability, budget management
      * Staffing & HR Risks: Peer workforce support, burnout, supervision
      * Health & Safety Risks: Overdose response, bloodborne virus exposure
      * Ethical & Legal Risks: Confidentiality, mandatory reporting, discrimination
      * Reputational Risks: Media coverage, political backlash, stigma
      * Cultural Safety Risks: Racism, cultural appropriation, trauma
    - **Mitigation Strategies**: Preventive controls and response plans for each risk
    - **Risk Ownership**: Assignment of responsibility for monitoring and action
    - **Review Process**: Regular risk assessment schedule and incident reporting

    NUAA's risk register balances genuine risk management with avoiding excessive
    risk aversion that could limit innovative harm reduction approaches. It emphasizes
    risks to participants (not just organizational risks) and includes cultural safety
    and peer workforce wellbeing as central concerns.
    """,
    fields=[
        FieldConfig("duration", "Program duration (e.g., '12 months')", max_length=100),
    ],
)

# Create handler
_handler = TemplateCommandHandler(CONFIG)


def register(app, show_banner_fn=None, console: Console | None = None):
    """Register the risk command with the Typer app."""
    console = console or Console()

    @app.command()
    def risk(
        program_name: str = typer.Argument(
            ..., help="Program name (used to derive feature folder)"
        ),
        duration: str = typer.Argument(..., help="Program duration (e.g., '12 months')"),
        feature: str | None = typer.Option(
            None, help="Override feature slug (e.g., '001-custom-slug')"
        ),
        force: bool = typer.Option(False, help="Overwrite existing files if present"),
    ):
        """Create a risk register for proactive risk management."""
        _handler.execute(
            program_name,
            duration,
            feature=feature,
            force=force,
            show_banner_fn=show_banner_fn,
            console=console,
        )
