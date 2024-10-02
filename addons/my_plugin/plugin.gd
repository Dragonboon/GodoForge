@tool
extends EditorPlugin


func _enter_tree() -> void:
	MyPluginSettings.set_update_notification()
	
	_setup_updater()
	

func _exit_tree() -> void:
	MyPluginSettings.remove_settings()

## Update tool referenced from https://github.com/MikeSchulze/gdUnit4/blob/master/addons/gdUnit4
func _setup_updater() -> void:
	if MyPluginSettings.is_update_notification_enabled():
		Engine.get_main_loop().root.add_child.call_deferred(preload("updater/update_notify_tool.tscn").instantiate())
