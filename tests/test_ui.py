"""
Tests for UI module (keyboard input handling and interactive selection).

This module tests the interactive UI utilities including keyboard input
normalization and arrow-key selection menus using mocked readchar input.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import typer
from rich.console import Console

from nuaa_cli.ui import get_key, select_with_arrows


class TestGetKey:
    """Tests for the get_key() function."""

    def test_get_key_up_arrow(self):
        """Test that UP arrow key is normalized to 'up'."""
        with patch("nuaa_cli.ui.readchar.readkey") as mock_readkey:
            with patch("nuaa_cli.ui.readchar.key") as mock_key:
                mock_key.UP = "\x1b[A"
                mock_key.CTRL_P = "\x10"
                mock_readkey.return_value = mock_key.UP

                result = get_key()
                assert result == "up"

    def test_get_key_ctrl_p_as_up(self):
        """Test that Ctrl+P is normalized to 'up'."""
        with patch("nuaa_cli.ui.readchar.readkey") as mock_readkey:
            with patch("nuaa_cli.ui.readchar.key") as mock_key:
                mock_key.UP = "\x1b[A"
                mock_key.CTRL_P = "\x10"
                mock_readkey.return_value = mock_key.CTRL_P

                result = get_key()
                assert result == "up"

    def test_get_key_down_arrow(self):
        """Test that DOWN arrow key is normalized to 'down'."""
        with patch("nuaa_cli.ui.readchar.readkey") as mock_readkey:
            with patch("nuaa_cli.ui.readchar.key") as mock_key:
                mock_key.DOWN = "\x1b[B"
                mock_key.CTRL_N = "\x0e"
                mock_readkey.return_value = mock_key.DOWN

                result = get_key()
                assert result == "down"

    def test_get_key_ctrl_n_as_down(self):
        """Test that Ctrl+N is normalized to 'down'."""
        with patch("nuaa_cli.ui.readchar.readkey") as mock_readkey:
            with patch("nuaa_cli.ui.readchar.key") as mock_key:
                mock_key.DOWN = "\x1b[B"
                mock_key.CTRL_N = "\x0e"
                mock_readkey.return_value = mock_key.CTRL_N

                result = get_key()
                assert result == "down"

    def test_get_key_enter(self):
        """Test that ENTER key is normalized to 'enter'."""
        with patch("nuaa_cli.ui.readchar.readkey") as mock_readkey:
            with patch("nuaa_cli.ui.readchar.key") as mock_key:
                mock_key.ENTER = "\r"
                mock_readkey.return_value = mock_key.ENTER

                result = get_key()
                assert result == "enter"

    def test_get_key_escape(self):
        """Test that ESC key is normalized to 'escape'."""
        with patch("nuaa_cli.ui.readchar.readkey") as mock_readkey:
            with patch("nuaa_cli.ui.readchar.key") as mock_key:
                mock_key.ESC = "\x1b"
                mock_readkey.return_value = mock_key.ESC

                result = get_key()
                assert result == "escape"

    def test_get_key_ctrl_c_raises_keyboard_interrupt(self):
        """Test that Ctrl+C raises KeyboardInterrupt."""
        with patch("nuaa_cli.ui.readchar.readkey") as mock_readkey:
            with patch("nuaa_cli.ui.readchar.key") as mock_key:
                mock_key.CTRL_C = "\x03"
                mock_readkey.return_value = mock_key.CTRL_C

                with pytest.raises(KeyboardInterrupt):
                    get_key()

    def test_get_key_other_key_returned_as_is(self):
        """Test that other keys are returned unchanged."""
        with patch("nuaa_cli.ui.readchar.readkey") as mock_readkey:
            mock_readkey.return_value = "a"

            result = get_key()
            assert result == "a"


class TestSelectWithArrows:
    """Tests for the select_with_arrows() function."""

    def test_select_with_arrows_basic_selection(self):
        """Test basic selection with Enter key on first option."""
        options = {
            "claude": "Claude by Anthropic",
            "copilot": "GitHub Copilot",
            "cursor": "Cursor AI"
        }

        with patch("nuaa_cli.ui.get_key") as mock_get_key:
            # Simulate pressing Enter immediately
            mock_get_key.return_value = "enter"

            result = select_with_arrows(options, "Choose an AI agent")

            # Should select the first option (claude)
            assert result == "claude"

    def test_select_with_arrows_navigate_down_and_select(self):
        """Test navigating down and selecting second option."""
        options = {
            "claude": "Claude by Anthropic",
            "copilot": "GitHub Copilot",
            "cursor": "Cursor AI"
        }

        with patch("nuaa_cli.ui.get_key") as mock_get_key:
            # Simulate: down arrow, then Enter
            mock_get_key.side_effect = ["down", "enter"]

            result = select_with_arrows(options, "Choose an AI agent")

            # Should select the second option (copilot)
            assert result == "copilot"

    def test_select_with_arrows_navigate_multiple_times(self):
        """Test navigating multiple times before selecting."""
        options = {
            "claude": "Claude by Anthropic",
            "copilot": "GitHub Copilot",
            "cursor": "Cursor AI"
        }

        with patch("nuaa_cli.ui.get_key") as mock_get_key:
            # Simulate: down, down, then Enter
            mock_get_key.side_effect = ["down", "down", "enter"]

            result = select_with_arrows(options, "Choose an AI agent")

            # Should select the third option (cursor)
            assert result == "cursor"

    def test_select_with_arrows_wrap_around_down(self):
        """Test that navigating down wraps around to first option."""
        options = {
            "claude": "Claude by Anthropic",
            "copilot": "GitHub Copilot",
            "cursor": "Cursor AI"
        }

        with patch("nuaa_cli.ui.get_key") as mock_get_key:
            # Simulate: down x3 (wraps to first), then Enter
            mock_get_key.side_effect = ["down", "down", "down", "enter"]

            result = select_with_arrows(options, "Choose an AI agent")

            # Should wrap around to first option (claude)
            assert result == "claude"

    def test_select_with_arrows_navigate_up(self):
        """Test navigating up (wraps to last option)."""
        options = {
            "claude": "Claude by Anthropic",
            "copilot": "GitHub Copilot",
            "cursor": "Cursor AI"
        }

        with patch("nuaa_cli.ui.get_key") as mock_get_key:
            # Simulate: up (wraps to last), then Enter
            mock_get_key.side_effect = ["up", "enter"]

            result = select_with_arrows(options, "Choose an AI agent")

            # Should wrap to last option (cursor)
            assert result == "cursor"

    def test_select_with_arrows_up_and_down_navigation(self):
        """Test navigating both up and down before selecting."""
        options = {
            "claude": "Claude by Anthropic",
            "copilot": "GitHub Copilot",
            "cursor": "Cursor AI"
        }

        with patch("nuaa_cli.ui.get_key") as mock_get_key:
            # Simulate: down, down, up, then Enter
            mock_get_key.side_effect = ["down", "down", "up", "enter"]

            result = select_with_arrows(options, "Choose an AI agent")

            # Should be on second option (copilot)
            assert result == "copilot"

    def test_select_with_arrows_escape_cancels(self):
        """Test that pressing Escape cancels selection."""
        options = {
            "claude": "Claude by Anthropic",
            "copilot": "GitHub Copilot"
        }

        with patch("nuaa_cli.ui.get_key") as mock_get_key:
            # Simulate: Escape key
            mock_get_key.return_value = "escape"

            with pytest.raises(typer.Exit) as exc_info:
                select_with_arrows(options, "Choose an AI agent")

            assert exc_info.value.exit_code == 1

    def test_select_with_arrows_keyboard_interrupt_cancels(self):
        """Test that KeyboardInterrupt (Ctrl+C) cancels selection."""
        options = {
            "claude": "Claude by Anthropic",
            "copilot": "GitHub Copilot"
        }

        with patch("nuaa_cli.ui.get_key") as mock_get_key:
            # Simulate: Ctrl+C (raises KeyboardInterrupt)
            mock_get_key.side_effect = KeyboardInterrupt()

            with pytest.raises(typer.Exit) as exc_info:
                select_with_arrows(options, "Choose an AI agent")

            assert exc_info.value.exit_code == 1

    def test_select_with_arrows_default_key(self):
        """Test starting with a default key selection."""
        options = {
            "claude": "Claude by Anthropic",
            "copilot": "GitHub Copilot",
            "cursor": "Cursor AI"
        }

        with patch("nuaa_cli.ui.get_key") as mock_get_key:
            # Start on copilot, then press Enter immediately
            mock_get_key.return_value = "enter"

            result = select_with_arrows(
                options,
                "Choose an AI agent",
                default_key="copilot"
            )

            # Should select copilot (the default)
            assert result == "copilot"

    def test_select_with_arrows_default_key_then_navigate(self):
        """Test starting with default key and then navigating."""
        options = {
            "claude": "Claude by Anthropic",
            "copilot": "GitHub Copilot",
            "cursor": "Cursor AI"
        }

        with patch("nuaa_cli.ui.get_key") as mock_get_key:
            # Start on cursor, navigate down (wrap to claude), then Enter
            mock_get_key.side_effect = ["down", "enter"]

            result = select_with_arrows(
                options,
                "Choose an AI agent",
                default_key="cursor"
            )

            # Should wrap from cursor to claude
            assert result == "claude"

    def test_select_with_arrows_invalid_default_key(self):
        """Test that invalid default key falls back to first option."""
        options = {
            "claude": "Claude by Anthropic",
            "copilot": "GitHub Copilot"
        }

        with patch("nuaa_cli.ui.get_key") as mock_get_key:
            # Invalid default, should start on first (claude)
            mock_get_key.return_value = "enter"

            result = select_with_arrows(
                options,
                "Choose an AI agent",
                default_key="invalid_key"
            )

            # Should fall back to first option (claude)
            assert result == "claude"

    def test_select_with_arrows_custom_console(self):
        """Test using a custom Rich console."""
        options = {
            "claude": "Claude by Anthropic",
            "copilot": "GitHub Copilot"
        }

        custom_console = Console()

        with patch("nuaa_cli.ui.get_key") as mock_get_key:
            mock_get_key.return_value = "enter"

            result = select_with_arrows(
                options,
                "Choose an AI agent",
                console=custom_console
            )

            assert result == "claude"

    def test_select_with_arrows_single_option(self):
        """Test selection with only one option available."""
        options = {
            "claude": "Claude by Anthropic"
        }

        with patch("nuaa_cli.ui.get_key") as mock_get_key:
            mock_get_key.return_value = "enter"

            result = select_with_arrows(options, "Choose an AI agent")

            assert result == "claude"

    def test_select_with_arrows_single_option_navigation(self):
        """Test that navigation with single option wraps to itself."""
        options = {
            "claude": "Claude by Anthropic"
        }

        with patch("nuaa_cli.ui.get_key") as mock_get_key:
            # Navigate up and down, should stay on same option
            mock_get_key.side_effect = ["down", "up", "down", "enter"]

            result = select_with_arrows(options, "Choose an AI agent")

            assert result == "claude"

    def test_select_with_arrows_custom_prompt_text(self):
        """Test with custom prompt text."""
        options = {
            "yes": "Proceed with action",
            "no": "Cancel action"
        }

        with patch("nuaa_cli.ui.get_key") as mock_get_key:
            mock_get_key.return_value = "enter"

            result = select_with_arrows(
                options,
                "Do you want to continue?"
            )

            assert result == "yes"


class TestSelectWithArrowsIntegration:
    """Integration tests for select_with_arrows()."""

    def test_complex_navigation_pattern(self):
        """Test complex navigation pattern with multiple ups and downs."""
        options = {
            "option1": "First option",
            "option2": "Second option",
            "option3": "Third option",
            "option4": "Fourth option",
            "option5": "Fifth option"
        }

        with patch("nuaa_cli.ui.get_key") as mock_get_key:
            # Complex pattern: down x2, up, down x3, up x2, enter
            mock_get_key.side_effect = [
                "down", "down",  # -> option3
                "up",             # -> option2
                "down", "down", "down",  # -> option5
                "up", "up",       # -> option3
                "enter"
            ]

            result = select_with_arrows(options, "Select an option")

            assert result == "option3"

    def test_full_cycle_navigation(self):
        """Test navigating through all options in both directions."""
        options = {
            "a": "Option A",
            "b": "Option B",
            "c": "Option C"
        }

        with patch("nuaa_cli.ui.get_key") as mock_get_key:
            # Navigate down through all, wrap around, go up, select
            mock_get_key.side_effect = [
                "down", "down", "down",  # Back to 'a' (wrapped)
                "up",                     # Wrap to 'c'
                "enter"
            ]

            result = select_with_arrows(options, "Select")

            assert result == "c"
