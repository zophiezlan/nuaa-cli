import ssl
from datetime import datetime
from pathlib import Path

import httpx
import importlib.metadata
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import truststore


ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
console = Console()


def _github_auth_headers(token: str | None = None) -> dict:
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


def version() -> None:
    """Display version and system information."""
    # CLI version
    cli_version = "unknown"
    try:
        cli_version = importlib.metadata.version("nuaa-cli")
    except importlib.metadata.PackageNotFoundError:
        # Fallback: pyproject.toml when running from source
        try:
            import tomllib

            pyproject_path = Path(__file__).parents[3] / "pyproject.toml"
            if pyproject_path.exists():
                with open(pyproject_path, "rb") as f:
                    data = tomllib.load(f)
                    cli_version = data.get("project", {}).get("version", "unknown")
        except FileNotFoundError:
            pass
        except PermissionError:
            pass
        except OSError:
            pass
        except (KeyError, ValueError):
            # Invalid TOML format or missing version key
            pass

    # Latest release info
    repo_owner = "zophiezlan"
    repo_name = "nuaa-cli"
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"

    template_version = "unknown"
    release_date = "unknown"

    try:
        with httpx.Client(verify=ssl_context) as http_client:
            response = http_client.get(
                api_url,
                timeout=10,
                follow_redirects=True,
                headers=_github_auth_headers(),
            )
            if response.status_code == 200:
                release_data = response.json()
                template_version = release_data.get("tag_name", "unknown")
                if template_version.startswith("v"):
                    template_version = template_version[1:]
                release_date = release_data.get("published_at", "unknown")
                if release_date != "unknown":
                    try:
                        dt = datetime.fromisoformat(release_date.replace("Z", "+00:00"))
                        release_date = dt.strftime("%Y-%m-%d")
                    except (ValueError, AttributeError):
                        # Invalid date format
                        pass
    except httpx.TimeoutException:
        # Network timeout - version info stays as "unknown"
        pass
    except httpx.ConnectError:
        # Cannot connect to GitHub - version info stays as "unknown"
        pass
    except httpx.HTTPError:
        # HTTP error - version info stays as "unknown"
        pass
    except (ValueError, KeyError):
        # JSON parsing error or missing keys - version info stays as "unknown"
        pass

    info_table = Table(show_header=False, box=None, padding=(0, 2))
    info_table.add_column("Key", style="cyan", justify="right")
    info_table.add_column("Value", style="white")

    info_table.add_row("CLI Version", cli_version)
    info_table.add_row("Template Version", template_version)
    info_table.add_row("Released", release_date)

    panel = Panel(
        info_table,
        title="[bold cyan]NUAA CLI Information[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
    )

    console.print(panel)
    console.print()


def register(app):
    app.command()(version)
