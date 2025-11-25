#!/usr/bin/env python3
"""
Compile .po translation files to .mo binary files.

This script compiles all translation files in the locales/ directory
without requiring the external msgfmt tool.
"""

import array
from pathlib import Path


def generate_mo_file(po_file, mo_file):
    """
    Generate a .mo file from a .po file.

    Args:
        po_file: Path to the .po source file
        mo_file: Path to the .mo output file
    """
    # Parse the .po file
    catalog = {}
    current_msgid = None
    current_msgstr = None

    with open(po_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue

            # Extract msgid
            if line.startswith("msgid "):
                # Save previous entry
                if current_msgid is not None and current_msgstr is not None:
                    catalog[current_msgid] = current_msgstr

                # Start new entry
                current_msgid = line[7:-1]  # Remove 'msgid "' and '"'
                current_msgstr = None

            # Extract msgstr
            elif line.startswith("msgstr "):
                current_msgstr = line[8:-1]  # Remove 'msgstr "' and '"'

            # Handle multiline strings
            elif line.startswith('"') and line.endswith('"'):
                content = line[1:-1]
                if current_msgstr is None:
                    if current_msgid is not None:
                        current_msgid += content
                else:
                    current_msgstr += content

    # Save last entry
    if current_msgid is not None and current_msgstr is not None:
        catalog[current_msgid] = current_msgstr

    # Remove the metadata entry (empty msgid)
    catalog.pop("", None)

    # Generate .mo file
    keys = sorted(catalog.keys())
    offsets = []
    ids = []
    strs = []

    for key in keys:
        ids.append(key.encode("utf-8"))
        strs.append(catalog[key].encode("utf-8"))

    # Calculate offsets
    keystart = 7 * 4 + 16 * len(keys)
    valuestart = keystart + sum(len(k) + 1 for k in ids)

    # Create the .mo file structure
    koffsets = []
    voffsets = []

    for i, (key, value) in enumerate(zip(ids, strs)):
        koffsets.append((len(key), keystart))
        keystart += len(key) + 1
        voffsets.append((len(value), valuestart))
        valuestart += len(value) + 1

    # Generate the header
    output = array.array("I")  # Use unsigned int
    output.append(0x950412DE)  # Magic number
    output.append(0)  # Version
    output.append(len(keys))  # Number of entries
    output.append(7 * 4)  # Start of key index
    output.append(7 * 4 + len(keys) * 8)  # Start of value index
    output.append(0)  # Size of hash table
    output.append(0)  # Offset of hash table

    # Add key index
    for length, offset in koffsets:
        output.append(length)
        output.append(offset)

    # Add value index
    for length, offset in voffsets:
        output.append(length)
        output.append(offset)

    # Write to file
    with open(mo_file, "wb") as f:
        f.write(output.tobytes())
        for key in ids:
            f.write(key)
            f.write(b"\x00")
        for value in strs:
            f.write(value)
            f.write(b"\x00")


def compile_all_translations():
    """Compile all .po files in the locales directory."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    locales_dir = project_root / "locales"

    if not locales_dir.exists():
        print(f"Error: locales directory not found at {locales_dir}")
        return

    compiled_count = 0
    error_count = 0

    # Find all .po files
    for po_file in locales_dir.rglob("*.po"):
        mo_file = po_file.with_suffix(".mo")

        try:
            print(f"Compiling {po_file.relative_to(project_root)}...")
            generate_mo_file(po_file, mo_file)
            print(f"  ✓ Created {mo_file.relative_to(project_root)}")
            compiled_count += 1
        except Exception as e:
            print(f"  ✗ Error compiling {po_file.name}: {e}")
            error_count += 1

    print("\nCompilation complete!")
    print(f"  Compiled: {compiled_count}")
    if error_count > 0:
        print(f"  Errors: {error_count}")


def main():
    """Main entry point."""
    print("NUAA CLI Translation Compiler")
    print("=" * 40)
    compile_all_translations()


if __name__ == "__main__":
    main()
