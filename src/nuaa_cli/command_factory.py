"""
Command Factory for Template-Based Commands
============================================

This module provides a factory pattern for creating template-based CLI commands,
eliminating 90% of boilerplate code across command files.

The factory pattern standardizes:
- Input validation
- Template loading and processing
- Error handling and user feedback
- Metadata generation
- File writing with force flag support

Usage:
    from .command_factory import create_template_command, FieldConfig, TemplateCommandConfig

    config = TemplateCommandConfig(
        command_name="propose",
        template_name="proposal.md",
        output_filename="proposal.md",
        help_text="Create a funding proposal...",
        fields=[
            FieldConfig("funder", "Funder name", max_length=200),
            FieldConfig("amount", "Amount requested", max_length=50),
        ],
    )

    register = create_template_command(config)

Benefits:
    - Reduces command files from ~120 lines to ~25 lines
    - Single source of truth for error handling
    - Consistent behavior across all commands
    - Easier testing (test factory once, not 11 times)
    - Faster to add new commands

Author: NUAA Project
License: MIT
"""

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional

import typer
from rich.console import Console
from rich.panel import Panel

from .scaffold import (
    _apply_replacements,
    _ensure_nuaa_root,
    _load_template,
    _next_feature_dir,
    _prepend_metadata,
    _slugify,
    _stamp,
    write_markdown_if_needed,
)
from .utils import validate_program_name, validate_text_field


@dataclass
class FieldConfig:
    """
    Configuration for a command field parameter.

    Attributes:
        name: Internal name used for mapping variable (e.g., "funder")
        help_text: Help text shown in CLI (e.g., "Funder name or grant program")
        max_length: Maximum allowed length for validation (default: 500)
        is_required: Whether field is required (default: True)
        default: Default value if not provided (default: None)

    Example:
        >>> field = FieldConfig("funder", "Funder name", max_length=200)
        >>> field.name
        'funder'
    """

    name: str
    help_text: str
    max_length: int = 500
    is_required: bool = True
    default: Optional[str] = None


@dataclass
class TemplateCommandConfig:
    """
    Complete configuration for a template-based command.

    Attributes:
        command_name: CLI command name (e.g., "propose", "measure")
        template_name: Template filename (e.g., "proposal.md")
        output_filename: Output filename in feature directory (e.g., "proposal.md")
        help_text: Complete docstring for the command
        fields: List of field configurations for command parameters
        requires_program: Whether command requires program_name argument (default: True)
        metadata_generator: Optional function to generate custom metadata dict
        additional_outputs: Optional list of additional files to create
        create_changelog: Whether to create a CHANGELOG.md if it doesn't exist (default: False)
        primary_field_name: Name for the primary field in mapping (default: "PROGRAM_NAME")
            For commands like "event" that use EVENT_NAME instead of PROGRAM_NAME

    Example:
        >>> config = TemplateCommandConfig(
        ...     command_name="propose",
        ...     template_name="proposal.md",
        ...     output_filename="proposal.md",
        ...     help_text="Create a funding proposal",
        ...     fields=[FieldConfig("funder", "Funder name")],
        ... )
    """

    command_name: str
    template_name: str
    output_filename: str
    help_text: str
    fields: list[FieldConfig]
    requires_program: bool = True
    metadata_generator: Optional[Callable[[str, dict[str, str]], dict[str, Any]]] = None
    additional_outputs: list[tuple[str, str]] = field(default_factory=list)  # (template, output)
    create_changelog: bool = False
    primary_field_name: str = "PROGRAM_NAME"


class TemplateCommandHandler:
    """
    Handler class that processes template-based commands.

    This class encapsulates the common logic for template commands,
    allowing command files to be dramatically simplified while maintaining
    full Typer compatibility.

    Usage in command files:
        handler = TemplateCommandHandler(config)
        handler.execute(program_name, field1, field2, force=False,
                       show_banner_fn=fn, console=console)
    """

    def __init__(self, config: TemplateCommandConfig):
        """Initialize handler with configuration."""
        self.config = config

    def execute(
        self,
        program_name: str,
        *field_values: str,
        feature: Optional[str] = None,
        force: bool = False,
        show_banner_fn: Optional[Callable] = None,
        console: Optional[Console] = None,
    ) -> None:
        """
        Execute the template command with given parameters.

        Args:
            program_name: Program name
            *field_values: Variable length field values matching config.fields order
            feature: Optional custom feature slug (e.g., '001-custom-slug' or 'custom-slug')
            force: Whether to overwrite existing files
            show_banner_fn: Optional banner display function
            console: Optional Rich console

        Raises:
            typer.Exit: If validation or processing fails
        """
        console = console or Console()

        if show_banner_fn:
            show_banner_fn()

        # Validate program name
        validated_program = validate_program_name(program_name, console)

        # Build field mapping from positional arguments
        mapping = self._build_field_mapping_from_args(
            program_name=validated_program,
            field_values=field_values,
            console=console,
        )

        # Get or create feature directory with optional custom slug
        feature_dir, num_str, slug = self._get_feature_dir(validated_program, feature, console)

        # Add feature info to mapping
        mapping["FEATURE_ID"] = num_str
        mapping["SLUG"] = slug

        # Process main template
        _process_template(
            config=self.config,
            feature_dir=feature_dir,
            mapping=mapping,
            program_name=validated_program,
            num_str=num_str,
            slug=slug,
            force=force,
            console=console,
        )

        # Process additional outputs if configured
        for template_name, output_name in self.config.additional_outputs:
            try:
                template = _load_template(template_name)
                filled = _apply_replacements(template, mapping)
                meta = {
                    "title": f"{validated_program} - {output_name}",
                    "feature": f"{num_str}-{slug}",
                }
                text = _prepend_metadata(filled, meta)
                dest = feature_dir / output_name
                write_markdown_if_needed(dest, text, force=force, console=console)
            except FileNotFoundError:
                console.print(f"[yellow]Optional template not found:[/yellow] {template_name}")
            except (PermissionError, OSError) as e:
                console.print(f"[yellow]Could not create {output_name}:[/yellow] {e}")

        # Create CHANGELOG if configured and doesn't exist
        if self.config.create_changelog:
            changelog = feature_dir / "CHANGELOG.md"
            if not changelog.exists():
                content = f"# Changelog for {num_str}-{slug}\n\n- {_stamp()} - Initialized {self.config.command_name}\n"
                write_markdown_if_needed(changelog, content, force=True, console=console)

        # Print success message
        console.print(
            Panel(
                f"Feature ready: [cyan]{feature_dir}[/cyan]",
                title=f"{self.config.command_name.title()} Created",
                border_style="green",
            )
        )

    def _get_feature_dir(
        self,
        program_name: str,
        feature: Optional[str],
        console: Console,
    ) -> tuple[Path, str, str]:
        """
        Get or create feature directory with optional custom slug.

        Args:
            program_name: Program name
            feature: Optional custom feature slug
            console: Rich console

        Returns:
            Tuple of (feature_dir, num_str, slug)
        """
        if feature:
            # If full number provided (e.g., "001-custom-slug"), respect it
            if re.match(r"^\d{3}-", feature):
                feature_dir = _ensure_nuaa_root() / feature
                feature_dir.mkdir(parents=True, exist_ok=True)
                num_str = feature[:3]
                slug = feature.split("-", 1)[1]
                return feature_dir, num_str, slug
            else:
                # Treat as slug only; compute next number
                slug = _slugify(feature)
                feature_dir, num_str, _ = _next_feature_dir(slug)
                return feature_dir, num_str, slug
        else:
            # Auto-generate from program name
            feature_dir, num_str, slug = _next_feature_dir(program_name)
            return feature_dir, num_str, slug

    def _build_field_mapping_from_args(
        self,
        program_name: str,
        field_values: tuple,
        console: Console,
    ) -> dict[str, str]:
        """Build field mapping from positional arguments."""
        mapping = {
            self.config.primary_field_name: program_name,
            "DATE": datetime.now().strftime("%Y-%m-%d"),
        }

        if len(field_values) != len(self.config.fields):
            console.print(
                f"[red]Error:[/red] Expected {len(self.config.fields)} field(s), "
                f"got {len(field_values)}"
            )
            raise typer.Exit(1)

        for field_cfg, value in zip(self.config.fields, field_values):
            # Validate field
            validated_value = validate_text_field(
                value, field_cfg.name, field_cfg.max_length, console
            )

            # Add to mapping (uppercase for template placeholders)
            mapping[field_cfg.name.upper()] = validated_value

        return mapping


def _process_template(
    config: TemplateCommandConfig,
    feature_dir: Path,
    mapping: dict[str, str],
    program_name: str,
    num_str: str,
    slug: str,
    force: bool,
    console: Console,
) -> None:
    """
    Load template, apply replacements, and write output file.

    Centralizes all error handling for template processing pipeline.

    Args:
        config: Command configuration
        feature_dir: Feature directory path
        mapping: Field mapping for replacements
        program_name: Program name
        num_str: Feature number string (e.g., "001")
        slug: Feature slug string
        force: Whether to overwrite existing files
        console: Rich console for output

    Raises:
        typer.Exit: If template processing fails
    """
    try:
        # Load template
        template_content = _load_template(config.template_name)

        # Apply variable replacements
        filled_content = _apply_replacements(template_content, mapping)

        # Generate metadata
        if config.metadata_generator:
            metadata = config.metadata_generator(program_name, mapping)
        else:
            metadata = {
                "title": f"{program_name} - {config.command_name.title()}",
                "created": mapping["DATE"],
                "feature": f"{num_str}-{slug}",
                "status": "draft",
            }

        # Prepend YAML frontmatter
        final_content = _prepend_metadata(filled_content, metadata)

        # Write file
        output_path = feature_dir / config.output_filename
        write_markdown_if_needed(output_path, final_content, force=force, console=console)

    except FileNotFoundError:
        console.print(f"[red]Template not found:[/red] {config.template_name}")
        console.print("[dim]Run 'nuaa init' to set up templates[/dim]")
        raise typer.Exit(1)
    except PermissionError:
        console.print("[red]Permission denied:[/red] Cannot read template or write output file")
        raise typer.Exit(1)
    except OSError as e:
        console.print(f"[red]File system error:[/red] {e}")
        raise typer.Exit(1)
