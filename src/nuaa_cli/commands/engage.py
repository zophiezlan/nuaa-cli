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
    def engage(
        program_name: str = typer.Argument(..., help="Program name (used to derive feature folder)"),
        target_population: str = typer.Argument(..., help="Target population description"),
        duration: str = typer.Argument(..., help="Planning period (e.g., '12 months')"),
        feature: Optional[str] = typer.Option(None, help="Override feature slug (e.g., '001-custom-slug')"),
        force: bool = typer.Option(False, help="Overwrite existing files if present"),
    ):
        """Create a stakeholder engagement plan for a NUAA program.

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
        """
        if show_banner_fn:
            show_banner_fn()

        # Validate inputs
        program_name = validate_program_name(program_name, console)
        target_population = validate_text_field(target_population, "target_population", 500, console)
        duration = validate_text_field(duration, "duration", 100, console)

        # Determine feature directory
        if feature:
            slug = _slugify(feature)
            feature_dir, num_str, _ = _next_feature_dir(slug)
        else:
            feature_dir, num_str, slug = _next_feature_dir(program_name)

        created = datetime.now().strftime("%Y-%m-%d")
        mapping = {
            "PROGRAM_NAME": program_name,
            "TARGET_POPULATION": target_population,
            "DURATION": duration,
            "DATE": created,
            "FEATURE_ID": num_str,
            "SLUG": slug,
        }

        # stakeholder-engagement-plan.md
        try:
            template = _load_template("stakeholder-engagement-plan.md")
            filled = _apply_replacements(template, mapping)
            meta = {
                "title": f"{program_name} - Stakeholder Engagement Plan",
                "created": created,
                "feature": f"{num_str}-{slug}",
                "status": "draft",
            }
            text = _prepend_metadata(filled, meta)
            dest = feature_dir / "stakeholder-engagement-plan.md"
            write_markdown_if_needed(dest, text, force=force, console=console)

            console.print(
                Panel(
                    f"Stakeholder engagement plan created: [cyan]{dest}[/cyan]\n\n"
                    f"This plan provides:\n"
                    f"  • Stakeholder mapping and analysis\n"
                    f"  • Engagement strategies for each stakeholder group\n"
                    f"  • Communication channels and timeline\n"
                    f"  • Cultural safety considerations\n\n"
                    f"Next steps:\n"
                    f"  1. Review and customize stakeholder groups\n"
                    f"  2. Set engagement priorities and activities\n"
                    f"  3. Develop communication materials",
                    title="Engagement Plan Ready",
                    border_style="green",
                )
            )
        except FileNotFoundError:
            console.print("[red]Template not found:[/red] stakeholder-engagement-plan.md")
            console.print("[dim]Run 'nuaa init' to set up templates[/dim]")
            raise typer.Exit(1)
        except PermissionError:
            console.print("[red]Permission denied:[/red] Cannot read template or write output file")
            raise typer.Exit(1)
        except OSError as e:
            console.print(f"[red]File system error:[/red] {e}")
            raise typer.Exit(1)
