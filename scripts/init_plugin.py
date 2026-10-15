#!/usr/bin/env python3
"""Safely initialize a Godot plugin template, interactively or via CLI flags."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
IDENTIFIER = re.compile(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*\Z")
SOURCE = ROOT / "addons" / "my_plugin"
FILES = [
    ROOT / "README.md",
    ROOT / "project.godot",
    SOURCE / "plugin.cfg",
    SOURCE / "plugin.gd",
    SOURCE / "editor" / "example_dock.gd",
    SOURCE / "editor" / "guide_topics.gd",
    ROOT / "tests" / "test_plugin.gd",
    ROOT / "tests" / "test_guides.gd",
    ROOT / "docs" / "DEVELOPMENT.md",
    ROOT / "docs" / "TESTING.md",
]

def _valid_text(value: str) -> bool:
    return bool(value.strip()) and not any(ord(c) < 32 or c == '"' or ord(c) == 127 for c in value)

def _valid_id(value: str) -> bool:
    return bool(IDENTIFIER.fullmatch(value)) and value != "my_plugin"

def _suggest_id(name: str) -> str:
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "_", ascii_name.lower()).strip("_")
    return slug if _valid_id(slug) else ""

def _interactive_terminal() -> bool:
    return sys.stdin.isatty()

def _supports_color(disabled: bool = False) -> bool:
    return (
        not disabled
        and "NO_COLOR" not in os.environ
        and os.environ.get("TERM", "") != "dumb"
        and sys.stdout.isatty()
    )

def _color(message: str, style: str, enabled: bool) -> str:
    codes = {"heading": "1;36", "hint": "36", "success": "1;32", "error": "1;31"}
    return f"\033[{codes[style]}m{message}\033[0m" if enabled else message

def _ask(label: str, explanation: str, validator, default: str = "",
         color: bool = False) -> str:
    while True:
        print(_color(label, "heading", color))
        print("  " + explanation)
        suffix = f" [{default}]" if default else ""
        value = input(f"  Value{suffix}: ").strip()
        if not value and default:
            value = default
        if validator(value):
            return value
        print(_color("  ERROR: Invalid value. Please try again.", "error", color))

def _wizard(args: argparse.Namespace) -> tuple[str, str, str] | None:
    colored = _supports_color(args.no_color)
    print(_color("\nGodot Plugin Setup  |  3 fields, no dependencies", "heading", colored))
    print("  Enter to accept suggested values. Ctrl+C cancels.")
    name = args.name or _ask(
        "\n[1/3] Plugin display name",
        'Human-readable name in Godot (e.g. "World Tools").',
        _valid_text, color=colored,
    )
    plugin_id = args.id or _ask(
        "\n[2/3] Plugin identifier",
        "Lowercase snake_case directory under addons/ (e.g. world_tools).",
        _valid_id, default=_suggest_id(name), color=colored,
    )
    author = args.author or _ask(
        "\n[3/3] Author",
        "Person or organization shown in plugin.cfg.",
        _valid_text, color=colored,
    )
    # Validate any values supplied via flags as well as prompted fields.
    if not _valid_id(plugin_id) or not _valid_text(name) or not _valid_text(author):
        raise ValueError("Invalid --id, --name or --author; run --help for examples.")
    print("\nReview (no files have been changed):")
    for label, value in (("Plugin", name), ("ID", plugin_id), ("Author", author),
                         ("Destination", f"addons/{plugin_id}/")):
        print(f"  {label}: {value}")
    answer = input("Create this plugin? [y/N]: ").strip().casefold()
    if answer not in ("y", "yes", "s", "si", "sí"):
        print("Cancelled. No files changed.")
        return None
    return plugin_id, name, author

def initialize(plugin_id: str, name: str, author: str, root: Path = ROOT) -> None:
    if not _valid_id(plugin_id):
        raise ValueError("Choose a new lowercase snake_case ID (e.g. world_tools)")
    if not _valid_text(name) or not _valid_text(author):
        raise ValueError("Name and author must be nonempty and contain no quotes/control characters")
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
    for p, content in contents.items():
        p.write_text(content, encoding="utf-8")
    original.rename(destination)
    print(f"Initialized {name} as addons/{plugin_id}/")
    print("Next: open project.godot, enable the plugin and run the checks.")

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Create a Godot plugin: flags for automation, or an interactive wizard."
    )
    parser.add_argument("--id", help="Lowercase snake_case plugin folder")
    parser.add_argument("--name", help="Human-readable plugin name")
    parser.add_argument("--author", help="Plugin author/organization")
    parser.add_argument("--no-color", action="store_true", help="Disable ANSI colors in the wizard")
    args = parser.parse_args(argv)
    try:
        if all((args.id, args.name, args.author)):
            values = (args.id, args.name, args.author)
        else:
            if not _interactive_terminal():
                print("ERROR: Missing plugin values; pass --id, --name and --author "
                      "when input is not a terminal. See --help.", file=sys.stderr)
                return 2
            values = _wizard(args)
            if values is None:
                return 0
        initialize(*values)
        return 0
    except (EOFError, KeyboardInterrupt):
        print("\nCancelled. No files changed.", file=sys.stderr)
        return 130
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
