# How to implement an editor dock in Godot 4.7

**Use when:** your plugin actually needs a persistent tool panel. **Not needed** for runtime libraries or simple editor actions. The starter creates no dock by default.

## Files to create

- `addons/pooling/editor/tool_panel.gd`: the dock's Control content.
- `addons/pooling/plugin.gd`: registration and cleanup.

### 1. UI content: `editor/tool_panel.gd`

```gdscript
@tool
extends ScrollContainer

func _ready() -> void:
    custom_minimum_size = Vector2.ZERO
    var content := VBoxContainer.new()
    content.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    add_child(content)

    var title := Label.new()
    title.text = "Pooling Tools"
    content.add_child(title)
```

### 2. Editor registration: `plugin.gd`

```gdscript
@tool
extends EditorPlugin

const ToolPanel = preload("editor/tool_panel.gd")
var _dock: EditorDock

func _enter_tree() -> void:
    _dock = EditorDock.new()
    _dock.name = "PoolingTools"
    _dock.title = "My Tools"
    _dock.layout_key = "pooling_tools"
    _dock.default_slot = EditorDock.DOCK_SLOT_RIGHT_BR
    _dock.available_layouts = EditorDock.DOCK_LAYOUT_VERTICAL | EditorDock.DOCK_LAYOUT_FLOATING
    _dock.add_child(ToolPanel.new())
    add_dock(_dock)

func _exit_tree() -> void:
    if is_instance_valid(_dock):
        remove_dock(_dock)
        _dock.queue_free()
        _dock = null
```

**Why only side/floating?** Keep Output and Debugger accessible, and do not push a large custom UI into the bottom dock. Use scrollable content and avoid large minimum sizes. If you *explicitly* want a bottom dock, Godot 4.7 supports `EditorDock.DOCK_SLOT_BOTTOM` with horizontal layouts; change this only by choice.

## Verify

1. Enable the plugin, open and resize the panel, and check Output/Debugger remain usable.
2. Disable/re-enable; ensure there are no duplicate tabs.
3. Test with a small editor window and restart Godot to verify saved layouts.
4. If a previous sample changed your layout, use **Editor > Editor Layouts > Default** after disabling it.

References: [EditorDock](https://docs.godotengine.org/en/4.7/classes/class_editordock.html), [EditorPlugin](https://docs.godotengine.org/en/4.7/classes/class_editorplugin.html).
