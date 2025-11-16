#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import subprocess
import sys
import os


def run(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}")
    # Set UTF-8 encoding for subprocess to handle Unicode in banner
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    subprocess.run(cmd, check=True, env=env)


def main() -> None:
    cwd = Path.cwd()
    # Run minimal design flow
    run([sys.executable, "-m", "pip", "install", "-e", ".[dev]"])
    run(
        [
            sys.executable,
            "-m",
            "nuaa_cli",
            "design",
            "E2E Program",
            "audience",
            "12 months",
        ]
    )
    run(
        [
            sys.executable,
            "-m",
            "nuaa_cli",
            "propose",
            "E2E Program",
            "NSW Health",
            "$50000",
            "12 months",
        ]
    )
    run(
        [
            sys.executable,
            "-m",
            "nuaa_cli",
            "measure",
            "E2E Program",
            "12 months",
            "$7000",
        ]
    )
    run([sys.executable, "-m", "nuaa_cli", "document", "E2E Program"])
    run(
        [
            sys.executable,
            "-m",
            "nuaa_cli",
            "report",
            "E2E Program",
            "--type",
            "final",
        ]
    )

    # Assert outputs exist
    nuaa_dir = cwd / "nuaa"
    assert nuaa_dir.is_dir(), "nuaa/ directory not created"

    # Find first feature dir
    feature_dirs = sorted([p for p in nuaa_dir.iterdir() if p.is_dir()])
    assert feature_dirs, "No feature directories created"
    fd = feature_dirs[0]

    expected_files = [
        fd / "program-design.md",
        fd / "logic-model.md",
        fd / "impact-framework.md",
        fd / "proposal.md",
        fd / "existing-program-analysis.md",
        fd / "report.md",
    ]
    for f in expected_files:
        assert f.exists(), f"Expected file missing: {f}"
        content = f.read_text(encoding="utf-8")
        assert content.strip(), f"Expected non-empty content in: {f}"


if __name__ == "__main__":
    main()
