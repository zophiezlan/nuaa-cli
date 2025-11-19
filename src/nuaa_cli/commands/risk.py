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
    def risk(
        program_name: str = typer.Argument(..., help="Program name (used to derive feature folder)"),
        duration: str = typer.Argument(..., help="Program duration (e.g., '12 months')"),
        feature: Optional[str] = typer.Option(None, help="Override feature slug (e.g., '001-custom-slug')"),
        force: bool = typer.Option(False, help="Overwrite existing files if present"),
    ):
        """Create a risk register for proactive risk management.

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

        Args:
            program_name: Name of the program or initiative requiring risk management
                (e.g., "Supervised Injection Facility", "Mobile Needle Exchange").
                Used to create a feature directory and populate the template.
            duration: Program duration or risk review cycle (e.g., "12 months", "ongoing",
                "2-year pilot"). Used to plan risk review frequency and long-term
                risk evolution.
            feature: Optional custom feature slug to override auto-generated numbering.
                Useful for maintaining consistent naming across program documentation.
            force: If True, overwrites existing risk-register.md file. Default is False
                to preserve risk assessments, incident logs, and mitigation progress.

        Raises:
            typer.Exit: Exits with code 1 if the risk register template is not found
                (requires 'nuaa init'), if permission is denied for file operations, or
                if other filesystem errors occur.

        Examples:
            Create risk register for new supervised injection facility:
                $ nuaa risk "Supervised Injection Facility" "2-year pilot"

            Establish risk management for peer workforce program:
                $ nuaa risk "Peer Support Network" "12 months"

            Document risks for advocacy campaign:
                $ nuaa risk "Drug Law Reform Campaign" "ongoing"

            Set up risk register for mobile service with custom slug:
                $ nuaa risk "Mobile Needle Exchange" "18 months" --feature mobile-nsp-risks
        """
        if show_banner_fn:
            show_banner_fn()

        # Validate inputs
        program_name = validate_program_name(program_name, console)
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
            "DURATION": duration,
            "DATE": created,
            "FEATURE_ID": num_str,
            "SLUG": slug,
        }

        # risk-register.md
        try:
            template = _load_template("risk-register.md")
            filled = _apply_replacements(template, mapping)
            meta = {
                "title": f"{program_name} - Risk Register",
                "created": created,
                "feature": f"{num_str}-{slug}",
                "status": "active",
            }
            text = _prepend_metadata(filled, meta)
            dest = feature_dir / "risk-register.md"
            write_markdown_if_needed(dest, text, force=force, console=console)

            console.print(
                Panel(
                    f"Risk register created: [cyan]{dest}[/cyan]\n\n"
                    f"This register includes:\n"
                    f"  • Risk assessment framework (likelihood × impact)\n"
                    f"  • 8 risk categories with examples:\n"
                    f"    - Program delivery risks\n"
                    f"    - Stakeholder & partnership risks\n"
                    f"    - Financial & resource risks\n"
                    f"    - Staffing & HR risks\n"
                    f"    - Health & safety risks\n"
                    f"    - Ethical & legal risks\n"
                    f"    - Reputational risks\n"
                    f"    - Cultural safety risks\n"
                    f"  • Risk summary dashboard\n"
                    f"  • Review and incident reporting processes\n\n"
                    f"Next steps:\n"
                    f"  1. Review and customize risk examples\n"
                    f"  2. Add program-specific risks\n"
                    f"  3. Schedule monthly risk reviews",
                    title="Risk Register Ready",
                    border_style="green",
                )
            )
        except FileNotFoundError:
            console.print("[red]Template not found:[/red] risk-register.md")
            console.print("[dim]Run 'nuaa init' to set up templates[/dim]")
            raise typer.Exit(1)
        except PermissionError:
            console.print("[red]Permission denied:[/red] Cannot read template or write output file")
            raise typer.Exit(1)
        except OSError as e:
            console.print(f"[red]File system error:[/red] {e}")
            raise typer.Exit(1)
