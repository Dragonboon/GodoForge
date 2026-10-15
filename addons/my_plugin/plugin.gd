@tool
extends EditorPlugin

## Starter-only learning UI; disable or remove it for runtime-only addons.
const ENABLE_EXAMPLE_DOCK := true
const ExampleDockScript = preload("editor/example_dock.gd")

var _example_dock: EditorDock


func _enter_tree() -> void:
	if not ENABLE_EXAMPLE_DOCK:
		return

	_example_dock = EditorDock.new()
	_example_dock.name = "MyPluginLearningDock"
	_example_dock.title = "Plugin Guide"
	_example_dock.layout_key = "my_plugin_learning_dock_v2"
	# Keep the developer's Output/Debugger and bottom bar available.
	_example_dock.default_slot = EditorDock.DOCK_SLOT_RIGHT_BR
	_example_dock.available_layouts = EditorDock.DOCK_LAYOUT_VERTICAL | EditorDock.DOCK_LAYOUT_FLOATING
	_example_dock.add_child(ExampleDockScript.new())
	add_dock(_example_dock)


func _exit_tree() -> void:
	if is_instance_valid(_example_dock):
		remove_dock(_example_dock)
		_example_dock.queue_free()
	_example_dock = null
