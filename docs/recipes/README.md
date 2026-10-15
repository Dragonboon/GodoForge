# Godot 4.7 recipes: how to implement X in Y

All recipes are **opt-in documentation**. They do not run on plugin activation, alter the editor layout or ship any UI code in the starter. Paths in examples use `addons/my_plugin/` and are renamed by `scripts/init_plugin.py` when you initialize your copy.

| Feature | Where it belongs | Recipe |
| --- | --- | --- |
| An editor-side custom UI | `plugin.gd` + `editor/` | [Editor dock](EDITOR_DOCK.md) |
| A new custom Create Node type | `plugin.gd` + `src/` | [Custom node](CUSTOM_NODE.md) |
| An Inspector extension | `plugin.gd` + `editor/` | [Inspector plugin](INSPECTOR_PLUGIN.md) |
| A Project > Tools command | `plugin.gd` | [Tools menu](TOOLS_MENU.md) |
| Reusable gameplay configuration | `src/` | [Runtime Resource](RUNTIME_RESOURCE.md) |
| Regression test and publication | `tests/` + release artifact | [Testing and release](TESTING_RELEASE.md) |

Each recipe answers: **When to use it, which files to create, how to implement it, how to undo it, and how to verify it**.

**Composing recipes:** Each editor integration recipe shows a *complete illustrative* `plugin.gd` for clarity. Do not overwrite existing features if combining recipes; merge their `_enter_tree()` and `_exit_tree()` bodies instead. Avoid installing multiple `EditorPlugin` entry scripts for one addon.

Official Godot docs: [Making plugins](https://docs.godotengine.org/en/4.7/tutorials/plugins/editor/making_plugins.html) and [EditorPlugin API](https://docs.godotengine.org/en/4.7/classes/class_editorplugin.html).
