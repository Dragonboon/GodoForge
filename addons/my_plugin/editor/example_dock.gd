@tool
extends VBoxContainer

## Small self-contained demo; safe to delete with its registration in plugin.gd.
func _ready() -> void:
	var heading := Label.new()
	heading.text = "My Plugin"
	add_child(heading)

	var hint := Label.new()
	hint.text = "Replace this dock with your editor tools."
	hint.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	add_child(hint)
