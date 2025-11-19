"""
Internationalization (i18n) module for NUAA CLI.

Provides multi-language support with fallback to English.
Supports locale-aware formatting for dates, numbers, and currencies.
"""

import gettext
import locale
import os
from pathlib import Path
from typing import Optional

# Supported languages with their locale codes
SUPPORTED_LANGUAGES = {
    "en_AU": "English (Australia)",
    "vi_VN": "Tiếng Việt (Vietnamese)",
    "th_TH": "ไทย (Thai)",
    "ar": "العربية (Arabic)",
    "zh_CN": "简体中文 (Simplified Chinese)",
    "es": "Español (Spanish)",
}

# Default language
DEFAULT_LANGUAGE = "en_AU"

# Global translation function
_translate = None
_current_locale = None


def get_locale_dir() -> Path:
    """Get the directory containing locale files."""
    return Path(__file__).parent.parent.parent.parent / "locales"


def initialize(language: Optional[str] = None) -> None:
    """
    Initialize the translation system.

    Args:
        language: Language code (e.g., 'en_AU', 'vi_VN'). If None, auto-detect from system.
    """
    global _translate, _current_locale

    # Determine language
    if language is None:
        language = detect_system_language()

    # Validate language
    if language not in SUPPORTED_LANGUAGES:
        language = DEFAULT_LANGUAGE

    _current_locale = language

    # Set up gettext
    locale_dir = get_locale_dir()

    try:
        translation = gettext.translation("nuaa_cli", localedir=str(locale_dir), languages=[language, "en_AU"])
        _translate = translation.gettext
    except FileNotFoundError:
        # Fallback to default (no translation)
        def _translate(s):
            return s

    # Set system locale for date/number formatting (best effort)
    try:
        locale.setlocale(locale.LC_ALL, f"{language}.UTF-8")
    except locale.Error:
        # Fallback to default locale
        pass


def detect_system_language() -> str:
    """
    Detect the system language from environment variables.

    Returns:
        Language code (e.g., 'en_AU', 'vi_VN')
    """
    # Try environment variables
    for env_var in ("LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG"):
        lang = os.environ.get(env_var)
        if lang:
            # Extract language code (e.g., 'en_AU' from 'en_AU.UTF-8')
            lang_code = lang.split(".")[0]

            # Check if supported
            if lang_code in SUPPORTED_LANGUAGES:
                return lang_code

            # Try just the language part (e.g., 'en' from 'en_US')
            lang_prefix = lang_code.split("_")[0]
            for supported_lang in SUPPORTED_LANGUAGES:
                if supported_lang.startswith(lang_prefix):
                    return supported_lang

    return DEFAULT_LANGUAGE


def _(message: str) -> str:
    """
    Translate a message to the current language.

    This is the main translation function. Use it like:
        from nuaa_cli.i18n import _
        print(_("Hello, world!"))

    Args:
        message: The message to translate (in English)

    Returns:
        Translated message
    """
    if _translate is None:
        initialize()

    return _translate(message)


def get_current_locale() -> str:
    """Get the current locale code."""
    if _current_locale is None:
        initialize()
    return _current_locale


def get_available_languages() -> dict[str, str]:
    """
    Get all available languages.

    Returns:
        Dictionary mapping language codes to language names
    """
    return SUPPORTED_LANGUAGES.copy()


def set_language(language: str) -> bool:
    """
    Set the active language.

    Args:
        language: Language code (e.g., 'en_AU', 'vi_VN')

    Returns:
        True if language was set successfully, False otherwise
    """
    if language not in SUPPORTED_LANGUAGES:
        return False

    initialize(language)
    return True


# Format helpers for locale-aware output
def format_date(date_obj, format_string: str = "%Y-%m-%d") -> str:
    """
    Format a date according to the current locale.

    Args:
        date_obj: datetime object
        format_string: strftime format string

    Returns:
        Formatted date string
    """
    return date_obj.strftime(format_string)


def format_currency(amount: float, currency: str = "AUD") -> str:
    """
    Format a currency amount according to the current locale.

    Args:
        amount: Amount to format
        currency: Currency code (default: AUD for Australian dollars)

    Returns:
        Formatted currency string
    """
    get_current_locale()

    # Simple formatting with locale awareness
    try:
        formatted = locale.currency(amount, symbol=True, grouping=True)
        return formatted
    except (ValueError, locale.Error):
        # Fallback to simple formatting
        return f"${amount:,.2f}"


def format_number(number: float, decimal_places: int = 2) -> str:
    """
    Format a number according to the current locale.

    Args:
        number: Number to format
        decimal_places: Number of decimal places

    Returns:
        Formatted number string
    """
    try:
        return locale.format_string(f"%.{decimal_places}f", number, grouping=True)
    except (ValueError, locale.Error):
        # Fallback
        return f"{number:,.{decimal_places}f}"
