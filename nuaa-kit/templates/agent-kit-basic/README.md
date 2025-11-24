# Agent Kit Templates

This directory contains templates for modern agent frameworks and protocols:

## CopilotKit

Templates for integrating with CopilotKit framework:
- Action definitions
- Agent configuration
- UI components

## AG-UI (Agentic UI)

Templates for agentic user interfaces:
- Widget scaffolds
- Event handlers
- State management

## Usage

These templates are automatically applied when using:

```bash
nuaa init --ai copilotkit my-project
```

Or can be bundled using:

```bash
nuaa bundle agent-pack --include-templates
```

## Customization

Templates support variable substitution:
- `{{PROJECT_NAME}}` - Project name
- `{{AGENT_TYPE}}` - Agent framework type
- `{{DATE}}` - Creation date
