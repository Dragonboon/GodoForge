# Development guide

## Choose the right addon type

- **Editor-only tool:** extend `EditorPlugin` in `plugin.gd`; use `@tool` for scripts that run in the editor.
- **Runtime library:** put reusable scripts/resources in `src/`; if you need no editor integration, you may omit `plugin.cfg` and `plugin.gd`.
- **Hybrid:** isolate editor registration in `plugin.gd` and keep runtime modules editor-independent.

## Create a new addon

For a guided terminal setup (colors when supported, clear prompts, validation, default ID and explicit confirmation):

```bash
python3 scripts/init_plugin.py
```

The wizard requests a display name, snake_case ID and author. Press Enter to accept the suggested ID; no files change until you confirm. Use `--no-color` for plain output, or set `NO_COLOR`. Ctrl+C cancels. Non-interactive shells fail safely unless all fields are supplied:

```bash
python3 scripts/init_plugin.py --id world_tools --name "World Tools" --author "Developer"
```

The command changes known template references and renames `addons/my_plugin` **once**; it refuses collisions and never overwrites an existing initialized addon.

## Inside Godot: the optional Plugin Guide dock

Enable the starter plugin in **Project > Project Settings > Plugins** and find **Plugin Guide** in a right-side tab. It contains six offline, selectable tutorials with steps, code to copy, and verification instructions:

1. Editor docks and reversible lifecycle
2. Custom node registration
3. Inspector extensions
4. Tools menu actions
5. Runtime Resource classes
6. Smoke tests and packaging

The content uses a scrollable container with no forced minimum height. Godot 4.7 supports side/floating `EditorDock` placement; this learning panel intentionally excludes bottom placement to avoid competing with Output/Debugger.

To remove the training UI, set `ENABLE_EXAMPLE_DOCK = false` in `plugin.gd`, or delete the demo registration and `editor/example_dock.gd` and `editor/guide_topics.gd`. Keep your own editor tools separate from runtime code.

## Lifecycle and compatibility

Register types, docks, inspector plugins and menu items in `_enter_tree()` and undo registration in `_exit_tree()`. Avoid global `class_name` collisions, silent ProjectSettings writes and network/update features in the basic starter.

**Layout caveat:** an oversized side dock can push the editor bottom panel offscreen in affected 4.7 builds. Do not assign large minimum dimensions to editor panels, and test at a small editor window size as well as after layout restoration. See [Godot issue #121574](https://github.com/godotengine/godot/issues/121574).

## Packaging and release

Ship only `addons/<plugin_id>/`. The template's tests, host `project.godot`, CI and docs are for developers only. Disable and re-enable the plugin repeatedly, install it into a fresh consuming project, run the targeted Godot versions, then tag the verified release.

Official reference: [Godot 4.7 EditorDock](https://docs.godotengine.org/en/4.7/classes/class_editordock.html), [creating editor plugins](https://docs.godotengine.org/en/4.7/tutorials/plugins/editor/making_plugins.html).
