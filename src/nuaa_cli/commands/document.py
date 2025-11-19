"""Existing program analysis command using factory pattern."""

import typer
from rich.console import Console

from ..command_factory import FieldConfig, TemplateCommandConfig, TemplateCommandHandler

# Configuration for the document command
CONFIG = TemplateCommandConfig(
    command_name="document",
    template_name="existing-program-analysis.md",
    output_filename="existing-program-analysis.md",
    help_text="""Create an existing program analysis document.

    This command generates a structured analysis template for documenting programs
    that are already running but may lack comprehensive written documentation. It's
    essential for institutional knowledge capture, continuity planning, and identifying
    opportunities for program improvement or expansion.

    The existing program analysis document includes sections for:
    - Program history and evolution over time
    - Current service delivery model and key activities
    - Target population served and reach statistics
    - Staffing structure and peer workforce composition
    - Partnerships and referral pathways
    - Funding sources and financial sustainability
    - Strengths, challenges, and lessons learned
    - Opportunities for enhancement or replication

    This tool is particularly valuable when transitioning programs from informal to
    documented models, preparing for external evaluation, training new staff, or
    developing funding applications for program expansion based on proven success.

    NUAA's template emphasizes capturing the tacit knowledge of peer workers who
    have been delivering services, ensuring their expertise and insights are
    preserved and valued in formal documentation.

    Args:
        program_name: Name or identifier of the existing program to document (e.g.,
            "Mobile Needle Exchange", "Peer Phone Support Line"). Will create or use
            an existing feature directory for this program.
        force: If True, overwrites existing existing-program-analysis.md file. Default
            is False to prevent loss of previously documented information.

    Raises:
        typer.Exit: Exits with code 1 if the existing program analysis template is not
            found (requires 'nuaa init'), if permission is denied for file operations,
            or if other filesystem errors occur.

    Examples:
        Document a long-running needle exchange service:
            $ nuaa document "Mobile Needle Exchange"

        Capture analysis of peer-led phone support:
            $ nuaa document "Peer Support Helpline"

        Create program analysis for advocacy work:
            $ nuaa document "Drug Law Reform Campaign"

        Update existing documentation with recent changes:
            $ nuaa document "Overdose Prevention Training" --force
    """,
    fields=[],  # No additional fields beyond program_name
    metadata_generator=lambda prog, m: {
        "title": f"{prog} - Existing Program Analysis",
    },
)

# Create handler instance
_handler = TemplateCommandHandler(CONFIG)


def register(app, show_banner_fn=None, console: Console | None = None):
    """Register the document command with the Typer app."""
    console = console or Console()

    @app.command()
    def document(
        program_name: str = typer.Argument(..., help="Existing program identifier/name"),
        force: bool = typer.Option(False, help="Overwrite if exists"),
    ):
        """Create an existing program analysis document."""
        _handler.execute(
            program_name,
            force=force,
            show_banner_fn=show_banner_fn,
            console=console,
        )
