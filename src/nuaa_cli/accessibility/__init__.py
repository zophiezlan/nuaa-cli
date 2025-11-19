"""
Accessibility module for NUAA CLI.

Provides accessibility features including screen reader support,
visual modes, and accessible output formatting.
"""

from enum import Enum
import os


class OutputMode(Enum):
    """Output modes for different accessibility needs."""

    STANDARD = "standard"
    SCREEN_READER = "screen_reader"
    HIGH_CONTRAST = "high_contrast"
    NO_COLOR = "no_color"
    DYSLEXIA_FRIENDLY = "dyslexia_friendly"
    SIMPLE = "simple"


class AccessibilityConfig:
    """Global accessibility configuration."""

    def __init__(self):
        self.output_mode: OutputMode = OutputMode.STANDARD
        self.audio_feedback: bool = False
        self.verbose_navigation: bool = False
        self.simple_mode: bool = False
        self.screen_reader_optimized: bool = False
        self._detect_preferences()

    def _detect_preferences(self):
        """Detect accessibility preferences from environment variables."""
        # Check for screen reader
        if os.environ.get("NVDA") or os.environ.get("JAWS") or os.environ.get("ORCA"):
            self.screen_reader_optimized = True
            self.output_mode = OutputMode.SCREEN_READER

        # Check for high contrast preference
        if os.environ.get("NUAA_HIGH_CONTRAST") == "1":
            self.output_mode = OutputMode.HIGH_CONTRAST

        # Check for no color preference (for color blindness)
        if os.environ.get("NO_COLOR") == "1" or os.environ.get("NUAA_NO_COLOR") == "1":
            self.output_mode = OutputMode.NO_COLOR

        # Check for dyslexia-friendly mode
        if os.environ.get("NUAA_DYSLEXIA_FRIENDLY") == "1":
            self.output_mode = OutputMode.DYSLEXIA_FRIENDLY

        # Check for simple mode (cognitive accessibility)
        if os.environ.get("NUAA_SIMPLE_MODE") == "1":
            self.simple_mode = True

        # Check for audio feedback
        if os.environ.get("NUAA_AUDIO_FEEDBACK") == "1":
            self.audio_feedback = True


# Global configuration instance
_config = AccessibilityConfig()


def get_config() -> AccessibilityConfig:
    """Get the global accessibility configuration."""
    return _config


def is_screen_reader_active() -> bool:
    """Check if a screen reader is detected."""
    return _config.screen_reader_optimized


def get_output_mode() -> OutputMode:
    """Get the current output mode."""
    return _config.output_mode


def set_output_mode(mode: OutputMode) -> None:
    """Set the output mode."""
    _config.output_mode = mode


def format_for_accessibility(text: str, level: str = "info", include_symbols: bool = True) -> str:
    """
    Format text for the current accessibility mode.

    Args:
        text: Text to format
        level: Message level ('info', 'success', 'warning', 'error')
        include_symbols: Whether to include visual symbols

    Returns:
        Formatted text appropriate for current accessibility mode
    """
    mode = get_output_mode()

    # Define symbols based on mode
    if mode == OutputMode.NO_COLOR or mode == OutputMode.SCREEN_READER:
        symbols = {
            "success": "[SUCCESS] ",
            "error": "[ERROR] ",
            "warning": "[WARNING] ",
            "info": "[INFO] ",
        }
    elif mode == OutputMode.HIGH_CONTRAST:
        symbols = {
            "success": "✓✓ SUCCESS: ",
            "error": "✗✗ ERROR: ",
            "warning": "⚠⚠ WARNING: ",
            "info": "ℹℹ INFO: ",
        }
    else:
        symbols = {
            "success": "✓ ",
            "error": "✗ ",
            "warning": "⚠ ",
            "info": "ℹ ",
        }

    if include_symbols and level in symbols:
        prefix = symbols[level]
    else:
        prefix = ""

    # Format based on mode
    if mode == OutputMode.DYSLEXIA_FRIENDLY:
        # Add extra spacing for dyslexia-friendly mode
        text = text.replace(" ", "  ")

    if mode == OutputMode.SCREEN_READER:
        # Screen reader mode: clear, verbose descriptions
        if level == "success":
            prefix = "Success: "
        elif level == "error":
            prefix = "Error occurred: "
        elif level == "warning":
            prefix = "Warning message: "
        elif level == "info":
            prefix = "Information: "

    return f"{prefix}{text}"


def announce_for_screen_reader(message: str, importance: str = "polite") -> None:
    """
    Announce a message for screen reader users.

    Args:
        message: Message to announce
        importance: 'polite' or 'assertive' (for important announcements)
    """
    if is_screen_reader_active():
        # In CLI context, we just ensure the message is properly formatted
        # Screen readers will read terminal output
        if importance == "assertive":
            print(f"\n>>> {message} <<<\n")
        else:
            print(f"{message}")


def get_navigation_hints() -> dict[str, str]:
    """
    Get navigation hints appropriate for current accessibility mode.

    Returns:
        Dictionary of navigation hints
    """
    if _config.verbose_navigation or is_screen_reader_active():
        return {
            "select": "Press ENTER to select, or use UP/DOWN arrow keys to navigate",
            "cancel": "Press ESC or Ctrl+C to cancel",
            "back": "Press BACKSPACE to go back",
            "help": "Press ? for help",
            "menu": "Use arrow keys to navigate menu, ENTER to select, ESC to cancel",
        }
    else:
        return {
            "select": "↑↓ Navigate, ENTER Select, ESC Cancel",
            "cancel": "ESC Cancel",
            "back": "← Back",
            "help": "? Help",
            "menu": "↑↓ Navigate, ENTER Select",
        }


def format_progress(current: int, total: int, description: str = "") -> str:
    """
    Format a progress indicator for accessibility.

    Args:
        current: Current step number
        total: Total number of steps
        description: Description of current step

    Returns:
        Formatted progress string
    """
    mode = get_output_mode()

    if mode == OutputMode.SCREEN_READER:
        return f"Step {current} of {total}: {description}"
    elif mode == OutputMode.SIMPLE:
        return f"[{current}/{total}] {description}"
    else:
        # Standard mode with visual progress bar
        percentage = int((current / total) * 100)
        bar_length = 20
        filled = int((current / total) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        return f"[{bar}] {percentage}% - {description}"


def get_line_length() -> int:
    """
    Get the appropriate line length for current accessibility mode.

    Returns:
        Maximum line length in characters
    """
    mode = get_output_mode()

    if mode == OutputMode.DYSLEXIA_FRIENDLY:
        return 60  # Shorter lines for dyslexia-friendly mode
    elif mode == OutputMode.SIMPLE:
        return 70
    else:
        return 100  # Standard line length


def should_use_emoji() -> bool:
    """
    Determine if emoji should be used in output.

    Returns:
        True if emoji should be used, False otherwise
    """
    mode = get_output_mode()
    return mode not in (OutputMode.SCREEN_READER, OutputMode.NO_COLOR, OutputMode.SIMPLE)
