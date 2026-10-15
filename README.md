<div align="center">

# GodoForge

**Build Godot plugins, not boilerplate.**

A lean, reproducible starter for **Godot 4.7** plugins: interactive setup, optional copy-and-adapt recipes, and automated smoke tests.

[![Godot 4.7](https://img.shields.io/badge/Godot-4.7-478CBF?logo=godotengine&logoColor=white)](https://godotengine.org/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![CI](https://github.com/Dragonboon/GodoForge/actions/workflows/godot-ci.yml/badge.svg)](https://github.com/Dragonboon/GodoForge/actions/workflows/godot-ci.yml)
[![MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Template](https://img.shields.io/badge/GitHub-Template-181717?logo=github)](https://github.com/Dragonboon/GodoForge/generate)

[**Create from template**](https://github.com/Dragonboon/GodoForge/generate) · [Quick start](#quick-start) · [Recipes](#learn-by-building) · [Testing](#quality-and-compatibility) · [Contribute](CONTRIBUTING.md)

</div>

---

## Why GodoForge?

GodoForge helps you ship a **small, modular Godot addon** without designing the scaffolding from scratch. It is a **GitHub repository template**, not a dependency, runtime framework, plugin manager, or code generator that guesses your plugin's features.

- **Start fast:** a keyboard-friendly Python wizard asks for your plugin name, identifier and author, previews changes and requires confirmation.
- **Nothing invasive:** enabling the unmodified starter registers no editor docks, bottom panels, menu items, autoloads or custom types.
- **Learn only what you need:** practical, self-contained GDScript recipes for editor features, runtime code and release testing.
- **Verify as you go:** Python regression tests plus a Godot **4.7.2** headless import and plugin smoke test in GitHub Actions.
- **Publish cleanly:** distribute your `addons/<plugin_id>/` folder, not this development repository.

## Quick start

### 1. Prepare your environment

You'll need **Godot 4.7** (CI tests **4.7.2**), **Python 3.10+** and a GitHub account if you want to use the template button. No Python third-party packages are required. Git is useful for development.

### 2. Create your own repository

Select **[Use this template → Create a new repository](https://github.com/Dragonboon/GodoForge/generate)**, then clone your newly created repository:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Alternatively, download the template sources and work locally. The setup script is intended to run **once** per copy.

### 3. Initialize your plugin

In an interactive terminal:

```bash
python3 scripts/init_plugin.py
```

The wizard asks for a **display name**, **lowercase `snake_case` identifier** and **author**. It suggests an identifier, validates inputs, shows a summary, and only changes files after explicit confirmation. Press **Ctrl+C** to cancel; use `--no-color` or `NO_COLOR=1` if you prefer plain text.

For CI or scripting, supply all arguments (no prompts):

```bash
python3 scripts/init_plugin.py \
  --id world_tools \
  --name "World Tools" \
  --author "Your Name"
```

This renames `addons/my_plugin/` to `addons/world_tools/`, updates known references, and refuses to overwrite an existing addon. The original template remains unchanged; run the initializer **in a newly created repository**, not in the upstream GodoForge repository. After initialization, edit the **generated project's README** to document *your* plugin's features and installation process.

### 4. Open Godot and start developing

Open `project.godot` with Godot and enable the addon under **Project → Project Settings → Plugins**. The starter deliberately changes **nothing** in the editor layout. Choose a recipe below when you want to implement a feature. If Godot says **Missing Project**, select the directory containing the generated `project.godot`, not `addons/`.

## Learn by building

The [recipe library](docs/recipes/README.md) is **documentation, not automatically installed code**. Each guide covers when to use the feature, where to create files, a working GDScript pattern, cleanup and verification.

| I want to… | Read this |
| --- | --- |
| Create a dock for an editor tool | [Editor dock](docs/recipes/EDITOR_DOCK.md) |
| Add a custom node to Create Node | [Custom node](docs/recipes/CUSTOM_NODE.md) |
| Extend the Inspector for a type | [Inspector extension](docs/recipes/INSPECTOR_PLUGIN.md) |
| Run an action from Project → Tools | [Tools menu action](docs/recipes/TOOLS_MENU.md) |
| Define reusable runtime configuration | [Runtime Resource](docs/recipes/RUNTIME_RESOURCE.md) |
| Test, package and release an addon | [Testing & release](docs/recipes/TESTING_RELEASE.md) |

**Combine recipes deliberately:** if multiple examples show `plugin.gd`, merge their registration and cleanup methods instead of replacing existing code. No guide is required for a minimal runtime-only library.

## Repository layout

```text
addons/my_plugin/            # Rename this folder with the initializer
  plugin.cfg                 # Addon metadata read by Godot
  plugin.gd                  # Minimal @tool EditorPlugin lifecycle
docs/
  DEVELOPMENT.md             # Architecture, setup and compatibility notes
  TESTING.md                 # Checks and acceptance criteria
  recipes/                   # Optional how-to guides
scripts/
  init_plugin.py             # Interactive/flag-driven setup; Python stdlib only
  ci/run_tests.py            # Strict headless Godot regression runner
tests/
  test_plugin.gd             # Addon import smoke test
  test_initializer.py        # Wizard and rename tests
  test_recipes.py            # Non-invasive default + documentation integrity
.github/workflows/
  godot-ci.yml               # Pinned Godot 4.7.2 checks
project.godot                # Development host, NOT part of your addon package
```

## Quality and compatibility

Run the same checks as CI:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/ci/run_tests.py --godot godot --timeout 90
```

If Godot isn't on your PATH, use `--godot /absolute/path/to/Godot` (or set `GODOT_BIN`). The runner imports the project headlessly, detects parse/runtime error output and runs Godot smoke tests; it is **not** a substitute for interactive editor checks.

| Area | Supported / verified |
| --- | --- |
| Godot | **4.7** baseline; CI executable pinned to **4.7.2-stable** |
| Language | GDScript for addon examples, Python **3.10+** for initializer/tests |
| Dependencies | Python standard library only |
| Editor integrations | **None by default**; recipes are opt-in |
| Older/newer Godot releases | **Not claimed compatible** until tested |

See [Testing](docs/TESTING.md) for the manual checklist, and [Development](docs/DEVELOPMENT.md) for lifecycle guidance.

## Shipping your addon

Copy or package only `addons/<plugin_id>/` into a consuming Godot project's `addons/` directory. Enable it under **Project → Project Settings → Plugins** if it has editor functionality. Runtime scripts can be used independently where appropriate.

Before publishing, test a clean install using **only the distributable addon folder**, verify enable/disable cleanup, update `plugin.cfg` metadata, choose your own versioning and release notes, and document your tested Godot versions. The setup script, CI, development host and recipe docs are not implicit runtime dependencies.

## Documentation, support and contributing

- [Development guide](docs/DEVELOPMENT.md) · [Test strategy](docs/TESTING.md) · [Recipe index](docs/recipes/README.md)
- [Report an issue](https://github.com/Dragonboon/GodoForge/issues/new/choose) · [Browse issues](https://github.com/Dragonboon/GodoForge/issues)
- [Contribution guide](CONTRIBUTING.md) · [Security policy](SECURITY.md) · [Code of conduct](CODE_OF_CONDUCT.md)
- [Official Godot editor plugin documentation](https://docs.godotengine.org/en/4.7/tutorials/plugins/editor/making_plugins.html)

This template draws on real-world design lessons from [Atrium](https://github.com/Dragonboon/Atrium), [Trispark](https://github.com/Dragonboon/Trispark) and [JigsawG](https://github.com/Dragonboon/JigsawG). These projects are **references, not bundled dependencies**.

**License:** [MIT](LICENSE). You can build and license your resulting addon independently; check the included LICENSE and adjust project attribution as needed.

---

<div align="center">

**GodoForge — a clean starting point, your plugin from here.**

[Create a repository](https://github.com/Dragonboon/GodoForge/generate) · [Explore recipes](docs/recipes/README.md)

</div>
