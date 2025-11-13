#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS_JSON = REPO_ROOT / "src" / "nuaa_cli" / "agents.json"
README = REPO_ROOT / "README.md"
AGENTS_MD = REPO_ROOT / "AGENTS.md"


def load_agents() -> dict:
    with open(AGENTS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def render_supported_agents_table(agents: dict) -> str:
    # README table: Agent | Website | Support
    rows = ["| Agent | Website | Support |", "|---|---|---|"]
    order = list(agents.keys())
    for key in order:
        a = agents[key]
        name = a.get("name", key)
        url = a.get("install_url")
        if url:
            agent_cell = f"[{name}]({url})"
            website = "Official"
        else:
            agent_cell = name
            website = "Official"
        rows.append(f"| {agent_cell} | {website} | Full |")
    return "\n".join(rows)


def render_agents_md_table(agents: dict) -> str:
    # AGENTS.md table: Agent | Directory | Format | CLI Tool | Description
    rows = [
        "| Agent | Directory | Format | CLI Tool | Description |",
        "|---|---|---|---|---|",
    ]
    order = list(agents.keys())
    for key in order:
        a = agents[key]
        name = a.get("name", key)
        folder = a.get("folder", "")
        fmt = a.get("format", "")
        cli = a.get("cli_tool") or "N/A"
        desc = a.get("description", "")
        rows.append(f"| **{name}** | `{folder}` | {fmt} | `{cli}` | {desc} |")
    return "\n".join(rows)


def replace_between_markers(text: str, start: str, end: str, replacement: str) -> str:
    start_idx = text.find(start)
    end_idx = text.find(end)
    if start_idx == -1 or end_idx == -1 or end_idx < start_idx:
        return text
    before = text[: start_idx + len(start)]
    after = text[end_idx:]
    return f"{before}\n\n{replacement}\n\n{after}"


def update_readme(agents: dict) -> None:
    content = README.read_text(encoding="utf-8")
    table = render_supported_agents_table(agents)
    updated = replace_between_markers(
        content,
        "<!-- SUPPORTED_AGENTS_START -->",
        "<!-- SUPPORTED_AGENTS_END -->",
        table,
    )
    README.write_text(updated, encoding="utf-8")


def update_agents_md(agents: dict) -> None:
    content = AGENTS_MD.read_text(encoding="utf-8")
    table = render_agents_md_table(agents)
    updated = replace_between_markers(
        content,
        "<!-- AGENTS_TABLE_START -->",
        "<!-- AGENTS_TABLE_END -->",
        table,
    )
    AGENTS_MD.write_text(updated, encoding="utf-8")


def main() -> None:
    agents = load_agents()
    update_readme(agents)
    update_agents_md(agents)


if __name__ == "__main__":
    main()
