# Development guide

## Choose the right addon type

- **Editor-only tool:** extend `EditorPlugin` in `plugin.gd`; use `@tool` for scripts that run in the editor. The included dock is an optional example.
- **Runtime library:** put reusable gameplay scripts/resources in `src/`, and only use an EditorPlugin if editor registration is needed. A library that requires no editor hooks can omit `plugin.cfg`/`plugin.gd`.
- **Hybrid:** keep editor integration in `plugin.gd` and gameplay features independent of the editor in `src/`.

## Safe plugin lifecycle

Register custom types, inspector plugins, docks and menus in `_enter_tree()`. Unregister each in `_exit_tree()`, disconnect signals you own, free created nodes, and clear references. Restart/disable/re-enable while testing to spot duplicate UI or lingering state.

Godot 4.7's `EditorDock` enables moveable/floating dock UI. It is **an optional pattern**, not a requirement for every addon. Keep the example panel trivial until you need more.

Avoid global `class_name` names for generic template helpers; they conflict with other installed addons. Prefer local preloads and plugin-relative paths. Never write user project settings just by enabling your plugin; prefer explicit opt-in and a reversible cleanup path.

## Create a new addon

Run the initializer **once**:

```bash
python3 scripts/init_plugin.py --id world_tools --name "World Tools" --author "Developer"
```

Identifiers must be lowercase snake_case, and names must be nonempty. The script renames `addons/my_plugin` and replaces the few known template markers, refuses overwrites, and will not run again after initialization. Review the generated `plugin.cfg` and `plugin.gd` before publishing.

The script changes **template identity**, not game code. Replace the demo UI with your implementation, add self-contained modules under `src/`, and add tests for each behavior.

## Packaging

Ship **only** `addons/<plugin_id>/` for normal editor plugins. Keep test suites, standalone example projects, README and automation outside the distributable directory. Declare your verified minimum Godot version in your release notes, and test it; a newer project version in `project.godot` is not a proof of backward compatibility.

## Release checklist

1. Enable/disable the addon repeatedly; verify no orphan docks or errors.
2. Import in a **fresh** Godot project using only `addons/<plugin_id>/`.
3. Run headless checks on the targeted Godot versions.
4. Verify no files or project settings are changed without user action.
5. Tag a release with version, supported Godot versions and changelog.

API: [Creating editor plugins](https://docs.godotengine.org/en/stable/tutorials/plugins/editor/making_plugins.html).
