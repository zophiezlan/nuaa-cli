import os
from pathlib import Path
from typing import Iterable

from typer.testing import CliRunner  # type: ignore[import-not-found]

# Import the Typer app from the CLI module
from nuaa_cli.__init__ import app  # type: ignore


def _copy_templates(templates_src: Path, kit_dir: Path, names: Iterable[str]) -> None:
    for name in names:
        src = templates_src / name
        dst = kit_dir / name
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")


def test_version_runs():
    runner = CliRunner()
    # prints info; we only care it runs successfully
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0


def test_design_scaffolds(tmp_path: Path):
    # Create a temp project with nuaa-kit/templates copied from repo
    repo_root = Path(__file__).resolve().parents[1]
    templates_src = repo_root / "nuaa-kit" / "templates"
    assert templates_src.is_dir(), "templates not found; run tests from repository root"

    # Make a temp project root and symlink/copy templates tree
    project_root = tmp_path
    kit_dir = project_root / "nuaa-kit" / "templates"
    kit_dir.mkdir(parents=True, exist_ok=True)

    # Copy only the minimal templates used by design
    _copy_templates(
        templates_src,
        kit_dir,
        ["program-design.md", "logic-model.md", "impact-framework.md"],
    )

    # Run the CLI from this directory
    cwd = os.getcwd()
    os.chdir(project_root)
    try:
        runner = CliRunner()
        result = runner.invoke(
            app,
            [
                "design",
                "Peer Naloxone Distribution",
                "people at risk of opioid overdose",
                "12 months",
            ],
        )
        assert result.exit_code == 0, result.output

        # Verify outputs created
        nuaa_dir = project_root / "nuaa"
        assert nuaa_dir.is_dir()
        features = [p for p in nuaa_dir.iterdir() if p.is_dir()]
        assert features, "feature folder not created"
        feature = features[0]
        assert (feature / "program-design.md").is_file()
        assert (feature / "logic-model.md").is_file()
        assert (feature / "impact-framework.md").is_file()
        assert (feature / "CHANGELOG.md").is_file()
    finally:
        os.chdir(cwd)


def test_additional_scaffolds(tmp_path: Path):
    repo_root = Path(__file__).resolve().parents[1]
    templates_src = repo_root / "nuaa-kit" / "templates"
    assert templates_src.is_dir(), "templates not found; run tests from repository root"

    project_root = tmp_path
    kit_dir = project_root / "nuaa-kit" / "templates"
    kit_dir.mkdir(parents=True, exist_ok=True)

    _copy_templates(
        templates_src,
        kit_dir,
        [
            "program-design.md",
            "logic-model.md",
            "impact-framework.md",
            "proposal.md",
            "existing-program-analysis.md",
        ],
    )

    cwd = os.getcwd()
    os.chdir(project_root)
    try:
        runner = CliRunner()
        program_name = "Community Harm Reduction"

        result = runner.invoke(
            app,
            [
                "design",
                program_name,
                "people who use drugs",
                "18 months",
            ],
        )
        assert result.exit_code == 0, result.output

        nuaa_dir = project_root / "nuaa"
        feature_dirs = [p for p in nuaa_dir.iterdir() if p.is_dir()]
        assert feature_dirs, "expected a feature directory after design"
        feature_dir = feature_dirs[0]

        result = runner.invoke(
            app,
            [
                "propose",
                program_name,
                "Local Health District",
                "$75000",
                "18 months",
            ],
        )
        assert result.exit_code == 0, result.output
        assert (feature_dir / "proposal.md").is_file()

        result = runner.invoke(
            app,
            [
                "measure",
                program_name,
                "FY25",
                "$5000",
                "--force",
            ],
        )
        assert result.exit_code == 0, result.output
        impact_text = (feature_dir / "impact-framework.md").read_text(encoding="utf-8")
        assert program_name in impact_text

        result = runner.invoke(app, ["document", program_name, "--force"])
        assert result.exit_code == 0, result.output
        assert (feature_dir / "existing-program-analysis.md").is_file()

        result = runner.invoke(
            app,
            ["report", program_name, "--type", "quarterly", "--force"],
        )
        assert result.exit_code == 0, result.output
        report_text = (feature_dir / "report.md").read_text(encoding="utf-8")
        assert "Quarterly Report" in report_text

        result = runner.invoke(
            app,
            ["refine", program_name, "--note", "Updated metrics"],
        )
        assert result.exit_code == 0, result.output
        changelog_text = (feature_dir / "CHANGELOG.md").read_text(encoding="utf-8")
        assert "Updated metrics" in changelog_text
    finally:
        os.chdir(cwd)
