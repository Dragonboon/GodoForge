# How to add a tool command in Godot 4.7

**Use when:** you need a one-shot editor operation (a generator, validator or import action) rather than a permanent dock.

## File to change

- `addons/my_plugin/plugin.gd`

```gdscript
@tool
extends EditorPlugin

const ACTION := "MyPlugin: Validate Scene"

func _enter_tree() -> void:
    add_tool_menu_item(ACTION, _validate_scene)

func _exit_tree() -> void:
    remove_tool_menu_item(ACTION)

func _validate_scene() -> void:
    var root := get_editor_interface().get_edited_scene_root()
    if root == null:
        push_warning("Open a scene before running this tool.")
        return
    print("Validating scene: ", root.name)
```

**Behavior:** no UI is registered until you opt into this recipe. Nothing changes in the edited scene; this is a safe pattern you can extend.

## Verify

1. Enable the plugin and find **MyPlugin: Validate Scene** under **Project > Tools**.
2. Trigger it with and without a scene open; confirm a clear message.
3. Disable the plugin and verify the menu item disappears.

Reference: [EditorPlugin methods](https://docs.godotengine.org/en/4.7/classes/class_editorplugin.html).
