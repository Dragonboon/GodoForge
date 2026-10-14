@tool
extends EditorPlugin

## Set to false or remove the example UI when developing runtime-only addons.
const ENABLE_EXAMPLE_DOCK := true
const ExampleDockScript = preload("editor/example_dock.gd")

var _example_dock: EditorDock


func _enter_tree() -> void:
	if not ENABLE_EXAMPLE_DOCK:
		return

	_example_dock = EditorDock.new()
	_example_dock.name = "MyPluginExampleDock"
	_example_dock.title = "My Plugin"
	_example_dock.layout_key = "my_plugin_example_dock"
	_example_dock.default_slot = EditorDock.DOCK_SLOT_RIGHT_UL
	_example_dock.available_layouts = EditorDock.DOCK_LAYOUT_ALL
	_example_dock.add_child(ExampleDockScript.new())
	add_dock(_example_dock)


func _exit_tree() -> void:
	if is_instance_valid(_example_dock):
		remove_dock(_example_dock)
		_example_dock.queue_free()
	_example_dock = null
