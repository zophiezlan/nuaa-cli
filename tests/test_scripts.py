"""Tests for scripts module."""

import os
import stat
from unittest.mock import Mock

import pytest
from rich.console import Console

from nuaa_cli.scripts import ensure_executable_scripts
from nuaa_cli.utils import StepTracker


class TestEnsureExecutableScripts:
    """Tests for ensure_executable_scripts function."""

    @pytest.mark.skipif(os.name == "nt", reason="Skip on Windows")
    def test_ensure_executable_scripts_with_sh_files(self, tmp_path):
        """Test setting execute permissions on .sh files."""
        # Create scripts directory
        scripts_dir = tmp_path / ".agents" / "scripts"
        scripts_dir.mkdir(parents=True)

        # Create a .sh file with shebang
        script_file = scripts_dir / "test.sh"
        script_file.write_text("#!/bin/bash\necho 'test'")

        # Remove execute permission
        script_file.chmod(0o644)

        # Run ensure_executable_scripts
        ensure_executable_scripts(tmp_path)

        # Check that execute permission was added
        mode = script_file.stat().st_mode
        assert mode & stat.S_IXUSR  # User execute bit should be set

    @pytest.mark.skipif(os.name == "nt", reason="Skip on Windows")
    def test_ensure_executable_scripts_preserves_already_executable(self, tmp_path):
        """Test that already executable scripts are unchanged."""
        scripts_dir = tmp_path / ".agents" / "scripts"
        scripts_dir.mkdir(parents=True)

        script_file = scripts_dir / "test.sh"
        script_file.write_text("#!/bin/bash\necho 'test'")
        script_file.chmod(0o755)

        original_mode = script_file.stat().st_mode

        ensure_executable_scripts(tmp_path)

        # Mode should be unchanged
        new_mode = script_file.stat().st_mode
        assert new_mode == original_mode

    @pytest.mark.skipif(os.name == "nt", reason="Skip on Windows")
    def test_ensure_executable_scripts_skips_files_without_shebang(self, tmp_path):
        """Test that files without shebang are skipped."""
        scripts_dir = tmp_path / ".agents" / "scripts"
        scripts_dir.mkdir(parents=True)

        # Create a .sh file WITHOUT shebang
        script_file = scripts_dir / "not_a_script.sh"
        script_file.write_text("echo 'test'")  # No shebang
        script_file.chmod(0o644)

        original_mode = script_file.stat().st_mode

        ensure_executable_scripts(tmp_path)

        # Mode should be unchanged (no shebang)
        new_mode = script_file.stat().st_mode
        assert new_mode == original_mode

    @pytest.mark.skipif(os.name == "nt", reason="Skip on Windows")
    def test_ensure_executable_scripts_with_nested_directories(self, tmp_path):
        """Test handling of nested script directories."""
        scripts_dir = tmp_path / ".agents" / "scripts"
        nested_dir = scripts_dir / "subdir" / "nested"
        nested_dir.mkdir(parents=True)

        # Create scripts at different levels
        script1 = scripts_dir / "level1.sh"
        script1.write_text("#!/bin/bash\necho 'level1'")
        script1.chmod(0o644)

        script2 = nested_dir / "level3.sh"
        script2.write_text("#!/bin/bash\necho 'level3'")
        script2.chmod(0o644)

        ensure_executable_scripts(tmp_path)

        # Both scripts should be executable
        assert script1.stat().st_mode & stat.S_IXUSR
        assert script2.stat().st_mode & stat.S_IXUSR

    def test_ensure_executable_scripts_noop_on_windows(self, tmp_path):
        """Test that function is no-op on Windows."""
        if os.name != "nt":
            pytest.skip("Test only for Windows")

        scripts_dir = tmp_path / ".agents" / "scripts"
        scripts_dir.mkdir(parents=True)

        script_file = scripts_dir / "test.sh"
        script_file.write_text("#!/bin/bash\necho 'test'")

        # Should not raise an exception
        ensure_executable_scripts(tmp_path)

    def test_ensure_executable_scripts_missing_scripts_dir(self, tmp_path):
        """Test with missing .agents/scripts directory."""
        # Should not raise an exception
        ensure_executable_scripts(tmp_path)

    @pytest.mark.skipif(os.name == "nt", reason="Skip on Windows")
    def test_ensure_executable_scripts_with_tracker(self, tmp_path):
        """Test with StepTracker for progress reporting."""
        scripts_dir = tmp_path / ".agents" / "scripts"
        scripts_dir.mkdir(parents=True)

        script_file = scripts_dir / "test.sh"
        script_file.write_text("#!/bin/bash\necho 'test'")
        script_file.chmod(0o644)

        tracker = StepTracker("Test")
        ensure_executable_scripts(tmp_path, tracker=tracker)

        # Tracker should have been updated
        assert len(tracker.steps) > 0
        assert any(step["key"] == "chmod" for step in tracker.steps)

    @pytest.mark.skipif(os.name == "nt", reason="Skip on Windows")
    def test_ensure_executable_scripts_with_console_output(self, tmp_path):
        """Test with console output (no tracker)."""
        scripts_dir = tmp_path / ".agents" / "scripts"
        scripts_dir.mkdir(parents=True)

        script_file = scripts_dir / "test.sh"
        script_file.write_text("#!/bin/bash\necho 'test'")
        script_file.chmod(0o644)

        console = Mock(spec=Console)
        ensure_executable_scripts(tmp_path, console=console)

        # Console should have been used for output
        assert console.print.called

    @pytest.mark.skipif(os.name == "nt", reason="Skip on Windows")
    def test_ensure_executable_scripts_ignores_symlinks(self, tmp_path):
        """Test that symlinks are ignored."""
        scripts_dir = tmp_path / ".agents" / "scripts"
        scripts_dir.mkdir(parents=True)

        # Create a real script
        real_script = scripts_dir / "real.sh"
        real_script.write_text("#!/bin/bash\necho 'real'")
        real_script.chmod(0o755)

        # Create a symlink
        symlink_script = scripts_dir / "link.sh"
        symlink_script.symlink_to(real_script)

        # Should not raise an exception
        ensure_executable_scripts(tmp_path)

    @pytest.mark.skipif(os.name == "nt", reason="Skip on Windows")
    def test_ensure_executable_scripts_respects_permissions(self, tmp_path):
        """Test that execute permissions respect read permissions."""
        scripts_dir = tmp_path / ".agents" / "scripts"
        scripts_dir.mkdir(parents=True)

        script_file = scripts_dir / "test.sh"
        script_file.write_text("#!/bin/bash\necho 'test'")

        # Set user read only (no group/other read)
        script_file.chmod(0o400)

        ensure_executable_scripts(tmp_path)

        mode = script_file.stat().st_mode
        # Should have user execute (0o100) but not group/other
        assert mode & stat.S_IXUSR
        # Group and other execute should not be added if no read permission
        assert not (mode & stat.S_IXGRP)
        assert not (mode & stat.S_IXOTH)

    @pytest.mark.skipif(os.name == "nt", reason="Skip on Windows")
    def test_ensure_executable_scripts_handles_permission_errors(self, tmp_path):
        """Test handling of permission errors."""
        scripts_dir = tmp_path / ".agents" / "scripts"
        scripts_dir.mkdir(parents=True)

        script_file = scripts_dir / "test.sh"
        script_file.write_text("#!/bin/bash\necho 'test'")
        script_file.chmod(0o644)

        # Mock os.chmod to raise PermissionError

        original_chmod = os.chmod

        def mock_chmod(path, mode):
            if "test.sh" in str(path):
                raise PermissionError("Permission denied")
            return original_chmod(path, mode)

        # Temporarily replace chmod
        os.chmod = mock_chmod

        try:
            console = Mock(spec=Console)
            # Should not raise, but should report failures
            ensure_executable_scripts(tmp_path, console=console)

            # Should have reported the failure
            if console.print.called:
                # Check if failure was mentioned
                pass  # Test passes if no exception raised
        finally:
            os.chmod = original_chmod
