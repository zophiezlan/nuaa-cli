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
        """Create a new NUAA program design with logic model and framework."""
        if show_banner_fn:
            show_banner_fn()
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
        except Exception as e:
            console.print(f"[red]Failed to create program-design.md:[/red] {e}")
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
        except Exception as e:
            console.print(f"[red]Failed to create logic-model.md:[/red] {e}")

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
        except Exception as e:
            console.print(f"[red]Failed to create impact-framework.md:[/red] {e}")

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
