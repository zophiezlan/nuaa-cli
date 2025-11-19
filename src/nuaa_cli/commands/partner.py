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
    def partner(
        program_name: str = typer.Argument(..., help="Program or partnership name"),
        partner_org: str = typer.Argument(..., help="Partner organization name"),
        duration: str = typer.Argument(..., help="Agreement duration (e.g., '2 years')"),
        feature: Optional[str] = typer.Option(None, help="Override feature slug (e.g., '001-custom-slug')"),
        force: bool = typer.Option(False, help="Overwrite existing files if present"),
    ):
        """Create a partnership agreement (MOU) template for a NUAA collaboration.

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

        Args:
            program_name: Name of the program or initiative being partnered on, or a
                descriptive name for the partnership itself (e.g., "Integrated Care Pathway",
                "Regional Needle Exchange Alliance").
            partner_org: Full legal name of the partner organization (e.g., "Sydney Local
                Health District", "Aboriginal Health Service", "Youth Justice NSW").
                Used throughout the MOU template.
            duration: Length of the partnership agreement (e.g., "2 years", "3-year pilot",
                "ongoing subject to annual review"). Establishes commitment timeframe and
                review schedule.
            feature: Optional custom feature slug to override auto-generated numbering.
                Useful for grouping related partnerships or maintaining naming conventions.
            force: If True, overwrites existing partnership-agreement.md file. Default is
                False to protect negotiated agreement language.

        Raises:
            typer.Exit: Exits with code 1 if the partnership agreement template is not found
                (requires 'nuaa init'), if permission is denied for file operations, or if
                other filesystem errors occur.

        Examples:
            Create MOU with a local health district:
                $ nuaa partner "Integrated Harm Reduction Services" "Sydney Local Health District" "2 years"

            Formalize partnership with Aboriginal health service:
                $ nuaa partner "Cultural Safety Training" "Aboriginal Medical Service" "3 years"

            Document alliance with peer organization:
                $ nuaa partner "National Advocacy Coalition" "Australian Injecting & Illicit Drug Users League" "ongoing"

            Establish collaboration with government agency:
                $ nuaa partner "Peer Workforce Pilot" "NSW Health" "18 months" --feature govt-partnership
        """
        if show_banner_fn:
            show_banner_fn()

        # Validate inputs
        program_name = validate_program_name(program_name, console)
        partner_org = validate_text_field(partner_org, "partner_org", 200, console)
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
            "PARTNER_ORG": partner_org,
            "DURATION": duration,
            "DATE": created,
            "FEATURE_ID": num_str,
            "SLUG": slug,
        }

        # partnership-agreement.md
        try:
            template = _load_template("partnership-agreement.md")
            filled = _apply_replacements(template, mapping)
            meta = {
                "title": f"{program_name} - Partnership Agreement with {partner_org}",
                "created": created,
                "feature": f"{num_str}-{slug}",
                "status": "draft",
                "partner": partner_org,
            }
            text = _prepend_metadata(filled, meta)
            dest = feature_dir / "partnership-agreement.md"
            write_markdown_if_needed(dest, text, force=force, console=console)

            console.print(
                Panel(
                    f"Partnership agreement created: [cyan]{dest}[/cyan]\n\n"
                    f"This MOU template includes:\n"
                    f"  • Purpose and scope of partnership\n"
                    f"  • Roles and responsibilities (NUAA & {partner_org})\n"
                    f"  • Governance and decision-making\n"
                    f"  • Information sharing protocols\n"
                    f"  • Financial arrangements\n"
                    f"  • Dispute resolution process\n\n"
                    f"Next steps:\n"
                    f"  1. Complete all [bracketed] sections\n"
                    f"  2. Review with {partner_org}\n"
                    f"  3. Finalize and sign agreement",
                    title="Partnership Agreement Ready",
                    border_style="green",
                )
            )
        except FileNotFoundError:
            console.print("[red]Template not found:[/red] partnership-agreement.md")
            console.print("[dim]Run 'nuaa init' to set up templates[/dim]")
            raise typer.Exit(1)
        except PermissionError:
            console.print("[red]Permission denied:[/red] Cannot read template or write output file")
            raise typer.Exit(1)
        except OSError as e:
            console.print(f"[red]File system error:[/red] {e}")
            raise typer.Exit(1)
