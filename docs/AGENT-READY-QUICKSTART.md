# Agent-Ready Quickstart Guide

**NUAA CLI 0.3.0+ • Agent-Ready MVP**

This guide introduces the new agent-ready features in NUAA CLI, including Model Context Protocol (MCP) support, agent bundling, and framework integrations.

---

## What's New in Agent-Ready NUAA CLI

NUAA CLI now supports modern agent frameworks and protocols:

✨ **MCP (Model Context Protocol)** - Standardized tool registration and invocation
📦 **Agent Bundling** - Package and distribute agent configurations
🎯 **CopilotKit Support** - Ready-to-use CopilotKit templates
🖥️ **AG-UI Widgets** - Agentic UI components
🔌 **Extended Agent Metadata** - Protocol and framework information

---

## Quick Start

### 1. Check Agent Capabilities

See which agents support MCP and other protocols:

```bash
nuaa check
```

This will show which agents are installed and their protocol support.

### 2. Use MCP Registry (Python API)

Register and call tools programmatically:

```python
from nuaa_cli.mcp import MCPRegistry, MCPToolDescriptor

# Create registry
registry = MCPRegistry()

# Register a tool
def design_program_handler(inputs):
    program_name = inputs['program_name']
    return f"Designing: {program_name}"

descriptor = MCPToolDescriptor(
    name="design_program",
    description="Create a new NUAA program design",
    input_schema={
        "program_name": str,
        "target_population": str,
        "duration": str
    },
    handler=design_program_handler
)

registry.register(descriptor)

# Call the tool
result = registry.call("design_program", {
    "program_name": "Peer Support Network",
    "target_population": "PWUD in Western Sydney",
    "duration": "12 months"
})

print(result)  # "Designing: Peer Support Network"
```

### 3. Create Agent Bundles

Package your agent configuration for distribution:

```bash
# Create a basic bundle
nuaa bundle my-agent-pack

# Include MCP configuration
nuaa bundle mcp-enabled --include-mcp

# Bundle specific agent
nuaa bundle claude-only --agent claude --version 2.0.0

# Full bundle with description
nuaa bundle nuaa-complete \
  --version 2.0.0 \
  --description "Complete NUAA setup for harm reduction programs" \
  --include-mcp
```

The bundle will be created in `./dist/` as a ZIP file containing:
- Agent command files (`.claude/`, `.github/agents/`, etc.)
- Templates (`nuaa-kit/templates/`)
- MCP configuration (if `--include-mcp`)
- Manifest with metadata

### 4. Use CopilotKit Templates

Initialize a project with CopilotKit support:

```bash
nuaa init my-project --ai copilot
```

This creates:
- `.github/agents/` - Copilot agent files
- `copilotkit/copilot-config.json` - CopilotKit configuration
- Standard NUAA templates

### 5. Use AG-UI Widgets

The agent-kit templates include a React widget for agentic UIs:

```bash
# Templates are in: nuaa-kit/templates/agent-kit-basic/ag-ui/

# Copy to your project
cp nuaa-kit/templates/agent-kit-basic/ag-ui/* your-project/src/components/
```

Import and use:

```tsx
import { NUAAWidget } from './components/widget';

function App() {
  const handleAction = (action, params) => {
    console.log(`Action: ${action}`, params);
    // Call NUAA CLI or API here
  };

  return <NUAAWidget onAction={handleAction} />;
}
```

---

## MCP Registry API Reference

### Creating a Registry

```python
from nuaa_cli.mcp import MCPRegistry

# Default registry (all tools allowed)
registry = MCPRegistry()

# Registry with allowlist (security)
registry = MCPRegistry(allowlist=["design_program", "create_proposal"])
```

### Registering Tools

```python
from nuaa_cli.mcp import MCPToolDescriptor

descriptor = MCPToolDescriptor(
    name="tool_name",              # Required: unique identifier
    description="What it does",     # Required: human-readable
    input_schema={"param": str},    # Required: parameter types
    handler=my_handler_function,    # Required: callable
    output_schema={"result": str},  # Optional: output structure
    requires_confirmation=False,    # Optional: needs user OK
    tags=["category", "feature"]    # Optional: for filtering
)

registry.register(descriptor)
```

### Calling Tools

```python
# Call tool
result = registry.call("tool_name", {"param": "value"})

# Validate without executing
is_valid = registry.validate("tool_name", {"param": "value"})

# Check if tool exists
exists = registry.has_tool("tool_name")
```

### Discovering Tools

```python
# List all tools
all_tools = registry.list_tools()

# Filter by tag
search_tools = registry.list_tools(tag="search")

# Get tool info
info = registry.get_tool_info("tool_name")
print(f"{info.name}: {info.description}")
```

---

## Agent Configuration Fields

Each agent in `agents.json` now includes protocol metadata:

```json
{
  "claude": {
    "name": "Claude Code",
    "folder": ".claude/commands/",
    "format": "Markdown",
    "cli_tool": "claude",
    "requires_cli": true,
    "protocol": "native",          // NEW: Protocol type
    "requires_mcp": false,          // NEW: Requires MCP
    "supports_mcp": true,           // NEW: Supports MCP
    "agent_framework": null         // NEW: Framework (e.g., "copilot")
  }
}
```

**Field Definitions**:

- `protocol`: Agent protocol type (`"native"`, `"mcp"`, `"a2a"`)
- `requires_mcp`: Whether agent requires MCP to function
- `supports_mcp`: Whether agent can use MCP tools
- `agent_framework`: Associated framework (`"copilot"`, `null`)

---

## Bundle Command Options

```bash
nuaa bundle NAME [OPTIONS]
```

**Arguments**:
- `NAME` - Bundle name (will be in filename)

**Options**:
- `--output, -o DIR` - Output directory (default: `./dist`)
- `--include-mcp` - Include MCP configuration
- `--include-templates` - Include NUAA templates (default: true)
- `--agent, -a AGENT` - Specific agent to bundle
- `--version, -v VERSION` - Bundle version (default: 1.0.0)
- `--description, -d TEXT` - Bundle description

**Examples**:

```bash
# Minimal bundle
nuaa bundle my-pack

# Production bundle
nuaa bundle production-v2 \
  --version 2.1.0 \
  --include-mcp \
  --description "Production-ready NUAA setup"

# Claude-only bundle
nuaa bundle claude-pack --agent claude

# Development bundle
nuaa bundle dev-setup \
  --output ./releases \
  --version 0.1.0-dev
```

---

## Error Handling

### MCP Registry Errors

```python
from nuaa_cli.mcp import (
    ToolNotFoundError,
    ToolValidationError,
    ToolExecutionError,
    ToolRegistrationError
)

try:
    result = registry.call("missing_tool", {})
except ToolNotFoundError as e:
    print(f"Tool not found: {e}")
except ToolValidationError as e:
    print(f"Invalid input: {e}")
except ToolExecutionError as e:
    print(f"Execution failed: {e}")
```

### Bundle Command Errors

```bash
# Bundle exists - will prompt for overwrite
nuaa bundle existing-pack

# Invalid agent - will warn and skip
nuaa bundle invalid --agent nonexistent
```

---

## Best Practices

### Tool Registration

1. **Use descriptive names**: `design_program` not `dp`
2. **Document thoroughly**: Good descriptions help users understand
3. **Validate inputs**: Let MCP handle validation automatically
4. **Keep handlers simple**: Complex logic should be in separate functions
5. **Tag appropriately**: Makes discovery easier

### Bundle Distribution

1. **Version consistently**: Use semantic versioning (e.g., `1.2.3`)
2. **Include documentation**: Add README.md to bundles
3. **Test before sharing**: Verify bundle works on clean install
4. **List dependencies**: Document any external requirements
5. **Provide examples**: Include sample usage in description

### Security

1. **Use allowlists**: Limit which tools can be registered
2. **Validate inputs**: Always validate in handlers
3. **Require confirmation**: For destructive operations
4. **Audit tool access**: Log tool calls in production
5. **Sandbox execution**: Consider containerization for untrusted tools

---

## Integration Examples

### With CLI Commands

```python
# Register NUAA commands as MCP tools
from nuaa_cli.mcp import MCPRegistry, MCPToolDescriptor
import subprocess

registry = MCPRegistry()

def nuaa_design_handler(inputs):
    cmd = [
        "nuaa", "design",
        inputs["program_name"],
        inputs["target_population"],
        inputs["duration"]
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

registry.register(MCPToolDescriptor(
    name="nuaa_design",
    description="Create NUAA program design",
    input_schema={
        "program_name": str,
        "target_population": str,
        "duration": str
    },
    handler=nuaa_design_handler
))
```

### With FastAPI

```python
from fastapi import FastAPI
from nuaa_cli.mcp import MCPRegistry

app = FastAPI()
registry = MCPRegistry()

# ... register tools ...

@app.post("/tools/{tool_name}")
async def call_tool(tool_name: str, inputs: dict):
    try:
        result = registry.call(tool_name, inputs)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/tools")
async def list_tools():
    tools = registry.list_tools()
    return [
        {"name": t.name, "description": t.description}
        for t in tools
    ]
```

---

## What's Next (Phase 2)

Future enhancements planned:

- **A2A Coordinator** - Agent-to-Agent communication
- **Advanced Bundling** - Dependency management, versioning
- **Marketplace Integration** - Publish and discover bundles
- **Extended Protocols** - More protocol adapters
- **UI Improvements** - Enhanced AG-UI components

---

## Support & Resources

- **Documentation**: `docs/`
- **Examples**: `nuaa-kit/examples/`
- **Issues**: https://github.com/zophiezlan/nuaa-cli/issues
- **AGENTS.md**: Full agent integration guide

---

**Version**: 0.3.0 (Agent-Ready MVP)
**Last Updated**: 2025-11-24
**Status**: ✅ Production Ready
