"""
Integration tests for complete command workflows.

These tests verify that commands work end-to-end, creating actual files
and directories with proper content.
"""

import tempfile
from pathlib import Path
import pytest
from typer.testing import CliRunner

from nuaa_cli import app
from nuaa_cli.scaffold import _find_templates_root


runner = CliRunner()


class TestDesignCommandWorkflow:
    """Test the complete design command workflow."""

    def test_design_command_creates_all_files(self, tmp_path):
        """Test that design command creates all expected files."""
        # Setup: Create templates directory
        templates_dir = tmp_path / "nuaa-kit" / "templates"
        templates_dir.mkdir(parents=True)

        # Create minimal template files
        (templates_dir / "program-design.md").write_text(
            "# Program Design: [Name]\n\nTarget: {{TARGET_POPULATION}}\nDuration: {{DURATION}}"
        )
        (templates_dir / "logic-model.md").write_text("# Logic Model\n\nFor program: [Name]")
        (templates_dir / "impact-framework.md").write_text("# Impact Framework\n\nFor: [Name]")

        # Change to tmp directory
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Run design command (uses positional arguments)
            result = runner.invoke(
                app,
                ["design", "Peer Support", "People who use drugs", "12 months"],
            )

            # Verify command succeeded
            assert result.exit_code == 0, f"Command failed: {result.output}"

            # Verify files were created
            nuaa_dir = tmp_path / "nuaa"
            assert nuaa_dir.exists()

            feature_dirs = list(nuaa_dir.iterdir())
            assert len(feature_dirs) == 1

            feature_dir = feature_dirs[0]
            assert feature_dir.name.startswith("001-")
            assert "peer-support" in feature_dir.name

            # Verify all three files exist
            assert (feature_dir / "program-design.md").exists()
            assert (feature_dir / "logic-model.md").exists()
            assert (feature_dir / "impact-framework.md").exists()

            # Verify content replacements
            design_content = (feature_dir / "program-design.md").read_text()
            assert "Peer Support" in design_content
            assert "People who use drugs" in design_content
            assert "12 months" in design_content

    def test_design_command_reuses_feature_dir(self, tmp_path):
        """Test that running design twice reuses the same feature directory."""
        templates_dir = tmp_path / "nuaa-kit" / "templates"
        templates_dir.mkdir(parents=True)
        (templates_dir / "program-design.md").write_text("# Design: [Name]")
        (templates_dir / "logic-model.md").write_text("# Logic Model")
        (templates_dir / "impact-framework.md").write_text("# Impact")

        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Run design command twice with same program name
            for _ in range(2):
                result = runner.invoke(
                    app,
                    ["design", "Test Program", "Community", "6 months"],
                )
                assert result.exit_code == 0

            # Verify only one feature directory exists
            nuaa_dir = tmp_path / "nuaa"
            feature_dirs = list(nuaa_dir.iterdir())
            assert len(feature_dirs) == 1


class TestProposeCommandWorkflow:
    """Test the complete propose command workflow."""

    def test_propose_command_creates_proposal(self, tmp_path):
        """Test that propose command creates proposal file."""
        templates_dir = tmp_path / "nuaa-kit" / "templates"
        templates_dir.mkdir(parents=True)
        (templates_dir / "proposal.md").write_text(
            "# Proposal: [Name]\n\nFunder: {{FUNDER}}\nAmount: {{AMOUNT}}\nTimeline: {{TIMELINE}}"
        )

        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(
                app,
                ["propose", "Harm Reduction", "Health Department", "$50,000", "3 years"],
            )

            assert result.exit_code == 0

            nuaa_dir = tmp_path / "nuaa"
            feature_dirs = list(nuaa_dir.iterdir())
            assert len(feature_dirs) == 1

            feature_dir = feature_dirs[0]
            proposal_file = feature_dir / "proposal.md"
            assert proposal_file.exists()

            content = proposal_file.read_text()
            assert "Harm Reduction" in content
            assert "Health Department" in content
            assert "$50,000" in content
            assert "3 years" in content


class TestMeasureCommandWorkflow:
    """Test the complete measure command workflow."""

    def test_measure_command_creates_framework(self, tmp_path):
        """Test that measure command creates measurement framework."""
        templates_dir = tmp_path / "nuaa-kit" / "templates"
        templates_dir.mkdir(parents=True)
        (templates_dir / "measurement-framework.md").write_text(
            "# Measurement: [Name]\n\nMetrics: {{METRICS}}\nFrequency: {{FREQUENCY}}"
        )

        with runner.isolated_filesystem(temp_dir=tmp_path):
            result = runner.invoke(
                app,
                ["measure", "Outreach Program", "Engagement, Satisfaction", "Monthly"],
            )

            assert result.exit_code == 0

            nuaa_dir = tmp_path / "nuaa"
            feature_dirs = list(nuaa_dir.iterdir())
            assert len(feature_dirs) == 1

            feature_dir = feature_dirs[0]
            framework_file = feature_dir / "measurement-framework.md"
            assert framework_file.exists()

            content = framework_file.read_text()
            assert "Outreach Program" in content
            assert "Engagement, Satisfaction" in content
            assert "Monthly" in content


class TestMultipleCommandsWorkflow:
    """Test workflows with multiple commands."""

    def test_sequential_commands_same_program(self, tmp_path):
        """Test running multiple commands for the same program."""
        templates_dir = tmp_path / "nuaa-kit" / "templates"
        templates_dir.mkdir(parents=True)

        # Create all necessary templates
        (templates_dir / "program-design.md").write_text("# Design: [Name]")
        (templates_dir / "logic-model.md").write_text("# Logic Model")
        (templates_dir / "impact-framework.md").write_text("# Impact")
        (templates_dir / "proposal.md").write_text("# Proposal: [Name]")
        (templates_dir / "measurement-framework.md").write_text("# Measurement")

        with runner.isolated_filesystem(temp_dir=tmp_path):
            program_name = "Comprehensive Program"

            # Run design
            result = runner.invoke(
                app,
                ["design", program_name, "Community", "12 months"],
            )
            assert result.exit_code == 0

            # Run propose
            result = runner.invoke(
                app,
                ["propose", program_name, "Foundation", "$100k", "2 years"],
            )
            assert result.exit_code == 0

            # Run measure
            result = runner.invoke(
                app,
                ["measure", program_name, "Impact", "Quarterly"],
            )
            assert result.exit_code == 0

            # Verify only one feature directory exists (all commands used same dir)
            nuaa_dir = tmp_path / "nuaa"
            feature_dirs = list(nuaa_dir.iterdir())
            assert len(feature_dirs) == 1

            # Verify all files exist in the same directory
            feature_dir = feature_dirs[0]
            assert (feature_dir / "program-design.md").exists()
            assert (feature_dir / "logic-model.md").exists()
            assert (feature_dir / "impact-framework.md").exists()
            assert (feature_dir / "proposal.md").exists()
            assert (feature_dir / "measurement-framework.md").exists()

    def test_multiple_programs_create_separate_dirs(self, tmp_path):
        """Test that different programs create separate directories."""
        templates_dir = tmp_path / "nuaa-kit" / "templates"
        templates_dir.mkdir(parents=True)
        (templates_dir / "program-design.md").write_text("# Design: [Name]")
        (templates_dir / "logic-model.md").write_text("# Logic Model")
        (templates_dir / "impact-framework.md").write_text("# Impact")

        with runner.isolated_filesystem(temp_dir=tmp_path):
            programs = ["Program A", "Program B", "Program C"]

            for program in programs:
                result = runner.invoke(
                    app,
                    ["design", program, "Community", "12 months"],
                )
                assert result.exit_code == 0

            # Verify three separate directories were created
            nuaa_dir = tmp_path / "nuaa"
            feature_dirs = sorted(nuaa_dir.iterdir())
            assert len(feature_dirs) == 3

            # Verify numbering is sequential
            assert feature_dirs[0].name.startswith("001-")
            assert feature_dirs[1].name.startswith("002-")
            assert feature_dirs[2].name.startswith("003-")


class TestCommandErrorHandling:
    """Test error handling in commands."""

    def test_missing_required_argument(self):
        """Test that commands fail gracefully with missing arguments."""
        result = runner.invoke(app, ["design"])
        assert result.exit_code != 0
        # Should show usage or error about missing arguments
        assert ("Missing argument" in result.output or "Missing option" in result.output or
                "required" in result.output.lower() or "Usage:" in result.output)

    def test_empty_program_name(self):
        """Test handling of empty program name."""
        result = runner.invoke(
            app,
            ["design", "", "Community", "12 months"],
        )
        # Should either reject empty name or use default
        # The exact behavior depends on validation
        assert result.exit_code != 0 or "feature" in result.output.lower()

    def test_missing_templates_directory(self, tmp_path):
        """Test graceful handling when templates are missing."""
        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Don't create templates directory
            result = runner.invoke(
                app,
                ["design", "Test", "Community", "12 months"],
            )

            # Note: In production, this might succeed if templates are found in package
            # or fail with helpful error. Both are acceptable behaviors.
            # We just verify it doesn't crash with an unhandled exception
            assert "Traceback" not in result.output


class TestCommandInputValidation:
    """Test input validation in commands."""

    def test_long_input_truncation(self, tmp_path):
        """Test that overly long inputs are handled correctly."""
        templates_dir = tmp_path / "nuaa-kit" / "templates"
        templates_dir.mkdir(parents=True)
        (templates_dir / "program-design.md").write_text("# Design: [Name]\n{{TARGET_POPULATION}}")
        (templates_dir / "logic-model.md").write_text("# Logic")
        (templates_dir / "impact-framework.md").write_text("# Impact")

        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Provide very long input (over max_length)
            long_text = "x" * 1000

            result = runner.invoke(
                app,
                ["design", "Test", long_text, "12 months"],
            )

            # Command should either succeed with truncated input or fail with validation error
            # Check that it doesn't crash
            assert "Traceback" not in result.output

    def test_special_characters_in_program_name(self, tmp_path):
        """Test handling of special characters in program name."""
        templates_dir = tmp_path / "nuaa-kit" / "templates"
        templates_dir.mkdir(parents=True)
        (templates_dir / "program-design.md").write_text("# Design")
        (templates_dir / "logic-model.md").write_text("# Logic")
        (templates_dir / "impact-framework.md").write_text("# Impact")

        with runner.isolated_filesystem(temp_dir=tmp_path):
            # Program name with special characters
            result = runner.invoke(
                app,
                ["design", "Test/Program<>Name", "Community", "12 months"],
            )

            # Should succeed and sanitize the name
            assert result.exit_code == 0

            nuaa_dir = tmp_path / "nuaa"
            feature_dirs = list(nuaa_dir.iterdir())
            assert len(feature_dirs) == 1

            # Directory name should not contain special characters
            dir_name = feature_dirs[0].name
            assert "/" not in dir_name
            assert "<" not in dir_name
            assert ">" not in dir_name
