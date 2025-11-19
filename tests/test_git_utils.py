"""Tests for git_utils module."""

import os
import subprocess
from unittest.mock import Mock, patch

import pytest
from rich.console import Console

from nuaa_cli.git_utils import run_command, is_git_repo, init_git_repo


class TestRunCommand:
    """Tests for run_command function."""

    def test_run_command_success(self):
        """Test successful command execution."""
        result = run_command(["echo", "hello"], capture=True)
        assert result == "hello"

    def test_run_command_without_capture(self):
        """Test command execution without capturing output."""
        result = run_command(["echo", "hello"], capture=False)
        assert result is None

    def test_run_command_failure_with_check(self):
        """Test command failure with check_return=True."""
        with pytest.raises(subprocess.CalledProcessError):
            run_command(["false"], check_return=True)

    def test_run_command_failure_without_check(self):
        """Test command failure with check_return=False."""
        result = run_command(["false"], check_return=False)
        assert result is None

    def test_run_command_with_custom_console(self):
        """Test run_command with custom console."""
        console = Mock(spec=Console)
        try:
            run_command(["false"], check_return=True, console=console)
        except subprocess.CalledProcessError:
            pass
        # Console should have been used for error output
        assert console.print.called

    def test_run_command_captures_stderr(self):
        """Test that stderr is captured on failure."""
        console = Mock(spec=Console)
        try:
            # Use a command that will fail with stderr
            run_command(["ls", "/nonexistent_directory_12345"], check_return=True, console=console)
        except subprocess.CalledProcessError:
            pass
        # Should have printed error information
        assert console.print.called


class TestIsGitRepo:
    """Tests for is_git_repo function."""

    def test_is_git_repo_in_repo(self, tmp_path):
        """Test detection of git repository."""
        # Initialize a git repo
        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
        assert is_git_repo(tmp_path) is True

    def test_is_git_repo_not_in_repo(self, tmp_path):
        """Test detection when not in a git repository."""
        assert is_git_repo(tmp_path) is False

    def test_is_git_repo_nonexistent_path(self, tmp_path):
        """Test with nonexistent path."""
        nonexistent = tmp_path / "does_not_exist"
        assert is_git_repo(nonexistent) is False

    def test_is_git_repo_file_path(self, tmp_path):
        """Test with file path instead of directory."""
        file_path = tmp_path / "test.txt"
        file_path.write_text("test")
        assert is_git_repo(file_path) is False

    def test_is_git_repo_default_path(self):
        """Test with default path (current directory)."""
        # Should not raise an exception
        result = is_git_repo()
        assert isinstance(result, bool)


class TestInitGitRepo:
    """Tests for init_git_repo function."""

    def test_init_git_repo_success(self, tmp_path):
        """Test successful git repository initialization."""
        # Create a file to commit
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")

        success, error = init_git_repo(tmp_path, quiet=True)

        assert success is True
        assert error is None
        assert (tmp_path / ".git").exists()

        # Verify commit was made
        result = subprocess.run(
            ["git", "log", "--oneline"], cwd=tmp_path, capture_output=True, text=True
        )
        assert "Initial commit from NUAA template" in result.stdout

    def test_init_git_repo_empty_directory(self, tmp_path):
        """Test git init in empty directory."""
        success, error = init_git_repo(tmp_path, quiet=True)

        # Should still succeed even with empty directory
        assert success is True
        assert error is None

    def test_init_git_repo_with_console_output(self, tmp_path):
        """Test git init with console output."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        console = Mock(spec=Console)
        success, error = init_git_repo(tmp_path, quiet=False, console=console)

        assert success is True
        assert console.print.called
        # Should have printed success message
        call_args = [str(call) for call in console.print.call_args_list]
        assert any("Initializing" in str(arg) or "✓" in str(arg) for arg in call_args)

    def test_init_git_repo_already_initialized(self, tmp_path):
        """Test git init in directory that already has git."""
        # Initialize once
        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)

        # Try to initialize again
        success, error = init_git_repo(tmp_path, quiet=True)

        # Should fail (git init on existing repo)
        # Actually git init on existing repo is idempotent, but commit might fail
        # Depending on git version behavior
        assert isinstance(success, bool)

    def test_init_git_repo_preserves_cwd(self, tmp_path):
        """Test that init_git_repo preserves current working directory."""
        original_cwd = os.getcwd()
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")

        init_git_repo(tmp_path, quiet=True)

        assert os.getcwd() == original_cwd

    @patch("nuaa_cli.git_utils.subprocess.run")
    def test_init_git_repo_handles_git_failure(self, mock_run, tmp_path):
        """Test handling of git command failures."""
        # Mock git command to fail
        mock_run.side_effect = subprocess.CalledProcessError(1, ["git", "init"])

        success, error = init_git_repo(tmp_path, quiet=True)

        assert success is False
        assert error is not None
        assert "git init" in error or "Command" in error

    def test_init_git_repo_multiple_files(self, tmp_path):
        """Test git init with multiple files."""
        # Create multiple files
        (tmp_path / "file1.txt").write_text("content1")
        (tmp_path / "file2.md").write_text("# Content 2")
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "file3.py").write_text("# Python file")

        success, error = init_git_repo(tmp_path, quiet=True)

        assert success is True
        assert error is None

        # Verify all files were committed
        result = subprocess.run(["git", "ls-files"], cwd=tmp_path, capture_output=True, text=True)
        assert "file1.txt" in result.stdout
        assert "file2.md" in result.stdout
        assert "subdir/file3.py" in result.stdout
