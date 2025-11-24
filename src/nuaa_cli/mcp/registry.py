#!/usr/bin/env python3
"""
MCP Registry - Model Context Protocol Tool Registry
====================================================

Provides a lightweight registry for managing MCP-compatible tools.
Supports registration, validation, invocation, and discovery of tools
that can be called by AI agents through standardized interfaces.

Key Features:
- Tool registration with schema validation
- Safe tool invocation with input validation
- Tool discovery and enumeration
- Allowlist-based security controls
- Optional sandboxing (future enhancement)

Example Usage:
    >>> from nuaa_cli.mcp import MCPRegistry, MCPToolDescriptor
    >>>
    >>> # Create registry
    >>> registry = MCPRegistry()
    >>>
    >>> # Register a tool
    >>> descriptor = MCPToolDescriptor(
    ...     name="get_weather",
    ...     description="Get current weather for a location",
    ...     input_schema={"location": str},
    ...     handler=lambda inputs: f"Weather in {inputs['location']}: Sunny"
    ... )
    >>> registry.register(descriptor)
    >>>
    >>> # Call the tool
    >>> result = registry.call("get_weather", {"location": "Sydney"})
    >>> print(result)  # "Weather in Sydney: Sunny"
    >>>
    >>> # List tools
    >>> tools = registry.list_tools()
    >>> for tool in tools:
    ...     print(f"{tool.name}: {tool.description}")

Author: NUAA Project
License: MIT
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from .exceptions import (
    ToolNotFoundError,
    ToolRegistrationError,
    ToolValidationError,
    ToolExecutionError,
)


@dataclass
class MCPToolDescriptor:
    """
    Descriptor for an MCP-compatible tool.

    Attributes:
        name: Unique tool identifier (e.g., "get_weather", "search_docs")
        description: Human-readable description of what the tool does
        input_schema: Dictionary describing expected input parameters and their types
        handler: Callable that implements the tool's logic
        output_schema: Optional dictionary describing output structure
        requires_confirmation: Whether tool execution requires user confirmation
        tags: Optional list of tags for categorization

    Example:
        >>> descriptor = MCPToolDescriptor(
        ...     name="search",
        ...     description="Search documentation",
        ...     input_schema={"query": str, "limit": int},
        ...     handler=lambda inputs: search_docs(inputs["query"], inputs["limit"]),
        ...     tags=["search", "docs"]
        ... )
    """

    name: str
    description: str
    input_schema: dict[str, type]
    handler: Callable[[dict[str, Any]], Any]
    output_schema: Optional[dict[str, type]] = None
    requires_confirmation: bool = False
    tags: list[str] = field(default_factory=list)

    def validate_inputs(self, inputs: dict[str, Any]) -> None:
        """
        Validate tool inputs against the schema.

        Args:
            inputs: Dictionary of input parameters

        Raises:
            ToolValidationError: If validation fails
        """
        # Check for missing required parameters
        missing = set(self.input_schema.keys()) - set(inputs.keys())
        if missing:
            raise ToolValidationError(
                f"Missing required parameters for tool '{self.name}': {', '.join(missing)}"
            )

        # Check for extra parameters
        extra = set(inputs.keys()) - set(self.input_schema.keys())
        if extra:
            raise ToolValidationError(
                f"Unexpected parameters for tool '{self.name}': {', '.join(extra)}"
            )

        # Type validation
        for param_name, expected_type in self.input_schema.items():
            value = inputs[param_name]
            if not isinstance(value, expected_type):
                raise ToolValidationError(
                    f"Parameter '{param_name}' for tool '{self.name}' "
                    f"expected {expected_type.__name__}, got {type(value).__name__}"
                )


@dataclass
class MCPTool:
    """
    Representation of a registered tool (read-only view).

    This is what gets returned by list_tools() - it doesn't include
    the handler function for security reasons.
    """

    name: str
    description: str
    input_schema: dict[str, type]
    output_schema: Optional[dict[str, type]]
    requires_confirmation: bool
    tags: list[str]


class MCPRegistry:
    """
    Registry for managing MCP-compatible tools.

    Provides centralized tool registration, validation, and invocation.
    Implements basic security controls through allowlists and validation.

    Attributes:
        _tools: Internal dictionary mapping tool names to descriptors
        _allowlist: Optional set of allowed tool names (None = all allowed)

    Example:
        >>> registry = MCPRegistry()
        >>> registry.register(tool_descriptor)
        >>> result = registry.call("tool_name", {"param": "value"})
    """

    def __init__(self, allowlist: Optional[list[str]] = None):
        """
        Initialize the MCP registry.

        Args:
            allowlist: Optional list of allowed tool names. If provided,
                only tools in this list can be registered and called.
        """
        self._tools: dict[str, MCPToolDescriptor] = {}
        self._allowlist: Optional[set[str]] = set(allowlist) if allowlist else None

    def register(self, descriptor: MCPToolDescriptor) -> None:
        """
        Register a tool in the registry.

        Args:
            descriptor: Tool descriptor containing metadata and handler

        Raises:
            ToolRegistrationError: If tool name is invalid, already registered,
                or not in allowlist
        """
        # Validate tool name
        if not descriptor.name or not descriptor.name.strip():
            raise ToolRegistrationError("Tool name cannot be empty")

        # Check if already registered
        if descriptor.name in self._tools:
            raise ToolRegistrationError(f"Tool '{descriptor.name}' is already registered")

        # Check allowlist
        if self._allowlist is not None and descriptor.name not in self._allowlist:
            raise ToolRegistrationError(f"Tool '{descriptor.name}' is not in the allowlist")

        # Register the tool
        self._tools[descriptor.name] = descriptor

    def unregister(self, tool_name: str) -> None:
        """
        Unregister a tool from the registry.

        Args:
            tool_name: Name of tool to unregister

        Raises:
            ToolNotFoundError: If tool is not registered
        """
        if tool_name not in self._tools:
            raise ToolNotFoundError(f"Tool '{tool_name}' is not registered")

        del self._tools[tool_name]

    def call(self, tool_name: str, inputs: dict[str, Any]) -> Any:
        """
        Call a registered tool with the provided inputs.

        Args:
            tool_name: Name of tool to call
            inputs: Dictionary of input parameters

        Returns:
            Tool execution result

        Raises:
            ToolNotFoundError: If tool is not registered
            ToolValidationError: If input validation fails
            ToolExecutionError: If tool execution fails
        """
        # Check if tool exists
        if tool_name not in self._tools:
            raise ToolNotFoundError(
                f"Tool '{tool_name}' not found. "
                f"Available tools: {', '.join(self._tools.keys())}"
            )

        descriptor = self._tools[tool_name]

        # Validate inputs
        try:
            descriptor.validate_inputs(inputs)
        except ToolValidationError:
            raise  # Re-raise validation errors as-is

        # Execute tool
        try:
            return descriptor.handler(inputs)
        except Exception as e:
            raise ToolExecutionError(f"Tool '{tool_name}' execution failed: {str(e)}") from e

    def validate(self, tool_name: str, inputs: dict[str, Any]) -> bool:
        """
        Validate inputs for a tool without executing it.

        Args:
            tool_name: Name of tool to validate
            inputs: Dictionary of input parameters

        Returns:
            True if validation succeeds

        Raises:
            ToolNotFoundError: If tool is not registered
            ToolValidationError: If validation fails
        """
        if tool_name not in self._tools:
            raise ToolNotFoundError(f"Tool '{tool_name}' is not registered")

        descriptor = self._tools[tool_name]
        descriptor.validate_inputs(inputs)
        return True

    def list_tools(self, tag: Optional[str] = None) -> list[MCPTool]:
        """
        List all registered tools.

        Args:
            tag: Optional tag to filter tools by

        Returns:
            List of MCPTool objects (read-only views without handlers)
        """
        tools = []
        for descriptor in self._tools.values():
            # Filter by tag if specified
            if tag and tag not in descriptor.tags:
                continue

            tools.append(
                MCPTool(
                    name=descriptor.name,
                    description=descriptor.description,
                    input_schema=descriptor.input_schema,
                    output_schema=descriptor.output_schema,
                    requires_confirmation=descriptor.requires_confirmation,
                    tags=descriptor.tags,
                )
            )
        return tools

    def has_tool(self, tool_name: str) -> bool:
        """
        Check if a tool is registered.

        Args:
            tool_name: Name of tool to check

        Returns:
            True if tool is registered, False otherwise
        """
        return tool_name in self._tools

    def get_tool_info(self, tool_name: str) -> MCPTool:
        """
        Get information about a registered tool.

        Args:
            tool_name: Name of tool

        Returns:
            MCPTool object with tool metadata

        Raises:
            ToolNotFoundError: If tool is not registered
        """
        if tool_name not in self._tools:
            raise ToolNotFoundError(f"Tool '{tool_name}' is not registered")

        descriptor = self._tools[tool_name]
        return MCPTool(
            name=descriptor.name,
            description=descriptor.description,
            input_schema=descriptor.input_schema,
            output_schema=descriptor.output_schema,
            requires_confirmation=descriptor.requires_confirmation,
            tags=descriptor.tags,
        )

    def clear(self) -> None:
        """Clear all registered tools from the registry."""
        self._tools.clear()

    def count(self) -> int:
        """Return the number of registered tools."""
        return len(self._tools)
