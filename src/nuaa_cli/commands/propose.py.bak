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
    def propose(
        program_name: str = typer.Argument(..., help="Program name (existing or new)"),
        funder: str = typer.Argument(..., help="Funder name"),
        amount: str = typer.Argument(..., help="Amount requested, e.g., $50000"),
        duration: str = typer.Argument(..., help="Duration e.g., '12 months'"),
        force: bool = typer.Option(False, help="Overwrite if proposal.md exists"),
    ):
        """Create a funding proposal from the template, linked to design.

        This command generates a comprehensive funding proposal document based on NUAA's
        proven proposal template. The proposal automatically links to an existing program
        design (created with 'nuaa design') or creates a new feature directory if needed.

        The generated proposal includes:
        - Executive summary aligned with harm reduction principles
        - Detailed program description referencing the logic model
        - Budget justification and financial sustainability plan
        - Evidence base and alignment with best practices
        - Evaluation framework tied to impact measurements
        - Organizational capacity and peer workforce credentials

        The proposal template is pre-structured to meet common funder requirements while
        emphasizing NUAA's unique peer-led approach, lived experience expertise, and
        commitment to reducing drug-related harm without judgment.

        This command is typically used after 'nuaa design' has established the program
        foundation, enabling you to quickly adapt the design for specific funding
        opportunities while maintaining consistency across applications.

        Args:
            program_name: Name of the program seeking funding. Should match an existing
                program created with 'nuaa design', or a new program name to create a
                feature directory automatically.
            funder: Name of the funding organization or grant program (e.g.,
                "NSW Health", "Commonwealth Department of Health", "Philanthropic Trust").
                Used to customize the proposal audience and alignment.
            amount: Funding amount requested, including currency symbol (e.g., "$50000",
                "$250,000", "€100k"). Used in budget sections and executive summary.
            duration: Funding period requested (e.g., "12 months", "2 years", "3-year pilot").
                Should align with program design duration and funder guidelines.
            force: If True, overwrites existing proposal.md file in the feature directory.
                Default is False to prevent accidental loss of proposal drafts.

        Raises:
            typer.Exit: Exits with code 1 if the proposal template is not found (requires
                'nuaa init'), if permission is denied for file operations, or if other
                filesystem errors occur.

        Examples:
            Create a proposal for an existing peer support program:
                $ nuaa propose "Peer Support Network" "NSW Health" "$75000" "12 months"

            Submit to a federal harm reduction grant:
                $ nuaa propose "Overdose Prevention" "Commonwealth Dept of Health" "$200000" "2 years"

            Apply for philanthropic funding:
                $ nuaa propose "Cultural Safety Training" "Harm Reduction Trust" "$45000" "18 months"

            Update an existing proposal with new budget (use force):
                $ nuaa propose "Needle Exchange Expansion" "Local Health District" "$120000" "1 year" --force
        """
        if show_banner_fn:
            show_banner_fn()

        # Validate inputs
        program_name = validate_program_name(program_name, console)
        funder = validate_text_field(funder, "funder", 200, console)
        amount = validate_text_field(amount, "amount", 50, console)
        duration = validate_text_field(duration, "duration", 100, console)

        feature_dir = get_or_create_feature_dir(program_name)
        created = datetime.now().strftime("%Y-%m-%d")
        mapping = {
            "PROGRAM_NAME": program_name,
            "FUNDER": funder,
            "AMOUNT": amount,
            "DURATION": duration,
            "DATE": created,
        }
        try:
            template = _load_template("proposal.md")
            filled = _apply_replacements(template, mapping)
            meta = {
                "title": f"{program_name} - Proposal",
                "funder": funder,
                "amount": amount,
                "created": created,
            }
            text = _prepend_metadata(filled, meta)
            dest = feature_dir / "proposal.md"
            write_markdown_if_needed(dest, text, force=force, console=console)
        except FileNotFoundError:
            console.print("[red]Template not found:[/red] proposal.md")
            console.print("[dim]Run 'nuaa init' to set up templates[/dim]")
            raise typer.Exit(1)
        except PermissionError:
            console.print("[red]Permission denied:[/red] Cannot read template or write output file")
            raise typer.Exit(1)
        except OSError as e:
            console.print(f"[red]File system error:[/red] {e}")
            raise typer.Exit(1)
