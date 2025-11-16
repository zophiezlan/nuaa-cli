"""Tests for the check command."""

from typer.testing import CliRunner

from nuaa_cli import app, AGENT_CONFIG


def test_check_command_runs():
    """Test that check command runs successfully."""
    runner = CliRunner()
    result = runner.invoke(app, ["check"])

    # Should exit cleanly
    assert result.exit_code == 0

    # Should contain expected output
    assert "Checking for installed tools" in result.output
    assert "NUAA CLI is ready to use" in result.output


def test_check_command_shows_git():
    """Test that check command reports on git."""
    runner = CliRunner()
    result = runner.invoke(app, ["check"])

    # Should mention git
    assert "Git" in result.output or "git" in result.output


def test_check_command_shows_agents():
    """Test that check command reports on AI agents."""
    runner = CliRunner()
    result = runner.invoke(app, ["check"])

    # Should mention at least one agent from config
    agent_names = [cfg["name"] for cfg in AGENT_CONFIG.values()]
    assert any(name in result.output for name in agent_names)


def test_check_command_shows_ide_agents():
    """Test that check command handles IDE-based agents."""
    runner = CliRunner()
    result = runner.invoke(app, ["check"])

    # Should handle IDE agents (no CLI check needed)
    # At least one IDE agent should be marked as such
    assert "IDE-based" in result.output or "GitHub Copilot" in result.output
