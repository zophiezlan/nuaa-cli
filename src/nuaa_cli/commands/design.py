from datetime import datetime
import re
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from ..scaffold import (
    _next_feature_dir,
    _ensure_nuaa_root,
    _slugify,
    _load_template,
    _apply_replacements,
    _prepend_metadata,
    write_markdown_if_needed,
    _stamp,
)
from ..utils import validate_program_name, validate_text_field


def register(app, show_banner_fn=None, console: Console | None = None):
    console = console or Console()

    @app.command()
    def design(
        program_name: str = typer.Argument(
            ..., help="Program name (used to derive feature folder)"
        ),
        target_population: str = typer.Argument(..., help="Target population description"),
        duration: str = typer.Argument(..., help="Program duration (e.g., '6 months')"),
        here: bool = typer.Option(True, help="Create under ./nuaa (current project)"),
        feature: Optional[str] = typer.Option(
            None, help="Override feature slug (e.g., '001-custom-slug')"
        ),
        force: bool = typer.Option(False, help="Overwrite existing files if present"),
    ):
        """Create a new NUAA program design with logic model and framework.

        This command initializes a comprehensive program design package for harm reduction
        initiatives. It creates a feature-numbered directory containing three foundational
        documents that guide the entire program lifecycle:

        - **program-design.md**: Core program architecture including goals, target population,
          cultural safety considerations, and implementation approach
        - **logic-model.md**: Theory of change mapping inputs, activities, outputs, and
          intended outcomes following evidence-based harm reduction principles
        - **impact-framework.md**: Measurement strategy defining KPIs, data collection methods,
          and evaluation approach aligned with NUAA's equity-focused values

        The command automatically generates a sequential feature ID (e.g., 001-, 002-) based
        on existing programs, or you can specify a custom feature slug. All documents are
        pre-populated with NUAA-specific templates emphasizing peer-led approaches, cultural
        safety, and trauma-informed practices.

        This is typically the first command in the NUAA program workflow, establishing the
        foundation for subsequent funding proposals, stakeholder engagement, and impact
        measurement activities.

        Args:
            program_name: Name of the harm reduction program or initiative (e.g.,
                "Peer Support Network", "Safe Consumption Spaces"). Used to derive the
                feature folder name and populate all template documents.
            target_population: Description of primary beneficiaries (e.g.,
                "People who use drugs in Western Sydney", "LGBTIQ+ PWUD aged 18-30").
                Should reflect NUAA's person-centered language principles.
            duration: Intended program duration (e.g., "6 months", "2 years", "ongoing").
                Used for planning timelines and evaluation schedules.
            here: If True (default), creates the feature under ./nuaa in the current project.
                Set to False for alternative locations.
            feature: Optional custom feature slug to override auto-generated numbering.
                Can be full format "001-custom-slug" or just "custom-slug" (number will
                be auto-assigned). Useful for maintaining specific naming conventions.
            force: If True, overwrites existing files in the feature directory. Default
                is False to prevent accidental data loss.

        Raises:
            typer.Exit: Exits with code 1 if template files are not found (requires 'nuaa init'),
                if permission is denied for file operations, or if other filesystem errors occur.

        Examples:
            Create a new peer support program design:
                $ nuaa design "Peer Support Network" "PWUD in Western Sydney" "12 months"

            Design a culturally-specific program with custom feature slug:
                $ nuaa design "Aboriginal Peer Program" "Aboriginal and Torres Strait Islander PWUD" "2 years" --feature aboriginal-peer-support

            Create a harm reduction initiative for young people:
                $ nuaa design "Youth Engagement Program" "Young PWUD aged 16-25" "6 months"

            Overwrite an existing design (use with caution):
                $ nuaa design "Naloxone Distribution" "PWUD in Sydney CBD" "ongoing" --force
        """
        if show_banner_fn:
            show_banner_fn()

        # Validate inputs
        program_name = validate_program_name(program_name, console)
        target_population = validate_text_field(
            target_population, "target_population", 500, console
        )
        duration = validate_text_field(duration, "duration", 100, console)

        # Determine feature directory
        if feature:
            # If full number provided, respect it; otherwise create next
            if re.match(r"^\d{3}-", feature):
                feature_dir = _ensure_nuaa_root() / feature
                feature_dir.mkdir(parents=True, exist_ok=True)
                num_str = feature[:3]
                slug = feature.split("-", 1)[1]
            else:
                # Treat as slug only; compute next number
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

        # program-design.md
        try:
            pd_template = _load_template("program-design.md")
            pd_filled = _apply_replacements(pd_template, mapping)
            pd_meta = {
                "title": f"{program_name} - Program Design",
                "created": created,
                "feature": f"{num_str}-{slug}",
                "status": "draft",
            }
            pd_text = _prepend_metadata(pd_filled, pd_meta)
            dest = feature_dir / "program-design.md"
            write_markdown_if_needed(dest, pd_text, force=force, console=console)
        except FileNotFoundError:
            console.print("[red]Template not found:[/red] program-design.md")
            console.print("[dim]Run 'nuaa init' to set up templates[/dim]")
            raise typer.Exit(1)
        except PermissionError:
            console.print("[red]Permission denied:[/red] Cannot read template or write output file")
            raise typer.Exit(1)
        except OSError as e:
            console.print(f"[red]File system error:[/red] {e}")
            raise typer.Exit(1)

        # logic-model.md
        try:
            lm_template = _load_template("logic-model.md")
            lm_text = _prepend_metadata(
                _apply_replacements(lm_template, mapping),
                {
                    "title": f"{program_name} - Logic Model",
                    "feature": f"{num_str}-{slug}",
                },
            )
            dest = feature_dir / "logic-model.md"
            write_markdown_if_needed(dest, lm_text, force=force, console=console)
        except FileNotFoundError:
            console.print("[red]Template not found:[/red] logic-model.md")
            console.print("[dim]Run 'nuaa init' to set up templates[/dim]")
        except PermissionError:
            console.print("[red]Permission denied:[/red] Cannot read template or write output file")
        except OSError as e:
            console.print(f"[red]File system error:[/red] {e}")

        # impact-framework.md (skeleton from template)
        try:
            if_template = _load_template("impact-framework.md")
            if_text = _prepend_metadata(
                _apply_replacements(if_template, mapping),
                {
                    "title": f"{program_name} - Impact Framework",
                    "feature": f"{num_str}-{slug}",
                },
            )
            dest = feature_dir / "impact-framework.md"
            write_markdown_if_needed(dest, if_text, force=force, console=console)
        except FileNotFoundError:
            console.print("[red]Template not found:[/red] impact-framework.md")
            console.print("[dim]Run 'nuaa init' to set up templates[/dim]")
        except PermissionError:
            console.print("[red]Permission denied:[/red] Cannot read template or write output file")
        except OSError as e:
            console.print(f"[red]File system error:[/red] {e}")

        # Changelog bootstrap
        changelog = feature_dir / "CHANGELOG.md"
        if not changelog.exists():
            content = (
                f"# Changelog for {num_str}-{slug}\n\n- {_stamp()} - Initialized program design\n"
            )
            write_markdown_if_needed(changelog, content, force=True, console=console)

        console.print(
            Panel(
                f"Feature ready: [cyan]{feature_dir}[/cyan]",
                title="Design Created",
                border_style="green",
            )
        )
