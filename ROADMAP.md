**Conceptual Plan (complete, prioritized)**

**Overview**

- Goal: Make NUAA CLI "agent-ready" for 2025 agent stacks by supporting AG-UI, MCP, and A2A, CopilotKit templates, agent bundles, and monetization helpers — while preserving existing CLI behavior and backwards compatibility.
- Approach: Add lightweight adapter layers (MCP shim, A2A coordinator), AG-UI scaffolds, template bundles, CLI commands, docs, tests, and packaging hooks. Deliver an MVP focused on developer UX and safe defaults, then iterate to extended features.

**MVP (high priority — minimal viable product)**

- Deliverables:
  - `AGENT_CONFIG` extension to include `protocol`/`requires_mcp` fields (**init**.py or agents.json).
  - MCP shim: `src/nuaa_cli/mcp/registry.py` with register/call/validate endpoints.
  - CLI commands: `nuaa init --ai <agent>` enhanced help text and `nuaa bundle` command in scaffold.py.
  - Templates: Add minimal CopilotKit-compatible templates under `nuaa-kit/templates/agent-kit-basic/`.
  - Docs: Short "Agent-ready quickstart" in quickstart.md and update AGENTS.md.
  - Tests: Unit tests for MCP shim and CLI changes under tests.
- Acceptance criteria:
  - `nuaa init --ai copilotkit` produces a project scaffold containing the new `.ag-ui/` or `.copilot/` template files.
  - MCP shim can register one local tool and execute a sample call (mocked in tests).
  - Tests pass locally via `pytest -q`.

**Extended features (phase 2)**

- Deliverables:
  - Full A2A coordinator in `src/nuaa_cli/a2a/` (message bus, delegation APIs, ACL).
  - AG-UI example widget (small React/Vite demo) and a server-side event connector example in `nuaa-kit/examples/ag-ui-demo/`.
  - Agent bundle packaging & monetization metadata (`nuaa bundle` enhancements, metadata generation helpers).
  - Devcontainer and CI updates for contributor environment.
  - Release packaging scripts updated in scripts and .github.
  - Optional runtime adapters for CopilotKit and other popular frameworks.
- Acceptance criteria:
  - Two-agent workflow demo works end-to-end locally (using the coordinator and MCP to call tools).
  - Packaging creates marketplace-ready artifact with metadata and README.
  - Documentation includes step-by-step “create and sell an agent pack” tutorial.

**File-level change map (examples)**

- **init**.py — extend `AGENT_CONFIG` and export new metadata fields.
- `src/nuaa_cli/mcp/registry.py` — new module for MCP-compatible tool registry and adapters.
- `src/nuaa_cli/a2a/coordinator.py` — new module implementing in-process message bus for A2A.
- scaffold.py — add CLI subcommands `bundle`, `publish-metadata`, `scaffold --agent-kit`.
- templates — add `copilotkit/`, `ag-ui/`, `agent-bundle/` templates.
- docs — add `agentic-stack.md`, update AGENTS.md, `quickstart.md`.
- scripts — update `create-release-packages.sh`, `update-agent-context.*` to include new agent dirs.
- tests — add `test_mcp_registry.py`, `test_a2a_coordinator.py`, `test_bundle_command.py`.

**Design decisions & interfaces (conceptual)**

- Adapter pattern:
  - Provide `Adapter` base class in `src/nuaa_cli/adapters/base.py`.
  - MCP shim implements `register_tool(tool_id, descriptor)`, `call_tool(tool_id, input)`, and `validate_tool(tool_id)`. The shim exposes a pure-Python API used by scaffolds and tests.
- A2A coordinator:
  - In-process message bus with channels. Agents register with `agent_id` and can `send(to_agent, message)` and `broadcast()`.
  - Persistence: keep ephemeral by default; optional file-based journal for debugging.
- AG-UI scaffolds:
  - Minimal static widget that receives SSE/WebSocket updates. Provide `nuaa serve-ag-ui` helper to run local dev server (optional).
- Security & safety:
  - Tool calls require explicit registration and an allowlist by default (no global exec).
  - Provide config toggles for sandboxed execution and rate-limits.

**Testing strategy**

- Unit tests for adapters and CLI argument parsing.
- Integration smoke tests:
  - Mock agent process interacts with MCP shim and A2A coordinator.
  - `nuaa bundle` creates a zip file with expected manifest.
- CI:
  - Run `pytest -q` and a quick packaging lint step in GitHub Actions.

**Migration & backwards compatibility**

- Keep `AGENT_CONFIG` consumer code resilient: accept extra fields and ignore unknown entries.
- Versioning: bump pyproject.toml when `__init__.py` changes (follow AGENTS.md rule).
- Provide a CLI flag `--legacy` for scaffolds that should not include agent scaffolding.

**Estimated timeline (rough)**

- MVP (1–2 weeks, 1–2 engineers):
  - Day 1–2: repo survey, design adapters, update `AGENT_CONFIG`.
  - Day 3–6: implement MCP shim + CLI commands + templates.
  - Day 7–10: add docs, unit tests, and devcontainer tweaks; run tests and polish.
- Extended phase (2–4 weeks):
  - A2A coordinator, AG-UI demo, packaging improvements, release script updates, more examples.

**Risks and mitigations**

- Risk: breaking existing agent config consumers.
  - Mitigation: maintain backward-compatible parsing and add extensive tests.
- Risk: scope creep (AG-UI frontends can balloon).
  - Mitigation: keep AG-UI as a minimal scaffold + a separate demo repo for a full-featured app.
- Risk: security from tool execution.
  - Mitigation: default deny list, explicit registration, and clear docs about credentials.

**Deliverables summary**

- High-level architecture doc (new).
- `src/nuaa_cli/mcp/` and `src/nuaa_cli/a2a/` modules.
- CLI commands: `nuaa bundle`, `nuaa publish-metadata`, enhancements to `nuaa init`.
- Templates in templates.
- Updated AGENTS.md and docs content.
- Unit tests and CI updates.

**Next steps (pick one)**

- Option A (recommended): Proceed to create the repo survey and map exact files to edit (I can run a quick scan and produce a patch plan).
- Option B: I implement the MVP changes directly (requires confirmation).
- Option C: Iterate the conceptual plan with your priorities (which features are must-have vs optional).
