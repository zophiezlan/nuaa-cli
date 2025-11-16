"""Additional tests for scaffold module."""

from nuaa_cli.scaffold import (
    _apply_replacements,
    _prepend_metadata,
    _stamp,
)


class TestApplyReplacements:
    """Tests for _apply_replacements function."""

    def test_bracket_placeholder_replacement(self):
        """Test replacing [Name] bracket placeholder."""
        text = "Program: [Name]"
        mapping = {"PROGRAM_NAME": "Test Program"}
        result = _apply_replacements(text, mapping)
        assert result == "Program: Test Program"

    def test_multiple_bracket_replacements(self):
        """Test replacing multiple bracket placeholders."""
        text = "[Name] - [Description] for [Timeframe]"
        mapping = {"PROGRAM_NAME": "Test", "TARGET_POPULATION": "Clients", "DURATION": "12 months"}
        result = _apply_replacements(text, mapping)
        assert "Test" in result
        assert "Clients" in result
        assert "12 months" in result

    def test_no_replacements(self):
        """Test with no placeholders to replace."""
        text = "This is plain text"
        mapping = {"PROGRAM_NAME": "Test"}
        result = _apply_replacements(text, mapping)
        assert result == "This is plain text"

    def test_empty_mapping(self):
        """Test with empty replacement mapping."""
        text = "Program: [Name]"
        mapping = {}
        result = _apply_replacements(text, mapping)
        # Should replace with empty string when key not found
        assert result == "Program: "

    def test_date_placeholder(self):
        """Test [Date] placeholder gets current date."""
        text = "Date: [Date]"
        mapping = {}
        result = _apply_replacements(text, mapping)
        # Should have a date in YYYY-MM-DD format
        assert "Date:" in result
        assert result != "Date: [Date]"


class TestPrependMetadata:
    """Tests for _prepend_metadata function."""

    def test_single_metadata_field(self):
        """Test prepending single metadata field."""
        text = "# Title\n\nContent"
        metadata = {"status": "draft"}
        result = _prepend_metadata(text, metadata)
        assert "status: draft" in result
        assert "# Title" in result

    def test_multiple_metadata_fields(self):
        """Test prepending multiple metadata fields."""
        text = "Content"
        metadata = {"status": "draft", "author": "Test", "date": "2025-11-17"}
        result = _prepend_metadata(text, metadata)
        assert "status: draft" in result
        assert "author: Test" in result
        assert "date: 2025-11-17" in result

    def test_empty_metadata(self):
        """Test with empty metadata dictionary."""
        text = "Content"
        metadata = {}
        result = _prepend_metadata(text, metadata)
        # Should return text with empty metadata block
        assert "---" in result

    def test_metadata_format(self):
        """Test that metadata is in YAML front matter format."""
        text = "Content"
        metadata = {"key": "value"}
        result = _prepend_metadata(text, metadata)
        # Should have YAML delimiters
        assert result.startswith("---\n")
        assert "\n---\n" in result


class TestStamp:
    """Tests for _stamp function."""

    def test_returns_timestamp_string(self):
        """Test that _stamp returns a timestamp string."""
        result = _stamp()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_timestamp_format(self):
        """Test timestamp has expected format."""
        result = _stamp()
        # Should be in ISO format: YYYY-MM-DD
        assert "-" in result
        parts = result.split("-")
        assert len(parts) >= 3

    def test_multiple_calls_same_day(self):
        """Test multiple calls on same day return similar timestamps."""
        stamp1 = _stamp()
        stamp2 = _stamp()
        # Should have same date part
        assert stamp1[:10] == stamp2[:10]
