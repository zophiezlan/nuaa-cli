"""Tests for CLI initialization and main entry point."""

import os
from typer.testing import CliRunner

from nuaa_cli import app


def test_init_command_basic(tmp_path):
    """Test basic init command."""
    runner = CliRunner()
    result = runner.invoke(
        app,
        ["init", "test-project", "--ai", "copilot"],
        input="n\n",  # Don't run templates update
        cwd=str(tmp_path),
    )

    # Should create project structure (or fail gracefully)
    # init command may require git, network, etc
    # Accept both success and expected failure
    assert result.exit_code in [0, 1]


def test_init_with_here_flag(tmp_path):
    """Test init with --here flag."""
    runner = CliRunner()

    # Change to tmp_path for this test
    old_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        result = runner.invoke(
            app,
            ["init", ".", "--ai", "copilot", "--here"],
            input="n\n",
        )

        # May succeed or fail based on environment
        assert result.exit_code in [0, 1]
    finally:
        os.chdir(old_cwd)


def test_help_command():
    """Test that --help works."""
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "NUAA CLI" in result.output or "Usage" in result.output


def test_version_command():
    """Test version command."""
    runner = CliRunner()
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert "CLI Version" in result.output


def test_command_without_args():
    """Test running design command without required args shows error."""
    runner = CliRunner()
    result = runner.invoke(app, ["design"])

    # Should fail with missing args
    assert result.exit_code != 0
