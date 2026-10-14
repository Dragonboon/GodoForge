# Godot Plugin Template

A small, modular starting point for **Godot 4.7** editor plugins. [Use this template](https://github.com/sempitern0/godot-plugin-template/generate) to create your own repository.

## Start in three steps

1. Install **Godot 4.7.2** (or a compatible 4.7 release) and Python 3.10+.
2. Run `python3 scripts/init_plugin.py --id my_awesome_plugin --name "My Awesome Plugin" --author "Your Name"` **once**, from the new repository root.
3. Open `project.godot` in Godot, then enable the plugin at **Project > Project Settings > Plugins**.

The template ships with a removable example dock. Set `ENABLE_EXAMPLE_DOCK = false` in `addons/<your_id>/plugin.gd`, or remove the example code when you implement your own editor integration.

## Layout

```text
addons/my_plugin/
  plugin.cfg           # Godot plugin manifest
  plugin.gd            # EditorPlugin lifecycle and optional editor UI
  editor/example_dock.gd # Removable editor UI example
  src/                 # Runtime features: add only what your plugin needs
docs/
  DEVELOPMENT.md       # Patterns, packaging and compatibility
  TESTING.md           # Local checks and CI
scripts/
  init_plugin.py       # One-time safe naming helper
  ci/run_tests.py      # Headless Godot checks
tests/
  test_plugin.gd       # Plugin load smoke test
```

The **only distributable plugin** is `addons/<your_id>/`. Do not copy tests, CI, `project.godot`, or this repository's documentation into consuming projects.

## Verify

```bash
python3 scripts/ci/run_tests.py --godot godot
python3 -m unittest discover -s tests -p 'test_*.py'
```

See [Development](docs/DEVELOPMENT.md), [Testing](docs/TESTING.md), and [Contributing](CONTRIBUTING.md). Godot versions are validated by CI; support beyond 4.7 is **not implied** without testing.

## Design principles

- **Minimal:** no release updater, network calls, autoloads, or global classes by default.
- **Modular:** editor-only integration stays in `plugin.gd`/`editor`; optional runtime code belongs in `src`.
- **Reversible:** register resources in `_enter_tree()` and release them in `_exit_tree()`.
- **Portable:** plugin paths are relative to its folder, with no references to the template repository after initialization.

Inspired by real Godot addons: [Atrium](https://github.com/Dragonboon/Atrium) (editor docking), [Trispark](https://github.com/Dragonboon/Trispark) (modular features), and [JigsawG](https://github.com/Dragonboon/JigsawG) (lean plugin entry point and regression tests).

MIT licensed. This repository is a **template**, not a published runtime dependency.
