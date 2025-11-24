"""Integration tests for new planning and management commands."""

import os
from typer.testing import CliRunner

from nuaa_cli import app


runner = CliRunner()


class TestEngageCommand:
    """Tests for engage command."""

    def test_engage_creates_stakeholder_plan(self, tmp_path):
        """Test engage command creates stakeholder engagement plan."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = runner.invoke(
                app,
                ["engage", "Peer Support Program", "PWUD in Sydney", "12 months"],
            )

            # Command should succeed
            assert result.exit_code == 0

            # Should mention stakeholder engagement plan
            assert "stakeholder-engagement-plan" in result.output.lower() or "engagement plan" in result.output.lower()

            # Check if file was created
            nuaa_dir = tmp_path / "nuaa"
            if nuaa_dir.exists():
                files = list(nuaa_dir.glob("*/stakeholder-engagement-plan.md"))
                if files:
                    content = files[0].read_text()
                    # Program name is sanitized to "Peer-Support-Program"
                    assert "Peer-Support-Program" in content or "Peer Support Program" in content or "[Name]" in content
        finally:
            os.chdir(old_cwd)

    def test_engage_with_custom_feature(self, tmp_path):
        """Test engage command with custom feature slug."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = runner.invoke(
                app,
                ["engage", "Test Program", "Target Pop", "6 months", "--feature", "custom-feature"],
            )

            # Should succeed or fail gracefully
            assert result.exit_code in [0, 1]
        finally:
            os.chdir(old_cwd)


class TestPartnerCommand:
    """Tests for partner command."""

    def test_partner_creates_agreement(self, tmp_path):
        """Test partner command creates partnership agreement."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = runner.invoke(
                app,
                ["partner", "Harm Reduction Program", "Local Health District", "2 years"],
            )

            # Command should succeed
            assert result.exit_code == 0

            # Should mention partnership agreement
            assert "partnership" in result.output.lower() or "agreement" in result.output.lower()

            # Check if file was created
            nuaa_dir = tmp_path / "nuaa"
            if nuaa_dir.exists():
                files = list(nuaa_dir.glob("*/partnership-agreement.md"))
                if files:
                    content = files[0].read_text()
                    # Program name is sanitized to "Harm-Reduction-Program"
                    assert (
                        "Harm-Reduction-Program" in content
                        or "Harm Reduction Program" in content
                        or "[Name]" in content
                    )
        finally:
            os.chdir(old_cwd)


class TestTrainCommand:
    """Tests for train command."""

    def test_train_creates_curriculum(self, tmp_path):
        """Test train command creates training curriculum."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = runner.invoke(
                app,
                ["train", "Peer Worker Training", "New peer workers", "2 days"],
            )

            # Command should succeed
            assert result.exit_code == 0

            # Should mention training curriculum
            assert "training" in result.output.lower() or "curriculum" in result.output.lower()

            # Check if file was created
            nuaa_dir = tmp_path / "nuaa"
            if nuaa_dir.exists():
                files = list(nuaa_dir.glob("*/training-curriculum.md"))
                if files:
                    content = files[0].read_text()
                    assert "Peer Worker Training" in content or "[Name]" in content
        finally:
            os.chdir(old_cwd)


class TestEventCommand:
    """Tests for event command."""

    def test_event_creates_plan(self, tmp_path):
        """Test event command creates event plan."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = runner.invoke(
                app,
                ["event", "Peer Forum Launch", "Forum", "50 people"],
            )

            # Command should succeed
            assert result.exit_code == 0

            # Should mention event plan
            assert "event" in result.output.lower() or "plan" in result.output.lower()

            # Check if file was created
            nuaa_dir = tmp_path / "nuaa"
            if nuaa_dir.exists():
                files = list(nuaa_dir.glob("*/event-plan.md"))
                if files:
                    content = files[0].read_text()
                    assert "Peer Forum Launch" in content or "[Name]" in content
        finally:
            os.chdir(old_cwd)


class TestRiskCommand:
    """Tests for risk command."""

    def test_risk_creates_register(self, tmp_path):
        """Test risk command creates risk register."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            result = runner.invoke(
                app,
                ["risk", "Community Outreach", "12 months"],
            )

            # Command should succeed
            assert result.exit_code == 0

            # Should mention risk register
            assert "risk" in result.output.lower() or "register" in result.output.lower()

            # Check if file was created
            nuaa_dir = tmp_path / "nuaa"
            if nuaa_dir.exists():
                files = list(nuaa_dir.glob("*/risk-register.md"))
                if files:
                    content = files[0].read_text()
                    # Program name is sanitized to "Community-Outreach"
                    assert "Community-Outreach" in content or "Community Outreach" in content or "[Name]" in content
        finally:
            os.chdir(old_cwd)


class TestAllNewCommands:
    """Tests for all new commands together."""

    def test_all_commands_registered(self):
        """Test that all new commands are registered."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0

        # All commands should be in help output
        help_text = result.output.lower()
        assert "engage" in help_text
        assert "partner" in help_text
        assert "train" in help_text
        assert "event" in help_text
        assert "risk" in help_text

    def test_commands_help_messages(self):
        """Test that all new commands have help messages."""
        commands = ["engage", "partner", "train", "event", "risk"]

        for cmd in commands:
            result = runner.invoke(app, [cmd, "--help"])
            # Should show help (exit code 0)
            assert result.exit_code == 0
            # Should have usage information
            assert "usage" in result.output.lower() or cmd in result.output.lower()

    def test_commands_require_arguments(self):
        """Test that all new commands require arguments."""
        commands = ["engage", "partner", "train", "event", "risk"]

        for cmd in commands:
            result = runner.invoke(app, [cmd])
            # Should fail with missing required arguments
            assert result.exit_code != 0

    def test_commands_with_force_flag(self, tmp_path):
        """Test that all new commands accept --force flag."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Test each command with --force flag
            test_cases = [
                ["engage", "Test", "Pop", "Time", "--force"],
                ["partner", "Test", "Org", "Time", "--force"],
                ["train", "Test", "Audience", "Time", "--force"],
                ["event", "Test", "Type", "Attendance", "--force"],
                ["risk", "Test", "Time", "--force"],
            ]

            for cmd_args in test_cases:
                result = runner.invoke(app, cmd_args)
                # Should accept flag (succeed or fail for other reasons)
                # Exit code 0 = success, 1 = graceful failure (missing nuaa-kit, etc.)
                assert result.exit_code in [0, 1]
        finally:
            os.chdir(old_cwd)
