from __future__ import annotations

import io
from typing import Any

from rich.console import Console

import nuaa_cli.commands.version as version_mod


class FakeHTTPXClientOffline:
    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: D401
        pass

    def __enter__(self) -> "FakeHTTPXClientOffline":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # noqa: D401
        return None

    def get(self, *args: Any, **kwargs: Any) -> Any:  # noqa: D401
        raise RuntimeError("offline")


class FakeResponse:
    def __init__(self, status_code: int, payload: dict[str, Any]) -> None:
        self.status_code = status_code
        self._payload = payload

    def json(self) -> dict[str, Any]:
        return self._payload


class FakeHTTPXClientOK:
    def __init__(self, *args: Any, **kwargs: Any) -> None:  # noqa: D401
        pass

    def __enter__(self) -> "FakeHTTPXClientOK":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # noqa: D401
        return None

    def get(self, *args: Any, **kwargs: Any) -> FakeResponse:  # noqa: D401
        return FakeResponse(
            200,
            {
                "tag_name": "v1.2.3",
                "published_at": "2025-11-12T00:00:00Z",
            },
        )


def test_version_offline(monkeypatch) -> None:
    # Patch httpx.Client to simulate offline
    monkeypatch.setattr(version_mod.httpx, "Client", FakeHTTPXClientOffline)

    # Capture console output
    buf = io.StringIO()
    version_mod.console = Console(
        file=buf,
        force_terminal=False,
        color_system=None,
    )

    # Run
    version_mod.version()
    out = buf.getvalue()

    assert "CLI Version" in out
    assert "Template Version" in out
    assert "Released" in out


def test_version_with_mock_release(monkeypatch) -> None:
    # Patch httpx.Client to return a fake successful response
    monkeypatch.setattr(version_mod.httpx, "Client", FakeHTTPXClientOK)

    buf = io.StringIO()
    version_mod.console = Console(
        file=buf,
        force_terminal=False,
        color_system=None,
    )

    version_mod.version()
    out = buf.getvalue()

    assert "Template Version" in out and "1.2.3" in out
    assert "Released" in out and "2025-11-12" in out
