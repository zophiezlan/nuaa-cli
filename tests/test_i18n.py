"""
Tests for internationalization (i18n) module.

This module tests multi-language support, locale detection, translation loading,
and locale-aware formatting for dates, numbers, and currencies.
"""

import os
import locale as system_locale
import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from pathlib import Path

from nuaa_cli.i18n import (
    SUPPORTED_LANGUAGES,
    DEFAULT_LANGUAGE,
    get_locale_dir,
    initialize,
    detect_system_language,
    _,
    get_current_locale,
    get_available_languages,
    set_language,
    format_date,
    format_currency,
    format_number,
)


class TestSupportedLanguages:
    """Tests for supported languages configuration."""

    def test_supported_languages_defined(self):
        """Test that supported languages are properly defined."""
        assert isinstance(SUPPORTED_LANGUAGES, dict)
        assert len(SUPPORTED_LANGUAGES) > 0

    def test_default_language_is_supported(self):
        """Test that default language is in supported languages."""
        assert DEFAULT_LANGUAGE in SUPPORTED_LANGUAGES

    def test_all_expected_languages_present(self):
        """Test that all expected languages are supported."""
        expected_languages = ["en_AU", "vi_VN", "th_TH", "ar", "zh_CN", "es"]

        for lang in expected_languages:
            assert lang in SUPPORTED_LANGUAGES

    def test_language_codes_have_descriptions(self):
        """Test that all language codes have descriptive names."""
        for code, description in SUPPORTED_LANGUAGES.items():
            assert isinstance(code, str)
            assert isinstance(description, str)
            assert len(description) > 0

    def test_english_australian_is_default(self):
        """Test that English (Australia) is the default language."""
        assert DEFAULT_LANGUAGE == "en_AU"


class TestGetLocaleDir:
    """Tests for get_locale_dir function."""

    def test_get_locale_dir_returns_path(self):
        """Test that get_locale_dir returns a Path object."""
        locale_dir = get_locale_dir()
        assert isinstance(locale_dir, Path)

    def test_locale_dir_path_structure(self):
        """Test that locale dir path has expected structure."""
        locale_dir = get_locale_dir()
        # Should end with 'locales'
        assert locale_dir.name == "locales"


class TestDetectSystemLanguage:
    """Tests for detect_system_language function."""

    def test_detect_language_from_lang_env(self):
        """Test language detection from LANG environment variable."""
        with patch.dict(os.environ, {"LANG": "en_AU.UTF-8"}, clear=True):
            detected = detect_system_language()
            assert detected == "en_AU"

    def test_detect_language_from_language_env(self):
        """Test language detection from LANGUAGE environment variable."""
        with patch.dict(os.environ, {"LANGUAGE": "vi_VN"}, clear=True):
            detected = detect_system_language()
            assert detected == "vi_VN"

    def test_detect_language_from_lc_all(self):
        """Test language detection from LC_ALL environment variable."""
        with patch.dict(os.environ, {"LC_ALL": "zh_CN.UTF-8"}, clear=True):
            detected = detect_system_language()
            assert detected == "zh_CN"

    def test_detect_language_from_lc_messages(self):
        """Test language detection from LC_MESSAGES environment variable."""
        with patch.dict(os.environ, {"LC_MESSAGES": "es.UTF-8"}, clear=True):
            detected = detect_system_language()
            assert detected == "es"

    def test_detect_language_strips_encoding(self):
        """Test that language code is extracted from locale string."""
        with patch.dict(os.environ, {"LANG": "th_TH.UTF-8"}, clear=True):
            detected = detect_system_language()
            assert detected == "th_TH"

    def test_detect_language_fallback_to_default(self):
        """Test fallback to default language when no env vars set."""
        with patch.dict(os.environ, {}, clear=True):
            detected = detect_system_language()
            assert detected == DEFAULT_LANGUAGE

    def test_detect_language_unsupported_falls_back(self):
        """Test that unsupported language falls back to default."""
        with patch.dict(os.environ, {"LANG": "de_DE.UTF-8"}, clear=True):
            detected = detect_system_language()
            # German not supported, should fall back to default
            assert detected == DEFAULT_LANGUAGE

    def test_detect_language_prefix_matching(self):
        """Test language prefix matching for variants."""
        with patch.dict(os.environ, {"LANG": "en_US.UTF-8"}, clear=True):
            detected = detect_system_language()
            # Should match en_AU since we don't have en_US
            assert detected.startswith("en") or detected == DEFAULT_LANGUAGE

    def test_detect_arabic_language(self):
        """Test detection of Arabic language."""
        with patch.dict(os.environ, {"LANG": "ar.UTF-8"}, clear=True):
            detected = detect_system_language()
            assert detected == "ar"

    def test_detect_vietnamese_language(self):
        """Test detection of Vietnamese language."""
        with patch.dict(os.environ, {"LANG": "vi_VN.UTF-8"}, clear=True):
            detected = detect_system_language()
            assert detected == "vi_VN"


class TestInitialize:
    """Tests for initialize function."""

    def test_initialize_with_specific_language(self):
        """Test initialization with a specific language."""
        initialize(language="es")

        current = get_current_locale()
        assert current == "es"

    def test_initialize_with_unsupported_language_falls_back(self):
        """Test initialization with unsupported language falls back to default."""
        initialize(language="de_DE")

        current = get_current_locale()
        assert current == DEFAULT_LANGUAGE

    def test_initialize_without_language_autodetects(self):
        """Test initialization without language parameter autodetects."""
        with patch.dict(os.environ, {"LANG": "vi_VN.UTF-8"}, clear=True):
            initialize()

            current = get_current_locale()
            assert current == "vi_VN"

    def test_initialize_sets_current_locale(self):
        """Test that initialize sets the current locale."""
        initialize(language="zh_CN")

        assert get_current_locale() == "zh_CN"

    def test_initialize_handles_missing_translation_files(self):
        """Test that initialize handles missing translation files gracefully."""
        # Should not raise an exception even if translation files don't exist
        try:
            initialize(language="th_TH")
            # Should succeed (with fallback to identity translation)
            assert True
        except FileNotFoundError:
            pytest.fail("initialize should handle missing translation files")


class TestTranslationFunction:
    """Tests for the _ (translation) function."""

    def test_translation_function_returns_string(self):
        """Test that translation function returns a string."""
        result = _("Hello, world!")
        assert isinstance(result, str)

    def test_translation_function_with_english_text(self):
        """Test translation function with English text."""
        initialize(language="en_AU")
        result = _("Test message")
        # Should return the message (even if no translation file)
        assert "Test" in result or result == "Test message"

    def test_translation_function_auto_initializes(self):
        """Test that translation function auto-initializes if needed."""
        # Reset the module's _translate variable
        from nuaa_cli import i18n
        i18n._translate = None

        result = _("Test")
        # Should not raise an error, should auto-initialize
        assert isinstance(result, str)

    def test_translation_function_with_different_languages(self):
        """Test translation function across different languages."""
        languages = ["en_AU", "es", "vi_VN", "zh_CN", "ar", "th_TH"]

        for lang in languages:
            initialize(language=lang)
            result = _("Welcome")
            assert isinstance(result, str)
            assert len(result) > 0


class TestGetCurrentLocale:
    """Tests for get_current_locale function."""

    def test_get_current_locale_after_initialization(self):
        """Test getting current locale after initialization."""
        initialize(language="es")
        locale = get_current_locale()
        assert locale == "es"

    def test_get_current_locale_auto_initializes(self):
        """Test that get_current_locale auto-initializes if needed."""
        from nuaa_cli import i18n
        i18n._current_locale = None

        locale = get_current_locale()
        assert locale is not None
        assert locale in SUPPORTED_LANGUAGES

    def test_get_current_locale_returns_string(self):
        """Test that get_current_locale returns a string."""
        locale = get_current_locale()
        assert isinstance(locale, str)


class TestGetAvailableLanguages:
    """Tests for get_available_languages function."""

    def test_get_available_languages_returns_dict(self):
        """Test that get_available_languages returns a dictionary."""
        languages = get_available_languages()
        assert isinstance(languages, dict)

    def test_get_available_languages_matches_supported(self):
        """Test that available languages match SUPPORTED_LANGUAGES."""
        languages = get_available_languages()
        assert languages == SUPPORTED_LANGUAGES

    def test_get_available_languages_returns_copy(self):
        """Test that get_available_languages returns a copy (not reference)."""
        languages1 = get_available_languages()
        languages2 = get_available_languages()

        # Should be equal but not the same object
        assert languages1 == languages2
        assert languages1 is not languages2


class TestSetLanguage:
    """Tests for set_language function."""

    def test_set_language_with_valid_language(self):
        """Test setting a valid language."""
        result = set_language("vi_VN")
        assert result is True
        assert get_current_locale() == "vi_VN"

    def test_set_language_with_invalid_language(self):
        """Test setting an invalid language."""
        result = set_language("invalid_LANG")
        assert result is False
        # Locale should not change

    def test_set_language_with_all_supported_languages(self):
        """Test setting each supported language."""
        for lang_code in SUPPORTED_LANGUAGES.keys():
            result = set_language(lang_code)
            assert result is True
            assert get_current_locale() == lang_code

    def test_set_language_returns_boolean(self):
        """Test that set_language returns a boolean."""
        result = set_language("en_AU")
        assert isinstance(result, bool)


class TestFormatDate:
    """Tests for format_date function."""

    def test_format_date_default_format(self):
        """Test date formatting with default format string."""
        test_date = datetime(2025, 11, 18, 10, 30, 0)
        result = format_date(test_date)

        assert "2025" in result
        assert "11" in result
        assert "18" in result

    def test_format_date_custom_format(self):
        """Test date formatting with custom format string."""
        test_date = datetime(2025, 11, 18, 10, 30, 0)
        result = format_date(test_date, format_string="%d/%m/%Y")

        assert "18/11/2025" == result

    def test_format_date_with_time(self):
        """Test date formatting including time."""
        test_date = datetime(2025, 11, 18, 14, 30, 45)
        result = format_date(test_date, format_string="%Y-%m-%d %H:%M:%S")

        assert "2025-11-18 14:30:45" == result

    def test_format_date_year_only(self):
        """Test formatting just the year."""
        test_date = datetime(2025, 11, 18)
        result = format_date(test_date, format_string="%Y")

        assert result == "2025"


class TestFormatCurrency:
    """Tests for format_currency function."""

    def test_format_currency_default(self):
        """Test currency formatting with default currency (AUD)."""
        result = format_currency(100.50)

        # Should contain the amount
        assert "100" in result
        # Should have currency symbol or formatting
        assert "$" in result or "100.50" in result

    def test_format_currency_with_custom_currency(self):
        """Test currency formatting with custom currency."""
        result = format_currency(1000.00, currency="USD")

        # Should format the amount
        assert "1000" in result or "1,000" in result

    def test_format_currency_handles_locale_errors(self):
        """Test that currency formatting handles locale errors gracefully."""
        # Even with locale errors, should return something reasonable
        result = format_currency(50.75)

        assert isinstance(result, str)
        assert "50" in result

    def test_format_currency_large_amount(self):
        """Test formatting large currency amounts."""
        result = format_currency(1000000.99)

        # Should handle large amounts
        assert "1000000" in result or "1,000,000" in result

    def test_format_currency_zero(self):
        """Test formatting zero currency."""
        result = format_currency(0.00)

        assert "0" in result


class TestFormatNumber:
    """Tests for format_number function."""

    def test_format_number_default_decimal_places(self):
        """Test number formatting with default 2 decimal places."""
        result = format_number(1234.5678)

        assert "1234.57" in result or "1,234.57" in result

    def test_format_number_custom_decimal_places(self):
        """Test number formatting with custom decimal places."""
        result = format_number(100.123456, decimal_places=3)

        assert "100.123" in result

    def test_format_number_zero_decimal_places(self):
        """Test number formatting with zero decimal places."""
        result = format_number(1234.99, decimal_places=0)

        assert "1235" in result

    def test_format_number_handles_locale_errors(self):
        """Test that number formatting handles locale errors gracefully."""
        result = format_number(999.99)

        assert isinstance(result, str)
        assert "999.99" in result

    def test_format_number_negative_value(self):
        """Test formatting negative numbers."""
        result = format_number(-500.50)

        assert "-500.50" in result or "-500.5" in result

    def test_format_number_large_value(self):
        """Test formatting large numbers with grouping."""
        result = format_number(1000000.00)

        # Should have some form of grouping or be formatted
        assert "1000000" in result or "1,000,000" in result


class TestI18nIntegration:
    """Integration tests for i18n functionality."""

    def test_complete_workflow_english(self):
        """Test complete workflow in English."""
        # Initialize with English
        initialize(language="en_AU")

        # Check current locale
        assert get_current_locale() == "en_AU"

        # Translate a message
        msg = _("Hello")
        assert isinstance(msg, str)

        # Format date
        date_str = format_date(datetime(2025, 1, 1))
        assert "2025" in date_str

        # Format currency
        currency_str = format_currency(100.0)
        assert "100" in currency_str

        # Format number
        number_str = format_number(1234.56)
        assert "1234" in number_str

    def test_complete_workflow_spanish(self):
        """Test complete workflow in Spanish."""
        initialize(language="es")

        assert get_current_locale() == "es"

        msg = _("Welcome")
        assert isinstance(msg, str)

        date_str = format_date(datetime(2025, 6, 15))
        assert "2025" in date_str

    def test_complete_workflow_vietnamese(self):
        """Test complete workflow in Vietnamese."""
        initialize(language="vi_VN")

        assert get_current_locale() == "vi_VN"

        msg = _("Thank you")
        assert isinstance(msg, str)

    def test_complete_workflow_chinese(self):
        """Test complete workflow in Simplified Chinese."""
        initialize(language="zh_CN")

        assert get_current_locale() == "zh_CN"

        msg = _("Goodbye")
        assert isinstance(msg, str)

    def test_language_switching(self):
        """Test switching between languages."""
        # Start with English
        set_language("en_AU")
        assert get_current_locale() == "en_AU"

        # Switch to Spanish
        set_language("es")
        assert get_current_locale() == "es"

        # Switch to Vietnamese
        set_language("vi_VN")
        assert get_current_locale() == "vi_VN"

        # Switch back to English
        set_language("en_AU")
        assert get_current_locale() == "en_AU"

    def test_all_supported_languages_work(self):
        """Test that all supported languages can be initialized."""
        for lang_code in SUPPORTED_LANGUAGES.keys():
            # Initialize the language
            initialize(language=lang_code)

            # Should succeed
            assert get_current_locale() == lang_code

            # Translation should work (even if it returns original text)
            msg = _("Test")
            assert isinstance(msg, str)

            # Formatting functions should work
            date_str = format_date(datetime(2025, 1, 1))
            assert isinstance(date_str, str)

            currency_str = format_currency(100.0)
            assert isinstance(currency_str, str)

            number_str = format_number(123.45)
            assert isinstance(number_str, str)

    def test_environment_variable_detection_workflow(self):
        """Test complete workflow with environment variable detection."""
        with patch.dict(os.environ, {"LANG": "ar.UTF-8"}, clear=True):
            # Auto-detect from environment
            initialize()

            # Should have detected Arabic
            locale = get_current_locale()
            assert locale == "ar"

            # Translation should work
            msg = _("Hello")
            assert isinstance(msg, str)

    def test_fallback_behavior(self):
        """Test fallback behavior with unsupported language."""
        # Try to set unsupported language
        result = set_language("unsupported")
        assert result is False

        # Should still have a valid locale (previous one)
        locale = get_current_locale()
        assert locale in SUPPORTED_LANGUAGES

        # Translation should still work
        msg = _("Test")
        assert isinstance(msg, str)
