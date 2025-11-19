import json
from pathlib import Path


def generate_agents_table(agents_data: dict, for_readme: bool = False) -> str:
    """Generates a Markdown table for the agents."""
    if for_readme:
        headers = ["Agent", "Website", "Support"]
    else:
        headers = ["Agent", "Directory", "Format", "CLI Tool", "Description"]

    lines = [f"| {' | '.join(headers)} |"]
    lines.append(f"|{'|'.join(['---'] * len(headers))}|")

    for key, data in agents_data.items():
        if for_readme:
            website = (
                f"[{data['name']}]({data['install_url']})" if data["install_url"] else data["name"]
            )
            support = "Full"  # Assuming full support for all listed agents
            row = [website, "Official", support]
        else:
            cli_tool = f"`{data['cli_tool']}`" if data["cli_tool"] else "N/A (IDE-based)"
            row = [
                f"**{data['name']}**",
                f"`{data['folder']}`",
                data["format"],
                cli_tool,
                data["description"],
            ]
        lines.append(f"| {' | '.join(row)} |")

    return "\n".join(lines)


def update_markdown_file(file_path: Path, table_content: str, marker_start: str, marker_end: str):
    """Updates the content of a Markdown file between specified markers."""
    if not file_path.exists():
        print(f"Warning: {file_path} not found. Skipping update.")
        return

    content = file_path.read_text(encoding="utf-8")

    start_index = content.find(marker_start)
    end_index = content.find(marker_end)

    if start_index == -1 or end_index == -1:
        print(f"Warning: Markers not found in {file_path}. Skipping update.")
        return

    new_content = (
        content[: start_index + len(marker_start)]
        + "\n\n"
        + table_content
        + "\n\n"
        + content[end_index:]
    )

    file_path.write_text(new_content, encoding="utf-8")
    print(f"Successfully updated {file_path}")


def main():
    """Main function to generate and update agent documentation."""
    repo_root = Path(__file__).parent.parent.parent
    agents_json_path = repo_root / "src" / "nuaa_cli" / "agents.json"

    with open(agents_json_path, "r", encoding="utf-8") as f:
        agents_data = json.load(f)

    # For AGENTS.md
    agents_md_table = generate_agents_table(agents_data, for_readme=False)
    agents_md_path = repo_root / "AGENTS.md"
    update_markdown_file(
        agents_md_path,
        agents_md_table,
        "<!-- AGENTS_TABLE_START -->",
        "<!-- AGENTS_TABLE_END -->",
    )

    # For README.md
    readme_table = generate_agents_table(agents_data, for_readme=True)
    readme_md_path = repo_root / "README.md"
    update_markdown_file(
        readme_md_path,
        readme_table,
        "<!-- SUPPORTED_AGENTS_START -->",
        "<!-- SUPPORTED_AGENTS_END -->",
    )


if __name__ == "__main__":
    main()
