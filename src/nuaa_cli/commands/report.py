from datetime import datetime

import typer
from rich.console import Console

from ..scaffold import (
    get_or_create_feature_dir,
    write_markdown_if_needed,
)
from ..utils import validate_program_name, validate_text_field


def register(app, show_banner_fn=None, console: Console | None = None):
    console = console or Console()

    @app.command()
    def report(
        program_name: str = typer.Argument(..., help="Program name (existing)"),
        report_type: str = typer.Option(
            "final",
            "--type",
            help="Report type: progress|mid-program|final|quarterly|annual",
        ),
        force: bool = typer.Option(False, help="Overwrite if exists"),
    ):
        """Generate a simple report scaffold referencing program artifacts.

        This command creates a structured reporting template pre-populated with sections
        that align with common funder requirements and NUAA's accountability standards.
        The scaffold provides a consistent framework for different reporting types while
        allowing customization for specific audiences.

        Generated report includes sections for:
        - **Overview**: Executive summary of reporting period
        - **Key Findings**: Headline achievements and significant developments
        - **Progress Against Logic Model**: Activities, outputs, and outcomes delivered
        - **Equity Analysis**: How the program reached diverse PWUD populations
        - **Budget vs Actuals**: Financial performance and expenditure variance
        - **Lessons Learned and Recommendations**: Insights for improvement

        The scaffold is intentionally lightweight, prompting you to reference existing
        program artifacts (design documents, logic models, impact frameworks) rather
        than duplicating content. This approach ensures reports stay synchronized with
        source documents while reducing reporting burden.

        Different report types serve different purposes:
        - **Progress**: Brief updates for ongoing monitoring (monthly/quarterly)
        - **Mid-program**: Interim assessment at program midpoint
        - **Final**: Comprehensive end-of-program evaluation and outcomes
        - **Quarterly**: Regular funder reporting cycle
        - **Annual**: Year-end review and planning for continuation

        Args:
            program_name: Name of existing program (must match a feature directory).
                The report will be created in this program's folder as report.md.
            report_type: Type of report to generate. Options are "progress", "mid-program",
                "final", "quarterly", or "annual". Default is "final". Customizes the
                scaffold's tone and emphasis (e.g., final reports focus on outcomes,
                progress reports emphasize activities).
            force: If True, overwrites existing report.md file. Default is False to
                prevent accidental loss of report drafts in progress.

        Raises:
            typer.Exit: Not explicitly raised by this command (generates content directly
                rather than loading templates), but file write errors could occur.

        Examples:
            Create final report for completed peer support program:
                $ nuaa report "Peer Support Network" --type final

            Generate quarterly update for ongoing initiative:
                $ nuaa report "Needle Exchange Expansion" --type quarterly

            Prepare mid-program evaluation:
                $ nuaa report "Overdose Prevention Training" --type mid-program

            Annual report for long-running service:
                $ nuaa report "Peer Phone Support Line" --type annual

            Progress report with force overwrite:
                $ nuaa report "Youth Engagement Program" --type progress --force
        """
        if show_banner_fn:
            show_banner_fn()

        # Validate inputs
        program_name = validate_program_name(program_name, console)
        report_type = validate_text_field(report_type, "report_type", 100, console)

        feature_dir = get_or_create_feature_dir(program_name)
        created = datetime.now().strftime("%Y-%m-%d")
        lines = [
            f"# {program_name} - {report_type.title()} Report",
            "",
            f"Generated: {created}",
            "",
            "This is a scaffold report. Populate the sections based on your " "impact framework and collected data.",
            "",
            "## Overview",
            "",
            "## Key Findings",
            "",
            "## Progress Against Logic Model",
            "",
            "## Equity Analysis",
            "",
            "## Budget vs Actuals",
            "",
            "## Lessons Learned and Recommendations",
            "",
        ]
        content = "\n".join(lines) + "\n"
        dest = feature_dir / "report.md"
        write_markdown_if_needed(dest, content, force=force, console=console)
