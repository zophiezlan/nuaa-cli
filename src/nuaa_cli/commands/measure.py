from datetime import datetime

import typer
from rich.console import Console

from ..scaffold import (
    get_or_create_feature_dir,
    _load_template,
    _apply_replacements,
    _prepend_metadata,
    write_markdown_if_needed,
)
from ..utils import validate_program_name, validate_text_field


def register(app, show_banner_fn=None, console: Console | None = None):
    console = console or Console()

    @app.command()
    def measure(
        program_name: str = typer.Argument(..., help="Program name (existing)"),
        evaluation_period: str = typer.Argument(..., help="Evaluation period"),
        budget: str = typer.Argument(..., help="Evaluation budget (e.g., $7000)"),
        force: bool = typer.Option(False, help="Overwrite if exists"),
    ):
        """Create or update the impact framework document from the template.

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
        """
        if show_banner_fn:
            show_banner_fn()

        # Validate inputs
        program_name = validate_program_name(program_name, console)
        evaluation_period = validate_text_field(evaluation_period, "evaluation_period", 100, console)
        budget = validate_text_field(budget, "budget", 100, console)

        feature_dir = get_or_create_feature_dir(program_name)
        mapping = {
            "PROGRAM_NAME": program_name,
            "EVALUATION_PERIOD": evaluation_period,
            "BUDGET": budget,
            "DATE": datetime.now().strftime("%Y-%m-%d"),
        }
        try:
            template = _load_template("impact-framework.md")
            text = _prepend_metadata(
                _apply_replacements(template, mapping),
                {"title": f"{program_name} - Impact Framework"},
            )
            dest = feature_dir / "impact-framework.md"
            write_markdown_if_needed(dest, text, force=force, console=console)
        except FileNotFoundError:
            console.print("[red]Template not found:[/red] impact-framework.md")
            console.print("[dim]Run 'nuaa init' to set up templates[/dim]")
            raise typer.Exit(1)
        except PermissionError:
            console.print("[red]Permission denied:[/red] Cannot read template or write output file")
            raise typer.Exit(1)
        except OSError as e:
            console.print(f"[red]File system error:[/red] {e}")
            raise typer.Exit(1)
