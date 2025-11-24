"""
Comprehensive tests for MCP Registry module.

Tests cover:
- Tool registration and validation
- Tool invocation and error handling
- Registry management operations
- Security (allowlists)
- Edge cases and error conditions
"""

import pytest
from unittest.mock import Mock

from nuaa_cli.mcp import (
    MCPRegistry,
    MCPTool,
    MCPToolDescriptor,
    MCPError,
    ToolNotFoundError,
    ToolValidationError,
    ToolExecutionError,
    ToolRegistrationError,
)


class TestMCPToolDescriptor:
    """Tests for MCPToolDescriptor validation."""

    def test_descriptor_creation(self):
        """Test creating a valid tool descriptor."""
        handler = Mock(return_value="result")
        descriptor = MCPToolDescriptor(
            name="test_tool",
            description="A test tool",
            input_schema={"param1": str, "param2": int},
            handler=handler,
        )

        assert descriptor.name == "test_tool"
        assert descriptor.description == "A test tool"
        assert descriptor.input_schema == {"param1": str, "param2": int}
        assert descriptor.handler == handler
        assert descriptor.output_schema is None
        assert descriptor.requires_confirmation is False
        assert descriptor.tags == []

    def test_descriptor_with_optional_fields(self):
        """Test descriptor with all optional fields."""
        handler = Mock()
        descriptor = MCPToolDescriptor(
            name="advanced_tool",
            description="Advanced tool",
            input_schema={"query": str},
            handler=handler,
            output_schema={"result": str},
            requires_confirmation=True,
            tags=["search", "advanced"],
        )

        assert descriptor.output_schema == {"result": str}
        assert descriptor.requires_confirmation is True
        assert descriptor.tags == ["search", "advanced"]

    def test_validate_inputs_success(self):
        """Test input validation with valid inputs."""
        descriptor = MCPToolDescriptor(
            name="test",
            description="Test",
            input_schema={"name": str, "count": int},
            handler=Mock(),
        )

        # Should not raise
        descriptor.validate_inputs({"name": "test", "count": 5})

    def test_validate_inputs_missing_parameter(self):
        """Test validation fails with missing parameter."""
        descriptor = MCPToolDescriptor(
            name="test",
            description="Test",
            input_schema={"required_param": str},
            handler=Mock(),
        )

        with pytest.raises(ToolValidationError) as exc_info:
            descriptor.validate_inputs({})

        assert "Missing required parameters" in str(exc_info.value)
        assert "required_param" in str(exc_info.value)

    def test_validate_inputs_extra_parameter(self):
        """Test validation fails with unexpected parameter."""
        descriptor = MCPToolDescriptor(
            name="test",
            description="Test",
            input_schema={"expected": str},
            handler=Mock(),
        )

        with pytest.raises(ToolValidationError) as exc_info:
            descriptor.validate_inputs({"expected": "value", "unexpected": "extra"})

        assert "Unexpected parameters" in str(exc_info.value)
        assert "unexpected" in str(exc_info.value)

    def test_validate_inputs_wrong_type(self):
        """Test validation fails with wrong parameter type."""
        descriptor = MCPToolDescriptor(
            name="test",
            description="Test",
            input_schema={"count": int},
            handler=Mock(),
        )

        with pytest.raises(ToolValidationError) as exc_info:
            descriptor.validate_inputs({"count": "not an int"})

        assert "expected int" in str(exc_info.value)
        assert "got str" in str(exc_info.value)


class TestMCPRegistry:
    """Tests for MCPRegistry core functionality."""

    def test_registry_initialization(self):
        """Test creating an empty registry."""
        registry = MCPRegistry()

        assert registry.count() == 0
        assert registry.list_tools() == []

    def test_registry_with_allowlist(self):
        """Test registry with allowlist initialization."""
        registry = MCPRegistry(allowlist=["tool1", "tool2"])

        # Allowlist is set internally
        assert registry._allowlist == {"tool1", "tool2"}

    def test_register_tool_success(self):
        """Test successful tool registration."""
        registry = MCPRegistry()
        handler = Mock(return_value="result")

        descriptor = MCPToolDescriptor(
            name="test_tool",
            description="Test tool",
            input_schema={"param": str},
            handler=handler,
        )

        registry.register(descriptor)

        assert registry.count() == 1
        assert registry.has_tool("test_tool")

    def test_register_tool_empty_name(self):
        """Test registration fails with empty tool name."""
        registry = MCPRegistry()

        descriptor = MCPToolDescriptor(
            name="",
            description="Test",
            input_schema={},
            handler=Mock(),
        )

        with pytest.raises(ToolRegistrationError) as exc_info:
            registry.register(descriptor)

        assert "Tool name cannot be empty" in str(exc_info.value)

    def test_register_tool_duplicate(self):
        """Test registration fails with duplicate tool name."""
        registry = MCPRegistry()

        descriptor1 = MCPToolDescriptor(
            name="duplicate",
            description="First",
            input_schema={},
            handler=Mock(),
        )

        descriptor2 = MCPToolDescriptor(
            name="duplicate",
            description="Second",
            input_schema={},
            handler=Mock(),
        )

        registry.register(descriptor1)

        with pytest.raises(ToolRegistrationError) as exc_info:
            registry.register(descriptor2)

        assert "already registered" in str(exc_info.value)

    def test_register_tool_not_in_allowlist(self):
        """Test registration fails when tool not in allowlist."""
        registry = MCPRegistry(allowlist=["allowed_tool"])

        descriptor = MCPToolDescriptor(
            name="forbidden_tool",
            description="Test",
            input_schema={},
            handler=Mock(),
        )

        with pytest.raises(ToolRegistrationError) as exc_info:
            registry.register(descriptor)

        assert "not in the allowlist" in str(exc_info.value)

    def test_unregister_tool_success(self):
        """Test successful tool unregistration."""
        registry = MCPRegistry()

        descriptor = MCPToolDescriptor(
            name="temporary_tool",
            description="Test",
            input_schema={},
            handler=Mock(),
        )

        registry.register(descriptor)
        assert registry.count() == 1

        registry.unregister("temporary_tool")
        assert registry.count() == 0
        assert not registry.has_tool("temporary_tool")

    def test_unregister_tool_not_found(self):
        """Test unregister fails with non-existent tool."""
        registry = MCPRegistry()

        with pytest.raises(ToolNotFoundError):
            registry.unregister("nonexistent")

    def test_call_tool_success(self):
        """Test successful tool invocation."""
        registry = MCPRegistry()
        handler = Mock(return_value="success result")

        descriptor = MCPToolDescriptor(
            name="calculator",
            description="Add numbers",
            input_schema={"a": int, "b": int},
            handler=handler,
        )

        registry.register(descriptor)
        result = registry.call("calculator", {"a": 5, "b": 3})

        assert result == "success result"
        handler.assert_called_once_with({"a": 5, "b": 3})

    def test_call_tool_not_found(self):
        """Test call fails with non-existent tool."""
        registry = MCPRegistry()

        with pytest.raises(ToolNotFoundError) as exc_info:
            registry.call("nonexistent", {})

        assert "not found" in str(exc_info.value)
        assert "Available tools:" in str(exc_info.value)

    def test_call_tool_validation_error(self):
        """Test call fails with invalid inputs."""
        registry = MCPRegistry()

        descriptor = MCPToolDescriptor(
            name="strict_tool",
            description="Requires exact inputs",
            input_schema={"required": str},
            handler=Mock(),
        )

        registry.register(descriptor)

        with pytest.raises(ToolValidationError):
            registry.call("strict_tool", {})  # Missing required parameter

    def test_call_tool_execution_error(self):
        """Test call fails when handler raises exception."""
        registry = MCPRegistry()

        def failing_handler(inputs):
            raise ValueError("Handler failed")

        descriptor = MCPToolDescriptor(
            name="faulty_tool",
            description="Fails on execution",
            input_schema={"param": str},
            handler=failing_handler,
        )

        registry.register(descriptor)

        with pytest.raises(ToolExecutionError) as exc_info:
            registry.call("faulty_tool", {"param": "test"})

        assert "execution failed" in str(exc_info.value)
        assert "Handler failed" in str(exc_info.value)

    def test_validate_tool_success(self):
        """Test validate without executing."""
        registry = MCPRegistry()

        descriptor = MCPToolDescriptor(
            name="test_tool",
            description="Test",
            input_schema={"name": str},
            handler=Mock(),
        )

        registry.register(descriptor)

        # Should return True for valid inputs
        assert registry.validate("test_tool", {"name": "valid"}) is True

    def test_validate_tool_not_found(self):
        """Test validate fails with non-existent tool."""
        registry = MCPRegistry()

        with pytest.raises(ToolNotFoundError):
            registry.validate("nonexistent", {})

    def test_validate_tool_invalid_inputs(self):
        """Test validate fails with invalid inputs."""
        registry = MCPRegistry()

        descriptor = MCPToolDescriptor(
            name="test_tool",
            description="Test",
            input_schema={"count": int},
            handler=Mock(),
        )

        registry.register(descriptor)

        with pytest.raises(ToolValidationError):
            registry.validate("test_tool", {"count": "not an int"})

    def test_list_tools_empty(self):
        """Test listing tools from empty registry."""
        registry = MCPRegistry()

        tools = registry.list_tools()

        assert tools == []

    def test_list_tools_multiple(self):
        """Test listing multiple registered tools."""
        registry = MCPRegistry()

        for i in range(3):
            descriptor = MCPToolDescriptor(
                name=f"tool{i}",
                description=f"Tool {i}",
                input_schema={},
                handler=Mock(),
            )
            registry.register(descriptor)

        tools = registry.list_tools()

        assert len(tools) == 3
        tool_names = [t.name for t in tools]
        assert "tool0" in tool_names
        assert "tool1" in tool_names
        assert "tool2" in tool_names

    def test_list_tools_filter_by_tag(self):
        """Test listing tools filtered by tag."""
        registry = MCPRegistry()

        descriptor1 = MCPToolDescriptor(
            name="search_tool",
            description="Search",
            input_schema={},
            handler=Mock(),
            tags=["search", "query"],
        )

        descriptor2 = MCPToolDescriptor(
            name="create_tool",
            description="Create",
            input_schema={},
            handler=Mock(),
            tags=["create", "modify"],
        )

        descriptor3 = MCPToolDescriptor(
            name="advanced_search",
            description="Advanced search",
            input_schema={},
            handler=Mock(),
            tags=["search", "advanced"],
        )

        registry.register(descriptor1)
        registry.register(descriptor2)
        registry.register(descriptor3)

        # Filter by "search" tag
        search_tools = registry.list_tools(tag="search")

        assert len(search_tools) == 2
        tool_names = [t.name for t in search_tools]
        assert "search_tool" in tool_names
        assert "advanced_search" in tool_names
        assert "create_tool" not in tool_names

    def test_list_tools_returns_mcp_tool(self):
        """Test list_tools returns MCPTool objects without handlers."""
        registry = MCPRegistry()

        handler = Mock()
        descriptor = MCPToolDescriptor(
            name="test",
            description="Test tool",
            input_schema={"param": str},
            handler=handler,
            output_schema={"result": str},
            requires_confirmation=True,
            tags=["test"],
        )

        registry.register(descriptor)
        tools = registry.list_tools()

        assert len(tools) == 1
        tool = tools[0]

        # Verify it's an MCPTool instance
        assert isinstance(tool, MCPTool)
        assert tool.name == "test"
        assert tool.description == "Test tool"
        assert tool.input_schema == {"param": str}
        assert tool.output_schema == {"result": str}
        assert tool.requires_confirmation is True
        assert tool.tags == ["test"]

        # Verify handler is NOT exposed
        assert not hasattr(tool, "handler")

    def test_has_tool_exists(self):
        """Test has_tool returns True for existing tool."""
        registry = MCPRegistry()

        descriptor = MCPToolDescriptor(
            name="existing_tool",
            description="Test",
            input_schema={},
            handler=Mock(),
        )

        registry.register(descriptor)

        assert registry.has_tool("existing_tool") is True

    def test_has_tool_not_exists(self):
        """Test has_tool returns False for non-existent tool."""
        registry = MCPRegistry()

        assert registry.has_tool("nonexistent") is False

    def test_get_tool_info_success(self):
        """Test getting tool information."""
        registry = MCPRegistry()

        descriptor = MCPToolDescriptor(
            name="info_tool",
            description="Tool for testing info",
            input_schema={"query": str},
            handler=Mock(),
            tags=["info", "test"],
        )

        registry.register(descriptor)
        info = registry.get_tool_info("info_tool")

        assert isinstance(info, MCPTool)
        assert info.name == "info_tool"
        assert info.description == "Tool for testing info"
        assert info.tags == ["info", "test"]

    def test_get_tool_info_not_found(self):
        """Test get_tool_info fails with non-existent tool."""
        registry = MCPRegistry()

        with pytest.raises(ToolNotFoundError):
            registry.get_tool_info("nonexistent")

    def test_clear_registry(self):
        """Test clearing all tools from registry."""
        registry = MCPRegistry()

        # Register multiple tools
        for i in range(3):
            descriptor = MCPToolDescriptor(
                name=f"tool{i}",
                description=f"Tool {i}",
                input_schema={},
                handler=Mock(),
            )
            registry.register(descriptor)

        assert registry.count() == 3

        # Clear registry
        registry.clear()

        assert registry.count() == 0
        assert registry.list_tools() == []

    def test_count_tools(self):
        """Test counting registered tools."""
        registry = MCPRegistry()

        assert registry.count() == 0

        for i in range(5):
            descriptor = MCPToolDescriptor(
                name=f"tool{i}",
                description=f"Tool {i}",
                input_schema={},
                handler=Mock(),
            )
            registry.register(descriptor)

        assert registry.count() == 5


class TestMCPRegistryIntegration:
    """Integration tests for complete workflows."""

    def test_complete_workflow(self):
        """Test complete workflow: register, validate, call, list."""
        registry = MCPRegistry()

        # Create a realistic handler
        def calculator_handler(inputs):
            operation = inputs["operation"]
            a = inputs["a"]
            b = inputs["b"]

            if operation == "add":
                return a + b
            elif operation == "subtract":
                return a - b
            elif operation == "multiply":
                return a * b
            else:
                raise ValueError(f"Unknown operation: {operation}")

        # Register tool
        descriptor = MCPToolDescriptor(
            name="calculator",
            description="Perform arithmetic operations",
            input_schema={"operation": str, "a": int, "b": int},
            handler=calculator_handler,
            output_schema={"result": int},
            tags=["math", "calculator"],
        )

        registry.register(descriptor)

        # Verify registration
        assert registry.has_tool("calculator")
        assert registry.count() == 1

        # List tools
        tools = registry.list_tools()
        assert len(tools) == 1
        assert tools[0].name == "calculator"

        # Validate inputs
        assert registry.validate("calculator", {
            "operation": "add",
            "a": 5,
            "b": 3
        })

        # Call tool
        result = registry.call("calculator", {
            "operation": "add",
            "a": 5,
            "b": 3
        })
        assert result == 8

        result = registry.call("calculator", {
            "operation": "multiply",
            "a": 4,
            "b": 7
        })
        assert result == 28

    def test_multiple_tools_workflow(self):
        """Test workflow with multiple tools."""
        registry = MCPRegistry()

        # Register multiple tools
        tools_data = [
            ("search", "Search documents", {"query": str}, lambda i: f"Results for: {i['query']}"),
            ("create", "Create document", {"title": str}, lambda i: f"Created: {i['title']}"),
            ("delete", "Delete document", {"id": int}, lambda i: f"Deleted: {i['id']}"),
        ]

        for name, desc, schema, handler in tools_data:
            descriptor = MCPToolDescriptor(
                name=name,
                description=desc,
                input_schema=schema,
                handler=handler,
            )
            registry.register(descriptor)

        # Verify all registered
        assert registry.count() == 3

        # Call each tool
        search_result = registry.call("search", {"query": "test"})
        assert "Results for: test" in search_result

        create_result = registry.call("create", {"title": "New Doc"})
        assert "Created: New Doc" in create_result

        delete_result = registry.call("delete", {"id": 123})
        assert "Deleted: 123" in delete_result

    def test_security_allowlist_workflow(self):
        """Test security workflow with allowlist."""
        # Create registry with allowlist
        registry = MCPRegistry(allowlist=["safe_tool", "approved_tool"])

        # Try to register allowed tool - should succeed
        safe_descriptor = MCPToolDescriptor(
            name="safe_tool",
            description="Safe tool",
            input_schema={},
            handler=Mock(),
        )
        registry.register(safe_descriptor)
        assert registry.has_tool("safe_tool")

        # Try to register non-allowed tool - should fail
        unsafe_descriptor = MCPToolDescriptor(
            name="unsafe_tool",
            description="Unsafe tool",
            input_schema={},
            handler=Mock(),
        )

        with pytest.raises(ToolRegistrationError):
            registry.register(unsafe_descriptor)

        # Verify only allowed tool is registered
        assert registry.count() == 1
        assert registry.has_tool("safe_tool")
        assert not registry.has_tool("unsafe_tool")


class TestMCPExceptions:
    """Tests for MCP exception hierarchy."""

    def test_mcp_error_is_base(self):
        """Test MCPError is base exception."""
        assert issubclass(ToolNotFoundError, MCPError)
        assert issubclass(ToolValidationError, MCPError)
        assert issubclass(ToolExecutionError, MCPError)
        assert issubclass(ToolRegistrationError, MCPError)

    def test_exception_messages(self):
        """Test exception messages are descriptive."""
        not_found = ToolNotFoundError("Tool 'test' not found")
        assert "not found" in str(not_found)

        validation_error = ToolValidationError("Invalid input: expected int")
        assert "Invalid input" in str(validation_error)

        execution_error = ToolExecutionError("Tool failed: division by zero")
        assert "failed" in str(execution_error)

        registration_error = ToolRegistrationError("Tool already registered")
        assert "already registered" in str(registration_error)
