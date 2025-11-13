import typer
from rich.console import Console

from ..scaffold import _find_feature_dir_by_program, _write_markdown, _stamp


def register(app, show_banner_fn=None, console: Console | None = None):
    console = console or Console()

    @app.command()
    def refine(
        program_name: str = typer.Argument(..., help="Program name (existing)"),
        note: str = typer.Option("Refinement applied", "--note", help="Changelog note to record"),
    ):
        """Record a refinement entry in the feature CHANGELOG.md."""
        if show_banner_fn:
            show_banner_fn()
        feature_dir = _find_feature_dir_by_program(program_name)
        if not feature_dir:
            console.print("[red]Could not find feature directory for program[/red]")
            raise typer.Exit(1)
        changelog = feature_dir / "CHANGELOG.md"
        entry = f"- {_stamp()} - {note}\n"
        if changelog.exists():
            with open(changelog, "a", encoding="utf-8") as f:
                f.write(entry)
        else:
            _write_markdown(changelog, f"# Changelog for {feature_dir.name}\n\n" + entry)
        console.print(f"[green]Updated:[/green] {changelog}")
