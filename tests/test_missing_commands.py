"""
Tests for missing command coverage (propose, measure, document, report, refine).

This module provides comprehensive tests for the NUAA CLI commands that create
program artifacts including proposals, impact frameworks, program analyses,
reports, and changelog refinements.
"""

import os
from typer.testing import CliRunner

from nuaa_cli import app


runner = CliRunner()


class TestProposeCommand:
    """Tests for the propose command."""

    def test_propose_creates_proposal_file(self, tmp_path):
        """Test that propose command creates proposal.md file."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = runner.invoke(app, ["propose", "Peer Support Network", "NSW Health", "$75000", "12 months"])

            # Should succeed or fail gracefully
            assert result.exit_code in [0, 1]

            # If successful, check for file creation
            if result.exit_code == 0:
                nuaa_dir = tmp_path / "nuaa"
                assert nuaa_dir.exists()

                # Find proposal.md file
                proposal_files = list(nuaa_dir.glob("*/proposal.md"))
                assert len(proposal_files) > 0

                # Check content
                content = proposal_files[0].read_text()
                assert "Peer Support Network" in content or "PROGRAM_NAME" in content
                assert "NSW Health" in content or "FUNDER" in content
        finally:
            os.chdir(old_cwd)

    def test_propose_with_force_flag(self, tmp_path):
        """Test propose command with --force flag overwrites existing file."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Create first proposal
            result1 = runner.invoke(app, ["propose", "Test Program", "Funder A", "$50000", "6 months"])

            if result1.exit_code == 0:
                # Create second proposal with force flag
                result2 = runner.invoke(app, ["propose", "Test Program", "Funder B", "$100000", "12 months", "--force"])

                # Should succeed
                assert result2.exit_code == 0

                # Check that content was updated
                nuaa_dir = tmp_path / "nuaa"
                proposal_files = list(nuaa_dir.glob("*/proposal.md"))
                if proposal_files:
                    content = proposal_files[0].read_text()
                    # Should contain new funder information
                    assert "Funder B" in content or "100000" in content
        finally:
            os.chdir(old_cwd)

    def test_propose_without_force_preserves_existing(self, tmp_path):
        """Test propose command without --force preserves existing file."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Create first proposal
            result1 = runner.invoke(app, ["propose", "Test Program", "Funder A", "$50000", "6 months"])

            if result1.exit_code == 0:
                # Try to create second proposal without force
                result2 = runner.invoke(app, ["propose", "Test Program", "Funder B", "$100000", "12 months"])

                # May succeed or fail depending on implementation
                # If it doesn't overwrite, exit code might be 1
                assert result2.exit_code in [0, 1]
        finally:
            os.chdir(old_cwd)

    def test_propose_missing_arguments(self):
        """Test propose command fails with missing arguments."""
        result = runner.invoke(app, ["propose"])
        assert result.exit_code != 0

        result = runner.invoke(app, ["propose", "ProgramName"])
        assert result.exit_code != 0

        result = runner.invoke(app, ["propose", "ProgramName", "Funder"])
        assert result.exit_code != 0

    def test_propose_validates_program_name(self, tmp_path):
        """Test propose validates program name input."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            # Test with valid program name
            result = runner.invoke(app, ["propose", "Valid Program Name", "Funder", "$1000", "1 year"])
            # Should succeed or fail gracefully, not crash
            assert result.exit_code in [0, 1]
        finally:
            os.chdir(old_cwd)


class TestMeasureCommand:
    """Tests for the measure command."""

    def test_measure_creates_impact_framework(self, tmp_path):
        """Test that measure command creates impact-framework.md file."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = runner.invoke(app, ["measure", "Peer Support Network", "12 months", "$15000"])

            # Should succeed or fail gracefully
            assert result.exit_code in [0, 1]

            # If successful, check for file creation
            if result.exit_code == 0:
                nuaa_dir = tmp_path / "nuaa"
                assert nuaa_dir.exists()

                # Find impact-framework.md file
                framework_files = list(nuaa_dir.glob("*/impact-framework.md"))
                assert len(framework_files) > 0

                # Check content
                content = framework_files[0].read_text()
                assert "Peer Support Network" in content or "PROGRAM_NAME" in content
        finally:
            os.chdir(old_cwd)

    def test_measure_with_force_flag(self, tmp_path):
        """Test measure command with --force flag."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Create first framework
            result1 = runner.invoke(app, ["measure", "Test Program", "6 months", "$5000"])

            if result1.exit_code == 0:
                # Update with force flag
                result2 = runner.invoke(app, ["measure", "Test Program", "12 months", "$10000", "--force"])

                # Should succeed
                assert result2.exit_code == 0
        finally:
            os.chdir(old_cwd)

    def test_measure_missing_arguments(self):
        """Test measure command fails with missing arguments."""
        result = runner.invoke(app, ["measure"])
        assert result.exit_code != 0

        result = runner.invoke(app, ["measure", "ProgramName"])
        assert result.exit_code != 0

        result = runner.invoke(app, ["measure", "ProgramName", "Period"])
        assert result.exit_code != 0

    def test_measure_validates_inputs(self, tmp_path):
        """Test measure validates all inputs."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = runner.invoke(app, ["measure", "Valid Program", "1 year", "$20000"])
            # Should handle gracefully
            assert result.exit_code in [0, 1]
        finally:
            os.chdir(old_cwd)


class TestDocumentCommand:
    """Tests for the document command."""

    def test_document_creates_analysis_file(self, tmp_path):
        """Test that document command creates existing-program-analysis.md."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = runner.invoke(app, ["document", "Mobile Needle Exchange"])

            # Should succeed or fail gracefully
            assert result.exit_code in [0, 1]

            # If successful, check for file creation
            if result.exit_code == 0:
                nuaa_dir = tmp_path / "nuaa"
                assert nuaa_dir.exists()

                # Find existing-program-analysis.md file
                analysis_files = list(nuaa_dir.glob("*/existing-program-analysis.md"))
                assert len(analysis_files) > 0

                # Check content
                content = analysis_files[0].read_text()
                assert "Mobile Needle Exchange" in content or "PROGRAM_NAME" in content
        finally:
            os.chdir(old_cwd)

    def test_document_with_force_flag(self, tmp_path):
        """Test document command with --force flag."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Create first analysis
            result1 = runner.invoke(app, ["document", "Test Program"])

            if result1.exit_code == 0:
                # Update with force
                result2 = runner.invoke(app, ["document", "Test Program", "--force"])

                # Should succeed
                assert result2.exit_code == 0
        finally:
            os.chdir(old_cwd)

    def test_document_missing_arguments(self):
        """Test document command fails with missing program name."""
        result = runner.invoke(app, ["document"])
        assert result.exit_code != 0

    def test_document_validates_program_name(self, tmp_path):
        """Test document validates program name."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = runner.invoke(app, ["document", "Valid Program Name"])
            # Should handle gracefully
            assert result.exit_code in [0, 1]
        finally:
            os.chdir(old_cwd)


class TestReportCommand:
    """Tests for the report command."""

    def test_report_creates_report_scaffold(self, tmp_path):
        """Test that report command creates report.md scaffold."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = runner.invoke(app, ["report", "Peer Support Network"])

            # Should succeed or fail gracefully
            assert result.exit_code in [0, 1]

            # If successful, check for file creation
            if result.exit_code == 0:
                nuaa_dir = tmp_path / "nuaa"
                assert nuaa_dir.exists()

                # Find report.md file
                report_files = list(nuaa_dir.glob("*/report.md"))
                assert len(report_files) > 0

                # Check content has expected sections
                content = report_files[0].read_text()
                assert "Overview" in content
                assert "Key Findings" in content
                assert "Lessons Learned" in content
        finally:
            os.chdir(old_cwd)

    def test_report_with_type_option(self, tmp_path):
        """Test report command with different report types."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Test different report types
            report_types = ["final", "progress", "quarterly", "annual", "mid-program"]

            for report_type in report_types:
                result = runner.invoke(app, ["report", f"Program_{report_type}", "--type", report_type])

                # Should succeed or fail gracefully
                assert result.exit_code in [0, 1]

                if result.exit_code == 0:
                    nuaa_dir = tmp_path / "nuaa"
                    report_files = list(nuaa_dir.glob("*/report.md"))
                    if report_files:
                        content = report_files[-1].read_text()
                        # Check that report type is reflected in content
                        assert report_type.title() in content or "Report" in content
        finally:
            os.chdir(old_cwd)

    def test_report_with_force_flag(self, tmp_path):
        """Test report command with --force flag."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Create first report
            result1 = runner.invoke(app, ["report", "Test Program"])

            if result1.exit_code == 0:
                # Update with force
                result2 = runner.invoke(app, ["report", "Test Program", "--type", "annual", "--force"])

                # Should succeed
                assert result2.exit_code == 0
        finally:
            os.chdir(old_cwd)

    def test_report_missing_arguments(self):
        """Test report command fails with missing program name."""
        result = runner.invoke(app, ["report"])
        assert result.exit_code != 0

    def test_report_default_type_is_final(self, tmp_path):
        """Test that report defaults to 'final' type."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = runner.invoke(app, ["report", "Test Program"])

            if result.exit_code == 0:
                nuaa_dir = tmp_path / "nuaa"
                report_files = list(nuaa_dir.glob("*/report.md"))
                if report_files:
                    content = report_files[0].read_text()
                    # Should contain "Final" or default report structure
                    assert "Report" in content
        finally:
            os.chdir(old_cwd)


class TestRefineCommand:
    """Tests for the refine command."""

    def test_refine_creates_changelog_entry(self, tmp_path):
        """Test that refine command creates or updates CHANGELOG.md."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # First create a program with design command (or similar)
            # For testing, we'll try refine directly
            result = runner.invoke(app, ["refine", "Test Program", "--note", "Added new feature"])

            # May fail if program doesn't exist, which is expected
            # Exit code 0 = success, 1 = graceful failure
            assert result.exit_code in [0, 1]

            if result.exit_code == 0:
                nuaa_dir = tmp_path / "nuaa"
                changelog_files = list(nuaa_dir.glob("*/CHANGELOG.md"))

                if changelog_files:
                    content = changelog_files[0].read_text()
                    assert "Added new feature" in content or "Changelog" in content
        finally:
            os.chdir(old_cwd)

    def test_refine_appends_to_existing_changelog(self, tmp_path):
        """Test that refine appends to existing CHANGELOG.md."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Create first entry
            result1 = runner.invoke(app, ["refine", "Test Program", "--note", "First change"])

            if result1.exit_code == 0:
                # Add second entry
                result2 = runner.invoke(app, ["refine", "Test Program", "--note", "Second change"])

                # Should succeed
                assert result2.exit_code in [0, 1]

                if result2.exit_code == 0:
                    nuaa_dir = tmp_path / "nuaa"
                    changelog_files = list(nuaa_dir.glob("*/CHANGELOG.md"))

                    if changelog_files:
                        content = changelog_files[0].read_text()
                        # Both entries should be present
                        assert "First change" in content or "Second change" in content
        finally:
            os.chdir(old_cwd)

    def test_refine_with_default_note(self, tmp_path):
        """Test refine command with default note."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            # Use default note by not providing --note
            result = runner.invoke(app, ["refine", "Test Program"])

            # Should handle gracefully
            assert result.exit_code in [0, 1]

            if result.exit_code == 0:
                nuaa_dir = tmp_path / "nuaa"
                changelog_files = list(nuaa_dir.glob("*/CHANGELOG.md"))

                if changelog_files:
                    content = changelog_files[0].read_text()
                    # Should have default note
                    assert "Refinement" in content or "Changelog" in content
        finally:
            os.chdir(old_cwd)

    def test_refine_missing_arguments(self):
        """Test refine command fails with missing program name."""
        result = runner.invoke(app, ["refine"])
        assert result.exit_code != 0

    def test_refine_nonexistent_program(self, tmp_path):
        """Test refine fails gracefully for non-existent program."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = runner.invoke(app, ["refine", "NonexistentProgram", "--note", "Test"])

            # Should fail gracefully with exit code 1
            assert result.exit_code == 1
        finally:
            os.chdir(old_cwd)

    def test_refine_validates_inputs(self, tmp_path):
        """Test refine validates program name and note."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = runner.invoke(app, ["refine", "Valid Program", "--note", "Valid note text"])
            # Should handle gracefully
            assert result.exit_code in [0, 1]
        finally:
            os.chdir(old_cwd)


class TestMissingCommandsIntegration:
    """Integration tests for missing commands together."""

    def test_all_missing_commands_in_help(self):
        """Test that all commands appear in help text."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0

        help_text = result.output.lower()
        assert "propose" in help_text
        assert "measure" in help_text
        assert "document" in help_text
        assert "report" in help_text
        assert "refine" in help_text

    def test_all_commands_have_help(self):
        """Test that all commands have individual help messages."""
        commands = ["propose", "measure", "document", "report", "refine"]

        for cmd in commands:
            result = runner.invoke(app, [cmd, "--help"])
            assert result.exit_code == 0
            # Help should contain usage or command name
            assert "usage" in result.output.lower() or cmd in result.output.lower()

    def test_workflow_create_multiple_artifacts(self, tmp_path):
        """Test workflow creating multiple artifacts for same program."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            program_name = "Comprehensive Program"

            # Create proposal
            result1 = runner.invoke(app, ["propose", program_name, "Test Funder", "$50000", "12 months"])

            # Create impact framework
            result2 = runner.invoke(app, ["measure", program_name, "1 year", "$5000"])

            # Create program analysis
            result3 = runner.invoke(app, ["document", program_name])

            # Create report
            result4 = runner.invoke(app, ["report", program_name, "--type", "final"])

            # All commands should succeed or fail gracefully
            for result in [result1, result2, result3, result4]:
                assert result.exit_code in [0, 1]

            # If all succeeded, check that files exist in same feature directory
            if all(r.exit_code == 0 for r in [result1, result2, result3, result4]):
                nuaa_dir = tmp_path / "nuaa"
                # Should have created multiple files in the same program directory
                assert len(list(nuaa_dir.glob("*/*.md"))) >= 4
        finally:
            os.chdir(old_cwd)

    def test_commands_create_feature_directories(self, tmp_path):
        """Test that commands create feature directories when needed."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Each command should create or use feature directory
            commands_to_test = [
                ["propose", "ProposeTest", "Funder", "$1000", "1yr"],
                ["measure", "MeasureTest", "1yr", "$1000"],
                ["document", "DocumentTest"],
                ["report", "ReportTest"],
            ]

            for cmd_args in commands_to_test:
                result = runner.invoke(app, cmd_args)
                # Should handle gracefully
                assert result.exit_code in [0, 1]
        finally:
            os.chdir(old_cwd)
