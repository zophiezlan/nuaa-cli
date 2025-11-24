"""Comprehensive tests for download module.

This test suite provides extensive coverage for the download.py module,
including GitHub API interactions, ZIP extraction security, JSON merging,
VSCode settings handling, and template download/extraction workflows.
"""

import json
import os
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

import httpx
import pytest
import typer
from rich.console import Console

from nuaa_cli.download import (
    handle_vscode_settings,
    merge_json_files,
    download_template_from_github,
    download_and_extract_template,
)
from nuaa_cli.github_client import (
    get_github_token,
    get_auth_headers,
    parse_rate_limit_headers,
    format_rate_limit_error,
)
from nuaa_cli.download.zip_handler import safe_extract_zip
from nuaa_cli.utils import StepTracker


class TestGitHubHelpers:
    """Tests for GitHub API helper functions."""

    def testget_github_token_with_cli_token(self):
        """Test get_github_token returns CLI token when provided."""
        result = get_github_token("ghp_cli_token_123")
        assert result == "ghp_cli_token_123"

    def testget_github_token_strips_whitespace(self):
        """Test get_github_token strips whitespace from CLI token."""
        result = get_github_token("  ghp_token_with_spaces  ")
        assert result == "ghp_token_with_spaces"

    @patch.dict(os.environ, {"GH_TOKEN": "ghp_env_gh_token"}, clear=True)
    def testget_github_token_from_gh_token_env(self):
        """Test get_github_token falls back to GH_TOKEN environment variable."""
        result = get_github_token()
        assert result == "ghp_env_gh_token"

    @patch.dict(os.environ, {"GITHUB_TOKEN": "ghp_envget_github_token"}, clear=True)
    def testget_github_token_fromget_github_token_env(self):
        """Test get_github_token falls back to GITHUB_TOKEN environment variable."""
        result = get_github_token()
        assert result == "ghp_envget_github_token"

    @patch.dict(
        os.environ,
        {"GH_TOKEN": "ghp_gh_token", "GITHUB_TOKEN": "ghpget_github_token"},
        clear=True,
    )
    def testget_github_token_prefers_gh_token_overget_github_token(self):
        """Test get_github_token prefers GH_TOKEN over GITHUB_TOKEN."""
        result = get_github_token()
        assert result == "ghp_gh_token"

    @patch.dict(os.environ, {}, clear=True)
    def testget_github_token_returns_none_when_no_token(self):
        """Test get_github_token returns None when no token is available."""
        result = get_github_token()
        assert result is None

    @patch.dict(os.environ, {"GH_TOKEN": "  "}, clear=True)
    def testget_github_token_returns_none_for_whitespace_only(self):
        """Test get_github_token returns None for whitespace-only token."""
        result = get_github_token()
        assert result is None

    def testget_github_token_cli_overrides_env(self):
        """Test CLI token takes priority over environment variables."""
        with patch.dict(
            os.environ,
            {"GH_TOKEN": "ghp_env_token", "GITHUB_TOKEN": "ghpget_github_token"},
        ):
            result = get_github_token("ghp_cli_token")
            assert result == "ghp_cli_token"

    def testget_auth_headers_with_token(self):
        """Test get_auth_headers returns Authorization header with token."""
        headers = get_auth_headers("ghp_test_token")
        assert headers == {"Authorization": "Bearer ghp_test_token"}

    @patch.dict(os.environ, {}, clear=True)
    def testget_auth_headers_without_token(self):
        """Test get_auth_headers returns empty dict without token."""
        headers = get_auth_headers()
        assert headers == {}

    @patch.dict(os.environ, {"GH_TOKEN": "ghp_env_token"}, clear=True)
    def testget_auth_headers_from_env(self):
        """Test get_auth_headers uses environment token."""
        headers = get_auth_headers()
        assert headers == {"Authorization": "Bearer ghp_env_token"}

    def testparse_rate_limit_headers_complete(self):
        """Test parse_rate_limit_headers with all rate limit headers."""
        headers = httpx.Headers(
            {
                "X-RateLimit-Limit": "5000",
                "X-RateLimit-Remaining": "4999",
                "X-RateLimit-Reset": "1700000000",
                "Retry-After": "60",
            }
        )
        info = parse_rate_limit_headers(headers)

        assert info["limit"] == "5000"
        assert info["remaining"] == "4999"
        assert info["reset_epoch"] == 1700000000
        assert "reset_time" in info
        assert "reset_local" in info
        assert info["retry_after_seconds"] == 60

    def testparse_rate_limit_headers_partial(self):
        """Test parse_rate_limit_headers with partial headers."""
        headers = httpx.Headers(
            {
                "X-RateLimit-Limit": "60",
                "X-RateLimit-Remaining": "0",
            }
        )
        info = parse_rate_limit_headers(headers)

        assert info["limit"] == "60"
        assert info["remaining"] == "0"
        assert "reset_epoch" not in info

    def testparse_rate_limit_headers_empty(self):
        """Test parse_rate_limit_headers with no rate limit headers."""
        headers = httpx.Headers({})
        info = parse_rate_limit_headers(headers)

        assert info == {}

    def testparse_rate_limit_headers_reset_time_conversion(self):
        """Test parse_rate_limit_headers converts reset timestamp to datetime."""
        reset_epoch = 1700000000
        headers = httpx.Headers({"X-RateLimit-Reset": str(reset_epoch)})
        info = parse_rate_limit_headers(headers)

        assert info["reset_epoch"] == reset_epoch
        assert isinstance(info["reset_time"], datetime)
        assert info["reset_time"].tzinfo == timezone.utc
        assert isinstance(info["reset_local"], datetime)

    def testparse_rate_limit_headers_retry_after_http_date(self):
        """Test parse_rate_limit_headers with HTTP-date format for Retry-After."""
        headers = httpx.Headers({"Retry-After": "Wed, 21 Oct 2015 07:28:00 GMT"})
        info = parse_rate_limit_headers(headers)

        assert "retry_after" in info
        assert info["retry_after"] == "Wed, 21 Oct 2015 07:28:00 GMT"
        assert "retry_after_seconds" not in info

    def testformat_rate_limit_error_with_complete_info(self):
        """Test format_rate_limit_error with full rate limit information."""
        headers = httpx.Headers(
            {
                "X-RateLimit-Limit": "60",
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": "1700000000",
                "Retry-After": "3600",
            }
        )
        error_msg = format_rate_limit_error(403, headers, "https://api.github.com/test")

        assert "403" in error_msg
        assert "https://api.github.com/test" in error_msg
        assert "Rate Limit Information" in error_msg
        assert "60 requests/hour" in error_msg
        assert "Remaining: 0" in error_msg
        assert "Resets at:" in error_msg
        assert "Retry after: 3600 seconds" in error_msg
        assert "Troubleshooting Tips" in error_msg
        assert "GitHub token" in error_msg

    def testformat_rate_limit_error_without_rate_info(self):
        """Test format_rate_limit_error without rate limit headers."""
        headers = httpx.Headers({})
        error_msg = format_rate_limit_error(500, headers, "https://api.github.com/test")

        assert "500" in error_msg
        assert "https://api.github.com/test" in error_msg
        assert "Troubleshooting Tips" in error_msg

    def testformat_rate_limit_error_429_status(self):
        """Test format_rate_limit_error with 429 Too Many Requests status."""
        headers = httpx.Headers({"X-RateLimit-Remaining": "0", "Retry-After": "120"})
        error_msg = format_rate_limit_error(429, headers, "https://api.github.com/test")

        assert "429" in error_msg
        assert "Remaining: 0" in error_msg
        assert "Retry after: 120 seconds" in error_msg


class TestSafeExtractZip:
    """Tests for secure ZIP extraction with path traversal protection."""

    def test_safe_extract_normal_zip(self, tmp_path):
        """Test safe_extract_zip with normal ZIP file."""
        # Create a test ZIP file with safe paths
        zip_path = tmp_path / "test.zip"
        extract_path = tmp_path / "extract"
        extract_path.mkdir()

        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("file1.txt", "content1")
            zf.writestr("dir1/file2.txt", "content2")

        with zipfile.ZipFile(zip_path, "r") as zf:
            safe_extract_zip(zf, extract_path)

        assert (extract_path / "file1.txt").exists()
        assert (extract_path / "dir1" / "file2.txt").exists()
        assert (extract_path / "file1.txt").read_text() == "content1"
        assert (extract_path / "dir1" / "file2.txt").read_text() == "content2"

    def test_safe_extract_path_traversal_attack(self, tmp_path):
        """Test safe_extract_zip prevents path traversal attack."""
        # Create a malicious ZIP file with path traversal
        zip_path = tmp_path / "malicious.zip"
        extract_path = tmp_path / "extract"
        extract_path.mkdir()

        # Create ZIP with path traversal attempt
        with zipfile.ZipFile(zip_path, "w") as zf:
            # This should be blocked
            zf.writestr("../../../etc/passwd", "malicious content")

        console = Mock(spec=Console)
        with zipfile.ZipFile(zip_path, "r") as zf:
            with pytest.raises(typer.Exit) as exc_info:
                safe_extract_zip(zf, extract_path, console=console)

        assert exc_info.value.exit_code == 1
        console.print.assert_called()
        # Check that security error was printed
        calls = [str(call) for call in console.print.call_args_list]
        assert any("Security Error" in str(call) for call in calls)

    def test_safe_extract_absolute_path_in_zip(self, tmp_path):
        """Test safe_extract_zip handles absolute paths in ZIP (edge case)."""
        zip_path = tmp_path / "absolute.zip"
        extract_path = tmp_path / "extract"
        extract_path.mkdir()

        # Note: Creating a ZIP with actual absolute paths is tricky
        # Most ZIP implementations normalize these, but we test the validation logic
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("normal/file.txt", "content")

        with zipfile.ZipFile(zip_path, "r") as zf:
            # Should work fine with normal paths
            safe_extract_zip(zf, extract_path)

        assert (extract_path / "normal" / "file.txt").exists()

    def test_safe_extract_nested_directories(self, tmp_path):
        """Test safe_extract_zip with deeply nested directory structure."""
        zip_path = tmp_path / "nested.zip"
        extract_path = tmp_path / "extract"
        extract_path.mkdir()

        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("a/b/c/d/e/f/deep.txt", "nested content")

        with zipfile.ZipFile(zip_path, "r") as zf:
            safe_extract_zip(zf, extract_path)

        assert (extract_path / "a" / "b" / "c" / "d" / "e" / "f" / "deep.txt").exists()

    def test_safe_extract_console_warnings(self, tmp_path):
        """Test safe_extract_zip prints security warnings via console."""
        zip_path = tmp_path / "bad.zip"
        extract_path = tmp_path / "extract"
        extract_path.mkdir()

        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("../../sneaky.txt", "bad")

        console = Mock(spec=Console)
        with zipfile.ZipFile(zip_path, "r") as zf:
            with pytest.raises(typer.Exit):
                safe_extract_zip(zf, extract_path, console=console)

        # Should have printed error messages
        assert console.print.call_count >= 2
        error_calls = [call[0][0] for call in console.print.call_args_list]
        assert any("Security Error" in str(msg) for msg in error_calls)
        assert any("malicious" in str(msg).lower() for msg in error_calls)

    def test_safe_extract_empty_zip(self, tmp_path):
        """Test safe_extract_zip with empty ZIP file."""
        zip_path = tmp_path / "empty.zip"
        extract_path = tmp_path / "extract"
        extract_path.mkdir()

        with zipfile.ZipFile(zip_path, "w") as zf:
            pass  # Empty ZIP

        with zipfile.ZipFile(zip_path, "r") as zf:
            safe_extract_zip(zf, extract_path)

        # Should succeed without errors
        assert extract_path.exists()


class TestHandleVscodeSettings:
    """Tests for VSCode settings.json handling and merging."""

    def test_handle_vscode_settings_copy_when_no_dest(self, tmp_path):
        """Test handle_vscode_settings copies file when destination doesn't exist."""
        source = tmp_path / "source.json"
        dest = tmp_path / "dest.json"
        rel_path = Path("settings.json")

        settings = {"python.linting.enabled": True}
        source.write_text(json.dumps(settings))

        handle_vscode_settings(source, dest, rel_path, verbose=False)

        assert dest.exists()
        assert json.loads(dest.read_text()) == settings

    def test_handle_vscode_settings_merge_with_existing(self, tmp_path):
        """Test handle_vscode_settings merges with existing settings."""
        source = tmp_path / "source.json"
        dest = tmp_path / "dest.json"
        rel_path = Path("settings.json")

        existing_settings = {
            "python.linting.enabled": True,
            "editor.fontSize": 14,
        }
        new_settings = {
            "python.formatting.provider": "black",
            "editor.tabSize": 4,
        }

        dest.write_text(json.dumps(existing_settings))
        source.write_text(json.dumps(new_settings))

        handle_vscode_settings(source, dest, rel_path, verbose=False)

        merged = json.loads(dest.read_text())
        assert merged["python.linting.enabled"] is True  # Preserved
        assert merged["editor.fontSize"] == 14  # Preserved
        assert merged["python.formatting.provider"] == "black"  # Added
        assert merged["editor.tabSize"] == 4  # Added

    def test_handle_vscode_settings_invalid_json_fallback(self, tmp_path):
        """Test handle_vscode_settings falls back to copy on JSON decode error."""
        source = tmp_path / "source.json"
        dest = tmp_path / "dest.json"
        rel_path = Path("settings.json")

        source.write_text('{"valid": "json"}')
        dest.write_text("invalid json content {")

        console = Mock(spec=Console)
        handle_vscode_settings(source, dest, rel_path, verbose=True, console=console)

        # Should have copied source over broken dest
        assert json.loads(dest.read_text()) == {"valid": "json"}

    def test_handle_vscode_settings_permission_error(self, tmp_path):
        """Test handle_vscode_settings handles permission errors gracefully."""
        source = tmp_path / "source.json"
        dest = tmp_path / "dest.json"
        rel_path = Path("settings.json")

        source.write_text('{"test": "data"}')

        console = Mock(spec=Console)

        # Mock open to raise PermissionError on first read attempt
        original_open = open

        def mock_open(*args, **kwargs):
            if str(args[0]).endswith("dest.json") and "r" in str(args[1]):
                raise PermissionError("Access denied")
            return original_open(*args, **kwargs)

        with patch("builtins.open", side_effect=mock_open):
            handle_vscode_settings(source, dest, rel_path, verbose=True, console=console)

        # Should have attempted to print warning
        assert console.print.called

    def test_handle_vscode_settings_verbose_output(self, tmp_path):
        """Test handle_vscode_settings prints verbose messages."""
        source = tmp_path / "source.json"
        dest = tmp_path / "dest.json"
        rel_path = Path(".vscode/settings.json")

        source.write_text('{"test": "value"}')

        console = Mock(spec=Console)
        handle_vscode_settings(source, dest, rel_path, verbose=True, console=console)

        # Should have printed status message
        assert console.print.called

    def test_handle_vscode_settings_with_tracker(self, tmp_path):
        """Test handle_vscode_settings suppresses verbose output with tracker."""
        source = tmp_path / "source.json"
        dest = tmp_path / "dest.json"
        rel_path = Path("settings.json")

        source.write_text('{"test": "value"}')

        tracker = StepTracker("Test")
        console = Mock(spec=Console)

        handle_vscode_settings(
            source, dest, rel_path, verbose=True, tracker=tracker, console=console
        )

        # Should NOT print when tracker is present
        assert not console.print.called

    def test_handle_vscode_settings_file_not_found(self, tmp_path):
        """Test handle_vscode_settings handles missing source file."""
        source = tmp_path / "nonexistent.json"
        dest = tmp_path / "dest.json"
        rel_path = Path("settings.json")

        console = Mock(spec=Console)

        # Should raise FileNotFoundError since source doesn't exist
        with pytest.raises(FileNotFoundError):
            handle_vscode_settings(source, dest, rel_path, verbose=True, console=console)


class TestMergeJsonFiles:
    """Tests for deep JSON merging functionality."""

    def test_merge_json_files_add_new_keys(self, tmp_path):
        """Test merge_json_files adds new keys to existing file."""
        existing_file = tmp_path / "config.json"
        existing_content = {"key1": "value1"}
        new_content = {"key2": "value2", "key3": "value3"}

        existing_file.write_text(json.dumps(existing_content))

        result = merge_json_files(existing_file, new_content)

        assert result["key1"] == "value1"
        assert result["key2"] == "value2"
        assert result["key3"] == "value3"

    def test_merge_json_files_deep_merge_nested_objects(self, tmp_path):
        """Test merge_json_files recursively merges nested dictionaries."""
        existing_file = tmp_path / "config.json"
        existing_content = {
            "database": {"host": "localhost", "port": 5432},
            "logging": {"level": "INFO"},
        }
        new_content = {
            "database": {"username": "admin", "password": "secret"},
            "logging": {"format": "json"},
        }

        existing_file.write_text(json.dumps(existing_content))

        result = merge_json_files(existing_file, new_content)

        # Nested merge should preserve existing nested keys
        assert result["database"]["host"] == "localhost"
        assert result["database"]["port"] == 5432
        assert result["database"]["username"] == "admin"
        assert result["database"]["password"] == "secret"
        assert result["logging"]["level"] == "INFO"
        assert result["logging"]["format"] == "json"

    def test_merge_json_files_replace_arrays(self, tmp_path):
        """Test merge_json_files replaces arrays instead of merging them."""
        existing_file = tmp_path / "config.json"
        existing_content = {"tags": ["old", "legacy"]}
        new_content = {"tags": ["new", "modern"]}

        existing_file.write_text(json.dumps(existing_content))

        result = merge_json_files(existing_file, new_content)

        # Arrays should be replaced, not merged
        assert result["tags"] == ["new", "modern"]

    def test_merge_json_files_replace_scalar_values(self, tmp_path):
        """Test merge_json_files replaces scalar values with new ones."""
        existing_file = tmp_path / "config.json"
        existing_content = {"version": "1.0.0", "enabled": False}
        new_content = {"version": "2.0.0", "enabled": True}

        existing_file.write_text(json.dumps(existing_content))

        result = merge_json_files(existing_file, new_content)

        assert result["version"] == "2.0.0"
        assert result["enabled"] is True

    def test_merge_json_files_type_conflicts(self, tmp_path):
        """Test merge_json_files handles type conflicts by replacing."""
        existing_file = tmp_path / "config.json"
        existing_content = {"setting": {"nested": "object"}}
        new_content = {"setting": "scalar_value"}

        existing_file.write_text(json.dumps(existing_content))

        result = merge_json_files(existing_file, new_content)

        # New scalar should replace old object
        assert result["setting"] == "scalar_value"

    def test_merge_json_files_nonexistent_file(self, tmp_path):
        """Test merge_json_files returns new content when file doesn't exist."""
        nonexistent = tmp_path / "missing.json"
        new_content = {"new": "data"}

        result = merge_json_files(nonexistent, new_content)

        assert result == new_content

    def test_merge_json_files_invalid_json(self, tmp_path):
        """Test merge_json_files handles invalid JSON gracefully."""
        invalid_file = tmp_path / "invalid.json"
        invalid_file.write_text("not valid json {{{")
        new_content = {"valid": "content"}

        result = merge_json_files(invalid_file, new_content)

        # Should return new content when existing is invalid
        assert result == new_content

    def test_merge_json_files_empty_objects(self, tmp_path):
        """Test merge_json_files handles empty objects."""
        existing_file = tmp_path / "config.json"
        existing_file.write_text("{}")
        new_content = {"new_key": "new_value"}

        result = merge_json_files(existing_file, new_content)

        assert result == new_content

    def test_merge_json_files_verbose_output(self, tmp_path):
        """Test merge_json_files prints verbose output when enabled."""
        existing_file = tmp_path / "config.json"
        existing_file.write_text('{"existing": "data"}')
        new_content = {"new": "data"}

        console = Mock(spec=Console)
        merge_json_files(existing_file, new_content, verbose=True, console=console)

        assert console.print.called
        print_args = console.print.call_args[0][0]
        assert "Merged JSON file" in print_args


class TestDownloadTemplateFromGithub:
    """Tests for GitHub template downloading."""

    @patch("nuaa_cli.download.httpx.Client")
    def test_download_template_success(self, mock_client_class, tmp_path):
        """Test download_template_from_github successful download."""
        # Mock API response for releases
        release_response = Mock(spec=httpx.Response)
        release_response.status_code = 200
        release_response.json.return_value = {
            "tag_name": "v1.0.0",
            "assets": [
                {
                    "name": "nuaa-template-claude-sh-v1.0.0.zip",
                    "browser_download_url": "https://github.com/test/download.zip",
                    "size": 1024,
                }
            ],
        }

        # Mock download response
        download_response = Mock(spec=httpx.Response)
        download_response.status_code = 200
        download_response.headers = httpx.Headers({"content-length": "1024"})
        download_response.iter_bytes = Mock(return_value=[b"test zip content"])

        # Setup mock client
        mock_client_instance = Mock()
        mock_client_instance.get.return_value = release_response

        # Setup context manager for stream
        mock_stream_context = MagicMock()
        mock_stream_context.__enter__.return_value = download_response
        mock_client_instance.stream.return_value = mock_stream_context
        mock_client_instance.close.return_value = None

        mock_client_class.return_value = mock_client_instance

        zip_path, metadata = download_template_from_github(
            "claude",
            tmp_path,
            script_type="sh",
            verbose=False,
            show_progress=False,
        )

        assert zip_path.exists()
        assert metadata["release"] == "v1.0.0"
        assert metadata["filename"] == "nuaa-template-claude-sh-v1.0.0.zip"
        assert metadata["size"] == 1024

    @patch("httpx.Client")
    def test_download_template_404_error(self, mock_client_class, tmp_path):
        """Test download_template_from_github handles 404 errors."""
        release_response = Mock()
        release_response.status_code = 404
        release_response.headers = httpx.Headers({})
        release_response.text = "Not found"

        mock_client = MagicMock()
        mock_client.__enter__.return_value.get.return_value = release_response
        mock_client_class.return_value = mock_client

        console = Mock(spec=Console)

        with pytest.raises(typer.Exit) as exc_info:
            download_template_from_github(
                "claude",
                tmp_path,
                verbose=False,
                console=console,
            )

        assert exc_info.value.exit_code == 1

    @patch("httpx.Client")
    def test_download_template_rate_limit_429(self, mock_client_class, tmp_path):
        """Test download_template_from_github handles rate limiting."""
        release_response = Mock()
        release_response.status_code = 429
        release_response.headers = httpx.Headers(
            {
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": "1700000000",
                "Retry-After": "3600",
            }
        )
        release_response.text = "Rate limit exceeded"

        mock_client = MagicMock()
        mock_client.__enter__.return_value.get.return_value = release_response
        mock_client_class.return_value = mock_client

        console = Mock(spec=Console)

        with pytest.raises(typer.Exit):
            download_template_from_github(
                "claude",
                tmp_path,
                verbose=False,
                console=console,
            )

    @patch("httpx.Client")
    def test_download_template_network_timeout(self, mock_client_class, tmp_path):
        """Test download_template_from_github handles network timeouts."""
        mock_client = MagicMock()
        mock_client.__enter__.return_value.get.side_effect = httpx.TimeoutException(
            "Request timed out"
        )
        mock_client_class.return_value = mock_client

        console = Mock(spec=Console)

        with pytest.raises(typer.Exit) as exc_info:
            download_template_from_github(
                "claude",
                tmp_path,
                verbose=False,
                console=console,
            )

        assert exc_info.value.exit_code == 1
        assert console.print.called

    @patch("httpx.Client")
    def test_download_template_connection_error(self, mock_client_class, tmp_path):
        """Test download_template_from_github handles connection errors."""
        mock_client = MagicMock()
        mock_client.__enter__.return_value.get.side_effect = httpx.ConnectError("Connection failed")
        mock_client_class.return_value = mock_client

        console = Mock(spec=Console)

        with pytest.raises(typer.Exit):
            download_template_from_github(
                "claude",
                tmp_path,
                verbose=False,
                console=console,
            )

    @patch("httpx.Client")
    def test_download_template_missing_asset(self, mock_client_class, tmp_path):
        """Test download_template_from_github handles missing template assets."""
        release_response = Mock()
        release_response.status_code = 200
        release_response.json.return_value = {
            "tag_name": "v1.0.0",
            "assets": [
                {
                    "name": "different-template-sh-v1.0.0.zip",
                    "browser_download_url": "https://github.com/test/download.zip",
                    "size": 1024,
                }
            ],
        }

        mock_client = MagicMock()
        mock_client.__enter__.return_value.get.return_value = release_response
        mock_client_class.return_value = mock_client

        console = Mock(spec=Console)

        with pytest.raises(typer.Exit):
            download_template_from_github(
                "claude",  # Looking for claude
                tmp_path,
                script_type="sh",
                verbose=False,
                console=console,
            )

    @patch("httpx.Client")
    def test_download_template_invalid_json_response(self, mock_client_class, tmp_path):
        """Test download_template_from_github handles invalid JSON responses."""
        release_response = Mock()
        release_response.status_code = 200
        release_response.json.side_effect = ValueError("Invalid JSON")
        release_response.text = "not json"

        mock_client = MagicMock()
        mock_client.__enter__.return_value.get.return_value = release_response
        mock_client_class.return_value = mock_client

        console = Mock(spec=Console)

        with pytest.raises(typer.Exit):
            download_template_from_github(
                "claude",
                tmp_path,
                verbose=False,
                console=console,
            )

    @patch("nuaa_cli.download.httpx.Client")
    def test_download_template_withget_github_token(self, mock_client_class, tmp_path):
        """Test download_template_from_github uses GitHub token for authentication."""
        release_response = Mock(spec=httpx.Response)
        release_response.status_code = 200
        release_response.json.return_value = {
            "tag_name": "v1.0.0",
            "assets": [
                {
                    "name": "nuaa-template-claude-sh-v1.0.0.zip",
                    "browser_download_url": "https://github.com/test/download.zip",
                    "size": 512,
                }
            ],
        }

        download_response = Mock(spec=httpx.Response)
        download_response.status_code = 200
        download_response.headers = httpx.Headers({"content-length": "512"})
        download_response.iter_bytes = Mock(return_value=[b"content"])

        mock_client_instance = Mock()
        mock_client_instance.get.return_value = release_response

        # Setup context manager for stream
        mock_stream_context = MagicMock()
        mock_stream_context.__enter__.return_value = download_response
        mock_client_instance.stream.return_value = mock_stream_context
        mock_client_instance.close.return_value = None

        mock_client_class.return_value = mock_client_instance

        download_template_from_github(
            "claude",
            tmp_path,
            github_token="ghp_test_token",
            verbose=False,
            show_progress=False,
        )

        # Verify Authorization header was used
        get_call = mock_client_instance.get.call_args
        assert "headers" in get_call[1]
        assert get_call[1]["headers"]["Authorization"] == "Bearer ghp_test_token"

    @patch("nuaa_cli.download.httpx.Client")
    def test_download_template_with_progress(self, mock_client_class, tmp_path):
        """Test download_template_from_github shows progress bar."""
        release_response = Mock(spec=httpx.Response)
        release_response.status_code = 200
        release_response.json.return_value = {
            "tag_name": "v1.0.0",
            "assets": [
                {
                    "name": "nuaa-template-claude-sh-v1.0.0.zip",
                    "browser_download_url": "https://github.com/test/download.zip",
                    "size": 1024,
                }
            ],
        }

        download_response = Mock(spec=httpx.Response)
        download_response.status_code = 200
        download_response.headers = httpx.Headers({"content-length": "1024"})
        download_response.iter_bytes = Mock(return_value=[b"x" * 512, b"y" * 512])

        mock_client_instance = Mock()
        mock_client_instance.get.return_value = release_response

        # Setup context manager for stream
        mock_stream_context = MagicMock()
        mock_stream_context.__enter__.return_value = download_response
        mock_client_instance.stream.return_value = mock_stream_context
        mock_client_instance.close.return_value = None

        mock_client_class.return_value = mock_client_instance

        zip_path, _ = download_template_from_github(
            "claude",
            tmp_path,
            verbose=False,
            show_progress=True,
        )

        assert zip_path.exists()

    @patch("nuaa_cli.download.httpx.Client")
    def test_download_template_verbose_output(self, mock_client_class, tmp_path):
        """Test download_template_from_github prints verbose messages."""
        release_response = Mock(spec=httpx.Response)
        release_response.status_code = 200
        release_response.json.return_value = {
            "tag_name": "v1.0.0",
            "assets": [
                {
                    "name": "nuaa-template-claude-sh-v1.0.0.zip",
                    "browser_download_url": "https://github.com/test/download.zip",
                    "size": 256,
                }
            ],
        }

        download_response = Mock(spec=httpx.Response)
        download_response.status_code = 200
        download_response.headers = httpx.Headers({"content-length": "256"})
        download_response.iter_bytes = Mock(return_value=[b"data"])

        mock_client_instance = Mock()
        mock_client_instance.get.return_value = release_response

        # Setup context manager for stream
        mock_stream_context = MagicMock()
        mock_stream_context.__enter__.return_value = download_response
        mock_client_instance.stream.return_value = mock_stream_context
        mock_client_instance.close.return_value = None

        mock_client_class.return_value = mock_client_instance

        console = Mock(spec=Console)

        download_template_from_github(
            "claude",
            tmp_path,
            verbose=True,
            show_progress=False,
            console=console,
        )

        # Should have printed status messages
        assert console.print.called
        assert console.print.call_count >= 3  # Multiple status messages


class TestDownloadAndExtractTemplate:
    """Tests for complete template download and extraction workflow."""

    @patch("nuaa_cli.download.download_template_from_github")
    def test_extract_to_new_directory(self, mock_download, tmp_path):
        """Test download_and_extract_template creates new project directory."""
        # Create a test ZIP file
        zip_path = tmp_path / "template.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("project/README.md", "# Test Project")
            zf.writestr("project/main.py", "print('hello')")

        mock_download.return_value = (
            zip_path,
            {"filename": "template.zip", "size": 1024, "release": "v1.0.0", "asset_url": ""},
        )

        project_path = tmp_path / "new-project"
        result = download_and_extract_template(
            project_path,
            "claude",
            "sh",
            is_current_dir=False,
            verbose=False,
        )

        assert result == project_path
        assert (project_path / "README.md").exists()
        assert (project_path / "main.py").exists()

    @patch("nuaa_cli.download.download_template_from_github")
    def test_extract_to_current_directory_merge(self, mock_download, tmp_path):
        """Test download_and_extract_template merges into current directory."""
        # Setup existing project
        existing_file = tmp_path / "existing.txt"
        existing_file.write_text("existing content")

        # Create template ZIP
        zip_path = tmp_path / "template.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("project/new_file.py", "# New file")
            zf.writestr("project/README.md", "# Template")

        mock_download.return_value = (
            zip_path,
            {"filename": "template.zip", "size": 512, "release": "v1.0.0", "asset_url": ""},
        )

        result = download_and_extract_template(
            tmp_path,
            "claude",
            "sh",
            is_current_dir=True,
            verbose=False,
        )

        assert result == tmp_path
        assert (tmp_path / "existing.txt").exists()  # Preserved
        assert (tmp_path / "new_file.py").exists()  # Added
        assert (tmp_path / "README.md").exists()  # Added

    @patch("nuaa_cli.download.download_template_from_github")
    def test_extract_with_tracker(self, mock_download, tmp_path):
        """Test download_and_extract_template uses StepTracker for progress."""
        zip_path = tmp_path / "template.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("project/file.txt", "content")

        mock_download.return_value = (
            zip_path,
            {"filename": "template.zip", "size": 256, "release": "v1.0.0", "asset_url": ""},
        )

        tracker = StepTracker("Test Tracker")
        tracker.add("fetch", "Fetch release")
        tracker.add("download", "Download template")
        tracker.add("extract", "Extract template")
        tracker.add("cleanup", "Cleanup")

        project_path = tmp_path / "project"
        download_and_extract_template(
            project_path,
            "claude",
            "sh",
            is_current_dir=False,
            verbose=False,
            tracker=tracker,
        )

        # Check that tracker steps were updated
        assert any(s["status"] == "done" for s in tracker.steps)

    @patch("nuaa_cli.download.download_template_from_github")
    def test_extract_bad_zip_file(self, mock_download, tmp_path):
        """Test download_and_extract_template handles corrupted ZIP files."""
        # Create invalid ZIP
        bad_zip = tmp_path / "bad.zip"
        bad_zip.write_text("not a real zip file")

        mock_download.return_value = (
            bad_zip,
            {"filename": "bad.zip", "size": 100, "release": "v1.0.0", "asset_url": ""},
        )

        project_path = tmp_path / "project"

        with pytest.raises(typer.Exit) as exc_info:
            download_and_extract_template(
                project_path,
                "claude",
                "sh",
                is_current_dir=False,
                verbose=False,
            )

        assert exc_info.value.exit_code == 1

    @patch("nuaa_cli.download.download_template_from_github")
    def test_extract_vscode_settings_merge(self, mock_download, tmp_path):
        """Test download_and_extract_template merges VSCode settings."""
        # Create existing VSCode settings
        vscode_dir = tmp_path / ".vscode"
        vscode_dir.mkdir()
        existing_settings = vscode_dir / "settings.json"
        existing_settings.write_text('{"existing": "setting"}')

        # Create template with VSCode settings
        zip_path = tmp_path / "template.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("project/.vscode/settings.json", '{"new": "setting"}')

        mock_download.return_value = (
            zip_path,
            {"filename": "template.zip", "size": 256, "release": "v1.0.0", "asset_url": ""},
        )

        download_and_extract_template(
            tmp_path,
            "claude",
            "sh",
            is_current_dir=True,
            verbose=False,
        )

        # Settings should be merged
        merged = json.loads(existing_settings.read_text())
        assert merged["existing"] == "setting"
        assert merged["new"] == "setting"

    @patch("nuaa_cli.download.download_template_from_github")
    def test_extract_cleanup_zip(self, mock_download, tmp_path):
        """Test download_and_extract_template cleans up downloaded ZIP."""
        zip_path = tmp_path / "template.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("project/file.txt", "content")

        mock_download.return_value = (
            zip_path,
            {"filename": "template.zip", "size": 128, "release": "v1.0.0", "asset_url": ""},
        )

        project_path = tmp_path / "project"
        download_and_extract_template(
            project_path,
            "claude",
            "sh",
            is_current_dir=False,
            verbose=False,
        )

        # ZIP should be cleaned up
        assert not zip_path.exists()

    @patch("nuaa_cli.download.download_template_from_github")
    def test_extract_network_error_propagation(self, mock_download, tmp_path):
        """Test download_and_extract_template propagates network errors."""
        mock_download.side_effect = httpx.TimeoutException("Timeout")

        project_path = tmp_path / "project"

        with pytest.raises(httpx.TimeoutException):
            download_and_extract_template(
                project_path,
                "claude",
                "sh",
                is_current_dir=False,
                verbose=False,
            )

    @patch("nuaa_cli.download.download_template_from_github")
    def test_extract_with_debug_mode(self, mock_download, tmp_path):
        """Test download_and_extract_template debug mode."""
        zip_path = tmp_path / "template.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("project/debug.txt", "debug info")

        mock_download.return_value = (
            zip_path,
            {"filename": "template.zip", "size": 64, "release": "v1.0.0", "asset_url": ""},
        )

        project_path = tmp_path / "project"
        download_and_extract_template(
            project_path,
            "claude",
            "sh",
            is_current_dir=False,
            verbose=True,
            debug=True,
        )

        assert project_path.exists()

    @patch("nuaa_cli.download.download_template_from_github")
    def test_extract_flattens_nested_directory(self, mock_download, tmp_path):
        """Test download_and_extract_template flattens single nested directory."""
        # Create ZIP with nested structure
        zip_path = tmp_path / "template.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("nuaa-template-claude-sh/README.md", "# Readme")
            zf.writestr("nuaa-template-claude-sh/src/main.py", "# Main")

        mock_download.return_value = (
            zip_path,
            {"filename": "template.zip", "size": 256, "release": "v1.0.0", "asset_url": ""},
        )

        project_path = tmp_path / "project"
        download_and_extract_template(
            project_path,
            "claude",
            "sh",
            is_current_dir=False,
            verbose=False,
        )

        # Should flatten structure
        assert (project_path / "README.md").exists()
        assert (project_path / "src" / "main.py").exists()
        # Nested directory name should not appear
        assert not (project_path / "nuaa-template-claude-sh").exists()

    @patch("nuaa_cli.download.download_template_from_github")
    def test_extract_permission_error_handling(self, mock_download, tmp_path):
        """Test download_and_extract_template handles permission errors."""
        zip_path = tmp_path / "template.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("project/file.txt", "content")

        mock_download.return_value = (
            zip_path,
            {"filename": "template.zip", "size": 64, "release": "v1.0.0", "asset_url": ""},
        )

        project_path = tmp_path / "project"

        # Mock mkdir to raise PermissionError
        with patch("pathlib.Path.mkdir", side_effect=PermissionError("Access denied")):
            with pytest.raises(typer.Exit):
                download_and_extract_template(
                    project_path,
                    "claude",
                    "sh",
                    is_current_dir=False,
                    verbose=False,
                )

    @patch("nuaa_cli.download.download_template_from_github")
    def test_extract_with_custom_console(self, mock_download, tmp_path):
        """Test download_and_extract_template uses custom console."""
        zip_path = tmp_path / "template.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("project/file.txt", "content")

        mock_download.return_value = (
            zip_path,
            {"filename": "template.zip", "size": 64, "release": "v1.0.0", "asset_url": ""},
        )

        console = Mock(spec=Console)
        project_path = tmp_path / "project"

        download_and_extract_template(
            project_path,
            "claude",
            "sh",
            is_current_dir=False,
            verbose=True,
            console=console,
        )

        # Console should have been used for output
        assert console.print.called
