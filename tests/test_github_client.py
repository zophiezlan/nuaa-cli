"""Tests for github_client module."""

import os
from unittest.mock import Mock, patch, MagicMock
import pytest
import httpx

from nuaa_cli.github_client import (
    GitHubClient,
    GitHubRateLimitError,
)


class TestGitHubClient:
    """Tests for GitHubClient class."""

    def test_init_without_token(self):
        """Test GitHubClient initialization without token."""
        client = GitHubClient()
        assert client.token is None or client.token == ""
        assert client.base_url == "https://api.github.com"

    def test_init_with_token(self):
        """Test GitHubClient initialization with token."""
        client = GitHubClient(token="test_token_123")
        assert client.token == "test_token_123"

    @patch.dict(os.environ, {"GITHUB_TOKEN": "env_token_456"})
    def test_get_token_from_env_github_token(self):
        """Test getting token from GITHUB_TOKEN environment variable."""
        client = GitHubClient()
        assert client.token == "env_token_456"

    @patch.dict(os.environ, {"GH_TOKEN": "gh_token_789"})
    def test_get_token_from_env_gh_token(self):
        """Test getting token from GH_TOKEN environment variable."""
        client = GitHubClient()
        assert client.token == "gh_token_789"

    def test_get_headers_with_token(self):
        """Test headers are set when token is provided."""
        client = GitHubClient(token="test_token")
        headers = client._get_headers()
        assert "Authorization" in headers
        assert headers["Authorization"] == "Bearer test_token"

    def test_get_headers_without_token(self):
        """Test headers without token."""
        client = GitHubClient(token=None)
        headers = client._get_headers()
        # Should still have Accept header
        assert "Accept" in headers

    def test_parse_rate_limit_headers(self):
        """Test parsing rate limit headers from GitHub API response."""
        mock_headers = httpx.Headers(
            {
                "X-RateLimit-Limit": "60",
                "X-RateLimit-Remaining": "59",
                "X-RateLimit-Reset": "1700000000",
            }
        )
        client = GitHubClient()
        info = client._parse_rate_limit_headers(mock_headers)

        assert info["limit"] == "60"
        assert info["remaining"] == "59"
        assert info["reset_epoch"] == 1700000000

    def test_parse_rate_limit_headers_empty(self):
        """Test parsing when rate limit headers are not present."""
        mock_headers = httpx.Headers({})
        client = GitHubClient()
        info = client._parse_rate_limit_headers(mock_headers)

        assert "limit" not in info
        assert "remaining" not in info

    @patch("httpx.Client")
    def test_get_latest_release_success(self, mock_client_class):
        """Test getting latest release from GitHub API."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "tag_name": "v1.0.0",
            "name": "Release 1.0.0",
            "assets": [],
        }

        mock_client = MagicMock()
        mock_client.__enter__.return_value.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = GitHubClient()
        release = client.get_latest_release("owner", "repo")

        assert release is not None
        assert release["tag_name"] == "v1.0.0"

    @patch("httpx.Client")
    def test_get_latest_release_rate_limit(self, mock_client_class):
        """Test rate limit handling when fetching latest release."""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.headers = httpx.Headers(
            {"X-RateLimit-Remaining": "0", "X-RateLimit-Reset": "1700000000"}
        )

        mock_client = MagicMock()
        mock_client.__enter__.return_value.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = GitHubClient()
        with pytest.raises(GitHubRateLimitError):
            client.get_latest_release("owner", "repo")

    @patch("httpx.Client")
    def test_get_latest_release_not_found(self, mock_client_class):
        """Test handling when release is not found."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.headers = httpx.Headers({})

        mock_client = MagicMock()
        mock_client.__enter__.return_value.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = GitHubClient()

        # Should raise RuntimeError for 404
        with pytest.raises(RuntimeError):
            client.get_latest_release("owner", "repo")

    def test_format_rate_limit_error(self):
        """Test formatting rate limit error message."""
        mock_headers = httpx.Headers(
            {
                "X-RateLimit-Limit": "60",
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": "1700000000",
            }
        )

        client = GitHubClient()
        formatted = client._format_rate_limit_error(
            403, mock_headers, "https://api.github.com/test"
        )

        assert "403" in formatted or "rate limit" in formatted.lower()

    def test_debug_mode(self):
        """Test that debug mode is properly set."""
        client = GitHubClient(debug=True)
        assert client.debug is True

        client = GitHubClient(debug=False)
        assert client.debug is False


class TestGitHubRateLimitError:
    """Tests for GitHubRateLimitError exception."""

    def test_exception_can_be_raised(self):
        """Test that GitHubRateLimitError can be raised and caught."""
        with pytest.raises(GitHubRateLimitError):
            raise GitHubRateLimitError("Rate limit exceeded")

    def test_exception_message(self):
        """Test that GitHubRateLimitError preserves message."""
        msg = "Rate limit exceeded. Try again later."
        try:
            raise GitHubRateLimitError(msg)
        except GitHubRateLimitError as e:
            assert str(e) == msg
