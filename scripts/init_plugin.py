#!/usr/bin/env python3
"""Safely initialize a newly generated Godot plugin repository exactly once."""
from __future__ import annotations
import argparse
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
IDENTIFIER = re.compile(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*\Z")
SOURCE = ROOT / "addons" / "my_plugin"
FILES = [
    ROOT / "README.md",
    ROOT / "project.godot",
    SOURCE / "plugin.cfg",
    SOURCE / "plugin.gd",
    SOURCE / "editor" / "example_dock.gd",
    ROOT / "tests" / "test_plugin.gd",
    ROOT / "docs" / "DEVELOPMENT.md",
    ROOT / "docs" / "TESTING.md",
]
def initialize(plugin_id: str, name: str, author: str, root: Path = ROOT) -> None:
    if not IDENTIFIER.fullmatch(plugin_id) or plugin_id == "my_plugin":
        raise ValueError("Choose a new lowercase snake_case ID (e.g. world_tools)")
    if not name.strip() or not author.strip() or any(c in name + author for c in '\r\n"'):
        raise ValueError("Name/author must be nonempty and contain no quotes/newlines")
    original = root / "addons" / "my_plugin"
    destination = root / "addons" / plugin_id
    if not original.is_dir() or destination.exists():
        raise ValueError("Template already initialized or destination already exists")
    paths = [root / path.relative_to(ROOT) for path in FILES]
    if not all(p.is_file() for p in paths):
        raise ValueError("Incomplete template; no changes made")
    contents = {p: p.read_text(encoding="utf-8") for p in paths}
    new_class = "".join(part.capitalize() for part in plugin_id.split("_"))
    for p, content in contents.items():
        content = content.replace("my_plugin", plugin_id).replace("MyPlugin", new_class)
        content = content.replace("My Plugin", name)
        if p.name == "plugin.cfg":
            content = content.replace("Template Author", author)
        if p.name == "project.godot":
            content = content.replace('config/name="Godot Plugin Template"', f'config/name="{name}"')
        contents[p] = content
    # All validation is complete before changing any files.
    for p, content in contents.items():
        p.write_text(content, encoding="utf-8")
    original.rename(destination)
    print(f"Initialized {name} as addons/{plugin_id}/")
    print("Next: open project.godot, enable the plugin and run the checks.")

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--author", required=True)
    args = parser.parse_args()
    try:
        initialize(args.id, args.name, args.author)
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
