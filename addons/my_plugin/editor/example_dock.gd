@tool
extends ScrollContainer

## Optional, self-contained learning dock. Scroll instead of forcing editor height.
const GuideTopics = preload("guide_topics.gd")

var _selector: OptionButton
var _goal: Label
var _steps: Label
var _code: TextEdit
var _check: Label
var _feedback: Label


func _ready() -> void:
	custom_minimum_size = Vector2.ZERO
	size_flags_horizontal = Control.SIZE_EXPAND_FILL
	size_flags_vertical = Control.SIZE_EXPAND_FILL
	horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	vertical_scroll_mode = ScrollContainer.SCROLL_MODE_AUTO

	var column := VBoxContainer.new()
	column.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	add_child(column)

	var heading := Label.new()
	heading.text = "Build your first Godot plugin"
	column.add_child(heading)

	var intro := Label.new()
	intro.text = "Pick a recipe. Each example is optional and removable."
	intro.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	column.add_child(intro)

	_selector = OptionButton.new()
	_selector.tooltip_text = "Choose a development recipe with mouse or keyboard."
	_selector.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	for topic: Dictionary in GuideTopics.TOPICS:
		_selector.add_item(topic["title"])
	column.add_child(_selector)
	_selector.item_selected.connect(_show_topic)

	_goal = _paragraph(column)
	_steps = _paragraph(column)
	var code_heading := Label.new()
	code_heading.text = "Example (selectable code)"
	column.add_child(code_heading)

	_code = TextEdit.new()
	_code.editable = false
	_code.wrap_mode = TextEdit.LINE_WRAPPING_BOUNDARY
	_code.scroll_fit_content_height = false
	_code.custom_minimum_size = Vector2(0.0, 160.0)
	_code.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	column.add_child(_code)

	var copy_button := Button.new()
	copy_button.text = "Copy example code"
	copy_button.tooltip_text = "Copy this GDScript snippet to the system clipboard."
	copy_button.pressed.connect(_copy_example)
	column.add_child(copy_button)

	_check = _paragraph(column)
	_feedback = _paragraph(column)
	_feedback.text = "Reference: docs/DEVELOPMENT.md in the template project."
	_show_topic(0)


func _paragraph(parent: Control) -> Label:
	var label := Label.new()
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	parent.add_child(label)
	return label


func _show_topic(index: int) -> void:
	if index < 0 or index >= GuideTopics.TOPICS.size():
		return
	var topic: Dictionary = GuideTopics.TOPICS[index]
	_goal.text = "Goal: " + topic["goal"]
	_steps.text = "Steps:\n" + topic["steps"]
	_code.text = topic["code"]
	_check.text = "Verify: " + topic["verify"]


func _copy_example() -> void:
	DisplayServer.clipboard_set(_code.text)
	_feedback.text = "Example copied. Paste into the script described in the steps."
