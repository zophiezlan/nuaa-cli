from pathlib import Path

from nuaa_cli.scaffold import (
    get_or_create_feature_dir,
    write_markdown_if_needed,
)


def test_get_or_create_feature_dir_creates_first_feature_dir(tmp_path: Path):
    root = tmp_path
    program = "Peer Naloxone Distribution"

    feature_dir = get_or_create_feature_dir(
        program_name=program,
        root=root,
    )

    # Expect nuaa root and numbered feature directory with slug
    assert (root / "nuaa").is_dir()
    assert feature_dir.exists()
    assert feature_dir.parent.name == "nuaa"
    assert feature_dir.name.startswith("001-")
    assert "peer-naloxone-distribution" in feature_dir.name


def test_feature_dir_reuse_and_increment(tmp_path: Path):
    root = tmp_path
    program1 = "Peer Naloxone Distribution"
    program2 = "Outreach & Needle Exchange"

    first = get_or_create_feature_dir(program_name=program1, root=root)
    # Same program should resolve to the same directory
    second = get_or_create_feature_dir(program_name=program1, root=root)
    assert first == second

    # New program should get the next number
    third = get_or_create_feature_dir(program_name=program2, root=root)
    assert first.name.startswith("001-")
    assert third.name.startswith("002-")


def test_write_markdown_if_needed_creates_and_respects_force(tmp_path: Path):
    md_path = tmp_path / "sample.md"

    # initial write
    write_markdown_if_needed(md_path, "first", force=False, console=None)
    assert md_path.read_text(encoding="utf-8") == "first"

    # no overwrite without force
    write_markdown_if_needed(md_path, "second", force=False, console=None)
    assert md_path.read_text(encoding="utf-8") == "first"

    # overwrite with force
    write_markdown_if_needed(md_path, "second", force=True, console=None)
    assert md_path.read_text(encoding="utf-8") == "second"
