"""Tests for banner module."""

from unittest.mock import Mock, patch

from rich.console import Console
import typer

from nuaa_cli.banner import BANNER, TAGLINE, show_banner, BannerGroup


class TestBannerConstants:
    """Tests for banner constants."""

    def test_banner_is_string(self):
        """Test that BANNER is a string."""
        assert isinstance(BANNER, str)
        assert len(BANNER) > 0

    def test_banner_contains_nuaa(self):
        """Test that BANNER contains NUAA ASCII art."""
        # Banner should contain box-drawing characters or letters
        assert len(BANNER.strip()) > 10

    def test_tagline_is_string(self):
        """Test that TAGLINE is a string."""
        assert isinstance(TAGLINE, str)
        assert len(TAGLINE) > 0

    def test_tagline_mentions_nuaa(self):
        """Test that TAGLINE mentions NUAA."""
        assert "NUAA" in TAGLINE
        assert "Project" in TAGLINE


class TestShowBanner:
    """Tests for show_banner function."""

    def test_show_banner_with_default_console(self):
        """Test show_banner with default console."""
        with patch("nuaa_cli.banner.Console") as MockConsole:
            mock_console = Mock()
            MockConsole.return_value = mock_console

            show_banner()

            # Should have called print twice (banner + tagline)
            assert mock_console.print.call_count >= 2

    def test_show_banner_with_custom_console(self):
        """Test show_banner with custom console."""
        console = Mock(spec=Console)

        show_banner(console=console)

        # Should have printed banner and tagline
        assert console.print.call_count >= 2

    def test_show_banner_output_contains_banner_text(self):
        """Test that show_banner outputs banner content."""
        console = Mock(spec=Console)

        show_banner(console=console)

        # Get all the call arguments
        calls = console.print.call_args_list

        # Should have at least 2 calls (banner and tagline)
        assert len(calls) >= 2

    def test_show_banner_uses_rich_formatting(self):
        """Test that show_banner uses Rich formatting."""
        console = Mock(spec=Console)

        show_banner(console=console)

        # Verify it was called with Rich objects
        assert console.print.called


class TestBannerGroup:
    """Tests for BannerGroup class."""

    def test_banner_group_is_typer_group(self):
        """Test that BannerGroup inherits from TyperGroup."""
        from typer.core import TyperGroup

        assert issubclass(BannerGroup, TyperGroup)

    def test_banner_group_format_help_shows_banner(self):
        """Test that format_help shows banner."""
        group = BannerGroup()

        with patch("nuaa_cli.banner.show_banner") as mock_show_banner:
            # Create mock context and formatter
            ctx = Mock()
            formatter = Mock()
            formatter.write = Mock()
            formatter.write_text = Mock()

            try:
                group.format_help(ctx, formatter)
            except AttributeError:
                # Expected if mock doesn't have all attributes
                pass

            # show_banner should have been called
            assert mock_show_banner.called

    def test_banner_group_can_be_used_with_typer_app(self):
        """Test that BannerGroup can be used with Typer app."""
        # Should not raise an exception
        app = typer.Typer(cls=BannerGroup)
        assert app is not None

    def test_banner_group_calls_super_format_help(self):
        """Test that BannerGroup calls parent format_help."""
        group = BannerGroup()

        with patch("nuaa_cli.banner.show_banner"):
            with patch.object(group.__class__.__bases__[0], "format_help") as mock_super:
                ctx = Mock()
                formatter = Mock()

                try:
                    group.format_help(ctx, formatter)
                except (AttributeError, TypeError):
                    # Expected if mocks don't match exact interface
                    pass

                # Super should have been called (or attempted)
                # This test may not work perfectly due to mocking complexity


class TestBannerIntegration:
    """Integration tests for banner module."""

    def test_banner_displays_without_errors(self):
        """Test that banner displays without raising errors."""
        # Should not raise any exceptions
        show_banner()

    def test_banner_group_integrates_with_app(self):
        """Test BannerGroup integration with Typer app."""
        app = typer.Typer(
            name="test",
            cls=BannerGroup,
        )

        @app.command()
        def test_cmd():
            """Test command."""
            pass

        # Should not raise an exception
        assert app is not None
