"""Training curriculum command using factory pattern."""

import typer
from rich.console import Console

from ..command_factory import FieldConfig, TemplateCommandConfig, TemplateCommandHandler

# Configuration for the train command
CONFIG = TemplateCommandConfig(
    command_name="train",
    template_name="training-curriculum.md",
    output_filename="training-curriculum.md",
    help_text="""Create a training curriculum for peer workforce development.

    This command generates a comprehensive training curriculum template for developing
    the capacity of peer workers, volunteers, community members, or external partners.
    Quality training is essential for effective peer-led harm reduction services, ensuring
    consistency, safety, cultural competence, and ethical practice.

    The training curriculum includes:
    - **Learning Objectives**: Clear, measurable outcomes aligned with harm reduction
      competencies and organizational values
    - **Session Structure**: Detailed lesson plans with timing, activities, facilitation
      notes, and required materials
    - **Core Content Areas**: Pre-populated sections covering NUAA's essential topics:
      * Harm reduction principles and history
      * Peer-led approaches and lived experience expertise
      * Cultural safety and trauma-informed practice
      * Overdose prevention and naloxone administration
      * Bloodborne virus awareness and safer injecting
      * Rights, advocacy, and challenging stigma
      * Boundaries, self-care, and vicarious trauma
    - **Training Methods**: Mix of facilitation techniques (presentations, group discussions,
      role-plays, case studies, experiential learning)
    - **Assessment and Evaluation**: Knowledge checks, skills demonstrations, participant
      feedback, post-training follow-up
    - **Resources and Materials**: Handouts, visual aids, equipment needs, reference materials
    - **Facilitator Notes**: Tips for engaging diverse learners, handling challenging topics,
      managing group dynamics

    NUAA's training approach values lived experience as expertise, creates psychologically
    safe learning environments, and recognizes that peer workers bring skills that cannot
    be taught in formal training. The curriculum balances structure with flexibility for
    participant-led learning.
    """,
    fields=[
        FieldConfig("target_audience", "Target audience (e.g., 'Peer workers')", max_length=300),
        FieldConfig("duration", "Training duration (e.g., '2 days', '8 weeks')", max_length=100),
    ],
    primary_field_name="TRAINING_NAME",
)

# Create handler
_handler = TemplateCommandHandler(CONFIG)


def register(app, show_banner_fn=None, console: Console | None = None):
    """Register the train command with the Typer app."""
    console = console or Console()

    @app.command()
    def train(
        training_name: str = typer.Argument(..., help="Training name (e.g., 'Peer Worker Induction')"),
        target_audience: str = typer.Argument(..., help="Target audience (e.g., 'Peer workers')"),
        duration: str = typer.Argument(..., help="Training duration (e.g., '2 days', '8 weeks')"),
        feature: str | None = typer.Option(None, help="Override feature slug (e.g., '001-custom-slug')"),
        force: bool = typer.Option(False, help="Overwrite existing files if present"),
    ):
        """Create a training curriculum for peer workforce development."""
        _handler.execute(
            training_name,
            target_audience,
            duration,
            feature=feature,
            force=force,
            show_banner_fn=show_banner_fn,
            console=console,
        )
