# Developing plugins with this template

## Start without editor UI

The starter contains just `addons/pooling/plugin.cfg` and an intentionally inert `plugin.gd`. Enabling it does **not** add an editor dock, bottom panel, inspector extension, menu or autoload. This keeps the host editor's layout unchanged.

Use the [recipe index](recipes/README.md) when you actually need a feature. Each recipe names its destination file, includes a standalone implementation and cleanup, and ends with a manual verification step. **Don't copy everything:** mix only the features required for your plugin.

## Create your own plugin identity

Run the accessible interactive initializer from a newly generated template repository:

```bash
python3 scripts/init_plugin.py
```

It asks for display name, snake_case ID and author; suggests an ID from the display name; validates input; previews the result; and asks for confirmation. You can disable ANSI colors with `--no-color` or `NO_COLOR=1`. Ctrl+C cancels. No input is requested in automation: use all flags instead.

```bash
python3 scripts/init_plugin.py --id world_tools --name "World Tools" --author "Developer"
```

The script renames `addons/pooling/` and updates the template's docs and smoke tests once. It refuses an existing destination or partial template and does not install packages or modify Godot's UI.

## Choose an addon type

- **Editor tool:** create `@tool` scripts under `addons/<id>/editor/` and register editor features in `plugin.gd`.
- **Runtime library:** put Godot `Node`/`Resource` modules under `addons/<id>/src/`; avoid dependencies on editor-only APIs.
- **Hybrid:** expose runtime APIs under `src/` and keep optional editor integrations behind `EditorPlugin`.

The base plugin intentionally leaves `_enter_tree()` and `_exit_tree()` empty. When adding editor registrations, undo each in `_exit_tree()`: menu items, custom types, docks, inspector plugins and signal connections. Do not register a dock just to show documentation.

## Editor layout recovery

If the earlier learning dock changed your editor layout, **disable the old plugin**, reopen the editor and select **Editor > Editor Layouts > Default** to restore the standard layout. The new starter no longer creates that dock, so it cannot reintroduce it. If you have saved a custom layout, choose your saved layout instead. See [Godot: Customizing the interface](https://docs.godotengine.org/en/4.7/tutorials/editor/customizing_editor.html).

## Compatibility and release

Use Godot 4.7 features only if you target 4.7. The host project's feature declaration is not proof that a feature works in an older version. Test against every supported engine version.

Only `addons/<id>/` belongs in the installable package. Keep documentation, CI, tests, examples and the template host `project.godot` outside it. Test in a fresh consuming project before publishing.
