#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS_JSON = REPO_ROOT / "src" / "nuaa_cli" / "agents.json"
BASH_SCRIPT = REPO_ROOT / "scripts" / "bash" / "update-agent-context.sh"
POWERSHELL_SCRIPT = REPO_ROOT / "scripts" / "powershell" / "update-agent-context.ps1"


def load_agent_keys() -> list[str]:
    data = json.loads(AGENTS_JSON.read_text(encoding="utf-8"))
    return list(data.keys())


def check_bash_usage(keys: list[str]) -> list[str]:
    text = BASH_SCRIPT.read_text(encoding="utf-8")
    errors: list[str] = []

    # Find the two lines we care about: top usage list and bottom Usage message
    usage_lines = []
    for line in text.splitlines():
        if "Agent types:" in line or "Usage: $0 [" in line:
            usage_lines.append(line)
    combined = "\n".join(usage_lines)
    for k in keys:
        if k not in combined:
            errors.append(f"bash usage missing: {k}")

    # Also ensure case labels exist for each key
    # crude check: 'case' section includes "<key>)"
    for k in keys:
        if f"{k})" not in text:
            errors.append(f"bash case missing: {k}")
    return errors


def check_powershell_validateset(keys: list[str]) -> list[str]:
    text = POWERSHELL_SCRIPT.read_text(encoding="utf-8")
    errors: list[str] = []

    # Extract ValidateSet content
    m = re.search(r"ValidateSet\(([^\)]*)\)", text)
    if not m:
        return ["powershell missing ValidateSet"]
    set_content = m.group(1)
    present = [s.strip(" ' ") for s in set_content.split(",") if s.strip()]
    for k in keys:
        if k not in present:
            errors.append(f"powershell ValidateSet missing: {k}")

    # Ensure switch cases exist: "'key' {"
    for k in keys:
        if f"'{k}'" not in text:
            errors.append(f"powershell switch missing: {k}")
    return errors


def main() -> None:
    keys = load_agent_keys()
    errs = []
    errs += check_bash_usage(keys)
    errs += check_powershell_validateset(keys)
    if errs:
        print("Agent script parity check failed:\n" + "\n".join(errs))
        raise SystemExit(1)
    print("Agent script parity check OK")


if __name__ == "__main__":
    main()
