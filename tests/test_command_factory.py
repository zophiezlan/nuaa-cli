"""Tests for command factory pattern."""

import os

import pytest
from typer.testing import CliRunner

from nuaa_cli import app
from nuaa_cli.command_factory import (
    FieldConfig,
    TemplateCommandConfig,
    TemplateCommandHandler,
)


runner = CliRunner()


class TestFieldConfig:
    """Tests for FieldConfig dataclass."""

    def test_field_config_initialization(self):
        """Test FieldConfig initialization with all parameters."""
        field = FieldConfig(
            name="funder",
            help_text="Funder name",
            max_length=200,
            is_required=True,
            default=None,
        )

        assert field.name == "funder"
        assert field.help_text == "Funder name"
        assert field.max_length == 200
        assert field.is_required is True
        assert field.default is None

    def test_field_config_defaults(self):
        """Test FieldConfig default values."""
        field = FieldConfig(name="test_field", help_text="Test field")

        assert field.max_length == 500
        assert field.is_required is True
        assert field.default is None


class TestTemplateCommandConfig:
    """Tests for TemplateCommandConfig dataclass."""

    def test_config_initialization(self):
        """Test TemplateCommandConfig initialization."""
        config = TemplateCommandConfig(
            command_name="test",
            template_name="test.md",
            output_filename="test-output.md",
            help_text="Test command",
            fields=[FieldConfig("field1", "Field 1")],
        )

        assert config.command_name == "test"
        assert config.template_name == "test.md"
        assert config.output_filename == "test-output.md"
        assert config.help_text == "Test command"
        assert len(config.fields) == 1
        assert config.requires_program is True
        assert config.metadata_generator is None
        assert config.additional_outputs == []


class TestTemplateCommandHandler:
    """Tests for TemplateCommandHandler class."""

    def test_handler_initialization(self):
        """Test handler initializes with config."""
        config = TemplateCommandConfig(
            command_name="test",
            template_name="test.md",
            output_filename="test.md",
            help_text="Test",
            fields=[],
        )
        handler = TemplateCommandHandler(config)

        assert handler.config == config

    def test_build_field_mapping_basic(self, tmp_path):
        """Test basic field mapping construction."""
        from rich.console import Console

        config = TemplateCommandConfig(
            command_name="test",
            template_name="test.md",
            output_filename="test.md",
            help_text="Test",
            fields=[
                FieldConfig("field1", "Field 1", max_length=100),
                FieldConfig("field2", "Field 2", max_length=100),
            ],
        )
        handler = TemplateCommandHandler(config)
        console = Console()

        mapping = handler._build_field_mapping_from_args(
            program_name="Test Program",
            field_values=("value1", "value2"),
            console=console,
        )

        assert mapping["PROGRAM_NAME"] == "Test Program"
        assert mapping["FIELD1"] == "value1"
        assert mapping["FIELD2"] == "value2"
        assert "DATE" in mapping

    def test_build_field_mapping_mismatch(self, tmp_path):
        """Test field mapping with mismatched arguments."""
        from rich.console import Console
        import typer

        config = TemplateCommandConfig(
            command_name="test",
            template_name="test.md",
            output_filename="test.md",
            help_text="Test",
            fields=[
                FieldConfig("field1", "Field 1", max_length=100),
            ],
        )
        handler = TemplateCommandHandler(config)
        console = Console()

        # Should raise typer.Exit when field count doesn't match
        with pytest.raises(typer.Exit):
            handler._build_field_mapping_from_args(
                program_name="Test Program",
                field_values=("value1", "value2"),  # Too many values
                console=console,
            )


class TestProposeCommandRefactored:
    """Test the refactored propose command using factory pattern."""

    def test_propose_command_works(self, tmp_path):
        """Test propose command still works after refactoring."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Initialize nuaa-kit templates directory
            templates_dir = tmp_path / "nuaa-kit" / "templates"
            templates_dir.mkdir(parents=True, exist_ok=True)

            # Create minimal proposal template
            proposal_template = templates_dir / "proposal.md"
            proposal_template.write_text(
                "# Funding Proposal\n\n"
                "Program: {{PROGRAM_NAME}}\n"
                "Funder: {{FUNDER}}\n"
                "Amount: {{AMOUNT}}\n"
                "Duration: {{DURATION}}\n"
            )

            result = runner.invoke(
                app,
                ["propose", "Test Program", "Test Funder", "$50000", "12 months"],
            )

            # Command should succeed
            assert result.exit_code == 0

            # Check if proposal was created
            nuaa_dir = tmp_path / "nuaa"
            if nuaa_dir.exists():
                files = list(nuaa_dir.glob("*/proposal.md"))
                assert len(files) > 0, "Proposal file should be created"

                content = files[0].read_text()
                # Program name is sanitized to "Test-Program" by validate_program_name
                assert "Test-Program" in content or "Test Program" in content

        finally:
            os.chdir(old_cwd)


class TestMeasureCommandRefactored:
    """Test the refactored measure command using factory pattern."""

    def test_measure_command_works(self, tmp_path):
        """Test measure command still works after refactoring."""
        old_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)

            # Initialize nuaa-kit templates directory
            templates_dir = tmp_path / "nuaa-kit" / "templates"
            templates_dir.mkdir(parents=True, exist_ok=True)

            # Create minimal impact framework template
            framework_template = templates_dir / "impact-framework.md"
            framework_template.write_text(
                "# Impact Framework\n\n"
                "Program: {{PROGRAM_NAME}}\n"
                "Evaluation Period: {{EVALUATION_PERIOD}}\n"
                "Budget: {{BUDGET}}\n"
            )

            result = runner.invoke(
                app,
                ["measure", "Test Program", "6 months", "$7000"],
            )

            # Command should succeed
            assert result.exit_code == 0

            # Check if framework was created
            nuaa_dir = tmp_path / "nuaa"
            if nuaa_dir.exists():
                files = list(nuaa_dir.glob("*/impact-framework.md"))
                assert len(files) > 0, "Impact framework file should be created"

                content = files[0].read_text()
                # Program name is sanitized to "Test-Program" by validate_program_name
                assert "Test-Program" in content or "Test Program" in content

        finally:
            os.chdir(old_cwd)


class TestFactoryCodeReduction:
    """Tests demonstrating code reduction benefits."""

    def test_multiple_commands_use_same_factory(self):
        """Verify multiple commands can use the same factory infrastructure."""
        # This demonstrates that propose and measure both use TemplateCommandHandler
        from nuaa_cli.commands import propose, measure

        # Both modules should have CONFIG and _handler
        assert hasattr(propose, "CONFIG")
        assert hasattr(propose, "_handler")
        assert hasattr(measure, "CONFIG")
        assert hasattr(measure, "_handler")

        # Both handlers should be instances of TemplateCommandHandler
        assert isinstance(propose._handler, TemplateCommandHandler)
        assert isinstance(measure._handler, TemplateCommandHandler)

        # Configs should have the expected structure
        assert propose.CONFIG.command_name == "propose"
        assert measure.CONFIG.command_name == "measure"
        assert len(propose.CONFIG.fields) == 3  # funder, amount, duration
        assert len(measure.CONFIG.fields) == 2  # evaluation_period, budget
