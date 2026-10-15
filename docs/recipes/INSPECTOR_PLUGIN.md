# How to extend the Inspector in Godot 4.7

**Use when:** objects of a certain type need additional Inspector controls.

## Files to create

- `addons/my_plugin/editor/my_inspector.gd`: the editor-only extension.
- `addons/my_plugin/plugin.gd`: registration.

### 1. Inspector extension: `editor/my_inspector.gd`

```gdscript
@tool
extends EditorInspectorPlugin

func _can_handle(object: Object) -> bool:
    return object is Node2D

func _parse_begin(_object: Object) -> void:
    var label := Label.new()
    label.text = "My Plugin: Node2D tools"
    add_custom_control(label)
```

**Note:** this demonstration applies to every Node2D; restrict `_can_handle()` to your own specific script or Resource in a real plugin.

### 2. Register the extension: `plugin.gd`

```gdscript
@tool
extends EditorPlugin

const Inspector = preload("editor/my_inspector.gd")
var _inspector: EditorInspectorPlugin

func _enter_tree() -> void:
    _inspector = Inspector.new()
    add_inspector_plugin(_inspector)

func _exit_tree() -> void:
    if is_instance_valid(_inspector):
        remove_inspector_plugin(_inspector)
        _inspector = null
```

## Verify

1. Enable the plugin, select a Node2D and look for the added label.
2. Select another type and confirm the additional label is absent.
3. Disable and re-enable the plugin; controls must not accumulate.

Reference: [Inspector plugins](https://docs.godotengine.org/en/4.7/tutorials/plugins/editor/inspector_plugins.html).
