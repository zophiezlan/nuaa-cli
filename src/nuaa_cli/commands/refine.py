import typer
from rich.console import Console

from ..scaffold import _find_feature_dir_by_program, _write_markdown, _stamp
from ..utils import validate_program_name, validate_text_field


def register(app, show_banner_fn=None, console: Console | None = None):
    console = console or Console()

    @app.command()
    def refine(
        program_name: str = typer.Argument(..., help="Program name (existing)"),
        note: str = typer.Option("Refinement applied", "--note", help="Changelog note to record"),
    ):
        """Record a refinement entry in the feature CHANGELOG.md.

        This command appends timestamped entries to a program's changelog, creating an
        audit trail of program evolution, adaptations, and continuous improvement activities.
        Maintaining a detailed changelog is essential for accountability, knowledge transfer,
        and demonstrating responsive program management to funders and stakeholders.

        The changelog serves multiple purposes:
        - **Documentation**: Record what changed, when, and why
        - **Compliance**: Demonstrate adherence to grant agreements and ethical protocols
        - **Learning**: Track which adaptations improved outcomes vs. those that didn't
        - **Continuity**: Help new staff understand program history and decisions
        - **Reporting**: Provide evidence of adaptive management in funder reports

        Each changelog entry is automatically timestamped and formatted consistently,
        making it easy to review program history chronologically. This lightweight
        documentation approach captures incremental changes that might otherwise be
        lost, building institutional memory over time.

        NUAA's peer-led approach values the insights of frontline workers. Use this
        command to record program refinements suggested by peer workers, participant
        feedback, or evaluation findings - honoring the expertise of lived experience.

        Args:
            program_name: Name of existing program (must match a feature directory created
                with 'nuaa design'). The changelog entry will be appended to
                CHANGELOG.md in this program's folder.
            note: Description of the refinement, update, or change being recorded.
                Default is "Refinement applied" but should be customized to describe
                specific changes (e.g., "Adjusted service hours based on peer feedback",
                "Added trauma-informed practice training for staff").

        Raises:
            typer.Exit: Exits with code 1 if the feature directory for the program cannot
                be found. Ensure the program exists (created with 'nuaa design' or similar).

        Examples:
            Record program adaptation based on participant feedback:
                $ nuaa refine "Peer Support Network" --note "Extended evening hours to 9pm based on participant requests"

            Document policy change for cultural safety:
                $ nuaa refine "Aboriginal Peer Program" --note "Implemented Welcome to Country at all group sessions"

            Track training implementation:
                $ nuaa refine "Overdose Prevention" --note "All peer workers completed trauma-informed care refresher training"

            Log partnership development:
                $ nuaa refine "Needle Exchange" --note "Established referral pathway with local sexual health clinic"

            Simple refinement with default note:
                $ nuaa refine "Youth Engagement Program"
        """
        if show_banner_fn:
            show_banner_fn()

        # Validate inputs
        program_name = validate_program_name(program_name, console)
        note = validate_text_field(note, "note", 500, console)

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
