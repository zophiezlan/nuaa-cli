#!/usr/bin/env python3
"""
NUAA CLI MCP (Model Context Protocol) Module
=============================================

Provides Model Context Protocol integration for NUAA CLI, enabling
standardized tool registration, invocation, and validation across
different AI agents and frameworks.

This module implements a lightweight MCP shim that allows:
- Tool registration with standardized descriptors
- Safe tool invocation with input validation
- Tool discovery and enumeration
- Basic security controls (allowlists, sandboxing)

Public API:
    - MCPRegistry: Main registry for tool management
    - MCPTool: Tool descriptor class
    - register_tool: Register a new tool
    - call_tool: Invoke a registered tool
    - list_tools: Enumerate available tools

Author: NUAA Project
License: MIT
"""

from .registry import MCPRegistry, MCPTool, MCPToolDescriptor
from .exceptions import MCPError, ToolNotFoundError, ToolValidationError

__all__ = [
    "MCPRegistry",
    "MCPTool",
    "MCPToolDescriptor",
    "MCPError",
    "ToolNotFoundError",
    "ToolValidationError",
]
