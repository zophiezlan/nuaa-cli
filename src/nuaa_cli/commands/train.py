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
from ..utils import validate_text_field


def register(app, show_banner_fn=None, console: Console | None = None):
    console = console or Console()

    @app.command()
    def train(
        training_name: str = typer.Argument(..., help="Training program name (e.g., 'Peer Worker Training')"),
        target_audience: str = typer.Argument(..., help="Target audience (e.g., 'Peer Workers', 'Volunteers')"),
        duration: str = typer.Argument(..., help="Training duration (e.g., '2 days', '8 weeks')"),
        feature: Optional[str] = typer.Option(None, help="Override feature slug (e.g., '001-custom-slug')"),
        force: bool = typer.Option(False, help="Overwrite existing files if present"),
    ):
        """Create a training curriculum for peer workers, volunteers, or staff.

        This command generates a comprehensive training curriculum template for building
        capacity in the peer workforce, volunteers, partner staff, or community members.
        Quality training is essential for effective harm reduction service delivery,
        peer worker confidence, and organizational sustainability.

        The training curriculum includes:
        - **Training Overview**: Purpose, learning objectives, and expected competencies
          aligned with peer-led harm reduction principles
        - **Detailed Training Schedule**: Session-by-session breakdown with timing,
          learning activities, and breaks (trauma-informed pacing)
        - **Core Training Modules**: 8+ customizable modules covering:
          * Harm reduction philosophy and person-centered approaches
          * Peer roles, boundaries, and ethical practice
          * Trauma-informed and culturally-safe practice
          * Communication skills and active listening
          * Overdose prevention and naloxone administration
          * Safer injecting/using practices and equipment
          * Bloodborne virus awareness and prevention
          * Self-care, burnout prevention, and peer support
        - **Facilitation Guidance**: Tips for engaging adult learners, creating safe
          learning environments, and responding to disclosure/distress
        - **Training Materials**: Handouts, activities, case studies, and resources
        - **Assessment and Certification**: Competency assessment approaches (not
          punitive), certificates, and ongoing professional development pathways
        - **Participant Support**: Accessibility accommodations, transport subsidies,
          childcare, honorariums for peer participation

        NUAA's training approach values lived experience as expertise, uses participatory
        adult learning methods, and ensures peer workers are compensated fairly for
        their time and knowledge sharing.

        Args:
            training_name: Descriptive name for the training program (e.g.,
                "Peer Worker Training", "Naloxone Administration Course",
                "Cultural Safety for Health Workers"). Used throughout curriculum.
            target_audience: Primary trainees (e.g., "Peer Workers", "Volunteers",
                "Health Service Staff", "Community Members"). Customizes content
                complexity, assumed knowledge, and learning approaches.
            duration: Total training length (e.g., "2 days", "8 weeks", "6 x 3-hour
                sessions", "self-paced online"). Determines depth of content and
                scheduling considerations.
            feature: Optional custom feature slug to override auto-generated numbering.
                Useful for maintaining consistent naming across training initiatives.
            force: If True, overwrites existing training-curriculum.md file. Default
                is False to preserve curriculum customizations and facilitator notes.

        Raises:
            typer.Exit: Exits with code 1 if the training curriculum template is not
                found (requires 'nuaa init'), if permission is denied for file operations,
                or if other filesystem errors occur.

        Examples:
            Create peer worker foundation training:
                $ nuaa train "Peer Worker Foundation Training" "New Peer Workers" "3 days"

            Develop naloxone training for community:
                $ nuaa train "Naloxone Administration" "PWUD and Family Members" "2 hours"

            Design cultural safety training for health workers:
                $ nuaa train "Cultural Safety in Harm Reduction" "Health Service Staff" "1 day"

            Build advanced peer supervision curriculum:
                $ nuaa train "Peer Supervision Skills" "Experienced Peer Workers" "6 weeks" --feature peer-supervision
        """
        if show_banner_fn:
            show_banner_fn()

        # Validate inputs
        training_name = validate_text_field(training_name, "training_name", 200, console)
        target_audience = validate_text_field(target_audience, "target_audience", 200, console)
        duration = validate_text_field(duration, "duration", 100, console)

        # Determine feature directory
        if feature:
            slug = _slugify(feature)
            feature_dir, num_str, _ = _next_feature_dir(slug)
        else:
            feature_dir, num_str, slug = _next_feature_dir(training_name)

        created = datetime.now().strftime("%Y-%m-%d")
        mapping = {
            "TRAINING_NAME": training_name,
            "TARGET_AUDIENCE": target_audience,
            "DURATION": duration,
            "DATE": created,
            "FEATURE_ID": num_str,
            "SLUG": slug,
        }

        # training-curriculum.md
        try:
            template = _load_template("training-curriculum.md")
            filled = _apply_replacements(template, mapping)
            meta = {
                "title": f"{training_name} - Training Curriculum",
                "created": created,
                "feature": f"{num_str}-{slug}",
                "status": "draft",
                "audience": target_audience,
            }
            text = _prepend_metadata(filled, meta)
            dest = feature_dir / "training-curriculum.md"
            write_markdown_if_needed(dest, text, force=force, console=console)

            console.print(
                Panel(
                    f"Training curriculum created: [cyan]{dest}[/cyan]\n\n"
                    f"This curriculum includes:\n"
                    f"  • Training overview and learning objectives\n"
                    f"  • Detailed training schedule\n"
                    f"  • 8+ training modules with activities\n"
                    f"  • Facilitation guidance and tips\n"
                    f"  • Training materials list\n"
                    f"  • Participant support and assessment\n\n"
                    f"Next steps:\n"
                    f"  1. Customize modules for {target_audience}\n"
                    f"  2. Develop activities and handouts\n"
                    f"  3. Schedule and promote training",
                    title="Training Curriculum Ready",
                    border_style="green",
                )
            )
        except FileNotFoundError:
            console.print("[red]Template not found:[/red] training-curriculum.md")
            console.print("[dim]Run 'nuaa init' to set up templates[/dim]")
            raise typer.Exit(1)
        except PermissionError:
            console.print("[red]Permission denied:[/red] Cannot read template or write output file")
            raise typer.Exit(1)
        except OSError as e:
            console.print(f"[red]File system error:[/red] {e}")
            raise typer.Exit(1)
