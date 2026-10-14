extends SceneTree

func _initialize() -> void:
	var config := ConfigFile.new()
	if config.load("res://addons/my_plugin/plugin.cfg") != OK:
		fail("missing plugin manifest")
		return
	if config.get_value("plugin", "script", "") != "plugin.gd":
		fail("incorrect plugin script")
		return
	var script: Script = load("res://addons/my_plugin/plugin.gd")
	if script == null or not script.can_instantiate():
		fail("plugin script cannot instantiate")
		return
	if script.get_instance_base_type() != "EditorPlugin":
		fail("plugin must extend EditorPlugin")
		return
	print("PASS: plugin smoke")
	quit(0)


func fail(message: String) -> void:
	push_error(message)
	quit(1)
