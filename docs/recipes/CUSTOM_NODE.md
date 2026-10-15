# How to register a custom node in Godot 4.7

**Use when:** users should create your special node from the **Create Node** dialog.

## Files to create

- `addons/my_plugin/src/my_marker.gd`: the node's behavior.
- `addons/my_plugin/plugin.gd`: editor registration.

### 1. Runtime node: `src/my_marker.gd`

```gdscript
@tool
extends Node2D

@export var label: String = "Marker"
```

### 2. Register the node: `plugin.gd`

```gdscript
@tool
extends EditorPlugin

const Marker = preload("src/my_marker.gd")

func _enter_tree() -> void:
    add_custom_type("MyPluginMarker", "Node2D", Marker, null)

func _exit_tree() -> void:
    remove_custom_type("MyPluginMarker")
```

This registers a script-backed node in the editor. Pick a unique type name to avoid collision with other plugins; it is different from declaring a global `class_name`.

## Verify

1. Enable the plugin and search for **MyPluginMarker** in **Create Node**.
2. Instantiate it, change `label`, save and reopen a scene.
3. Disable the addon and ensure no duplicate type remains in the Create Node list.

Reference: [EditorPlugin.add_custom_type](https://docs.godotengine.org/en/4.7/classes/class_editorplugin.html#class-editorplugin-method-add-custom-type).
