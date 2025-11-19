"""
Tests for accessibility module.

This module tests accessibility features including screen reader support,
output modes, and accessible formatting for diverse user needs.
"""

import os
from unittest.mock import patch

from nuaa_cli.accessibility import (
    OutputMode,
    AccessibilityConfig,
    get_config,
    is_screen_reader_active,
    get_output_mode,
    set_output_mode,
    format_for_accessibility,
    announce_for_screen_reader,
    get_navigation_hints,
    format_progress,
    get_line_length,
    should_use_emoji,
)


class TestOutputMode:
    """Tests for OutputMode enum."""

    def test_output_mode_values(self):
        """Test that all output modes are defined."""
        assert OutputMode.STANDARD.value == "standard"
        assert OutputMode.SCREEN_READER.value == "screen_reader"
        assert OutputMode.HIGH_CONTRAST.value == "high_contrast"
        assert OutputMode.NO_COLOR.value == "no_color"
        assert OutputMode.DYSLEXIA_FRIENDLY.value == "dyslexia_friendly"
        assert OutputMode.SIMPLE.value == "simple"

    def test_output_mode_count(self):
        """Test that we have all expected output modes."""
        modes = list(OutputMode)
        assert len(modes) == 6


class TestAccessibilityConfig:
    """Tests for AccessibilityConfig class."""

    def test_config_default_initialization(self):
        """Test default config initialization."""
        with patch.dict(os.environ, {}, clear=True):
            config = AccessibilityConfig()

            assert config.output_mode == OutputMode.STANDARD
            assert config.audio_feedback is False
            assert config.verbose_navigation is False
            assert config.simple_mode is False
            assert config.screen_reader_optimized is False

    def test_config_detects_nvda_screen_reader(self):
        """Test config detects NVDA screen reader."""
        with patch.dict(os.environ, {"NVDA": "1"}, clear=True):
            config = AccessibilityConfig()

            assert config.screen_reader_optimized is True
            assert config.output_mode == OutputMode.SCREEN_READER

    def test_config_detects_jaws_screen_reader(self):
        """Test config detects JAWS screen reader."""
        with patch.dict(os.environ, {"JAWS": "1"}, clear=True):
            config = AccessibilityConfig()

            assert config.screen_reader_optimized is True
            assert config.output_mode == OutputMode.SCREEN_READER

    def test_config_detects_orca_screen_reader(self):
        """Test config detects ORCA screen reader (Linux)."""
        with patch.dict(os.environ, {"ORCA": "1"}, clear=True):
            config = AccessibilityConfig()

            assert config.screen_reader_optimized is True
            assert config.output_mode == OutputMode.SCREEN_READER

    def test_config_detects_high_contrast_mode(self):
        """Test config detects high contrast preference."""
        with patch.dict(os.environ, {"NUAA_HIGH_CONTRAST": "1"}, clear=True):
            config = AccessibilityConfig()

            assert config.output_mode == OutputMode.HIGH_CONTRAST

    def test_config_detects_no_color_preference(self):
        """Test config detects NO_COLOR environment variable."""
        with patch.dict(os.environ, {"NO_COLOR": "1"}, clear=True):
            config = AccessibilityConfig()

            assert config.output_mode == OutputMode.NO_COLOR

    def test_config_detects_nuaa_no_color(self):
        """Test config detects NUAA_NO_COLOR environment variable."""
        with patch.dict(os.environ, {"NUAA_NO_COLOR": "1"}, clear=True):
            config = AccessibilityConfig()

            assert config.output_mode == OutputMode.NO_COLOR

    def test_config_detects_dyslexia_friendly_mode(self):
        """Test config detects dyslexia-friendly preference."""
        with patch.dict(os.environ, {"NUAA_DYSLEXIA_FRIENDLY": "1"}, clear=True):
            config = AccessibilityConfig()

            assert config.output_mode == OutputMode.DYSLEXIA_FRIENDLY

    def test_config_detects_simple_mode(self):
        """Test config detects simple mode for cognitive accessibility."""
        with patch.dict(os.environ, {"NUAA_SIMPLE_MODE": "1"}, clear=True):
            config = AccessibilityConfig()

            assert config.simple_mode is True

    def test_config_detects_audio_feedback(self):
        """Test config detects audio feedback preference."""
        with patch.dict(os.environ, {"NUAA_AUDIO_FEEDBACK": "1"}, clear=True):
            config = AccessibilityConfig()

            assert config.audio_feedback is True


class TestAccessibilityFunctions:
    """Tests for accessibility helper functions."""

    def test_get_config_returns_global_config(self):
        """Test that get_config returns the global configuration."""
        config = get_config()
        assert isinstance(config, AccessibilityConfig)

    def test_is_screen_reader_active_default_false(self):
        """Test that screen reader detection returns False by default."""
        with patch.dict(os.environ, {}, clear=True):
            # Reset the global config
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            assert is_screen_reader_active() is False

    def test_is_screen_reader_active_with_nvda(self):
        """Test screen reader detection with NVDA."""
        with patch.dict(os.environ, {"NVDA": "1"}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            assert is_screen_reader_active() is True

    def test_get_output_mode_default(self):
        """Test getting default output mode."""
        with patch.dict(os.environ, {}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            assert get_output_mode() == OutputMode.STANDARD

    def test_set_output_mode_changes_mode(self):
        """Test setting output mode."""
        with patch.dict(os.environ, {}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            set_output_mode(OutputMode.HIGH_CONTRAST)
            assert get_output_mode() == OutputMode.HIGH_CONTRAST

            set_output_mode(OutputMode.DYSLEXIA_FRIENDLY)
            assert get_output_mode() == OutputMode.DYSLEXIA_FRIENDLY


class TestFormatForAccessibility:
    """Tests for format_for_accessibility function."""

    def test_format_info_standard_mode(self):
        """Test formatting info message in standard mode."""
        with patch.dict(os.environ, {}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            result = format_for_accessibility("Test message", level="info")
            assert "ℹ" in result or "INFO" in result
            assert "Test message" in result

    def test_format_success_standard_mode(self):
        """Test formatting success message in standard mode."""
        with patch.dict(os.environ, {}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            result = format_for_accessibility("Success!", level="success")
            assert "✓" in result or "SUCCESS" in result
            assert "Success!" in result

    def test_format_error_standard_mode(self):
        """Test formatting error message in standard mode."""
        with patch.dict(os.environ, {}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            result = format_for_accessibility("Error occurred", level="error")
            assert "✗" in result or "ERROR" in result
            assert "Error occurred" in result

    def test_format_warning_standard_mode(self):
        """Test formatting warning message in standard mode."""
        with patch.dict(os.environ, {}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            result = format_for_accessibility("Warning!", level="warning")
            assert "⚠" in result or "WARNING" in result
            assert "Warning!" in result

    def test_format_screen_reader_mode(self):
        """Test formatting for screen reader mode."""
        with patch.dict(os.environ, {"NVDA": "1"}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            result = format_for_accessibility("Test", level="success")
            assert "Success:" in result
            assert "Test" in result

    def test_format_no_color_mode(self):
        """Test formatting for no-color mode."""
        with patch.dict(os.environ, {"NO_COLOR": "1"}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            result = format_for_accessibility("Test", level="error")
            assert "[ERROR]" in result
            assert "Test" in result

    def test_format_high_contrast_mode(self):
        """Test formatting for high contrast mode."""
        with patch.dict(os.environ, {"NUAA_HIGH_CONTRAST": "1"}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            result = format_for_accessibility("Test", level="success")
            # Should have doubled symbols for high contrast
            assert "✓✓" in result or "SUCCESS" in result
            assert "Test" in result

    def test_format_dyslexia_friendly_mode(self):
        """Test formatting for dyslexia-friendly mode."""
        with patch.dict(os.environ, {"NUAA_DYSLEXIA_FRIENDLY": "1"}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            result = format_for_accessibility("Test message", level="info")
            # Should have extra spacing
            assert "Test  message" in result

    def test_format_without_symbols(self):
        """Test formatting without symbols."""
        with patch.dict(os.environ, {}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            result = format_for_accessibility("Test", level="info", include_symbols=False)
            assert result == "Test"


class TestAnnounceForScreenReader:
    """Tests for announce_for_screen_reader function."""

    def test_announce_when_screen_reader_active(self, capsys):
        """Test announcement when screen reader is active."""
        with patch.dict(os.environ, {"NVDA": "1"}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            announce_for_screen_reader("Test message", importance="polite")

            captured = capsys.readouterr()
            assert "Test message" in captured.out

    def test_announce_assertive_importance(self, capsys):
        """Test announcement with assertive importance."""
        with patch.dict(os.environ, {"NVDA": "1"}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            announce_for_screen_reader("Important!", importance="assertive")

            captured = capsys.readouterr()
            assert "Important!" in captured.out
            assert ">>>" in captured.out

    def test_announce_when_screen_reader_inactive(self, capsys):
        """Test announcement when screen reader is not active."""
        with patch.dict(os.environ, {}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            announce_for_screen_reader("Test message")

            captured = capsys.readouterr()
            # Should not print when screen reader is not active
            assert captured.out == ""


class TestGetNavigationHints:
    """Tests for get_navigation_hints function."""

    def test_navigation_hints_standard_mode(self):
        """Test navigation hints in standard mode."""
        with patch.dict(os.environ, {}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            hints = get_navigation_hints()

            assert isinstance(hints, dict)
            assert "select" in hints
            assert "cancel" in hints
            assert "↑↓" in hints["select"] or "Navigate" in hints["select"]

    def test_navigation_hints_screen_reader_mode(self):
        """Test navigation hints for screen reader users."""
        with patch.dict(os.environ, {"NVDA": "1"}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            hints = get_navigation_hints()

            assert isinstance(hints, dict)
            assert "select" in hints
            # Screen reader mode should have verbose hints
            assert "ENTER" in hints["select"] or "arrow keys" in hints["select"]

    def test_navigation_hints_all_keys_present(self):
        """Test that all expected hint keys are present."""
        with patch.dict(os.environ, {}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            hints = get_navigation_hints()

            expected_keys = ["select", "cancel", "back", "help", "menu"]
            for key in expected_keys:
                assert key in hints


class TestFormatProgress:
    """Tests for format_progress function."""

    def test_format_progress_standard_mode(self):
        """Test progress formatting in standard mode."""
        with patch.dict(os.environ, {}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            result = format_progress(3, 10, "Processing files")

            assert "Processing files" in result
            # Should have visual progress bar
            assert "█" in result or "%" in result

    def test_format_progress_screen_reader_mode(self):
        """Test progress formatting for screen readers."""
        with patch.dict(os.environ, {"NVDA": "1"}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            result = format_progress(3, 10, "Processing files")

            assert "Step 3 of 10" in result
            assert "Processing files" in result

    def test_format_progress_simple_mode(self):
        """Test progress formatting in simple mode."""
        with patch.dict(os.environ, {"NUAA_SIMPLE_MODE": "1"}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            result = format_progress(5, 20, "Loading")

            assert "[5/20]" in result
            assert "Loading" in result

    def test_format_progress_percentage(self):
        """Test progress percentage calculation."""
        with patch.dict(os.environ, {}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            result = format_progress(5, 10, "Test")

            # 50% complete
            assert "50%" in result


class TestGetLineLength:
    """Tests for get_line_length function."""

    def test_line_length_standard_mode(self):
        """Test line length in standard mode."""
        with patch.dict(os.environ, {}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            length = get_line_length()
            assert length == 100

    def test_line_length_dyslexia_friendly_mode(self):
        """Test line length in dyslexia-friendly mode (shorter)."""
        with patch.dict(os.environ, {"NUAA_DYSLEXIA_FRIENDLY": "1"}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            length = get_line_length()
            assert length == 60

    def test_line_length_simple_mode(self):
        """Test line length in simple mode."""
        with patch.dict(os.environ, {"NUAA_SIMPLE_MODE": "1"}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            length = get_line_length()
            assert length == 70


class TestShouldUseEmoji:
    """Tests for should_use_emoji function."""

    def test_should_use_emoji_standard_mode(self):
        """Test emoji usage in standard mode."""
        with patch.dict(os.environ, {}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            assert should_use_emoji() is True

    def test_should_not_use_emoji_screen_reader_mode(self):
        """Test emoji disabled for screen readers."""
        with patch.dict(os.environ, {"NVDA": "1"}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            assert should_use_emoji() is False

    def test_should_not_use_emoji_no_color_mode(self):
        """Test emoji disabled in no-color mode."""
        with patch.dict(os.environ, {"NO_COLOR": "1"}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            assert should_use_emoji() is False

    def test_should_not_use_emoji_simple_mode(self):
        """Test emoji disabled in simple mode."""
        with patch.dict(os.environ, {"NUAA_SIMPLE_MODE": "1"}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            assert should_use_emoji() is False

    def test_should_use_emoji_high_contrast_mode(self):
        """Test emoji allowed in high contrast mode."""
        with patch.dict(os.environ, {"NUAA_HIGH_CONTRAST": "1"}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            # High contrast still allows emoji
            assert should_use_emoji() is True

    def test_should_use_emoji_dyslexia_friendly_mode(self):
        """Test emoji allowed in dyslexia-friendly mode."""
        with patch.dict(os.environ, {"NUAA_DYSLEXIA_FRIENDLY": "1"}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            # Dyslexia-friendly still allows emoji
            assert should_use_emoji() is True


class TestAccessibilityIntegration:
    """Integration tests for accessibility features."""

    def test_multiple_accessibility_preferences(self):
        """Test behavior with multiple accessibility preferences set."""
        # Screen reader takes precedence
        with patch.dict(
            os.environ,
            {"NVDA": "1", "NUAA_HIGH_CONTRAST": "1", "NUAA_SIMPLE_MODE": "1"},
            clear=True,
        ):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            # Screen reader mode should win
            assert get_output_mode() == OutputMode.SCREEN_READER
            assert accessibility._config.simple_mode is True

    def test_complete_accessibility_workflow(self):
        """Test complete workflow with accessibility features."""
        with patch.dict(os.environ, {"NUAA_HIGH_CONTRAST": "1"}, clear=True):
            from nuaa_cli import accessibility

            accessibility._config = AccessibilityConfig()

            # Format different message types
            info_msg = format_for_accessibility("Information", level="info")
            success_msg = format_for_accessibility("Done!", level="success")
            error_msg = format_for_accessibility("Failed", level="error")

            # All should be formatted
            assert "Information" in info_msg
            assert "Done!" in success_msg
            assert "Failed" in error_msg

            # Get navigation hints
            hints = get_navigation_hints()
            assert len(hints) > 0

            # Format progress
            progress = format_progress(1, 5, "Step 1")
            assert "Step 1" in progress

            # Check line length
            line_length = get_line_length()
            assert line_length > 0

            # Check emoji usage
            use_emoji = should_use_emoji()
            assert isinstance(use_emoji, bool)
