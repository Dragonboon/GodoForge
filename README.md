# Godot Plugin Template

A **minimal Godot 4.7 plugin starter** with a guided setup CLI, headless checks and practical recipes. [Create a repository from this template](https://github.com/sempitern0/godot-plugin-template/generate).

**This template adds nothing to the Godot editor UI by default.** No sample docks, bottom panels, menus, project settings or autoloads are registered. Enable the plugin in Project Settings to verify its lifecycle, then opt into only the features you want.

## Quick start

1. Install Godot **4.7.2** (or another compatible 4.7 version) and Python 3.10+.
2. Run `python3 scripts/init_plugin.py` from your new repository: the terminal wizard asks for a name, ID and author and confirms the changes before creating your plugin. For automation use:

   ```bash
   python3 scripts/init_plugin.py --id world_tools --name "World Tools" --author "Developer"
   ```

3. Open `project.godot`, enable the plugin under **Project > Project Settings > Plugins**, and choose a [recipe](docs/recipes/README.md) to implement a specific feature.

## How do I implement X in Godot?

The [**recipe index**](docs/recipes/README.md) gives short, independent examples with file locations, GDScript, cleanup and a checklist:

| I want to... | Guide |
| --- | --- |
| Add an editor dock (only when needed) | [Editor dock](docs/recipes/EDITOR_DOCK.md) |
| Register a custom node | [Custom node](docs/recipes/CUSTOM_NODE.md) |
| Extend the Inspector | [Inspector plugin](docs/recipes/INSPECTOR_PLUGIN.md) |
| Add a Project > Tools command | [Tools menu](docs/recipes/TOOLS_MENU.md) |
| Share data with a runtime Resource | [Runtime Resource](docs/recipes/RUNTIME_RESOURCE.md) |
| Add a smoke test and prepare a release | [Testing & release](docs/recipes/TESTING_RELEASE.md) |

These **documentation-only examples** are not installed into the Godot editor or the addon until you copy the relevant snippet.

## Project layout

```text
addons/my_plugin/
  plugin.cfg          # plugin metadata
  plugin.gd           # intentionally empty EditorPlugin lifecycle
docs/
  recipes/            # opt-in "how to implement X" guides
  DEVELOPMENT.md      # design, initialization and lifecycle
  TESTING.md          # automated and manual checks
scripts/
  init_plugin.py      # accessible interactive wizard / CLI
  ci/run_tests.py     # strict Godot headless regression
tests/
  test_plugin.gd      # plugin smoke test
  test_initializer.py # CLI/wizard regression tests
  test_recipes.py     # no UI by default; recipe integrity
```

## Validate

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/ci/run_tests.py --godot godot
```

Distribute **only** `addons/<plugin_id>/` to downstream Godot projects. Neither docs, tests, build scripts nor the host project are required.

## Philosophy

- Minimal by default; examples exist in documentation, not in running code.
- Modular and reversible editor integrations, with cleanup in `_exit_tree()`.
- Editor and runtime logic stay separate; no hidden project mutations.
- Accessible setup: labels, keyboard input, clear errors, `--no-color`/`NO_COLOR`, and explicit confirmation.
- Verified against Godot 4.7.2 in CI; other engine versions require their own compatibility validation.

Design references: [Atrium](https://github.com/Dragonboon/Atrium), [Trispark](https://github.com/Dragonboon/Trispark) and [JigsawG](https://github.com/Dragonboon/JigsawG).

MIT licensed. This repository is a template, not a runtime framework.
