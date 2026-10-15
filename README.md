# Godot Plugin Template

A small, modular starting point for **Godot 4.7** editor plugins. [Use this template](https://github.com/sempitern0/godot-plugin-template/generate) to create your own repository.

## Start in three steps

1. Install **Godot 4.7.2** (or a compatible 4.7 release) and Python 3.10+.
2. Run **`python3 scripts/init_plugin.py`** from the new repository root. Follow the accessible terminal wizard to enter a name, ID and author; review and confirm. For CI, use `--id world_tools --name "World Tools" --author "Developer"`.
3. Open `project.godot` in Godot, then enable the plugin at **Project > Project Settings > Plugins**.

The optional right-side **Plugin Guide** dock contains six offline tutorials (editor dock, custom node, Inspector, Tools menu, resources, tests) with selectable snippets and a copy button. It uses scrollable content instead of forcing editor height; its layout does not include the bottom panel. Remove it before publishing if it is not part of your addon.

## Layout

```text
addons/my_plugin/
  plugin.cfg                  # Godot plugin manifest
  plugin.gd                   # EditorPlugin registration and cleanup
  editor/example_dock.gd     # Optional, scrollable learning interface
  editor/guide_topics.gd     # Optional, offline how-to recipes
  src/                        # Runtime features: add only what you need
docs/
  DEVELOPMENT.md              # Creating editor features, packaging, compatibility
  TESTING.md                  # Local checks and GUI checklist
scripts/
  init_plugin.py              # One-time wizard or noninteractive CLI
  ci/run_tests.py             # Headless Godot checks
tests/
  test_plugin.gd              # Plugin import smoke test
  test_guides.gd              # Offline guide data and layout smoke test
```

Only `addons/<your_id>/` is distributed to consuming projects. Do not copy the test suite, CI or template's host project.

## Verify

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/ci/run_tests.py --godot godot
```

See [Development](docs/DEVELOPMENT.md), [Testing](docs/TESTING.md) and [Contributing](CONTRIBUTING.md). Godot versions are validated by CI; support beyond 4.7 is not implied.

## Principles

- **Minimal:** no updater, network requests, autoloads, or global classes by default.
- **Modular:** editor-only integration lives in `plugin.gd`/`editor`; optional runtime modules go in `src/`.
- **Reversible:** resources are registered on enter and removed on exit.
- **Accessible:** plain-text terminal prompts and keyboard-navigable, scrollable guides.
- **Portable:** relative plugin paths, no repository-specific runtime dependencies after initialization.

Inspired by [Atrium](https://github.com/Dragonboon/Atrium) (editor docking), [Trispark](https://github.com/Dragonboon/Trispark) (modular features), and [JigsawG](https://github.com/Dragonboon/JigsawG) (slim entry point and regression tests).

MIT licensed. This repository is a **template**, not a published runtime dependency.
