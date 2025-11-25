"""
Scaffolding utilities for NUAA CLI.

This module provides core scaffolding functionality for creating
program directories, loading templates, and managing NUAA project structure.

Functions:
    _slugify: Convert text to filesystem-friendly slug
    _find_templates_root: Locate templates directory
    _ensure_nuaa_root: Ensure nuaa directory exists
    _next_feature_dir: Generate next feature directory
    _find_feature_dir_by_program: Find existing feature directory
    _load_template: Load template file
    _apply_replacements: Apply template variable replacements
    _prepend_metadata: Add YAML metadata to documents
    _write_markdown: Write markdown file
    _stamp: Get current timestamp
    get_or_create_feature_dir: Get or create feature directory
    write_markdown_if_needed: Conditionally write markdown file
"""

import re
from datetime import datetime
from pathlib import Path


def _slugify(text: str) -> str:
    """
    Convert text to a filesystem-friendly slug.

    Transforms text by:
    1. Converting to lowercase
    2. Removing non-alphanumeric characters (except spaces and hyphens)
    3. Replacing spaces/underscores with hyphens
    4. Removing leading/trailing hyphens

    Args:
        text: Input text to slugify

    Returns:
        Slugified text safe for filesystem use

    Example:
        >>> _slugify("My Program Name!")
        'my-program-name'
        >>> _slugify("Test_Program  123")
        'test-program-123'
    """
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return re.sub(r"^-+|-+$", "", text) or "feature"


def _find_templates_root(start: Path | None = None) -> Path:
    """
    Find templates directory by walking up from starting path.

    Searches for templates in the following order:
    1. .nuaa/templates or nuaa-kit/templates in current directory and parents
    2. .nuaa/templates or nuaa-kit/templates relative to package installation

    Args:
        start: Starting path for search (defaults to current working directory)

    Returns:
        Path to templates directory

    Raises:
        FileNotFoundError: If templates directory cannot be located

    Example:
        >>> templates = _find_templates_root()
        >>> assert templates.is_dir()
    """
    search_origin = start or Path.cwd()

    candidates: list[Path] = []
    for path in [search_origin, *search_origin.parents]:
        candidates.append(path / ".nuaa" / "templates")
        candidates.append(path / "nuaa-kit" / "templates")

    repo_root = Path(__file__).parent.parent.parent
    candidates.append(repo_root / ".nuaa" / "templates")
    candidates.append(repo_root / "nuaa-kit" / "templates")

    for candidate in candidates:
        if candidate.is_dir():
            return candidate

    raise FileNotFoundError(
        "Could not locate '.nuaa/templates' or 'nuaa-kit/templates'. "
        "Run 'nuaa init' first or ensure NUAA templates are available."
    )


def _ensure_nuaa_root(root: Path | None = None) -> Path:
    """Ensure the 'nuaa' directory exists under the project root."""
    if root is None:
        root = Path.cwd()
    nuaa_root = root / "nuaa"
    nuaa_root.mkdir(parents=True, exist_ok=True)
    return nuaa_root


def _next_feature_dir(program_name: str, root: Path | None = None) -> tuple[Path, str, str]:
    """
    Compute next feature directory and return (path, num_str, slug).

    This function implements atomic directory creation to prevent race conditions
    when multiple processes try to create directories simultaneously. It will retry
    up to 100 times if a directory already exists.

    Args:
        program_name: Name of the program for slugification
        root: Optional root path (defaults to current working directory)

    Returns:
        Tuple of (feature_dir, num_str, slug)

    Raises:
        RuntimeError: If unable to create a unique directory after maximum retries
    """
    nuaa_root = _ensure_nuaa_root(root)
    slug = _slugify(program_name)

    # Maximum retries to prevent infinite loops
    max_retries = 100

    for attempt in range(max_retries):
        # Find highest NNN prefix (refresh on each attempt to handle concurrent creation)
        highest = 0
        for child in nuaa_root.iterdir() if nuaa_root.exists() else []:
            if child.is_dir():
                m = re.match(r"^(\d{3})-", child.name)
                if m:
                    try:
                        highest = max(highest, int(m.group(1)))
                    except ValueError:
                        pass

        next_num = highest + 1
        num_str = f"{next_num:03d}"
        feature_dir = nuaa_root / f"{num_str}-{slug}"

        try:
            # Atomic operation: create directory only if it doesn't exist
            feature_dir.mkdir(parents=True, exist_ok=False)
            return feature_dir, num_str, slug
        except FileExistsError:
            # Another process created this directory, retry with next number
            continue

    # If we exhausted all retries, raise an error
    raise RuntimeError(
        f"Failed to create unique feature directory after {max_retries} attempts. "
        f"This may indicate a problem with concurrent directory creation."
    )


def _find_feature_dir_by_program(program_name: str, root: Path | None = None) -> Path | None:
    """Find an existing feature dir whose slug starts with the program slug."""
    nuaa_root = _ensure_nuaa_root(root)
    slug = _slugify(program_name)
    for child in sorted(nuaa_root.iterdir()) if nuaa_root.exists() else []:
        pattern = rf"-\b{re.escape(slug)}\b"
        if child.is_dir() and re.search(pattern, child.name):
            return child
    return None


def _load_template(name: str) -> str:
    """Load a template file from the discovered NUAA templates directory."""
    templates_root = _find_templates_root()
    path = templates_root / name
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {name}")
    return path.read_text(encoding="utf-8")


def _apply_replacements(text: str, mapping: dict[str, str]) -> str:
    """Apply placeholder replacements for [Placeholders] and {{TOKENS}}."""
    out = text
    # Bracket placeholders used in templates
    bracket_map = {
        "[Name]": mapping.get("PROGRAM_NAME", ""),
        "[Description]": mapping.get("TARGET_POPULATION", ""),
        "[Timeframe]": mapping.get("DURATION", ""),
        "[Date]": mapping.get("DATE", datetime.now().strftime("%Y-%m-%d")),
    }
    for k, v in bracket_map.items():
        out = out.replace(k, v)
    # Curly token replacements
    for k, v in mapping.items():
        out = out.replace(f"{{{{{k}}}}}", v)
    return out


def _prepend_metadata(text: str, metadata: dict[str, str]) -> str:
    """Prepend a YAML-style metadata block to markdown text."""
    lines = ["---"]
    for k, v in metadata.items():
        lines.append(f"{k}: {v}")
    lines.append("---\n")
    return "\n".join(lines) + text


def _write_markdown(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _stamp() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")


def get_or_create_feature_dir(program_name: str, root: Path | None = None) -> Path:
    """
    Get existing feature directory or create a new one.

    This function first searches for an existing feature directory matching
    the program name. If found, returns it. Otherwise, creates a new
    numbered feature directory.

    Args:
        program_name: Name of the program to find or create
        root: Optional root path (defaults to current working directory)

    Returns:
        Path to feature directory (existing or newly created)

    Example:
        >>> feature_dir = get_or_create_feature_dir("Peer Support Program")
        >>> assert feature_dir.exists()
        >>> assert feature_dir.name.endswith("peer-support-program")
    """
    found = _find_feature_dir_by_program(program_name, root=root)
    if found:
        return found
    return _next_feature_dir(program_name, root=root)[0]


def write_markdown_if_needed(
    path: Path,
    content: str,
    force: bool = False,
    console=None,
) -> bool:
    """Write markdown if needed; prints a message. Returns True if written."""
    if path.exists() and not force:
        if console:
            console.print(f"[yellow]File exists, skipping:[/yellow] {path}")
        return False
    _write_markdown(path, content)
    if console:
        console.print(f"[green]Created:[/green] {path}")
    return True
