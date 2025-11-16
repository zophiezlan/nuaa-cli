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


def register(app, show_banner_fn=None, console: Console | None = None):
    console = console or Console()

    @app.command()
    def partner(
        program_name: str = typer.Argument(
            ..., help="Program or partnership name"
        ),
        partner_org: str = typer.Argument(
            ..., help="Partner organization name"
        ),
        duration: str = typer.Argument(
            ..., help="Agreement duration (e.g., '2 years')"
        ),
        feature: Optional[str] = typer.Option(
            None, help="Override feature slug (e.g., '001-custom-slug')"
        ),
        force: bool = typer.Option(False, help="Overwrite existing files if present"),
    ):
        """Create a partnership agreement (MOU) template for a NUAA collaboration."""
        if show_banner_fn:
            show_banner_fn()

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
        except Exception as e:
            console.print(
                f"[red]Failed to create partnership-agreement.md:[/red] {e}"
            )
            raise typer.Exit(1)
