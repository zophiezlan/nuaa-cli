#!/usr/bin/env python3
"""
MCP Exception Classes
======================

Custom exceptions for MCP registry operations.
"""


class MCPError(Exception):
    """Base exception for all MCP-related errors."""

    pass


class ToolNotFoundError(MCPError):
    """Raised when attempting to access a tool that doesn't exist in the registry."""

    pass


class ToolValidationError(MCPError):
    """Raised when tool input validation fails."""

    pass


class ToolExecutionError(MCPError):
    """Raised when tool execution fails."""

    pass


class ToolRegistrationError(MCPError):
    """Raised when tool registration fails due to invalid descriptor or duplicate name."""

    pass
