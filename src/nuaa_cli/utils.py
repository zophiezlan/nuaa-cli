import shutil
import re
from pathlib import Path
from rich.tree import Tree
from rich.console import Console
import typer


# Special handling for Claude CLI after `claude migrate-installer`
CLAUDE_LOCAL_PATH = Path.home() / ".claude" / "local" / "claude"


class StepTracker:
    """Track and render hierarchical steps without emojis.

    Similar to Claude Code tree output. Supports live auto-refresh via a
    provided refresh callback.
    """

    def __init__(self, title: str):
        self.title = title
        self.steps: list[dict] = []  # list of dicts: {key, label, status, detail}
        self.status_order = {
            "pending": 0,
            "running": 1,
            "done": 2,
            "error": 3,
            "skipped": 4,
        }
        self._refresh_cb = None  # callable to trigger UI refresh

    def attach_refresh(self, cb):
        self._refresh_cb = cb

    def add(self, key: str, label: str):
        if key not in [s["key"] for s in self.steps]:
            self.steps.append({"key": key, "label": label, "status": "pending", "detail": ""})
            self._maybe_refresh()

    def start(self, key: str, detail: str = ""):
        self._update(key, status="running", detail=detail)

    def complete(self, key: str, detail: str = ""):
        self._update(key, status="done", detail=detail)

    def error(self, key: str, detail: str = ""):
        self._update(key, status="error", detail=detail)

    def skip(self, key: str, detail: str = ""):
        self._update(key, status="skipped", detail=detail)

    def _update(self, key: str, status: str, detail: str):
        for s in self.steps:
            if s["key"] == key:
                s["status"] = status
                if detail:
                    s["detail"] = detail
                self._maybe_refresh()
                return

        self.steps.append({"key": key, "label": key, "status": status, "detail": detail})
        self._maybe_refresh()

    def _maybe_refresh(self):
        if self._refresh_cb:
            try:
                self._refresh_cb()
            except Exception:
                pass

    def render(self):
        tree = Tree(f"[cyan]{self.title}[/cyan]", guide_style="grey50")
        for step in self.steps:
            label = step["label"]
            detail_text = step["detail"].strip() if step["detail"] else ""

            status = step["status"]
            if status == "done":
                symbol = "[green]●[/green]"
            elif status == "pending":
                symbol = "[green dim]○[/green dim]"
            elif status == "running":
                symbol = "[cyan]○[/cyan]"
            elif status == "error":
                symbol = "[red]●[/red]"
            elif status == "skipped":
                symbol = "[yellow]○[/yellow]"
            else:
                symbol = " "

            if status == "pending":
                if detail_text:
                    line = f"{symbol} [bright_black]{label} ({detail_text})[/bright_black]"
                else:
                    line = f"{symbol} [bright_black]{label}[/bright_black]"
            else:
                if detail_text:
                    line = (
                        f"{symbol} [white]{label}[/white] "
                        f"[bright_black]({detail_text})[/bright_black]"
                    )
                else:
                    line = f"{symbol} [white]{label}[/white]"

            tree.add(line)
        return tree


def check_tool(tool: str, tracker: StepTracker | None = None) -> bool:
    """Check if a tool is installed. Optionally update tracker.

    Args:
        tool: Name of the tool to check
        tracker: Optional StepTracker to update with results

    Returns:
        True if tool is found, False otherwise
    """
    # Prioritize special local Claude installer alias
    if tool == "claude":
        if CLAUDE_LOCAL_PATH.exists() and CLAUDE_LOCAL_PATH.is_file():
            if tracker:
                tracker.complete(tool, "available")
            return True

    found = shutil.which(tool) is not None

    if tracker:
        if found:
            tracker.complete(tool, "available")
        else:
            tracker.error(tool, "not found")

    return found


def validate_non_empty(value: str, field_name: str, console: Console) -> str:
    """
    Validate that a string is not empty.

    Args:
        value: The value to validate
        field_name: Name of the field for error messages
        console: Rich console for error output

    Returns:
        Stripped value if valid

    Raises:
        typer.Exit: If validation fails
    """
    stripped = value.strip()
    if not stripped:
        console.print(f"[red]Error:[/red] {field_name} cannot be empty")
        raise typer.Exit(1)
    return stripped


def validate_length(value: str, field_name: str, max_length: int, console: Console) -> str:
    """
    Validate that a string does not exceed maximum length.

    Args:
        value: The value to validate
        field_name: Name of the field for error messages
        max_length: Maximum allowed length
        console: Rich console for error output

    Returns:
        Value if valid

    Raises:
        typer.Exit: If validation fails
    """
    if len(value) > max_length:
        console.print(
            f"[red]Error:[/red] {field_name} is too long (max {max_length} characters, got {len(value)})"
        )
        raise typer.Exit(1)
    return value


def sanitize_name(name: str, console: Console, allow_path_sep: bool = False) -> str:
    """
    Sanitize a name to prevent path traversal and ensure safe filesystem use.

    Args:
        name: The name to sanitize
        console: Rich console for warnings
        allow_path_sep: Whether to allow path separators (/ and \\)

    Returns:
        Sanitized name
    """
    original = name

    # Remove path traversal patterns
    name = name.replace("..", "")

    # Remove or replace dangerous characters
    if allow_path_sep:
        # Keep path separators but remove other dangerous chars
        safe_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -_./\\")
    else:
        # Remove all path separators and dangerous chars
        safe_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -_")

    sanitized = "".join(c for c in name if c in safe_chars)

    # Clean up multiple spaces/dashes
    sanitized = re.sub(r"[ -]+", "-", sanitized).strip("-")

    if sanitized != original:
        console.print(
            f"[yellow]Note:[/yellow] Name sanitized from '[cyan]{original}[/cyan]' to '[cyan]{sanitized}[/cyan]'"
        )

    return sanitized


def validate_program_name(name: str, console: Console) -> str:
    """
    Validate and sanitize a program name.

    Args:
        name: The program name to validate
        console: Rich console for error/warning output

    Returns:
        Validated and sanitized name

    Raises:
        typer.Exit: If validation fails
    """
    # Check non-empty
    name = validate_non_empty(name, "program_name", console)

    # Check length
    name = validate_length(name, "program_name", 100, console)

    # Sanitize for filesystem safety
    name = sanitize_name(name, console, allow_path_sep=False)

    # Final check after sanitization
    if not name:
        console.print("[red]Error:[/red] program_name becomes empty after sanitization")
        raise typer.Exit(1)

    return name


def validate_text_field(value: str, field_name: str, max_length: int, console: Console) -> str:
    """
    Validate a general text field (description, population, etc.).

    Args:
        value: The value to validate
        field_name: Name of the field for error messages
        max_length: Maximum allowed length
        console: Rich console for error output

    Returns:
        Validated value

    Raises:
        typer.Exit: If validation fails
    """
    # Check non-empty
    value = validate_non_empty(value, field_name, console)

    # Check length
    value = validate_length(value, field_name, max_length, console)

    return value
